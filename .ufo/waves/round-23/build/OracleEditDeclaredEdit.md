# OracleEditDeclaredEdit — source-only oracle for `DECLARED_EDIT -> ALLOW`

Round 23 / attempt 1. Seat binding: leaf member, no dispatch. Scope of this document is the
single policy row `DECLARED_EDIT` in `.ufo/waves/round-23/sources/edit-decision-policy.json`,
cross-read against the round-23 preregister and the S086 observation source it cites.

All digests below are **supplied declarations**, not independently computed. No command was
executed, no example or checker was invoked, no file outside the seat's declared read/write
paths was opened, and no network or subprocess surface was used.

## 0. Axes

1. **Literal identity** — is the target match exact (byte-identical absolute path) or fuzzy
   (prefix, basename, directory, normalized)?
2. **Authority completeness** — which independent grants must co-exist for an edit to be
   declared, and which single missing grant produces a different decision id?
3. **Source/policy separation** — which facts come from observed metadata (S086) and which
   come from a decision table / preregister, and can either alone establish the row?
4. **Falsifiability** — what observation would make `ALLOW` demonstrably wrong without any
   claim about body content or effect.
5. **Honesty of scope** — what this row does *not* assert (runtime enforcement, body/effect
   semantics, reading proof, universal tool semantics).

## 1. The row, quoted from source

`edit-decision-policy.json`, `decisions[0]`:

    "id": "DECLARED_EDIT",
    "decision": "ALLOW",
    "reason": "Exact target is predeclared for edit and for both read and write",
    "evidence": "S086",
    "policy": "round23-preregister"

`preregister.json`, `edit_decisions[0]`, the same triple in array form:

    ["DECLARED_EDIT", "ALLOW", "Exact target is predeclared for edit and for both read and write"]

File-level scope statement of the policy (verbatim intent): *"Declared audit authority for
structured target metadata only; no native prevention, opaque patch interpretation, effect or
reading proof."* The policy also declares its own provenance pointer
`source_path: .ufo/waves/round-23/sources/structured-edit-observations.json` and pins
`schema: tsukuroi-edit-policy-v1`.

### 1.1 Cross-source agreement on this row (and on all eight)

Comparing `edit-decision-policy.json` `decisions[*]` against `preregister.json`
`edit_decisions[*]`: the eight rows agree in **id, decision value, reason text and order**.
The policy adds `evidence` and `policy` keys and drops the array nesting; it does not restate
or alter any reason. The preregister's `sources_opened` binds `S086` to *"observed structured
edit request keys and recorded adapter steps"*, matching the policy's `evidence: "S086"`.

**Finding A (low, structural).** The same eight decisions are carried in two places. A metric
of "8 validated edit decisions" can be satisfied while the *reason* strings drift between the
two carriers. The reconciliation invariant that must hold — and that a checker should assert —
is: for i in 0..7, `policy.decisions[i].(id, decision, reason) == preregister.edit_decisions[i]`
as an ordered triple. This report verified that invariant by reading both files; it did not
execute anything.

## 2. Source vs. policy separation

| Layer | File | What it actually contributes | What it cannot contribute |
|---|---|---|---|
| Observed source (S086) | `.ufo/waves/round-23/sources/structured-edit-observations.json` | Shape of a structured edit request as *metadata*: `seat`, `agent`, `transcript_sha256`, `request_line`, `call_id`, `tool`, `argument_keys`, `path`, `body_fields`, `recorded_starts`; plus the observed adapter-step vocabulary (`read`, `write`, `edit`) | Any grant; any decision; any body content (`body_fields` is literally recorded as *"omitted; no report text copied"*); any universal tool/patch semantics (its own `scope` line says so) |
| Decision table | `.ufo/waves/round-23/sources/edit-decision-policy.json` | The mapping decision-id → decision value + reason, and the declared scope limits | Evidence of any individual instance; authority over any concrete path |
| Claim registration | `.ufo/waves/round-23/preregister.json` | The 8 triples, the C1/C2/C3 claims and their declared metrics/commands, `limits`, `separability` | The binding data itself |
| Authority carrier | seat binding (shape as supplied in this seat's binding: `name`, `root`, `read_paths`, `write_paths`, `edit_paths`, `commands`, `fetches`) | Which exact paths a named seat may read / write / edit | Effects; native enforcement; per-seat behaviour of any tool |

**Finding B (medium, separation).** The policy row cites `evidence: "S086"`, but S086 contains
**no binding and no authority facts whatsoever** — it contains only observed request metadata
and recorded adapter steps. Therefore S086 can support the *vocabulary and shape* of the
`DECLARED_EDIT` case (a structured edit request carrying an explicit target path, with
recorded read/write/edit starts), but it cannot supply the predicate that the row actually
tests ("is predeclared"). The predicate's data lives in the C2 lane (explicit v2 edit-target
audit authority), while the row text lives in the C1 lane. This is consistent with the
preregister's declared `separability` ("C1 reads only new decision/prose/source contract; C2
reads only explicit v2 authority and captured events"), and it means:

- A checker that evaluates `DECLARED_EDIT` must read both a decision table (C1) and a
  binding/authority artifact (C2). A decision-table-only checker can count 8 declared rows but
  cannot distinguish `DECLARED_EDIT` from `UNDECLARED_EDIT`, `READ_ONLY_EDIT`,
  `WRITE_ONLY_EDIT`, `EDIT_TRAVERSAL`, `EDIT_EXTERNAL` or `OPAQUE_PATCH` — those are
  separated *only* by the authority facts.
- Consequently `C1.target = 8` (validated_edit_decisions) is a **document** claim, and C2's
  `structured_edit_mode = 1` is the **evaluation** claim. Reading C1's metric as "8 runtime
  behaviours repaired" would be false; the preregister's own `scope` for C1 says "new document
  contract, not eight repaired runtime behaviors."

**Finding C (low, provenance hygiene).** `policy.source_path` is repo-relative
(`.ufo/waves/round-23/sources/structured-edit-observations.json`) while every path in the
observation records and in the seat bindings is absolute. Two consequences: (i) the relative
string is a **provenance pointer, not an edit target** — no seat's `edit_paths` grants editing
the policy or the source by virtue of this pointer; (ii) any implementation that folds
`source_path` into a candidate-target list would be doing exactly what `EDIT_EXTERNAL`/
`EDIT_TRAVERSAL` deny. Flag for the implementing lane, not a defect in the row.

## 3. Authority preconditions for `DECLARED_EDIT -> ALLOW`

Derived by reading the reason text of the row together with the sibling rows it must not
collide with. Each precondition below is stated so that dropping exactly one of it yields a
**different named decision id** in the same table — that is the test of a well-formed
precondition set.

- **P1 — Target is a filesystem path, not a URI.** Remote/internal URI forms do not become
  edit targets (`EDIT_EXTERNAL` → DENY). The policy's own scope names "remote or internal
  URIs".
- **P2 — No dot-segment or alternate spelling.** The declared target and the requested target
  must be the *same* path; no dot-segment, `..`, symlink-ish or alternate spelling expands the
  target list (`EDIT_TRAVERSAL` → DENY).
- **P3 — Structured target present.** The request must expose an explicit target in metadata.
  If the target is only inside opaque patch text, there is no structured target to adjudicate
  (`OPAQUE_PATCH` → UNKNOWN, deliberately *not* DENY and *not* ALLOW).
- **P4 — Edit authority.** The exact path is predeclared for edit by this seat.
- **P5 — Read authority.** The exact path is predeclared for read by this seat.
- **P6 — Write authority.** The exact path is predeclared for write by this seat.
  (P4+P5+P6 is the literal reading of *"predeclared for edit and for both read and write"*:
  the edit grant plus read and write over the same target.)
- **P7 — No implicit grant.** If the exact path is absent from the seat's declaration,
  generic role defaults, report ownership, or "this file obviously belongs to me" do **not**
  grant it (`UNDECLARED_EDIT` → DENY). Per-seat literal binding is narrower than role
  defaults.
- **P8 — Seat identity.** The declared grant belongs to the seat named on the event; a grant
  held by a sibling seat, a parent seat, or another wave's seat does not transfer.
- **P9 — Per-item scoping under expansion.** If one request carries multiple recorded
  adapter reads/writes, `ALLOW` applies **per recorded item**, each item independently
  satisfying P1–P8 (`EXPANSION` → CHECK_EACH). A blanket ALLOW over the whole request is
  outside the table.

**Minimality caveat on P4–P6 (Finding D, medium).** The reason wording admits two readings:
(i) `edit_paths` is a third, independent grant, so the minimal positive fixture needs the path
in three lists; or (ii) `write_paths` *is* the edit grant and `edit_paths` merely restates
it, so two lists suffice. The seat-binding shape supplied to this seat carries `write_paths`
and `edit_paths` as distinct keys with identical content for this seat's draft path, so both
are present in the smallest observed instance. **S086 contains no binding data**, so source
evidence cannot decide between (i) and (ii). The minimal fixture below therefore states both
variants and marks the reduction as unverified. Whoever implements the C2 checker must fix
this in the schema contract; an implementation that requires all three lists when the schema
guarantees edit ⊆ write would reject valid positives, and one that requires only one list
would accept `WRITE_ONLY_EDIT`/`READ_ONLY_EDIT` positives.

**Reading-authority vs. reading-proof (Finding E, medium).** P5 is a *declaration* predicate
("the seat is authorized to read this target"), not an *observation* predicate ("a read of this
target is recorded"). The two are not interchangeable and the source shows why:

- The observation records contain `recorded_starts` entries such as a read at
  `…/round-22/build/CritRuntime.md:raw` — a **read-view selector suffix** — followed by a
  write at `…/round-22/build/CritRuntime.md` with no suffix.
- Therefore the string that appears in a recorded read start is not byte-identical to the
  plain declared path. If authority matching were done by literal string equality over every
  recorded start string, the observed read start would fail to match a plainly declared
  target; if matching strips a trailing selector, the observed read start matches.
- Neither the row text nor the policy scope states which is intended, and the policy scope
  explicitly disclaims *reading proof*. The defensible reading, and the one consistent with
  "Exact target", is that **target identity** is the plain filesystem path and a read-view
  selector is not an alternate spelling of the target (P2 governs alternate spellings of the
  *path*, not read selectors). [INFERENCE] — the implementation must state this explicitly,
  because a naive equality check over recorded starts will reject the S086-observed shape.

## 4. Smallest literal fixtures (metadata only)

These are the minimal metadata fragments that separate `DECLARED_EDIT -> ALLOW` from every
sibling row. They are stated as literal values, not as a schema, because the v2 binding and
event schemas are C2-lane artifacts that this source-only oracle was not given. Field names
follow the seat-binding shape supplied to this seat (`read_paths`, `write_paths`,
`edit_paths`) and the S086 observation record shape; every use of them here is a proposal,
not a claim about the landed v2 schema.

### 4.1 Smallest valid positive (variant A — three independent grants)

  seat_binding:
    seat: "<seat>"
    read_paths:  ["/abs/root/.ufo/waves/round-23/build/<name>.md"]
    write_paths: ["/abs/root/.ufo/waves/round-23/build/<name>.md"]
    edit_paths:  ["/abs/root/.ufo/waves/round-23/build/<name>.md"]

  event:
    seat: "<seat>"
    tool: "edit"
    argument_keys: ["path"]
    path: "/abs/root/.ufo/waves/round-23/build/<name>.md"

  why minimal: `tool` + `argument_keys` establish "structured edit request"; `path` is the
  target; the three path lists are exactly P4+P5+P6; `seat` is exactly P8. Nothing else in the
  S086 record shape is load-bearing for this row — `transcript_sha256`, `request_line`,
  `call_id`, `agent`, `body_fields`, `recorded_starts` are provenance/context, not predicates.

### 4.2 Smallest valid positive (variant B — write is the edit grant)

  seat_binding:
    seat: "<seat>"
    read_paths:  ["/abs/root/.ufo/waves/round-23/build/<name>.md"]
    write_paths: ["/abs/root/.ufo/waves/round-23/build/<name>.md"]

  event:
    seat: "<seat>"
    tool: "edit"
    argument_keys: ["path"]
    path: "/abs/root/.ufo/waves/round-23/build/<name>.md"

  Difference from A: only the `edit_paths` list is dropped. This variant is admissible only if
  the v2 schema guarantees the edit grant is implied by `write_paths` (Finding D). If the
  schema does not guarantee that, variant B is not a positive and the row's minimal positive is
  variant A.

### 4.3 Smallest valid negatives — one predicate removed each

  N1 UNDECLARED_EDIT (P7 dropped):
    read_paths: [], write_paths: [], edit_paths: []
    event path: "/abs/root/other.md"      -> DENY ("No implicit edit permission from generic report ownership")

  N2 READ_ONLY_EDIT (P6 dropped):
    read_paths: ["/abs/root/t.md"], write_paths: [], edit_paths: ["/abs/root/t.md"]
    event path: "/abs/root/t.md"          -> DENY ("Read authority never grants a write")

  N3 WRITE_ONLY_EDIT (P5 dropped):
    read_paths: [], write_paths: ["/abs/root/t.md"], edit_paths: ["/abs/root/t.md"]
    event path: "/abs/root/t.md"          -> DENY ("Edit also needs its explicit target read authority")

  N4 EDIT_TRAVERSAL (P2 broken):
    read_paths: ["/abs/root/t.md"], write_paths: ["/abs/root/t.md"], edit_paths: ["/abs/root/t.md"]
    event path: "/abs/root/./t.md"        -> DENY ("No dot-segment or alternate spelling expands the target list")

  N5 EDIT_EXTERNAL (P1 broken):
    event path: "agent://<peer>"  |  "http://host/x"  |  "proc://<job>"  |  "xd://<tool>"
    -> DENY ("Remote or internal URIs do not become filesystem edit targets")

  N6 OPAQUE_PATCH (P3 dropped):
    event: tool "edit", argument_keys without "path" (target only inside body text)
    -> UNKNOWN ("Missing structured target is not inferred from opaque patch text")

  N7 EXPANSION (P9):
    event records two adapter steps, one with a declared target and one with an undeclared target
    -> CHECK_EACH: ALLOW for the declared item, DENY for the undeclared item, never ALLOW for the pair

Each negative differs from the positive in exactly one predicate, so each exercises exactly one
row of the table. That is the property that makes the eight rows non-overlapping.

### 4.4 Source-shape constraints the fixtures must respect

From `structured-edit-observations.json` (S086) — these are the shapes a fixture must not
contradict:

- **Adapter variance.** Observed edit argument keys are `["path","stream_content"]` (seat
  `CritRuntime`) and `["i","new_string","old_string","path"]` (seat `OraclePathArtifact`).
  Two different edit interfaces exist in the observed corpus. Therefore the fixture must NOT
  hard-code `old_string`/`new_string`; the only invariant across observed adapters is that a
  path argument key is present. A checker that requires the
  `i/new_string/old_string/path` quartet would reject an observed legitimate edit shape, and
  one that requires `path`+`stream_content` would reject the other. [INFERENCE] the predicate
  is "argument keys contain a path-shaped argument", not a fixed key set.
- **Step vocabulary.** `recorded_starts` entries observed are `read`, `write`, `edit`. The
  `EXPANSION` row says "Every recorded adapter read or write remains separately scoped" —
  i.e. the itemization is over the recorded steps, and the `read` step carries a `:raw`
  selector suffix (Finding E).
- **Bodies are absent by construction.** `body_fields` is recorded as *"omitted; no report
  text copied"*, and the preregister `limits` include *"Raw command/fetch body content is not
  copied"*. Therefore a metadata-only decision is the only decision this source can support;
  any implementation that reads body text to decide would be operating outside both the
  observation schema and the stated scope.
- **Seat identity is present on the record.** Both `seat` and `agent` are recorded, so P8 is
  checkable from the source shape.

## 5. What would falsify `DECLARED_EDIT -> ALLOW`

Each item below is an observable that would make the row demonstrably wrong. None of them
requires, and none is offered as, a claim about body content or about effect.

- **F1 — Declaration-vs-decision collapse.** A seat binding that declares the exact path for
  read only, yet whose event is classified `DECLARED_EDIT / ALLOW`. Then the row is not
  separating `READ_ONLY_EDIT` and the table's four DENY reasons are decorative.
- **F2 — Write-only accepted.** A seat binding that declares the exact path for write only
  (no read), classified ALLOW. Breaks `WRITE_ONLY_EDIT`.
- **F3 — Fuzzy identity.** An event whose path matches a declared path only by prefix,
  directory, basename, or a normalized form, classified ALLOW. Breaks "Exact target" and
  smuggles in `EDIT_TRAVERSAL`.
- **F4 — Alternate spelling accepted.** A dot-segment or otherwise differently-spelled but
  same-file path classified ALLOW. Breaks `EDIT_TRAVERSAL` directly.
- **F5 — URI accepted.** A `agent://`/`http://`/`proc://`/`xd://` path classified ALLOW.
  Breaks `EDIT_EXTERNAL`.
- **F6 — Opaque patch resolved.** An event with no structured path argument classified ALLOW
  (rather than UNKNOWN), i.e. a target was inferred from patch text. Breaks `OPAQUE_PATCH`.
- **F7 — Blanket expansion.** A multi-step request where one recorded step's target is
  undeclared, and the whole request is ALLOW without per-item scoping. Breaks
  `EXPANSION/CHECK_EACH`.
- **F8 — Implicit grant.** A path absent from the seat's declaration but covered by a generic
  role default or by report ownership, classified ALLOW. Breaks `UNDECLARED_EDIT` and the
  "per-seat literal binding is narrower than generic role defaults" rule.
- **F9 — Cross-seat leakage.** A seat's request ALLOWed on the strength of a grant held by a
  different seat. Breaks P8.
- **F10 — Row-text drift.** The eight triples in `edit-decision-policy.json` and the eight in
  `preregister.json` disagreeing in id, decision value, reason, or order, while both are
  reported as "8 validated decisions". Breaks Finding A's reconciliation invariant.
- **F11 — Overreach into effect or enforcement.** Any artifact or report asserting that the
  ALLOW outcome is *enforced* by tooling, or that it proves the edit body was correct, was
  applied, or was read-then-written. This falsifies the policy's declared scope
  (`no native prevention ... effect or reading proof`) and the preregister's limit
  *"No native per-seat restrictive tool interface exists"* — the table is an audit authority
  over metadata, not a runtime gate.
- **F12 — Cross-lane contamination.** A C3-path reconciliation or an r22 historical artifact
  being rewritten, relabeled, or re-authorized by this row's landing. Falsifies the
  preregister's `separability` and the limit *"No historical manifest/report rewrite or
  retrospective authorization"*.

**What is deliberately NOT falsifiable here:** whether the body was correct, whether the write
succeeded, whether the file now contains what was intended, whether the recorded adapter steps
were complete, and whether any tool would have refused the operation. This source supports
none of those, and this report asserts none of them.

## 6. Residual risk and verification gaps

1. **Finding D (schema-level, unresolved).** Whether `edit_paths` is an independent grant or a
   restatement of `write_paths` cannot be settled from S086 or the decision table. The
   implemented checker will pick one silently unless the schema contract states it. Highest
   practical impact: it decides whether the minimal positive fixture has two or three lists.
2. **Finding E (selector semantics, unresolved).** The S086-observed read start carries a
   `:raw` suffix that is not byte-identical to the plain declared path. A literal-equality
   implementation over recorded start strings will reject observed legitimate shapes. The
   intended rule must be written down explicitly ("target identity is the plain path; a
   read-view selector is not an alternate spelling").
3. **Row-text duplication.** Two carriers, one set of eight decisions; no observed mechanism
   forces them to stay equal (Finding A).
4. **Predicate set is derived, not quoted.** P1–P9 are reconstructed from the reason text plus
   the requirement that each sibling row be separated by exactly one dropped predicate. If the
   landed v2 schema names or orders grants differently, the *content* of P4–P6 may shift even
   though the row text is unchanged.
5. **Evidence coverage is thin by construction.** Four observation records across two seats.
   The `stream_content` vs `old_string/new_string` split shows at least two adapter
   interfaces; the corpus does not establish that two is the complete set.
6. **No native enforcement is asserted anywhere.** The preregister limit is explicit: no
   native per-seat restrictive tool interface exists. Any downstream text that implies runtime
   prevention contradicts the source and must be corrected at the source-of-truth layer.
7. **Nothing here was executed.** `tools/check-edit-contract.py`, `tools/check-seat-bindings.py`
   and `tools/check-path-reconciliation.py` are named in the preregister as the declared
   commands for C1/C2/C3; none was invoked, consistent with this seat's empty command and
   fetch lists and its NO-EXEC/NO-FETCH scope.

## 7. Conclusion (recommendation, not adjudication)

`DECLARED_EDIT -> ALLOW` is **consistent** with the source as read: the row's stated
precondition ("exact target predeclared for edit and for both read and write") is expressible
over the metadata the observation source actually carries, and it is separable from all seven
sibling rows by dropping exactly one predicate each (§4.3). Two implementation-critical points
are not settled by the source and must be fixed in the v2 schema contract before the row can be
*evaluated* rather than merely *declared*: whether `edit_paths` is independent of
`write_paths` (Finding D), and whether read-view selectors participate in target identity
(Finding E). This report is a recommendation only; it edits no production file, changes no
contract, and adjudicates nothing.

Report: .ufo/waves/round-23/build/OracleEditDeclaredEdit.md

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditdeclarededit
Scope: executed=none
