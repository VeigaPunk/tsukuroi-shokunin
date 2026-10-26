VERDICT: supports

# C1-12 — live real-surface check of the storage arm

Item: run the census arm against the real `/sys/fs/btrfs`, confirm the STORAGE fields equal
what the sysfs files carry, confirm the files are world-readable, and report whether
`btrfs device stats /` works without root. Read-only; no sudo, no host mutation, no installs.

Result: the arm's live line is
`STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`
and it is exactly what the files show (one fsid dir, one devinfo device, five zero counters).
The files are world-readable (0444 file under 0755 dirs) and were read as uid 1000.
`btrfs device stats /` **does** work without root here (rc=0, empty stderr) — no error to report.

## 1. Revision under test

- Lane HEAD `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`; `git diff --quiet
  52ffd65f868431f021b8615ab281efd87195eac6 HEAD -- tools/tsukuroi-census.sh` → "census bytes
  identical to impl commit", and `git merge-base --is-ancestor` confirms the impl commit is an
  ancestor (observed in-session; no receipt file needed).
- Arm body `tools/tsukuroi-census.sh:1848-1887`, line assembled at `:1884`, emitted once between
  DRIFT and the rollup at `:3007-3008`; grammar/contract `:353-366` (`filesystems` = UUID-named
  entries of `TSUKUROI_BTRFS_SYSFS` at `:355`; absent root = HEALTHY 0/0/0 at `:363`).
- Exit map DEGRADED→1, BLOCKED→2 at `tools/tsukuroi-census.sh:3022-3025`.

## 2. Live run of the census

Command and result (`.ufo/waves/round-38/w1/C1ExecLiveSurface/census-run.txt:1-5`):

```
command: bash .../tools/tsukuroi-census.sh
exit=1 wall_ms=3252 stderr_bytes=0
STORAGE line (run3): STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0
rollup (run3): TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
```

Full output: `.../C1ExecLiveSurface/census-full.out` (8 368 bytes, 12 lines) — STORAGE at
`census-full.out:11`, DRIFT at `:10`, rollup at `:12`; exactly one STORAGE line, six PLANE lines,
one rollup (`.../shape-and-uuid.txt:1-4`). exit=1 is the documented DEGRADED rollup, not an arm
failure. Second and third runs printed the same STORAGE line byte-for-byte
(`.../neutrality.txt:3`, `census-run.txt:4`; `cmp` of run2/run3 STORAGE lines identical).

## 3. Independent host view (not the arm's code)

`.../host-fs-view.txt`:

- `findmnt -t btrfs -o TARGET,SOURCE,UUID` → four mount rows, **all one UUID**
  `1d02a454-c549-4a35-b567-89d60902af8e` (`host-fs-view.txt:2-6`).
- `ls /sys/fs/btrfs` → `1d02a454-c549-4a35-b567-89d60902af8e` and `features`
  (`host-fs-view.txt:8-10`); `ls -l` shows both as `drwxr-xr-x root root`
  (`host-fs-view.txt:12-15`). The fsid dir name equals the mounted UUID and equals
  `metadata_uuid` (`shape-and-uuid.txt:5-10`).
- `cat /sys/fs/btrfs/*/devinfo/*/error_stats` → exactly the five counters, each `0`
  (`host-devinfo.txt:2-7`); `devinfo/` holds only device `1` (`host-devinfo.txt:11-13`);
  `features` has no `devinfo/` (`host-devinfo.txt:10`).

Independent recount by a separate Python reading, not the arm
(`.../independent-recount.txt:2`): `filesystems=1 devices=1 nonzero=0` — identical to the
census fields. So the arm counted 1 filesystem and not 2, i.e. the live `features` sibling is
skipped as the contract says (`tools/tsukuroi-census.sh:355`), and `devices=1` matches
`btrfs filesystem show /` "Total devices 1" (`.../host-btrfs-extra.txt:25`).

## 4. World-readability

`.../perm-detail.txt:2-6` — every path component is `0755 root root` and the file is
`-r--r--r-- 444 root root .../devinfo/1/error_stats` (also `host-devinfo.txt:14,17`). The
read in §3 was performed as `uid=1000(vgpnk)`, euid non-root
(`.../btrfs-device-stats.txt:2`), so both traversal and the file read need no privilege, as
the contract states (`tools/tsukuroi-census.sh:364`, `corpus/knowledge/storage-health-r26.md:21`
"no privilege needed"). Two spaced reads of the file were identical (`.../stability.txt:4-5`).

## 5. `btrfs device stats /` without root

It works: btrfs-progs v7.1, uid 1000, rc=0, empty stderr
(`.../btrfs-device-stats.txt:5-14`; `.../device-path-check.txt:10-12`), and the five values match
sysfs (all zero). No permission error was produced, so there is none to report. Two invocations
were identical (`.../stability.txt:7-8`). This is the second read path SH1 names
(`corpus/knowledge/storage-health-r26.md:21`) and it reproduces SH1's host reading exactly:
"One device (devid 1, /dev/mapper/root). All five counters are 0 in sysfs ... and through the
ioctl" (`storage-health-r26.md:19`).

Side observation, not an arm defect: `btrfs filesystem show /` marks that device path `MISSING`
(`.../host-btrfs-extra.txt:26`) because `/dev/mapper/root` resolves to `/dev/dm-0` which is
`brw-rw---- root disk` (`.../stability.txt:2`) and uid 1000 is not in `disk` — `[INFERENCE]`:
btrfs-progs cannot open the block node, while `device stats` needs only the mount through
ioctls (`.../host-btrfs-extra.txt:34-37`). This is a small, concrete argument for the arm
reading sysfs rather than resolving the device path.

## 6. Verdict neutrality and override, live

Three runs in the same minute (`.../neutrality.txt:1-7`): default env, `TSUKUROI_BTRFS_SYSFS`
= an empty dir, and = a nonexistent dir. All three: rollup lines and exit code identical
(`rc live=1 empty=1 absent=1`), STORAGE differs only as designed (1/1/0 vs 0/0/0 vs 0/0/0).
`diff` with the STORAGE line removed shows only the header timestamp and the drivers plane's
inherently time-varying readings (`C4_sweep` 198/200/202, C6 psi/avail figures) — no PLANE,
HANDOFF, DRIFT or rollup text changed (`neutrality.txt:8-25`). So the live arm is verdict-neutral
and honours its env override (`tools/tsukuroi-census.sh:446`, `:363`).

## 7. Counter-environment replay (why the frozen receipt says `census_exit: 2`)

The frozen C1 receipt's live leg records `census_exit: 2` while a login-shell run exits 1
(`after/c1-after-52ffd65.json:200,242`). Replaying the counter's scrubbed environment
(`env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch>/home TMPDIR=<scratch>/tmp`) reproduces
exit=2 with `PLANE systemd: BLOCKED (... no user scope bus ...)` and the **same** STORAGE line,
`HEALTHY filesystems=1 devices=1 nonzero=0` (`.../counter-env-replay.txt:1-2,4,9-10`). So the
receipt's live leg is a genuine read of the real `/sys/fs/btrfs`; its exit code reflects the
scrubbed environment, not the arm, and exit is not part of the predicate
(`tools/score-storage-arm-r38.py:5-8`, live comparison at `:222-229`). The receipt's live
expected/got tuple `(HEALTHY, 1, 1, 0)` is identical to today's independent recount.

## 8. Caveats a reader must not misread

- `filesystems=1` is filesystems, **not mounts**: this host has one btrfs filesystem with four
  subvolume mount rows (`host-fs-view.txt:3-6`). The contract defines the field as fsid entries
  (`tools/tsukuroi-census.sh:355`); compare with `findmnt` by UUID, not by row count.
- The live surface carries no nonzero pair (`nonzero=0`), so the real host does not exercise
  the nonzero/DEGRADED accounting or the `detail=` list; that leg is covered by fixtures and the
  other seats (`tools/tsukuroi-census.sh:2899-2917`).
- A zero counter is a lifetime total with no date (`tools/tsukuroi-census.sh:361`, SH2); HEALTHY
  here says "no recorded device errors", not "no incident ever".
- Only one filesystem and one device exist, so multi-fs/multi-device live counting is not
  exercised on this host.

## 9. What I did not do

- No sudo, no `pacman`, no service/sysfs/firewall/boot change, no counter reset (`-z` never
  used), no `btrfs device stats -z`. No host write of any kind.
- No selftest, no counter re-run, no clones/mutants — other seats own those; this seat ran only
  the live census plus read-only host queries.
- Lane tracked files untouched: `git status --porcelain` shows no `M`/`A`/`D` entries, only the
  wave's pre-existing untracked `.ufo/waves/round-38/*` paths (observed in-session).
- No tools installed or upgraded. One `bc`-based timing attempt failed (`bc` absent); timing was
  redone with integer nanosecond arithmetic and the receipt records the correction
  (`census-run.txt:3`).
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C1ExecLiveSurface` removed after copying receipts;
  nothing written outside this seat dir in the lane.

## 10. Receipts (all under `.ufo/waves/round-38/w1/C1ExecLiveSurface/`)

| file | content |
|---|---|
| `census-full.out` | full live census output, 12 lines (STORAGE at :11) |
| `census-run.txt` | command, exit, wall ms, STORAGE + rollup of run 3 |
| `census-storage-lines.txt` | STORAGE and rollup lines of run 1 |
| `host-fs-view.txt` | `findmnt`, `ls /sys/fs/btrfs`, `ls -l` |
| `host-devinfo.txt` | `cat` of error_stats, `ls -l` devinfo, `stat` modes |
| `perm-detail.txt` | permission chain, uid note, mount options |
| `independent-recount.txt` | separate Python recount of the same fields |
| `btrfs-device-stats.txt` | id, btrfs-progs version, unprivileged `btrfs device stats /` |
| `btrfs-stats-stderr.txt` | empty stderr file of that command |
| `device-path-check.txt` | device symlink, stats stderr rc, findmnt row count |
| `host-btrfs-extra.txt` | fs sysfs entries, `btrfs filesystem show /`, `device stats --help` |
| `stability.txt` | read-to-read stability, `/dev/dm-0` mode |
| `shape-and-uuid.txt` | line counts/order, fsid vs UUID vs metadata_uuid |
| `neutrality.txt` | three-run override/neutrality comparison |
| `counter-env-replay.txt` | scrubbed-env replay explaining the receipt's exit 2 |
