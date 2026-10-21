# FxC2ClassifyEdit — falsify round 23 (attempt 1)

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`
(landed copy of the `ExecEditAudit` draft; declared SHA256 supplied by the seat binding, **not** independently computed).
Baseline `ae01e50f582016384e620022be38bf5367000e2e`; landed revision `5a25c88b77f52e940bcad87825c4ac1cd529470d`.

Method: static read/grep only. This seat is NO-EXEC / NO-FETCH: no bash, no eval, no subprocess, no import, no
tool run, no hashing, no delegation. Every path read is inside this seat's declared `read_paths`
(candidate tool, snapshot tool, `preregister.json`, `candidate/collect.py`, `candidate/.ufo/waves/round-23/measure/l1-mutation.json`,
`build/bindings.json`, `skill://godspeed`). `skill://godspeed` resolved, so the copied directive was not needed.
Nothing was executed, so every verdict below is derived by construction from the cited source lines, not observed output.

## Attacked claim

- **Primary: C2** (`axis: operability`, `metric: structured_edit_mode`, `before: 0`, `target: 1`) — "New explicit
  schema-v2 audit authority for exact predeclared structured edit targets". The v2 authority is implemented by
  `classify_edit()` (candidate tool lines 116–130) reached from `classify()` line 76–77, and the metric is emitted at
  line 206 (`result['structured_edit_mode'] = int(code != 2)`).
- **Secondary: C1** decision `DECLARED_EDIT / ALLOW` ("Exact target is predeclared for edit and for both read and write")
  and `OPAQUE_PATCH / UNKNOWN` — the adjudication contract that `classify_edit()` implements for the eight
  `edit_decisions` rows in `preregister.json`.
- **Tertiary: C3** — checked only for interaction (does the recorder's key projection feed the path census?).
  No C3 impact found; see "C3 cross-check".

---

## Findings

### F1 — MAJOR: `EDIT_SHAPES` omits the native edit tool's optional `replace_all` key, so a *legal* edit call is
adjudicated as `SCOPE-SCHEMA` and escalates the whole wave audit to `CANNOT_EVALUATE` (zeroing C2's metric)

Evidence.

- `candidate/tools/check-seat-bindings.py:116`
  `EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})`
- `candidate/tools/check-seat-bindings.py:121`
  `if not isinstance(args, dict) or set(args) - {'i'} not in EDIT_SHAPES: raise ValueError('unstructured or unknown edit arguments')`
- `candidate/tools/check-seat-bindings.py:186-188` — `ids = classify(...)` inside `try`, `except (ValueError, ...) -> ids = ['SCOPE-SCHEMA']`
- `candidate/tools/check-seat-bindings.py:194` — `code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else ...`
- `candidate/tools/check-seat-bindings.py:199` — `'request_audit_mode': int(code != 2)`
- `candidate/tools/check-seat-bindings.py:206` — `result['structured_edit_mode'] = int(code != 2)`
- `candidate/collect.py:49` — recorder key whitelist
  `known = {'i','path','pattern','case','gitignore','skip','hidden','limit','content','stream_content','old_string','new_string'}`
- `candidate/collect.py:51` — `projected = {key if key in known else '__unknown_argument__': None for key in args}`

The harness `edit` tool of this substrate is signed `i, path, old_string, new_string, replace_all?: boolean`
(`replace_all` is a documented, optional, first-class parameter of that tool). In-repo corroboration that the author
normally derives key sets from the tool schemas rather than inventing them: the v1 `allowed_keys` map at
candidate lines 96–101 matches the live schemas exactly (`read {i,path}`, `grep {i,pattern,path,case,gitignore,skip}`,
`glob {i,path,hidden,gitignore,limit}`, `write {i,path,content}`). The `edit` entry is the only one that is not
schema-derived: it lists a key (`stream_content`) that no harness tool exposes and omits a key (`replace_all`) that
the harness edit tool does expose.

Falsifier chain (construction, no execution):

1. A seat issues a native, in-scope edit: `edit(path=<declared edit target>, old_string=..., new_string=..., replace_all=true)`.
2. Recorder (`collect.py:51`) rewrites the legal key `replace_all` to `__unknown_argument__`, because `replace_all` is
   not in `known` at `collect.py:49`. The recorded event loses the distinction between a legal tool parameter and a
   genuinely unknown argument.
3. Auditor (`check-seat-bindings.py:121`): `set(args) - {'i'}` = `{'path','old_string','new_string','__unknown_argument__'}`,
   which is not a member of `EDIT_SHAPES` → `ValueError` → `SCOPE-SCHEMA` (line 188).
   Even if the recorder were fixed, the auditor alone still fails the same call: `{'path','old_string','new_string','replace_all'}`
   is likewise not a member of `EDIT_SHAPES`. **The defect is two-site; either site alone reproduces it.**
4. `evaluate()` line 194 turns the presence of any `SCOPE-SCHEMA` finding into `code = 2` →
   `status = 'CANNOT_EVALUATE'`, `request_audit_mode = 0` (line 199) and, for a v2 manifest,
   `structured_edit_mode = 0` (line 206).
5. C2's declared metric is `structured_edit_mode` with `target: 1` (`preregister.json` claims list). One legal
   `replace_all` edit anywhere in the wave therefore drives the measured metric to **0** and the whole audit verdict to
   `CANNOT_EVALUATE`, with the only reported signal being a generic `SCOPE-SCHEMA` site (`<seat>:<index>`).

Impact on C1's `DECLARED_EDIT / ALLOW`: an exactly-declared target with a legal optional parameter is *not* clean
under the shipped adjudication, contradicting the decision the contract claims to validate.

Why the shipped selftest does not catch this: every v2 edit case in `selftest()` (candidate lines ~318–345) uses the
invented `stream_content` key (`v2-stream-edit`, `v2-read-only-target`, `v2-write-only-target`, `v2-undeclared-target`,
all `v2-spelling-*`, `v2-url-target`, `v2-nested-edit`, `v2-nested-denied`, `v2-write-target`, …). **No case exercises the
native replace shape with `replace_all`.** The shape set and its tests are mutually consistent but disconnected from the
real tool signature — which is exactly why the L1 mutation work (which mutates the shape set) never noticed the drift.

Smallest in-scope remedy (two one-line edits, no existing selftest expectation changes):

- `candidate/tools/check-seat-bindings.py:116` →
  `EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'}, {'path', 'old_string', 'new_string', 'replace_all'})`
- `candidate/collect.py:49` → add `'replace_all'` to `known`.
- Add one selftest case: `v2case('v2-replace-all-edit', 'edit', {'i': None, 'path': target, 'old_string': None, 'new_string': None, 'replace_all': True}, 0)`.
  Expected today (by construction): exit 2 with `SCOPE-SCHEMA`; expected after the fix: exit 0 with no findings.

I re-checked the proposed shape set against every existing v2 case: `v2-unknown-key`
(`{path,stream_content,__unknown_argument__}`), `v2-mixed-shapes` (`{path,stream_content,old_string,new_string}`),
`v2-half-replace` (`{path,old_string}`) and `v2-missing-path` (`{stream_content}`) remain non-members, so all four
still adjudicate to `SCOPE-SCHEMA`. No existing expectation moves, and the eight C1 decision rows are untouched.

### F2 — MEDIUM: the shape test grants "clean" to edit call shapes the substrate cannot execute (`stream_content`;
missing `i`; missing required replace keys)

`EDIT_SHAPES` member `{'path','stream_content'}` (line 116) is not a parameter set of any harness tool, and
`set(args) - {'i'}` (line 121) makes the mandatory intent key `i` optional, while the two required replace keys
`old_string`/`new_string` may both be absent. Consequences, all in the false-clean direction:

- `{'path': <declared target>, 'stream_content': <body>}` → `classify_edit` returns `[]` (no finding) although the native
  `edit` tool cannot accept that call (it requires `old_string` and `new_string`). `structured_edit_mode` can therefore
  reach 1 on the strength of a shape that could not have executed.
- `{'path': <declared target>, 'old_string': ..., 'new_string': ...}` with **no** `i` → also clean, although `i` is a
  required parameter of every tool in this substrate.

No out-of-scope *effect* follows (an unexecutable call has no effect), so this is a calibration defect on the C2 metric
rather than an escape. It matters because C2's metric is read as evidence that a real structured-edit authority was
exercised. Smallest remedy: require `'i' in args` and require exactly one of `('old_string','new_string')` /
`('stream_content')` to be present, i.e. replace the bare set-equality with a schema-derived predicate; drop
`stream_content` if no adapter in the observed corpus actually emits it (the wave's own `sources/structured-edit-observations.json`
is the file that decides this, and it is outside this seat's declared read paths).

### F3 — MEDIUM: a request-level schema verdict is a *global* all-or-nothing switch on C2's metric

Line 194 escalates to `code = 2` on the presence of **any** `SCOPE-SCHEMA` finding anywhere in any seat, and lines
199/206 then publish `request_audit_mode = 0` and `structured_edit_mode = 0` for the entire wave. One unrecognized
request shape in one seat therefore makes C2 *unmeasurable* rather than *failed*, and the published finding list shows a
generic `SCOPE-SCHEMA` site with no indication whether the offending request was in-scope, legal, or hostile. Combined
with F1 this is the mechanism by which C2's `structured_edit_mode` can collapse to 0 on legal traffic.

Smallest remedy (v1-preserving): keep the existing v1 semantics untouched, but compute the v2 metric from the *edit*
requests rather than from the global exit code, e.g. `structured_edit_mode = int(no SCOPE-SCHEMA finding was raised for an
`edit` request)`, and add a separate published counter (e.g. `schema_requests`) so a malformed request is visible as a
request-level datum instead of silently zeroing the claim metric.

### F4 — LOW (latent, not present in the landed manifest): no cross-seat exclusivity check on `edit_paths` / `write_paths`

The v2 manifest validation (candidate lines ~150–157) checks each seat in isolation: `edit_paths` must be a duplicate-free
list of `local()` paths that are also in that seat's `read_paths` and `write_paths`. Nothing forbids seat A's
`edit_paths` from containing seat B's report, or two seats from declaring the same edit target. Both would adjudicate as
*clean* for both seats, defeating "every seat writes its report only" at the authority layer.

I checked the landed `build/bindings.json` for this: every seat's `edit_paths` are its own report plus its own
worktree draft (e.g. seat `ExecEditAudit` → `build/ExecEditAudit.md` and
`worktrees/ExecEditAudit/draft/check-seat-bindings.py`, bindings.json lines 49–52), and no path is claimed by two seats.
So this is a **latent authority gap in the checker, not a present violation in the landed manifest**. Smallest remedy: one
manifest-level pass asserting that no path appears in more than one seat's `write_paths ∪ edit_paths` (unless the seat set
is intentionally shared).

### F5 — INFORMATIONAL / positive: the "exact declared target" boundary holds; the removed `local()` check really is redundant

The bounded search for a *clean spelling that is outside the exact declared target* found **none**, and the mechanism is
structural rather than accidental:

- Cleanliness requires, in order: dict args; `set(args) - {'i'}` ∈ `EDIT_SHAPES`; `path` a non-empty string; the path not
  matching either fetch regex (lines 126–127); and `value in binding['edit_paths']` (line 128). The last test is exact
  string membership in a list whose every entry passed `local()` at manifest-validation time.
- `local()` (lines 34–38) enforces LANE-absolute prefix, no backslash, no control characters, no `*?[];:` glob
  characters, and no empty / `.` / `..` path component. The manifest validator additionally requires every `edit_paths`
  entry to be in that seat's `read_paths` **and** `write_paths` (so `READ_ONLY_EDIT / DENY` and
  `WRITE_ONLY_EDIT / DENY` are enforced at declaration time), and forbids `skill://godspeed` in `edit_paths`.
- Therefore the `local()` check that the L1 mutation log records as removed
  (`l1-mutation.json` → `survivors_fixed_before_record[2]`: "seat-bindings classify_edit local(): redundant with validated
  local edit_paths, removed") is genuinely implied by the membership test. I concur with that removal.

Spelling classes enumerated and their adjudicated outcome (each also asserted by the shipped selftest, candidate lines
~322–330, so these are the author's own intended answers):

| class | example | adjudicated | basis |
|---|---|---|---|
| trailing separator | `<target>/` | `SCOPE-EDIT-DENIED` | not an exact member |
| dot segment | `<lane>/drafts/./A.md` | `SCOPE-EDIT-DENIED` | not an exact member |
| dot-dot segment | `<lane>/x/../drafts/A.md` | `SCOPE-EDIT-DENIED` | not an exact member |
| double slash | `<lane>//drafts/A.md` | `SCOPE-EDIT-DENIED` | not an exact member |
| reader selector | `<target>:raw` | `SCOPE-EDIT-DENIED` | edit takes no selector; no stripping here |
| relative | `drafts/A.md` | `SCOPE-EDIT-DENIED` | not an exact member |
| internal URI | `xd://edit` | `SCOPE-EDIT-DENIED` | not an exact member |
| skill URI | `skill://godspeed` | `SCOPE-EDIT-DENIED` | forbidden in `edit_paths`; not a member |
| case change | `<TARGET>.MD` | `SCOPE-EDIT-DENIED` | not an exact member (conservative on case-insensitive filesystems) |
| http(s) | `https://example.invalid/A.md` | `SCOPE-FETCH-DENIED` | line 126 fetch regex |
| host:port | `localhost:9222/` | `SCOPE-FETCH-DENIED` | line 126 host:port regex |

The fetch detection cannot be evaded into a clean verdict either: any URL-ish spelling that escapes both regexes
(`ftp://x/`, `https:/x`, `http://` with one slash) still fails the exact membership test and is denied as
`SCOPE-EDIT-DENIED`. And no legitimate local target can be mis-flagged as FETCH, because `edit_paths` entries are
LANE-absolute (leading `/`), while the host:port regex `^[^/:\s]+:[0-9]+/` requires a non-`/` first character.

### F6 — INFORMATIONAL / calibration note: v2 edit authority never exceeds write authority

Because the manifest validator requires `edit_paths ⊆ read_paths ∩ write_paths`, every path a seat may *edit* it may also
*write* wholesale with the `write` tool (`write` is admitted at line 78 and checked against `write_paths` at lines 112–113).
So the observable difference between a granted structured edit and a plain write on the same path is nil; what C2's
`structured_edit_mode` measures is *adjudication of the edit tool's spelling*, not confinement of its effect. This is
consistent with the tool's own `SCOPE` string ("Recorded request spellings only; not runtime prevention …"), but it should
be stated plainly so that C2's metric is not read as an effect-confinement claim.

### C3 cross-check

`collect.py`'s `known` whitelist is shared between the request projection (line 49) and nothing in the path census:
`scope_path()` (lines 68–83) and `projected_path()` (lines 20–34) consume only the `path` value, and `projected_path`
returns a LANE-absolute path unchanged. The `replace_all` drift of F1 therefore has **no** effect on the C3
rough-versus-lane path census; it is confined to the C2 audit path. C3 is unaffected by anything found here.

---

## Residual risk and verification gaps

1. **Not executed.** This seat is NO-EXEC, so F1/F2/F3 are established by source construction and line citation, not by
   observed exit codes. The author should confirm F1 with one added selftest case (given verbatim above) and one
   `--selftest` run.
2. **The landed r23 trace was not inspected.** `.ufo/waves/round-23/build/events.json` is outside this seat's declared
   `read_paths`, so I could not check whether any recorded edit request in the landed wave actually carried
   `replace_all` (i.e. whether F1 is already live for this wave's C2 number) or only `stream_content`/replace shapes.
   This is the single most decision-relevant unknown: if the landed events contain a `replace_all` key, C2's measured
   `structured_edit_mode` for round 23 is already 0 by construction; if not, it is a latent defect that fires on the
   first seat that uses the native replace-all form.
3. **Corpus provenance of `stream_content` not verified.** The wave's `sources/structured-edit-observations.json`
   (preregister source S086, "observed structured edit request keys and recorded adapter steps") is outside this seat's
   declared read paths. Whether `stream_content` is an observed real key from another adapter, or an invented
   placeholder, decides whether F2's first bullet is a real false-clean or merely an inert shape. Recommendation: derive
   `EDIT_SHAPES` from the union of (recorded observed keys) ∪ (native tool schema), not from either alone.
4. **Native `multi_tool_use.parallel` schema unverified.** The recorder rejects a parallel request carrying any key
   beyond `tool_uses` (`collect.py:44` adds `__unknown_argument__`; the auditor's `set(args) != {'tool_uses'}` test then
   yields `SCOPE-SCHEMA`). If the substrate's parallel tool exposes additional optional parameters, the same F3
   escalation applies to parallel requests. I could not verify the parallel tool's schema from this seat's inventory;
   flagged as unverified, not asserted.
5. **Out of declared scope and not claimed:** runtime prevention, symlink/hardlink effect proof, file-content reading
   proof, recorder completeness, and any native per-seat restrictive toolset. This report claims nothing about runtime
   enforcement, and the tool's own `SCOPE` string is honest on this point.
6. **Not verified:** whether the landed `bindings.json` was regenerated from the recorder after any of the above; the
   manifest was read and found internally consistent with the v2 validator (every `edit_paths` entry is `local()` and
   present in that seat's `read_paths` and `write_paths`).

## Summary judgement

The *target* boundary that C2 claims — "exact predeclared structured edit targets" — is **sound**: no spelling of a path
outside a seat's declared `edit_paths` adjudicates as clean, in either the path dimension (F5) or the URL/host:port
dimension, and the removed `local()` check was genuinely redundant. The defect is in the **request-shape dimension**:
`EDIT_SHAPES` is not derived from the native edit tool's schema, so the shipped adjudicator mis-handles the legal
`replace_all` form (F1, major), grants "clean" to non-executable shapes (F2, medium), and turns a single request-level
schema verdict into a global zero of C2's published metric (F3, medium). Remedy is two one-line key-set additions plus
one selftest case, with no existing expectation and no C1 decision row disturbed.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2classifyedit
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
