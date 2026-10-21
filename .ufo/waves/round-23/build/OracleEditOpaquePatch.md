# Oracle — OPAQUE_PATCH → UNKNOWN (source-only, no execution)

Round 23, seat OracleEditOpaquePatch. Independent source-only oracle for the single policy row
`OPAQUE_PATCH → UNKNOWN`. No command was run, no checker was invoked, no example was replayed,
no network fetch occurred, and no file other than this report was written.

## 0. Axes named (godspeed)

- **A1 Evidentiary basis** — does the cited source actually exhibit this case, or is the row a
  normative abstention rule with no observed instance?
- **A2 Fixture minimality** — the smallest literal structured metadata that separates
  `OPAQUE_PATCH` from its nearest neighbours (`DECLARED_EDIT`, `UNDECLARED_EDIT`,
  `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`).
- **A3 Authority preconditions** — the exact v2 preconditions under which a structured target is
  resolved, and under which read / write / edit authority exists.
- **A4 Source-vs-policy separation** — no policy row is imported into the source record, and no
  recorded event is used as proof that the mapping holds.
- **A5 Falsifiability** — concrete metadata-level observations that would kill the decision or the
  fixture, stated without any body, effect, or reading claim.

## 1. What the row says, and what it does not say

Policy source: `.ufo/waves/round-23/sources/edit-decision-policy.json`
(schema `tsukuroi-edit-policy-v1`). The relevant row, verbatim in substance:

  id: OPAQUE_PATCH
  decision: UNKNOWN
  reason: "Missing structured target is not inferred from opaque patch text"
  evidence: S086
  policy: round23-preregister

The preregister (`.ufo/waves/round-23/preregister.json`, `edit_decisions[4]`) states the same
triple — `OPAQUE_PATCH`, `UNKNOWN`, "Missing structured target is not inferred from opaque patch
text" — so the policy document and the preregister agree on id, decision, and reason.

The document's own scope clause bounds it: "Declared audit authority for structured target
metadata only; no native prevention, opaque patch interpretation, effect or reading proof."
Two consequences are load-bearing:

- The decision is about **structured target metadata**. It is a statement about whether a target
  can be resolved from metadata, not about what a patch body would do.
- "opaque patch interpretation" is explicitly out of scope. So the row forbids *reading* a
  target out of patch text; it does not describe, forbid, or authorise any patch semantics.

## 2. The source record (S086), read literally

`.ufo/waves/round-23/sources/structured-edit-observations.json`
(schema `tsukuroi-structured-edit-observations-v1`) contains exactly four observations, all
`tool: "edit"`:

- CritRuntime / `TsukuroiR22.CritRuntime-3`: `argument_keys: ["path", "stream_content"]`, with
  `path` present and absolute; `body_fields: "omitted; no report text copied"`; `recorded_starts`
  show a `read` of the target then a `write` of the same target.
- OraclePathArtifact / `TsukuroiR22.OraclePathArtifact-3`, three separate observations:
  `argument_keys: ["i", "new_string", "old_string", "path"]`, with `path` present and absolute;
  `body_fields: "omitted; no report text copied"`; `recorded_starts` show a single `edit` step
  each.

Observed facts, and only these:

1. **Every observed edit carries a `path` key.** No observation lacks it.
2. **Target values are absolute literal path strings.**
3. **No body text was captured.** The record states bodies are omitted and no report text was
   copied; the vocabulary `stream_content`, `old_string`, `new_string` appears only as argument
   *key names*, never as content.
4. **Recorded adapter steps are incomplete with respect to read authority.** OraclePathArtifact's
   `recorded_starts` contain an `edit` step but no `read` step for the same path. The record's
   own scope clause says it covers "recorded adapter steps only, not ... reading proof", so a
   missing `read` step is **not** evidence that read authority was absent.

### 2.1 The load-bearing negative finding

**The source contains zero `OPAQUE_PATCH` instances.** All four observed edits carry a structured
target. Therefore:

- The row's *reason* ("missing structured target is not inferred from opaque patch text") is
  consistent with the source's declared limits, because the source itself refuses to supply patch
  text that a target could be inferred from.
- But the row's *trigger* — a request whose structured target is missing — is **not exercised by
  any observed event**. The row is a contract-level abstention rule, not a source-validated
  classification of a recorded request.

Consequence for C1's `validated_edit_decisions` metric: eight rows can be counted as validated
while zero of them (as far as `OPAQUE_PATCH` goes) is backed by a replayed instance. "Validated"
here must mean "the row is internally consistent with the declared source contract", not "an
observed event exercises the row". Reporting the latter would be a fabricated instance.

## 3. Smallest literal metadata fixture

The discriminator is **presence of a target-bearing key in `argument_keys`**, not anything about
the body. `OPAQUE_PATCH` is the case where the target is *not* structured.

### 3.1 Positive fixture (resolves to `OPAQUE_PATCH → UNKNOWN`)

Smallest literal form — one body-only argument key, no target key, target list irrelevant
because no target can be resolved:

  binding:
    read_paths:  ["/abs/target.md"]
    write_paths: ["/abs/target.md"]
    edit_paths:  ["/abs/target.md"]
  event:
    tool: "edit"
    argument_keys: ["stream_content"]
    path: <absent>

Note the fixture is deliberately *binding-saturated*: every list names the same absolute target,
so the only thing that can produce `UNKNOWN` is the absence of the structured target itself. If
the same event were classified `DECLARED_EDIT`, the classifier would be ignoring the missing
target and matching on the patch's presumed content.

### 3.2 Negative fixture (must not resolve to `OPAQUE_PATCH`)

  binding:
    read_paths:  ["/abs/target.md"]
    write_paths: ["/abs/target.md"]
    edit_paths:  ["/abs/target.md"]
  event:
    tool: "edit"
    argument_keys: ["path", "old_string", "new_string"]
    path: "/abs/target.md"

This resolves to `DECLARED_EDIT → ALLOW` (exact target predeclared for edit and for both read and
write), **not** to `OPAQUE_PATCH`. The pair differs in exactly one field: the presence of the
`path` key and its literal value.

### 3.3 Negative control (guards against "absent ⇒ opaque" being vacuous)

  binding:
    read_paths:  ["/abs/other.md"]
    write_paths: ["/abs/other.md"]
    edit_paths:  ["/abs/other.md"]
  event:
    tool: "edit"
    argument_keys: ["path", "old_string", "new_string"]
    path: "/abs/target.md"

This resolves to `UNDECLARED_EDIT → DENY`: a structured target exists and is outside the declared
lists. It must **not** be `OPAQUE_PATCH`, because "not declared" and "not resolvable" are
different facts with different dispositions — the first is a final refusal, the second is an
abstention.

### 3.4 Precedence requirement

The four target-bearing rows (`DECLARED_EDIT`, `UNDECLARED_EDIT`, `READ_ONLY_EDIT`,
`WRITE_ONLY_EDIT`) all presuppose that a structured target exists. `OPAQUE_PATCH` must therefore be
evaluated **first**, on target-resolution failure, and must be **mutually exclusive** with the
four. If the classifier applies the target rows first, a targetless request will fall through to
`UNDECLARED_EDIT → DENY`, and the observable disposition of the row (`UNKNOWN` vs `DENY`) is
wrong even though both block the edit. The policy document states the eight rows as an unordered
array; the precedence is therefore an unstated requirement on the implementing checker.

## 4. Exact authority preconditions

Preconditions under which the decision above holds, each tied to the artefact that carries it:

- **P1 — Target resolution fails on metadata.** No target-bearing key appears in the event's
  `argument_keys`. Source basis: the observed vocabulary distinguishes `path` from the body keys
  `stream_content` / `old_string` / `new_string` (`structured-edit-observations.json`).
  The exact key set is `{"path"}` **as observed**; if the v2 audit authority recognises further
  target-bearing keys, the set is larger (see F1).
- **P2 — Patch text is not an admissible inference source.** Bodies were never captured
  (`body_fields: "omitted; no report text copied"`), and the policy scope excludes "opaque patch
  interpretation". So there is no permitted channel by which a missing structured target could be
  recovered from the request.
- **P3 — Declared authority is literal-list membership, never inferred.** The declared target lists
  are matched by exact absolute string. "No implicit edit permission from generic report
  ownership" (`UNDECLARED_EDIT` reason) forbids promoting report ownership into edit authority.
- **P4 — No spelling expansion.** "No dot-segment or alternate spelling expands the target list"
  (`EDIT_TRAVERSAL` reason). Consequence: an *absent* target cannot be cured by an alternate
  spelling of a declared path, and a *present but differently spelled* target stays
  `UNDECLARED_EDIT`.
- **P5 — UNKNOWN is not an authorisation.** The decision must leave the edit unperformed and the
  case open for source-level resolution. It is neither `ALLOW` nor `DENY`. **Gap:** the policy
  document defines no handling rule for `UNKNOWN`; nothing in it says "unknown does not permit".
  A checker that treats a non-`DENY` outcome as permitted would make `UNKNOWN` a silent `ALLOW`,
  which is exactly the inference the row exists to prevent.
- **P6 — Authority is declaration, not observed behaviour.** Read authority is a fact of the
  binding's `read_paths` list, not of the recorded adapter steps. The OraclePathArtifact
  observations have an `edit` step and no `read` step; that absence is unproven read state and
  must not be read as `READ_ONLY_EDIT`.
- **P7 — Metadata only.** No claim about patch body, applied effect, file content afterwards, or
  whether the target was ever read.

Authority-shape caveat, stated as an assumption rather than a finding: the three-way
`read_paths` / `write_paths` / `edit_paths` split used in the fixtures above is taken from the
schema-v2 seat-binding payload carried in this assignment, and the policy row
`DECLARED_EDIT` independently implies the three dimensions ("predeclared for edit **and** for both
read and write", with the two one-sided rows `READ_ONLY_EDIT` and `WRITE_ONLY_EDIT` each denying
exactly one missing dimension). The v2 schema document itself was **not** among the declared read
paths for this seat, so the fixture's field names are an inference from the binding payload plus
the policy reasons, not a quotation of the schema. See F2.

## 5. Source-vs-policy separation

| Layer | Carries | Must not carry |
|---|---|---|
| Source (S086, `structured-edit-observations.json`) | Observed `argument_keys`, literal absolute `path` values, `recorded_starts`, transcript digests, request line, call id | Patch bodies, effect, universal tool semantics, native enforcement, reading proof |
| Policy (`edit-decision-policy.json`) | id → decision mapping, reasons, `evidence: S086`, `policy: round23-preregister`, scope disclaimer | Any recorded event, any claim that an instance of the row was observed |

How this oracle used them:

- The source was used **only** to fix the metadata vocabulary (what a target key looks like, what
  a body key looks like, that bodies are not captured) and to establish the fact that no observed
  instance exists.
- The policy was used **only** for the mapping and for the reasons that constrain it.
- The mapping was not validated by pointing at a recorded event, because no recorded event
  exercises it. The positive fixture in §3.1 is a **constructed** metadata fixture, and is labelled
  as such.
- No policy sentence was rewritten into the source record, and no source field was treated as
  carrying a decision.

Wave-level separation (preregister `separability`): `OPAQUE_PATCH` is C1 content — a decision/prose
contract row. The v2 authority preconditions (P1–P4) are C2 content — explicit v2 authority and
captured events. The frozen round-22 path census (C3) bears on neither and was not read. This
oracle's §2 observation that the source has no `OPAQUE_PATCH` instance is a C1 statement about the
C1 evidence base; it makes no claim about the C2 event corpus or the C3 census, and the row's
`UNKNOWN` disposition must not be re-derived from either.

## 6. What would falsify this decision (metadata level only)

- **F1 — Wider target vocabulary.** If the v2 audit authority recognises target-bearing keys
  beyond `path` (for example a `file` or `target_path` key), then "missing structured target" must
  be evaluated against that wider set, and the §3.1 fixture's single `stream_content` key would no
  longer be targetless. Falsifies the fixture, not the row.
- **F2 — Authority shape differs.** If the v2 schema derives edit authority by inheritance (for
  example `edit_paths` inheriting from `write_paths`, or read authority implied by report
  ownership), then P3/P6 and the fixture binding block are wrong, and the three-dimension matrix
  behind `DECLARED_EDIT` / `READ_ONLY_EDIT` / `WRITE_ONLY_EDIT` must be restated. Falsifies §4.
- **F3 — UNKNOWN treated as permissive.** If any checker or document treats a non-`DENY` outcome
  as permitting the edit, the abstention collapses into a hidden allow and the row's reason is
  defeated. Falsifies the operative meaning of the decision. (P5 gap; this is the most consequential
  live risk.)
- **F4 — A targetless edit is classified by target-based rows.** If an event lacking a target key
  is reported as `DECLARED_EDIT`, `UNDECLARED_EDIT`, `READ_ONLY_EDIT` or `WRITE_ONLY_EDIT`, then
  the taxonomy's mutual exclusivity and the precedence requirement of §3.4 are broken.
- **F5 — OPAQUE defined over body opacity instead of target opacity.** All four recorded
  observations have `body_fields: "omitted; no report text copied"` *and* a structured `path`. If
  "opaque" were taken to mean "body not recorded", every observed edit would be `OPAQUE_PATCH` and
  `DECLARED_EDIT` would become unreachable — falsifying the eight-row taxonomy's separability.
  The row's own wording ("missing structured target") forbids this reading; a checker that
  implements it would be the defect.
- **F6 — A recorded instance appears.** A later captured event with an edit whose `argument_keys`
  contain no target key would turn the row from a contract-level rule into a source-validated
  classification. That would *strengthen* the row, and would also require the §3.1 fixture to be
  re-derived from the real vocabulary rather than constructed.
- **F7 — Normalisation contradicts literal matching.** If the checker normalises paths before
  matching the declared lists (resolving `.`/`..`, symlinks, or trailing separators), then P3/P4
  fail, `EDIT_TRAVERSAL`'s denial becomes unenforceable at the metadata level, and the exact-string
  negative fixture in §3.3 could flip to `DECLARED_EDIT`.

## 7. Residual risk and verification gaps

- **No instance coverage.** The row's trigger is unexercised in S086 (§2.1). Nothing in the
  available sources demonstrates that the checker classifies a targetless edit as `UNKNOWN`; the
  decision is currently a declared contract, not an observed behaviour. This gap cannot be closed
  by reading the frozen sources further — it needs either a constructed fixture run against the
  checker (out of this seat's scope) or a future captured event.
- **UNKNOWN handling is unspecified.** P5 is an inference from the row's disposition and from the
  policy's own disclaimer, not an explicit rule in the document.
- **Precedence is unstated.** §3.4's requirement is derived from the semantic presupposition of
  the four target-bearing rows, not from an explicit ordering statement in the policy file.
- **v2 schema not read.** The three-list authority shape is inferred (see §4 caveat, F2).
- **Enforcement and effects remain out of scope.** No claim is made that any runtime prevents the
  edit, that a patch body means anything, that a write took effect, or that a target was read. The
  policy scope and the source scope both disclaim these, and this oracle adds nothing to them.
- **Baseline.** All statements are anchored to the round-23 preregister baseline and to the three
  declared read artefacts; no other file was consulted.

## 8. Lane bounds (informational)

This seat is a leaf member of round 23; it dispatched no subagent, opened no extra filesystem
path beyond its declared read list, and executed no command and no fetch.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditopaquepatch
Scope: executed=none
