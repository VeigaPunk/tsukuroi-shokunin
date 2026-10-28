VERDICT: defect-found

Seat R51RevNoHarm, item N-1 (no-harm and self-assessment) at frozen revision 2732ee6c06108c031c4d8043239b994e0504eb2f. Non-counted w1 seat. Receipts: `.ufo/waves/round-51/w1/R51RevNoHarm/`.

## Summary

| Check (at 2732ee6c) | Result | Base c0ad548a | Attribution |
|---|---|---|---|
| `check-self-assessment.py` | FAIL, checked 27, **mismatches 3** | FAIL, mismatches 1 (K10) | K10 pre-dates the round. K08 and K09 are **new, caused by this round's SKILL.md edit** (+11 registry rows). |
| `check-registry-coverage.py` | PASS, registered 88, tools 88, missing 0 | FAIL, registered 77, tools 83, missing 6 | Round fixes the 6 missing rows and adds 5 for new tools. |
| `tsukuroi-census.sh --selftest` | PASS, 168 cases, 168 passed, 0 failed, rc 0 | n/a | Census unchanged (see below). |
| `check-fd-band-r49.py` | PASS (`stale_ok 1, diag_ok 1, band_ok 1, cases 168`) | n/a (round-49 counter) | Not affected. |
| `check-adjacency-anchors.py` | PASS (inbound 114 classified, outbound_portable 10/10, live_object_match 10/10) | n/a | Not affected. |

## 1. Self-assessment: one pre-existing mismatch, two self-inflicted

Frozen output (`.ufo/waves/round-51/w1/R51RevNoHarm/self-assessment-summary.txt`):
- K08: depth row states `SKILL.md` 4594 `wc -l`; file has 4605 newlines.
- K09: depth row states 1326 table lines; file has 1337 pipe-prefixed lines.
- K10: depth row states 75 lesson files; `corpus/lessons/` holds 76.

Base: the before-receipt `.ufo/waves/round-51/before/self-assessment-at-base.json` shows `mismatches: 1` with only K10. I quote that receipt rather than re-running the checker at c0ad548a; the base comparison is therefore receipt-based, not an independent re-run.

Attribution:
- **K10 pre-dates the round.** `git ls-tree -r --name-only 2732ee6c corpus/lessons | wc -l` = 76 at the frozen rev; the round's diff stat (`.ufo/waves/round-51/w1/R51RevNoHarm/round-diff.out`) touches no `corpus/lessons/` file.
- **K08 and K09 are caused by the round.** `git show c0ad548a:SKILL.md | wc -l` = 4594 and `grep -c '^|'` = 1326 at base; at 2732ee6c they are 4605 and 1337. The +11 is exactly the 11 registry rows added in SKILL.md (`git diff c0ad548a 2732ee6c -- SKILL.md`). The checker reads the last `## Axes - ` block (`tools/check-self-assessment.py:459-472`), which is the round-50 block at `SCORECARD.md:3251-3255`; that depth row was not refreshed.
- The round's SCORECARD addition (`git diff c0ad548a 2732ee6c -- SCORECARD.md`, +23 lines) is a `## Round 51 — declaration` section, not a new `## Axes - ` block, so it does not move the binding row.

Consequence: calibration (judged axis) goes from 1 to 3 mismatches in this round's own surface. The round's declaration (`SCORECARD.md` round-51 block) records base "mismatches 1" and does not mention the new failures.

Proposed fix (planner decision; I did not run it): after SKILL.md is final for the round, append a new block `## Axes — current self-assessment (round 51 final measured surface)` that copies the round-50 six-row table verbatim except the depth row, which becomes:
`| depth | 8 | 67 notes (...); `SKILL.md` 4605 `wc -l` / 1337 table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` 76 files (`find corpus/lessons -type f \| wc -l`); ... | round 4; unchanged |`
This must be the last commit touching SKILL.md, because any further row shifts K08/K09. Then re-run `python3 tools/check-self-assessment.py --revision <REV>` (NOT run by me; the checker's 27 checks would run against the new block and must be re-verified). Do not edit the round-50 block in place.

## 2. Registry coverage

`check-registry-coverage.py --revision 2732ee6c…` → `registered 88, tools_total 88, missing 0, findings []` (`.ufo/waves/round-51/w1/R51RevNoHarm/rc.out`). The base receipt `.ufo/waves/round-51/before/registry-coverage-at-base.json` shows missing 6 (check-adjacency-table-r49, check-fd-band-r49, check-scrub-admission-r47, -r48, plus two more). The round's 11 new rows are the 6 previously-missing tools plus 5 new r51 tools.

## 3. SKILL.md's 11 new rows: entry command and flags

Every entry command exists at the frozen rev (`git archive 2732ee6c tools`; each `tools/<name>` present). `--help` run on the frozen bytes (`entry-help.txt`):

| Row | Entry command | Flags in row | Present in argparse |
|---|---|---|---|
| scrub-admission-r47 | check-scrub-admission-r47.py | --revision, --lane, --section-hash | yes |
| scrub-admission-r48 | check-scrub-admission-r48.py | same | yes |
| scrub-admission-r49 | check-scrub-admission-r49.py | + --wave-dir, --results-file | yes |
| adjacency-table-r49 | check-adjacency-table-r49.py | --revision, --lane | yes |
| fd-band-r49 | check-fd-band-r49.py | --work, --lane | yes |
| selftest-tmpdir-r48 | score-selftest-tmpdir-r48.py | --revision, --census, --lane, --work, --cases | yes |
| grounding-lint-r51 | lint-grounding-r51.py | --worktree, --lane, --emit-gaps | yes |
| scrub-admission-r51 | check-scrub-admission-r51.py | + --wave-dir, --results-file, --dispatch-file | yes |
| selftest-matcher-r51 | check-selftest-matcher-r51.py | --scratch, --runs, --census-file | yes |
| counter-cheats-r51 | score-counter-cheats-r51.py | --scratch, --counter, --skip-r50, --runs | yes |
| adjacency-table-r51 | check-adjacency-table-r51.py | see nit below | yes |

Nit (defect-level, text only): the adjacency-table-r51 row writes `[--control ...]`. The argparse flag is `ap.add_argument('--control', action='store_true')` (`tools/check-adjacency-table-r51.py:308`) and `--help` shows bare `[--control]`. Proposed row text: replace `[--control ...]` with `[--control]`. The row also omits `--siblings-root`, `--province-file`, `--registry-file`, `--skip-anchors-check` (all override flags that trigger OVERRIDE-NOT-MEASURED at `check-adjacency-table-r51.py:208-210`); adding `[--siblings-root <DIR>] [--province-file <F>] [--registry-file <F>] [--skip-anchors-check]` is optional.

Exit code 3 for an un-`--control` override in the row matches the code (`check-adjacency-table-r51.py:209-210`, return 3).

## 4. Census selftest and census identity

- `TMPDIR=<scratch> bash tools/tsukuroi-census.sh --selftest` → `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)`, exit 0, stderr 0 bytes (`selftest.out`, `selftest.err`). One run only.
- `git diff c0ad548a 2732ee6c --stat -- tools/tsukuroi-census.sh` is empty (`census-diff.out`, 0 bytes). Sha256 of `tools/tsukuroi-census.sh` is `aeda2cbc…0245dc` in the working tree, at 2732ee6c and at c0ad548a — identical.
- The fd-band check (`check-fd-band-r49.py`) also ran the census selftest internally; 168 cases, PASS.

## 5. Other observations

- The lane `master` tip is now 6d051ef06 (commit "round-51: wave w1 spec, validated dispatch…"), a descendant of 2732ee6c. Its diff is 6 files under `.ufo/waves/round-51/` only (w1-spec.json, w1-dispatch.json, make-spec.py, controls summaries); no SKILL.md, tools/ or corpus/ change. Checks above are at 2732ee6c as instructed.

## Limits and what I did not do

- I did not re-run `check-self-assessment.py` at c0ad548a; the base mismatch comparison uses the committed before-receipt.
- I did not run the proposed new `## Axes` block through the checker (it is a planner decision and I may not edit SCORECARD).
- I did not run any of the round's counted or C1-C3 counters (out of scope for this seat).
- Tool installs: none. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51RevNoHarm/` removed after copying receipts.
