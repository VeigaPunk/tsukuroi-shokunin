ROW SR3 VERDICT: holds

Seat C2RevSR3 (reviewer), round 43 wave w2, item V-SR3-R. Row SR3 of `corpus/knowledge/btrfs-scrub-record-r43.md` at 8acf0b022586a0f3164c77659fb96ba5f90949b6. Sources: S237 = round-42 frozen `src/scrub.c` (btrfs-progs v7.1), S240 = round-43 frozen `src/ioctl.c` (Linux v7.2.11), S241 = round-43 frozen `hostcap/capture.txt`.

## Pins (verified)

- `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` → `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` (matches the claim).
- `cd .ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS` → `ioctl.c: OK` (ioctl.c sha256 `7b3488f2…4ba01`).
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` → `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` (matches the claim).
- Row text read via `git -C <lane> show 8acf0b022586a0f3164c77659fb96ba5f90949b6:corpus/knowledge/btrfs-scrub-record-r43.md`; SR3 section = lines 51-95 of that text (`## SR3` to `## SR6`).

## Quotes — all 14 verbatim on their named lines (S237 scrub.c)

Checked by reading the pinned scrub.c at the named lines:

- :1833 `return scrub_start(cmd, argc, argv, true);` ✓
- :1434 `sp[i].resumed = last_scrub;` ✓
- :864 `use = scrub_resumed_stats(&data[i], &local);` ✓
- :803 `if (!data->resumed || data->skip)` ✓
- :819 `_SCRUB_COPY(dest, data, last_physical);` ✓
- :823 `dest->stats.t_start = data->resumed->stats.t_start;` ✓
- :1436 `sp[i].skip = 1;` ✓
- :1402 `sp = calloc(fi_args.num_devices, sizeof(*sp));` ✓
- :1502 `/* write all-zero progress file for a start */` ✓
- :1698 `error("recording progress failed: %m");` ✓
- :1706 `error("failed to record the result: %m");` ✓
- :1249 `bool do_print = false;` ✓
- :1295 `do_print = true;` ✓
- :1333 `do_print = false;` ✓

## Statement — every sentence supported (lines checked per sentence)

1. "`btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`." — `cmd_scrub_resume` calls `scrub_start(cmd, argc, argv, true)` (scrub.c:1831-1835); `cmd_scrub_start` calls `scrub_start(cmd, argc, argv, false)` (:1759-1763). Same function `scrub_start` (:1233-1234). ✓
2. "For each device whose record (`last_dev_scrub`) is canceled or unfinished, resume makes that record the device's `resumed` source" — :1427 `last_scrub = last_dev_scrub(past_scrubs, devid);`; :1430-1434 `if (resume && last_scrub && (last_scrub->stats.canceled || !last_scrub->stats.finished)) { … sp[i].resumed = last_scrub; }`. ✓
3. "every record write passes each device through `scrub_resumed_stats` (in `scrub_write_file`), which for such a device writes the record's thirteen counted progress fields added to the new run's, the record's `t_start`, and the two durations summed, while `last_physical`, `canceled` and `finished` come from the new run and `t_resumed` is taken from the new run's `t_start`." — `scrub_write_file` calls `scrub_resumed_stats(&data[i], &local)` per device (:864); `scrub_resumed_stats` (:800-828): 13 `_SCRUB_SUM` fields where `dest = data->resumed->p.name + data->scrub_args.progress.name` (:795-796, :806-818), `last_physical` copied from new run (:819), `canceled`/`finished` from new run (:820-821), `t_resumed = data->stats.t_start` (:822), `t_start = data->resumed->stats.t_start` (:823), `duration = resumed duration + data duration` (:824-825). `scrub_write_progress` calls `scrub_write_file` (:922). ✓
4. "So the first record a resume writes for a resumed device carries the interrupted run's counters and start time." — resumed device has `sp[i].resumed = last_scrub` (:1434), so the first record write (:1501-1504 via `scrub_write_progress`, then `scrub_write_file`) goes through the sum path: counters include resumed/old values and `t_start` is the resumed record's (:823). ✓
5. "A device without a `resumed` source, or one that resume skips (`skip` set: its record is finished, or it has no record), passes through unchanged" — `scrub_resumed_stats` returns `data` unchanged when `!data->resumed || data->skip` (:803-804); skip set when a resume target has no record or its record is neither canceled nor unfinished (:1435-1438). ✓
6. "and in a run's first record its counters are zero (`sp` is zero-allocated)" — `sp = calloc(fi_args.num_devices, sizeof(*sp))` (:1402); unchanged pass-through of the zeroed entry gives zero counters. ✓
7. "under a fresh `start` that is every device." — for `resume == false` every device takes the else branch `sp[i].resumed = NULL` (:1439-1443). ✓
8. "Once the first record is written, a failed progress-record write ends the progress thread with its error" — progress thread: `ret = scrub_write_progress(...); if (ret) goto out;` (:1121-1126); `out:` returns `ERR_PTR(ret)` (:1131-1133). ✓
9. "which is printed ("recording progress failed") only when `do_print` is set" — `if (do_print && terr && terr != PTHREAD_CANCELED) { … error("recording progress failed: %m"); }` (:1690-1698). ✓
10. "and a failed final write prints "failed to record the result" under the same condition." — `if (ret && do_print) { … error("failed to record the result: %m"); }` (:1701-1707). ✓
11. "`do_print` is false by default, set by `-B`, and cleared again when output is quiet." — `bool do_print = false;` (:1249); `case 'B': … do_print = true;` (:1292-1295); `if (bconf.verbose == BTRFS_BCONF_QUIET && do_print) do_print = false;` (:1331-1333). ✓
12. "Neither branch assigns the command's `err` status." — the progress-record failure path (:1696-1698) and the final-write failure path (:1704-1707) set `errno` and print but never assign `err`; exit status derives from `err` at :1725-1726. ✓

No sentence of the Statement is marked [inference]; no sentence says more than the lines support.

## Host reading — supported

"Not observable on this host: there is no record to resume from (capture.txt:7)." — capture.txt:7 `var_lib_btrfs absent`, consistent with capture.txt:2 (uid 1000, no effective caps). The sentence states non-observability and is supported by the capture line. ✓

## Conclusion

Every sentence of SR3's Statement and Host reading is supported by the pinned lines (S237 scrub.c, S241 capture.txt); all 14 quotes are verbatim on their named lines; pins verify. No false sentence, no over-claiming unmarked sentence. VERDICT: holds.
