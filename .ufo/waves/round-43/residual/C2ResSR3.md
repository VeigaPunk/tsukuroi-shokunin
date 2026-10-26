ROW SR3 VERDICT: holds
 Seat C2ResSR3 (counted residual verdict), round 43 residual call, hyaku run 9. Row SR3 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 5647d4ff94f5882f99c02d20ec703d0191aea2d9, read via
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 5647d4ff…:corpus/knowledge/btrfs-scrub-record-r43.md`;
the `## SR3` section is lines 51-95 of that text (receipt `C2ResSR3/SR3-at-5647d4ff.numbered`). Sources: S237 =
`.ufo/waves/round-42/frozen/src/scrub.c` (btrfs-progs v7.1), S241 = `.ufo/waves/round-43/frozen/hostcap/capture.txt`.
Row SR3 cites only S237 and S241; I did not need S240 for this row.

## Pins (verified 2026-10-26)

- `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` → `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` (matches the declared pin).
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` → `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` (matches the declared pin).

## Quotes — all 14 verbatim on their named lines

Verified two ways: `sed -n <n>p` with `cat -A` (only leading tabs differ; the row strips leading whitespace) and a
programmatic strip-compare of every row quote against its named line (receipt `C2ResSR3/quotes-verified.txt`):
1833, 1434, 864, 803, 819, 823, 1436, 1402, 1502, 1698, 1706, 1249, 1295, 1333 — 14 checked, 14 OK, 0 mismatches.

## Wave-2 reads and the narrowing (item 6)

- `.ufo/waves/round-43/w2/C2RevSR3.md` = `holds` (at 8acf0b022586a0f3164c77659fb96ba5f90949b6).
- `.ufo/waves/round-43/w2/C2CritSR3.md` = `partly`, item 6 only: the skip parenthetical "its record is finished,
  or it has no record" overstates the skip condition for a record that is both finished and canceled (1430-1431
  resumes `canceled || !finished`; 1435-1438 set `skip = 1` exactly when that disjunction fails); its demanded
  narrower text: "(`skip` set: its record is finished and not canceled, or it has no record)".
- At 5647d4ff the parenthetical (row lines 59-61) reads exactly "(`skip` set: its record is finished and not
  canceled, or it has no record)" — byte-identical to the demanded narrower text. The narrowing answers the `partly`.
- I re-derived the condition myself from the pinned source: 1427 `last_scrub = last_dev_scrub(past_scrubs, devid);`,
  1430-1434 resume branch `if (resume && last_scrub && (last_scrub->stats.canceled || !last_scrub->stats.finished))`,
  1435-1438 `else if (resume) { sp[i].skip = 1; sp[i].resumed = last_scrub; continue; }`. So under resume, skip is set
  iff the record is absent (no `last_scrub`) or `!(canceled || !finished)` = finished and not canceled. De Morgan
  confirms the narrowed parenthetical exactly; the both-flags record (`canceled && finished`, set at 969/974 for a
  failed ioctl) is resumed, not skipped. No contradiction remains.

## Statement — per-sentence line checks (S237 scrub.c unless noted)

1. "`btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`." — 1833 `return scrub_start(cmd, argc, argv, true);` vs 1761 `return scrub_start(cmd, argc, argv, false);`, same function defined at 1233-1234. Checked: 1833, 1761, 1233-1234.
2. "For each device whose record (`last_dev_scrub`) is canceled or unfinished, resume makes that record the device's `resumed` source" — 1427, 1430-1434. Checked: 1427, 1430-1434.
3. "every record write passes each device through `scrub_resumed_stats` (in `scrub_write_file`), which for such a device writes the record's thirteen counted progress fields added to the new run's, the record's `t_start`, and the two durations summed, while `last_physical`, `canceled` and `finished` come from the new run and `t_resumed` is taken from the new run's `t_start`." — every record write goes through `scrub_write_progress` (897) → `scrub_write_file` (922) → per-device `use = scrub_resumed_stats(&data[i], &local);` (864); call sites 1503 (initial, pre-fork), ~1121-1123 (progress thread), 1702 (final); the peer-socket write ~1108-1114 also uses `scrub_write_file`. Counted fields: exactly 13 `_SCRUB_SUM` lines (806-818; macro 794-796 sums `data->resumed->p.name + data->scrub_args.progress.name`); `t_start` from the record (823); durations summed (824-825); `last_physical` copied from the new run (819, `_SCRUB_COPY` macro 796-797); `canceled`/`finished` from the new run (820-821); `t_resumed = data->stats.t_start` (822). Checked: 794-797, 800-828, 864, 897-935, 1108-1114, 1121-1126, 1503, 1702.
4. "So the first record a resume writes for a resumed device carries the interrupted run's counters and start time." — initial write 1501-1504 happens pre-fork, before the ioctl/progress threads exist; `sp` calloc-zeroed (1402), so each `_SCRUB_SUM` is 0 + the record's value, and 823 takes the record's `t_start`. Checked: 1402, 1501-1504, 806-818, 823.
5. "A device without a `resumed` source, or one that resume skips (`skip` set: its record is finished and not canceled, or it has no record), passes through unchanged" — 803-804 `if (!data->resumed || data->skip) return data;`; skip set exactly as derived above (1427, 1430-1438). Checked: 803-804, 1427, 1430-1438.
6. "and in a run's first record its counters are zero (`sp` is zero-allocated);" — 1402 calloc; unchanged pass-through of the zeroed entry; initial write at 1503 with comment 1502. Checked: 1402, 1502-1503, 803-804.
7. "under a fresh `start` that is every device." — for `resume == false` every device takes the else branch, `sp[i].resumed = NULL` (1442), then `sp[i].skip = 0` (1444); no device gets a `resumed` source. Checked: 1439-1444, 1761.
8. "Once the first record is written, a failed progress-record write ends the progress thread with its error" — thread loop: `ret = scrub_write_progress(...); if (ret) goto out;` (~1121-1126), `out:` path returns `ERR_PTR(ret)` (~1131-1133); the thread body is `scrub_progress_cycle` (read 1019-1135). Checked: 1020-1135.
9. "which is printed ("recording progress failed") only when `do_print` is set" — 1696-1698 `if (do_print && terr && terr != PTHREAD_CANCELED) { errno = -PTR_ERR(terr); error("recording progress failed: %m"); }`; `do_print` is a necessary condition of the print ("only when" claims necessity, not sufficiency — no overreach). Checked: 1690-1699.
10. "and a failed final write prints "failed to record the result" under the same condition." — 1704-1707 `if (ret && do_print) { errno = -ret; error("failed to record the result: %m"); }` inside `if (do_record)` (1700-1708). Checked: 1700-1708.
11. "`do_print` is false by default, set by `-B`, and cleared again when output is quiet." — 1249 `bool do_print = false;`; 1292-1295 `case 'B': … do_print = true;`; 1331-1333 `if (bconf.verbose == BTRFS_BCONF_QUIET && do_print) do_print = false;`. Checked: 1249, 1292-1295, 1331-1333.
12. "Neither branch assigns the command's `err` status." — the two failure print branches (1696-1698, 1704-1707) set only `errno` and print; exit status derives from `err` at 1725-1726 (`if (err) return 1;`), with `nothing_to_resume` (1727) and error counters following. Checked: 1690-1708, 1725-1736.

No sentence of SR3 is marked [inference]; none needs the label — every claim above is directly readable from the pinned lines.

## Host reading — supported

"Not observable on this host: there is no record to resume from (capture.txt:7)." — capture.txt:7 is `var_lib_btrfs absent`; consistent with capture.txt:2 (`uid 1000 euid_caps 0000000000000000`). The sentence claims only non-observability and is supported by that line. Checked: capture.txt:2, capture.txt:7.

## Cross-check of the other wave-2 read

C2RevSR3's per-sentence checks (its own quotes section lists the same 14 lines) agree with mine; its text predates the narrowing, and nothing it relied on is weakened by the narrowed parenthetical — the narrowing only tightens sentence 5's condition toward what 1430-1438 encode.

## What I did not do

No scrub start/cancel/resume, no record write, no btrfs ioctl, no `/var/lib/btrfs` access, no host mutation, no
installs, no subagent dispatch, no git/jj mutation anywhere; read-only on the pinned sources and the lane text via
`git show`. I did not run the frozen counters (`score-bootinputs-r43.py`, `check-scrub-record-r43.py`): they are the
L1's instruments and this item's verdict is decided by the pinned source lines, which I checked directly. Scratch
`/fast/scratch/hyaku/tsukuroi-r43/C2ResSR3` was removed after receipts were copied to `C2ResSR3/`.

## Conclusion

Every sentence of SR3's Statement and Host reading is supported by the pinned S237/S241 lines; all 14 quotes are
verbatim on their named lines; the L1's narrowing resolves C2CritSR3's `partly` exactly as demanded, and my own read
of 1427-1444 and 803-804 confirms the narrowed condition is precisely what the code does. No false sentence, no
unmarked over-claiming sentence. Verdict: holds.

Report: .ufo/waves/round-43/residual/C2ResSR3.md
