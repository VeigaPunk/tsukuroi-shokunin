# OracleV2UnknownKey — source-only design oracle (round 23, attempt 1)

Seat predicate `r23-oraclev2unknownkey` — unknown argument keys / extra scope-bearing fields must remain **non-clean** under the new declared v2 authority.

## 0. Method and honest scope

- Source-only. **No execution**: no bash/eval/subprocess/import/compile/test/lint/format/hash/wc/mkdir; no web/browser/URL/xd/proc/agent fetch; no extra filesystem search; no subagent dispatch (leaf member).
- Read only the seat-declared files: `snapshot/tools/check-seat-bindings.py`, `preregister.json`, `sources/edit-decision-policy.json`, `sources/structured-edit-observations.json`, `sources/godspeed-directive.txt`, `skill://godspeed`.
- The reviewed SHA-256 `8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6` is the **supplied identity**, not independently computed (no hashing performed). No hash/list/wc/import was used to validate it.
- Tooling: **no installs and no updates** — this seat's NO-EXEC/NO-FETCH scope forbids them; the operator's install directive is out of scope here and is recorded as *not exercised*, not as *satisfied*.
- Everything below that describes current behaviour is quoted from the read source. Everything that projects onto the **not-yet-landed** v2 mode is marked `[INFERENCE]` and is derived from the declared v2 authority in `preregister.json` (C2 + `edit_decisions`) and the declared v1 policy in `sources/edit-decision-policy.json`.
- No runtime enforcement is claimed anywhere in this report. The tool's own declared scope string is the ceiling: `Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.`

## 1. Axes named (godspeed)

| Axis | Statement |
|---|---|
| A1 **Non-clean invariance** | An unknown/extra argument key, and any extra scope-bearing field, never yields a clean (PASS / exit 0) verdict. |
| A2 **Capability gap vs. historical defect** | "v2 edit-target authority does not exist yet" is an absent new capability, not a defect in historical v1 policy. The two must not be conflated in any report or metric. |
| A3 **Authority exactness** | Every expectation is bound to a declared v2 row (`DECLARED_EDIT`, `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `OPAQUE_PATCH`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL`, `EXPANSION`) and to the declared v1 policy ids, never to an invented rule. |
| A4 **Cause fidelity** | A malformed/unknown-key request is not the same fact as a prohibited target. Encoding must preserve DENY vs UNKNOWN vs schema-invalid. |
| A5 **Honest scope** | Recorded request spellings only; opaque body; no native prevention/effect/reading claims. |
| A6 **Historical stability** | v1 policy and historical reds stay unchanged; v2 ports them, it does not rewrite them. |

## 2. Literal v1 facts read from `snapshot/tools/check-seat-bindings.py`

Source: `classify(tool, args, binding, depth=0)`:

```
    if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'):
        return ['SCOPE-TOOL-UNKNOWN']
    ...
    allowed_keys = {
        'read': {'i', 'path'},
        'grep': {'i', 'pattern', 'path', 'case', 'gitignore', 'skip'},
        'glob': {'i', 'path', 'hidden', 'gitignore', 'limit'},
        'write': {'i', 'path', 'content'},
    }
    unknown_keys = bool(set(args) - allowed_keys[tool])
    value = args.get('path')
    if not isinstance(value, str) or not value:
        raise ValueError('missing explicit path')
    values = value.split(';') if tool in ('grep', 'glob') else [value]
    findings = ['SCOPE-SCHEMA'] if unknown_keys else []
```

Source: `evaluate(manifest, events)` verdict encoding:

```
        code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)
        ...
                  'violations': violations,
        ...
        violations += sum(fid != 'SCOPE-SCHEMA' for fid in ids)
```

Consequences (literal, not inferred):

1. **Extra/unknown key ⇒ `SCOPE-SCHEMA`**, emitted at site `f'{name}:{index}'`, and the *entire run* is escalated: `code = 2`, status `CANNOT_EVALUATE`, `request_audit_mode = 0`. It is **not** a per-event soft note and **not** counted in `violations` (`fid != 'SCOPE-SCHEMA'` filter).
2. The path check still runs for a request that already carries an unknown key (the loop is independent of `findings`), so a request with both an unknown key and an out-of-scope path yields `SCOPE-SCHEMA` **and** the path finding — e.g. the historical selftest case `fetch-with-extra-key` expects `('SCOPE-SCHEMA', 'SCOPE-FETCH-DENIED')`.
3. **Only extra keys are detected.** Missing declared keys are not: `unknown_keys` is a set *difference*, so `write` with `{'path': ...}` only (no `content`, no `i`) produces no `SCOPE-SCHEMA`; the only missing-field error is the explicit `missing explicit path` raise.
4. **`edit` is invisible to the v1 key check.** `edit` is not in the admitted tool tuple, so `classify` returns `SCOPE-TOOL-UNKNOWN` *before* any argument validation. The recorded r22 edit key sets therefore never reach the v1 key logic at all.
5. **Forbidden tools short-circuit first.** `bash`/`eval`/`task` ⇒ `SCOPE-EXEC-DENIED`; `web_search`/`browser*` ⇒ `SCOPE-FETCH-DENIED`, both before any key or path inspection (deliberate: *"A known forbidden tool remains evidence even when its payload is missing."*).
6. **Manifest/trace top-level key sets are strict, seat-level key sets are not.**
   - `set(data) != {'schema','seats'}` and `data.get('schema') != 'tsukuroi-seat-bindings-v1'` ⇒ `ValueError('binding schema')` ⇒ `SCOPE-SCHEMA` at site `input`, exit 2, `CANNOT_EVALUATE`.
   - `set(trace) - {'schema','seats','coverage'}` non-empty ⇒ `ValueError('events schema')` ⇒ same encoding.
   - The per-seat validation is `not isinstance(seat, dict) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', seat.get('name','')) or seat['name'] in bound or seat.get('root') != LANE or seat.get('commands') != [] or seat.get('fetches') != []` plus the `read_paths`/`write_paths` checks — **there is no seat key-set equality check**, so unknown seat-level fields are accepted and silently ignored.
7. **Multi-target spelling:** only `grep`/`glob` split their `path` on `;`, and each part is checked against the binding — the `EXPANSION`/`CHECK_EACH` "each recorded step separately scoped" behaviour is realised for the *`path` key only*; a second scope-bearing field carried in a different key is never split or path-checked (it is merely an unknown key ⇒ `SCOPE-SCHEMA`).
8. **Duplicate JSON keys** are rejected globally by the `unique()` `object_pairs_hook` (`raise ValueError('duplicate JSON key')` ⇒ `SCOPE-SCHEMA`).

Historical selftest cases that already pin the non-clean behaviour (names quoted from the source, expectations are literal in `selftest()`):

```
    case('extra-argument', 'glob', {'path': src, 'pattern': '/outside/*'}, 2, 'SCOPE-SCHEMA')
    case('extra-url-key', 'read', {'path': src, 'url': 'https://example.invalid'}, 2, 'SCOPE-SCHEMA')
    case('fetch-with-extra-key', 'read', {'path': 'https://example.invalid', 'url': 'https://example.invalid'}, 2, ('SCOPE-SCHEMA', 'SCOPE-FETCH-DENIED'))
    case('parallel-malformed', 'multi_tool_use.parallel', {'tool_uses': [None]}, 2, 'SCOPE-SCHEMA')
```

`extra-argument` expects **exit 2**, i.e. the historical policy already treats "an argument key outside the declared set" as structurally non-clean and audit-invalidating. That is the canonical precedent v2 must port.

## 3. The two facts that must not be conflated (A2)

- **Absent new capability.** The v1 gate has no schema-v2 acceptance: a v2 manifest is rejected by the literal `data.get('schema') != 'tsukuroi-seat-bindings-v1'` test ⇒ `SCOPE-SCHEMA` / exit 2 / `CANNOT_EVALUATE`; and `edit` is not an admitted tool ⇒ `SCOPE-TOOL-UNKNOWN` / exit 1 / `FAIL`. `preregister.json` C2 records this exactly as a *before→target* capability metric: `{"id":"C2","axis":"operability","metric":"structured_edit_mode","before":0,"target":1,...,"scope":"New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."}`. A `before: 0` capability is a gap to be closed, **not** a v1 defect.
- **Historical policy quality.** On this axis the v1 policy is *sound and already tested*: unknown keys ⇒ `SCOPE-SCHEMA` ⇒ exit 2 ⇒ `CANNOT_EVALUATE`, with three dedicated selftest cases. There is **no** observed v1 behaviour that lets an unknown or extra scope-bearing field pass clean. So "the v1 gate had a bug about unknown keys" would be a false finding, and "v1 correctly refuses unknown keys" is the honest one.
- **The only genuine v1 gaps found are narrow and are v2 design obligations, not v1 regressions**: (i) seat-level unknown fields are ignored rather than rejected (fact 6); (ii) missing declared keys are not detected (fact 3); (iii) edit-request key sets are unexamined because `edit` short-circuits (fact 4). Each is stated below with its own finding id so it cannot be misfiled as "v1 was broken".

## 4. Independent literal fixtures and exact policy expectations

Fixtures are literal request-level spellings (stable across v1/v2), built from the *recorded* r22 key spellings in `sources/structured-edit-observations.json` — `{"path","stream_content"}` (seat `CritRuntime`, transcript `345fb766…`) and `{"i","new_string","old_string","path"}` (seat `OraclePathArtifact`, transcript `ce11e69a…`). The body is opaque throughout (`body_fields: "omitted; no report text copied"`), matching the declared v2 scope *"Body data opaque"*.

### F-A — control: exact declared key set, predeclared target with read **and** write authority

```
tool: "edit"
args: {"i": "<intent>", "old_string": "<opaque>", "new_string": "<opaque>",
       "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleV2UnknownKey.md"}
seat: read_paths ∋ target AND write_paths ∋ target
```

- Expected v2 policy outcome: **`DECLARED_EDIT` → ALLOW** ⇒ clean (exit 0, no finding). Row reason: *"Exact target is predeclared for edit and for both read and write"*.
- Expected v1 outcome (literal): `SCOPE-TOOL-UNKNOWN`, exit 1, `FAIL` — the capability-gap signature of fact 4.
- Binding requirement check: `READ_ONLY_EDIT`/`WRITE_ONLY_EDIT` remain DENY — the target must appear in **both** lists; a target in only one is not this fixture.

### F-B — extra unknown argument key (the axis under test)

```
tool: "edit"
args: {"i": "<intent>", "old_string": "<opaque>", "new_string": "<opaque>",
       "path": "<LANE>/.ufo/waves/round-23/build/OracleV2UnknownKey.md",
       "stream_content": "<opaque>"}
```

- Expected v2 policy outcome: **non-clean**. No declared row grants ALLOW to a request whose argument key set is not the declared set; the structured target is not established ⇒ closest row `OPAQUE_PATCH` → **UNKNOWN** (*"Missing structured target is not inferred from opaque patch text"*), reinforced by `UNDECLARED_EDIT` → DENY (*"No implicit edit permission from generic report ownership"*).
- Expected **encoding** (port of the historical precedent, fact 2): findings `['SCOPE-SCHEMA']` at site `<seat>:<index>`; **exit 2**; status **`CANNOT_EVALUATE`**; `request_audit_mode` `0`; the `violations` counter is **not** incremented by this finding.
- Expected **negative** (what must *not* happen): not exit 0; not exit 1 `FAIL` attributed to a path violation; not a `SCOPE-PATH-DENIED` (the path here is in scope — misattributing the cause would corrupt any path-census reconciliation); not silently ignored because the target path is legitimate.

### F-C — extra scope-bearing field (second target-shaped field)

```
tool: "edit"
args: {"i": "<intent>", "old_string": "<opaque>", "new_string": "<opaque>",
       "path": "<LANE>/.ufo/waves/round-23/build/OracleV2UnknownKey.md",
       "file": "<LANE>/.ufo/waves/round-23/build/Other.md"}
```

(and the variant where `file` holds `https://example.invalid/`)

- Expected v2 policy outcome: **non-clean**, with two independent requirements satisfied simultaneously:
  - `EXPANSION` → **CHECK_EACH** (*"Every recorded adapter read or write remains separately scoped"*): the extra field is a *separate* scope-bearing fact and must be scoped on its own — it is neither merged into the declared target nor used to widen it;
  - `EDIT_EXTERNAL` → DENY (*"Remote or internal URIs do not become filesystem edit targets"*) for the URL variant, and `EDIT_TRAVERSAL` → DENY (*"No dot-segment or alternate spelling expands the target list"*) for any traversal-spelled variant.
- Expected **encoding**: `SCOPE-SCHEMA` (structural: the key is outside the declared set) ⇒ exit 2 / `CANNOT_EVALUATE`; the URL variant must additionally never be reported as an in-scope target.
- Expected **negative**: the extra field must not be *silently dropped*. Silent drop is exactly the failure mode fact 6/7 describe, and it is the one place where an extra scope-bearing field can look "clean" — a v2 port that only checks the `path` key would reproduce it. Under the v1 precedent the extra field is *not* dropped: it is an unknown key ⇒ `SCOPE-SCHEMA`.

### F-D — missing declared structured keys (symmetry arm)

```
tool: "edit"
args: {"i": "<intent>", "path": "<LANE>/.ufo/waves/round-23/build/OracleV2UnknownKey.md"}
```

- Expected v2 policy outcome: **non-clean** — but of a *different class* than F-B/F-C. Fact 3 shows the v1 set-difference test cannot see a missing key; a naive port would let this pass as clean, which would be a **false ALLOW** under `DECLARED_EDIT` ("exact target is predeclared") and a false clean for an edit request with no structured body.
- Declared-row mapping: `OPAQUE_PATCH` → **UNKNOWN** (*"Missing structured target is not inferred from opaque patch text"*) — i.e. **not** DENY. Under A4 (cause fidelity) the UNKNOWN class must remain distinguishable from a prohibition; collapsing UNKNOWN into DENY would inflate the violation count and mislabel a malformed request as a scope escape.
- Expected **encoding** `[INFERENCE]`: `SCOPE-SCHEMA` ⇒ exit 2 / `CANNOT_EVALUATE`, mirroring the missing-`path` raise (`raise ValueError('missing explicit path')`), i.e. the v1 module already models "required structured metadata absent" as schema-invalid, not as path-denied.

### F-E — v2 manifest offered to the v1 gate (capability-gap signature)

```
manifest: {"schema": "tsukuroi-seat-bindings-v2", "seats": [...]}
events:   {"schema": "tsukuroi-seat-events-v2", "seats": [...]}
```

- Expected v1 outcome (literal): `SCOPE-SCHEMA` at site `input` ⇒ exit 2, `CANNOT_EVALUATE`, `request_audit_mode` `0`, `seats_bound` `0`.
- Interpretation: this is the *expected* pre-land reading of a not-yet-existing mode, i.e. **A2 evidence**: absent capability, unchanged historical policy. It must not be recorded as a v1 defect, and it must not be counted as a "path violation".

## 5. Findings (by severity)

**F-1 (High, v2 design obligation) — unknown seat-level binding fields are silently ignored; a declared-but-unenforced v2 edit authority would look clean.**
Evidence: `evaluate()`'s per-seat validation has no key-set equality check, while the manifest top level is strict (`set(data) != {'schema','seats'}`) and the trace top level is strict (`set(trace) - {'schema','seats','coverage'}`).
Impact: a v2 binding that declares edit authority through a new seat field (e.g. an edit-target list) would be *accepted* by the v1 validator and *ignored*; the same request would then fail only with `SCOPE-TOOL-UNKNOWN`, and a reader could wrongly infer "the seat declared no edit target" instead of "the declared target was never enforced".
Requirement: v2 must reject unknown seat keys with `SCOPE-SCHEMA` (exit 2), and must validate the edit-authority field explicitly rather than by omission. This is a *port* obligation for v2, not a fix to historical v1 policy.

**F-2 (High, v2 design obligation) — required-key absence is invisible; the unknown-key invariant is one-sided.**
Evidence: `unknown_keys = bool(set(args) - allowed_keys[tool])` — a set difference; missing `content`/`old_string`/`new_string`/`i` cannot raise a schema finding, and only `path` absence raises (`missing explicit path`).
Impact: F-D would be a false clean under a naive port; that is a false `DECLARED_EDIT`/ALLOW.
Requirement: v2 must check the declared key set in **both** directions (no extras *and* no omissions) for admitted edit/adapter requests, and keep the omission case in the UNKNOWN/`SCOPE-SCHEMA` class rather than ALLOW or DENY.

**F-3 (High, v2 design obligation) — `edit` short-circuits before key validation, so a v2 port that admits `edit` must not inherit the blind spot.**
Evidence: `if tool not in ('read','grep','glob','write','multi_tool_use.parallel','parallel'): return ['SCOPE-TOOL-UNKNOWN']` precedes the whole `allowed_keys` block.
Impact: an admitted-`edit` v2 mode that reuses this structure without adding `edit` to `allowed_keys` would classify every edit request as tool-unknown, i.e. exactly the capability gap, while *also* dropping the key-set question (F-B, F-C, F-D) — a silent false-clean for the key axis.
Requirement: `edit` must enter the key-check path with its own declared key set(s) before any path evaluation, and the resulting verdict must remain non-clean for extra keys.

**F-4 (Medium) — the recorded corpus contains two distinct edit key spellings; the v2 allowlist must be declared per spelling, not inferred.**
Evidence: `sources/structured-edit-observations.json` records `argument_keys: ["path","stream_content"]` for seat `CritRuntime` and `["i","new_string","old_string","path"]` for seat `OraclePathArtifact`.
Impact: a v2 allowlist containing only one canonical spelling would make the *other* recorded spelling a "contains an extra key" case (F-B class). That would be non-clean for the wrong reason and would misattribute a historical r22 spelling as a scope escape — precisely the relabelling that C2's scope forbids (*"legacy schema-v1 policy and historical reds unchanged"*) and that C3's calibration metric would then have to explain.
Requirement: the v2 declared key sets must cover both observed spellings explicitly, and the unknown-key rule must be a *declared allowlist per recorded adapter spelling*.

**F-5 (Medium) — the non-clean escalation is global, not per-event; a v2 port must preserve the global escalation.**
Evidence: `code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)` and `violations += sum(fid != 'SCOPE-SCHEMA' for fid in ids)`.
Impact: if v2 downgraded a schema finding to a per-event note, a run containing one unknown-key event could still return PASS/exit 0. The whole point of A1 is that unknown keys invalidate the audit result, not merely annotate it.
Requirement: preserve (a) global escalation to `CANNOT_EVALUATE`/`request_audit_mode 0`, and (b) the schema-vs-violation counter split, so that unknown keys never enter a path-violation census.

**F-6 (Low) — forbidden-tool deny precedence must survive the v2 port.**
Evidence: the `bash`/`eval`/`task` and `web_search`/`browser` returns precede argument validation, with the source comment *"A known forbidden tool remains evidence even when its payload is missing."*
Impact: a v2 mode that validates keys before the deny list would turn a `SCOPE-EXEC-DENIED` into a `SCOPE-SCHEMA` (or vice versa), changing exit codes 1↔2 for historical red rows and therefore changing historical reds — forbidden by C2's scope.
Requirement: keep deny precedence; never let a payload-bearing forbidden request be downgraded to a schema-only note.

**F-7 (Low) — unknown keys never cause a path violation to be suppressed, and vice versa.**
Evidence: the `for value in values:` path loop runs independently of `findings`.
Impact/requirement: for a request that is both key-malformed and path-out-of-scope, both facts must be reported (historical case `fetch-with-extra-key` expects exactly `('SCOPE-SCHEMA','SCOPE-FETCH-DENIED')`). Suppressing either one loses a distinct fact and corrupts per-event reconciliation.

**F-8 (Info) — no claim of runtime enforcement anywhere.** The tool audits *recorded request spellings*; the declared scope string forbids prevention, symlink/effect, reading proof and universal-trace claims. The v2 authority as declared inherits the same limit ("Body data opaque, no native enforcement/effects claim"). Any report or metric wording that implies prevention would be unsupported by the read source.

## 6. Axis ledger

| Axis | Verdict | Evidence |
|---|---|---|
| A1 non-clean invariance | **Satisfied by v1 precedent; must be ported, not invented** | `unknown_keys` → `SCOPE-SCHEMA`; `extra-argument`/`extra-url-key`/`fetch-with-extra-key` cases (exit 2) |
| A2 capability gap ≠ historical defect | **Separable and separated** | v1 literal `SCOPE-TOOL-UNKNOWN` (edit) and v1 literal `SCOPE-SCHEMA` (v2 schema) vs. preregister C2 `before:0 → target:1` |
| A3 authority exactness | **Bound** | preregister `edit_decisions` rows + `sources/edit-decision-policy.json` ids |
| A4 cause fidelity | **At risk in v2** (F-2, F-4, F-5) | `violations += sum(fid != 'SCOPE-SCHEMA' ...)`; `OPAQUE_PATCH → UNKNOWN` |
| A5 honest scope | **Held** | `SCOPE` string in source; C2 scope; preregister `limits` |
| A6 historical stability | **Port-only obligation** (F-1, F-2, F-3, F-6) | C2 scope: *"legacy schema-v1 policy and historical reds unchanged"* |

## 7. Residual risk and verification gaps

1. **No v2 implementation exists in the read scope**, so every "expected v2 outcome" for F-B/F-C/F-D is `[INFERENCE]` from the declared rows plus the v1 precedent. The v2 schema string, the v2 seat-field names and the v2 edit key-set table are **undeclared** in the files I am bound to read; they are an L1 (canonical planner) decision. I did not invent them and did not read beyond the declared paths.
2. **Fixture F-A's clean outcome (exit 0) is itself `[INFERENCE]`** for the same reason: it depends on a v2 mode and on the seat binding declaring the target in both `read_paths` and `write_paths`, which no bound file contains.
3. The recorded corpus is 4 observations over 2 seats (2 distinct edit key spellings). It is the **entire** evidence available to me for "the declared v2 allowlist shape"; no other r22 spelling (e.g. a `write`-style edit adapter, or an edit with a `body` key) is observable from the bound files, so the v2 allowlist's completeness cannot be closed from here.
4. I could not confirm whether the historical r22 reds for these spellings were already `SCOPE-SCHEMA`/`SCOPE-TOOL-UNKNOWN` — the bound files contain the v1 tool, the preregister and the r22 observations, but not the r22 verdict records. Any statement about "historical reds unchanged" is therefore a design requirement, not a verified observation.
5. `preregister.json` `sources_opened` lists S085/S086 prospectively; I verified S086's content only through `sources/structured-edit-observations.json` (the observations file). I did not open S085 (path-census source cell), which is outside this seat's declared read paths and outside this predicate.
6. The `.ufo/waves/round-23/build/` directory listing was not enumerated (extra filesystem search is forbidden by the seat scope); the report path was created directly from the seat-declared write path.

## 8. Bottom line

Unknown argument keys and extra scope-bearing fields are already **non-clean** in the historical v1 policy — literally `SCOPE-SCHEMA` with global escalation to exit 2 / `CANNOT_EVALUATE` / `request_audit_mode 0`, and with three dedicated selftest cases pinning it. The absence of a v2 structured-edit authority is an **absent new capability** (preregister C2, `structured_edit_mode` `before: 0 → target: 1`), **not** a defect in that historical policy. The design obligations a v2 port must satisfy, each traceable to a literal source line above, are: reject unknown seat-level binding fields (F-1), check the declared key set in both directions (F-2), route admitted `edit` requests through a key check instead of the `SCOPE-TOOL-UNKNOWN` short-circuit (F-3), declare the allowlist per recorded adapter spelling — there are two (F-4), preserve the global escalation and the schema-vs-violation counter split (F-5), keep forbidden-tool deny precedence (F-6), and keep the two facts orthogonal (F-7). No native enforcement, effect, or reading proof is claimed.

Reviewed-SHA256: 8fccb655fe94e49d4189dc7e2311e1e29cf50ac6b59f4ff280f49676316a04b6
Predicate: r23-oraclev2unknownkey
Scope: executed=none
