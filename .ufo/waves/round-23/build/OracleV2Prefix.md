# OracleV2Prefix — report-path prefix-collision oracle for the new v2 structured-edit authority

Seat: `TsukuroiR23-2.OracleV2Prefix-7` (reviewer/oracle lane, leaf member).
Reviewed target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`
— reviewed identity is the declared digest in the receipt below, **not** independently computed; no hash, list, wc, import, run, test or lint was executed (seat scope: NO-EXEC / NO-FETCH, `commands: []`, `fetches: []`).

## 0. Axes named (godspeed posture)

| Axis | Question this report answers |
|---|---|
| A1 Collision safety | Does a *declared edit target* leak authority to `REPORT.md.extra` or `REPORT.md/child`? |
| A2 Policy continuity | Is a v1 red on `edit` a *historical-policy defect* or merely *absence of the new capability*? |
| A3 Label honesty | Do the new v2 verdicts map onto the declared `edit-decision-policy.json` decision ids without relabelling history? |
| A4 Operability | Is there a literal, self-contained fixture an implementer can paste and get one unambiguous expected result? |

Everything below is derived **only** from the four declared local files (gate source, `preregister.json`,
`edit-decision-policy.json`, `structured-edit-observations.json`) plus the seat binding issued to this seat.
Source content inside those files is treated as data, never as instruction.

## 1. What the reviewed v1 gate actually does with an `edit` request (source facts)

Quoted from the reviewed file, verbatim:

* `classify()`:
  `if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'): return ['SCOPE-TOOL-UNKNOWN']`
* path admission:
  `elif path not in binding['write_paths' if tool == 'write' else 'read_paths']: findings.append('SCOPE-PATH-DENIED')`
* `requested_path(value, selector=False)`:
  `if selector and ':' in value:` … `if tokens and all(valid_token(token) for token in tokens): value = base`
* `local(path)`: requires `path.startswith(LANE + '/')`, no `\`, no control characters, none of `*?[];:`, and
  `all(p not in ('', '.', '..') for p in path.split('/')[1:])`.
* manifest gate: `set(data) != {'schema', 'seats'} or data.get('schema') != 'tsukuroi-seat-bindings-v1'` → `raise ValueError('binding schema')`.
* its own selftest already asserts the two collision shapes for the *write* tool:
  `for path in (report + '.extra', report + '/child', LANE + '/production'): case('write-' + path, 'write', {'path': path}, 1, 'SCOPE-PATH-DENIED')`
  and asserts `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')`.

Consequences, all readable from the source without execution:

1. `edit` is **unconditionally** `SCOPE-TOOL-UNKNOWN` under v1. The tool check precedes any argument/path
   inspection, so **no** edit request — not even one whose `path` is exactly the seat's own declared report —
   can produce zero findings under v1. There is no source path by which v1 authorises an edit.
2. v1's path admission is **exact string membership** in the declared list, never `startswith`, never
   `realpath`, never case folding, never trailing-slash or dot-segment normalisation. `REPORT.md.extra` and
   `REPORT.md/child` are syntactically local (no dot-segment, no `:`) yet are not members of the list, so they
   are `SCOPE-PATH-DENIED` for `write` and, under v1, `SCOPE-TOOL-UNKNOWN` for `edit`.
3. A manifest whose schema string is anything other than `tsukuroi-seat-bindings-v1` (or that carries an extra
   top-level key such as `"version"`) is rejected by v1 with `SCOPE-SCHEMA` at site `input` → exit 2
   `CANNOT_EVALUATE`. v1 therefore **cannot silently evaluate a v2 manifest**; it refuses it.

## 2. A1/A2 — Absence of the new capability vs a defect in historical policy

The distinction the assignment asks for, stated exactly:

* **Absence of new capability (not a defect).** v1 was never declared to audit structured edits. Its own module
  docstring scopes it to "Audit recorded requests against frozen prompt scopes; not preventive enforcement", and
  its `SCOPE` string limits it to "Recorded request spellings only". The r22 structured-edit requests captured in
  `structured-edit-observations.json` (three `edit` events for `CritRuntime`, four for `OraclePathArtifact`,
  each with a concrete `path`, `argument_keys`, and a `recorded_starts` read/write trail) are therefore **reds
  under v1 for lack of a capability that v1 never claimed** — `SCOPE-TOOL-UNKNOWN`, one violation per request.
  That is the honest reading and it must stay the reading.
* **A historical-policy defect would require** v1 to *claim* edit auditing and then classify edit targets
  wrongly, or v1 to *authorise* an undeclared path. Neither is present: v1 never authorises an edit (finding 1
  above) and never treats a path as in-scope by prefix (finding 2 above).
* **The r23 requirement that follows.** `preregister.json` C2 scope pins: "New explicit schema-v2 audit
  authority for exact predeclared structured edit targets; **legacy schema-v1 policy and historical reds
  unchanged**", and `limits` pins "No historical manifest/report rewrite or retrospective authorization". So the
  v2 capability must be **added alongside** v1, never **in place of** it, and must never turn an r22 red into
  a pass by re-reading it.

**Oracle verdict on the collision specifically:** the new v2 authority must carry the same *exact-membership*
discipline v1 already uses for `write`. The prefix shapes `REPORT.md.extra` and `REPORT.md/child` are
**DENY** under the new authority, and the denial must be a *violation* (v1 severity, exit 1), not a soft
"unknown" and not an allowance.

## 3. A3 — Exact policy expectation from the new declared v2 authority

`edit-decision-policy.json` (`tsukuroi-edit-policy-v1`, `policy: round23-preregister`, `evidence: S086`) is the
declared authority for structured target metadata. The eight decision ids and their declared outcomes:

| decision id | decision | declared reason (verbatim) |
|---|---|---|
| `DECLARED_EDIT` | ALLOW | Exact target is predeclared for edit and for both read and write |
| `UNDECLARED_EDIT` | DENY | No implicit edit permission from generic report ownership |
| `READ_ONLY_EDIT` | DENY | Read authority never grants a write |
| `WRITE_ONLY_EDIT` | DENY | Edit also needs its explicit target read authority |
| `OPAQUE_PATCH` | UNKNOWN | Missing structured target is not inferred from opaque patch text |
| `EDIT_TRAVERSAL` | DENY | No dot-segment or alternate spelling expands the target list |
| `EDIT_EXTERNAL` | DENY | Remote or internal URIs do not become filesystem edit targets |
| `EXPANSION` | CHECK_EACH | Every recorded adapter read or write remains separately scoped |

Mapping the two collision shapes onto that table — the paths are well-formed local paths with **no dot
segment**, **no alternate spelling of a declared target**, and **no remote/URI form**; they are simply
**not the declared target**. Hence the governing id is `UNDECLARED_EDIT` (DENY). Note that
`EDIT_TRAVERSAL`'s stated reason ("No dot-segment or alternate spelling **expands the target list**") is also
about target-list expansion, so an implementer may reasonably label the `.extra` case that way instead — the
**decision (DENY) and severity are identical either way**, so the outcome must not depend on the label; but the
label must be stable and must not be `DECLARED_EDIT`. This report's expectation uses `UNDECLARED_EDIT`.

Adjacent shapes, same authority, for completeness of the fixture family:

| shape | governing id | decision | why |
|---|---|---|---|
| `REPORT.md` (exact declared edit target) | `DECLARED_EDIT` | ALLOW | predeclared for edit **and** for read **and** for write |
| `REPORT.md.extra` | `UNDECLARED_EDIT` | DENY | not the declared target; suffix is not a dot-segment |
| `REPORT.md/child` | `UNDECLARED_EDIT` | DENY | not the declared target; child component is not a dot-segment |
| `REPORT.md:raw` | `EDIT_TRAVERSAL` | DENY | alternate spelling must not alias a declared target (see D2) |
| `REPORT.md/../REPORT.md` | `EDIT_TRAVERSAL` | DENY | dot-segment; v1's `local()` already forbids dot segments |
| `skill://godspeed`, `xd://tool` | `EDIT_EXTERNAL` | DENY | remote/internal URI is not a filesystem edit target |
| edit request with no structured path | `OPAQUE_PATCH` | UNKNOWN | target not inferred from patch text |

## 4. A4 — Independent literal fixture (v2 expectation)

Deliberately **independent** of the reviewed gate's own selftest: the v1 selftest exercises `write` with
`src`/`report` synthetic names and never exercises `edit`, so it cannot witness a v2 edit verdict. The fixture
below is the minimum that forces the collision behaviour to be observable.

Fixture A — bindings (paste as `bindings.json`):

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "OracleV2Prefix",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Prefix.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Prefix.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Prefix.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

Fixture A — events (paste as `events.json`):

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "OracleV2Prefix",
      "agent": "TsukuroiR23-2.OracleV2Prefix-7",
      "complete": true,
      "events": [
        {"tool": "edit", "args": {"i": "declared target", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Prefix.md", "old_string": "A", "new_string": "B"}},
        {"tool": "edit", "args": {"i": "suffix collision", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Prefix.md.extra", "old_string": "A", "new_string": "B"}},
        {"tool": "edit", "args": {"i": "child collision", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2Prefix.md/child", "old_string": "A", "new_string": "B"}}
      ]
    }
  ]
}
```

Fixture A — **exact expected result under the new v2 authority** (this is the expectation an implementer must
satisfy; it was **not** executed here):

```json
{
  "status": "FAIL",
  "request_audit_mode": 1,
  "seats_bound": 1,
  "requests_total": 3,
  "violations": 2,
  "incomplete_seats": 0,
  "missing_seats": 0,
  "findings": [
    {"id": "SCOPE-PATH-DENIED", "site": "OracleV2Prefix:1"},
    {"id": "SCOPE-PATH-DENIED", "site": "OracleV2Prefix:2"}
  ]
}
```

with process exit code **1**, and the per-event decision ledger:

```text
event 0  path .../build/OracleV2Prefix.md          DECLARED_EDIT  ALLOW  -> no finding
event 1  path .../build/OracleV2Prefix.md.extra    UNDECLARED_EDIT  DENY  -> SCOPE-PATH-DENIED (OracleV2Prefix:1)
event 2  path .../build/OracleV2Prefix.md/child    UNDECLARED_EDIT  DENY  -> SCOPE-PATH-DENIED (OracleV2Prefix:2)
```

Fixture B — **contrast**: the same bindings/events under the **reviewed v1 gate** (this is the "absence vs
defect" discriminator, and it is what the historical reds look like):

* Fixture A's bindings as written (schema `…-v2`) under the reviewed gate → `CANNOT_EVALUATE`, exit **2**,
  single finding `SCOPE-SCHEMA` at site `input` (v1 rejects the schema string; it does not silently pass).
* The same bindings with only the schema string relabelled `tsukuroi-seat-bindings-v1` (seat keys
  `read_paths`/`write_paths`/`edit_paths` are *not* key-set-checked by v1, so the seat still validates) →
  exit **1**, `status FAIL`, `requests_total 3`, `violations 3`, findings `SCOPE-TOOL-UNKNOWN` ×3 — i.e. v1
  **never** authorises an edit and **never** treats a collision path as in-scope.

So: a v1 red on `edit` is **absence of capability**, provable from source alone; a v2 green on `REPORT.md.extra`
or `REPORT.md/child` would be a **defect in the new policy** — exactly the axis this oracle exists to pin.

## 5. Findings (by severity)

**D1 — HIGH — prefix/derived matching on edit targets would authorise the collision shapes.**
Evidence: reviewed file, `classify()` path admission is `path not in binding['write_paths' if tool == 'write' else 'read_paths']` —
exact membership; its selftest asserts `report + '.extra'` and `report + '/child'` → `SCOPE-PATH-DENIED`.
A v2 that resolves edit authority with `startswith`, `os.path.commonprefix`, `os.path.realpath`, `Path.parent`
containment, case folding, or trailing-slash stripping would turn Fixture A events 1 and 2 into ALLOWs.
Requirement: edit-target admission must be **exact string equality** against the declared edit list, with the
**same** normalisation-freedom v1 already has (no `realpath`, no dot-segment collapsing, no trailing-slash
folding). Dot-segment and control-character rejections from v1's `local()` must be carried into the edit path
(`EDIT_TRAVERSAL` DENY).

**D2 — HIGH — the read-path selector helper must not be reused for edit paths.**
Evidence: `requested_path(value, selector=False)` strips a valid selector only when `selector=True`, and the
gate passes `selector=tool in ('read', 'grep')`. For a read, `…/OracleV2Prefix.md:raw` legitimately resolves
to the base path. For an **edit**, the `path` argument is a literal filesystem target — the recorded edit
requests in `structured-edit-observations.json` show plain absolute paths, no selector. If v2 routes edit
through the selector-aware branch, `…/OracleV2Prefix.md:raw` silently aliases the declared target and becomes
ALLOW, which is precisely the `EDIT_TRAVERSAL` denial ("alternate spelling") and a second collision vector.
Requirement: edit paths must be evaluated with selector handling **off**; a colon-bearing edit path is not a
declared target.

**D3 — MEDIUM — the v2 edit argument-key set must cover both recorded adapter shapes, or r22-shaped corpora
degrade to `SCOPE-SCHEMA`.**
Evidence: `structured-edit-observations.json` records two distinct edit shapes —
`CritRuntime` with `argument_keys: ["path", "stream_content"]`, and `OraclePathArtifact` with
`argument_keys: ["i", "new_string", "old_string", "path"]`. The reviewed gate maps *unknown argument keys* to
`SCOPE-SCHEMA` (exit 2, `CANNOT_EVALUATE`) via its `allowed_keys` table, which today has no `edit` entry at
all. If v2 defines the edit key set as `{i, path, old_string, new_string}`, every `CritRuntime`-shaped event
becomes `SCOPE-SCHEMA`, the whole run becomes exit 2, and C2's metric (`structured_edit_mode`) would be
measured against a non-evaluable run rather than an audit. Requirement: v2's edit key set must admit
`{i, path, old_string, new_string, stream_content}` (or otherwise explicitly accept both recorded shapes) while
still rejecting genuinely unknown keys as `SCOPE-SCHEMA`.

**D4 — MEDIUM — `OPAQUE_PATCH` = UNKNOWN needs its own verdict bucket, distinct from both ALLOW and DENY.**
Evidence: `edit-decision-policy.json` declares `OPAQUE_PATCH` → `UNKNOWN` ("Missing structured target is not
inferred from opaque patch text"), while the reviewed gate's only "cannot decide" bucket is `SCOPE-SCHEMA`
(exit 2). If v2 maps a pathless edit to `SCOPE-SCHEMA`, the declared UNKNOWN disappears into
`CANNOT_EVALUATE`; if v2 folds it into DENY, the declared distinction is lost; if v2 folds it into ALLOW, it
retroactively authorises an unresolvable request (forbidden by `limits`: "No … retrospective authorization").
Requirement: v2 emits a distinct non-ALLOW verdict for `OPAQUE_PATCH` and reports it separately from
violations. **[INFERENCE]** The declared sources do **not** specify how an UNKNOWN affects exit code and
overall status; this is an open contract decision that must be settled before C2's `structured_edit_mode = 1`
can be claimed, because a run containing only UNKNOWNs must not report as a clean PASS.

**D5 — MEDIUM — v2 must route legacy v1 manifests to the unchanged v1 evaluator (or refuse them), never to the
new edit-aware path.**
Evidence: `preregister.json` C2 scope ("legacy schema-v1 policy and historical reds unchanged") and `limits`
("No historical manifest/report rewrite or retrospective authorization"); the reviewed gate's manifest gate
(`schema != 'tsukuroi-seat-bindings-v1'` → `SCOPE-SCHEMA` at `input` → exit 2) proves refusal is already the
historical behaviour. Requirement: a v1-schema manifest must keep yielding the same v1 verdicts (`edit` →
`SCOPE-TOOL-UNKNOWN`, exit 1). If v2 silently accepted v1 manifests and treated `edit` on an owned report as
ALLOW, the r22 reds would be relabelled — the precise outcome C2 forbids.

**D6 — LOW — `EDIT_EXTERNAL` must not degrade to a filesystem target.**
Evidence: policy declares `EDIT_EXTERNAL` DENY ("Remote or internal URIs do not become filesystem edit
targets"); the reviewed gate treats `skill://godspeed` as the only non-filesystem read path and denies
`write` to it (`case('skill-write', 'write', {'path': 'skill://godspeed'}, 1, 'SCOPE-PATH-DENIED')`), and
routes `http(s)://` / `host:port/` to `SCOPE-FETCH-DENIED`. Requirement: an edit whose `path` is `skill://`,
`xd://`, `artifact://`, `agent://`, `local://`, `http(s)://` or `host:port/` is DENY, and must not be recorded
as a filesystem write; the audit reports a recorded *request spelling* only, never an effect.

**D7 — LOW — the v2 binding schema field carrying edit authority is not named by any declared source.**
Evidence: the declared authority names *decisions*, not a manifest field; the seat binding issued to this seat
carries the three-way list `read_paths` / `write_paths` / `edit_paths` over the same report path, and the
reviewed gate's seat validation ignores unknown seat keys. **[INFERENCE]** `edit_paths` is the intended field
name in this round (it is the only in-repo signal), and the events schema name
(`tsukuroi-seat-events-v1`) may stay unchanged since the binding schema and trace schema are separate
namespaces in the reviewed gate. Both choices must be pinned in the v2 source before the fixture in §4 can be
treated as canonical, because an implementer using a different field name would silently produce an empty edit
authority and turn Fixture A event 0 into a false DENY.

## 6. Residual risk

* **R1 — Severity continuity is the real contract, not the finding id.** The collision shapes must produce the
  *same* severity under v2 as v1 produces for `write` (a counted violation, exit 1). If v2 renames the id to
  something like `SCOPE-EDIT-DENIED`, the outcome stays correct only if the new id is still counted as a
  violation and still yields exit 1 — the id itself is cosmetic. Fixture A pins the *count* (2 violations of 3
  requests) and the *exit* (1), not merely the label.
* **R2 — The declared sources do not fix the v2 manifest/event schema names or the UNKNOWN→status mapping**
  (D4, D7). Until those are pinned, "the exact expected result" of §4 is exact in *decision, count and exit
  code*, but the literal JSON keys of a v2 result object remain implementation-defined.
* **R3 — `EXPANSION` = `CHECK_EACH` interacts with the collision.** Each recorded adapter step in
  `structured-edit-observations.json` (`recorded_starts` read/write trails) must be scoped separately; a
  single edit event must not be collapsed into one "expansion" verdict that could mask one of the two collision
  shapes behind an allowed parent step.
* **R4 — Audit scope stays post-hoc.** Whatever v2 decides, it audits *recorded request spellings*; the
  reviewed gate's own `SCOPE` string, `preregister.json` `limits` ("No native per-seat restrictive tool
  interface exists", "No runtime prevention, effect/reading/recorder-completeness …") and the task framing all
  forbid reading an ALLOW as permission at runtime or as proof that the write happened. There is no native
  per-seat restrictive toolset in this environment; **no runtime enforcement is claimed anywhere in this report.**
* **R5 — No oracle, no proof.** Fixture A is a *design* expectation derived from source reading, not an
  observation. Only the implementer's own v2 selftest can convert it into evidence.

## 7. Verification gaps

1. Fixture A was **not executed** (seat scope: nothing run): no `check-seat-bindings.py --selftest`, no
   `--revision` run, no import, no hash, no listing. Every "expected" value in §4 is a source-derived
   expectation, marked as such.
2. The reviewed file's digest is the **declared** identity from the seat assignment; it was not recomputed.
3. The v2 manifest/event schema names, the edit argument-key set, and the UNKNOWN→status mapping are
   **unresolved by the declared sources** (D3, D4, D7) — an implementer must pin them in source before
   Fixture A can be executed verbatim.
4. No transcript of the r22 seats was opened: the four captured `edit` observations in
   `structured-edit-observations.json` are the only evidence used for the two adapter shapes, and the file's
   own scope statement ("Observed structured path metadata and recorded adapter steps only, not universal tool
   semantics …") bounds them accordingly.
5. Nothing outside the four declared local files (plus the seat binding issued to this seat) was read; no
   repository-wide search for an existing v2 draft was performed or is claimed.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2prefix
Scope: executed=none
