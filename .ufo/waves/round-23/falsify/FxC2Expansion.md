# FxC2Expansion — round-23 falsify (EXPANSION / CHECK_EACH)

## Attacked claim

C1 row 8 `EXPANSION / CHECK_EACH` ("Every recorded adapter read or write remains separately scoped"). It reaches C2 through the schema-v2 audit in `candidate/tools/check-seat-bindings.py` and through the event projection in `candidate/collect.py`. Questions asked: (a) does the gate audit each additional recorded start on its own; (b) can a valid edit target clear a backend read or write of another path.

## Axes

- depth (C1 decision fidelity: CHECK_EACH as stated versus as realized)
- operability (C2 `structured_edit_mode` audit soundness)
- calibration of the claim boundary (is "every recorded start" actually every recorded start)

## Result summary

- Gate (C2): no falsifier found. Every event, including `origin: additional-recorded-start` rows, goes through `classify` on its own, and findings are never cleared across events. A valid edit event cannot neutralize a denied read or write event.
- Collector (feeds C2): falsifier found. A same-tool recorded start whose `path` is truncated (`…`) or missing never becomes an event, so the gate never sees it and can return PASS. CHECK_EACH is fail-open for that start class.
- Selftest coverage gap: no v2 fixture shows CHECK_EACH, meaning a valid edit followed by an additional-start read or write of another path.

## Evidence

### Gate audits each event on its own (no falsifier)

`evaluate` loops over every event in `seat['events']` and classifies each one with no reference to `origin`, `call_id` or neighbouring events (candidate `check-seat-bindings.py` lines 181–192). Findings only accumulate. `code` is 1 if any finding exists and 2 if any SCHEMA exists (line 194). Nothing removes a finding.

Bounded search over the ways an additional-start event can be shaped once it reaches the gate:

| Additional-start shape | Gate outcome | Fail mode |
|---|---|---|
| `read` of edit target T | pass (v2 enforces `edit_paths ⊆ read_paths`, line 160) | correct |
| `write` of T | pass (`edit_paths ⊆ write_paths`) | correct |
| `read` of undeclared O | `SCOPE-PATH-DENIED` (line 111–112) | closed |
| `write` of undeclared O | `SCOPE-PATH-DENIED` | closed |
| `read` of O where O ∈ read_paths | pass | correct per CHECK_EACH (separately scoped, separately authorized) |
| `edit` of O, full shape | `SCOPE-EDIT-DENIED` (line 129) | closed |
| `edit` of O, partial shape `{path}` | `SCOPE-SCHEMA` → CANNOT_EVALUATE (line 121) | closed, but the path denial is relabelled as schema and not counted in `violations` |
| unknown adapter name (`read_file`, `apply_patch`, …) | `SCOPE-TOOL-UNKNOWN` (line 79) | closed |
| non-dict start args (projection `None`) | SCHEMA | closed |
| truncated path on a *different* tool start | appended; the ellipsis path fails exact membership, giving `SCOPE-PATH-DENIED` | closed |

Wrapper nesting also forwards `allow_structured_edit` (line 91; mutant 6 in `l1-mutation.json` was killed). So a parallel-wrapped edit child cannot bypass this either.

### Collector drops same-tool starts with a truncated or missing path (falsifier)

`candidate/collect.py` emits an additional event only if `ident in requested and (different_tool or different_path)` (line 275). `different_path` requires that **both** `request_path` and `start_path` are non-`None` (line 272). `scope_path` returns `None` when `path` is missing, not a string, or contains `…` (lines 80–82).

Concrete transcript falsifier (all paths absolute under the lane, seat bound with v2 `edit_paths = [T]`):

    assistant toolCall id=X name=edit args={path: T, old_string, new_string}
    custom tool_execution_start toolCallId=X toolName=edit args={path: "<LANE>/production…", old_string, new_string}

Trace through the collector:
- `different_tool` is false (`edit` == `edit`).
- `start_path` is `None` because of the ellipsis, so `different_path` is false.
- No additional event is emitted. The only effect is a `start_argument_limits` note (line 273–274), which affects neither `complete` (line 255) nor the gate. `evaluate` ignores extra seat keys.

Trace through the gate: the single event `edit T` passes classify_edit, so the result is PASS with code 0. A recorded start whose visible prefix (`<LANE>/production`) is not a prefix of T is never scoped.

The same pass happens when the same-tool start replaces `path` with another key, e.g. `args={file: "<LANE>/production", …}`. `start_path` is `None`, no event is emitted, and the gate returns PASS.

By contrast, a different-tool start (`read`/`write`) with a truncated or missing path *is* appended and fails closed. The fail-open is therefore specific to same-tool starts, and that asymmetry is the defect.

[INFERENCE] I cannot tell from my bound files whether real native adapters emit same-tool starts with truncated or keyless paths. `structured-edit-observations.json` and the wave `events.json` are outside this seat's read binding. The collector's own truncation branch (line 273) shows truncated start metadata is an anticipated input.

### Coverage gap

The v2 fixtures (candidate lines 301–337) contain no event that carries `origin: additional-recorded-start`. They also contain no two-event trace of the form "allowed edit T, then read or write of O". `v2-malformed-then-bash` does cover per-event iteration in general. CHECK_EACH as a named decision has no direct control, so a future skip-by-`origin` regression would not be killed.

## Impact

- C2 gate: holds for what it receives. This is not a gate defect.
- C1 row 8 / CHECK_EACH: the claim "every recorded adapter read or write remains separately scoped" is too strong for the landed pipeline. Same-tool recorded starts with truncated or missing paths are not scoped. This is a fixable defect, not a tradeoff for the judge to reject. The no-runtime-enforcement limit is unaffected.
- Secondary (closed but lossy): a partial-shape `edit` start of an undeclared path becomes `SCOPE-SCHEMA`, not `SCOPE-EDIT-DENIED`, so `violations` undercounts while the result is still CANNOT_EVALUATE.

## Smallest in-scope remedy

1. `collect.py` line 272: stop treating a `None` start path as "same path". Emit the additional event whenever the request and start path identities differ, with one exception: a truncated start path is treated as the same only when its pre-`…` prefix is a literal prefix of the request path. Keyless or non-string start paths are then appended, and the gate fails them closed through SCHEMA. Same-path, same-tool starts stay deduplicated, so legitimate adapters add no noise.
2. `check-seat-bindings.py` selftest: add two v2 controls:
   - events `[edit T (valid), {tool: read, path: O, origin: additional-recorded-start}]` expecting code 1 with `SCOPE-PATH-DENIED`
   - the same with `write O`
   These pin CHECK_EACH so that an `origin`-based skip would be killed.
3. Optional calibration: narrow the C1 row 8 reason to "every recorded start whose tool or path identity is observable" until remedy 1 lands.

## Method

NO-EXEC and NO-FETCH: I only read the bound files with read and grep. I computed no hashes and ran no tools. The baseline snapshot `check-seat-bindings.py` has no edit handling (edit gives `SCOPE-TOOL-UNKNOWN`, snapshot line 199), so the v2 path is new and v1 is not regressed.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2expansion
Scope: executed=none
