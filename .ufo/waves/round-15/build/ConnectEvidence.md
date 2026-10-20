# ConnectEvidence — Round 15 Evidence Chain Analysis & Connector Synthesis

**Seat:** `TsukuroiR15.ConnectEvidence` (connector, leaf member)  
**Baseline:** `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`  
**Contract & Boundaries:** Read-only research; strictly report only; no tests, builds, linters, or gate executions; tools installed/updated: **none**.  
**Judged on:** `depth`

---

## 1. Declared Axes & Delta Accountability

- **Claimed Axes:**
  - **`depth`:** Resolves round 14 verifier documentation debts via stable heading locators (`SANDBOXING > ProtectSystem=`) and positive domain definition (`Takes a boolean argument or the special values "full" or "strict".`). Ordinal remains **8 → 8** (delta 0).
  - **`freshness`:** Re-verifies update-safety state following the 2026-10-20 04:25:16-0300 (07:25:16Z) libinput partial upgrade. Ordinal remains **9 → 9** (delta 0).
- **Unchanged Axes:**
  - `coverage`: 9 (retains existing rollback-net / update-safety substrate; no expansion).
  - `operability`: 9 (census gate preserved; small conformance gate added without claiming broad host capability).
  - `calibration`: 9 (no inflation, no automated health certifications, outside verifier spot-check required).
  - `adjacency`: 8 (no fleet or sibling tree mutation; leaf boundary preserved).

---

## 2. End-to-End Evidence Chain Tracing: Separable C1 and C2 Chains

Tracing the evidence chain reveals that C1 (depth) and C2 (freshness) are strictly **separable claims**:
- **C1 Chain (Source & Docs Clarification):** Reopened upstream documentation (`systemd.exec(5)` S046) -> `LocatorEntry` -> `source-locator-clarification-r15.{md,json}` -> `check-locator-clarification.py` gate -> Scorecard. **C1 does NOT consume the host snapshot.**
- **C2 Chain (Host Incident Recheck):** Host event log (`pacman.log:2429`, 04:25:16-0300 = 07:25:16Z) -> `HostSnapshot` (`host-snapshot.json`) + Sources S047/S048 -> `IncidentEntry` -> `partial-upgrade-recheck-r15.{md,json}` -> `measure-update-recheck.py` counting probe -> Scorecard.

```
[Upstream Source] (S046 systemd.exec.5)            [Host Incident] (pacman.log:2429, 04:25:16-0300 = 07:25:16Z)
       │                                                                  │
       ▼ (LocatorEntry)                                                   ▼ (HostSnapshot only)
[C1 Knowledge Pair]                                                [Host Snapshot JSON]
(source-locator-clarification-r15.{md,json})                       (host-snapshot.json; SHA256: b101f374...)
       │                                                                  │
       ▼ (L1 post-integration)                                            ▼ (IncidentEntry + S047/S048)
[C1 Conformance Gate]                                              [C2 Knowledge Pair]
(tools/check-locator-clarification.py)                             (partial-upgrade-recheck-r15.{md,json})
(Gate standard, exits 0/1/2, --selftest)                                  │
       │                                                                  ▼ (L1 post-integration)
       │                                                           [C2 Counting Probe]
       │                                                           (tools/measure-update-recheck.py)
       │                                                           (Counting probe, exits 0/2, no verdict gate)
       │                                                                  │
       └──────────────────────────────┬───────────────────────────────────┘
                                      ▼
                        [Scorecard & Durable Report]
                  (LOG.md -> SCORECARD.md -> tsukuroi.md)
```

---

## 3. Spotting the Missing Links & Structural Hazards

Static analysis across wave specifications, task assignments, and peer reviews (`ReviewEvidencePins`, `ReviewCounting`, `ReviewIncidentObservation`, `ReviewGateRegistry`, `AttackSnapshotTamper`) exposes **three critical links** in the evidence chain:

### Link 1: Separability of Claims & Snapshot Dependency
- **Hazard:** Conflating C1 with host snapshot data.
- **Trace:** C1 is purely a documentation-debt clarification for ProtectSystem= (addressing renderer-dependent line numbers and negative absence phrasing from round 14). It grounds exclusively in reopened S046. Only C2 consumes `host-snapshot.json`. Keeping C1 free of host-snapshot inputs preserves clean causal separation.

### Link 2: The C2 Digest & Capture Timestamp Schema Linkage
- **Hazard:** `spec.json` (Interfaces for C2 JSON) vs `IncidentMeasure` dispatch contract.
- **Trace:** The base schema definition lacked explicit `snapshot_sha256` and `snapshot_captured_at` fields. If omitted by `IncidentEntry`, `IncidentMeasure` would exit with code 2 (`CANNOT_EVALUATE`).
- **Resolution:** Explicitly require `snapshot_sha256` (bound to raw bytes `b101f374...`) and `snapshot_captured_at` (`2026-10-20T07:44:39Z`) in `partial-upgrade-recheck-r15.json`, matching peer coordination.

### Link 3: Decoupling Probe Absence & Observations from Operational Health
- **Hazard:** Treating probe absence (exit 0) or symbol consistency as a clean bill of health.
- **Trace:** `IncidentMeasure` exits 0 with `count0` on baseline/absence. Concurrently, `libinput 1.32.0-1` having matching soname (`libinput.so.10`) does not imply running system health (the compositor retains the unlinked 1.31.3 inode in memory, and 413 packages remain pending against the stale 2026-10-18 sync DB).
- **Resolution:** `measure-update-recheck.py` must distinguish status (`ABSENT` vs `PRESENT_VERIFIED`), hardcode `health: "not_assessed"`, and preserve `decision: "BLOCKED_FOR_AGENT_PACKAGE_ACTION"` due to the mkinitcpio 42 `/sysroot` boot-chain hook coupling.

---

## 4. Distinguishing Author Gates from Outside Verifier Gates

Under `PROTOCOL.md:375-415` (Gate Standard) and round 14 verifier spot-check precedents (`corpus/lessons/round-14-verifier-spotcheck.md:65-158`), author-side enforcement and outside verifier validation are fundamentally distinct tiers:

| Dimension | Author-Side Domain Gate (`tsukuroi`) | Outside Independent Verifier (`hyaku closure` / verifier seats) |
|---|---|---|
| **Identity & Scope** | Lane-internal tools (`check-locator-clarification.py`, `tsukuroi-census.sh`). Bound strictly to repo files and committed git blobs. | Non-author integrator / external review seats (`CloseTsukuroiR14`, `CloseMadoR15`). Crosses outside boundaries. |
| **Capability** | Bounded structural, syntactic, and token conformance (e.g. 11-word quote match, notice presence, exit code 0/1/2). | Independent source reopening, manual man-page reading, network API validation, census script execution. |
| **Semantic Proof** | **Cannot prove source truth.** Docstrings must explicitly state: *"Not a semantic proof; narrow conformance only."* | Verifies semantic truth and quote proposition alignment directly against live/pinned upstream endpoints. |
| **Host Probes** | Hermetic `--selftest` using in-memory string literals. Probing live host state is restricted to explicit read-only research snapshots. | Performs step-1 conformance audits, git commit ancestry checks, working-tree dirty sweeps, and external gate verification. |
| **Verification Rule** | Subagents **never** execute gates; L1 executes once after integration. Author gate results are committed as frozen JSON evidence. | Outside verifier verifies committed evidence artifacts (`verification.json`) and evaluates hashes without rerun storms. |

---

## 5. Non-Obvious Move & Synthesis Proposal

**Proposed Move:**  
*Formally establish a dual-discipline verification contract that decouples lexical/structural conformance from semantic source authority in C1, and decouples point-in-time observation from system health in C2.*

1. **In C1 (Depth):**
   - The gate (`check-locator-clarification.py`) reports `conforming_correction_count: 2` based strictly on structural invariants (heading `SANDBOXING > ProtectSystem=`, footer `systemd 262.1`, exact 11-word quote, and r14 supersession notices).
   - Semantic authority rests on dated source witness evidence (`C1SourceWitness.json` / `SOURCES.md:S046`), leaving semantic agreement to outside verifier spot-checking.
2. **In C2 (Freshness):**
   - The measurement tool (`measure-update-recheck.py`) acts strictly as a **counting probe**, never a gate.
   - It hashes raw snapshot bytes (`snapshot_sha256 = b101f374...`), verifies probe exit codes (`exit == 0`), records `pending_count = 413` against the 2026-10-18 sync DB metadata, and emits `health: "not_assessed"`.
   - The decision field is permanently bound to `BLOCKED_FOR_AGENT_PACKAGE_ACTION` due to the uncrossed mkinitcpio 42 `/sysroot` boot-chain hook coupling.

### Second-Order Effects & Trade-Offs
- **Substrate Safety:** Zero risk of package transactions, hook breakage, or unauthorized upgrades during autonomous runs.
- **Verifiability:** Outside verifiers can independently recalculate hashes and confirm findings without ambiguity.
- **Contract Integrity:** Eliminates the vulnerability of declaring clean health from an empty query or a structurally passing checker.

---

## 6. Exact Sources, Limits, and Verification Boundaries

- **Sources Examined (Read-Only):**
  - `AGENTS.md`, `PROTOCOL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`.
  - `corpus/lessons/round-14-verifier-spotcheck.md`.
  - `.ufo/waves/round-15/build/` artifacts: `spec.json`, `dispatch.json`, `assignments.json`, `host-snapshot.json`, `HostSnapshot.md`, `ReviewEvidencePins.md`, `ReviewCounting.md`, `ReviewIncidentObservation.md`, `ReviewGateRegistry.md`, `ReverseGatePattern.md`, `BootCoupling.md`, `IncidentTimeline.md`, `RuntimeMapping.md`, `SafetySourceInjection.md`, `PacmanPrint.md`, `ConnectFrontier.md`.
- **Limits:** Read-only research analysis; no external network requests made; no subagent dispatch; no live host commands or probes executed; no test suites, gates, or selftests run.
- **Tools Installed / Updated:** **None**. Passwordless sudo was not invoked. Zero package or service modifications.
