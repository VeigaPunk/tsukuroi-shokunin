# FxC2Unknown — source-only falsification of `check-seat-bindings.py`

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2unknown
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.

Note: the SHA256 above is the assignment's declared target digest. This seat cannot hash files under NO-EXEC, so the bytes were not independently hashed. Reviewed bytes: `candidate/tools/check-seat-bindings.py`, read in full.

## Verdict

The tool-name claim holds within its bounds. Every tool name outside the literal set `{read, grep, glob, write}` (after one `functions.` prefix strip, with exec and fetch names handled first) returns `SCOPE-TOOL-UNKNOWN` at `classify` lines 79–80. That happens before any argument inspection, so `edit`, `wait`, `Edit`, `WebFetch`, `mcp__rea_*`, homoglyph names, names with trailing whitespace or NUL, and `functions.functions.bash` cannot reach an allow branch. No tool name is allowed implicitly.

There is one residual defect, on the argument axis of the same UNKNOWN decision. The decision row says "unrecognized tool **or malformed arguments** → DENY", but on allowed tools the classifier inspects only `args['path']`. Argument keys it does not recognize are ignored silently, which is an implicit allow.

## Bounded reasons the name claim holds (source lines)

- Line 61: a non-string or empty `tool`, or a non-dict `args`, raises `ValueError`. That becomes `SCOPE-SCHEMA` with exit 2, which is nonclean.
- Lines 63–72: parallel wrappers recurse per child, with depth bounded at 8. A child `recipient_name` of `functions.edit` or `wait` reaches line 80, so it is UNKNOWN. A missing or non-string `recipient_name` raises SCHEMA. The wrapper check runs before the prefix strip, so `functions.parallel` and `functions.multi_tool_use.parallel` become UNKNOWN rather than being unwrapped. That fails closed.
- Lines 73–74: the strip happens once only. `functions.functions.read` stays UNKNOWN, so the strip cannot widen anything.
- Lines 79–80: the allow set is an exact tuple membership test. There is no case folding, prefix match, or normalization, so nothing passes by default.
- Lines 139–142 in `evaluate`: every returned id is appended to `findings`, and line 144 then gives exit 1 (FAIL). UNKNOWN can never be dropped from `findings` or from the code.

## Expected fixture verdicts (not executed; derived from source)

| Fixture event (seat A, complete trace) | Expected exit | Expected finding ids |
|---|---|---|
| `edit`, `{}` | 1 | `SCOPE-TOOL-UNKNOWN` (already in the selftest) |
| `wait`, `{}` | 1 | `SCOPE-TOOL-UNKNOWN` |
| `functions.wait`, `{}` | 1 | `SCOPE-TOOL-UNKNOWN` |
| `Read`, `{path: src}` | 1 | `SCOPE-TOOL-UNKNOWN` |
| parallel `[functions.edit {}]` | 1 | `SCOPE-TOOL-UNKNOWN` |
| `functions.parallel`, `{tool_uses:[read src]}` | 1 | `SCOPE-TOOL-UNKNOWN` |
| `edit`, `null` args | 2 | `SCOPE-SCHEMA` (nonclean, but the UNKNOWN id is not emitted) |
| `glob`, `{path: src, pattern: "/home/vgpnk/**"}` | **0 PASS** | none — counterexample below |
| `grep`, `{path: src, glob: "../../**", pattern: "x"}` | **0 PASS** | none — counterexample below |

Observed runtime: none. No fixture, import, or selftest was run (NO-EXEC).

## Counterexample (argument-axis implicit allow)

```json
{"tool": "glob", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json", "pattern": "/home/vgpnk/.ssh/*"}}
```

The bound path is in `read_paths`. Lines 81–91 check only `path`, so this returns `[]`. The seat counts as clean, and the overall result is exit 0 PASS if nothing else fails.

[INFERENCE] The harness semantics are not proven here, because tool docs were out of seat scope. If the host `glob` tool honours an absolute or traversing `pattern`, or `grep` honours a `glob` filter outside the base, this request names out-of-scope paths while the audit reports clean. That contradicts the UNKNOWN row's "malformed arguments → DENY" and LOCAL_READ's "only literal bound source paths". Even if the host clamps `pattern` to `path`, an argument key the auditor does not understand is still not inspected, and that is the definition of an implicit allow. The same gap covers any future path-bearing key the auditor has not seen, such as `paths` or `sel`.

Secondary gaps:

- The selftest has only one UNKNOWN case, `edit` (line 178). There is no fixture for `wait`, for a qualified unknown, or for an unknown nested in a parallel wrapper. The logic is correct, but those properties are not pinned against regression.
- When an unknown tool is paired with malformed arguments (`edit` with null args), the result is SCOPE-SCHEMA, and the raise at line 61 aborts evaluation of the remaining seats. The result stays nonclean, so this is a tradeoff, not a defect.

## Impacted axes

- **Operability (C2 `request_audit_mode`)**: a clean audit can hide an out-of-binding selector carried in an argument key that is not checked. The contract's UNKNOWN decision for "malformed arguments" is enforced only for the `path` key.
- **Depth (C1)**: the UNKNOWN decision row overstates what the C2 checker implements for arguments.
- **Calibration**: none.

## Smallest safe correction

1. In `classify`, fail closed on any argument key outside a per-tool allowlist:
   - `read`: `{path, offset, limit}`
   - `write`: `{path, content}`
   - `grep`: `{path, pattern, -A, -B, -C, -i, output_mode, head_limit, offset, multiline, type}`, with `glob` and `type` either forbidden or validated
   - `glob`: `{path}`, with `pattern` required to be a relative pattern with no `/`-anchor, no `..`, and no controls; otherwise deny it outright for source-only seats

   Unexpected keys should map to `SCOPE-TOOL-UNKNOWN`, or to a new `SCOPE-ARGS-UNKNOWN`.
2. Add negative selftest fixtures:
   - `wait`
   - `functions.edit`
   - a parallel wrapper whose child is `edit`
   - `glob` with an absolute `pattern`
   - `grep` with an out-of-scope `glob`
   - `read` with an extra key such as `paths`

No production edits were made by this seat.
