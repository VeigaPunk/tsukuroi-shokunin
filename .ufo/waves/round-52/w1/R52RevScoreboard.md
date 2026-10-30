VERDICT: defect-found

# W-D3 — eight-counter scoreboard spot check

Axes: calibration (distinguish scored PASS from equivalence-only evidence); considerthese (arm/PASS ledger fidelity); provenance (frozen report bytes, not mutable working tree).

## Scope and method

All evidence below was opened with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:<path>`. Paths below are relative to that lane and identify blobs at that exact revision. The table under review is `.ufo/waves/round-51/w1/R51ScoutConsider.md`, section “Scoreboard”. Eight counter rows, covering sixteen numeric cells, were checked against the cited seat reports themselves. No counter was rerun.

`read xd://lsp` returned `No such tool: xd://lsp`; semantic-device checks are unavailable. These are Markdown evidence checks, not semantic caller proofs. Frozen `git ls-tree -r --name-only <freeze> corpus/lessons` lists lessons through round 51, not round 52: this review checks the frozen source scoreboard, not an unobserved landed round-52 lesson.

## Findings, by severity

### Medium — r45 conflates equivalence tests with full-counter scoring

The `score-census-readers-r45.py` PASS cell says `0. "All 30 mutants were killed"`, but its cited report, `.ufo/waves/round-45/a2w1/C1MutSites.md`, explicitly qualifies that statement with “except the noted equivalent cases.” Its equivalence table has six equivalent variants: (b) S1/S4/S5 and (c) S1/S4/S5, each `0/0/0/0`. The remaining 24 have mismatches. The report's “Full counter runs” section records only (a) S1 and (f) S3, both FAIL; it explicitly says “No full-counter run was made for the other mutants.” Thus zero *observed* full-counter PASS is supported, not zero across thirty full-counter trials or thirty killed mutants.

Exact replacement PASS cell:

`0 observed in 2 full-counter runs ((a) S1 and (f) S3, both FAIL); the other 28 were not full-counter scored. Equivalence-only tests: 24 mismatching mutants and 6 equivalent variants, not 30 kills (a2w1/C1MutSites.md, Equivalence results / Full counter runs).`

Exact replacement arms cell:

`30 single-site mutation variants tested for equivalence; only 2 received full-counter scoring (a2w1/C1MutSites.md, Mutation scope / Full counter runs).`

### Low — r44 arms denominator includes an explicitly faithful implementation

The `score-scrub-arm-r44.py` row lists 10 arms, but `.ufo/waves/round-44/w1/C1CritEvasion.md`, Battery table, identifies V7 as `none (36-line faithful rewrite, no comments)`. The scoreboard itself excludes V7 from its five cheating PASSes. Under its own definition, an arm attempts to pass without the claimed work; V7 does the work. The ten-entry battery contains nine cheating candidates and one faithful comparator.

Exact replacement arms cell:

`9 cheating candidates (V1–V6, V8–V10), plus faithful comparator V7; 10 total scored variants (w1/C1CritEvasion.md, Battery).`

The five-cheat PASS cell is sourced and needs no numerical correction.

### Low — r43 counts the declared-limit reproduction as a new arm/beat

The `check-scrub-record-r43.py` row counts seven fixtures and six PASSes, including Z-k3. Its own scoreboard preamble excludes declared expect-PASS controls unless a seat built a further member. `.ufo/waves/round-43/w1/C2CritControl.md`, “Cheap forgeries beyond K3”, calls Z-k3 `none (control K3 reproduction)` and `harness parity`. The remaining six are further mutations; five pass and E-dupdispatch fails. Seven/six is a sourced raw fixture tally, but is miscounted as new-arm/new-beat totals under the scoreboard's stated convention.

Exact replacement arms cell:

`6 further mutation fixtures, plus Z-k3 declared-limit reproduction for harness parity; 7 total scored fixtures (w1/C2CritControl.md, Cheap forgeries beyond K3).`

Exact replacement PASS cell:

`5 further PASSes: A-inv-SR1, A-inv-all, B-scripted, C-smuggle, D-residual. Z-k3 also PASSes as the declared-limit reproduction, excluded from new beats; E-dupdispatch FAILs.`

## Cell-by-cell checks

Each source was opened by the frozen `git show` command specified above. The located sections and short verbatim excerpts below are evidence from those command outputs, not new runtime claims.

| Counter / round | Arms fielded cell | Reached frozen PASS cell | Source evidence |
|---|---|---|---|
| `check-transaction-order-r39.py` / 39 | **sourced**: 11 (V1–V10 plus V4b) | **sourced**: 8, V1/V2/V3/V4/V6/V7/V8/V10 | `.ufo/waves/round-39/w1/C2CritControl.md`, opening “Eight of eleven entries”; variant table enumerates all 11, with V4b/V5/V9 FAIL. The opening's subsequent “Two variants fail” is internally wrong; the table has three and supports 8/11. |
| `score-selftest-literals-r40.py` / 40 | **sourced**: 4 | **sourced**: 3 | `.ufo/waves/round-40/w1/C1CritControl.md`, “The family, scored”: A/B/C PASS, negative v3 FAIL. C's first attempt failed a neutral; its rerun PASS is explicitly disclosed. |
| `check-scrub-record-r43.py` / 43 | **miscounted under arm convention**: 7 raw fixtures, 6 further mutations | **miscounted under beat convention**: 6 raw PASS, 5 further PASS | `.ufo/waves/round-43/w1/C2CritControl.md`, “Cheap forgeries beyond K3”: Z-k3 is “control K3 reproduction”; A-inv-SR1/A-inv-all/B-scripted/C-smuggle/D-residual PASS; E-dupdispatch FAIL. Corrections above. |
| `score-scrub-arm-r44.py` / 44 | **miscounted as arms**: 10 raw variants, 9 cheating candidates | **sourced**: 5 cheating PASS, V1–V5 | `.ufo/waves/round-44/w1/C1CritEvasion.md`, Battery: V7 is “faithful rewrite”; V1–V5 PASS, V6/V8/V9/V10 FAIL. Correction above. |
| `score-census-readers-r45.py` / 45 | **sourced as mutation count, not 30 scored arms**: 30 equivalence variants, 2 full-counter runs | **unsourced as blanket full-counter result**; 0 observed of 2 is sourced | `.ufo/waves/round-45/a2w1/C1MutSites.md`, equivalence table and “Full counter runs”; “No full-counter run was made for the other mutants.” Corrections above. |
| `check-scrub-admission-r46.py` / 46 | **sourced**: 2 | **sourced**: 2 | `.ufo/waves/round-46/w1/C2CritControls.md`, “Missing controls scored”: “Both scored **PASS**, exit 0”; following bullets identify K22 nonexistent citation and K23 identical reports. |
| `check-fd-band-r49.py` / 49 | **sourced**: 3 | **sourced**: 2 | `.ufo/waves/round-49/w1/R49CritFdB.md`, Results table: A PASS, B PASS, C FAIL on band_ok. Opening: “Two of the three cheats PASS the counter.” |
| `check-selftest-matcher-r50.py` / 50 | **sourced**: 6, a/a2/b/c/d/e (real baseline excluded) | **sourced**: 2 distinct variants, c and e | `.ufo/waves/round-50/w1/R50CritCheatC2.md`, “Fixtures and results”: a/a2/b/d FAIL, c/e PASS. c passed runs 1 and 2; e was only runs 1. These are report-observed invocations, not proof that e passed the counted runs-2 invocation. |

## Residual risk / verification gaps

- These are eight source-scoreboard row checks, not verification of all rounds 38–50 or of the final lesson integration.
- Report-observed PASS is not independent runtime reproduction. No battery, selftest, scorer, fixture, or alternate runtime was invoked.
- r50 e is explicitly only a runs-1 observation; preserve that qualification if the lesson equates “Reached frozen PASS” with the counted runs-2 predicate.
- No scratch directory was created, so no cleanup was necessary. No tool installed or updated; no tracked file edited, no index or fixture mutation.

Self-evaluation: accuracy 4/5 (report evidence only, not receipt reproduction); completeness 4/5 (16 cells checked, final lesson absent at freeze); clarity 4/5 (raw fixture and arm counts necessarily distinguished); actionability 5/5 (exact replacement cells supplied); conciseness 4/5 (evidence table repeats corrections for auditability). Overall 4.2/5. Highest-impact improvement is to preserve the explicit full-counter/equivalence and comparator distinctions when the L1 lands the lesson. This assessment is scoped to the requested source verification.
