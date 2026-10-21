# OracleV2Traversal — C2 structured-edit traversal oracle

Round 23 / attempt 1 · baseline `ae01e50f582016384e620022be38bf5367000e2e` · source-only oracle; nothing executed, fetched, or hashed.

**One-line answer.** The frozen v1 gate is not defective on traversal: for every tool it models it already refuses to normalize or expand a target. It simply has no `edit` branch, so a traversal-spelled edit and an exact-spelled edit both collapse to the same out-of-vocabulary finding. C2 needs an additive schema-v2 edit decision layer; retrofitting v1 would reclassify historical r22 edit events and is forbidden by the declared limits.

## 1. Basis

| Source | What it fixes here | Identity |
|---|---|---|
| `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` | the frozen v1 audit gate | declared SHA-256 `8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6` (supplied identity, not recomputed) |
| `.ufo/waves/round-23/preregister.json` | C2 command/scope, `edit_decisions`, `limits` | as read |
| `.ufo/waves/round-23/sources/edit-decision-policy.json` | eight decision rows, `evidence: S086`, `policy: round23-preregister` | as read |
| `.ufo/waves/round-23/sources/structured-edit-observations.json` | S086 observed r22 edit key shapes | as read |
| this seat's binding | a live r23 binding that already carries `edit_paths` | as issued |

Line anchors below are to `check-seat-bindings.py`. "Observed" = read from source; "[INFERENCE]" = derived, not declared; "Unresolved" = not fixable from the bound sources.

## 2. Observed facts in the v1 gate

- **F1 — v1 schema only.** `evaluate` requires `data.get('schema') == 'tsukuroi-seat-bindings-v1'` and `set(data) == {'schema','seats'}` (l.120-121). Any other token, including any v2 token, raises `ValueError('binding schema')`, is caught (l.163-166), and returns `CANNOT_EVALUATE`, code 2, `SCOPE-SCHEMA`. A v2 manifest today is indistinguishable from a malformed manifest.
- **F2 — `edit` is out of vocabulary, and the check short-circuits.** l.72-73 returns `['SCOPE-TOOL-UNKNOWN']` for any tool outside `{read, grep, glob, write, multi_tool_use.parallel, parallel}` **before** the `args` type check (l.74) and before `path` extraction (l.96). Consequence: `edit` with an exact declared path, with a dot-segment path, with `../`, with no args at all, or with `None` args all return the identical single finding. v1 cannot discriminate traversal from compliance for edit.
- **F3 — `edit_paths` is silently inert.** Seat validation (l.123-130) checks name, root, `commands == []`, `fetches == []`, then only `read_paths`/`write_paths` (each non-empty, `local()`-valid or the exact `skill://godspeed` read exception, duplicate-free). There is no `set(seat)` key check, so an `edit_paths` field is tolerated and then never read. This seat's own binding is an instance: it declares `edit_paths`, and under v1 that declaration has zero effect.
- **F4 — binding validation is literal-only.** `local()` (l.33-36) requires the exact `LANE + '/'` prefix, rejects `\`, rejects Unicode categories `Cc/Cf/Cs/Zl/Zp`, rejects any of `*?[];:`, and rejects every `''`, `.` or `..` segment in `path.split('/')[1:]`. Declared targets therefore can never themselves be dot-segment or alternate spellings.
- **F5 — request evaluation is literal-only, with no normalization anywhere.** `requested_path` (l.43-58) only special-cases `http(s)://`, `host:port/`, the exact literal `skill://godspeed`, and read/grep selector stripping; everything else goes through `local()`. Membership is plain Python string equality (`path not in binding[...]`, l.105). There is no `resolve`, `realpath`, `normpath`, case-fold, Unicode-normalize, percent-decode, or trim on either side of the comparison.
- **F6 — the self-test pins the intended v1 results.** Read-side dot segments: `LANE + '/../sibling/file'`, `LANE + '/x/../source'`, `LANE + '/./source'` → `SCOPE-PATH-DENIED` (l.194). Double slash `LANE + '//source'` → denied (l.241). Semicolon list with a foreign component → denied (l.198). Write-side child/extra/sibling → denied (l.197). `case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')` (l.199) — the edit-is-unknown result is **pinned as intended v1 behaviour**, not a bug report.
- **F7 — v1 disclaims exactly the things traversal arguments could overclaim.** `SCOPE` (l.17): "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."
- **F8 — the v1 argument vocabulary cannot express an observed edit.** Allowed keys (l.89-94) are read/grep/glob/write only; `stream_content`, `old_string`, `new_string` are unknown under every v1 tool, so any call that reached the key check with them yields `SCOPE-SCHEMA` (l.95,100). Under v1 as frozen such a call is first stopped as `SCOPE-TOOL-UNKNOWN` (F2), but the key set is the reason a naive "add `edit` to the tuple" patch would still fail the observed corpus. The S086 observations record exactly those keys.
- **F9 — the mode indicator precedent.** `request_audit_mode = int(code != 2)` (l.167): the mode field reports *evaluability*, not success. C2's metric `structured_edit_mode` is the direct analogue for a v2 dispatch. [INFERENCE: field name/spelling follows the metric name; no bound source declares the JSON key.]
- **F10 — two different "v1"s.** The eight decisions live in a document whose schema is `tsukuroi-edit-policy-v1`; the gate's manifest schema is `tsukuroi-seat-bindings-v1`. C2's "schema-v2" names the **audit authority** (manifest/event dispatch), not the policy document. Conflating them would make reviewers "upgrade" the policy file instead of the gate.

Two secondary observations, both test-coverage rather than behaviour:

- The write-side self-test pins child/extra/sibling spellings (l.197) but not a `/./`, `/../` or trailing-`/.` write spelling, even though write reaches the same `local()` predicate through l.102. Source-equal, self-test-unpinned.
- `case('empty-trace', ..., 0, None)` (l.211) accepts zero events as PASS. A v2 mode demonstrated by an empty trace would therefore prove nothing.

## 3. Absence of capability, not a defect in historical policy

The question is whether "dot segment and alternate path spelling never expands target" exposes a v1 defect. By inspection it does not, for the surface v1 claims:

1. **No normalization path exists.** Nothing in the gate transforms a request spelling into a different string, so a dot segment can never be resolved onto a declared target; the only possible outcome is denial by the segment predicate (F4) or by literal membership (F5).
2. **The declared list cannot be poisoned.** `read_paths`/`write_paths` are validated with `local()` and deduplicated (F3/F4), so an alternate spelling cannot enter the target list at declaration time.
3. **The self-test pins the denials** (F6), including the read-side dot-segment and double-slash cases, and pins `edit → SCOPE-TOOL-UNKNOWN` as the designed out-of-vocabulary result.

What v1 genuinely lacks is the entire edit decision layer: schema dispatch (F1), an `edit` vocabulary (F2), a live `edit_paths` authority (F3), edit body-key tolerance (F8), and a distinction between a well-formed traversal event and malformed input. That is a missing capability.

Calling it a defect and repairing v1 is also actively forbidden by the declared authority:

- C2 scope: "legacy schema-v1 policy and historical reds unchanged."
- `limits`: "No historical manifest/report rewrite or retrospective authorization."
- S086 records real r22 edit calls. Adding `edit` to v1's vocabulary would flip those recorded events from `SCOPE-TOOL-UNKNOWN` to `ALLOW`/`PATH-DENIED`; adding `stream_content`/`old_string`/`new_string` to the key set would flip them from a one-code-1 violation to `SCOPE-SCHEMA`/code 2. Either move rewrites the historical result of already-recorded requests — retrospective authorization or retrospective invalidation.

So the correct shape is additive: dispatch on the manifest schema token, keep the v1 branch byte-identical for v1 inputs (including `edit → SCOPE-TOOL-UNKNOWN`, the round-22 default manifest/events paths, and the `request_audit_mode` field), and give v2 its own edit evaluation and mode field.

A useful sanity check on the "defect" hypothesis: under v1 an edit of a *foreign* path and an edit of the seat's own declared report both produce `SCOPE-TOOL-UNKNOWN`. The gate is not wrongly authorizing traversal; it is declining to classify edit at all. That is absence.

## 4. Declared v2 authority (verbatim)

C2 scope: "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."

| id | decision | reason (declared) |
|---|---|---|
| `DECLARED_EDIT` | ALLOW | Exact target is predeclared for edit and for both read and write |
| `UNDECLARED_EDIT` | DENY | No implicit edit permission from generic report ownership |
| `READ_ONLY_EDIT` | DENY | Read authority never grants a write |
| `WRITE_ONLY_EDIT` | DENY | Edit also needs its explicit target read authority |
| `OPAQUE_PATCH` | UNKNOWN | Missing structured target is not inferred from opaque patch text |
| `EDIT_TRAVERSAL` | **DENY** | **No dot-segment or alternate spelling expands the target list** |
| `EDIT_EXTERNAL` | DENY | Remote or internal URIs do not become filesystem edit targets |
| `EXPANSION` | CHECK_EACH | Every recorded adapter read or write remains separately scoped |

Every row carries `evidence: S086` and `policy: round23-preregister`. The policy document's own scope: "Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof."

Reading the `EDIT_TRAVERSAL` row exactly: it fixes the **verdict** (DENY) and the **decision identity**, and it does not enumerate the spelling families. The faithful mapping of dot segments, empty segments, dot-dot segments, selector suffixes, separator variants, encoding variants and Unicode/whitespace variants is therefore `EDIT_TRAVERSAL` (the reason clause names "dot-segment **or alternate spelling**"), while an implementation that treats a given variant as merely a non-matching literal would produce `UNDECLARED_EDIT` — also DENY. **The verdict is invariant; the id is faithful-but-not-enumerated for the non-dot families.** This distinction matters because a fixture that hard-codes ids for undocumented families would be asserting more than the authority declares.

## 5. Non-expansion invariant (what v2 must hold)

Let `E`, `R`, `W` be the literal declared lists `edit_paths`, `read_paths`, `write_paths` from the manifest at the audited revision; let `t(e)` be the recorded `path` string of edit event `e`, taken verbatim.

1. `t(e)` is never normalized, trimmed, case-folded, Unicode-normalized, percent-decoded, selector-stripped or separator-split. `E/R/W` are never normalized either.
2. `ALLOW ⇔ t(e) ∈ E ∧ t(e) ∈ R ∧ t(e) ∈ W`, by exact string equality.
3. `t(e) ∉ E` ⇒ DENY (`UNDECLARED_EDIT`, or `EDIT_TRAVERSAL` when the spelling is a dot-segment/alternate-spelling form).
4. `t(e)` containing a `.`/`..`/empty segment, backslash, or `Cc/Cf/Cs/Zl/Zp` ⇒ `EDIT_TRAVERSAL` DENY **regardless of any canonical equivalence** to a declared target. Dot-dot resolution is not an admission path.
5. `t(e)` that is a remote/internal URI ⇒ `EDIT_EXTERNAL` DENY; it never becomes a filesystem target.
6. `e` with no structured `path` ⇒ `OPAQUE_PATCH` UNKNOWN; body text never supplies a target.
7. No event mutates `E/R/W`. No event adds a target; no event aliases one target onto another.
8. Each recorded event is judged alone (`EXPANSION` CHECK_EACH); a preceding read or write never lends its authority to an edit.

Boundary this invariant does **not** cross, inherited verbatim from F7 and the C2 scope: it is a statement about the recorded target list, not about filesystem resolution. A literal declared path that is a symlink still passes; a distinct spelling that a *downstream adapter* would resolve to the same inode is still denied (and is not claimed to have had no effect). No native prevention, no effect proof.

## 6. Independent literal fixture

Independent of any live seat binding and of the round-22 observation rows. Paths are literal spellings under the declared lane root; they need not exist, because the authority is spelling-only and makes no reading claim (F7).

Declared paths:

- `P` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md`
- `Q` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/report_owned.md`
- `U` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/read_only.md`
- `W` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/write_only.md`
- `X` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/sub/other.md` (body text only; never a target)

`P` is declared read + write + edit; `Q` read + write but not edit; `U` read + edit but not write; `W` write + edit but not read. That makes each of the four membership decisions reachable from one manifest.

### 6.1 Manifest

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "TraversalFixture",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/report_owned.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/read_only.md",
        "skill://godspeed"
      ],
      "write_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/report_owned.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/write_only.md"
      ],
      "edit_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/read_only.md",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/write_only.md"
      ],
      "commands": [],
      "fetches": []
    }
  ]
}
```

`tsukuroi-seat-bindings-v2` is the minimal-step token by the v1 naming convention; the exact v2 token is not declared by any bound source ([INFERENCE]; the dispatch requirement is declared, the literal token is not).

### 6.2 Events

`\u200b` in E18 denotes one U+200B ZERO WIDTH SPACE; every other character is literal.

```json
{
  "schema": "tsukuroi-seat-events-v2",
  "seats": [
    {
      "name": "TraversalFixture",
      "agent": "fixture-agent",
      "complete": true,
      "events": [
        {"tool": "edit", "args": {"i": "E01", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E02", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/./declared.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E03", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/sub/../declared.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E04", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture//declared.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E05", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md/.", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E06", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md:1-5", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E07", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md:raw", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E08", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md;/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/report_owned.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E09", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/report_owned.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E10", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/read_only.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E11", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/write_only.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E12", "stream_content": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md\n"}},
        {"tool": "edit", "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md", "stream_content": "body only"}},
        {"tool": "edit", "args": {"i": "E14", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md", "old_string": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/report_owned.md", "new_string": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/sub/other.md"}},
        {"tool": "edit", "args": {"i": "E15", "path": "skill://godspeed", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E16", "path": "xd://edit", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E17", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/%2e/declared.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E18", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared\u200b.md", "old_string": "a", "new_string": "b"}},
        {"tool": "edit", "args": {"i": "E19", "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/fixture/declared.md ", "old_string": "a", "new_string": "b"}}
      ]
    }
  ]
}
```

Each row carries exactly one offending feature, so the expected decision does not depend on any id-precedence rule that the bound sources leave undeclared.

## 7. Exact policy expectation

Declared fields are the decision id and verdict from §4; the audit record must carry both, plus the literal target and no normalized target field. The `findings[].id` string used by the tool is **not** declared — only the decision identity is ([INFERENCE: a stable finite machine id should mirror the decision id or be traceably mapped to it]).

| Row | Recorded `path` (feature) | Expected verdict | Faithful decision id | Binding strength |
|---|---|---|---|---|
| E01 | `P` exact | **ALLOW** | `DECLARED_EDIT` | exact (§4 row 1) |
| E02 | `P` with `/./` segment | **DENY** | `EDIT_TRAVERSAL` | exact (dot-segment clause) |
| E03 | `P` with `sub/../` | **DENY** | `EDIT_TRAVERSAL` | exact (dot-segment clause; canonical equivalence to `P` must **not** admit) |
| E04 | `P` with `//` | **DENY** | `EDIT_TRAVERSAL` | exact (empty segment = dot/alternate clause) |
| E05 | `P` with trailing `/.` | **DENY** | `EDIT_TRAVERSAL` | exact (dot-segment clause) |
| E06 | `P:1-5` | **DENY** | `EDIT_TRAVERSAL` | verdict exact; id faithful (alternate-spelling clause) — must not strip the suffix |
| E07 | `P:raw` | **DENY** | `EDIT_TRAVERSAL` | verdict exact; id faithful — must not strip the suffix |
| E08 | `P;Q` | **DENY** | `UNDECLARED_EDIT` (no split) — `UNDECLARED_EDIT` for `Q` if split | verdict exact; **must not** report one overall ALLOW |
| E09 | `Q` exact (read+write, not edit) | **DENY** | `UNDECLARED_EDIT` | exact (§4 row 2) |
| E10 | `U` exact (read+edit, no write) | **DENY** | `READ_ONLY_EDIT` | exact (§4 row 3) |
| E11 | `W` exact (write+edit, no read) | **DENY** | `WRITE_ONLY_EDIT` | exact (§4 row 4) |
| E12 | no `path`; `stream_content` contains `P` | **UNKNOWN** | `OPAQUE_PATCH` | exact (§4 row 5); must not be `SCOPE-SCHEMA`/code 2, must not seed a target |
| E13 | `P` + `stream_content` (observed S086 shape) | **ALLOW** | `DECLARED_EDIT` | exact; body opaque |
| E14 | `P`; `old_string`/`new_string` hold `Q` and `X` | **ALLOW** | `DECLARED_EDIT` | exact; **`Q` and `X` are not targets** and are not scoped by this event |
| E15 | `skill://godspeed` | **DENY** | `EDIT_EXTERNAL` | exact (§4 row 7: internal URI) |
| E16 | `xd://edit` | **DENY** | `EDIT_EXTERNAL` | exact (§4 row 7) |
| E17 | `P` with `%2e` segment | **DENY** | `EDIT_TRAVERSAL` | verdict exact; id faithful — decode must not occur before the decision |
| E18 | `P` with U+200B before `.md` | **DENY** | `EDIT_TRAVERSAL` | verdict exact; id faithful (U+200B is `Cf`; `local()` rejects it) |
| E19 | `P` with trailing space | **DENY** | `EDIT_TRAVERSAL` | verdict exact; id faithful — trim must not occur |

Aggregate expectation for this fixture, if and only if v2 is dispatched:

- `seats_bound: 1`, `requests_total: 19`, status `FAIL`, exit code **1** (findings present, but the input is evaluable and well-formed).
- `structured_edit_mode: 1`, paralleling `request_audit_mode: int(code != 2)` (F9). Mode reflects **capability presence**, not pass/fail; a code-1 trace must still report mode 1 or C2's target is unreachable on any trace that contains a denial.
- `violations` is 15 if UNKNOWN is not counted and 16 if it is; the policy does not declare UNKNOWN accounting, so the fixture fixes only "at least one finding per DENY, exactly none for the three ALLOW rows".
- **No** `SCOPE-SCHEMA`, `SCOPE-TOOL-UNKNOWN` or `CANNOT_EVALUATE` may appear: §4 provides a decision for every row, so classifying a traversal or external spelling as malformed input would contradict the declared authority.

Contrast under the frozen v1 branch, derived from source, not executed:

- The same v2 manifest → `CANNOT_EVALUATE`, code 2, `SCOPE-SCHEMA` (F1). Mode field absent ⇒ `structured_edit_mode` 0 ⇒ C2 target unreachable.
- The same 19 events under a v1 manifest → 19 × `SCOPE-TOOL-UNKNOWN` (F2), code 1, zero discrimination between E01 and E03. That is the absence C2 measures.

### 7.1 Manifest-level cases

| Case | Manifest change | Expected |
|---|---|---|
| M1 | duplicate `edit_paths` entry (`P` twice) | reject manifest (schema-class, code 2) — parity with the existing `len(paths) != len(set(paths))` rule (l.127-129) |
| M2 | `edit_paths` entry spelled `.../fixture/./declared.md` | reject manifest — a declaration is the target list; a non-literal declaration is the declaration-side expansion vector. [INFERENCE from "exact predeclared" + `local()` parity; not separately enumerated] |
| M3 | `edit_paths` absent | one of {absent, empty} must be legal (see M4) |
| M4 | `edit_paths: []` | one of {absent, empty} must be legal |

M3/M4 are a derivable pair: v1 requires every seat's `read_paths` and `write_paths` to be non-empty (l.127-128). If v2 also required `edit_paths` non-empty, every seat would be forced to hold edit authority, which the declared policy does not imply and which contradicts the existence of read-only or write-only seats (the `READ_ONLY_EDIT`/`WRITE_ONLY_EDIT` rows presuppose edit targets that sit on only one side). At least one of "absent" or "empty" must therefore be a valid expression of *no edit authority*. No bound source says which.

## 8. Implementation hazards grounded in the v1 source

These are the concrete ways a v2 branch could accidentally realize the forbidden expansion:

1. **Do not reuse selector stripping for edit.** l.102 strips at `:` for read/grep. Applied to edit, `P:1-5` or `P:raw` would reduce to `P` and ALLOW. Edit has no selector semantics; fixtures E06/E07 pin the required DENY.
2. **Do not reuse `;` splitting for edit.** l.99 splits for grep/glob. Applied to edit, `P;Q` would yield two targets and could authorize `Q` on `P`'s authority. Fixture E08 pins DENY with no overall ALLOW.
3. **Do not inherit the v1 key set for edit.** F8: a v2 edit branch that reused the l.89-94 key sets would flag the observed S086 shapes (`i,path,old_string,new_string` and `path,stream_content`) as `SCOPE-SCHEMA`. The minimum tolerated edit keys covering the observed corpus are `{i, path, old_string, new_string, stream_content}`; all body keys are opaque.
4. **Do not inherit `missing explicit path ⇒ ValueError`.** l.96-98 raises; the declared `OPAQUE_PATCH` row (and the S086 `stream_content` shape) requires a pathless edit event to be a decidable UNKNOWN, not a schema failure.
5. **Validate and dedup `edit_paths` with the same predicate as read/write.** Otherwise M2 becomes legal and the declaration side itself accepts a dot segment.
6. **Set the mode field on well-formed dispatch, independent of findings.** l.167 is the precedent; a mode derived from exit 0 would make any trace containing a denial look like absent capability.
7. **Keep the revision-bound reads and empty allowlists.** v2 must still read manifest and events from the audited revision (l.270-277) and still require `root == LANE`, `commands == []`, `fetches == []`. v2 adds an edit decision, not execution or fetch authority.
8. **Keep the v1 branch byte-identical**, including default paths for the round-22 manifest/events, the `SCOPE` string, the self-test expectations, and `edit → SCOPE-TOOL-UNKNOWN` (F6/P3).

## 9. Limits of this oracle

- No execution, hashing, import, listing or fetch; every behavioural statement is by source inspection. The contrast results in §7 are derivations from l.72-73 and l.120, not observed runs.
- No native enforcement claim: a v2 DENY is a recorded finding, not a blocked call. No native restrictive per-seat tool interface exists (preregister `limits`).
- No effect, symlink, reading or recorder-completeness proof (§5 boundary).
- The exact v2 schema tokens, the `structured_edit_mode` JSON key, the `findings[].id` vocabulary, UNKNOWN's contribution to `violations`, and the absent-vs-empty `edit_paths` choice are not declared by the bound sources.
- Id precedence for a hypothetical multi-feature event is undeclared; the fixture avoids it by using single-feature rows.

## 10. Unresolved

1. Exact literal v2 schema token(s); only "schema-v2" is declared.
2. Exact machine finding ids and their mapping to the eight decision ids.
3. Whether `OPAQUE_PATCH`/UNKNOWN increments `violations` and `status`.
4. Whether `edit_paths` is optional or may be empty (M3/M4).
5. Whether the aggregate C2 run is expected to exit 0 or whether `structured_edit_mode: 1` alone satisfies the target on a FAIL trace.
6. Whether a selector-like `:` suffix and separator/encoding/Unicode/whitespace variants are to be recorded as `EDIT_TRAVERSAL` or `UNDECLARED_EDIT`; only the DENY verdict is fixed by the authority.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2traversal
Scope: executed=none
