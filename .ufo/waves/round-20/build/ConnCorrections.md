# ConnCorrections — Bounded Proposal: Durable Correction Placement via Additive Supersession

**Seat:** `TsukuroiR19Recovery.ConnCorrections-2`  
**Role:** UFO-FSD Connector  
**Author Round:** Tsukuroi round 20, attempt 1 (`TsukuroiR20`)  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472`  
**Mode:** NO-EXEC (read/grep/glob only; no subprocesses, shell/eval, host probes, or verification executions)

---

## 1. Declared Axes

The round's declared axes and contract metrics (per `.ufo/waves/round-20/preregister.json` and canonical assignment):

- **C1 Adjacency** (ordinal 8, lowest/tied-lowest, ordinal delta 0):
  Metric: `ownership_corrections` (before: 0, after: 1).
  Evaluator: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
  Scope: Explicit sibling-declaration wording for OUT-009 at retained pinned scope, no integrator arbitration or write authority.
- **C2 Operability** (ordinal 9, ordinal delta 0):
  Metric: `object_selector_tools` (before: 0, after: 9).
  Evaluator: `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`.
  Scope: Original-nine consumer continuity under object-only hexadecimal selector tests; supporting read-only systemctl execution-log classifier.
- **C3 Calibration** (ordinal 9, ordinal delta 0):
  Metric: `audit_live_map_errors` (before: 1, after: 0).
  Evaluator: `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.
  Scope: Highest operative boot-chain-audit live map is `0 CONSISTENT/observation`, `2 UNKNOWN/could-not-evaluate`; code 1 is selftest failure only, never live DEGRADED. Append named R19 false-erratum and non-prefix disclosure.

All ordinal deltas remain strictly 0; genuine finite improvements within bounded claims, with no claims of host or boot safety.

---

## 2. Evidence: The Triad of Past Failure Modes

A careful cross-examination of the baseline repository, round-19 outside closure (`corpus/lessons/round-19-verifier-spotcheck.md`), round-20 preregistration (`preregister.json`), and seeded implementations reveals that three seemingly disparate defects share a single structural pathology in correction placement:

### A. False Operative-Map Repair (`R20-FALSE-OPERATIVE-MAP`)
- **Evidence:** In round 19, fleet-report erratum C3 (`report:r19:122`) and `LOG.md:1023` claimed that the operative `boot-chain-audit` verdict row had stopped advertising live `1 DEGRADED`. However, the outside verifier spotcheck (§2 C3, lines 79–92; §5 item 2) refuted this: the committed tip still advertised live `1 DEGRADED` in the operative table (`SKILL.md:2073`).
- **Mechanism:** In `tools/check-registry-coverage.py:133–146`, `_operative_rows()` parses `SKILL.md` by identifying all headings matching `^## Gate and probe registry — round([0-9]+) superseding current rows$` and selecting the **unique highest round number**. In round 19, the author swarm attempted to repair the map by editing historical round-18 row 1965 in place. Because the parser selected the higher round-19 table (`round19 > round18`), editing the older table had zero effect on the operative contract. The operative table at line 2073 remained uncorrected.

### B. Nonappend Exception (`R20-SKILL-PREFIX-EXCEPTION`)
- **Evidence:** Round 19 fleet-report quality verdict (`report:r19:78`) asserted that all edits to `PROVINCE.md`, `SKILL.md`, and knowledge corpus were strictly append-only, preserving baseline prefixes. Outside closure (§1 row 30, §5 item 3) refuted this for `SKILL.md`: the committed diff was `+80/−1`, mutating historical row 1965 in place.
- **Mechanism:** In-place mutation of historical lines directly violates immutable baseline prefix preservation. While attempting to fix the live-map contract, an in-place modification broke historical integrity, leaving the operative table broken while introducing an unflagged nonappend defect.

### C. No-Write Locality and Diffuse Contradictions (`R20-OUT009` and `R20-RULE4`)
- **Evidence 1 (OUT-009 / C1):** Baseline `PROVINCE.md:129` stated: `"Revenger owns shipped-artifact reverse engineering (binaries, packages, APKs)..."`. This conflicted directly with `PROVINCE.md:79–80` (which establishes that Kaidoku and Revenger both claim shipped-artifact RE and that Tsukuroi neither picks an owner nor absorbs it, reserving arbitration to the protocol integrator), with `PROVINCE.md:8–9` (Tsukuroi owns pacman package state; Revenger declared only Electron/JavaScript packages), and with `PROVINCE.md:39–40` (no handoff confers write authority).
- **Evidence 2 (Rule 4 / boot-writers):** Baseline `boot-writers-r19.md:93` asserted: `"No write: a snapper-cleanup run with no Updated: line is not a write"`. At line 164, a qualification was added stating that absence of `Updated:` is not proof of "not a write". Outside closure (§5 item 5) observed that this qualification was nonlocal and diffuse; because it failed to explicitly supersede operator decision rule 4 at line 93, the text retained an unanchored direct contradiction.

---

## 3. Synthesis: Connecting the Triad to Durable Correction Placement

The structural connection across these three defects is direct:

1. **In-place historical mutation is both contractually futile and integrity-breaking:**
   Modifying an earlier historical block (e.g. Round 18 in `SKILL.md` or the historical OUT-009 row in `PROVINCE.md`) cannot fix a downstream operative selector that inspects the highest section, but it *guarantees* a nonappend violation (`+N/-M`) that invalidates baseline prefix verification.
2. **Diffuse, unanchored qualifications create unresolved contradictions:**
   Placing a qualification tens or hundreds of lines away without an explicit, named supersession heading creates semantic ambiguity where evaluators and human operators cannot determine whether the older rule, the newer qualification, or an arbitrary compromise governs.
3. **No-write boundaries must be anchored locally at the point of clarification:**
   Whenever an external declaration or negative observation is clarified, the boundary prohibiting configuration, service, package, boot, or sibling writes must be locally reaffirmed within that exact named section. Passive observation (whether a sibling province statement or absence of a journal event) must never be converted into remedial permission or an overclaimed negative proof of zero substrate modification.

Therefore, **durable correction placement** requires:
- **Strictly additive, named supersession blocks** placed at document tails (`## <Round> <Target> — named supersession / clarification`).
- **Preservation of historical baseline prefixes**, treating historical tables, pins, and snapshots as immutable evidence data.
- **Explicit local re-anchoring of the no-write / non-remediation invariant** within the correction itself.

---

## 4. Proposed Move: Unified Additive-Supersession Integration Invariant

**The Proposed Move:**  
For L1 final integration, establish and enforce the **Unified Additive-Supersession Invariant** across all three claims (C1, C2, C3) and documentation updates:

1. **C1 (Adjacency Anchor Placement in `PROVINCE.md`):**
   - Retain lines 1–146 of `PROVINCE.md` byte-for-byte identical to baseline (preserving the full raw prefix, the original ADJ-06 line-range table, and the historical `OUT-009` row in `## Adjacent — portable ownership anchors (round 19)`).
   - Place the clarification exclusively as an appended tail section:
     `## R20 ownership clarification — OUT-009`
     containing the exact text of `.ufo/waves/round-20/ownership-correction.txt`.
   - Ensure the correction explicitly anchors the no-write boundary:
     `"No configuration, service, package, boot or sibling-file write is authorized."`
   - Gate verification (`tools/check-adjacency-anchors.py --ownership-corrections`) must check that the original OUT-009 pin in `registry_doc` and `census_doc` still binds to snapshot `cf02419276e5`, that `OWNERSHIP_ARBITRATION_LINES` remain in the body, and that the appended clarification heading is unique.

2. **C3 (Operative Registry Placement in `SKILL.md`):**
   - Never mutate historical Round 18 (`SKILL.md:1965`) or Round 19 (`SKILL.md:2066–2082`) rows in place.
   - Append the named disclosures:
     `## R20 — named corrections and read-only limits`
     explicitly naming `R20-FALSE-OPERATIVE-MAP` and `R20-SKILL-PREFIX-EXCEPTION`.
   - Append the superseding operative table:
     `## Gate and probe registry — round20 superseding current rows`
     containing all 17 registered tools with the corrected `boot-chain-audit` cell:
     `live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance`.
   - This ensures `tools/check-registry-coverage.py --audit-live-map` selects the round 20 table as highest (`highest == 20`), emitting `audit_live_map_errors=0` while preserving baseline prefix integrity for earlier sections.

3. **Substrate & Knowledge Locality (`boot-writers-r19.md`):**
   - Do not delete or rewrite Operator rule 4 at line 93.
   - Append the dedicated named heading:
     `## R20-RULE4 — named supersession of Operator decision rule item 4`
     explicitly superseding the unsupported deduction that "no Updated event implies no write", while affirming that the cause of the 09:08:04 cleanup remains an unresolved unknown and that no host write action follows.

---

## 5. Second-Order Effects & Affected Axes

- **C1 Adjacency (Primary Beneficiary, 8→8):**
  - Advances `ownership_corrections` from 0 to 1.
  - Prevents regression of the existing 10 anchor / 114 inbound locator checks by maintaining immutable historical records while resolving the OUT-009 overclaim.
  - Eliminates ambiguity regarding Kaidoku/Revenger arbitration and prevents misinterpretation of RE handoffs as write authority.
- **C3 Calibration (Primary Beneficiary, 9→9):**
  - Advances `audit_live_map_errors` from 1 to 0.
  - Aligns the operative registry table with `tools/boot-chain-audit.sh`'s actual runtime contract (schema-v2 live returns 0/2; code 1 reserved for selftest assertion failures).
  - Preserves full backward-compatibility for generic coverage checks across all 17 tools.
  - Avoids a repeat of the R19 nonappend defect by ensuring all R20 documentation and registry additions are strictly appended.
- **C2 Operability (Unharmed, 9→9):**
  - Orthogonal: C2's object-selector fixes in `_revision.py` and consumer tools operate without dependence on document text locations.
  - Supporting systemctl exec-log classification benefits from the reaffirmed read-only boundary across all documents.
- **Substrate & Runtime Surfaces:**
  - Absolute zero risk to host substrate: no pacman, systemd, bootloader, kernel, or mount writes are performed or authorized.
  - Transcript bytes and manual URLs remain inert data.

---

## 6. Risks and Mitigations

| Risk | Severity | Mechanism | Mitigation |
|---|---|---|---|
| **Accidental In-Place Historical Rewrite** | High | Integrator edits historical table row to "clean up" past errors, repeating R19 `+80/-1` defect. | Maintain strict append-only discipline; verify git diff against baseline `0cbc34dd...` contains only additions (`+N/-0`) for `PROVINCE.md`, `SKILL.md`, and `boot-writers-r19.md`. |
| **Heading Duplication or Typo in Table Opener** | High | A typo in `## Gate and probe registry — round20 superseding current rows` causes `check-registry-coverage.py` to fall back to round 19 (failing C3 with `audit_live_map_errors=1`) or crash with `TableError`. | Match exact regex `^## Gate and probe registry — round([0-9]+) superseding current rows$`; ensure exactly one round 20 table exists. |
| **Missing Tool Rows in Round 20 Table** | Medium | The round 20 table corrects `boot-chain-audit` but omits one of the other 16 tools, causing generic coverage failure (`REGISTRY-ROW-MISSING`). | Verify all 17 tool rows are carried forward into the round 20 table with updated/consistent cell contents. |
| **Arbitration or Permission Leak in OUT-009** | Medium | Paraphrasing OUT-009 inadvertently implies Kaidoku/Revenger dispute resolution or host remediation permission. | Use exact verbatim text from `ownership-correction.txt`, which includes explicit disclaimers of arbitration and write authority. |

---

## 7. Verification Plan (For L1 Post-Wave Final Evaluation)

*Note: Per seat contract, NO verification commands were executed by this seat.*

Once all wave seats settle and L1 integrates the external worktrees, L1 will run the unchanged final evaluators:

1. **C1 Adjacency Ownership Verification:**
   ```bash
   python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections
   ```
   *Expected:* `ownership_corrections=1`, findings empty, exit code `0`. (Baseline red: `OWNERSHIP-CORRECTION-MISSING`, exit `1`).
2. **C3 Audit Live Map Verification:**
   ```bash
   python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map
   ```
   *Expected:* `audit_live_map_errors=0`, findings empty, exit code `0`. (Baseline red: `REGISTRY-AUDIT-LIVE-MAP`, exit `1`).
3. **C2 Object Selector Verification:**
   ```bash
   python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors
   ```
   *Expected:* `object_selector_tools=9`, exit code `0`.
4. **Append-Only Prefix Verification:**
   ```bash
   git diff --stat 0cbc34dd6b20896085a8fb07943e3ea4027d8472..<REV> -- PROVINCE.md SKILL.md corpus/knowledge/boot-writers-r19.md
   ```
   *Expected:* Zero line deletions (`-0`) across all three core document surfaces.

---

Scope: executed=none
