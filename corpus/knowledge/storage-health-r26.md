source: S128, S129, S130, S131, S132, S133, S134, S135 and S139 in `corpus/SOURCES.md` (btrfs-progs v7.1 Documentation/btrfs-device.rst, btrfs-scrub.rst, mkfs.btrfs.rst and ch-scrub-intro.rst; Arch btrfs-progs 7.1-1 btrfs-scrub@.timer; Linux v7.2 fs/btrfs/volumes.c and fs/btrfs/sysfs.c; smartmontools 7.5 smartmontools/nvmeprint.cpp; NVM Express Base Specification 2.4 SMART / Health Information log page), plus the read-only host capture `.ufo/waves/round-26/capture/capture.txt` (sha256 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd)
verified-at: 2026-10-22 (capture 2026-10-22T13:39:52Z, kernel 7.2.11-arch1-1, btrfs-progs 7.1-1, smartmontools 7.5-2, nvme-cli 3.1-1)
recheck: `python3 tools/check-storage-health.py --revision <REV>` for the evidence links; re-run `.ufo/waves/round-26/capture/capture.sh <out>` (read-only) for the host readings; re-open the sources on a btrfs-progs, kernel or smartmontools release

# Storage integrity: btrfs device errors, scrub and NVMe health (round 26)

## Scope

This entry opens a new frontier area of the OS substrate: whether the root filesystem and its device can detect, record and repair data corruption, and how to read the signals. It covers the btrfs per-device error counters, the scrub record, what the block group profiles allow scrub to repair, and the NVMe SMART / Health log as smartctl reports it. It does not cover disk-space runway (mori's surface), filesystem repair, scrub runs, counter resets or firmware updates (operator actions). Machine-readable rows: `corpus/knowledge/storage-health-r26.json`.

Host at capture time: root is btrfs on LUKS (`/dev/mapper/root` on `nvme0n1p2`), one device, data profile `single`, metadata and system `dup`, mount options include `discard=async`.

## SH1

**Statement.** btrfs keeps five per-device error counters: write_io_errs (failed writes), read_io_errs (failed reads), flush_io_errs (failed FLUSH writes), corruption_errs (checksum mismatch or corrupted metadata header) and generation_errs (block generation mismatch). The sysfs file devinfo/<devid>/error_stats prints the same five counters, read by the same kernel function, under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs); `btrfs device stats` reads them through an ioctl.

**Host reading.** One device (devid 1, /dev/mapper/root). All five counters are 0 in sysfs (capture lines 40-44) and through the ioctl (lines 112-116).

**Verdict.** `HEALTHY`

**Action.** None. Read the counters with `cat /sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats` (no privilege needed) or `btrfs device stats <mountpoint>`; never add -z, which zeroes them and destroys the history.

**Sources.** S128, S133, S132. Quotes: S128 (btrfs-device.rst line 254): "corruption_errs"; S128 (btrfs-device.rst line 255): "A block checksum mismatched or a corrupted metadata header was found."; S128 (btrfs-device.rst line 260): "Since kernel 5.14 the device stats are also available in textual form in"; S133 (fs/btrfs/sysfs.c line 2074): "static ssize_t btrfs_devinfo_error_stats_show(struct kobject *kobj,"; S132 (fs/btrfs/volumes.c line 8490): "stats->values[i] = btrfs_dev_stat_read(dev, i);".

**Capture pointers.** line 40 (`write_errs`), line 43 (`corruption_errs`), line 112 (`write_io_errs`), line 115 (`corruption_errs`).

## SH2

**Statement.** The counters are a persistent cumulative record: the kernel loads them from the device tree at mount, writes changes back at transaction commit, and clears them only on an explicit reset (`btrfs device stats -z`), which it logs. A non-zero counter therefore says errors happened at some time, not when. The kernel prints the same `bdev ... errs: wr ..., rd ..., flush ..., corrupt ..., gen ...` text twice: at error level when an error is counted (rate limited) and at info level at mount when any counter is non-zero. Only the error-level line dates an incident.

**Host reading.** Counters are 0, so no mount-time line is printed; 0 `errs: wr` lines and 0 BTRFS error, critical, warning or forced-readonly lines over 6 retained boots (capture lines 154-161). Persistence across mounts cannot be observed on all-zero counters; it rests on the source.

**Verdict.** `HEALTHY`

**Action.** When a counter is non-zero, search the kernel journal of every retained boot for error-level `errs:` lines to date the errors; treat an info-level mount-time line as the stored total, not a new incident. Resetting counters stays an operator decision.

**Sources.** S132, S128. Quotes: S132 (fs/btrfs/volumes.c line 8352): "called from commit_transaction. Writes all changed device stats to disk."; S132 (fs/btrfs/volumes.c line 8429): ""bdev %s errs: wr %u, rd %u, flush %u, corrupt %u, gen %u","; S132 (fs/btrfs/volumes.c line 8446): "return; /* all values == 0, suppress message */"; S128 (btrfs-device.rst line 231): "The device stats keep persistent record of several error classes related to".

**Capture pointers.** line 41 (`read_errs`), line 116 (`generation_errs`).

## SH3

**Statement.** Scrub reads all data and metadata and checks checksums; it repairs a bad block only by copying a verified good copy from another replica. With the data profile `single` there is one copy, so a data checksum error is detected and reported as uncorrectable, not repaired. Metadata with `dup` has two logical copies on the same device and can be repaired from the second, but an SSD may store both as one physical copy. File data with the NOCOW attribute has no checksums and scrub does not verify it; systemd sets that attribute on journal files by default.

**Host reading.** Data profile single (capture line 64); metadata and system profiles dup (`btrfs filesystem df` and sysfs allocation directories); one NVMe SSD under LUKS.

**Verdict.** `DEGRADED`

**Action.** Read this as limited self-repair, not a fault: a data checksum error on this host can be found but not fixed from a replica, so backups are the repair path for file data. Changing the data profile is an operator decision and is not proposed here.

**Sources.** S139, S130, S129. Quotes: S139 (ch-scrub-intro.rst line 13): "On filesystems that use replicated block group profiles (e.g. RAID1), read-write"; S139 (ch-scrub-intro.rst line 14): "scrub will also automatically repair any damage by copying verified good data"; S139 (ch-scrub-intro.rst line 24): "be validated and corrected by scrub, the actual file data is not."; S130 (mkfs.btrfs.rst line 639): "For example, a SSD drive can remap the blocks internally to a single copy--thus"; S129 (btrfs-scrub.rst line 190): "*  *Uncorrectable* -- errors detected at read time but not possible to repair from other copy"; S130 (mkfs.btrfs.rst line 635): "The mkfs utility will let the user create a filesystem with profiles that write".

**Capture pointers.** line 64 (`single`).

## SH4

**Statement.** No scrub record exists on this host for the root filesystem: `btrfs scrub status /` reports no stats, and /var/lib/btrfs, where btrfs-progs keeps scrub.status.<UUID> files, does not exist. The packaged monthly btrfs-scrub@.timer exists but its instance for `/` is disabled and inactive. Ordinary reads do verify checksums, so data that was read has been checked, but no record shows a full pass over stored data.

**Host reading.** `no stats available` (capture line 121); `/var/lib/btrfs` absent (line 127); `btrfs-scrub@-.timer` disabled (line 131) and inactive (line 134). The `Error summary: no errors found` line printed beside `no stats available` is not a health reading.

**Verdict.** `UNVERIFIED`

**Action.** Operator decision: run `btrfs scrub start /` once or enable `btrfs-scrub@-.timer`; the lane never starts a scrub or enables a timer. After a scrub, read `btrfs scrub status /` for csum, verify, read and super errors and the corrected versus uncorrectable split.

**Sources.** S139, S131, S129. Quotes: S139 (ch-scrub-intro.rst line 71): "The scrubbing status is recorded in :file:`/var/lib/btrfs/` in textual files named"; S139 (ch-scrub-intro.rst line 68): "recommended period is a month but it could be less."; S139 (ch-scrub-intro.rst line 17): "Such automatic repair is also carried out when reading metadata or data from a"; S131 (btrfs-scrub@.timer line 5): "OnCalendar=monthly"; S129 (btrfs-scrub.rst line 133): "Show status of a running scrub for the filesystem identified by *path*".

**Capture pointers.** line 121 (`no stats available`), line 127 (`/var/lib/btrfs`).

## SH5

**Statement.** smartctl 7.5 derives the NVMe overall-health line from one byte: it prints PASSED when the controller's Critical Warning byte is zero and FAILED! otherwise, and then lists the set warning bits (bit 0x01 means available spare has fallen below its threshold). Available Spare, Percentage Used and Media and Data Integrity Errors are printed but are not inputs to the PASSED or FAILED result.

**Host reading.** PASSED with Critical Warning 0x00 (capture lines 181, 184); Available Spare 100% against threshold 10%, Percentage Used 2%, Media and Data Integrity Errors 0 (lines 186-188, 197).

**Verdict.** `HEALTHY`

**Action.** Read the Critical Warning byte and the other fields separately: a PASSED result does not mean wear or media errors were judged. Watch Percentage Used, spare against threshold and media errors as their own signals with `sudo smartctl -H -A <device>` (read-only; never -t, -s or -X).

**Sources.** S134, S135. Quotes: S134 (smartmontools/nvmeprint.cpp line 451): "(!w ? "PASSED" : "FAILED!"));"; S134 (smartmontools/nvmeprint.cpp line 459): "jout("- available spare has fallen below threshold\n");"; S134 (smartmontools/nvmeprint.cpp line 840): "print_critical_warning(smart_log.critical_warning);".

**Capture pointers.** line 181 (`PASSED`), line 184 (`0x00`), line 188 (`Percentage Used`).

## SH6

**Statement.** The NVMe SMART / Health log reports information over the life of the controller, retained across power cycles. Power Cycles, Unexpected Power Losses (the field smartctl and nvme-cli still label Unsafe Shutdowns), Media and Data Integrity Errors and Number of Error Information Log Entries are lifetime counts, not dated events. Unexpected Power Losses increments only when main power is lost while the controller had not reported it was ready to power off, so it is not a count of host-visible crashes.

**Host reading.** Power Cycles 325, Unsafe Shutdowns 200, Media and Data Integrity Errors 0, Error Information Log Entries 0 (capture lines 194, 196-198; nvme-cli agrees at lines 221, 223-225). Only six boots are retained in the journal, so most of the 200 cannot be dated.

**Verdict.** `HEALTHY`

**Action.** Compare two dated reads to see whether the count grew in a window; correlate growth with the journal's boot list before naming a cause. A high lifetime ratio alone is not a fault; report it to the operator as context.

**Sources.** S135, S134. Quotes: S135 (NVMe Base Specification 2.4, SMART / Health Information log page, excerpt line 14): "the life of the controller and is retained across power cycles unless otherwise specified."; S135 (excerpt line 258): "Note that this field was previously named Unsafe Shutdowns."; S135 (excerpt line 276): "Entries over the life of the controller."; S134 (smartmontools/nvmeprint.cpp line 528): "jout("Unsafe Shutdowns:                   %s\n", le128_to_str(buf, smart_log.unsafe_shutdowns));".

**Capture pointers.** line 194 (`Power Cycles`), line 196 (`Unsafe Shutdowns`), line 223 (`unsafe_shutdowns`).

## How this changes OS triage

- A zero `PASSED` from smartctl is a statement about one byte; read wear (Percentage Used), spare and media errors as separate signals (SH5).
- A non-zero btrfs error counter is a lifetime total; date it from error-level kernel lines, never from the counter or the mount-time print (SH1, SH2).
- On this host a data checksum error is detectable but not repairable from a replica, and nothing has recorded a full scrub; integrity of stored data is `UNVERIFIED`, not `HEALTHY` (SH3, SH4).
- The NVMe Unexpected Power Losses count (labelled Unsafe Shutdowns) is lifetime and narrow; the journal-boot plane, not this counter, dates abrupt boot ends (SH6; wave-1 ScoutJournalBoots found five of five completed retained boots without a persisted final shutdown record, one of them a proven orderly reboot, so a missing record is not an unsafe shutdown).

## Adjacent

Disk-space runway stays with mori (`mori-shokunin/PROVINCE.md`, `SURFACE disk`); wave-1 ConnSiblingOverlap found no sibling that owns btrfs integrity or NVMe health. The kernel-journal reads here are OS triage, not fleet correlation (PROVINCE row ADJ-04).

## Limits

- One capture, one host, one device. Counter persistence across mounts is from the source, not observed (all counters are 0).
- The sysfs and ioctl counters agree here only trivially (all 0); their identity rests on S133 and S132.
- NOCOW file data (systemd journals) is outside scrub; which files carry NOCOW on this host was not measured.
- Whether the SSD deduplicates the `dup` metadata copies is not observable from the host.
- No census arm reads these signals yet; until one exists the area stays frontier (`PROVINCE.md`).
