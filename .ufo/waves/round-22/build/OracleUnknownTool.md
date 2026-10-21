# OracleUnknownTool — source-only boundary oracle

## Axes
- Exact unknown-tool classification, without conflating it with a known tool outside a seat's scope.
- Minimal fixture and one plausible fail-open defect.
- Honest separation of policy expectation, observed evidence, and unexercised runtime behavior.

## Authorized evidence
- `sources/host-tool-boundary.json:9-12` states that task `tools` are additive extras, not a native-tool allowlist, and that the approved boundary is prompt-level scope plus fail-closed post-hoc audit.
- `preregister.json:6,9-13` identifies C2 request auditing and expressly limits enforcement and recovery claims.
- Neither authorized source supplies the audit event schema, a closed tool-name registry, name-normalization rules, diagnostic precedence, or a serialized verdict enum. The expected diagnostic below is supplied by this assignment, not independently specified by those source files.

## Smallest literal decision fixture

```json
{"tool":"r22_unknown_tool"}
```

This is the minimal logical fixture for the tool-name decision: one nonempty, syntactically ordinary identifier and no path, command, URL, or nested request. Its prerequisite is that `r22_unknown_tool` is absent from the auditor's recognized tool registry. That membership cannot be independently established from the two authorized source files.

This JSON is a decision-input projection, not a claim that it is a complete, schema-valid events file. Any required seat/event envelope must be valid before this decision is tested; its exact representation is unavailable within this seat's read binding. Adding guessed `args`, `arguments`, seat identifiers, or result fields would fabricate a harness contract rather than resolve that gap.

## Exact oracle expectation

- Semantic verdict: **REJECT / nonconformant audit event**.
- Exact policy diagnostic ID: **`SCOPE-TOOL-UNKNOWN`**.
- `REJECT` is oracle notation, not an asserted implementation enum or observed output.
- This is a post-hoc audit expectation. It does not mean the host prevents, intercepts, or rolls back an attempted tool request.

The expected detector is the preregistered C2 request auditor, applied to one otherwise-valid event carrying the fixture's tool name. A conforming detection must reject that event specifically as `SCOPE-TOOL-UNKNOWN`; rejection for a malformed envelope or a different scope violation would not demonstrate this decision.

## One plausible defect challenged

**Mutant:** change the unknown-name/default branch from emitting `SCOPE-TOOL-UNKNOWN` to ignoring the event or accepting it. This is a single behavior-bearing fail-open decision, not a change to the policy contract. No source bytes were mutated in this source-only seat.

The detector should distinguish that mutant from the intended policy: the fixture must not disappear from accounting or receive an acceptable audit result. A nonzero aggregate result alone is insufficient if another event or schema error caused it. If this branch were exercised and the mutant remained acceptable, that would be a coverage finding, not permission to admit unknown tools.

## Ambiguity attack

1. **Unknown versus out-of-scope:** a recognized tool prohibited for this seat is not necessarily an unknown tool. This fixture requires registry absence, not merely absence from a seat's declared scope. Additive task tools establish neither a closed registry nor a wildcard permission.
2. **Name normalization:** the evidence does not specify whether bare names, qualified names, aliases, or normalization are supported. A registry lookup must establish that the selected literal remains unknown after the auditor's actual normalization; spelling alone is not proof.
3. **Envelope and precedence:** an omitted required envelope field could produce a parse/schema failure before tool classification. Conversely, applying path/command checks before unknown-name handling could produce a different diagnostic. Either outcome is inconclusive for this oracle, not a killed mutant.
4. **Runtime interpretation:** a host-level “tool unavailable” response would not, by itself, establish that the C2 audit emitted the required policy ID. Source policy and runtime request handling are distinct boundaries.

## Actual outputs and verdict

| Probe state | Detector invocation | Actual behavioral output |
| --- | --- | --- |
| Pristine | None; NO-EXEC | Not observed |
| Mutated | None; no source mutation and NO-EXEC | Not observed |
| Restored | None; no source mutation and NO-EXEC | Not observed |

**Verdict: INCONCLUSIVE / source-only expectation.** No mutant was killed or observed to survive. The reads established the policy-boundary facts above, but did not exercise a detector. The exact runnable fixture envelope, tool-registry membership, and runtime verdict serialization remain unestablished because their defining files are outside this seat's authorized read paths.

## Hash and restoration evidence

- Source SHA-256 supplied by the assignment: `d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30`.
- Independently computed before/after hashes: not obtained; no hash computation or execution was authorized.
- Before/after source relationship: this seat issued no source writes or edits. Only this report was written. No mutation was applied, so there were no source bytes to restore; this is an operation-history statement, not a measured after-hash assertion.
- No commands, fetches, runtime probes, delegated tasks, installations, or updates were performed.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oracleunknowntool
Scope: executed=none
