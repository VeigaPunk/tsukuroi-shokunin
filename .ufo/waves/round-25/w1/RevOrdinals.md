Verdict: At claim base b9046016 the six ordinals are depth 8, coverage 9, operability 9, freshness 9, calibration 9 and adjacency 8; every current move record and outside closure agrees with these values once the two superseded statements at lines 68 and 749 are set aside (F3), and the declared rule picks the right value on all six axes. The round-11 axes table that the rule must read (SCORECARD lines 47 to 52) still says coverage 8, freshness 8 and adjacency 7, so checks K02, K04 and K06 would fail at that base (3 of 6 mismatches).

## Scope and method

1. Claim base. Commit b9046016 is "round-24 verifier spot-check (integrator, hyaku): non-author admit/reject", dated 2026-10-22 06:49:31 -0300. Its SCORECARD.md has 782 lines. A copy of those bytes is at /fast/scratch/hyaku/tsukuroi-r25/RevOrdinals/SCORECARD.b9046016.md, sha256 c93edf029ee0b79721434dbc4096e29b7b3d9f3e5e30a477907c9161603297ea. Every SCORECARD line number in this report is a committed-base number. [obs]
2. The working tree is not the claim base. `git diff --stat b9046016 -- SCORECARD.md corpus/lessons` reports `SCORECARD.md | 31 +++` and nothing under corpus/lessons. The 31 uncommitted lines follow line 782; the round-25 declaration sits at working-tree lines 784 to 802 and a refinement block at lines 803 to 813. My first read of the working tree showed 801 lines and a later read showed 813, so the file changed during this review. Lines 1 to 782 are identical in both versions. [obs]
3. Closure sources: corpus/lessons/round-1, round-12 to round-19, round-23 and round-24 verifier spot-check files. The lessons directory has no closure file for rounds 20, 21 or 22. The lane has 24 MANIFEST entries with lane "tsukuroi" under /home/vgpnk/Projects/shokunin/MANIFEST.json `.rounds` (0-based indices): train entries 97, 101, 105, 109, 113, 117, 121, 125, 129 and 133 for rounds 2 to 11, and closure entries 309 (round 1), 324, 331, 336, 344, 352, 365, 371, 389, 404, 416, 422, 436 and 445 (rounds 12 to 24). Index 404 is round 20 and index 422 is round 22, as the SCORECARD cites them. [obs]
4. The declared rule, as refined in the working-tree block at line 807, is the last line in line order, outside the axes table, that matches `\b<axis>\b[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})` with both numbers from 0 to 10. I ran that rule and several variant parsers in Python on the committed copy. These results are my own simulation, not output of the L1 tool. [obs]

## Findings

F1. Current ordinals at b9046016, with every ordinal-form transition after line 53. [obs]
"Spaced" means the axis word, a space, then the numbers. "Glued" means no space, as in `operability9→9`. "Two-cell" means the axis word sits in one table cell and the numbers in the next cell.
- depth 8. Transitions: 256, 324, 388, 424, 446, 492, 517, 537 and 572 (two-cell, all 8→8); 481, 658, 678, 698, 716 and 730 (glued, all 8→8); 759 "recorded against **depth 8 → 8 (tied lowest)**" (spaced, 8→8, last). No depth arrow follows line 759 in the committed file.
- coverage 9. Transitions: 192 "| B | coverage (+ capability `sources-registry`) | 8 → 9 |" (two-cell, 8→9); 224 "**B — coverage 8→9**" (spaced, 8→9, last). Line 224 is the fleet round-1 post-review move and the only coverage move after line 53.
- operability 9. Transitions: 255, 519, 538 and 573 (two-cell, all 9→9); 621 "operability 9→9 (0)" (spaced, 9→9); 659, 679, 699, 717 and 731 (glued, all 9→9; 731 is the last operability arrow in the file).
- freshness 9. Transitions: 193 "| C | freshness | 8 → 9 |" (two-cell, 8→9); 240 "**C — freshness 8→9**" (spaced, 8→9); 425, 447, 518, 539 and 574 (two-cell, all 9→9); 749 "freshness 8 → 8 (tied lowest)" (spaced, 8→8, corrected later, see F3); 772 "C2, originally freshness (actual 9 → 9)" (spaced with "(actual " between the axis word and the numbers, 9→9, last).
- calibration 9. Transitions: 622 "calibration 9→9 (0)" (spaced, 9→9); 680, 700, 718 and 732 (glued, all 9→9); 748 "calibration 9 → 9" (spaced, 9→9); 771 "C1, calibration 9 → 9" (spaced, 9→9, last).
- adjacency 8. Transitions: 191 "| A | adjacency | 7 → 8 |" (two-cell, 7→8); 213 "**A — adjacency 7→8**" (spaced, 7→8, the only real adjacency move); 620 "adjacency 8→8 (0)" (spaced, 8→8, last).
- The lane's own full six-axis statement in the committed file is line 616: "Baseline ordinals: depth8, adjacency8, coverage9, operability9, freshness9, calibration9". The round-25 declaration (working-tree line 786) states the same six values.
- After line 53 there is no ASCII numeric N->M ordinal. The only numeric "->" in the whole file is line 31, "(26->35)", a test count in the move-log row for "adjacency + operability". Lines 32 to 36 contain "alibaba->hyper", which has no digits.

F2. One record disagrees with the six values: the round-11 axes table at lines 45 to 52. [obs]
Depth 8 (line 47), operability 9 (line 49) and calibration 9 (line 51) agree. Coverage 8 (line 48), freshness 8 (line 50) and adjacency 7 (line 52) do not. Their "Last change" cells say r9, r6 and r5, which predate the fleet round-1 moves at lines 191 to 193 and 213 to 240. The lane itself says at lines 295 to 297 that "the later fleet-r1 corrections supersede the historical terminal table", but the table was never edited. [inf] The lane left it in place because the table is the one the rule must read.
Result of checks K01 to K06 at b9046016: K01 depth 8 equals 8, pass. K02 coverage 8 does not equal 9, FAIL. K03 operability 9 equals 9, pass. K04 freshness 8 does not equal 9, FAIL. K05 calibration 9 equals 9, pass. K06 adjacency 7 does not equal 8, FAIL.

F3. Two stale statements also name a wrong value, but both are superseded inside the same committed file. [obs]
- Line 68: "Lowest LIVE axis: **adjacency (7)**." It sits in the 2026-10-15 appendix whose heading is at line 59 and predates the fleet round-1 move at line 191.
- Line 749: "freshness 8 → 8 (tied lowest)" in the round-24 declaration. The lane corrected it at line 759 ("Freshness was 9 at the base, not 8") and in the measured outcome at line 772.
A reader who takes these as current would name adjacency 7 or freshness 8. The arrow rule does not take them, because later arrows for the same axes exist.

F4. The declared rule picks the right value for all six axes at b9046016. [obs]
| axis | line picked by the rule as written | transition text | after-value | matches the declared base value |
|---|---|---|---|---|
| depth | 759 | depth 8 → 8 (tied lowest) | 8 | yes |
| coverage | 224 | coverage 8→9 | 9 | yes |
| operability | 621 as written; 731 after a boundary fix (F5) | operability 9→9 (0); operability9→9 (0) | 9 | yes |
| freshness | 772 | freshness (actual 9 → 9 | 9 | yes |
| calibration | 771 | calibration 9 → 9 | 9 | yes |
| adjacency | 620 | adjacency 8→8 (0) | 8 | yes |
The operability line differs between the two versions of the rule, but both lines carry 9, so the value is unaffected. The rule also finds no false positive at b9046016: every line it matches is a real ordinal transition.

F5. Blind spots of the rule as written. [obs]
(a) The leading `\b` fails when the axis word is followed directly by a digit, because a letter and a digit are both word characters. This hides 15 glued lines: depth 481, 658, 678, 698, 716 and 730; operability 659, 679, 699, 717 and 731; calibration 680, 700, 718 and 732. Replacing `\b` with `(?<![A-Za-z])` and `(?![A-Za-z])` sees all of them. With that change the operability pick at b9046016 becomes 731 and no other pick changes.
(b) The character class `[^0-9|→\n]` excludes the pipe, so two-cell table rows are hidden. This hides 21 lines: depth 256, 324, 388, 424, 446, 492, 517, 537 and 572; operability 255, 519, 538 and 573; coverage 192; adjacency 191; freshness 193, 425, 447, 518, 539 and 574. Each of these lies before the picked line for its axis, so the base values do not change. A table row added after the pick would be invisible to the rule.
(c) The 0-to-10 range check is what rejects "coverage rows 10 → 15" on line 192. Without it that count would read as coverage 15.

F6. Regex traps. Each trap lists the wrong value a naive parser would produce. [obs]
- T1. `freshness (actual 9 → 9` (line 772). A pattern that needs digits right after the axis word misses this line and reads line 749, freshness 8. The rule's 12-character gap is what catches "(actual ".
- T2. `coverage rows 10 → 15` (line 192). A loose parser reads coverage 15. A last-arrow-on-line parser reads coverage 4, because the same line ends with "SKILL update-gate rows 0 → 4". The 0-to-10 check rejects 15.
- T3. `depth8→8` glued (lines 481, 658, 678, 698, 716 and 730). A pattern using `\bdepth\b` or `depth\s+` misses them. The depth pick (759) is unaffected.
- T4. `operability9→9` glued (lines 659, 679, 699, 717 and 731). Missed by the rule as written, so the pick becomes 621 instead of 731. The value is 9 either way.
- T5. `calibration9→9` glued (lines 680, 700, 718 and 732). Missed; the pick (771) is unaffected.
- T6. A count arrow after a tied-lowest parenthetical. Line 591 reads adjacency 114 ("inbound_classified 0 → 114"). Line 592 reads depth 12 ("attributed_events 0 → 12"). Line 638 reads depth 5 ("decision_rows0→5"). Line 593 reads calibration 0 ("missing 1 → 0"). None of these lines is a pick, but each defeats a loose parser.
- T7. Counts in the same cell as the axis. Line 620 read by its last arrow gives adjacency 1 (from "ownership_corrections 0→1"). Line 622 gives calibration 0 ("audit_live_map_errors 1→0"). Line 771 gives calibration 268 ("Not a successful 0→268"). Line 425 gives freshness 1 ("record0→1"). Line 256 gives depth 4 ("records 0 → 4"). Line 660 gives calibration 1 ("exit1→1").
- T8. Two axes on one line. Line 759 names depth and adjacency, and its only arrow belongs to depth. A loose parser reads adjacency 8 from it. The value happens to match the true adjacency, but the line is wrong.
- T9. Axis words inside tool or file names. Lines 593 and 622 contain `check-registry-coverage.py`, line 518 contains `check-freshness-r17.py`, and lines 591 and 620 contain `check-adjacency-anchors.py`. A line-level parser reads these as axis lines. Line 622 gives coverage 0 this way, and line 518 gives freshness 0 (from "exit 1 → 0").
- T10. Digits next to an arrow inside a commit hash. Line 447 contains "…20a2 → 6de977d…". A digit-only parser reads "2 → 6" and so reports freshness 6.
- T11. Chains of counts. Line 28 (freshness row) has "198→208→211→220→224", "247→251→260→339" and "drivers `other` class 2→65". Line 37 (operability row) has "3→4→5(uncommitted, ~12 min)→6". Line 49 (operability table row) has "17→26→35→49→74→80". A last-pair parser reads freshness 65, operability 5 and operability 80 from these lines.
- T12. Reverse order, with the count before the axis word. Line 197 "QUALITY criteria 5 → 13 are supporting work, not a claimed calibration move" reads calibration 13 under a reversed parser. Line 518 "exit 1 → 0 (python3 tools/check-freshness-r17.py)" reads freshness 0.
- T13. Paragraph scope. Line 242 "counts 9→14" contains no axis word, but it sits in the freshness paragraph at lines 240 to 242. A paragraph-level parser reads freshness 14.
- T14. Table identity. Lines 73 to 80 hold a second table whose first column names the six axes ("| depth | unchanged |" and so on) under the 2026-10-15 appendix. A parser that takes the last table with axis rows reads that table, which has no numeric score. Only the heading rule selects lines 45 to 52: the one heading that starts `## Axes — ` is line 39, and the table under it is lines 47 to 52.
- T15. Statement-only values. Line 68 "adjacency (7)" and the table cell at line 50 "freshness | 8" are not transitions. A parser that reads any axis-number statement reads adjacency 7 and freshness 8.
- T16. Long gaps and missing digits before the arrow. Line 563 "freshness completeness … give59→65" has more than 12 characters before the pair, so a loose parser reads freshness 65. Line 522 "freshness 53 … Recheck gate 5 flagged → 0" has no digit before its arrow, so a parser that checks only for "→ digit" reads freshness 0.
- T17. The rule's own text and examples. Line 795 contains the template `<axis> N → M`, which has no digits. Working-tree line 807 contains "`freshness (actual 9 → 9`" and "`coverage rows 10 → 15`" as examples. Once committed, the rule would read line 807 as a freshness transition (value 9), and the declared rows at working-tree lines 792 (calibration 9 → 9) and 793 (depth 8 → 8) as transitions too. The values coincide with the base values, but these picks are declarations rather than recorded moves. [inf]

F7. Outside closures agree with the six values. [obs]
The table lists all 14 closure entries for this lane. "Verdict" columns are the MANIFEST labels; "Ordinal statement" is the closure text, where one exists.
| round | MANIFEST index | admitted | depth | coverage | operability | freshness | calibration | adjacency | ordinal statement in the closure text |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 309 | true | unchanged | improved | unchanged | improved | unchanged | improved | "score 8→9" for freshness (round-1 spot-check, line 17) |
| 12 | 324 | false | harmed | unchanged | improved | unchanged | unchanged | unchanged | "An unchanged ordinal 8→8 is not itself a failure" (round-12 spot-check, line 137); "all six ordinal scores remain unchanged" (lines 36 to 37) |
| 13 | 331 | false | harmed | unchanged | unchanged | unchanged | unchanged | unchanged | "ordinal scores remain depth8/coverage9/operability9/freshness9/calibration9/adjacency8" (round-13 spot-check, lines 104 to 105) |
| 14 | 336 | true | improved | unchanged | unchanged | unchanged | unchanged | unchanged | "No ordinal score is re-certified" (round-14 spot-check, lines 5 to 8); "Ordinal8 unchanged" (line 211) |
| 15 | 344 | true | improved | unchanged | unchanged | improved | unchanged | unchanged | "Ordinal 8→8" and "Ordinal 9→9" (round-15 spot-check, lines 120 to 121) |
| 16 | 352 | true | improved | unchanged | unchanged | unchanged | unchanged | unchanged | "ordinal 8→8 unchanged by design" (round-16 spot-check, line 87) |
| 17 | 365 | true | improved | unchanged | improved | improved | unchanged | unchanged | "No ordinal changed (depth 8→8, freshness 9→9, operability 9→9)" (round-17 spot-check, line 88); calibration ruling at lines 128 to 139 |
| 18 | 371 | true | improved | unchanged | improved | improved | unchanged | unchanged | "Ordinal deltas are 0 on every axis" (round-18 spot-check, line 41) |
| 19 | 389 | true | improved | unchanged | unchanged | unchanged | improved | improved | "Ordinals stay unchanged" (round-19 spot-check, line 140) |
| 20 | 404 | true | unchanged | unchanged | improved | unchanged | improved | improved | MANIFEST only; the declared deltas are 0 at base lines 620 to 622 |
| 21 | 416 | false | improved | unchanged | improved | unchanged | unprovable | unchanged | MANIFEST only; declared deltas 0 at base lines 658 to 660 |
| 22 | 422 | true | improved | unchanged | improved | unchanged | improved | unchanged | MANIFEST only; declared deltas 0 at base lines 678 to 680 |
| 23 | 436 | false | improved | unchanged | unprovable | unchanged | improved | unchanged | "Not admitted; rejected-honest-stop" (round-23 spot-check, line 8); "C1 depth, score held8" (line 16) |
| 24 | 445 | false | unchanged | unchanged | unchanged | unchanged | unchanged | unchanged | "No axis was harmed" and "changes no ordinal" (round-24 spot-check, line 63) |
No closure re-certified a number. The round-14 closure says so at its line 8 ("No ordinal score is re-certified"). Every number a closure states matches the six values above. The only numeric move a closure states is freshness 8 to 9 (round-1 spot-check line 17). The coverage and adjacency moves from the same round are labelled "improved" there; their numbers appear in the SCORECARD post-review lines 213 and 224.

F8. The closure verdict labels are not ordinal moves. [obs]
Closures labelled depth "improved" in rounds 14 to 19, 21, 22 and 23, and labelled depth "harmed" in rounds 12 and 13, while the depth score stayed 8. Calibration, adjacency and operability were labelled "improved" in rounds 19 to 23 while the declared ordinal deltas stayed 0 (base lines 620 to 622, 658 to 660, 678 to 680 and 698 to 700). The lane has no count-to-ordinal scale (base line 366 says "no new count-to-score mapping"), so these labels cannot be converted into moves. One lesson shows the gap: the round-19 spot-check (line 131) justifies "calibration improved" by "C3 fixes the missing baseline library row 1→0", which is a count.

F9. Whether "harmed" must lower an ordinal cannot be checked from the lane. [unk]
The SCORECARD cites AXES.md for the six-axis vocabulary (line 3) and for the stagnation rule (line 173). It also cites LEARNING.md for trend verdicts (line 3). `git ls-tree --name-only b9046016 -- AXES.md LEARNING.md` printed nothing, so neither file is in the committed lane tree. The lane never lowered an ordinal after a harmed verdict.

F10. The training-round MANIFEST verdicts disagree with the SCORECARD move log. [obs]
The ten train entries (indices 97 to 133) list depth and calibration as improved in every round from 2 to 11. They list operability in every round, freshness in rounds 3 to 10, coverage in rounds 6 to 10 and adjacency in rounds 5 and 6. The move log (lines 25 to 37) has depth only in rounds 3 and 4 (lines 29 and 30), calibration only in round 10 (line 36), freshness in rounds 1, 3, 4 and 6 (lines 26, 28, 30 and 32), coverage in rounds 6, 7 and 9 (lines 32, 33 and 35), adjacency in round 5 (line 31), and operability in rounds 1, 2, 5, 7, 8, 9 and 11 (lines 25, 27, 31, 33, 34, 35 and 37). The "Last change" cells (lines 47 to 52) also conflict with the MANIFEST: depth says r4 where MANIFEST's last improved round is 11; freshness says r6 where MANIFEST says 10; coverage says r9 where MANIFEST says 10; adjacency says r5 where MANIFEST says 6; calibration says r10 where MANIFEST says 11. These verdicts are not numeric and lie outside K01 to K06, so they do not change the six values. They are still conflicting records.

F11. The C1 before-value cannot be measured at b9046016. [obs]
`git cat-file -e b9046016:tools/check-self-assessment.py` exits 128 with "path 'tools/check-self-assessment.py' does not exist in 'b9046016'". The round-25 declaration (working-tree line 792) gives the before-value as "the number the tool reports at b9046016 (hand count by the L1 predicts 12 of 23)". That number cannot be produced. The round-24 precedent was "tool absent at base, exit 2, no measured value (absence recorded as 0)". The same kind of absence record applies here.

F12. The working tree adds lines that the rule would read. [obs]
Applied to the working tree (813 lines), the rule picks: depth at 793 (8), coverage at 224 (9), operability at 621 (9), freshness at 807 (9, the refinement example), calibration at 792 (9) and adjacency at 620 (8). The values match. The picks at 792, 793 and 807 are declared or illustrative text, not recorded moves. Excluding the round's own declaration and refinement block from the rule's scope would remove this.

F13. Other checks. [obs]
`git status --porcelain` at the lane prints 4 entries. I inspected only SCORECARD.md. I made no write to the lane, ran no jj command, and changed no file in the lane tree.

## Recommendations for the L1 (not applied by me)

1. Replace the round-11 table values for coverage, freshness and adjacency with 9, 9 and 8, or move the table to a historical heading. Without this, K02, K04 and K06 fail at any revision that keeps the table.
2. If the rule is kept as written, change the leading `\b` to `(?<![A-Za-z])` and `(?![A-Za-z])` and add a table-cell reading. At b9046016 this changes only the operability line, from 621 to 731.
3. Record the C1 before-value as "tool absent at b9046016, git exit 128", not as a count.
4. Keep the round's own declaration and refinement block out of the rule's scope, or the rule will read its own declared rows once they are committed.

## Residual risk and verification gaps

- I did not run tools/check-self-assessment.py, because it is absent at b9046016, and I did not evaluate checks K07 to K23.
- The closures for rounds 20 to 22 exist only as MANIFEST labels. I did not read any text for them.
- The harm-to-ordinal rule is unverified ([unk], F9).
- My regex results are simulations. A different parser could differ on glued and two-cell forms (F5 and F6).
- The working tree may change again before the L1 commits. Every line number in this report refers to the committed base.

Scope: read=lane SCORECARD.md (committed bytes at b9046016 and the working tree), corpus/lessons/round-1, round-12 through round-19, round-23 and round-24 verifier spot-check files, the lane tree listing, and the tsukuroi entries of /home/vgpnk/Projects/shokunin/MANIFEST.json (read-only jq queries); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/RevOrdinals.md and /fast/scratch/hyaku/tsukuroi-r25/RevOrdinals/{SCORECARD.b9046016.md,SCORECARD.worktree-vs-b9046016.diff}; executed=git rev-parse --short b9046016; git log -1 --format='%h %ci %s' b9046016; git show b9046016:SCORECARD.md | wc -l (782); git diff --stat b9046016 -- SCORECARD.md corpus/lessons; git status --porcelain | wc -l (4); git diff b9046016 -- SCORECARD.md; git cat-file -e b9046016:tools/check-self-assessment.py (exit 128); git ls-tree --name-only b9046016 -- tools/ (26 entries) and -- AXES.md LEARNING.md (no output); python3 regex simulations over the committed copy and the working tree (results quoted in F1 to F12)
Model: anthropic/claude-haiku-5-5 (from the workstation context block of this session)
Installs: none
