# FxC2OraclePrefix — falsification of the v2 structured-edit audit on declared-path suffix expansion

Seat: `TsukuroiR23-2.FxC2OraclePrefix-2` (falsify, leaf, no dispatch)
Round: tsukuroi round23 attempt1, FALSIFY wave
Artifact under attack: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`
The artifact's identity digest is supplied by the assignment and was **not** independently computed (NO-EXEC forbids hashing).
Mode: **NO-EXEC / NO-FETCH.** No command was run, no file was hashed, listed, counted, imported or executed. Every statement below is a hand derivation from the landed source text quoted by line anchor, plus the declared local files listed in the seat binding. `Scope: executed=none` is literal: the auditor did not execute the artifact it audits.

---

## 1. Attacked claim

**C2 — "New explicit schema-v2 audit authority for exact predeclared structured edit targets"** (preregister claim `C2`, axis `operability`, metric `structured_edit_mode`, before `0` → target `1`), read through the adjacent **C1** decision it implements:

> `EDIT_TRAVERSAL / DENY / "No dot-segment or alternate spelling expands the target list"` (preregister `edit_decisions[5]`)

The concrete falsifier attempted: **does a recorded request whose path is a *declared* target plus a suffix (`.extra` extension, `/child` child-segment) get accepted as if it were the declared target?** i.e. does the v2 edit target list silently expand under alternate spelling, in either the `edit` (structured) branch or the `read`/`write` branch?

Secondary claim probed under the same artifact: whether the v2 audit's own observable contract (`structured_edit_mode`, exit code, finding IDs) is honest for such a request, and whether the landed selftest pins it.

---

## 2. Hand derivation of the exact audit outcome

### 2.1 The v2 dispatch path

* `classify()` strips a `functions.` prefix, denies `bash|eval|task` as `SCOPE-EXEC-DENIED` and `web_search|browser*` as `SCOPE-FETCH-DENIED` **before** any tool dispatch (source lines 70–75).
* Line 76–77: `if tool == 'edit' and allow_structured_edit: return classify_edit(args, binding)`.
* `allow_structured_edit` is **not** a request-, row- or event-level input: it is passed from `evaluate()` at line 186 as `allow_structured_edit=v2`, where `v2` is computed once at line 144 from the *top-level manifest schema string* (`data.get('schema') == 'tsukuroi-seat-bindings-v2'`). Docstring lines 64–65 state this explicitly. So a v2 audit routes every `edit` request to `classify_edit`; a v1 audit cannot reach it (see 2.6).

### 2.2 `classify_edit` (source lines 119–130), verbatim logic

```
119 def classify_edit(args, binding):
120     """v2 structured edit: exact declared target, finite observed key shapes; bodies stay opaque."""
121     if not isinstance(args, dict) or set(args) - {'i'} not in EDIT_SHAPES:
122         raise ValueError('unstructured or unknown edit arguments')
123     value = args.get('path')
124     if not isinstance(value, str) or not value:
125         raise ValueError('missing explicit edit target')
126     if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
127         return ['SCOPE-FETCH-DENIED']
128     if value not in binding['edit_paths']:
129         return ['SCOPE-EDIT-DENIED']
130     return []
```

`EDIT_SHAPES = ({'path','stream_content'}, {'path','old_string','new_string'})` (line 116).

**Decisive structural fact:** `classify_edit` applies **no path normalization whatsoever** — no `local()`, no `requested_path()`, no selector stripping, no `os.path` normalization, no case folding, no prefix/suffix expansion. Line 128 is a plain **exact string membership test** against `binding['edit_paths']` (a Python list → exact `str` equality). The only gates before it are the *argument shape* (line 121) and a *URL* test (lines 126–127).

Therefore, for `value = declared_target + suffix`:

* line 121 passes iff the observed key shape is one of the two recorded shapes (optionally plus `i`);
* line 123–125 pass (`suffix` keeps it a non-empty `str`);
* line 126–127 cannot fire: the declared targets are absolute paths starting with `/` (`local()` requires `path.startswith(LANE + '/')`, lines 33–36, and every `edit_paths` entry must pass `local()` — see line 160), so `^https?://` cannot match, and the second regex `^[^/:\s]+:[0-9]+/` cannot match a string whose first character is `/`;
* **line 128 fails** → `['SCOPE-EDIT-DENIED']`.

The suffix is never "absorbed" into the target: the exact-match test cannot match a longer string.

### 2.3 Exact outcome for the attacked request (v2 manifest, one complete seat, one event)

| requested `path` | tool | finding ID | site string | exit code | `status` | `request_audit_mode` | `structured_edit_mode` | `violations` |
|---|---|---|---|---|---|---|---|---|
| `declared + '.extra'` | `edit` | `SCOPE-EDIT-DENIED` | `<seat>:<event-index>` | **1** | `FAIL` | 1 | **1** | 1 |
| `declared + '/child'` | `edit` | `SCOPE-EDIT-DENIED` | `<seat>:<event-index>` | **1** | `FAIL` | 1 | **1** | 1 |
| `declared + '.extra'` | `read` | `SCOPE-PATH-DENIED` | `<seat>:<event-index>` | **1** | `FAIL` | 1 | **1** | 1 |
| `declared + '/child'` | `read` | `SCOPE-PATH-DENIED` | `<seat>:<event-index>` | **1** | `FAIL` | 1 | **1** | 1 |
| `declared + '.extra'` | `write` | `SCOPE-PATH-DENIED` | `<seat>:<event-index>` | **1** | `FAIL` | 1 | **1** | 1 |
| `declared + '/child'` | `write` | `SCOPE-PATH-DENIED` | `<seat>:<event-index>` | **1** | `FAIL` | 1 | **1** | 1 |

Derivation of the aggregate fields:

* **Finding ID.** For `edit`: `SCOPE-EDIT-DENIED` (line 129). For `read`/`write`: the request goes through `requested_path()` (lines 43–57) → `local()` (lines 33–36) → membership against `read_paths`/`write_paths` (lines 110–112) → `SCOPE-PATH-DENIED`.
* **`.extra` is *not* rejected by `local()`** — `local()` forbids `*?[];:` and the path components `''`, `'.'`, `'..'`, but `'A.md.extra'` is one ordinary component, so `local()` returns **True** for `.extra` and for `/child` (components `'A.md'`, `'child'`). The denial for both suffixes therefore comes from the **exact membership test**, not from the shape filter. This is worth stating precisely: the suffix is denied for the *right* reason (not in the declared list), not incidentally.
* **Exit code.** Line 194: `code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)`. A single `SCOPE-EDIT-DENIED` / `SCOPE-PATH-DENIED` is not `SCOPE-SCHEMA`, the seat trace is present and `complete`, so `code = 1`.
* **`structured_edit_mode`.** Line 205–206: `if v2: result['structured_edit_mode'] = int(code != 2)`. With `code = 1` → **`structured_edit_mode = 1`**. (It is emitted only for a v2 manifest; a v1 manifest has **no** `structured_edit_mode` key at all.)
* **`violations`.** Line 191 counts only ids `!= 'SCOPE-SCHEMA'`, so the denial counts as **1** violation.
* **Site string.** `add(fid, f'{name}:{index}')` (line 190) → e.g. `OracleV2Prefix:0` — seat name plus the event's 0-based index inside that seat's `events` list.

### 2.4 The suffix is *never* accepted — the core falsification result

Across all three admitted tools, `declared + '.extra'` and `declared + '/child'` are **denied** in a v2 audit, with the IDs and exit code in the table above. **No expansion of the declared target list occurs.** The C1 decision `EDIT_TRAVERSAL / DENY` is honored by the landed code for these two suffix families, and C2's "exact predeclared structured edit targets" wording matches the implementation (exact string equality at line 128).

### 2.5 Where the suffix *is* normalized away (contrast, not a defect)

`requested_path()` (lines 43–57) strips a *valid* selector suffix for `read`/`grep` only (`selector=tool in ('read','grep')`, line 108): `base, *tokens = value.split(':')` and `value = base` when every token matches `raw|img|conflicts|\d+(?:[-+]\d*)?|-\d+`. So a `read` of `declared + ':1-5'` is admitted as the declared path. This is *not* target expansion — it is the documented read-selector feature, and it does not apply to `edit`, where `declared + ':raw'` is denied (landed selftest line 307 covers that spelling). The asymmetry (read selectors admitted, edit selectors denied) is deliberate and is asserted by the landed selftest.

### 2.6 v1 continuity (unchanged legacy policy)

In a v1 manifest `v2` is `False` (line 144), so line 76 does not fire, `'edit'` is not in the admitted tool tuple (line 78), and the same suffixed request yields **`SCOPE-TOOL-UNKNOWN`**, exit **1**, with **no** `structured_edit_mode` key. Legacy v1 policy is untouched — consistent with C2's "legacy schema-v1 policy and historical reds unchanged".

---

## 3. Does the landed selftest contain an equivalent control?

The landed selftest (`selftest()`, lines 210–353) contains, **for the `read`/`write` branch**, literal suffix fixtures:

* line 229–230 (read): `src + '-extra'`, `src + '/child'` → expect exit 1 / `SCOPE-PATH-DENIED`;
* line 231–232 (write): `report + '.extra'`, `report + '/child'` → expect exit 1 / `SCOPE-PATH-DENIED`.

For the **v2 `edit` branch** it contains **no literal `.extra` or `/child` fixture**. It contains the *equivalent* control:

* line 307–308: `for spelling in (target + '/', LANE + '/drafts/./A.md', LANE + '/x/../drafts/A.md', LANE + '//drafts/A.md', target + ':raw', 'drafts/A.md', 'skill://godspeed', 'xd://edit', target.upper()): v2case('v2-spelling-' + spelling, 'edit', {'path': spelling, 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')`.

**Assessment: the coverage is behaviourally equivalent, but not literal.** Because `classify_edit` performs *no* normalization, `target + '/'`, `target + '/child'` and `target + '.extra'` all traverse the identical code path (lines 121–129) and must produce the identical triple (`SCOPE-EDIT-DENIED`, exit 1, `structured_edit_mode` 1). The landed fixture at line 307 therefore *does* pin the outcome for the suffix attack, by equivalence — it just does not name the two suffix spellings literally. A future refactor that added normalization to `classify_edit` would be caught by the existing `target + '/'` and `target + ':raw'` fixtures for the trailing-slash and selector families, but **not** by any fixture for the `.extra` (extension) or `/child` (child-segment) families, which are the two families most likely to be produced by a real path-manipulating agent.

**Literal fixture the landed selftest lacks** (smallest form, to be appended next to line 307, using the existing `target`/`v2`/`v2case` bindings already in scope):

```python
    v2case('v2-suffix-extra', 'edit', {'path': target + '.extra', 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
    v2case('v2-suffix-child', 'edit', {'path': target + '/child', 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
```

and, for the read/write branch symmetry that the `edit` fixtures currently lack (`.extra` on `read` is only covered as `-extra` at line 229):

```python
    case('path-' + src + '.extra', 'read', {'path': src + '.extra'}, 1, 'SCOPE-PATH-DENIED')
```

These three lines are the complete remedy for the coverage gap; no production logic change is implied by the suffix attack itself.

---

## 4. Findings by severity

### F1 (Medium) — the v2 `edit` shape set is a closed list that omits a parameter the `edit` tool itself advertises, and the omission is **run-fatal** rather than request-scoped

`EDIT_SHAPES` (line 116) is `({'path','stream_content'}, {'path','old_string','new_string'})`. The shape test at line 121 is `set(args) - {'i'} not in EDIT_SHAPES` — a **closed** set (note the operator precedence: `set(args) - {'i'}` binds first, then `not in`; so only the optional `i` key is stripped). Any recorded `edit` request carrying a key outside those two shapes raises `ValueError`, is caught at lines 186–188 and becomes `SCOPE-SCHEMA`.

`SCOPE-SCHEMA` is **not** a scoped denial: line 194 makes **one** schema finding anywhere in the run promote the **entire** audit to `code = 2`, and lines 205–206 then set `structured_edit_mode = int(code != 2)` → **`0`** for the whole run.

Concretely: the `edit` tool advertised in this session's own tool contract carries `replace_all` (alongside `i`, `path`, `old_string`, `new_string`). A recorded edit request that used `replace_all: true` — an ordinary, documented way to rename every occurrence — yields `set(args) - {'i'} == {'path','old_string','new_string','replace_all'}`, which is **not** in `EDIT_SHAPES`, hence `SCOPE-SCHEMA`, hence exit **2** / `status = CANNOT_EVALUATE` / **`structured_edit_mode = 0`** for the entire r23 fleet audit. That directly contradicts C2's metric target (`structured_edit_mode` → 1) for reasons that have nothing to do with any seat's scope compliance, and it would also erase the distinction between "no seat misbehaved" and "the audit could not classify one request shape".

Note the asymmetry that makes this sharp: `SCOPE-SCHEMA` from a *request* (line 106, `unknown_keys`, for read/grep/glob/write) is also promoted to run-level exit 2 — so the closed-set discipline is already run-fatal in the pre-existing v1 path as well; the v2 edit branch merely inherits that blast radius.

*Verification status:* the shape set and the run-fatal promotion are read directly from the landed source (lines 116, 121, 186–194, 205–206). Whether any r23 seat actually emitted such a request is **not verifiable from this seat** (see §5).

### F2 (Low) — `structured_edit_mode` measures *mode*, not *compliance*; a FAIL run still reports 1

Lines 205–206: `structured_edit_mode = int(code != 2)`. A run with violations but no schema error therefore reports `structured_edit_mode = 1` together with `status = 'FAIL'` and `violations > 0`. If C2's metric is reported as "`structured_edit_mode = 1`" without the accompanying `status`/`violations`, the number is honest but **readable as false assurance**. The landed `SCOPE` string (line 18) does not mention this: *"Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."* It states what the audit does **not** prove, but not that the metric is an *enablement* flag rather than a *compliance* count.

### F3 (Info) — coverage: no literal `.extra` / `/child` fixture for the v2 `edit` branch

See §3. Behaviourally equivalent coverage exists (`target + '/'`, line 307); the literal families are absent. Remedy given as three fixture lines.

### F4 (Info) — the attack itself is **not** falsifiable on the landed source

`declared + '.extra'` and `declared + '/child'` are denied in every admitted branch of a v2 audit, with the exact IDs/exit/mode in §2.3. The v2 edit target list does **not** expand under these alternate spellings. The C1 `EDIT_TRAVERSAL` decision and C2's "exact predeclared" wording are consistent with the landed implementation.

---

## 5. Residual risk and verification gaps (bounded, honest)

1. **F1 impact is unmeasured.** The seat binding allows reading only `candidate/tools/check-seat-bindings.py`, `preregister.json`, `sources/godspeed-directive.txt`, `skill://godspeed`, this report, and `build/bindings.json`. The recorded request key shapes live in `.ufo/waves/round-23/sources/structured-edit-observations.json` and the r23 request stream (`build/events.json`), neither of which is in this seat's read paths. **I therefore cannot confirm whether any recorded r23 `edit` request carries a key outside `EDIT_SHAPES`.** F1 is stated as a *latent* run-fatal defect, not as an observed failure.
2. **Candidate vs snapshot divergence unchecked.** The audit executed by the fleet runs the committed `snapshot/tools/check-seat-bindings.py` (as referenced by the seat bindings in `build/bindings.json`), while this seat reviewed `candidate/tools/check-seat-bindings.py`. The two were not diffed — the snapshot copy is outside this seat's declared read paths. If the candidate and the committed snapshot differ, the derivation in §2 applies to the candidate only.
3. **Post-hoc, not preventive.** Consistent with the artifact's own `SCOPE` string and the round's `limits` ("No native per-seat restrictive tool interface exists", "No runtime prevention, effect/reading/recorder-completeness or universal tool/patch semantics"), nothing here shows that a suffixed request would be *refused* at request time — only how the recorded spelling is *classified*. No runtime-enforcement claim is made or implied.
4. **Selector asymmetry is intentional but untested in v2 form.** `read` strips a valid `:selector` (lines 49–54); `edit` does not. The landed selftest pins `read` selector admission ('selector', line 220) and `edit` selector denial (line 307, `target + ':raw'`), so this is covered — but only for `read`/`grep` in v1 form; no v2-manifest read-selector case exists (v2 fixtures use the same `trace()` helper with a v2 manifest, and `v2-read-still-scoped` covers a *denied* read, not a selector-admitted read). Low impact: the read path is byte-identical between v1 and v2.
5. **Bounded search actually performed** (all read-only): (a) full read of the artifact's 396 lines across four ranged reads plus targeted raw reads of lines 66–82, 110–135, 133–155, 194–208; (b) literal grep over the artifact for `extra|child|production`, `replace_all|stream_content|EDIT_SHAPES|edit_paths|SCOPE-EDIT-DENIED|structured_edit_mode`, and `allow_structured_edit|v2 = isinstance|classify(event`; (c) structural read of `build/bindings.json` (v2 schema; every seat's `edit_paths` ⊆ `read_paths` ∩ `write_paths`, enforced at source line 160 — e.g. `OracleV2Prefix` at bindings lines ~798–812); (d) reading of `preregister.json` claims C1/C2/C3 and the eight `edit_decisions`. **No command, import, hash, or execution was performed** — the search was textual over declared files only.

---

## 6. Smallest in-scope remedy

**Primary (coverage only, no production logic change — 3 lines in the landed selftest):** add the three fixtures given in §3 (two v2 `edit` suffix cases, one v2-manifest read `.extra` case).

**Secondary (only if F1 is confirmed by a seat holding the observation source):** extend `EDIT_SHAPES` to include the observed shape(s) actually emitted by the `edit` adapter — e.g. `{'path','old_string','new_string','replace_all'}` — and add the matching selftest fixture; **or**, if the closed set is intended to stay closed, state the consequence inside the artifact's `SCOPE` string, so that a `SCOPE-SCHEMA` promotion to `CANNOT_EVALUATE` (and `structured_edit_mode = 0`) is read as "shape not covered", not as "audit passed / audit failed". Both are one-line changes; the second is preferable if the observation source cannot be re-read.

**Not recommended:** any change that relaxes the exact-match test at line 128, weakens the `EDIT_TRAVERSAL` denial, or adds prefix/suffix normalization to `classify_edit` — the exact-match test is precisely what makes the suffix attack non-falsifiable against this artifact.

**Verdict:** the suffix attack **fails to falsify** C2/C1 on the landed source — `declared + '.extra'` and `declared + '/child'` are denied in every branch of a v2 audit with finding IDs `SCOPE-EDIT-DENIED` (edit) / `SCOPE-PATH-DENIED` (read, write), exit code **1**, `status = FAIL`, `request_audit_mode = 1`, and **`structured_edit_mode = 1`**. The residual defects are F1 (closed edit shape set that is run-fatal and omits the tool-advertised `replace_all` key — impact unmeasured) and F2 (`structured_edit_mode` is an enablement flag, not a compliance count). F3's remedy is the three literal selftest fixtures above.
