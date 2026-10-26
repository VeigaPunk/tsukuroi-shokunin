ROW SR3 VERDICT: partly

Seat C2CritSR3 (counted verdict, adversarial) on row SR3 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 (the wave-2
text, read from the lane). Verdict: **partly**.

## Pins verified (2026-10-26)

- `sha256sum .ufo/waves/round-42/frozen/src/scrub.c` → `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` (S237) — matches the declared digest.
- `cd .ufo/waves/round-43/frozen/src && sha256sum -c SHA256SUMS` → `ioctl.c: OK` (S240).
- `sha256sum .ufo/waves/round-43/frozen/hostcap/capture.txt` → `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556` (S241) — matches.
- Receipt: `C2CritSR3/quotes-verified.txt`, `C2CritSR3/source-facts.txt`.

## Quotes (all fourteen verified verbatim at named lines)

1833, 1434, 864, 803, 819, 823, 1436, 1402, 1502, 1698, 1706, 1249, 1295, 1333 — every quoted string
matches `sed -n <n>p` on the frozen scrub.c (leading tabs stripped). No quote is displaced.

## Sentence-by-sentence read (against S237 only; SR3 cites no ioctl.c lines)

1. "`btrfs scrub resume` runs the same function as `start`, `scrub_start(…, true)`." — HOLDS. 1833
   `return scrub_start(cmd, argc, argv, true);` vs 1761 `false`.

2. "For each device whose record (`last_dev_scrub`) is canceled or unfinished, resume makes that record the
   device's `resumed` source" — HOLDS. 1427 `last_scrub = last_dev_scrub(past_scrubs, devid);`, 1430-1434
   `if (resume && last_scrub && (last_scrub->stats.canceled || !last_scrub->stats.finished)) { … sp[i].resumed = last_scrub; }`.

3. "every record write passes each device through `scrub_resumed_stats` (in `scrub_write_file`)" — HOLDS.
   All record writes go through `scrub_write_progress` (897) → `scrub_write_file` (922) → per-device
   `use = scrub_resumed_stats(&data[i], &local);` (864). Call sites: 1503 (initial, pre-fork), 1123 (progress
   thread), 1702 (final); the peer-socket write 1112 also uses `scrub_write_file`.

4. "which for such a device writes the record's thirteen counted progress fields added to the new run's, the
   record's `t_start`, and the two durations summed, while `last_physical`, `canceled` and `finished` come from
   the new run and `t_resumed` is taken from the new run's `t_start`." — HOLDS. 806-818 are exactly thirteen
   `_SCRUB_SUM` fields; 823 `dest->stats.t_start = data->resumed->stats.t_start;`; 824-825 durations summed;
   819 `_SCRUB_COPY(dest, data, last_physical);`; 820-821 canceled/finished from `data`; 822
   `dest->stats.t_resumed = data->stats.t_start;`.

5. "So the first record a resume writes for a resumed device carries the interrupted run's counters and start
   time." — HOLDS. The initial record (1501-1510) is written before any ioctl thread exists (1565/1585);
   `sp` is calloc-zeroed (1402), so for a resumed device `_SCRUB_SUM` = 0 + record's fields and 823 writes the
   record's `t_start`.

6. "A device without a `resumed` source, or one that resume skips (`skip` set: its record is finished, or it
   has no record), passes through unchanged, and in a run's first record its counters are zero (`sp` is
   zero-allocated); under a fresh `start` that is every device." — PARTLY. The pass-through (803
   `if (!data->resumed || data->skip) return data;`), the first-record zeros (calloc 1402; pre-fork write 1503),
   and "under a fresh `start` that is every device" (1440-1443: `resumed = NULL` for all, `skip = 0` at 1444)
   all hold. The parenthetical's skip-condition characterization is narrower than the lines support: skip is set
   only for a record that is finished **and not canceled**, or absent (1435-1438 set `skip = 1` only when the
   1430-1431 resume condition fails). A record that is both finished and canceled is real and reachable:
   `scrub_one_dev` sets `sp->stats.canceled = !!ret` and `sp->stats.finished = 1` for every scrub whose ioctl
   returns an error (969, 974; ECANCELED is an expected outcome, 1626-1627), and the record carries both flags
   (820-821). Such a record is resumed, not skipped. As written, "its record is finished" overstates the skip
   condition for that state. Exact narrower text: "(`skip` set: its record is finished and not canceled, or it
   has no record)". (Out-of-row context, read from the pinned source only, not reproduced: for a skipped device
   with no record the child copy-in at 1550 dereferences `sp[i].resumed->p` unconditionally, so a resume mixing a
   resumable device with a record-less device faults after the initial record write; this does not contradict any
   statement sentence.)

7. "Once the first record is written, a failed progress-record write ends the progress thread with its error,
   which is printed ("recording progress failed") only when `do_print` is set, and a failed final write prints
   "failed to record the result" under the same condition." — HOLDS. 1121-1126 `if (ret) goto out;` → 1133
   `return ERR_PTR(ret);`; print gated by `do_print` (and `terr != PTHREAD_CANCELED`) at 1696-1699; final write
   1701-1708 prints only under `do_print`.

8. "`do_print` is false by default, set by `-B`, and cleared again when output is quiet." — HOLDS. 1249, 1295,
   1332-1333.

9. "Neither branch assigns the command's `err` status." — HOLDS. 1690-1708 touch only `ret`/`errno`; the return
   path (1725-1736) uses `err`, `nothing_to_resume`, `e_uncorrectable`, `e_correctable`.

**Host reading.** — HOLDS. capture.txt:7 = "var_lib_btrfs absent"; no record exists to resume from. (No scrub,
record write, or ioctl was run on this host.)

## Wave-1 integration check

The integrated text answers the wave-1 attacks: the count and source of each summed field (DraftCrit F3), the
`last_dev_scrub` naming (F5), the zero-counter sentence scoped to a run's first record with the skip/no-source
pass-through (DraftRev S3, DraftCrit F2, CallGraph D1), the `do_print` quiet-clearing, and the error-print
gating. The rejected F1 claim ("device id is never emitted") is indeed false: `scrub_writev` writes its own
formatted buffer (782-792 `return scrub_write_buf(fd, buf, ret);`), so the devid digits follow the colon; the
extra `scrub_write_buf(fd, buf, ret)` at 868 with ret==0 writes nothing. Reader state 4 (693-698) accepts the
line. Resume selection is therefore reachable for self-written records; the row's sentences stand as code
description. The residual defect I find is the skip-condition parenthetical of sentence 6 (above).

## What I did not do

No scrub start/cancel/resume, no record write, no btrfs ioctl, no /var/lib/btrfs access, no host mutation, no
counter run (this seat returns a verdict line; the frozen counter is the L1's), no git/jj mutation, no installs,
no subagent dispatch. All reading was on the frozen S237/S241 files and the lane text at 8acf0b0.

Report: .ufo/waves/round-43/w2/C2CritSR3.md
