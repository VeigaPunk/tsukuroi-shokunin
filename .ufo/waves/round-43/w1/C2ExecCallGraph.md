VERDICT: defect-found

# C2-5 — mechanical call-path check of SR1/SR3/SR6 universal words

Seat `C2ExecCallGraph`, lane tsukuroi-shokunin, round 43 wave 1. Read-only: no lane file, no
`/var/lib/btrfs` write, no privileged ioctl, no scrub command. All evidence is from the frozen
source and from `grep -n` / a Python scanner run against it (receipts below are copies of the
commands and their outputs).

Source under test: `S237` = btrfs-progs v7.1 `cmds/scrub.c`, frozen at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c`,
`sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — matches
`.ufo/waves/round-42/frozen/src/SHA256SUMS:1` and the claim text. Claims text read from
`corpus/knowledge/btrfs-scrub-record-r43.md:17-112`.

Receipts (this seat dir, `.ufo/waves/round-43/w1/C2ExecCallGraph/`):
- `receipt.txt` — sha256 of the source + full scanner output.
- `scan.py` / `scan.out` — brace-aware function spans, call sites, unlink family, do_print, err,
  `in_progress` inventory (re-run: `python3 scan.py`).
- `sr3-skip-trace.txt` — numbered excerpt chain for the SR3 finding.
- `messages.h` / `messages.c` — btrfs-progs v7.1 `common/` files fetched only to settle the
  `warning()` gate (URLs and digests in the tooling record at the end).

Scanner-reported spans (1-based inclusive): `scrub_start` 1233-1737, `scrub_write_file` 843-895,
`scrub_write_progress` 897-947, `scrub_resumed_stats` 800-828,
`is_scrub_running_in_kernel` 1190-1206, `cmd_scrub_status` 1847-`…`,
`cmd_scrub_resume` 1831-1834, `scrub_open_file_w` 508-518, `scrub_rename_file` 520-536,
`scrub_datafile` 446-476.

---

## (1) Every call of `scrub_write_file` and `scrub_write_progress`, and whether it passes through `scrub_resumed_stats`

Command and output (from `scan.out`):

```
CALLS scrub_write_file:
  922: err = scrub_write_file(fd, fsid, data, n);
  1112: ret = scrub_write_file(
CALLS scrub_write_progress:
  1123: ret = scrub_write_progress(spc->write_mutex, fsid,
  1503: ret = scrub_write_progress(&spc_write_mutex, fsid, sp,
  1702: ret = scrub_write_progress(&spc_write_mutex, fsid, sp,
RESUMED_STATS sites:
  800: static struct scrub_progress *scrub_resumed_stats(struct scrub_progress *data,
  864: use = scrub_resumed_stats(&data[i], &local);
```

| call | caller | destination | passes `scrub_resumed_stats`? |
|---|---|---|---|
| `scrub.c:922` | inside `scrub_write_progress` (897-947) | `_tmp` record fd | yes — the callee applies it per element at `scrub.c:864` |
| `scrub.c:1112` | `scrub_progress_cycle`, `peer_fd` from `accept()` `scrub.c:1049` | status **socket**, not the record | yes — same callee path, `scrub.c:864` |
| `scrub.c:1123` | `scrub_progress_cycle` periodic record write (gated `spc->do_record`, `scrub.c:1121`) | record file via 922 | yes (922 → 864) |
| `scrub.c:1503` | `scrub_start` initial "all-zero progress file" (`if (do_record)`, `scrub.c:1501`) | record file | yes (922 → 864) |
| `scrub.c:1702` | `scrub_start` final write (`if (do_record)`, `scrub.c:1701`) | record file | yes (922 → 864) |

So all five call sites reach `scrub_resumed_stats` at `scrub.c:864`; the per-device transform is
applied inside `scrub_write_file`'s loop regardless of caller (`scrub.c:863-864`). The record file
itself has exactly one writer: the only `scrub_open_file_w` call is `scrub.c:917`, inside
`scrub_write_progress`, and the only `scrub_rename_file` call is `scrub.c:925`, immediately after
the `scrub_write_file` return test. The direct `scrub_write_file` at `1112` writes a **status
snapshot to an accepted client socket** (`peer_fd = accept(...)`, `scrub.c:1049`), not to the
record — a reader of "every record update goes through `scrub_write_progress`" (SR1) should not
infer that every `scrub_write_file` call is a record write.

## (2) Every `unlink(` / `remove(` / `unlinkat(` call and its argument

```
UNLINK FAMILY:
  1485: unlink(sock_path)
  1497: unlink(sock_path)
  1721: unlink(sock_path)
RENAME sites:
  534: ret = rename(datafile_old, datafile_new);
```

- Exactly three unlink-family calls, all `unlink(sock_path)`: `scrub.c:1485` (EADDRINUSE retry),
  `scrub.c:1497` (socket-open failure cleanup), `scrub.c:1721` (`out:` cleanup). No `remove(` and
  no `unlinkat(` occurs anywhere in the file.
- `sock_path` is built from `SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"`
  (`scrub.c:68`) at `scrub.c:1461-1462` (start) and `scrub.c:1923` (status), never from
  `SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` (`scrub.c:67`).
- The only rename is `scrub.c:534`, called from `scrub.c:925`, on `datafile_old = <base>_tmp`
  (suffix built by `scrub_datafile`, `scrub.c:446-476`, with `fn_tmp = "tmp"`, `scrub.c:917`) over
  `<base>`.

Mechanical consequence for SR1: nothing in `scrub.c` removes a `_tmp` file; a failed write
(`scrub.c:922-923` `goto out1`), a failed rename (`scrub.c:925-926`) or a killed writer leaves the
`_tmp` inode in place.

## (3) Every assignment to `do_print` and every read of it

```
DO_PRINT (line: kind: text):
  1249: ASSIGN: bool do_print = false;
  1295: ASSIGN: do_print = true;
  1332: READ  : if (bconf.verbose == BTRFS_BCONF_QUIET && do_print)
  1333: ASSIGN: do_print = false;
  1568: READ  : if (do_print) {
  1587: READ  : if (do_print) {
  1610: READ  : if (do_print) {
  1622: READ  : if (do_print)
  1630: READ  : if (do_print) {
  1648: READ  : if (do_print) {
  1690: READ  : if (do_print && ret) {
  1696: READ  : if (do_print && terr && terr != PTHREAD_CANCELED) {
  1704: READ  : if (ret && do_print) {
```

All 13 occurrences are inside `scrub_start` (1233-1737); nothing in `cmd_scrub_status`,
`cmd_scrub_cancel` or `scrub_progress_cycle` reads it.

- Init `false` `scrub.c:1249`; set `true` only in `case 'B'` `scrub.c:1295` (which also clears
  `do_background` and sets `do_wait`); cleared `scrub.c:1333` when
  `bconf.verbose == BTRFS_BCONF_QUIET` at `scrub.c:1332`. The clear runs once after option parsing
  (post-`getopt_long` loop), so argv order of `-B`/`-q` does not matter; `-q` reaches the global via
  `bconf_be_quiet()` at `scrub.c:1301`, a global `--quiet` is handled outside this file.
- Reads: thread-creation failures `1568`, `1587`; join/ioctl failure prints `1610`, `1622`, `1630`;
  final stats block `1648`; progress-thread handling `1690`; progress-thread's own error `1696`;
  final record write `1704`.

## (4) Every assignment to `err` in `scrub_start` after the first record write, and whether any depends on a record write

First record write is the call at `scrub.c:1503` (inside `if (do_record)` at `1501`; the comment at
`1502` is the claimed one). Assignments after that line, from `scan.out`:

```
ERR_ASSIGN in scrub_start after line 1503:
  1516: err = 1;                                  (fork failed)
  1527: err = 0;                                  (parent, !do_wait, before exit)
  1533: err = 1;                                  (wait() failed)
  1537: err = WIFEXITED(stat) ? WEXITSTATUS(stat) : -1;   (child exit status)
  1541: err = 0;                                  (wait() ok)
  1574: err = 1;                                  (pthread_create scrub_one_dev failed)
  1591: err = 1;                                  (pthread_create progress thread failed)
  1595: err = 0;                                  (baseline for the join loop)
  1616: ++err;                                    (pthread_join failed)
  1627: ++err;                                    (scrub ioctl ECANCELED)
  1637: ++err;                                    (scrub ioctl other failure)
```

Before/at 1503 (for completeness): `1242 int err = 0`, `1351`, `1356`, `1397`, `1407`, `1424`
(argument/fs-info/socket/malloc setup failures).

Dependency check: **none** of the ten post-1503 assignments is derived from a record write.
- The initial write's failure branch (`scrub.c:1505-1509`) sets `errno`, prints, and sets
  `do_record = false`; it does not touch `err`.
- The periodic write's failure (`scrub.c:1125-1126`) only `goto out` → `return ERR_PTR(ret)`
  (`scrub.c:1128-1133`); the error surfaces as `terr` at `scrub.c:1696`, never as `err`.
- The final write's failure (`scrub.c:1704-1707`) only prints under `do_print`.
- `err` is consumed at `scrub.c:1725` (`if (err) return 1;`), before `nothing_to_resume`
  (`1727`) and the error counters (`1729-1734`).

So `btrfs scrub start`/`resume` cannot return 1 because of a record-write failure, and neither
record-write branch assigns `err` — SR3's last sentence holds.

## (5) Every caller of `is_scrub_running_in_kernel`, and every place `in_progress` is set

```
IS_SCRUB_RUNNING_IN_KERNEL:
  1190: DEF: static int is_scrub_running_in_kernel(int fd,
  1378: USE: if (!is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices))
  1946: USE: in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);
IN_PROGRESS set/read:
  78:  READ: int in_progress;                                  (struct scrub_stats field)
  186: READ: if (s->in_progress) {                             (_print_scrub_ss, time-left block)
  341: READ: (ss->in_progress ? "running" :                   (the only "running" print)
  1859: READ: int in_progress;                                 (cmd_scrub_status local)
  1946: SET: in_progress = is_scrub_running_in_kernel(...)
  1962: SET: last_scrub->stats.in_progress = in_progress;      (-d branch, in-memory record)
  1974: SET: fs_stat.s.in_progress = in_progress;              (summary branch)
```

- Callers: `scrub.c:1378` (start path: stale-record check, `if (!… ) force = true;`) and
  `scrub.c:1946` (status path). The function itself is `scrub.c:1190-1206`.
- The only producer of the value is the ioctl at `scrub.c:1200`; the function answers `1` on the
  first `ioctl()==0` (`scrub.c:1201-1202`) and `0` after the loop (`scrub.c:1205`).
- Writes of the field: `scrub.c:1962` (in-memory record used by `print_scrub_dev`) and
  `scrub.c:1974` (`fs_stat.s`), both copying the `1946` result. The sibling ioctl at
  `scrub.c:986` (`BTRFS_IOC_SCRUB_PROGRESS` per device in the progress thread) writes
  `sp->scrub_args.progress` / `sp->ret` / `sp->ioctl_errno` only — it never touches `in_progress`.
- `scrub_start`'s own stats printing (`scrub.c:1648-1683`, `init_fs_stat` at `scrub.c:1654`) leaves
  `in_progress` zero (memset, `scrub.c:309`), and for skipped devices it copies the parsed record's
  stats (`scrub.c:1551`) which are memset zero and have no `in_progress` key (`scrub.c:731-741`).

## (6) Whether any path other than the ioctl sets `in_progress` to 1

No. Mechanically:
- The local `in_progress` is declared `scrub.c:1859` and assigned exactly once, `scrub.c:1946`,
  from the ioctl-only function.
- Its two consumers (`1962`, `1974`) copy that value; neither adds, ORs or defaults it to 1.
- The on-disk record cannot carry it: `scrub_read_file` allocates zeroed records (`scrub.c:661`)
  and its key list (`scrub.c:703-741`) contains `finished, t_start, t_resumed, duration, canceled`
  and no `in_progress`; `scrub_write_file` writes exactly that key list (`scrub.c:870-889`).
- `add_to_fs_stat` (`scrub.c:282-305`) copies only counters and `t_start/t_resumed/duration/
  canceled/finished`, never `in_progress`.
- The only kernel-state query in the file is `scrub.c:1200`; the other scrub ioctls are start
  (`scrub.c:965`), cancel (`scrub.c:421`, `1792`) and per-device progress polling
  (`scrub.c:986`), none of which writes `in_progress`.

Therefore, given the kernel precondition SR6 cites (ioctl fails `-EPERM` without `CAP_SYS_ADMIN`,
`S240` ioctl.c:3132-3133), an unprivileged `btrfs scrub status` has `in_progress == 0` and the
only "running" print (`scrub.c:341`) cannot fire. SR6's path is mechanically supported.

---

## Universal-word audit

### SR1 — supports

| word in SR1 | mechanical result |
|---|---|
| "Every record update goes through `scrub_write_progress`" | true for the record file: sole `scrub_open_file_w` at `917`, sole `scrub_rename_file` at `925`, all record writes at `1123`, `1503`, `1702`. (The direct `scrub_write_file` at `1112` is a status-socket write, `accept()` at `1049`.) |
| "`O_WRONLY|O_CREAT` and no `O_TRUNC` (mode 0600, then a non-blocking `flock` `LOCK_EX`)" | `scrub.c:517`, `483`, `487` verbatim; no `O_TRUNC`/`O_APPEND` anywhere in the file |
| "writes the whole record from the start of that file" | true: fresh fd at offset 0, whole record written sequentially; no `O_APPEND` |
| "renames `_tmp` … only when the write returned no error; a failed write skips the `rename`" | `scrub.c:922-926` (`if (err) goto out1;` precedes `925`) |
| "its three `unlink` calls all name the progress socket path" | true: `1485`, `1497`, `1721`, all `sock_path`; zero `remove`/`unlinkat` |
| trailing-bytes consequence | mechanically follows from no `O_TRUNC` + no `_tmp` removal; the claim already marks it `[inference]`. Parser consequence is consistent: a stray tail is parsed as another line and hits `_SCRUB_INVALID` (`scrub.c:569-576`, `661-696`) |

No defect found in SR1 as written.

### SR3 — defect-found (one universal clause; see below)

| word in SR3 | mechanical result |
|---|---|
| "`btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`" | `scrub.c:1833` |
| "For each device whose last record is canceled or unfinished, resume makes that record the device's `resumed` source" | `scrub.c:1430-1434`; note the `else if (resume)` branch also assigns `resumed` while setting `skip = 1` (`1435-1438`) |
| "every record write passes each device through `scrub_resumed_stats` (in `scrub_write_file`)" | `scrub.c:864` inside the per-device loop of every `scrub_write_file` call (table in item 1) |
| "writes the earlier record's progress counters added to the new run's, the earlier record's `t_start`, and the two durations summed" | `scrub.c:806-818` (`_SCRUB_SUM`), `823` (`t_start`), `824-825` (duration sum); also `822` `t_resumed = data->stats.t_start` |
| "the first record a resume writes for a resumed device carries the interrupted run's counters and start time" | true for a device with `skip == 0`: `1503` → `864` → `803` false → sums |
| "only a fresh `start` (no `resumed` source) writes zero counters" | **false** — see finding D1 |
| "a failed progress-record write ends the progress thread with its error … printed … only when `do_print` is set" | `scrub.c:1123-1126` → `ERR_PTR` `1128-1133`; print `1696-1698` under `do_print` |
| "a failed final write prints 'failed to record the result' under the same condition" | `scrub.c:1704-1706` |
| "`do_print` is false by default, set by `-B`, and cleared again when output is quiet" | `1249`, `1295`, `1332-1333` |
| "Neither branch assigns the command's `err` status" | true: `1505-1509` sets `do_record=false`; `1704-1707` prints only; no `err` assignment after `1503` depends on a record write (item 4) |

**D1 (defect).** The universal "only a fresh `start` (no `resumed` source) writes zero counters"
is falsified by the `skip` path of a `resume`. Chain (line-numbered excerpt in
`.ufo/waves/round-43/w1/C2ExecCallGraph/sr3-skip-trace.txt`):

1. On `resume`, a device whose last record is `finished` and not `canceled` (or that has no
   record) takes `else if (resume)`: `sp[i].skip = 1; sp[i].resumed = last_scrub;`
   (`scrub.c:1435-1438`).
2. The initial record write happens **before** fork/threads and passes the **whole array**:
   `scrub_write_progress(&spc_write_mutex, fsid, sp, fi_args.num_devices, …)` (`scrub.c:1503-1504`).
   At that moment the skipped entry's stats are still zero (calloc at `scrub.c:1402`; the saved
   stats are copied only later at `scrub.c:1549-1552`).
3. `scrub_resumed_stats` returns the entry unchanged when `skip` is set (`scrub.c:803-804`), so
   `scrub_write_file` writes that entry verbatim (`scrub.c:863-864`, counters at `scrub.c:870-883`).
   Record line for that devid: all counters 0, `t_start:0`, `t_resumed:0`, `duration:0`,
   `canceled:0`, `finished:0`.
4. The progress thread's periodic writes are equally affected: it copies only
   `devid/fd/t_start/resumed/skip/finished` into its working array (`scrub.c:1027-1039`), the
   `skip` entry short-circuits `resumed` summation (`scrub.c:803`), and the write is gated only on
   `spc->do_record` (`scrub.c:1121-1126`). The skipped device then reads back as counters 0,
   `finished:1`, `duration:0`.
5. The final write (`scrub.c:1701-1708`) uses the shared array where the saved stats were copied
   at `scrub.c:1551`, so a **normally finishing** resume restores the skipped device's counters.

Consequences: a resume on a multi-device filesystem where at least one device is resumed and
another is skipped writes zero counters for the skipped device in the initial record and in every
periodic record; if the process dies without the final write (SIGKILL, panic, OOM kill — this
lane's OOM plane), the zero-counter record persists and the skipped device's status reads
`interrupted`/zero counters instead of `finished` with its history. [Inference for the
kill case; the zero-write itself is line-for-line above.] The scope is narrow (mixed
resumed/skipped multi-device resume; a single-device all-skip resume writes nothing because of
`scrub.c:1452-1456`) but the clause as written says "only", so it is false.

**Exact proposed text** (replace the last sentence of SR3's Statement; keep the rest):

> So the first record a resume writes for a resumed device carries the interrupted run's counters
> and start time. A fresh `start` writes zero counters, and so does the record a `resume` writes
> for a device it *skips*: a device whose last record is finished (and not canceled), or that has
> no record, takes the `skip` branch (`scrub.c:1435-1438`) and is written by the initial record
> write (`scrub.c:1503-1504`) before its saved stats are copied (`scrub.c:1549-1552`), with
> `scrub_resumed_stats` returning the entry untouched for `skip` (`scrub.c:803-804`); its periodic
> records likewise carry zero counters with `finished=1` (`scrub.c:1027-1039`, `1121-1126`), and
> only the final write (`scrub.c:1701-1708`) restores the saved stats, so an unclean exit leaves
> that device recorded with zero counters.

**D2 (defect, derived text).** The triage bullet
`corpus/knowledge/btrfs-scrub-record-r43.md:120`: "A scrub started without `-B` (the default)
fails to record silently; only `-B` runs show recording errors (SR3)" is mechanically false for
the **initial** record write. `scrub.c:1501-1510` runs before the fork and its failure prints
`warning("failed to write the progress status file: …")` at `scrub.c:1507` outside any `do_print`
guard. In btrfs-progs v7.1, `warning()` expands to `__btrfs_warning` →
`__btrfs_msg`/`__btrfs_printf` (`messages.h:93-94`, `136-141`), which is a direct
`vfprintf(stderr, …)` with no `bconf.verbose` test (`messages.c:33-40`); the `bconf` gate exists
only in `should_print`/`pr_verbose` (`messages.c:88-99`, `107-117`), which `warning()` does not
call. So a default (non-`-B`) start **does** report an initial recording failure, even under
`-q`. Only the later failures are `do_print`-gated.

Exact replacement for that bullet:

> A scrub started without `-B` (the default) reports no *periodic* or *final* recording failure:
> both prints are gated on `do_print`, which only `-B` sets (`scrub.c:1696-1698`, `1704-1706`,
> `1295`). The initial record write is different — its failure prints unconditionally as
> `warning("failed to write the progress status file: …")` (`scrub.c:1507`), and `warning()` in
> btrfs-progs v7.1 is an ungated write to stderr (`common/messages.h:136-141`,
> `common/messages.c:33-40`).

### SR6 — supports, with one wording precision

| word in SR6 | mechanical result |
|---|---|
| "`btrfs scrub status` calls `is_scrub_running_in_kernel`" | `scrub.c:1946` (second caller is the start stale-check, `1378`) |
| "issues `BTRFS_IOC_SCRUB_PROGRESS` once per device and answers 1 only when a call returns 0" | `scrub.c:1197-1203`: `ioctl` per device, `return 1` on the first `ret == 0`, `return 0` after the loop. For the unprivileged case (all calls fail) this is exactly one call per device; for a privileged success it short-circuits before later devices, so "once per device" is a bound, not an exact count |
| "any failed call, whatever its errno, reads as not running" | true: `if (!ret)` is the only success test; the errno is not inspected |
| "for an unprivileged caller the status command's `in_progress` is always 0" | mechanically the value is the ioctl result (`1946`), with no other producer (item 6); kernel-side `-EPERM` is S240's row |
| "its `btrfs scrub status` never prints `running`" | the only "running" print is `scrub.c:341` under `ss->in_progress`; status paths get 0 |
| no non-ioctl path sets `in_progress` | confirmed (item 6) |

Optional precision (not a defect): replace "issues `BTRFS_IOC_SCRUB_PROGRESS` once per device and
answers 1 only when a call returns 0" with "issues `BTRFS_IOC_SCRUB_PROGRESS` device by device and
answers 1 on the first call that returns 0, 0 only after every call failed (`scrub.c:1197-1205`)".
The unprivileged conclusion is unchanged.

---

## Adjacent observations (not part of SR1/SR3/SR6 as written)

1. `void *terr;` is uninitialized at `scrub.c:1274` and read at `scrub.c:1696` whenever
   `pthread_cancel(t_prog)` returns non-zero (`scrub.c:1685-1687` skips the join in that case), an
   uninitialized read in upstream v7.1. It cannot rescue a record-write error (that path has
   `ret == 0`), so it does not change SR3's sentence.
2. `is_scrub_running_in_kernel` is also the start path's stale-record check (`scrub.c:1378`):
   when the ioctl fails for every device, `force` becomes `true` and the
   `is_scrub_running_on_fs` guard (`scrub.c:1392-1398`) is skipped. For an unprivileged caller
   that removes the userspace "Scrub is already running" refusal; the later `BTRFS_IOC_SCRUB`
   (`scrub.c:965`) then fails with `-EPERM`. [Inference from the two call sites; not run.]
3. The direct `scrub_write_file` at `scrub.c:1112` writes the resumed-summed snapshot to a status
   client (`accept()` at `1049`), so `btrfs scrub status` served by a live scrub also shows the
   cumulative numbers; this is consistent with SR3 but is not stated in it.

## Limits — what I did not do

- Did not build btrfs-progs, did not run any btrfs command, did not issue any ioctl, did not read
  or write `/var/lib/btrfs`, did not touch the lane's Git/jj state (only read frozen files and
  `corpus/knowledge/`).
- Did not verify S240's kernel-side `-EPERM` (another seat's row); I only verified the userspace
  call path that consumes its result.
- Did not reproduce the SR1 trailing-bytes or D1 zero-record consequences on a live record; both
  are source-level traces, and the kill-case wording is flagged as inference.
- Did not run any build/lint/test gate (wave is in flight; the parent owns gates).

## Tooling record

- No tool installed or upgraded; no pacman/uv/npm transaction. `sudo` not used.
- Read-only network fetch (evidence only, into scratch, then copied into this seat dir):
  `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/common/messages.h` →
  sha256 `7db69d2cdfc064355b06e0a99df7a7833ae189ef40a438879c79a137da069945`;
  `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/common/messages.c` →
  sha256 `3b1413fcf1304d10eb3589c723fa3df86d44c5b2306651acc3aea8598e2e38e5`;
  access date 2026-10-26, same tag/commit as
  `.ufo/waves/round-42/frozen/src/FETCH.txt` (v7.1 = 0a919c7d6e389c07920675b7fad3f793b92aa78b).
  Purpose: settle the `warning()` verbosity gate for D2.
- Scratch `/fast/scratch/hyaku/tsukuroi-r43/C2ExecCallGraph/` removed after receipts were copied;
  nothing was written under `/tmp`, the fleet root, or any tracked lane path other than this
  report and the receipt dir named by the seat spec.
