# OracleV2Scheme — v2 structured-edit target authority

Round 23, C2 (operability) source-only design oracle. Baseline
`ae01e50f582016384e620022be38bf5367000e2e`. No execution, no fetch, no installs.
The digest of the reviewed tool is the seat-declared identity and was not recomputed.

## Question

Does an `edit` request whose structured target is a URL, an internal URI, or a skill URI
ever become a filesystem edit under the seat-binding audit? The existing gate is
schema-v1 and has no `edit` concept. This report separates that missing capability from
any claimed defect in historical policy, then declares the exact v2 authority, its
predicate order, and an independent literal fixture with exact expected output.

## Observed facts in the existing v1 gate

All line references are to `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`.

1. The tool vocabulary is an explicit four-tool tuple plus the parallel wrapper
   (`read`, `grep`, `glob`, `write`, `multi_tool_use.parallel`, `parallel`). `edit` is
   absent, and any tool outside that tuple returns `SCOPE-TOOL-UNKNOWN` (lines 72-73)
   *before* tool arguments are inspected.
2. `edit` occurs exactly once in the whole program: the selftest case
   `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')` at line 199. There is no
   production branch, no argument schema, and no binding field for edits.
3. Binding validation admits only `read_paths` and `write_paths` (lines 126-129).
   `skill://godspeed` is admissible only inside `read_paths` (line 128), and every
   `write_paths` entry must satisfy `local()`. Seat dictionaries with extra keys are
   tolerated: validation reads specific fields and does not enforce an exact seat key set.
4. `requested_path` (lines 43-58) has three behaviours: `https?://` and host:port spellings
   become `SCOPE-FETCH-DENIED` (line 47); the exact string `skill://godspeed` returns no
   denial (lines 48-49); any other value that fails `local()` becomes `SCOPE-PATH-DENIED`
   (lines 52-53). The skill carve-out is a read-authority admission, not a path
   normalization.
5. `local()` (lines 33-36) is a pure shape predicate: prefix `LANE + '/'`, no backslash,
   no `Cc/Cf/Cs/Zl/Zp` controls, no `*?[];:` characters, and no empty, `.` or `..`
   segment. It performs no decoding, case folding, unicode normalization, symlink
   resolution or dot-segment collapse.
6. Membership is a binary selector at line 105:
   `binding['write_paths' if tool == 'write' else 'read_paths']`. There is no third
   branch. `write` is checked only against `write_paths`; `read`/`grep`/`glob` only
   against `read_paths`.
7. Authority is selected by an exact schema string: the manifest must be
   `tsukuroi-seat-bindings-v1` (line 120) and the trace `tsukuroi-seat-events-v1`
   (line 131). Anything else is `SCOPE-SCHEMA` / `CANNOT_EVALUATE`.
8. The gate is explicitly post-hoc: docstring line 2 ("not preventive enforcement") and
   `SCOPE` line 17 ("Recorded request spellings only; not runtime prevention,
   symlink/effect proof, reading proof or universal trace completeness").
9. CLI defaults still point at round-22 artifacts (`.ufo/waves/round-22/build/bindings.json`
   and `events.json`, lines 287-288), and both inputs are read from the committed revision
   (`_revision.bind` then `git_read(binding.sha, …)`, lines 270-277 and 298-299), not from
   the worktree.
10. The observation source records four round-22 `edit` requests: `CritRuntime` request
    line 15 with keys `path` + `stream_content`, and `OraclePathArtifact` request lines
    30, 33 and 36 with keys `i` + `new_string` + `old_string` + `path`. Every recorded
    target is a `build/*.md` report path under the lane; body fields are declared omitted.
    The file's own scope is metadata and recorded adapter steps only.

## Absence of capability vs defect in historical policy

Historical v1 is **not** defective on this question; it simply cannot express it.

- v1 never allows an edit. Every recorded `edit`, including a well-formed edit of a
  declared report, returns `SCOPE-TOOL-UNKNOWN` (line 73), and the selftest pins that
  result (line 199).
- v1 never inspects an edit target. Because the tool gate precedes `requested_path`, a
  `https://…` edit yields `SCOPE-TOOL-UNKNOWN`, not `SCOPE-FETCH-DENIED`; `agent://…`
  yields `SCOPE-TOOL-UNKNOWN`, not `SCOPE-PATH-DENIED`.
- v1 cannot grant a `skill://godspeed` edit. The carve-out at lines 48-49 returns no
  denial, but line 105 consults `read_paths` only for non-`write` tools and `write_paths`
  only for `write`; `edit` never reaches line 105. Even if it did, line 128 keeps
  `skill://godspeed` out of `write_paths`, and line 105 tests `read_paths` for non-write
  tools — so the carve-out is safe only because `edit` is outside the tuple.

The tempting one-line widening is the actual defect (derived statically from lines 72,
89-94, 105; not executed):

| hypothetical change | resulting classification | policy violated |
|---|---|---|
| add `edit` to the tuple and `allowed_keys`, leave line 105 | edit of a read-only declared report → `read_paths` hit → **no finding** | `READ_ONLY_EDIT` |
| same | edit of exact `skill://godspeed` → no denial at line 49, `read_paths` hit → **no finding** | `EDIT_EXTERNAL` (and `DECLARED_EDIT`) |
| same | edit of `https://…` → `SCOPE-FETCH-DENIED` | wrong class; an edit is not a fetch |
| same | edit of `agent://…`, `xd://…`, `local://…` → `SCOPE-PATH-DENIED` | wrong class; no filesystem spelling was attempted |

That leak is not a property of the shipped v1 file (which fails closed on every edit); it
is the reason v2 must add a separate classifier branch, a new `edit_paths` field, and the
binding invariant below, instead of widening the v1 tuple or reusing `requested_path`.
The skill carve-out and selector stripping are read/grep grammar and must not be invoked
for edit targets.

## Declared v2 authority

The declared decision vocabulary is exactly the eight rows of
`sources/edit-decision-policy.json` (`DECLARED_EDIT`, `UNDECLARED_EDIT`, `READ_ONLY_EDIT`,
`WRITE_ONLY_EDIT`, `OPAQUE_PATCH`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL`, `EXPANSION`), whose
scope is "structured target metadata only; no native prevention, opaque patch
interpretation, effect or reading proof". The scheme below operationalizes those tokens
without adding, renaming or reordering them.

### Schemas and exact keys

- Manifest: exactly `{"schema","seats"}`, `schema == "tsukuroi-seat-bindings-v2"`.
- Seat: exactly `{"name","root","read_paths","write_paths","edit_paths","commands","fetches"}`.
  Missing or extra seat key → `SCOPE-SCHEMA`.
- Trace: keys ⊆ `{"schema","seats","coverage"}`, `schema == "tsukuroi-seat-events-v2"`.
- Trace seat: exactly `{"name","agent","complete","events"}`.
- Event: exactly `{"tool","args"}`; a sidecar `path` key outside `args` → `SCOPE-SCHEMA`.
- Edit args: keys ⊆ `{"i","path","old_string","new_string","stream_content"}`. `i` and the
  three body fields are optional and opaque. No body value is read, copied or searched for
  a path.
- Parallel args: exactly `{"tool_uses"}`; child exactly `{"recipient_name","parameters"}`;
  nesting depth ≤ 8, deeper → `SCOPE-SCHEMA`.

### Binding invariants

- **I1** v2 manifest and v2 trace are required together; any v1/v2 mixture is
  `CANNOT_EVALUATE` with `SCOPE-SCHEMA` at `input`.
- **I2** Seat name matches `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`, is unique, `root == LANE`,
  `commands == []`, `fetches == []`.
- **I3** `read_paths` non-empty, unique, every entry `local()` or exactly `skill://godspeed`;
  `write_paths` non-empty, unique, every entry `local()`.
- **I4** `edit_paths` is present, a list (empty is legal), unique, every entry `local()`, and
  `set(edit_paths) ⊆ set(read_paths) ∩ set(write_paths)`. A manifest asserting an edit on a
  read-only or write-only path is `CANNOT_EVALUATE`, never a classified event.
- **I5** No transformation of recorded targets: no dot-segment collapse, empty-segment
  collapse, case folding, unicode normalization, percent decoding, prefix trimming/joining
  or symlink resolution. Membership is exact string equality.
- **I6** Authority is selected by the manifest schema string. The v1 evaluator stays
  byte-identical and is reached for v1 manifests only; a v1 manifest carrying an
  `edit_paths` key is still evaluated as v1 (the key is not read), and its edits remain
  `SCOPE-TOOL-UNKNOWN`. A v2 manifest never reaches v1 code.

### Predicate order (evaluation precedence)

1. Normalize one `functions.` prefix; expand parallel wrappers (`EXPANSION`) and classify
   each child independently; no child inherits a sibling's target or outcome.
2. Reject foreign tools as today (`bash`/`eval`/`task` → `SCOPE-EXEC-DENIED`,
   `web_search`/`browser*` → `SCOPE-FETCH-DENIED`, other unknown → `SCOPE-TOOL-UNKNOWN`).
   Under v2, `edit` joins the known set and therefore never yields
   `SCOPE-TOOL-UNKNOWN`; that token remains reachable only for genuinely unknown tools.
3. For `edit` only: enforce the exact argument key set. A non-string `path` is
   `SCOPE-SCHEMA`; a missing or empty-string `path` with at least one body field is
   `OPAQUE_PATCH`; a missing/empty `path` with no body field is `SCOPE-SCHEMA`.
4. `EDIT_EXTERNAL` before any `local()` or membership test.
5. `EDIT_TRAVERSAL` when the value is not external and not `local()` (the v1 shape
   predicate, lines 33-36).
6. Membership classes, disjoint: `READ_ONLY_EDIT` when in `read_paths` only;
   `WRITE_ONLY_EDIT` when in `write_paths` only; `UNDECLARED_EDIT` otherwise (including a
   canonical path declared for both read and write but not for edit).
7. `DECLARED_EDIT` only on exact membership in `edit_paths` (which I4 guarantees is also in
   `read_paths` and `write_paths`).

No `edit` path is ever split on `;` (that is grep/glob grammar) and no selector suffix is
stripped (that is read/grep grammar). A `;` or selector suffix in an edit target therefore
makes the value non-canonical, i.e. `EDIT_TRAVERSAL`.

### Decision table

| policy id | decision | v2 predicate | finding id | aggregate effect |
|---|---|---|---|---|
| `EXPANSION` | `CHECK_EACH` | parallel wrapper | none at wrapper | wrapper counted; children classified separately |
| `OPAQUE_PATCH` | `UNKNOWN` | edit; no structured path; body present | `OPAQUE_PATCH` | findings+1, unresolved+1 |
| `EDIT_EXTERNAL` | `DENY` | edit; path matches `S1` or `S2` | `EDIT_EXTERNAL` | findings+1, violations+1 |
| `EDIT_TRAVERSAL` | `DENY` | edit; not external; not `local()` | `EDIT_TRAVERSAL` | findings+1, violations+1 |
| `READ_ONLY_EDIT` | `DENY` | canonical; in `read_paths` \ `write_paths` | `READ_ONLY_EDIT` | findings+1, violations+1 |
| `WRITE_ONLY_EDIT` | `DENY` | canonical; in `write_paths` \ `read_paths` | `WRITE_ONLY_EDIT` | findings+1, violations+1 |
| `UNDECLARED_EDIT` | `DENY` | canonical; not in `edit_paths`; not read-only or write-only | `UNDECLARED_EDIT` | findings+1, violations+1 |
| `DECLARED_EDIT` | `ALLOW` | canonical; in `edit_paths` | none | allow+1 |

`S1 = (?i)^[A-Za-z][A-Za-z0-9+.\-]*://` (all scheme URIs, including `https:`, `file:`,
`skill:`, `agent:`, `xd:`, `local:`, `artifact:`, `history:`, `proc:`, `ssh:`, `issue:`,
`pr:`, `mcp:`).
`S2 = ^[^/:\s]+:[0-9]+/` (v1's host:port form, e.g. `localhost:9222/`).

Finding ids are the policy decision ids verbatim, so audit output and the policy file map
one-to-one. Only edit findings use these ids; `read`/`grep`/`glob`/`write` keep the v1
vocabulary unchanged (`SCOPE-SCHEMA`, `SCOPE-PATH-DENIED`, `SCOPE-FETCH-DENIED`,
`SCOPE-EXEC-DENIED`, `SCOPE-TOOL-UNKNOWN`).

Exit aggregation: `code = 2` when the trace is incomplete or any `SCOPE-SCHEMA` finding
exists; else `code = 1` when any finding exists (including `OPAQUE_PATCH`); else `0`.
`status` maps `PASS`/`FAIL`/`CANNOT_EVALUATE`; `request_audit_mode = int(code != 2)`.
Counters: `violations` = count of `DENY` findings; `unresolved` = count of `OPAQUE_PATCH`.
A per-seat `findings` list preserves event order. (v1 named this row key `violations`; v2
uses `findings` because it also carries `UNKNOWN` entries — flag for L1.)

### Why an external target can never become a filesystem edit

Three independent locks, strongest first:

1. **Declaration lock.** Every `edit_paths` entry must satisfy `local()`, which requires
   the literal prefix `LANE + '/'` and bans `:`. No URI-shaped string can be declared as an
   edit target, so `ALLOW` is unreachable for every value matching `S1`/`S2` by string
   equality alone.
2. **Classifier lock.** `EDIT_EXTERNAL` is tested before traversal and membership; the edit
   branch consults only `edit_paths` and never calls `requested_path`. The v1 skill
   carve-out therefore cannot admit, and the selector grammar cannot rewrite, an edit
   target.
3. **Exactness lock.** No normalization (I5) means a `file://` URI whose tail is byte-equal
   to the declared path is still not equal to the declared string. `EDIT_EXTERNAL` is the
   label; lock 1 is the guarantee. Even a reordered branch could only change the label,
   not produce `ALLOW` — except by reintroducing the rejected read-path fallback.

Read authority and edit authority are orthogonal: the same seat may read `skill://godspeed`
with no finding and must be denied an edit of that exact token in the same trace.

## Fixture A — independent literal v2 target matrix

Synthetic names only; no round-22 or round-23 seat data is reused, and the fixture paths
need not exist (the audit classifies recorded spellings, not filesystem state). Bodies are
placeholders and are never inspected.

### Manifest

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "FixtureSeat",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBoth.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureUnlisted.md",
        "skill://godspeed"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBoth.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

### Trace

```json
{
  "schema": "tsukuroi-seat-events-v2",
  "seats": [
    {
      "name": "FixtureSeat",
      "agent": "fixture-agent-01",
      "complete": true,
      "events": [
        {"tool": "read", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md"}},
        {"tool": "read", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md"}},
        {"tool": "read", "args": {"path": "skill://godspeed"}},
        {"tool": "edit", "args": {"i": "fixture-3", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md", "old_string": "<old>", "new_string": "<new>"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md", "stream_content": "<stream>"}},
        {"tool": "functions.edit", "args": {"i": "fixture-5", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md", "old_string": "<old>", "new_string": "<new>"}},
        {"tool": "edit", "args": {"path": "https://example.invalid/patch:1-5"}},
        {"tool": "edit", "args": {"path": "file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md"}},
        {"tool": "edit", "args": {"path": "skill://godspeed"}},
        {"tool": "edit", "args": {"path": "skill://godspeed:raw"}},
        {"tool": "edit", "args": {"path": "agent://FixturePeer"}},
        {"tool": "edit", "args": {"path": "xd://ast_edit"}},
        {"tool": "edit", "args": {"path": "local://fixture-report"}},
        {"tool": "edit", "args": {"path": "localhost:9222/"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/../build/FixtureEdit.md"}},
        {"tool": "edit", "args": {"path": ".ufo/waves/round-23/build/FixtureEdit.md"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23//build/FixtureEdit.md"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md:1-5"}},
        {"tool": "edit", "args": {"path": "/etc/passwd"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBoth.md"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureUnlisted.md"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/%2e%2e/%2e%2e/etc/passwd"}},
        {"tool": "edit", "args": {"i": "fixture-24", "old_string": "<old>", "new_string": "<new>"}},
        {"tool": "edit", "args": {"i": "fixture-25", "path": "", "old_string": "<old>", "new_string": "<new>"}},
        {"tool": "multi_tool_use.parallel", "args": {"tool_uses": [{"recipient_name": "edit", "parameters": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md", "old_string": "<old>", "new_string": "<new>"}}, {"recipient_name": "edit", "parameters": {"path": "https://example.invalid/", "old_string": "<old>", "new_string": "<new>"}}]}},
        {"tool": "multi_tool_use.parallel", "args": {"tool_uses": [{"recipient_name": "edit", "parameters": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md", "old_string": "<old>", "new_string": "<new>"}}, {"recipient_name": "read", "parameters": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureEdit.md"}}]}}
      ]
    }
  ]
}
```

### Exact expectation (event index → decision → finding)

| idx | target shape | decision | finding |
|---|---|---|---|
| 0 | read editable report | n/a (read) | none |
| 1 | read read-only report | n/a (read) | none |
| 2 | read `skill://godspeed` | n/a (read) | none (orthogonality) |
| 3 | edit declared, `i`+old/new | `DECLARED_EDIT` | none |
| 4 | edit declared, `stream_content` only | `DECLARED_EDIT` | none |
| 5 | `functions.edit` declared | `DECLARED_EDIT` | none |
| 6 | `https://example.invalid/patch:1-5` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 7 | `file://` URI equal to declared tail | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 8 | `skill://godspeed` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 9 | `skill://godspeed:raw` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 10 | `agent://FixturePeer` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 11 | `xd://ast_edit` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 12 | `local://fixture-report` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 13 | `localhost:9222/` | `EDIT_EXTERNAL` | `EDIT_EXTERNAL` |
| 14 | `…/build/../build/FixtureEdit.md` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` |
| 15 | repo-relative `.ufo/…` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` |
| 16 | `…/round-23//build/…` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` |
| 17 | `…/FixtureEdit.md:1-5` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` |
| 18 | `/etc/passwd` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` |
| 19 | read-only report | `READ_ONLY_EDIT` | `READ_ONLY_EDIT` |
| 20 | write-only report | `WRITE_ONLY_EDIT` | `WRITE_ONLY_EDIT` |
| 21 | read+write report, no edit | `UNDECLARED_EDIT` | `UNDECLARED_EDIT` |
| 22 | canonical, undeclared | `UNDECLARED_EDIT` | `UNDECLARED_EDIT` |
| 23 | `%2e%2e` spelling (no decoding) | `UNDECLARED_EDIT` | `UNDECLARED_EDIT` |
| 24 | no path, body present | `OPAQUE_PATCH` | `OPAQUE_PATCH` |
| 25 | empty path, body present | `OPAQUE_PATCH` | `OPAQUE_PATCH` |
| 26 | parallel [declared edit, https edit] | `EXPANSION` | `EDIT_EXTERNAL` (child) |
| 27 | parallel [declared edit, read] | `EXPANSION` | none |

Event 18 (`/etc/passwd`) is declared `EDIT_TRAVERSAL`, not `UNDECLARED_EDIT`, because it is
not a canonical lane-rooted spelling at all; the defect is the spelling, not a missing
declaration. Event 23 stays `UNDECLARED_EDIT` because nothing decodes `%2e`; it cannot
match a declared path unless declared in that exact spelling, so the guarantee is
unchanged even if a reviewer would prefer the traversal label there.

### Exact expected result

```json
{
  "status": "FAIL",
  "request_audit_mode": 1,
  "structured_edit_mode": 1,
  "seats_bound": 1,
  "requests_total": 28,
  "requests_children": 4,
  "classifications": 32,
  "violations": 19,
  "unresolved": 2,
  "incomplete_seats": 0,
  "missing_seats": 0,
  "present_incomplete_seats": 0,
  "seats": [
    {
      "name": "FixtureSeat",
      "agent": "fixture-agent-01",
      "requests": 28,
      "complete": true,
      "findings": ["EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_EXTERNAL", "EDIT_TRAVERSAL", "EDIT_TRAVERSAL", "EDIT_TRAVERSAL", "EDIT_TRAVERSAL", "EDIT_TRAVERSAL", "READ_ONLY_EDIT", "WRITE_ONLY_EDIT", "UNDECLARED_EDIT", "UNDECLARED_EDIT", "UNDECLARED_EDIT", "OPAQUE_PATCH", "OPAQUE_PATCH", "EDIT_EXTERNAL"],
      "decisions": {"DECLARED_EDIT": 5, "UNDECLARED_EDIT": 3, "READ_ONLY_EDIT": 1, "WRITE_ONLY_EDIT": 1, "OPAQUE_PATCH": 2, "EDIT_TRAVERSAL": 5, "EDIT_EXTERNAL": 9, "EXPANSION": 2}
    }
  ],
  "findings": [
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:6"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:7"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:8"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:9"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:10"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:11"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:12"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:13"},
    {"id": "EDIT_TRAVERSAL", "site": "FixtureSeat:14"},
    {"id": "EDIT_TRAVERSAL", "site": "FixtureSeat:15"},
    {"id": "EDIT_TRAVERSAL", "site": "FixtureSeat:16"},
    {"id": "EDIT_TRAVERSAL", "site": "FixtureSeat:17"},
    {"id": "EDIT_TRAVERSAL", "site": "FixtureSeat:18"},
    {"id": "READ_ONLY_EDIT", "site": "FixtureSeat:19"},
    {"id": "WRITE_ONLY_EDIT", "site": "FixtureSeat:20"},
    {"id": "UNDECLARED_EDIT", "site": "FixtureSeat:21"},
    {"id": "UNDECLARED_EDIT", "site": "FixtureSeat:22"},
    {"id": "UNDECLARED_EDIT", "site": "FixtureSeat:23"},
    {"id": "OPAQUE_PATCH", "site": "FixtureSeat:24"},
    {"id": "OPAQUE_PATCH", "site": "FixtureSeat:25"},
    {"id": "EDIT_EXTERNAL", "site": "FixtureSeat:26"}
  ],
  "scope": "Recorded structured edit-target metadata only; post-hoc audit, no native prevention, no path normalization/resolution, no opaque-patch interpretation, no effect or reading proof."
}
```

Arithmetic check: 28 events + 4 parallel children = 32 classifications; 2 wrappers are
`EXPANSION`; 26 edit requests (23 top-level + 3 children) and 4 reads; edit decisions
5 + 19 + 2 = 26; findings 19 + 2 = 21; `violations` = 19, `unresolved` = 2.

## Fixture B — schema negatives (each evaluated alone, exact `CANNOT_EVALUATE`)

All use Fixture A's seat and one clean read event unless noted; expected `code = 2`,
`status = "CANNOT_EVALUATE"`, `structured_edit_mode = 0`.

| case | delta | expected finding site |
|---|---|---|
| B1 | `edit_paths` contains `"skill://godspeed"` | `SCOPE-SCHEMA` at `input` (fails `local()`) |
| B2 | `edit_paths` contains `FixtureReadOnly.md` | `SCOPE-SCHEMA` at `input` (I4, not in `write_paths`) |
| B3 | `edit_paths` contains `FixtureWriteOnly.md` | `SCOPE-SCHEMA` at `input` (I4, not in `read_paths`) |
| B4 | seat omits `edit_paths` | `SCOPE-SCHEMA` at `input` (exact seat keys) |
| B5 | duplicate `edit_paths` entry | `SCOPE-SCHEMA` at `input` (uniqueness) |
| B6 | seat gains extra key `extra` | `SCOPE-SCHEMA` at `input` (exact seat keys) |
| B7 | edit args add key `body` | `SCOPE-SCHEMA` at the event site |
| B8 | event gains sidecar `path` beside `tool`/`args` | `SCOPE-SCHEMA` at the event site |
| B9 | edit args `{"i": "x"}` only | `SCOPE-SCHEMA` at the event site (no target, no body) |
| B10 | edit args `{"path": 42, "old_string": "<old>", "new_string": "<new>"}` | `SCOPE-SCHEMA` at the event site (non-string path) |
| B11 | v2 manifest with `tsukuroi-seat-events-v1` trace | `SCOPE-SCHEMA` at `input` (I1) |
| B12 | v1 manifest with `tsukuroi-seat-events-v2` trace | `SCOPE-SCHEMA` at `input` (v1 line 131, unchanged) |
| B13 | manifest schema `tsukuroi-seat-bindings-v3` | `SCOPE-SCHEMA` at `input` (unknown authority) |

## Fixture C — explicit empty edit authority

Seat `FixtureSeat` with `read_paths` and `write_paths` both containing exactly
`…/FixtureEdit.md`, `edit_paths: []`, one event `{"tool":"edit","args":{"path":"…/FixtureEdit.md"}}`.
Expected: `code = 1`, one `UNDECLARED_EDIT` at `FixtureSeat:0`, `violations = 1`,
`unresolved = 0`, `structured_edit_mode = 1`, `decisions.UNDECLARED_EDIT = 1`. This is the
literal reading of `UNDECLARED_EDIT`'s reason, "No implicit edit permission from generic
report ownership".

## Fixture D — historical v1 counterfactual on Fixture A's trace

v1 binding for the same seat (`tsukuroi-seat-bindings-v1`, same `read_paths`/`write_paths`,
no `edit_paths`) and Fixture A's events. Expected, from v1 lines 72-73 and 199:

- Every one of the 26 edit requests returns `SCOPE-TOOL-UNKNOWN`; `findings` length 26,
  `violations = 26`, `code = 1`, `status = "FAIL"`.
- Zero `EDIT_EXTERNAL`, zero `EDIT_TRAVERSAL`, zero `READ_ONLY_EDIT`, zero `ALLOW`; the
  `skill://godspeed`, `file://` and `https://` edits are indistinguishable from the
  declared edit.
- The `https://` child of event 26 yields `SCOPE-TOOL-UNKNOWN`, **not**
  `SCOPE-FETCH-DENIED`, proving the tool gate precedes path handling.
- Adding an ignored `edit_paths` key to the v1 seat changes nothing (line 123-129
  tolerates extra seat keys), so a v1 manifest can never silently grant edit authority.

This is the observed gap: v1 has no edit capability. It is not a historical red to retract.

## Integration notes for C2's command

Command shape is unchanged:
`python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`.

1. Dispatch on the manifest `schema` string. Retain the v1 evaluator verbatim (including
   the round-22 CLI defaults and selftest case at line 199); v2 code must be unreachable
   from a v1 manifest.
2. Both inputs are read from the committed revision (`git_read(binding.sha, …)`), so the
   v2 manifest and trace must be committed at `<REV>`; an uncommitted fixture yields
   `SCOPE-READ` / `CANNOT_EVALUATE` rather than a pass.
3. `repo_path` gates the CLI paths unchanged; replace the `<WAVE>` placeholder with a real
   single segment or the input-path check yields `SCOPE-SCHEMA` / `CANNOT_EVALUATE`.
4. Add `structured_edit_mode = int(authority == v2 and code != 2)` for the C2 metric, plus
   `unresolved`, `requests_children` and `classifications`. Keep `request_audit_mode`.
5. Keep body fields out of findings and reports; v2 findings carry only id and site.

## Limits and unresolved gaps

- Post-hoc audit only. No native per-seat restrictive tool interface exists, and nothing
  here is runtime prevention, symlink/effect proof or reading proof (inherits v1 `SCOPE`,
  line 17). The C2 claim must not be described as enforcement.
- `local()` is a string predicate, so a symlink inside the lane that resolves outside it is
  not detected; the audit denies by spelling, not by resolved effect.
- `file://` is denied even when its tail equals a declared target. This is intentional and
  is the fixture's strongest external case.
- A bracketed IPv6 endpoint such as `[::1]:9222/` matches neither `S1` nor `S2` and would be
  labelled `EDIT_TRAVERSAL`; no observed request uses that form. The outcome is still
  `DENY`.
- Observed adapter key shapes differ (3 of 4 rows carry `i`; 1 of 4 uses `stream_content`).
  The v2 key union tolerates both; whether round-23 adapters keep both shapes is unknown
  and does not affect the guarantee.
- Exact fixtures and expected results here are declared from source reading and were not
  executed under this seat. Whether L1 adopts the row-key rename (`violations` →
  `findings`), the four added counters and the `structured_edit_mode` field is an
  integration decision, not an observed fact.
- No historical manifest, report or binding is rewritten; no round 24 is started.

## Tooling

No installations, no upgrades, no commands, no fetches: this seat is NO-EXEC/NO-FETCH and
all host package transactions are paused.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2scheme
Scope: executed=none
