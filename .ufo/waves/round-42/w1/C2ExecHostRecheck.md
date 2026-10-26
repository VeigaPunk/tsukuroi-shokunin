VERDICT: supports

Item C2-7 (host capture re-run + read-only scrub queries against SC4/SC5). Seat C2ExecHostRecheck, wave w1.
Entry under test: `corpus/knowledge/btrfs-scrub-record-r42.md` rows SC4/SC5 (entry commit f50c28d8, lane tip at
dispatch). Nothing was started, cancelled, resumed, limited, or written outside my scratch and this seat dir; no
sudo, no `pacman`, no host mutation. Ran as uid 1000(vgpnk) (`id` → `uid=1000(vgpnk) ... 998(wheel)`, wheel not
exercised).

## 1. Capture re-run reproduces the frozen capture, timestamp only

Command (exactly the item's, output to scratch, `TMPDIR` set under my scratch):

```
bash .../.ufo/waves/round-42/frozen/hostcap/capture.sh \
  /fast/scratch/hyaku/tsukuroi-r42/C2ExecHostRecheck/capture.txt   # EXIT=0
```

`diff -u frozen/hostcap/capture.txt <rerun>` is one hunk, one line — the timestamp
(receipt `.ufo/waves/round-42/w1/C2ExecHostRecheck/capture-diff.txt`):

```
-captured_utc 2026-10-26T19:13:44Z
+captured_utc 2026-10-26T19:41:05Z
```

With `captured_utc` stripped, both files hash identically — the nine content lines are byte-identical:

```
5ffb601e2b84f1234675f22fdeafecf1c1c51ecda9487c9054efa61c8a840487  frozen.nots
5ffb601e2b84f1234675f22fdeafecf1c1c51ecda9487c9054efa61c8a840487  rerun.nots
```

The frozen capture's own digest still matches the pin in the entry header and in the counter
(`CAPTURE`, `tools/check-scrub-record-r42.py:52`):

```
942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c  frozen/hostcap/capture.txt
```

Content lines re-verified from the re-run (`capture-rerun.txt`): kernel 7.2.11-arch1-1; btrfs-progs 7.1-1;
root_fstype btrfs; root_fsid 1d02a454-c549-4a35-b567-89d60902af8e; `var_lib_btrfs absent`;
`scrub_timers_listed 0`; `scrub_timer_unit_file btrfs-scrub@.timer disabled disabled`;
`scrub_speed_max 1d02a454-…/devinfo/1 0`; `journal_scrub_lines 0`.

## 2. `btrfs scrub status /` — unprivileged, exit 0, prints `no stats available` (SC4 prediction confirmed)

```
$ btrfs scrub status /
UUID:             1d02a454-c549-4a35-b567-89d60902af8e
	no stats available
Total to scrub:   308.83GiB
Rate:             0.00B/s
Error summary:    no errors found
EXIT=0
```

Receipts: `scrub-status.out`, `scrub-status.err` (0 bytes — no warning), `scrub-status-run3.txt`.

So SC4's host reading ("the status summary of this root would print `no stats available`") is now an observed
fact, and its parenthetical "it needs the filesystem open" does not describe an obstacle: the command works
unprivileged against the mounted root, read-only, exit 0, no stderr.

`strace -f -e trace=socket,connect,openat,flock,ioctl btrfs scrub status /` shows exactly the ENOENT path SC4
quotes at `scrub.c:1931`, and no `flock` because the open never succeeded
(`scrub-status.strace:21-26`):

```
socket(AF_UNIX, SOCK_STREAM, 0) = 4
connect(4, {sa_family=AF_UNIX, sun_path="/var/lib/btrfs/scrub.progress.1d02a454-…"}, 110) = -1 ENOENT
openat(AT_FDCWD, "/var/lib/btrfs/scrub.status.1d02a454-…", O_RDONLY) = -1 ENOENT
openat(AT_FDCWD, "/sys/fs/btrfs/1d02a454-…/devinfo/1/scrub_speed_max", O_RDONLY) = 4
```

`-d -R /` prints the per-device line, also `no stats available`, exit 0
(`scrub-dev-and-limit.txt`):

```
UUID:             1d02a454-c549-4a35-b567-89d60902af8e

Scrub device /dev/mapper/root (id 1) 
	no stats available
EXIT=0
```

`/var/lib/btrfs` is still absent after these runs (`ls: cannot access '/var/lib/btrfs': No such file or
directory`), so status created nothing.

## 3. `btrfs scrub limit /` — exit 0, limit column renders the 0 as `-`, not `0`

```
UUID: 1d02a454-c549-4a35-b567-89d60902af8e
Id  Limit              Path
--  -----  ----------------
 1      -  /dev/mapper/root
EXIT=0
```

The sysfs value is 0 (capture.txt:9, re-confirmed), and the table prints `-` because of the else-branch at
`scrub.c:2200-2201` (`table_printf(table, idx++, 2 + i, ">%s", "-");`). So "limit 0" holds in the value plane, but
an operator reading only the table sees a dash that SC5 does not explain. The 0 = unlimited meaning is stated in
the CLI's own help: `scrub.c:2017` ("…, or 0 to reset to unlimited") and `scrub.c:1747` ("--limit SIZE", "set the
throughput limit for each device (0 for unlimited), restored afterwards").

## 4. sysfs mode bits

```
$ stat -c '%a %A %U:%G' /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max
644 -rw-r--r-- root:root
$ [ -w <same path> ] && echo WRITABLE || echo NOT_WRITABLE
NOT_WRITABLE
```

No write was attempted (that would mutate the host); the `-w` test shows an unprivileged write cannot succeed.
Neighbouring devinfo entries are `-r--r--r--` except `scrub_speed_max`, which is `-rw-r--r--` — i.e. the only
writable knob in that directory is the limit, root-only. `btrfs scrub limit` sets it via
`sysfs_write_fsid_file_u64` (`scrub.c:1222-1230`), which is why setting a limit is privileged while reading the
status and the limit is not.

## 5. Findings (refinements, not falsifications)

**(a) Gap: the progress socket is missing from SC1/SC3/SC4.** In btrfs-progs v7.1 `scrub status` does not read
the record file first: it connects to `/var/lib/btrfs/scrub.progress.<fsid>` and reads the record stream from a
running `scrub start` process, falling back to the file only when the connect fails:

- `scrub.c:68`: `#define SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/scrub.progress"`
- `scrub.c:1459`, `1466`, `1488`: the start process `socket()`/`bind()`/`listen()`s that path, and `EADDRINUSE`
  plus a successful `connect` is its "scrub already running" test (`scrub.c:1467-1479`, error text at `1476`).
- `scrub.c:1049`, `1112-1114`: the progress thread `accept()`s and writes the same record stream to the peer.
- `scrub.c:1121`: `if (!spc->do_record) continue;` comes **after** the socket write — so a start process running
  with recording disabled still answers a status query with live progress while leaving no record at all. That is
  the strongest form of SC3's conclusion, and SC3 does not state it.
- Host trace: the connect to that socket is the first thing the command does (line 22 above).

The gap is closeable **inside the frozen quote windows** (window bounds from
`tools/check-scrub-record-r42.py:55-61`): SC4's window `scrub.c 1925-1945` contains `1927`
(`ret = connect(fdres, (struct sockaddr *)&addr, sizeof(addr));`) and `1930`
(`fdres = scrub_open_file_r(SCRUB_DATA_FILE, fsid);`); SC3's window `1110-1125` contains `1112-1114` (the peer
write) and `1121` (`if (!spc->do_record)`). The socket path define at `68` and the `scrub_datafile` call at `1923`
are outside every registered window, so those must not be quoted — citing them would drop `quotes_ok` below 5 and
turn the predicate false. No corpus file mentions the socket (`grep -rn 'scrub\.progress|progress socket|
SCRUB_PROGRESS_SOCKET' corpus/ tools/` → no matches), and CHANGES has no line for the feature, so this is new
depth rather than a duplication.

**(b) SC5 statement covers `scrub start` but does not cite the 6.6.3 bullet for it.** `CHANGES:469` reads
`* scrub start: report the limit if set`; the row quotes only 467 (status) and 468 (limit). 469 is inside SC5's
window `CHANGES 460-470`, so it can be added without disturbing the counter.

**(c) Do not append `btrfs scrub status` output to the frozen capture.** Between 19:41:05Z and 19:43:33Z the
`Total to scrub` line moved 308.83GiB → 308.84GiB → 308.84GiB (three runs, `scrub-status.out`, `scrub-status-run3.txt`);
it is live space usage, not record data, so a byte-compared capture would flake. If the record-absence signal is
wanted in capture.txt, capture a projection (the UUID line plus a presence test for
`/var/lib/btrfs/scrub.status.<fsid>`), not the space line.

## 6. Exact proposed text (frozen-window-compatible; L1 integrates, I did not touch the entry)

SC4 — replace its **Host reading.** paragraph with (still one line, keeps its `capture.txt:<n>` reference, as
`HOST_RE` requires):

> **Host reading.** With no record (capture.txt:6) `btrfs scrub status /` exits 0 unprivileged and prints `no
> stats available` for the filesystem summary, and `-d -R` prints it for devid 1; stderr is empty and
> `/var/lib/btrfs` is still absent afterwards (`.ufo/waves/round-42/w1/C2ExecHostRecheck/scrub-status.out`,
> `scrub-status.err`, `scrub-dev-and-limit.txt`).

SC4, statement addendum (quotes both inside the frozen window 1925-1945):

> Before the record is read, the status command offers the progress socket `/var/lib/btrfs/scrub.progress.<fsid>`
> and takes the record stream from a running `scrub start` instead, opening `SCRUB_DATA_FILE` only when nothing
> answers; the observed command did exactly that (socket `ENOENT`, then file `ENOENT`, no warning).
>
> **Quote.** `S237` scrub.c:1927: "ret = connect(fdres, (struct sockaddr *)&addr, sizeof(addr));"
> **Quote.** `S237` scrub.c:1930: "fdres = scrub_open_file_r(SCRUB_DATA_FILE, fsid);"

SC3, statement addendum (quotes inside window 1110-1125):

> While the scrub runs, the start process also serves the record stream over that socket, and it does so before
> the `do_record` test, so a scrub with recording disabled still shows live progress in `btrfs scrub status` while
> leaving no record.
>
> **Quote.** `S237` scrub.c:1112: "ret = scrub_write_file("
> **Quote.** `S237` scrub.c:1121: "if (!spc->do_record)"

SC5 — replace its **Host reading.** paragraph with, and add the `start` quote:

> **Host reading.** The root's only device (devid 1) reads `scrub_speed_max` 0, no limit (capture.txt:9);
> `btrfs scrub limit /` renders that 0 as `-` in its Limit column (not as `0`), and the file is mode 0644
> root:root, so reading needs no privilege while setting a limit does (`.ufo/waves/round-42/w1/C2ExecHostRecheck/scrub-dev-and-limit.txt`).
>
> **Quote.** `S238` CHANGES:469: "* scrub start: report the limit if set"

## 7. Not done / limits

- No scrub was started, cancelled or resumed, and no `limit -l` was run (forbidden); therefore the `running`
  branch of SC4's status word, `_SCRUB_FS_STAT_*` folding with more than one device, and the `interrupted` case
  remain source-only, not host-observed. The root has a single device (`scrub limit` table, one row).
- A failed sysfs limit read (`scrub.c:1218`) was not induced; only the `0` value path was observed.
- I did not modify the entry, the capture, the counter or any tracked file; the counter was not run (wave-1 C2
  re-check, not my item) and no lane git/jj command was run.
- Receipts (this seat dir): `capture-rerun.txt`, `capture-diff.txt`, `scrub-status.out`, `scrub-status.err`,
  `scrub-status.strace`, `scrub-status-run3.txt`, `scrub-dev-and-limit.txt`. Scratch
  `/fast/scratch/hyaku/tsukuroi-r42/C2ExecHostRecheck/` removed after copying.
- Tooling: nothing installed or upgraded; `strace` was already present (`/usr/bin/strace`).
