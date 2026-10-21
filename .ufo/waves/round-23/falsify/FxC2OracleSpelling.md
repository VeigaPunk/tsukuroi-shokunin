# FxC2OracleSpelling — C2 v2 edit authority under alias spellings

Seat `TsukuroiR23-2.FxC2OracleSpelling-2`. Evidence: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`, declared SHA256 `4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6` (supplied identity, not computed here). All findings are hand-derived from that source; no execution, hashing, listing or import was performed (NO-EXEC/NO-FETCH). Lane bounds: leaf member — no subagent dispatch.

## Attacked claim

C2 (`preregister.json:31-37`): metric `structured_edit_mode`, before 0, target 1, scope *"New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."* The concrete decision under test is the `EDIT_TRAVERSAL` row (`preregister.json:84-86`): **"No dot-segment or alternate spelling expands the target list"** (DENY). This is C2, not C1: the eight edit-contract decisions live in `check-edit-contract.py`, while the audit authority and `structured_edit_mode` live in this checker. Nothing about C3 is touched.

## Hand derivation from the landed source

Minimal well-formed v2 wave used for the derivation (one seat, one event):

```json
{"schema":"tsukuroi-seat-bindings-v2","seats":[{"name":"A","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
 "read_paths":["<src>","/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md","skill://godspeed"],
 "write_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"],
 "edit_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"],"commands":[],"fetches":[]}]}
```
```json
{"schema":"tsukuroi-seat-events-v1","seats":[{"name":"A","agent":"agent-A","complete":true,
 "events":[{"tool":"edit","args":{"path":"<SPELLING>","stream_content":null}}]}]}
```

Branch-by-branch for `target = LANE + '/drafts/A.md'` and each spelling:

1. Manifest validation (lines 145-161) passes: exactly the seven v2 keys (158), every `edit_paths` entry `local()` (160), and `edit_paths ⊆ read_paths ∩ write_paths` (160). `v2` is set true at 144.
2. Event dispatch calls `classify(..., allow_structured_edit=v2)` at 186; line 76 routes `tool == 'edit'` to `classify_edit` (77).
3. `classify_edit` shape gate (121): `set(args) - {'i'} == {'path','stream_content'}`, which is `EDIT_SHAPES[0]` (116) — no raise.
4. Target is a non-empty string (123-125).
5. Neither fetch regex fires (126-127): both `(?i)^https?://` and `^[^/:\s]+:[0-9]+/` are anchored and the spelling begins with `/`. No `SCOPE-FETCH-DENIED`.
6. `value not in binding['edit_paths']` is true (128-129). Membership is plain Python string equality over the literal list: **no case folding, no NFC/NFD normalization, no `normpath`, no dot-segment collapse, no trailing-slash strip, no selector strip**. `local()` is not consulted here. Result `['SCOPE-EDIT-DENIED']`.
7. `evaluate` records `{'id':'SCOPE-EDIT-DENIED','site':'A:0'}`, seat `violations: ['SCOPE-EDIT-DENIED']`, `violations = 1` (189-192).
8. Exit-code line 194: `incomplete = 0` and no `SCOPE-SCHEMA`; findings non-empty → **code 1**. Line 199 maps code 1 to `status = "FAIL"`.
9. Lines 205-206: v2 → **`structured_edit_mode = int(code != 2) = 1`**.
10. `main` prints with `sort_keys=True` (391) and **returns 1** (392).

Exact result object (before `main` adds `revision`/`branch`/`branch_tip`):

```json
{"findings":[{"id":"SCOPE-EDIT-DENIED","site":"A:0"}],
 "incomplete_seats":0,"missing_seats":0,"present_incomplete_seats":0,
 "request_audit_mode":1,"requests_total":1,
 "scope":"Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.",
 "seats":[{"agent":"agent-A","complete":true,"name":"A","requests":1,"violations":["SCOPE-EDIT-DENIED"]}],
 "seats_bound":1,"status":"FAIL","structured_edit_mode":1,"violations":1}
```

| Class | Literal spelling (relative to `target`) | Branch reached | Finding IDs | Exit | `structured_edit_mode` |
|---|---|---|---|---|---|
| trailing slash | `target + '/'` | 128-129 | `SCOPE-EDIT-DENIED` (only) | 1 | 1 |
| dot segment | `LANE + '/drafts/./A.md'` | 128-129 | `SCOPE-EDIT-DENIED` (only) | 1 | 1 |
| dot-dot traversal | `LANE + '/x/../drafts/A.md'` | 128-129 | `SCOPE-EDIT-DENIED` (only) | 1 | 1 |
| double slash | `LANE + '//drafts/A.md'` | 128-129 | `SCOPE-EDIT-DENIED` (only) | 1 | 1 |
| case variant | `target.upper()` | 128-129 | `SCOPE-EDIT-DENIED` (only) | 1 | 1 |

All five converge because exact membership is the only target test. The result is identical for the same spellings wrapped in `multi_tool_use.parallel` (children inherit `allow_structured_edit`, line 91).

Manifest-side gate (defense in depth): the same alias spellings cannot be *declared* either. `local()` (33-36) requires every component after the leading `/` to be non-empty and not `.`/`..`, so dot segments, double slashes and trailing slashes fail; lines 158-161 then raise `ValueError('v2 edit authority')`, caught at 195 as `SCOPE-SCHEMA` at site `input`, exit 2, `structured_edit_mode` 0 (v2 already detected at 144). Only a case variant can be declared, and then only as an additional literal string that must also appear in `read_paths` and `write_paths` (160).

## Landed selftest control: present, equivalent, no fixture needed

The selftest already builds exactly this v2 manifest and asserts the outcome for every one of the four classes (`check-seat-bindings.py`):

```
295  target, other = LANE + '/drafts/A.md', LANE + '/drafts/B.md'
296  v2 = {'schema': 'tsukuroi-seat-bindings-v2', 'seats': [{'name': 'A', 'root': LANE, 'read_paths': [src, target, other, 'skill://godspeed'],
297                                                        'write_paths': [target, LANE + '/w-only.md'], 'edit_paths': [target], 'commands': [], 'fetches': []}]}
299  def v2case(name, tool, args, code, fid=None, manifest=None, mode=None, events=None):
300      v2_cases.append((name, v2 if manifest is None else manifest, trace(tool, args) if events is None else events, code, fid, (int(code != 2) if mode is None else mode)))
307  for spelling in (target + '/', LANE + '/drafts/./A.md', LANE + '/x/../drafts/A.md', LANE + '//drafts/A.md', target + ':raw', 'drafts/A.md', 'skill://godspeed', 'xd://edit', target.upper()):
308      v2case('v2-spelling-' + spelling, 'edit', {'path': spelling, 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
```

Mapping: trailing slash → `target + '/'`; dot segment → `LANE + '/drafts/./A.md'` and `LANE + '/x/../drafts/A.md'`; double slash → `LANE + '//drafts/A.md'`; case variant → `target.upper()`. Each expects code 1 with `SCOPE-EDIT-DENIED`; the default `mode` at line 300 is `int(code != 2) = 1`, and the pass predicate at 348-350 requires `code == expected`, the id present, and `result.get('structured_edit_mode') == 1`. My derivation matches on all three fields, so the controls pass as landed and would fail on admission (code 0) or on non-evaluation (code 2). **No literal fixture is missing for the attacked classes.** Cross-check: the v1 analogue at line 276 (`LANE + '//source'` on `read`) denies via `local()` as `SCOPE-PATH-DENIED` — a different gate, same denial.

## Bounded falsifier search — none found

Routes examined for any path from an alias spelling to exit 0 or an admitted edit:

1. **No normalization exists in the edit path.** `classify_edit` (121-130) contains only a shape gate, a type/emptiness check, two fetch regexes, and list membership. `requested_path` (43-58), which is the only selector-stripping and `local()`-calling routine, is used exclusively for read/grep/glob/write (108-112).
2. **Fetch branches cannot capture these spellings.** Both regexes at 126 are start-anchored; an absolute path starts with `/`, and a case variant cannot introduce `:` because no declared edit path may contain `:` (`local()`, 35) and the terminal components do not.
3. **Tool routing is exact.** One `functions.` strip (68-70), then only the literal `'edit'` reaches `classify_edit` (76-77); `'Edit'`, `'edit '`, or `edit` under v1 fall to `SCOPE-TOOL-UNKNOWN` (79) — still a denial. Nested children inherit the v2 flag (91), so a wrapper cannot downgrade to the v1 branch.
4. **Authority cannot be forged from event data.** The seat key set is fixed (158), a payload marker such as `allow_structured_edit` makes the args shape fail (121; control at 337), a schema typo fails 145 (control 336), and duplicate JSON keys raise in `unique` (20-27) before v2 detection.
5. **`edit_paths ⊆ write_paths` is enforced** (160), so a declared edit target can never exceed write authority; and non-canonical spellings are undeclarable (33-36, 161).
6. **Landed manifest spot-check** (read-only on the declared path `build/bindings.json`): schema is `tsukuroi-seat-bindings-v2` with 64 seats, all carrying `edit_paths`; a query for seats with `edit_paths - read_paths` or `edit_paths - write_paths` non-empty returned empty, and a query for `edit_paths` containing `//`, `/./`, `/../` or ending `/` returned empty — both non-vacuous against a positive control that returned all 64 seat names. The landed manifest can therefore establish v2 mode. The events file for the C2 command is not in this seat's declared read set, so **no empirical audit result is claimed**.

## Residual observations (non-falsifying, bounded)

- **Assertion strength is containment, not equality.** Line 350 uses `all(item in ids ...)` for non-zero cases; an extra co-emitted non-schema finding at the same site would not fail the control. It cannot arise from the membership branch (single-element return), but the control is not an exact-set assertion.
- **Adjacent uncovered shape.** An edit event carrying a target but no body key, e.g. `{'path': target}`, fails the shape gate at 121 and becomes `SCOPE-SCHEMA` → exit 2, mode 0. No selftest pins that exact combination (nearest are `v2-opaque-patch` 310, `v2-half-replace` 313, `v2-missing-path` 314). Outside the four attacked classes; the smallest optional fixture would be `v2case('v2-path-only', 'edit', {'path': target}, 2, 'SCOPE-SCHEMA')`.
- **Edit targets are necessarily whole-file writable.** Because `edit_paths ⊆ write_paths` is mandatory (160), `write` to any edit target is ALLOW (pinned at 320). This is the intended `READ_ONLY_EDIT`/`WRITE_ONLY_EDIT` design (edit is the narrowest authority: read ∧ write ∧ edit), not an expansion of the target set.
- **Case variants may both be declared.** `local()` performs no case canonicalization, so `.../drafts/A.md` and `.../DRAFTS/A.md` could both appear as literal targets; each would still need read and write authority, and filesystem/effect identity is explicitly disclaimed by `SCOPE` (line 17). No undeclared target becomes reachable.
- **Mode 1 is wave-global.** Any missing/incomplete trace or any `SCOPE-SCHEMA` elsewhere forces code 2 and `structured_edit_mode` 0 (194, 206) while the edit denial stays in `findings`; the metric measures v2 activation plus evaluability, not per-event authority.

## Verdict

Attacked claim **C2 / `EDIT_TRAVERSAL`** survives. For a dot segment, double slash, trailing slash, or case variant of a declared edit target, a clean v2 audit yields exactly one finding `SCOPE-EDIT-DENIED` at site `<seat>:<index>`, `status` `FAIL`, `request_audit_mode` 1, `violations` 1, **process exit code 1**, and **`structured_edit_mode` 1**. The landed selftest already contains equivalent controls for all four literal fixtures (lines 307-308), so no new fixture is required. Smallest in-scope remedy: none for the attacked classes; the only optional hardening is the adjacent `v2-path-only` fixture noted above. Confidence: high on the derivation (every branch cited, single code path, no runtime needed) and on control presence (literal lines); no claim is made about production events, which are outside this seat's declared read scope.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oraclespelling
Scope: executed=none
