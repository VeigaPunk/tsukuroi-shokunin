# C37Ledger723 — C3 falsification item 7/8: self-assessment mismatch repair

Claim attacked (pre-freeze C3, SCORECARD.md, commit b8ededd, 2026-10-25):
"The self-assessment checker reports zero mismatches (all 27 fixed checks match) at the
measured round-37 tip. Before: at base `564db0b614` `check-self-assessment.py --revision <base>`
reported checked 27, mismatches 5, FAIL, exit 1 (K07-K11). After: append-only correction of the
five current self-assessment count cells to the measured tip values, then the same command at the
measured round-37 branch-tip revision reports checked 27, mismatches 0, PASS, exit 0. The checker
bytes and fixed 27-check population are unchanged."

## Method (all read-only; no lane bytes mutated)
- Read `tools/check-self-assessment.py` (K01-K27 logic: evaluate() lines 434-886; K07-K11 count
  extraction, K16-K19 capability-row path grammar via backtick spans + PATH_CHARSET, K20-K27
  SHONEN boxes, K13/K17 census selftest).
- Ran the unchanged checker at five revisions (each run includes the census selftest):
  base `564db0b614`, `d06cedb`, `ee36f9e`, `5124bf3`, tip `0e5f70f`.
- Checker blob sha256 identical at base and tip: `ac28365ff10e8a8c91747bf6b08d3df1a5b3b5aa`
  (claim's "checker bytes unchanged" holds).
- Emulated the checker's table selection (find_section `^## Axes` / `^## Capabilities`;
  pick_table last table with header cell "Capability"/"Axis"; split_cells; backtick spans;
  stated_case_count patterns) against each revision's SCORECARD.md blob to attribute every
  mismatch and the cannot-evaluate state.

## Observed results (actual checker outputs)
| revision | outcome | detail |
|---|---|---|
| 564db0b614 (base) | 27/5 FAIL exit 1 | K07 55 vs 56 notes; K08 3009 vs 3110 SKILL newlines; K09 784 vs 839 pipe lines; K10 46 vs 49 lessons; K11 256 vs 269 README newlines. Confirms the claim's before-value exactly. |
| d06cedb (first repair: count cells corrected + first r37 axes/caps tables) | 27/2 FAIL exit 1 | K17: token `after.md` (bare backtick `after.md` in the host-census-gate row) names path absent at the revision; K18: tokens `selftest-after.json`, `mode-policy-mutant.json` absent. The claimed five-cell correction alone did NOT reach zero at this tip. |
| ee36f9e (pointer correction: capability row paths trimmed) | 27/1 FAIL exit 1 | K17: stated None cases; observed 105. The host-census-gate row lost the literal count phrase "PASS (105 cases, ...)" so stated_case_count returns None -> mismatch. |
| 5124bf3 (repair census capability measured case count) | CANNOT_EVALUATE | error "missing capability row", detail "sources-registry". The appended partial 1-row capability table became the table the picker selects (last `## Capabilities` section's last "Capability" table), so the operative view lost sources-registry / root-metadata-observer / boot-chain-audit rows. |
| 0e5f70f (tip: complete current capability table) | 27/0 PASS exit 0 | Final appended `## Capabilities - complete current table (round 37)` contains all four rows; host-census-gate states "prints PASS (105 cases, 105 passed, 0 failed)"; every cited path exists at the revision. |

## Falsification finding
The repair claim, as written ("append-only correction of the five count cells -> tip reports
zero"), is falsified by the intermediate repair states:
1. d06cedb (the five-cell correction itself) reported 2 mismatches (K17+K18) at its own tip;
2. ee36f9e fixed those but broke K17's case-count text (stated None vs observed 105);
3. 5124bf3's case-count fix made the checker unable to evaluate at all (missing capability row —
   the picker binds to the last table, which had become the partial 1-row host-census-gate table).
Zero mismatches appeared only at the fourth commit (0e5f70f) after a complete-table append.
So the predicate `mismatches == 0 && checked == 27 && exit == 0` is revision-fragile: each of the
first three repair commits violated it (2 mismatches, then 1, then cannot-evaluate), and only the
final 4-commit series satisfies it.

## Concrete stale checks at the declaration base
- K07-K11 (the five count cells) are stale at base 564db0b614 as the claim itself documents
  (observed: 55/3009/784/46/256 stated vs 56/3110/839/49/269 measured).
- The repair itself introduces further stale/faulty self-assessment states: K17/K18 path tokens at
  d06cedb (bare relative tokens `after.md`, `selftest-after.json`, `mode-policy-mutant.json`), K17
  missing count text at ee36f9e, and the cannot-evaluate table-selection flaw at 5124bf3.

## Correction proposal that makes the unchanged checker report zero (grounded in observed tip 0e5f70f)
- Operative axes table (the last `## Axes` section) must carry the literal count phrases: depth
  "56 notes ... `SKILL.md` 3110 `wc -l` / 839 table lines ... `corpus/lessons/` 49 files";
  coverage "`corpus/README.md` 269 `wc -l`" (verified equal to the observations).
- The operative `## Capabilities` section must contain ONE table with ALL FOUR rows
  (sources-registry, host-census-gate, root-metadata-observer, boot-chain-audit); the
  host-census-gate row must include the literal sentence "prints PASS (105 cases, 105 passed, 0
  failed)"; every cited path must be individually backticked with its full repository path and be
  present at the measured revision; bare relative tokens (after.md, selftest-after.json,
  mode-policy-mutant.json) must not appear outside full-path context.
- Do not append partial capability tables after the operative table: the checker selects the LAST
  "Capability"-headed table in the LAST `## Capabilities` section, so a partial trailing table
  drops rows (observed cannot-evaluate at 5124bf3).
Expected: `checked 27, mismatches 0, PASS, exit 0` at the tip (exactly the observed 0e5f70f state).

## Evidence / citations (all opened this round)
- tools/check-self-assessment.py: evaluate() lines 434-886 (K07-K11, K13/K17, K16-K23), main()
  lines 1084-1100.
- SCORECARD.md blob @ 564db0b614:1564-1575 (r35 axes table, the stale declaration).
- SCORECARD.md blob @ d06cedb:1992-2011 (first r37 caps: host-census-gate `after.md`, root-metadata
  `selftest-after.json`/`mode-policy-mutant.json`).
- SCORECARD.md blob @ ee36f9e:2013-2022 (host-census-gate row without count sentence).
- SCORECARD.md blob @ 5124bf3:2012-2030 (partial appended table -> cannot-evaluate).
- SCORECARD.md blob @ 0e5f70f:1988-2041 (operative axes rows 2006-2011; complete capability table
  2035-2041).
- Lane receipts .ufo/waves/round-37/after-c3-d06ced.json, after-c3-ee36f9.json,
  after-c3-5124bf.json, after-c3-0e5f70.json (observed lane runs; 5124bf3 = CANNOT_EVALUATE).
- git log/diff (read-only) for the r37 commit series: b8ededd (C3 correction),
  d06cedb -> ee36f9e -> 5124bf3 -> 0e5f70f.
No web sources used; no tools installed (read-only git + python3; no pacman).

## Restoration evidence
No tracked lane file was modified by this seat; all checker runs read git blobs only. The sole
worktree entries at probe time were pre-existing untracked `.ufo/waves/round-37/*` files
(verified via `git status --porcelain`). Nothing to restore.
