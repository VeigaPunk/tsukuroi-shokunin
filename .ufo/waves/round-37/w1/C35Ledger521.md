# C35Ledger521 — C3 falsification item 5/8: self-assessment mismatch repair

## Scope and verdict

Axis: **C3 calibration** (round-37 claim at `SCORECARD.md:1958-1968`: the unchanged
`check-self-assessment.py` (27 fixed checks K01-K27) reports `mismatches == 0` at the
measured round-37 tip, after an append-only correction of five stale self-assessment count
cells). Seat attacked the repair claim only; no lane/source/Git state changed, no host
changes, no tools installed. Tooling rules read first: `/home/vgpnk/.omp/agent/RULES.md`
lines 1-14 (no install needed).

**Verdict:** the claim's before-state reproduces exactly (5 mismatches, K07-K11, exit 1 at
base `564db0b614`). The claim's stated repair — *"append-only correction of the five current
self-assessment count cells"* — does **not** by itself produce the declared after-state in
the lane: the commit that carries exactly that correction (`d06cedb`) still fails with 2
capability-row mismatches (K17/K18), and the next commit (`ee36f9e`) still fails with 1
(K17 case-count unstated). Zero mismatches appear only after a **third**, capability-row
correction (`0e5f70f`). The after-predicate holds at the final tip, but the claim under-
specifies the repair; the correction proposal below is the smallest set that makes the
unchanged checker report zero, verified on a scratch fixture.

## Evidence opened (all read-only; checker bytes pinned)

- `tools/check-self-assessment.py` K01-K27 implementation, read lines 434-810; sha256
  `1e1ab6113d665684e15d147c0f3dae519cf2d313877e1603b841ad4db85d4257` identical at base
  `564db0b614` and tip `0e5f70f` (unchanged tool).
- `SCORECARD.md` (working tree, 2026-10-25): round-37 declaration lines 1857-1968;
  pre-freeze C3 correction lines 1950-1974; axes tables lines 1976-2011; capabilities
  tables lines 2013-2022; K17 supersession row lines 2026-2039.
- Checker runs (JSON captured, status/counts/reasons): base `564db0b614` → `FAIL`, 27
  checked, 5 mismatches; `d06cedb` → `FAIL`, 2; `ee36f9e` → `FAIL`, 1; tip `0e5f70f`
  → `PASS`, 27 checked, 0 mismatches, exit 0 (`declaring_round` 37; axes heading
  `## Axes — current self-assessment (round 37)`).
- L1 receipts `.ufo/waves/round-37/after-c3-ee36f9.json` (mismatches 1, FAIL) and
  `after-c3-0e5f70.json` (mismatches 0, PASS) corroborate the same point.

## Concrete fixed check with a stale self-assessment value at the declaration base

At base `564db0b614`, the unchanged checker reports 5 mismatches — all count cells:

| Check | Subject | Stated | Observed |
|---|---|---|---|
| K07 | depth notes | 55 | 56 |
| K08 | `SKILL.md` lines | 3009 | 3110 |
| K09 | `SKILL.md` table lines | 784 | 839 |
| **K10** | `corpus/lessons/` files | **46** | **49** |
| K11 | `corpus/README.md` lines | 256 | 269 |

Concrete instance: **K10** — the depth row states 46 lesson files, while
`corpus/lessons/` holds 49 at the revision (mismatch reason from run JSON:
`depth row states 46 lesson files; corpus/lessons holds 49 files`). K07-K11 are the
"four stale depth counts and one stale README line count" named by the claim; reproduced
exactly.

## Correction proposal (verified with the unchanged checker on a scratch fixture)

1. Restate the five count cells (K07-K11) to the measured values using parser-literal
   phrases: `56 notes`, `` `SKILL.md` 3110 `wc -l` ``, `839 table lines`,
   `` `corpus/lessons/` (49 files) ``, `` `corpus/README.md` 269 `wc -l` ``.
2. Keep the operative `host-census-gate` capability row stating a numeric selftest case
   count (`PASS (105 cases, 105 passed, 0 failed)` or `PASS 105/105`) and only existing
   paths — required because the capability-row rewrites between `d06cedb` and
   `0e5f70f` (K17/K18) otherwise keep the checker red.

Verification: fresh `mktemp` repo (top-level verified equal to fixture root before commit)
built from `git archive 564db0b614` + step 1 only → unchanged checker reports `PASS`, 27
checked, 0 mismatches, exit 0. Current tip `0e5f70f` (steps 1+2 both landed) reports
`PASS`, 27 checked, 0 mismatches, exit 0.

## Falsification finding (why the claim as written is over-narrow)

- `d06cedb` "self-assessment counts corrected to measured tree" = exactly the five-cell
  correction, yet the unchanged checker reports 2 mismatches: K17 `host-census-gate row
  names 1 path(s) absent at the revision: after.md`; K18 `root-metadata-observer row
  names 2 path(s) absent at the revision: mode-policy-mutant.json, selftest-after.json`.
- `ee36f9e` "correct missing capability evidence pointers" fixes the paths but drops the
  case-count phrase from the operative row → K17 `host-census-gate row states None cases;
  the census selftest at this revision prints 105 cases` (stated_line 2020).
- `0e5f70f` adds the K17 supersession row (`SCORECARD.md:2026,2030,2039`, "K17 requires
  the current host-census-gate capability row to state the selftest case count") → PASS 0.
- Therefore the after-predicate `mismatches == 0 && checked == 27 && exit == 0` is satisfied
  only at the final tip, and only because of capability-row edits the claim does not name;
  the do-nothing control (base) and the literal five-cell-only repair are both red.

## Gates, touched surfaces, limits

- Read-only: no lane/fleet/sibling Git or jj writes; no `git add/commit/push/fetch` on
  lane repos; scratch repos lived only under `/tmp` (`c35basefix2-*`) and were deleted
  with the session; no pacman/host changes; no delegation or background jobs.
- Cited sources were opened this round (paths + lines above); no external URLs.
- Out of scope: other falsification items, other claims, and implementing the correction;
  scratch validation used the unchanged production checker only.

## Artifact paths

- This report: `.ufo/waves/round-37/w1/C35Ledger521.md`
- Run outputs: `/tmp/c35_base.json` (base, 5 mismatches), `/tmp/c35_head2.json` (tip
  `0e5f70f`, PASS 0), `/tmp/c35_5cell.json` (scratch five-cell fix, PASS 0),
  `/tmp/c35_$r.json` for `b8ededd`/`d06cedb`/`ee36f9e` where noted.
- L1 receipts read: `.ufo/waves/round-37/after-c3-ee36f9.json`,
  `.ufo/waves/round-37/after-c3-0e5f70.json`.

## Tool install/update

None (RULES.md channels not needed).
