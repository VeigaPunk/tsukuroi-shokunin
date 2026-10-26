ROW SC4 VERDICT: holds

Item V-4a, seat C2RevSC4, wave w2. Row SC4 of `corpus/knowledge/btrfs-scrub-record-r42.md` read at 78abb8b5cdc9da511b4fc523e661517a68dd33d3 (integrated text extracted with `git show 78abb8b5cdc9da511b4fc523e661517a68dd33d3:corpus/knowledge/btrfs-scrub-record-r42.md`; receipt `record-at-78abb8b5.md` in this seat dir). The SC4 section carries no appended corrections and the record has no `Corrections` section at that commit (full 168-line extraction inspected). Pinned sources verified first: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-42/frozen/src` → `scrub.c: OK`, `CHANGES: OK` (exit 0). Frozen capture digest re-hashed: `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c capture.txt`, equal to the pin in the record header.

## Quote lines (7/7 occur at the cited line)

Verified by `grep -n -F` over `.ufo/waves/round-42/frozen/src/scrub.c`:

- scrub.c:1931 `if (fdres < 0 && fdres != -ENOENT) {` — present (the same text also occurs at 1362 in the progress path; 1931 is the cmd_scrub_status occurrence the row means).
- scrub.c:300 `_SCRUB_FS_STAT_ZMIN(ss, t_start, fs_stat);` — present.
- scrub.c:303 `_SCRUB_FS_STAT_ZMAX(ss, canceled, fs_stat);` — present.
- scrub.c:304 `_SCRUB_FS_STAT_MIN(ss, finished, fs_stat);` — present.
- scrub.c:310 `fs_stat->s.finished = 1;` — present.
- scrub.c:321 `pr_default("\tno stats available\n");` — present.
- scrub.c:342 `(ss->canceled ? "aborted" :` — present.

## Statement, sentence by sentence

1. "`btrfs scrub status` treats a missing record as no history (an open failure of `ENOENT` is not an error; any other open failure prints a warning and the command exits with an error)." — TRUE.
   - Missing record → no history: on connect failure (scrub.c:1927-1928) the command opens the record file (1930); with `-ENOENT` the guard at 1931 does not set `err`, `fdres` stays negative so the `if (fdres >= 0)` read at 1939 is skipped and `past_scrubs` stays NULL; `last_dev_scrub` returns NULL for a NULL table (1140-1141), every device is skipped at 1983-1984, `fs_stat` stays at its `init_fs_stat` state (307-311), and `_print_scrub_ss` prints `no stats available` (320-322) via `print_fs_stat` (384-391, called at 1995-1996).
   - ENOENT not an error: scrub.c:1931 excludes `-ENOENT`; `scrub_open_file_r` (497-506) returns `-errno` from `open` (481-483), so a missing file yields exactly `-ENOENT`; `err` stays 0 and `return !!err` (2007) exits 0. Observed: wave-1 `.ufo/waves/round-42/w1/C2ExecHostRecheck.md` §2 — exit 0, empty stderr (`scrub-status.err` 0 bytes), strace shows the ENOENT open.
   - Any other open failure → warning + error exit: scrub.c:1932-1935 (`errno = -fdres; warning("failed to open status file: %m"); err = 1; goto out;`) and 2007 (`return !!err;`) → exit 1. This also covers the `flock(LOCK_EX|LOCK_NB)` failure inside `scrub_open_file` (485-492) and `scrub_datafile` overflow, which surface through the same negative `fdres`.

2. "The filesystem summary folds the per-device lines together: the start time is the smallest device start (`_SCRUB_FS_STAT_ZMIN`, where an unset value is always replaced), the run counts as canceled if any device was canceled, and it counts as finished only if every device that has a record in the file is finished (the flag starts at 1 and takes the minimum, `_SCRUB_FS_STAT_MIN`; devices without a record are skipped)." — TRUE.
   - ZMIN macro (268-273) replaces when the folded value is unset (0) or greater; applied to `t_start` at 300 (and `t_resumed` at 301). "Smallest device start, unset always replaced" is exactly the macro.
   - ZMAX macro (275-280) applied to `canceled` at 303; per-device `canceled` is 0/1, so the max is 1 iff any device was canceled.
   - MIN macro (261-266) applied to `finished` at 304; `init_fs_stat` sets `finished = 1` (309-310); devices with no record `continue` before `add_to_fs_stat` (1983-1986). Min starting at 1 over recorded devices is 1 iff every recorded device is finished.

3. "The status word is `running` when the kernel reports a scrub in progress, else `aborted` when canceled, else `finished`, else `interrupted`; with no start time the summary prints `no stats available` instead." — TRUE.
   - Ternary order running/aborted/finished/interrupted at 340-343. `in_progress` comes from `is_scrub_running_in_kernel` (1946; per-device `BTRFS_IOC_SCRUB_PROGRESS` ioctl at 1200), assigned to the per-device stats (1962) and to `fs_stat.s.in_progress` (1974). `canceled`/`finished` are the folded values of sentence 2. The same `_print_scrub_ss` serves the filesystem summary (`print_fs_stat` 391), so the summary prints the same status word.
   - No start time: `if (!ss || !ss->t_start)` → `no stats available` and return (320-322); with no device record, `t_start` stays 0 from the memset (309). Matches the observed output in w1 §2 (`UUID:` line, then `no stats available`, then the space/limit summary).

4. "An `interrupted` status therefore means an unfinished record with nothing running now (for example a start process that ended before the scrub did) [inference], not a device error." — TRUE as scoped; the speculative mechanism is explicitly tagged `[inference]` in the row.
   - `interrupted` is the ternary fall-through: not in_progress (kernel ioctl negative on every device), not canceled (folded max 0), not finished (folded min 0 ⇒ at least one recorded device unfinished). A status word is printed only when `t_start != 0` (320-322), so `interrupted` presupposes a record with a start time — "an unfinished record with nothing running now" is exact.
   - "not a device error": the status word reads only the three flags (340-343); the error sums are folded separately for display (286-298) and never feed the status word.

## Host reading — TRUE

"With no record (capture.txt:6) the status summary of this root prints `no stats available`: wave-1 seat C2ExecHostRecheck ran `btrfs scrub status /` unprivileged, read-only, exit 0, and it printed that line (`.ufo/waves/round-42/w1/C2ExecHostRecheck.md` §2); the frozen capture holds the absent directory only."

- capture.txt:6 is `var_lib_btrfs absent` (verified by reading lines 1-12 of the frozen capture; digest matches the header pin).
- w1 `C2ExecHostRecheck.md` §2 exists and says exactly that: `btrfs scrub status /`, run as uid 1000 (§ preamble), EXIT=0, output `UUID: 1d02a454-…` / `\tno stats available` / Total / Rate / Error summary. Receipts present on disk: `.ufo/waves/round-42/w1/C2ExecHostRecheck/scrub-status.out` (shows that output), `scrub-status.err` (0 bytes), `scrub-status-run3.txt` (EXIT=0).
- "the frozen capture holds the absent directory only": the frozen capture's nine content lines contain no scrub-status output; the record's absence on this host rests on `var_lib_btrfs absent` (line 6) alone. Correct.

## Checked and dismissed (no finding)

- Progress-socket precedence (w1 finding 5a): `connect` (1927) precedes the file open (1930), and when the socket answers the record file is never opened. No SC4 sentence is false because of this: sentence 1 describes the treatment of a missing record on the file path, and the integrated SC1 at 78abb8b5 fences the socket explicitly ("a different file, created by `bind`, not covered here"). Within that declared scope SC4 does not overreach.
- `last_dev_scrub` returns the first record matching the devid (1142-1145); the record file carries one record per device (rewritten wholesale per run, per SC2/SC3), so "every device that has a record in the file" is device-granular and accurate.
- Read failures (`scrub_read_file` returns ERR_PTR, warned at 1940-1944 without setting `err`) are outside the sentence, which claims only about open failures. No conflict.
- ZMIN would let a zero device `t_start` clear the fold (270-271 replaces a set value with 0); SC4 makes no claim about that edge.

## What I did not do

- I did not run `btrfs scrub status` myself; the host reading's runtime evidence is the wave-1 run, which I verified from its report and on-disk receipts. Nothing in SC4 needs a fresh run.
- I did not compile or execute the pinned `scrub.c`; verification is source reading plus the wave-1 runtime evidence.
- No tools installed (none needed).
