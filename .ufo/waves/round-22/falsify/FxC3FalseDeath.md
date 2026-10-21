# FxC3FalseDeath — source-only false-death probe

## Scope and verdict

Axes: schema soundness; absent/dead classification fidelity; evidence calibration.

**Source verdict: bounded reason the invariant holds.** With a schema-valid manifest, a readable fixture, and a settlement seat declaring `outcome="failed"` and `error=""`, the candidate rejects the settlement with exit 2, status `CANNOT_EVALUATE`, and finding `COHORT-SCHEMA`. It cannot classify that seat as `absent_dead`. No concrete counterexample to this empty-error predicate was found in the inspected control flow.

**Mutation-test verdict: INCONCLUSIVE / NOT EXECUTED.** This seat permits source-only analysis, not source mutation or detector execution. No killed or surviving mutant is claimed.

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-review-cohort.py`.

Dependency inspected: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-review-snapshots.py`.

## Source-visible reasoning

1. Cohort lines 30–31 parse both JSON inputs with the strict dependency's `unique_object`; that helper rejects duplicate JSON keys at dependency lines 33–39. A duplicate `error` declaration cannot bypass validation by being silently overwritten.
2. Cohort line 42 requires every settlement row's `error` to be a string. Missing, null, or non-string errors therefore raise the settlement schema exception.
3. Cohort lines 44–45 explicitly reject `outcome == 'failed'` when `not error.strip()`. This includes the empty string and strings consisting only of characters removed by Python's `str.strip()`.
4. The full settlement-validation loop precedes the classification loop. The `absent_dead` branch at cohort lines 58–59 is reachable only after the failed-row error guard and complete cohort identity validation succeed. Report absence does not skip that guard.
5. The resulting `ValueError` is caught at cohort lines 75–76, setting exit 2 and exactly the finding `{'id': 'COHORT-SCHEMA', 'site': 'input'}`. Line 79 sets status `CANNOT_EVALUATE`. This result does not contain seat classifications or bucket counts; it is not an accounting PASS with a dead-seat count.

The dependency's missing-report path merely adds `REVIEW-REPORT-MISSING` (dependency lines 98–99) and returns strict exit 1 when no read or encoding error intervenes (line 121). It does not preempt settlement validation, so an absent report does not create a route around the empty-error guard.

## Expected fixture verdicts — static inference only

Use the existing one-seat fixture definitions at cohort lines 84–89 as the bounded reference. Their source, manifest identity, and report are already specified in the candidate; no fixture was instantiated or run for this review.

| Fixture description | Expected evaluator result from source | Observed runtime |
| --- | --- | --- |
| Existing `false-death` selftest case: change only the completed seat's outcome to `failed`, retaining its empty error and delivered report (lines 104–106). | Exit 2; `COHORT-SCHEMA`; status `CANNOT_EVALUATE`; no seat classification. | None; not executed. |
| Same empty-error failed seat, but report absent and source unchanged. This directly exercises the alleged masquerade route. | Exit 2; `COHORT-SCHEMA`; no `absent_dead` bucket in the returned schema-error result. | None; not executed. |
| Same absent-report seat with a nonempty error, as the existing `dead-missing` positive control (lines 94–95). | Exit 0 accounting PASS; `absent_dead=1`; strict receipt exit 1 remains a separate failed strict-conformance result. | None; not executed. |

The existing `false-death` case uses a delivered report, not an absent report. It nevertheless targets the unconditional settlement guard. The absent-report variant above is an additional source-derived expectation, not a claim that the candidate already executes that variant.

## Single hypothetical mutant and expected detector

**Mutant:** remove only the two-line failed/blank-error guard at cohort lines 44–45. This is a behavior-bearing counterfactual; no candidate bytes were edited.

**Expected detector:** the existing `false-death` selftest case and its assertion at cohort lines 115–118. Without that guard, its delivered valid report would instead produce exit 0 and `delivered_conformant=1`, rather than the expected exit 2 and `COHORT-SCHEMA`; that case would be marked unsuccessful. The absent-report variant would additionally expose the precise defect: exit 0 accounting PASS with `absent_dead=1` despite the empty failure error.

**Actual detector outputs:** none for pristine, hypothetical-mutated, or restored bytes. No baseline success, mutant kill, selftest PASS, or restoration rerun is asserted.

## Preservation and limits

- The assignment supplies target SHA-256 `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0`. This is the declared reviewed identity, not an independently computed digest from this seat.
- Independently measured before/after hashes: unavailable under this source-only tool scope. No source write or mutation was performed, so no restoration operation was needed. The only filesystem write was this authorized findings report; build reports and production files were not changed.
- No commands, imports, tests, examples, network fetches, installations, or subagent dispatch were performed.
- This conclusion is a syntactic empty/blank-error rejection result. A nonblank error string is not authenticated evidence of a genuine provider failure. C3 is post-hoc accounting and detection, not preventive runtime enforcement or proof of actual reading/nonexecution.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3falsedeath
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
