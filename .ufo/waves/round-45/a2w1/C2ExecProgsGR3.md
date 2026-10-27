VERDICT: supports

# C2-5 — the btrfs-progs side of GR3: what `scrub start -B` does after SIGINT

Seat: C2ExecProgsGR3 (executor, wave a2w1). Item: trace the SIGINT path of a foreground
`btrfs scrub start -B` in the pinned btrfs-progs v7.1 `scrub.c`
(`S237` = `.ufo/waves/round-42/frozen/src/scrub.c`, sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`,
verified in this seat against `tools/check-scrub-grounding-r45.py` `SNAP`); decide whether
`SIGCONT` is harmless and whether the process has one copy of the signal per thread; and test
whether GR3's `[inference]` ("whether the start writes its canceled record within the 5 s") is the
honest boundary.

Bottom line: the progs trace holds in every particular, the row's `[inference]` is honest as to
*duration* and should stay, but the source **does** decide the **ordering**, the **atomicity** and
the **shape** of the record a SIGKILL can leave — so the row's bracket is under-specified, not
wrong. Exact replacement text and verified quotes are in §5. `SIGINT` is delivered **once to the
one process**, not once per thread (§3). `SIGCONT` is harmless (§2).

All line numbers below are `S237` unless prefixed `k:` (kernel Linux v7.2.11
`.ufo/waves/round-44/frozen/src/scrub.c` = `S242`) or `i:` (kernel
`.ufo/waves/round-43/frozen/src/ioctl.c`).

## 1. The trace, in execution order

1. **`-B` is a foreground, single-process mode.** `-B` sets `do_background = false; do_wait =
   true; do_print = true;` (`scrub.c:1292-1295`). The only `fork()` in the start path is inside
   `if (do_background)` (`scrub.c:1512-1544`), so for `-B` that whole branch — parent
   `scrub_handle_sigint_parent()` (`:1522`), `wait()` (`:1530`) — is skipped: the `-B` start is
   **one process** and the "child" code below `:1546` is that process itself.
2. **First record, before any thread exists.** `if (do_record)` writes the all-zero record
   (`scrub.c:1501-1510`, `sp` is `calloc`'d at `:1402` and `t_start` is only set later at
   `:1557-1558`, so this record carries `t_start=0 duration=0 canceled=0 finished=0` and zero
   counters). This is *before* the handler is installed.
3. **The handler is installed for the whole process** at `scrub.c:1546`
   (`scrub_handle_sigint_child(fdmnt);`) → `sigaction(SIGINT, {.sa_handler =
   scrub_sigint_record_progress}, NULL)` with `sa_flags` 0 and `cancel_fd = fdmnt`
   (`scrub.c:436-443`). The handler body is `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)`
   (`:421`), `perror("Scrub cancel failed")` on error (`:422-423`). **Before `:1546` the
   disposition is still `SIG_DFL`**: a SIGINT that lands in the window between exec and `:1546`
   (which includes the first record write) kills the start outright, with no cancel and no new
   record.
4. **Threads.** One `scrub_one_dev` thread per non-skipped device (`scrub.c:1565-1566`), each
   running `ioctl(sp->fd, BTRFS_IOC_SCRUB, &sp->scrub_args)` (`:965`), then on return setting
   `sp->ret`, `sp->stats.duration`, `sp->stats.canceled = !!ret`, `sp->ioctl_errno`
   (`:967-970`) and `sp->stats.finished = 1` under `progress_mutex` (`:971-976`); plus
   `scrub_progress_cycle` (`:1585`), which wakes on a 5 s `poll()` timeout (`:1043`), queries each
   device with `BTRFS_IOC_SCRUB_PROGRESS` (`:986`) and writes a record every iteration
   (`:1121-1126`) — or answers a `btrfs scrub status` client over the progress socket
   (`:1104-1119`). The **main** thread writes back the old `scrub_speed_max` (`:1596-1603`) and
   then parks in `pthread_join` per device (`:1608`): that is where the process waits.
5. **SIGINT → handler → cancel.** `SIGINT` (process-directed, once — §3) runs the handler, which
   issues `BTRFS_IOC_SCRUB_CANCEL`. Kernel path: `i:5580-5581` dispatch →
   `btrfs_ioctl_scrub_cancel` (`i:3118-3124`, `capable(CAP_SYS_ADMIN)` then
   `btrfs_scrub_cancel(fs_info)`) → `k:3277-3296`: if `scrubs_running` is 0 it returns
   `-ENOTCONN` at once (`k:3280-3284`), otherwise it `atomic_inc(&fs_info->scrub_cancel_req)`
   (`k:3285`) and **waits** `while (atomic_read(&fs_info->scrubs_running))` (`k:3286-3290`) before
   dropping the request (`k:3292`). The cancelled scrub observes the request in
   `should_cancel_scrub`, `if (atomic_read(&fs_info->scrub_cancel_req) || ...) return -ECANCELED`
   (`k:2081-2083`), checked at the top of each `queue_scrub_stripe` iteration
   (`k:2321-2323`) and per RAID56 full stripe (`k:2176-2178`). **So the handler does not return
   until the kernel has finished tearing the scrub down**, and `scrubs_running` is decremented at
   the end of `btrfs_scrub_dev` (`k:3211-3212`) — a few instructions before the ioctl copies its
   args back to user space (`i:3093-3110`, whose comment names `-ECANCELED` explicitly). One
   cancel covers **every** device ioctl of the filesystem, because `scrub_cancel_req` lives on
   `fs_info`, not on a device or a thread.
6. **How they return.** `BTRFS_IOC_SCRUB` runs `btrfs_scrub_dev` **synchronously in the calling
   thread** (`i:3093-3095`) and returns `-ECANCELED` with the partial progress copied out
   (`i:3097-3110`), so each device thread returns from `:965` with `ret = -1`,
   `ioctl_errno = ECANCELED`, `stats.canceled = 1` (`:969`), `stats.finished = 1` (`:974`).
7. **The main thread's join loop.** `case ECANCELED: ++err;` (`:1626-1628`) — deliberately silent,
   no message. The `do_print` block then marks the run canceled because `sp[i].ret` is set
   (`:1671-1672`) and prints `scrub %s for %s` with `append = "canceled"` (`:1679`). Then
   `pthread_cancel(t_prog)` + `pthread_join` (`:1685-1687`); the cycle sets
   `PTHREAD_CANCEL_ASYNCHRONOUS` (`:1021`), so it dies in `poll()` or right after the one write during
   which `scrub_write_progress` had cancellation disabled (`:905`, SR1) — a short, bounded join.
8. **Where the final record is written.** `if (do_record)` → `scrub_write_progress(...)`
   (`:1701-1708`) → `scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp")` (`:917`),
   `scrub_write_file` (`:922`), `scrub_rename_file(..., "tmp")` (`:925`) =
   `rename("/var/lib/btrfs/scrub.status.<fsid>_tmp", "/var/lib/btrfs/scrub.status.<fsid>")`
   (path built by `scrub_datafile` at `:446-476` from `#define SCRUB_DATA_FILE
   "/var/lib/btrfs/scrub.status"` at `:67`; rename at `:520-535`). This is the **last** thing the
   start writes: after it come only `scrub_handle_sigint_child(-1)` (handler back to `SIG_DFL`,
   `:1710`, via `:436-443`), the `out:` cleanup and `if (err) return 1;` (`:1725-1726`).
   Citation nit for the item text: the *write discipline* (tmp + `rename`, no `O_TRUNC`) is
   **SR1** of `btrfs-scrub-record-r43.md`; **SR3** is the resume/record-content row. The
   "where the final record is written" question is answered by SR1 plus `:1701-1708`.
9. **Exit status.** A canceled `-B` start exits **1** (`err` set at `:1627`, returned at
   `:1725-1726`), after printing `scrub canceled for <fsid>` (`:1671-1672`, `:1679`). The unit sets
   no `Type=` (`S244:1-10`, so the `systemd.service` default `Type=simple` applies); what systemd
   records for a stop-killed `Type=simple` process is not pinned by any frozen source here and is
   not claimed.

## 2. `SIGCONT` — harmless

- The row's own source: `S248` `systemd.kill.xml:114` — "Note that, right after sending the
  signal specified in this setting, systemd will always send SIGCONT, to ensure that even
  suspended tasks can be terminated cleanly."
- `scrub.c` installs no `SIGCONT` handler (`grep -n SIGCONT scrub.c` → no match; the only
  `SIGINT` sites are `:431`, `:443`). `SIGCONT`'s default action is "Continue if stopped"
  (`man 7 signal` table, `/usr/share/man/man7/signal.7.gz` line 362: `SIGCONT P1990 Cont
  Continue if stopped`; owned by `man-pages 6.19-1`), so for a **running** scrub process it is a
  no-op: it cannot be blocked, cannot be caught here, cannot perturb `SIGINT`'s disposition and
  cannot un-cancel anything.
- Empirical analogue (uid 1000, one process, 3 threads blocked in a blocking syscall, main thread
  in `pthread_join`; receipt `a2w1/C2ExecProgsGR3/sigshape-run.out`): with an **observing**
  `SIGCONT` handler installed — the stricter case, since the real code has none — the blocked
  reads had not returned by the time `SIGINT` was sent
  (`done_before_SIGINT=0 (SIGCONT did not abort the blocked reads)`), `SIGCONT` was delivered once
  (`sigcont_observer_invocations=1`), and with `SIG_DFL` restored a second `SIGCONT` left the
  process running (`alive_after_default_SIGCONT=1`).
- Residual: `SIGCONT` is *also* a process-directed signal; if it ever arrived while the process
  were group-stopped it would resume it, which is what systemd intends.

## 3. One process, one delivery — not one handler run per thread

- For `-B` there is exactly one process (§1.1) and `N+1` threads (one per device, the progress
  thread, the initial thread). `sigaction` is process-wide (`:443`), so **whichever** thread runs
  the handler performs the same filesystem-wide cancel, and **one** cancel covers all device
  ioctls (§1.5: `scrub_cancel_req` is on `fs_info`, `k:2081`). No device is left uncancelled for
  want of its own signal.
- Empirical analogue, same receipt: one process, three threads blocked in a syscall, main thread
  in `pthread_join`, handler installed exactly as `:438-443` (`sa_flags = 0`), one
  `kill(getpid(), SIGINT)`:
  `sigint_handler_invocations=1 sigint_handler_tid=2616825 (main_tid=2616825)` — one handler run,
  on the **group-leader** thread, not once per thread — and
  `device_reads_returned=3 of 3` with `read_ret=1` on each: the single cancel released all three
  blocked threads. Re-run reproduced the same shape (`sigshape-run2.out`).
- `[inference]` (kernel `signal.c` is not in any frozen set): because the leader is the thread
  parked in `pthread_join`/`write_scrub_device_limit` and nothing in `scrub.c` blocks `SIGINT`,
  the leader takes the signal. The pathological alternative — delivery to a device thread — would
  only run the handler *after* that thread's ioctl returned, i.e. the cancel would be late; for a
  single-device filesystem it then finds `scrubs_running == 0` and prints the handler's
  `perror("Scrub cancel failed")` (`:422-423`, `ENOTCONN`). Nothing in the service path produces
  that (systemd sends one `KillSignal`, `S248:108-116`).

## 4. The GR3 boundary — honest as an `[inference]`, but the bracket can be decided

The row keeps *"Whether the start then writes its canceled record (SR3) within the 5 s before
SIGKILL is not established [inference: a start killed before that write leaves the record as it
was last written during the run]"*. Assessment, in three parts:

- **Duration — not decidable, keep the `[inference]`.** The wait in `btrfs_scrub_cancel`
  (`k:3286-3290`) is a `wait_event` with **no timeout**, and the scrub only observes the request
  between queued stripe groups (`k:2321`), after `flush_scrub_stripes` has waited for that group's
  reads (`k:1974-1979`). A device whose in-flight read does not return keeps the start **inside
  the SIGINT handler** until systemd's `SIGKILL`. No pinned line bounds that latency, so "within
  5 s" is genuinely inference — but the inference is about the **kernel unwind**, not about
  progs' scheduling, the join, or the rename.
- **Ordering — decidable, and the row should state it.** Because the cancel ioctl blocks until
  `scrubs_running == 0` (`k:3285-3292`, decrement `k:3211`), the handler returns only after the
  scrub runs have left with `ECANCELED`; the start's next userspace steps are then join
  (`:1608`), the `ECANCELED` branch (`:1626-1628`), progress-thread cancel+join (`:1685-1687`) and
  the final record write (`:1701-1708`), after which it only deregisters the handler and exits 1.
  There is **no unbounded userspace wait** between "kernel finished" and "record written" (§1.7).
- **What "as it was last written during the run" can be — decidable.** The record is published by
  `rename` (SR1), so a SIGKILL can never leave a torn record; it leaves the previous atomic
  record, which is either (a) the start's own all-zero record (`:1501-1510`, `t_start=0` because
  `:1557` has not run yet, `canceled=0 finished=0`), or (b) a periodic record at most one 5 s
  `poll` cycle old (`:1043`, `:1121-1126`) — refreshed sooner if a `btrfs scrub status` client
  connected (`:1104-1119`). Shape (a) is exactly what progs itself calls stale
  ("Check for stale information in the status file, ie. if it's" / "canceled=0, finished=0 but no
  scrub is running.", `:1375-1376`, acted on at `:1378-1379`) and exactly what
  `is_scrub_running_on_fs` treats as *running* (`:1184`). That is the concrete triage hazard the
  row's note gestures at, and it is source-decided.
- **One edge the row omits (source-decided):** the handler exists only from `:1546`, while the
  first record is written at `:1501`; a SIGINT that lands in that window (exec → handler
  installed) is `SIG_DFL` and kills the start with no cancel and **no new record at all**, leaving
  the previous run's record — a second way to get a record without a `canceled` mark.

## 5. Proposed replacement text (exact)

Replace, in `corpus/knowledge/btrfs-scrub-grounding-r45.md` `## GR3` `**Statement.**`, exactly
this sentence:

```
SIGINT reaches the
foreground start's handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9). Whether the start then writes its
canceled record (SR3) within the 5 s before SIGKILL is not established [inference: a start killed before that write
leaves the record as it was last written during the run].
```

with:

```
SIGINT reaches the
foreground start's handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9), and that ioctl does not return until the
kernel has torn the scrub down: `btrfs_scrub_cancel` sets the filesystem's cancel request and waits for
`scrubs_running` to reach 0 (S242 scrub.c:3285-3290), a counter decremented as `btrfs_scrub_dev` finishes
(:3211), so each device's `BTRFS_IOC_SCRUB` returns `ECANCELED` first, and the start's remaining userspace work
is the device join (:1608), the `ECANCELED` branch (:1626-1628), the progress thread's cancel and join
(:1685-1687) and the final record write (:1701-1708) before it exits 1 (:1726) — no unbounded userspace wait sits between
the kernel's unwind and that write. Whether the start writes its canceled record (SR3) within the 5 s before
SIGKILL is not established [inference: the wait in :3286 has no timeout, and cancel is observed only between queued
stripe groups (:2321) after that group's reads complete (S242 scrub.c:1974-1979), so a device whose in-flight read
does not return keeps the start inside the handler until SIGKILL; on a healthy device that is one stripe group's
I/O, not a source-bounded value]. What such a SIGKILL leaves is decided: the record is published by `rename`
(SR1), so it is never torn, only the start's own last atomic record — either the all-zero first record (:1501-1510,
written before `t_start` is set at :1557, `canceled=0 finished=0`) or a periodic record at most one 5 s poll cycle
old (:1043, :1121-1126); the first shape is what the start itself treats as stale (:1375-1379) and what
`is_scrub_running_on_fs` treats as running (:1184). A second, narrower window exists before the handler is
installed at :1546 and after the first record is written at :1501: a SIGINT there is the default action, so the
start dies with no cancel and no new record.
```

Quotes to add to the row (each verified in this seat with the counter's own `quote_good()` against the
digest-checked snapshots — every line below passes; of my 21 candidates only the two-line comment at
`:1375-1376` failed the "at least half the line" rule, so it is quoted in prose above, not as a `**Quote.**`
line. `S242` is already a known snapshot, and the existing
`S237` window 412-424 quote at `:421` is untouched, so the row's quote requirements and all seven proposition
tokens (`KillSignal`, `SIGINT`, `control-group`, `SIGCONT`, `SIGKILL`, `DefaultTimeoutStopSec`, `5 s`) still
hold):

```
**Quote.** `S237` scrub.c:1546: "scrub_handle_sigint_child(fdmnt);"
**Quote.** `S237` scrub.c:965: "ret = ioctl(sp->fd, BTRFS_IOC_SCRUB, &sp->scrub_args);"
**Quote.** `S237` scrub.c:969: "sp->stats.canceled = !!ret;"
**Quote.** `S237` scrub.c:1608: "ret = pthread_join(t_devs[i], NULL);"
**Quote.** `S237` scrub.c:1626: "case ECANCELED:"
**Quote.** `S237` scrub.c:1702: "ret = scrub_write_progress(&spc_write_mutex, fsid, sp,"
**Quote.** `S237` scrub.c:1726: "return 1;"
**Quote.** `S237` scrub.c:1043: "ret = poll(&accept_poll_fd, 1, 5 * 1000);"
**Quote.** `S237` scrub.c:1378: "if (!is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices))"
**Quote.** `S237` scrub.c:1184: "if (!(sfr->stats.finished || sfr->stats.canceled))"
**Quote.** `S242` scrub.c:3285: "atomic_inc(&fs_info->scrub_cancel_req);"
**Quote.** `S242` scrub.c:3286: "while (atomic_read(&fs_info->scrubs_running)) {"
**Quote.** `S242` scrub.c:3211: "atomic_dec(&fs_info->scrubs_running);"
**Quote.** `S242` scrub.c:2321: "ret = should_cancel_scrub(sctx);"
**Quote.** `S242` scrub.c:2081: "if (atomic_read(&fs_info->scrub_cancel_req) ||"
```

If the row must stay short, the three that carry the new content are `S242` `:3286`, `S242` `:3211`
and `S237` `:1608`; the record-shape sentences then lose their quotes and should instead be
paraphrased as `[inference from SR1]`.

Optional, for the "How this changes OS triage" bullet: replace *"A scrub record left without a
`canceled` mark after a stop is therefore possible [inference]"* with

```
A scrub record left without a `canceled` mark after a stop is possible and has a decided shape: the
start's all-zero first record (`canceled=0 finished=0`, `t_start=0`), which the next `btrfs scrub start`
re-reads and treats as stale, or a record at most one 5 s poll cycle old (GR3).
```

## 6. Adjacent, cross-row: the same cancel ioctl can abort a device replace

Not part of GR3 and not a GR3 defect, reported because it is a host-plane consequence the entry's
triage section does not carry.

- `btrfs scrub cancel` (the standalone subcommand, `cmd_scrub_cancel`, `scrub.c:1773-1800`) issues
  the same `BTRFS_IOC_SCRUB_CANCEL` (`:1792`) with **no** check for a running replace.
- A replace's copy *is* a scrub (`S247` dev-replace.c:700-703, `is_dev_replace = true`), and
  `should_cancel_scrub` tests `fs_info->scrub_cancel_req` unconditionally (`S242` :2081), so the
  replace's copy obeys the cancel too.
- Consequence: `btrfs_dev_replace_finishing` then writes
  `dev_replace->replace_state = scrub_ret ? BTRFS_IOCTL_DEV_REPLACE_STATE_CANCELED : ...`
  (`S247` dev-replace.c:926-928), skips the mapping-tree swap and destroys the target device
  (`:946-958`). So a `btrfs scrub cancel` during a replace **ends the replace as CANCELED and
  discards the target**.
- The *service-stop* path is not that route: a `-B` start cannot be running its scrub during a
  replace — the kernel refuses it with `EINPROGRESS` (GR2, `S242` :3146-3153) — so its SIGINT
  handler's cancel either finds no scrub (harmless `ENOTCONN`) or cancels a scrub that cannot
  coexist with a replace. The hazard is the operator subcommand (or any other caller of the
  ioctl), not `systemctl stop btrfs-scrub@…`.

## 7. Host readings (read-only; nothing started, stopped, cancelled or written)

- `btrfs --version` → `btrfs-progs v7.1` (`-EXPERIMENTAL -INJECT -STATIC +LZO +ZSTD +UDEV
  +FSVERITY +ZONED CRYPTO=libgcrypt`), matching the pinned `S237` tag; the host build is the one
  the r43 entry's Limits pin (no patch).
- `ls -ld /var/lib/btrfs` → **`No such file or directory`**: this host has no scrub record file at
  all, so the record view cannot be observed here (SR1's trailing-bytes and SR3's content stay
  source-read).
- `btrfs scrub status /home/vgpnk/Projects/shokunin` (read-only query) → `UUID:
  1d02a454-c549-4a35-b567-89d60902af8e`, `no stats available`, `Total to scrub: 301.13GiB`,
  `Rate: 0.00B/s`, `Error summary: no errors found`, `rc=0` — i.e. absent record and no
  permission to see kernel state as uid 1000 (SR6), consistent with the row's host block.
- `journalctl --no-pager -n 5 -u 'btrfs-scrub@*'` → `Failed to add filter for units: No data
  available`; nothing to read, no stop of this service ever happened in this journal.
- No tool was installed or upgraded (no package, `uv`, `npx` or binary channel used).

## 8. What this seat did **not** do

- Started, stopped, resumed or cancelled no scrub; called no privileged ioctl; ran no
  `btrfs replace`; wrote no sysfs attribute; touched no unit. `/var/lib/btrfs` does not exist on
  this host, so no record was read or produced.
- Did not measure the cancel latency (the 5 s question): that needs a scrub on this host as root
  and, for the interesting case, a stalled device. The claim that the wait is unbounded is from
  `k:3286-3290` (no timeout) and `k:2321`/`k:1974-1979` (cancel polled between stripe groups),
  not from a measurement.
- The signal-shape receipts are a Linux/POSIX analogue (one process, N+1 threads, one blocking
  call per thread), not btrfs-progs itself: `btrfs scrub start -B` cannot be exercised unprivileged.
- Did not run the frozen C1 or C2 counters (another seat owns them; the C2 counter is not
  affected by this report, which touches no lane file).

## Receipts

- `a2w1/C2ExecProgsGR3/sigshape.c` — the analogue source (compiled `cc -O0 -pthread`).
- `a2w1/C2ExecProgsGR3/sigshape-run.out` — first run, uid 1000, 2026-10-27T03:30:44Z.
- `a2w1/C2ExecProgsGR3/sigshape-run2.out` — repeat run.
- Scratch `/fast/scratch/hyaku/tsukuroi-r45/C2ExecProgsGR3/` removed at end of seat.
