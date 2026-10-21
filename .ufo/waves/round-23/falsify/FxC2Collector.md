# FxC2Collector — falsification report (round 23, C2: v2 edit audit authority)

Seat: FxC2Collector (leaf reviewer, no subagent dispatch). Lane bounds: leaf member — no subagent dispatch.
Wave: round-23, attempt 1, FALSIFY phase, post-build, from integrated landed state
`5a25c88b77f52e940bcad87825c4ac1cd529470d`. Baseline `ae01e50f582016384e620022be38bf5367000e2e`.
Method: static read-only analysis of the two declared in-scope artifacts plus the declared fixtures.
No command was executed, nothing was hashed, nothing was fetched, no file outside the seat's declared
read/write paths was opened. The declared digest below is supplied identity, not an independent computation.

Artifacts read (all inside the seat's declared `read_paths`):

- `.ufo/waves/round-23/candidate/tools/check-seat-bindings.py` (r23 candidate auditor; the attack target)
- `.ufo/waves/round-23/snapshot/tools/check-seat-bindings.py` (r22 baseline auditor, for delta)
- `.ufo/waves/round-23/candidate/collect.py` (r23 collector; produces the events projection the auditor consumes)
- `.ufo/waves/round-23/build/bindings.json` (the landed v2 manifest)
- `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed`
- `.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json` (author-side mutation record)

## 0. Axes named

| Axis | Question |
| --- | --- |
| A1 authority honesty | Does the v2 edit authority grant exactly what was declared, and nothing adjacent to it? |
| A2 projection fidelity | Does the r23 collector's projection (`collect.py`) preserve the request facts the auditor needs to decide? |
| A3 metric calibration | Does C2's metric `structured_edit_mode` mean what the claim says it means? |
| A4 blast radius | Can one ordinary request degrade or launder an entire wave's evidence? |

## 1. Attacked claim

**C2 — "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy
schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."**
(`.ufo/waves/round-23/preregister.json`, claims[1]; metric `structured_edit_mode`, before 0, target 1.)

The attacked surface is the *round-23 collector projection for edit requests* — key presence only,
values redacted, unknown keys mapped to `__unknown_argument__` — and the auditor's consumption of it:
`collect.py:34-54` (`projection`) feeding `check-seat-bindings.py:61-130` (`classify` / `classify_edit`)
with the shape set at `check-seat-bindings.py:116` (`EDIT_SHAPES`).

The specific proposition under attack: **"a recorded edit request is projected into a clean v2 shape
only when the original request was in fact a structured edit on a declared target."**

Scope honesty, restated: the auditor audits *recorded request spellings* only
(`check-seat-bindings.py:19` `SCOPE`). Nothing here is runtime enforcement, effect proof, symlink proof,
reading proof, or universal recorder completeness. No claim of native prevention is made or implied.

## 2. Bounded search: the projection is key-faithful, so no key-level false-clean exists

Let `K` be the recorded key set of an original `edit` request and `P(K)` the collector's projection.

`collect.py:51` — `projected = {key if key in known else '__unknown_argument__': None for key in args}`
with `known` at `collect.py:49`. Therefore

```
P(K) = (K ∩ known)  ∪  ({'__unknown_argument__'} if K \ known ≠ ∅ else ∅)
```

The auditor's clean test is `check-seat-bindings.py:121`
`set(args) - {'i'} not in EDIT_SHAPES` → raise → `SCOPE-SCHEMA`, with
`EDIT_SHAPES = ({'path','stream_content'}, {'path','old_string','new_string'})` at line 116.
`__unknown_argument__ ∉ known`, so any unrecognised member survives as a distinct key and can never
satisfy the exact-shape test. Hence:

> **Lemma (bounded search result).** `P(K)` is classified clean **iff**
> `K ∈ { {path,stream_content}, {i,path,stream_content}, {path,old_string,new_string}, {i,path,old_string,new_string} }`.

Two consequences:

1. **No key-level false-clean.** The collector cannot launder an edit request that carried an
   unrecognised argument into a clean v2 shape — an unknown member always survives as
   `__unknown_argument__` and forces `SCOPE-SCHEMA` (`check-seat-bindings.py:121`, fixture
   `v2-unknown-key` at line 311). The feared "unknown key silently absorbed" failure does **not** occur.
   This half of the attack returns a clean negative.
2. **The false-clean space is therefore exactly four key sets**, so it can be enumerated exhaustively
   rather than sampled. Every false-clean must live in those four forms, or in a projection defect that
   removes a member the auditor needs (F4 below). This is the bounded search that found the findings.

Because of (2), the surviving false-clean is a *semantic* one: the collector faithfully preserves a key
set that the auditor has pre-declared to be "structured", so any original whose key set matches one of
the four accepted forms is credited regardless of whether the original was an executable structured edit.

## 3. Findings (severity order)

### F1 — HIGH — `{path, stream_content}` is a false-clean shape: the accepted "structured edit" form
### is not a member of the audited edit request surface

**Evidence.** `check-seat-bindings.py:116` accepts `{path, stream_content}` as one of exactly two
structured-edit shapes; `collect.py:49` promotes `stream_content` to a first-class known key.
The *same file* enumerates the audited tool surface for the other four tools at
`check-seat-bindings.py:95-100`:

```
'read':  {'i', 'path'}
'grep':  {'i', 'pattern', 'path', 'case', 'gitignore', 'skip'}
'glob':  {'i', 'path', 'hidden', 'gitignore', 'limit'}
'write': {'i', 'path', 'content'}
```

That table is a faithful transcription of the audited tool surface (it matches the read/grep/glob/write
parameter sets exactly, member for member). By the same surface, the audited `edit` request surface is
`{i, path, old_string, new_string, replace_all}` — it contains **`replace_all`** and contains **no
`stream_content`**. `EDIT_SHAPES` therefore (a) invents a member the surface does not have, and (b) omits a
member the surface does have. `collect.py:49` mirrors the same defect: `known` contains `content`
(write's real body key) but not `replace_all`, and adds `stream_content`.

**The falsifier.** A recorded edit request whose arguments are

```json
{"tool": "edit", "args": {"i": "...", "path": "<declared edit target>", "stream_content": "<opaque blob>"}}
```

is projected by `collect.py:51` to `{"i": null, "path": "<declared edit target>", "stream_content": null}`,
which `check-seat-bindings.py:121` accepts (lemma, case 2), `check-seat-bindings.py:128` matches against
the seat's declared `edit_paths`, and returns `[]` — **exit 0, no finding, the seat is credited with an
authorised structured edit on the declared target.** Yet the original was *not* a structured edit:

- `stream_content` is not a parameter of the audited `edit` tool, so such a recorded request could not
  have been an executed `edit` call; no `edit` ever ran against that target under it.
- Semantically `{path, stream_content}` is a *whole-file overwrite* — the `write`/`content` operation —
  not a matched-anchor replacement. The v2 authority distinguishes edit authority from write authority
  (C1 decision `DECLARED_EDIT`: the target must be predeclared "for edit **and** for both read and
  write"; the eight decisions treat edit authority as a third, narrower grant). A whole-file overwrite
  is credited as an *edit*, i.e. the credit names the wrong authority. There is no privilege escalation
  (edit targets are forced ⊆ read ∩ write at `check-seat-bindings.py:160`), so this is a mislabelling and
  an honesty defect, not an escalation.

The false-clean is **locked in by the fixture**: `v2-stream-edit` (line 301), `v2-qualified-edit`
(line 303), `v2-read-only-target` (304), `v2-write-only-target` (305), `v2-undeclared-target` (306),
the whole spelling table (307-309) and `v2-nested-edit` (315) all use `stream_content` as the *only*
body spelling for the "clean" cases. Not one clean-path fixture exercises the surface's real
`old_string`/`new_string` pair without also exercising the ungrounded one.

**[INFERENCE / grounding gap]** The grounding file for the shape set
(`.ufo/waves/round-23/sources/structured-edit-observations.json`, preregister source S086
"observed structured edit request keys and recorded adapter steps") is **not** in this seat's declared
`read_paths`, so I could not confirm whether `stream_content` was observed in a recorded request. If it
was observed, F1 downgrades from "shape unsourced against the audited surface" to "shape accepted with no
run-time check that the recorded body was an edit body and no citation of the observation in the claim".
Either way the shape is currently credited on key presence alone.

**Smallest in-scope remedy.** Delete `{'path', 'stream_content'}` from `EDIT_SHAPES`
(`check-seat-bindings.py:116`) *and* drop `stream_content` from `known` (`collect.py:49`), so such a
request projects to `__unknown_argument__` → `SCOPE-SCHEMA` instead of clean credit; then re-point the
clean fixtures from `stream_content` to the surface's real pair (lines 301, 303-309, 315, 332, 337) and
add one fixture asserting `stream_content` → `SCOPE-SCHEMA`. If the observation file does ground
`stream_content`, the alternative minimal remedy is to keep the shape but cite the observation in the C2
claim scope and add a fixture that exercises it with a *string* body rather than only `None`.
Remedy applies to the candidate tool only; no production, manifest or route file is touched.

### F2 — HIGH — the surface's real edit member `replace_all` is unknown to both halves, and it can zero
### C2's own metric for an entire wave

**Evidence.** `replace_all` occurs **nowhere** in `check-seat-bindings.py` or `collect.py` (grep over
both declared files: no match). It is therefore (a) not in `known` (`collect.py:49`) and (b) not in
`EDIT_SHAPES` (`check-seat-bindings.py:116`).

**The falsifier / failure path.** A recorded edit request that is a perfectly ordinary member of the
audited surface —

```json
{"tool": "edit", "args": {"i": "...", "path": "<declared edit target>",
                           "old_string": "...", "new_string": "...", "replace_all": true}}
```

— is projected by `collect.py:51` to `{i, path, old_string, new_string, __unknown_argument__}` (one
unknown member survives as the sentinel, per the lemma). `check-seat-bindings.py:121` then rejects the
exact-shape test and raises; `evaluate` converts the raise to `SCOPE-SCHEMA`
(`check-seat-bindings.py:187-188`). At `check-seat-bindings.py:194`,
`code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' ...)` → **code 2** →
`status = 'CANNOT_EVALUATE'`, `request_audit_mode = 0` (line 200) and, for a v2 manifest,
`structured_edit_mode = int(code != 2) = 0` (line 206).

Consequences, both material:

- **C2's metric target (1) becomes unreachable for any wave in which one seat made such a call.** The
  metric is hostage to an unrelated, legitimate request spelling. The r23 build wave's own seats held
  `edit_paths` on draft `.py` files (`build/bindings.json`, seats `ExecEditContract`, `ExecEditAudit`,
  `ExecReconciliation`), so this is a live risk, not a hypothetical one.
- **The deviation is invisible in the violation count.** `check-seat-bindings.py:192` counts a finding as
  a violation only when `fid != 'SCOPE-SCHEMA'`; the malformed-edit finding is therefore *not* counted as
  a violation, yet it is the sole cause of `CANNOT_EVALUATE`. A wave whose only defect is one
  surface-legal edit call reports zero violations and no usable metric.
- **Asymmetry with the v1 baseline.** Under the r22 baseline (`snapshot/tools/check-seat-bindings.py`),
  `edit` fell through to `SCOPE-TOOL-UNKNOWN` (baseline line 78) → code 1 (FAIL), not code 2. v2 converts
  that class of event from *FAIL* to *CANNOT_EVALUATE*. The C2 claim's "legacy schema-v1 policy and
  historical reds unchanged" still holds for v1 manifests (baseline and candidate agree on the v1 path),
  so this is not a legacy-red rewrite — but it is a new third outcome class that the claim does not name.

**Smallest in-scope remedy.** Add `'replace_all'` to `known` (`collect.py:49`) and add the shape
`{'path','old_string','new_string','replace_all'}` to `EDIT_SHAPES` (`check-seat-bindings.py:116`); add
two fixtures — one asserting `{path, old_string, new_string, replace_all}` on a declared target is clean
(exit 0) and one asserting the same on an undeclared target is `SCOPE-EDIT-DENIED`.

### F3 — MEDIUM — `structured_edit_mode` is a mode flag, not coverage: C2's metric is vacuously
### satisfiable and survives a FAIL

**Evidence.** `check-seat-bindings.py:206` — `result['structured_edit_mode'] = int(code != 2)`. It is 1
whenever the wave evaluated at all (code 0 *or* code 1) and 0 only for `CANNOT_EVALUATE`. The result
object carries **no count** of structured edit events: `requests_total` counts every event
(line 201), and `seats[].requests` counts events per seat (line 193); neither distinguishes an edit event
that was audited under v2 authority from any other event.

Consequences against the C2 claim wording ("New explicit schema-v2 audit authority for exact predeclared
structured edit targets"):

- A wave containing **zero** `edit` requests scores `structured_edit_mode = 1`. The metric therefore does
  not evidence that v2 edit authority was ever exercised.
- A wave that produced `status = FAIL` with real scope violations also scores `structured_edit_mode = 1`.
  The metric cannot distinguish "v2 authority engaged and everything was in scope" from "v2 authority
  engaged and something was out of scope".

**Smallest in-scope remedy.** Count v2-audited edit events (e.g. increment a counter in the
`check-seat-bindings.py:186` loop when `event.get('tool')` resolves to `edit` and the manifest is v2),
emit it as `structured_edits_audited` next to `structured_edit_mode`, and state in the C2 claim scope that
the metric requires that count to be > 0 — or state the vacuity explicitly as a limit. This changes no
finding id and no exit code.

### F4 — MEDIUM — the collector drops unrecognised members of parallel children, laundering a
### malformed envelope into a clean structured-edit classification

**Evidence.** `collect.py:42-44` rebuilds each parallel child as exactly
`{'recipient_name': ..., 'parameters': ...}`; any other recorded member of that child is **silently
discarded**. The auditor, by contrast, treats exactly that deviation as a schema violation:
`check-seat-bindings.py:88` — `if not isinstance(child, dict) or set(child) != {'recipient_name','parameters'}: raise ValueError`
→ `SCOPE-SCHEMA` (line 93).

**The falsifier.** A recorded parallel request whose child carries an extra recorded member —

```json
{"tool": "multi_tool_use.parallel",
 "args": {"tool_uses": [{"recipient_name": "edit",
                         "parameters": {"path": "<declared edit target>", "old_string": "...", "new_string": "..."},
                         "id": "call_1"}]}}
```

— is projected by `collect.py:42-44` to a child with exactly two members, so the auditor's
`set(child) != {...}` test at line 88 never fires, and the inner edit is classified clean
(`check-seat-bindings.py:121` → line 128 → `[]`). The *unprojected* original would have been
`SCOPE-SCHEMA`. The projection therefore converts a schema deviation into a clean v2 structured-edit
credit — a false-clean produced by the projection, not by the auditor.

Note the asymmetry with the envelope level: the collector **does** flag unexpected *envelope* members
(`collect.py:45-46`, `if set(args) != {'tool_uses'}: projected['__unknown_argument__'] = None`) but not
unexpected *child* members. The fixture set covers a non-dict child (`parallel-malformed`, line 237) and
a malformed envelope (`v2-events-trace-marker`, line 337), but **no fixture covers a dict child with an
extra member** — the exact case the projection launders.

**Smallest in-scope remedy.** In `collect.py:42-44`, add the sentinel to the projected child when
`set(child) != {'recipient_name','parameters'}` (mirroring lines 45-46), e.g. build the child dict and
insert `'__unknown_argument__': None` on deviation; then add one fixture asserting that a child with an
extra member yields `SCOPE-SCHEMA`.

### F5 — LOW — unknown-member multiplicity is destroyed by the sentinel, so the projected event cannot
### show how far the original deviated

**Evidence.** `collect.py:51` maps *every* unrecognised member to the same key
`'__unknown_argument__'`; a dict comprehension collapses N unknown members into one. The auditor only
consumes presence (`check-seat-bindings.py:101` `unknown_keys = bool(set(args) - allowed_keys[tool])`;
line 121 exact-shape test), so classification is unaffected — the projection is still sound as a
*classifier* input. But the projected event cannot distinguish one unknown member from five, and a
recorded request that literally used the member name `__unknown_argument__` is indistinguishable from a
redaction artefact. The collector's own coverage string
(`collect.py:9-11`, "Path/tool arguments are retained; command bodies, write contents, queries,
environment, credentials and arbitrary tool payloads are not copied") does not promise member
multiplicity, so this is a documentation-grade gap rather than a defect.

**Smallest in-scope remedy.** Either record the unknown-member count alongside the sentinel
(e.g. `'__unknown_argument__': None` plus a separate count field) or state in the collector's coverage
string that unknown-member multiplicity is not retained.

### F6 — LOW / residual — the auditor binds a trace seat to its binding by seat *name* only

**Evidence.** `check-seat-bindings.py:167-171` matches trace seats to manifest seats by `name`, and
records `seat['agent']` without cross-checking it against anything in the manifest (the manifest has no
agent field). The chain seat → agent id → transcript is established upstream by the collector
(`collect.py:108-110`, `index = {p.stem: p for p in transcripts.glob('*.jsonl')}` and
`trace = index.get(aid)` with `aid = member['agentId']`), so the auditor inherits it transitively — but
the auditor itself does not verify it, and a hand-built or substituted `events.json` would pass. This is
inside the declared scope limits ("not ... universal trace completeness", `check-seat-bindings.py:19`) and
is not a v2 regression.

**Smallest in-scope remedy.** No change required for C2; if the L1 wants belt-and-braces, record the
trace `agent` ids in the v2 manifest and cross-check them in `evaluate` — a manifest schema change, so it
is out of scope for this wave and is listed as a residual only.

## 4. What was checked and found sound (negative results, so the frontier is not re-walked)

- **Unknown-key laundering into a clean shape: none.** Proved in §2 (lemma). `__unknown_argument__`
  always survives, and `check-seat-bindings.py:311` pins it (`v2-unknown-key` → `SCOPE-SCHEMA`).
- **Row/trace marker forgery: none.** `allow_structured_edit` is set only from the validated manifest
  schema (`check-seat-bindings.py:144`, passed at line 186); `check-seat-bindings.py:158` rejects any seat
  carrying an extra field, and fixtures `v2-row-marker` (331) and `v2-events-trace-marker` (337) pin it.
- **Edit authority widening: none.** `edit_paths` must be a subset of both `read_paths` and `write_paths`
  (`check-seat-bindings.py:160`); mutants that weaken this are recorded as killed in the author's
  mutation file (`l1-mutation.json`, mutants 2 and 3).
- **Target spelling expansion: none.** `classify_edit` compares the path by exact membership
  (`check-seat-bindings.py:128`); the spelling table at line 307-308 pins trailing slash, `./`, `x/../`,
  `//`, `:raw`, relative, `skill://`, `xd://` and case changes to `SCOPE-EDIT-DENIED`.
- **Path-value laundering through the projection: none for local paths.** `projected_path`
  (`collect.py:20-32`) only rewrites URL-shaped and `://`-bearing values, and every rewrite lands on a
  non-`edit_paths` token, so a rewritten path can only become more denied, never more permitted.
- **v1 continuity: intact.** Under a v1 manifest an `edit` request still yields `SCOPE-TOOL-UNKNOWN`
  (`check-seat-bindings.py:78`; fixtures 334-335), and the baseline
  (`snapshot/tools/check-seat-bindings.py`) has no `edit` branch at all — the v2 branch is purely additive.

## 5. Residual risk and verification gaps

1. **Grounding gap (F1).** `.ufo/waves/round-23/sources/structured-edit-observations.json` (preregister
   S086) and `edit-decision-policy.json` are outside this seat's declared `read_paths`; whether
   `stream_content` was observed in a recorded request is therefore unconfirmed here. If S086 grounds it,
   F1's remedy switches to the "cite the observation + add a string-body fixture" branch.
2. **Live metric risk (F2).** No `events.json` for any r23 wave is in this seat's read paths, so I could
   not check whether any recorded r23 `edit` call carried `replace_all`. The L1 should check this first:
   if any r23 wave recorded such a call, that wave's C2 metric is already 0 / `CANNOT_EVALUATE`, and F2
   is not latent but already realised.
3. **Metric semantics (F3).** C2's `structured_edit_mode` cannot distinguish "authority exercised" from
   "authority merely enabled". Any downstream saturation statement about C2 should be re-read against the
   code at `check-seat-bindings.py:206` before it is asserted as coverage.
4. **Projection fidelity beyond edits.** F4 shows the collector drops unrecognised *child* members. The
   same class of defect (silent member loss) was checked for the non-parallel tools at `collect.py:51`
   and does not occur there — the sentinel preserves presence — so F4 is confined to the parallel branch.
5. **Scope honesty.** Every finding above is about *recorded request spellings* and the *projection* of
   those spellings. None of it is runtime prevention, effect proof, symlink proof, reading proof or
   recorder-completeness proof, and none of it implies that any seat's edit was or was not actually
   applied. No native restrictive task toolset exists; the v2 authority is an audit-time authority only.

## 6. Recommended smallest change set for C2 (candidate-only, no production/manifest/route edits)

1. `check-seat-bindings.py:116` — `EDIT_SHAPES` → `({'path','old_string','new_string'}, {'path','old_string','new_string','replace_all'})`.
2. `check-seat-bindings.py:116` — remove `{'path','stream_content'}` (F1) unless S086 is cited in the claim.
3. `collect.py:49` — `known`: drop `stream_content`, add `replace_all`.
4. `collect.py:42-44` — preserve an unexpected child member as `__unknown_argument__` (F4).
5. `check-seat-bindings.py:206` — emit `structured_edits_audited` and require > 0 for the C2 claim (F3).
6. Fixtures: replace the `stream_content` clean-path fixtures with the surface pair; add
   `replace_all` clean/denied fixtures, an extra-member parallel child fixture, and a
   `stream_content` → `SCOPE-SCHEMA` fixture.

Each of 1-6 is a local edit inside the two declared candidate files plus fixture updates; none touches
production code, the Git index, refs, routes or configs.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-fxc2collector
Scope: executed=none
