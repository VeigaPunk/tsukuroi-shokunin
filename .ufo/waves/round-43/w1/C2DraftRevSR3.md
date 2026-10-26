VERDICT: defect-found

Seat C2DraftRevSR3, round 43 w1. First-falsifier review (not a counted verdict) of row SR3 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 717b716a8943151ace8657e0ca23d7d9b8434f26. Five of the six
**Statement.** sentences and the **Host reading.** hold against the frozen sources; one sentence partly fails
(its "only a fresh `start` … writes zero counters" clause) and gets proposed replacement text below. All ten
**Quote.** lines verify verbatim on their named lines.

## Freeze and digests

- `cd .ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS` → `ioctl.c: OK` (receipt `digests.txt`).
  Note: the round-43 `SHA256SUMS` lists only ioctl.c (S240); scrub.c (S237) is not in it — `FETCH.txt` states
  scrub.c is the round-42 snapshot, so it was verified at that path:
  `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` →
  `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, matching the declared digest.
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` →
  `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556`, matching the entry header's S241 digest.
- Freeze integrity: re-fetched `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`
  (curl -sSfL, 2026-10-26) → sha256 `48df2e2f…`, byte-identical to the frozen snapshot (receipt
  `scrub-v71-live.c`). The `recheck` instruction in the entry header is therefore exercisable and passes for
  S237.

## Quotes (all ten)

`grep -n -F` over the frozen scrub.c finds every quoted string verbatim on its named line (receipt
`quotes-and-guards.txt`): :1833, :1434 (the same text also occurs at :1437; the row names the
canceled/unfinished branch, which is :1434), :864, :823, :1502, :1698, :1706, :1249, :1295, :1333. All ten fall
inside the SR3 quote windows of `tools/check-scrub-record-r43.py` (:78-80).

## Statement, sentence by sentence

S1 — "`btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`." — **HOLDS.**
`scrub_start`'s fourth parameter is `resume` (scrub.c:1233-1234); `cmd_scrub_start` returns
`scrub_start(cmd, argc, argv, false)` (:1761), `cmd_scrub_resume` returns `scrub_start(cmd, argc, argv, true)`
(:1833).

S2 — "For each device whose last record is canceled or unfinished, resume makes that record the device's
`resumed` source, and every record write passes each device through `scrub_resumed_stats` (in
`scrub_write_file`), which for such a device writes the earlier record's progress counters added to the new
run's, the earlier record's `t_start`, and the two durations summed." — **HOLDS.**
- Selection: `if (resume && last_scrub && (last_scrub->stats.canceled || !last_scrub->stats.finished))` →
  `sp[i].resumed = last_scrub;` (:1430-1434).
- Path: every record write goes `scrub_write_progress` (:897) → `scrub_write_file` (:922) → per-device
  `use = scrub_resumed_stats(&data[i], &local);` (:864, inside `scrub_write_file`, :843-895). The record writes
  are the initial one (:1503), the progress thread's periodic one (:1123), and the final one (:1702).
- Sums: `_SCRUB_SUM` = `data->resumed->p.name + data->scrub_args.progress.name` (:794-795); `t_start` =
  `data->resumed->stats.t_start` (:823); duration = `data->resumed->stats.duration + data->stats.duration`
  (:824-825). A resumed device has `skip` = 0 (:1444), so the guard `if (!data->resumed || data->skip)` (:803)
  lets the sums apply.

S3 — "So the first record a resume writes for a resumed device carries the interrupted run's counters and start
time; only a fresh `start` (no `resumed` source) writes zero counters." — **PARTLY.** First half HOLDS; second
half FAILS as written.
- First half holds: the first record a resume writes is the initial write (:1501-1510), before any scrub thread
  starts. For a resumed device the new run's counters are still zero (`sp` is calloc'd, :1402), so `_SCRUB_SUM`
  writes the interrupted record's counters and :823 writes the interrupted record's `t_start`.
- Second half fails: the pass-through condition in `scrub_resumed_stats` is `!data->resumed || data->skip`
  (:803) — not "no `resumed` source". Under `resume`, a device whose last record is finished (or that is absent
  from the record) takes the else-if branch: `sp[i].skip = 1; sp[i].resumed = last_scrub;` (:1436-1437) — it
  HAS a `resumed` source whenever a finished record exists, yet `scrub_resumed_stats` returns `data` (:803) and
  the initial write (:1503) emits that device's own counters, which are zero at that moment (calloc :1402; the
  skip copy-in :1550-1553 runs later, after the fork). So a resume's first record write does contain
  zero-counter entries. Reproduction-by-reading (no host run): two-device fs, devid 1 canceled, devid 2
  finished → the same first record carries devid 1 = interrupted counters and devid 2 = zeros.

S4 — "Once that first record is written, a failed progress-record write ends the progress thread with its
error, which is printed ("recording progress failed") only when `do_print` is set, and a failed final write
prints "failed to record the result" under the same condition." — **HOLDS.**
- The qualifier is right: if the FIRST write fails, `do_record` is set false (:1505-1509) and the thread never
  writes (`if (!spc->do_record) continue;` :1121-1122).
- Thread: `ret = scrub_write_progress(...); if (ret) goto out;` (:1123-1126) → `return ERR_PTR(ret);` (:1133).
- Print: `if (do_print && terr && terr != PTHREAD_CANCELED) { errno = -PTR_ERR(terr); error("recording progress
  failed: %m"); }` (:1696-1698) — `do_print` is necessary; `terr` comes from `pthread_join` (:1687).
- Final write: `if (ret && do_print) { errno = -ret; error("failed to record the result: %m"); }` (:1704-1706)
  — same condition.

S5 — "`do_print` is false by default, set by `-B`, and cleared again when output is quiet." — **HOLDS.**
:1249 `bool do_print = false;`; :1292-1295 `case 'B': … do_print = true;`; :1332-1333
`if (bconf.verbose == BTRFS_BCONF_QUIET && do_print) do_print = false;` (quiet comes from `-q` →
`bconf_be_quiet()`, :1301).

S6 — "Neither branch assigns the command's `err` status." — **HOLDS.** The progress-thread branch (:1690-1699)
and the final-write branch (:1701-1708) assign only `ret`/`errno` and call `error()`; `err` is untouched there,
so a recording failure does not change the exit status (`if (err) return 1;` :1725-1726 sees only the
device-error count).

H1 — "Not observable on this host: there is no record to resume from (capture.txt:7)." — **HOLDS.**
capture.txt:7 is `var_lib_btrfs absent` (receipt `capture-numbered.txt`); the record lives at
`/var/lib/btrfs/scrub.status` (scrub.c:67 `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`), so with the
directory absent there is no record to resume from. The capture is the unprivileged read-only probe
(capture.sh: BTRFS_IOC_SCRUB_PROGRESS probe, `btrfs scrub status`, `stat`; writes nothing outside its output
file).

## Proposed replacement text (S3, second clause only)

Replace:

"So the first record a resume writes for a resumed device carries the interrupted run's counters and start
time; only a fresh `start` (no `resumed` source) writes zero counters."

with:

"So the first record a resume writes for a resumed device carries the interrupted run's counters and start
time. A device with no `resumed` source, or with `skip` set, is passed through `scrub_resumed_stats` unchanged
and written with its own counters — zero in a run's first record write; under a fresh `start` that is every
device, and under `resume` it is each skipped device (last record finished, or the device absent from the
record), where a skipped device with a finished record carries that record's counters after the skip copy-in."

Supporting lines: :803 (pass-through guard `!data->resumed || data->skip`), :1402 (calloc-zeroed `sp`),
:1503 (initial write), :1442 (start: `sp[i].resumed = NULL;`), :1436-1437 (resume: `sp[i].skip = 1;`
`sp[i].resumed = last_scrub;`), :1550-1553 (skip copy-in). The row's proposition tokens (`scrub_resumed_stats`,
`t_start`, `do_print`, `-B`, `err` — the counter's SR3 props, tools/check-scrub-record-r43.py:77) are
untouched: they live in S2/S4/S5/S6, which are unchanged.

## Out-of-row observation (not proposed as row text)

- The skip copy-in dereferences `sp[i].resumed->p` unconditionally (:1550). A device absent from the record
  takes `skip = 1` with `resumed = NULL` (:1436-1437; `last_dev_scrub` returns NULL at :1141-1142/:1148), so a
  `resume` mixing a resumable device with a device added after the last scrub would segfault there — after the
  initial record write (:1503) has already recorded that device with zero counters. Read from the frozen source
  only; not reproduced (no scrub may be run on this host). Upstream devel (fetched 2026-10-26, receipt
  `scrub-devel.c`) has the identical code at :1549-1555, so this is not a v7.1-only quirk.

## Not done

- No scrub started/resumed/canceled on this host (forbidden by the seat guard); the resume cumulation and the
  recording-failure prints are verified by source reading only.
- No counter run: `tools/check-scrub-record-r43.py` counts wave-2 seats only; this wave-1 review is a first
  falsifier, not a verdict.
- ioctl.c (S240) was digest-verified but not otherwise read: row SR3 cites no ioctl.c lines.
- No tools installed or upgraded (none needed; the pacman pause was not touched).

Receipts: `.ufo/waves/round-43/w1/C2DraftRevSR3/` — `digests.txt`, `quotes-and-guards.txt`,
`capture-numbered.txt`, `scrub-v71-live.c`, `scrub-devel.c`.

Report: .ufo/waves/round-43/w1/C2DraftRevSR3.md
