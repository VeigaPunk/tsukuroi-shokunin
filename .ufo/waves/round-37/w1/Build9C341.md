# Build9C341 — C3 checker red-before control (design item 9/12)

Seat: Build9C341 (executor, wave tsukuroi-r37-w1). Axis: calibration (build:C3 baseline control design).
Date: 2026-10-25. All commands sandboxed; lane repo touched read-only; git writes only in a fresh mktemp fixture repo.

## Axis and moves (godspeed)

- Axis A (calibration): prove the C3 self-assessment checker is **red on the unchanged baseline**, so a later green is meaningful and the do-nothing target is unreachable.
- Axis B (isolation): the control must run standalone from a fixture repo, never from lane state, and must fail loudly if the baseline is green.

Kept: only moves that improve A/B and harm nothing. No lane/fleet/sibling writes, no pacman/host changes, no delegation. Tooling: no tool installed (uses existing `git`, `python3`, `bash`; RULES.md read, update-safety gate not triggered).

## Deliverables (seat directory `.ufo/waves/round-37/w1/Build9C341/`)

1. `c3-red-before-control.sh` — isolated runnable control harness (executable).
2. `patch-r35-axes-C3.patch` — precise five-cell correction proposal (15 lines, 2 rows).
3. `before.json` / `after.json` — captured checker payloads from the fixture runs.

## How the check fails on unchanged baseline (red-before)

Baseline revision `564db0b614b2914de5452f9ebd537a0653ae1de5` (round-36 verifier spot-check commit; the recorded before receipt). Run:

```
python3 tools/check-self-assessment.py --revision 564db0b614b2914de5452f9ebd537a0653ae1de5
```

Observed (also reproduced inside the fixture, see below): exit **1**, `status: FAIL`, `checked: 27`, `mismatches: 5`. The five red checks are K07-K11, all stale count cells in the round-35 axes table (`SCORECARD.md:1570-1571` at the base):

| check | subject | stated | observed |
|---|---|---|---|
| K07 | depth row note count | 55 | 56 |
| K08 | depth row `SKILL.md` line count | 3009 | 3110 |
| K09 | depth row table-line count | 784 | 839 |
| K10 | depth row `corpus/lessons/` file count | 46 | 49 |
| K11 | coverage row `corpus/README.md` line count | 256 | 269 |

This matches the committed before receipt (`.ufo/waves/round-37/before/c3-before.json`: 27 checked / 5 mismatches / FAIL, revision 564db0b…; `c3-before-exit.txt`: `exit=1`).

## What after state it measures

Frozen C3 predicate (declaration, `SCORECARD.md` round-37 correction section): `mismatches == 0 && checked == 27 && exit == 0`. The control measures the corrected revision: same checker bytes, same 27-check population, self-assessment cells updated to tip values. Observed after correction (fixture): exit **0**, `status: PASS`, 27 checked, 0 mismatches. The same transition holds live on the lane: at the measured HEAD `0e5f70fa` the checker exits 0 with 0 mismatches (run this round).

## Harness behavior (evidence)

Fixture built via `git -C <lane> archive <base>` (read-only) into a fresh `mktemp` repo; top-level verified equal to fixture root before each commit (`git rev-parse --show-toplevel` == fixture root). Results:

- Baseline fixture commit `22f1d85` → `rc=1`, checked=27, mismatches=5, ids `['K07','K08','K09','K10','K11']` — **CONTROL OK (red-before)**.
- Corrected fixture commit `e1e3423` (patch applied, committed) → `rc=0`, checked=27, mismatches=0 — **AFTER OK (green)**.
- The harness exits 2 if the baseline is not red, 3 if the correction does not reach green.

The patch touches only the two axes-table rows (depth/coverage); replacements are line-scoped (no global number substitution): `55→56`, `3009→3110`, `784→839`, `46→49`, `256→269`.

## Sources opened this round (anchors)

- `tools/check-self-assessment.py` (read: `evaluate()` lines 434-810, `main()` 1084-1119, K13 census selftest 649-655, `_GIT_SANDBOX` 69-72).
- `.ufo/waves/round-37/before/c3-before.json` / `c3-before-exit.txt` (5 mismatches, exit=1).
- `.ufo/waves/round-37/after-c3-d06ced.json` (2 mismatches at d06cedb, pre-header correction).
- `SCORECARD.md` at 564db0b (axes table lines 1570-1571) and at HEAD (round-37 tables ~2006-2007), and the round-37 declaration/correction sections.
- `git log` / `git diff 564db0b HEAD -- SCORECARD.md` (confirms correction commit d06cedb "self-assessment counts corrected to measured tree" and current tip 0e5f70fa).

## Risks / notes

- K13 runs the census selftest inside the fixture (`git archive` worktree), so the harness takes ~35 s; it is hermetic.
- The control proves the *checker's* red-before; it does not verify the census or other checks independently (out of scope).
- The replacement is append-only per declaration; the patch edits the round-35 table in place (the checker reads the last axes section).
