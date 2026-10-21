# OracleV2Legacy — v1 `edit_paths` inertness, absence-vs-defect, and literal v2 edit-authority fixture

Axes: (A) source-faithful inertness proof for v1 data, (B) separation of missing capability from historical-policy defect, (C) independence/executability of the fixture, (D) legacy-v1 invariance. No execution was performed; every behavioral statement below is either a quoted source fact or an explicitly marked inference.

Bound sources: `snapshot/tools/check-seat-bindings.py` (declared digest 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6), `preregister.json`, `sources/edit-decision-policy.json`, `sources/structured-edit-observations.json`. The production v2 checker, the wave `bindings.json`/`events.json`, and r22 event files are outside this seat's read set and are not characterized here.

## 1. Verdict

1. **v1 extra `edit_paths` is inert, not authoritative.** In the bound v1 gate the key is never read: `edit_paths` and `structured_edit_mode` do not occur anywhere in the module, and `'edit'` occurs only as the selftest expectation `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')` (L199). A v1 manifest carrying `edit_paths` evaluates identically to the same manifest without it, for every trace.
2. **This is absence of a new capability, not a defect in the historical policy.** The v1 gate is a closed vocabulary over recorded request spellings. `edit` is outside that vocabulary, so `SCOPE-TOOL-UNKNOWN` is the correct v1 output; it asserts nothing about adapter capability, authorization, or effects. No v1 invariant is violated by edit data because no edit data reaches a decision.
3. **C2 therefore cannot be reached by manifest data.** It requires a distinct schema-level authority with its own decision table, its own edit-target validation, and its own metric. A v1 document plus `edit_paths` must keep `structured_edit_mode` at 0.
4. **Legacy reds stay red.** The v2 gate must not re-read, rewrite, upgrade or retroactively authorize r22 manifests/events; the v1 evaluator must remain behaviorally frozen for v1 inputs. Exclusivity must be selected by the `schema` string, never by a flag applied to v1 data.

## 2. Observed source facts (v1 gate)

Quoted anchors, with line numbers from the bound snapshot:

- L2 docstring: `"""Audit recorded requests against frozen prompt scopes; not preventive enforcement."""` — the instrument claims post-hoc audit of recorded spellings only.
- L33-36 `local()`: requires `LANE + '/'` prefix, no `\`, no `unicodedata` Cc/Cf/Cs/Zl/Zp controls, no `*?[];:`, and no empty/`.`/`..` segments.
- L43-58 `requested_path()`: remote fetch patterns (`^https?://`, `host:port/`) return `SCOPE-FETCH-DENIED` before any local check; the only URI exception is `skill://godspeed`; selectors are stripped only when `selector=True`; any other non-local spelling returns `SCOPE-PATH-DENIED`.
- L63-64: `classify()` rejects non-string/empty tool names and `depth > 8`.
- L71-73: `web_search`/`browser*` → `SCOPE-FETCH-DENIED`; then `if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'): return ['SCOPE-TOOL-UNKNOWN']`. The tool `edit` hits this branch before arguments are inspected.
- L89-96: per-tool argument allowlists exist only for `read`, `grep`, `glob`, `write`; unknown keys yield `SCOPE-SCHEMA`.
- L99: `values = value.split(';') if tool in ('grep', 'glob') else [value]` — semicolon expansion exists only for grep/glob.
- L102: `requested_path(value, selector=tool in ('read', 'grep'))` — selector normalization is read/grep only.
- L105: `elif path not in binding['write_paths' if tool == 'write' else 'read_paths']:` — the only authority buckets are read and write.
- L120: `set(data) != {'schema', 'seats'} or data.get('schema') != 'tsukuroi-seat-bindings-v1'` — top-level keys are strict, and the schema literal is exact v1.
- L126-129: only `for field in ('read_paths', 'write_paths')` is validated; each must be a nonempty, duplicate-free list of `local()` paths, with the sole `skill://godspeed` exception scoped to `read_paths`.
- L124: the seat identity check constrains `name`, `root`, `commands`, `fetches` — but **never compares `set(seat)`**, so extra seat keys (including `edit_paths`) are accepted and ignored.
- L167-172 result dict: `status`, `request_audit_mode`, `seats_bound`, `requests_total`, `violations`, `incomplete_seats`, `missing_seats`, `present_incomplete_seats`, `seats`, `findings`, `scope` — **no `structured_edit_mode` field**.
- L286-287: CLI defaults are `.ufo/waves/round-22/build/bindings.json` and `.../events.json`; `main()` reads both via `git show <rev>:<path>` (`git_read`) with repo-relative path validation (`repo_path`). The snapshot is the historical v1 instrument.
- Literal search: `edit_paths` → 0 occurrences; `structured_edit_mode` → 0 occurrences; the only `'edit'` token is L199.

## 3. Inertness proof (static, no run)

Let `M` be any v1 manifest accepted by `evaluate`, and `M' = M` with arbitrary `edit_paths` added to any seat. For every trace `T`:

- `evaluate` parses `M`/`M'` with the same `json`/`unique` path (duplicate keys rejected identically).
- The top-level check (L120) looks only at `{'schema','seats'}` and the exact string `tsukuroi-seat-bindings-v1`; the added key is nested in a seat, so it is not seen.
- Seat validation (L124-129) reads `name`, `root`, `commands`, `fetches`, then iterates the fixed pair `('read_paths','write_paths')`. The identifier `edit_paths` does not exist in the module, so the added key is never read.
- Event classification (L61-107) never loads `edit_paths`; the only binding reads are `binding['write_paths' ...]` and `binding['read_paths']` at L105.
- Therefore the executed statement sequence is identical for `M` and `M'`, and so are `code`, `findings`, `seats`, `violations`, and every metric.

**Corollary 1.** For any v1 manifest, an `edit` event returns `['SCOPE-TOOL-UNKNOWN']` regardless of path membership, because L72-73 returns before `args.get('path')` is reached. `functions.edit` and `multi_tool_use.parallel` children are equivalent: `classify` strips the `functions.` prefix (L65-66), and the parallel branch re-enters the same whitelist for every child.

**Corollary 2.** `structured_edit_mode` is unrepresentable in v1 output. The metric cannot move from 0 to 1 on any v1 input, with or without `edit_paths`, even if a top-level wrapper tried to derive it, because the v1 result contains no edit decision at all.

**Corollary 3.** No path content in `edit_paths` can create an ALLOW, a DENY of a different class, a schema error, or a seat-binding failure — the value is not merely unchecked, it is unaddressed. This is stronger than "ignored by convention."

## 4. Absence versus defect

### 4.1 What the historical policy actually asserted

The v1 gate's declared scope is recorded request spellings against frozen prompt scopes, explicitly disclaiming "preventive enforcement," native permission, symlink/effect proof, reading proof, and universal trace completeness (L2 and the `SCOPE` constant). Its decision language is `SCOPE-*` findings, and its tool vocabulary is finite. Under that contract:

- `edit` was never a v1 term. `SCOPE-TOOL-UNKNOWN` is the truthful v1 statement "this request is outside the audited language."
- It is not the statement "editing was forbidden," "the adapter could not edit," or "authority was denied." Those are v2 predicates the v1 gate does not contain.
- The r22 records in `structured-edit-observations.json` (two argument shapes, paths under `LANE`, transcript digests supplied) are real adapter events observed after the fact; the v1 red on them is a vocabulary gap, not a policy contradiction.

### 4.2 Defect test — none is met

A defect would require one of: an internal contradiction; a violated v1-declared guarantee (e.g., denying an exactly declared read/write target, or allowing a non-declared one); or an output that depends on data the gate claims to ignore. None holds:

- Declared reads/writes still classify by L105; selftest cases `read-write-only`, `write-read-only`, `skill-write`, `double-slash` pin that behavior (L212-217, L241).
- The only anomaly an operator can produce with `edit_paths` is *nothing*: accepted-at-parse, never-read (L124/L126).
- The historical red is reproducible because the vocabulary is frozen, not because a rule misfires.

### 4.3 Schema conflation to avoid

`edit-decision-policy.json` declares `"schema": "tsukuroi-edit-policy-v1"`. That is the **decision document** schema, not seat-binding authority. C2's "schema-v2" is a new **seat-binding** schema. The policy document being v1 neither proves nor supplies v2 seat authority; and the seat-binding v1 being old does not downgrade the edit-decision policy. Both must be cited under their own names.

### 4.4 Consequence for C2

C2's `structured_edit_mode` target of 1 requires a new evaluator that (a) accepts a distinct schema literal, (b) validates `edit_paths` as first-class authority, (c) classifies `edit` against the eight declared decisions, and (d) emits the metric. Until that lands, the honest C2 value is 0, and the v1 gate's red is not a regression to repair. "Fix the old gate to allow edit" would be a capability change disguised as a bugfix and would violate `legacy schema-v1 policy and historical reds unchanged`.

The seat-binding envelope supplied to this seat is itself an instance of the gap: it carries `edit_paths`, but the bound v1 gate has no term that can read it, validate it, or derive a decision from it. The field is a prompt-level declaration awaiting a v2 consumer; it is not audited authority today, and its presence must not be reported as capability.

## 5. Derived v2 authority (decision function)

The declared authority is the eight rows of `edit-decision-policy.json` / `preregister.json.edit_decisions`. Normalizing them into a total function is an inference; each step quotes its declared reason.

Inputs: a request with tool `edit`, an argument object, and a seat binding with sets `R` (read), `W` (write), `E` (edit), all exact strings.

1. **Binding validity** → `SCOPE-SCHEMA`, exit 2, no seats bound. `E` must be a nonempty, duplicate-free list of `local()` paths with no `skill://` exception (the v1 exception is read-only by construction, L128), and every `e ∈ E` must satisfy `e ∈ R ∧ e ∈ W`; otherwise the DECLARED_EDIT condition is unreachable and the authority is incoherent. [DERIVED from "predeclared for edit and for both read and write."]
2. **Structured target first** → missing/non-string/empty `path` is `OPAQUE_PATCH`, decision `UNKNOWN`, exit 2. "Missing structured target is not inferred from opaque patch text." Body fields are never searched for a path.
3. **Spelling** → remote (`^https?://`, `host:port/`) or any internal URI scheme (`^[A-Za-z][A-Za-z0-9+.-]*://`, e.g. `xd://`, `artifact://`, `local://`, `skill://`) is `EDIT_EXTERNAL`, `DENY`. Any non-`local()` spelling (`.`, `..`, `//`, `\`, controls, `*?[];:`) is `EDIT_TRAVERSAL`, `DENY`. "No dot-segment or alternate spelling expands the target list"; "Remote or internal URIs do not become filesystem edit targets."
4. **Prerequisites, in order** (all exact membership):
   - `p∈R ∧ p∈W ∧ p∈E` → `DECLARED_EDIT`, `ALLOW`.
   - `p∈R ∧ p∉W` → `READ_ONLY_EDIT`, `DENY` ("Read authority never grants a write").
   - `p∉R ∧ p∈W` → `WRITE_ONLY_EDIT`, `DENY` ("Edit also needs its explicit target read authority").
   - `p∈R ∧ p∈W ∧ p∉E` → `UNDECLARED_EDIT`, `DENY` ("No implicit edit permission from generic report ownership").
   - `p∉R ∧ p∉W` → `DENY` with `UNDECLARED_EDIT` semantics; when `p∈E` this corner has **no uniquely named decision** in the eight (see §8).
5. **Expansion** → `CHECK_EACH`: every recorded adapter child is classified separately; rows are per child, no collapse, no short-circuit that hides siblings; the semicolon is **not** an edit-target separator (unlike grep/glob at L102), so a `;`-bearing edit path is one denied spelling, not two targets.
6. **Aggregation** → any `DENY` gives exit 1 with the deny attributed to the offending child; any `UNKNOWN` gives exit 2 (`CANNOT_EVALUATE`) while retaining already-derived rows, following the v1 code convention (`2` if incomplete/schema, `1` if findings, else `0`).
7. **Body opacity** → `old_string`, `new_string`, `stream_content` (and any future body key) are declared body fields: accepted under the edit key allowlist, never parsed for targets, never counted as expansion. Observed shapes require `stream_content` to be a known key; `i` is optional in recorded events (the CritRuntime shape lacks it), so v2 must not require it.

## 6. Independent literal fixture

Inputs only; expectations are in §7, deliberately not embedded, so the fixture cannot be reverse-engineered from its own assertions. Paths are literal and absolute under `LANE`; the loader does not stat paths, so `FixtureOther.md`/`FixtureWriteOnly.md` need not exist.

Runner contract: feed `manifest` verbatim to the manifest argument; for each case build
`{"schema":"tsukuroi-seat-events-v1","seats":[{"name":<seat>,"agent":"fixture-<seat>","complete":true,"events":<events>}]}`
and feed that to the events argument. Paths used: `R` = `.ufo/waves/round-23/build/OracleV2Legacy.md`, `O` = `.ufo/waves/round-23/build/FixtureOther.md`, `S` = `.ufo/waves/round-23/sources/godspeed-directive.txt`, `W` = `.ufo/waves/round-23/build/FixtureWriteOnly.md`, all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`.

The schema string below is a **proposed literal**, not an observed one; the implementation must substitute its declared v2 literal without changing structure or expectations.

```json
{
  "fixture": "OracleV2Legacy-v2-edit-authority",
  "manifest": {
    "schema": "tsukuroi-seat-bindings-v2",
    "seats": [
      {
        "name": "F",
        "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
        "read_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOther.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt"
        ],
        "write_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOther.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md"
        ],
        "edit_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOther.md"
        ],
        "commands": [],
        "fetches": []
      },
      {
        "name": "G",
        "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
        "read_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOther.md"
        ],
        "write_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md",
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOther.md"
        ],
        "edit_paths": [
          "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md"
        ],
        "commands": [],
        "fetches": []
      }
    ]
  },
  "cases": [
    {"id": "01-allow-edit-canonical", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing declared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md", "old_string": "-- marker --", "new_string": "-- marker --"}}]},
    {"id": "02-allow-edit-stream", "seat": "F", "events": [{"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md", "stream_content": "replacement body"}}]},
    {"id": "03-allow-body-not-target", "seat": "F", "events": [{"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md", "stream_content": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md"}}]},
    {"id": "04-allow-read-selector", "seat": "F", "events": [{"tool": "read", "args": {"i": "Reading declared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md:raw"}}]},
    {"id": "05-allow-write-report", "seat": "F", "events": [{"tool": "write", "args": {"i": "Writing declared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md", "content": "report"}}]},
    {"id": "06-allow-write-only", "seat": "F", "events": [{"tool": "write", "args": {"i": "Writing write-only target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md", "content": "x"}}]},
    {"id": "07-deny-write-read-only", "seat": "F", "events": [{"tool": "write", "args": {"i": "Writing read-only source", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt", "content": "x"}}]},
    {"id": "08-deny-read-only-edit", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing read-only source", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt", "old_string": "a", "new_string": "b"}}]},
    {"id": "09-deny-write-only-edit", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing write-only target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md", "old_string": "a", "new_string": "b"}}]},
    {"id": "10-deny-undeclared-edit", "seat": "G", "events": [{"tool": "edit", "args": {"i": "Editing undeclared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOther.md", "old_string": "a", "new_string": "b"}}]},
    {"id": "11-deny-dotdot", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing traversal spelling", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/../build/OracleV2Legacy.md", "old_string": "a", "new_string": "b"}}]},
    {"id": "12-deny-dot", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing dot spelling", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/./OracleV2Legacy.md", "old_string": "a", "new_string": "b"}}]},
    {"id": "13-deny-double-slash", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing double-slash spelling", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin//.ufo/waves/round-23/build/OracleV2Legacy.md", "old_string": "a", "new_string": "b"}}]},
    {"id": "14-deny-selector-spelling", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing selector spelling", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md:raw", "old_string": "a", "new_string": "b"}}]},
    {"id": "15-deny-semicolon", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing semicolon spelling", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md;/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt", "old_string": "a", "new_string": "b"}}]},
    {"id": "16-deny-remote", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing remote URI", "path": "https://example.invalid/report", "old_string": "a", "new_string": "b"}}]},
    {"id": "17-deny-internal-uri", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing internal URI", "path": "xd://tool", "old_string": "a", "new_string": "b"}}]},
    {"id": "18-unknown-opaque-keys", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing unknown target", "old_string": "a", "new_string": "b"}}]},
    {"id": "19-unknown-opaque-stream", "seat": "F", "events": [{"tool": "edit", "args": {"stream_content": "path=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt"}}]},
    {"id": "20-reject-unknown-key", "seat": "F", "events": [{"tool": "edit", "args": {"i": "Editing with extra key", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md", "old_string": "a", "new_string": "b", "content": "x"}}]},
    {"id": "21-check-each-parallel", "seat": "F", "events": [{"tool": "multi_tool_use.parallel", "args": {"tool_uses": [{"recipient_name": "functions.edit", "parameters": {"i": "Editing declared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md", "old_string": "a", "new_string": "b"}}, {"recipient_name": "edit", "parameters": {"i": "Editing read-only source", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt", "old_string": "a", "new_string": "b"}}]}}]},
    {"id": "22-check-each-legacy", "seat": "F", "events": [{"tool": "multi_tool_use.parallel", "args": {"tool_uses": [{"recipient_name": "functions.read", "parameters": {"i": "Reading declared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Legacy.md"}}, {"recipient_name": "glob", "parameters": {"i": "Listing source path", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt"}}]}}]}
  ]
}
```

## 7. Exact policy expectation per case

Membership columns: `R` read, `W` write, `E` edit. "Decision" is the declared decision name; the concrete finding id is an implementation label that must be stable and documented, but it must not be `SCOPE-TOOL-UNKNOWN` for an edit request (that would misstate v2 capability).

| Case | Seat | Request | R | W | E | Decision | Exit |
|---|---|---|---|---|---|---|---|
| 01 | F | edit `R` with `{i,path,old_string,new_string}` | in | in | in | `DECLARED_EDIT` ALLOW | 0 |
| 02 | F | edit `R` with `{path,stream_content}`, no `i` | in | in | in | `DECLARED_EDIT` ALLOW; body opaque; `i` optional | 0 |
| 03 | F | edit `R`, `stream_content` contains `W` as text | in | in | in | `DECLARED_EDIT` ALLOW; exactly one target row; no row for `W` | 0 |
| 04 | F | read `R:raw` | in | in | in | ALLOW; read-selector normalization preserved | 0 |
| 05 | F | write `R` | in | in | in | ALLOW; write bucket unchanged | 0 |
| 06 | F | write `W` | out | in | out | ALLOW; write-only authority suffices for write | 0 |
| 07 | F | write `S` | in | out | out | DENY; read authority does not grant write | 1 |
| 08 | F | edit `S` | in | out | out | `READ_ONLY_EDIT` DENY | 1 |
| 09 | F | edit `W` | out | in | out | `WRITE_ONLY_EDIT` DENY | 1 |
| 10 | G | edit `O`; `E={R}` | in | in | out | `UNDECLARED_EDIT` DENY | 1 |
| 11 | F | edit `.../build/../build/R` | spelling | | | `EDIT_TRAVERSAL` DENY | 1 |
| 12 | F | edit `.../build/./R` | spelling | | | `EDIT_TRAVERSAL` DENY | 1 |
| 13 | F | edit `...//.ufo/.../R` | spelling | | | `EDIT_TRAVERSAL` DENY | 1 |
| 14 | F | edit `R:raw` | spelling | | | `EDIT_TRAVERSAL` DENY; selectors are not stripped for edit | 1 |
| 15 | F | edit `R;S` | spelling | | | DENY, exactly one row; no grep-style split | 1 |
| 16 | F | edit `https://example.invalid/report` | external | | | `EDIT_EXTERNAL` DENY | 1 |
| 17 | F | edit `xd://tool` | external | | | `EDIT_EXTERNAL` DENY | 1 |
| 18 | F | edit `{i,old_string,new_string}`, no `path` | n/a | | | `OPAQUE_PATCH` UNKNOWN | 2 |
| 19 | F | edit `{stream_content:"path=..."}`, no `path` | n/a | | | `OPAQUE_PATCH` UNKNOWN; no target derived from body | 2 |
| 20 | F | edit `R` with extra key `content` | n/a | | | `SCOPE-SCHEMA` (inherited fail-closed key strictness) | 2 |
| 21 | F | parallel `[functions.edit R; edit S]` | mixed | | | `CHECK_EACH`: child 0 ALLOW, child 1 `READ_ONLY_EDIT`; deny attributed to child 1; child 0 not reported as a violation | 1 |
| 22 | F | parallel `[functions.read R; glob S]` | in | | | `CHECK_EACH`: both ALLOW; v1 parallel semantics unregressed | 0 |

The exit 2 for `UNKNOWN` rows is the derived encoding of the v1 `CANNOT_EVALUATE` convention; the declared invariant is only that `UNKNOWN` is neither `ALLOW` (0) nor `DENY` (1). An implementation that folds `OPAQUE_PATCH` into exit 1 has collapsed "cannot decide" into "decided against," which the policy's `UNKNOWN` value forbids.

Metric and schema expectations:

- `structured_edit_mode` = 1 only when a v2 manifest is evaluated by the v2 evaluator and every case row matches this table; 0 for every v1 input, every schema refusal, and every seat-binding failure.
- Schema selection must be by the `schema` string alone. A CLI flag that forces v2 semantics onto a v1 document, or v1 semantics onto a v2 document, breaks the C2 contract.
- A v2 manifest must be rejected by the v1 evaluator with `SCOPE-SCHEMA` (exit 2, no seats bound), and a v1 manifest must be rejected by the v2 evaluator the same way. The two schemas are exclusive.
- Binding-level rejection cases (exit 2, `SCOPE-SCHEMA`, metric 0): empty/duplicate `edit_paths`; an `edit_paths` entry outside `read_paths ∩ write_paths`; an `edit_paths` entry that is not `local()` (including `skill://godspeed`, `xd://…`, relative paths, dot segments); nonempty `commands`/`fetches`; foreign `root`; duplicate seat name; duplicate JSON key anywhere; parallel nesting exceeding depth 8.

## 8. Laundering probes (v1 data must not become v2 authority)

- **L1 — v1 manifest plus `edit_paths` under the v1 evaluator.** `{"schema":"tsukuroi-seat-bindings-v1","seats":[{"name":"F","root":LANE,"read_paths":[R],"write_paths":[R],"edit_paths":[R],"commands":[],"fetches":[]}]}` with case 01's edit event. Expected: exit 1, `SCOPE-TOOL-UNKNOWN` at site `F:0`, `violations` 1, `seats_bound` 1, `request_audit_mode` 1, no `structured_edit_mode` field (or 0 if a wrapper supplies it). Source-derived, not executed.
- **L2 — same v1 manifest under the v2 evaluator.** Expected: exit 2, `SCOPE-SCHEMA`, `seats_bound` 0, metric 0. No partial upgrade, no silent `edit_paths` import.
- **L3 — v2 manifest under the v1 evaluator.** Expected: exit 2, `SCOPE-SCHEMA`, `seats_bound` 0, metric 0. The historical gate cannot be pushed forward by data either.
- **L4 — inertness identity.** For any v1 manifest, evaluate with and without `edit_paths`; the serialized outputs (status, code, seats, findings, violations, request counts) must be byte-identical. This is the executable form of §3; a difference proves the v2 authority leaked into v1.

## 9. Falsifiers for a C2 claim

Any one of these refutes a claim that C2's v2 authority is present and correct:

1. A v1 manifest with `edit_paths` produces exit 0 for an edit event, or `structured_edit_mode` 1.
2. The v2 evaluator accepts `tsukuroi-seat-bindings-v1`, or the v1 evaluator accepts v2 while attributing edit authority.
3. An edit target not in `R ∩ W ∩ E` is ALLOWed, or a target in `R ∩ W ∩ E` is denied.
4. An edit path with `:raw`, `;`, `//`, `.`/`..`, or a URI scheme is ALLOWed or split into multiple targets.
5. A missing `path` is satisfied by parsing `old_string`/`new_string`/`stream_content` as a target, or is reported as ALLOW.
6. A `DENY` child in a parallel request disappears behind an ALLOW sibling, or an `UNKNOWN` is reported as PASS.
7. `read`/`write`/`glob`/`grep` semantics change for v1 inputs (historical reds move, declared targets newly denied, selectors newly stripped for edit).
8. The metric is selected by a flag rather than by the manifest schema.

## 10. Residual unknowns and gaps (not improvised)

- The exact v2 schema literal and the exact output field `structured_edit_mode` are **not declared** in the bound sources; the literal above is proposed, and the metric name is taken only from the preregister's C2 entry.
- The edit-only corner `E ∧ ¬R ∧ ¬W` has no uniquely named decision among the eight; the safe requirement is "not ALLOW," but the label must be declared before C2 claims exhaustive decision coverage.
- Whether v2's edit key allowlist includes `replace_all` (present in the current tool signature, absent from both recorded r22 shapes) is undeclared. The two observed shapes `{path,stream_content}` and `{i,path,old_string,new_string}` are the minimum.
- Whether the events schema stays `tsukuroi-seat-events-v1` or bumps is undeclared. Events carry only `tool`/`args`, so no structural change is required; if it bumps, historical v1 events stay with the v1 evaluator.
- Existence checks, symlink resolution, effect proof, reading proof, and native enforcement remain outside both versions by their declared scope; the fixture asserts classification only.
- The production v2 checker, the wave `bindings.json`/`events.json`, and the frozen r22 event/manifest files are not in this seat's read set, so no statement is made about their current content or state. The C2 verdict must rest on the declared revision's checker, which the bound snapshot shows as v1-only.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2legacy
Scope: executed=none