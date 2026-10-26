VERDICT: supports

Item C1-10 — sysfs-not-mounted scenario. Hypothesis held byte-exactly in a private
`unshare -rm` namespace where sysfs is *entirely absent from the namespace* (tmpfs over
`/sys`) while `/proc/self/mounts` still lists btrfs: the implementation blob at
`49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` printed `state=BLOCKED … detail=mounts:btrfs-without-sysfs`
and the base blob at `0eff65b21bb81195ee06c96a83afbd7a07e52eef` printed `state=HEALTHY filesystems=0
devices=0 nonzero=0`. Both revisions still emitted all six `PLANE` lines, exactly one `STORAGE`
line and exactly one rollup line, with empty stderr.

Receipts: `.ufo/waves/round-39/w1/C1LabratSysUnmounted/`
(`00-environment.txt`, `01-storage-lines-by-leg.txt`, `L0…L6*.out`, `L1-ns-facts-and-counts.txt`,
`L7-selftest.tail.txt`, `scripts/`). Scratch used and removed:
`/fast/scratch/hyaku/tsukuroi-r39/C1LabratSysUnmounted/` (`TMPDIR` set there for every run).

## Method

Census blobs were extracted from the lane object store into scratch — never written in the lane:
`git show 49cc53c7…:tools/tsukuroi-census.sh` → `census-impl.sh`
(sha256 `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d`, 3098 lines);
`git show 0eff65b2…:tools/tsukuroi-census.sh` → `census-base.sh`
(sha256 `6a675a4e06939e451bb6d1f7eb50f783b61c435e0d9d1efc983a0c7dfc81c33d`, 3054 lines)
(`C1LabratSysUnmounted/00-environment.txt`). Each leg ran both blobs under identical inputs.
No host mutation: the only mount is `mount -t tmpfs t /sys` **inside** `unshare -rm`; no sudo, no
pacman (host-wide pause honoured), no package/service/sysfs change, no tool installed, nothing
written in the lane outside this report and its receipt dir.

Arm under test: `probe_storage_arm` at `tools/tsukuroi-census.sh:1862` (impl blob), the round-39
guard at `:1903-1914`, state/emission at `:1915-1918`, call site `:3077-3078`; overrides
`BTRFS_SYSFS`/`PROC_MOUNTS` at `:459-460`, contract text at `:363-370`. Base blob: same function at
`:1855`, state at `:1896`, emission at `:1898` — the base storage arm contains **zero** occurrences
of `PROC_MOUNTS` and zero occurrences of `mount` (observed: `grep -c PROC_MOUNTS census-base.sh` → `0`;
`sed -n '1855,1905p' … | grep -c mount` → `0`), i.e. structurally incapable of the round-39 read.

## L1 — primary scenario: `mount -t tmpfs t /sys` inside `unshare -rm`

In-namespace facts (`C1LabratSysUnmounted/L1-ns-facts-and-counts.txt`, command
`unshare -rm bash …/facts.sh …`):

```
uid=0 sys_dir_readable=yes
sys_top_level_entries=''                 # tmpfs is empty: /sys/fs does not exist at all
test -d /sys/fs/btrfs: false
test -e /sys/fs/btrfs: false
grep -c ' btrfs ' /proc/self/mounts: 4
btrfs mount entries:
  /dev/mapper/root / btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@ 0 0
  /dev/mapper/root /home btrfs …  /var/cache/pacman/pkg btrfs …  /var/log btrfs …
PLANE-line counts and exit codes:
  impl rc=2 planes=6 TSUKUROI_CENSUS_lines=1 STORAGE_lines=1 :: STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
  base rc=2 planes=6 TSUKUROI_CENSUS_lines=1 STORAGE_lines=1 :: STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0
```

Byte-exact check against the declared claim string (both sides 108 bytes / 74 bytes, no
trailing whitespace or double spaces):

```
declared : STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
observed : STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
→ BYTE-EXACT MATCH
```

This is a stricter shape than the fixtures: not "root present but empty" and not "/sys/fs/btrfs
missing" — `/sys` is replaced wholesale, so `[ -d "$root" ]` is false and the round-39 branch
(`:1903-1914`) is the path that fires. Base printed the silent clean disk from the same namespace,
same table, same second (`L1-ns-tmpfs-over-sys.{impl,base}.out`).

Whole-file A/B between the two revisions in this one namespace — the *only* semantic difference is
the storage line (all other diffs are the timestamp and volatile `C4_sweep`/`C5`/`C6` counters):

```
10c10
< STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0
---
> STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
```

Six-plane question, answered: **yes**, both revisions still emit six `PLANE` lines under a
sysfs-less namespace, in order `packages, systemd, drivers, journal, update-safety, oom`, plus one
rollup — nothing is skipped, suppressed or reordered by the storage arm (it prints after the DRIFT
line, before the rollup, at `:3077-3078`). In this leg `drivers` and `journal` go `BLOCKED` because
the empty `/sys` removes their inputs (`PCI inventory unreadable…`, `boot target prob…`) — honest
fail-closed, not a crash: stderr was 0 bytes in both revisions (`wc -c` → `0`), and the census
completed with a rollup line and rc=2. That collateral is my fixture (an alarmingly empty `/sys`),
not a defect of the storage arm; L2 below isolates it.

## L2 — variant: tmpfs over `/sys/fs` (sysfs present, its `fs` subtree replaced)

`L2-ns-tmpfs-over-sysfs.{impl,base}.out`; facts: `sys_btrfs_dir: absent`,
`ls: cannot access '/sys/fs/btrfs': No such file or directory`, `mounts_btrfs_lines: 4`.
Result: impl `BLOCKED … detail=mounts:btrfs-without-sysfs`, base `HEALTHY filesystems=0 devices=0
nonzero=0`; `planes=6 storage_lines=1` in both. Same verdict with the rest of `/sys` intact — the
guard keys on the btrfs root, not on `/sys` existing.

## L3 — control: absent root and a mount table with no btrfs (no over-blocking)

Override leg, host context, overrides are env-only (`TSUKUROI_BTRFS_SYSFS=<scratch>/emptyroot`,
`TSUKUROI_PROC_MOUNTS=<scratch>/nobtrfs/mounts`, the latter holding `proc /proc proc`,
`tmpfs /run tmpfs`, `ext4 /data ext4`): impl `STORAGE … state=HEALTHY filesystems=0 devices=0
nonzero=0`, base the same, rc=1 for both, rollup unchanged
(`L3-no-btrfs-in-table.{impl,base}.out`). The new arm is conditional, not a blanket BLOCKED.

## L4 — control: absent root and an unreadable mount table

`TSUKUROI_PROC_MOUNTS=<scratch>/unreadable-mounts` (`chmod 000`, contains a btrfs line): impl
`STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable`
(rc=1), base `HEALTHY filesystems=0 devices=0 nonzero=0` (`L4-unreadable-table.{impl,base}.out`).
Declared "an unreadable table gives detail=mounts:unreadable" holds, and the comma-terminated
detail list ends clean (`…unreadable`, no trailing comma — `${detail%,}` at `:1918`).

## L5 — verdict-neutrality (observation, not a claim breach)

Host, live context, only the root is overridden: impl `STORAGE … BLOCKED … detail=mounts:btrfs-without-sysfs`
while the rollup line and exit code are **identical** to the unmodified host run
(`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED
update-safety=DEGRADED oom=DEGRADED)`, rc=1 in both; `diff` of L0 vs L5 excluding `STORAGE` shows
only timestamp and volatile counters). This is the documented contract — header
`:369-370` "The line is verdict-neutral: no PLANE [term]" — so the arm cannot raise the exit code.
Operational consequence for the milestone: in a container-like namespace the *exit status alone
does not distinguish the revisions* (both rc=2 in L1, base because its other planes also blocked);
an operator must read the `STORAGE` line, which is exactly what the round-39 arm exists to make
readable. Not a defect; recorded because C1-10 is judged on operability and a rollup-only consumer
still sees nothing.

## L6 — control: a root with fsid entries never reads the table

Live root, `TSUKUROI_PROC_MOUNTS` pointed at the same `chmod 000` table: impl
`STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`, rc=1
(`L6-root-present-unreadable-table.impl.out`). Unreadable table + populated root → still HEALTHY
1/1/0: the exclusive branch holds, so the new read cannot produce a spurious `mounts:unreadable` on
a healthy host.

## Selftest (implementation blob, scratch TMPDIR)

`bash census-impl.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)`,
rc=0 (`L7-selftest.tail.txt`). The four round-39 cases are at impl blob `:2972-2992`
(`storage-hidden-absent`, `storage-hidden-empty`, `storage-mounts-unreadable`,
`storage-mounted-populated`) and they encode exactly the shapes above; L1 is the first run I know of
that exercises the same branch with a real kernel mount namespace rather than the fixture tree.

## Residuals (honest limits, outside the declared predicate)

1. The guard is only as good as the namespace's own mount table. A namespace that hides *both*
   sysfs and the btrfs mounts still reads `HEALTHY 0/0/0` — L3 is that code path with a fixture
   table. The declared claim is explicitly conditioned on "the mount table … lists a btrfs mount",
   so this is scope, not a defect; it is worth one sentence wherever the arm's reach is documented.
2. `PROC_MOUNTS` parsing relies on `/proc/*/mounts` field 3 being the fstype and on octal-escaping
   of spaces in mount points (impl `:1907-1909`); a hand-written table with a tab-separated fstype
   at field 3 would be counted, which is fine, and a line with fewer than three fields is ignored
   (`fst` empty). No forgery vector found: fields are read, never echoed, into the one-line grammar.
3. `detail=` is comma-joined and `mounts:*` reasons are appended last; a host firing both
   `root:unreadable` and `mounts:*` is impossible (the mounts read is inside the `fsn=0 && blocked=0`
   guard, `:1903`), so the grammar cannot carry two contradictory reasons.

## Not done

No counter run (`tools/score-storage-hidden-r39.py` is the frozen counter's job — the parent owns
post-integration gates); no mutation testing; no `--sample` sweep; no review of the C2 corpus rows
(not my item, so no `TO<n>:` lines); no verification of the IN-109 anchor repin. No tool was
installed or upgraded.
