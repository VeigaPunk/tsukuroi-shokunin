ROW SC4 VERDICT: partly

Seat C2CritSC4, item V-4b (counted row verdict, adversarial), wave w2 of round 42 (hyaku run 9).
Row under test: `corpus/knowledge/btrfs-scrub-record-r42.md:91-121` (`## SC4`), the integrated text at the dispatch
tip `78abb8b5cdc9da511b4fc523e661517a68dd33d3`. The file is byte-identical at the dispatch tip and at the lane tip
I found (`a968393c`), and carries no `Corrections` section:

```
$ sha256sum corpus/knowledge/btrfs-scrub-record-r42.md
536846f6cb49c2c41cc48228bb03945da0d232dff28c89b35164dc88ee445ef8  corpus/knowledge/btrfs-scrub-record-r42.md
$ git show 78abb8b5cdc9da511b4fc523e661517a68dd33d3:corpus/knowledge/btrfs-scrub-record-r42.md | sha256sum
536846f6cb49c2c41cc48228bb03945da0d232dff28c89b35164dc88ee445ef8  -
$ git show 78abb8b5…:corpus/knowledge/btrfs-scrub-record-r42.md | grep -c -i correction
0
```
(`git diff 78abb8b5…HEAD -- corpus/knowledge/btrfs-scrub-record-r42.md` is empty; `##` headings at 17/42/64/91/122/
142/152/161 only.)

Nothing was written in the lane outside this report and this seat dir; no git/jj mutation, no host mutation, no
scrub, no sudo, no pacman. Scratch was `/fast/scratch/hyaku/tsukuroi-r42/C2CritSC4/`, removed with `rm -rf` at the end
and then verified absent, after the receipts below were copied.

## 0. Pins verified before reading

```
$ cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS
scrub.c: OK
CHANGES: OK
$ sha256sum frozen/hostcap/capture.txt
942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c  capture.txt   # = doc header
```
The snapshot digests match the entry header (line 2), the counter's `SNAP` (`tools/check-scrub-record-r42.py:48-51`)
and the capture pin.

## 1. Every Quote line resolves (7/7)

`sed -n '<n>p' scrub.c` for each quoted line, observed verbatim:

| quote | line text | in the SC4 window (280-330 / 1925-1945)? |
|---|---|---|
| :1931 | `if (fdres < 0 && fdres != -ENOENT) {` | yes |
| :300 | `_SCRUB_FS_STAT_ZMIN(ss, t_start, fs_stat);` | yes |
| :303 | `_SCRUB_FS_STAT_ZMAX(ss, canceled, fs_stat);` | yes |
| :304 | `_SCRUB_FS_STAT_MIN(ss, finished, fs_stat);` | yes |
| :310 | `fs_stat->s.finished = 1;` | yes |
| :321 | `pr_default("\tno stats available\n");` | yes |
| :342 | `(ss->canceled ? "aborted" :` | yes |

No quote is wrong, on the wrong line, or outside the counter's window. Nothing in the row misquotes the source.

## 2. Sentence-by-sentence audit

### S1 (lines 93-94) — "treats a missing record as no history (… ENOENT is not an error; any other open failure … exits with an error)"

`scrub.c:1927-1940`: the **progress socket is tried first**; only if `connect` fails does the code open the record
(`fdres = scrub_open_file_r(SCRUB_DATA_FILE, fsid)`, :1930), and the ENOENT / other-error split is at :1931-1936
(`err = 1` → `return !!err` at :2007). So the parenthetical is **true**: ENOENT leaves `err` 0 and `past_scrubs`
NULL; any other negative returns a warning plus exit 1. Verified against the code and against this host's real run
(§4). **Incomplete**: if a scrubbing process is live, `connect` succeeds, `fdres` is the socket, `scrub_read_file`
parses the socket (:1939-1940) and the record file is never opened — so a *missing* record is not "no history"
then. Reachable by deleting the record while a scrub runs, or when the first record write failed (:1505-1509) but
the socket bound (:1459-1499). See F3 for replacement text.

### S2 (lines 94-96) — "the start time is the smallest device start (`_SCRUB_FS_STAT_ZMIN`, where an unset value is always replaced)"

Macro body `scrub.c:268-273`: `if (!fs_stat->s.name || fs_stat->s.name > ss->name) fs_stat->s.name = ss->name;`.
"Smallest" and "an unset accumulator is always replaced" are both exactly right. **Minor incompleteness**: the
guard tests only the *accumulator*, so a device value of 0 also replaces a set accumulator — i.e. a record whose
`t_start` is 0 pins the fold at 0 and the summary prints `no stats available`. That state is normal, not corrupt:
the CLI writes an all-zero record when a scrub starts (`scrub.c:1501-1504`, comment ": write all-zero progress file
for a start") *before* `t_start` is assigned (:1558), and the progress thread only rewrites it after a
`poll(…, 5*1000)` (:1043) or a socket accept. So during the first seconds of a live scrub the summary says
`no stats available` even though the run is in progress. No falsehood here — S5's last clause already covers the
output — but the mechanism is unstated. Optional one-clause addition in F4.

### S3 (line 96) — "the run counts as canceled if any device was canceled"

`_SCRUB_FS_STAT_ZMAX(ss, canceled, fs_stat);` at :303, body at :275-280 (max, and only over folded devices).
**True.**

### S4 (lines 96-98) — "finished only if every device that has a record in the file is finished (…)"

`init_fs_stat` sets `finished = 1` (:307-311) and `_SCRUB_FS_STAT_MIN` (:261-266, invoked at :304) takes the minimum
over the folded devices; devices without a record `continue` (:1983-1984). **Overreach**: the fold does *not*
iterate records, it iterates the filesystem's **current** device list — `for (i = 0; i < fi_args.num_devices; ++i)`
(:1975) with `last_dev_scrub(past_scrubs, di_args[i].devid)` (:1981-1982), and `last_dev_scrub` only matches a
record's `devid` (:1136-1150). A record line whose devid is no longer in the fs is never folded. Such a line is
reachable: the writer rewrites the whole file with exactly the current device set on every write (:922-925
`scrub_write_file` + `rename`; n = `fi_args.num_devices` at :1503 and :1702-1703), so a device that was removed or
replaced after the last write leaves its line behind until the next scrub rewrites the file. Counterexample: two
devices, a scrub where dev 1 finished and dev 2 did not, then `btrfs device remove` of dev 2 — the summary prints
`finished` while the file still holds an unfinished line. Under the reading "device = a device of this filesystem"
the sentence survives; as written ("every device that has a record in the file") it does not. See F1.

### S5 (lines 99-100) — "running … else aborted … else finished, else interrupted; with no start time … `no stats available`"

`_print_scrub_ss` :313-345: early return with `no stats available` when `!ss->t_start` (:319-322); otherwise the
exact ternary `in_progress ? "running" : canceled ? "aborted" : finished ? "finished" : "interrupted"`
(:339-343). `fs_stat.s.in_progress = in_progress` at :1974, `in_progress` at :1946 from
`is_scrub_running_in_kernel` (:1190-1205). **True, including the careful verb "reports"** — the kernel returns 0
from `BTRFS_IOC_SCRUB_PROGRESS` only while a scrub context exists (`kscrub.c:3141-3157`:
`return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`). The consequence is F2.

### S6 (lines 100-102) — "An `interrupted` status therefore means an unfinished record with nothing running now … [inference], not a device error"

The flag combination is right; "not a device error" is right (device errors land in the per-device counters).
**The clause "nothing running now" is not entailed by the code**: `in_progress` is only what
`BTRFS_IOC_SCRUB_PROGRESS` says, and that ioctl refuses callers without `CAP_SYS_ADMIN`
(`fs/btrfs/ioctl.c:3291-3292`, `if (!capable(CAP_SYS_ADMIN)) return -EPERM;`), which is the initial user namespace,
so a container/userns root is refused too. On this host, uid 1000, the ioctl returns EPERM (§4), so
`is_scrub_running_in_kernel` returns 0 without asking the kernel anything and `interrupted` is what the summary
prints *during* a live scrub. The row's own Host reading is an unprivileged run, so this is not hypothetical for
the reading it invites. See F2.

### Host reading (lines 118-120) — **true**

`capture.txt:6` is `var_lib_btrfs absent`; `.ufo/waves/round-42/w1/C2ExecHostRecheck.md` §2 records
`btrfs scrub status /` as uid 1000, exit 0, `\tno stats available`, empty stderr. I reproduced it independently:

```
$ strace -f -e trace=socket,connect,openat,ioctl -o strace-status.txt btrfs scrub status / ; echo EXIT=$?
UUID:             1d02a454-c549-4a35-b567-89d60902af8e
	no stats available
Total to scrub:   307.92GiB
Rate:             0.00B/s
Error summary:    no errors found
EXIT=0
```
The wording "the frozen capture holds the absent directory only" is accurate (capture.txt:6 records only the
absence, not any status output). The residual "Total to scrub / Rate / Error summary" lines after
`no stats available` do not contradict the sentence: it claims that line, not that it is the only output.

## 3. Findings (smallest safe corrections)

### F1 — S4 quantifies over the wrong set (overreach; nothing false under the "device of this filesystem" reading)

Evidence: `scrub.c:1975`, `:1981-1986`, `:1136-1150` (read side, current device list only); `:922-925`,
`:1502-1504`, `:1702-1703` (write side, whole-file rewrite of exactly the current devices).

Replace lines 96-98 with:

> counts as canceled if any device was canceled, and it counts as
> finished only if every device **of the filesystem** that has a record in the file is finished (the fold walks the
> filesystem's current device list with `last_dev_scrub`, so a line left behind by a device that has since been
> removed is never folded; the flag starts at 1 and takes the minimum,
> `_SCRUB_FS_STAT_MIN`; devices without a record are skipped).

### F2 — S6 states an observation as a fact about the world (overreach)

Evidence: `scrub.c:1946`, `:1190-1205`; kernel `fs/btrfs/ioctl.c:3291-3292` (`capable(CAP_SYS_ADMIN)`);
`kscrub.c:3156` (0 only with a live scrub ctx); host `strace-status.txt:24`
(`ioctl(3, BTRFS_IOC_SCRUB_PROGRESS, {devid=makedev(0, 0x1)}) = -1 EPERM`).

Replace lines 100-102 with:

> An
> `interrupted` status therefore means an unfinished record and **no run reported by the kernel** — the run is probed
> only through `BTRFS_IOC_SCRUB_PROGRESS`, which needs `CAP_SYS_ADMIN` (this host, uid 1000: `EPERM`), so a caller
> the ioctl refuses reads `interrupted` even while a scrub runs (for example a start process that ended before the
> scrub did) [inference], not a device error.

Reachability caveat, stated so the correction is not overstated: with the shipped mode 0600 on the record (SC1),
a caller without `CAP_SYS_ADMIN` normally fails the record open first and exits 1 at :1931-1936, so F2 needs a
readable record with an unprivileged-or-namespaced ioctl (chmod'ed record, bind-mounted record, userns root). It
is an overreach of the *conditional*, not a claim about the common case.

### F3 — S1 omits the socket branch (incomplete)

Evidence: `scrub.c:1927-1940` (connect first; record opened only on connect failure; `scrub_read_file` runs on the
socket fd).

Replace lines 93-94 with:

> **Statement.** `btrfs scrub status` treats a missing record as no history **when no scrubbing process answers on
> the progress socket** — the socket is tried first (`scrub.c:1927`) and a live scrub's records are read from it, so
> the record file is not opened then; when the socket is absent, an open failure of `ENOENT` is not an error, and any
> other open failure prints a warning and the command exits with an error.

### F4 — S2 omits the zero-t_start poison (minor, optional; not a defect that blocks the row)

Evidence: macro `:268-273` (guard tests only the accumulator), all-zero start record `:1501-1504` written before
`:1558`, first rewrite within the 5 s `poll` at `:1043`.

Optional insertion in lines 94-96, after "always replaced":

> , and a record whose `t_start` is 0 (the all-zero record written when a scrub starts,
> `scrub.c:1501-1504`) pins the fold at 0 and puts the whole summary back to `no stats available`

### Downstream restatement

`btrfs-scrub-record-r42.md:146-149` ("a filesystem `finished` needs every device that has a record finished" and
"`interrupted` is a process outcome (an unfinished record, nothing running)") restates F1 and F2 and needs the same
two qualifiers.

## 4. Counterexamples I tried that did not break the row (anti-false-positive record)

- "aborted must beat running" — no: the ternary order at :339-343 is running → aborted → finished → interrupted,
  exactly as written.
- "`finished` starts at 1 so an empty record prints `finished`" — no: with no folded device `t_start` stays 0 and
  :319-322 returns `no stats available` first; S5 says so.
- "`_SCRUB_FS_STAT_MIN` compares an unsigned flag wrongly" — no: `struct scrub_stats.finished` is `u64`
  (`scrub.c:72-79`).
- "a second writer's flock makes status fail silently" — no: `scrub_open_file` returns the errno, which is not
  ENOENT, so :1931-1936 warns and exits 1 (consistent with S1).
- "ENOENT still exits nonzero" — no: `err` is untouched and `return !!err` (:2007); reproduced here, EXIT=0.
- "a corrupt/header-only record is an error" — no: `scrub_read_file` returns `ERR_PTR(-ENODATA)` (:604-611, at :610), the
  warning at :1941-1944 does not set `err`, and the summary still prints `no stats available` — it does not
  contradict any sentence of the row, it is simply unaddressed.
- "`last_dev_scrub` returns the newest record" — no, it returns the first match (:1136-1150), but the writer emits
  one line per devid, so the row's "the device's record" stays unambiguous.
- Host reading: re-ran the command myself; same output, exit 0, empty stderr (receipts).

## 5. What I did not do

- I did not start, cancel, resume or limit a scrub, and did not write `/var/lib/btrfs`; the socket path (F3) and
  the stale-line fold (F1) are read from the pinned source, not exercised live. This host has a single device and
  no record, so F1's counterexample cannot be staged here without mutating the host.
- I did not have the running kernel's own source: `/lib/modules/7.2.11-arch1-1/build` and `/usr/src/linux-lts` ship
  no `fs/btrfs/scrub.c`. Kernel statements come from `torvalds/linux` tag `v6.12`
  (`https://raw.githubusercontent.com/torvalds/linux/v6.12/fs/btrfs/{scrub.c,ioctl.c}`, fetched 2026-10-26; quoted
  lines `capable(CAP_SYS_ADMIN)` / `return -EPERM;` and `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`) plus the
  host's own strace, which is version-exact.
- I did not run the frozen counter (`tools/check-scrub-record-r42.py`); it is the orchestrator's, it takes several
  CPU-minutes, and this item is a row reading, not a counter run.
- I did not judge, admit, edit, integrate or commit anything.

## 6. Tooling record

No installs or upgrades: `curl` 8.x, `strace` 6.x, `btrfs-progs v7.1` (host 7.1-1) were already present; no
pacman, no uv/npx install, no PATH write.

## 7. Receipts (this seat dir)

- `strace-status.txt` — my unprivileged `strace -f -e trace=socket,connect,openat,ioctl btrfs scrub status /`
  (line 24: the EPERM ioctl; line 23: record open ENOENT; line 22: socket connect ENOENT).
- `status.out`, `status.err` (0 bytes) — the command's output and exit-0 evidence.
- `kscrub-progress.txt`, `kioctl-scrub-progress.txt` — the two kernel functions quoted above, numbered.
- `quotes.txt` — the seven `sed -n '<n>p' scrub.c` resolutions.
