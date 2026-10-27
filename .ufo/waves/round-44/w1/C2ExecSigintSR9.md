VERDICT: supports

# C2ExecSigintSR9 — the `-B` SIGINT path and the canceled scrub record (S237, btrfs-progs v7.1)

Seat item C2-7. Question: in `cmds/scrub.c` v7.1 does a SIGINT to a foreground (`-B`) scrub
actually leave a record with `canceled` set, which code writes the final record, does the main
thread survive, is `SA_RESTART` set, is "a device whose scrub ioctl returns nonzero is recorded
with canceled set" exact, and does `resume` take it up (SR3)?

Method: static trace of the two frozen pins plus a compiled harness that includes the pinned
handler block verbatim. Nothing was run against btrfs: no `btrfs scrub` command, no ioctl on a
btrfs fd, no sysfs write, no unit change, no write to `/var/lib/btrfs` (absent on this host,
`frozen/hostcap/capture.txt:3`). Pins verified against their own `SHA256SUMS` (receipt
`hashes.txt`): r42 `scrub.c` = `48df2e2f…f0801` (v7.1 tag `0a919c7d…`, `frozen/src/FETCH.txt`),
r43 `ioctl.c` = `7b3488f2…4ba01`, r44 `scrub.c`/`sysfs.c`/units/PKGBUILD all OK.

## Short answer

Yes, with a precise chain. The SIGINT handler itself writes nothing to the record; it issues
`BTRFS_IOC_SCRUB_CANCEL`, **which blocks in the kernel until every running scrub has stopped**
(`fs/btrfs/scrub.c:3277-3295`). Each device thread's `BTRFS_IOC_SCRUB` then returns nonzero
(`-ECANCELED`), the worker sets `sp->stats.canceled = !!ret` (`cmds/scrub.c:969`) and
`finished = 1` (`:974`), and the **main thread**, after joining every worker and cancelling the
progress thread, writes the final record itself (`:1701-1703` → `scrub_write_progress` `:897-946`,
tmp file + `rename` `:508-536`, `canceled` field `:887`). The main thread survives: the disposition
installed at `:1546` is a handler, and on this kernel a process-directed SIGINT lands on the
leader (observed). `SA_RESTART` is **not** set for that handler (`:438-440`, observed
`sa_flags=0x04000000`); only the *parent* handler (not used by `-B`) sets it (`:430`). The
"nonzero → canceled" sentence is exact as a statement about the field, and `resume` does take it
up (`:1430-1434`), but `!!ret` is errno-blind, so `canceled=1` means "the scrub ioctl did not
return 0", not "a signal cancelled this device". Eight narrowings below, each with lines.

## 1. The `-B` pipeline, line by line

| step | evidence (S237 `cmds/scrub.c` v7.1) |
|---|---|
| defaults `do_background=true, do_wait=false, do_print=false, do_record=true` | `:1247-1250` |
| `-B` → `do_background=false; do_wait=true; do_print=true` | `:1292-1296` |
| record dir failure disables recording (`do_record=false`, warning) | `:1335-1338` |
| mount fd for every later ioctl (scrub, cancel, progress) | `:1343-1345`, `sp[i].fd = fdmnt` `:1429` |
| read past records; stale (`canceled=0, finished=0`) → `force` | `:1360-1370`, `:1375-1379` |
| resume predicate: `last_scrub->stats.canceled \|\| !last_scrub->stats.finished` → `start = last_physical`; else (resume) `skip=1` | `:1429-1437` |
| all-zero record written **before** the handler is armed | `:1501-1510` |
| `if (do_background)` fork block — skipped by `-B` (block spans the `if` at `:1512` to `:1544`) | `:1512-1544` |
| `scrub_handle_sigint_child(fdmnt)` — handler armed here | `:1546` |
| one `scrub_one_dev` thread per device; each enters `BTRFS_IOC_SCRUB` at `:965` | `:1548-1578`, `:965` |
| handler body: `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)`, `perror` on failure | `:416-424` |
| parent (not `-B`) handler: `SIG_IGN` + `SA_RESTART` | `:426-434` |
| child handler: `sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress`, **no `sa_flags`** | `:436-444` |
| worker: `ret = ioctl(fd, BTRFS_IOC_SCRUB, …)`, `sp->ret = ret`, `sp->stats.canceled = !!ret`, `ioctl_errno = errno`, `finished = 1` | `:965-974` |
| main: join each worker; switch on `ioctl_errno` (`ENODEV` → continue, `ECANCELED` → `++err`, default → error + `++err`) | `:1608-1640` |
| main: `pthread_cancel(t_prog)`, join, print `recording progress failed` if the thread returned an error | `:1685-1699` |
| **main: final record write** `scrub_write_progress(&spc_write_mutex, fsid, sp, num_devices)` | `:1701-1708` |
| handler disarmed (`-1` → `SIG_DFL`) only **after** the final write | `:1710` |
| exit: `err` → 1 (ECANCELED sets it), `nothing_to_resume` → 2 | `:1626-1627`, `:1725-1728` |

Kernel side (S242 `fs/btrfs/scrub.c` v7.2.11): cancel sets `scrub_cancel_req` and then
`wait_event(scrub_pause_wait, scrubs_running == 0)` before returning, `-ENOTCONN` if nothing is
running (`:3277-3295`); scrub loops notice it at check points via `should_cancel_scrub()` →
`-ECANCELED` (`:2077-2084`, `:2176-2178`, `:2321-2323`); progress is copied to userspace even on
error (`:3214-3215`, and `ioctl.c:3109-3110` copies the whole args struct unconditionally).

## 2. The four sub-questions

### 2.1 Is the record actually written with `canceled` set after SIGINT?

Yes, by this sequence, not by the handler:

1. signal → handler (`:417-424`) → `BTRFS_IOC_SCRUB_CANCEL`, which *waits* until
   `scrubs_running == 0` (kernel `:3285-3291`); it writes no record.
2. each worker's scrub ioctl returns `-ECANCELED` (kernel `:2321-2323`, returned by
   `btrfs_scrub_dev` at `:3247`), worker stores `ret`, `canceled = !!ret`, `finished = 1`
   (`:967-974`), and the kernel already copied its final progress into `sp->scrub_args`
   (kernel `:3214-3215`; `ioctl.c:3109-3110`).
3. main joins the workers (`:1608`), prints `scrub canceled for <fsid>` (`:1671-1672`, `:1679`), cancels
   and joins the progress thread (`:1685-1687`), then writes the record (`:1701-1703`).
4. `scrub_write_progress` disables cancellation for the whole call, takes the mutex, writes
   `/var/lib/btrfs/scrub.status.<fsid>_tmp`, renames onto `scrub.status.<fsid>`
   (`:905-940`, `:508-536`); the per-device line carries `|canceled:N` from
   `use->stats.canceled` (`:887`), and for a resumed device `scrub_resumed_stats` takes
   `canceled`/`finished` from the **new** run (`:820-821`), as SR3 states.

Caveat, not a contradiction: the periodic record written by the progress thread every ~5 s
(`:1043`, `:1121-1125`) can already carry `canceled=1` once the shared `finished` flag is set and
the progress ioctl answers `-ENOTCONN` (`:1085-1104`). Either way the flag comes from `:969`.

### 2.2 Which code writes the final record?

The **main thread of `scrub_start`**, at `:1701-1703`, via `scrub_write_progress` (`:897`),
`scrub_write_file` (`:843-891`), `scrub_open_file_w(..., "tmp")` (`:905`, `:508-518`) and
`scrub_rename_file(..., "tmp")` (`:908`, `:520-536`). Neither the SIGINT handler nor the worker
threads write the record.

### 2.3 Does the main thread survive the signal; is `SA_RESTART` set?

* Disposition is a handler, so no default terminate. Observed: with the pinned `:436-444`
  installer, a process-directed `SIGINT` while main was in `pthread_join` ran the handler and
  `pthread_join` returned 0 (receipt `run.log`).
* Delivery: a process-directed SIGINT is taken by the leader on this host — probe output
  `process-directed SIGINT handled by leader/main`. The leader is the thread in `pthread_join`
  after `:1548-1578`, so the normal case is exactly the intended one. (Kernel `signal->curr_target`
  starts at the leader; that specific kernel mechanism is not in the pins — `[INFERENCE]`.)
* `SA_RESTART` is **not** set for the child handler: observed `child-install sa_flags=0x04000000`
  (only glibc's `SA_RESTORER`; `SA_RESTART` is `0x10000000`, `/usr/include/asm-generic/signal-defs.h:59`).
  The parent installer's `sa_flags=0x14000000` includes it (`:430`), but `-B` never reaches the
  fork branch (`:1512-1544`) that installs the parent handler.
* Consequence of no `SA_RESTART`, observed in the same harness: `poll(...,5000)` in a worker
  returned `-1/EINTR` (`errno=4`), and a blocked `write()` returned `-1/EINTR` — i.e. the
  `-EINTR` branch of the progress loop (`:1043-1046`) is reachable if the signal lands on that
  thread, and the final write's syscalls are interruptible by a further signal.

### 2.4 Is "a device whose scrub ioctl returns nonzero is recorded with canceled set" exact,
and does resume take it up?

Exact as written at the field level: `sp->stats.canceled = !!ret` (`:969`) with `ret` the
`BTRFS_IOC_SCRUB` return (`:965`), written to the record at `:887`, read back at `:739`. It is
errno-blind (N4) and only applies to devices that actually ran an ioctl (N5).

Resume uptake: `resume` is the same function (`cmd_scrub_resume` `:1831-1833`, `scrub_start(…, true)`); the
predicate at `:1430-1431` treats a canceled **or** unfinished record as resumable, sets
`scrub_args.start = last_scrub->p.last_physical` (`:1433`) and `resumed` (`:1434`); a finished,
non-canceled record is skipped (`:1435-1437`) and, if nothing is left, the run exits 2 with
`nothing to resume` (`:1452-1457`, `:1727-1728`). Because the kernel copies scrub progress before
returning the cancel error, `last_physical` in a canceled record is the position at cancellation
(kernel `:3214-3215`). So SR3's take-up is real. Note `!finished` alone also qualifies: even a
record whose final write was lost (still `finished=0`) is resumed from the last periodic
`last_physical`.

## 3. Narrowings

**N1 — the handler is armed late, after the initial record write.** `:1501-1510` writes the
all-zero record, `:1546` arms the handler. A SIGINT before `:1546` keeps the inherited
disposition (`SIG_DFL` for a systemd service or a shell job) and terminates the process; the record then reads `canceled=0,
finished=0` ("interrupted", `:342-343`) and is still resumable via `!finished` (`:1430-1431`).
So "a SIGINT sent to it … leaves a canceled record" has a startup exception; the record stays
semantically correct (`interrupted`), it just does not say `canceled`.

**N2 — cancel before the scrub is running does nothing.** Between `:1546` and the first worker
reaching the kernel (`:1548-1578`, `:965`), or after the last worker returned,
`btrfs_scrub_cancel` returns `-ENOTCONN` (kernel `:3280-3282`), the handler prints
`Scrub cancel failed` (`:422-423`, message string present in the installed binary), and the scrub
runs to completion → record `canceled=0, finished=1`. The row's sentence is safe only under its
"the running scrub" qualifier.

**N3 — the handler is not a fire-and-forget flag; it blocks.** `btrfs_scrub_cancel` waits in an
uninterruptible `wait_event` for `scrubs_running == 0` (kernel `:3285-3291`), so the receiving
thread is parked for the whole cancellation. `scrub_sigint_record_progress` is not
async-signal-safe (`perror` at `:423`). If a scrub cannot reach a cancel check point within
systemd's `TimeoutStopSec`, systemd escalates to SIGKILL and no final record is written — the
record stays interrupted. `[INFERENCE]` for the systemd escalation (not in the pins; SR9's own
Limits already mark the systemd side as inference); the blocking is source-exact.

**N4 — `canceled` means "the scrub ioctl did not return 0", not "a signal cancelled it".**
`!!ret` at `:969` also fires for `-EPERM` (both scrub and cancel require `CAP_SYS_ADMIN`,
`ioctl.c:3066-3073`, `:3118-3123`), `-EOPNOTSUPP`/`-EINVAL` (`ioctl.c:3075-3085`), `-ENODEV`,
`-EINTR` (see 2.3), `-ENOMEM`. The record's status word for such a device is `aborted`
(`:342`). The `ENODEV` case is specially quiet: main `continue`s without incrementing `err`
(`:1621-1625`), so a scrub can exit 0 with a `canceled=1` line for the missing device.

**N5 — skipped devices never run an ioctl.** In resume mode, devices whose record is finished and
not canceled are copied through (`:1549-1555`) with `ret = 0`, so their record line keeps the old
`canceled` (necessarily 0 by the skip predicate). The sentence is about devices that ran an
ioctl, which is what it says, but a SIGINT'd multi-device record is not uniformly `canceled=1`.

**N6 — the final write is conditional and can be lost.** `do_record` may already be false
(`:1335-1338`, `:1501-1508`) → no record at all; a failed final write only warns, even under
`-B` (`:1704-1707`) and does not set `err` (`SR3` already says this). Because the handler stays
armed until `:1710` — after the final write — a second SIGINT during `scrub_write_progress`
interrupts its `write()` (`EINTR` observed in the harness; that a regular-file write blocks is
device-dependent `[INFERENCE]`), yielding `failed to record the result` and keeping the previous
record. Interactive `Ctrl-C` twice is the realistic case.

**N7 — delivery target changes the shape of the result.** Process-directed SIGINT hits the leader
here (observed). If the leader is inside the thread-creation loop (`:1548-1578`) the cancel covers
only the devices already running; the handler returns (`cancel_req` is decremented, kernel
`:3292`) and later-created device threads scrub to completion → a **mixed** record. If the signal
lands on a worker inside `BTRFS_IOC_SCRUB`, that worker's ioctl returns `-EINTR` after the
handler; the record still gets `canceled=1` (N4) but main prints `scrubbing … failed … errno=4`
(`:1629-1639`) instead of `canceled`. The pathological variant — the blocking
`btrfs_scrub_cancel` running on the very thread whose scrub ioctl must return — is not reachable
when the leader takes the signal; `[INFERENCE]`, not observed.

**N8 — a signal on the progress thread ends it early.** `poll(&accept_poll_fd, 1, 5000)` at
`:1043-1046` returns `-EINTR` → `goto out`; the thread's `ERR_PTR(-EINTR)` makes main print
`recording progress failed: Interrupted system call` (`:1695-1699`) under `-B`. The final record
is still written afterwards (`:1701`); observed `worker poll_ret=-1 errno=4`. Cosmetic in the
journal, not a record defect.

## 4. What the compiled harness shows (and what it does not)

`harness.c` `#include`s `handlers.h`, a byte-exact extract of pinned `cmds/scrub.c:416-444`
(sha256 `43dfd0de…e77f`), and runs five observations; `probe.c` is a separate delivery probe with
its own handler (not pinned code). Output (`run.log`):

```
parent-install sa_flags=0x14000000 SA_RESTART=1 handler=SIG_IGN
child-install ret=0 cancel_fd=3
child-install sa_flags=0x04000000 SA_RESTART=0 handler=pinned-child
Scrub cancel failed: Inappropriate ioctl for device
main pthread_join ret=0 (0 = main thread survived the SIGINT)
worker poll_ret=-1 errno=4 (Interrupted system call)
worker write_ret=-1 errno=4 (Interrupted system call)
ret=-1 -> canceled=1 ; ret=0 -> canceled=0 (errno not consulted)
process-directed SIGINT handled by leader/main
```

It shows the two dispositions, that the handler runs and blocks nothing fatal, that main survives
`pthread_join`, and that `poll`/`write` are interruptible under the pinned flags. It does **not**
show a real cancel: the harness's `cancel_fd` is a regular file, so the pinned handler prints
`ENOTTY`. No btrfs ioctl was issued; the kernel half is source-only.

## 5. Optional tightened wording for SR9 (proposal; wave 1 sets no verdict)

Replace the last third of SR9's Statement from "the foreground start installs …" with:

> the foreground start installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL` (scrub.c:1546,
> :421), and the kernel's cancel waits until every running scrub has stopped (fs/btrfs/scrub.c:3285-3291)
> and answers `-ENOTCONN` when none is running (:3280-3282, handler prints `Scrub cancel failed` and
> nothing is cancelled). Each device thread then sees its `BTRFS_IOC_SCRUB` return nonzero, records
> `canceled = !!ret` — any nonzero return, not only a cancellation (scrub.c:969-970) — and the main
> thread's final record write (scrub.c:1701-1703) persists it; `btrfs scrub resume` takes the device up
> from that record's `last_physical` (scrub.c:1430-1434). A SIGINT that arrives before scrub.c:1546, or
> while no scrub ioctl is running, cancels nothing.

and add to Limits:

> SR9 is read from source only; no SIGINT was sent to a scrub and no record was produced on this host
> (`/var/lib/btrfs` is absent, capture.txt:3). The handler is armed at scrub.c:1546, after the initial
> record write; a SIGINT before that kills the process with the default disposition and leaves the
> record `canceled=0, finished=0` (interrupted, still resumable). `canceled=1` in a record means the
> device's scrub ioctl returned nonzero, not that a signal cancelled it.

## 6. Limits / not done

- No live scrub, no SIGINT to a real scrub, no btrfs ioctl: forbidden by the host guard and
  impossible unprivileged (`capture.txt:1` `CapEff=0000000000000000`, `capture.txt:3`
  `var_lib_btrfs absent`). The record write path is therefore source- and harness-grounded only.
- Leader-targeted signal delivery is observed on this host (kernel 7.2.11-arch1-1) but the
  `curr_target` mechanism is not in the pinned sources → `[INFERENCE]` for the explanation.
- The installed `/usr/bin/btrfs` is btrfs-progs 7.1-1, built from the unpatched v7.1 tag
  (`frozen/src/PKGBUILD:45-46` source list has no patch; `prepare()` applies none) and contains the
  handler's unique string `Scrub cancel failed` plus `failed to record the result: %m`
  (`strings -a /usr/bin/btrfs`), so the shipped binary carries the traced paths; the binary is
  stripped (no `.symtab`), so no per-function disassembly check was made.
- I did not verify the corpus row's own `props`/`host_ok` machinery (that is the C2 counter's job)
  and did not edit the row.

## Receipts

`.ufo/waves/round-44/w1/C2ExecSigintSR9/`: `harness.c`, `handlers.h` (pinned extract),
`probe.c`, `run.log`, `trace-lines.txt` (every cited range with original line numbers),
`hashes.txt` (`sha256sum -c SHA256SUMS` for the three frozen dirs + extract hash).
Scratch was `/fast/scratch/hyaku/tsukuroi-r44/C2ExecSigintSR9` and has been removed.
