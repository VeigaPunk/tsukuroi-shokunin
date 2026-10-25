author: tsukuroi-shokunin L1, round 35 (TsukuroiR35)

# Round-34 wave-2 outputs that were not integrated at filing (landed in round 35 as records)

Round-34 spot-check §5 item 7 (`corpus/lessons/round-34-verifier-spotcheck.md:194`): decide on the
22 untracked `.ufo/waves/round-34/w2/` paths. Round 35 lands them unchanged as records. They are
**not round-34 evidence** (the round-34 report and lesson cite none of them) and **not round-35
evidence**: round 35 re-measures anything it relies on and cites its own receipts.

The spot-check calls them post-filing. That is true of integration, not of every file time. The
report commit `af8bce57` is 2026-10-23 06:27:26 -03:00. File modification times (earliest and
latest file per path, `find -printf '%T…'`, read 2026-10-23 by the round-35 L1):

| Path | Earliest | Latest |
|---|---|---|
| ConnSiblingAfter.md | 06:26:00 | 06:26:00 |
| CritC1AxisFitAfter.md | 06:26:35 | 06:26:35 |
| CritC1AxisFitAfter/ | 06:24:32 | 06:24:32 |
| MutBinGitAlias/ | 06:20:30 | 06:25:01 |
| MutHomeKeep.md | 06:29:15 | 06:29:15 |
| MutHomeKeep/ | 06:19:04 | 06:27:27 |
| MutKeptDrop.md | 06:27:03 | 06:27:03 |
| MutKeptDrop/ | 06:18:32 | 06:24:28 |
| MutNestedNoneBuilder.md | 06:26:36 | 06:26:36 |
| MutNestedNoneBuilder/ | 06:18:28 | 06:25:16 |
| MutRenamedExpanduser.md | 06:30:23 | 06:30:23 |
| MutRenamedExpanduser/ | 06:19:09 | 06:28:08 |
| RegressionAfter.md | 06:34:17 | 06:34:17 |
| RegressionAfter/ | 06:21:08 | 06:28:30 |
| RerunCoredumpReconcile.md | 06:32:12 | 06:32:12 |
| RerunCoredumpReconcile/ | 06:32:12 | 06:32:12 |
| RevAmendment2.md | 06:28:52 | 06:28:52 |
| RevC1Diff.md | 06:28:07 | 06:28:07 |
| RevCensusV5.md | 06:31:01 | 06:31:01 |
| RevHeaderGate.md | 06:30:11 | 06:30:11 |
| RevHeaderGate/ | 06:29:20 | 06:29:20 |
| RevR33NoteRepairs.md | 06:33:10 | 06:33:10 |

All times are 2026-10-23, -03:00. Eight paths have every file written before the filing commit
(CritC1AxisFitAfter/, MutBinGitAlias/, MutKeptDrop/, MutNestedNoneBuilder/ and the reports
ConnSiblingAfter.md, CritC1AxisFitAfter.md, MutKeptDrop.md, MutNestedNoneBuilder.md); they were on disk but not
read into the round-34 record. MutBinGitAlias was recorded in the round-34 lesson as a
`cyber_policy` hold, yet it left `mutant.jsonl` and `pristine.jsonl`; the hold record is corrected
in the round-35 lesson, and under the fleet rule a refusal or safety-filter switch ends the item,
so these bytes stay non-evidence.
