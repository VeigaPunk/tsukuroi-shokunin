# FxC2OracleOldNew — v2 structured-edit oracle (old/new derivation + control)

## Claim under attack

**C2 / operability / `structured_edit_mode` (before 0, target 1).**
Scope as preregistered: "New explicit schema-v2 audit authority for exact predeclared
structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data
opaque, no native enforcement/effects claim."
(`.ufo/waves/round-23/preregister.json`, claims[] C2.)

Attacked surface: the total function `evaluate()` in the landed checker, specifically the
`edit` branch reached through `classify()` → `classify_edit()`, and the `structured_edit_mode`
key it emits. Source of record:
`candidate/tools/check-seat-bindings.py` (declared SHA-256
`4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6` — supplied identity, not
recomputed here).

## Hand derivation — v2 audit of `path` + `old_string` + `new_string` + `i`

Request R: one recorded event with `tool = "edit"` and
`args = {"i": <string>, "path": D, "old_string": <string>, "new_string": <string>}`,
where D is the **exact literal** path of the draft declared for that seat, and the manifest is
schema `tsukuroi-seat-bindings-v2`.

Step chain, landed source only:

1. `evaluate()` line 140–145: `v2` is set from `data.get("schema") == "tsukuroi-seat-bindings-v2"`;
   schema key set must be exactly `{schema, seats}`; `seats` non-empty list. Assumed satisfied.
2. Per-seat validation, lines 148–161: `name` matches `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`,
   `root == LANE`, `commands == []`, `fetches == []`; `read_paths`/`write_paths` non-empty,
   duplicate-free, each `local(p)` (except the single literal `skill://godspeed` in reads).
   v2 branch (156–161): `set(seat)` must equal exactly
   `{name, root, read_paths, write_paths, edit_paths, commands, fetches}`;
   `edit_paths` duplicate-free; **each edit path** `local(p)` **and** `p in read_paths`
   **and** `p in write_paths`.
3. Trace validation, lines 163–173, then 174–179: every bound seat must have exactly one trace
   entry with a unique non-empty `agent`, `type(complete) is bool`, `events` a list. A missing
   seat adds `SCOPE-TRACE-MISSING` *and* increments `incomplete`; `complete is False` adds
   `SCOPE-TRACE-INCOMPLETE` and increments `incomplete`. Both force code 2.
4. Event classification, line 186:
   `classify("edit", args, binding, allow_structured_edit=v2)`.
   The flag originates only here, from the validated top-level schema (docstring 61–65;
   line 158's exact key set rejects a row-carried `allow_structured_edit`, and line 337 proves
   the event-carried marker is rejected).
5. `classify()` line 76–77: `tool == "edit" and allow_structured_edit` → `classify_edit(args, binding)`.
6. `classify_edit()`:
   - line 118: `set(args) - {"i"}` = `{"path","old_string","new_string"}`. `EDIT_SHAPES`
     (line 116) is `({"path","stream_content"}, {"path","old_string","new_string"})`; the set is
     `in` it, so `not in` is False → **no** `ValueError`.
   - line 121–123: `path` is a non-empty string → no raise.
   - lines 126–127: not `^https?://` and not `^[^/:\s]+:[0-9]+/`. An absolute `LANE + "/…"` path
     begins with `/`, so the port-like alternative cannot match, and the path contains no colon.
     → no `SCOPE-FETCH-DENIED`.
   - lines 128–130: `value in binding["edit_paths"]` — string identity against the seat's declared
     list. D is the exact declared spelling → **`return []`**.
7. `evaluate()` lines 189–193: `ids == []`; no `add()` call; `violations += 0`; row records
   `requests: 1`, `violations: []`.
8. Line 194: no `incomplete`, no `SCOPE-SCHEMA` in findings, `findings` empty
   → `code = 0`.
9. Lines 199–206: `status = "PASS"`, `request_audit_mode = int(0 != 2) = 1`,
   `seats_bound = len(bound)`, `requests_total = 1`, `violations = 0`,
   `incomplete_seats = 0`, `missing_seats = 0`, `present_incomplete_seats = 0`,
   `findings = []`; because `v2` is True, `structured_edit_mode = int(code != 2) = 1`.

**Derived result for R (exact declared draft, v2 manifest, seat present and complete):**

| field | value |
|---|---|
| exit code (return of `main`/`evaluate`) | **0** |
| finding IDs | **none — `findings` is exactly `[]`** (no `SCOPE-EDIT-DENIED`, no `SCOPE-SCHEMA`) |
| `structured_edit_mode` | **1** |
| ancillary | `status = "PASS"`, `request_audit_mode = 1`, `violations = 0`, `requests_total = 1` |

`structured_edit_mode` is `int(code != 2)`, i.e. "manifest was v2 and the audit was evaluable".
It is **not** an "edit was granted" bit: a v2 audit whose only edit is denied also reports
mode 1 (see `v2-empty-edit-paths`, line 332). Only `exit 0` together with `findings == []`
certifies the grant.

## Exactness sensitivity (why "exact" is load-bearing)

Same request, single mutations, all derived from the same lines:

| mutation of R | exit | finding IDs | `structured_edit_mode` |
|---|---|---|---|
| exact declared D | 0 | `[]` | 1 |
| `D + "/"`, `./` segment, `x/..` segment, `//`, `D + ":raw"`, relative spelling, `D.upper()`, `skill://godspeed`, `xd://edit` | 1 | `[SCOPE-EDIT-DENIED]` | 1 |
| `https://…` target | 1 | `[SCOPE-FETCH-DENIED]` | 1 |
| extra arg key; `stream_content` mixed with `old_string`/`new_string`; half replace; missing/non-string path; non-dict args | 2 | `[SCOPE-SCHEMA]` | 0 |
| v1 manifest that even carries `edit_paths` | 1 | `[SCOPE-TOOL-UNKNOWN]` | key absent |
| seat absent from trace | 2 | `[SCOPE-TRACE-MISSING]` (+ `incomplete_seats = 1`) | 0 |
| seat `complete: false` with an otherwise allowed edit | 2 | `[SCOPE-TRACE-INCOMPLETE]` | 0 |
| any allowed edit plus any other `SCOPE-SCHEMA` event | 2 | `[SCOPE-SCHEMA, …]` | 0 |

Note the two different one-step reds: a *denial* finding yields 1, a *schema/incomplete* finding
yields 2. A v2 audit of an exact declared target therefore cannot land on 1 by any argument-shape
mutation — it either stays 0 or becomes 2/1 for a named reason.

## Control check — landed selftest

**Equivalent control exists; no new fixture needed.** Landed at line 302:

```python
v2case('v2-replace-edit', 'edit', {'i': None, 'path': target, 'old_string': None, 'new_string': None}, 0)
```

with the literal v2 probe manifest (lines 295–297):

```python
target, other = LANE + '/drafts/A.md', LANE + '/drafts/B.md'
v2 = {'schema': 'tsukuroi-seat-bindings-v2', 'seats': [{'name': 'A', 'root': LANE,
      'read_paths': [src, target, other, 'skill://godspeed'],
      'write_paths': [target, LANE + '/w-only.md'], 'edit_paths': [target],
      'commands': [], 'fetches': []}]}
```

This matches R on every decision-bearing feature: same key shape modulo the opaque `i` value,
same `path`-membership class (exact declared draft, present in read ∩ write ∩ edit), expected
exit 0. It is *stronger* than R on body opacity (bodies are `None`, and `classify_edit` never
reads them) and *weaker* only on `i` being a string — immaterial, since `i` is never inspected.

The v2 assertion loop (lines 345–350) checks exactly the fields R is about:

```python
mode_ok = ('structured_edit_mode' not in result) if mode == -1 else result.get('structured_edit_mode') == mode
... 'pass': code == expected and all(item in ids for item in required) and (expected != 0 or not ids) and mode_ok
```

with `mode` defaulting to `int(code != 2)` (line 300) → for this case `mode == 1`, so the control
asserts exit 0 **and** empty findings **and** `structured_edit_mode == 1`.

Old-side continuity is also controlled, which is the "old" half of this oracle:

- line 335 `v1-edit-continuity`: v1 manifest, edit event → exit 1, `SCOPE-TOOL-UNKNOWN`,
  `mode = -1` (asserts the `structured_edit_mode` key is **absent**, not zero).
- line 334 `v1-extra-edit-field-no-grant`: v1 manifest that *does* carry `edit_paths` → still
  `SCOPE-TOOL-UNKNOWN`, mode key absent. This is the direct proof that v2 authority is not
  reachable from a v1 manifest.
- line 337 `v2-events-trace-marker`: `allow_structured_edit` smuggled through event args →
  `SCOPE-SCHEMA`; line 331 `v2-row-marker`: smuggled through the seat row → `SCOPE-SCHEMA`.

So the old/new oracle pair is coherent: v1 request → `1 / [SCOPE-TOOL-UNKNOWN] / mode absent`;
v2 exact request → `0 / [] / mode 1`.

## Falsifier search

Bounded, source-only; nothing executed (NO-EXEC).

1. **Argument-shape partitions.** `EDIT_SHAPES` (line 116) is an equality test on
   `set(args) - {"i"}`. Enumerated partitions reachable from the two declared shapes:
   exact replace, exact stream, mixed, half, unknown-key, opaque `input`, missing path,
   non-dict. Each maps to 0 or `SCOPE-SCHEMA` (2) exactly as the landed controls
   (`v2-replace-edit` 302, `v2-mixed-shapes` 312, `v2-half-replace` 313, `v2-unknown-key` 311,
   `v2-opaque-patch` 310, `v2-missing-path` 314) assert. No partition yields an allow with an
   inexact target.
2. **Target spellings.** The eight C1 decisions' adversarial forms (traversal, prefix,
   alternate scheme, uppercase, read-only, write-only, undeclared) are all denied at
   lines 128–129 and are all individually controlled (307–308, 304–306).
   `classify_edit` performs no `local()` call of its own; that is safe *because* lines 156–161
   refuse any manifest whose `edit_paths` are not already `local` and in both read and write
   lists. So an event path can never be outside `LANE`, `;`-joined, globbed, or a URI.
3. **Authority laundering.** `allow_structured_edit` has exactly one producer (line 186, from
   `v2`) — confirmed by exhaustive grep of `structured_edit_mode|edit_paths|allow_structured_edit`:
   the only other occurrences are the manifest validator (156–161), the selftest fixtures, and
   line 206's emission. No row field, event field, or nested wrapper can set it.
4. **Whole-manifest validity** (the one way an allowed event still cannot yield 0): I read all
   1316 lines of `build/bindings.json`. All 64 seat blocks carry exactly the seven keys; in every
   block `write_paths` and `edit_paths` are the identical single/twin lists; every one of those
   paths also appears in that seat's `read_paths`; `commands`/`fetches` are `[]` throughout; no
   duplicated string was observed inside any single list. So the landed v2 manifest does not
   itself force `SCOPE-SCHEMA`/exit 2.
5. **Exact seat analog.** `OracleV2OldNew` (bindings.json: 672–712) declares
   `read_paths` including `.ufo/waves/round-23/build/OracleV2OldNew.md`, `write_paths` and
   `edit_paths` equal to exactly that path. An audit of an exact `path+old_string+new_string`
   edit against that declaration returns 0 / `[]` / 1 by the chain above.

**Result: no falsifier found.** C2's decision "exact declared target → allow, everything else
named-red" is closed over the mutation space the claim names, and the landed selftest already
pins both the new (v2) and old (v1) sides, including the mode assertion.

## Residual gaps (recorded, not falsifiers)

- **Vacuity of the metric.** `structured_edit_mode = 1` for *any* evaluable v2 audit, including
  one with no edit event at all (a v2 manifest whose seats have `events: []` returns 0 / `[]` / 1).
  The metric is a capability/parse indicator, not non-vacuity of the C2 run. Whether the
  round-23 events actually contain the documented edit is a property of
  `.ufo/waves/round-23/**/events.json`, which is **outside this seat's declared read set** —
  recorded as an unread gap, not assumed.
- **Cross-seat isolation is derived but not directly controlled.** All v2 edit controls use a
  one-seat manifest. The code is per-seat (`binding["edit_paths"]`, binding looked up by the
  event's seat name at 174/186), so seat A cannot edit seat B's declared draft; that is an
  [INFERENCE] from the code path, not a landed assertion.
- **This seat is absent from the landed build manifest.** Grep of
  `build/bindings.json` for `FxC2OracleOldNew` returns no match; the landed manifest is the
  build-phase seat set. My own dispatch binding declares
  `.ufo/waves/round-23/falsify/FxC2OracleOldNew.md` as read/write/edit target, but that
  declaration lives in the dispatch envelope, not in this file. Since the grant is a pure
  membership test on the seat's own `edit_paths`, the derivation transfers unchanged; the
  realized falsify-wave audit result is [UNKNOWN — out of read scope].
- **No native enforcement claimed or observed.** The checker's own docstring (line 2, and
  `SCOPE` at line 19) says "Audit recorded requests … not preventive enforcement". Nothing here
  supports a runtime-restriction claim, and none is made.

## Smallest in-scope remedy

No production change is required for C2: the attacked request is already derived as
`0 / [] / 1` and the landed selftest already contains the equivalent control.

If the frontier wants to close the one control-coverage gap above, the minimal addition is a
single v2 case in `selftest()` — literal, one-seat-per-side, no production manifest:

```python
v2x = copy.deepcopy(v2); v2x['seats'].append({'name': 'B', 'root': LANE, 'read_paths': [other],
    'write_paths': [], 'edit_paths': [], 'commands': [], 'fetches': []})
```

This probe is **not valid as written** under lines 148–161 (`write_paths` non-empty required,
and `edit_paths` must be a list) — the usable literal is instead: give seat `A` the existing
probe and assert that `A`'s event naming `other` (seat B's target, not in A's `edit_paths`)
yields `1 / [SCOPE-EDIT-DENIED] / 1`, which is already exactly `v2-read-only-target` (line 304)
generalized. In other words: the cross-seat case collapses to the existing undeclared-target
control, so **no new fixture is warranted**. Record instead, in the C2 evidence line, that
`structured_edit_mode = 1` must be read together with `exit 0` and `findings == []`, since mode
alone is also 1 on a fully denied v2 audit.

## Scope / provenance

Read (declared only): `candidate/tools/check-seat-bindings.py` (full, 396 lines),
`preregister.json` (full), `build/bindings.json` (full, 1316 lines),
`skill://godspeed`. Wrote: this report only.
No commands, no fetches, no imports, no hashing, no listing: `executed=none`.
Digest `4e00ab1f…8cf3d6` is the supplied declaration; it was not recomputed.
No installs or updates occurred (and are forbidden in this seat's NO-EXEC scope).

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oracleoldnew
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
