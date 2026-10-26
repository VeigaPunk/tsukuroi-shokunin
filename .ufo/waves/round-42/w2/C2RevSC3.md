ROW SC3 VERDICT: fails

Seat C2RevSC3, item V-3a (counted verdict). Row SC3 of `corpus/knowledge/btrfs-scrub-record-r42.md` at 78abb8b5cdc9da511b4fc523e661517a68dd33d3 (extracted with `git show <commit>:corpus/knowledge/btrfs-scrub-record-r42.md`, receipt-04). The SC3 section has no appended correction paragraphs and the file has no `Corrections` section at that commit.

Preliminaries (all observed, receipt-01):
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-42/frozen/src`: `scrub.c: OK`, `CHANGES: OK`.
- `.ufo/waves/round-42/frozen/hostcap/capture.txt` sha256 = `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c`, matching the row header.
- All five Quote lines verified verbatim on their cited lines by `grep -nF`: scrub.c:1502, :1336, :1507, :1121, :1200. No quote is misplaced.

## Statement, sentence by sentence

S1 "The record is written by the userspace `btrfs scrub start` process, not by the kernel: it writes an all-zero record when the scrub starts (or is resumed) and progress records while it runs."

- Writer attribution: supported. The only record-writing helper is `scrub_write_progress` (scrub.c:897-943, opens via `scrub_open_file_w` at :917); its callers are the progress thread (:1123), the start-of-run write (:1503) and the final write (:1702), all inside `scrub_start`/its thread; `cmd_scrub_resume` delegates to the same `scrub_start(..., resume=true)` (:1831-1834); `cmd_scrub_status` opens the record read-only (:1930). The kernel does not write the file; `BTRFS_IOC_SCRUB_PROGRESS` returns in-memory counters (:1200). Holds.
- "all-zero record when the scrub starts": supported. `sp` is calloc'd (:1402), `resumed=NULL` on a fresh start (:1442), `scrub_resumed_stats` returns the zeroed entry when `resumed` is NULL (:803-804), written at :1501-1504; the pinned comment says "for a start" (:1502).
- "(or is resumed)": **false**. The same write block executes on resume (no `resume` guard between :1460 and :1510), but each written device line merges the counters carried over from the interrupted record: `_SCRUB_SUM` is `dest->scrub_args.progress.name = data->resumed->p.name + data->scrub_args.progress.name` (scrub.c:795-796), applied for every resumed device (:806-819), with the original `t_start` restored (:823) and duration accumulated (:824-825); `sp[i].resumed = last_scrub` is set for resumed devices (:1430-1434). A resumed scrub therefore rewrites a record carrying the previous run's counters and start time — not an all-zero record. The row's own quote (scrub.c:1502, "for a start") contradicts the extension.
- "progress records while it runs": supported. The progress thread writes when `do_record` (:1121-1125) in its run loop.

S2 "Recording is switched off, with a warning that ends 'status recording disabled', when the directory `/var/lib/btrfs` cannot be created or the first record cannot be written; the scrub itself still runs."

- Supported. mkdir failure: `mkdir_p(datafile)` fails → warning `"cannot create scrub data file, mkdir %s failed: %m, status recording disabled"` and `do_record = false` (scrub.c:1335-1339); after `%m` expansion the rendered warning ends "status recording disabled". First write failure: `if (do_record)` all-zero write fails → warning `"failed to write the progress status file: %m, status recording disabled"` and `do_record = false` (:1505-1509). In both cases execution continues into the scrub (:1341 onward; fork at :1512-1513), and with `do_record=false` the thread skips record writes (:1121-1122) and the final write is skipped (:1701). Holds.
- Minor caveat, not a defect of the sentence: `mkdir_p` (common/utils.c) is not in the pinned snapshot; the row's "the directory /var/lib/btrfs cannot be created" is inferred from `mkdir_p(datafile)` called on the full file path (datafile initialized from `SCRUB_DATA_FILE` at :1269, unchanged before :1335). Consistent, but the helper body is unpinned (see Residual risk).

S3 "Whether a scrub is running is asked from the kernel with the `BTRFS_IOC_SCRUB_PROGRESS` ioctl per device, independent of the file."

- Supported. `is_scrub_running_in_kernel` loops devices (`sp.scrub_args.devid = di_args[i].devid`, :1197-1199), issues `ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, ...)` per device (:1200), returns 1 on the first success (:1201-1202); the function touches no file. Used by `cmd_scrub_status` unconditionally after the optional record read (:1946, not nested in the `fdres` branches) and by start (:1378). Holds.

S4 "A record-write failure later in the run ends the progress writes without that warning; only the final write reports a failure ('failed to record the result')."

- First clause: supported. On write failure the thread does `goto out` and returns the error (:1123-1125, :1130-1133); no warning is printed in the thread.
- "only the final write reports a failure": **false**, in both directions:
  - A mid-run record-write failure IS reported at scrub end (when the start prints, i.e. `-B`/`do_print`): the parent cancels and joins the progress thread at :1685-1687. Either `pthread_cancel` returns ESRCH because the thread already terminated (→ `ret != 0` → `error("progress thread handling failed: %m")`, :1690-1693) or the cancel lands first and `pthread_join` yields the thread's error pointer (→ `error("recording progress failed: %m")`, :1696-1699). Neither message comes from the final write, and "recording progress failed" names the recording itself — contradicting the "only".
  - The final write's own report is conditional: `if (ret && do_print) error("failed to record the result: %m")` (:1704-1706). `do_print` defaults false (:1249) and is set only by `-B` (:1292-1296); a default background start (fork at :1512-1513, child continues at :1546+) prints none of these. So in the default mode even the final write reports nothing — the unconditional claim is wrong there too.

S5 "So a missing record does not prove that no scrub ran: a scrub whose recording was disabled, or one driven by another tool through the ioctl [inference from the write path], leaves none."

- Acceptable as a labeled inference. `do_record=false` is only ever set before/at start (:1338, :1508), so a disabled-recording scrub creates no record; the only record-writing code is the start process's (:917/:1123/:1503/:1702), so an ioctl-driven scrub from another tool leaves none. The inference bracket is honest. Holds (as inference).

S6 "That conclusion was already held (SH4 note); new here are the mechanism and the disable conditions."

- Supported. `corpus/knowledge/storage-health-r26.md` at the pinned commit: SH4 statement (:57) and the RevRowSH4 correction (:133: "older scrubs, or scrubs run with recording disabled, cannot be excluded") already hold that a missing record is not "never scrubbed". Holds.

## Host reading

- "No scrub timer is enabled (`btrfs-scrub@.timer disabled`, capture.txt:8; no `btrfs-scrub@*` timer listed, capture.txt:7)": line 8 is `scrub_timer_unit_file btrfs-scrub@.timer disabled disabled`, line 7 is `scrub_timers_listed 0`. Matches (capture.sh: `systemctl list-unit-files --no-legend 'btrfs-scrub@.timer'` / `list-timers --all --no-legend 'btrfs-scrub@*'`).
- "the current boot's kernel log holds no `scrub: started` or `scrub: finished` line (capture.txt:10)": line 10 is `journal_scrub_lines 0`; capture.sh counts `journalctl -k -b 0 --no-pager -q --grep 'scrub: (started|finished)' | wc -l` — `-b 0` is the current boot, the pattern is exactly those strings. Matches.
- "together with the absent directory (capture.txt:6) ... weaker than 'no scrub ran'": line 6 is `var_lib_btrfs absent`; the conclusion is correctly weaker than "no scrub ran", matching SH4's narrowed wording. Holds.

## Findings (falsify the row as written)

F1. Statement S1, "(or is resumed)": the record written at resume is not all-zero — it merges the resumed counters and original start time (scrub.c:795-796, 803-827, 1430-1434). The pinned comment scopes the zero write to a start (:1502).

F2. Statement S4, "only the final write reports a failure ('failed to record the result')": a mid-run record-write failure is reported from the parent as `progress thread handling failed: %m` or `recording progress failed: %m` (scrub.c:1685-1699) in a printing (`-B`) start, and in the default background start the final write reports nothing either (`do_print` guard, :1704-1706, :1249, :1292-1296).

## Exact replacement text

In S1, replace:
"it writes an all-zero record when the scrub starts (or is resumed) and progress records while it runs"
with:
"it writes an all-zero record when the scrub starts; a resumed scrub rewrites the record through the same call, but each resumed device line merges the counters and start time carried over from the interrupted record (`scrub_resumed_stats`, scrub.c:795-796, 803-827), so only a fresh start writes all-zero — and progress records while it runs"

In S4, replace:
"only the final write reports a failure (\"failed to record the result\")"
with:
"in a `-B` (printing) start the failure is still reported at the end as `progress thread handling failed: %m` or `recording progress failed: %m` (scrub.c:1685-1699); the final write's own failure prints `failed to record the result: %m` only when printing (scrub.c:1701-1707), and a default background start prints none of these"

Suggested additional Quote to bind F2: `S237` scrub.c:1698: `error("recording progress failed: %m");` (verified verbatim at that line by grep -nF).

## Residual risk and gaps

- `mkdir_p` is not in the pinned snapshot (only scrub.c and CHANGES are); S2's directory-creation semantics rest on the call at :1335 plus the warning text, not on a pinned helper body. I did not verify `mkdir_p` behavior from an unpinned source, and per host guard I could not exercise directory creation on the live system.
- My F2 evidence is robust to glibc `pthread_cancel` semantics: if cancel returns ESRCH for the already-terminated thread, :1690-1693 fires; if the cancel succeeds and join returns the thread's error, :1696-1699 fires. I did not experimentally confirm which branch glibc 2.4x takes; either contradicts the row. Side observation on the source (not the row): in the ESRCH branch the join at :1687 is skipped, so `terr` (:1274) is read uninitialized at :1696 — source-level UB worth flagging upstream, outside this row's scope.
- Not done: no scrub was started, no host state was changed, no packages installed (none needed); wave-1 reports were not consulted (this item names none).
- All claims above carry file:line evidence into receipts 01-03 in `.ufo/waves/round-42/w2/C2RevSC3/`; the pinned row text is receipt-04.
