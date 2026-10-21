# FxC2Mode — falsify `structured_edit_mode` (C2, operability)

Attacked claim: C2 (`structured_edit_mode` 0 → 1). Stated semantics: the flag is emitted only for schema v2, equals 1 when exit code is 0 or 1, and equals 0 when the run could not be evaluated. Target: `candidate/tools/check-seat-bindings.py` (declared SHA-256 below; the digest was supplied and not computed). Static reading only; nothing was executed.

## Verdict

No false green. With a v2 manifest, I could not build a recorded trace where an edit outside `edit_paths` returns exit code 0. The flag is honest as an availability bit: it says the audit was evaluated, not that the trace complied. A red v2 audit with mode 1 is also honest, because `status`/exit carry the verdict and the selftest deliberately pins mode to 1 on code-1 cases. However, the claim is weaker than its name suggests, and one stated semantic is falsified. Details follow.

## Falsifier F1 — "0 on could-not-evaluate" does not always hold (fixable defect, low severity)

- In `evaluate()`, lines 142–144 parse the manifest, then parse the events, and only then compute `v2 = ... data.get('schema') == 'tsukuroi-seat-bindings-v2'`.
- Counterexample: the manifest is a valid v2 file, but `events` is malformed JSON (for example a truncated `events.json` at the revision, or a duplicate JSON key, which `unique()` rejects). Then `json.loads(events)` raises before `v2` is assigned, the `except` branch sets code 2, `v2` stays `False`, and lines 205–206 omit `structured_edit_mode` entirely instead of emitting 0.
- The output is CANNOT_EVALUATE with no mode key, for a run whose manifest is v2. A consumer expecting `0` gets an absent value. This is not a false positive, because absence is not 1, but it contradicts the declared semantics. No selftest covers it: `v2_cases` only use dict events, and `v2-schema-typo` is the only expected-absent v2 case.
- Smallest remedy: compute `v2` immediately after the manifest parse, before the events parse. Add one `v2case` with well-formed v2 manifest and events `'{"schema":"tsukuroi-seat-events-v1","seats":[],"seats":[]}'`, expecting code 2 and mode 0.

## Finding F2 — the flag is a gated copy of `request_audit_mode` (tradeoff, so judge it as availability only)

- Lines 199 and 205–206: `request_audit_mode = int(code != 2)` and `structured_edit_mode = int(code != 2)`. Whenever the key is present, the two values are always equal. The selftest oracle uses the same formula (line 300, `int(code != 2) if mode is None`). The selftest therefore checks consistency, not meaning. The mutant `structured_edit_mode = result['request_audit_mode']` would be equivalent, and no case could kill it.
- Vacuity counterexamples, all yielding mode 1:
  - A v2 manifest with a trace that contains no `edit` request at all, giving code 0 and mode 1. Nothing structured-edit-specific was exercised.
  - A v2 manifest where every seat has `edit_paths: []`. This is accepted at lines 157–161 (the list may be empty), and the selftest `v2-empty-edit-paths` gives code 1 and mode 1. Mode 1 holds with zero declared edit authority.
  - A v2 trace containing only `bash`, giving code 1 (SCOPE-EXEC-DENIED), status FAIL and mode 1.
- Mode also turns to 0 for reasons unrelated to edits: an incomplete or missing seat trace (line 194, `incomplete` leads to code 2), or one malformed `read` anywhere in the wave. So the flag is not edit-specific in either direction. It measures two things: whether the manifest declares the schema v2 string, and whether the whole wave was evaluable.
- Is availability being sold as compliance? In the code, no:
  - The selftest pins mode 1 on red v2 cases (`v2-read-only-target`, `v2-undeclared-target`, `v2-url-target`).
  - The preregister C2 scope says "audit authority" and disclaims native enforcement.
  - The risk is at the metric layer. The preregister's `before 0 → target 1` is met by any evaluable v2 run, including a FAIL run and a run with zero edit requests. If someone reads only the metric field, a red, edit-free wave would look like delivered operability.
- Provenance note: `before: 0` is a convention for absence, not a measured 0. The baseline snapshot tool never emits the key (it emits only `request_audit_mode`, at snapshot lines 115 and 167).
- Smallest remedy (in scope, no semantic change to the verdict):
  1. Emit `structured_edit_requests` next to the mode. It would count the events (including nested parallel children) that reached `classify_edit`. Mode 1 with zero requests would then be visibly vacuous.
  2. Let the C2 receipt or judge cite `status` and that count together with the mode, never the mode alone.
  3. Optionally reject or flag v2 seats with an empty `edit_paths` if C2 is meant to show declared authority, not just the schema string.

## Bounded search for a false green (none found)

I checked each candidate against the code paths listed:

- Edit targets in a v2 manifest:
  - Spelling variants (trailing `/`, `./`, `../`, `//`, `:raw` selector, relative path, `skill://`, `xd://`, upper-case) all give `SCOPE-EDIT-DENIED`. The selftest covers each of these at lines 307–308.
  - URL and `host:port/` targets give `SCOPE-FETCH-DENIED`.
  - The collector's projection to `redacted-internal-uri` is not in `edit_paths`, so it is denied.
- Edit arguments and tool names:
  - The `edit` tool under a v1 manifest gives `SCOPE-TOOL-UNKNOWN`.
  - `Edit` and `ast_edit` give `SCOPE-TOOL-UNKNOWN`.
  - `functions.edit`, including inside nested `parallel` calls (the flag is propagated at line 91), is classified.
  - Opaque, mixed, half-filled, or unknown-key edit arguments give `SCOPE-SCHEMA`, so code 2 and mode 0. The same holds for harness-specific edit keys that `collect.py` projects to `__unknown_argument__`.
- Authority markers:
  - A row-level `allow_structured_edit` marker or an event-level marker gives `SCOPE-SCHEMA`.
  - Under v2, edit authority must be a subset of both read and write authority (line 160). The mutants that drop either half are recorded as killed in `l1-mutation.json`.

Result: no path gives code 0 together with an undeclared edit.

## Impacted axes

- Operability (C2): the claim holds as availability only. F1 is a fixable inconsistency in emitting the flag, and F2 means the metric needs companion fields before it can stand for "edits were audited".
- C1 and C3 were not attacked by this seat.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2mode
Scope: executed=none
