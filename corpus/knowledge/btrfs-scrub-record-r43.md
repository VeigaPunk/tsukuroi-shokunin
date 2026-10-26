source: S237 S240 S241 (rows in `corpus/SOURCES.md`; S237 is the round-42 snapshot `.ufo/waves/round-42/frozen/src/scrub.c`, sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801; S240 is `.ufo/waves/round-43/frozen/src/ioctl.c`, digest in its `SHA256SUMS`, fetch log `FETCH.txt`; S241 is the host capture `.ufo/waves/round-43/frozen/hostcap/capture.txt`, sha256 f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556)
verified-at: 2026-10-26 (btrfs-progs tag v7.1, peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b; Linux tag v7.2.11, peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea; host btrfs-progs 7.1-1, kernel 7.2.11-arch1-1; capture 2026-10-26T21:51:26Z)
recheck: on-release — re-fetch the URLs in `.ufo/waves/round-42/frozen/src/FETCH.txt` and `.ufo/waves/round-43/frozen/src/FETCH.txt` and compare `sha256sum` with each `SHA256SUMS`; re-run `bash .ufo/waves/round-43/frozen/hostcap/capture.sh <file>` (unprivileged, read-only); `python3 tools/check-scrub-record-r43.py --revision <REV>`
extended-by: round 44 — rows SR7 (the success direction of the scrub-progress ioctl SR6 cites), SR8 (the per-device `scrub_speed_max` attribute) and SR9 (the packaged scrub timer and service) are in `corpus/knowledge/btrfs-scrub-record-r44.md`; the "Limits" sentence on SR1 is corrected in "Corrections — round 44" at the end of this file.

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

**Statement.** Every update of the record file goes through `scrub_write_progress` (its three call sites write the
first record, the progress thread's records and the final record): it opens `scrub.status.<fsid>_tmp` with
`O_WRONLY|O_CREAT` and no `O_TRUNC` (open mode argument 0600, subject to the umask; then a non-blocking `flock`
`LOCK_EX`), writes the whole record from the start of that file, and renames `_tmp` over `scrub.status.<fsid>` only
when the write returned no error; a failed write skips the `rename`. No code in `scrub.c` removes a `_tmp` file: its
three `unlink` calls all name the progress socket path. So a `_tmp` left behind by a failed write, a failed `rename`,
or a writer process killed between the open and the rename (for example by SIGKILL; the progress thread itself
disables cancellation from before the open until after the rename) is opened again by the next update; if that
update's write and rename succeed and the new record is shorter, the old file's bytes past the new end stay in place
and are renamed into the record with it [inference from the open flags; reproduced in a scratch harness compiled
from the pinned write path, round-43 wave-1 seat C2ExecTailRepro; not observed on this host].

**Quote.** `S237` scrub.c:517: "return scrub_open_file(datafile, O_WRONLY|O_CREAT);"

**Quote.** `S237` scrub.c:483: "fd = open(datafile, m, 0600);"

**Quote.** `S237` scrub.c:487: "ret = flock(fd, LOCK_EX|LOCK_NB);"

**Quote.** `S237` scrub.c:905: "ret = pthread_setcancelstate(PTHREAD_CANCEL_DISABLE, &old);"

**Quote.** `S237` scrub.c:917: "fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");"

**Quote.** `S237` scrub.c:922: "err = scrub_write_file(fd, fsid, data, n);"

**Quote.** `S237` scrub.c:925: "err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");"

**Quote.** `S237` scrub.c:534: "ret = rename(datafile_old, datafile_new);"

**Quote.** `S237` scrub.c:1485: "ret = unlink(sock_path);"

**Host reading.** Not observable on this host: there is no record directory (`var_lib_btrfs absent`, capture.txt:7).

## SR3

**Statement.** `btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`. For each device whose
record (`last_dev_scrub`) is canceled or unfinished, resume makes that record the device's `resumed` source; every
record write passes each device through `scrub_resumed_stats` (in `scrub_write_file`), which for such a device
writes the record's thirteen counted progress fields added to the new run's, the record's `t_start`, and the two
durations summed, while `last_physical`, `canceled` and `finished` come from the new run and `t_resumed` is taken
from the new run's `t_start`. So the first record a resume writes for a resumed device carries the interrupted run's
counters and start time. A device without a `resumed` source, or one that resume skips (`skip` set: its record is
finished and not canceled, or it has no record), passes through unchanged, and in a run's first record its counters are zero (`sp` is
zero-allocated); under a fresh `start` that is every device. Once the first record is written, a failed
progress-record write ends the progress thread with its error, which is printed ("recording progress failed") only
when `do_print` is set, and a failed final write prints "failed to record the result" under the same condition.
`do_print` is false by default, set by `-B`, and cleared again when output is quiet. Neither branch assigns the
command's `err` status.

**Quote.** `S237` scrub.c:1833: "return scrub_start(cmd, argc, argv, true);"

**Quote.** `S237` scrub.c:1434: "sp[i].resumed = last_scrub;"

**Quote.** `S237` scrub.c:864: "use = scrub_resumed_stats(&data[i], &local);"

**Quote.** `S237` scrub.c:803: "if (!data->resumed || data->skip)"

**Quote.** `S237` scrub.c:819: "_SCRUB_COPY(dest, data, last_physical);"

**Quote.** `S237` scrub.c:823: "dest->stats.t_start = data->resumed->stats.t_start;"

**Quote.** `S237` scrub.c:1436: "sp[i].skip = 1;"

**Quote.** `S237` scrub.c:1402: "sp = calloc(fi_args.num_devices, sizeof(*sp));"

**Quote.** `S237` scrub.c:1502: "/* write all-zero progress file for a start */"

**Quote.** `S237` scrub.c:1698: "error("recording progress failed: %m");"

**Quote.** `S237` scrub.c:1706: "error("failed to record the result: %m");"

**Quote.** `S237` scrub.c:1249: "bool do_print = false;"

**Quote.** `S237` scrub.c:1295: "do_print = true;"

**Quote.** `S237` scrub.c:1333: "do_print = false;"

**Host reading.** Not observable on this host: there is no record to resume from (capture.txt:7).

## SR6

**Statement.** In `btrfs scrub status`, whether a scrub is running comes only from the kernel: the command sets
`in_progress` once, from `is_scrub_running_in_kernel`, which issues `BTRFS_IOC_SCRUB_PROGRESS` device by device and
answers 1 on the first call that returns 0, and 0 only after every call failed, whatever the errno; the status word
`running` is printed only from `in_progress`. (Elsewhere, `btrfs scrub start` also reads an unfinished record and a
live progress socket as a running scrub; this row covers the status command.) In Linux v7.2.11 that ioctl
(`btrfs_ioctl_scrub_progress`) returns `-EPERM` before doing anything else unless `capable(CAP_SYS_ADMIN)` holds for
the caller, as do the scrub start and cancel ioctls (`capable()` tests the capability in the initial user namespace
[inference: `capable()` is defined outside the pinned file]). So for an unprivileged caller every call fails and
`in_progress` is 0: its `btrfs scrub status` never prints `running`, and a census running as the user cannot learn
from the kernel whether a scrub is in progress.

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

- `scrub.status.<fsid>_tmp` lying beside the record means an update failed or its writer died before the rename;
  a later, shorter update can carry that file's tail into the record (SR1).
- After `btrfs scrub resume`, a resumed device's counters and start time are cumulative over the interrupted run and
  the resume (SR3); do not add a previous reading to them.
- A default `btrfs scrub start` (no `-B`) still warns when the record directory cannot be created or the first record
  cannot be written (`status recording disabled`); later recording failures are printed only with `-B` (SR3).
- An unprivileged reader can never see `running`; a user-level census reads the record's absence or its mode-0600
  refusal, never the kernel's running state (SR6). Running state is an elevation-gated reading.

## Limits

- Upstream behaviour is pinned at btrfs-progs v7.1 and Linux v7.2.11 source lines. The Arch btrfs-progs 7.1-1
  build applies no patch (round-42 wave-1 C2ExecLiveSources). The Arch kernel 7.2.11-arch1-1 applies one patch,
  `linux-v7.2.11-arch1.patch.zst` (sha256 741d473c…, matching its PKGBUILD), which touches no file under `fs/`, so
  `fs/btrfs/ioctl.c` of the booted kernel is the pinned one (round-43 wave-1 seat C2ExecKernelPatch); the host
  `EPERM` (S241) agrees with the pinned line.
- SR1's trailing-bytes consequence is read from the open flags and was not reproduced (no record exists on this
  host and no scrub is run).
- No census arm reads the record; this entry stays on Frontier ground.

## Corrections — round 44

Appended 2026-10-26 (round-43 closure routed defect R43-SR1-LIMITS-CONTRADICTION, `corpus/lessons/round-43-verifier-spotcheck.md` §5 item 1); the text above stays as filed. The second "Limits" bullet ("SR1's trailing-bytes consequence is read from the open flags and was not reproduced") contradicts SR1's own statement and its evidence: the consequence was not observed on this host (no record exists and no scrub is run), but it was reproduced in a scratch harness compiled from the pinned write path, round-43 wave-1 seat C2ExecTailRepro (`.ufo/waves/round-43/w1/C2ExecTailRepro.md`, the relation `final = new_record || old_record[len(new_record):]` checked byte-wise there). Read that bullet as: "SR1's trailing-bytes consequence is inferred from the open flags and reproduced in a harness compiled from the pinned write path; it is not observed on this host (no record exists and no scrub is run)." `SKILL.md` "Scrub record re-grounded — round 43" already says "[inference, reproduced in a harness]" and `PROVINCE.md` carries no reproduction claim, so neither needs a correction.
