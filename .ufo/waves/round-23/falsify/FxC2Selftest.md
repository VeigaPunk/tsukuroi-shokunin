# FxC2Selftest — falsification of the 37 v2 selftest controls

Seat: FxC2Selftest (reviewer, leaf member). Wave: round-23, attempt 1, FALSIFY phase, post-build from integrated landed state 5a25c88b77f52e940bcad87825c4ac1cd529470d; baseline ae01e50f582016384e620022be38bf5367000e2e.

Target under attack: `candidate/tools/check-seat-bindings.py` (declared SHA256 `4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6`, supplied identity — not independently computed, not hashed/listed/wc'd/imported/run).

## Scope of this attack

Static cross-tabulation of the v2 selftest control set against the v2 code path. This seat is NO-EXEC/NO-FETCH (`commands: []`, `fetches: []`): no mutant was executed, no `--selftest` was run, no file was hashed or listed. Every survival claim below is a line-by-line trace of the selftest's own case table against the mutated line, not an observed run.

## Attacked claim

**C2** (`operability` / `structured_edit_mode`), specifically its scope sentence "New explicit schema-v2 audit authority for **exact predeclared structured edit targets**", and the preregistered edit decisions that C2 is supposed to make discriminating: `DECLARED_EDIT` (exact target is predeclared), `UNDECLARED_EDIT` (no implicit edit permission), `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL`.

The baseline snapshot has no v2 surface at all — `grep 'classify_edit|edit_paths|EDIT_SHAPES|structured_edit_mode'` over `snapshot/tools/check-seat-bindings.py` returns **no matches** — so the entire v2 path (lines 93–130 plus the `v2` branch in `evaluate`) is new in round 23 and is the object of the attack.

## Finding 1 — HIGH: a one-line mutant of the v2 path that none of the 37 v2 controls (nor any of the 73 v1-style controls) kills

**Mutant** — `candidate/tools/check-seat-bindings.py:128`, inside `classify_edit` (v2-only function):

```
-    if value not in binding['edit_paths']:
+    if value not in binding['edit_paths'] and set(args) - {'i'} != {'path', 'old_string', 'new_string'}:
```

Equivalent single-line variant (arguably the more plausible hand-written bug — the stream case is checked, the replace case forgotten):

```
-    if value not in binding['edit_paths']:
+    if 'stream_content' not in args and value not in binding['edit_paths']:
```

**Behavioural effect.** Any edit request carrying the *replace* shape `{path, old_string, new_string}` is audited **clean regardless of its target**: outside the lane, outside the seat's `read_paths`/`write_paths`/`edit_paths`, a production path, `skill://godspeed`, `xd://edit` — anything. The exact-target check, which is the entire substance of the v2 authority, applies only to the `{path, stream_content}` shape. This directly contradicts the v2 authority's own docstring ("exact declared target") and preregistered decisions `DECLARED_EDIT`/`UNDECLARED_EDIT`/`READ_ONLY_EDIT`/`WRITE_ONLY_EDIT`/`EDIT_TRAVERSAL`/`EDIT_EXTERNAL`, all of which are exercised by the selftest on the stream shape only.

**Why no control kills it — the v2 matrix is missing one cell.** The v2 controls form a *shape × target* cross-product:

| | allowed target (`∈ edit_paths`) | denied target |
|---|---|---|
| stream shape `{path, stream_content}` | `v2-stream-edit` (301), `v2-qualified-edit` (303), `v2-nested-edit` (315) | `v2-read-only-target` (304), `v2-write-only-target` (305), `v2-undeclared-target` (306), 9 × `v2-spelling-*` (307–308) |
| replace shape `{path, old_string, new_string}` | `v2-replace-edit` (302) | **— no control —** |

- The only replace-shape control is `v2-replace-edit` (line 302), whose target **is** in `edit_paths`; under the mutant the `and` short-circuits and the case still returns `[]` → exit 0 → PASS.
- The only other controls mentioning `old_string`/`new_string` are `v2-mixed-shapes` (312) and `v2-half-replace` (313); both are rejected by the **shape** check at line 121 before line 128 is ever reached, so they cannot observe the target decision.
- Every target-denial control (304–308) and every nested-denial control (`v2-nested-denied`, 316) uses `{path, stream_content}`.
- Therefore the mutated branch is reachable with the replace shape by exactly one control, and that control is insensitive to the mutation.

Exit code, findings ids, `site` strings and `structured_edit_mode` are **byte-identical for all 110 cases** (37 v2 + 73 v1-style; the 73 is a hand count — the script reports `v1_cases`/`v2_cases` at runtime, which this seat may not execute). The mutation is a pure discrimination hole, invisible to the whole selftest.

**This is not a re-run of an already-killed mutant.** The L1 log (`candidate/.ufo/waves/round-23/measure/l1-mutation.json`) records 10 seat-binding mutants, all killed: 0 (`tool == 'edit'` unconditionally), 1 (membership widened to `read_paths`), 2 (drop the read-path requirement), 3 (drop the write-path requirement), 4 (drop the seat-key-set check), 5 (rewrite the *shape* check to `'path' not in args`), 6 (drop `allow_structured_edit` propagation into the parallel branch), 7 (`structured_edit_mode = 1`), 8 (drop the edit path's URL check), 9 (`v2` schema prefix match). Mutants 1–3 rewrite the *membership set*; mutant 5 rewrites the *shape* check; **none makes the target check conditional on the shape.** That class is untested.

**Honest limitation on materiality.** The mutant does not falsify the C2 *metric*: `structured_edit_mode` is computed independently of the target decision, so the preregistered C2 acceptance command would still report the metric as met. The hole is latent — it falsifies the *discriminating* form of C2 (does the audit actually deny an undeclared edit target?) rather than the measured flag. Whether any round-23 recorded event trips it is unknown to this seat: `round-23/build/events.json` is not in this seat's read paths and was not opened.

**Materiality context (evidence + one inference).** Evidence: `candidate/collect.py:48-52` projects recorded `edit` requests retaining argument-key presence for `old_string`, `new_string` and `stream_content` alike, so both shapes can appear in captured events; the wave's own seat bindings (`build/bindings.json`, schema `tsukuroi-seat-bindings-v2`, ~60 seats each carrying `edit_paths`) use the `{i, path, old_string, new_string}` edit schema. [INFERENCE] I did not read recorded event bodies, so I cannot state which shape dominates in practice — only that the audit supports both and tests the deny path for one of them only.

**Smallest in-scope remedy** (additive controls in the owning seat's file `candidate/tools/check-seat-bindings.py`; this seat's write scope is its report only, so this is a recommendation, not an edit):

```python
v2case('v2-replace-edit-read-only-target', 'edit', {'path': other, 'old_string': None, 'new_string': None}, 1, 'SCOPE-EDIT-DENIED')
v2case('v2-replace-edit-undeclared-target', 'edit', {'path': LANE + '/production', 'old_string': None, 'new_string': None}, 1, 'SCOPE-EDIT-DENIED')
```

Both pass against the current code (exit 1, `SCOPE-EDIT-DENIED`) and both kill the mutant (the mutant returns `[]` → exit 0 → FAIL). No production-behaviour change; the fix is coverage, not logic. A replace-shaped variant of `v2-url-target` would additionally make the two shapes symmetric (see Finding 3).

## Finding 2 — MEDIUM: v1 continuity is asserted only at the top level, leaving the nested propagation of the v2 grant unconstrained

**Mutant** — `candidate/tools/check-seat-bindings.py:91`:

```
-                findings.extend(classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1, allow_structured_edit))
+                findings.extend(classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1, True))
```

**Effect.** Under a **v1** manifest, a nested `edit` child stops being `SCOPE-TOOL-UNKNOWN` (exit 1) and becomes `SCOPE-SCHEMA` (exit 2, `CANNOT_EVALUATE`): a v1 seat has no `edit_paths` key, so `classify_edit` raises `KeyError` at line 128, which the event loop converts to `SCOPE-SCHEMA`. No permit is created, but the v1 audit's exit code and status change for any v1 trace that nests an edit request.

**Why no control kills it.** The two v1-continuity controls are top-level only: `v1-extra-edit-field-no-grant` (334) and `v1-edit-continuity` (335). No v1-style control nests an `edit` child — the parallel controls use `read`/`bash`/`None` children (`parallel-exec`, `parallel-fetch`, `parallel-local`, `parallel-malformed`, `mixed-parallel`, `qualified-parallel`, `nested-exec`). The v2 direction of the same propagation *is* constrained (L1 mutant 6, killed), but only in the v2 direction. `allow_structured_edit` is therefore free to be hard-coded `True` in the wrapper branch without any control noticing.

**Smallest remedy:** one v1-manifest parallel case with an edit child, e.g. `case('parallel-edit-v1', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': report, 'stream_content': None}}]}, 1, 'SCOPE-TOOL-UNKNOWN')`.

## Finding 3 — LOW: the edit path's own scheme, internal-URI and empty-target rules have no v2 control

Three further one-line survivors in `classify_edit`. None creates a permit — membership in `edit_paths` is the gate, so all three only change the *finding label* or the *exit code* of an already-denied request — but each leaves a stated rule unverified on the v2 path:

1. **`:124`** `if not isinstance(value, str) or not value:` → `if not isinstance(value, str):` — an **empty-string** target becomes `SCOPE-EDIT-DENIED` (exit 1) instead of `SCOPE-SCHEMA` (exit 2). The "missing target" control `v2-missing-path` (314) covers an *absent* key, never an empty string.
2. **`:126`** `re.match(r'(?i)^https?://', value)` → `re.match(r'^https?://', value)` — an **uppercase-scheme** edit target becomes `SCOPE-EDIT-DENIED` instead of `SCOPE-FETCH-DENIED`. The scheme-case control exists only on the read path (`HTTPS://EXAMPLE.INVALID/:1-5`); the edit path's own `(?i)` is never exercised, so the two paths could silently diverge on scheme case.
3. **`:126`** dropping the alternative `or re.match(r'^[^/:\s]+:[0-9]+/', value)` — an **internal URI** edit target (`localhost:9222/...`) becomes `SCOPE-EDIT-DENIED` instead of `SCOPE-FETCH-DENIED`. The internal-URI control exists only on the read path (`localhost:9222/`). Note this is already an inconsistency in the *unmutated* code: `file:///...` matches neither alternative and is classified `SCOPE-EDIT-DENIED` on the edit path, while the read path's `requested_path` treats any `://` string as a fetch candidate — so `EDIT_EXTERNAL`'s "internal URIs" rule is not uniformly applied across the two paths.

**Remedy:** one control per shape for scheme case, internal URI and empty target, e.g. `v2case('v2-upper-scheme-target', 'edit', {'path': 'HTTPS://EXAMPLE.INVALID/A.md', 'stream_content': None}, 1, 'SCOPE-FETCH-DENIED')` and `v2case('v2-empty-target', 'edit', {'path': '', 'stream_content': None}, 2, 'SCOPE-SCHEMA')`.

## Finding 4 — LOW: the wrapper-nesting limit is not pinned by any control

**Mutant** — `candidate/tools/check-seat-bindings.py:67`: `depth > 8` → `depth > 9`.

**Effect.** Invisible to every control. The `depth-exhausted` case still yields exactly one `SCOPE-SCHEMA` finding at site `A:0` — the overflow merely occurs one level deeper, and the finding is appended by the enclosing parallel branch's `except` handler (line 92-93) at the same event index, so the emitted result JSON is unchanged. No other case reaches depth 9.

**Why it matters beyond tidiness.** `candidate/collect.py:33` uses the same threshold (`depth > 8`) for projection. The auditor's and the collector's limits are kept in sync only by convention; the selftest pins "some overflow yields SCOPE-SCHEMA" but never the threshold value, so the two files can drift apart undetected — a drift that would silently truncate recorded wrapper depth.

**Remedy:** a control that asserts the threshold exactly (e.g. a 9-level wrapper is accepted, a 10-level wrapper is `SCOPE-SCHEMA`).

## Residual risk

- **The audit is post-hoc and spelling-only by its own declaration** (`SCOPE` constant, line 20: "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness."). This round has no native restrictive per-seat task toolset (preregister `limits`), and nothing in this report claims runtime enforcement. Finding 1 is a defect in the audit's *discrimination*, not in enforcement, and no enforcement claim is made or implied.
- Finding 1 is latent against the round-23 C2 metric (`structured_edit_mode` is independent of the target decision), so it can pass both the selftest and the preregistered acceptance command while the exact-target authority is undiscriminating for one supported adapter shape. A metric-only acceptance test cannot detect it.
- The L1 mutation log's 27 mutants cover the v2 surface only along the *membership-set* and *shape-set* axes; the *shape-conditional target* axis (Finding 1), the *nested v1 continuity* axis (Finding 2), and the *scheme/empty-target* axis (Finding 3) have no mutant in the log at all.

## Verification gaps (what this seat did not and could not establish)

- **No execution.** `executed=none` by seat binding: no mutant was run, no `--selftest` was run, nothing was hashed, listed, counted by shell, imported, compiled or tested. All survival statements are static traces of the selftest's own case table against the quoted mutated line. A confirmation step (run the two added `v2case` controls against a mutated temp copy) belongs to the owning seat, which holds the script's write scope and an executable scope.
- The claimed v1 control count (73) is a **hand count** of the `cases`/`cases.extend` lists; the script's own `v1_cases`/`v2_cases` counters were not executed. The v2 count (37) was verified by enumerating every `v2case(...)` call site, including the 9-entry spelling loop at lines 307–308, and matches the assignment.
- `round-23/build/events.json` was not opened (not in this seat's read paths), so I cannot state whether any recorded replace-shaped edit in this wave targets an undeclared path; the materiality of Finding 1 against real r23 traffic is therefore undetermined.
- `candidate/collect.py` was read only as far as the projection function (lines 1–73) to establish which argument keys are retained; its event-emission tail was not read.
- The declared SHA256 was taken as supplied identity and was not recomputed; the snapshot comparison was made by reading the snapshot file's content for v2 identifiers, not by diffing digests.
- No peer, fleet or sibling file was modified; the only file written is this report.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2selftest
Scope: executed=none
