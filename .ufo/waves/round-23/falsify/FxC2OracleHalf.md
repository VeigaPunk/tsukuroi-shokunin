# FxC2OracleHalf — v2 edit-shape oracle and audit-authority attack

Round 23, falsify, attempt 1. Baseline `ae01e50f582016384e620022be38bf5367000e2e`; landed state `5a25c88b77f52e940bcad87825c4ac1cd529470d`.
Scope of this seat: read-only reasoning over the landed candidate audit tool plus the preregister contract. `executed=none` — every exit code, finding ID and mode below is hand-derived from control flow, never observed.

Lane bounds: leaf member — no subagent dispatch.

## 1. Attacked claim

**C2** (axis `operability`, metric `structured_edit_mode`, before 0 → target 1;
command `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`;
scope: "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim.").

Attack surface: the v2 branch of `classify_edit` and the `code`/`mode` computation in the landed candidate tool
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`.
Question: do malformed admissibility shapes (half a replace; two bodies at once) fall inside the claim's finite authority outcomes, or do they crash, silently pass, or get misattributed?

C1 and C3 are not attacked here; no frontier claim exists in C2's scope, so the frontier is untouched. The preregister's eight `edit_decisions` were used only as the contract side of the comparison (see §5).

## 2. Landing points (candidate tool, line-anchored)

| line | content |
|---|---|
| 76–77 | `if tool == 'edit' and allow_structured_edit: return classify_edit(args, binding)` |
| 116 | `EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})` |
| 121–122 | `if not isinstance(args, dict) or set(args) - {'i'} not in EDIT_SHAPES: raise ValueError('unstructured or unknown edit arguments')` |
| 144 | `v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'` |
| 186–188 | `ids = classify(..., allow_structured_edit=v2)` / `except (...): ids = ['SCOPE-SCHEMA']` |
| 191–192 | `violations += sum(fid != 'SCOPE-SCHEMA' for fid in ids)` |
| 194 | `code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)` |
| 205–206 | `if v2: result['structured_edit_mode'] = int(code != 2)` |

Two structural properties decide everything below:

1. The shape guard is **exact set equality after deleting `i`** (line 121). There is no subset, prefix, or type test. The admitted key sets are exactly two literals; every other key set raises at the same statement.
2. The raise happens **before** the target/URL/denial checks (lines 123–128), and the `except` at 187 **replaces** any accumulated ids with `['SCOPE-SCHEMA']`. So an admissibility failure cannot also emit `SCOPE-EDIT-DENIED` or `SCOPE-FETCH-DENIED`.

## 3. Oracle: the two attacked requests

Assume the v2 manifest validates (target `T` present in that seat's `edit_paths`, which v2 forces to be a subset of both `read_paths` and `write_paths`), the trace has one complete seat `S` with exactly one event, and `T` is otherwise irrelevant because the guard aborts first.

### A. `old_string` without `new_string`

Event: `{"tool": "edit", "args": {"path": T, "old_string": "x"}}`

1. 76–77 → `classify_edit`.
2. 121: `{'path','old_string'} - {'i'}` = `{'path','old_string'}`; not equal to `{'path','stream_content'}` and not equal to `{'path','old_string','new_string'}` → `raise ValueError`.
3. 187–188: `ids = ['SCOPE-SCHEMA']`; `total += 1`; loop adds `{'id':'SCOPE-SCHEMA','site':'S:0'}` and `seat_findings=['SCOPE-SCHEMA']`.
4. 191–192: `violations += 0` (SCOPE-SCHEMA is excluded from the violation tally).
5. 194: a `SCOPE-SCHEMA` finding exists → `code = 2`.
6. 202–206: `status='CANNOT_EVALUATE'`, `request_audit_mode=0`, `structured_edit_mode=0`.
7. `main` returns `code`; `sys.exit(2)`.

Oracle result payload (seat `A` standing in for `S`):

```json
{"status": "CANNOT_EVALUATE", "request_audit_mode": 0, "seats_bound": 1,
 "requests_total": 1, "violations": 0, "incomplete_seats": 0,
 "missing_seats": 0, "present_incomplete_seats": 0,
 "seats": [{"name": "A", "agent": "agent-A", "requests": 1, "complete": true,
            "violations": ["SCOPE-SCHEMA"]}],
 "findings": [{"id": "SCOPE-SCHEMA", "site": "A:0"}],
 "scope": "Recorded request spellings only; ...", "structured_edit_mode": 0}
```

**exit 2 · ids `['SCOPE-SCHEMA']` · `structured_edit_mode` 0.**

### B. `stream_content` mixed with `old_string`

Two spellings, identical outcome.

- 3-key: `{"path": T, "stream_content": "b", "old_string": "x"}` → `{'path','stream_content','old_string'} - {'i'}` ∉ `EDIT_SHAPES` → raise → same path as A.
- 4-key (also carrying `new_string`): `{'path','stream_content','old_string','new_string'}` ∉ `EDIT_SHAPES` → raise → same path as A.

**exit 2 · ids `['SCOPE-SCHEMA']` · `structured_edit_mode` 0** (identical payload to A).

Adding `i` to either request changes nothing: line 121 deletes `i` before comparison, so `i` is optional for both admitted shapes and inert for both attacked ones.

Non-attacked controls from the same guard, for contrast:

- `{'path', 'stream_content'}` → admitted → `classify_edit` returns `[]` → exit 0, no ids, `structured_edit_mode` 1.
- `{'path', 'old_string', 'new_string'}` (with or without `i`) → admitted → exit 0, no ids, `structured_edit_mode` 1.

### Derived consequence not covered by the attacked phrasing

Because the raise precedes lines 123–128, a malformed shape aimed at an **undeclared** target also reports `SCOPE-SCHEMA` and not `SCOPE-EDIT-DENIED`, e.g. `{"path": "<LANE>/production", "old_string": "x"}` → exit 2, `['SCOPE-SCHEMA']`, mode 0, `violations` still 0. Confidence high (straight-line control flow), but this is inference-from-source, not observed output.

## 4. Selftest control check — controls exist

The landed selftest already pins both attacked triples, with the mode assertion attached:

- line 313 `v2-half-replace`, `{'path': target, 'old_string': None}`, expected `(2, 'SCOPE-SCHEMA')` — **exact equivalent of case A**.
- line 312 `v2-mixed-shapes`, `{'path': target, 'stream_content': None, 'old_string': None, 'new_string': None}`, expected `(2, 'SCOPE-SCHEMA')` — **exact equivalent of case B's 4-key spelling**.
- adjacent pins on the same guard: 310 `v2-opaque-patch` `{'input': None}`, 311 `v2-unknown-key` (superset), 314 `v2-missing-path` (subset, no `path`), 337 `v2-events-trace-marker` (event marker cannot grant).
- mode is asserted, not incidental: `v2case` defaults `mode = int(code != 2)` (lines 299–300), so each of these asserts `structured_edit_mode == 0`; line 348 (`mode_ok`) enforces it, and line 350 adds `(expected != 0 or not ids)` so an admitted case must carry no findings.

So the answer to the assigned "if not" branch: a control **is** present for both attacked spellings. The only spelling without a literal fixture is the 3-key `stream_content + old_string` (no `new_string`). That is not a behavioral gap — line 121 makes every non-literal key set an exact equivalence class, so `v2-half-replace` and `v2-mixed-shapes` bracket it from below and above. If the wave nevertheless wants per-spelling coverage, the literal fixtures are:

```python
v2case('v2-stream-half-replace', 'edit', {'path': target, 'stream_content': None, 'old_string': None}, 2, 'SCOPE-SCHEMA')
v2case('v2-half-replace-i', 'edit', {'i': None, 'path': target, 'new_string': None}, 2, 'SCOPE-SCHEMA')
```

Both list `target` (declared) deliberately, so the fixture isolates the shape guard rather than the target check.

## 5. Contract cross-check (preregister, contract side only)

The eight declared decisions map onto the candidate's finite outcomes: `DECLARED_EDIT/ALLOW`→`[]`; `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `EDIT_TRAVERSAL`→`SCOPE-EDIT-DENIED` (read/write-only are additionally blocked at manifest validation by the subset rule at 155–158, so they can never even reach `classify_edit`); `OPAQUE_PATCH/UNKNOWN`→`SCOPE-SCHEMA` with exit 2, which is the tool's encoding of UNKNOWN (`CANNOT_EVALUATE`), not a DENY; `EDIT_EXTERNAL`→`SCOPE-FETCH-DENIED`; `EXPANSION/CHECK_EACH`→ per-child classification in the parallel branch with `allow_structured_edit` propagated (line 91) and per-child `SCOPE-SCHEMA` on malformed children (92–93). No contract row is contradicted by the code, and no code outcome lacks a contract row.

## 6. Falsifier search: bounded, and what it found

Bounded search space: every decision point reachable from `classify_edit` and from the `code`/`mode` computation in the v2 event path (lines 76–77, 116–128, 144, 155–158, 180–206). Exhaustive by construction because the only input-dependent branch in the edit path is the literal set-equality at 121.

Negative results (no falsifier of the derived triple):

- No third admitted shape exists; no prefix/subset/type leniency. Half-replace and mixed bodies cannot reach a path check, so cannot yield 0 or 1.
- Only two producers of exit 2 exist on this path — a `SCOPE-SCHEMA` finding (194) or an exception escaping the whole `try` (195–197). Both yield 2; neither yields 1.
- `structured_edit_mode` has exactly one writer (206) and no other branch can set it.

Positive results (bounded weaknesses in the *metric*, not the code path):

1. **Vacuous satisfaction.** A validated v2 manifest plus a complete seat with `events: []` yields exit 0, no findings, `requests_total: 0`, and `structured_edit_mode: 1` (144 → empty loop 180–193 → 194 → 206). Evidence: the v1 fixture at 244–246 (`empty-trace`, expected exit 0) already asserts that the empty-events path is admitted; v2 only adds the mode field, so the same path returns mode 1. Consequence: `structured_edit_mode: 1` alone does not evidence that any structured edit was admitted; C2's target is satisfiable with zero edit requests. There is no `v2-empty-events` fixture, so this vacuity is unpinned and undisclosed.
2. **Global, not per-seat, mode.** Any unrelated `SCOPE-SCHEMA` from any seat or event (e.g. a read carrying an extra argument key, the v1 `extra-argument` class) forces `code = 2` and therefore mode 0, even with zero edit events involved. Consequence: mode 0 must not be read as "v2 edit authority broken"; symmetrically, mode 1 requires *every* recorded request in *every* bound seat to be schema-clean.
3. **Masking and zero violations.** Shape errors precede target checks and are excluded from the `violations` tally (191–192). Consequence: `violations: 0` cannot be read as "no seat attempted an out-of-scope edit", and a malformed edit at an undeclared path is recorded as schema, not denial.

None of 1–3 falsifies the hand-derived exit/id/mode triples, and none is contradicted by the selftest; 1 is the one that bears directly on whether C2's *witness* is sufficient.

Confidence: triples in §3 — high (straight-line control flow, all functions pure apart from JSON decoding). §4 equivalence — high (line-level fixtures, mode asserted). §6.1 — high (same code path as an asserted v1 fixture). §6.2–6.3 — high.

## 7. Remaining unknowns (declared-scope gaps, not improvised)

- `.ufo/waves/round-23/<WAVE>/events.json` is outside this seat's declared read set, so I cannot state whether the captured events contain a malformed edit or any unrelated `SCOPE-SCHEMA`. That single unread fact decides whether the round's C2 witness reports mode 1 or 0.
- `tools/check-edit-contract.py` (C1's command) is outside this seat's declared read set; the C1 side above is contract-text only, not tool behavior.
- No execution was permitted (`executed=none`), so no output here is observed; every value is derived. This report never claims runtime enforcement, and the tool's own `SCOPE` string disclaims prevention/effect proof.

## 8. Smallest in-scope remedy

For the attacked triples: **none** — the candidate's selftest already pins both, and the code returns the finite `SCOPE-SCHEMA`/exit-2/mode-0 outcome rather than crashing or passing.

For the metric-sufficiency gap found in §6, the smallest in-scope move (this seat's write scope is this report only, so the remedy is witness-side):

- When C2 cites `structured_edit_mode: 1`, also cite `requests_total > 0` and at least one `seats[*].violations == []` row whose event tool was `edit`/`functions.edit` in an admitted shape; and state that mode is a conjunction over schema cleanliness of every bound seat, not a per-seat edit verdict (so mode 0 and `violations: 0` are not over-read).
- If a test pin is wanted, one line: `v2case('v2-empty-events', 'edit', ..., 0, None)` is *not* the right pin (it would bless vacuity); the right pin is a positive admitted-edit fixture already present at 301/302, cited as the non-vacuous pair alongside an empty-events case that asserts mode 1 while `requests_total == 0`, so the vacuity is disclosed rather than hidden.

No production file, manifest, event trace, selftest, or git state is modified by this seat.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oraclehalf
Scope: executed=none
