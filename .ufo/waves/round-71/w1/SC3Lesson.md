# SC3Lesson — round 71, wave w1 (scribe): lesson skeleton, Mistakes, QUALITY 105, scoreboard rows

status: draft delivered to the wave dir; no lane-tree write, no commit, no delegation. The L1 is the
only writer of `corpus/` and `SCORECARD.md`; nothing below is landed.

## Behavior

Drafted the round-71 lesson skeleton (`## Gate`, `## Mistakes`, `## Considerthese`, `## Trend
verdicts`, seat-harm tally) and the r70-routed QUALITY criterion 105, plus the round-71
counter-attack scoreboard row set. Every after-measurement cell is left `<wave>`. The three
r70-routed classes (D1 stale tally, D2 unbacked final-revision receipt, D3 shebang/source mismatch)
were re-measured at `0fcfca31`; a fourth, new measured defect (the declaration's battery case count)
was added.

## Checks run (all read-only; lane tree untouched)

| Check | Command | Observed |
|---|---|---|
| snapshots complete | `sha256sum -c .ufo/waves/round-71/before/src/SHA256SUMS` | 4/4 OK, rc 0 |
| map keys | `python3 -c "json.load(...SOURCES.json)"` | 4 keys, digests equal pins |
| registry at base | `git show 930d5530:corpus/SOURCES.md \| grep -cE '^\|\s*S[0-9]{3,}\s*\|'` | 296 |
| planned ids free | same file, `grep -cE 'S29[7-9]\|S300'` | 0 |
| notes at base | `git ls-tree -r --name-only 930d5530 -- corpus/knowledge \| grep -c '\.md$'` | 88 |
| r70 final receipt | `.ufo/waves/round-70/after/selftest-after.txt:217` | `PASS (214 cases, 214 passed, 0 failed)`, 18 `R70-C2` lines |
| D1 sweep (red) | `sweep-selftest-tally.py --receipt … --label R70-C2 --range b2aa0be0..79dac76c -- PROVINCE.md corpus/README.md SKILL.md` | 5 mismatches, rc 1 |
| D1 sweep (green control) | same, `--diff-file r70-added-corrected.diff` | 0 mismatches, rc 0 |
| D1 open state | `grep -n "212 cases\|196 -> 212\|196 → 212" PROVINCE.md corpus/README.md SKILL.md` | 3 files still carry 212/16 |
| D2 | report `.ufo/reports/round-70/tsukuroi.md:104-105` vs `git ls-tree 79dac76c -- .ufo/waves/round-70/after .ufo/waves/round-70/probes` | no receipt names `79dac76c` |
| D3 | `git show 0fcfca31:tools/count-xs-rows-r70.py \| head -1`; `git diff --stat tools/count-xs-rows-r70.py` | `#!/usr/bin/env bash` at the commit; one-line repair uncommitted in the worktree |
| battery count | `0fcfca31:SCORECARD.md:5467` vs `before/control/battery.txt:24` | prose 12 (1+11) vs receipt `cases=11` (1 control + 10 mutants) |
| considerthese status | exact-phrase greps over `corpus/ SKILL.md PROVINCE.md` | scoreboard 15, seat-harm 4, burst 2, cross-note 0 (5 case-insensitive "propagation map") |

## Findings

- **F1 (new, measured)** — the round-71 declaration's battery sentence (`12 cases: 1 control + 11
  mutants`) contradicts the committed battery's own footer (`cases=11`, 1 control + 10 mutants); the
  prose also enumerates ten mutants. Not a claim conjunct; recorded as `R71-DECL-BATTERY-COUNT`.
- **F2 (r70 D1)** — `PROVINCE.md:372`, `corpus/README.md:613`, `SKILL.md:5773-5774` still carry
  212/16 against the r70 final receipt 214/18. Status at draft: open.
- **F3 (r70 D2)** — the r70 report's final-revision re-run claims (75 files; counter 6/6 at
  `79dac76c`) have no committed receipt at that revision. Status: open.
- **F4 (r70 D3)** — the `count-xs-rows-r70.py` shebang repair exists only as an uncommitted worktree
  modification at `0fcfca31`. Status: repair present, uncommitted.
- **F5** — r70 spot-check routed items 4 (inherited dispatcher markers) and 5 (open L0 watches) are
  operator/closure items, not lane round debt; recorded as such, not as Mistakes.

## Out of scope (not done, by rule)

No lane-tree write/commit, no repair of D1/D2/D3 (L1's append-only work), no wave attack rows, no
round-end census, no non-author admit/reject spot-check, no `SCORECARD.md`/`corpus/` edits. Scratch
tree removed at yield; no tool installed.

## Artifacts

- `.ufo/waves/round-71/w1/SC3Lesson/lesson.md`
- `.ufo/waves/round-71/w1/SC3Lesson/quality.md`
- `.ufo/waves/round-71/probes/SC3Lesson/sweep-selftest-tally.py`
- `.ufo/waves/round-71/probes/SC3Lesson/sweep-receipt.txt`
- `.ufo/waves/round-71/probes/SC3Lesson/r70-added.diff`
- `.ufo/waves/round-71/probes/SC3Lesson/r70-added-corrected.diff`

KEY=VALUE
MISTAKES=4
QUALITY_CRITERION=105
CONSIDERTHESE_STATUS=verified
