# FxC2OracleLegacy — round 23, attempt 1, FALSIFY wave

Seat: `TsukuroiR23-2.FxC2OracleLegacy-2` (leaf reviewer). Binding lane: `leaf member — no subagent dispatch`.
Target under review: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py` (landed copy of the r23 candidate; declared SHA256 supplied, not independently computed).
Scope of this seat: post-hoc audit of the landed C2 v2 edit-audit authority, reached from the v1 legacy branch.

Tooling policy: this seat's NO-EXEC / NO-FETCH scope forbids installs, execution, hashing and delegation. No package was installed, updated or removed; no host/service/boot action was taken. Every statement below is derived by reading the declared landed source and the declared v2 production manifest, or is explicitly marked `[INFERENCE]`.

Nothing in this report claims runtime prevention or enforcement. The audited tool's own declared scope is: *"Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."* (line 18). The audit is post-hoc classification of recorded request spellings against a manifest; it neither prevents nor proves effects.

---

## 1. Axes named (godspeed)

| Axis | What it means here | Measure used in this report |
|---|---|---|
| A1 **Correctness of the oracle** | Does the hand-derived audit outcome match the landed code exactly (exit code, finding IDs, mode flag)? | Step-by-step branch derivation against line anchors |
| A2 **Legacy continuity** | Does the schema-v1 path keep its historical policy, or did the v2 addition leak into it? | Enumeration of every branch that can flip edit authority |
| A3 **Control completeness** | Is every branch that can change the answer pinned by a landed selftest case? | Selftest case census vs. branch census |
| A4 **Manifest integrity** | Does the landed production v2 manifest satisfy the authority rule the tool itself defines? | Read-only JSON queries over `build/bindings.json` |
| A5 **Calibration honesty** | Do the emitted metrics/findings mean what the claim says they mean? | Semantic reading of `structured_edit_mode`, finding IDs, exit codes |

Cheap parallel moves executed: full-source read (2 ranged reads), line-anchored grep, preregister read, bindings read + 5 independent JSON queries — all in batches, no serialization.

---

## 2. Attack A (primary): a schema-v1 manifest that carries an `edit_paths` field

### 2.1 Derivation from landed source only

Fixture premise (the shape the landed selftest itself uses for the v1 branch): a manifest whose top-level `schema` is `"tsukuroi-seat-bindings-v1"`, whose `seats` is a non-empty list of seats `{name, root, read_paths, write_paths, commands: [], fetches: []}` **plus an extra `edit_paths` list on the seat**, and whose seats otherwise satisfy the loader's preconditions (`root == LANE`, `commands == []`, `fetches == []`, non-empty duplicate-free lane-local path lists).

Walk-through of `evaluate()`:

1. `manifest is None`? No → the `SCOPE-BINDINGS-MISSING` early return (line 139) is not taken.
2. `data = json.loads(manifest, object_pairs_hook=unique)`; `trace = json.loads(events, ...)` (lines 142–143). No duplicate JSON key → no `ValueError`.
3. **`v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'`** (line 144). The manifest declares v1 → **`v2 = False`**. This single assignment is the only thing that can enable structured-edit semantics anywhere in the file.
4. Top-level shape gate (line 145): `set(data) != {'schema','seats'}` — the manifest's *top level* holds exactly `schema` and `seats` → passes. `data.get('schema') in ('tsukuroi-seat-bindings-v1','tsukuroi-seat-bindings-v2')` → passes. `seats` is a non-empty list → passes.
5. Per-seat identity gate (line 149) and `read_paths`/`write_paths` gate (lines 152–154): satisfied by the premise.
6. **The v2 edit-authority block is `if v2:`-guarded (lines 155–161).** With `v2 = False` the block is *never entered*. Consequences, all three load-bearing:
   - the seat's `edit_paths` list is **not read, not validated, not compared** to `read_paths`/`write_paths`;
   - the exact-seat-key-set requirement `set(seat) != {'name','root','read_paths','write_paths','edit_paths','commands','fetches'}` (line 158) is **not applied**, so the extra `edit_paths` key is tolerated rather than rejected;
   - no `ValueError('v2 edit authority')` can be raised for a v1 manifest.
7. Trace gate (lines 163–167) and per-seat trace identity gate (lines 169–173): satisfied by a matching `tsukuroi-seat-events-v1` trace.
8. Event classification: `ids = classify(event.get('tool'), event.get('args'), binding, allow_structured_edit=v2)` (line 186) — **`allow_structured_edit=False`** for a v1 manifest, by construction of step 3.
9. Inside `classify()`: `tool == 'edit' and allow_structured_edit` is False (line 76), so `classify_edit()` is never reached; `edit` is not in the permitted tuple `('read','grep','glob','write','multi_tool_use.parallel','parallel')` (line 78) → **`return ['SCOPE-TOOL-UNKNOWN']`** (line 79). Note this happens *before* any path check, so the edit target's spelling is irrelevant.
10. Exit-code rule (line 194): `code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' ...) else (1 if findings else 0)`. Findings = `[{'id':'SCOPE-TOOL-UNKNOWN','site':'<seat>:<index>'}]`; no `SCOPE-SCHEMA`, no incomplete seat → **`code = 1`**.
11. Mode flag: `if v2: result['structured_edit_mode'] = int(code != 2)` (lines 205–206). `v2` is False → **`structured_edit_mode` is absent from the result object** — not `0`, not `1`. The key does not exist.

### 2.2 Derived outcome (seat-level reading — the reading the landed data model supports)

For a schema-v1 manifest whose seat carries `edit_paths`, with one recorded `edit` event:

| Field | Derived value |
|---|---|
| exit code | **1** |
| finding IDs | **`SCOPE-TOOL-UNKNOWN`** (exactly one; site `"<seat-name>:<event-index>"`, e.g. `"A:0"`) |
| `structured_edit_mode` | **absent — the key is not present in the result JSON** |
| `status` | `FAIL` |
| `request_audit_mode` | `1` |
| `violations` | `1` |
| `seats_bound` / `requests_total` | number of bound seats / number of recorded events |
| `incomplete_seats` / `missing_seats` | `0` / `0` (assuming a complete, matching trace) |

Important corollary of step 6: under v1 the `edit_paths` field is **entirely inert**. The same request against the *identical* seat payload under schema v2 yields `SCOPE-EDIT-DENIED` for an undeclared target and exit `1`; under v1 it yields `SCOPE-TOOL-UNKNOWN` and exit `1`. The exit code is the same, the finding ID differs — see Finding 4.

### 2.3 Second reading of the same words (top-level `edit_paths`)

"A schema-v1 manifest that carries an `edit_paths` field" can also be read as an **extra top-level key** on the manifest object. Hand-derived:

| Field | Derived value |
|---|---|
| exit code | **2** |
| finding IDs | **`SCOPE-SCHEMA`** (site `"input"`) |
| `structured_edit_mode` | **absent** (`v2` is False; and the raise happens before any seat is bound) |
| `status` | `CANNOT_EVALUATE` |
| `request_audit_mode` | `0` |
| `seats_bound` / `requests_total` / `violations` | `0` / `0` / `0` |

Reason: line 145 (`set(data) != {'schema','seats'}`) raises `ValueError('binding schema')` → caught at line 195 → `add('SCOPE-SCHEMA','input')`, `code = 2`, and `bound = locals().get('bound', {})` resolves to `{}` because `bound = {}` (line 147) is only reached *after* the gate. `v2` was already computed False at line 144, so no mode key is emitted.

Both readings are reported because the task wording is ambiguous and the two outcomes are materially different (exit 1 + `SCOPE-TOOL-UNKNOWN` vs. exit 2 + `SCOPE-SCHEMA`).

---

## 3. Does the landed selftest contain an equivalent control?

### 3.1 Seat-level reading — **YES**, an equivalent control exists

Landed selftest, lines 333–335:

```
v1_with_edit_field = copy.deepcopy(v2); v1_with_edit_field['schema'] = 'tsukuroi-seat-bindings-v1'
v2case('v1-extra-edit-field-no-grant', 'edit', {'path': target, 'stream_content': None}, 1, 'SCOPE-TOOL-UNKNOWN', manifest=v1_with_edit_field, mode=-1)
v2case('v1-edit-continuity', 'edit', {'path': report, 'stream_content': None}, 1, 'SCOPE-TOOL-UNKNOWN', manifest=binding, mode=-1)
```

The first case is exactly the attacked input: the v2 fixture with its top-level `schema` string flipped to v1, so the seat **still carries `edit_paths`** while the manifest is v1; the recorded event edits `target`, which *is* a declared edit target of that seat (the strongest possible case: a correctly-declared v1 edit still gets no grant). Its asserted expectations are exactly the derived values of §2.2: exit `1`, `SCOPE-TOOL-UNKNOWN` present, and `mode=-1` meaning **`'structured_edit_mode' not in result`** (line 348: `mode_ok = ('structured_edit_mode' not in result) if mode == -1 else ...`).

The second case covers the v1 seat *without* `edit_paths` and asserts the same exit/ID/mode-absence, which pins "the v2 addition did not change legacy v1 policy".

**Conclusion: the primary (seat-level) reading is covered by an equivalent landed control; no new fixture is required for it.** My hand-derivation and the landed assertion agree on all three fields (exit 1, `SCOPE-TOOL-UNKNOWN`, mode absent).

### 3.2 Top-level reading — **NO equivalent control exists**; literal fixture supplied

Census of every landed selftest manifest that is malformed at the *manifest* level (as opposed to the seat level):

| Landed case | Mechanism that actually fires | Does it exercise the top-level key-set gate `set(data) != {'schema','seats'}` (line 145)? |
|---|---|---|
| `duplicate-json-key` (`'{"seats":[],"seats":[]}'`) | `unique()` raises `ValueError('duplicate JSON key')` in the parser (line 142) | No — fails earlier, in parsing |
| `duplicate-valid-json` (`'{"schema":"bad",' + json.dumps(binding)[1:]`) | the injected string contains the key `"schema"` **twice** → `unique()` raises in the parser (line 142) | No — fails earlier, in parsing. (The case name suggests it targets the bad-schema path; it actually exercises duplicate-key rejection.) |
| `v2-schema-typo` (`dict(v2, schema='tsukuroi-seat-bindings-v3')`) | key set is exactly `{schema, seats}` → passes the key-set gate; fails the schema-membership clause of line 145 | No — exercises the *membership* clause, not the *key-set* clause |
| `v2-row-marker`, `v2-edit-paths-missing`, `v2-edit-paths-duplicate`, `v2-edit-not-readable`, `v2-edit-not-writable` | seat-level mutations | No — all seat-level (line 158) |
| `foreign-root`, `nonempty-commands`, `duplicate-bound-name`, `duplicate-bound-path`, `nonempty-fetch-allowlist` | seat-level mutations | No |

**No landed case adds an extra top-level key to a schema-valid manifest.** The branch `set(data) != {'schema','seats'}` is therefore *unexercised*: deleting it from the tool would leave the entire selftest green while the tool would silently begin accepting manifests with extra top-level keys.

Literal fixture (to be added to the landed `selftest()`, in the v2_cases list so that mode-absence is asserted too):

```python
v2case('v1-manifest-toplevel-edit-paths', 'read', {'path': src}, 2, 'SCOPE-SCHEMA',
       manifest={'schema': 'tsukuroi-seat-bindings-v1',
                 'seats': copy.deepcopy(binding['seats']),
                 'edit_paths': []},
       mode=-1)
```

Expected result under the landed code: exit `2`; findings `[{'id': 'SCOPE-SCHEMA', 'site': 'input'}]`; `structured_edit_mode` **absent**; `status` `CANNOT_EVALUATE`; `request_audit_mode` `0`; `seats_bound` `0`; `requests_total` `0`; `violations` `0`.

Equivalent string form (JSON) if the manifest is passed as text rather than as a dict:

```python
'{"schema":"tsukuroi-seat-bindings-v1","seats":' + json.dumps(binding['seats']) + ',"edit_paths":[]}'
```

---

## 4. Falsification attempts against C2 (bounded search)

Claim attacked: **C2** — "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged." Metric: `structured_edit_mode`, before `0`, target `1`.

| # | Falsifier attempted | Bounded search / evidence | Outcome |
|---|---|---|---|
| F1 | Can a v1 manifest's seat-level `edit_paths` grant edit authority? | Only `allow_structured_edit` can reach `classify_edit` (line 76). It is set at exactly one call site, line 186, from `v2`, which is set at exactly one place, line 144, from the **top-level** `schema` string. A seat field cannot reach it. | **Refuted.** No grant. (This is the primary attack and it failed to falsify.) |
| F2 | Can a v1 manifest forge v2 by carrying `edit_paths` plus a `schema` variant? | `data.get('schema') == 'tsukuroi-seat-bindings-v2'` is an exact string compare; any other spelling (e.g. trailing space, `-v2`) falls through to line 145 and raises → `SCOPE-SCHEMA`, exit 2. A manifest that declares v2 *is* a v2 manifest and must satisfy line 158's exact 7-key seat set. | **Refuted.** Fail-closed. |
| F3 | Can a v1 manifest smuggle authority through a row/trace marker (`allow_structured_edit` in a seat or in an event)? | `allow_structured_edit` is never read from a row or an event; the docstring (lines 70–74) states the same. Landed controls `v2-row-marker` (line 336) and `v2-events-trace-marker` (line 337) pin it. | **Refuted.** |
| F4 | Does the v1 branch *validate* `edit_paths` at all? | No: lines 155–161 are `if v2:`-guarded. A v1 seat may carry `edit_paths` containing duplicates, non-local absolute paths, `skill://godspeed`, or paths outside `read_paths`/`write_paths`, and the manifest still loads cleanly (exit 0 if no violations). Under v2 each of those is `SCOPE-SCHEMA`, exit 2. | **Partial hit — Finding 2** (asymmetric validation; no false grant, but no signal either). |
| F5 | Does the landed production v2 manifest satisfy the rule the tool itself defines? | Read-only JSON queries over `.ufo/waves/round-23/build/bindings.json` (declared v2, 64 seats): `edit_paths ⊄ (read_paths ∪ write_paths)` → `[]` (no violations); duplicate `edit_paths` → `[]`; duplicate `read_paths`/`write_paths` → `[]`; seat key sets → exactly one distinct set, `commands,edit_paths,fetches,name,read_paths,root,write_paths`; seat names 64 total / 64 unique; non-LANE roots → `[]`; non-empty `commands`/`fetches` → `[]`; seats with empty `edit_paths` → `[]`; `read_paths` entries outside the lane → `[]` (only `skill://godspeed`, which line 153 explicitly permits for `read_paths`). | **Refuted.** The production manifest passes every loader precondition that is checkable from my read scope. |
| F6 | Can the `edit_paths` field change a **write** verdict under v1? | `classify()` checks `binding['write_paths']` for the `write` tool (line 113) independently of `edit_paths`. | **Refuted.** No write is granted by an inert field. |
| F7 | Can a `write`/`edit` spelling variant (trailing `/`, `./`, `//`, `:raw`, uppercased, relative) reach an edit target under v2? | `classify_edit` (lines 119–131) compares `value not in binding['edit_paths']` by **exact string equality** after a URL-shape rejection; no normalisation exists. Landed controls cover 8 spellings (lines 308–310). | **Refuted.** |
| F8 | Does the mode flag mean "the v2 structured-edit audit ran", or "the audit passed"? | `result['structured_edit_mode'] = int(code != 2)` (line 206) → it is `1` whenever the audit **executed** under v2 semantics, *including* when the audit FAILs with violations (code 1) — i.e. it is a mode flag, not a pass flag. | **Calibration note — Finding 5.** Consistent with the claim's metric name, but a reader must not read `structured_edit_mode: 1` as "no violations". |
| F9 | Can a legitimate recorded structured edit be misclassified as malformed and degrade the whole run to exit 2? | `classify_edit` accepts only key sets `{'path','stream_content'}` or `{'path','old_string','new_string'}`, optionally plus `'i'` (lines 116, 121). The harness `edit` tool also accepts `replace_all`; a recorded request carrying `replace_all` is **not** in `EDIT_SHAPES` → `ValueError` → `SCOPE-SCHEMA` → `code = 2` → `structured_edit_mode = 0`, i.e. the C2 metric would read **0**. | **Open risk — Finding 3** (conditional on the recorded event spellings, which are outside my read scope). |
| F10 | Can a seat-set or trace-set mismatch between the production manifest and the wave's events degrade the run? | A bound seat absent from the trace → `SCOPE-TRACE-MISSING` → `incomplete` → code 2 → `structured_edit_mode = 0`; a trace seat absent from the manifest → `ValueError` → `SCOPE-SCHEMA`, code 2. The production manifest binds 64 seats; the matching events file is outside my read scope. | **Verification gap** (not a code defect). |

**Bounded-search summary:** no falsifier for C2's core assertion was found. The v1 branch is inert with respect to edit authority, and the production v2 manifest satisfies the tool's own authority rule. The three residual items below are calibration/coverage risks, not false grants.

---

## 5. Findings by severity

### Finding 1 — MEDIUM — The manifest top-level key-set gate has no landed selftest control
- **Claim attacked:** C2 (audit authority) / A3 control completeness.
- **Evidence:** `candidate/tools/check-seat-bindings.py:145` — `set(data) != {'schema','seats'}` raises `ValueError('binding schema')`. Selftest census (§3.2) shows every malformed-manifest fixture fails earlier in the parser (`unique()` duplicate-key raise at line 142) or is seat-level; no case adds a top-level key to a schema-valid manifest.
- **Concrete falsifier:** remove/relax the `set(data) != {'schema','seats'}` clause and the entire landed selftest still passes, while the tool would begin accepting manifests carrying arbitrary extra top-level keys (including a top-level `edit_paths`, the exact object of this attack's second reading).
- **Smallest in-scope remedy:** add the single literal fixture given in §3.2 (`v1-manifest-toplevel-edit-paths`) to `selftest()`. One case, no production behavior change, no change to any historical red.

### Finding 2 — LOW/MEDIUM — Under schema v1, `edit_paths` is accepted but neither validated nor reported
- **Claim attacked:** C2 ("legacy schema-v1 policy unchanged") and A5 calibration.
- **Evidence:** lines 155–161 are `if v2:`-guarded, so a v1 seat's `edit_paths` is never validated (unlike v2, where a non-local path, a duplicate, a path outside `read_paths`/`write_paths`, or a missing key each force `SCOPE-SCHEMA`, exit 2). A v1 manifest declaring edit authority and recording **zero** edit events audits as **exit 0 / `PASS` / `findings: []`**, with no indication anywhere in the result that an edit-authority declaration was present and ungranted.
- **Concrete falsifier:** v1 manifest, seat with `edit_paths: ['/outside/lane/x.md', 'skill://godspeed', dup, dup]`, empty event list → exit 0, `PASS`, no findings. The declaration is silently swallowed.
- **Smallest in-scope remedy:** **do not** add a new finding id — that would change the legacy v1 exit-code semantics and break "historical reds unchanged". Instead add one non-scoring, informational field in the `v2 == False` case, e.g. `result['ignored_edit_declarations'] = <count of seats carrying edit_paths>`, so a reader can distinguish "plain legacy v1" from "v1 that declared edit authority". This changes no finding id, no exit code and no historical verdict.

### Finding 3 — LOW (conditional, unverified in my scope) — The structured-edit key-shape whitelist omits `replace_all`
- **Claim attacked:** C2 (operability of the v2 audit) — a single event can force the whole manifest to `CANNOT_EVALUATE` and the C2 metric to `0`.
- **Evidence:** `EDIT_SHAPES = ({'path','stream_content'}, {'path','old_string','new_string'})` (line 116) and the check `set(args) - {'i'} not in EDIT_SHAPES` (line 121). The harness `edit` tool's documented parameters include `replace_all`; a recorded request `{'path': ..., 'old_string': ..., 'new_string': ..., 'replace_all': true}` is not in `EDIT_SHAPES` → `ValueError` → caught at lines 187–188 → `SCOPE-SCHEMA` → `code = 2` (line 194) → `structured_edit_mode = int(code != 2) = 0` (line 206).
- **Concrete falsifier:** one recorded edit event whose args carry `replace_all` (or any key outside the whitelist) collapses the entire audit to exit 2 and the C2 metric to 0, regardless of everything else being clean.
- **Smallest in-scope remedy:** extend `EDIT_SHAPES` to `({'path','stream_content'}, {'path','old_string','new_string'}, {'path','old_string','new_string','replace_all'})` — i.e. enumerate the *observed* key shapes rather than a closed two-element set, and add one selftest case pinning the accepted `replace_all` shape. `[INFERENCE]` on intent: the tool's own docstring says "finite observed key shapes", and `S086` is declared as the source of "observed structured edit request keys"; if `S086` does not contain `replace_all`, then the two-element set is exactly right and the risk is theoretical.
- **Verification gap:** the wave's recorded events file is not in this seat's declared read paths, so I could not confirm whether any recorded edit carries `replace_all`.

### Finding 4 — LOW — The same recorded request changes finding ID across schema versions
- **Claim attacked:** C2's "historical reds unchanged" (A5 calibration).
- **Evidence:** under v1 an `edit` event yields `SCOPE-TOOL-UNKNOWN` (line 79); under v2 the same event yields `SCOPE-EDIT-DENIED` (line 129). Exit code is `1` in both cases, so pass/fail is stable, but the finding ID is not.
- **Concrete falsifier:** re-auditing a legacy r22 event record against the r23 **v2** manifest renames its finding from `SCOPE-TOOL-UNKNOWN` to `SCOPE-EDIT-DENIED`. The C2 scope's "historical reds unchanged" holds only when the manifest schema is unchanged; it does **not** hold under same-identity rerouting of old events onto the new v2 manifest.
- **Smallest in-scope remedy:** prose-level, inside the C2 scope statement — state explicitly that finding-ID stability is bound to the manifest schema version, and that archived reds must be re-audited against the archived (v1) manifest. No code change; adding both ids to the v2 finding set would change the v2 output contract.

### Finding 5 — LOW — `structured_edit_mode` is a mode flag, not a pass flag
- **Claim attacked:** C2 metric semantics (A5).
- **Evidence:** `result['structured_edit_mode'] = int(code != 2)` (line 206) — the value is `1` for a **FAILED** v2 audit (exit 1 with violations) as well as for a clean one (exit 0), and `0` only when the audit could not evaluate (exit 2). The claim's metric name (`structured_edit_mode`) is consistent with this reading, but a reader can easily take `1` as "clean".
- **Concrete falsifier:** a v2 manifest with a legitimate edit target and a recorded `edit` event carrying an unlisted key yields exit 2 → `structured_edit_mode = 0`; a v2 manifest with a recorded `edit` event targeting a non-declared path yields exit 1 → `structured_edit_mode = 1` **with** a `SCOPE-EDIT-DENIED` finding. Both are "mode on"; only the second is a red.
- **Smallest in-scope remedy:** none in code; the claim prose already names the metric `structured_edit_mode`. If a stricter signal is wanted later, add a separate non-metric field such as `structured_edit_violations` rather than re-purposing the mode flag.

---

## 6. Residual risk and verification gaps

1. **Events coverage unverified.** The wave's `events.json` is outside this seat's declared read paths. Three of the outcomes above (exit 0/1/2 for the *production* run, `structured_edit_mode` = 1 vs 0, and Finding 3's trigger) depend on it. A seat whose events are missing from the trace yields `SCOPE-TRACE-MISSING` → exit 2 → C2 metric 0; a trace seat absent from the 64-seat production manifest yields `SCOPE-SCHEMA` → exit 2.
2. **`_revision.py` not read.** `ROOT = Path(__file__).resolve().parents[1]` and `git_read()` use `_revision.bind` / `_revision.clean_env`; that module is not in my declared read paths, so I could not verify the revision-binding idempotence ("same-identity rerouting": that the same `--revision` yields the same manifest/events bytes) or the clean-environment guarantees.
3. **One canonical runtime not verifiable in my scope.** I confirmed only that the landed candidate file is internally consistent; whether the `snapshot/tools/` copy and the `worktrees/ExecEditAudit/draft/` copy are byte-identical to the candidate could not be checked (those paths are not in my read scope). The production manifest binds the ExecEditAudit seat to the worktree draft copy (`build/bindings.json` seat `ExecEditAudit`), while the r23 C2 command in `preregister.json` names `tools/check-seat-bindings.py` — the same-identity question between these two artifacts is therefore **open**, not answered.
4. **Production manifest verified for shape, not for behaviour.** F5 confirms the 64-seat v2 manifest satisfies every loader precondition checkable read-only; it does not confirm that any *recorded* edit request in the wave is actually authorized by its seat's `edit_paths`.
5. **No enforcement claim.** Everything above concerns post-hoc classification of recorded request spellings. Nothing here demonstrates that a seat was prevented from performing an edit, nor that the recorded trace is complete.

---

## 7. Answer to the assigned question, in one place

- **Attacked claim:** C2 (v2 edit audit authority), specifically its legacy-continuity half; secondary A3 (control completeness).
- **Exact derived outcome for a schema-v1 manifest whose seat carries `edit_paths` (seat-level reading):** exit code **1**; finding id **`SCOPE-TOOL-UNKNOWN`** (site `"<seat>:<index>"`); **`structured_edit_mode` absent from the result** (key not present — not `0`); `status` `FAIL`; `request_audit_mode` `1`; `violations` `1`. The `edit_paths` field is inert under v1: it is neither validated nor reported, and it grants nothing.
- **Alternative reading (extra top-level `edit_paths` on the manifest):** exit code **2**; finding id **`SCOPE-SCHEMA`** (site `"input"`); **`structured_edit_mode` absent**; `status` `CANNOT_EVALUATE`; `request_audit_mode` `0`; `seats_bound` `0`.
- **Landed selftest equivalent control:** **present** for the seat-level reading (`v1-extra-edit-field-no-grant`, lines 333–334, asserting exit 1 + `SCOPE-TOOL-UNKNOWN` + mode absence; `v1-edit-continuity`, line 335). **Absent** for the top-level reading → literal fixture supplied in §3.2.
- **Falsifier found:** yes, one coverage-level falsifier (Finding 1: the top-level manifest key-set gate is unexercised; deleting it keeps the selftest green) and one operational falsifier path (Finding 3: an unlisted edit key such as `replace_all` forces exit 2 and C2 metric 0, conditional on the recorded event spellings). No falsifier for C2's core "legacy v1 grants nothing" assertion.
- **Smallest in-scope remedy:** add the single selftest fixture in §3.2 (Finding 1); add one non-scoring `ignored_edit_declarations` field for v1 (Finding 2); enumerate observed edit key shapes in `EDIT_SHAPES` (Finding 3); two prose-level clarifications for Findings 4 and 5. No production behavior change beyond the enumerating whitelist, and no change to any historical red.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oraclelegacy
Scope: executed=none
