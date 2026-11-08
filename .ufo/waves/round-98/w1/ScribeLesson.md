# ScribeLesson — round 98, wave w1 — scoped findings

Seat: `ScribeLesson` (scribe). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Files written (this seat only): `.ufo/waves/round-98/w1/ScribeLesson/round-98.md` (the lesson
draft), `.ufo/waves/round-98/w1/ScribeLesson/round-98.review.md` (the review of the L1's own
`corpus/lessons/round-98.md`), `.ufo/waves/round-98/w1/ScribeLesson/report.md` (commands, raw
output, PASS/FAIL, receipts) and `.ufo/waves/round-98/w1/ScribeLesson/receipts/` (41 receipts).
Scratch `/fast/scratch/hyaku/tsukuroi-r98/ScribeLesson` deleted before yield. No mutating git or
jj command; the only commits were in my scratch clone, each preceded by a `--show-toplevel`
assertion. No tool installed; no pacman, no `sudo`.

## What this seat measured (every number run by this seat)

| leg | expected | measured | verdict |
|---|---|---|---|
| C1 landed gate, r98 battery, 3 runs | `105/105` met ×3, `failed_families []`, 0 error rows | met 105/105 ×3, cases 420/run, 0 error rows | PASS |
| C1 N07 bend, 3 runs | `103/105` unmet ×3, failed exactly `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows | as stated | PASS |
| C1 N08 bend, 3 runs | `104/105` unmet ×3, failed exactly `[LEADING-ZERO-NORMALIZE]`, 0 error rows | as stated | PASS |
| C1 blindness, r97 do-nothing battery on the landed gate and both bends | `met 105/105` ×3, 0 error rows on each | as stated; the control is byte-identical to the r97 landed battery (`e678c34f…`) | PASS |
| C2 `--selftest` (r98 / r97) | `PASS 14/14` / `PASS 12/12` | as stated | PASS |
| C2 M08 on the r98 checker (red-after) | `FAIL 12/14`, both gap cases red | `span-gap FAIL ['RC-VALUE-MISMATCH']`, `span-gap-lie FAIL []` | PASS |
| C2 M08 on the r97 checker (red-before) | `PASS 12/12` | `PASS 12/12` | PASS |
| C2 D1 / D2 / D2lie | r98 FAIL one `RC-VALUE-MISMATCH` / r98 PASS / r98 FAIL one; r97 `RC-CELL-MISSING` on D1 | as stated; M08 inverts on D2/D2lie | PASS |
| C2 coverage blindness | `PASS 157/157`, 0 findings, on each doctored revision | ×3 | PASS |
| Gate S392 re-open | byte-identical; offsets 157767 / 153202 / 159315 | byte-identical to the r97 pin (`d92580dd…`, 331 022 bytes); all three offsets re-measure | PASS |
| Gate S393/S394 offsets | 11230 / 11344 / 4425 and 16931 / 17037 / 4425 | re-measured with `grep -abo`, with line numbers 200 / 202 / 47 and 316 / 318 / 47 | PASS |
| Gate rejected candidate | a reason grounded in the bytes | limine `CONFIG.md` v12.9.6: 200 / 27 609 / `f44f3a19…`; zero occurrences of `limine_version`, `visibility_era`, `echo`, `version`, `JSON` | PASS |
| Census | exit 0, 0 E findings | exit 0, 0 E, 57 W04 + 1 W01; rows 392 (`b3be3f90`) → 393 (freeze `1cfeb5d5`) → **394 (working tree, S394 added after the freeze)** | PASS with a stated deviation |

## Findings for the L1

1. **The L1's draft needs seven citation/number fixes** — the census row count (393 → 394 after
   S394), the "only in-place change" claim (two fields changed on S393), the M08 red-before
   pointer (it cites the pristine r97 selftest, not the M08-on-r97 receipt), the N08 green-after
   pointer (`before/dev/c1-bend-N08-runs3.json` does not exist; the frozen `…-runs3.txt` is 0
   bytes), the Routed rows for R97-D1/R97-D2 (they cite a not-yet-existing report and a
   revision-free summary), and the rejected candidate's missing bytes/sha256/token counts. Detail
   with each command in `round-98.review.md` § (a).
2. **The L1's draft has seven missing Gate/mistake fields** — most importantly no
   `## Counter-attack scoreboard` (QUALITY 115 requires one for a frozen counter, and two arms
   survive), no `## Frontier moved this round`, no PROPOSED criterion text for the field-coverage
   class that R97-D3/A6 asks for, and no mention of the two surviving arms (ReviewBattery g6, the
   Y-cap field lie; MutRegistry B01/B02/B03). Detail in `round-98.review.md` § (b).
3. **The counter-attack scoreboard rows are sourceable now** — one table covering all 14 seats,
   with the four seats that had not written a `report.md` at review time named as such
   (`ExecBends`, `ExecGateRuns`, `ScoutDrift`, `ScribeKnowledge`, `CriticClaims` — receipts only)
   and their receipts used. `round-98.review.md` § (c) and `round-98.md`.
4. **Settle item**: `tools/check-registry-coverage.py` reads `FAIL` at the tip (3 ×
   `REGISTRY-ROW-MISSING` for the three r98 tools; `tools_total 160` vs `registered 157`) and
   `PASS 157/157` at the pre-round base `b3be3f90` — the rows exist uncommitted at
   `SKILL.md:5944-5946`, so the finding clears on the settle commit (receipt
   `receipts/coverage-at-tip.txt`).

## Out-of-scope items

The r97 gaps re-measured on the r98 checker and still open (a printed-tally fake that executes no
case reads `PASS 7/7`, `receipts/10-gap-printed-tally.txt`; an unbound-cell doctor reads `PASS 7/7`,
`receipts/11-gap-unbound-cell.txt`); the C2 checker's 150 unbound
rows; the capture's two new false-PASS shapes (the hybrid cell `VARIANTS N01-N04,N05`, and a
same-cell contradictory restatement); M07 (the ancestor check) unchanged; the assertion's being
bound to two families only, so the X/Y families' field lies stay uncertified; and the battery
selftest's inability to see a metadata assertion (no echo/era lie kind), which is the class behind
B01–B03.

{"seat":"ScribeLesson","verdict":"findings","notes":"Lesson draft (round-98.md) + review of the L1's draft (round-98.review.md) + report.md + 41 receipts; C1 legs 105/105 met x3, N07 103/105, N08 104/105, r97 control blind 105/105 x3 on all three gates; C2 selftest 14/14, M08 12/14 (same mutation PASS 12/12 on r97), D1/D2/D2lie and coverage PASS 157/157 x3; S392 byte-identical, S393/S394 byte offsets re-measured, limine CONFIG.md rejected with bytes/sha256/token counts; census exit 0, 0 E, rows 392 -> 393 (freeze) -> 394 (tree after S394); 7 citation defects and 7 missing fields in the L1's draft reported with commands."}
