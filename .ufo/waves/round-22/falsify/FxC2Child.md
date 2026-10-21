# FxC2Child — "task delegation denied even read-only child"

Candidate: `candidate/tools/check-seat-bindings.py`
Reviewed digest: declared `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`; not recomputed here (hashing is shell execution, forbidden in this seat).
Method: source-only reading of the candidate, `_revision.py`, `preregister.json`, `sources/host-tool-boundary.json`, and `corpus/knowledge/seat-boundary-r22.{json,md}`. No execution, no imports, no mutations.

## Attack

The auditor classifies every recorded `task` request as `SCOPE-EXEC-DENIED`, including a request whose `tasks[]` payload would spawn a child restricted to the parent's declared read paths. If that were an over-broad false positive, C2's post-hoc audit would report a violation for a request that never executed anything and whose child never left the bound read set.

## Verdict

**The attack fails; the candidate holds.** The denial is by tool identity, is the declared policy surface, and is the only finite fail-closed classification the audited schemas can support. The attack is also not independently checkable from the record it attacks: the schemas carry no child scope and no child event stream.

## Observed source facts

1. `classify()` strips a `functions.` prefix (`check-seat-bindings.py:73-74`) and then unconditionally returns `SCOPE-EXEC-DENIED` for `bash`, `eval`, or `task` (`:75-76`). This branch precedes any inspection of `args` beyond the `isinstance(args, dict)` guard at `:61`, and precedes `path` extraction at `:81`. A `task` event's `tasks[]`, `tools`, or prose is never parsed.
2. The fixture encodes the same rule: `for tool in ('bash', 'eval', 'task'): case(tool, tool, {}, 1, 'SCOPE-EXEC-DENIED')` (`:167-168`). The fixture uses empty args, proving the expected verdict is driven by the tool spelling, not by a claimed effect. Consequence: a well-formed read-only-child payload and an empty payload are indistinguishable to `classify`.
3. The binding schema has no delegation field. Each seat must satisfy `root == LANE`, `commands == []`, `fetches == []` (`:108-110`); only `read_paths`/`write_paths` are validated (`:111-115`). There is no `tools`, `children`, `delegation`, or child-binding key, so a read-only-child carve-out cannot be expressed in the manifest the auditor consumes.
4. The event schema carries no child trace. Each seat supplies `events`, each event is `{tool, args}` only, and `evaluate()` audits them one by one (`:134-141`, especially `ids = classify(event.get('tool'), event.get('args'), binding)` at `:138`). A spawned child's reads are never merged into the parent's `events`, and `evaluate()` does not recurse into child seats.
5. The host boundary removes the premise of the attack. `sources/host-tool-boundary.json` records `tools_semantics: "Eval-defined additive extras; not an allowlist or replacement of native tools."` and `native_per_seat_allowlist: false` (Main-confirmed). Therefore `task` with `tools: ["read"]` does not restrict the child's native tools: "read-only child" is not a dispatch-verifiable category on this host, only a description in prose.
6. The policy table names this exact surface. `corpus/knowledge/seat-boundary-r22.json` NO_EXEC: surface `bash/eval/task`, decision `DENY`, reason "No execution or delegation in source-only seats". The markdown repeats that seats "are instructed never to invoke other tools, commands, or URLs". The seat contract here likewise states "All roles leaf; no child task". The denial is therefore declared policy, not an inference the checker invents.
7. Declaration scope is explicit and disclaims the only escape hatch: `SCOPE = 'Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.'` (`:17`).

## Why no source-visible allow exists

I enumerated every exit-0 path: `classify` allows only `read`, `grep`, `glob`, `write` (`:79`), with exact bound paths (`:86-91`). `task` reaches `:75` before any such path. Alias checks:

- `functions.task` → stripped at `:73-74` → denied at `:75-76`.
- `task` inside `multi_tool_use.parallel` → recursion at `:62-72`, child denied at `:75-76`.
- `Task`, `task_*`, or another delegation spelling → `SCOPE-TOOL-UNKNOWN` at `:79-80`, exit 1; still fail closed, no allow.
- `functions.multi_tool_use.parallel` → the parallel branch at `:62` tests the *unstripped* name, so this spelling falls through the prefix strip to `:79-80` and is reported as `SCOPE-TOOL-UNKNOWN` rather than recursing. Exit 1 either way; a mis-identified finding id, not an allow.
- Nesting deeper than 8 wrappers → `ValueError` at `:61-62` → `SCOPE-SCHEMA`, exit 2; fail closed.

No recorded spelling reaches delegation through an allowed branch. The candidate cannot both permit a read-only child and remain faithful to `SCOPE`, the NO_EXEC decision, and `native_per_seat_allowlist: false`.

## Expected fixture verdict vs observed runtime

Expected fixture verdict, for a schema-conforming single-seat binding and event `{"tool":"task","args":{"tasks":[{"task":"read bound paths only","solutionSpace":"one fix: read","tools":["read"]}],"i":"read-only child"}}`:

    exit code: 1
    findings: [{"id":"SCOPE-EXEC-DENIED","site":"A:0"}]
    status: FAIL
    request_audit_mode: 1
    violations: 1
    seats[0].violations: ["SCOPE-EXEC-DENIED"]

Expected fixture verdict, for the nearest asserted case (`task` with `{}`): exit 1, `SCOPE-EXEC-DENIED`, per `:167-168`. Identical to the read-only payload outcome because the branch at `:75` is unconditional.

Observed runtime: **none**. The seat is NO-EXEC, so `--selftest` was not run and no runtime verdict is claimed. The digest was likewise not recomputed. This report compares a source-determined expectation against an explicitly unobserved runtime.

Fixture coverage gap (bounded): no selftest case asserts a well-formed `task` payload with `tasks[]` or `tools`. The behavior is fixed by `:75-76`, but the fixed negative fixtures do not pin it. Adding such a case would strengthen the fixture set; its absence is a coverage gap, not a divergence, and does not make the attack true.

## Bounded residuals (not the attack, no allow)

- Missing manifest: `evaluate(None, ...)` returns `request_audit_mode: 0`, status FAIL, `SCOPE-BINDINGS-MISSING` (`:99-100`). If `build/bindings.json` is not committed at the evaluated revision, C2's preregistered `request_audit_mode` metric reads 0 even though the audit code path exists. Fail-closed, but C2 scoring depends on the manifest being committed.
- Empty trace: `complete: true` with `events: []` yields exit 0 (selftest `empty-trace`, `:188`). A dead seat whose trace is nonetheless marked complete with no events would read clean here. This auditor cannot see finals; the DEAD decision defers that to receipt/cohort accounting, and `:17` disclaims trace completeness.
- The auditor validates recorded spellings, not resolution: a `read` event spelled with an exact bound path proves neither the resolved inode nor that reading occurred (`:17`). This is a declared limit, not an allow for delegation.

## Confidence and remaining unknowns

Confidence: high that every recorded `task` spelling yields `SCOPE-EXEC-DENIED` and exit 1 (branch is unconditional and fixtures agree); high that no delegation spelling reaches an allow branch; medium that the event schema is exhaustive, because that conclusion is bounded by `SCOPE` ("universal trace completeness" not claimed).

Remaining unknowns:

- Contents of `.ufo/waves/round-22/build/events.json` and `bindings.json` are outside this seat's declared read paths, so whether any real seat issued `task` is not observable here.
- Only the declared digest of `check-seat-bindings.py` was reviewed; any later revision is out of scope.
- No runtime confirmation of the expected fixture verdict, by design (NO-EXEC).

Conclusion: "task delegation denied even read-only child" describes the intended, declared behavior. The candidate does not over-report relative to its own policy and schemas: on this host a read-only child is unverifiable at dispatch (`tools` is not an allowlist), invisible to the parent trace, and inexpressible in the binding. Denial by tool identity is the correct finite verdict; the only actionable finding is the missing fixture that would pin the read-only-child payload.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2child
Scope: executed=none
