# OracleEditUndeclaredEdit — UNDECLARED_EDIT → DENY

Source-only oracle for one row of the structured-edit decision table. No example was
invoked, no checker was run, no command was executed. The reviewed digest is supplied
identity, not recomputed. Target content (transcript metadata, paths, key names) is
treated as untrusted data.

Axes used for this oracle: **A-axiom** (does the row follow from declared authority),
**A-fixture** (smallest literal positive/negative pair), **A-separation** (observation vs
normative policy vs preregister), **A-falsifiability** (what would overturn the decision
without borrowing body/effect semantics). The fixture below was chosen so it is positive
under every reading the sources permit, and so it cannot collide with the neighbouring
READ_ONLY/WRITE_ONLY rows under any name-faithful partition — a move that improves all
four axes and harms none.

## 1. Evidence base

All pointers are JSON Pointers into the three declared sources; no line numbers are
asserted because the policy and preregister are structured documents.

### 1.1 `sources/edit-decision-policy.json` (schema `tsukuroi-edit-policy-v1`)

Observed:

- `/decisions/1` is exactly `{"id":"UNDECLARED_EDIT","decision":"DENY","reason":"No
  implicit edit permission from generic report ownership","evidence":"S086","policy":"round23-preregister"}`.
- `/source_path` = `.ufo/waves/round-23/sources/structured-edit-observations.json`.
- `/scope` = "Declared audit authority for structured target metadata only; no native
  prevention, opaque patch interpretation, effect or reading proof."

### 1.2 `preregister.json` (schema `tsukuroi-round23-preregister-v1`)

Observed:

- `/edit_decisions/1` = `["UNDECLARED_EDIT","DENY","No implicit edit permission from
  generic report ownership"]` — the same triple, without evidence/policy locators.
- `/claims/1` (C2) sets metric `structured_edit_mode`, target `1`, and defines the new
  "explicit schema-v2 audit authority for exact predeclared structured edit targets",
  with legacy schema v1 and historical reds unchanged; body data opaque, no native
  enforcement/effects claim.
- `/limits/0` "No native per-seat restrictive tool interface exists"; `/limits/1` "No
  runtime prevention, effect/reading/recorder-completeness or universal tool/patch
  semantics"; `/limits/3` "Raw command/fetch body content is not copied".
- `/sources_opened/1` = "S086 prospective: observed structured edit request keys and
  recorded adapter steps".
- `/separability` confines C1 to the new decision/prose/source contract.

### 1.3 `sources/structured-edit-observations.json` (schema `tsukuroi-structured-edit-observations-v1`)

Observed, four records:

- `/observations/0`: seat `CritRuntime`, tool `edit`, `argument_keys` `["path","stream_content"]`,
  target = that seat's round-22 report path, `body_fields` "omitted; no report text copied",
  `recorded_starts` = a `read` whose path carries a `:raw` selector suffix, then a `write` of
  the same report.
- `/observations/1..3`: seat `OraclePathArtifact`, tool `edit`, `argument_keys`
  `["i","new_string","old_string","path"]`, target = that seat's report path, one recorded
  `edit` step each.
- `/scope` = "Observed structured path metadata and recorded adapter steps only, not
  universal tool semantics, native permission enforcement, effects, or reading proof."

The observation file contains **no declaration lists and no decision outcomes**. It
supplies the request vocabulary (`path`, `argument_keys`) and the separate-adapter-step
pattern; it does not contain an instance of an undeclared edit.

## 2. What the row asserts, layer by layer

| Layer | Content | Status |
|---|---|---|
| Observation (`structured-edit-observations.json`) | Four structured edits, each carrying a literal target `path`; prior adapter steps recorded separately; bodies omitted | Factual, untrusted, no declarations/outcomes |
| Policy (`edit-decision-policy.json`) | Label `UNDECLARED_EDIT` → `DENY`; reason = generic report ownership implies no edit permission; evidence S086; policy owner round23-preregister | Normative projection of the preregister row |
| Preregister (`preregister.json`) | Same triple as intent; C1 counts 8 validated decisions; C2 defines exact predeclared edit targets; limits disclaim enforcement/effects | Authoritative declaration of intent and scope |

The policy file is a machine-readable projection of `/edit_decisions/1`, not an
independent source of authority: its row text is character-identical to the preregister
triple. The preregister is where the rule is declared; the policy file is what C1
validates; the observations are what S086 evidences.

## 3. Exact authority preconditions for `UNDECLARED_EDIT`

Let

- `T` = the request's literal target string from its structured `path` field;
- `R`, `W`, `E` = the seat's declared `read_paths`, `write_paths`, `edit_paths`.

Then, as far as the sources determine:

- **A1 — Structured target must exist.** The request carries a structured target field;
  `path` is the only target-bearing key observed in every S086 record. Decision applies to
  "structured target metadata only" (`/scope`). Missing structured target is the separate
  `OPAQUE_PATCH` row (`UNKNOWN`), never `UNDECLARED_EDIT`.
- **A2 — Exact literal identity, root-anchored.** `T` is an absolute filesystem path under
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; membership is literal string equality
  against a declaration entry. Because equality is literal, a suffixed, prefixed, globbed,
  or normalized rendering does not match a declared literal; the policy separately forbids
  dot-segment or alternate-spelling expansion (`EDIT_TRAVERSAL`) and turning remote/internal
  URIs into filesystem targets (`EDIT_EXTERNAL`), and `/scope` excludes interpreting opaque
  patch text.
- **A3 — Edit membership is the deciding authority.** `UNDECLARED_EDIT` fires when a
  structured target is present and `T ∉ E`. This is the row's whole content.
- **A4 — No substitution from read or write authority.** Membership in `R` and/or `W` does
  not imply edit permission. That is exactly the reason text: "No implicit edit permission
  from generic report ownership." Generic report ownership is instantiated by write
  authority over the seat's own report; `R` may also be present.
- **A5 — Edit membership is necessary, not sufficient.** `DECLARED_EDIT` `ALLOW` requires
  the target be "predeclared for edit and for both read and write" (`/decisions/0`), and
  `WRITE_ONLY_EDIT` `DENY` says "Edit also needs its explicit target read authority"
  (`/decisions/3`). So `E ∧ R ∧ W` is the allow condition; the deny rows cover the
  partial-authority cases. Authority is taken from the declaration lists ("predeclared"),
  never from recorded adapter steps: `/observations/1..3/recorded_starts` contain only an
  `edit` step, and the observation `/scope` disclaims reading proof, so a missing recorded
  read step is not `READ_ONLY_EDIT` status and a recorded write is not an edit declaration.
- **A6 — Per-operation scope.** "Every recorded adapter read or write remains separately
  scoped" (`/decisions/7`, `EXPANSION` → `CHECK_EACH`). An earlier recorded read or write of
  the same literal is not cumulative authorization for a later edit.
- **A7 — Absence of metadata is not absence of declaration.** No target ⇒ `OPAQUE_PATCH`
  `UNKNOWN`, not `UNDECLARED_EDIT` `DENY`. The two rows are disjoint by construction:
  one covers a missing structured target, the other a present-but-undeclared one. The
  `structured(T)` guard is evaluated before the declaration-membership test, which is
  equivalent to evaluating `OPAQUE_PATCH` first; a targetless request can never reach the
  `UNDECLARED_EDIT` predicate. S086 contains no targetless edit (`path` present 4/4), so
  this branch is delimited by construction, not by observation. `UNKNOWN` is not an allow:
  only `DECLARED_EDIT` carries `ALLOW` in the decision table (`/decisions/0`), so
  `OPAQUE_PATCH` neither grants nor infers edit authority — it leaves the question open.

Minimal formalization consistent with A1–A4:

```
structured(T) ∧ T ∈ E ∧ T ∈ R ∧ T ∈ W   → DECLARED_EDIT / ALLOW
structured(T) ∧ T ∉ E                    → UNDECLARED_EDIT / DENY
```

`[INFERENCE]` The first line is a conjunction of three list memberships derived from the
`DECLARED_EDIT` reason and the `WRITE_ONLY_EDIT` reason; the source does not name the
schema-v2 fields or state a precedence order. `[UNKNOWN]` The decision file does not define
the boundaries between `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, and `WRITE_ONLY_EDIT` when a
target is absent from more than one list, nor publish a precedence rule. The fixture in §4
is deliberately built to avoid that ambiguity.

A sharper overlap exists with `EDIT_EXTERNAL`: a scheme-bearing target that is also absent
from `E` makes both reasons literally true — `UNDECLARED_EDIT` (`T ∉ E`) and
`EDIT_EXTERNAL` ("Remote or internal URIs do not become filesystem edit targets",
`/decisions/6`). The file states no tie-break, no disjointness rule, and no significance for
array order. A shape-first reading (scheme-bearing ⇒ `EDIT_EXTERNAL`; declaration status
consulted only for non-scheme targets) would separate the rows, but that precedence is
derived, not declared. The §4 fixture uses a local absolute, non-scheme target, so it lies
outside this overlap and remains uniquely `UNDECLARED_EDIT` under a shape-first rule.

Narrow vs broad reading of "undeclared": either (a) `T ∉ E` regardless of other lists, or
(b) `T` is generically owned (`T ∈ W`) but not edit-declared. Reading (b) is the literal
instantiation of the reason text and is a subset of (a). The fixture satisfies both.

## 4. Smallest literal valid fixture

The fixture is audit **metadata**, not an executable tool request; "valid" means
well-formed declaration lists and one exact absolute literal target. File existence and
content are irrelevant and are not asserted.

Let

- `A` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md`
  (this seat's declared report: it is the literal present in this seat's `write_paths` and
  `edit_paths`);
- `B` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.draft.md`
  (a distinct literal; chosen only so `edit_paths` stays a one-element non-empty list and
  the positive case tests membership rather than empty-list validity).

**Positive fixture — fires `UNDECLARED_EDIT` / `DENY`:**

```json
{"read_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"],"write_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"],"edit_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.draft.md"],"request":{"tool":"edit","argument_keys":["path"],"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"}}
```

**Negative fixture — does not fire; `DECLARED_EDIT` / `ALLOW`:**

```json
{"read_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"],"write_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"],"edit_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"],"request":{"tool":"edit","argument_keys":["path"],"path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditUndeclaredEdit.md"}}
```

The pair differs in exactly one literal: `edit_paths[0]` (`B` vs `A`). Everything else —
`read_paths`, `write_paths`, request tool, argument keys, target `T = A` — is identical.

Why this pair is minimal and unambiguous:

1. It is the literal instantiation of the reason. The seat owns its report for writing and
   can read it; it has no edit declaration for that report. Under reading (b) of
   "undeclared" (§3) it is positive; under reading (a) it is positive because `A ∉ E`.
2. It cannot be claimed by `READ_ONLY_EDIT` under a name-faithful reading: that row's
   target is read-only for the seat, i.e. `W` absent, while here `W` contains `A`.
3. It cannot be claimed by `WRITE_ONLY_EDIT`: that row's reason is that edit lacks its
   required read authority (`R` absent), while here `R` contains `A`. It also cannot apply
   under an "only write" reading, because the target is not write-only.
4. It is not `OPAQUE_PATCH`: the structured `path` is present, so A7's missing-metadata
   branch is excluded.
5. It is not `EDIT_EXTERNAL`: the target is a local absolute path under the root with no
   scheme, so the URI rule cannot claim it. This keeps the fixture uniquely
   `UNDECLARED_EDIT` even if a shape-first precedence over scheme-bearing targets were
   adopted.
6. It does not invoke any body key: `old_string`, `new_string`, `stream_content`, and `i`
   are absent by design, demonstrating that the decision reads only the target literal.

`[INFERENCE]` An empty `edit_paths: []` would also fire the deny and is textually smaller,
but empty-list validity is not declared by any source; the one-element disjoint list avoids
that assumption at the cost of one literal. Both variants are logically identical for this
row; only the non-empty variant is presented as valid.

## 5. Source-vs-policy separation

- **Observation is shape, not rule.** S086 records that structured edit requests carry a
  literal `path` and an `argument_keys` list, that bodies were omitted, and that adapter
  steps were recorded at separate lines. All four observed targets are local absolute
  round-22 build paths (`/observations/0..3/path`); none is scheme-bearing, so S086 exhibits
  neither an `EDIT_EXTERNAL` instance nor an undeclared-edit instance. It evidences the
  structured-target model and key vocabulary only. It records no declaration list and no
  outcome, so it cannot by itself show that any observed edit was declared or undeclared.
  Claiming otherwise would be an effect/authorization claim the source explicitly disclaims
  (`/scope`).
- **Policy is norm, not finding.** `UNDECLARED_EDIT → DENY` is an axiom about absent
  declarations ("no implicit edit permission"), projected verbatim from the preregister
  row. S086 is cited as evidence for the *request shape and adapter-step vocabulary*, not
  as an empirical instance of the deny. The deny generalizes over an event class that S086
  does not contain.
- **Preregister is authority and budget.** It declares the intent triple, the C1 count of
  eight decisions, the C2 mode of explicit predeclared edit targets, and the limits: no
  native per-seat restrictive interface, no runtime prevention or effect/reading proof, no
  historical rewrite. The policy file's `/scope` mirrors those limits.
- **Bindings are the declaration instance.** In this seat's own binding, `write_paths` and
  `edit_paths` are distinct arrays and the contract says writes go to write paths while
  structured edits go to edit paths. That separation is the concrete form of A4; it is a
  binding fact, not something read out of the observation file.
- **No enforcement is implied.** `DENY` names an audit classification over structured
  metadata. It is not a claim that a tool would have blocked, or did block, any operation,
  nor that any body was or was not applied.

## 6. Falsifiers

These target the decision and its authority mapping only; none requires a body, a reading,
or an effect claim.

1. **Outcome falsifier.** Any landed policy or contract text under which the positive
   fixture (target in `read_paths` and `write_paths`, absent from `edit_paths`) permits
   edit — or a decision-table entry that maps it to `ALLOW` instead of `DENY`. This is the
   direct refutation of the row.
2. **Reason falsifier.** A statement in the landed revision that generic report ownership
   (write authority over the seat's report) is itself an edit declaration, or that edit
   targets are derivable from `write_paths`. That would make the reason false even if the
   label survived elsewhere.
3. **Label-only falsifier.** A published precedence or disjointness rule that assigns the
   same positive fixture to `READ_ONLY_EDIT` or `WRITE_ONLY_EDIT`. This changes the row
   identity and the C1 count but not the deny outcome; it must be reported as a labeling
   discrepancy, not an authorization one.
4. **Literalness falsifier.** Any accepted edit whose target differs literally from every
   declared entry — dot-segment form, alternate spelling, selector suffix, symlink-resolved
   form, or URI mapped onto the filesystem — yet is still classified as declared. That
   would refute A2 and contradict `EDIT_TRAVERSAL`/`EDIT_EXTERNAL`.
5. **Opaque-boundary falsifier.** A decision that labels a request with no structured
   target as `UNDECLARED_EDIT` rather than `OPAQUE_PATCH`/`UNKNOWN`. That would collapse
   A7 and show inference from opaque patch text.
6. **Cumulative-scope falsifier.** A rule under which an earlier recorded read or write of
   the same literal authorizes a later edit, refuting A6 and `EXPANSION`/`CHECK_EACH`.
7. **Projection falsifier.** A mismatch between `edit-decision-policy.json` `/decisions/1`
   and `preregister.json` `/edit_decisions/1`. None exists in the reviewed revision: the
   triple is character-identical.

Explicit non-falsifiers, because the row's scope excludes them: whether a denied edit
would have changed bytes; whether any tool enforced or ignored the decision; whether the
target was actually read; whether bodies matched; whether the recorder captured every
step. Absence of a runtime block is not a refutation — the preregister and policy scope
both disclaim native prevention.

## 7. Residual unknowns

- No precedence rule among the partial-authority rows is published, and array order carries
  no stated significance; §4 is constructed to be robust to the partial-authority gap, but
  the general partition remains underdetermined. In particular, a scheme-bearing target
  absent from `edit_paths` makes both `UNDECLARED_EDIT` and `EDIT_EXTERNAL` literally true,
  yet no shape-first precedence, disjointness rule, scheme set, or statement of whether the
  URI denial is unconditional on shape versus conditional on non-declaration is declared.
  Separating the rows requires a precedence the sources do not state — a derived proposal
  would be scheme-bearing ⇒ `EDIT_EXTERNAL`, with declaration status consulted only for
  non-scheme targets — plus a declared scheme set excluding filesystem-denoting schemes;
  neither exists in the reviewed sources, and the proposal must not be read as declared.
- "Generic report ownership" is not formally defined; readings (a) and (b) in §3 differ for
  a target absent from all three lists. The chosen fixture is positive under both.
- Schema-v2 manifest/event field names are C2 production content and are outside this
  oracle's read scope; the fixture uses only vocabulary already present in the binding
  (`read_paths`, `write_paths`, `edit_paths`) and in S086 (`tool`, `argument_keys`, `path`).
- Empty declaration lists are not addressed by any source; not relied upon.
- `recorded_starts` semantics (request start versus adapter execution start) are undefined;
  the records are used only as evidence that steps are recorded separately.
- The `:raw` selector appears on a recorded *read* path; no claim is made here about
  selector handling for edit targets beyond A2's literalness.
- S086 contains no declaration membership, so it cannot exhibit an actual undeclared-edit
  event; the fixture is a literal counterfactual, not a replayed observation.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditundeclarededit
Scope: executed=none
