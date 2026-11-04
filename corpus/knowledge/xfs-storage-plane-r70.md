source: S290, S291, S292 and S293 in `corpus/SOURCES.md` (Linux stable v7.2.11 `Documentation/admin-guide/xfs.rst`, `fs/xfs/xfs_stats.c`, `fs/xfs/xfs_sysfs.c`; xfsprogs v7.2.0 `spaceman/health.c`), plus the read-only host capture `.ufo/waves/round-70/before/host.txt` (2026-11-04T00:02:40Z; kernel 7.2.11-arch1-1, xfsprogs 7.2.0-1)
verified-at: 2026-11-03 (committed snapshots under `.ufo/waves/round-70/before/src/`, `SHA256SUMS` rc 0; host capture 2026-11-04T00:02:40Z)
recheck: `python3 tools/count-xs-rows-r70.py --revision <REV>` for the six row predicates; re-run the read-only `.ufo/waves/round-70/before/capture.sh <out>` for the host readings; re-open the four sources on a kernel or xfsprogs release; recheck cadence: on-release

# XFS storage plane: sysfs stats, log, error configuration and online health (round 70)

| id | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| XS1 | xfs_stats_format emits one summary line per xstats entry, each xstats_entry naming an endpoint where counter_val accumulates per-CPU u32 values. | source=S291 | snapshot=xfs_stats.c | digest=4b6a9b6c239a92abb56838798a2d5657a53ba5a7fb1bee6aa9c12b89f7c9e452 | quote="/* Loop over all stats groups */" |
| XS2 | counter_val sums each per_cpu_ptr 32-bit slot into an int, while xfs_stats_format emits four extra precision lines: xpc with three %llu values, defer_relog and gc xpc as %llu, and debug as %u. | source=S291 | snapshot=xfs_stats.c | digest=4b6a9b6c239a92abb56838798a2d5657a53ba5a7fb1bee6aa9c12b89f7c9e452 | quote="xs_xstrat_bytes += per_cpu_ptr(stats, i)->s.xs_xstrat_bytes; xs_write_bytes += per_cpu_ptr(stats, i)->s.xs_write_bytes;" |
| XS3 | The xfs_stats_ktype exposes stats through XFS_SYSFS_ATTR_RO and stats_clear through XFS_SYSFS_ATTR_WO, whose stats_clear_store rejects any parsed value other than 1 with EINVAL before calling xfs_stats_clearall. | source=S292 | snapshot=xfs_sysfs.c | digest=1cbcffa12346ebe3ebb29b466196786ea07450d67e4e4d1cbd675603784a5805 | quote="if (val != 1) return -EINVAL;" |
| XS4 | xfs_log_ktype publishes log_head_lsn and log_tail_lsn as two decimal fields joined by a colon, and reserve_grant_head_bytes plus write_grant_head_bytes as atomic64 grant values in bytes. | source=S292 | snapshot=xfs_sysfs.c | digest=1cbcffa12346ebe3ebb29b466196786ea07450d67e4e4d1cbd675603784a5805 | quote="ATTR_LIST(log_head_lsn), ATTR_LIST(log_tail_lsn), ATTR_LIST(reserve_grant_head_bytes), ATTR_LIST(write_grant_head_bytes)," |
| XS5 | Each mounted filesystem exposes /sys/fs/xfs/<dev>/error/<class>/<error>/, and as of 4.9 the only defined class named metadata applies to metadata buffer write IO. | source=S290 | snapshot=xfs.rst | digest=53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c | quote="The configuration files are organized into the following hierarchy for each mounted filesystem:" |
| XS6 | health_f prints that health status has not been collected for this filesystem and advises running xfs_scrub(8) to remedy this situation when the report pass produced no sick flag. | source=S293 | snapshot=health.c | digest=84fdd0bec52a7f0efc592c588a6d001c2b8ba389a7e33de7daf5d13a34215950 | quote="Health status has not been collected for this filesystem." |

## Scope

This entry holds the XFS sysfs storage plane, the kernel-side counterpart to the btrfs and NVMe
signals already recorded in `storage-health-r26.md` (S128-S139): the per-filesystem and global
`stats/stats` file with its one-line-per-group counter layout and four extra-precision lines, the
write-only `stats_clear` contract, the four `log/` files (head and tail LSN, two grant heads), the
`error/` configuration tree and its metadata class, and the online health reader's "not collected"
state. It is a read-only detection surface on the second NVMe device (xfs on `/dev/nvme1n1p1` at
`/tmp` and `/dev/nvme1n1p2` at `/fast`); the btrfs counters, the NVMe SMART log and the scrub record
of S128-S139 are already held and are not restated here. Nothing in this entry authorizes a write:
`stats_clear`, `error/*/max_retries`, `fail_at_unmount`, a scrub run and any counter reset are
operator decisions, and this lane never performs them. Free capacity and disk-space runway
remain mori's question (`PROVINCE.md` round-26 wave-2 split); this entry states no capacity,
threshold or fleet-runway reading.

## Host readings

**XS1.** Both per-filesystem `stats/stats` files and the global file are 34 lines. Their opening
group lines begin `extent_alloc 9985713 64290045 9956026 58170740` (`/tmp`),
`extent_alloc 29392098 416623409 27382505 351226382` (`/fast`) and continue through `metafile`; the
takeaway is shape only — 30 named group lines plus 4 precision lines — not the counter magnitudes,
which are workload history.

**XS2.** The same 34-line files end `defer_relog 3768`, `debug 0`, `gc xpc 0` on `/tmp` and
`defer_relog 1311`, `debug 0`, `gc xpc 0` on `/fast`. The group lines above show runs of small
decimal fields; the 64-bit sums are the four trailing lines, and `debug` carries 0 on this
non-DEBUG build.

**XS3.** `/sys/fs/xfs/nvme1n1p1/stats/stats` and `/sys/fs/xfs/nvme1n1p2/stats/stats` are `-r--r--r--`
(0444), and `/sys/fs/xfs/stats/stats` is likewise read-only. All three `stats_clear` files are
`--w-------` (0200, root). No `stats_clear` read or write was attempted: a write discards the
recorded history, so only the mode and the source contract are reported.

**XS4.** Each filesystem's `log/` holds four `-r--r--r--` files. The `/tmp` values read
`log_head_lsn = 9443:142464`, `log_tail_lsn = 9443:140968`,
`reserve_grant_head_bytes = 21737264`, `write_grant_head_bytes = 22157760`; `/fast` reads
`12767:325728`, `12767:270960`, `24590144`, `24590492`. The LSN files are `cycle:block`; the grant
files are decimal byte counts.

**XS5.** Each filesystem's `error/` subtree holds 9 regular files: `fail_at_unmount` = 1, and under
`metadata/` the `default`, `EIO` and `ENOSPC` handlers each carry `max_retries` = -1 and
`retry_timeout_seconds` = -1, while `ENODEV` carries 0 and 0 — eight handler files plus
`fail_at_unmount`. `metadata` is the only class directory present, matching the source's single
defined class.

**XS6.** `xfs_spaceman -c health` against both `/tmp` and `/fast` prints
`Health status has not been collected for this filesystem.` followed by
`Please run xfs_scrub(8) to remedy this situation.`, rc 0. No scrubbed metadata state exists to
report yet, so the reader is not a clean bill of health; it is the absence of a record.

## Limits

- The row quotes and identifiers are anchored to the upstream tag bytes
  (`v7.2.11` for the three kernel files, `v7.2.0` for `health.c`), not to host-build line numbers:
  this host runs the distribution build `linux 7.2.11.arch1-1` / `xfsprogs 7.2.0-1`, which may carry
  patches that shift lines, so no host-side line number is claimed here (QUALITY 103, R69-PATCH-OFFSET).
  A recheck that needs a host line must name the package build, not the tag.
- The counters in `stats/stats` are workload and error telemetry, not a health grade: a large
  `extent_alloc` or `rw` field says the filesystem is busy, not that it is sound; XFS has no
  aggregate "healthy" counter in this file.
- `stats_clear` is write-only and this lane never writes it; the 0200 mode means no read-back of the
  previous state is possible from an unprivileged or privileged read.
- The error tree exposes retry configuration, not error history: it cannot say whether an error
  occurred, only how the filesystem is configured to propagate one.
- No scrub state is readable unprivileged (or from these files at all); the `health` reader's
  "not collected" line is the only scrub-derived signal on this host, and it says there is none.
- The grant-head values are instantaneous and move with log traffic; they are not a corruption or
  space-exhaustion signal by themselves.

## Provenance

`source:` S290 (`xfs.rst`, v7.2.11, sha256 `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c`),
S291 (`xfs_stats.c`, v7.2.11, sha256 `4b6a9b6c239a92abb56838798a2d5657a53ba5a7fb1bee6aa9c12b89f7c9e452`),
S292 (`xfs_sysfs.c`, v7.2.11, sha256 `1cbcffa12346ebe3ebb29b466196786ea07450d67e4e4d1cbd675603784a5805`),
S293 (`health.c`, v7.2.0, sha256 `84fdd0bec52a7f0efc592c588a6d001c2b8ba389a7e33de7daf5d13a34215950`), all
byte-identical to `.ufo/waves/round-70/before/src/SHA256SUMS` and `SOURCES.json`; host capture
`.ufo/waves/round-70/before/host.txt`.
`verified-at:` 2026-11-03 for the snapshots; 2026-11-04T00:02:40Z for the capture.
`recheck:` `python3 tools/count-xs-rows-r70.py --revision <REV>`; re-run the read-only capture; re-open
the four sources on a kernel or xfsprogs release; cadence on-release.
