# FxC2ParallelLocal — C2 parallel transparency and malformed-wrapper falsification

- Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`
- Assigned target digest: `c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4`. The digest was not independently recomputed: this seat is NO-EXEC, so no hashing/subprocess was run.
- Predicate: `r22-fxc2parallellocal`
- Method: literal reads of the declared local paths only; source trace only; no execution, mutation, fetch, or edit. "Observed runtime" below is explicitly **not** produced: no fixture was run.

## Claim under attack

1. A transparent parallel wrapper whose leaves are allowed local requests must classify as PASS (exit 0, no wrapper-level finding).
2. A parallel wrapper whose syntax is malformed must classify as CANNOT_EVALUATE (exit 2, `SCOPE-SCHEMA`), not PASS and not a plain scope FAIL.

## Source facts

- `classify` (lines 59–88) recognizes wrappers by exact name at line 63: `('multi_tool_use.parallel', 'parallel')`.
- Wrapper shape checks at lines 64–70: `tool_uses` must be a non-empty list; each child must be a dict, else `ValueError`.
- Children are recursively classified at line 71 with the same binding; the wrapper adds no finding itself.
- The `functions.` namespace strip (lines 73–74) runs **after** wrapper dispatch; the exec/fetch/leaf name tests follow at lines 75–80.
- `evaluate` calls `classify` at line 138; a `ValueError` is caught at lines 145–147, which adds `SCOPE-SCHEMA` and sets code 2; line 149 maps code 2 to `CANNOT_EVALUATE`.
- Selftest anchors: `qualified` leaf `functions.read` is expected PASS at line 163; `parallel-local` (unqualified) expected 0 at line 182; `parallel-malformed` (`tool_uses: [None]`, unqualified) expected 2 with `SCOPE-SCHEMA` at line 183.

## Clause 1 — transparent parallel with allowed local leaves

For the unqualified spelling, this holds by construction. The wrapper branch returns only the union of child findings; each child is classified with the same binding; allowed leaves (`read`/`grep`/`glob` on declared read paths, `write` on the exact write path, `skill://godspeed`) produce no findings, so the event adds zero findings and exit stays 0. This matches the `parallel-local` fixture expectation at line 182.

Counterexample at the namespace boundary: a parallel wrapper recorded as `functions.multi_tool_use.parallel` (or `functions.parallel`) never enters the wrapper branch at line 63 because the `functions.` strip occurs at lines 73–74, after dispatch. After stripping, the name becomes `multi_tool_use.parallel`, but the wrapper branch is not revisited; the name is not in the exec/fetch/leaf sets, so line 80 returns `['SCOPE-TOOL-UNKNOWN']`. A schema-accepted trace whose only leaf is the declared read path therefore yields exit 1 (`FAIL`) instead of exit 0.

This is not hypothetical input outside the tool's own name space: line 163 explicitly accepts the `functions.`-qualified spelling as equivalent for leaf tools, and the parallel fixtures themselves use `functions.read`/`functions.bash` as child recipients (lines 180–182). The normalization is asymmetric for the wrapper name.

## Clause 2 — malformed wrapper syntax must be CANNOT_EVALUATE

For the unqualified spelling, this holds. Each malformed shape raises `ValueError` before any result:
- missing / non-list / empty `tool_uses` → line 66;
- non-dict child (the line 183 fixture payload `[None]`) → line 70;
- child with missing/empty `recipient_name`, non-dict `parameters`, or a leaf without `path` → lines 61 or 83.

`evaluate` catches the error at lines 145–147, adds `SCOPE-SCHEMA`, sets code 2, and line 149 reports `CANNOT_EVALUATE`. The line 183 fixture therefore passes by construction.

Counterexample at the same boundary: with tool name `functions.multi_tool_use.parallel` and the **exact** malformed payload `{'tool_uses': [None]}`, the wrapper branch is skipped, line 74 strips the prefix, and line 80 returns `['SCOPE-TOOL-UNKNOWN']` without examining `args` at all. No `ValueError` is raised, so `evaluate` returns exit 1 (`FAIL`) with `SCOPE-TOOL-UNKNOWN`, not exit 2 (`CANNOT_EVALUATE`) with `SCOPE-SCHEMA`. The malformed wrapper syntax is never evaluated; the strict "must cannot-evaluate" clause is breached for any qualified wrapper spelling.

## Expected fixture verdict vs observed

| Case | Expected (fixture / invariant symmetry) | Observed runtime | Source-traced outcome |
|---|---|---|---|
| `parallel-local`, unqualified (line 182) | PASS, exit 0 | not executed (NO-EXEC) | PASS, exit 0, no findings |
| `parallel-malformed`, unqualified (line 183) | CANNOT_EVALUATE, exit 2, `SCOPE-SCHEMA` | not executed (NO-EXEC) | CANNOT_EVALUATE, exit 2, `SCOPE-SCHEMA` |
| qualified `functions.multi_tool_use.parallel`, allowed leaf | PASS, exit 0 (symmetry with lines 163/182) | not executed (NO-EXEC) | FAIL, exit 1, `SCOPE-TOOL-UNKNOWN` |
| qualified `functions.multi_tool_use.parallel`, `tool_uses: [None]` | CANNOT_EVALUATE, exit 2, `SCOPE-SCHEMA` | not executed (NO-EXEC) | FAIL, exit 1, `SCOPE-TOOL-UNKNOWN` |

The two rightmost rows have no fixture in the checked source; their expected values follow from the stated invariant plus the qualified-leaf precedent at line 163. No runtime observation exists because execution is prohibited; the source-traced outcomes are deterministic readings of lines 61–80 and 138–149, not runs.

## Bounds, severity, and remaining unknowns

- The breach is a false FAIL / missing CANNOT_EVALUATE, never a false PASS for malformed wrapper syntax. Fail-closed posture is preserved; classification fidelity is not.
- If the event contract were to fix wrapper spelling to the two literal names, the defect would be latent rather than reachable. The checked source and fixtures state no such restriction, and the same classifier canonicalizes `functions.`-qualified leaf names, so the qualified wrapper is admitted by the input schema as written.
- The selftest cannot detect this: there is no qualified-wrapper case; lines 182–183 use only the unqualified name.
- The `depth > 8` guard and unknown-tool denial remain fail-closed and consistent with the malformed/evaluated distinction, except that deep-but-well-formed nesting also returns CANNOT_EVALUATE (a documented bound, not a counterexample here).
- Not assessed here: actual request-recorder spelling of wrapper names (build artifacts and fixtures outside this seat's declared read paths), independent digest verification (NO-EXEC), and any production fix (no edits permitted).
- No production files were modified; this report is the only write.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2parallellocal
Scope: executed=none
