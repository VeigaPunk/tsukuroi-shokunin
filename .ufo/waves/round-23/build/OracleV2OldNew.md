# OracleV2OldNew — old v1 seat gate vs declared v2 structured-edit authority

Seat: `TsukuroiR23-2.OracleV2OldNew-7`. Source-only design oracle; no execution, no
import, no hash, no fetch, no install. The digest in the receipt is accepted as supplied
identity. Target content was read as data only.

Tags used below: `[OBSERVED]` = literal source text or literal JSON member read from a
declared path; `[INFERENCE]` = a consequence I derive from that text, not executed;
`[GAP]` = a question the declared authority does not settle.

## Axes

1. **Authority generation** — old seat-events gate schema `tsukuroi-seat-bindings-v1`
   versus the new edit-policy document `tsukuroi-edit-policy-v1` versus the schema-v2
   seat authority named by C2. These are three different version axes; conflating the
   `-v1` in the new policy document with the old seat schema is the main naming trap.
2. **Shape-to-decision exactness** — which literal event shape yields which of the eight
   declared decisions, and which shape is not expressible at all.
3. **Fail-closed direction** — an unknown tool must not be silently mapped onto write
   authority; a missing structured target must be UNKNOWN, not ALLOW and not DENY.
4. **Non-retroactivity** — r22 observed edit requests are shape evidence only; the
   preregister forbids historical rewrite or retrospective authorization.
5. **Fixture independence** — the fixture must not reuse S086 report bodies or marker
   strings; it uses synthetic filenames and synthetic edit bodies.

## 1. Answer

1. The frozen v1 gate has **no structured-edit capability at all**. This is absence, not
   a defect: `classify` rejects the tool name before it ever inspects `path` or argument
   keys, so an `edit` request is recorded as `SCOPE-TOOL-UNKNOWN` and is never evaluated
   for path authorization. A valid declared v2 edit cannot be expressed under v1 by any
   relabeling of the same request.
2. A **valid declared edit** under the new authority is a path-centric shape: tool `edit`
   (or `functions.edit`), an argument mapping with a non-empty string `path` that is
   lane-absolute, lexically local, selector-free, non-URI, and literally present in
   `edit_paths` **and** `read_paths` **and** `write_paths`. The body (`old_string` /
   `new_string`) is opaque to the target decision. Exact v2 expectation:
   `DECLARED_EDIT` / `ALLOW`, evidence `S086`, policy `round23-preregister`, zero findings.
3. A missing `path` is `OPAQUE_PATCH` / `UNKNOWN` under v2. It is not DENY and it is not
   v1's `SCOPE-SCHEMA`, which is a gate-level cannot-evaluate category.
4. The v1 gate is **not defective for having been written that way**. It fails closed
   (unknown tool becomes a finding, not a pass), it does not silently reuse `write_paths`
   for edits, and it emits no false `DENY` verdict for a decision vocabulary that did not
   yet exist. The change C2 asks for is a new declared schema and a new decision
   vocabulary, plus a strictness increase for the surgical shape.

## 2. What the frozen v1 gate actually declares `[OBSERVED]`

Source: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (310 lines).
Line anchors below are from `grep` over that file.

- Line 2 docstring: `Audit recorded requests against frozen prompt scopes; not preventive enforcement.`
- Line 17 scope constant: `SCOPE = 'Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.'`
- Lines 33–36 `local(path)`: absolute under `LANE`, no backslash, no control
  characters (`Cc`, `Cf`, `Cs`, `Zl`, `Zp` per lines 29–30), none of `*?[];:`, and no
  empty/`.`/`..` component after the root.
- Lines 72–73 tool vocabulary:
  `if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'): return ['SCOPE-TOOL-UNKNOWN']`.
  This check runs **after** `functions.` stripping (line 65) and after the exec/fetch
  checks (lines 68–71), and **before** the argument-dict check (line 74), the key check
  (line 95), and the path read (lines 96–98).
- Lines 89–94 key vocabulary: `read {i,path}`, `grep {i,pattern,path,case,gitignore,skip}`,
  `glob {i,path,hidden,gitignore,limit}`, `write {i,path,content}`. There is no key set
  for `edit`; `old_string`/`new_string` appear nowhere in the file.
- Line 95: any key outside the table makes `findings` start with `SCOPE-SCHEMA`.
- Lines 96–98: a non-string or empty `path` raises `ValueError('missing explicit path')`
  for the tools that reach this point.
- Lines 101–106: path outcome is either a denial id from `requested_path` or
  `SCOPE-PATH-DENIED`; the membership list is
  `binding['write_paths' if tool == 'write' else 'read_paths']`. `write` therefore needs
  no read authority; `read`/`grep`/`glob` need no write authority.
- Lines 120–121: manifest must be a dict whose key set is exactly `{'schema','seats'}`,
  `schema == 'tsukuroi-seat-bindings-v1'`, non-empty seats. Otherwise
  `ValueError('binding schema')` → caught at line 163, `SCOPE-SCHEMA` at site `input`,
  code 2.
- Lines 124–128: per-seat validation checks `name` regex, `root == LANE`, empty
  `commands`, empty `fetches`, and iterates only `('read_paths','write_paths')`. There is
  **no seat key-set equality check**, so an extra member such as `edit_paths` is accepted
  and then never read. Lines 130 and 167 keep the whole seat dict, but no later code path
  reads `edit_paths`.
- Line 160: `violations += sum(fid != 'SCOPE-SCHEMA' for fid in ids)`; `SCOPE-TOOL-UNKNOWN`
  therefore counts as a violation.
- Line 162: code `2` if any trace is incomplete or any `SCOPE-SCHEMA` finding exists,
  else `1` if any finding exists, else `0`. Line 167 maps code to
  `PASS`/`FAIL`/`CANNOT_EVALUATE` and `request_audit_mode = int(code != 2)`.
- Line 177 selftest binding uses schema `tsukuroi-seat-bindings-v1` and
  `read_paths`/`write_paths` only.
- Line 186: `skill://godspeed` is allowed for **read** only.
- Line 199: `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')` — the selftest locks
  "edit is an unknown tool" as a **passing** expectation of v1.
- Lines 215–217: `skill://godspeed` as a write target, `skill://other`, and
  `skill://godspeed:raw` are all denied.
- Lines 286–287: CLI defaults remain `--manifest .ufo/waves/round-22/build/bindings.json`
  and `--events .ufo/waves/round-22/build/events.json`.

Absence check `[OBSERVED]`: a literal grep over the whole file for
`edit_paths|old_string|new_string|structured_edit_mode|DECLARED_EDIT` returns **no
matches**; the token `'edit'` occurs only in the selftest case at line 199. This is
literal coverage of that file, not a semantic proof about other tools.

## 3. Absence versus historical defect

| Proposition | Evidence in the frozen gate | Verdict |
|---|---|---|
| v1 should have allowed the r22 edits | `edit` is not in the line 72 vocabulary; the decision vocabulary of the edit policy did not exist in r22 | **Absence of new capability** |
| v1 denied the edits | It emits `SCOPE-TOOL-UNKNOWN`, a finding id, and FAIL status; it has no `DENY` decision rows and never asserts an edit authorization outcome | **Absence of decision vocabulary**, not a denial |
| v1 silently routed edit through write authority | Tool check (72–73) precedes key/path handling (95–106); no edit request reaches `write_paths` | **Fail-closed**, no implicit authorization |
| v1 accepted an `edit_paths` member as authority | Lines 124–128 do not constrain seat keys; lines 130/167 retain the dict; nothing reads `edit_paths`; an edit event still hits line 73 | **Inert field**, latent false-assurance risk, fails closed at event time |
| v1 handled a missing structured target as UNKNOWN | Lines 96–98 raise; line 162/164 makes that `SCOPE-SCHEMA` / CANNOT_EVALUATE, not a policy verdict | **Different category**, not a wrong decision |
| v1 mishandled `{path, old_string, new_string}` | Under the label `write`, lines 95 and 100 produce `SCOPE-SCHEMA`; under `edit`, line 73 produces `SCOPE-TOOL-UNKNOWN` | **Shape not expressible** under either label; vocabulary gap |

Historical boundary `[OBSERVED]` from the preregister limits:
`No historical manifest/report rewrite or retrospective authorization`. The four S086
requests were made in round 22. They are evidence for the shape; they are not re-adjudicated
by a v2 policy, and applying v2 to them would be a retrospective reclassification.

The one fair criticism is not "v1 was wrong" but "a v1 manifest carrying `edit_paths`
looks authoritative and is not". C2's schema bump is the correct fix: authority must be
explicit in the schema version, not inferred from an ignored member.

## 4. Declared v2 authority `[OBSERVED]`

Source: `.ufo/waves/round-23/sources/edit-decision-policy.json`.

- `schema`: `tsukuroi-edit-policy-v1`
- `source_path`: `.ufo/waves/round-23/sources/structured-edit-observations.json`
- `scope`: `Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.`

Eight rows, verbatim (every row carries `evidence: "S086"`, `policy: "round23-preregister"`):

| id | decision | reason |
|---|---|---|
| `DECLARED_EDIT` | `ALLOW` | Exact target is predeclared for edit and for both read and write |
| `UNDECLARED_EDIT` | `DENY` | No implicit edit permission from generic report ownership |
| `READ_ONLY_EDIT` | `DENY` | Read authority never grants a write |
| `WRITE_ONLY_EDIT` | `DENY` | Edit also needs its explicit target read authority |
| `OPAQUE_PATCH` | `UNKNOWN` | Missing structured target is not inferred from opaque patch text |
| `EDIT_TRAVERSAL` | `DENY` | No dot-segment or alternate spelling expands the target list |
| `EDIT_EXTERNAL` | `DENY` | Remote or internal URIs do not become filesystem edit targets |
| `EXPANSION` | `CHECK_EACH` | Every recorded adapter read or write remains separately scoped |

The same eight `(id, decision, reason)` triples appear in the preregister's
`edit_decisions` array. The policy file adds `evidence` and `policy` per row; it adds no
ninth row.

Binding to the goal, from the preregister `[OBSERVED]`:

- C1 `axis=depth`, `metric=validated_edit_decisions`, `before=0`, `target=8`,
  command `python3 tools/check-edit-contract.py --revision <REV>`.
- C2 `axis=operability`, `metric=structured_edit_mode`, `before=0`, `target=1`,
  command `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`,
  scope includes `New explicit schema-v2 audit authority for exact predeclared structured
  edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque,
  no native enforcement/effects claim.`
- C2's command overrides both r22 defaults; the r22 defaults at lines 286–287 are legacy
  convenience, not a silent-audit path when the command is used as declared.

**Naming trap `[OBSERVED]`:** `tsukuroi-edit-policy-v1` is the new policy document.
`tsukuroi-seat-bindings-v1` is the old gate manifest schema. The schema-v2 in C2 is the
new seat authority. These are independent version labels; `-v1` in the policy name does
not mean "legacy behavior".

## 5. Shape evidence and the valid declared edit shape

Source: `.ufo/waves/round-23/sources/structured-edit-observations.json`.
Four observations, bodies omitted (`body_fields: "omitted; no report text copied"`):

| seat | request line | tool | argument keys | path |
|---|---|---|---|---|
| `CritRuntime` | 15 | `edit` | `path`, `stream_content` | its own `round-22/build/CritRuntime.md` |
| `OraclePathArtifact` | 30 | `edit` | `i`, `new_string`, `old_string`, `path` | its own `round-22/build/OraclePathArtifact.md` |
| `OraclePathArtifact` | 33 | `edit` | `i`, `new_string`, `old_string`, `path` | same |
| `OraclePathArtifact` | 36 | `edit` | `i`, `new_string`, `old_string`, `path` | same |

Key lists are sets; their recorded order is alphabetical. The canonical structured-edit
target shape is therefore `{i, path, old_string, new_string}` with `path` present. The
`CritRuntime` entry shows a second body-key family (`stream_content`) with a structured
path; the policy is body-opaque, so the body key must not decide the target verdict
`[INFERENCE]`.

Valid declared edit, stated as a predicate over a seat binding `B` and one recorded event:

```
tool      = 'edit' or 'functions.edit'                      # functions. prefix normalized as v1 line 65
args      = a mapping
path      = args['path'], non-empty string
local     : path.startswith(LANE + '/')                     # v1 lines 33-36
            and '\\' not in path
            and no Cc/Cf/Cs/Zl/Zp character
            and no '*', '?', '[', ']', ';', ':'
            and every component after the root is not '', '.', '..'
not URI   : not http(s)://, not host:port/, not skill://, not artifact://, not xd://
declared  : path in B.edit_paths and path in B.read_paths and path in B.write_paths
=> decision DECLARED_EDIT, value ALLOW, zero findings
```

Notes on the predicate:

- The three-list conjunction is literal: `DECLARED_EDIT` requires the target to be
  "predeclared for edit and for both read and write". A target that is in `edit_paths`
  but not `write_paths`, or not `read_paths`, cannot be ALLOW.
- The body is not part of the decision. `old_string`/`new_string` are the observed
  adapter shape, not a policy requirement; the policy scope says "structured target
  metadata only". Whether the v2 gate schema-rejects `stream_content` is `[GAP]`.
- The path must be selector-free: `local()` rejects `:`, and the policy declares no
  selector grammar for edits. The suffix spelling is an "alternate spelling" and belongs
  to `EDIT_TRAVERSAL` `[INFERENCE]`; it cannot be ALLOW because exact membership fails.
- `skill://godspeed` is a legal **read** value under v1 (line 186) but is an internal URI;
  `EDIT_EXTERNAL` says internal URIs do not become filesystem edit targets, so an edit
  attempt on it is DENY, not an inherited read exception `[INFERENCE]`.

**Decision partition `[INFERENCE]`** (the authority fixes the decision values and the
ALLOW conjunction; the precedence below is my derived partition, since all eight rows
must be reachable without contradiction):

| target class | row | decision |
|---|---|---|
| in `edit ∩ read ∩ write`, lexically valid | `DECLARED_EDIT` | ALLOW |
| in `read ∩ write`, not in `edit` (generic report ownership) | `UNDECLARED_EDIT` | DENY |
| in `read`, not in `write` | `READ_ONLY_EDIT` | DENY |
| in `write`, not in `read` (including in `edit` but not `read`) | `WRITE_ONLY_EDIT` | DENY |
| in `edit` but not `write`, while in `read` | `READ_ONLY_EDIT` | DENY |
| in no list | `UNDECLARED_EDIT` | DENY |
| dot-segment or alternate spelling | `EDIT_TRAVERSAL` | DENY |
| remote or internal URI | `EDIT_EXTERNAL` | DENY |
| `path` member absent | `OPAQUE_PATCH` | UNKNOWN |
| wrapper expands into multiple adapter calls | `EXPANSION` | CHECK_EACH |

`EDIT_TRAVERSAL`, `EDIT_EXTERNAL`, and `OPAQUE_PATCH` are checked before membership: none
of them names a legal declared target, so membership cannot rescue them.

## 6. Independent literal fixture (inert; no file is created)

Synthetic names and markers; nothing here is copied from an S086 report body. The fixture
is illustrative text for design review, not a request to write any path.

Manifest proposal, `schema-v2` = v1 seat fields plus `edit_paths` `[INFERENCE]`:

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "FixtureSeat",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBeta.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOmega.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

Event trace proposal (events schema reuse is `[INFERENCE]`; the policy file announces no
events-schema change):

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "FixtureSeat",
      "agent": "fixture-agent",
      "complete": true,
      "events": [
        {
          "tool": "edit",
          "args": {
            "i": "Editing FixtureAlpha",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md",
            "old_string": "FIXTURE-OLD-9b1f",
            "new_string": "FIXTURE-NEW-4e2a"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing FixtureGamma",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md",
            "old_string": "FIXTURE-OLD-1c07",
            "new_string": "FIXTURE-NEW-8d31"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing FixtureBeta",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureBeta.md",
            "old_string": "FIXTURE-OLD-77aa",
            "new_string": "FIXTURE-NEW-77ab"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing FixtureOmega",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureOmega.md",
            "old_string": "FIXTURE-OLD-5e5e",
            "new_string": "FIXTURE-NEW-5e5f"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Applying opaque patch",
            "patch": "@@ FIXTURE @@"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing via dot segment",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/scratch/../FixtureAlpha.md",
            "old_string": "FIXTURE-OLD-c0de",
            "new_string": "FIXTURE-NEW-c0df"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing via selector spelling",
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md:raw",
            "old_string": "FIXTURE-OLD-a1a1",
            "new_string": "FIXTURE-NEW-a1a2"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing internal URI",
            "path": "skill://godspeed",
            "old_string": "FIXTURE-OLD-eeee",
            "new_string": "FIXTURE-NEW-eeef"
          }
        },
        {
          "tool": "edit",
          "args": {
            "i": "Editing remote URI",
            "path": "https://example.invalid/FixtureAlpha.md",
            "old_string": "FIXTURE-OLD-f00d",
            "new_string": "FIXTURE-NEW-f00e"
          }
        },
        {
          "tool": "multi_tool_use.parallel",
          "args": {
            "tool_uses": [
              {
                "recipient_name": "functions.read",
                "parameters": {
                  "i": "Reading FixtureAlpha",
                  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureAlpha.md"
                }
              },
              {
                "recipient_name": "functions.edit",
                "parameters": {
                  "i": "Editing FixtureGamma",
                  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/FixtureGamma.md",
                  "old_string": "FIXTURE-OLD-2b2b",
                  "new_string": "FIXTURE-NEW-2b2c"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## 7. Exact v2 expectations for the fixture `[INFERENCE]` mapping over `[OBSERVED]` rows

| event | target class | policy row | decision |
|---|---|---|---|
| 1 Alpha | in `edit ∩ read ∩ write` | `DECLARED_EDIT` | ALLOW, zero findings |
| 2 Gamma | in `read ∩ write`, not `edit` | `UNDECLARED_EDIT` | DENY |
| 3 Beta | in `read` only | `READ_ONLY_EDIT` | DENY |
| 4 Omega | in `write` only | `WRITE_ONLY_EDIT` | DENY |
| 5 no `path` | missing structured target | `OPAQUE_PATCH` | UNKNOWN |
| 6 `scratch/../` | dot-segment | `EDIT_TRAVERSAL` | DENY |
| 7 `:raw` suffix | alternate spelling | `EDIT_TRAVERSAL` | DENY |
| 8 `skill://godspeed` | internal URI | `EDIT_EXTERNAL` | DENY |
| 9 `https://…` | remote URI | `EDIT_EXTERNAL` | DENY |
| 10 parallel read + edit | wrapper expansion | `EXPANSION` | CHECK_EACH: read child no finding, edit child `UNDECLARED_EDIT` DENY, two independent outcomes |

Gate-level expectation for a conforming v2 run: `structured_edit_mode` 1 (the metric the
preregister names), and the per-event UNKNOWN must remain distinguishable from both ALLOW
and DENY. `UNKNOWN` must not be counted as an authorization denial `[INFERENCE]`, because
the row's literal decision value is `UNKNOWN`, not `DENY`; the policy also refuses to infer
a target from patch text. Exact scoring of UNKNOWN in `violations` is `[GAP]`.

## 8. The same fixture through the frozen v1 gate (predicted from source, not executed)

1. Keep `schema: tsukuroi-seat-bindings-v2`: lines 120–121 reject the manifest before any
   seat is bound → `SCOPE-SCHEMA` at site `input`, code 2, status CANNOT_EVALUATE,
   `request_audit_mode` 0, `seats_bound` 0 (line 166 falls back to `{}` because `bound`
   was never assigned).
2. Relabel only the schema to `tsukuroi-seat-bindings-v1`, keep `edit_paths`: the seat is
   accepted (lines 124–128 never inspect extra keys). Every direct `edit` event returns
   `['SCOPE-TOOL-UNKNOWN']` (line 73) before path or key inspection. Findings are
   non-empty → code 1 FAIL; each event increments `violations` (line 160).
3. Event 5 with no `path` still returns `SCOPE-TOOL-UNKNOWN`, because line 73 precedes the
   missing-path raise at line 98. The v1 gate therefore cannot express UNKNOWN at all.
4. Event 10: the read child is allowed; the edit child returns `SCOPE-TOOL-UNKNOWN`; the
   overall result is FAIL code 1. v1 already evaluates parallel children additively, so
   `EXPANSION`'s "check each" structure is **not** the missing piece; the missing piece is
   the edit row and the per-row verdict.
5. If the same `{path, old_string, new_string}` body is relabeled `write`: line 95 sees
   `old_string`/`new_string` outside `{'i','path','content'}`, adds `SCOPE-SCHEMA`, and
   line 162 raises the result to code 2 CANNOT_EVALUATE. The path may still be in
   `write_paths`; the shape, not the path, blocks it.
6. `edit_paths` containing a non-local or URI value would be accepted by the v1 manifest
   check without any finding, because the field is never read. This is the inert-authority
   hazard, not a misclassification.

## 9. Old/new on this seat's own declared binding

Delivered seat binding, verbatim members `[OBSERVED]`:
`name = OracleV2OldNew`, `root = /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
`read_paths` = seven entries including the report path and `skill://godspeed`,
`write_paths` = the single report path, `edit_paths` = the same report path,
`commands = []`, `fetches = []`.

| Event on the same target (report path) | v1 `tsukuroi-seat-bindings-v1` | declared v2 edit authority |
|---|---|---|
| `edit` report path, canonical body | `SCOPE-TOOL-UNKNOWN` (line 73) | `DECLARED_EDIT` ALLOW (path in read+write+edit) |
| `write` report path | allowed by `write_paths` (line 105); no read needed | unchanged legacy rule (C2: legacy policy unchanged) |
| `edit` a declared source read path | `SCOPE-TOOL-UNKNOWN`, not `READ_ONLY_EDIT` | `READ_ONLY_EDIT` DENY |
| `edit` any other lane path | `SCOPE-TOOL-UNKNOWN` | `UNDECLARED_EDIT` DENY |
| `edit` `skill://godspeed` | `SCOPE-TOOL-UNKNOWN` | `EDIT_EXTERNAL` DENY, despite read authority |
| `edit` no `path` | `SCOPE-TOOL-UNKNOWN` | `OPAQUE_PATCH` UNKNOWN |

Consequence: the new edit authority is **narrower** than the legacy write authority on the
same target — `edit` needs read+write+edit predeclaration, while `write` still needs only
`write_paths`. That is a declared boundary, not a defect: C2's scope says the legacy
schema-v1 policy is unchanged, so `edit_paths` adds surgical-edit authority and does not
constrain whole-file writes. A v2 run that claimed otherwise would be inventing policy.

## 10. Remaining gaps and limits

1. `[GAP]` The literal v2 manifest schema string and top-level key set are not declared.
   C2's prose says "schema-v2"; it does not give the literal token. The fixture's
   `tsukuroi-seat-bindings-v2` is my proposal.
2. `[GAP]` `edit_paths ⊆ read_paths ∩ write_paths` validation at manifest time versus
   event time is not declared. Only the ALLOW conjunction is literal. If checked at
   manifest time, `READ_ONLY_EDIT` and `WRITE_ONLY_EDIT` remain reachable for targets that
   are not in `edit_paths`; the rows do not collapse.
3. `[GAP]` The emitted finding-id strings for the eight decisions are not declared. The
   policy ids are the natural evidence labels; whether the gate emits `DECLARED_EDIT` or a
   new transport id is unstated.
4. `[GAP]` The emissive condition for `structured_edit_mode = 1` is not declared. A gate
   that accepts schema v2 but sees no edit event should not claim the mode; my reading is
   "1 only when at least one edit event is evaluated under the policy".
5. `[GAP]` Effect of `UNKNOWN` on status, `violations`, and `request_audit_mode` is not
   declared. It is neither ALLOW nor DENY and must not be silently folded into either.
6. `[GAP]` No body-key allowlist is declared. The S086 `stream_content` variant shows that
   bodies vary; body opacity implies key names should not decide the target, but the gate's
   schema handling of unknown body keys is unstated. Do not turn the observed
   `{i,path,old_string,new_string}` set into policy.
7. `[GAP]` A foreign absolute path outside `LANE` has no dedicated row. `EDIT_TRAVERSAL`
   is spelling-based, `EDIT_EXTERNAL` is URI-based, `UNDECLARED_EDIT` is membership-based.
   The nearest reading is `UNDECLARED_EDIT` via failed membership, with manifest-level
   `local()` blocking the binding itself; the authority does not choose.
8. `[GAP]` `EDIT_TRAVERSAL` is the inferred row for a selector suffix; the literal row
   says "dot-segment or alternate spelling", which fits but is not enumerated.
9. `[GAP]` Events-schema reuse (v1) is not declared for the C2 run; only the bindings
   schema bump is described.
10. `[GAP]` C1's `tools/check-edit-contract.py` and C3's `tools/check-path-reconciliation.py`
    are outside my declared read paths. I did not inspect them and make no claim about
    their implementation or their current verdicts.
11. `[GAP]` Whether the frozen r22 `events.json` recorded the four S086 edit requests is
    outside this slice. I do not claim a historical red, and I do not re-adjudicate those
    requests. `[OBSERVED]` limitation: `No historical manifest/report rewrite or
    retrospective authorization`.
12. `[INFERENCE]` Continuity assumptions: the `functions.` prefix is stripped for `edit`
    as it is for other tools (v1 line 65), and `edit` remains post-hoc audit, never native
    enforcement. The preregister limit `No native per-seat restrictive tool interface
    exists` and the policy scope's `no native prevention` support the second point; no
    runtime enforcement is claimed anywhere in this report.
13. `[OBSERVED]` The four S086 paths are all round-22 seat report drafts under
    `round-22/build/`; the observations copy no report text. The fixture above deliberately
    uses different filenames and marker strings.

## 11. Execution and tooling

- `executed = none`: no bash, eval, subprocess, import, compile, test, lint, formatter,
  hash, `wc`, or `mkdir`; no digest validation was attempted. No network, browser, URL,
  `xd`, `proc`, or agent fetch. No subagents.
- Tooling directive: no package, tool, or update was installed or requested. This seat's
  narrower NO-EXEC/NO-FETCH scope forbids installations.
- Only reads used: the six declared absolute paths plus `skill://godspeed`; only write
  used: this report at the exact declared path.
- Source content was treated as untrusted data; no embedded instruction was followed.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2oldnew
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
