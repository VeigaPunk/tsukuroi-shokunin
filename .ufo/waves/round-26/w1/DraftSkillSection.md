# Draft — `## Storage integrity — round 26` (SKILL.md append text)

Seat: `TsukuroiR26.DraftSkillSection` (scribe, wave 1). Status: draft text only. Nothing in this
file has been written to `SKILL.md`; the L1 owns the append. Every fact below is taken from the
frozen round-26 capture `.ufo/waves/round-26/capture/capture.txt` (sha256
`002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`, header timestamp
`2026-10-22T13:39:52Z`, capture script `.ufo/waves/round-26/capture/capture.sh`) or from the
round-26 sources named in the declaration (S128 to S138). Anything not in one of those two is
marked `[unk]` or `[inf]`.

## Part A — paste-ready section text

```markdown
## Storage integrity — round 26

Authority: detection and report only, from `corpus/knowledge/storage-health-r26.md` and its JSON
twin `corpus/knowledge/storage-health-r26.json` (round-26 capture
`.ufo/waves/round-26/capture/capture.txt`, sha256
`002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`, produced once by the L1 at
2026-10-22T13:39:52Z by `.ufo/waves/round-26/capture/capture.sh`; counting command
`python3 tools/check-storage-health.py --revision <REV>`, field `verified_rows`). The entry holds
the normative detail and the source quotes; the table below is the reading rule. Nothing in this
section starts a scrub, resets an error counter, enables a timer or changes a package. This lane
never runs `btrfs scrub start`, never runs `btrfs device stats -z` or `--reset`, never enables
`btrfs-scrub@.timer`, never writes `/etc` or `/var/lib/btrfs`, and never touches the LUKS mapping.
The privileged reads used here are exactly the round-26 read-only allow-list: `sudo -n btrfs
device stats <mountpoint>` without `-z`, `sudo -n btrfs scrub status <mountpoint>`, `sudo -n
smartctl -H -A <device>` without `-i`/`-t`/`-s`/`-X`, `sudo -n nvme smart-log <device>`, and
`sudo -n journalctl --no-pager` with read options.

Host frame of the capture: the root filesystem is btrfs on LUKS, `/dev/mapper/root` on
`/dev/nvme0n1p2`, one device, with `/home`, `/var/cache/pacman/pkg` and `/var/log` as btrfs
subvolumes of the same filesystem (capture lines 20 to 23 for the subvolumes, lines 29 to 33 for
the LUKS device). Installed versions: `btrfs-progs 7.1-1`, `smartmontools 7.5-2`, `nvme-cli
`3.1-1`, `systemd 262-1`, `linux 7.2.11` (capture lines 12 to 16). The healthy and non-healthy
columns describe a reading, not a verdict word: the per-row verdicts (`HEALTHY`, `DEGRADED`,
`BLOCKED`, `UNVERIFIED`) live in the entry and its JSON twin.

| id | signal | read-only command | healthy reading | what a non-healthy reading means | operator action | entry pointer |
|---|---|---|---|---|---|---|
| SH1 | The five btrfs per-device error counters — write, read, flush, corruption and generation — reported twice under two names: the sysfs file `error_stats` and the `btrfs device stats` ioctl. | `cat /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats`; `sudo -n btrfs device stats /` | All five counters are 0 in both views. Capture line 40 (`write_errs 0`) with lines 41 to 44 (`read_errs 0`, `flush_errs 0`, `corruption_errs 0`, `generation_errs 0`) and capture line 112 (`write_io_errs`) with lines 113 to 116 (`read_io_errs`, `flush_io_errs`, `corruption_errs`, `generation_errs`); the two views carry the same five counters under different field names. | A non-zero counter names a class of failure that already happened under the filesystem: a failed write, read or flush to the block device, a block checksum mismatch or corrupted metadata header (`corruption_errs`), or a block generation that did not match the expected value (`generation_errs`) [S128]. The counter says that the class occurred, never when. | Record the counter class and the device path, then read the kernel error line (E1) and the NVMe health reading (SH5) before drawing a conclusion. Never reset the counter: a reset destroys the only persistent record. | `corpus/knowledge/storage-health-r26.md` (row SH1) |
| SH2 | The same counters are a persistent record, not a dated event. | The two SH1 reads at mount time; `sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep "BTRFS.*errs: wr"`; `sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep "forced readonly"`; the capture's third kernel grep covers `BTRFS error`, `BTRFS critical` and `BTRFS warning` (capture lines 157 to 159) | Counters read 0 and no per-error kernel line was found over the 6 retained boots: capture line 155 reads `0` for the device-error grep and capture line 158 reads `0` for the broader grep, with capture line 161 reading `6` for the retained boot count. The current boot shows 7 BTRFS kernel lines and all of them are informational (capture lines 167 to 173). | The counters keep a persistent record of error classes and are printed at mount time, so a value survives a remount and only an explicit reset (`btrfs device stats -z`) clears it [S128]. A non-zero counter with no matching kernel line is therefore an undated past incident; the dated evidence is the kernel's own per-error line (E1) [S132, S133 — attribution pending those two snapshots; this seat did not open them]. | Never reset a counter to make the reading look clean. Search the journal for the matching kernel line to date the incident; a counter that rose with no kernel line is `[unk]` and is reported as undated. | `corpus/knowledge/storage-health-r26.md` (row SH2) |
| SH3 | What a scrub verifies and when it can repair, decided by the block group profiles: data is `single`, metadata and system are `dup`, on a single-device filesystem. | `ls /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/allocation/data` (and the same for `metadata` and `system`); `sudo -n btrfs scrub status /` | The data allocation directory carries the `single` marker (capture line 64) and the metadata and system directories carry the `dup` marker (capture lines 79 and 100). `single` data keeps one copy; `dup` metadata on a single device keeps a second logical copy [S130]; on an SSD the physical independence of that second copy is not guaranteed by the profile, and DUP is not a backup [S130]. | A scrub verifies checksums of the data and metadata it reads, and its automatic repair applies only to block groups that have redundancy [S129]. With the data profile `single` a data checksum mismatch is detected but cannot be repaired, so it is reported as uncorrectable, while a metadata error can be repaired from the `dup` copy [inf from S129 and S130]. | Read the scrub error summary classes (`csum`, `super`, `verify`, `read`) with the `Corrected` and `Uncorrectable` counts [S129] and report them with the affected profile. Never start a scrub to test a theory: scrub start is an operator-owned write. | `corpus/knowledge/storage-health-r26.md` (row SH3) |
| SH4 | This host's scrub record and the shipped scrub timer. | `sudo -n btrfs scrub status /`; `sudo -n ls -la /var/lib/btrfs`; `systemctl is-enabled btrfs-scrub@-.timer`; `systemctl cat btrfs-scrub@.timer` | A healthy reading is a completed scrub with a recorded status. This host has none: capture line 121 reads `no stats available`, capture line 127 records `/var/lib/btrfs` absent with exit 2, capture line 131 reads `disabled` for `btrfs-scrub@-.timer` with exit 1 and capture line 134 reads `inactive` with exit 3, while the installed unit is monthly (`OnCalendar=monthly`, capture lines 136 to 149). | There is no evidence that stored data has been verified end to end on this host [inf]. The `Error summary: no errors found` line at capture line 124 is the empty-record default and is not a clean bill of health. `fstrim.timer` is enabled (capture line 151) but discard maintenance is not verification. | Report the absence of a scrub record and the disabled timer. Enabling the shipped monthly timer and running a first scrub are operator-owned decisions; this lane never enables a timer and never starts a scrub. | `corpus/knowledge/storage-health-r26.md` (row SH4) |
| SH5 | How `smartctl` derives the NVMe overall-health result and which fields it prints next to it. | `sudo -n smartctl -H -A /dev/nvme0n1`; `sudo -n nvme smart-log /dev/nvme0n1` | `SMART overall-health self-assessment test result: PASSED` (capture line 181) with `Critical Warning: 0x00` (capture line 184), `Available Spare: 100%` against `Available Spare Threshold: 10%` (capture lines 186 and 187), `Percentage Used: 2%` (capture line 188) and `Media and Data Integrity Errors: 0` (capture line 197). | `smartctl` prints the overall-health line from the critical warning byte alone: the byte zero gives `PASSED`, any other value gives `FAILED!`, and the reason is named per bit — available spare below threshold `0x01`, temperature out of range `0x02`, NVM subsystem reliability degraded `0x04`, media placed in read only mode `0x08`, volatile memory backup device failed `0x10`, persistent memory region read-only or unreliable `0x20` [S134]. A non-zero critical warning is a hard failure even when spare, percentage used and media errors look good, and it also sets smartctl's exit status to `FAILSTATUS` (source line 842) [S134]. | Read the reason bullets that `smartctl` prints under the `FAILED!` line, then read the lifetime counters (SH6) and the btrfs counters (SH1). The printed spare, percentage-used and media-error attributes are attributes, not the verdict; only the critical warning byte decides the overall-health line, and spare below threshold is what raises bit `0x01`. | `corpus/knowledge/storage-health-r26.md` (row SH5) |
| SH6 | The NVMe lifetime counters are cumulative over the device's life, not dated incidents. | `sudo -n smartctl -H -A /dev/nvme0n1`; `sudo -n nvme smart-log /dev/nvme0n1` | `Power Cycles: 325` (capture line 194), `Unsafe Shutdowns: 200` (capture line 196), `Media and Data Integrity Errors: 0` (capture line 197), `Error Information Log Entries: 0` (capture line 198) and `Power On Hours: 1,855` (capture line 195); the `nvme smart-log` view repeats the same values at capture lines 221 to 225. | These are totals since the drive was first powered, not events [S134; the lifetime-counter semantics are S135's primary definition, not opened by this seat]. A rising unsafe-shutdown count is a device-lifetime fact and never dates an incident; a dated incident needs the kernel line (E1) or the device's own error information log. | Compare against the previous capture and report the delta; a delta that moved is a finding, the absolute total is not. Never describe a cumulative counter as an incident and never reset one. | `corpus/knowledge/storage-health-r26.md` (row SH6) |

### Error patterns

- **E1 — kernel device error line.** A kernel line of the form `BTRFS error (device ...): bdev ...
  errs:` — the btrfs per-device error report naming the block device and the error classes it
  counted. Action: ERROR. The counters it prints are the dated incident; capture the whole line
  and the boot it belongs to, and read the same class in the two SH1 views. The capture's own
  greps are `BTRFS.*errs: wr` (capture lines 154 to 156) and
  `BTRFS (error|critical|warning)|forced readonly` (capture lines 157 to 159); the round-26
  capture counted 0 such lines over the 6 retained boots (capture lines 155 and 161).
- **E2 — forced readonly.** A kernel line containing `forced readonly`: the filesystem was
  remounted read-only after an error. Action: ERROR. Treat the filesystem as suspect — while it
  is read-only no write is accepted, and the write that failed is the one to date [inf] — and
  capture the whole line. Never remount it read-write. The round-26 capture counted 0 such lines
  over the 6 retained boots (capture lines 158 and 161).
- **E3 — NVMe health failure.** The `SMART overall-health self-assessment test result:` line
  reading `FAILED!` instead of `PASSED`, or a `Critical Warning:` byte other than `0x00`. Action:
  ERROR. Record the byte and the reason bullets `smartctl` prints under it [S134], then read the
  lifetime counters (SH6) and the btrfs counters (SH1). A device reporting media or data
  integrity errors is a replacement candidate, not something to scrub around or reset.

Recheck: after any kernel, btrfs-progs, smartmontools or firmware change, and after any storage
incident. Run `bash .ufo/waves/round-26/capture/capture.sh <new-output-file>`, point the entry's
capture pointers at the new capture, and re-run
`python3 tools/check-storage-health.py --revision <commit>`. A live re-capture needs an explicit
read-only authorization; a committed gate count does not grant it. Re-check the NVMe lifetime
counters as a delta against the previous capture, never as an absolute reading.
```

## Part B — the new registry row, and the operative table it belongs to

The round-25 registry table (heading `## Gate and probe registry — round25 superseding current
rows`, SKILL.md line 2322 at the claim base `e9f5356c`) has 28 body rows. `tools/check-registry-coverage.py`
makes the unique highest `## Gate and probe registry — round<N> superseding current rows` table
operative, so round 26 needs a new table with all 28 round-25 rows carried forward plus the new
row below. The round-25 table stays in place as historical.

New row (8 cells, same shape as the round-25 rows; the row names exactly one tool path, and the
`--selftest` literal must exist in that tool's source or the gate raises
`REGISTRY-SELFTEST-UNRESOLVED`):

```markdown
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
```

One carried-forward row needs an update, because the round-26 tool measures a different fixed
check set. The round-25 `self-assessment` row reads, in its pinned-values cell, "R25 fixed check
set K01 to K23 read at the bound revision; a measured self-assessment only, never a host
verdict". For the round-26 table that cell should read "R26 fixed check set K01 to K27 read at
the bound revision; a measured self-assessment only, never a host verdict". This is a wording
change in one cell of one carried-forward row; the L1 owns it.

## Part C — notes the L1 needs before the append

1. **Capture pointers that qualify.** A counted pointer is a line number plus a token of at least
   three characters, on a line whose text occurs exactly once in the capture and which is not a
   `### ` header, not a `$ ` command echo and not an `[exit ` line. In this capture the lines
   `155`, `158` and `161` read only `0`, `0` and `6`; their text is not unique, so they are
   supporting citations by line number only, exactly as the round-25 entry did for its
   text-identical lines. The counted pointers usable in the SKILL text are lines 40 to 44
   (`write_errs 0` and friends), 64 (`single`), 79 and 100 (`dup`, cited by line number only,
   because the text `dup` occurs twice), 112 to 116 (`write_io_errs` and friends), 121
   (`no stats available`), 124 (`no errors found`), 127 (`No such file`), 131 (`disabled`), 134
   (`inactive`), 151 (`enabled`), 181 (`PASSED`), 184 (`0x00`), 186 (`100%`), 187 (`10%`), 188
   (`Percentage Used`), 194 (`325`), 195 (`1,855`), 196 (`200`), 197 (`Integrity`), 198
   (`Information`), and the seven current-boot kernel lines 167 to 173.
2. **Capture line map used above.** header 1 to 17 (timestamp at line 3, kernel release at line
   9, package versions at lines 12 to 16); root filesystem 18 to 34; sysfs error counters 36 to
   45; allocation profiles 46 to 110; `btrfs device stats` 111 to 117; scrub status 118 to 128;
   scrub timer 129 to 152; kernel journal 153 to 174; `smartctl` 175 to 204; `nvme smart-log` 205
   to 237; footer 238 to 241.
3. **Profile evidence.** The `single` and `dup` markers are the only profile evidence in the
   capture. Reading a marker file named after the profile as the statement of that profile is
   the sysfs semantics of S133 (`fs/btrfs/sysfs.c`), which this seat did not open; until the
   source seat lands that snapshot the attribution is `[unk]` here and the entry must mark it
   the same way. The `dup` marker means two metadata copies on one device, which is also the
   `mkfs` default for metadata on a single-device filesystem [S130]; the capture does not itself
   show the `mkfs` command line that created the filesystem, so the profile is read from the
   live allocation directories, not from a creation record.
4. **SH5 nuance worth keeping.** The declaration text lists critical warning, available spare
   against its threshold, percentage used and media errors as the fields that "decide" the
   overall-health result. In smartmontools 7.5 the overall-health line is decided by the critical
   warning byte alone; the other three are printed as attributes, and available spare below
   threshold is what the device reports in critical warning bit `0x01` [S134]. The draft above
   states the source behaviour and marks the declaration wording as the looser reading, so the
   entry and this table do not contradict each other.
5. **SH3 repair semantics are an inference.** `btrfs-scrub.rst` states that automatic repair
   applies to block group profiles with redundancy [S129] and `mkfs.btrfs.rst` states that
   `single` has no redundancy while `DUP` has two copies on one device [S130]. The statement
   that a data checksum error under `single` is detected but not repairable is the combination
   of those two, and is marked `[inf]`. The entry seat should keep the same marking.
6. **`btrfs device stats -c`** is documented to add 64 to the exit status when a counter is
   non-zero [S128], which would be a convenient one-command check. It is not inside this round's
   sudo allow-list, which allows `sudo -n btrfs device stats <mountpoint>` only, so the draft
   does not use it and it is `[unk]` as a host-permitted read this round.
7. **The `-z` reset is forbidden.** `btrfs device stats -z` resets the counters [S128]; the
   allow-list forbids it and this lane never runs it. The SKILL text therefore says "never reset
   the counter" in SH1 and SH2 and repeats it in the SH6 action.
8. **Self-assessment line counts.** Appending Part A and a new registry table changes the
   `SKILL.md` line count and the pipe-line count that the K08 and K09 checks measure
   (`tools/check-self-assessment.py`), so the SCORECARD depth row must be restated at the
   revision that adds the section. Measured at the claim base `e9f5356c`: `SKILL.md` is 2355
   lines (`wc -l`) with 297 pipe-prefixed lines. Part A as drafted adds 58 lines, of which 8 are
   pipe-prefixed (one header, one separator, six SH rows). The round-26 registry section adds a
   heading, one prose paragraph and the 31-line table, of which 31 lines are pipe-prefixed.
   A plain concatenation of Part A and Part E therefore lands at 2355 + 58 + 33 = 2446 lines
   with 297 + 8 + 31 = 336 pipe-prefixed lines; the exact figures depend on the blank lines the
   L1 places around the two blocks, and must be measured after the append, not assumed.
9. **Nothing in this draft was executed against the host.** No command from the table was run
   during this seat; every reading quoted above comes from the frozen capture, and every source
   statement comes from the files listed in Part D.
10. **The declared S131 location cannot be honoured as written.** The declaration names
    "btrfs-progs v7.1 units/btrfs-scrub@.timer"; the sibling source seat records that the
    upstream v7.1 tree ships no systemd unit at all and that the bytes come from the Arch
    packaging repository (packaging tag 7.1-1, sha256
    `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad`, byte-identical to the
    installed `/usr/lib/systemd/system/btrfs-scrub@.timer`). The SOURCES row for S131 must state
    that true location; SH4 in this section leans only on the installed unit, which the capture
    already holds at lines 136 to 149, so the section text does not depend on the correction.
11. **The declared SH5 wording is looser than the source.** The declaration lists critical
    warning, available spare against its threshold, percentage used and media errors as the
    fields that "decide" the overall-health result. In smartmontools 7.5 the verdict is the
    critical warning byte alone; spare reaches it only through bit `0x01`, and percentage used
    and media errors never reach it at all (the sibling S134 seat reports the same limit).
    This section states the source behaviour so that the entry and the table do not contradict
    each other; the L1 should decide whether the declaration wording stays as it is or is
    narrowed in the entry.

## Part D — sources I opened read-only for this draft (no snapshot written; the source seats own
the committed snapshots)

I did not write any file under `.ufo/waves/round-26/sources/` (that path belongs to the source
seats). The bytes below are what I fetched into
`/fast/scratch/hyaku/tsuku26/DraftSkillSection/` for reading only; the entry's counted quotes
must be taken from the committed snapshot, and its sha256 goes in the SOURCES anchor cell.

| round-26 id | upstream file I fetched | fetch url | sha256 of my copy | line ranges used |
|---|---|---|---|---|
| S128 | `Documentation/btrfs-device.rst`, btrfs-progs v7.1 | `https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git/plain/Documentation/btrfs-device.rst?h=v7.1` | `0d4f425a49c1483f1cc598695d9a456e6d5542e5c59df4946fd471e5d4f7a0e6` | 127 to 158 (options), 226 to 272 (DEVICE STATS) |
| S129 | `Documentation/btrfs-scrub.rst`, btrfs-progs v7.1 | `https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git/plain/Documentation/btrfs-scrub.rst?h=v7.1` | `7900b474aebfee2be79ff168c750f282ee33803ee6914928c20117a24aefe3f0` | 73 to 92 (start), 175 to 200 (status summary) |
| S130 | `Documentation/mkfs.btrfs.rst`, btrfs-progs v7.1 | `https://git.kernel.org/pub/scm/linux/kernel/git/kdave/btrfs-progs.git/plain/Documentation/mkfs.btrfs.rst?h=v7.1` | `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769` | 42 to 80 (profile options), 506 to 560 (PROFILES table), 632 to 660 (DUP chapter) |
| S131 | the shipped `btrfs-scrub@.timer` unit | not fetched by this seat: the declared upstream path `units/btrfs-scrub@.timer` and `units/btrfs-scrub@.timer.in` both return 404 at `h=v7.1` in the kernel.org cgit tree, and the sibling source seat records that upstream btrfs-progs v7.1 ships no systemd unit at all; the bytes come from the Arch packaging repository | — | the installed unit is host truth in the capture at lines 136 to 149; the sibling seat records the packaged file at sha256 `9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad`, byte-identical to `/usr/lib/systemd/system/btrfs-scrub@.timer` |
| S134 | `smartmontools/nvmeprint.cpp`, smartmontools `RELEASE_7_5` | `https://codeload.github.com/smartmontools/smartmontools/tar.gz/refs/tags/RELEASE_7_5` (member `smartmontools-RELEASE_7_5/smartmontools/nvmeprint.cpp`) | `4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98` | 448 to 482 (critical warning and the verdict byte), 486 to 540 (health information log) |
| S132, S133, S135 | kernel `fs/btrfs/volumes.c`, `fs/btrfs/sysfs.c`, NVMe SMART/Health log definition | not fetched by this seat | — | used only as the attribution for SH2 and SH6; the source seats own the bytes |

Cross-check with the sibling source seats: `SrcSmartNvmeprint.md` records the same sha256
`4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98` for
`.ufo/waves/round-26/sources/S134.cpp` (tag `RELEASE_7_5`, path `smartmontools/nvmeprint.cpp`,
959 lines), so my copy and the committed snapshot are the same bytes and the quote candidate
below matches the snapshot. That seat also records that the file lives under
`smartmontools/nvmeprint.cpp`, not at the repository root, and that a non-zero critical warning
sets `FAILSTATUS` in smartctl's exit status (source line 842), which is why SH5 names it.
`SrcBtrfsProfilesDoc.md` records the same sha256 `ce7c0cbca90eda4bc84040e9f5a43c227bd02d77bd50b006e481f19d918de769`
for `.ufo/waves/round-26/sources/S130.rst` (723 lines) and four ready quotes at its lines 518,
520, 635 to 636 and 639 to 640; its finding that DUP is a second logical copy whose physical
independence on a single SSD is not guaranteed is what bounds the SH3 wording above.
`SrcBtrfsScrubUnit.md` records that the declared S131 upstream path never existed and that the
shipped unit comes from the Arch packaging repository, byte-identical to the installed file.

Quote candidates (each at most 25 words, taken from the bytes above; the entry seat must copy
them from the committed snapshot, not from this table):

- S128: "The device stats keep persistent record of several error classes related to doing IO."
- S128: "Since kernel 5.14 the device stats are also available in textual form in"
- S129: "The automatic repairs of damaged copies are performed by default for block group profiles with redundancy."
- S129: "Uncorrectable -- errors detected at read time but not possible to repair from other copy"
- S130: "Default on a single device filesystem is *DUP* and is recommended for metadata in general."
- S134: `(!w ? "PASSED" : "FAILED!")` — the code that turns the critical warning byte into the
  overall-health word.

## Part E — the round-26 operative registry table (generated, not hand-copied)

Generated mechanically from the round-25 table at the claim base so that no cell was retyped by
hand. The L1 pastes this after the round-25 registry table.

<!-- BEGIN GENERATED ROUND26 TABLE -->

```markdown
## Gate and probe registry — round26 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round25 row is retained verbatim, including its pinned values and its write scope, except the
two cells of the `self-assessment` row named below; round26 adds the storage-health claim
instrument. A self-test flag is resolved against the committed tool source at the bound revision,
not against this prose. Selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
```

Two cells of one carried-forward row change, because the round-26 tool measures a different
fixed check set: the `self-assessment` verdict-map cell reads `0 all 27 fixed checks match`
instead of `0 all 23 fixed checks match`, and its pinned-values cell reads `R26 fixed check
set K01 to K27` instead of `R25 fixed check set K01 to K23`. Every other round25 row is byte
identical to the round25 table.

The table is 31 pipe lines: one header, one separator, the 28 round25 body rows and the one
new `storage-health` row. `tools/check-registry-coverage.py` requires that a row name exactly
one committed tool path, that a gate verdict map publish the codes 0, 1 and 2, and that the
`--selftest` literal in the self-test cell exist in the tool source; the storage-health row
satisfies the first two by construction and the third only if the checker implements
`--selftest`.

<!-- END GENERATED ROUND26 TABLE -->

## Part F — what this seat did not do

- Did not write to `SKILL.md`, `corpus/`, `SCORECARD.md`, `corpus/SOURCES.md` or any lane file
  outside `.ufo/waves/round-26/w1/DraftSkillSection.md` and the seat scratch directory.
- Did not run any host command from the table: the readings come from the frozen capture, and
  the source statements come from the files listed in Part D.
- Did not open S132, S133 or S135; the SH2 and SH6 attributions to them are carried from the
  declaration and are marked `[unk]` here until the source seats land their snapshots.
- Did not create the entry, the JSON twin or the checker: those are the `DraftEntry`,
  `ExecStorageChecker` and L1 seats.
