source: S128, S129, S130, S131, S132, S133, S134, S135 and S139 in `corpus/SOURCES.md` (btrfs-progs v7.1 `Documentation/btrfs-device.rst`, `btrfs-scrub.rst`, `mkfs.btrfs.rst` and `ch-scrub-intro.rst`; Arch packaging `btrfs-progs` 7.1-1 `btrfs-scrub@.timer`; Linux v7.2 `fs/btrfs/volumes.c` and `fs/btrfs/sysfs.c`; smartmontools 7.5 `smartmontools/nvmeprint.cpp`; NVM Express Base Specification 2.4 SMART / Health Information log page), plus the read-only host capture `.ufo/waves/round-26/capture/capture.txt` (sha256 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd).
verified-at: 2026-10-22 (capture header 2026-10-22T13:39:52Z; kernel 7.2.11-arch1-1, btrfs-progs 7.1-1, smartmontools 7.5-2, nvme-cli 3.1-1)
recheck: `python3 tools/check-storage-health.py --revision <REV>` for the evidence links; re-run `.ufo/waves/round-26/capture/capture.sh <out>` (read-only) for the host readings; re-open the sources on a btrfs-progs, kernel or smartmontools release. A live re-capture needs an explicit read-only authorization; a committed gate count does not grant it.

# Storage integrity: btrfs device errors, scrub and NVMe health (round 26)

## Scope

This entry opens a frontier area of the OS substrate: whether the root filesystem and its device can detect, record and repair data corruption, and how to read the signals. It covers the btrfs per-device error counters, the scrub record this host keeps, what the block group profiles allow scrub to repair, and the NVMe SMART / Health log as smartctl reports it. It does not cover disk-space runway (mori's surface), filesystem repair, scrub runs, counter resets, timer enablement or firmware updates (all operator actions). Machine-readable twin: `corpus/knowledge/storage-health-r26.json`.

Host at capture time: root is btrfs on LUKS (`/dev/mapper/root` on `nvme0n1p2`), one device, data profile `single`, metadata and system `dup`, mount options include `discard=async`.

Verdict words are `HEALTHY | DEGRADED | BLOCKED | UNVERIFIED` as in `SKILL.md` §Verdict vocabulary, applied to each row's reading of this host. Every action below is operator-owned: the lane never scrubs, never resets a counter and never enables a timer.

## SH1

**Statement.** btrfs keeps five per-device IO error counters: write_io_errs (failed writes), read_io_errs (failed reads), flush_io_errs (failed FLUSH writes), corruption_errs (a block checksum mismatch or a corrupted metadata header) and generation_errs (a block generation that does not match the expected value). The sysfs file devinfo/<devid>/error_stats prints the same five counters read by the same kernel function under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs), and the btrfs device stats query reads them through an ioctl.

**Host reading.** One device (devid 1, /dev/mapper/root on nvme0n1p2). All five counters are 0 in sysfs (capture lines 40-44) and all five are 0 through the ioctl (capture lines 112-116).

**Verdict.** `HEALTHY`

**Action.** None. Read the counters with cat /sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats (no privilege needed) or btrfs device stats <mountpoint>. Never pass -z or --reset: the reset is destructive to the record and is an operator decision.

**Sources.** S128, S133, S132. Quotes: S128 (btrfs-device.rst line 254): "corruption_errs"; S128 (btrfs-device.rst line 255): "A block checksum mismatched or a corrupted metadata header was found."; S128 (btrfs-device.rst line 260): "Since kernel 5.14 the device stats are also available in textual form in"; S133 (fs/btrfs/sysfs.c line 2074): "static ssize_t btrfs_devinfo_error_stats_show(struct kobject *kobj,"; S132 (fs/btrfs/volumes.c line 8490): "stats->values[i] = btrfs_dev_stat_read(dev, i);".

**Capture pointers.** line 40 (`write_errs`), line 43 (`corruption_errs`), line 112 (`write_io_errs`), line 115 (`corruption_errs`).

## SH2

**Statement.** The five counters are a persistent cumulative record, not dated events. The kernel loads them from the btrfs device tree at mount and writes changed values back at transaction commit, and clears them only through an explicit reset, which it logs. The same bdev ... errs: wr ..., rd ..., flush ..., corrupt ..., gen ... text is printed twice: at error level when an error is counted (rate limited), and at info level at mount when any stored counter is non-zero. Only the error-level line dates an increment; the info-level line replays the stored total.

**Host reading.** All five counters are 0, so no mount-time line is printed. The journal greps count 0 errs: wr lines and 0 BTRFS error, critical, warning or forced-readonly lines over the 6 retained boots (capture lines 154-161); the 7 BTRFS kernel lines of the current boot are all informational (lines 167-173). Persistence across mounts is not observable on all-zero counters; it rests on the source.

**Verdict.** `HEALTHY`

**Action.** When a counter is non-zero, search every retained boot's kernel journal for the error-level errs: line to date the errors, and read an info-level mount-time line as the stored total rather than a new incident. The lane never resets a counter; resetting is operator-owned.

**Sources.** S132, S128. Quotes: S132 (fs/btrfs/volumes.c line 8352): "called from commit_transaction. Writes all changed device stats to disk."; S132 (fs/btrfs/volumes.c line 8429): ""bdev %s errs: wr %u, rd %u, flush %u, corrupt %u, gen %u","; S132 (fs/btrfs/volumes.c line 8446): "return; /* all values == 0, suppress message */"; S128 (btrfs-device.rst line 231): "The device stats keep persistent record of several error classes related to".

**Capture pointers.** line 41 (`read_errs`), line 116 (`generation_errs`).

## SH3

**Statement.** Scrub reads all filesystem data and metadata and checks their checksums, and it repairs a damaged copy only by copying a verified good copy from another replica of the same block group profile. With the data profile single there is one copy, so a data checksum error is detected and reported as uncorrectable rather than repaired. Metadata with the dup profile has two logical copies on the same device and can be repaired from the second, but an SSD may store both as one physical copy, so dup is not a backup. File data carrying the NOCOW attribute has no checksums and is not verified at all; systemd sets that attribute on journal files by default.

**Host reading.** The data allocation directory carries the single marker (capture line 64) and the metadata and system directories carry the dup marker (capture lines 79 and 100). One device, one NVMe SSD under LUKS. Which files on this host carry NOCOW was not measured.

**Verdict.** `DEGRADED`

**Action.** Read this as limited self-repair rather than a fault: a data checksum error on this host can be found but not fixed from a replica, so backups are the repair path for file data. Changing the data profile is an operator decision and is not proposed here. The lane never starts a scrub.

**Sources.** S139, S130, S129. Quotes: S139 (ch-scrub-intro.rst line 13): "On filesystems that use replicated block group profiles (e.g. RAID1), read-write"; S139 (ch-scrub-intro.rst line 14): "scrub will also automatically repair any damage by copying verified good data"; S139 (ch-scrub-intro.rst line 24): "be validated and corrected by scrub, the actual file data is not."; S130 (mkfs.btrfs.rst line 639): "For example, a SSD drive can remap the blocks internally to a single copy--thus"; S129 (btrfs-scrub.rst line 190): "*  *Uncorrectable* -- errors detected at read time but not possible to repair from other copy"; S130 (mkfs.btrfs.rst line 635): "The mkfs utility will let the user create a filesystem with profiles that write".

**Capture pointers.** line 64 (`single`).

## SH4

**Statement.** No scrub record exists on this host for the root filesystem: btrfs scrub status / reports that there are no statistics, and /var/lib/btrfs, the directory where btrfs-progs keeps the scrub.status.UUID file, does not exist. The packaged monthly btrfs-scrub@.timer is present, but its instance for / is disabled and inactive. Ordinary reads verify checksums, so data that has been read has been checked, but nothing on this host records a full verification pass over stored data.

**Host reading.** no stats available (capture line 121); /var/lib/btrfs absent (line 127); btrfs-scrub@-.timer disabled (line 131) and inactive (line 134); the installed unit is monthly (lines 139-148). The Error summary: no errors found line printed beside no stats available (line 124) is not a health reading: it belongs to statistics of a last finished or cancelled scrub, and this host has none.

**Verdict.** `UNVERIFIED`

**Action.** Operator decision: run btrfs scrub start / once, or enable btrfs-scrub@.timer. The lane never starts a scrub and never enables a timer. After a scrub, read btrfs scrub status / for the csum, verify, read and super error classes and the corrected versus uncorrectable split.

**Sources.** S139, S131, S129. Quotes: S139 (ch-scrub-intro.rst line 71): "The scrubbing status is recorded in :file:`/var/lib/btrfs/` in textual files named"; S139 (ch-scrub-intro.rst line 68): "recommended period is a month but it could be less."; S139 (ch-scrub-intro.rst line 17): "Such automatic repair is also carried out when reading metadata or data from a"; S131 (btrfs-scrub@.timer line 5): "OnCalendar=monthly"; S129 (btrfs-scrub.rst line 133): "Show status of a running scrub for the filesystem identified by *path*".

**Capture pointers.** line 121 (`no stats available`), line 127 (`/var/lib/btrfs`), line 131 (`disabled`), line 142 (`OnCalendar=monthly`).

## SH5

**Statement.** smartctl 7.5 derives the NVMe overall-health line from one byte: it prints PASSED when the controller's Critical Warning byte is zero and FAILED! otherwise, and then names the warning bits it sees, of which bit 0x01 means available spare has fallen below its threshold. Available Spare, Percentage Used and Media and Data Integrity Errors are printed beside the verdict but are not inputs to it, and the conditions that set the reliability bit are controller-defined.

**Host reading.** PASSED with Critical Warning 0x00 (capture lines 181, 184); Available Spare 100% against threshold 10% (lines 186-187), Percentage Used 2% (line 188) and Media and Data Integrity Errors 0 (line 197).

**Verdict.** `HEALTHY`

**Action.** Read the Critical Warning byte and the other fields separately: a PASSED result does not mean wear or media errors were judged. Watch Percentage Used, spare against its threshold and media errors as their own signals, with sudo smartctl -H -A <device> (read-only; never -t, -s or -X).

**Sources.** S134, S135. Quotes: S134 (smartmontools/nvmeprint.cpp line 451): "(!w ? "PASSED" : "FAILED!"));"; S134 (smartmontools/nvmeprint.cpp line 459): "jout("- available spare has fallen below threshold\n");"; S134 (smartmontools/nvmeprint.cpp line 840): "print_critical_warning(smart_log.critical_warning);".

**Capture pointers.** line 181 (`PASSED`), line 184 (`0x00`), line 187 (`Available Spare Threshold`), line 188 (`Percentage Used`).

## SH6

**Statement.** The NVMe SMART / Health log reports information over the life of the controller, retained across power cycles. Power Cycles, Unexpected Power Losses (the field smartctl and nvme-cli still label Unsafe Shutdowns), Media and Data Integrity Errors and Number of Error Information Log Entries are lifetime counts, not dated events. Unexpected Power Losses increments only when main power is lost while the controller had not reported itself ready to power off, so it is not a count of host-visible crashes.

**Host reading.** Power Cycles 325, Unsafe Shutdowns 200, Media and Data Integrity Errors 0 and Error Information Log Entries 0 (capture lines 194, 196-198); nvme-cli reads the same values at lines 221, 223-225. Only 6 boots are retained in the journal, so almost none of the 200 can be dated from it.

**Verdict.** `HEALTHY`

**Action.** Take two dated reads of the same counter to see whether it grew in a window, and correlate growth with the journal boot list before naming any cause. A high lifetime ratio alone is not a fault; report it as context. This entry adds to the lane's journal-boot plane by naming the counter as a lifetime total beside the boot list, not by dating any shutdown.

**Sources.** S135, S134. Quotes: S135 (NVM Express Base Specification 2.4, SMART / Health Information log page, excerpt line 14): "the life of the controller and is retained across power cycles unless otherwise specified."; S135 (excerpt line 258): "Note that this field was previously named Unsafe Shutdowns."; S135 (excerpt line 276): "Entries over the life of the controller."; S134 (smartmontools/nvmeprint.cpp line 528): "jout("Unsafe Shutdowns:                   %s\n", le128_to_str(buf, smart_log.unsafe_shutdowns));".

**Capture pointers.** line 194 (`Power Cycles`), line 196 (`Unsafe Shutdowns`), line 197 (`Media and Data Integrity Errors`), line 198 (`Error Information Log Entries`), line 223 (`unsafe_shutdowns`).

## Adjacent

- The journal-boot plane stays where it is: the NVMe lifetime counters (SH6) are undated device totals, while `corpus/knowledge/journal-boot-plane.md` holds the dated per-boot records. This entry adds the counter to that plane as a lifetime total beside the boot list, and dates nothing. Wave-1 ScoutJournalBoots found five of five completed retained boots without a persisted final shutdown record, one of them a proven orderly reboot, so a missing record is not an unsafe shutdown; the entry makes no dated incident claim.
- Disk-space runway (`df` targets, free capacity, write-rate) is mori's surface (`mori-shokunin/PROVINCE.md`, `SURFACE disk`). Percentage Used and Data Units Written appear here as device-health facts only, never as a runway measure (wave-1 CritLearningFrontier, finding 6).
- No sibling lane declares btrfs integrity or NVMe health (wave-1 ConnSiblingOverlap); mori's `fs/btrfs/sysfs.c` row is the same file as S133 but a different proposition, so the rows stay separate.
- The kernel-journal reads here are OS triage, not fleet correlation (`PROVINCE.md` row ADJ-04).

## Limits

- One capture, one host, one device. Counter persistence across mounts rests on the source, not on an observation: every counter is 0 here.
- The sysfs and the ioctl view agree only trivially, because both are all-zero; their identity rests on S133 and S132, not on the capture.
- The `dup` metadata profile keeps two logical copies on one device; whether the SSD stores them as one physical copy is not observable from the host, and DUP is not a backup (S130).
- NOCOW file data (systemd journals) is outside scrub's data verification; which files on this host carry NOCOW was not measured.
- `btrfs scrub status` prints `Error summary: no errors found` beside `no stats available`; that line belongs to statistics of a last finished or cancelled scrub and is not a health reading.
- `smartctl`'s PASSED reflects one byte. Wear (Percentage Used), spare against its threshold and media errors are separate signals with no threshold defined in the sources.
- No census arm reads these signals yet; until one exists the area stays frontier (`PROVINCE.md`).
