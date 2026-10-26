source: S237 S238 S239 (rows in `corpus/SOURCES.md`; pinned snapshots `.ufo/waves/round-42/frozen/src/`, digests in its `SHA256SUMS`, fetch log `FETCH.txt`; host capture `.ufo/waves/round-42/frozen/hostcap/capture.txt`, sha256 942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c)
verified-at: 2026-10-26 (btrfs-progs tag v7.1, peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b; host btrfs-progs 7.1-1, kernel 7.2.11-arch1-1; capture 2026-10-26T19:13:44Z)
recheck: on-release — re-fetch the two URLs in `.ufo/waves/round-42/frozen/src/FETCH.txt` and compare `sha256sum` with `SHA256SUMS`; re-run `bash .ufo/waves/round-42/frozen/hostcap/capture.sh <file>` (unprivileged, read-only); `python3 tools/check-scrub-record-r42.py --revision <REV>`

# The btrfs scrub status record: who writes it, what it holds, and what its absence means (round 42)

Scope: the storage-integrity frontier (`PROVINCE.md` Frontier, scrub record; `corpus/README.md` `## Frontier`).
The lane already holds what scrub verifies and repairs and that `btrfs scrub status` reads a file under
`/var/lib/btrfs` (`corpus/knowledge/storage-health-r26.md` SH3, SH4; S129, S139), including the record's name
pattern (SH4) and that a scrub run with recording disabled cannot be excluded (SH4 note). It held no statement of the
record itself: how the file is replaced, its line format, which process writes it and when recording is switched off,
how the status command turns per-device lines into one filesystem verdict, and the per-device throughput limit that
same command reports (SC5). Those decide how far "no record" may be read as "never scrubbed". Rows SC1-SC5 state upstream behaviour of btrfs-progs v7.1 (the
version this host runs) from `cmds/scrub.c` and `CHANGES`; the host readings are this machine's, unprivileged.
Nothing here runs a scrub, writes `/var/lib/btrfs` or changes a scrub limit (operator actions).

## SC1

**Statement.** The record for one filesystem is the file `/var/lib/btrfs/scrub.status.<fsid>` (the base path plus a
dot plus the filesystem UUID; the name pattern is already held, SH4). Every update is written to a sibling file `scrub.status.<fsid>_tmp` and then moved
over the record with `rename`, so a reader sees either the old or the new record, never a half-written one. A record or
`_tmp` file the CLI creates gets mode 0600 (the `open` mode argument, subject to the umask), and every open of either,
for reading or writing, must take a non-blocking exclusive `flock` (`LOCK_EX`), so a second writer or a reader that
finds the lock held fails at once instead of waiting. (The progress socket `/var/lib/btrfs/scrub.progress.<fsid>` is a
different file, created by `bind`, not covered here.)

**Quote.** `S237` scrub.c:67: "#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status""

**Quote.** `S237` scrub.c:459: "datafile[ret] = '.';"

**Quote.** `S237` scrub.c:467: "datafile[ret] = '_';"

**Quote.** `S237` scrub.c:483: "fd = open(datafile, m, 0600);"

**Quote.** `S237` scrub.c:487: "ret = flock(fd, LOCK_EX|LOCK_NB);"

**Quote.** `S237` scrub.c:534: "ret = rename(datafile_old, datafile_new);"

**Host reading.** No record exists: `/var/lib/btrfs` is absent (capture.txt:6) for the root filesystem
`1d02a454-c549-4a35-b567-89d60902af8e` (capture.txt:5).

## SC2

**Statement.** The record is text. Its first line is `scrub status:1` (format prefix and version 1). Each further
line belongs to one device: the filesystem UUID, a colon, the device id, then one `|key:value` pair per field, in
this order — the progress counters `data_extents_scrubbed`, `tree_extents_scrubbed`, `data_bytes_scrubbed`,
`tree_bytes_scrubbed`, `read_errors`, `csum_errors`, `verify_errors`, `no_csum`, `csum_discards`, `super_errors`,
`malloc_errors`, `uncorrectable_errors`, `corrected_errors`, `last_physical`, then the run fields `t_start`,
`t_resumed`, `duration`, `canceled`, `finished`. A record therefore carries per-device error sums and a per-device
finished flag, not one filesystem verdict.

**Quote.** `S237` scrub.c:69: "#define SCRUB_FILE_VERSION_PREFIX "scrub status""

**Quote.** `S237` scrub.c:856: "ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":""

**Quote.** `S237` scrub.c:840: "return scrub_writev(fd, buf, max, "|%s:%lld", key, val);"

**Quote.** `S237` scrub.c:870: "_SCRUB_KVWRITE(fd, buf, data_extents_scrubbed, use) ||"

**Quote.** `S237` scrub.c:888: "_SCRUB_KVWRITE_STATS(fd, buf, finished, use) ||"

**Host reading.** Not observable on this host: there is no record to parse (capture.txt:6).

## SC3

**Statement.** The record is written by the userspace `btrfs scrub start` process, not by the kernel: it writes an
all-zero record when the scrub starts (or is resumed) and progress records while it runs. Recording is switched off, with a
warning that ends "status recording disabled", when the directory `/var/lib/btrfs` cannot be created or the first
record cannot be written; the scrub itself still runs. Whether a scrub is running is asked from the kernel with the
`BTRFS_IOC_SCRUB_PROGRESS` ioctl per device, independent of the file. A record-write failure later in the run
ends the progress writes without that warning; only the final write reports a failure ("failed to record the
result"). So a missing record does not prove that no scrub ran: a scrub whose recording was disabled, or one driven
by another tool through the ioctl [inference from the write path], leaves none. That conclusion was already held
(SH4 note); new here are the mechanism and the disable conditions.

**Quote.** `S237` scrub.c:1502: "/* write all-zero progress file for a start */"

**Quote.** `S237` scrub.c:1336: "warning("cannot create scrub data file, mkdir %s failed: %m, status recording disabled","

**Quote.** `S237` scrub.c:1507: "warning("failed to write the progress status file: %m, status recording disabled");"

**Quote.** `S237` scrub.c:1121: "if (!spc->do_record)"

**Quote.** `S237` scrub.c:1200: "ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);"

**Host reading.** No scrub timer is enabled (`btrfs-scrub@.timer disabled`, capture.txt:8; no `btrfs-scrub@*` timer
listed, capture.txt:7) and the current boot's kernel log holds no `scrub: started` or `scrub: finished` line
(capture.txt:10); together with the absent directory (capture.txt:6) nothing on this host records a scrub, which
is weaker than "no scrub ran" (this row).

## SC4

**Statement.** `btrfs scrub status` treats a missing record as no history (an open failure of `ENOENT` is not an
error; any other open failure prints a warning and the command exits with an error). The filesystem summary folds the per-device lines together: the
start time is the smallest device start (`_SCRUB_FS_STAT_ZMIN`, where an unset value is always replaced), the run
counts as canceled if any device was canceled, and it counts as
finished only if every device that has a record in the file is finished (the flag starts at 1 and takes the minimum,
`_SCRUB_FS_STAT_MIN`; devices without a record are skipped).
The status word is `running` when the kernel reports a scrub in progress, else `aborted` when canceled, else
`finished`, else `interrupted`; with no start time the summary prints `no stats available` instead. An
`interrupted` status therefore means an unfinished record with nothing running now (for example a start process
that ended before the scrub did) [inference], not a device error.

**Quote.** `S237` scrub.c:1931: "if (fdres < 0 && fdres != -ENOENT) {"

**Quote.** `S237` scrub.c:300: "_SCRUB_FS_STAT_ZMIN(ss, t_start, fs_stat);"

**Quote.** `S237` scrub.c:303: "_SCRUB_FS_STAT_ZMAX(ss, canceled, fs_stat);"

**Quote.** `S237` scrub.c:304: "_SCRUB_FS_STAT_MIN(ss, finished, fs_stat);"

**Quote.** `S237` scrub.c:310: "fs_stat->s.finished = 1;"

**Quote.** `S237` scrub.c:321: "pr_default("\tno stats available\n");"

**Quote.** `S237` scrub.c:342: "(ss->canceled ? "aborted" :"

**Host reading.** With no record (capture.txt:6) the status summary of this root prints `no stats available`: wave-1
seat C2ExecHostRecheck ran `btrfs scrub status /` unprivileged, read-only, exit 0, and it printed that line
(`.ufo/waves/round-42/w1/C2ExecHostRecheck.md` §2); the frozen capture holds the absent directory only.

## SC5

**Statement.** Each device has a scrub throughput limit in sysfs, `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max`
(bytes per second; 0 means no limit). `btrfs scrub status` and `btrfs scrub start` read it and report a set limit,
and `btrfs scrub limit` shows or sets it; all three arrived in btrfs-progs 6.6.3. A failed read is reported as 0,
so the status command cannot tell "no limit" from "limit unreadable" (on a kernel without the file the limit
silently reads as none). A scrub that looks slow should be checked against this file before the device is blamed.

**Quote.** `S237` scrub.c:1215: "snprintf(path, sizeof(path), "devinfo/%llu/scrub_speed_max", devid);"

**Quote.** `S237` scrub.c:1218: "limit = 0;"

**Quote.** `S238` CHANGES:460: "btrfs-progs-6.6.3 (2023-12-14)"

**Quote.** `S238` CHANGES:467: "* scrub status: report limit if set in sysfs/../scrub_speed_max"

**Quote.** `S238` CHANGES:468: "* scrub limit: new command to show or set the per-device scrub limits"

**Host reading.** The root's only device (devid 1) reads `scrub_speed_max` 0, no limit (capture.txt:9).

## How this changes OS triage

- Read "no scrub record" as a gap in evidence (`UNVERIFIED`, SH4), not as "never scrubbed" (SC3); what SC3 adds is
  the mechanism, not a new verdict.
- A record is per device; a filesystem `finished` needs every device that has a record finished, and one canceled
  device makes the whole run `aborted` (SC2, SC4).
- `interrupted` is a process outcome (an unfinished record, nothing running), not a media fault; read the error
  sums in the per-device lines (`btrfs scrub status -d`, raw `-R`) before calling the device (SC4).
- Before reading a slow scrub as a device problem, read `scrub_speed_max` (SC5).

## Limits

- Upstream behaviour is pinned at btrfs-progs v7.1 source lines; the host runs the Arch build 7.1-1, whose packaging
  applies no patch (wave-1 C2ExecLiveSources: `source=()` names the v7.1 tag and no `*.patch`), so the line pins hold
  for the installed binary.
- The host readings show the absence of a record and of a timer; they cannot show that no scrub ever ran (SC3).
- No census arm reads the record; this entry stays on Frontier ground (`PROVINCE.md` promotion condition for the
  scrub record unchanged).

## QUALITY check

- QUALITY 79 (row = quote bound to a digest-checked snapshot at a cited line): every quote names its snapshot line;
  the snapshots' sha256 are pinned in `SHA256SUMS` and in the counter.
- QUALITY 86 (rule rows rest on an upstream row): every row cites S237 or S238 (kind `code`/`docs`); S239
  (`own-work`) carries only the host readings.
- QUALITY 87 (the counter reads what it credits): each row carries its frozen proposition token and is judged by two
  bound non-author seat verdicts (QUALITY 89 binding); the lexical checks are shape gates only.
