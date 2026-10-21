# ConnFxSiblings — sibling-overlap scan (r23 FALSIFY, attempt 1)

Scope of this seat: read-only falsification of sibling overlap between the landed
round-23 lane artifacts and another lane's province (orchestration/tooling, kumitate).
Declared reads only; no commands, no fetches, no subagents, no installs.

## 1. Attacked claims

| Claim | Axis | Attacked proposition |
|---|---|---|
| **C2** | operability | "New explicit schema-v2 audit authority for exact predeclared structured edit targets" — does the landed decision table adjudicate *other* lanes' bindings (cross-lane authority), thereby overlapping the hub/binding-semantics owner (kumitate, OUT-006) or sibling lanes' own authority surfaces? |
| **C1** | depth | The eight-row decision table + bounded procedure — does it define a *fleet* binding-schema convention (diffusion / de facto schema ownership) rather than a lane-local audit convention? |
| **C3** | calibration | "Both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts" — does the path-census reconciliation absorb the census/router owner (kumitate, ufo-fsd scripts & runtime) or relabel another lane's violations? |
| **frontier** | adjacency | Corpus claims held ground only: "not an uncovered frontier, repertoire addition or outside promotion" — is that contradicted by anything the landed file claims over siblings? |

## 2. Bounded search actually executed (declared files only)

Declared set read in full: `candidate/corpus/knowledge/structured-edit-r23.md` (35 lines),
`preregister.json` (121 lines), `snapshot/PROVINCE.md`, `sources/godspeed-directive.txt`,
`skill://godspeed`, plus this seat's own bound report path. Searches were grep-only over
those declared files (no `ls`/`wc`/hash/command of any kind).

| Search | Scope | Result |
|---|---|---|
| `kumitate\|mori\|kama\|kagi\|mado\|tameshi\|kaidoku\|revenger\|sibling\|province` | structured-edit-r23.md | **0 matches** — the landed lane file names no sibling lane, no province, no owner |
| `census\|reconcil\|path count\|rough\|lane count\|r22` | structured-edit-r23.md | **0 matches** — C1/C2 artifact contains no path-census or reconciliation language at all |
| `dispatch\|hub\|manifest\|bindings\|events\|orchestrat\|enforce\|gate\|tools/\|check-` | structured-edit-r23.md | 3 hits only: line 9 "before dispatch"; line 29 "captured native read/write expansion … forbidden command/fetch"; line 31 the non-enforcement disclaimer |
| `dispatch\|routing\|hub\|enforce\|allowlist\|schema-v1\|schema-v2\|task API` | structured-edit-r23.md | lines 9, 26, 29, 31 (quoted below) |
| `dispatch\|routing\|hub\|enforce\|outside\|closure\|classifier\|census` | preregister.json | C2 scope + separability + `outside_round22` scope lines (quoted below) |
| `kumitate\|tameshi\|orchestration\|ufo-fsd\|each lane keeps its own gate\|path census` | PROVINCE.md | OUT-006 (kumitate domain), OUT-010 (tameshi), ADJ-05, ADJ-07, "Out of province → report, never absorb." |

**Gaps (declared-path limits, not improvised):** `tools/check-edit-contract.py`,
`tools/check-seat-bindings.py`, `tools/check-path-reconciliation.py`, the r23 C3 corpus
artifact, and sibling `PROVINCE.md` files are outside this seat's read set, and NO-EXEC
forbids running the gates. C3's sibling-overlap is therefore assessed from its
preregister scope text only, not from its landed document.

## 3. Findings

### F1 — C2 seam: procedure text is wave-scoped, document text is lane-scoped (contradiction, not smoothed)

The landed file's *title* scopes it: "**Structured edit authority for this lane's evidence
files**". Line 9 scopes authority: "Authority is separately declared lane policy."
Line 31 scopes effect: "This is declared post-hoc audit authority only. It is not native
permission enforcement, a sandbox, body/patch interpretation, actual reading or effects
proof, complete recorder coverage…"

But bounded procedure step 4 (line 29) is unqualified in the opposite direction:
"**Audit every captured native read/write expansion against its own authority.** A valid
frontend target cannot clear an out-of-binding backend step or a forbidden command/fetch."

C2's gate command (preregister) reads *wave-level* artifacts:
`--manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`.
Wave-level `bindings.json`/`events.json` contain every seat's binding and recorded steps,
not only tsukuroi's. So the document's declared scope ("this lane's evidence files") and the
procedure's actual scope ("every captured native read/write expansion") disagree, and the
decision table's rows are keyed on *binding semantics* (`edit_paths`, read/write subsets,
forbidden command/fetch) that belong to the seat-binding contract the hub produces.

Overlap consequence: if the C2 gate applies the eight rows to sibling seats' recorded
steps, tsukuroi's table grades *other lanes'* authority compliance — a claim on sibling
lanes' own authority surface and, in substance, an audit of dispatch-time binding
semantics that OUT-006 assigns to kumitate ("Kumitate scopes OMP task/hub and orchestration
tooling, so task/hub dispatch and routing semantics are its analysis, not tsukuroi's").

This is a *seam*, not a proven violation: the gate implementation is outside this seat's
read set, so whether grading is lane-restricted in code is unobserved here.

### F2 — second-order effect: a lane-local convention in a shared-corpus location diffuses into fleet schema ownership

Second-order trace across surfaces:

- *contract surface*: the eight rows are written as unconditional propositions ("Exact
  target is predeclared for edit and for both read and write"; "Unknown means
  could-not-evaluate or rejection, never permission"). They read as rules about what a
  binding *is*, not as rules about how *this lane* grades *its own* bindings.
- *runtime surface*: none asserted — line 31 explicitly disclaims enforcement, and
  preregister `limits` says "No native per-seat restrictive tool interface exists". Good.
- *verification surface*: step 4 plus "Independent literal positive/negative controls"
  are an application to tsukuroi's own gate, which OUT-010 permits ("each lane keeps its
  own gate"). No method-ownership claim; no overlap with tameshi.
- *substrate surface*: none; host/package/service/boot actions explicitly excluded.
- *diffusion surface (the second-order harm)*: the artifact lives in `corpus/knowledge/`,
  a location sibling lanes read as fleet reference. PROVINCE's own frontier discipline
  ("the pins are stale by design once a sibling commits again") shows siblings consume
  each other's artifacts as declarations. A lane-local audit convention placed there,
  without a normative-scope marker, can be read by a sibling as the definition of
  schema-v2 `edit_paths` — converting tsukuroi's audit convention into de facto fleet
  binding-schema ownership. Nothing in the file forbids that adoption; the file only
  disclaims enforcement.

### F3 — C3: no sibling overlap found within the bounded search; scope text is clean

The C3 preregister scope is the only reachable C3 surface from this seat:
"Both fixed r22 cohorts have exhaustive per-event/component explanation of
rough-versus-lane path counts, frozen digests and declared arithmetic; **does not relabel
old violations** or retry historic checks for confirmation."
`outside_round22.scope`: "Given outside observations are ground truth; r23 **explains**
classifier/unit differences rather than rerunning closure merely to confirm them."
`separability`: "C3 reads frozen r22 evidence and its reconciliation record, never new
C1/C2 production content."

Those words keep C3 explanatory, not owning: it neither renames another lane's
violations nor re-runs the fleet's closure. Combined with the 0-match result for
census/reconciliation terms in the C1/C2 artifact, C3 and C1/C2 do not bleed into each
other. Residual unobserved: the C3 landed document itself (outside read set).

### F4 — no overlap on tooling/gates: the lane's own gate scripts are lane-local

`tools/check-edit-contract.py`, `tools/check-seat-bindings.py`,
`tools/check-path-reconciliation.py` live in the tsukuroi repo and are tsukuroi's own
gates. OUT-010 (tameshi): "Tameshi owns the reusable verification/mutation-testing
method, applied to fleet gates as read-only primary surfaces; **each lane keeps its own
gate**." OUT-006 (kumitate) scopes "OMP task/hub, ufo-fsd scripts & runtime" — fleet
runtime, not a sibling lane's repo-local `tools/`. So writing/running lane-local gate
scripts is *not* a kumitate overlap; it is the explicitly sanctioned arrangement.

### F5 — frontier: no sibling promotion claimed

Line 35: "This deepens held evidence-operability ground, not an uncovered frontier,
repertoire addition or outside promotion." Line 7: observations "establish those finite
metadata shapes, not universal editor semantics or proof of effects." Line 31 disclaims
enforcement, effects, recorder completeness. `preregister.capability_acquisition: false`,
`exploratory: false`, `retired: []`, `ordinal_delta: 0`. The outside r22 entry (422,
CloseKaidoku22) is treated as ground truth, not re-litigated. No frontier overlap found.

## 4. The boundary text that keeps this lane-local (verbatim)

1. Title, line 5: "Structured edit authority for **this lane's evidence files**"
2. Line 9: "**Authority is separately declared lane policy.**" / "Schema-v1 historical bindings remain unchanged and retain all earlier violations. No grant is retroactive."
3. Line 31: "This is declared **post-hoc audit authority only**. It is not native permission enforcement, a sandbox, body/patch interpretation, actual reading or effects proof, complete recorder coverage… The task API still has no restrictive per-seat allowlist."
4. Line 35: "…not an uncovered frontier, repertoire addition or outside promotion."
5. `preregister.separability`: "C1 reads only new decision/prose/source contract; C2 reads only explicit v2 authority and captured events; C3 reads frozen r22 evidence and its reconciliation record, never new C1/C2 production content."
6. `preregister` C2 scope: "legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."
7. `preregister` C3 scope: "does not relabel old violations or retry historic checks for confirmation."
8. `preregister.limits`: "No native per-seat restrictive tool interface exists"; "No historical manifest/report rewrite or retrospective authorization"; "No round24 starts".
9. PROVINCE.md: "**Out of province → report, never absorb.**"; OUT-006 (kumitate owns dispatch/routing semantics); OUT-010 ("each lane keeps its own gate").

Gap in the boundary text: items 1–2 scope the *document* to this lane; item 3 scopes the
*effect*; **nothing scopes the *population* of audited steps to this lane's own seat**,
which is exactly what step 4 (line 29) plus the wave-level `--manifest/--events`
arguments leave open (F1).

## 5. The move (one, non-obvious, cross-round compatible)

**Make the audit population explicitly this-lane, and label the artifact's normative
scope — one sentence, both in the corpus file.**

Proposed single sentence for `structured-edit-r23.md` (lane-local, no decision row
changed):

> "Normative scope: these eight decisions are tsukuroi's audit convention for bindings
> this lane declares, applied only to this lane's own recorded steps; they are not a fleet
> binding-schema definition, and sibling lanes' bindings remain governed by their own
> declarations."

Why this is the non-obvious move rather than a scope trim:
- it **closes F1 without shrinking the claim**: C2's metric is `structured_edit_mode`
  (the mode exists), and the eight rows stay 8 — depth (C1) is untouched;
- it **closes F2 (diffusion)** by making the artifact self-limiting where siblings read
  it, so sibling adoption cannot convert an audit convention into fleet schema ownership,
  which is the second-order harm of the current wording;
- it **pre-empts the kumitate overlap** (OUT-006) by stating that dispatch/binding
  semantics remain kumitate's and that this lane only grades its own evidence steps;
- it **does not touch tameshi's method** (OUT-010) — the controls remain lane-local
  positive/negative checks of this lane's own gate;
- it is **compatible** with sibling r23 proposals because it adds a scope qualifier, not a
  row, a metric, or a tool — sibling C1/C2/C3 artifacts are unaffected.

Affected axes: **adjacency** (primary — sibling-overlap hygiene), **calibration** (no
misattributed verdict cohorts), **operability** (the C2 mode keeps its measured meaning).
Not harmed: **depth** (8 rows unchanged), **coverage**, **freshness**, **operability**
measurement semantics.

Risks, stated plainly:
- If the C2 gate in fact already restricts grading to this lane's seats, the sentence is
  redundant-but-true documentation (low harm); if it does not, the sentence makes the
  code's current behavior a stated divergence — then the remedy must become a code
  restriction, and that file is outside this seat's scope.
- A scope sentence could be read as narrowing C2's reach. Guard: the sentence adds no
  condition to any row, so no row's outcome changes; the metric is mode presence.
- A sibling lane may read the added sentence as tsukuroi narrowing the fleet's semantics.
  Guard: it explicitly disclaims fleet-schema status rather than asserting priority.

## 6. Concrete falsifier for the seam (for L1/Main to run — this seat may not)

**Negative control, one case:** construct a wave `bindings.json`/`events.json` pair
containing a *non-tsukuroi* seat with a schema-v2 `edit_paths` entry whose target is
outside its own read/write sets, plus that seat's recorded structured edit event.
- If the C2 gate grades that event with tsukuroi's rows (ALLOW/DENY/UNKNOWN verdict
  attributed to tsukuroi's decision table), **F1 is confirmed as a live cross-lane
  adjudication** and the sentence alone is insufficient — the gate must restrict grading
  to this lane's seats.
- If the gate skips non-tsukuroi seats entirely (or attributes the verdict to the seat's
  own declaring lane), **F1 is refuted as a live overlap** and the sentence is pure
  documentation.

Second, non-executing falsifier for F2: ask a sibling lane's reader (one grep over a
sibling `corpus/knowledge/`) whether the current file would be cited as the definition of
schema-v2 `edit_paths`; if yes, F2 is live diffusion and the normative-scope sentence is
the smallest in-scope remedy.

## 7. Smallest in-scope remedy (proposal only — this seat writes its report alone)

One sentence added to `structured-edit-r23.md` after line 9 (or as a trailing sentence of
line 31), exactly as quoted in §5. No new row, no metric change, no tool change, no
production file touched by this seat.

## 8. Second-order contradictions left open (not smoothed)

- Document scope ("this lane's evidence files") vs procedure scope ("every captured native
  read/write expansion") — unresolved by the landed text.
- preregister `separability` says C2 reads "captured events" (wave-level by path) while
  the corpus says "this lane's evidence files" (seat-level by intent).
- `preregister.limits` "No native per-seat restrictive tool interface exists" is a global
  negative asserted by this lane about the hub's surface (kumitate's per OUT-006). It is a
  limitation, not an ownership claim, but it will silently go stale if kumitate ships a
  restrictive per-seat allowlist — the sentence should stay a *declared* limitation with a
  date, not a standing fact.

## 9. Honest limits of this seat

- No gate executed (NO-EXEC): C1/C2/C3 measured values are not re-derived here and none
  are asserted.
- No sibling `PROVINCE.md`, no `tools/*.py`, no C3 landed document read (undeclared paths);
  F1 is stated as a seam with an explicit falsifier, F3 is assessed from preregister text
  only, F4/F5 from the declared artifacts.
- Digest above is the supplied declared identity, not independently computed (no hash run).
- No installs or updates were performed or attempted: this seat's NO-EXEC/NO-FETCH scope
  forbids them, and nothing in the task required a tool change.

Reviewed-SHA256: 4e9e79f1ee2f8d5becb039a5669e916c6758860dc9d1a073d61ed9b3fbdd8014
Predicate: r23f-connfxsiblings
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
