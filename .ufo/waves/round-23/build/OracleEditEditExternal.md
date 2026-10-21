# OracleEditEditExternal — source-only oracle for `EDIT_EXTERNAL` → `DENY`

Round 23, attempt 1. Independent source-only derivation. No example, fixture, checker, adapter or
runtime was invoked; nothing was executed, compiled, imported, hashed, listed or counted by a
command. The target digest below is a **supplied declaration** copied from the seat binding; it was
not independently recomputed.

## 0. Bound material actually read

| # | Path (bound) | Role in this derivation |
|---|---|---|
| S1 | `.ufo/waves/round-23/sources/edit-decision-policy.json` | **Target** — machine-readable decision table (`tsukuroi-edit-policy-v1`) |
| S2 | `.ufo/waves/round-23/preregister.json` | Normative preregistration, claims C1–C3, `edit_decisions` table, `limits`, `sources_opened` |
| S3 | `.ufo/waves/round-23/sources/structured-edit-observations.json` | The observation source that S1's `evidence: "S086"` points at |
| S4 | `.ufo/waves/round-23/sources/godspeed-directive.txt` | Copy of the Godspeed directive (verbatim, 4 numbered axes + the immediate-action rule) |
| S5 | `skill://godspeed` | Same directive in skill form; content identical to S4 |

Read-only. The only file written is this report. No tool was installed or updated: this seat's
NO-EXEC/NO-FETCH scope forbids installation, and the tooling directive's install channel is a
host-mutating action outside the seat binding. **Install log: none (no install, no update, no
package, no service, no host action).**

## 1. Axes named (Godspeed step 1)

For this seat the axes are properties of a *declared* edit-authority decision, evaluated only over
source text:

- **A1 — Decision fidelity.** Does the target's `EDIT_EXTERNAL` record agree with the
  preregistered row, field for field, and with the observation source it cites?
- **A2 — Evidence reach.** Does the cited evidence actually exhibit the phenomenon the decision
  names, or is the citation only structural? (This is the axis on which the decision is weakest.)
- **A3 — Determinism.** Given only the declared metadata, is the classification of a fixture
  unique? (Precedence, scheme set, categorical-vs-conditional reading.)
- **A4 — Claim honesty.** Does the decision's reach stay inside the declared scopes (no native
  prevention, no body/effect semantics, no reading proof, no universal tool semantics)?
- **A5 — Falsifiability.** Is there a *source-level* observation that would overturn the decision
  without appealing to body or effect semantics?

Steps 2–4 of the directive (iterate cheap in parallel, keep moves that improve an axis and harm
none, don't aim) were applied by reading the five bound artifacts concurrently in one batch, then
one more batch for the elided ranges of S2/S3; no other corpus search was performed because the
seat binding forbids extra filesystem search.

## 2. The declared decision, verbatim, and its cross-source agreement

From S1 `decisions[]` (exact fields):

```json
{
  "id": "EDIT_EXTERNAL",
  "decision": "DENY",
  "reason": "Remote or internal URIs do not become filesystem edit targets",
  "evidence": "S086",
  "policy": "round23-preregister"
}
```

From S2 `edit_decisions[6]` (exact triple): `["EDIT_EXTERNAL", "DENY", "Remote or internal URIs
do not become filesystem edit targets"]`.

**A1 result: agreement confirmed by reading.** The id string, the decision string, and the reason
string are byte-identical between S1 and S2. S1 additionally binds `evidence: "S086"` and
`policy: "round23-preregister"` to every one of the eight rows, and points at S3 via
`"source_path": ".ufo/waves/round-23/sources/structured-edit-observations.json"`. S2's
`sources_opened` lists `S086 prospective: observed structured edit request keys and recorded
adapter steps`, which is the content of S3.

Scope sentences, verbatim and mutually consistent:

- S1 `scope`: "Declared audit authority for structured target metadata only; no native prevention,
  opaque patch interpretation, effect or reading proof."
- S3 `scope`: "Observed structured path metadata and recorded adapter steps only, not universal
  tool semantics, native permission enforcement, effects, or reading proof."
- S2 `limits[0..1]`: "No native per-seat restrictive tool interface exists" / "No runtime
  prevention, effect/reading/recorder-completeness or universal tool/patch semantics".

**A4 result: the three scopes agree, and all three foreclose the same over-claims.** Any reading
of `DENY` as "the write was prevented", "the write had no effect", "the file was not changed",
"the patch text was understood", or "no tool can ever edit a URI" is outside the declared scope of
all three bound sources. The decision's reach is: *the declared audit classification of a
structured edit target whose value is a URI is DENY.*

## 3. A2 — Source-vs-policy separation (the load-bearing finding)

S3 contains **four** observation records. Every field relevant to the target-shape question:

- Seats: `CritRuntime` (1 record), `OraclePathArtifact` (3 records).
- `tool`: `edit` in all four.
- `argument_keys`: `["path","stream_content"]` once; `["i","new_string","old_string","path"]`
  three times. → `path` is present in **4/4** records; it is the target-bearing key.
- `path`: in all four, an absolute local filesystem path under
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/`.
- `body_fields`: `"omitted; no report text copied"` in all four.
- `recorded_starts`: adapter steps, all on the same local absolute path family
  (`read` / `write` / `edit` on the round-22 build file).

**Zero of the four observed targets is scheme-bearing.** There is no `https://`, no `ssh://`, no
internal URI scheme, and no non-`/`-prefixed target of any kind in S3.

Therefore:

1. **The citation `evidence: "S086"` does not exhibit the subject matter of this decision.** S086
   supports the *model* in which an edit request carries an explicit, structured, path-typed
   target and an opaque body — that is what the four records show. It does **not** support a
   claim that an external/remote/internal target was observed and denied. A report or checker
   commentary that cites S086 as "the source shows external edits being denied" is a false
   evidentiary claim and would have to be struck.
2. **The decision's warrant is the reason string, not the observations.** "Remote or internal URIs
   do not become filesystem edit targets" is a *category* claim about what a filesystem edit
   target is. It is normative and prospective. S2 reinforces this by labelling S086
   `prospective`.
3. **S1 is not independent evidence for S2's table.** The eight rows in S1's `decisions[]` mirror
   S2's `edit_decisions` verbatim; S1 adds machine-readable structure, a uniform evidence pointer
   and a scope sentence, but no new warrant. The dependency direction is
   preregister → policy → (pointer to) observations, never observations → decision for this row.
4. **The separation that does hold** is the one between *observation* (S3: what path metadata was
   recorded) and *policy* (S1/S2: how such a target is classified). The oracle's job on this row
   is therefore to derive a *classifiable* fixture, because no instance of the class exists in
   the frozen evidence. This is the honest form of the claim, and it is the claim I make below.

## 4. Exact authority preconditions for a `EDIT_EXTERNAL` → `DENY` record

These are the conditions that must hold for the record to be well-formed against the bound
sources. They are stated as preconditions, not as behaviour of any runtime.

- **P1 — Structured target present.** The request must carry an explicit target argument key.
  Observed key: `path` (4/4 records). Absence of a structured target is the `OPAQUE_PATCH` class
  (S1: "Missing structured target is not inferred from opaque patch text"), so the two classes are
  disjoint by construction: `EDIT_EXTERNAL` may only ever be reached *with* a structured target
  in hand.
- **P2 — Target value is scheme-bearing.** The target must be a URI-shaped value (a scheme
  component followed by `:`), not a local filesystem path. "Remote or internal URIs" names the
  class; S1 does not enumerate the schemes, so P2 is decidable only against an explicitly
  declared scheme set. **The scheme set is missing from the bound sources** (see §7, G3).
- **P3 — Body is opaque and unused.** `body_fields` is `"omitted"` in the source model, and S1's
  scope forbids "opaque patch interpretation". The decision is therefore computed from target
  metadata alone; the body is neither read nor needed.
- **P4 — The declared authority is a local-filesystem target list.** The seat's v2 authority
  (S2 claim C2: "New explicit schema-v2 audit authority for exact predeclared structured edit
  targets") enumerates exact predeclared targets. For this row the enumerated targets are local
  filesystem paths, so a URI target is not among them.
- **P5 — Reading the DENY branch.** `DECLARED_EDIT` (S1/S2) allows only when the "Exact target
  is predeclared for edit and for both read and write". A URI target satisfies P4's list only if
  such a URI were enumerated — which the current source does not do. Hence the DECLARED_EDIT
  branch is unavailable and the row lands on `EDIT_EXTERNAL` → `DENY`.
- **P6 — No enforcement, effect, or reading claim is attached.** Enforced by S1 scope, S3 scope,
  S2 limits. The DENY records an *audit classification*; it asserts nothing about what any
  adapter did, whether bytes changed, or whether a file can be read.
- **P0 (precedence precondition, derived — see §7, G1).** The eight ids are disjoint only if
  classification is *shape-first*: a scheme-bearing target is `EDIT_EXTERNAL` regardless of
  declaration status; a non-scheme target is then `DECLARED_EDIT` / `UNDECLARED_EDIT` /
  `READ_ONLY_EDIT` / `WRITE_ONLY_EDIT` by declaration status; `EDIT_TRAVERSAL` applies to
  non-scheme targets containing dot-segments or alternate spellings; `OPAQUE_PATCH` applies when
  no structured target exists; `EXPANSION` (`CHECK_EACH`) is a per-operation scoping directive
  over recorded adapter steps rather than a target-shape class. **S1 and S2 declare no
  tie-break rule**, so P0 is a derived requirement, not a source fact.

## 5. Smallest literal valid metadata fixture

Derived by construction from the fields S3 actually records (`tool`, `argument_keys`, `path`,
`body_fields`) plus the v2 authority lists S2's C2 names. Deliberately minimal: every retained
field is load-bearing for the classification, and each removed field would weaken the claim.

### 5.1 Positive fixture — expects `EDIT_EXTERNAL` → `DENY`

```json
{
  "request": {
    "tool": "edit",
    "argument_keys": ["path", "old_string", "new_string"],
    "path": "https://example.invalid/build/OracleEditEditExternal.md",
    "body_fields": "omitted"
  },
  "binding": {
    "name": "OracleEditEditExternal",
    "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
    "read_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md"],
    "write_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md"],
    "edit_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md"]
  },
  "expected": { "id": "EDIT_EXTERNAL", "decision": "DENY" }
}
```

Why each part is necessary (each is a precondition from §4):

- `path` = `https://example.invalid/...` — the *most literal* instance of "Remote **or** internal
  URIs": a remote scheme with an authority, so the fixture is decidable under either limb of the
  reason and does not depend on the undefined notion of "internal". `example.invalid` is reserved
  and non-routable, so the fixture carries no reachable endpoint and no fetch is implied.
- `argument_keys` containing `path` — satisfies P1 and, equally important, keeps the fixture out
  of `OPAQUE_PATCH`. `old_string`/`new_string` are the observed pair from S3's
  `OraclePathArtifact` records; they are inert here because `body_fields` is opaque.
- `body_fields: "omitted"` — satisfies P3, and keeps the decision free of any body/effect claim.
- `edit_paths` / `write_paths` / `read_paths` non-empty and local — satisfies P4 and makes the
  class *unique* under P0: the seat does hold edit authority, so the denial is not merely
  "no authority declared"; it is that a URI is categorically not a filesystem edit target.
- `expected` — the decision tuple, matching S1's `EDIT_EXTERNAL` record and S2's row 7.

### 5.2 Negative fixture — the minimal contrast, expects `DECLARED_EDIT` → `ALLOW`

Identical to §5.1 in every field **except** the target string and its membership:

```json
{
  "request": {
    "tool": "edit",
    "argument_keys": ["path", "old_string", "new_string"],
    "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md",
    "body_fields": "omitted"
  },
  "binding": {
    "name": "OracleEditEditExternal",
    "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
    "read_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md"],
    "write_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md"],
    "edit_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md"]
  },
  "expected": { "id": "DECLARED_EDIT", "decision": "ALLOW" }
}
```

The negative fixture isolates exactly one variable: the *shape* of the target string, holding
authority constant (the target is predeclared for edit, for write and for read in all three
lists). A classifier that denies both fixtures is denying on "not listed" and never on the URI
category; a classifier that allows both is treating URIs as filesystem targets. The pair
therefore discriminates the decision itself.

### 5.3 Boundary fixture — exposes the over-broad reading of the reason

```json
{
  "request": {
    "tool": "edit",
    "argument_keys": ["path", "old_string", "new_string"],
    "path": "file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditExternal.md",
    "body_fields": "omitted"
  },
  "binding": {
    "name": "OracleEditEditExternal",
    "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
    "read_paths": [],
    "write_paths": [],
    "edit_paths": []
  },
  "expected": { "id": "EDIT_EXTERNAL", "decision": "DENY" }
}
```

`file://` is scheme-bearing but *denotes a filesystem location*, which is in direct tension with
the reason's own wording ("do not become filesystem edit targets"). The categorical reading
denies it; this is the single most likely point of over-reach in the current wording, and it is
the one I would flag to the preregisterer (§7, G3).

## 6. What would falsify this decision (no body/effect semantics invoked)

Each item is a *source-level* observation that would overturn the row. None requires reading
patch bodies, observing bytes, or claiming what an adapter did.

- **F1 — A declared URI edit target.** A round-23 v2 binding that lists a scheme-bearing target
  in `edit_paths`/`write_paths`/`read_paths`, with a matching captured event treated as an
  authorised edit. The categorical reading of `EDIT_EXTERNAL` is then falsified: the model
  demonstrably permits declared URI targets, and the row must be re-expressed as a *conditional*
  denial (URI target **and** not enumerated), collapsing toward `UNDECLARED_EDIT` with the reason
  reworded from a category claim to a declaration claim.
- **F2 — A scheme-bearing target classified as authorised by the contract model**, observed in S3
  or a successor observation file. Same consequence as F1, from the observation side rather than
  the binding side.
- **F3 — A `file://` (or other filesystem-denoting scheme) target treated as a filesystem target**
  by the declared model. The reason's category claim is then over-broad and needs a
  scheme-exclusion refinement (exclude filesystem-denoting schemes from the class).
- **F4 — A URI that appears only inside an opaque patch body, with no structured target argument.**
  The correct class is `OPAQUE_PATCH` → `UNKNOWN` ("Missing structured target is not inferred
  from opaque patch text"). If the model classified that as `EDIT_EXTERNAL`, the two rows would
  not be disjoint and P1 would be violated.
- **F5 — A second, incompatible meaning of "external" in the same corpus**, namely "a local path
  outside the declared root". The decision id would then be mis-scoped relative to
  `UNDECLARED_EDIT` (which already owns "not declared"), and the reason text would be describing
  a different phenomenon than the id names. I could not test this from the bound material: the
  seat forbids corpus-wide search, so this remains an open check against the wider corpus.
- **F6 — A re-preregistered v2 decision table** that splits the row (e.g. `EDIT_EXTERNAL_UNDECLARED`
  → DENY and `EDIT_EXTERNAL_DECLARED` → ALLOW). The single-branch form is then falsified as an
  8-row decomposition, and C1's `validated_edit_decisions` target of 8 (from 0) would need
  re-preregistration; S1's eight rows would no longer mirror S2's `edit_decisions`.
- **F7 — Adapter-dependent outcome for an identical target string** within one wave: the same
  structured target evaluated by two adapters with different declared-authority outcomes. The
  DENY would then be a property of adapter identity rather than of the target metadata, and the
  policy would be under-specified.

## 7. Residual risk and verification gaps

- **G1 — No precedence rule (highest-impact gap).** S1 and S2 declare eight decision ids with no
  tie-break, no disjointness statement, and no statement of whether the array order is
  significant. Any fixture that violates two rules at once (a URI that is also undeclared; a URI
  containing `..`; a URI with no structured argument) has an unspecified id. The §5.1 fixture is
  unique only under the derived P0. This is the gap most likely to produce a checker/author
  disagreement, and it is a preregistration gap, not a source-reading gap.
- **G2 — Zero observed instances.** S3 contains no scheme-bearing target, so this class has never
  been exercised in the frozen evidence. Any statement that EDIT_EXTERNAL is *empirically
  covered* by the current observation source would be false. The honest statement is: the class
  is defined by the preregistered rule and instantiated only by the §5 fixtures.
- **G3 — The scheme set is unenumerated.** "Remote or internal URIs" does not name schemes, so
  the class is not machine-decidable from the bound sources alone, and the `file://` boundary
  case (§5.3) is unresolved. A declared scheme list (with an explicit filesystem-denoting
  exclusion) is required for the row to be decidable without interpretation.
- **G4 — Categorical vs conditional reading is unstated.** §5.1 and §5.3 only classify
  deterministically if the reading is fixed. Under the categorical reading, even a *declared* URI
  target is denied (and S1's `DECLARED_EDIT` reason, which is not restricted to filesystem paths,
  would contradict it). Under the conditional reading, the rule is a special case of
  `UNDECLARED_EDIT` and the reason text is over-strong.
- **G5 — `EDIT_EXTERNAL` vs `EDIT_TRAVERSAL` boundary.** A scheme-bearing target containing
  dot-segments is both URI-shaped and traversal-shaped. With no precedence rule (G1) the id is
  unspecified; the §5.1 fixture deliberately avoids the overlap.
- **G6 — "Internal" is undefined in the bound sources.** The harness surface uses several
  internal URI families, but the bound sources neither enumerate them nor state whether an
  internal-URI target is denied on the same grounds as a remote one. The §5.1 fixture was chosen
  remote precisely to avoid depending on this undefined term.
- **G7 — Enforcement is absent by declaration.** S2's limits state plainly that no native
  per-seat restrictive tool interface exists. Nothing in this row can be reported as prevention.
- **G8 — Verification gaps in this report.** The C1 checker (`python3 tools/check-edit-contract.py
  --revision <REV>`) and the C2 seat-binding checker were **not invoked** — the seat forbids it,
  and §5 fixtures are proposed, not executed. The C3 path-reconciliation checker is outside this
  seat's scope. Cross-source agreement in §2 is a reading-level comparison of the two bound JSON
  documents, not a checker verdict. The declared digest was not recomputed. Whether the landed
  C1 document admits the §5 fixture at all is an unverified prediction, and it should be treated
  as a hypothesis to be checked by the C1 executor, not as a result of this oracle.

## 8. Verdict (recommendation, not admission)

`EDIT_EXTERNAL` → `DENY` is **faithful to the preregistered row** (A1 confirmed by reading) and
**correctly scoped** as an audit classification of structured target metadata (A4 confirmed against
all three bound scopes). Its evidentiary basis is **prospective and declarative, not
observational** (A2: 0/4 source records are scheme-bearing), and it is **not uniquely decidable**
until precedence (G1), the scheme set (G3) and the categorical-vs-conditional reading (G4) are
fixed in the preregistration. I recommend the preregisterer add: (i) an explicit precedence/disjointness
rule, (ii) a declared scheme list with filesystem-denoting schemes excluded, and (iii) an explicit
statement of whether the denial is unconditional on scheme shape or conditional on non-declaration.
I make no claim about any runtime's behaviour, any patch body, or any file's contents.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleediteditexternal
Scope: executed=none
