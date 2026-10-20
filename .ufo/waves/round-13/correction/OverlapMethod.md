# OverlapMethod: Correction Gate Purpose vs Tameshi Province and Verification Registry Boundary

**Seat:** `TsukuroiR13.OverlapMethod` (connector)  
**Round:** tsukuroi round 13 (C1 depth correction)  
**Assigned Report Path:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-13/correction/OverlapMethod.md`  
**Tooling Record:** No packages installed or updated (standard core inspection tools sufficient).

---

## 1. Declared Axes and Frontier Binding

- **Target Axes:** `depth` (primary evaluated axis for round 13 C1 correction) and `adjacency` (tied lowest at 8 in scorecard).
- **Godspeed Invariant:** Synthesize a non-obvious move across round proposals that improves `depth` and `adjacency` without harming `operability`, `coverage`, `freshness`, or `calibration`.
- **Core Distinction:** 
  - `tsukuroi` owns host operability & system repair (mending): package state, systemd, drivers/firmware, boot health, and the rollback-net surface (`PROVINCE.md:3-24`).
  - `tameshi` owns verification-fixture craft: the reusable method of honest checks, hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, and before/after proof (`../tameshi-shokunin/PROVINCE.md:3-18`).

---

## 2. Comparison: Correction Gate Purpose vs Tameshi Province

### A. Purpose of Tsukuroi's Round-13 Correction Gate (`check-root-dac-correction.py`)
1. **Domain-Specific Correctness Falsification:**
   The round-13 correction gate (`CorrectionCheck` seat) exists solely to enforce domain invariants within `tsukuroi`'s rollback-net knowledge base (`root-dac-decision-r12.md/.json` vs `root-dac-correction-r13.md/.json`).
2. **Narrow Structural and Semantic Contract:**
   - Detects and rejects the round-12 false universal (the claim that *only* `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a systemd unit).
   - Validates that active advice cites the complete set of alternative unit-side read-only mechanisms (`BindReadOnlyPaths=`, `TemporaryFileSystem=` with `ro`, `RootDirectory=`, `RootImage=`).
   - Ensures immutable historical r12 records remain byte-preserved with explicit supersession markers rather than rewritten in place.
   - Evaluates exact committed strings/ASTs across active and historical revisions via git object inspection (`--revision REV`).

### B. Tameshi's Fleet Method Province
1. **Reusable Verification Craft:**
   `tameshi` governs general harness design, mutation-testing frameworks (`tools/mutate-and-run.sh`), kill-rate ledger accounting (`corpus/knowledge/fleet-kill-rate-ledger.md`), and cross-lane service engagements (`corpus/knowledge/service-optin-protocol.md`).
2. **Explicit Province Boundary and Refusals:**
   - `tameshi` explicitly *refuses* product domains: *"every lane's gate remains its own; tameshi owns only the reusable craft... Never edits a sibling's gate code"* (`tameshi-shokunin/PROVINCE.md:14-18`).
   - Sibling gates (`kumitate`'s `kimi-census`, `kagi`'s `surface-census`, `tsukuroi`'s `tsukuroi-census.sh`, `mado`'s `mado-verify.sh`) remain strictly owned, maintained, and hardened by their respective home lanes.
3. **Adjacency Contract (ADJ-07):**
   `tsukuroi`'s `PROVINCE.md` (ADJ-07) and `corpus/knowledge/adjacency-handoffs-fleet-r1.json` specify that when a census blind spot raises a reusable verification or mutation-testing question, `tsukuroi retains census implementation, domain contract, repair and lane-local verdict ownership`, requesting method advice only.

---

## 3. Second-Order Contradictions & Risks of Fleet Duplication

1. **Risk of Absorbing Gate Ownership into Fleet Tooling:**
   If `tsukuroi` models `check-root-dac-correction.py` as a general fleet-wide verifier or exports it to `tameshi`, it violates `PROVINCE.md:82` (*"Out of province → report, never absorb"*) and `tameshi`'s refusal of product domain gates.
2. **Risk of Duplicating Tameshi's Mutation Runner:**
   If `tsukuroi` writes its own bespoke mutation framework to test `check-root-dac-correction.py` (e.g., executing arbitrary AST mutators), it creates duplicate, drifting verification methods that bypass tameshi's established single-edit mutant discipline and ledger standards.
3. **Risk of False "Passing Gate = Semantic Truth":**
   As noted in round-12 closure (`round-12-verifier-spotcheck.md:136-162`), a passing structural counter or regex check does not establish factual truth. The verification gate must assert semantic invariants (specific exclusions and required alternatives), not mere field presence.

---

## 4. Recommended Lane-Local Verification Registry Boundary

To cleanly separate lane-local gate mechanics from tameshi's reusable verification craft without duplicating fleet methods, `tsukuroi` must enforce the following three-tier boundary:

| Boundary Tier | Owner | Artifacts & Scope | Interface / Hand-off Contract |
|---|---|---|---|
| **Tier 1: Domain Verification Gate (Lane-Local)** | `tsukuroi` (`CorrectionCheck`, L1) | `tools/check-root-dac-correction.py`, `corpus/knowledge/root-dac-correction-r13.*` | **Strictly lane-internal.** Executable read-only gate with hermetic `--selftest`. Evaluates domain contract: rejects false universal, requires alternative namespace mechanisms, verifies supersession pointers. Exits 0 (PASS), 1 (FAIL), 2 (SETUP/USAGE error). |
| **Tier 2: Mutation Defect Spec (Lane-Local)** | `tsukuroi` (`GateMutationDesign`) | Lane-local single-edit defect table/spec (e.g. in `.ufo/waves/round-13/correction/GateMutationDesign.md` or a knowledge note) | **Tameshi-compatible request shape.** Concrete single-edit semantic mutants (`@old` / `@new` pairs: restore "only", remove "TemporaryFileSystem", claim private namespace absent). Stored as data, not an executable runner. |
| **Tier 3: Reusable Mutation Verification (Fleet Craft)** | `tameshi` (via ADJ-07 opt-in) | `tameshi-shokunin/tools/mutate-and-run.sh`, `fleet-kill-rate-ledger.md` | **Service Opt-In Protocol (`service-optin-protocol.md`).** When `tsukuroi` requests kill-rate certification, it provides: (1) Pinned commit hash, (2) One-command hermetic suite (`python tools/check-root-dac-correction.py --selftest`), (3) Clause-mapped defect spec. `tameshi` replays the mutants against the isolated copy and records the kill rate. |

---

## 5. Proposed Move: Synthesis Across Round Proposals

1. **Isolate the Domain Gate within Tsukuroi:**
   `tools/check-root-dac-correction.py` remains an autonomous, read-only domain tool within `tsukuroi`. It implements `--selftest` and `--revision REV` following the standard firmware-style exit map (0/1/2) established by `tsukuroi-census.sh`.
2. **Formulate Semantic Mutants to Tameshi Specification Standards:**
   The `GateMutationDesign` output should follow `tameshi`'s contract items 1–3 (`service-optin-protocol.md:58-75`):
   - Exactly one unique `@old` string per mutant.
   - Pre-registered expected outcomes (`killed` by semantic failure).
   - Zero execution of mutants by child seats (complying with leaf contract).
3. **Register Boundary in ADJ-07 Ledger:**
   In future adjacency reviews, reference `check-root-dac-correction.py` as an unabsorbed lane gate with an opt-in-ready mutation spec, preserving `tameshi`'s role as the method authority and `tsukuroi`'s role as the domain owner.

---

## 6. Verification and Acceptance

- **Self-Contained Verification:**
  - Verify that `tools/check-root-dac-correction.py` requires no external fleet dependencies outside Python 3 standard library (`argparse`, `subprocess`, `json`, `sys`, `pathlib`).
  - Verify that no sibling files outside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/` were modified.
- **Contract Adherence:**
  - Preserves leaf contract: no tests, benchmarks, or git commits run.
  - Verification left to L1 integrator upon landing.
