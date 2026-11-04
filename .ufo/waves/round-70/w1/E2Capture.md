# E2Capture — independent host enumeration binding the C2 `XFS xfs-stats` counts

Seat: E2Capture (round 70, wave w1). Scope: read-only enumeration; no lane write. Captured
2026-11-04T00:09:44Z on the canonical Arch host, uid 1000 (`vgpnk`), `uname -r` 7.2.11-arch1-1,
xfsprogs 7.2.0-1, `xfs_spaceman version 7.2.0`. This enumeration was taken before reading any other
seat's output (no E1XfsArm artifact was opened).

Witness (committed output of one script invocation, start and end counts inside it):
`.ufo/waves/round-70/probes/E2Capture/host-enum.txt`.

## Field derivations (command → output)

| field | command | output |
|---|---|---|
| mounts | `awk '$3=="xfs"{print $1}' /proc/self/mounts \| sort -u \| wc -l` | **2** (`/dev/nvme1n1p1`, `/dev/nvme1n1p2`; `findmnt -t xfs -n -o SOURCE \| sort -u \| wc -l` also **2**; duplicate sources **0**) |
| present | per distinct source, `test -d /sys/fs/xfs/<basename>` | **2** (`nvme1n1p1`, `nvme1n1p2`; both `-r` and `-x`) |
| absent | mounts − present | **0** |
| unreadable | present dirs failing `-r`/`-x` | **0** |
| stats | per mount, readable `stats/stats` whose **first line** matches `^[a-z][a-z0-9_]*([ ][0-9]+)+$` | **2** (both mode 444 root:root, 34 lines, first line `extent_alloc …` → MATCH) |
| error | Σ `find /sys/fs/xfs/<base>/error -type f` over mounts | **18** (9 per filesystem, all readable) |
| log | Σ `find /sys/fs/xfs/<base>/log -type f` over mounts | **8** (4 per filesystem, all readable) |
| detail | closed vocabulary | **none** fired (no absent, no unreadable, every stats first line matches) |

Counts were re-derived inside the same invocation at both ends of the capture and are identical
(`mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`).

Expected live line body, for a diff against the landed census line:
`XFS xfs-stats mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`.

## Adjacent facts re-measured (not C2 fields, they bound the reading)

- `/sys/fs/xfs/*/` lists **three** dirs: the two device dirs plus the global `stats` dir. The global
  dir is not a mount: counting sysfs dirs as devices reads `present=3`, which contradicts `mounts=2`.
- Global stats `/sys/fs/xfs/stats/stats` exists, mode 444, 34 lines, first line matches. Counting it in
  `stats` reads 3, breaking `stats ≤ present`.
- `stats_clear` is mode **200 root:root** on both filesystems and on the global dir; not writable by
  uid 1000. Nothing was written (read-only seat).
- `/proc/fs/xfs/stat` → `/sys/fs/xfs/stats/stats` (readlink), readable, 34 lines.
- `stats/stats` line 34 is `gc xpc 0` (group `gc`, per-CPU `xpc` sub-counter) and therefore does **not**
  match the per-line regex; 33 of 34 lines match. Only the contract's **first-line** test is safe — a
  whole-file "every line matches" reading yields `stats=0`.
- `find <error> -maxdepth 1 -type f` reads **1 per fs (2 total)**; the contract's "regular files under
  `error/`" is the recursive 9 per fs (8 of them under `error/metadata`).
- `xfs_spaceman -c health` per mount: `Health status has not been collected for this filesystem.` /
  `Please run xfs_scrub(8) to remedy this situation.`, rc 0 for both `/tmp` and `/fast`.

## Divergence worth the parent's attention (evidence, not a predicate reading)

The frozen declaration's host-facts prose (`SCORECARD.md`, round-70 §(b)) says "error subtree **7**
regular files per filesystem". Both the declaration's own committed capture
(`.ufo/waves/round-70/before/host.txt`, committed at `1710bd74`: **9** `/error/` file lines for
`nvme1n1p1` and **9** for `nvme1n1p2`, `ENODEV` present) and the live tree today read **9 per fs, 18
total**. The frozen *predicate* is "`error`/`log` equal to the enumerated regular-file counts", so the
operative target is **18 / 8**; the prose `7` is stale and cannot be the counter value. Not amended,
not reinterpreted here — reported only.

## Bounds observed

Read-only: only `/proc/self/mounts`, `/sys/fs/xfs/**` (stat/find/read), `findmnt`, `xfs_spaceman -V` and
`-c health`, `pacman -Q`, `date`, `uname` were executed. No privilege escalation, no sysfs write, no
package transaction, no host service touched. Files written: this report and the witness under
`.ufo/waves/round-70/probes/E2Capture/`. Scratch `/fast/scratch/hyaku/tsukuroi-r70/E2Capture` removed
before yield. No NVMe serial, WWID or hostname recorded.

MOUNTS=2
PRESENT=2
ABSENT=0
STATS=2
ERROR_FILES=18
LOG_FILES=8
STATS_LINES=34
HEALTH_READER=Health status has not been collected for this filesystem.
