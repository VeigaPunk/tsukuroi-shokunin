# MutGateUniquePointer — C2 evidence rule mutation probe

Verdict: the C2 evidence rule (SCORECARD.md:761 counting rule, enforced by
`tools/check-pause-gate.py`) **survives** the three assigned mutation probes —
boilerplate-only pointers, a duplicate-substring pointer, and a pointer at the
gate's own `.md`. Each mutant dropped premise P1 (`premises_verified` 5 -> 4,
exit 1). No defect found; no correction required.

Baseline (pristine, clone at 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0):
`python3 tools/check-pause-gate.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`
from the clone root -> exit 0, `status PASS`, `premises_total 5`,
`premises_verified 5`, `findings []`. This matches the declared after-value
(SCORECARD.md:749).

1. [obs] Mutant A (boilerplate-only pointers): P1's evidence array replaced in
   the clone's `corpus/knowledge/pause-lift-gate-r24.json` by exactly three
   pointers whose `contains` strings start with the boilerplate prefixes: `### time`
   (capture line 1), `$ date -u +%FT%TZ` (line 2), `exit=0` (line 4).
   Detector: exit 1, `status FAIL`, `premises_verified 4`, finding
   `GATE-PREMISE P1:no-unique-capture-pointer`; P1 `verified: false`,
   `problems: ["no-unique-capture-pointer"]`.
   Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutGateUniquePointer/m-boiler.json`.
   Mechanism: the anchor filter (`tools/check-pause-gate.py:122-124`) requires a
   capture pointer whose `contains` does not start with the boilerplate prefixes
   (`### `, `$ `, `exit=`; `tools/check-pause-gate.py:36`) and whose text occurs
   exactly once in the pinned capture. With only boilerplate needles, `anchors`
   is empty -> premise fails.

2. [obs] Mutant B (duplicate-substring pointer): P1's evidence replaced by one
   pointer, path capture, line 40, `contains "BETA-1"` — a substring that occurs
   exactly twice in the capture (`grep -o 'BETA-1' ...capture.txt | wc -l` =
   2). Detector: exit 1, `status FAIL`, `premises_verified 4`, finding
   `GATE-PREMISE P1:no-unique-capture-pointer`; P1 `verified: false`.
   Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutGateUniquePointer/m-dup.json`.
   Mechanism: `capture_text.count(needle) == 1` uniqueness check
   (`tools/check-pause-gate.py:124`) rejects the twice-occurring substring.

3. [obs] Mutant C (self-evidence): P1's evidence replaced by one pointer naming
   the gate's own markdown, `corpus/knowledge/pause-lift-gate-r24.md`, line 1,
   `contains "source: round-24 L1 read-only capture"`. Detector: exit 1,
   `status FAIL`, `premises_verified 4`, findings `GATE-PREMISE
   P1:no-unique-capture-pointer` and `GATE-PREMISE
   P1:self-evidence:corpus/knowledge/pause-lift-gate-r24.md`; P1 `verified: false`.
   Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutGateUniquePointer/m-self.json`.
   Mechanism: the self-evidence check (`tools/check-pause-gate.py:132-134` and
   `SELF_PATHS` at `:39`) rejects any pointer whose path is the gate JSON or the
   gate markdown, confirmed rejected as assigned.

4. [inf] The smallest behavior-bearing point in each probe (the error
   contents) was detected in all three shapes, so no defect in the claimed
   invariant survives. Smallest correction: none required.

Restoration evidence (clone `/fast/scratch/hyaku/tsuku24w2-MutGateUniquePointer/lane`):
- Before (baseline blob at 22fd1642): sha256 of `corpus/knowledge/pause-lift-gate-r24.json`
  = `279f2b7811d4a4b4083fb51b555cac0ad0d8b865ec45d8999c5b27b7b7a9f2ef`.
- Mutant blob sha256: m-boiler (commit 50d546900c07) `2e7781f5228d3b51bc08a79d6fedda32e994299200979ad27b488fbe2b26375c`;
  m-dup (commit 616f73419534) `b0f6e6007445b2ca306367796d9cb6f9990800537e142b8b419ed3081c8feea2`;
  m-self (commit fae2ece142c7) `9ec7556b9f3838bf863c9ea406c6709ccd4b4630246be08347790b81ed9f1065`.
- After restore: mutant branches deleted, HEAD back at 22fd1642e7fa...,
  `git status --porcelain` empty, JSON bytes identical to the original
  (sha256 re-computed as `279f2b7811d4a4b4083fb51b555cac0ad0d8b865ec45d8999c5b27b7b7a9f2ef`).

Scope: read=scorecard round-24 declaration and refinements, pause-lift gate entry
(.md and .json), tools/check-pause-gate.py, tools/_revision.py, round-24 capture
l1-4/capture.txt, clone state; wrote=.ufo/waves/round-24/w2/MutGateUniquePointer.md,
m-boiler.json, m-dup.json, m-self.json, m-boiler.exit, m-dup.exit, m-self.exit
(in .ufo/waves/round-24/w2/MutGateUniquePointer/); executed=git clone/checkout/
branch/commit/rev-parse/status (scratch clone only), python3 tools/check-pause-gate.py
--revision/--branch runs (baseline + 3 mutants), sha256sum/grep occurrence counts.
Installs: none
