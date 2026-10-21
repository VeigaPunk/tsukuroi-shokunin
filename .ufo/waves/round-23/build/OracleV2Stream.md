# OracleV2Stream — design oracle: valid declared `path` + `stream_content` shape under an explicit v2 edit-target audit authority

Seat: `OracleV2Stream` (leaf member; no subagent dispatch, no delegation).
Target: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (declared SHA256 `8fccb655…a04b6`, **supplied identity, not independently computed**).
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

---

## 0. Method, scope, and non-actions

**Method (read-only, no execution).** I read the four declared source paths with `read`, and located exact line anchors with `grep` over the same declared paths only. Every v1 behaviour asserted below is cited to a line in the target file; no behaviour is inferred from memory or from a prior round.

**Declared paths read (all absolute, all inside the seat binding):**

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/edit-decision-policy.json`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/structured-edit-observations.json`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/godspeed-directive.txt`
- `skill://godspeed`

**Non-actions (contractual).** No `bash`, no `eval`, no `task`, no subprocess, no import, no compile, no test/lint/format, **no hash/`sha256sum`/`wc`/`ls`/directory listing**, no network or URL fetch, no `xd://`/`proc://`/`agent://` fetch, no filesystem search beyond the declared paths, no git or jj state access, no write to any path other than this report. The declared digest is treated as supplied identity, exactly as the contract states; it was not recomputed and must not be presented as an independently verified digest.

**Authority this report is derived from (all r23-new, all declared):**

- `preregister.json` claim **C2** — axis `operability`, metric `structured_edit_mode`, `before: 0`, `target: 1`, scope: *"New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."*; plus `edit_decisions` (the eight), `limits`, and `separability`.
- `edit-decision-policy.json` — the eight declared decisions with reasons, evidence `S086`, and the scope line: *"Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof."*
- `structured-edit-observations.json` — the captured structured-edit request metadata (`S086`): the observed argument-key shapes.

---

## 1. Axes (godspeed posture, named before iteration)

| # | Axis | What "better" means for this seat |
|---|------|-------------------------------|
| A1 | **Target identity** | A v2 edit request is recognised by an exact declared filesystem path plus a *shape*, never by body text. |
| A2 | **Policy completeness** | Every v2 verdict is one of the eight declared C1 decision ids, and every id is reachable. |
| A3 | **Historical non-regression** | v1 verdicts, v1 selftest expectations and v1 output bytes are untouched; r22 reds stay red. |
| A4 | **Verdict honesty** | "Undecidable" is never reported as "permitted" and never as "violation"; no claim exceeds recorded request spellings. |
| A5 | **Operability** | The declared C2 command, unchanged, yields a v2 verdict surface with `structured_edit_mode` readable. |

---

## 2. What the existing (v1) gate actually does with a structured edit request

Source of truth: `check-seat-bindings.py` (r23 snapshot). Line anchors are from that file.

1. **The tool gate is total for `edit`.** `classify()` reaches the tool allow-list at line **72–73**:

   ```
   72|  if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'):
   73|      return ['SCOPE-TOOL-UNKNOWN']
   ```

   `edit` is not in that tuple, so the function **returns before any path is ever looked at**. The early returns for exec/fetch (lines 68–71) are the same shape. Consequences that matter downstream:

   - The declared `path` of an edit is **never compared** against `read_paths`/`write_paths` (the membership test lives at line **105–106**, unreachable for `edit`).
   - The `allowed_keys` table (lines **89–94**) has **no `edit` entry**; keys are only checked for tools that survive line 72, so an edit's `stream_content` is not even inspected for key validity.
   - `SCOPE-TOOL-UNKNOWN` is not `SCOPE-SCHEMA`, so in `evaluate()` it is counted as a **violation** (the violation counter at line ~157 counts every id except `SCOPE-SCHEMA`) and yields exit code **1** (FAIL), not 2.

2. **The v1 manifest schema is hard-pinned.** Line **120** requires `set(data) == {'schema','seats'}` *and* `data['schema'] == 'tsukuroi-seat-bindings-v1'`; anything else raises → `SCOPE-SCHEMA` at site `input` → exit **2** (`CANNOT_EVALUATE`). A v2 manifest handed to the v1 path therefore cannot be evaluated at all — it is not a "red", it is *out of vocabulary*.

3. **The v1 events schema is hard-pinned** at line **131** (`tsukuroi-seat-events-v1`).

4. **v1 seat validation tolerates unknown seat keys.** Lines **122–130** validate `name`, `root`, `commands`, `fetches`, `read_paths`, `write_paths` but never assert an exact key set on a seat. So a v1 manifest could carry an `edit_paths` array today and v1 would **silently ignore it**. That is a fact about v1's tolerance, not a v1 bug — but it matters for the v2 design: the *absence* of the field is what v1 enforces, not its presence.

5. **v1 has a read-only exception for `skill://godspeed`** (lines **48–49**, inside `requested_path()`), and v1's selftest pins that it is read-scoped: writing to it is `SCOPE-PATH-DENIED` (line **215**), `skill://other` is denied (line **216**), and even a selector spelling `skill://godspeed:raw` is denied (line **217**).

6. **v1's selftest pins the edit behaviour explicitly.** Line **199**:

   ```
   199|  case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')
   ```

   i.e. exit **1** with `SCOPE-TOOL-UNKNOWN` is the *declared, asserted* v1 answer for an edit request. (v1 strips a `functions.` prefix at lines 65–66, so `functions.edit` behaves identically.)

---

## 3. The distinction this seat was asked to draw: **absence of v2 capability, not a defect in historical policy**

**Verdict: absence, not defect. The v1 policy is internally consistent and self-verified; the gap is a missing *authority*, not a broken *rule*.**

Evidence, in order of strength:

- **(a) v1 never claims edit-target authority.** Its allow-list (72) and key table (89–94) contain no `edit` entry; its own scope string (line **17**) is *"Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."* A gate that never asserted it could adjudicate an edit target is not defective for failing to adjudicate one. Under the same scope, "cannot rule this request in" is correctly reported as a finding rather than as a pass.

- **(b) v1's selftest pins the behaviour, so it is policy rather than accident.** Line 199 asserts `edit → SCOPE-TOOL-UNKNOWN / exit 1`. The surrounding cases (185–199, 214–220) pin the whole historical surface: read/write asymmetry, `skill://` asymmetry, traversal rejection, fetch classification, `functions.` prefix stripping, parallel nesting depth, malformed-args handling. An accident does not get 40+ pinned cases.

- **(c) The eight C1 decisions and the `S086` corpus are r23-new.** `edit-decision-policy.json` and `structured-edit-observations.json` are round-23 sources; `preregister.json` C2 says explicitly *"legacy schema-v1 policy and historical reds unchanged"*. Judging v1 by a policy document that did not exist in v1 would be retroactive authorization in the wrong direction, which `preregister.json` `limits` forbids (*"No historical manifest/report rewrite or retrospective authorization"*).

- **(d) I looked for a genuine historical defect and found none in this path.** Checks performed, all source-level:
  - Does v1 ever *allow* an edit to an undeclared target? **No** — it never allows any edit (72–73).
  - Does v1 ever mis-classify `skill://godspeed` as writable? **No** — the exception is a *return* before the membership test, but the membership test at 105 uses `write_paths` for `write`, and the binding validator (128) only permits `skill://godspeed` inside `read_paths`; 215–217 pin it.
  - Does v1 ever accept a traversal spelling? **No** — `local()` (33–36) rejects `.`/`..`/empty segments and `*?[];:`; `requested_path()` (43–58) rejects scheme-like prefixes before that.
  - Is any v1 selftest expectation inconsistent with the implementation it pins? **No** — the cases I traced (selector stripping 50–58 vs 185; depth guard 63–64 vs the nested-exec/depth-exhausted pair; `unique` duplicate-key hook 20–26 vs the `duplicate-json-key` case) are mutually consistent.

- **Therefore:** the r22 reds caused by recorded edits are the *correct historical output* of a v1 gate that had no edit authority. The v2 work item (C2) is *additive*: it adds a second vocabulary, and it must leave v1's vocabulary and its reds exactly as they are.

**One thing that would be a historical defect if it happened, and does not:** a v2 implementation that reuses v1's shared `allowed_keys` table to add an `edit` entry, thereby making a **v1** manifest start accepting edit events (v1 line 72 would still return `SCOPE-TOOL-UNKNOWN` first, so a careless implementer could be tempted to *also* add `'edit'` to the line-72 tuple). That single tuple edit would change v1's pinned behaviour at line 199 and flip every historical r22 edit red to a pass — a silent retrospective authorization. §7.1 makes this a hard prohibition.

---

## 4. The v2 design (source-only proposal; nothing here was executed)

### 4.1 Dispatch must be strictly additive and outside v1's code path

`evaluate()` already accepts a **pre-parsed** manifest: line **118** is `json.loads(manifest, object_pairs_hook=unique) if isinstance(manifest, (str, bytes)) else manifest` (and the same for events at 119). Therefore the v2 dispatcher can parse once and route without touching v1's logic:

```
parsed = json.loads(manifest, object_pairs_hook=unique)   # same duplicate-key hook as v1
if isinstance(parsed, dict) and parsed.get('schema') == 'tsukuroi-seat-bindings-v2':
    -> evaluate_v2(parsed, events)
else:
    -> evaluate(manifest, events)          # v1 path, byte-identical behaviour
```

Constraints that follow from the source:

- Do **not** modify `classify()` (61–107), `allowed_keys` (89–94), the line-72 tool tuple, or the line-120/131 schema pins. v2 needs its own evaluator, its own tool/arg rules, and its own decision table.
- v1's `evaluate()` keeps rejecting a v2 manifest with `SCOPE-SCHEMA`/exit 2 if it is ever called with one (line 120) — correct, and it is now unreachable from the dispatcher.
- The v1 selftest (175–268) must remain green **unchanged**, including line 199.

### 4.2 v2 manifest shape — `tsukuroi-seat-bindings-v2`

Mirror v1's top-level key set exactly (`{'schema','seats'}`, cf. line 120) and v1's seat rules (name regex at 124, `root == LANE` at 124, `commands == []` and `fetches == []` at 124, `read_paths`/`write_paths` non-empty + unique + `local()`-valid with the single `skill://godspeed` read exception at 128), **plus one new seat field**:

- `edit_paths` — the explicit predeclared structured-edit targets. Rules: non-empty list, unique, every element `local()`-valid (i.e. under `LANE`, no control chars, no `*?[];:`, no `.`/`..`/empty segments — reuse `local()` at 33–36 so the vocabulary is *identical* to v1's), and **every element must also appear in `read_paths` and in `write_paths`**.

  That last rule is not an invention of mine; it is the literal text of the declared decision `DECLARED_EDIT` — *"Exact target is predeclared for edit and for both read and write"* (`edit-decision-policy.json`; identical in `preregister.json` `edit_decisions`). A target declared for edit but missing a read or write leg could never satisfy `DECLARED_EDIT`, so it is a **manifest error**, not a request decision: reject it at binding validation with `SCOPE-SCHEMA` (exit 2) rather than leaving a permanently-unknowable binding. (I flag the alternative — accept and let every request to it DENY — as *worse*: it makes a mis-declared manifest look like a seat violation and hides the declaration error.)

### 4.3 v2 events shape — `tsukuroi-seat-events-v2`

Mirror v1's events shape (line 131; seat keys `name`,`agent`,`complete`,`events[{tool,args}]`). The only new content is the **edit argument shape**, which must be derived from the captured corpus (`structured-edit-observations.json`), not invented:

- Observation `CritRuntime` (lines 11–17): `tool: "edit"`, `argument_keys: ["path","stream_content"]`, `path: …/round-22/build/CritRuntime.md`, `body_fields: "omitted; no report text copied"`, and `recorded_starts` showing a `read` (line 12), a `write` (line 13) and the `edit` (line 15) **on the same path**.
- Observations `OraclePathArtifact` ×3 (lines 37–41, 60–64, 83–87): `argument_keys: ["i","new_string","old_string","path"]`.

Derived v2 edit shapes:

| shape | required keys | optional | forbidden |
|-------|---------------|----------|----------|
| **stream** | `stream_content` | `i`, `path` | `old_string`, `new_string` |
| **patch** | `old_string` **and** `new_string` | `i`, `path` | `stream_content` |

- **`i` must be optional in both shapes.** The captured stream edit has *no* `i` key (observation `CritRuntime`), while the captured patch edits *do*. Requiring `i` would make the one real stream observation schema-invalid — i.e. the gate would reject a shape the fleet actually produces. This is a concrete, corpus-grounded reason not to tighten the key set.
- **Both a stream body and patch keys present, or neither → `SCOPE-SCHEMA`** (exit 2). The shape is then not decidable and the record is malformed.
- **A missing `path` is *not* a schema error.** It is the declared `OPAQUE_PATCH` case: the shape is known, the *target* is not. Verdict `UNKNOWN` (see 4.5).

**Opaqueness rule (the "opaque shape" half of my mandate).** In a v2 events trace the stream body must be recorded as a single declared redaction token, e.g. `"stream_content": "<opaque>"`. The evaluator never inspects, copies, hashes or interprets the value; the v2 result echoes only the path, the decision id and the site. If the recorded value is anything other than the declared token, the producer broke the redaction invariant and the record is `SCOPE-SCHEMA` (exit 2).

*Why the token and not "accept any string and ignore it":* the weaker variant makes a leaked body undetectable and lets a recorder smuggle content into an artifact that the C2 scope calls *"Body data opaque"*. The token costs one constant and one selftest case. It also matches the observed practice (`body_fields: "omitted; no report text copied"`) and the preregister limit *"Raw command/fetch body content is not copied"*.

### 4.4 The v2 decision table (one of the eight declared ids per edit request)

The v2 evaluator must emit **only** the eight ids from `edit-decision-policy.json`; an id outside that set is `SCOPE-SCHEMA`. The evaluator's decision function over an edit request with structured path `P`:

| order | condition | decision id | verdict | finding id | counted as violation |
|-------|----------|-------------|---------|-----------|----------------------|
| 1 | `P` is a scheme/URI (remote or internal: `http(s)://`, `skill://`, `xd://`, `artifact://`, `proc://`, `agent://`, `host:port/`) | `EDIT_EXTERNAL` | DENY | `SCOPE-EDIT-EXTERNAL` | yes |
| 2 | `P` is a local path whose spelling is not exact (contains `.`/`..`/empty segment, duplicate slash, or otherwise fails `local()`) | `EDIT_TRAVERSAL` | DENY | `SCOPE-EDIT-TRAVERSAL` | yes |
| 3 | the request carries **no** structured `path` (opaque patch text) | `OPAQUE_PATCH` | **UNKNOWN** | `SCOPE-EDIT-UNKNOWN` (in `unknowns`, not `findings`) | **no** |
| 4 | `P ∈ edit_paths ∩ read_paths ∩ write_paths` | `DECLARED_EDIT` | ALLOW | — | no |
| 5 | `P ∉ edit_paths` and `P ∈ read_paths \ write_paths` | `READ_ONLY_EDIT` | DENY | `SCOPE-EDIT-READ-ONLY` | yes |
| 6 | `P ∉ edit_paths` and `P ∈ write_paths \ read_paths` | `WRITE_ONLY_EDIT` | DENY | `SCOPE-EDIT-WRITE-ONLY` | yes |
| 7 | `P ∉ edit_paths` and `P` in neither | `UNDECLARED_EDIT` | DENY | `SCOPE-EDIT-UNDECLARED` | yes |

`EXPANSION` is the remaining declared id and it is a **scope rule, not a per-request verdict**: *"Every recorded adapter read or write remains separately scoped."* Concretely, in a v2 trace each recorded step is judged against its own authority set, and a **prior successful step grants nothing**. The `CritRuntime` observation (read → write → edit on one path) is exactly the shape that a naive implementation would "optimise" into a single pass; the v2 evaluator must not, and the fixture E-H in §5 pins the violation count at **1**, not 2.

**Implementer hazard (naming inversion).** The ids name *the authority the seat already has*, while the reasons name *what is missing*:
- `READ_ONLY_EDIT` — reason *"Read authority never grants a write"* → the seat holds **read** only → the edit DENIES.
- `WRITE_ONLY_EDIT` — reason *"Edit also needs its explicit target read authority"* → the seat holds **write** only → the edit DENIES.

A reader who assumes "READ_ONLY_EDIT = the request is read-only" will invert rows 5 and 6. The table above is the authoritative mapping for this round; it should be transcribed verbatim into the landed implementation's selftest.

### 4.5 Exit-code and result semantics for v2

Mirror v1's precedence, with one honest addition:

- **exit 0 `PASS`** — no violation, no unknown, trace complete.
- **exit 1 `FAIL`** — ≥1 DENY finding.
- **exit 2 `CANNOT_EVALUATE`** — incomplete trace, schema error, **or ≥1 UNKNOWN decision**.

`OPAQUE_PATCH → UNKNOWN` must **not** be counted as a violation (`violations` stays 0) *and* must not be laundered into a PASS. Reporting "no authority" for a request whose target is unknown would be a false verdict in the permissive direction; counting it as a violation would be a false verdict in the strict direction. The honest report is a separate `unknowns` array plus exit 2, so no consumer can read a PASS over an undecided request.

**v2 result surface** = the v1 result keys (`status`, `request_audit_mode`, `seats_bound`, `requests_total`, `violations`, `incomplete_seats`, `missing_seats`, `present_incomplete_seats`, `seats`, `findings`, `scope`) **plus** `structured_edit_mode: 1`, `decisions` (per-request `{id, decision, site}`), `unknowns`, and a v2 `scope` string that additionally names the opaque-body limit.

**Recommendation on `structured_edit_mode` in v1 output:** do **not** add the field to the v1 result. C2's scope says *"legacy schema-v1 policy and historical reds unchanged"*, and the strictest reading is that a v1 run's JSON is byte-identical to today's. The C2 metric `structured_edit_mode: 0 → 1` should then be read from the **v2 artifact** (the v2 run reports 1; the v1 tool could not report the mode at all, which is the "before 0"). The alternative (emit `structured_edit_mode: 0` in v1 output) is a one-key change that makes the two modes directly comparable, at the cost of changing v1's output bytes for every existing consumer. Flagging this as a decision for the implementer/main, not resolving it unilaterally.

---

## 5. Independent literal fixtures and their exact expected policy outcomes

These fixtures are **authored here**, independent of the r22 records (they use an invented seat name and invented file names; the *shapes* are taken from `S086`). No fixture was executed. All paths are absolute under the lane root and pass `local()` (33–36); the seat name matches the v1 name regex (124) `FixtureSeat`.

### 5.1 Shared v2 manifest (M0)

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "FixtureSeat",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureTarget.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureTarget.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureTarget.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

`FixtureTarget.md` ∈ read ∩ write ∩ edit (the only `DECLARED_EDIT`-reachable target). `FixtureReadOnly.md` ∈ read only. `FixtureWriteOnly.md` ∈ write only. `FixtureUndeclared.md` is in no set.

### 5.2 Event traces and expected outcomes

Every trace below is `{"schema":"tsukuroi-seat-events-v2","seats":[{"name":"FixtureSeat","agent":"fixture-agent","complete":true,"events":[…]}]}`; only the `events` array varies, and it is given literally per case. Sites use v1's `f'{name}:{index}'` convention.

**E-A — stream edit to a fully declared target (the positive case).**

```json
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureTarget.md","stream_content":"<opaque>"}}
```

Expected: exit **0**, `status: PASS`, `findings: []`, `violations: 0`, `unknowns: []`, `decisions: [{"id":"DECLARED_EDIT","decision":"ALLOW","site":"FixtureSeat:0"}]`, `structured_edit_mode: 1`.

**E-B — stream edit to an undeclared path → `UNDECLARED_EDIT` / DENY.**

```json
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureUndeclared.md","stream_content":"<opaque>"}}
```

Expected: exit **1**, `findings: [{"id":"SCOPE-EDIT-UNDECLARED","site":"FixtureSeat:0"}]`, `violations: 1`, decision `UNDECLARED_EDIT` / DENY.

**E-C — stream edit to a read-only path → `READ_ONLY_EDIT` / DENY.**

```json
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md","stream_content":"<opaque>"}}
```

Expected: exit **1**, finding `SCOPE-EDIT-READ-ONLY` at `FixtureSeat:0`, `violations: 1`, decision `READ_ONLY_EDIT` / DENY.

**E-D — stream edit to a write-only path → `WRITE_ONLY_EDIT` / DENY.**

```json
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureWriteOnly.md","stream_content":"<opaque>"}}
```

Expected: exit **1**, finding `SCOPE-EDIT-WRITE-ONLY` at `FixtureSeat:0`, `violations: 1`, decision `WRITE_ONLY_EDIT` / DENY.

**E-E — patch edit with no structured path → `OPAQUE_PATCH` / UNKNOWN.**

```json
{"tool":"edit","args":{"i":"fixture intent","old_string":"a","new_string":"b"}}
```

Expected: exit **2**, `status: CANNOT_EVALUATE`, `findings: []`, `violations: 0`, `unknowns: [{"id":"SCOPE-EDIT-UNKNOWN","decision":"OPAQUE_PATCH","site":"FixtureSeat:0"}]`, decision `OPAQUE_PATCH` / UNKNOWN. **Not** a violation (the target is unknown, not unauthorised).

**E-F — stream edit with a traversal spelling → `EDIT_TRAVERSAL` / DENY.** Two spellings, same verdict.

```json
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/../build/FixtureTarget.md","stream_content":"<opaque>"}}
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/./FixtureTarget.md","stream_content":"<opaque>"}}
```

Expected: exit **1** each, finding `SCOPE-EDIT-TRAVERSAL` at `FixtureSeat:0` and `FixtureSeat:1` respectively, `violations: 2`, decision `EDIT_TRAVERSAL` / DENY. The target is *the same file* as E-A — the point is that an alternate spelling does **not** expand the target list (declared reason: *"No dot-segment or alternate spelling expands the target list"*).

**E-G — stream edit to a non-filesystem target → `EDIT_EXTERNAL` / DENY.**

```json
{"tool":"edit","args":{"path":"skill://godspeed","stream_content":"<opaque>"}}
{"tool":"edit","args":{"path":"https://example.invalid/x","stream_content":"<opaque>"}}
```

Expected: exit **1** each, finding `SCOPE-EDIT-EXTERNAL` at `FixtureSeat:0` and `FixtureSeat:1`, `violations: 2`, decision `EDIT_EXTERNAL` / DENY. Note the deliberate difference from v1: v1 would classify the second path `SCOPE-FETCH-DENIED` (line 46) and would let `skill://godspeed` through the read exception (48–49); a v2 **edit** target must not inherit either, because the declared reason is *"Remote or internal URIs do not become filesystem edit targets"* — both remote *and* internal URIs. v1's `skill://` exception is read-scoped by construction (binding validation at 128 admits it only in `read_paths`; selftest 215–217 pins that write to it is denied).

**E-H — expansion control: a prior read grants nothing.**

```json
{"tool":"read","args":{"i":"fixture intent","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md"}}
{"tool":"edit","args":{"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureReadOnly.md","stream_content":"<opaque>"}}
```

Expected: exit **1**, the read produces **no** finding (it is in `read_paths`), the edit produces `SCOPE-EDIT-READ-ONLY` at `FixtureSeat:1`, and `violations: 1` — **not 2**. This is the machine-checkable anti-expansion property, and it mirrors the observed `CritRuntime` read→write→edit sequence.

**E-V1 — historical-red control (the "absence, not defect" evidence, in fixture form).** Replay E-A's event under the **v1** schema (`tsukuroi-seat-bindings-v1` manifest without `edit_paths`, `tsukuroi-seat-events-v1` trace):

Expected under the *unchanged* v1 evaluator: exit **1**, `findings: [{"id":"SCOPE-TOOL-UNKNOWN","site":"FixtureSeat:0"}]`, `violations: 1` — identical to the v1 selftest's own pinned expectation at line 199. The v1 red is therefore *unchanged by design*; the v2 verdict for the same request differs only because v2 has the authority v1 lacks. The r22 reds stay red; no retrospective authorization (preregister `limits`).

### 5.3 Exact expected-outcome table

| fixture | shape | declared target | decision | verdict | exit | finding / unknown id | violations | unknowns |
|---------|-------|------------------|----------|---------|------|---------------------|-----------|----------|
| E-A | stream | edit∩read∩write | `DECLARED_EDIT` | ALLOW | 0 | — | 0 | 0 |
| E-B | stream | none | `UNDECLARED_EDIT` | DENY | 1 | `SCOPE-EDIT-UNDECLARED` | 1 | 0 |
| E-C | stream | read only | `READ_ONLY_EDIT` | DENY | 1 | `SCOPE-EDIT-READ-ONLY` | 1 | 0 |
| E-D | stream | write only | `WRITE_ONLY_EDIT` | DENY | 1 | `SCOPE-EDIT-WRITE-ONLY` | 1 | 0 |
| E-E | patch, no path | unknown | `OPAQUE_PATCH` | UNKNOWN | 2 | `SCOPE-EDIT-UNKNOWN` (unknowns) | 0 | 1 |
| E-F | stream, dot-segment | edit∩read∩write (alternate spelling) | `EDIT_TRAVERSAL` | DENY | 1 | `SCOPE-EDIT-TRAVERSAL` | 2 (2 events) | 0 |
| E-G | stream, URI | not a file | `EDIT_EXTERNAL` | DENY | 1 | `SCOPE-EDIT-EXTERNAL` | 2 (2 events) | 0 |
| E-H | read then stream | read only | `READ_ONLY_EDIT` (edit event only) | DENY | 1 | `SCOPE-EDIT-READ-ONLY` | 1 | 0 |
| E-V1 | stream, **v1** schema | edit∩read∩write | *(no v1 decision)* | n/a | 1 | `SCOPE-TOOL-UNKNOWN` | 1 | 0 |

### 5.4 Example expected receipt for a v2 run (fixture; indented, placeholder digest)

```
  Reviewed-SHA256: <64-hex supplied digest>
  Predicate: r23-oraclev2stream
  Scope: executed=none
```

(The real three-line receipt is emitted once, unfenced, at the end of my final message; it is not duplicated here, and the placeholder above is a fixture, not a computed digest.)

---

## 6. What the v2 authority does **not** establish (honesty limits)

- **Post-hoc only.** The target's own docstring: *"Audit recorded requests against frozen prompt scopes; not preventive enforcement."* The v2 gate inherits that: it audits recorded request spellings; it prevents nothing.
- **No runtime enforcement claim.** `preregister.json` `limits[0]`: *"No native per-seat restrictive tool interface exists"*, and the main session confirms no native restrictive task toolset. A v2 gate is an **audit report**, not a sandbox. Any C2 summary must say "audit authority", never "enforcement".
- **No effect, reading, symlink or recorder-completeness proof** (SCOPE, line 17). The v2 verdict covers the *spelling* of the target in the recorded request; it cannot show that the file was written, that the written bytes are the recorded body, or that the trace is complete.
- **The body stays opaque.** Because the stream body is redacted to a token, the v2 audit can prove *which path* was targeted and *that a stream-shaped request was made* — it cannot prove what was streamed. That limit is exactly C2's *"Body data opaque"* and `edit-decision-policy.json`'s *"no … opaque patch interpretation, effect or reading proof."*
- **Corpus bound.** The `S086` capture contains **four** edit observations across **two** seats and **two** transcripts: one stream-shaped (`CritRuntime`, `["path","stream_content"]`) and three patch-shaped (`OraclePathArtifact`, `["i","new_string","old_string","path"]`). That is enough to exercise both v2 shapes and the read→write→edit sequence, and it is **not** evidence of universal adapter semantics (`S086` scope: *"not universal tool semantics"*). A v2 coverage claim must be phrased as "both observed shapes are covered by the design", never "all edit semantics are covered".
- **No retroactive authorization.** v2 governs v2 traces; r22's edit reds stay red (preregister `limits`).
- **Separability.** v2 reads only the explicit v2 authority and the captured events; it does not read or relabel r22 evidence (`preregister.separability`).

---

## 7. Findings, ordered by severity

### 7.1 (blocking, for the v2 implementer) The v2 tool/arg vocabulary must not be merged into v1's shared tables

*Severity: high — silent retrospective authorization of every historical edit red.*
`check-seat-bindings.py:72` and `:199` together pin v1's answer for `edit`. Adding `'edit'` to the line-72 tuple, or adding an `'edit'` entry to the shared `allowed_keys` table (89–94) *and* the tuple, would let a **v1** manifest start accepting edit events, flipping r22's recorded edit reds to passes without any operator decision. Required: a separate v2 evaluator reached by schema dispatch (§4.1), with v1's `classify()`, `allowed_keys`, line-72 tuple, line-120/131 schema pins and the whole v1 selftest left untouched.

### 7.2 (high) `OPAQUE_PATCH`/UNKNOWN must not be folded into either verdict

*Severity: high — a false verdict in one direction or the other.*
`edit-decision-policy.json` gives `OPAQUE_PATCH` the verdict `UNKNOWN` with reason *"Missing structured target is not inferred from opaque patch text"*. If v2 emits `SCOPE-PATH-DENIED` for it, an undecidable request is reported as a violation; if v2 lets it pass, an undecidable request yields a PASS. The only honest encoding is a separate `unknowns` array plus exit 2 (§4.5), which is also why a missing `path` must be a *decision*, not a `SCOPE-SCHEMA` error.

### 7.3 (high) `i` must be optional in the v2 edit key set

*Severity: high — would invalidate the only observed stream shape.*
`structured-edit-observations.json` shows the one real stream edit with `argument_keys: ["path","stream_content"]` — **no** `i` — while the three patch edits carry `i`. A v2 rule that requires `i` (mirroring v1's `write` allowance of `{'i','path','content'}` at 89–94) would mark the observed stream request malformed and turn a policy decision into a schema failure.

### 7.4 (medium) The decision-id naming invites inversion of `READ_ONLY_EDIT` / `WRITE_ONLY_EDIT`

*Severity: medium — wrong DENY reason attached to a real request.*
`READ_ONLY_EDIT` = the seat holds **read** authority only (reason: *"Read authority never grants a write"*); `WRITE_ONLY_EDIT` = the seat holds **write** authority only (reason: *"Edit also needs its explicit target read authority"*). The ids name the authority present; the reasons name what is missing. §4.4's table is the transcription that must land in the implementation's selftest.

### 7.5 (medium) The v2 edit path must not inherit v1's `skill://godspeed` read exception or v1's fetch classification

*Severity: medium — mislabelled decision.*
`requested_path()` returns the `skill://godspeed` read exception unconditionally (48–49) and classifies `http(s)://` as `SCOPE-FETCH-DENIED` (46). For an **edit target** both must be routed to `EDIT_EXTERNAL` (declared reason covers "Remote or internal URIs"), matching v1's read-scoped treatment (binding validation 128; selftest 215–217).

### 7.6 (medium) The redaction token must be a single declared constant, and the v2 result must not echo bodies

*Severity: medium — opacity is the whole point of C2's scope.*
A v2 events trace must record the stream body as one fixed token; the evaluator must never inspect, hash, copy or interpret it, and the result JSON must echo only path + decision + site. This is what makes the claim "Body data opaque" true rather than aspirational, and it matches `S086`'s recorded practice (`body_fields: "omitted; no report text copied"`) and the preregister limit *"Raw command/fetch body content is not copied"*.

### 7.7 (low) `structured_edit_mode` placement is an open decision, not a detail

*Severity: low — output-shape coupling, no verdict change.*
Emitting `structured_edit_mode: 0` in v1 output would make the C2 metric directly comparable but changes v1's output bytes; keeping v1 output byte-identical and reading the metric from the v2 artifact honours *"legacy schema-v1 policy and historical reds unchanged"* more strictly. Recommendation and trade-off in §4.5; this is a main/implementer call, not an oracle call.

### 7.8 (informational) v1's tolerance of unknown seat keys is a trap for the v2 author

*Severity: informational.*
v1's seat validation (122–130) asserts no exact key set, so a v1 manifest can carry `edit_paths` and v1 will ignore it silently. A v2 author who "just adds the field" without a schema bump would get a manifest that *looks* like it grants edit authority while the v1 evaluator grants none — the worst of both worlds. Hence §4.2's `tsukuroi-seat-bindings-v2` + dispatch.

---

## 8. Residual risk and verification gaps (explicit, under NO-EXEC)

- **Nothing was executed.** No selftest run, no fixture run, no v2 implementation exists in the snapshot. Every v1 expectation above is read from source (line-cited) or from v1's own declared selftest expectations (199); every v2 expectation is a **proposal** with a fixture, not a measured result.
- **The digest was not independently verified** (contract: supplied identity). It is reported as declared, and no hash/listing was performed.
- **Read-set limits bound this report.** Only the seven declared read paths were opened. Consequently I could not check: whether another tool (e.g. the C1 checker `check-edit-contract.py` named in `preregister.json` C1) already consumes a v2 shape and would collide with this proposal; whether the landed `tools/` tree differs from the r23 snapshot; or whether the round-22 build artifacts contain edit evidence beyond the four `S086` observations. These are named gaps, not implicit claims.
- **Corpus narrowness.** Four observations, two seats, two transcripts. The v2 shapes are designed against the *observed* keys; a future capture with a third edit shape (e.g. a rename-style edit, or `edit` carrying both `path` and a selector suffix) would need a shape rule this design does not yet have. A future corpus should be re-checked against §4.3's shape table before the v2 design is called complete.
- **Symlink/effect reading.** By construction, a v2 verdict is about the *spelling* of a target. If the declared `edit_paths` entries were to include symlinked paths, `local()` (33–36) would accept them and the audit would still say nothing about where the write lands — the v1 SCOPE string's own caveat, inherited unchanged.
- **No claim of runtime enforcement is made anywhere in this report**, and none should be made in the C2 summary: the main session confirms no native restrictive task toolset, so the v2 authority is an *audit* of recorded requests.

---

## 9. Handoff (ordered, concrete)

1. Implement the dispatcher (§4.1) with **no** edit to v1's `classify`, `allowed_keys`, line-72 tuple, line-120/131 pins, or the v1 selftest. Keep line 199's expectation green.
2. Add `tsukuroi-seat-bindings-v2` with the `edit_paths` seat field and the §4.2 validation (including `edit_paths ⊆ read_paths ∩ write_paths`).
3. Add `tsukuroi-seat-events-v2` with the §4.3 shape table (`i` optional; stream vs patch; missing `path` → `OPAQUE_PATCH`/UNKNOWN) and the single redaction token.
4. Bind the eight decision ids (§4.4) and reject any id outside the declared set; keep the `unknowns` array separate from `findings` and force exit 2 on any unknown (§4.5).
5. Add v2 selftest cases mirroring E-A…E-H and E-V1, with the §5.3 table transcribed verbatim as the expected (exit, id) pairs.
6. Decide §7.7 (`structured_edit_mode` placement) with main; then bind the C2 metric to the v2 artifact.
7. Keep the C2 summary wording at "explicit v2 **audit** authority for exact predeclared structured edit targets; body data opaque; no native enforcement, effect or reading proof; legacy v1 policy and historical reds unchanged" — never "enforcement", never "proves the write happened".
