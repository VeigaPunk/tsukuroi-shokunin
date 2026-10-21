# ReviewScopeTrailer

Axes: trailer conformance; declaration-versus-event evidence; scope-boundary honesty.

## Findings

- **Medium — conflicting repeated scope declarations are accepted.** In `snapshot/tools/check-seat-scope.py`, `scope_value()` returns the last matching scope line, and `evaluate()` judges only that value. The checker’s own `last-line-clean` selftest expects PASS for a report declaring `probe` and later `none`. Thus a report can contain an earlier explicit command declaration and still be classified clean by ending with a bare `none`. This conflicts with this assignment’s once-only receipt requirement and drops contradictory report evidence. This is a self-declaration inconsistency, not proof that a command actually ran. Require exactly one scope line (and reject conflicting duplicates) if the gate is expected to enforce the once-only contract.

- **Low — this gate does not validate the full three-line receipt.** It extracts only the scope declaration; neither the supplied SHA-256 nor the predicate is parsed or checked. Consequently, a wrong or absent hash/predicate does not affect this gate’s verdict. The required final scope line is interoperable: the exact bare `none` value is normalized and accepted. The gate also does not require that this line be physically at EOF; it uses the last matching line. The assignment’s receipt is stricter and satisfies the gate, but this checker alone does not enforce all receipt details.

## Declaration versus actual events

The checker explicitly describes its counts as declarations, says a bare `none` cannot prove absence of execution, and emits `evidence_class` as self-reported declarations with no independent absence-of-execution proof. This distinction is correct: the final receipt is a declaration, not an observed event record. Round-22 preregistration identifies C2 as a separate request-audit command consuming manifest and event inputs; the host-tool-boundary source says there is no native per-seat allowlist and characterizes the approved design as prompt-level scope bindings plus fail-closed post-hoc audit. Do not describe this scope gate or its `none` result as runtime enforcement or proof of no execution. The C2 checker and event records are outside this seat’s declared read paths, so their implementation and event coverage were not verified here.

## Scope and verification gaps

The assignment declares `commands: []` and `fetches: []`; the supplied checker source was read, not executed. The assignment supplied the target hash, but this seat did not independently compute it under NO-EXEC, and this checker does not verify it. The registry/spec files that determine the seat names and report basenames are outside the declared read paths, so registration of `ReviewScopeTrailer` against this report path was not independently confirmed. No other files or runtime behavior were inspected.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: add541d8b8d4ea7f4c38415bb31f5f9ffbcaeb177aebb2431239bbb489829dac
Predicate: r22-reviewscopetrailer
Scope: executed=none