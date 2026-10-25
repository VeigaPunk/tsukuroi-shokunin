# C36Ledger622 — C3 falsification item 6/8: self-assessment mismatch repair (K17)

## Scope and verdict

Axis: **C3 calibration**; attack target: the round-37 self-assessment mismatch repair claim ("existing self-assessment mismatch repair; 27 fixed checks"). Tooling rule read first: `/home/vgpnk/.omp/agent/RULES.md` lines 1–9. No tools installed or updated; no pacman; no lane Git/jj writes; no campaign tools; no delegation. All checker runs read the lane through Git blobs and run the census selftest on `git archive` in temp dirs (hermetic; the working tree is never read — checker docstring lines 2–13).

**Verdict: the repair claim is falsified at four of the five audited revisions of its own lineage.** The unchanged checker reports zero mismatches only at the final repair tip `0e5f70f` (observed 0/27, exit 0). At the wave's declaration base `564db0b` five checks mismatch permanently (exit 1; immutable history), and each intermediate repair revision was itself defective: `d06cedb` 2 mismatches (K17, K18 — introduced by the repair commit), `ee36f9e` 1 mismatch (K17), `5124bf3` exit 2 CANNOT_EVALUATE (the repair broke evaluability). "Repair ⇒ zero mismatches" was never true until the last of five commits, and the passing state rests on positional last-table selection, not on the file being consistent.

## Concrete fixed check: K17 (with the K16 shared-table prerequisite)

Check K17 — "host-census-gate row names only repository paths that exist at the revision" and states a census case count equal to the selftest (checker `tools/check-self-assessment.py` lines 687–725; count forms at lines 561–574; path grammar at lines 63–67: a backticked token ending `.md`/`.json` is resolved as a repository path **from the token itself**, so a bare basename must exist at the repo root).

**Stale self-assessment value at the capability declaration base.** In `d06cedb` ("round-37: self-assessment counts corrected to measured tree"), the new `## Capabilities — current (round 37)` table (SCORECARD.md:1989–1998) states, in the host-census-gate evidence cell (line 1996): "historical receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `after.md`". The bare `` `after.md` `` resolves to repo-root path `after.md`, which is absent at the revision — the similarly named file exists only as `.ufo/evidence/round-1-kaika/after.md` (verified present at `d06cedb` and at HEAD via `git cat-file -e`; the bare root path is not in the tree). The unchanged checker reported (observed, exit 1, saved receipt `csa-d06cedb.json`):

- K17: "host-census-gate row names 1 path(s) absent at the revision: after.md"
- K18 (same defect class, SCORECARD.md:1997): bare `selftest-after.json`, `mode-policy-mutant.json` — both exist only as `.ufo/waves/round-12/resumed/<name>`; K18: "names 2 path(s) absent at the revision: mode-policy-mutant.json, selftest-after.json"

Note the precision: the full paths exist; the declared shorthand does not resolve. The repair commit's own transcription created both mismatches — at the pre-repair base `564db0b` K16–K19 all matched (before receipt).

At `ee36f9e` the repair removed the shorthand tokens but also removed every case-count phrase from the operative row (SCORECARD.md:2020), so K17 mismatched in a second form: "host-census-gate row states None cases; the census selftest at this revision prints 105 cases" (observed, exit 1, `csa-ee36f9e.json`). At `5124bf3` the fix appended a one-row correction table under a `###` heading inside the same `## Capabilities` section; `pick_table` (line 259) audits only the **last** table under the last `## Capabilities` heading (lines 476–489), that table lacked `sources-registry`, and the checker exited 2: `CannotEvaluate: missing capability row: sources-registry` (line 489) — observed, `csa-5124bf3.json`. Exit 2 is not "zero mismatches"; the check set cannot be evaluated at all.

**Declaration base `564db0b` (wave before-control).** The wave's own receipt `.ufo/waves/round-37/before/c3-before.json` records revision `564db0b`, declaring_round 35, 5/27 mismatches, exit 1. My rerun matches (`csa-564db0b.json`): the round-35 axes rows (SCORECARD.md at `564db0b`:1570–1571) state 55 notes / `SKILL.md` 3009 / 784 table lines / 46 lessons / `corpus/README.md` 256, while the tree holds 56 / 3110 / 839 / 49 / 269 — stale K07–K11, exactly the round-36 delta that no r36 axes refresh absorbed. These five are permanently mismatched at that base; no append-only repair can zero the checker *at the declaration base* — it can only re-declare at a new tip. The repair's own axes text concedes the phrase-form sensitivity ("the self-assessment parser requires the literal count phrases shown here", `d06cedb` SCORECARD).

## Correction proposal (not implemented)

One append-only commit to SCORECARD.md that appends a **single new `## Capabilities …` section whose last table retains all four capability rows** (sources-registry included), where the host-census-gate row:

1. cites only full repository paths that exist at the revision — `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` (or the full `.ufo/evidence/round-1-kaika/after.md` if the historical snapshot is to be cited — never a bare basename);
2. states the measured count in an accepted phrase form — "…hermetic selftest prints PASS (105 cases, 105 passed, 0 failed)…" (matches `PASS \((\d+)\s+cases`, line 562).

Applied once, this yields 0/27: demonstrated against the unchanged checker by fixture V4 (`fixture-results.json`, exit 0, zero mismatches). The same fixture set reproduces every observed defect with the unchanged checker: V1 = K17+K18 basename mismatches (`d06cedb` form), V2 = K17 None-cases mismatch (`ee36f9e` form), V3 = exit 2 `missing capability row: sources-registry` (`5124bf3` form). Fixtures are fresh `mktemp` repos built via `git -C` with top level verified equal to the fixture root before any commit; module base fixture `fixture_files("clean")`, census selftest printing 3 cases.

Residual exposure even after a correct repair: the PASS depends on positional table selection; superseded capability tables remain in the file (round-11/12-era rows at SCORECARD.md:157–163 at `d06cedb`, brace shorthand `{after,selftest-after,mode-policy-mutant}.json`), checker-invisible until some future edit makes their table last; and K07–K11 restale with any content change, so every subsequent content round re-runs the same mismatch cycle unless counts are re-measured at the new tip.

## Gates, touched surfaces, limits

- Observed runs: checker at `564db0b` (exit 1, K07–K11), `d06cedb` (exit 1, K17+K18), `ee36f9e` (exit 1, K17), `5124bf3` (exit 2 CANNOT_EVALUATE), `0e5f70f` (exit 0, 0/27); fixture driver 4/4 expected outcomes, selftest PASS.
- Not executed: the proposed correction on the lane (forbidden — do not implement); checker selftest suite; K01–K06 ordinal-reference audit beyond observed behavior.
- Touched surface: this report and the seat directory `C36Ledger622/` only. No tracked lane file, Git/jj state, fleet repo, sibling lane, or `shokuknow` touched. Fixture Git writes only in `/tmp/c36ledger622-fixtures-*`.
- Tool install/update: none. Cited sources: all local files, opened this round; no external URLs.

## Artifact paths

- `.ufo/waves/round-37/w1/C36Ledger622.md` — this report.
- `.ufo/waves/round-37/w1/C36Ledger622/csa-564db0b.json`, `csa-d06cedb.json`, `csa-ee36f9e.json`, `csa-5124bf3.json`, `csa-0e5f70f.json` (+ `.err`) — my observed checker receipts, one per lineage revision.
- `.ufo/waves/round-37/w1/C36Ledger622/fixture-driver.py`, `fixture-results.json` — hermetic reproduction of K17/K18/K16-defect states and the zeroing correction, unchanged checker.
- Corroborating lane receipts read: `.ufo/waves/round-37/before/c3-before.json`, `before/c3-before-exit.txt`, `after-c3-d06ced.json`, `after-c3-ee36f9.json`, `after-c3-5124bf.json`, `after-c3-0e5f70.json`.

Report: .ufo/waves/round-37/w1/C36Ledger622.md
