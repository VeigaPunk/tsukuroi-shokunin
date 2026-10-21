# Round 22 source-only oracle: failed with no observed error

Axes: depth, adjacency, coverage, operability, freshness, calibration. This review exercises calibration/policy interpretation only; the case was not invoked.

## Minimal literal manifest fixture

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","report":"r","source":"s","sha256":"0000000000000000000000000000000000000000000000000000000000000000","predicate":"p"}]}
```

This is the smallest valid one-row manifest shape accepted by `evaluate`: the schema and nonempty `reviews` array are required, and a row requires all five fields validated at `check-review-snapshots.py:63-78`. The zero digest is syntactically valid; the source bytes need not be examined if reading `s` fails. The manifest alone does **not** encode a read failure or an absent error observation: `evaluate` receives the reader separately.

## Finite policy expectation and ambiguity

For the fixture above, if the reader raises a caught `OSError`, `RuntimeError`, or `subprocess.TimeoutExpired` while reading `s`, the source predicts exactly **CANNOT_EVALUATE** (return code 2), with finding ID **REVIEW-READ-FAILED** at site `A`. The exception branch adds that ID and sets `read_error` (`:83-89`); the final status mapping selects CANNOT_EVALUATE for a read error (`:119-127`). Exception text is not required, so an empty-message exception still has an observed failure signal.

But “failed with no observed error” does not specify that exception branch. If it means the reader returned `None` for `s` without raising, the checker instead records **FAIL** (return code 1), finding ID **REVIEW-SNAPSHOT-MISMATCH** at `A` (`:90-91`, `:121-127`), assuming the report read is valid and conforms. If the entire manifest read returned `None`, it is **FAIL / REVIEW-MANIFEST-MISSING** (`:56-59`), not CANNOT_EVALUATE. Thus the stated CANNOT_EVALUATE expectation is sound only when “failed” denotes an observed caught read exception; absence of an observed error is not itself represented in the JSON and does not imply that result. The source does not establish a runtime observation for this case.

No case invocation, test, or command was performed. No LSP device was exposed in the authorized tool set, so no LSP semantic query was available; conclusions above are directly grounded in the permitted source lines.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortfalsedeath
Scope: executed=none