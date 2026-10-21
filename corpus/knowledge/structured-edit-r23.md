source: S086 — .ufo/waves/round-23/sources/structured-edit-observations.json, observations argument_keys/path/recorded_starts; policy: .ufo/waves/round-23/preregister.json edit_decisions
verified-at: 2026-10-21; source snapshot baseline ae01e50f582016384e620022be38bf5367000e2e; final gate measurement recorded in SCORECARD
recheck: python3 tools/check-edit-contract.py --revision <landed-hex>

# Structured edit authority for this lane's evidence files

The source observes structured `edit` requests with a `path` field and either `stream_content` or `old_string`/`new_string` argument keys. Body values are deliberately omitted. Recorded native steps include report reads/writes under the same parent call ID. These observations establish those finite metadata shapes, not universal editor semantics or proof of effects.

Authority is separately declared lane policy. A source-only report writer can be granted exact prospective report-read/write/edit targets before dispatch; report ownership alone never grants extra reads or an edit. Schema-v1 historical bindings remain unchanged and retain all earlier violations. No grant is retroactive.

## Decision table

| ID | Decision | Reason | Evidence | Policy |
|---|---|---|---|---|
| DECLARED_EDIT | ALLOW | Exact target is predeclared for edit and for both read and write | S086 | round23-preregister |
| UNDECLARED_EDIT | DENY | No implicit edit permission from generic report ownership | S086 | round23-preregister |
| READ_ONLY_EDIT | DENY | Read authority never grants a write | S086 | round23-preregister |
| WRITE_ONLY_EDIT | DENY | Edit also needs its explicit target read authority | S086 | round23-preregister |
| OPAQUE_PATCH | UNKNOWN | Missing structured target is not inferred from opaque patch text | S086 | round23-preregister |
| EDIT_TRAVERSAL | DENY | No dot-segment or alternate spelling expands the target list | S086 | round23-preregister |
| EDIT_EXTERNAL | DENY | Remote or internal URIs do not become filesystem edit targets | S086 | round23-preregister |
| EXPANSION | CHECK_EACH | Every recorded adapter read or write remains separately scoped | S086 | round23-preregister |

## Bounded procedure

1. Freeze explicit schema-v2 `edit_paths` as canonical literal subsets of both read and write targets. A malformed authority declaration is non-clean before interpreting an event.
2. For a recorded structured edit, require the exact declared target and one of the two observed finite argument-key shapes, with only separately allowed metadata keys. Opaque body data is not interpreted or executed by the auditor.
3. Missing structured targets, freeform patches, unknown keys, URI targets and alternate path spellings never gain authority by inference. Unknown means could-not-evaluate or rejection, never permission.
4. Audit every captured native read/write expansion against its own authority. A valid frontend target cannot clear an out-of-binding backend step or a forbidden command/fetch.

This is declared post-hoc audit authority only. It is not native permission enforcement, a sandbox, body/patch interpretation, actual reading or effects proof, complete recorder coverage, or permission for host/package/service/boot actions. The task API still has no restrictive per-seat allowlist. Numeric mode availability is not compliance.

## QUALITY check

The eight finite policy decisions are falsifiable, with observed source metadata separated from normative authority (QUALITY1/3/7/19/45). Independent literal positive/negative controls must check every row, source/policy mapping and refusal class; source-only opinions are not empirical runs. QUALITY42/46–48 require frozen inputs, actual request precedence and honest incomplete evidence. This deepens held evidence-operability ground, not an uncovered frontier, repertoire addition or outside promotion. Final admitted/rejected decisions and actual measurements belong to the round23 lesson and SCORECARD; no unrun result is asserted here.
