source: S164–S169 in `corpus/SOURCES.md`: btrfs-progs v7.1 Documentation/Defragmentation.rst (`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/Defragmentation.rst`, sha256 `71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b`); btrfs-rescue.rst (`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-rescue.rst`, sha256 `838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d`); btrfs-check.rst (`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-check.rst`, sha256 `927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c`); ch-mount-options.rst (`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-mount-options.rst`, sha256 `aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f`); btrfs-replace.rst (`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-replace.rst`, sha256 `da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e`); Trim.rst (`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/Trim.rst`, sha256 `2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc`); frozen source URLs and pins: `tools/check-btrfs-repair-r31.py:56-91`.
verified-at: 2026-10-22 (the six downloaded snapshots' `sha256sum` values matched the pins at `tools/check-btrfs-repair-r31.py:60-90`).
recheck: `python3 tools/check-btrfs-repair-r31.py --revision "$(git rev-parse HEAD)"` for the frozen C1 row and source-pin predicate (`tools/check-btrfs-repair-r31.py:43-46,60-90`; read-only gate conventions: `tools/check-recheck-commands.py:4-11,34-38`). Recheck cadence: on-release.
companion: `corpus/knowledge/btrfs-repair-r31.json` (Q01–Q08 rows) and `SKILL.md` (the eight `| [R31-Qnn] ` decision lines), as required by `tools/check-btrfs-repair-r31.py:7-13,16-27`.

# Btrfs repair and maintenance decisions (round 31)

## Decision table

| id | situation | decision | source file and line |
|---|---|---|---|
| Q01 | Files created with `cp --reflink` or present in multiple snapshots share extents. | Defragmentation does not preserve extent sharing; data-space consumption may increase. | `Defragmentation.rst:24-27` (S164) |
| Q02 | A filesystem mount fails during log replay and the backtrace resembles the documented example. | `btrfs rescue zero-log` clears the filesystem log tree; the documentation says to use it when the errors are like the sample. Clearing the log may lose changes since the last transaction commit, up to 30 seconds by default or less. | `btrfs-rescue.rst:123-152` (S165) |
| Q03 | A structural check or repair is being considered. | Unmounting before a check is recommended, and the default check does not modify the device. Do not use `--repair` without developer or experienced-user advice and acceptance that not all filesystem corruption can be repaired and other software or hardware bugs may fatally damage a volume. | `btrfs-check.rst:12-18,29-33` (S166) |
| Q04 | Small random writes occur, or the workload is a large database. | `autodefrag` (default off) detects and queues small random writes in the tens-of-kilobytes range (currently 64 KiB); it may not be well suited for large database workloads, and adjacent-block reads may increase read latency. | `ch-mount-options.rst:33-43` (S167) |
| Q05 | The `commit=<seconds>` periodic transaction-commit interval is set. | The default is 30 seconds; the upper bound is not forced, a warning is printed above 300 seconds, and higher values let more unwritten data accumulate in memory with consequences if the system crashes; the documentation says to use with care. | `ch-mount-options.rst:89-101` (S167) |
| Q06 | `nodatacow` is enabled for newly created files. | `nodatacow` implies `nodatasum` and disables compression; in-place updates may improve performance for frequent overwrites but carry a risk of partial writes if interrupted. `nodatasum` files inherit the no-checksums property. | `ch-mount-options.rst:131-159` (S167) |
| Q07 | The source device is unavailable for replacement. | Start replacement with `btrfs replace start <srcdev|devid> <targetdev> <path>`; if the source is unavailable, data is built only using RAID redundancy, and a disconnected source must be named by devid. The target must be the same size as or larger than the source; the filesystem must be resized to use a larger target fully. | `btrfs-replace.rst:20-38` (S168) |
| Q08 | Trim is being considered on a flash or other trim-capable device. | Synchronous `discard=sync` trims immediately after extents are freed and is not recommended because of possible severe performance impact; `discard=async` batches freed extents and throttles I/O; periodic `fstrim` is suitable as a periodic service. The cited text does not state a universal winner between async discard and periodic `fstrim` [inf]. | `Trim.rst:12-32,40-43` (S169) |

## Error patterns

| Observation | Reading |
|---|---|
| A mount-failure backtrace includes `open_ctree` and function names containing `replay`, `recover` or `log_tree`. | `open_ctree` indicates the failure is during mount; if the errors are like the documented sample, the documentation says `zero-log` should be used to clear the log (`btrfs-rescue.rst:141-152`, S165). |
| Sample frames include `replay_one_dir_item`, `walk_log_tree` or `btrfs_recover_log_trees`. | These are among the sample backtrace frames offered for deciding whether `zero-log` is needed (`btrfs-rescue.rst:136-152`, S165). |
| `zero-log` is used. | It clears the filesystem log tree and may lose changes since the last transaction commit, up to 30 seconds by default or less (`btrfs-rescue.rst:123-134`, S165). |

## Boundary

Mori owns the resource-runway surface [inf]: its runway row names `df -P` on the fleet root and `/tmp` (`mori-shokunin/SKILL.md:19`), and its explicit boundary is “Never threshold the btrfs chunk percent” and “Keep the `df -P` parser” (`mori-shokunin/SKILL.md:415-418`). This tsukuroi entry states repair and maintenance decisions only and sets no runway threshold [inf] (`btrfs-check.rst:12-33`, S166; `mori-shokunin/SKILL.md:19,415-418`).

## Not covered

- The possible extra data-space use from defragmentation is not quantified here [inf]; the source only says that consumption may increase (`Defragmentation.rst:24-27`, S164).
- This entry does not determine whether a particular host has enough RAID redundancy for an unavailable-source replacement [inf]; the source says that replacement data is built only using RAID redundancy (`btrfs-replace.rst:23-33`, S168).
- The source text does not select one universal winner between `discard=async` and periodic `fstrim` [inf]; it describes async batching and calls periodic `fstrim` suitable as a periodic service (`Trim.rst:20-32,40-43`, S169).
- No host-specific corruption diagnosis or repair result is stated [inf]; the checker documentation describes general checks and cautions that `--repair` cannot successfully repair every type of filesystem corruption (`btrfs-check.rst:12-18,29-33`, S166).
- No disk-runway threshold or verdict is set [inf]; mori's runway row specifies `df -P`, and its boundary forbids thresholding btrfs chunk percent (`mori-shokunin/SKILL.md:19,415-418`).
