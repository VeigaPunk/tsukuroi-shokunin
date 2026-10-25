# Seat report — C33Ledger319 (mutation-tester, C3 falsification item 3/8)

Round 37 attempt 1, wave 1. Axis: C3 — calibration (self-assessment mismatch repair; 27 fixed checks). Access date for every source cited below: 2026-10-25. All measurements are read-only on lane content; the only byte written into the lane repo is this seat report. No git/jj writes in lane/fleet/sibling repos; no pacman; no delegation/background jobs.

## 1. Claim under attack (target)

SCORECARD.md:1958-1968 ("Round 37 — pre-freeze C3 correction"), opened this round:

> "C3 — calibration: the self-assessment checker reports zero mismatches (all 27 fixed checks match) at the measured round-37 tip. Before: at base `564db0b614…`, `python3 tools/check-self-assessment.py --revision 564db0b614…` reported `checked: 27`, `mismatches: 5`, `status: FAIL`, exit 1 (K07-K11: four stale depth counts and one stale README line count). After: append-only correction of the five current self-assessment count cells to the measured tip values, then the same command at the measured round-37 branch-tip revision reports `checked: 27`, `mismatches: 0`, `status: PASS`, exit 0. The frozen predicate is `mismatches == 0 && checked == 27 && exit == 0` … The checker bytes and fixed 27-check population are unchanged; only the self-assessment values may change."

Attack: does a concrete fixed check carry a currently stale self-assessment value that produces a mismatch at the declaration base, and does the correction of that value make the **unchanged** checker report zero mismatches?

## 2. Tool read

`tools/check-self-assessment.py` (opened this round, lines 434-810 for `evaluate()`; 584-630 for K07-K11; 649-727 for K13/K16-K19). 27 fixed checks K01-K27. Checker blob hash identical at all four revisions measured: `ac28365ff10e8a8c91747bf6b08d3df1a5b3b5aa` for `564db0b614…`, `d06cedb…`, `ee36f9e…`, `0e5f70f…` (`git rev-parse <rev>:tools/check-self-assessment.py`). The claim's "checker bytes unchanged" premise holds.

## 3. Declaration base: five stale cells reproduce exactly the claimed "before"

`python3 tools/check-self-assessment.py --repo <lane> --revision 564db0b614b2914de5452f9ebd537a0653ae1de5` → exit 1, `checked 27`, `mismatches 5`, status FAIL. Mismatch records (verbatim reasons):

| Check | stated | observed | reason |
|---|---|---|---|
| K07 | 55 | 56 | depth row states 55 notes; corpus/knowledge holds 56 .md files |
| K08 | 3009 | 3110 | depth row states 3009 SKILL.md lines; SKILL.md holds 3110 newline characters |
| K09 | 784 | 839 | depth row states 784 table lines; SKILL.md holds 839 pipe-prefixed lines |
| K10 | 46 | 49 | depth row states 46 lesson files; corpus/lessons holds 49 files |
| K11 | 256 | 269 | coverage row states 256 corpus/README.md lines; the file holds 269 newline characters |

Stale cells live in the operative depth/coverage rows at SCORECARD.md:1570-1571 (base revision). The claim's own "before" (K07-K11, four stale depth counts + one stale README count) is accurate.

### Concrete fixed check (item 3/8): K08

Subject (checker lines 592-600): "depth row SKILL.md line count equals the line count of SKILL.md". At the declaration base, the depth row states `SKILL.md 3009 wc -l` while the blob at that revision holds 3110 newline characters → mismatch. K07/K09/K10/K11 are the same staleness family (count cells not re-derived after the measured tree grew).

## 4. Correction proposal (self-assessment values only; checker untouched)

Restate the five operative count cells to the measured values at the revision (exact before → after fragments):

1. K07: `55 notes` → `56 notes` (depth row evidence cell)
2. K08: `` `SKILL.md` 3009 `wc -l` `` → `` `SKILL.md` 3110 `wc -l` `` (depth row)
3. K09: `784 table lines` → `839 table lines` (depth row)
4. K10: `` `corpus/lessons/` (46 files) `` → `` `corpus/lessons/` (49 files) `` (depth row)
5. K11: `` `corpus/README.md` 256 `wc -l` `` → `` `corpus/README.md` 269 `wc -l` `` (coverage row)

Historical/superseded tables keep their text; only the operative current rows change. No checker edit, no new check, no config change.

## 5. Fixture verification (fresh mktemp repos; top-level verified == fixture root before commit)

- **Pristine fixture** (git archive of `564db0b614…` extracted into fresh mktemp dir; `git init`, add, commit; fixture HEAD `82ba24a501c690843d1223bef0bc7b37a9fb08c0`; SCORECARD.md sha256 `2357bb9af388dd642b64ff68d7d00a40430c45c0df4e9370116e12deab9ec519`): same checker, same revision → exit 1, FAIL, `checked 27`, `mismatches 5`, exactly K07-K11 with the same reasons as the lane base.
- **Corrected fixture** (same pristine tree + the five cell corrections above; fixture HEAD `adffc504792310a505bc5ae9893f4e86d8684f76`; SCORECARD.md sha256 `792186d3de42c9a45c1ce3543305caa777e24811abad0abeec68cccd094c8824`): same checker, same revision → exit 0, PASS, `checked 27`, `mismatches 0`.

Result: the unchanged checker flips from 1 mismatch (K08) / 5 total to zero mismatches when the five values are corrected. K08 (and K07/K09/K10/K11) is a genuine stale-value check; the proposed correction is sufficient for the frozen predicate.

## 6. Chain observation (tip-dependence of the claim)

This round's own measurement artifacts (`.ufo/waves/round-37/after-c3-*.json`, opened this round) show the repair only reached the predicate at the **last** commit:

| revision | checker result |
|---|---|
| `d06cedb` | FAIL, 2 mismatches (K17 names absent path `after.md`; K18 names absent `selftest-after.json`, `mode-policy-mutant.json`) |
| `ee36f9e` | FAIL, 1 mismatch (K17: host-census-gate row states None cases; census selftest prints 105) |
| `5124bf3` | CANNOT_EVALUATE — "missing capability row sources-registry" |
| `0e5f70f` (final tip) | PASS, 0 mismatches, exit 0 (re-measured this round) |

So the C3 predicate holds only at the final tip; any earlier candidate "measured round-37 tip" would falsify the claim as written (the declaration does not pin which commit is the measured tip). This is a robustness finding, not a change request: the frozen predicate is satisfied at the current tip.

## 7. Verdict

- K08 (with K07/K09/K10/K11) is a concrete fixed check whose stale self-assessment value produced real mismatches at the declaration base `564db0b614` — reproduced byte-for-byte in a pristine fixture.
- The proposed five-cell correction makes the unchanged checker report `checked 27 / mismatches 0 / PASS / exit 0` — reproduced in the corrected fixture.
- Checker bytes unchanged across base→tip (identical blob hash), so the claim's "only the self-assessment values may change" precondition held.
- No lane content was mutated; fixture repos are disposable scratch copies under `/tmp` (hashes above).
