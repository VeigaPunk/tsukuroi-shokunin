# Round 71 — QUALITY criterion draft (105) and counter-attack scoreboard continuation

author: `SC3Lesson` (wave w1, round 71), drafted for the L1 to land append-only in `corpus/QUALITY.md`
(the file's last criterion at `0fcfca31` is 104) and to carry into `corpus/lessons/round-71.md`.
status: draft — nothing here is adopted until the L1 lands it, and no cell is an after-measurement.

105. **A round's selftest figures are diffed against the final receipt line before the report is written (R71-STALE-TALLY-SWEEP):** every selftest case-count and label-count figure a round writes into `SCORECARD.md`, `PROVINCE.md`, `corpus/README.md`, `SKILL.md`, the report or the lesson is swept, before the report is filed, over the round's own added lines (`git diff -U0 <base> <head>`) against the final receipt's own `PASS (N cases, N passed, 0 failed)` line and its label-line count; the sweep prints each `file:line` with the figure written and the receipt's figure, and a round with a mismatch does not file that figure until it is corrected append-only. Scoping to added lines keeps historical figures in the same files out of scope by construction, and a battery's own `BATTERY cases=N passed=N failed=0` footer is the receipt line for any figure about that battery. Red state: round 70's landing added five figures its own final receipt contradicts — `PROVINCE.md:372` `(212 cases, 16 labelled R70-C2)`, `corpus/README.md:613` `196 -> 212`, `SKILL.md:5773-5774` `196 → 212 cases` / `16 of them labelled` — against `.ufo/waves/round-70/after/selftest-after.txt:217` `PASS (214 cases, 214 passed, 0 failed)` with 18 `R70-C2` lines, and round 71's declaration repeats the class with `12 cases: 1 well-formed control + 11 mutants` against `before/control/battery.txt:24` `BATTERY cases=11 passed=11 failed=0`. Green state: the same sweep over the corrected diff prints `added_figures_mismatched=0` and rc 0. Shown able to fail: `python3 .ufo/waves/round-71/probes/SC3Lesson/sweep-selftest-tally.py --receipt .ufo/waves/round-70/after/selftest-after.txt --label R70-C2 --range b2aa0be0..79dac76c -- PROVINCE.md corpus/README.md SKILL.md` prints 5 mismatches and rc 1; the `--diff-file .ufo/waves/round-71/probes/SC3Lesson/r70-added-corrected.diff` control prints 0 and rc 0 (receipt `.ufo/waves/round-71/probes/SC3Lesson/sweep-receipt.txt`). Lesson: `corpus/lessons/round-71.md` §Mistakes `R71-D1-STALE-TALLY-OPEN` and `R71-DECL-BATTERY-COUNT`.

## Sweep receipt

Run at `0fcfca31`, 2026-11-04T00:59Z; full transcript in
`.ufo/waves/round-71/probes/SC3Lesson/sweep-receipt.txt`. The sweep's scope is the round's added
lines, so the same three files' historical figures (17, 26, 35, 49, 74, 80, … 196) are not scored.

```
### RED — round-70 added figures vs round-70 final receipt
MISM PROVINCE.md:372 cases_figure=212 receipt=214
MISM PROVINCE.md:372 label_figure=16 receipt=18
MISM SKILL.md:5773 cases_figure=212 receipt=214
MISM SKILL.md:5774 label_figure=16 receipt=18
MISM corpus/README.md:613 cases_figure=212 receipt=214
SWEEP added_figures_mismatched=5 receipt_cases=214 receipt_labels=18
rc=1

### GREEN control — same diff, the five figures corrected to the receipt
OK   PROVINCE.md:372 cases_figure=214 receipt=214
OK   PROVINCE.md:372 label_figure=18 receipt=18
OK   SKILL.md:5773 cases_figure=214 receipt=214
OK   SKILL.md:5774 label_figure=18 receipt=18
OK   corpus/README.md:613 cases_figure=214 receipt=214
SWEEP added_figures_mismatched=0 receipt_cases=214 receipt_labels=18
rc=0
```

The corrected diff is a **control only** (`r70-added-corrected.diff`); the r70 files themselves still
carry 212/16 at `0fcfca31` and the correction is owed append-only (lesson `R71-D1-STALE-TALLY-OPEN`).
The same sweep, pointed at the round-71 declaration's battery sentence, reads `12` against the
receipt's `11` (lesson `R71-DECL-BATTERY-COUNT`).

## Scoreboard continuation — round 71 (continuation of the r64 ledger)

Rows are the round's C1 counter arms and C2 harness arms; the survivor and class cells are left as
`<wave>` for the wave's attack receipts to fill. Rounds 40-70 rows stay in their own lessons.

| Counter | Round / arm source | Arms fielded (receipts) | Survivors (arms that reached PASS) | Class that beat it |
|---|---|---|---|---|
| `count-mp-rows-r71.py` (C1) | r71 pre-data battery (`before/control/battery.txt`) | 11 cases: 1 control + 10 mutants (the declaration's prose says 12: lesson `R71-DECL-BATTERY-COUNT`) | `<wave>` | `<wave>` |
| `count-mp-rows-r71.py` (C1) | r71 wave w1 attack receipts (`w1/<seat>.md`, `probes/<seat>/`) | `<wave>` | `<wave>` | `<wave>` |
| `selftest-case-timeout` harness (C2) | r71 pre-data red-before (`before/redbefore-timeout.txt`) | 1 blocking probe at an external 20 s bound (rc 124, 0 verdict lines) | `<wave>` | `<wave>` |
| `selftest-case-timeout` harness (C2) | r71 wave w1 harness mutants (`probes/<seat>/`) | `<wave>` | `<wave>` | `<wave>` |

Landing note for the L1: the criterion is appended as 105 in `corpus/QUALITY.md`; the sweep script is
drafted at `.ufo/waves/round-71/probes/SC3Lesson/sweep-selftest-tally.py` and needs its own `tools/`
row (QUALITY 70) if the lane adopts it as a tool. The scoreboard rows belong in the lesson's
`## Considerthese` section, as at r70.
