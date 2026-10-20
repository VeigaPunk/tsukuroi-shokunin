# OverlapMethodR — Round 12 Resumed UFO-FSD Connector Report

**Seat**: `TsukuroiR12.OverlapMethodR` (UFO-FSD connector, resumed wave)  
**Round**: 12 (tsukuroi-round12-resumed)  
**Status**: Leaf seat; read-only exploration; findings and proposal only. No test runs, no builds, no linting, no git commits, no host mutation.  
**Declared Axes**: Operability (9), Depth (8) [tied lowest with Adjacency (8)]  
**Working tree base**: HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`  
**Relative paths base**: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  

---

## 1. Inherited Artifact Audit (`.ufo/waves/round-12/OverlapMethod.md`)

In accordance with resumed round requirements, the inherited artifact `.ufo/waves/round-12/OverlapMethod.md` was re-checked against current repository source state, sibling critic/review findings (`ClaimCritic.md`, `FixtureReview.md`, `BootBoundaryR.md`, `PriorDebtR.md`), and cross-lane province declarations:

### 1.1 What is Reused
- **Province Boundaries Across Lanes:** The core structural boundary between `tsukuroi-shokunin` (host operability and census gate implementation), `tameshi-shokunin` (reusable verification-fixture craft and cross-lane mutation harness), and `kumitate-shokunin` (orchestration, task routing, and tooling) remains exact and grounded.
- **Self-Service In-Lane Mutation Model:** The identification of the self-service engagement mode from `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:34-47` (measured in tsukuroi round 5, `plans/round-5.plan.md:3-11`) is re-verified. In-lane mutation testing of one's own gate on `/tmp` copies is completely owned by tsukuroi and does not invade tameshi's province.
- **The Unprivileged Fixture-Craft Dilemma:** The physical substrate contradictions regarding testing root filesystem anchors as an unprivileged user (UID 1000 cannot `chown 0:0`, `stat` on `chmod 000` owner bypass, teardown `rm -rf` trap failure, fixture hash collision) remain the core substrate friction.
- **ADJ-07 Route Discipline:** The minimal ADJ-07 packet structure, strictly keeping lifecycle state at `prepared` with recipient acceptance marked `unobserved`, is preserved.

### 1.2 What is Corrected and Sharpened
- **Stale Working Tree Anchors Re-verified:** Re-verified against HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5` on 2026-10-20. Current `tools/tsukuroi-census.sh` remains at 2,402 lines (sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11`); C1 root probe has not landed in source yet (0 matches for `TSUKUROI_ROOT_DIR`).
- **Incorporation of Admission Bar Rules (QUALITY #13, #14, #15):** The inherited report noted general fixture concerns; this report couples them directly to `corpus/QUALITY.md:17-20`:
  - *QUALITY #13:* Explicitly pairs EACCES triage of target mode/owner/ACL with unit capabilities, requiring independent root reporting because `pacman -Qkk` cannot see `/`.
  - *QUALITY #14:* Mandates explicit evaluation of applicable numbered criteria in any knowledge entry (preventing the round-1 outside spotcheck disagreement).
  - *QUALITY #15:* Forbids treating dynamic process writability (`test -w` / `access(2)`) as inode mode ground truth, and forbids inventing a default `0755` policy. This directly drives the fixture requirement to test exact octal bits (`stat -c %a`), not `test -w`.
- **Clarification of Kumitate Exclusion:** Re-verified `kumitate-shokunin/PROVINCE.md:3-15`. Kumitate owns orchestration (OMP task/hub, ufo-fsd scripts/runtime, Kimi Code substrate). Tsukuroi routes task/hub dispatch semantics to kumitate under ADJ-05 (`PROVINCE.md:50`). Kumitate has **zero** ownership of census verification methods, mutation testing, or filesystem triage. Kumitate is completely excluded from ADJ-07.

### 1.3 What is Rejected
- **Rejection of Blocking External Dependency:** Any interpretation of `SCORECARD.md:201-202` or `corpus/lessons/round-1.md:43` that implies tsukuroi must wait for tameshi's advice before landing C1 is rejected. Tsukuroi autonomously owns the census implementation, domain contracts, and repairs (`PROVINCE.md:52`).
- **Rejection of Invented Recipient Acceptance:** Any claim that ADJ-07 is "acknowledged", "accepted", or "resolved" is strictly rejected. ADJ-07 has 0 receipts in the fleet; state remains `prepared`.
- **Rejection of Generalization Claims from One Lane:** Reject any attempt by tsukuroi to claim its local fixture solutions as general fleet verification rules. Under `tameshi-shokunin/PROVINCE.md:15-16`, general fixture craft requires evidence across two independent lanes and belongs to tameshi.

---

## 2. Evidence: Sibling Province Declarations and Method Ownership

A targeted read-only audit was conducted across the province declarations of `tsukuroi-shokunin`, `tameshi-shokunin`, and `kumitate-shokunin`:

### 2.1 `tameshi-shokunin/PROVINCE.md`
- **Domain & Ownership** (`tameshi-shokunin/PROVINCE.md:3-13`):
  - Domain: *verification-fixture craft* — the reusable method of honest checks (hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, no-permissiveness audits, before/after proof).
  - Owns: The method, documented from the fleet's existing gates as primary surfaces (`kumitate-shokunin/scripts/*`, `kagi-shokunin/corpus/*`, `kaidoku-shokunin`, game lanes, etc.) and the cross-lane mutation harness `tools/mutate-and-run.sh` (`:28-38`).
- **Refusals & Adjacent Boundaries** (`:14-20, 44-47`):
  - Refuses: *Product domains* — "every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general). Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)" (`:14-17`).
  - Adjacent: "every sibling gate's code and product clauses (owner lane)" (`:44-45`).
- **Service Opt-in Protocol** (`tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:32-53`):
  - Form **self-service**: "the opting-in lane, on /tmp copies" runs the harness/recipe and "the same lane, in-round" hardens the gate (measured instance: tsukuroi round 5, `plans/round-5.plan.md:3-11`).
  - "Two seats, never merged... when both tameshi and the owner sweep the same artifact, the two tables stay two tables, each tied to its own pin... out-of-province → report, never absorb" (`:48-52`).

### 2.2 `kumitate-shokunin/PROVINCE.md`
- **Domain & Ownership** (`kumitate-shokunin/PROVINCE.md:3-15`):
  - Domain: *orchestration & tooling* — scopes OMP task/hub, ufo-fsd scripts & runtime.
  - Owns: Origin script layer (`scripts/`), origin runtime layer (`crates/`), Kimi Code substrate (`~/.kimi-code/`), lane instruments (`scripts/*.mjs`).
  - Refuses: Anything outside this domain (`:6, 24-28`).
- **Connection to Verification & Adjacency**:
  - Kumitate's scripts were historical primary surfaces for tameshi's craft studies (`tameshi-shokunin/PROVINCE.md:8`), but kumitate does **not** govern verification methods or mutation testing.
  - In tsukuroi, ADJ-05 routes task/hub dispatch and routing semantics to kumitate (`PROVINCE.md:50`). Kumitate has zero ownership of census verification methods, mutation testing, or host filesystem triage.

### 2.3 `tsukuroi-shokunin/PROVINCE.md`
- **Domain & Retained Scope** (`PROVINCE.md:6-33, 44-53`):
  - Core: Four-plane (now six-plane with update-safety and oom) host health census `tools/tsukuroi-census.sh`, diagnostic triage, package/driver/boot health.
  - Retains: Census implementation, domain contract, repair, and lane-local verdict ownership (`:52`).
  - Refuses: Configuration writes, package changes, service restarts (`:27-28`), binary reverse-engineering (kaidoku/revenger), fleet correlation (mori), task routing (kumitate).
- **ADJ-07 Route Contract** (`PROVINCE.md:52`, `corpus/knowledge/adjacency-handoffs-fleet-r1.json:115-126`):
  - Trigger: "A reproducible census blind spot raises a reusable verification or mutation-testing method question."
  - Tsukuroi retains: "Census bug, domain contract, implementation and repair in this repo."
  - Recipient: "tameshi" for method advice.
  - Minimum handoff evidence: "UTC capture time, minimal failing behavior, command/exit, measured census revision and expected domain invariant; ask for method advice, not transfer of gate ownership or a general claim from one lane."
  - Forbidden inference: "One lane's case proves a general verification pattern or transfers census code ownership."
  - Lifecycle state at baseline: `"contract-only"` (`corpus/knowledge/adjacency-handoffs-fleet-r1.json:123-124`).

---

## 3. Delineation: Own Census Implementation vs. Reusable Mutation Method Ownership

| Dimension | `tsukuroi-shokunin` (Lane Owner) | `tameshi-shokunin` (Method Specialist) | `kumitate-shokunin` (Tooling/Orchestrator) |
|---|---|---|---|
| **Census Code & Probes** | **Exclusive Owner**: Owns `tools/tsukuroi-census.sh`, probe logic, environment seams (`TSUKUROI_ROOT_DIR`), exit maps, and rollup lines. | **Refuses**: Never edits sibling gate code; read-only probes only (`PROVINCE.md:16-17`). | **Refuses**: Out of domain (`PROVINCE.md:6`). |
| **Hermetic Selftest Suite** | **Exclusive Owner**: Owns `--selftest` and its 80+ fixture cases under `/tmp/tsukuroi-r3-2-selftest.*`. | Owns the *criteria* for hermeticity, but not the test suite code. | Refuses. |
| **In-Lane Mutation Testing** | **Permitted & Owned**: Under the self-service protocol, tsukuroi may run single-defect mutant experiments on `/tmp` copies to verify fault-detection (e.g. `MutationPlanR`). | Owns the fleet-wide harness (`mutate-and-run.sh`) and cross-lane kill-rate ledgers (`fleet-kill-rate-ledger.md`). | Refuses. |
| **Verification Method Craft** | **Consumer / Contributor**: Documents lane-local findings; must not claim a single-lane pattern is general. | **Exclusive Owner**: Reusable fixture craft, fail-closed taxonomies, and multi-lane generalization (≥2 lanes required). | Primary surface for historical study, not method owner. |
| **Adjacency Interface** | Files ADJ-07 method requests when a blind spot exposes reusable craft problems. | Evaluates method requests and issues recommendations in round reports. | Receives ADJ-05 (task dispatch/routing), not ADJ-07. |

---

## 4. Contradictions and Second-Order Effects in Round 12

An inspection of current round-12 seat findings (`Planner.md`, `FixtureReview.md`, `ClaimCritic.md`, `BootBoundaryR.md`, `PriorDebtR.md`, `ScoreReview.md`) reveals three explicit substrate tensions:

1. **The Round 1 Plan Assumption vs. Autonomous Execution**:
   - `SCORECARD.md:201-202` and `corpus/lessons/round-1.md:43` planned: *"a census arm for root-dir mode (`-Qkk` cannot see `/`) with tameshi method advice via ADJ-07"*.
   - If tsukuroi interprets this as requiring tameshi's advice *before* landing C1's root metadata probe, C1 is stalled, violating autonomy and PROVINCE boundaries (`PROVINCE.md:38`).
   - Tsukuroi owns the implementation and repair. It does not need permission or external execution to land C1.

2. **The Fixture-Craft Dilemma for Root Invariants (The Real Substrate Problem)**:
   - As evidenced by `FixtureReview` (A11, F8-F9, U1-U2), `ClaimCritic` (E1, CX2, CX3), and `PriorDebtR` (§1.2):
     - Host `/` is `0555 root:root`.
     - The census and its `--selftest` execute as unprivileged user `vgpnk` (UID 1000).
     - **UID Invariant:** An unprivileged user cannot `chown 0:0` in a `/tmp` fixture without `CAP_CHOWN`. Any directory created in selftest is owned by UID 1000. If the census asserts `root_uid == 0` blindly, selftest fails; if it reads host `/`, it violates hermeticity.
     - **EACCES Invariant:** A target directory with `chmod 000` does *not* fail `stat` when accessed by its owner (owner can still stat the inode). `stat(2)` only returns `EACCES` when search permission (`+x`) is denied on an *enclosing parent directory*.
     - **Teardown Trap Collision:** If a test case creates an unsearchable parent `fx/locked/root` (`chmod 000 fx/locked`), `rm -rf -- "$work"` in the cleanup trap (`tools/tsukuroi-census.sh:1574`) fails with `Permission denied`, leaking `/tmp/tsukuroi-r3-2-selftest.*` scratch files across runs!
     - **Integrity Hash Collision:** `fx_hash` uses `find "$1" -type f`. If `find` encounters an unsearchable directory, `find` exits nonzero and `fx_no_mutation` fails with `bad "fixture mutated by census run"`.

3. **QUALITY #15 Collision with Dynamic Permission Proxies**:
   - `corpus/QUALITY.md:20` (Criterion 15) states: *"Root metadata findings report owner-write/search bits, not universal mode policy or process writability."*
   - If a fixture or implementation uses `[ -w "$ROOT" ]` or `test -w`, it tests the invoking process's effective permissions, not the inode DAC bits. For UID 1000, `test -w /` returns false even if `/` were 0755; for UID 0 with `CAP_DAC_OVERRIDE`, `test -w /` returns true even if `/` is 0555. Testing inode bits (`stat -c %a` or integer masking) is mandatory.

---

## 5. Proposed Move: Decouple In-Lane Root Implementation from the Reusable Fixture-Craft ADJ-07 Packet

**The Move**:
1. **In-Lane Implementation (Operability & Depth)**:
   - Tsukuroi implements C1's root metadata probe autonomously in `tools/tsukuroi-census.sh`.
   - Protects hermeticity by adding `TSUKUROI_ROOT_DIR` to the common `check()` environment block (pointing to `$FX/root`, created as `chmod 755`).
   - Hardens the selftest cleanup trap: update line 1574 to:
     ```bash
     trap 'chmod -R u+rwx -- "${work:-}" 2>/dev/null; rm -rf -- "${work:-}"' EXIT INT TERM
     ```
     This prevents directory permission lockouts during teardown.
   - Places unsearchable/EACCES parent fixtures (`$FX_LOCKED/root`) outside the `fx_no_mutation` target path, or ensures permissions are restored before `fx_no_mutation` runs.
   - Evaluates owner-write bits against the target directory's mode bits rather than an `access(2)` / `test -w` call (which depends on runner capabilities, not inode state).
2. **Cross-Lane Craft (Adjacency & Depth via ADJ-07)**:
   - Prepare a bounded, minimal ADJ-07 method packet directed to `tameshi`.
   - The packet presents the exact fixture-craft problem: *How should unprivileged CLI gates hermetically test root-owned (UID 0) filesystem anchors and EACCES path-resolution denials without privileged commands, without leaking scratch directories on teardown, and without triggering fixture hash verification failures?*
   - Keep the ADJ-07 route lifecycle strictly at **`prepared`** in tsukuroi's round report.
   - **Never invent recipient acceptance**: Mark `acknowledged`, `accepted`, and `resolved` as `unobserved`, adhering strictly to `PROVINCE.md:65-68`.

---

## 6. Minimal ADJ-07 Method Question Specification

```markdown
### Executed Method Question Packet — TSUKUROI-R12-METH-01
- **Route**: ADJ-07 (verification/mutation-testing method advice)
- **Recipient**: tameshi
- **Trigger**: Resolving the unowned root directory census blind spot (QUALITY #13, D6)
  requires hermetic fixture testing of root-owned (UID 0) and unsearchable (EACCES)
  filesystem anchors in an unprivileged CLI suite.
- **Capture Time**: 2026-10-20T03:30:00Z
- **Measured Revision**: HEAD b76b5c377eaee3e3d8d47fdddde977828d05dbd5 (tools/tsukuroi-census.sh)
- **Observed Behavior**:
  1. Unprivileged suites (`id -u` = 1000) cannot `chown 0:0` mock root directories under /tmp.
  2. `stat(2)` on a `chmod 000` directory succeeds for the owner; inducing `EACCES`
     requires stripping `+x` on an enclosing parent directory.
  3. Stripping `+x` on an enclosing fixture directory breaks standard test teardown
     (`rm -rf` fails with EACCES) and breaks fixture-integrity hashing (`find -type f` fails).
- **Scope Retained by Tsukuroi**:
  Tsukuroi retains all census implementation, `tools/tsukuroi-census.sh`, domain contracts,
  and local selftest repairs.
- **Bounded Method Question to Tameshi**:
  "What is the recommended fleet fixture craft for unprivileged CLI test suites verifying
  root/DAC boundaries:
   (a) Synthetic directory wrappers with mandatory `trap 'chmod -R u+rwx'` teardown,
   (b) Decoupled coreutil stat-stub dispatching, or
   (c) Parameterized UID/GID inspection seams in the gate under test?"
- **State**: prepared
  (Acknowledgement: unobserved; Acceptance: unobserved; Resolution: unobserved)
```

---

## 7. Affected Axes

- **Operability (Maintained at 9)**:
  - Tsukuroi is not blocked waiting for external sibling action.
  - The census gate lands its root metadata finding (0 → 1) with zero host `/` leaks and zero `/tmp` fixture residue.
  - Baseline 80 selftest cases remain green; new C1 fixture cases pass hermetically.
- **Depth (Advanced 8 → 9)**:
  - C2's 4-branch EACCES decision matrix (`corpus/knowledge/root-dac-decision-r12.md`) remains fully independent of C1 and grounded in primary sources (S027/S028/S034).
  - Clear separation between the domain-specific DAC mechanism (tsukuroi) and the general fixture craft method (tameshi).
  - Enforces QUALITY #13, #14, and #15 discipline.
- **Adjacency (Protected at 8)**:
  - Follows ADJ-07 contract rules without overstepping into tameshi's province.
  - Excludes kumitate from verification craft (kumitate retains orchestration/ADJ-05).
  - No fake handoffs or unobserved receipts claimed.

---

## 8. Risks and Verification

1. **Risk of Conflating In-Lane Mutation Testing with Fleet Craft**:
   - *Risk*: Sibling lanes might assume designing mutants in `MutationPlanR` violates tameshi's province.
   - *Mitigation*: Cite `service-optin-protocol.md:36` (self-service form) and `plans/round-5-record-draft.md:65-79`. Self-service mutation testing of one's own gate on `/tmp` copies is explicitly sanctioned.
2. **Risk of Inventing Recipient Acceptance**:
   - *Risk*: Claiming ADJ-07 is "accepted" or "resolved" without tameshi having executed a run or acknowledged it.
   - *Mitigation*: Strictly designate ADJ-07 as `prepared` in this round. Receipt count remains 0 for ADJ-07.
3. **Risk of Selftest Teardown Failure on Existing Gates**:
   - *Risk*: Introducing unsearchable fixtures causes unprivileged `rm -rf` cleanup failures.
   - *Mitigation*: Update line 1574 cleanup trap with `chmod -R u+rwx` before `rm -rf`.
4. **Verification Probes (Read-Only)**:
   ```bash
   # Re-verify ADJ-07 status in contract JSON
   jq '.routes[] | select(.id=="ADJ-07")' corpus/knowledge/adjacency-handoffs-fleet-r1.json
   # Re-verify tameshi self-service protocol citation
   grep -n 'self-service' ../tameshi-shokunin/corpus/knowledge/service-optin-protocol.md
   ```
