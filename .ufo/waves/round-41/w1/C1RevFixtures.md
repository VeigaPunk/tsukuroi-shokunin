VERDICT: supports

Item C1-8 — review of the four round-41 selftest cases (`grep -n 'R41-C1' tools/tsukuroi-census.sh` → lines 3042, 3048, 3054, 3061), lane tip 71851d636ab1bffaf8fee5016617c88878a666f1. Review time working tree: 10 dirty entries (`git status --porcelain`), none in tools/tsukuroi-census.sh or tools/score-selftest-mounts-r41.py; the census file is byte-identical at the implementation commit (568c397d), HEAD, and in the tree I read (`git log --oneline 568c397d..HEAD -- tools/tsukuroi-census.sh` and `git diff --stat 568c397d HEAD -- tools/tsukuroi-census.sh` both empty).

## A. The cases run green at tip, and cannot pass for a host-read reason

- One census selftest run at tip (TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/C1RevFixtures): rc=0, `TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)`; the four cases PASS at receipt lines 123-126 (receipt `selftest-r41.log`, seat dir). 37.35 s wall.
- No vacuous pass: `check()` re-invokes the census with per-case overrides `TSUKUROI_BTRFS_SYSFS="$FX/btrfs"` (census:2165) and `TSUKUROI_PROC_MOUNTS="$FX/mounts"` (census:2166) and refuses any output without `host=fixture-host` (census:2175). The live host table (4 btrfs lines, below) cannot satisfy these cases.
- Implementation commit touches cases only: `git show 568c397d --stat` = `tools/tsukuroi-census.sh | 27 +++++++`, 0 deletions; grep of the commit diff for `probe_storage_arm|PROC_MOUNTS|BTRFS_SYSFS` returns no matches — `probe_storage_arm` unchanged, as declared.

## B. Mount-line syntax — all four valid

/proc/self/mounts lines are 6 whitespace-separated fields with specials octal-escaped (fields here contain none). Checked token by token (census:3040-3041, 3046-3047, 3052-3053, 3058-3060): every line is `source mountpoint fstype opts dump pass` with `0 0` finals; H6's `UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8` is 8-4-4-4-12 hex, valid. All four files end with newline and `read -r _src _mp fst _rest` (census:1912) splits them correctly.

## C. Kernel producibility — 2 realistic, 2 deliberate counterexamples, 1 vintage note

1. **H5 `relative/mnt` mountpoint (census:3041): NOT kernel-producible.** The kernel renders the mountpoint from the mount-namespace root: fs/proc_namespace.c:117-118 (master, accessed 2026-10-26, https://raw.githubusercontent.com/torvalds/linux/master/fs/proc_namespace.c) — comment "mountpoints outside of chroot jail will give SEQ_SKIP on this", then `err = seq_path_root(m, &mnt_path, &p->root, " \t\n\\");` — output is always absolute. The line is syntactically valid, so the census rule still applies to it; it exists solely to kill mutant H5 (`[[ ${_mp:-} == /* ]]` guard, tools/score-selftest-mounts-r41.py:98-99), which every kernel-producible table would satisfy and thus survive. Acceptable as a counterexample; not a table shape any host can present.
2. **H6 `UUID=…` source on a btrfs line (census:3047): NOT kernel-producible for btrfs.** btrfs overrides the source field with the latest device's name: fs/btrfs/super.c:2405-2415 (master, accessed 2026-10-26), `seq_escape(m, btrfs_dev_name(fs_info->fs_devices->latest_dev), " \t\n\\");` — always a device path. A literal `UUID=` source can only appear for filesystems that echo the raw userspace source string (e.g. FUSE `fsname=`), never for btrfs — so the item's "can appear for some filesystems" holds only for those, not for this fixture's fstype. Live sample: `grep -c 'UUID=' /proc/self/mounts` → `0` (accessed 2026-10-26). Same status as H5: valid-line counterexample aimed at the `_src == /dev/*` guard (counter lines 100-101). No kernel-producible btrfs source outside /dev exists, so this is the only kind of table that kills that mutant.
3. **H9 no `subvol=` option (census:3053): kernel-producible only on old kernels.** v3.10's `btrfs_show_options` prints mount options only — no subvolid/subvol display anywhere in the function (fs/btrfs/super.c:881-945, v3.10, accessed 2026-10-26); v4.19 prints `,subvolid=%llu` + `,subvol=` unconditionally (super.c:1363-1366, v4.19, accessed 2026-10-26); master prints `subvolid=` unconditionally and `subvol=` unless name resolution fails (super.c:1142-1148). So the item's "btrfs without subvol= appears on older kernels" is correct for the pre-display era (≤3.x), and `rw,commit=60` with no subvol matches that shape; current kernels always add at least `subvolid=`. Expectation still rule-correct (options are never inspected).
4. **H10 two btrfs lines (census:3058-3060): normal subvolume layout, fully realistic.** Live host sample (accessed 2026-10-26): `awk '$3=="btrfs"' /proc/self/mounts | wc -l` → `4`, one device `/dev/mapper/root` with subvolid=256/257/258/259, subvol=/@ /@home /@log /@pkg — same shape as the fixture (one device, two subvolumes, non-btrfs lines interleaved).

## D. Expected STORAGE lines match the round-39 rule exactly

Rule (census:364-369): a root with no fsid entry reads HEALTHY 0/0/0 only when the table lists no btrfs mount; with one, `BLOCKED detail=mounts:btrfs-without-sysfs`. Implementation: fsn=0 with `fx_default` (census:2022-2061 — it creates no `$FX/btrfs`; its default table is the ext4-root one at census:2034-2035); each case's table has ≥1 line with fstype field exactly `btrfs` → counted at census:1913, `blocked=1; detail+='mounts:btrfs-without-sysfs,'` at census:1915; state=BLOCKED precedes DEGRADED (census:1919-1921); grammar at census:1922-1923 composes `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` (trailing comma stripped). All four expected regexes (census:3043, 3049, 3055, 3062) are exactly that string, and H10's mt=2 collapses to the same detail (no count is printed) — the expectation is correct, not accidentally so. All four PASS in the run under A.

## E. Novelty — each case tests a shape no round-39/40 table varies

Round-39/40 btrfs lines: `/dev/mapper/root / …subvol=/@` (census:2978), `/dev/nvme0n1p3 /home …subvol=/` (census:3012-3014), `/dev/sda2 /var/lib/machines …subvol=/machines` (census:3020-3021). Shared shape: absolute mountpoint, `/dev*` source, `subvol=` in options, exactly one btrfs line per table. Therefore:
- H5 kills `mt-count requires absolute mountpoint` (counter:98-99) — no prior table has a relative mountpoint.
- H6 kills `mt-count requires /dev/* source` (counter:100-101) — every prior btrfs source is `/dev/…` (the round-40 `UUID=0b1c` at census:3020 sits on a vfat line).
- H9 kills `keyed *'subvol='*` (counter:102, keyed() at counter:81-82) — no prior table lacks `subvol=`; this fixture additionally re-kills M8 (`*'subvol=/@'*`, counter line in MUTANTS list) for free.
- H10 kills `-eq 1` count direction (counter:103) — every prior table has exactly one btrfs line, so `mt -eq 1` was indistinguishable from `mt -gt 0` until a second line appeared.

No case repeats a round-40 shape, and no case has a wrong expectation.

## Findings

1. (Non-blocking, realism caveat) H5 and H6 pin census behavior on inputs the kernel cannot produce as btrfs lines (relative mountpoint: /proc_namespace.c:117-118; UUID= source: super.c:2405-2415). They are the only possible counterexamples to their over-strict mutants, and the round-39 rule prescribes fstype-field-only counting, so the expectations are right — but neither case is evidence about real host tables, and the report of H5/H6-as-mutant-kills should not be read as covering a producible shape.
2. (Non-blocking, vintage) H9's no-subvol shape is old-kernel output only (verified absent from display in v3.10, unconditional in v4.19+); a live modern host shows `subvolid=` on every btrfs line. Fine as declared ("older kernels"); worth keeping the era qualifier in any prose that cites it.
3. No tooling installed or updated this run. Scratch /fast/scratch/hyaku/tsukuroi-r41/C1RevFixtures removed after receipts were copied to the seat dir.

## What I did not do

I did not run tools/score-selftest-mounts-r41.py (the 13-mutant counter) — the kill claims in §E are established by reading the mutant replacement bodies against the case fixtures, not by a counter run; the counter has its own seat. I did not attempt a real btrfs mount to reproduce H9's shape empirically (loop-device setup is host-global /dev state, out of bounds); the v3.10/v4.19/master source comparison stands in for it. Kernel citations are master/v4.19/v3.10 as fetched 2026-10-26; the host runs 7.2.11-arch1-1, whose exact btrfs/proc source I did not fetch.

Receipts: .ufo/waves/round-41/w1/C1RevFixtures/{selftest-r41.log, proc_namespace.c, btrfs-super.c, btrfs-super-v4.19.c, btrfs-super-v3.10.c}.
