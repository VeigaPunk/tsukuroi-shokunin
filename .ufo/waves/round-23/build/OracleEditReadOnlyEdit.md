# OracleEditReadOnlyEdit — source-only oracle for `READ_ONLY_EDIT -> DENY`

Round 23, attempt 1. Seat: `OracleEditReadOnlyEdit`. Lane: leaf member (no subagent dispatch).
Scope of this document: **source-only** derivation from the declared read set. No command was
executed, no file was hashed, no checker or example was invoked, no manifest outside the declared
read set was opened. Every statement below is derived by reading the four declared local files and
the in-context seat-binding literal.

## 0. Sources used (declared identity, not independently computed)

| Ref | Path | Role |
|---|---|---|
| P1 | `.ufo/waves/round-23/sources/edit-decision-policy.json` | Policy layer: the decision table under review (`schema: tsukuroi-edit-policy-v1`) |
| P2 | `.ufo/waves/round-23/preregister.json` | Round policy of record: claims C1/C2/C3, the 8 `edit_decisions` triples, `separability`, `limits` |
| P3 | `.ufo/waves/round-23/sources/structured-edit-observations.json` | Source layer (the policy's own `source_path`): observed structured path metadata (S086) |
| P4 | `.ufo/waves/round-23/sources/godspeed-directive.txt` | Godspeed directive (copied directive; `skill://godspeed` also read) |
| P5 | in-context seat-binding literal | A literal round-23 schema-v2 per-seat binding shape (`name`, `root`, `read_paths`, `write_paths`, `edit_paths`, `commands`, `fetches`) |

Not read (outside this seat's declared `read_paths`): `tools/check-edit-contract.py`,
`tools/check-seat-bindings.py`, `.ufo/waves/round-23/<WAVE>/bindings.json`,
`.ufo/waves/round-23/<WAVE>/events.json`, and any schema document for the v2 binding. Consequently
**no claim below is certified "checker-valid"**; the fixtures are *decision-minimal* and are stated
against the literal shape in P5, with every schema assumption flagged.

## 1. Oracle verdict (source-only)

`READ_ONLY_EDIT -> DENY` is **consistent** with P1/P2/P3, subject to three declared-shape
preconditions that P1 does not state explicitly (positive read membership; write authority as the
union of the two write-ish lists; the id depends on the *edit/write* event kind, not on the target
merely being read-only). The DENY direction itself is the only direction the readable corpus
supports, and it is the direction the policy states. The corpus contains **no read-only-authority
instance at all** (see F1), so this id is structurally derived rather than observationally
exemplified. No body, effect, enforcement, blocking, or reading-proof claim is made or implied.

### 1.1 What the policy actually says (P1, row 3)

    "id": "READ_ONLY_EDIT", "decision": "DENY",
    "reason": "Read authority never grants a write",
    "evidence": "S086", "policy": "round23-preregister"

P2 carries the same eight rows positionally as `edit_decisions` triples `[id, decision, reason]`
and C1 scopes them as "Eight finite source-grounded structured-edit authority decisions; new
document contract, not eight repaired runtime behaviors."

### 1.2 The four-quadrant partition (derived from P1 rows 1-4)

P1's first four reasons partition the (read-authority, write-authority) membership of one target
path in one seat binding:

| `P ∈ read set` | `P ∈ write set` | id | decision |
|---|---|---|---|
| yes | yes | `DECLARED_EDIT` | ALLOW |
| no | no | `UNDECLARED_EDIT` | DENY |
| yes | no | `READ_ONLY_EDIT` | DENY |
| no | yes | `WRITE_ONLY_EDIT` | DENY |

The two ALLOW-side reasons are symmetric and jointly conjunctive: `DECLARED_EDIT` requires the
target be "predeclared for edit and for both read and write"; `WRITE_ONLY_EDIT`'s reason states
"Edit also needs its explicit target read authority". Hence **an edit needs both memberships**, and
each of the four quadrants is a distinct id. This is the tightest reading of the policy and is the
basis for the fixtures in §4.

## 2. Source-vs-policy separation

Three layers, three owners, distinct jobs:

1. **Policy layer (P1)** — the *rule table*. Owns the id → decision mapping, one line of human
   reason each, an `evidence` pointer (`S086`) and a `policy` pointer (`round23-preregister`). P1
   declares its own scope: "Declared audit authority for structured target metadata only; no native
   prevention, opaque patch interpretation, effect or reading proof." P1 also names its own
   `source_path` → P3. P1 states **no field names, no schema, no precedence, no examples**.
2. **Source layer (P3, = S086)** — the *observations*. Owns observed structured path metadata:
   per record `seat`, `agent`, `transcript_sha256`, `request_line`, `call_id`, `tool`,
   `argument_keys`, `path`, `body_fields`, `recorded_starts[]`. Its scope line: "Observed
   structured path metadata and recorded adapter steps only, not universal tool semantics, native
   permission enforcement, effects, or reading proof." Bodies are deliberately not copied
   (`"body_fields": "omitted; no report text copied"`).
3. **Round policy of record (P2)** — the *plan and bounds*. Owns the three claims, the metric
   before/target pairs, `separability` ("C1 reads only new decision/prose/source contract; C2 reads
   only explicit v2 authority and captured events; C3 reads frozen r22 evidence…"), the eight
   triples, and `limits` (no native per-seat restrictive tool interface; no runtime prevention,
   effect/reading/recorder-completeness or universal tool/patch semantics; no historical
   manifest/report rewrite or retrospective authorization; no round24 starts).

**Separation result.** The separation *is* clean along the "who decides vs who observes" axis: the
policy decides only over metadata classes, the source supplies only observed metadata, the
preregister supplies only bounds and the audit plan. But the readable corpus contains a **third
artifact type that the policy scores and the readable source does not supply: the authority
record**. P1 scores *declared authority* (membership in a seat's read/write lists). P3 supplies
*tool-call metadata* (what an adapter step did), not *authority metadata* (what a seat was
permitted to do). The bridge — the schema-v2 bindings/events manifests named in P2's C2 command
(`--manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`)
— is outside this seat's declared read set. Therefore the two policy premises below are inferred
from the shape of P5 and the wording of P1, not read off a source record:

- **P-A (union write set).** `W(B) = B.write_paths ∪ B.edit_paths`. The binding literal in P5 lists
  the same path under both `write_paths` and `edit_paths`, and P3 shows both a `write` adapter step
  (`argument_keys: ["path","stream_content"]`) and `edit` steps
  (`argument_keys: ["i","new_string","old_string","path"]`). The per-tool mapping (which list
  authorizes which tool) is not determinable from readable sources; the union is the only reading
  under which the DECLARED_EDIT ALLOW is reachable for both tool kinds. `[INFERENCE]`
- **P-B (seat identity linkage).** An event's authority is taken from the binding of *the same
  seat*. P3 carries both `seat` ("CritRuntime", "OraclePathArtifact") and `agent`
  ("TsukuroiR22.CritRuntime-3"); P5's binding carries `name` ("OracleEditReadOnlyEdit"). Which key
  links an event to its binding is undefined in readable sources (see F5). `[INFERENCE]`

## 3. Exact authority preconditions for `READ_ONLY_EDIT -> DENY`

Let `B` = one per-seat binding record; `E` = one recorded adapter step; `P` = the step's declared
target path, selector-stripped and canonicalized (§3.2); `Op(E) ∈ {read, write}` = the step's
operation kind.

**Membership test.**

    READ_ONLY_EDIT(B, E)  ⟺  Op(E) = write
                           ∧  P ∈ R(B)            (R(B) = B.read_paths)
                           ∧  P ∉ W(B)            (W(B) = B.write_paths ∪ B.edit_paths)
                           ∧  seat(E) = seat(B)   (linkage key undefined — P-B)

**Decision.** `DENY`, unconditionally given the class. Rationale in the policy's own words:
"Read authority never grants a write." Operationally, a write to `P` is authorized only if
`P ∈ W(B)`; `P ∈ R(B)` is a *separate* requirement (per `WRITE_ONLY_EDIT`'s reason) and is never
*sufficient* for a write.

**Ordering preconditions** (needed for a deterministic fixture; see F4 for why these are inferred):

1. **Target resolvable.** If the step carries no structured target path, the class is
   `OPAQUE_PATCH -> UNKNOWN` — "Missing structured target is not inferred from opaque patch text."
   A missing target must never be coerced into `READ_ONLY_EDIT` (that would convert an UNKNOWN into
   a DENY by inference, exactly what the policy forbids).
2. **Path form.** `EDIT_EXTERNAL -> DENY` ("Remote or internal URIs do not become filesystem edit
   targets") and `EDIT_TRAVERSAL -> DENY` ("No dot-segment or alternate spelling expands the target
   list"). A read-only membership obtained only through a dot-segment or alternate spelling is
   therefore not a `READ_ONLY_EDIT` instance; it is a traversal/denial.
3. **Identity.** The binding must be the *literal per-seat* v2 binding of the step's own seat. P2's
   C2 scope restricts authority to "exact predeclared structured edit targets", and P1's
   `UNDECLARED_EDIT` reason states "No implicit edit permission from generic report ownership" —
   i.e. a role-level or ownership-level default never contributes write authority to this test.
   Per-seat literal v2 binding is narrower than generic role defaults.
4. **Quadrant.** Membership of `P` in `R(B)` and `W(B)` selects exactly one of the four ids in §1.2.
5. **Per-step scoping.** P1's `EXPANSION -> CHECK_EACH` ("Every recorded adapter read or write
   remains separately scoped") means the test is applied per (seat, path, operation-kind) record
   and never aggregated across steps, paths, or seats. A binding may therefore be *mixed*: one path
   `ALLOW`, another `DENY` — and `EXPANSION` is a scoping instruction, not a ninth quadrant.

**Explicitly not part of this decision:** whether a call succeeded, was refused, took effect, or was
recorded; whether any enforcement exists; whether the file changed; what the patch body contains.
Both P1's and P3's scope lines exclude these, and P2's `limits` exclude "No native per-seat
restrictive tool interface exists" and "No runtime prevention, effect/reading/recorder-completeness
or universal tool/patch semantics".

### 3.2 Path-identity nuance (source-grounded, affects "exact target")

P3 records the same physical file under two spellings within one observation: `observation.path`
is bare (`/…/round-22/build/CritRuntime.md`) while the corresponding `recorded_starts[].path` for
the read step carries a selector suffix (`/…/round-22/build/CritRuntime.md:raw`); the `write` step
in the same record is bare. Therefore "exact target" cannot be raw string equality over whatever
path field the record happens to expose: the comparator must establish identity of the
*filesystem target* (selector-stripped), while still rejecting dot-segment/alternate spellings per
`EDIT_TRAVERSAL`. These two requirements coexist only if the comparator distinguishes
(a) a read-selector suffix, which is not a different target, from (b) a path-spelling variation,
which is not a match. P1/P2 do not state the distinction; P3 is the only readable evidence that it is
needed.

## 4. Smallest literal metadata fixtures

**Minimality basis.** Under the policy's scope ("Declared audit authority for structured target
metadata only"), the decision inputs are exactly: the two authority sets, the step's target path,
and the step's operation kind. Everything else in the record shapes is audit-linkage
(`transcript_sha256`, `request_line`, `call_id`, `agent`, `recorded_starts`) or body opacity
(`body_fields`, `old_string`/`new_string`/`stream_content`), and is dropped. `root` is retained in
the fixtures for legibility only: under a literal absolute-path comparator it is decision-irrelevant
(it documents scope); it becomes decision-relevant only if the comparator is root-relative.
**Caveat:** "valid" here means *decision-minimal and internally consistent with P1/P2/P5*. Whether
these fixtures are *checker-accepted* is not verifiable from this seat's read set (see §6).

**Negative fixture — `READ_ONLY_EDIT -> DENY`** (smallest record that yields the class: one
read-authorized path, empty write-ish lists, one edit/write step against that path):

    {
      "binding": {
        "name": "S",
        "root": "/R",
        "read_paths": ["/R/t.md"],
        "write_paths": [],
        "edit_paths": []
      },
      "event": {
        "seat": "S",
        "tool": "edit",
        "path": "/R/t.md"
      }
    }

The three DENY siblings are obtained from the same skeleton by changing *only* membership, which is
the sharpest available demonstration that the four ids are separated by nothing but the two sets:

    UNDECLARED_EDIT (DENY):  read_paths: [],  write_paths: [],  edit_paths: []
    WRITE_ONLY_EDIT (DENY):  read_paths: [],  write_paths: ["/R/t.md"], edit_paths: []
    READ_ONLY_EDIT (DENY):  read_paths: ["/R/t.md"],  write_paths: [],  edit_paths: []
    DECLARED_EDIT  (ALLOW):  read_paths: ["/R/t.md"],  write_paths: ["/R/t.md"], edit_paths: []

**Positive fixture — `DECLARED_EDIT -> ALLOW`** (the negative fixture with one membership added):

    {
      "binding": {
        "name": "S",
        "root": "/R",
        "read_paths": ["/R/t.md"],
        "write_paths": ["/R/t.md"],
        "edit_paths": ["/R/t.md"]
      },
      "event": {
        "seat": "S",
        "tool": "edit",
        "path": "/R/t.md"
      }
    }

**Variants of the positive fixture** (three ways to satisfy "predeclared for edit and for both
read and write", reflecting P-A's unresolved per-tool mapping):

    V1 (write-listed):  write_paths: ["/R/t.md"],  edit_paths: []
    V2 (edit-listed):   write_paths: [],         edit_paths: ["/R/t.md"]
    V3 (both-listed):   write_paths: ["/R/t.md"],  edit_paths: ["/R/t.md"]   <- P5's own shape

The union rule W(B) = write_paths ∪ edit_paths accepts all three for a write/edit step. A
tool-scoped rule (write tool ⇒ `write_paths`, edit tool ⇒ `edit_paths`) would accept only V1 for a
`write` step and only V2/V3 for an `edit` step. **This is the single most load-bearing schema
assumption in the fixture set** and it is unverifiable from the readable sources (F3).

**Operation-kind dependence.** The negative fixture's `tool` field matters under the event-kind
reading (§1, `Op(E) = write`). Under a pure-membership reading, `Op(E)` is irrelevant and the id
means only "the target is read-only"; the difference is observable, because under the pure reading
an ordinary **read** step against `/R/t.md` would also be labeled `READ_ONLY_EDIT -> DENY`, which
would mislabel a permitted read as a denial. P1's `EXPANSION` wording ("Every recorded adapter
**read or write** remains separately scoped") supports the event-kind reading; P1 never states it
outright (F4).

**Path-form negatives (form classes precede authority classes under the ordering above).** These
do not change the outcome (all DENY) but change the *id*, and therefore change what a per-id
validation count would report:

    EDIT_TRAVERSAL (DENY): read_paths: ["/R/t.md"], write_paths: [], edit_paths: [],
                          event.path: "/R/./t.md"   (or "/R/x/../t.md")
    EDIT_EXTERNAL  (DENY): read_paths: ["/R/t.md"], write_paths: [], edit_paths: [],
                          event.path: "https://host/x/t.md"   (or an internal URI form)

**OPAQUE_PATCH (UNKNOWN).** A step with no structured target (e.g. only a body field) yields
UNKNOWN, never `READ_ONLY_EDIT`:

    OPAQUE_PATCH (UNKNOWN): event: { "seat": "S", "tool": "edit", "body_fields": "omitted; no report text copied" }

## 5. What would falsify this decision (metadata level only)

The decision is falsifiable only by evidence inside its declared scope — declared metadata about
targets and authority. Effects, refusals, enforcement, and body content are outside the scope and
can never falsify it (and can never support it either).

- **F-A (authority inversion).** A binding in which `P ∈ R(B)` and `P ∉ W(B)`, with the framework
  classifying the corresponding write/edit step as `ALLOW`. That would falsify the DENY as a rule
  about declared metadata. *Not present in the readable corpus.*
- **F-B (read-only observation).** A recorded adapter step performing a write/edit on a path that
  appears in that seat's binding **only** under `read_paths`. Such a record would show that write
  authority exists outside `W(B)`, which would make the DENY a misdescription of the authority in
  force (the class would have to be restated, e.g. as `UNDECLARED_EDIT`, or the rule amended to
  admit an authority source outside the two lists). *Not present: in P3, every write/edit step
  co-occurs with the seat writing/editing that same path.*
- **F-C (schema inversion).** A v2 binding schema, or C2 prose, in which write authority is
  derivable from read authority for the same target (e.g. "write_paths defaults to read_paths", or
  "read on a target implies write on that target"). Under such a schema the reason "Read authority
  never grants a write" is false as a framework statement and the DENY row must be withdrawn or
  re-scoped. *Not present in P1/P2/P5.*
- **F-D (ground collapse).** P1's row cites `evidence: S086`. If S086 (P3) were found to contain no
  structured write/edit step, the row's "a write needs write authority" half would be ungrounded.
  *Falsified for this reading: P3 does contain such steps — CritRuntime's `write` step
  (`argument_keys: ["path","stream_content"]`) and three OraclePathArtifact `edit` steps
  (`argument_keys: ["i","new_string","old_string","path"]`).*
- **F-E (comparator test).** The "exact target" comparator is falsifiable independently: if the
  framework's comparator is raw string equality over the exposed path field, then P3's own
  `…/CritRuntime.md:raw` spelling never matches the bare declared path, so a legitimate
  `DECLARED_EDIT` instance would be misclassified. Observing such a misclassification would falsify
  the *comparator*, not the DENY. The DENY survives either way (a false negative on ALLOW and a
  false positive on DENY are different failures), which is why the comparator must be specified
  rather than inferred.
- **What would NOT falsify it:** an observed successful write to a read-only path; an observed
  blocked call; absence of any enforcement; the content of any patch body; the number of times the
  path was read. All are excluded by P1's scope line, P3's scope line, and P2's `limits`.

## 6. Findings by severity

**F1 — HIGH — `READ_ONLY_EDIT` is structurally derived, not observationally exemplified.**
P1 grounds the row in `S086`; P3 (S086) contains four observations, all of which pair a write/edit
step with a path that the same seat also wrote. There is no record anywhere in the readable corpus
of a target that is read-authorized and *not* write-authorized — i.e. no instance of the very
condition that distinguishes `READ_ONLY_EDIT` from `DECLARED_EDIT`. The DENY direction is
nevertheless the only direction the readable material supports (a corpus where write steps always
co-occur with write authority is consistent with, and gives no counterexample to, "read authority
never grants a write"). Impact: C1's "source-grounded … decisions" wording is only partly met for
this id; the class is grounded in *schema semantics* plus the *absence* of a counterexample.
Recommended wording for downstream prose (not applied here): the row is source-consistent and
counterexample-free within S086, rather than source-exemplified.

**F2 — HIGH — no declared precedence among the eight ids; some fixtures are ambiguous.**
P1 maps each id to a decision but never states an order, and never states a total function from a
metadata record to exactly one id. Concretely ambiguous combinations: (a) an opaque patch whose
target is read-only (`OPAQUE_PATCH`/UNKNOWN vs `READ_ONLY_EDIT`/DENY — an UNKNOWN versus a DENY
outcome difference, which is *outcome-visible*); (b) a traversal-spelled read-only target
(`EDIT_TRAVERSAL`/DENY vs `READ_ONLY_EDIT`/DENY — outcome-invisible, id-visible); (c) an external
URI that is also read-only (same). Any checker must implement an undeclared ordering, and a
per-id validation count (C1's `validated_edit_decisions` = 8) is sensitive to that ordering. The
ordering in §3 is inferred, not declared.

**F3 — MEDIUM — the policy is schema-agnostic while the decision is entirely schema-dependent.**
P1 names no authority field, no event field, no seat-key, and no tool→list mapping. The fixture in
§4 is stated against P5's literal shape (the only schema artifact readable here) and rests on P-A
(union write set). If the checker's actual model is tool-scoped (`write` ⇒ `write_paths`, `edit` ⇒
`edit_paths`), then positive-fixture V1/V2/V3 split differently, and the *negative* fixture
(edit_paths empty, write_paths empty) is unaffected — the DENY row's own fixture is the
robust one. That is a genuine asymmetry worth stating: **the DENY fixture is schema-robust; the
ALLOW fixture is not.**

**F4 — MEDIUM — event-kind dependence is undeclared.** The two DENY reasons both name "edit"
("Read authority never grants a write", "Edit also needs its explicit target read authority"), which
suggests the id is indexed by the *requested operation*, not merely by the target's authority
profile. Under the pure-membership reading, permitted reads would be mislabeled as denials. The
fixture's `tool` field is therefore load-bearing under one reading and inert under the other, and
the policy does not disambiguate.

**F5 — MEDIUM — seat-identity linkage is undefined.** The three record shapes use different keys:
P5's binding has `name`; P3's observations have `seat` and `agent`; P2's C2 command names a
manifest and an events file whose internal keys are unreadable here. If an event's seat key does not
match a binding key, no authority applies — a case the policy's eight ids do not name (it is
"no applicable binding", which is neither `UNDECLARED_EDIT` (a declared-but-unmatched binding) nor
`READ_ONLY_EDIT`). The fixtures use `seat: "S"` against `name: "S"`.

**F6 — LOW — dual encoding of the same eight rows.** P2's `edit_decisions` (positional triples)
and P1's `decisions` (objects with `evidence`/`policy`) encode the same eight rows twice, with no
declared single source of truth and no stated invariant tying them. P1 is not a pure projection of
P2 (it adds `evidence: S086` and `policy: round23-preregister`, which P2 lacks), and P2 alone
cannot ground `S086`. Divergence between the two encodings is therefore possible without violating
either document's stated scope.

**F7 — LOW — the two scope sentences exclude different things.** P1's scope: "Declared audit
authority for structured target metadata only; no native prevention, opaque patch interpretation,
effect or reading proof." P3's scope: "Observed structured path metadata and recorded adapter steps
only, not universal tool semantics, native permission enforcement, effects, or reading proof." P1
omits "universal tool semantics" (P3 states it); P3 omits "opaque patch interpretation" (P1 states
it). Neither mentions body opacity, which P3 demonstrates in practice via
`"body_fields": "omitted; no report text copied"`. Minor, but the exclusions should be stated
once, identically, if the two documents are to be read as a separated pair.

**F8 — INFO — selector-suffixed path spellings in the source (see §3.2).** P3 records
`…/CritRuntime.md:raw` in `recorded_starts[].path` while `observation.path` for the same record is
bare. Any "exact target" implementation must strip read selectors while still refusing dot-segment
and alternate-spelling matches, and the policy text does not distinguish the two.

**F9 — INFO — provenance vs decision inputs.** P3's provenance fields (`transcript_sha256`,
`request_line`, `call_id`, `agent`) and `recorded_starts[]` are audit-linkage, not decision inputs
under P1's scope. The §4 fixtures drop them; if the checker requires them for admissibility, the
fixtures must grow by linkage fields, and the decision-relevant core remains the four fields named
above.

## 7. Residual risk

- **Outcome risk is low, id risk is not.** Every plausible reading of P1/P2/P3 that admits a
  read-only target yields **DENY**; the risk concentrates in *which* id is reported, which is what
  F2/F3/F4 expose, and in whether the C1 count of eight "validated" decisions is reproducible under
  an undeclared precedence.
- **Unreadable-schema risk.** The fixtures are decision-minimal and internally consistent, but
  checker-acceptance is untested here (F3). If the checker's model differs on the union rule, the
  positive fixture must be re-spelled; the negative fixture (both write-ish lists empty) survives
  either model unchanged.
- **Event-vs-authority gap.** The readable source demonstrates tool-call metadata but never
  authority metadata; every claim linking "declared read membership" to "the recorded step was
  unauthorized" is an inference over a schema that is outside this seat's read set (F1, P-A, P-B).
- **No runtime claim.** Nothing here asserts that any write was prevented, blocked, permitted,
  or effected. The oracle's competence is confined to declared metadata.

## 8. Verification gaps (declared, not improvised)

- `tools/check-edit-contract.py` (C1) and `tools/check-seat-bindings.py` (C2) are outside the
  declared read set: their schema expectations, precedence order, and admissibility rules could not
  be read, so no "checker-valid" claim is made for any fixture above.
- `.ufo/waves/round-23/<WAVE>/bindings.json` and `events.json` are outside the declared read set:
  the authority-side ground truth that P1 scores is unreadable here; only the event-side (P3) is.
- The v2 binding schema document, and any specification of how a binding's `name` maps to an
  event's `seat`/`agent`, are unreadable (F5).
- The SHA-256 of P1 is the supplied declared identity; it was **not** independently computed, and
  no hash, list, or byte-count command was run to check it.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditreadonlyedit
Scope: executed=none
