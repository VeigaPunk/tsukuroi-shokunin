# Round 25, wave 1 — draft of the `## Mistakes` table and QUALITY criterion 57

Seat: `TsukuroiR25.DraftLessonMistakes` (scribe). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Claim base `b9046016831237cd04d38da11ba76e50d5380c53`. Date 2026-10-22.

Verdict: the primary candidate is confirmed as a real, measurable defect — the only axes table in `SCORECARD.md` was never refreshed after round 11 and contradicts the repository at the round-25 base on every row — and the `## Mistakes` table plus QUALITY criterion 57 are drafted and ready for the L1 to integrate.

## Deliverables (drafts, for the L1)

| Draft | Path |
|---|---|
| `## Mistakes` section for `corpus/lessons/round-25.md` (two rows) | `.ufo/waves/round-25/w1/DraftLessonMistakes/mistakes-table-r25.md` |
| QUALITY criterion 57 (with optional clarification and notes) | `.ufo/waves/round-25/w1/DraftLessonMistakes/quality-57.md` |
| Red-before receipt A: the table's own counting commands re-run at the base (tool-independent) | `.ufo/waves/round-25/w1/DraftLessonMistakes/red-before.txt` |
| Red-before receipt B: the checker's own failure output at the base (re-verified by this seat) | `.ufo/waves/round-25/w1/DraftLessonMistakes/checker-red-before-b9046016.json` |

No production lane file was edited. `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/`, `SKILL.md`, `SHONEN.md` and `tools/` are untouched by this seat.

## Findings

1. **[obs] The axes table at `SCORECARD.md:45-52` is the only axes table and it is a round-11 artifact.** The heading `## Axes — final self-assessment (landed round 11; …)` is at `SCORECARD.md:39`; the table header is at `SCORECARD.md:45` and its six rows at `SCORECARD.md:47-52`. No later axes table exists in the file. The round-25 declaration names the same table by rule, not by line: "The current axes table is the last table under the last heading that starts `## Axes — ` in SCORECARD.md at `<REV>`" (`SCORECARD.md:795`).

2. **[obs] The table contradicts the repository at the claim base on every row it states.** Re-running the table's own counting commands at `b9046016` (full command, output and exit code in `.ufo/waves/round-25/w1/DraftLessonMistakes/red-before.txt`):

   | Table claim (`SCORECARD.md:47-52`) | Observed at `b9046016` |
   |---|---|
   | depth: 24 notes | 46 (`git ls-tree -r --name-only b9046016 corpus/knowledge/ \| grep -c '\.md$'`) |
   | depth: `corpus/lessons/` never written (0 files) | 25 files |
   | depth: `SKILL.md` 1631 `wc -l` | 2301 |
   | depth: 55 table lines | 259 |
   | depth: census 2402 `wc -l` | 2679 |
   | depth + operability: 80 executed cases | 97 (`PASS (97 cases, 97 passed, 0 failed)`, exit 0) |
   | coverage: `corpus/README.md` 20 `wc -l` | 231 |
   | calibration: `calibration-synthesis.md` 463 `wc -l` | 470 |
   | freshness score 8, adjacency score 7, coverage score 8 | freshness 9, adjacency 8, coverage 9 (`SCORECARD.md:275`, `SCORECARD.md:481`) |

   The census selftest that produced "97 cases" ran against a script byte-identical to the base (`git rev-parse b9046016:tools/tsukuroi-census.sh HEAD:tools/tsukuroi-census.sh` both print blob `4610af7b3450ee3d3158590fb7a3300d0a86bee0`), and the worktree was not mutated by it (`git status --porcelain` showed the same 4 untracked wave paths before and after).

3. **[obs] A file anchor inside the stale table also drifted.** The coverage row points at the six `PLANE` emitters as `tools/tsukuroi-census.sh:2377-2382` and the rollup keys at `:2392`; at the base those lines hold selftest fixture code, and the six emitters now sit at `tools/tsukuroi-census.sh:2654-2659`. This is a symptom of the same stale table, not a second mistake, and the draft row states it inside the evidence pointer.

4. **[obs] Round 24 read that table and booked C2 on it.** The round-24 declaration row reads "C2 pause-lift update-safety gate entry … | freshness 8 → 8 (tied lowest) |" (`SCORECARD.md:749`); the round-24 lane later corrected itself at `SCORECARD.md:759` ("Freshness was 9 at the base, not 8; the tied-lowest axes are depth and adjacency at 8"). The round-25 declaration reads the ordinals from the move records instead: "Ordinals at the base, read from the latest move records rather than from the stale round-11 axes table: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8" (`SCORECARD.md:786`). The round-24 lesson already carries the premise error as `R24-STALE-PREMISE` (`corpus/lessons/round-24.md:45`), and the round-24 spot-check routed it as defect 1 (`corpus/lessons/round-24-verifier-spotcheck.md:98`).

5. **[obs] The second half of routed defect 1 is a separate, distinct error: the round-24 calibration claim measured the wrong quantity.** "C1 also fails claim sizing: a calibration claim has to count mismatches between SCORECARD/SHONEN and the repo, and C1 counts attribution instead." (`corpus/lessons/round-24-verifier-spotcheck.md:42`). The instrument confirms it: `tools/report-red-causes.py` emits `attributed_findings`, `reclassify_mismatches` and `pin_mismatches` (`tools/report-red-causes.py:180-182`) and has no field that compares the self-assessment with observed repository state. The draft therefore carries two rows, `R25-STALE-AXES-TABLE` (class `stale-premise`) and `R25-CALIBRATION-METRIC-OFF-AXIS` (class `scope`), both from the same routed defect; the L1 may keep only the first.

6. **[obs] `tools/check-self-assessment.py` is absent from the lane at both revisions this round names, so the L1 must integrate it.** `git ls-tree b9046016 tools/` lists no `check-self-assessment.py`, and the same is true at the declaration commit `6c580b15`; the file exists only in the executor's clone until the L1 lands it. That is why the criterion's before-state is cited with the clone path and the receipt digest, and why the draft keeps a second, tool-independent witness: the table's own counting commands contradict it, and that receipt is committed.

7. **[obs] The instrument-level red-before has landed and I re-verified it.** The executor seat `TsukuroiR25.ExecSelfAssessTool` built `tools/check-self-assessment.py` in its own clone and ran it against the lane at the base. I re-ran the same command myself and got the same result: exit code 1, one JSON object with `"status": "FAIL", "mismatches": 12, "checked": 23, "revision": "b9046016831237cd04d38da11ba76e50d5380c53"`, and the mismatching checks K02, K04, K06, K07, K08, K09, K10, K11, K12, K13, K15 and K17. Command: `python3 tools/check-self-assessment.py --revision b9046016 --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, run from `/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo`; my saved output `.ufo/waves/round-25/w1/DraftLessonMistakes/checker-red-before-b9046016.json` has sha256 `2e9cfb4540f82e83c86501338462794451594983dd4602434734c906411698f6`, byte-identical to the executor's receipt `.ufo/waves/round-25/w1/ExecSelfAssessTool/c1-base-b9046016.json`. The lane was not mutated by the run (`git status --porcelain` unchanged: the same four untracked wave paths). The machine count of 12 equals the declaration's hand count of 12 (`SCORECARD.md:792`).

8. **[obs] The checker's per-check reasons add two staleness facts beyond the axes table.** K12: the coverage row says the `PROVINCE.md` Core/Frontier/Adjacent sections are not landed, and the checker finds all three headings present at the base. K15: the adjacency row says there is no formal overlap table, and the checker finds a table at `PROVINCE.md:44` whose header row reads `ID` and `Finding`. K17 repeats the stale 80-case count in the capabilities table. The lesson row now states these in its evidence pointer, so the fix's scope is the whole self-assessment surface and not only the axes table.

9. **[obs] `Captured-by` is `none` for both rows, as the assignment states.** No criterion and no tool covered the lane's own self-assessment at declaration time. QUALITY 55 (round-24) covers stale host-state premises, not the lane's self-assessment, so it does not capture this defect; criterion 57 is the new coverage.

10. **[obs] A separate, unmined label drift exists and is left to the L1.** QUALITY 54's heading ID is `R24-SUMMARY-RECALL` while the lesson row is `R24-KEY-RECOLLECTION`, and QUALITY 55's heading ID is `R24-PREMISE-STALE` while the lesson row is `R24-STALE-PREMISE` (`corpus/QUALITY.md:107-108` against `corpus/lessons/round-24.md:45`). That is routed defect 6 and belongs to the L1's append; I did not draft it as a round-25 mistake row because its fix is not landed.

## Class vocabulary check

Classes used are taken from the `CORPUS.md` mistakes vocabulary (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`): `stale-premise` for the never-refreshed self-assessment and `scope` for a claim that measured a quantity outside its axis metric. The number drift inside the table and the drifted file anchor are stated inside the primary row's evidence pointer rather than being split into extra rows, so the table carries no padding.

## Out of scope for this seat

- Writing `corpus/lessons/round-25.md`, `corpus/QUALITY.md` or any other production file (L1 integrates).
- Building `tools/check-self-assessment.py` (executor seat `TsukuroiR25.ExecSelfAssessTool`).
- The C2 memory-pressure entry and its rows MP1 to MP6 (other wave-1 seats).
- Any host write, package transaction, service action or configuration change (none performed).

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin SCORECARD.md, corpus/QUALITY.md, corpus/lessons/round-24.md, corpus/lessons/round-24-verifier-spotcheck.md, tools/report-red-causes.py, tools/tsukuroi-census.sh, corpus/knowledge/calibration-synthesis.md, SHONEN.md; /home/vgpnk/Projects/shokunin/CORPUS.md; /fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py (read-only, executor seat's clone); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/DraftLessonMistakes.md, .ufo/waves/round-25/w1/DraftLessonMistakes/mistakes-table-r25.md, .ufo/waves/round-25/w1/DraftLessonMistakes/quality-57.md, .ufo/waves/round-25/w1/DraftLessonMistakes/red-before.txt, .ufo/waves/round-25/w1/DraftLessonMistakes/checker-red-before-b9046016.json; executed=git ls-tree/git show/git rev-parse/git status/git diff --stat (read-only) at base b9046016, grep/awk/sed over SCORECARD.md, corpus/QUALITY.md, corpus/lessons/round-24.md and corpus/lessons/round-24-verifier-spotcheck.md, ls/wc over corpus and SKILL.md, bash tools/tsukuroi-census.sh --selftest (exit 0, no worktree mutation), python3 tools/check-self-assessment.py --revision b9046016 --repo <lane> (exit 1, from the executor seat's clone, read-only against the lane)
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
