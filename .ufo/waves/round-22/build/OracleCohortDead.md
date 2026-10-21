# OracleCohortDead — source-only oracle

## Minimal literal fixture

Smallest valid one-seat manifest shape for `evaluate` (line references below are to the assigned checker source):

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"Dead","report":"r.md","source":"s","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"r22-oraclecohortdead"}]}
```

For this fixture's source read, let `read_bytes("s")` return empty bytes (matching the declared SHA-256). The JSON does not encode the read outcome: it must be supplied by the oracle harness. The two materially different report cases are:

* `read_bytes("r.md")` returns `None`: the checker adds `REVIEW-REPORT-MISSING` at `Dead` (lines 93–100), returns `FAIL`, exit 1, total_reviews 1 and pinned_reviews 0.
* `read_bytes("r.md")` raises `OSError`, `RuntimeError`, or `subprocess.TimeoutExpired`: it adds `REVIEW-READ-FAILED` at `Dead` and continues (lines 93–97); with no other findings, it returns `CANNOT_EVALUATE`, exit 2, total_reviews 1 and pinned_reviews 0. This is not reported as `REVIEW-REPORT-MISSING` for that row.

These are source-derived expected evaluator outcomes, not observed runtime results: I did not invoke the case or execute the checker. The checked-in selftest `read-failed-retains-missing` (lines 210–222) explicitly distinguishes both cases: `One` returns `None`, while `Two` raises `RuntimeError`; its exact expected exit is 2 and finding-ID set is `{REVIEW-REPORT-MISSING, REVIEW-READ-FAILED}`. The selftest asserts total 2 and pinned 0 (lines 233–235).

## Cohort-policy expectation and ambiguity

The requested finite cohort-policy expectation is `absent_dead` for a seat whose run has an independently observed failed outcome and produced no report. This is a policy expectation only, not a verdict observed from the assigned snapshot checker. Preregister C3 names `absent-dead` as a cohort category and says to preserve strict receipt findings; it does not specify the event schema or define whether “observed error” means a run failure or a report/source-read failure.

That distinction matters. If “observed error” means a run-level failure bound to this seat, absent-dead can be the finite policy classification while the separate strict receipt check still reports `REVIEW-REPORT-MISSING` when it successfully observes `None`. If “observed error” instead means the checker’s read exception, this source does not prove the seat died: it classifies the audit as `CANNOT_EVALUATE` / `REVIEW-READ-FAILED`, not absent-dead and not report-missing. A report-read exception is not evidence that the seat's run failed. Thus the fixture alone cannot establish absent-dead; the oracle needs a separately authenticated, identity-bound run-failure observation plus an independently established report absence. Do not collapse read failure into known death or erase the strict missing finding.

## Residual risk and verification gaps

* No runtime result was observed; no case, selftest, or checker was invoked.
* The permitted source set contains no C3 implementation or run-event schema, so the mapping from a particular observed failure to `absent_dead` cannot be independently verified here.
* The checker source describes its scope as declarations only, not proof of actual reading, chronology, or command nonexecution (line 128); neither a cohort classification nor a strict receipt finding establishes those claims.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortdead
Scope: executed=none