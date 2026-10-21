# ConnPlanner — Bounded Planning Data-Walk and Integration Synthesis

**Seat:** `TsukuroiR19Recovery.ConnPlanner-2`  
**Role:** UFO-FSD Connector  
**Round:** Tsukuroi round 20, attempt 1 (`TsukuroiR20`)  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472`  
**Lane:** Production lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Target File:** `.ufo/waves/round-20/build/ConnPlanner.md`  
**Mode:** NO-EXEC (read/grep/glob only; zero subprocesses, shell/eval, host probes, or verification executions)

---

## 1. Declared Axes

The canonical axes and contract metrics for round 20 attempt 1 (per `.ufo/waves/round-20/preregister.json:4-29` and canonical assignment):

1. **C1 Adjacency** (ordinal 8, tied-lowest axis, ordinal delta 0):
   - Metric: `ownership_corrections` (before: 0, after: 1).
   - Evaluator: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
   - Scope: Explicit sibling-declaration wording for OUT-009 at retained pinned scope, no integrator arbitration or write authority.
2. **C2 Operability** (ordinal 9, ordinal delta 0):
   - Metric: `object_selector_tools` (before: 0, after: 9).
   - Evaluator: `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`.
   - Scope: Original-nine consumer continuity under object-only hexadecimal selector tests; discovered tools separate. Read-only `systemctl` exec-log classifier supporting repair.
3. **C3 Calibration** (ordinal 9, ordinal delta 0):
   - Metric: `audit_live_map_errors` (before: 1, after: 0).
   - Evaluator: `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.
   - Scope: Highest operative boot-chain-audit live map is `0 CONSISTENT/observation`, `2 UNKNOWN/could-not-evaluate`; code 1 is selftest failure only, never live DEGRADED. Append named R19 false-erratum and non-prefix disclosure.

All ordinal deltas remain strictly 0; genuine finite improvements within bounded claims, with no claims of host or boot safety.

---

## 2. Bounded Planning Data-Walk Against Claims and Lowest Axis

A systematic walk across the round-20 planning artifacts (`preregister.json`, `dispatch.json`, `plan.json`, `seeded-implementation.json`), external executor worktrees, and baseline files reveals the operational contract held by the canonical planner (L1):

1. **L1 Canonical Role and Integration Ownership:**
   - L1 is the sole integration writer and held canonical planner (`context:4`).
   - Wave seats operate as isolated leaf members without delegation or shared-checkout write authority.
   - Implementation worktrees were segregated across external paths:
     - `/tmp/tsukuroi-r20-adjacency-20261021` (C1, unseeded)
     - `/tmp/tsukuroi-r20-binder-20261021` (C2 binder, seeded)
     - `/tmp/tsukuroi-r20-registry-20261021` (C3 registry coverage, seeded)
     - `/tmp/tsukuroi-r20-execscope-20261021` (C2 supporting exec-log repair, seeded)
   - L1 integrates the external worktree deltas into the production lane and executes the final measurement wave once all seats settle.

2. **The Lowest Axis (C1 Adjacency):**
   - Baseline ordinal is 8 (tied lowest with depth, compared to 9 for operability, calibration, coverage, and freshness).
   - The C1 claim addresses historical defect OUT-009 (`.ufo/waves/round-19/falsify/FxConnOverlap.md:46`), where baseline `PROVINCE.md:129` asserted that "Revenger owns shipped-artifact reverse engineering...", contradicting `PROVINCE.md:79-80` (integrator must arbitrate between Kaidoku and Revenger) and `PROVINCE.md:8-9` (Tsukuroi owns OS package state, whereas Revenger only declared Electron/JavaScript packages).
   - The production lane appends `## R20 ownership clarification — OUT-009` at `PROVINCE.md:148-152` as an explicit sibling declaration without altering historical rows or registries.

3. **Concrete Missing Finite Criterion Identified:**
   - In `dispatch.json:436` (the canonical planner's explicit directive for `ExecAdjacency`), the specification instructed:
     > *"Prefix preservation against base can be checked for PROVINCE to ensure no old rewrite. Keep baseline red named actual missing correction, not missing registry."*
   - Inspection of `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:123-178` (`_ownership_correction`) reveals that this criterion was **omitted from the candidate implementation**:
     - The function locates `OWNERSHIP_HEADING` (`## R20 ownership clarification — OUT-009`).
     - If absent, it emits `OWNERSHIP-CORRECTION-MISSING`.
     - If present, it checks that `lines[start:end]` strictly matches `OWNERSHIP_SECTION_LINES`, that `OWNERSHIP_ARBITRATION_LINES` exist in the file, and that strings `"| OUT-008 | ADJ-06 |"` and `"| OUT-009 | ADJ-06 |"` appear in `province_text`.
     - **However, `_ownership_correction` never compares `lines[:start]` against the baseline `PROVINCE.md`.**
   - Why this omission is a critical planning defect:
     - In round 19, an author claimed an "append-only" addition to `SKILL.md`, but silently rewrote historical row 1965 in place (`+80/−1`). This broke historical integrity, failed to repair the operative row, and forced the round-20 disclosure `R20-SKILL-PREFIX-EXCEPTION` (`SKILL.md:2088`).
     - In round 20, if `PROVINCE.md` prefix preservation is not verified by the C1 gate, a candidate or integrator could silently alter lines 1–147 of `PROVINCE.md` (e.g. rewriting line 129 in place, modifying core surfaces, or tampering with handoff boundaries) while still passing `--ownership-corrections`.
     - Standard round-19 `_outbound_publication()` does not check the `proposition` column of table rows (it checks only anchor ID, quote, commit, SHA-256, and heading; `check-adjacency-anchors.py:241-255`). Thus, an in-place rewrite of line 129 would slip past both default and correction modes undetected.

---

## 3. Second-Order Effects Across Surfaces

1. **Runtime Surface:**
   - GitReader in `tools/check-adjacency-anchors.py` already implements memoized committed blob retrieval (`reader.read(revision, path)`). Reading `PROVINCE.md` at the immutable baseline revision `0cbc34dd6b20896085a8fb07943e3ea4027d8472` adds one in-memory dictionary lookup.
   - No additional subprocess or shell is spawned.

2. **Contract Surface:**
   - Enforces the invariant that C1's clarification is strictly additive and non-regressive.
   - Symmetrically closes the class of defects represented by `R20-SKILL-PREFIX-EXCEPTION` across both primary markdown planes (`SKILL.md` and `PROVINCE.md`).

3. **Substrate Surface:**
   - Read-only; zero mutation of host state, pacman packages, systemd units, or `/boot` filesystems.

4. **Verification Surface:**
   - Preserves exact oracle conformance with `.ufo/waves/round-20/preregister.json:31-36`:
     - Baseline commit: `OWNERSHIP_HEADING` absent $\rightarrow$ emits `OWNERSHIP-CORRECTION-MISSING; exit=1` (baseline red preserved).
     - Altered prefix commit: `OWNERSHIP_HEADING` present, but `lines[:start]` modified $\rightarrow$ emits `OWNERSHIP-CORRECTION-INVALID; exit=1`.
     - Clean candidate commit: `OWNERSHIP_HEADING` present, `lines[:start]` intact, `lines[start:end]` valid $\rightarrow$ emits `ownership_corrections=1; exit=0`.

---

## 4. Affected Axes

- **Improves C1 (Adjacency, tied-lowest axis, ordinal 8, delta 0):**
  Provides concrete, machine-checked verification that OUT-009 attribution clarification preserves the entire historical province and round-19 adjacency baseline intact, eliminating the risk of unflagged in-place rewrites.
- **Harms None (C2 Operability & C3 Calibration, ordinal 9, delta 0):**
  - C2 Operability: `check-adjacency-anchors.py` is probed as an additional tool by `check-revision-binding.py` using default mode (`python3 tools/check-adjacency-anchors.py --revision <REV>`). Because prefix preservation is gated behind `--ownership-corrections`, default mode behavior and discovery probes remain completely unaffected.
  - C3 Calibration: Operates strictly on `SKILL.md` registry tables and `boot-chain-audit.sh`; completely orthogonal file surface.

---

## 5. Proposed Move: Grounded Integration Improvement

**One Bounded Move:**  
When L1 integrates `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py` into production, incorporate the missing baseline prefix invariance check into `_ownership_correction()`:

1. **Define the round-20 baseline anchor in `tools/check-adjacency-anchors.py`:**
   ```python
   BASELINE_R20 = "0cbc34dd6b20896085a8fb07943e3ea4027d8472"
   ```

2. **Sequence the check in `_ownership_correction()`:**
   - First, check for `OWNERSHIP_HEADING`:
     ```python
     lines = province_text.splitlines()
     headings = [index for index, line in enumerate(lines) if line == OWNERSHIP_HEADING]
     if not headings:
         return 0, [_finding("OWNERSHIP-CORRECTION-MISSING", "OUT-009",
                             "the exact R20 ownership clarification is absent")]
     if len(headings) != 1:
         return invalid("the R20 ownership clarification heading must be unique")
     ```
     *(This ensures the baseline commit immediately fails with `OWNERSHIP-CORRECTION-MISSING` without evaluating prefix invariance).*
   - Second, verify baseline prefix invariance:
     ```python
     start = headings[0]
     baseline_loaded = reader.read(BASELINE_R20, "PROVINCE.md")
     if baseline_loaded.issue is not None or baseline_loaded.data is None:
         return invalid("baseline PROVINCE.md is unreadable at round-20 baseline")
     baseline_lines = baseline_loaded.data.decode("utf-8", "strict").splitlines()
     if tuple(lines[:start]) != tuple(baseline_lines):
         return invalid("baseline PROVINCE prefix was altered before the clarification section")
     ```
   - Third, verify the exact clarification section lines and arbitration context (`lines[start:end]` and `OWNERSHIP_ARBITRATION_LINES`).

3. **Hermetic Selftest Case:**
   In `selftest()`, add a case mutating a line before `start` (e.g. line 129) and assert that it emits `OWNERSHIP-CORRECTION-INVALID` and `count=0`.

---

## 6. Risks, Contradictions, and Verification

1. **Risk: Breaking Baseline Red Evaluation:**
   - *Risk:* If the baseline prefix check ran before checking `if not headings:`, running against baseline might fail with `OWNERSHIP-CORRECTION-INVALID` rather than `OWNERSHIP-CORRECTION-MISSING`.
   - *Mitigation:* The check is strictly sequenced *after* the `if not headings:` guard. On baseline, the heading is absent; the gate exits early with `OWNERSHIP-CORRECTION-MISSING`, exactly matching preregister expectation.

2. **Risk: Hermetic Selftest Disconnection:**
   - *Risk:* In `selftest()`, the test repo has a private commit history that does not contain commit `0cbc34dd6b20896085a8fb07943e3ea4027d8472`.
   - *Mitigation:* Allow `baseline_revision` to default to `BASELINE_R20` in CLI invocation, but pass the fixture's base revision during selftests (identical to how `check-registry-coverage.py` handles `--baseline-tools` in its fixture suite).

3. **Verification Plan (for L1 Canonical Measurement Wave):**
   - **Check 1 (Baseline Red):**
     `python3 tools/check-adjacency-anchors.py --revision 0cbc34dd6b20896085a8fb07943e3ea4027d8472 --ownership-corrections`
     $\rightarrow$ Exit 1, Finding: `OWNERSHIP-CORRECTION-MISSING`, `ownership_corrections=0`.
   - **Check 2 (Candidate Green):**
     `python3 tools/check-adjacency-anchors.py --revision <CANDIDATE_REV> --ownership-corrections`
     $\rightarrow$ Exit 0, Findings: `[]`, `ownership_corrections=1`.
   - **Check 3 (Tampered Prefix Red):**
     Candidate with line 129 mutated in `PROVINCE.md`
     $\rightarrow$ Exit 1, Finding: `OWNERSHIP-CORRECTION-INVALID`, `ownership_corrections=0`.
   - **Check 4 (Gate Hermetic Selftest):**
     `python3 tools/check-adjacency-anchors.py --selftest`
     $\rightarrow$ Exit 0, `PASS (<N> cases ...)`.
   - **Check 5 (Cross-Tool Continuity):**
     `python3 tools/check-revision-binding.py --tools-revision <CANDIDATE_REV> --object-selectors`
     $\rightarrow$ Exit 0, `object_selector_tools: 9`, `additional_consistent_tools` includes `check-adjacency-anchors.py`.

---

Scope: executed=none
