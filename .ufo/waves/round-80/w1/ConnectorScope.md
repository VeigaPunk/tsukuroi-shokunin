# Seat ConnectorScope — Binding Report (Round 80, Wave w1)

Execution class: **NO-EXEC**  
Status: **COMPLETE**  
Round: **Tsukuroi round 80, wave w1**  
Base commit: `467a9b7891a5939dab8460ec6f591fbb16bd82e9`  
Frozen commit: `61ec89ec6e6f284b6fba2127721359e6931a5789`  
Axes: **depth**, **operability**

---

## 1. Declared Axes
1. **Depth (8)**: Sourced worked-example documentation depth on the systemd service restart plane (Claim C1: 42 pinned matrix cells across 6 failure causes × 7 restart settings, derived from systemd v262 `man/systemd.service.xml`, digest-bound to independent review and explanatory companion).
2. **Operability (9)**: Truthful interfaces, standard gate shape, and byte-bound hermetic execution receipts (Claim C2: two tools `count-kr-rows-r69.py` and `check-transaction-order-r39.py` repaired to expose hermetic `--selftest`, exit code 3 on selftest failure, with byte-bound execution receipts).

---

## 2. Cross-Axis & Sibling Boundary Scan (PROVINCE vs Round 80 Claim Spec)
A full boundary scan across `PROVINCE.md` and the Round 80 claim specification confirms that Round 80 work remains strictly within Tsukuroi's owned OS substrate and tool operability domains:

- **kama (ADJ-01 / OUT-002)**: Model serving health vs driver/device state. Tsukuroi retains driver, device, and unit health; model serving endpoints remain kama's. Untouched.
- **kagi (ADJ-02 / OUT-003)**: Secrets & vault operations. Tsukuroi retains package and filesystem mode evidence; no credential reads or helper execution. Untouched.
- **mado (ADJ-03 / OUT-004)**: Desktop UI/compositor environment. Tsukuroi retains user manager units; UI configuration files and runtime behavior remain mado's. Untouched.
- **mori (ADJ-04 / OUT-005)**: Memory pressure, OOM event clusters, and fleet wave attribution. While C1 documents the systemd documentation cause `"Termination due to OOM"` for `Restart=`, and ExecHost reports live `Restart=always` for `systemd-journald.service`, Tsukuroi diagnoses only OS unit state and documented policy. Correlating OOM kills across fleet waves remains strictly mori's. Untouched.
- **kumitate (ADJ-05 / OUT-006, OUT-007)**: Tooling, task dispatch, and orchestration. Tsukuroi diagnoses host service units; dispatch semantics and queue routing remain kumitate's. Untouched.
- **tameshi (ADJ-07 / OUT-010)**: Reusable verification and mutation testing method. Tsukuroi runs internal test gates and seat controls; verification methodology ownership remains tameshi's. Untouched.

---

## 3. Untouched ADJ-06 / OUT-009 Arbitration
- **Boundary rule**: `PROVINCE.md:51, 79-80, 128-129, 148-152, 314-315` and R20 clarification (`R20-OUT009`).
- **Status in Round 80**: **Completely Untouched**.
- **Arbitration record**: Kaidoku (`OUT-008`) and Revenger (`OUT-009`) both declare shipped-artifact reverse engineering. As established in `PROVINCE.md`, Tsukuroi neither absorbs reverse engineering nor decides between Kaidoku and Revenger. OUT-009 is an attributed sibling declaration, not a grant of ownership. Neither claim in Round 80 involves binary reverse engineering, driver internals inspection, or binary artifact unpacking. Arbitration remains exclusively the protocol integrator's call.

---

## 4. Analysis of Latest considerthese Proposals (`considerthese/2026-10-26.md`)
The five proposals in `considerthese/2026-10-26.md` were evaluated against the round 80 work:

1. **Seat-harm incident log**:
   - *Status*: **Covered / Already Implemented**.
   - *Evidence*: Formally adopted in Round 79 as a QUALITY criterion requiring a per-round `## Seat harm` tally in `SCORECARD.md` (`SCORECARD.md:6665-6668`).
2. **Burst-aware reading**:
   - *Status*: **Unimplemented**.
   - *Evaluation*: Applies to reflection and multi-round curation cadence; not directly applicable to C1/C2 claim instruments.
3. **Counter-attack scoreboard**:
   - *Status*: **Unimplemented**.
   - *Evaluation*: Tracks attack arms, survivors, and failure classes (leak read, fixture literal, answer-key read, presence-based shape) across rounds. Informally described in prose in Round 79 outcome, but no structured instrument or scoreboard exists.
4. **Downstream patch-offset check**:
   - *Status*: **Unimplemented (Matching Current C1 Work)**.
   - *Evaluation*: Proposes flagging when knowledge anchors cite upstream line numbers for code that the host runs as a patched Arch build. In Round 80 C1, `systemd.service.xml` is explicitly pinned from upstream v262 XML, while the live host runs `systemd 262.1-1-arch`. Both Round 79 and Round 80 declarations contain explicit caveats ("These are upstream man-page lines, not installed Arch build lines"; "The matrix is documentation, not installed-build/live-restart behavior... Snapshot line numbers identify the v262 source reading only."). This proposal directly addresses this recurring tension between upstream documentation and downstream packaging.
5. **Cross-note correction propagation map**:
   - *Status*: **Unimplemented (Matching Current C2 Work)**.
   - *Evaluation*: Proposes mapping dependencies between propositions and knowledge notes/SKILL sections when corrections occur. In Round 80 C2, `check-transaction-order-r39.py` is repaired, which verifies the TO1–TO8 transaction order rules that originally had to be manually propagated to 7 older notes and 3 SKILL sections.

---

## 5. S330 Collision Analysis: Lane Registry vs Read-Only shokuknow Staged Package
- **Lane Registry (`corpus/SOURCES.md`)**:
  - Contains exactly 329 data rows (S001–S329) at `master`.
  - Next planned row: **S330**, systemd v262 `man/systemd.service.xml`, tier `A/docs/mined`, scoped strictly to `Restart=` table and conditions.
  - Prior lane citations of `systemd.service.xml`: S070 cited `systemd.service(5) ExecStopPost` at v262.1, scoped strictly to `OPTIONS ExecStopPost=`. Planned S330 scopes strictly to `Restart=` at v262, adhering to Tsukuroi's single-scope documentation rule.
- **shokuknow Staged Package (`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`)**:
  - Staged row S330 cites `lanes/tsukuroi/round14/captures/mirror-language-list-capture.txt` (own-work capture of mirror changelog path).
  - Staged package contains **zero** citations of `systemd.service.xml` or systemd service restart documentation.
- **Collision Verdict**:
  - **Document Collision**: **None**. The documents cited by Tsukuroi's planned S330 and the staged package S330 are completely distinct.
  - **ID Collision**: **Hard Collision on Unadopted Package**. If assimilation were attempted, staged S200–S346 collides with Tsukuroi's authoritative S200–S330.
  - **Contract Compliance**: Assimilation is held ("Assimilation none; no package rows adopted"). Tsukuroi does **not** adopt the staged package, does **not** arithmetically renumber its authoritative registry, and performs **no** writes to external repositories. S330 correctly advances as the next local sequential row.

---

## 6. Frozen Expected, Counter, and R79 Routed Items: Durable Binding & Coupling Scan
- **Durable-File Binding avoids R79 Defect**:
  - In Round 79, C1 failed due to two distinct causes: (1) a semantic divergence in DP6 between source continuation text and expected answer; and (2) counter coupling to `w1-results.json`, which suffered null outputs from an orchestrator kernel restart.
  - In Round 80, `tools/measure-round80.py` completely bypasses `w1-results.json` and seat stdout dumps. It binds exclusively to **durable files** committed to the repository tree:
    - C1 binds to `.ufo/waves/round-80/w1/ReviewMatrix/verdict.json` (requiring exact `artifact_sha256` and `companion_sha256`).
    - C2 binds to `.ufo/waves/round-80/w1/count-kr-rows-r69.py.receipt.json` and `.ufo/waves/round-80/w1/check-transaction-order-r39.py.receipt.json`.
- **Causal Coupling Flagged**:
  - *C1 Digest Lock*: `ReviewMatrix/verdict.json` requires the exact SHA-256 of `corpus/knowledge/service-restart-matrix-r80.json` and `corpus/knowledge/service-restart-matrix-r80.md`. If `ScribeMatrix` edits either file after `ReviewMatrix` computes its digest, the counter aborts with finding `review-binding` (exit 1). ReviewMatrix must only bind to final, frozen drafts.
  - *C2 Tool SHA Lock*: Each `.receipt.json` embeds `tool_sha256`. If `ExecKR` or `ExecTransaction` modifies the tool source (even formatting or comments) after running `--selftest` and producing the receipt, `measure-round80.py` fails with `gate-standard` (exit 1).
- **Scope Bleed Flagged**:
  - *Host vs Documentation*: ExecHost observed live host units (`systemd-journald.service` with `Restart=always`, `dbus-broker.service` with `Restart=no`) and identified that rate limits (`StartLimitBurst=5 / 10s`) and `RestartUSec` govern effective behavior. C1 must strictly preserve its boundary as upstream v262 XML documentation, never claiming to predict live restart or recovery without taking overrides and rate limits into account.
  - *Registry Section Bleed*: `measure-round80.py` strictly parses `SKILL.md` under `## Gate and probe registry — round71 superseding current rows`. Sibling edits to other headings or structural reformatting in `SKILL.md` could break the string split logic in `measure-round80.py:50`.

---

## 7. The One Non-Obvious Move (UFO-FSD Connector Synthesis)

### Evidence
1. `tools/measure-round80.py` lines 41–43 enforces C1 via byte-exact answer-key equality against `before/expected.json` plus reviewer digest binding. `SCORECARD.md:6750-6752` admits that finite equality shadows semantic entailment: a synthetically identical review bundle passes even if semantic conditions (clean exit vs unclean signal, manual stops, oneshot behavior) are misunderstood.
2. In C2, `tools/measure-round80.py` lines 58–62 verifies tool conformance via static inspection of `.receipt.json` and token matching (`--selftest`, `SELFTEST`), but does not dynamically re-execute the tool's selftest during counter evaluation. ReviewRegistry in R79 noted this "presence-based shape leg" vulnerability.
3. Upstream seats (`ScribeMatrix`, `ExecKR`, `ExecTransaction`) produce artifacts whose SHA-256 digests are required by downstream binding seats (`ReviewMatrix`, receipt records).

### Contradictions Stated Explicitly
- **Answer-Key Rigidity vs Semantic Scope**: Requiring 100% literal JSON match to `expected.json` guarantees numeric passage, but conceals documentation omissions (as shown by R79's DP6 failure). The companion markdown must carry the real conditional semantics that cannot fit into a boolean matrix cell.
- **Static Receipt Verification vs Active Gate Conformance**: C2 verifies that an execution receipt *exists* and asserts `rc=0`, but the counter itself avoids running the tool to maintain execution hermeticity.

### Affected Axes
- **depth**: Strengthens C1 semantic depth by explicitly validating the explanatory companion against the conditional boundaries identified by ExecHost and ScoutSource.
- **operability**: Strengthens C2 operability by ensuring that tool selftests can be independently executed and validated from durable receipts without creating race conditions or stale-digest traps.

### Proposed Move
**Pre-Flight Digest-Lock Staging Protocol (Two-Phase In-Wave Durable Handoff)**:
1. **Phase 1 (Artifact Freeze & Verification)**: Upstream author seats (`ScribeMatrix`, `ExecKR`, `ExecTransaction`) write candidate artifacts into their seat directories and publish an authoritative SHA-256 checksum file alongside them.
2. **Phase 2 (Atomic Binding & Receipt Generation)**:
   - `ReviewMatrix` reads the published checksum from `ScribeMatrix`, validates that the companion explicitly addresses the 4 documented override conditions (oneshot services, manual `systemctl stop`, `RestartPreventExitStatus`/`RestartForceExitStatus`, and rate limits), and writes `verdict.json` using the verified SHA.
   - `ExecKR` and `ExecTransaction` generate their `.receipt.json` directly from the exact file to be placed into `tools/`, asserting `tool_sha256` matching `sha256sum tools/<tool>` in a single atomic step.

### Risks
- Minor sequential dependency: Reviewer must wait for Scribe's final freeze before writing `verdict.json`.
- Mitigated because wave w1 is small (10 seats) and seats can draft contents while awaiting the final digest lock.

### Verification
- Run `python3 tools/measure-round80.py --fixture <DIR> --claim C1` and `--claim C2` against a synthetic staging tree containing the durable files; assert both return `count=42 met=true` and `count=2 met=true` respectively.

---

## 8. Artifacts Written
- Seat directory: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ConnectorScope/`
  - `boundary-scan.json`: Structured boundary scan, proposal status, and S330 collision audit.
- Binding report: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ConnectorScope.md`

Scratch directory: `/fast/scratch/hyaku/tsukuroi-r80/ConnectorScope/` (confirmed clean; no live trees remaining).

---

Scope: executed=none
