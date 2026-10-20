# HistoryBoundary — Append-Only Protocol and Preservation Floor Analysis

author: TsukuroiR15.HistoryBoundary (scout, depth axis)
date: 2026-10-20
baseline: `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`
status: read-only research complete; leaf seat (no subagent dispatch)
judged_on: depth

## 1. Executive Summary & Declared Axes

- **Target:** Thoroughly review the append-only protocol (`PROTOCOL.md`, `corpus/QUALITY.md`, `AGENTS.md`) and independent verifier findings (`corpus/lessons/round-14-verifier-spotcheck.md`, `round-13-verifier-spotcheck.md`, `round-12-verifier-spotcheck.md`). Deliver the definitive inventory of historical files across the workspace that must remain strictly unchanged except for additive, non-destructive notices, along with the precise preservation rules and validation criteria.
- **Axes:**
  - `depth`: Rigorous structural analysis of byte-preservation invariants, AST/JSON order-preservation constraints, line-preservation mechanics, and exact loci of supersession notices.
  - `operability`: Explicit definition of automated verification checks to ensure zero historical regressions across wave transitions without causing conformance failures.
- **Ownership:** Report only; read-only research. No verification runs, test suites, live-host mutations, or subagent dispatch.

---

## 2. Foundations of the Append-Only Protocol

### 2.1 Fleet Canonical Invariants (`PROTOCOL.md`)
1. **Never Rewrite or Delete Log Records (`PROTOCOL.md:463`):**
   > "`LOG.md` is append-only: entries are never rewritten or deleted; corrections land as new entries."
2. **Corpus Corrections Are New Entries (`PROTOCOL.md:477-479`):**
   > "`corpus/` inherits the evidence standard: every `knowledge/` entry cites a resolvable source; `corpus/lessons/` entries cite the round and its LOG.md entry or lane report. Corpus corrections are new entries, never in-place rewrites: no lane edits another lane's corpus files..."
3. **Queue of Record & Correction Disciplines (`PROTOCOL.md:366-368`):**
   > "A falsified claim in an append-only file gets a named correction entry in the lane's next round — appended, never rewritten; it stays on the routed-defect queue until it lands."
4. **SOURCES Registry Contract (`PROTOCOL.md:435`, `CORPUS.md`):**
   > Curated source registry is strictly append-only. Existing S### rows, anchors, and tier definitions are immutable historical text. New sources append S### rows; re-evaluations append Search-log entries or superseding rows.

### 2.2 Lane Operating Rules (`AGENTS.md` & `corpus/QUALITY.md`)
1. **Motivating Evidence (`AGENTS.md:3`):**
   > "Every change appends a `LOG.md` entry with motivating evidence."
2. **Criterion 4 (`corpus/QUALITY.md:7`):**
   > "4. Errata are append-only blocks."
3. **Criterion 5 (`corpus/QUALITY.md:8`):**
   > "5. A rejection is kept, not silently dropped."
4. **Criterion 10 (`corpus/QUALITY.md:16-17`):**
   > "10. Before a correction commit, sweep every mention in README.md, SKILL.md and corpus/knowledge/ for superseded text, and verify changed Markdown tables retain their intended column count and delimiters..."
5. **Criterion 19 & 20 (`corpus/QUALITY.md:30-41`):**
   > Criterion 19 (`R14-SOURCE-SCOPE`) enforces exact source object citation, located $\le$25-word quotes, and separate bounded checker failures for preserved prior defects. Criterion 20 formally supersedes criterion 18's blanket bot attribution via append-only mechanism, leaving criterion 18's historical text intact.
6. **Criteria 21 & 22 (`corpus/QUALITY.md:43-50`):**
   > Appended in round 15 to establish portable heading-based locators (`R15-LOCATOR`) and positive option definition semantics (`R15-POSITIVE-DOMAIN`), without editing criteria 1–20.

---

## 3. Analysis of Round 14 Verifier Corrections & Preservation Witness

In `corpus/lessons/round-14-verifier-spotcheck.md` (authored by hyaku closure integrator `@m_strong`), independent preservation checks were executed over `git show` bytes across baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6` and delivered implementation `932e32d6d2d360e18fa7fe4cdd397215fd166e4b`:

1. **Source Rows S001–S043:** **0** changed original registry rows (`:124`).
2. **JSON Object Reversibility:** Original round-13 JSON object equals the final object after removing only its additive `r14_supersession` key (`:125-126`).
3. **Zero Deleted or Missing Lines Across Ten Historical Text Files (`:127-131`):**
   - Baseline text lines remained in order in: `LOG.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-13.md`, `corpus/knowledge/root-dac-correction-r13.md`, and `corpus/knowledge/snapper-eacces-mechanism.md`. Missing lines in each: **0**.
   - Note on SKILL: An apparent one-line replacement was an EOF missing newline normalization at line 1785, not deleted teaching.
4. **Byte-Identical Core Artifacts (`:132-134`):**
   - Census script (`tools/tsukuroi-census.sh`), old gate (`tools/check-root-dac-correction.py`), outside verifier lessons (`corpus/lessons/round-12-verifier-spotcheck.md`, `round-13-verifier-spotcheck.md`), and promotion checklist (`SHONEN.md`) were **byte-identical** across revisions.
5. **Adjudicated Routing Instructions for Successor Rounds (`:233-256`):**
   - *Concern 1 (Renderer line locators):* Supplemental line numbers (e.g. lines 1266–1267) were renderer-dependent presentation artifacts. Integrator ruling: **"Append a renderer-qualified locator clarification or rely on the stable heading; do not rewrite the filed history."**
   - *Concern 2 (Negative-claim documentation):* Negative claim "documents no further values" lacked a dedicated command/date sweep. Integrator ruling: **"Append the bounded documentation sweep or use only the positive source-definition proposition; do not treat this closure as a claim of exhaustive parser proof."**
   - *Reviewer suggestions rejected as defects:* Criterion 18 did not need an inline edit because appended criterion 20 explicitly supersedes that clause. "Ten changed historical text files" was accurate because the eleventh modified file was the JSON twin.

---

## 4. Comprehensive Inventory of Historical Files & Boundary Rules

Across the `tsukuroi-shokunin` workspace, files are categorized into four distinct preservation tiers. Any modification violating these classifications constitutes a protocol breach.

### Tier 1: Historical Ledger & Contract Files (Additive Notices & Appends Only)

These files represent the progressive historical ledger of the lane. Existing lines are permanently frozen; only new dated sections, move-log entries, or errata notices may be appended.

| File Path | Historical Baseline Status | Permitted Modifications | Prohibited Modifications |
|---|---|---|---|
| `LOG.md` | Contains rounds 0–14 records (`lines 1–792+`). | Append new dated round blocks (e.g. `## 2026-10-20 — round 15...`) at end of file. | Rewriting, reordering, editing, or deleting any historical entry. |
| `SCORECARD.md` | Contains final closeout assessment, move logs, and rounds 1–14 assessments (`lines 1–440+`). | Append new round move-log rows and new round assessment appendix at end of file. | Modifying historical scores, deleting past move-log rows, or changing baseline citations. |
| `SKILL.md` | Domain specialist playbook (`lines 1–1785`). | Append new errata blocks, routing notes, and gate/probe registry table rows. | Modifying existing decision tables, removing historical rules, or altering past gate registry rows. |
| `PROVINCE.md` | Domain boundary, Core/Adjacent handoffs (`lines 1–106`). | Append new round errata / boundary refinement paragraphs at end of file. | Modifying historical Core owns/refuses blocks or changing existing ADJ-01..07 contracts. |
| `corpus/QUALITY.md` | Core admission criteria 1–20 (`lines 1–41`). | Append new numbered criteria (e.g. 21, 22) as distinct blocks at end of file. | Editing, rephrasing, or deleting criteria 1–20. |
| `corpus/README.md` | Coverage map, quality bar, and historical round summaries (`lines 1–94`). | Append new round coverage rows, errata blocks, and frontier notes. | Rewriting existing coverage table rows or removing historical round summaries. |
| `corpus/SOURCES.md` | Registry rows S001–S045, search log, study paths (`lines 1–108`). | Append new sequential S### rows (S046, S047, S048) and new dated Search-log paragraphs. | Editing any field (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`, `recheck`) of rows S001–S045. |

### Tier 2: Historical Knowledge Notes & JSON Twins (Additive Notices Only)

Historical knowledge notes preserve past analyses (and their superseded defects) to maintain evidentiary integrity for independent verifiers.

| File Path | Active Status | Required Preservation State | Allowed Additive Loci |
|---|---|---|---|
| `corpus/knowledge/snapper-eacces-mechanism.md` | Historical | Contains original round-1 analysis and round-12/13/14 errata (`lines 1–121`). | Append dated `## Erratum` blocks at end of file. Do not edit body. |
| `corpus/knowledge/root-dac-decision-r12.md` | Historical (Rejected C2) | Contains r12 create-failure decision matrix (`lines 1–159`). Retains false universal. | Top blockquote banner and bottom `## Round-13 correction` notice are frozen. No inline edits. |
| `corpus/knowledge/root-dac-decision-r12.json` | Historical (Rejected C2) | `tsukuroi-dac-decision-matrix-v1`. | Top-level additive keys (`superseded_by`, `correction_notice`) are frozen. Object must deep-equal baseline when keys stripped. |
| `corpus/knowledge/root-dac-correction-r13.md` | Historical (Superseded loci) | Contains R13-DAC-EXCLUSIVITY (`lines 1–245`). Retains superseded MD:97 value-domain cell and QUALITY 18 triage phrase. | Provenance trio and top notice frozen; `## R14 named corrections` notice frozen. Any R15 notice must append. |
| `corpus/knowledge/root-dac-correction-r13.json` | Historical (Superseded loci) | `tsukuroi-dac-correction-v1`. | Additive top-level `r14_supersession` key frozen. All original keys (`schema`, `branches`, `gate_contract`, `sources[0]`) preserved verbatim. |
| `corpus/knowledge/source-scope-correction-r14.md` | Historical / Active Base | Contains R14-VALUE-DOMAIN & R14-COMMENT-ATTRIBUTION (`lines 1–248`). Retains supplemental reader lines 1266-1267 and negative claim. | Additive `## Round-15 locator & positive-domain clarification` block at end or prominent header banner. Zero deletions of existing lines. |
| `corpus/knowledge/source-scope-correction-r14.json` | Historical / Active Base | `tsukuroi-source-scope-correction-v1`. | Additive top-level `r15_supersession` key. Removing `r15_supersession` must leave original JSON object identical. |

### Tier 3: Historical Lessons & Independent Verifier Reviews (Strictly Immutable)

Lessons and independent verifier spot-checks record historical review judgments and integrator verdicts. They are durable audit records and must **never** be modified under any circumstances.

| File Path | Authority & Role | Preservation Invariant |
|---|---|---|
| `corpus/lessons/round-1.md` | Historical Lane Lesson (Round 1) | **0 lines modified or deleted.** Append-only notice at end permitted only if routed by protocol. |
| `corpus/lessons/round-1-verifier-spotcheck.md` | Integrator Audit (Round 1) | **Byte-identical.** Strictly immutable. |
| `corpus/lessons/round-12.md` | Historical Lane Lesson (Round 12) | **0 lines modified or deleted.** |
| `corpus/lessons/round-12-verifier-spotcheck.md` | Integrator Audit (Round 12, C2 Rejected) | **Byte-identical.** Strictly immutable. |
| `corpus/lessons/round-13.md` | Historical Lane Lesson (Round 13) | Retains R14 append-only attribution notices (`lines 1–190`). **0 lines deleted.** |
| `corpus/lessons/round-13-verifier-spotcheck.md` | Integrator Audit (Round 13, Rejected) | **Byte-identical.** Strictly immutable. |
| `corpus/lessons/round-14.md` | Historical Lane Lesson (Round 14) | Retains r14 Gates and Mistakes (`lines 1–154`). **0 lines deleted.** |
| `corpus/lessons/round-14-verifier-spotcheck.md` | Integrator Audit (Round 14, Admitted True) | **Byte-identical.** Strictly immutable. Canonical reference for R15 documentation debts. |

### Tier 4: Mechanical Gates, Checklists & Invariant Tools (Byte-Identical Floor)

These executable tools and template forms enforce consistency and must not drift during documentation or recheck waves.

| File Path | Invariant Requirement | Validation Mechanism |
|---|---|---|
| `SHONEN.md` | Byte-identical to canonical template modulo `<name>` substitution (`PROTOCOL.md:419-431`). | Exact diff against canonical template seed; 4 `[~]` lines; zero unauthorized prose. |
| `tools/tsukuroi-census.sh` | Health census gate script (2679 lines). | Byte-identical; `--selftest` zero mutation contract; live contract read-only. |
| `tools/check-root-dac-correction.py` | Historical narrow r13 gate evaluator (375 lines). | Byte-identical; SHA256 pinned in historical evidence (`4422941d...`). |
| `tools/check-source-scope-correction.py` | Round 14 source-scope evaluator (539 lines). | Byte-identical; SHA256 pinned in round-14 verifier spotcheck (`0771619d...`). |

---

## 5. Additive Notice Mechanics & JSON Supersession Rules

To fulfill the protocol requirement where historical false or imprecise claims are preserved while active routing points to corrected surfaces:

### 5.1 Markdown Additive Notice Structure
1. **Notice Placement:** Either placed as a top banner immediately below the provenance trio (`source:`, `verified-at:`, `recheck:`), or as a dedicated, explicitly titled section at the end of the file (e.g. `## R14 named corrections` or `## R15 locator clarification`).
2. **Required Notice Fields:**
   - Date and active round identification (`2026-10-20, round 15`).
   - Specific correction identifier(s) (`R15-LOCATOR`, `R15-POSITIVE-DOMAIN`).
   - Explicit pointer to the active successor document (`corpus/knowledge/source-locator-clarification-r15.md` and `.json`).
   - Precise scope of supersession: identifying exact line numbers, headings, or clauses in the historical file that are superseded, while affirming that the technical findings and unaffected surrounding prose remain active.
3. **Zero-Deletion Diff Requirement:**
   - Any git diff of the historical file against baseline must show `old-count = 0` across all hunks (i.e. `@@ -N,0 +N,M @@`).
   - The only recognized exception is EOF newline normalization, where `new_bytes.startswith(old_bytes)` remains True.

### 5.2 JSON Additive Supersession Structure
When superseding or clarifying structured knowledge in a JSON twin (such as `source-scope-correction-r14.json` or `root-dac-correction-r13.json`):
1. **Never Mutate Historical Keys:** Top-level keys (`schema`, `round`, `corrections`, `errata`, `sources`, etc.) and all nested elements must retain their original values, types, and ordering.
2. **Additive Schema Envelope:** Add a single top-level key (e.g. `"r15_supersession"`) containing:
   - `"schema"`: Versioned supersession schema identifier (e.g. `"tsukuroi-r15-supersession-v1"`).
   - `"notice"`: Human-readable explanation affirming that all prior keys are preserved historical authoring bytes.
   - `"active_corrections"`: Pointers to the active successor MD/JSON files.
   - `"superseded_loci"`: Array of objects identifying each superseded locus, the defect, and the active reading.
   - `"historical_bytes_preserved"`: `true`.
3. **Reversibility Invariant:**
   A mechanical test must verify:
   ```python
   data = json.loads(git_show(HEAD, path), object_pairs_hook=collections.OrderedDict)
   data.pop("r15_supersession", None)
   assert data == json.loads(git_show(BASELINE, path), object_pairs_hook=collections.OrderedDict)
   ```

---

## 6. Verification and Boundary Recommendations for Tsukuroi Round 15

1. **Enforce Preservation in CI / Integration:**
   Before committing any round 15 integration commit, L1 should run a mechanical diff check across all historical text files:
   ```sh
   git diff -U0 $BASELINE HEAD -- LOG.md SCORECARD.md SKILL.md PROVINCE.md \
     corpus/QUALITY.md corpus/README.md corpus/SOURCES.md corpus/lessons/*.md \
     corpus/knowledge/root-dac-decision-r12.* corpus/knowledge/snapper-eacces-mechanism.md \
     corpus/knowledge/root-dac-correction-r13.* corpus/knowledge/source-scope-correction-r14.*
   ```
   Verify that no deletion hunks (`-N,M` where $M > 0$) exist, except for known EOF newline normalization.
2. **Isolate New Knowledge in Disjoint Files:**
   All new technical findings, clarified locators, and partial-upgrade measurements for round 15 must reside strictly in new files:
   - `corpus/knowledge/source-locator-clarification-r15.md`
   - `corpus/knowledge/source-locator-clarification-r15.json`
   - `corpus/knowledge/partial-upgrade-recheck-r15.md`
   - `corpus/knowledge/partial-upgrade-recheck-r15.json`
   - `tools/check-locator-clarification.py`
   - `tools/measure-update-recheck.py`
3. **Preserve Source Registry Immutability:**
   In `corpus/SOURCES.md`, rows S001 through S045 must remain byte-identical. Rows S046, S047, and S048 must be appended at the end of the table with valid fields. Disclose expected W04 duplicate-URL census warnings without mutating historical URLs.

---

## 7. Sources, Limits, and Tooling

### Exact Sources
- `PROTOCOL.md`: Fleet lifecycle, gate standard, append-only invariants, file contracts (`lines 124, 314, 366-370, 419-439, 463-479`).
- `corpus/QUALITY.md`: Numbered criteria 1–22 (`lines 1–50`).
- `AGENTS.md`: Operating invariants (`lines 1–6`).
- `corpus/lessons/round-14-verifier-spotcheck.md`: Step-1 conformance, C1 depth measurements, preservation checks, outside quote discernment, and adjudicated concerns (`lines 1–265`).
- `corpus/lessons/round-13-verifier-spotcheck.md`: Historical verification and rejected claims (`lines 1–275`).
- `corpus/lessons/round-12-verifier-spotcheck.md`: Historical verification and C2 rejection (`lines 1–260`).
- `corpus/knowledge/source-scope-correction-r14.md` & `.json`: Baseline R14 correction records.
- `corpus/knowledge/root-dac-correction-r13.md` & `.json`: Preserved R13 records with additive R14 notices.
- `corpus/knowledge/root-dac-decision-r12.md` & `.json`: Preserved R12 matrix records.

### Limits
- Read-only static research and git blob inspection. No live-host state was queried or modified.
- No gate scripts (`tools/tsukuroi-census.sh`, `tools/check-source-scope-correction.py`, `tools/check-root-dac-correction.py`) were executed by this seat.
- No tests were run and no verification pass is claimed.

### Tooling Directive Record
- Tools installed or updated by this seat: **none**.
- Work completed purely via read-only filesystem and git inspection tools.
