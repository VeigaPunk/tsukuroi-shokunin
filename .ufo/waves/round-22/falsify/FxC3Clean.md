# FxC3Clean: round-22 C3 cohort accounting, source-only falsification

## Binding and scope

- Target: `candidate/tools/check-review-cohort.py`, 164 lines. The assigned Reviewed-SHA256 is recorded as assigned. I did not recompute it (NO-EXEC). The read tool's snapshot tag `ADD3` is a content tag, not a SHA-256, so the digest match is unverified.
- Read, declared paths only: the target (all lines); `check-review-snapshots.py` (all 278 lines, including `strict.evaluate` and its selftest); `_revision.py` (contract, `clean_env`, `bind`, `_object_commit`, `_commit`, `_ancestor`, `_exists`, `branch_tip`); `preregister.json`; `sources/host-tool-boundary.json`; `corpus/knowledge/seat-boundary-r22.json` and `.md`; `skill://godspeed`.
- Executed: none. Fetched: none. Tests, imports, installs, subagents, mutations: none.
- Every "expected" below is a source trace. Observed runtime: none.

## Claim under attack

"One genuinely strict receipt maps to `delivered_conformant`, meaning receipt-only and independent of C2 scope."

## Verdict

- Literal reading (receipt-only): does not hold. The category also depends on the committed source snapshot (F2). The cohort SCOPE string (L19, "receipt-well-formed") understates the mapping.
- Narrowed reading: holds. For review row `r`, the category is `delivered_conformant` iff:
  1. `r.report` exists at the landed commit and decodes as UTF-8;
  2. exactly one physical line starts with each of `Reviewed-SHA256:`, `Predicate:`, `Scope:`, and each equals its declared value (digest = `r.sha256`, predicate = `r.predicate`, scope = `executed=none`) (strict L107-118);
  3. committed `r.source` has sha256 = `r.sha256` (strict L85-91);
  4. the whole manifest and settlement pass validation (cohort L30-51; strict L56-81).
  Otherwise the row is `delivered_faulty` (report present) or an absent category.
- C2 independence: holds structurally. A delivered category's inputs are the row, the manifest `schema`, and committed report and source bytes. Settlement outcome affects only absent categories (L58-59), validation (L42-47), and row recording (L63). No C2 artifact (bindings.json, events.json) is read. All reads are pinned to one `bind()` commit (`_revision` L172-192), so working-tree edits are not observed.
- Expected fixture verdict for the named case (`clean`, cohort L93): exit 0, status PASS, delivered_conformant 1, strict_receipt_exit 0. Observed runtime: none (NO-EXEC).
- Highest-impact item: F1, the C3 metric field.

## Findings

**F1. High if the harness reads the field alone. `cohort_accounting_mode` is 1 on fail-closed exits.**
- L76 (COHORT-SCHEMA) and L78 (COHORT-READ) return `cohort_accounting_mode: 1` with exit 2; L79 sets status CANNOT_EVALUATE. Manifest-missing returns 0 (L24). Completed accounting returns 1 (L71), including when `strict_code` is 2 and exit is 2 (L70). Revision-binding failures emit no field (main L155-158).
- The field does not separate completed accounting from fail-closed input errors. The selftest does not assert it (L112-118).
- Expected fixture (duplicate-json-key, L110): exit 2, CANNOT_EVALUATE, `cohort_accounting_mode` 1 under current code. Observed: none.

**F2. Medium. CE-1: a strict receipt with drifted source maps to `delivered_faulty`, and the cohort still exits 0.**
- Receipt lines pass. Committed source sha ≠ `r.sha256` raises REVIEW-SNAPSHOT-MISMATCH (strict L91), so `one_code` is 1 and the row is `delivered_faulty` (cohort L61). Delivered-faulty adds no cohort finding (L66-70), so exit is 0 and status PASS (L70, L79).
- Expected (P1): exit 0; PASS; delivered_faulty 1; strict_receipt_exit 1; strict_conformance FAIL; row finding REVIEW-SNAPSHOT-MISMATCH. Observed: none.
- Counterexample under the literal reading; not one under the narrowed reading.

**F3. Medium. Settlement-blind delivered mapping.** A row with outcome `failed` or `unknown` and a strict committed receipt is `delivered_conformant`.
- L61 does not read the outcome. No finding is raised, exit is 0, and the row keeps outcome and error (L63). No selftest covers this.
- Expected (P2): exit 0; PASS; delivered_conformant 1; absent_dead 0; seats[0].outcome `failed`. Observed: none.
- Whether a provider-failed seat with a complete receipt should count as conformant or raise a finding is a policy decision for Main. The code does not settle it.

**F4. Medium (labeling). `status` PASS and exit 0 coexist with delivered_faulty, strict_conformance FAIL, and all-absent_dead cohorts.**
- Only absent_unresolved and strict-unavailable add findings (L66-70). The selftest expects exit 0 for dead-missing (L95), partial-failed (L96), and receipt-fault cases (L99-100, L102). `status` therefore reports accounting completion, not receipt conformance. The knowledge note says clean accounting is never a clean receipt verdict; the output key does not say so.

**F5. Low. Identical receipt bytes across seats are each `delivered_conformant`.**
- Strict enforces unique report paths (L73, L80), not unique content. `report_sha256` (L65) is recorded and never compared. Holds under receipt-only; "one receipt, one seat" is not enforced.

**F6. Low (type fidelity; git behavior not executed).**
- `git_read` (cohort L124-131; strict L131-142) returns whatever `git show rev:path` prints, with no mode or type check. A committed symlink prints its target text. On Linux that text can contain newlines, so a symlink report whose target text carries the three declarations passes L107-118.
- A committer who can land a manifest can already land a regular receipt file, so this adds no capability. It is a fidelity gap. Fix candidate: require `ls-tree` mode 100644 or 100755 before reading.

**F7. Low. Finding-id collision.** REVIEW-SNAPSHOT-MISMATCH is emitted for source drift (strict L91) and for receipt digest mismatch (strict L114). The cohort's `strict_receipt_findings` (L72) cannot separate them.

**F8. Low. Scope string.** Cohort SCOPE (L19) omits the "not proof of ... command nonexecution ... chronology" disclaimers carried by strict scope (strict L128). `executed=none` is a nonexecution declaration; the cohort scope should say delivered_conformant does not prove it.

**F9. Bounded gap, not a falsification of C3's own claim.** Independence is structural. Nothing reconciles reviews.json rows with bindings.json, or settlement agents with events.json. The denominator is whatever manifest and settlement sit at the chosen commit. preregister.json pins no manifest hash and no seat count.

## Bounded holds (fail-closed, source-traced)

- Line level: leading or trailing spaces, indentation, BOM, CR-only lines, U+2028, U+0085, VT or FF inside a line, duplicate or missing prefixed lines, case changes, NUL, non-UTF-8. None yield conformant (strict L42-44, L107-118; strict selftest L145-209; cohort selftest L98-102).
- Indented receipt examples do not count (column-0 `startswith`). The Lane bounds line is not checked.
- Schema: duplicate keys, duplicate names, agents or reports, unknown or missing settlement rows, `failed` without error, `completed` with error, unsafe paths → exit 2 (cohort L30-51; strict L56-81, L122-124).
- Absence: `git show` failure plus empty `ls-tree` → absent category. Any other git failure → RuntimeError → COHORT-READ (cohort L124-131, L77-78).

## Fixture expectations (source trace; observed: none, NO-EXEC)

| Fixture | Expected |
| --- | --- |
| clean (existing, L93), the named attack | exit 0; PASS; cohort_accounting_mode 1; total 1; delivered_conformant 1; accounted 1; strict_receipt_exit 0; strict_conformance PASS; findings []; strict_receipt_findings []; seats[0] delivered_conformant, strict_exit 0 |
| P1 source drift with strict receipt (F2) | exit 0; PASS; delivered_faulty 1; strict_receipt_exit 1; strict_conformance FAIL; REVIEW-SNAPSHOT-MISMATCH in row findings |
| P2 failed outcome with strict receipt (F3) | exit 0; PASS; delivered_conformant 1; absent_dead 0; outcome `failed` kept |
| P3 duplicate-json-key (existing, L110) | exit 2; CANNOT_EVALUATE; cohort_accounting_mode 1 under current code (F1) |
| P4 two rows, identical receipt bytes (F5) | exit 0; delivered_conformant 2; equal report_sha256 |
| P5 cohort read raises RuntimeError (no fixture today) | exit 2; COHORT-READ; cohort_accounting_mode 1 under current code (F1) |
| Other 17 existing cohort selftest cases | source trace predicts all pass |

Proposed fixtures are not added; no production edits were made.

## Residual risk and verification gaps

- The digest is not recomputed; the bytes read are unverified against the assigned digest.
- F1 severity depends on the C3 harness, which is outside my declared reads.
- F6 assumes git object-model behavior (symlink blob equals link text). Not executed.
- `_revision.py` selftest (L195-432) and the snapshot main beyond `bind` were not reviewed; no receipt-relevant defect appeared in the ranges read.
- Sibling checkers and the harness are outside my declared reads; no claims are made about them.

## Receipt

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3clean
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
