# R70 w1 — E1XfsArm: C2 census XFS arm draft (corrected after R2 attack review)

Base: lane HEAD `84e013a732d7526d08064c6823858d602029ecd7` (`tools/tsukuroi-census.sh`
sha256 `21b0eba3d8ccad1c351720b9b18f63655a231e550a0ad3f566dd9bd6ef37ff46`, clean).
Declaration read at `1710bd74` (Round 70 C2, `xfs-stats-arm`). Sandbox:
`/fast/scratch/hyaku/tsukuroi-r70/E1XfsArm/clone` (re-created from lane HEAD; verified
`--show-toplevel`).

## Deliverable

`probes/E1XfsArm/r70-xfs-arm.diff` — 273 insertions, 0 deletions, one file
(`tools/tsukuroi-census.sh`), sha256
`003cf0d5a98e39d7411bc5f39b8cde220f54218afd3f21192ed8793e8637f1ad`.
`git apply --check` passes on a fresh `--shared` clone of the lane HEAD; the applied file
sha256 equals the sandbox file (`apply-check.txt`). The L1 applies it; nothing in the lane tree
was written. Superseded drafts: `88d94bc8…` (R2-reviewed) and `cb147b10…` (first cut).

## Behavior

`probe_xfs_arm` prints exactly one line after the KERNEL printf and before the rollup:

`XFS xfs-stats mounts=<n> present=<n> absent=<n> unreadable=<n> stats=<n> error=<n> log=<n> detail=<none|token,...>`

- `mounts`: distinct xfs sources from `PROC_MOUNTS` (`TSUKUROI_PROC_MOUNTS`). Only a readable,
  non-empty regular file is a mount table; a FIFO, directory, empty file or failing cat names
  `mounts:unreadable` and leaves every count 0.
- `present`/`absent`/`unreadable`: the sysfs tri-state of each distinct source's
  `/sys/fs/xfs/<basename>` (`XFS_SYSFS`/`TSUKUROI_XFS_SYSFS`); the three sum to `mounts`.
  Present = existing readable searchable directory. Missing entry = absent + `sysfs:absent`.
  Existing but unlistable entry, non-directory entry, or an unlistable sysfs root = unreadable +
  `sysfs:unreadable` (never absent). A source basename outside `^[A-Za-z0-9._:-]+$` is never
  echoed, never used to build a path, counts absent and names `echo:bad-name`.
- `stats`: present filesystems whose `stats/stats` is a readable regular file (FIFO/special is
  never opened) and whose FIRST line matches `^[a-z][a-z0-9_]*([ ][0-9]+)+$`. Malformed first
  line = `stats:malformed`; missing/unreadable/non-regular = `stats:unreadable`.
- `error`, `log`: readable regular files anywhere under `error/` and `log/`, enumerated with
  `find <dir> -type f -readable -printf 'x'` (GNU find, default `-P`): dot files Included;
  symlink entries are type `l` and never count; symlinked directories are never descended;
  nothing is opened. Directories, FIFOs and unreadable entries never count.
- `detail` is always printed and reads `none` when empty; each token once, in encounter order,
  all from the closed vocabulary. No rollup term, PLANE text or exit-code path is touched.
- No write, no privilege, no package transaction, no external xfs tool (no findmnt/xfs_info/
  xfs_spaceman, no `/proc/fs/xfs/stat`), and the write-only clear files, error values and log
  values are never read.

## Corrections after the R2 attack review (disclosed, not hidden)

R2Reviewer-4 reproduced two enumeration defects in the `88d94bc8` draft:
(a) a hidden regular file under `error/`/`log/` was omitted (the glob `*` skipped dot files);
(b) a symlink whose target is a regular file was counted as a regular file (`-f` follows).
Both are fixed by the `find -P -type f -readable` enumeration above, each pinned by a new
hermetic case (`xfs-hidden-dotfiles` expects error=3 log=3; `xfs-symlink-not-regular` expects
error=4 log=2 with a real file, a real nested dir, a file symlink and a dir symlink present).
The reviewer also flagged that the `88d94bc8` fixture WROTE files named with operator-owned
control names inside the scratch fixture. No host path was touched, but that crossed the
letter of the prohibition; the corrected fixture writes no such name (grep of the patch for
`stats_clear|fail_at_unmount|max_retries` = 0) and the arm still only reads `stats/stats`,
first lines and directory entry types. Live counts are unchanged by the fix.

## Retained evidence (`probes/E1XfsArm/`)

- `selftest-full.txt`: `TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)`
  rc 0; 18 PASS lines carry `(R70-C2)` (16 fixture cases + 2 neutrality assertions; baseline
  196). Required shapes: healthy two-fs, absent sysfs, unreadable stats, malformed first line,
  FIFO stats (no block), escaped-space source plus embedded forged line, global stats dir not a
  filesystem, zero xfs mounts, unreadable mount table, A/B rollup/exit neutrality; plus dedupe,
  per-fs and root-level unreadable, non-directory entry, first-line-only, hidden dot files,
  symlink non-counting.
- `live-census.txt` / `live-xfs-line.txt`: exactly one live line,
  `XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`
  (10 whitespace fields, every field once in contract order), live rc 1.
- `findmnt-at-live.txt`: `findmnt -t xfs` distinct sources = 2; mount-table distinct xfs
  sources = 2.
- `enumeration-at-live.txt`: per fs error readable 9, log readable 4; totals error 18, log 8;
  both stats first lines match the frozen regex; 2 readable stats files.
- `neutrality-and-fields.txt`: rollup line byte-identical to
  `before/census-live-base.txt`; live rc 1; selftest summary; label/probe counts; prohibited
  fixture name count 0.
- `apply-check.txt`, `r70-xfs-arm.diff.sha256`.

## Risks and limits (named, not hidden)

1. The declaration prose says "error subtree 7 regular files per fs"; the declaration's own
   `before/host.txt` lists 9 per fs and the live tree has 9 readable regular files per fs
   (18 total, `log` 8). The arm follows the frozen predicate's "enumerated regular-file
   counts"; R2Reviewer-4 independently enumerated 9 per fs. Expected live `error=18`, not 14.
2. `unreadable` counts the sysfs tri-state only; an unreadable stats file is named by
   `stats:unreadable` without incrementing it, so `present+absent+unreadable == mounts` stays
   exact. Stated in the header contract and pinned by tests.
3. Sources that are not device basenames (`UUID=`, `LABEL=`, `/dev/mapper/<name>`) cannot be
   mapped to a sysfs device name without blkid; they read absent (`sysfs:absent`), or
   `echo:bad-name` when the basename fails the validated shape. Honest mapping failure, never a
   guessed device.
4. The enumeration now depends on GNU `find` (`-printf`, `-readable`); the script already uses
   `find -printf` in its selftest hash, and the host is GNU findutils. `find -P` does not follow
   symlinks, so no loop and no symlink double count.
5. No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/tsukuroi-r70/E1XfsArm` is
   deleted before yield.
