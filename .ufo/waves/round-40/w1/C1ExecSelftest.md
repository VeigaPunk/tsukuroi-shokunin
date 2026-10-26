VERDICT: supports

# C1ExecSelftest — C1-2: census `--selftest` at lane tip f951f28

Lane tip at dispatch and at every run below: `f951f288483c1af0cef4afd458488b84cf7a2165`
(`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD`). No lane file was
created or modified; all work in `/fast/scratch/hyaku/tsukuroi-r40/C1ExecSelftest/`, removed at
the end. No package/service/mount/sysfs/host change; no sudo; no signal sent to any process.

## 1. Export and identity

```
git -C <lane> show f951f288483c1af0cef4afd458488b84cf7a2165:tools/tsukuroi-census.sh > $S/c.sh
sha256sum $S/c.sh <lane>/tools/tsukuroi-census.sh
032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733  c.sh
032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733  tools/tsukuroi-census.sh
```
Exported copy is byte-identical to the lane file at tip (3149 lines). Base export
`53b294a274656be6479aadf2ec2fee890ded77ce:tools/tsukuroi-census.sh` = `432cd5834a2de1ab…`.

Base→tip diff of the census is **one hunk, pure addition**: `36 0 tools/tsukuroi-census.sh`
(`git diff --numstat`), hunk `@@ -3006,6 +3006,42 @@`, i.e. inside `run_selftest()`
(1928–3055). Therefore the live census path is unchanged: `probe_storage_arm()` extracted
from base and tip both hash `71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56`
(61 lines) — this independently confirms the claim's "probe_storage_arm is NOT changed".

## 2. Selftest at tip — two runs, cwd `/`, TMPDIR=$S/t

| run | command | result | wall |
|---|---|---|---|
| 1 | `cd / && TMPDIR=$S/t bash $S/c.sh --selftest` | exit 0, `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` | 19 501 ms |
| 2 | same | exit 0, `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` | 21 422 ms |

`cmp st1.out st2.out` → **IDENTICAL** (byte-for-byte over all 124 case lines + summary), so the
result is deterministic, not a lucky ordering. Receipts: `st1.out` (whole run), `SHA256SUMS`.

## 3. The five new R40-C1 cases — each prints PASS

`grep -n 'R40-C1' st1.out` gives exactly five lines:

```
119:PASS healthy rollup: a btrfs /home on another device and options, not last, is BLOCKED (R40-C1) (exit 0, HEALTHY)
120:PASS healthy rollup: one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1) (exit 0, HEALTHY)
121:PASS healthy: btrfs in the device, mountpoint or options of an ext4 line is no btrfs mount (R40-C1) (exit 0, HEALTHY)
122:PASS healthy: the fstype match is exact, so BTRFS is not btrfs (R40-C1) (exit 0, HEALTHY)
123:PASS healthy rollup: an unlistable root keeps its one reason; the mount table is never added (R40-C1) (exit 0, HEALTHY)
```

Source lines: `tools/tsukuroi-census.sh:3011-3043` (tip). All five are in the run; none skipped,
none marked SKIP. The five fixtures do what the claim says, read at source:

- `storage-mounts-varied-home` (`:3011-3016`) — btrfs is **line 2 of 3** (not last), device
  `/dev/nvme0n1p3`, mountpoint `/home`, long option list incl. `space_cache=v2,subvolid=5,subvol=/`.
- `storage-mounts-varied-multi` (`:3018-3024`) — **line 3 of 4**, read-only
  (`ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines`), device `/dev/sda2`, plus a
  `UUID=` device line and a sysfs/vfat line: device, mountpoint, options, subvolume and position
  all vary from the R39 fixture.
- `storage-mounts-btrfs-in-path` (`:3026-3030`) — `btrfs` appears in device
  (`/dev/disk/by-label/btrfs-old`), mountpoint (`/mnt/btrfs-backup`) **and** options
  (`comment=btrfs`) of an **ext4** line; expects HEALTHY 0/0/0, i.e. literals outside the fstype
  field must not count.
- `storage-mounts-fstype-case` (`:3032-3035`) — `BTRFS` uppercase in field 4; expects HEALTHY
  (exact match, not case-folded).
- `storage-root-unreadable-mounted` (`:3037-3043`) — root `chmod 000` **with** a btrfs mount
  listed; expects `detail=root:unreadable` only, i.e. the mount table is never consulted when the
  root is unreadable (guard arm).

Base comparison: `bash base.sh --selftest` → `PASS (119 cases, 119 passed, 0 failed)`, exit 0,
27 664 ms, `grep -c 'R40-C1'` = **0**. Tip 124 − base 119 = **exactly +5**, matching the claim
and the one-hunk/36-line addition.

## 4. Load-bearing spot check (my own, independent of the frozen counter)

Two single-edit mutants of the tip census in scratch (exact-substring replacements, `edit` tool,
never the lane file), each run with `--selftest`:

| mutant | edit | result | failing cases |
|---|---|---|---|
| mut1 — literal-keyed arm | `:1913` `[ "${fst:-}" = btrfs ]` → `[[ "$_src $_mp $_rest" == *btrfs* ]]` (btrfs anywhere in the line counts) | `FAIL (124 cases, 119 passed, 5 failed)`, 34 667 ms | 2 pre-existing R39-C1 + **3 new**: varied-home, varied-multi, btrfs-in-path |
| mut2 — position monoculture | `:1914` `done <<< "$mtab"` → `done <<< "$(printf '%s\n' "$mtab" \| tail -n 1)"` (only the last line scanned) | `FAIL (124 cases, 122 passed, 2 failed)`, 36 513 ms | **only new**: varied-home, varied-multi |

mut2 matters most: a last-line-only scan is caught **exclusively** by the new R40 fixtures, so
that defect class would have survived the pre-round-40 selftest — the fixtures are load-bearing,
not decorative. mut1 shows the "btrfs in device/mountpoint/options" case failing as designed.
Full FAIL text: `mut1-fail.txt`, `mut2-fail.txt`.

## 5. Live census at tip vs base (same host, same minute, read-only)

Both run from cwd `/` with `TMPDIR=$S/t`, tip first then base, 4 s apart:

- tip: `tsukuroi-census census-v2 — host=plazir27 — 2026-10-26T07:15:36Z — read-only`,
  **4 118 ms, exit 1**
- base: `… 2026-10-26T07:15:40Z …`, **4 000 ms, exit 1**
- exit 1 on both = `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` — the census's contractual non-healthy exit, identical at both revisions; it is not an error.

Counts: **6 `PLANE` lines** (packages, systemd, drivers, journal, update-safety, oom) and
**1 `STORAGE` line**, in both runs (plus the 2 `HANDOFF ADJ-04`, 1 `DRIFT pacnew-plane` lines).

`STORAGE` line — **byte-identical** in both runs:
```
STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
```

`diff` of all `PLANE`+`STORAGE` lines tip vs base: **one differing line, `PLANE drivers`**, and
only in four live gauges that measure kernel state at the instant of the run —
`C5_pswp 6896/158373` (tip) vs `6900/158373` (base), `C6_psi_full_total_us 11404372` vs
`11411173`, `C6_avail_kb 19713868` vs 19591084, `C6_shmem_kb 19552` vs 19540. Every verdict and
every static field on all six planes is identical (`packages=DEGRADED`, `systemd=HEALTHY`,
`drivers=DEGRADED`, `journal=DEGRADED`, `update-safety=DEGRADED`, `oom=DEGRADED`), and a whole-body
`diff` (header timestamp excluded) shows no other difference. So the six PLANE lines and the
STORAGE line match the base census's live run; the field-level caveat is stated rather than
papered over: **exact byte equality of `PLANE drivers` is not attainable** between two runs
seconds apart because those four fields are live counters. This is not divergence — the base→tip
code change is confined to `run_selftest()` (§1) and `probe_storage_arm()` is byte-identical.

Receipts: `live-tip.out`, `live-base.out`, `live-tip-planes.txt`, `live-base-planes.txt`.

## 6. Timing / cost

Selftest at tip 19.5 s and 21.4 s; base 27.7 s; mutants 34.7 s and 36.5 s (all single-job here,
no `--jobs` flag — the selftest itself uses a handful of CPUs as documented); live census 4.1 s.
Total seat wall ≈ 3 min. No concurrency pressure beyond the default selftest fan-out.

## 7. Not done / residual risk

- Not run: the frozen counter `tools/score-selftest-literals-r40.py` (13 selftests, 9 mutants,
  N1–N3, selfref) — C1-1's item, not this seat's; I did not duplicate it.
- Also not done: the counter against the after receipt
  `.ufo/waves/round-40/after/c1-after-c707e35.jsonl` (same reason).
- Not assessed: the `chmod 000` guard fixture under **uid 0**. My runs were uid 1000
  (`id -u` → 1000) and all five new cases pass; as root, `chmod 000` does not deny listing, so
  `storage-root-unreadable-mounted` (`:3041`) would flip to the mounts-match branch. This pattern
  is **inherited**, not introduced: base already has `chmod 000 "$FX/btrfs"` at `:2972`
  (`storage-mounts-unreadable`, R39). Recorded as a latent constraint (selftest expects a
  non-root uid), not a round-40 defect.
- Tooling: nothing installed or upgraded; no package transaction attempted (pacman paused).
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1ExecSelftest/` removed after copying receipts; the
  selftest left no residue in `$TMPDIR` (`find $S/t -maxdepth 1 | wc -l` → 1, the dir itself).

## Receipts

`.ufo/waves/round-40/w1/C1ExecSelftest/`: `st1.out` (tip pass, all 124 cases), `st-base.out`
(119-case base run), `live-tip.out`, `live-base.out`, `live-tip-planes.txt`,
`live-base-planes.txt`, `mut1.out` + `mut1-fail.txt`, `mut2.out` + `mut2-fail.txt`, `SHA256SUMS`.
