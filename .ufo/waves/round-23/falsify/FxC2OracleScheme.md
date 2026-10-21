# FxC2OracleScheme — C2 v2 edit audit authority vs. URI/scheme edit targets

## Attack target

- Claim attacked: **C2** (axis *operability*, metric `structured_edit_mode`, before 0 → target 1), i.e. "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged."
- Underlying C1 decision exercised: **EDIT_EXTERNAL — DENY**, "Remote or internal URIs do not become filesystem edit targets" (`.ufo/waves/round-23/preregister.json`, `edit_decisions[6]`).
- Source under attack: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py` (declared SHA256 `4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6`, supplied identity — **not** recomputed here).
- Method: hand-derivation from the landed source text only. NO-EXEC / NO-FETCH: no command was run, nothing was imported, no hash/list/wc was computed, no network or browser access, no subagent dispatch. Only the declared local files were read.

## 1. Hand-derivation of the v2 audit outcome for four edit targets

### 1.1 The code path that a v2 `edit` request takes

- `evaluate()` sets `v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'` (line ~140) and calls `classify(event.get('tool'), event.get('args'), binding, allow_structured_edit=v2)` (line ~186). `allow_structured_edit` is set **only** from the validated top-level manifest schema, never from a row field or event marker (guard case `v2-row-marker`).
- `classify()` strips a `functions.` prefix, rejects `bash`/`eval`/`task` (`SCOPE-EXEC-DENIED`) and `web_search`/`browser*` (`SCOPE-FETCH-DENIED`), and then — **before** the generic tool allow-list — dispatches `tool == 'edit'` with `allow_structured_edit=True` to `classify_edit()` (lines ~73–80).
- `classify_edit()` (lines 120–130), verbatim shape:

```python
def classify_edit(args, binding):
    if not isinstance(args, dict) or set(args) - {'i'} not in EDIT_SHAPES:
        raise ValueError('unstructured or unknown edit arguments')
    value = args.get('path')
    if not isinstance(value, str) or not value:
        raise ValueError('missing explicit edit target')
    if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
        return ['SCOPE-FETCH-DENIED']
    if value not in binding['edit_paths']:
        return ['SCOPE-EDIT-DENIED']
    return []
```

with `EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})`.

- Manifest-side v2 authority (lines ~155–160): every `edit_paths` entry must satisfy `local(p)` **and** be present in that seat's `read_paths` **and** `write_paths`; `local()` requires the string to start with `LANE + '/'` and to contain no `* ? [ ] ; :`, no `\`, no control characters, and no empty/`.`/`..` path segment. Consequently **no URI of any scheme can ever appear in a valid v2 `edit_paths`**: `local('skill://godspeed')`, `local('xd://edit')`, `local('artifact://a')` are all False. (Selftest case `v2-edit-paths-skill` pins the manifest-level rejection.)

### 1.2 Per-spelling derivation (well-formed structured edit: `{'path': <spelling>, 'stream_content': ...}` or `{'path': <spelling>, 'old_string': ..., 'new_string': ...}`)

| # | edit target spelling | branch taken in `classify_edit` | finding ID | exit code | `structured_edit_mode` |
|---|---|---|---|---|---|
| 1 | `skill://godspeed` | shape OK; not `^https?://`; `^[^/:\s]+:[0-9]+/` fails (`skill` + `:` + `//godspeed` — no digits); not in `edit_paths` | `SCOPE-EDIT-DENIED` | **1** | **1** |
| 2 | `xd://edit` | same as #1 (`xd` + `:` + `//edit`) | `SCOPE-EDIT-DENIED` | **1** | **1** |
| 3 | `artifact://a` | same as #1 (`artifact` + `:` + `//a`) | `SCOPE-EDIT-DENIED` | **1** | **1** |
| 4 | `https://example.invalid/A.md` | `(?i)^https?://` matches → returns before the `edit_paths` membership test | `SCOPE-FETCH-DENIED` | **1** | **1** |

Exit-code derivation: `evaluate()` accumulates one finding per returned ID, `violations += sum(fid != 'SCOPE-SCHEMA' …)`, and finally

```python
code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)
```

None of the four spellings raises inside `classify_edit` (all four pass the shape and "path present" checks), so no `SCOPE-SCHEMA` is produced; with a present, complete seat the code is therefore `1` (`status: "FAIL"`, `request_audit_mode: 1`). `structured_edit_mode` is emitted only when `v2` is true and is `int(code != 2)` → **1** for each of the four.

### 1.3 Combined audit (all four events in one seat)

- exit code **1**; `status` `FAIL`; `request_audit_mode` **1**; `structured_edit_mode` **1**; `requests_total` 4; `violations` 4.
- `findings` (site = `A:<event index>`): `SCOPE-EDIT-DENIED` (skill://), `SCOPE-EDIT-DENIED` (xd://), `SCOPE-EDIT-DENIED` (artifact://), `SCOPE-FETCH-DENIED` (https://) — in event order.
- No spelling reaches exit `0` (none can be an authorized target) and none reaches exit `2` under a well-formed structured edit.

### 1.4 The only exit-2 routes (spelling-independent)

1. **Malformed edit shape.** If the recorded event args are not one of the two `EDIT_SHAPES` (e.g. `{'path': 'artifact://a'}` alone, or `{'path':…, 'stream_content':…, 'old_string':…, 'new_string':…}`), `classify_edit` raises `ValueError`, which `evaluate()` maps to `SCOPE-SCHEMA` → exit **2**, `status CANNOT_EVALUATE`, `request_audit_mode 0`, `structured_edit_mode` **0**. This holds identically for all four spellings: the denial ID is never observed when the shape is malformed. (Selftest pins this for other shapes: `v2-opaque-patch`, `v2-mixed-shapes`, `v2-half-replace`, `v2-missing-path`.)
2. **Manifest-level URI grant.** Attempting to grant edit authority over a URI (`edit_paths: ["skill://godspeed"]`, `["xd://edit"]`, `["artifact://a"]`) fails v2 manifest validation → `ValueError('v2 edit authority')` → outer `except` → `SCOPE-SCHEMA` at site `input` → exit **2**, `structured_edit_mode` **0**, `requests_total` 0, `seats_bound` = number of seats validated before the failing one (the `bound` dict is mutated in place). One malformed seat therefore collapses the whole multi-seat audit.

## 2. Does the landed selftest contain an equivalent control?

| spelling | landed selftest control | verdict |
|---|---|---|
| `skill://godspeed` (edit, v2) | line 307 spelling tuple → case `v2-spelling-skill://godspeed`, expected exit 1 / `SCOPE-EDIT-DENIED` | **present** |
| `xd://edit` (edit, v2) | line 307 spelling tuple → case `v2-spelling-xd://edit`, expected exit 1 / `SCOPE-EDIT-DENIED` | **present** |
| `https://example.invalid/A.md` (edit, v2) | line 309 → case `v2-url-target`, expected exit 1 / `SCOPE-FETCH-DENIED` | **present** |
| `artifact://a` (edit, v2) | — | **ABSENT** |

`artifact://` occurs exactly **once** in the whole landed checker, at line 229, inside the **v1 read** path list (`'xd://tool', 'artifact://a'` → expected `SCOPE-PATH-DENIED` for tool `read`). There is **no** v2 `edit` control for `artifact://`, and no control for the `artifact://` spelling under any other v2 shape. The v1 read control does not substitute: it exercises `requested_path()` (lines 43–57), which is a different function from `classify_edit()` (lines 120–130), with a different finding-ID vocabulary (`SCOPE-PATH-DENIED` vs `SCOPE-EDIT-DENIED`) and a different branch order (the read path special-cases `skill://godspeed` at line 48; the edit path has no such special case).

Secondary, lower-severity gaps in the same family (all *read*-only controls at line 225: `'https://example.invalid', 'HTTPS://EXAMPLE.INVALID/:1-5', 'http://127.0.0.1/', 'localhost:9222/'`):

- uppercase `HTTPS://…` as an **edit** target is unpinned (derivation: `(?i)` inline flag → `SCOPE-FETCH-DENIED`, exit 1);
- host:port form `localhost:9222/` as an **edit** target is unpinned (derivation: matches `^[^/:\s]+:[0-9]+/` → `SCOPE-FETCH-DENIED`, exit 1).

## 3. Concrete falsifier / bounded search

**Bounded search performed** (all by reading the landed source; nothing executed): for each of the four spellings I enumerated every branch of `classify_edit` reachable with (a) each of the two `EDIT_SHAPES`, (b) a malformed shape, (c) an attempt to grant the spelling through `edit_paths` in the manifest, and (d) the read-path contrast via `requested_path()`. Additionally I enumerated the exit-code/mode consequences in `evaluate()` for each of those states.

**Result of the search:**

- No spelling produces a false ALLOW. There is no spelling-dependent bypass: `classify_edit` compares the raw path string by exact equality against `edit_paths`, and every v2 `edit_paths` entry is a `local()` absolute path, so no URI, no dot-segment, no trailing-slash, no case-variant and no selector-suffixed spelling can ever equal a declared target. (Spelling-flip controls already present: `v2-spelling-…/`, `…/drafts/./A.md`, `…/x/../drafts/A.md`, `…//drafts/A.md`, `…:raw`, `drafts/A.md`, `target.upper()`.)
- The derived outcome for all four attacked spellings is **exit 1 + `SCOPE-EDIT-DENIED`×3 + `SCOPE-FETCH-DENIED`×1 + `structured_edit_mode` 1**, which is *consistent with* C1 `EDIT_EXTERNAL = DENY` and with C2's contract that v2 grants authority only to "exact predeclared structured edit targets".
- Therefore **C2 as stated is not falsified by the four spellings**; the only defect produced is a **control-coverage gap** (F1 below), not a behavioural defect.
- The concrete falsifier for C2, if one existed, would be a v2 trace in which one of these four spellings yields exit `0` (no finding) or exit `2` (CANNOT_EVALUATE with `structured_edit_mode` 0) while the args carry a well-formed `EDIT_SHAPES` body. Hand-derivation excludes both; no such state exists in the landed source.

## 4. Findings by severity

### F1 — MEDIUM (control-coverage): no landed v2 selftest control for an `artifact://` edit target
- Evidence: `candidate/tools/check-seat-bindings.py:229` is the only occurrence of `artifact://` in the file (v1 `read` path, expected `SCOPE-PATH-DENIED`); the v2 spelling tuple at `:307` covers `skill://godspeed` and `xd://edit` but not `artifact://`; the v2 URL case at `:309` covers only lowercase `https://`.
- Impact: the third internal-URI scheme is behaviourally denied (derivation §1.2, `SCOPE-EDIT-DENIED`, exit 1), but nothing in the selftest pins it. A future edit of the URI branch — e.g. widening the fetch rule to any `://` spelling — would flip `artifact://` from `SCOPE-EDIT-DENIED` to `SCOPE-FETCH-DENIED` with **no selftest red**, and would equally change the read-path ID vocabulary that the C3 path census keys on. C1's `EDIT_EXTERNAL` decision is therefore under-pinned for one of its three named scheme families.
- Not a false-PASS today: no landed behaviour contradicts the claim.

### F2 — LOW (taxonomy asymmetry between read and edit paths)
- Evidence: for the same "not a filesystem target" fact the read path emits `SCOPE-PATH-DENIED` (`requested_path`, line 57) while the edit path emits `SCOPE-EDIT-DENIED` (line 129); schemes that are neither `http(s)://` nor `host:port/` (`skill://`, `xd://`, `artifact://`, and also `file://`, `https:/x`, `skill://other`) land in the generic denial bucket, never in `SCOPE-FETCH-DENIED`.
- Impact: none on the verdict (all four are denials at exit 1), but any downstream ID-keyed count (C3 path census / report receipts) must not assume "URI denial ⇒ `SCOPE-FETCH-DENIED`". Note also that the read path has a `skill://godspeed` special case (line 48) that the edit path deliberately lacks — which is the correct asymmetry for C1 `EDIT_EXTERNAL`.

### F3 — LOW (metric granularity): `structured_edit_mode` is a whole-audit flag, not per-seat
- Evidence: `evaluate()` emits `result['structured_edit_mode'] = int(code != 2)` only when the manifest schema is v2; a single invalid v2 seat aborts the whole evaluation via the outer `except` (site `input`, `SCOPE-SCHEMA`) with `requests_total` 0 and `seats_bound` = seats validated before the failure.
- Impact: C2's metric `structured_edit_mode == 1` is observable only for a fully valid manifest **and** fully evaluable trace; a manifest defect reports `0` with partial `seats_bound`, so the metric alone cannot distinguish "authority evaluated and passing" from "authority not evaluated" without also reading `status`/`request_audit_mode`. The landed round-23 `build/bindings.json` is schema-v2 with 60+ seats whose `edit_paths` are all `local()` absolute paths (no URI grants), so the landed production state is unaffected.

### F4 — INFORMATIONAL (not a defect): v2 cannot express URI edit authority at all
- Confirms C1 `EDIT_EXTERNAL` at the manifest layer: `edit_paths ⊆ local()` means `skill://godspeed` — which every round-23 seat carries in `read_paths` — can never be an edit target, and attempting it yields a whole-manifest `SCOPE-SCHEMA` (exit 2) rather than a per-request denial. Already pinned by `v2-edit-paths-skill`.

## 5. Smallest in-scope remedy

One literal added to the existing v2 spelling tuple in the landed checker (production-file edit belongs to the L1 integrator; this seat writes only its report):

`candidate/tools/check-seat-bindings.py:307`

```python
    for spelling in (target + '/', LANE + '/drafts/./A.md', LANE + '/x/../drafts/A.md', LANE + '//drafts/A.md', target + ':raw', 'drafts/A.md', 'skill://godspeed', 'xd://edit', 'artifact://a', target.upper()):
        v2case('v2-spelling-' + spelling, 'edit', {'path': spelling, 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
```

i.e. insert the single literal `'artifact://a'` before `target.upper()`. Expected selftest effect: one new case `v2-spelling-artifact://a` with exit 1, ids `['SCOPE-EDIT-DENIED']`, `structured_edit_mode` 1 — matching the hand-derivation in §1.2, so the case passes on the landed behaviour and pins it.

Optional (same file, secondary — only if the maintainer wants the whole fetch-branch family pinned under `edit`; each is one added `v2case` line):

```python
    v2case('v2-url-uppercase-target', 'edit', {'path': 'HTTPS://EXAMPLE.INVALID/A.md', 'stream_content': None}, 1, 'SCOPE-FETCH-DENIED')
    v2case('v2-hostport-target', 'edit', {'path': 'localhost:9222/', 'stream_content': None}, 1, 'SCOPE-FETCH-DENIED')
```

No change to `classify_edit`, `evaluate`, the schema strings, the finding-ID vocabulary or the exit-code ladder is required or recommended.

## 6. Residual risk and verification gaps

- **Audit-input vs. attacked-file identity.** The C2 command (`check-seat-bindings.py --revision <REV> --manifest … --events …`) executes the checker *committed at the revision* and reads the manifest/events *from that committed tree* (`git_read(binding.sha, …)`), not from the `.ufo/waves/round-23/candidate/` copy I attacked. I verified the candidate copy only; I could not diff it against the committed blob at `5a25c88b77f52e940bcad87825c4ac1cd529470d` because NO-EXEC forbids `git show`/`git cat-file`. The declared digest is a supplied identity and was not recomputed. **If the committed blob differs from the candidate copy, §1–§3 do not transfer to the audit.**
- **Events not observed.** `.ufo/waves/round-23/build/events.json` is not in this seat's declared `read_paths`, so I did not open it; the round-23 production event stream was not inspected. The C2 metric `structured_edit_mode == 1` for the production wave is therefore **unverified by this seat** (only the derivable behaviour is).
- **Spelling coverage is finite, not exhaustive.** The derivation covers exactly the four requested spellings plus the malformed-shape and manifest-grant variants. Other URI spellings (`file://`, `data:`, `proc://`, `agent://`, `mcp://`, `omp://`, `local://`, `history://`, `ssh://`) were not individually enumerated; by the same branch analysis they all take the `SCOPE-EDIT-DENIED` route (none match `^https?://`; none match `^[^/:\s]+:[0-9]+/` because the `//` after the colon is not digits), but no selftest control exists for them either.
- **Scope of the audit itself.** As the tool's own `SCOPE` string states, this is "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness." No claim of runtime enforcement is made or supported here; Main confirms no native per-seat restrictive toolset exists.
- **No historical rewrite.** The remedy in §5 is forward-looking (add a control); it does not re-authorize any r22 manifest, event or report, and no round24 is proposed.

## 7. Verdict on C2

C2 is **not falsified** by the four attacked edit-target spellings: a v2 audit of `skill://godspeed`, `xd://edit`, `artifact://a` and `https://…/A.md` yields exit code **1** with finding IDs `SCOPE-EDIT-DENIED`, `SCOPE-EDIT-DENIED`, `SCOPE-EDIT-DENIED`, `SCOPE-FETCH-DENIED` and `structured_edit_mode` **1** (well-formed `EDIT_SHAPES` bodies), matching C1 `EDIT_EXTERNAL = DENY`. The single actionable defect is **F1**, a missing landed selftest control for the `artifact://` edit target, remediable by adding one literal to the existing v2 spelling tuple.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2oraclescheme
Scope: executed=none
