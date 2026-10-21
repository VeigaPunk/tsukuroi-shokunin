# FxC2OracleStream — falsification of C2 v2 edit audit authority (stream_content shape)

Seat: FxC2OracleStream (falsify wave, round 23, attempt 1)
Target under review: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py` (declared SHA256 supplied by the assignment; **not** independently computed, hashed, listed or executed — this seat is NO-EXEC/NO-FETCH).
Method: hand-derivation from the landed source text only (read-only), plus a bounded enumeration over the landed `build/bindings.json` v2 manifest. No command was run, no test executed, no sibling or production file touched.

Lane bounds: leaf member — no subagent dispatch.

---

## 1. Attacked claim

**C2 — "operability / structured_edit_mode, before 0 → target 1"** (preregister `.ufo/waves/round-23/preregister.json:33-43`):
> "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."

Attacked sub-claim (this seat's slice): *an `edit` request carrying `path` + `stream_content` aimed at the exact declared report of a schema-v2 seat is classified as an authorized (non-violating) structured edit*, i.e. it must produce **exit code 0, no finding IDs, `structured_edit_mode = 1`**.

C1 (eight edit-contract decisions) and C3 (path-census ledger) are owned by other seats; only the C2 v2 authority path in `check-seat-bindings.py` is in scope here.

## 2. Hand-derivation of the target scenario (from landed source only)

Scenario A — "exact declared report", stream shape:

* manifest `schema = "tsukuroi-seat-bindings-v2"`, one seat whose `edit_paths` contains the exact declared report string `R` (production shape: `R` is also in `read_paths` and `write_paths`);
* trace: seat present, `complete = true`, exactly one event `{"tool": "edit", "args": {"path": R, "stream_content": <any body>}}`.

Derivation, step by step, with source anchors in the candidate file:

1. `evaluate()` sets `v2 = data.get('schema') == 'tsukuroi-seat-bindings-v2'` (line 144). Manifest shape check passes (lines 145-146).
2. Per-seat validation: identity/root/allowlist check (line 148-151), path lists non-empty, local, duplicate-free (lines 152-154) — `R` is `local()` (no control chars, no `*?[];:`), and `skill://godspeed` is only tolerated in `read_paths` (line 153).
3. **v2 authority gate** (lines 155-161): the seat key set must be exactly `{name, root, read_paths, write_paths, edit_paths, commands, fetches}`; `edit_paths` must be a list, duplicate-free, and every element must satisfy `local(p) and p in read_paths and p in write_paths`. `R` satisfies this by construction, so the manifest validates and `v2` stays `True`.
4. Trace validation (lines 165-178): seat name known, unique, `complete` is a bool, `events` a list.
5. Event classification (line 186): `classify('edit', args, binding, allow_structured_edit=v2)` → `allow_structured_edit=True` is threaded **only** from the validated top-level v2 schema (docstring lines 62-66; the row-marker and event-marker counter-cases are covered by `v2-row-marker` / `v2-events-trace-marker` at lines 331 and 337).
6. `classify()` (lines 61-79): `edit` is not `bash/eval/task` (no `SCOPE-EXEC-DENIED`), not `web_search/browser` (no `SCOPE-FETCH-DENIED`); the `tool == 'edit' and allow_structured_edit` branch (line 76-77) routes to `classify_edit` **before** the unknown-tool whitelist (so `edit` is not reported as `SCOPE-TOOL-UNKNOWN` under v2).
7. `classify_edit()` (lines 119-130):
   * `set(args) - {'i'} == {'path','stream_content'}` ∈ `EDIT_SHAPES` (line 116) → the shape is accepted, `i` being the only tolerated extra key;
   * `value = args['path']` is a non-empty `str` (line 124-125);
   * `value` matches neither `(?i)^https?://` nor `^[^/:\s]+:[0-9]+/` (line 126-127) → no `SCOPE-FETCH-DENIED`;
   * `value in binding['edit_paths']` → `R` is an exact member → **returns `[]`** (line 128-130). The body (`stream_content`) is never inspected — body opacity as claimed.
8. Back in `evaluate()`: `ids == []` → no finding is appended (lines 189-192); `violations` stays 0, `incomplete` stays 0, and no `SCOPE-SCHEMA` exists.
9. Verdict line 194: `code = 2 if incomplete or any(SCOPE-SCHEMA) else (1 if findings else 0)` → **`code = 0`**.
10. Result assembly (lines 199-206): `status = 'PASS'`, `request_audit_mode = int(code != 2) = 1`, `violations = 0`, `requests_total = 1`, `incomplete_seats = 0`, `missing_seats = 0`, `findings = []`; and since `v2` is true, **`structured_edit_mode = int(code != 2) = 1`** (lines 205-206).

**Derived answer for scenario A:**

| quantity | value |
|---|---|
| exit code (process, `sys.exit(main())`) | **0** |
| finding IDs | **none** (`findings == []`; no `SCOPE-*` entry, no `site` string) |
| `structured_edit_mode` | **1** |
| `request_audit_mode` | 1 |
| `status` | `PASS` |
| body sensitivity | none — `stream_content` value/type is never read |

Derived answer for the two neighbouring shapes (same derivation, different branch):

* **Scenario B — declared report in `write_paths`/`read_paths` but *not* in `edit_paths`** (a v2 seat with no explicit edit grant for that report): line 128 fires → `['SCOPE-EDIT-DENIED']` at site `<seat>:0` → `violations = 1` → line 194 → **exit code 1**, `status = 'FAIL'`, finding ID **`SCOPE-EDIT-DENIED`**, `structured_edit_mode = 1` (code != 2). This is the `UNDECLARED_EDIT → DENY` decision encoded.
* **Scenario C — report path spelled differently** (trailing `/`, `./`, `../`, `//`, `:raw`, relative, upper-cased, `skill://…`, `xd://…`): none of those strings are members of `edit_paths`, so each yields `SCOPE-EDIT-DENIED` (**exit 1**), not a path-normalization grant. URL-shaped targets are caught earlier at line 126-127 → `SCOPE-FETCH-DENIED` (**exit 1**).

No path exists in the landed code by which a `path`+`stream_content` request aimed at the exact declared report of a valid v2 seat produces a non-zero exit or any finding ID. **The primary attacked sub-claim survives.**

## 3. Does the landed selftest contain an equivalent control?

**Yes.** The landed selftest contains a control that is behaviourally equivalent to scenario A, and it is *stronger* than my derivation alone because the harness additionally asserts emptiness of the finding list and the mode value:

* `check-seat-bindings.py:301` — `v2case('v2-stream-edit', 'edit', {'path': target, 'stream_content': None}, 0)` where `target = LANE + '/drafts/A.md'` (line 295) is simultaneously in the v2 fixture's `read_paths`, `write_paths` **and** `edit_paths` (lines 296-297) — i.e. exactly the production relation of a declared report in a v2 seat. Expected exit `0`, no finding ID required.
* `check-seat-bindings.py:350` — the v2 observation pass predicate is `code == expected and all(required in ids) and (expected != 0 or not ids) and mode_ok`. For `expected == 0` this forces `ids == []` (no finding of *any* ID, so not just "the required one is present"), and `mode_ok` (line 348) forces `result['structured_edit_mode'] == int(code != 2) == 1`.
* `check-seat-bindings.py:303` (`v2-qualified-edit`, `functions.edit`) and `:315` (`v2-nested-edit`, inside `multi_tool_use.parallel`) cover the qualified and nested spellings of the same shape.
* The deny side of the same family is covered too: `:304` (`v2-read-only-target`), `:305` (`v2-write-only-target`), `:306` (`v2-undeclared-target`), `:332` (`v2-empty-edit-paths` — the manifest keeps `target` in `read_paths ∩ write_paths` while `edit_paths` is emptied, exactly scenario B).

Therefore **no literal fixture is needed for the primary scenario**: the landed selftest already pins exit 0, empty findings and `structured_edit_mode == 1` for `path` + `stream_content` on an exact declared target.

## 4. Bounded search performed (and its limit)

Bounded enumeration, from source and from the landed `build/bindings.json` only:

1. Every branch reachable from an `edit` request under `allow_structured_edit=True` was enumerated by hand: shape acceptance (line 121), missing/empty path (124-125), URL/scheme denial (126-127), membership denial (128-129), success (130). No branch produces a finding ID for an exact member of `edit_paths`.
2. Every route that could *bypass* `classify_edit` was checked: `bash/eval/task` → `SCOPE-EXEC-DENIED`; `web_search/browser*` → `SCOPE-FETCH-DENIED`; `multi_tool_use.parallel` children recurse into `classify` with `allow_structured_edit` preserved (line 91); depth is capped at 8 (line 67); the v2 flag can only come from the validated top-level schema (lines 144, 186) — a row-level `allow_structured_edit` key makes the manifest fail the exact key-set check (line 158 → `SCOPE-SCHEMA`), and an event-level marker makes the key set fail the shape check (line 121 → `SCOPE-SCHEMA`).
3. The landed v2 manifest `.ufo/waves/round-23/build/bindings.json` was read seat-by-seat (all 41 seats) for the v2 authority invariant at lines 155-161: every seat carries the exact 7-key set, `root == LANE`, `commands == []`, `fetches == []`; every `edit_paths` element is byte-identical to a corresponding `write_paths` element and is present in `read_paths` (verified for all seats, including the three multi-path seats `ExecEditContract`, `ExecEditAudit`, `ExecReconciliation` whose `edit_paths` hold the report *and* the worktree draft). No `edit_paths` entry is a `skill://` URI, a glob, or a control-character path.
4. Limit of the search: the *recorded* round-23 event trace (`events.json`) and the falsify-phase manifest are **not** in this seat's declared read paths, so I could not confirm which request shapes actually occur in the recorded trace. Findings F1/F2 below are therefore stated as source-level defects with an explicit trigger condition, not as observed wave failures.

## 5. Findings by severity

### F1 — HIGH (conditional on one recorded event): the edit shape whitelist is closed, and one out-of-whitelist request destroys the entire audit verdict

`EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})` (line 116) is checked with `set(args) - {'i'} not in EDIT_SHAPES` (line 121). The `old_string`/`new_string` branch corresponds to this harness's `edit` tool, whose documented parameter set is `{i, path, old_string, new_string, replace_all}` — `replace_all` is a first-class documented flag of that same tool. The whitelist therefore omits a key that the audited tool legitimately emits.

Concretely, a recorded event

```json
{"tool": "edit", "args": {"i": "...", "path": "<exact declared report>", "old_string": "...", "new_string": "...", "replace_all": true}}
```

takes `set(args) - {'i'} == {'path','old_string','new_string','replace_all'}`, which is not in `EDIT_SHAPES` → `ValueError` (line 122) → caught at line 187-188 → `ids = ['SCOPE-SCHEMA']` → line 194 (`any(f['id'] == 'SCOPE-SCHEMA' …)`) → **exit code 2**, `status = 'CANNOT_EVALUATE'`, `request_audit_mode = 0`, **`structured_edit_mode = 0`**.

Impact on the attacked claim: the C2 metric (`structured_edit_mode`, target 1) is reported by the *whole-file* verdict, so one such event — in any seat, for any reason — drives the C2 metric to 0 and the command to exit 2, even though the v2 authority mechanism itself worked correctly for every other request in the same trace. The same escalation applies to the shape `OPAQUE_PATCH` (`{'input': …}` → `SCOPE-SCHEMA`, lines 310 / 317-318), i.e. an *unknown body* — which the C1 decision table grades as `UNKNOWN`, not as a schema failure — silently cancels the audit verdict for all seats.

The same escalation path is reachable with the harness's `edit` tool as it is actually spelled in this environment (`replace_all` present), so this is not a hypothetical spelling.

**Smallest in-scope remedy** (one constant, one new selftest case; no behavioural change for any other shape):

* line 116 → `EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'}, {'path', 'old_string', 'new_string', 'replace_all'})`
* new control next to line 302:
  `v2case('v2-replace-all-edit', 'edit', {'i': None, 'path': target, 'old_string': None, 'new_string': None, 'replace_all': True}, 0)` — expected exit 0, empty findings, `structured_edit_mode == 1` (the harness predicate at line 350 already enforces all three).

If, instead, the wave's position is that `replace_all` was genuinely never observed in recorded requests, then the *shape* exclusion is acceptable as "unknown shape → unknown" — but the **escalation** is still the defect, and the smallest remedy for that part is to keep per-event unknowns from cancelling the whole-file verdict (i.e. decide `SCOPE-SCHEMA` at event granularity rather than letting it set the file-level `code = 2`).

### F2 — MEDIUM: `structured_edit_mode` is coupled to the whole-file verdict, so the C2 metric under-reports the v2 capability

`result['structured_edit_mode'] = int(code != 2)` (lines 205-206) is emitted **only** when the manifest schema is v2 (line 205), yet its value is governed by the *global* verdict code, not by whether the v2 structured-edit path was available and exercised. Consequences:

* Any `SCOPE-SCHEMA` anywhere (F1) or any incomplete/missing seat (lines 168-176) sets the whole file to `code = 2` and hence `structured_edit_mode = 0`, i.e. C2's metric reads 0 for a wave in which v2 edit authority did operate for every well-formed request.
* Symmetrically, `structured_edit_mode` is 1 for a v2 manifest in which **no** structured edit was ever attempted — the flag measures "the audit could evaluate", not "the v2 authority was exercised". As a C2 metric (`before 0 → target 1`) this is a mode flag, not an outcome count, and it is satisfiable by an empty event list.

**Smallest in-scope remedy**: report the v2 capability independently of the file-level verdict — e.g. emit `structured_edit_mode` as a function of `v2 and (the v2 path was reachable for at least one event)`, and/or add a separate per-file counter such as `structured_edits_classified` / `structured_edits_denied` so the C2 metric has an outcome-bearing denominator instead of a mode bit. This is a metric-definition fix in the result assembly (lines 199-206) plus the preregister metric wording; it must not be applied by editing preregister numbers post hoc.

### F3 — LOW / informational: no defect, but a boundary worth stating explicitly for the record

Under v2, `edit` reaches `classify_edit` *before* the unknown-tool whitelist (line 76 precedes line 78). Under v1, `edit` therefore still returns `SCOPE-TOOL-UNKNOWN` (exit 1) and no `structured_edit_mode` key is emitted at all (line 205 is v2-only; controls `v1-extra-edit-field-no-grant` line 334 and `v1-edit-continuity` line 335, both with `mode=-1` asserting the key's absence). Legacy v1 policy and the historical reds are therefore unchanged, as C2 claims. This is a correct outcome, but it means the v2 grant is *manifest-wide and per-edit-shape*, not per-request: any seat in a v2 manifest inherits edit semantics for its own `edit_paths`. The landing manifest keeps `edit_paths` exactly equal to each seat's own report/draft, so the blast radius is the intended one — but the invariant is enforced by manifest curation, not by the tool.

## 6. Residual risk and verification gaps

* **Not executed.** No command, test, import, hash or linter was run (NO-EXEC/NO-FETCH). Every exit code, finding ID and `structured_edit_mode` value above is a hand-derivation from the landed source text with cited line anchors; the landed selftest was read, never run.
* **Digest supplied, not verified.** `4e00ab1f…3d6` is taken from the assignment as an identity claim only; no hashing, listing or byte count was performed.
* **Recorded trace not inspected.** The round-23 `events.json` and the falsify-phase bindings are outside this seat's declared read paths, so F1's trigger condition ("a recorded edit carries `replace_all`", or any out-of-whitelist shape) is **unconfirmed for this wave**. The defect is a property of the source and would fire on such an event; whether it fired in r23 is unknown here. A sibling seat with read access to the wave event trace should confirm or refute it — that check is the single highest-value follow-up, because it decides whether F1 is a latent defect or an active C2 regression (`structured_edit_mode` = 0, exit 2).
* **`local()` semantics relied upon.** The v2 authority gate delegates spelling safety to `local()` (line 40-42): it rejects control characters, `*?[];:` and empty/`.`/`..` path components, but does not resolve symlinks. Consistent with the tool's declared scope ("Recorded request spellings only; not runtime prevention, symlink/effect proof …", line 19), and unchanged from v1 — recorded here as scope, not as a defect.
* **No runtime enforcement is claimed.** `classify()`/`classify_edit()` never execute the requested operation (docstring line 62); the audit is post-hoc over recorded spellings. Nothing in this report asserts preventive enforcement, effect proof or reading proof.
* **Pre-registration respected.** The eight C1 edit decisions and the C3 census were not re-derived, re-scored or re-labelled here; no historical manifest or report was rewritten; no round-24 artefact was started.

## 7. Verdict (recommendation only)

The attacked sub-claim of **C2** — *`path` + `stream_content` against the exact declared report of a valid schema-v2 seat* — **survives** the hand-derivation: **exit code 0, no finding IDs, `structured_edit_mode = 1`**, `status = 'PASS'`, body opacity intact, v1 legacy behaviour untouched. The landed selftest already pins exactly this outcome (`v2-stream-edit`, line 301, with the empty-findings and `mode == 1` assertions at lines 348-350), so no new fixture is required for the primary scenario.

Two defects remain open against the C2 *metric as a whole*: **F1** (closed shape whitelist ⇒ a single out-of-whitelist `edit` request, e.g. one carrying the tool's own documented `replace_all`, escalates the entire audit to `SCOPE-SCHEMA` / exit 2 / `structured_edit_mode = 0`; smallest remedy: one extra `EDIT_SHAPES` member plus one selftest case, or event-granular instead of file-granular schema handling) and **F2** (`structured_edit_mode` is a whole-file mode bit coupled to the global verdict and satisfiable by an empty trace; smallest remedy: emit an outcome-bearing structured-edit counter alongside the mode flag). Both are recommendations for the landing integrator; this seat neither edits production files nor judges the wave.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oraclestream
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
Report: .ufo/waves/round-23/falsify/FxC2OracleStream.md
