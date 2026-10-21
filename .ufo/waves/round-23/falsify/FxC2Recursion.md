# FxC2Recursion — round 23 / attempt 1 / falsification of C2 (structured-edit authority through parallel nesting and the depth limit)

Seat: `TsukuroiR23-2.FxC2Recursion-2` (leaf; no subagent dispatch, no delegation).
Target reviewed: `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py` (declared SHA256 `4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6`).
Baseline for delta context: `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (pre-round v1 checker).
Cross-read: `.ufo/waves/round-23/candidate/collect.py` (L1 event projector), `.ufo/waves/round-23/build/bindings.json` (real r23 v2 manifest), `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`.

Method: static reading only. This seat is NO-EXEC / NO-FETCH: no interpreter, no hash, no listing, no subprocess, no network was run. Every behavioural statement below is a **derivation from the source text** with a line citation, plus the exact input construction a reader can run. Nothing here is an observed execution. The declared digest was supplied by the assignment and was **not** independently computed.

## Axes named (godspeed step 1)

| Axis | Question | Verdict |
|---|---|---|
| A — grant containment | Can any spelling (nested wrapper, row field, event marker, manifest field, schema variant, depth) cause a structured edit to be classified **clean** under v1, or outside a seat's exact `edit_paths` under v2? | **No grant path found.** Attack refuted (negative result). |
| B — denial fidelity | When a recorded request *is* out of scope, is it reported with the correct denial id, and does it count in the `violations` metric? | **Falsified in part** (F1). |
| C — depth/recursion bound | Does the wrapper-depth limit preserve the identity classification of the leaves it refuses? | **Falsified** (F1). |
| D — metric honesty | Does C2's `structured_edit_mode` mean what the C2 claim text says it means? | **Falsified in part** (F2). |
| E — hardening residue | Are forged authority fields *rejected* everywhere, or merely ignored where the key set is not closed? | **Falsified in part** (F3). |

## Attacked claim

**C2 (axis `operability`, metric `structured_edit_mode`, before 0 → target 1)** — "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."

The specific sub-claim under attack, as stated in the assignment: *"`allow_structured_edit` is set only by `evaluate()` from a validated top-level v2 schema, never from a row field or event marker"* (checker docstring, `candidate/tools/check-seat-bindings.py:64-65`), **plus** the implicit sub-claim that the wrapper-depth limit and parallel nesting cannot weaken the resulting classification.

C1 and C3 are **not** attacked here: C1 reads a different tool (`check-edit-contract.py`) and C3 reads a different tool (`check-path-reconciliation.py`); neither file is in this seat's read scope. My falsification therefore bears on C2 only, plus the shared `collect.py` event shape that feeds C2's audit.

## Result summary

| ID | Severity | Axis | Status |
|---|---|---|---|
| F1 | MEDIUM | B, C | Falsified — depth guard converts recorded exec/fetch/edit denials into a non-violating `SCOPE-SCHEMA` |
| F2 | LOW–MEDIUM | D | Falsified in part — `structured_edit_mode` is satisfiable with zero structured edits recorded |
| F3 | LOW | E | Falsified in part — v1 seat rows are not key-closed, so a forged row field is silently ignored rather than rejected |
| F4 | LOW | A/B/C | Coverage gap — the v1-nested-edit and the exact depth boundary are not asserted by the selftest |
| F5 | LOW (question) | A | `stream_content` is accepted as a structured-edit shape although it is not an `edit` argument in the tool contract |
| F6 | LOW | B | `violations` denotes two different things (aggregate int vs per-seat list) |
| — | — | A | **Negative result:** no nesting, row field, event marker, manifest field or schema variant enables an edit under v1 or outside `edit_paths` under v2 |

---

## F1 — MEDIUM — the depth guard masks out-of-scope denials and drops them from the violation metric

**Where.** `candidate/tools/check-seat-bindings.py:67-68` (guard), `:71-79` (deny lists and tool whitelist), `:91-93` (recursive call and per-child `except`), `:192` (violation counter), `:194` (exit-code rule).

**Mechanism.** `classify()` refuses a node *before* it looks at the node's tool identity:

```python
if not isinstance(tool, str) or not tool or depth > 8:
    raise ValueError('malformed tool name or excessive wrapper nesting')
```

The `bash`/`eval`/`task` → `SCOPE-EXEC-DENIED` and `web_search`/`browser` → `SCOPE-FETCH-DENIED` tests live at `:71-75`, i.e. *after* the guard. The `ValueError` raised at depth ≥ 9 is swallowed by the parallel branch's per-child handler (`:92-93`), which appends `SCOPE-SCHEMA`. `SCOPE-SCHEMA` is explicitly excluded from the violation counter (`:192` `violations += sum(fid != 'SCOPE-SCHEMA' for fid in ids)`).

**Concrete falsifier (input construction; not executed here).** Take the recorded event

```
{"tool": "multi_tool_use.parallel",
 "args": {"tool_uses": [ W1 ]}}          # W1 = 8 nested multi_tool_use.parallel wrappers,
                                         # W8's only child = {"recipient_name": "bash", "parameters": {}}
```

Derivation of the depths (top event = depth 0, one increment per nesting level): `W1` = 1 … `W8` = 8, the `bash` leaf = **9**. The guard trips *on the leaf itself* (`9 > 8`), so the leaf's tool name is never classified. Predicted findings for that event: `['SCOPE-SCHEMA']`; predicted aggregate `violations` contribution: **0**; predicted exit code: 2 (`CANNOT_EVALUATE`).

The same construction with **7** wrappers puts the leaf at depth 8 → the leaf *is* classified → `['SCOPE-EXEC-DENIED']`, `violations` += 1, exit 1. The boundary is therefore exactly *leaf depth 8 = classified, leaf depth 9 = masked*.

**Why the mask is not hypothetical.** `candidate/collect.py:34-44` uses the same `depth > 8` bound but projects differently: when the projector reaches depth 9 it returns `None` for that node's **parameters** while the parent's list comprehension still records the child's `recipient_name` (`collect.py:42-43`: `{'recipient_name': child.get('recipient_name'), 'parameters': projection(...)}`). A real recorded deep wrapper therefore carries `{"recipient_name": "bash", "parameters": null}` inside the trace. The checker refuses that node at depth 9 *by depth alone* and never reads the preserved `bash` name — the exec denial is lost even though the evidence is present in the recorded trace.

**Consequences (all derived, none observed):**
1. `SCOPE-EXEC-DENIED` / `SCOPE-FETCH-DENIED` is replaced by `SCOPE-SCHEMA` for every leaf at depth ≥ 9. The audit still fails closed (exit 2 → `CANNOT_EVALUATE`, `request_audit_mode` 0), so **there is no false PASS** — but the denial *label* and the violation *count* are wrong.
2. `violations` (`:200`) under-reports: a trace containing a recorded `bash` can report `violations: 0` while the seat row's `violations` list (`:193`) contains `['SCOPE-SCHEMA']` — the same key name carrying two different meanings (see F6).
3. The v2 structured-edit denial is masked identically: an out-of-scope `edit` at leaf depth ≥ 9 yields `SCOPE-SCHEMA` instead of `SCOPE-EDIT-DENIED`, and an **in-scope** `edit` at leaf depth ≥ 9 also yields `SCOPE-SCHEMA`, which forces exit 2 and therefore `structured_edit_mode = 0` (`:206`) — a false negative on C2's own metric caused by a legal recording shape.
4. This behaviour is currently *baked into the expected results*: `candidate/tools/check-seat-bindings.py:283-285` builds 11 wrapper levels and asserts exit 2 + `SCOPE-SCHEMA` for the nested `bash`. The masking is intended at the *schema* dimension, but the *exec* dimension is collateral and unasserted.

**Smallest in-scope remedy.** Move the depth bound so that it limits *recursion*, not *leaf identity classification*. Split the guard and reorder it below the deny lists:

```python
if not isinstance(tool, str) or not tool:
    raise ValueError('malformed tool name')
...
if tool in ('bash', 'eval', 'task'):
    return ['SCOPE-EXEC-DENIED']          # now reached at any depth
if tool in ('web_search', 'browser') or tool.startswith('browser.'):
    return ['SCOPE-FETCH-DENIED']
if tool == 'edit' and allow_structured_edit:
    return classify_edit(args, binding)
if depth > 8:
    raise ValueError('excessive wrapper nesting')   # still bounds wrapper descent
```

This keeps the depth-9 wrapper refusal (a wrapper is not on a deny list, so it still raises) and restores `SCOPE-EXEC-DENIED` for a depth-9 `bash` leaf whose `recipient_name` the collector preserved. It requires exactly one expectation change: `:285` `case('depth-exhausted', …, 2, 'SCOPE-SCHEMA')` becomes exit 1 + `SCOPE-EXEC-DENIED`. (Alternative, larger: pre-screen the child's `recipient_name` against the deny lists inside the parallel loop at `:88-93` before recursing.) Under either remedy the in-scope-deep-edit false negative of consequence 3 remains, because the collector nulls that leaf's parameters — that one needs a separate decision (see "Residual risk").

---

## F2 — LOW–MEDIUM — C2's metric `structured_edit_mode` is satisfiable without a single structured edit

**Where.** `candidate/tools/check-seat-bindings.py:144` (mode derivation), `:194` (exit code), `:199-206` (result assembly).

```python
v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'
...
code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)
...
if v2:
    result['structured_edit_mode'] = int(code != 2)
```

`structured_edit_mode` is a pure function of *evaluability*: it is 1 whenever the v2 manifest parsed and the trace produced no `SCOPE-SCHEMA`/incomplete seat. It is **1 even when the trace contains zero `edit` events at all** (a v2 manifest plus a seat whose `events` list is empty: `total = 0`, no findings → code 0 → mode 1 — the empty-trace case at `:285`/`:305` already establishes that an empty trace is a legal, passing trace). It is also **1 when the run has violations** (code 1 → `1 != 2` → 1); only `status` distinguishes PASS/FAIL.

**Falsifier (input construction).** `bindings.json` = schema-v2 with one seat whose `edit_paths` is non-empty; `events.json` = one seat, `complete: true`, `events: []`. Predicted result: `status: 'PASS'`, `requests_total: 0`, `violations: 0`, `structured_edit_mode: 1`. C2's declared metric is therefore met by a run in which no structured edit was ever recorded, requested, authorised or denied.

**Why it matters here.** C2's preregistered metric *is* `structured_edit_mode` (before 0 → target 1), and the claim text reads "New explicit schema-v2 audit authority for exact predeclared structured edit targets". If the intended reading is "the v2 authority is declarable and the audit is evaluable under it", the number is honest but the C2 report must say so explicitly; if the intended reading is "structured edit authority is operably exercised", the current metric cannot support it. Note the mutation record already pins only the *evaluability* semantics: `l1-mutation.json` mutant 7 replaced `int(code != 2)` with `1` and was killed — by the code-2 cases, i.e. by the evaluability distinction alone, not by any edit-count distinction.

**Smallest in-scope remedy.** Either (a) state the intended reading in the C2 report ("`structured_edit_mode` = the v2 authority is active and the trace was evaluable; it does not evidence that any structured edit was exercised"), or (b) add a companion counter to the result (e.g. `structured_edits_authorized` / `structured_edits_denied`, incremented where `classify_edit` returns `[]` / `['SCOPE-EDIT-DENIED']`) and cite that counter, not `structured_edit_mode` alone, as the operability evidence.

---

## F3 — LOW — v1 seat rows are not key-closed, so a forged authority field is silently ignored instead of rejected

**Where.** `candidate/tools/check-seat-bindings.py:147-161` (seat validation), `:78` (tool whitelist).

The v2 branch closes the seat key set exactly:

```python
if v2:
    edits = seat.get('edit_paths')
    if (set(seat) != {'name', 'root', 'read_paths', 'write_paths', 'edit_paths', 'commands', 'fetches'} or …):
        raise ValueError('v2 edit authority')
```

The v1 branch validates only the identity fields and the two path lists; **any other key on a v1 seat row is accepted without comment**. A v1 manifest whose seat carries `"edit_paths": [...]` or `"allow_structured_edit": true` is therefore a *valid* v1 manifest whose forged authority is silently dropped.

**This is not a grant.** Under v1 `allow_structured_edit` is `False` (`:144`, `:186`), so `edit` reaches `:78` and returns `SCOPE-TOOL-UNKNOWN` regardless of any row field — the selftest already pins this at `:334` (`'v1-extra-edit-field-no-grant'` → exit 1 + `SCOPE-TOOL-UNKNOWN`, `mode == -1`). The defect is that the *forgery* is not *reported*: the manifest is accepted as valid, and a reviewer reading it may believe edit authority was granted, while the checker silently ignores it. That is an evidence-fidelity gap on exactly the "row marker" dimension of this attack, and it is asymmetric with v2, where the same row field is loudly rejected as `SCOPE-SCHEMA` (`:331` `'v2-row-marker'`).

**Smallest in-scope remedy.** Close the v1 seat key set as well: in the non-v2 branch require `set(seat) == {'name', 'root', 'read_paths', 'write_paths', 'commands', 'fetches'}`, so a forged row field on a v1 manifest is rejected as `SCOPE-SCHEMA` instead of ignored. One condition, same file.

---

## F4 — LOW — the attacked invariants are not asserted by the selftest (coverage gap, not a live defect)

**Where.** `candidate/tools/check-seat-bindings.py:279-285` (depth cases), `:315-316` (v2 nested cases), `:334-335` (v1 cases); mutation record `candidate/.ufo/waves/round-23/measure/l1-mutation.json` mutant 6.

Two properties that this wave's C2 authority rests on are *derived* correct but not *asserted*:

1. **No case puts a nested `edit` child under a v1 manifest.** `v2-nested-edit` (`:315`) and `v2-nested-denied` (`:316`) are v2 cases; the v1 cases (`:334`, `:335`) are top-level only. The invariant "a nested wrapper cannot enable an edit under v1" — the assignment's primary question — therefore has no direct assertion. The code path is correct by reading: `:91` threads `allow_structured_edit` unchanged, and under v1 that value is `False`, so a nested `edit` child hits `:78` → `SCOPE-TOOL-UNKNOWN`.
2. **The depth boundary is not pinned.** The asserted nesting depths are 3 wrappers (`:282` → `SCOPE-EXEC-DENIED`) and 11 wrappers (`:285` → `SCOPE-SCHEMA`). The 7-vs-8 boundary — the exact point at which F1's masking begins — is asserted nowhere.
3. Mutation mutant 6 (dropping `allow_structured_edit` from the recursive call at `:91`) is killed, but by the **v2** case at `:315`, not by any v1 case; a flag inversion that only manifests on the v1 branch is not directly pinned either.

**Smallest in-scope remedy.** Add three selftest cases: `'v1-nested-edit'` (v1 manifest, `parallel` → `edit` child, expect exit 1 + `SCOPE-TOOL-UNKNOWN`), `'v1-nested-exec'` (v1 manifest, `parallel` → `bash` child, expect exit 1 + `SCOPE-EXEC-DENIED`), and a boundary pair (7 wrappers → `SCOPE-EXEC-DENIED`; 8 wrappers → whatever F1's remedy makes it). If F1 is not remedied, the 8-wrapper case should assert `SCOPE-SCHEMA` **and** document that the exec label is intentionally dropped, so the behaviour is a recorded decision rather than an accident.

---

## F5 — LOW (question, not a defect) — `stream_content` is accepted as a structured-edit shape but is not an `edit` argument

`candidate/tools/check-seat-bindings.py:116` `EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})`. The `edit` tool's declared arguments in the seat/tool contract are `i`, `path`, `old_string`, `new_string`; `stream_content` is not one of them (it does appear in the collector's known-key set at `collect.py:51`, so the *spelling* is at least recordable). Consequence: under v2, an `edit` event spelled `{"path": <declared target>, "stream_content": …}` is audited as a **clean structured edit** although the tool has no such argument — an over-acceptance in the shape dimension (still path-gated, so no scope grant). The `old_string`/`new_string` shape is the tool's real one. If `stream_content` is an observed *adapter* spelling from the S086 corpus, that belongs in the checker's docstring next to `EDIT_SHAPES`; if it is not, it should be dropped from the accepted set. Ask the C1 policy owner, do not guess here.

---

## F6 — LOW — `violations` names two different things

`candidate/tools/check-seat-bindings.py:200` publishes an aggregate `violations` integer that counts only non-`SCOPE-SCHEMA` ids (`:192`), while `:193` publishes a per-seat `violations` **list** that includes `SCOPE-SCHEMA` entries. A seat row can read `"violations": ["SCOPE-SCHEMA"]` while the top-level counter reads `0`. This shape is inherited unchanged from the snapshot (pre-round) checker, so it is **not a round-23 regression** — but it is the reporting surface on which F1's under-count becomes visible, and it is the key a C2 consumer would read. Smallest remedy: rename the per-seat key to `findings`, or count `SCOPE-SCHEMA` separately as `schema_findings`.

---

## Negative result — the primary attack did not land

**Axis A holds.** I could not construct any input — nested wrapper, row field, event marker, manifest field, schema variant, or depth — under which a structured edit is classified clean outside a seat's exact `edit_paths`, or under v1 at all. Derivation of the full surface:

1. **Sole grant source.** `allow_structured_edit` is a keyword parameter of `classify` with default `False` (`:61`). There are exactly three call sites: the definition (`:61`), the parallel recursion (`:91`, which threads the *same* value unchanged), and `evaluate` (`:186`, which passes `allow_structured_edit=v2`). `v2` is set at `:144` **solely** from the manifest's top-level `schema` string being exactly `'tsukuroi-seat-bindings-v2'`. No row field, no event field, no argument, and no depth value can influence it.
2. **v2 mode still grants nothing without per-seat authority.** `:157-161` requires, for every seat, `set(seat) == {name, root, read_paths, write_paths, edit_paths, commands, fetches}` and every entry of `edit_paths` to satisfy `local(p)` and to be present in *both* `read_paths` and `write_paths` of that same seat. `classify_edit` then requires exact string membership (`:128`); there is no glob, no prefix, no normalisation, no selector stripping on the edit path.
3. **v1 cannot be escalated.** Under v1 the `edit` tool is not in the whitelist (`:78`) → `SCOPE-TOOL-UNKNOWN`, a counted violation (`:192`), exit 1. A v1 manifest that additionally carries a v1-with-`edit_paths` row is accepted but grants nothing (`:334`). A v1 manifest with an `allow_structured_edit` row field is likewise accepted-and-ignored (F3) and grants nothing.
4. **Row / event / manifest markers are rejected where they are key-closed, ignored where they are not.** v2 seat row marker → `SCOPE-SCHEMA` (`:158`, asserted `:331`); event-argument marker → `SCOPE-SCHEMA` (`:116`/`:120` shape check, asserted `:337`); manifest-level extra key → `SCOPE-SCHEMA` (`:145` `set(data) != {'schema','seats'}`); schema typo/prefix (`'…-v3'`, `'…-v1 '`) → `SCOPE-SCHEMA` (`:145`), and the prefix-widening mutant (`startswith('tsukuroi-seat-bindings-v')`) is killed in `l1-mutation.json` mutant 9.
5. **Nesting cannot change the flag.** `:91` passes `allow_structured_edit` positionally, unchanged, at every depth; mutant 6 (dropping it) is killed by `l1-mutation.json`.
6. **No false PASS exists on any of these paths.** Every attack input above produces at least one finding, and `:194` maps any finding to exit 1 and any `SCOPE-SCHEMA`/incomplete seat to exit 2; exit 0 requires zero findings, zero schema findings and zero incomplete seats.

**Also verified as unchanged from the snapshot (C2 "legacy schema-v1 policy and historical reds unchanged"):** the snapshot checker has `def classify(tool, args, binding, depth=0)` (no flag parameter) and no `EDIT_SHAPES`/`classify_edit`/v2 branch; under v1 the candidate's `classify` is behaviourally identical to the snapshot's, and the candidate's result dict omits `structured_edit_mode` for v1 manifests (asserted by the `mode == -1` cases at `:334-336`). The real r23 manifest `.ufo/waves/round-23/build/bindings.json` is `tsukuroi-seat-bindings-v2` with per-seat `edit_paths` that are a subset of that seat's `read_paths`/`write_paths` — consistent with the validated shape, and it contains **no** `allow_structured_edit` row or event marker (grep over the manifest found none).

---

## Residual risk

1. **F1's mask is a fidelity defect, not a grant.** The audit still exits 2 (`CANNOT_EVALUATE`) on such a trace, so no false PASS is produced. The exposure is (a) the missing denial label, (b) the under-counted `violations` metric, and (c) the in-scope-deep-edit false negative on `structured_edit_mode`. Severity is capped by the fact that the denial itself is not lost — only its label and its count.
2. **`structured_edit_mode` remains a declaration/evaluability metric** until F2 is addressed in prose or code. Any C2 report that cites it as evidence that structured edit authority *works* would overstate it.
3. **The checker's own contract is post-hoc.** `SCOPE` (`:17`) states the audit covers "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness." Nothing in this report may be read as runtime enforcement; no native per-seat restrictive toolset exists in this round (`preregister.json` `limits`), and this seat has no native restrictive task toolset either.
4. **The v1 row non-closure (F3) leaves a standing invitation**: any future consumer that reads `edit_paths` from a manifest *without* re-deriving the schema gate could mistake a v1 manifest for an authority grant. The checker itself does not, but the manifest is a shared artifact.
5. **Only C2 was attacked.** C1's eight edit-contract decisions and C3's path-census ledger were not in this seat's read scope; no statement here should be taken as a verdict on C1 or C3.

## Verification gaps (what a reader must still run)

This seat is NO-EXEC, so the following were **not** performed and are the reader's to run:

1. Confirm F1 by running the checker with a trace containing a `bash` leaf at wrapper depth 9 and at depth 8 and comparing the finding ids and the `violations` count (expected: depth 8 → `SCOPE-EXEC-DENIED`/violations 1; depth 9 → `SCOPE-SCHEMA`/violations 0). The same run over a real `events.json` produced by `collect.py` from a trace containing a deep wrapper would confirm the collector/checker depth alignment (collector nulls parameters at depth 9, checker refuses the node at depth 9).
2. Confirm F2 by running the checker on the real `bindings.json` with an empty-but-complete seat trace and reading `structured_edit_mode`.
3. Confirm F3 by feeding the checker a v1 manifest whose seat carries an extra `edit_paths` key and observing that it is accepted (no `SCOPE-SCHEMA`) while the edit is still denied.
4. Confirm the negative result by running the two constructions that a *grant* would require: a v1 manifest with a nested `edit` child, and a v2 manifest with a nested `edit` child whose target is outside `edit_paths`; both must not yield exit 0.
5. The declared digest was not recomputed; it is a supplied identity only.

---

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
  Predicate: r23f-fxc2recursion
  Scope: executed=none
