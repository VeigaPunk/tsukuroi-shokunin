source: S237 S240 S241 (rows in `corpus/SOURCES.md`; S237 is the round-42 snapshot `.ufo/waves/round-42/frozen/src/scrub.c`, sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801; S240 is `.ufo/waves/round-43/frozen/src/ioctl.c`, digest in its `SHA256SUMS`, fetch log `FETCH.txt`; S241 is the host capture `.ufo/waves/round-43/frozen/hostcap/capture.txt`, sha256 f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556)
verified-at: 2026-10-26 (btrfs-progs tag v7.1, peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b; Linux tag v7.2.11, peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea; host btrfs-progs 7.1-1, kernel 7.2.11-arch1-1; capture 2026-10-26T21:51:26Z)
recheck: on-release — re-fetch the URLs in `.ufo/waves/round-42/frozen/src/FETCH.txt` and `.ufo/waves/round-43/frozen/src/FETCH.txt` and compare `sha256sum` with each `SHA256SUMS`; re-run `bash .ufo/waves/round-43/frozen/hostcap/capture.sh <file>` (unprivileged, read-only); `python3 tools/check-scrub-record-r43.py --revision <REV>`

# The btrfs scrub record, re-grounded: write discipline, resume, and who can see a running scrub (round 43)

Scope: the storage-integrity frontier, scrub record line (`PROVINCE.md` Frontier; `corpus/README.md` `## Frontier`).
Round 42 (`corpus/knowledge/btrfs-scrub-record-r42.md`) withdrew two of its rows after its counted reads: SC1 (the
"never half-written" sentence) and SC3 (the "(or is resumed)" and "only the final write reports a failure"
sentences). Its appended "Corrections — round-42 wave 2" section put seat-written replacement text in their place,
read by no counted seat, and it stated the running-state limit (SC4 narrowing) from a host errno alone. This entry
re-grounds those three points as rows, each read against the pinned source lines: SR1 replaces SC1's write-discipline
sentence, SR3 replaces SC3's start/resume and failure-report sentences, SR6 grounds the running-state limit in the
kernel source. Rows SC2, SC4 (as narrowed) and SC5 (as narrowed) of the round-42 entry are not restated here.
Nothing here runs a scrub, writes `/var/lib/btrfs` or calls a privileged ioctl.

## SR1

**Statement.** Every record update goes through `scrub_write_progress`: it opens `scrub.status.<fsid>_tmp` with
`O_WRONLY|O_CREAT` and no `O_TRUNC` (mode 0600, then a non-blocking `flock` `LOCK_EX`), writes the whole record
from the start of that file, and renames `_tmp` over `scrub.status.<fsid>` only when the write returned no error; a
failed write skips the `rename`. No code in `scrub.c` removes a `_tmp` file: its three `unlink` calls all name the
progress socket path. So a `_tmp` left behind by a failed write, a failed `rename` or a killed writer is opened again
by the next update, and when the new record is shorter, the old file's bytes past the new end stay in place and are
renamed into the record with it [inference from the open flags; not reproduced on this host].

**Quote.** `S237` scrub.c:517: "return scrub_open_file(datafile, O_WRONLY|O_CREAT);"

**Quote.** `S237` scrub.c:483: "fd = open(datafile, m, 0600);"

**Quote.** `S237` scrub.c:487: "ret = flock(fd, LOCK_EX|LOCK_NB);"

**Quote.** `S237` scrub.c:917: "fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");"

**Quote.** `S237` scrub.c:922: "err = scrub_write_file(fd, fsid, data, n);"

**Quote.** `S237` scrub.c:925: "err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");"

**Quote.** `S237` scrub.c:534: "ret = rename(datafile_old, datafile_new);"

**Quote.** `S237` scrub.c:1485: "ret = unlink(sock_path);"

**Host reading.** Not observable on this host: there is no record directory (`var_lib_btrfs absent`, capture.txt:7).

## SR3

**Statement.** `btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`. For each device whose
last record is canceled or unfinished, resume makes that record the device's `resumed` source, and every record
write passes each device through `scrub_resumed_stats` (in `scrub_write_file`), which for such a device writes the
earlier record's progress counters added to the new run's, the earlier record's `t_start`, and the two durations
summed. So the first record a resume writes for a resumed device carries the interrupted run's counters and start
time; only a fresh `start` (no `resumed` source) writes zero counters. Once that first record is written, a failed
progress-record write ends the progress thread with its error, which is printed ("recording progress failed") only
when `do_print` is set, and a failed final write prints "failed to record the result" under the same condition.
`do_print` is false by default, set by `-B`, and cleared again when output is quiet. Neither branch assigns the
command's `err` status.

**Quote.** `S237` scrub.c:1833: "return scrub_start(cmd, argc, argv, true);"

**Quote.** `S237` scrub.c:1434: "sp[i].resumed = last_scrub;"

**Quote.** `S237` scrub.c:864: "use = scrub_resumed_stats(&data[i], &local);"

**Quote.** `S237` scrub.c:823: "dest->stats.t_start = data->resumed->stats.t_start;"

**Quote.** `S237` scrub.c:1502: "/* write all-zero progress file for a start */"

**Quote.** `S237` scrub.c:1698: "error("recording progress failed: %m");"

**Quote.** `S237` scrub.c:1706: "error("failed to record the result: %m");"

**Quote.** `S237` scrub.c:1249: "bool do_print = false;"

**Quote.** `S237` scrub.c:1295: "do_print = true;"

**Quote.** `S237` scrub.c:1333: "do_print = false;"

**Host reading.** Not observable on this host: there is no record to resume from (capture.txt:7).

## SR6

**Statement.** Whether a scrub is running comes only from the kernel: `btrfs scrub status` calls
`is_scrub_running_in_kernel`, which issues `BTRFS_IOC_SCRUB_PROGRESS` once per device and answers 1 only when a call
returns 0; any failed call, whatever its errno, reads as not running. In Linux v7.2.11 that ioctl
(`btrfs_ioctl_scrub_progress`) returns `-EPERM` before doing anything else unless the caller has `CAP_SYS_ADMIN`, as
do the scrub start and cancel ioctls. So for an unprivileged caller the status command's `in_progress` is always 0:
its `btrfs scrub status` never prints `running`, and a census running as the user cannot learn from the kernel
whether a scrub is in progress.

**Quote.** `S237` scrub.c:1200: "ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);"

**Quote.** `S237` scrub.c:1201: "if (!ret)"

**Quote.** `S237` scrub.c:1946: "in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);"

**Quote.** `S237` scrub.c:341: "(ss->in_progress ? "running" :"

**Quote.** `S240` ioctl.c:5582: "case BTRFS_IOC_SCRUB_PROGRESS:"

**Quote.** `S240` ioctl.c:3126: "static long btrfs_ioctl_scrub_progress(struct btrfs_fs_info *fs_info,"

**Quote.** `S240` ioctl.c:3132: "if (!capable(CAP_SYS_ADMIN))"

**Quote.** `S240` ioctl.c:3133: "return -EPERM;"

**Quote.** `S240` ioctl.c:3072: "if (!capable(CAP_SYS_ADMIN))"

**Quote.** `S240` ioctl.c:3120: "if (!capable(CAP_SYS_ADMIN))"

**Host reading.** As uid 1000 with no effective capabilities (capture.txt:2), the ioctl on `/` for devid 1 failed
with `EPERM` (capture.txt:6), and `btrfs scrub status /` exited 0 printing `no stats available` (capture.txt:8,
capture.txt:10); with no record (capture.txt:7) the summary prints no status word at all.

## How this changes OS triage

- A record that fails to parse after a failed or killed write is a leftover `_tmp` tail, not a device fault
  [inference] (SR1); `scrub.status.<fsid>_tmp` lying beside the record is the sign.
- After `btrfs scrub resume`, the record's counters and start time are cumulative over the interrupted run and the
  resume (SR3); do not subtract a previous reading.
- A scrub started without `-B` (the default) fails to record silently; only `-B` runs show recording errors (SR3).
- An unprivileged reader can never see `running`; a user-level census reads the record's absence or its mode-0600
  refusal, never the kernel's running state (SR6). Running state is an elevation-gated reading.

## Limits

- Upstream behaviour is pinned at btrfs-progs v7.1 and Linux v7.2.11 source lines. The Arch btrfs-progs 7.1-1
  build applies no patch (round-42 wave-1 C2ExecLiveSources); whether the Arch kernel 7.2.11-arch1-1 patches
  `fs/btrfs/ioctl.c` is not checked here, and the host `EPERM` (S241) is consistent with the upstream line.
- SR1's trailing-bytes consequence is read from the open flags and was not reproduced (no record exists on this
  host and no scrub is run).
- No census arm reads the record; this entry stays on Frontier ground.
