source: S086 — .ufo/waves/round-23/sources/structured-edit-observations.json, observations argument_keys/path/recorded_starts; policy: .ufo/waves/round-23/preregister.json edit_decisions
verified-at: 2026-10-21; round23 source packet derived from round22 transcripts at baseline ae01e50f582016384e620022be38bf5367000e2e; landed gate measurements in SCORECARD.md Round23
recheck: python3 tools/check-edit-contract.py --revision <landed-hex>; recheck cadence: 90d

# Structured edit authority for this lane's evidence files

The source is a finite sample of four structured `edit` requests from two round22 seats, with a `path` field and either `stream_content` or `old_string`/`new_string` argument keys. Body values are deliberately omitted. The producer nests recorded starts under each request, but those starts do not carry their own call IDs; one read/write pair precedes its request line and three other requests have edit-only starts. Nesting is producer attribution, not independent causal, reading or effects proof. The sample witnesses metadata shapes, not any permission outcome or a denial instance.

Authority is separately declared lane policy. A source-only report writer can be granted exact prospective report-read/write/edit targets before dispatch; report ownership alone never grants extra reads or an edit. Schema-v1 historical bindings remain unchanged and retain all earlier violations. No grant is retroactive.

All eight table rows are prospective lane-policy decisions; S086 supplies the metadata vocabulary, not normative permission. Any missing leg of the read/write/edit conjunction is non-authorizing, including an edit-only declaration with neither read nor write. In the v2 auditor a malformed authority declaration or an unstructured edit is could-not-evaluate (exit2); a supported edit with a non-declared target is a finding (exit1). This does not enlarge the frozen eight-row target.

These decisions are tsukuroi's finite audit convention for bindings this lane declares and its own recorded steps, not a fleet binding-schema definition or a rule for sibling-owned tools. Supported edit keys are exactly `{path,stream_content}` or `{path,old_string,new_string}`, optionally `i`; body values remain opaque.

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
