# Crit23OpaqueBody — round 23 critic report

Seat: Crit23OpaqueBody (leaf critic, NO-EXEC, NO-FETCH). Lane bounds: leaf member, so no subagent dispatch.
Inputs read: `preregister.json` (declared digest supplied, not recomputed), `sources/r22-closure.json`, `sources/structured-edit-observations.json`, and `sources/godspeed-directive.txt` (the copied directive, used in place of `skill://godspeed`). No commands, fetches, installs or other paths. This report covers the preregistered contract and the S086 observation source. I had no landed C1 or C2 implementation bytes in scope, so every statement about checker behavior is marked [INFERENCE].

Target: whether structured path metadata (`argument_keys`, `path`, `recorded_starts`) can be used as proof of opaque-body semantics or of multi-target effects.

## Verdict

These are fixable defects; none is fatal. The preregistered edit-decision table and the C2 scope ("Body data opaque, no native enforcement/effects claim") are sound only if three conditions hold:

1. ALLOW means "the request's structured target is authorized". It must not mean "the edit only touched that target".
2. Recorded adapter starts are attached to a request through an explicit join key. Line position must not be used.
3. One literal selector rule exists for recorded read paths.

The S086 evidence contains a concrete counterexample to the second and third conditions. The decision table also has an undefined precedence that breaks the first.

## Counterexample 1: recorded starts come before their request (join-key gap)

Evidence (`structured-edit-observations.json`, CritRuntime): the edit request is at `request_line: 15` (call_id `toolu_014nToY7USd3cckcqeieNJ4o`, keys `path`, `stream_content`). Its `recorded_starts` are at lines 12 (`read`) and 13 (`write`), both before the request line. For OraclePathArtifact, each start sits at `request_line + 1` (30→31, 33→34, 36→37).

The two seats therefore use opposite orderings, and the start records carry no `call_id` or other join key. No single positional rule ("next lines after the request" or "nearest preceding lines") attributes both seats correctly:

- A "following lines" rule drops CritRuntime's read and write. That request then shows an ALLOW with no checked adapter effects, which is a false green.
- A "preceding lines" rule assigns OraclePathArtifact's line-31 start to nothing, or to the line-30 request's predecessor.

The observation file shows that someone made an association, but not how [INFERENCE]. A checker that copies the association from this file inherits an undocumented authority.

Impacted axes: operability (C2's EXPANSION / CHECK_EACH row cannot be evaluated deterministically) and calibration (false provenance: an association presented as observed when it was actually derived).

Smallest correction: give each recorded start the parent `call_id` (or the transcript's tool-call id) in the v2 events capture. A start without that key gets the decision UNKNOWN; it is never joined by line distance. This is a data-shape addition to the C2 capture and a one-sentence contract rule. It does not change any historical record.

## Counterexample 2: a `:raw` selector on a recorded read conflicts with EDIT_TRAVERSAL

Evidence: CritRuntime's line-12 start reads `.../round-22/build/CritRuntime.md:raw`, while the declared target is `.../CritRuntime.md`. The preregistered rows conflict on this input:

- EDIT_TRAVERSAL: "No dot-segment or alternate spelling expands the target list." The `:raw` suffix is an alternate spelling. Under exact matching, the read start is DENY, so a legitimate DECLARED_EDIT becomes a false red.
- If the checker silently strips selectors so the read passes, the suffix-stripping is an unstated normalization that accepts alternate spellings. That contradicts EDIT_TRAVERSAL's literal text.

r22 closure (`verification.rechecks`) attributes the rough 25/33 versus lane 23/29 census gap to "selector-normalization differences". So selector handling also drives C3. If C2 v2 and C3 each define selector handling implicitly, there are two authorities. If they disagree, C3's explanation of the r22 gap and C2's audit of the same path shape contradict each other.

Impacted axes: operability (C2 false red or silent widening), calibration (C3 explanation depends on an undeclared rule), and depth (C1 table is ambiguous on this input).

Smallest correction: state one finite literal rule in the C2 v2 contract, for example:

    recorded read start whose path equals a declared read target plus exactly ":raw" → same target
    any other suffix, selector or spelling → UNKNOWN

C3 then records its own frozen r22 rule as a separate declared input. It must not claim equivalence with C2, which also respects the separability clause that C3 never reads C1/C2 content.

## Counterexample 3: structured `path` plus an opaque body (undefined precedence between DECLARED_EDIT and OPAQUE_PATCH)

Evidence: CritRuntime's request keys are `path` and `stream_content`, and the body is "omitted; no report text copied". The table has two separate rows:

- DECLARED_EDIT → ALLOW when the structured target is declared.
- OPAQUE_PATCH → UNKNOWN when there is no structured target.

It has no row for a structured target that is present while the body is an opaque stream. That body could carry its own targets or rename/move semantics; `stream_content` is not interpreted, by design. A patch-format body naming a second file under a declared `path` would get ALLOW from the table as written. Its extra effect would only show up if the adapter recorded a start for it, and the limits explicitly disclaim recorder completeness. So when no extra start is recorded, that absence proves nothing.

Impacted axes: depth (the eight decisions do not cover this case, so C1's "validated" count overstates its coverage) and no-harm/provenance (an ALLOW could be read as single-target effect proof, which the limits forbid).

Smallest correction, contract text only:

1. ALLOW is scoped to request-target authority, with this wording in the C1 rationale and C2 output: "structured target authorized; body opaque; effects not proven".
2. Each tool has a closed whitelist of known structured argument-key sets, taken from S086: `{path, stream_content}` and `{i, new_string, old_string, path}`. Any other key set returns UNKNOWN, never ALLOW.
3. Aggregation precedence is DENY > UNKNOWN > ALLOW across the request decision and every linked recorded-start decision.

## Counterexample 4: recorded `edit` starts fall outside CHECK_EACH

Evidence: OraclePathArtifact's three recorded starts all have `tool: "edit"`. They are not read/write pairs. The EXPANSION row says "Every recorded adapter read or write remains separately scoped", which literally does not cover an `edit` start. A recorded `edit` start on an undeclared path would escape CHECK_EACH [INFERENCE about a literal implementation].

Also, the old_string/new_string request implies a read, but no read start is recorded. The WRITE_ONLY_EDIT requirement therefore has to be checked against the request's declared target, not against recorded starts.

Impacted axes: operability (C2 coverage hole).

Smallest correction: CHECK_EACH covers every recorded start of any tool. A recorded `edit` start needs both read and write authority for its path, the same as DECLARED_EDIT.

## Fixable defects versus judge rejections

All four corrections above fit inside the C1/C2 document and capture contract. None touches history, and none needs native enforcement.

The canonical judge should **reject** a landed C1/C2 if any of the following holds:

- It describes DECLARED_EDIT ALLOW as proof of single-target effects or body semantics.
- It joins recorded starts to requests by line proximity.
- It strips `:raw` (or any other selector) without a declared literal rule.
- It counts the structured-path-plus-opaque-body case as covered by the eight validated decisions.

These are false provenance or premature saturation, not acceptable tradeoffs.

Tool installs or updates: none. The seat scope is NO-EXEC.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23opaquebody
Scope: executed=none
