# FxC3ReturnModes — source-only return-mode probe

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3returnmodes
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.

## Axes and evidence

Axes: return-mode correctness; accounting/strict-verdict separation; detector sensitivity; literal seat-scope compliance.

Read-only source anchors:

- **T**: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-review-cohort.py`.
- **S**: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-review-snapshots.py`.
- **P**: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json`.
- **D**: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`.

## Result: bounded source-level hold, with a detector blind spot

For `evaluate` with its documented byte-reader shape, the named return-mode distinction holds in the inspected source:

1. Missing manifest is the literal `manifest is None` branch. It immediately returns exit **1**, status **FAIL**, accounting mode **0**, and `COHORT-MANIFEST-MISSING` (T:22–24). Settlement parsing and receipt reads are not reached. Empty or malformed manifest bytes are not this case.
2. With a present, well-formed manifest and malformed settlement JSON, settlement parsing raises `ValueError`; missing settlement (`None`) instead raises `TypeError`. Both are caught at T:75–76, returning exit **2**, accounting mode **1**, `COHORT-SCHEMA`, and finally status **CANNOT_EVALUATE** at T:79–80. Parseable settlement schema/identity/cohort errors follow the same path (T:38–51).
3. Consequently, accounting mode **1 is not acceptance**: it also labels schema and read failures (T:75–78). These error payloads do not contain completed seat counts or an `accounted` total. P:7–9 names a calibration metric but also requires accounting for every declared seat and preserving strict findings; observing the metric alone does not establish that bound.
4. Even exit **0 / PASS** from this tool means accounting success, not strict receipt success. Delivered faulty receipts are classified rather than waived (T:55–65); strict exit/findings/conformance remain separate output fields (T:68–74). D:24 and D:31 explicitly preserve that distinction.

This is not a universal CLI-output guarantee. Path/revision/read failures in `main` can return exit 2 without any accounting-mode field (T:148–158). In particular, both committed input reads are evaluated before `evaluate` is called at T:153; an unavailable settlement read can prevent a missing manifest from reaching its mode-0 branch. The bounded claim above requires entry into `evaluate`, not merely absence of a manifest in an otherwise unreadable revision.

## Expected fixture verdicts — source-derived, not runtime observations

Use T:84–89's one-seat manifest/source/report fixtures; any changes below are hypothetical inputs, not edits or executed examples.

| Fixture | Expected exit / status | Expected accounting result |
|---|---|---|
| Manifest `None`; ordinary settlement bytes | 1 / FAIL | mode 0; `COHORT-MANIFEST-MISSING`; no receipt reads |
| Present valid manifest; settlement bytes consisting only of `{` | 2 / CANNOT_EVALUATE | mode 1; `COHORT-SCHEMA`; no completed accounting totals |
| Present valid manifest; settlement `None` | 2 / CANNOT_EVALUATE | mode 1; `COHORT-SCHEMA` |
| Clean built-in fixture | 0 / PASS | mode 1; total/accounted 1; delivered_conformant 1; strict exit 0 |
| Built-in `partial-failed` fixture (T:94–96) | 0 / PASS | mode 1; delivered_faulty 1; strict exit 1; strict_conformance FAIL |

The last row is intentional accounting, not a counterexample to the bounded contract. S:108–118 supplies the receipt faults; T:72–73 retains the strict verdict.

## One plausible mutant and expected detector

**Hypothetical mutant only:** change the schema-error payload's `cohort_accounting_mode` from **1 to 0** at T:76. This is one behavior-bearing scalar change; exit 2, `COHORT-SCHEMA`, and CANNOT_EVALUATE would remain unchanged.

**Expected detector:** an explicit malformed-settlement fixture must assert the complete relevant tuple: `(exit=2, status=CANNOT_EVALUATE, mode=1, finding=COHORT-SCHEMA)`. That assertion would reject this mutant [INFERENCE].

**Source-visible blind spot:** the existing selftest includes malformed settlement cases at T:104–110, but its actual predicate at T:117 checks only exit, optional category count, optional finding membership, and optional strict exit. It never checks accounting mode. Its recorded observations at T:118 also omit that field. Therefore this scalar mutant would leave the built-in selftest's comparisons and printed observations unchanged [INFERENCE]. This finding concerns that selftest only; no uninspected acceptance detector is assessed.

## Actual output, verdict, and restoration evidence

- **Observed runtime output:** none. No baseline, mutant, restored detector, import, test, example, command, or subprocess was executed. No mutation was applied.
- **Runtime mutation verdict:** **INCONCLUSIVE / not exercised**, not a killed or observed surviving mutant. The narrower source-only assignment prohibits the usual three-phase behavioral probe.
- **Source verdict:** the specified evaluator return modes hold under the stated bounds; the existing selftest has a concrete source-visible accounting-mode assertion gap.
- **Before SHA-256:** assignment-supplied `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0`; not independently measured.
- **After SHA-256:** not independently measured. Expected to equal the supplied before hash because this seat made no source writes [INFERENCE]; no measured hash equality is claimed.
- **Restoration:** not applicable: candidate bytes were never mutated. The sole write was this authorized report. No production/build report, receipt fixture, sibling source, or VCS state was altered.
- **Tools installed or updated:** none. No preventive runtime enforcement, actual-reading proof, or request-effect proof is claimed.
