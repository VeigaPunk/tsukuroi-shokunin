VERDICT: supports

# C2-17 — GR2's btrfs-progs side (S237, btrfs-progs v7.1 `cmds/scrub.c`)

Item: GR2 marks the btrfs-progs side `[inference]` — "how `btrfs scrub start` reports a scrub ioctl that returns
EINPROGRESS, and what a privileged `btrfs scrub status` prints for the replace source device while a replace runs".
Answer: **both halves are decided by S237 and the `[inference]` can be replaced by a pinned statement**, but the
second half must be stated **conditionally on the scrub record file**: the kernel's "0" answer (SR7) is printed as
`Status:           running` only when `/var/lib/btrfs/scrub.status.<fsid>` holds an entry for that devid; with no
entry — the normal case during a replace, since only a scrub start writes that file — status prints
`no stats available` and **no `Status:` line at all**, and the print differs between `-d` and the default form.
Second correction the row needs: the refusal is reported **only in foreground mode** (`-B`, which the packaged unit
uses); a default background `btrfs scrub start` prints `scrub started … (pid=N)` and exits 0, saying nothing about
the EINPROGRESS.

S237 = `.ufo/waves/round-42/frozen/src/scrub.c`, sha256
`48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`; a fresh `git clone --depth 1 --branch v7.1
https://github.com/kdave/btrfs-progs.git` (2026-10-27) gives HEAD `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` and a
`cmds/scrub.c` with the **same sha256**, so the snapshot is byte-identical to upstream v7.1 — the version this host
ships (`pacman -Q btrfs-progs` → `btrfs-progs 7.1-1`; receipt `C2ExecGR2Progs/provenance.txt`).

All line numbers below are S237 `scrub.c` unless prefixed `messages.h`/`messages.c` (btrfs-progs v7.1
`common/`; fetched 2026-10-27 from
`https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/common/messages.h`, sha256
`7db69d2cdfc064355b06e0a99df7a7833ae189ef40a438879c79a137da069945`; and `.../common/messages.c`, sha256
`3b1413fcf1304d10eb3589c723fa3df86d44c5b2306651acc3aea8598e2e38e5`).

## P1 — what `btrfs scrub start` prints for an `EINPROGRESS` scrub ioctl

`EINPROGRESS` appears **zero times** in the file (`grep -c EINPROGRESS scrub.c` → `0`; tree-wide over the v7.1 clone
it appears only in `cmds/balance.c:356,819` and `cmds/quota.c:225`). There is no refusal-specific branch: the value
falls through the generic per-device error arm.

Mechanism, in order:

1. Per-device thread: `ret = ioctl(sp->fd, BTRFS_IOC_SCRUB, &sp->scrub_args);` (:965), then `sp->ret = ret;` (:967),
   `sp->stats.canceled = !!ret;` (:969), `sp->ioctl_errno = errno;` (:970), `sp->stats.finished = 1;` (:974).
   For a replace source the ioctl returns −1 with `errno = EINPROGRESS` (115) — S247/S242 as quoted in GR2.
2. After `pthread_join` (:1608) the main thread switches on the stored errno (`if (sp[i].ret) {` :1619,
   `switch (sp[i].ioctl_errno) {` :1620). The only named cases are `ENODEV` (:1621) and `ECANCELED` (:1626);
   `EINPROGRESS` takes `default:` (:1629) and prints, on **stderr**, with `errno` set to 115 (:1631):

   `ERROR: scrubbing <path> failed for device id <devid>: ret=-1, errno=115 (Operation now in progress)`

   from `"scrubbing %s failed for device id %lld: ret=%d, errno=%d (%m)",` (:1633) with `%m` → `strerror(115)`
   ("Operation now in progress"; `python3 -c "import os,errno;print(os.strerror(errno.EINPROGRESS))"` → that exact
   string). The `ERROR: ` prefix and the trailing newline come from `__btrfs_msg`: `#define PREFIX_ERROR "ERROR: "`
   (messages.h:83), `fputs((prefix), stderr);` (messages.h:88), `__btrfs_printf` → `vfprintf(stderr, fmt, args);`
   (messages.c:38), `fputc('\n', stderr);` (messages.h:90).
3. `++err;` (:1637) → `if (err) return 1;` (:1725-1726). Exit status **1**.
4. Stdout, before the thread starts: `pr_default("Starting scrub on devid %llu", devid);` (:1559, with the
   ` (limit …)` / newline tail at :1560-1563). Stdout after the join, in the `do_print` block (:1648):
   `scrub canceled for <fsid>` (:1679, because `if (sp[i].ret) append = "canceled";` :1671-1672), then the
   filesystem summary `Scrub started: <now>` (:333), `Status:           aborted`
   (:340-343, the `canceled` arm), `Duration:         0:00:00` (:344), `Total to scrub:   0.00B`,
   `Rate:             0.00B/s`, `Error summary:    no errors found`. So a foreground start during a replace reads
   like a scrub that ran and was cancelled — although none ran.
5. Record side effect (both modes): before the fork a start writes the all-zero record
   (`/* write all-zero progress file for a start */` :1502, `scrub_write_progress(...)` :1503-1504) into
   `/var/lib/btrfs/scrub.status.<fsid>` (`#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` :67), and after the
   failed ioctl it writes the record again (:1701-1707) with `dest->stats.canceled = data->stats.canceled;` (:820)
   and `dest->stats.finished = data->stats.finished;` (:821) — i.e. `canceled=1 finished=1` (:969, :974). A failed
   start therefore **replaces** the filesystem's scrub record with a zero-progress `aborted` entry.

Foreground vs background (this is the second thing the row must say):

- `-B` sets `do_wait` and `do_print` (`case 'B':` :1292-1296, `do_print = true;` :1295); the packaged unit's
  `ExecStart=/usr/bin/btrfs scrub start -B %f` (S244:10) is exactly this, so **the unit's journal gets the ERROR
  line and the unit fails with exit 1**.
- Default (no `-B`): `bool do_print = false;` (:1249), and `-q` clears it too (:1332-1333). The per-device error
  (:1630) and the summary (:1648) are both inside `if (do_print)`, so a plain `btrfs scrub start /mnt` prints the
  parent's `scrub %s on %s, fsid %s (pid=%d)\n` → `scrub started on <path>, fsid <fsid> (pid=<n>)` (:1523-1525),
  returns 0 (`if (!do_wait) { err = 0; goto out; }` :1526-1529), and the child prints only its un-gated
  `Starting scrub on devid <devid>` (:1559, `pr_default`, not inside `if (do_print)`) before exiting 1 — **no refusal
  text anywhere**, on stderr or otherwise.
- Pre-ioctl guard (can pre-empt everything, and can mislabel the cause): the kernel check only clears `force`
  (`if (!is_scrub_running_in_kernel(...)) force = true;` :1378-1379), and the refusal actually printed is the
  *record* check `if (!force && is_scrub_running_on_fs(...))` (:1392) whose predicate is a record entry with
  `!(sfr->stats.finished || sfr->stats.canceled)` (:1184) →
  `ERROR: Scrub is already running.` / `To cancel use 'btrfs scrub cancel %s'.` (:1393-1396), exit 1. During a
  replace this fires only if a previous scrub left an unfinished record, and it then names a scrub that is not
  running; with no record (or a finished/canceled one) the start proceeds to the ioctl and the EINPROGRESS path
  above. Nothing in the file inspects replace state: `grep -n replace scrub.c` → the single hit is the comment at
  :81, `/* TBD: replace with #include "linux/ioprio.h" in some years */`.

## P2 — what a privileged `btrfs scrub status` prints for the replace source device

`in_progress` is one per-filesystem boolean: `in_progress = is_scrub_running_in_kernel(fdmnt, di_args,
fi_args.num_devices);` (:1946), and that helper returns 1 on the **first** devid whose
`BTRFS_IOC_SCRUB_PROGRESS` returns 0 (`ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);` :1200,
`if (!ret)` :1201 `return 1;` :1202), 0 on any error (idle device `ENOTCONN`, unprivileged `EPERM`) (:1205).
A running replace makes the source answer 0 (SR7/S242:3336), so `in_progress = 1`.

The visible output then depends entirely on the record file, which status reads after failing to connect to the
scrub progress socket (`ret = connect(...)` :1927, `if (ret == -1) {` :1928,
`fdres = scrub_open_file_r(SCRUB_DATA_FILE, fsid);` :1930, `past_scrubs = scrub_read_file(fdres, 1);` :1940);
`last_dev_scrub` returns `NULL` for a missing list (`if (!past_scrubs || IS_ERR(past_scrubs)) return NULL;` :1141-1142)
or a devid absent from it (:1144-1148).

**(a) No record entry for that devid** — the live host case (`ls -ld /var/lib/btrfs` → `No such file or directory`),
and the case during a replace because `cmds/replace.c` never touches the scrub record (`grep -n
"SCRUB_DATA_FILE\|scrub_datafile\|scrub.status" cmds/replace.c` in the v7.1 clone → no output):

- `btrfs scrub status -d <mnt>`: `if (!last_scrub) { print_scrub_dev(&di_args[i], NULL, print_raw, NULL, NULL,
  limit); continue; }` (:1957-1960) → the device header `pr_default("\nScrub device %s (id %llu) %s\n", di->path,
  di->devid,` (:352, `append` NULL → empty, so the line ends in a space) followed by
  `if (!ss || !ss->t_start) {` (:320) `pr_default("\tno stats available\n");` (:321). **No `Status:` line, no byte
  counts** — the replace is invisible. `in_progress` is never used on this branch.
- `btrfs scrub status <mnt>` (summary form): `init_fs_stat(&fs_stat);` (:1973) then
  `fs_stat.s.in_progress = in_progress;` (:1974), records summed (:1981-1986) — none, so `t_start` stays 0 and
  `_print_scrub_ss` prints `\tno stats available` (:321) and **returns** (:322). `print_fs_stat` then still calls
  `print_scrub_summary` with `in_progress` 1, which takes the `if (s->in_progress) {` branch (:186) and prints
  `Time left:        0:00:00` (:196-197), `ETA:              <now>` (:198), `Total to scrub:   <fs used bytes>`
  (:199-200), `Bytes scrubbed:   0.00B  (0.00%)` (:201-203), then `Rate:             0.00B/s` and
  `Error summary:    no errors found`. That is: a scrub-like progress block at 0.00 % with **no `Status:` line**.
  [This exact privileged rendering is derived from the quoted lines; I could not run it — see Limits.]
- Exit status 0 in both forms: `return !!err;` (:2007), and `err` is only set by setup failures (:1919-1921,
  :1933-1935).

**(b) A record entry exists for that devid** (e.g. last month's finished scrub): `last_scrub->stats.in_progress =
in_progress;` (:1962) → `_print_scrub_ss` prints `Status:           running` (:340-341) together with the record's
**old** `Scrub started:`/`Duration:` (:324-334, :344), and the summary branch (:186-203) prints `Time left`/`ETA`/
`Bytes scrubbed` computed from the stale record. Note the header suffix comes from the record's own flag, not from
`in_progress`: `last_scrub->stats.finished ? "history" : "status"` (:1964-1965), so a finished record during a
replace yields `Scrub device … (id N) history` with `Status: running` underneath — an internally inconsistent pair.

**(c) Privilege**: `BTRFS_IOC_SCRUB_PROGRESS` sits behind `CAP_SYS_ADMIN` (SR6/S241), so an unprivileged status
always reads `in_progress = 0` (:1205) and never prints the `running`/`Time left` lines; the record file is opened
with `fd = open(datafile, m, 0600);` (:483), so an unprivileged status cannot read a record either.

## Observed on this host (unprivileged, read-only; nothing started, stopped or written)

`btrfs scrub status /` as uid 1000, 2026-10-27 (receipt `C2ExecGR2Progs/status-probe.txt`):

```
UUID:             1d02a454-c549-4a35-b567-89d60902af8e
	no stats available
Total to scrub:   301.19GiB
Rate:             0.00B/s
Error summary:    no errors found
exit=0
```

`btrfs scrub status -d /` (same receipt; `cat -A` confirms a trailing space after `(id 1)` and a TAB before
`no stats available`):

```
UUID:             1d02a454-c549-4a35-b567-89d60902af8e

Scrub device /dev/mapper/root (id 1) 
	no stats available
exit=0
```

This is branch (a) with `in_progress = 0`; a privileged run that saw the replace's source answer 0 would add exactly
the `Time left`/`ETA`/`Bytes scrubbed` group of :196-203 and nothing else. The `ERROR: ` prefix is confirmed live from the same binary:
`btrfs scrub status /nonexistent-xyz` → `ERROR: cannot check /nonexistent-xyz: No such file or directory` (the
`error("cannot check %s: %m", dev)` call site is `common/open-utils.c:162` in the v7.1 clone), followed by
`ERROR: '/nonexistent-xyz' is not a mounted btrfs device`, exit 1.

The host binary carries the pinned strings verbatim (`strings -a /usr/bin/btrfs`, grep line numbers):
`8649:Scrub device %s (id %llu) %s`, `8739:scrubbing %s failed for device id %lld: ret=%d, errno=%d (%m)`,
`8745:Scrub is already running.`, `10525:\tno stats available`, `10602:scrub %s for %s`,
`8733:scrub %s on %s, fsid %s (pid=%d)`, and one `Starting scrub on devid` — so the v7.1 control flow above is the
host's binary, not only the frozen text.

## Proposed text for GR2 (splice-ready; replaces the bracketed `[inference for the btrfs-progs side …]`)

Statement continuation, after "…makes a privileged progress query for that devid answer 0" [sentence unchanged]:

> The btrfs-progs side is decided by the pinned v7.1 `cmds/scrub.c` (S237, the source of the host's
> `btrfs-progs 7.1-1`), which names `EINPROGRESS` nowhere. `btrfs scrub start -B` — the packaged unit's
> `ExecStart` — stores the failed ioctl as `ret=-1, errno=115` and reports it through the generic per-device arm:
> `ERROR: scrubbing <path> failed for device id <devid>: ret=-1, errno=115 (Operation now in progress)` on stderr,
> then `scrub canceled for <fsid>` with `Status:           aborted` and `Duration:         0:00:00` on stdout, exit
> status 1; before and after the ioctl it rewrites `/var/lib/btrfs/scrub.status.<fsid>` (all-zero before,
> `canceled=1 finished=1` after), so the failed attempt itself replaces the filesystem's scrub record with an
> `aborted` entry. Without `-B` no refusal text is printed at all — the error and the summary sit behind
> `do_print`, which only `-B` sets — so a plain `btrfs scrub start` prints `scrub started on <path>, fsid <fsid>
> (pid=N)`, then only the child's `Starting scrub on devid <devid>`, and exits 0 while the child exits 1 without any
> refusal text. `btrfs scrub status` asks the kernel once per filesystem
> and prints `running` only where the record holds an entry for that devid: with an entry it prints
> `Status:           running` beside the record's old timestamps and byte counts (a finished record even labels the
> device `history` while printing `running`); with no entry, the normal case since only a scrub start writes the
> record, `status -d` prints `Scrub device <path> (id <devid>) ` and `no stats available` with no `Status:` line,
> and the summary form prints `no stats available` followed by `Time left:        0:00:00`, an `ETA` of now,
> `Total to scrub` of the filesystem's used bytes and `Bytes scrubbed:   0.00B  (0.00%)` — a scrub at zero percent,
> without a `Status:` line. Both status forms exit 0,
> so neither the start nor the status tells the operator that a *replace* is what holds the scrub machinery.

Quote block to add (each verified in the frozen file):

**Quote.** `S237` scrub.c:965: "ret = ioctl(sp->fd, BTRFS_IOC_SCRUB, &sp->scrub_args);"
**Quote.** `S237` scrub.c:969: "sp->stats.canceled = !!ret;"
**Quote.** `S237` scrub.c:970: "sp->ioctl_errno = errno;"
**Quote.** `S237` scrub.c:1620: "switch (sp[i].ioctl_errno) {"
**Quote.** `S237` scrub.c:1633: ""scrubbing %s failed for device id %lld: ret=%d, errno=%d (%m)","
**Quote.** `S237` scrub.c:1725: "if (err)"
**Quote.** `S237` scrub.c:1523: "pr_default("scrub %s on %s, fsid %s (pid=%d)\n","
**Quote.** `S237` scrub.c:1679: "pr_default("scrub %s for %s\n", append, fsid);"
**Quote.** `S237` scrub.c:1502: "/* write all-zero progress file for a start */"
**Quote.** `S237` scrub.c:1200: "ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);"
**Quote.** `S237` scrub.c:1201: "if (!ret)"
**Quote.** `S237` scrub.c:1946: "in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);"
**Quote.** `S237` scrub.c:1962: "last_scrub->stats.in_progress = in_progress;"
**Quote.** `S237` scrub.c:341: "(ss->in_progress ? "running" :"
**Quote.** `S237` scrub.c:320: "if (!ss || !ss->t_start) {"
**Quote.** `S237` scrub.c:321: "pr_default("\tno stats available\n");"
**Quote.** `S237` scrub.c:352: "pr_default("\nScrub device %s (id %llu) %s\n", di->path, di->devid,"
**Quote.** `S237` scrub.c:186: "if (s->in_progress) {"
**Quote.** `S237` scrub.c:201: "pr_default("Bytes scrubbed:   %s  (%.2f%%)\n","
**Quote.** `S237` scrub.c:2007: "return !!err;"

Shorter variant, if the row must stay brief:

> The btrfs-progs side is decided by S237 (v7.1, the host's 7.1-1), which names `EINPROGRESS` nowhere: `scrub start
> -B` reports the refusal only through its generic arm, `ERROR: scrubbing <path> failed for device id <devid>:
> ret=-1, errno=115 (Operation now in progress)` (scrub.c:1633), exits 1, and rewrites the filesystem's scrub record
> as `canceled=1 finished=1` (scrub.c:969,974,1701-1707); without `-B` it prints `scrub started … (pid=N)` and exits
> 0 with no refusal text (scrub.c:1249,1523-1529). `scrub status` prints `Status:           running` only where the
> record has an entry for the devid (scrub.c:1962,341); with no entry — the replace case — `-d` prints `Scrub device
> <path> (id <devid>) ` + `no stats available` (scrub.c:352-353,320-321) and the summary form prints `no stats
> available` then `Time left: 0:00:00`, `ETA` now, `Bytes scrubbed: 0.00B  (0.00%)` (scrub.c:186-203), both exit 0
> (scrub.c:2007): neither command names the replace.

Follow-on edit the row needs in "How this changes OS triage", second bullet: after "check the replace first (GR2)",
add that with the unit's `-B` the journal carries `ERROR: scrubbing … failed … errno=115`, while a hand-run
`btrfs scrub start` prints `scrub started … (pid=N)` and exits 0, and that `btrfs scrub status` keeps saying
`no stats available` (or, with an old record, `running`) rather than naming the replace.

## Limits / what I did not do

- I did **not** run `btrfs scrub start` (forbidden by the wave guard) and did not run a privileged status; nothing
  was started, stopped, mounted, or written to sysfs, and no replace exists. Branch (b) and the privileged half of
  (a) are **source-derived predictions**, marked as such inline; only the unprivileged rendering, the `ERROR: `
  prefix, the format strings and the stream/exit facts are observed.
- The "Operation now in progress" text is the host C library's `strerror(115)` (observed via Python), not a
  btrfs-progs string; the binary contains no `in progress` string of its own (`strings -a /usr/bin/btrfs | grep -i
  "in progress"` → balance/rescan/replace strings only, the closest being `scrub is in progress`, which is
  `cmds/replace.c:60` — the reverse direction, a replace start refused while a scrub runs).
- Version scope: the pinned file is upstream v7.1 and the host package is `7.1-1`; I did not diff the Arch
  package's patched source, only its binary strings (all quoted format strings present).
- GR2's kernel half (S247/S242) was read, not re-verified; my quotes from it are the row's own.
- Cost: no counters run (neither C1 nor C2), no tools installed.

## Cleanup

Scratch `/fast/scratch/hyaku/tsukuroi-r45/C2ExecGR2Progs/` (the v7.1 clone, `messages.c/.h`, `strings` dump,
`status-probe.txt`) is removed after the receipts were copied to
`.ufo/waves/round-45/a2w1/C2ExecGR2Progs/` (`status-probe.txt`, `provenance.txt`). Only this report and those two
receipt files were written in the lane; no tracked lane file was touched.
