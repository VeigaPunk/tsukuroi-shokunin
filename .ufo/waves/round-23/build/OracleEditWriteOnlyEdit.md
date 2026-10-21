# OracleEditWriteOnlyEdit — source-only oracle for WRITE_ONLY_EDIT → DENY

Question: derive, from declared source only, the smallest literal metadata fixture that
places a structured edit request in the WRITE_ONLY_EDIT class, the exact authority
preconditions for the DENY verdict, and the boundary between source evidence and policy
rule. No checker, example harness, manifest, or event file was invoked; no command, hash,
listing, import, subprocess, or fetch was performed. The published source identity is a
supplied declaration, not a recomputation.

## 1. Declared instances read

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/edit-decision-policy.json`
  (declared identity f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`
  (plan copy of the same eight tuples; claims C1/C2/C3).
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/structured-edit-observations.json`
  (the source named by `source_path` and by evidence id S086).

The policy row and the preregister row agree verbatim on the subject tuple:

```
id       WRITE_ONLY_EDIT
decision DENY
reason   Edit also needs its explicit target read authority
evidence S086
policy   round23-preregister
```

This agreement is an observed fact about the two files I read; it is not a digest claim.

## 2. What the evidence source can and cannot establish

S086 (`structured-edit-observations.json`) records, per observation: `seat`, `agent`,
`transcript_sha256`, `request_line`, `call_id`, `tool`, `argument_keys`, `path`,
`body_fields`, `recorded_starts`. Its own `scope` field restricts it to "Observed
structured path metadata and recorded adapter steps only, not universal tool semantics,
native permission enforcement, effects, or reading proof."

Therefore S086 establishes only:

- Structured edit requests carry an explicit literal `path` argument key. Two observed
  payload shapes appear: `["path","stream_content"]` (CritRuntime) and
  `["i","new_string","old_string","path"]` (OraclePathArtifact).
- Requests are accompanied by `recorded_starts`: adapter steps with `line`, `tool`, and
  `path`. CritRuntime line 15 (`edit`) is preceded by `read` at line 12 on the same path
  with a `:raw` selector and `write` at line 13 on the same plain path. OraclePathArtifact
  records only an adjacent `edit` step on the same path.
- Bodies are withheld (`body_fields` = "omitted"), so nothing about `old_string`,
  `new_string`, or `stream_content` content is in the source.

S086 does not establish any seat's declared authority sets, any ALLOW/DENY classification,
whether a target was readable or writable, whether an edit applied, or any effect. A
recorded `read` step is an observed access, not a grant of read authority; a recorded
`write` step is an observed adapter call, not an authority declaration. The r22 observations
predate the schema-v2 authority model, so they must not be retro-classified.

## 3. Policy rows as an authority matrix

The eight tuples partition on three membership facts for a target `P`: `P ∈ read_paths`,
`P ∈ write_paths`, `P ∈ edit_paths`. Reading each row's stated reason literally:

- DECLARED_EDIT → ALLOW, reason "predeclared for edit and for both read and write":
  requires all three memberships.
- UNDECLARED_EDIT → DENY, reason "No implicit edit permission from generic report
  ownership": covers `P ∉ edit_paths`; ownership/write alone does not imply edit.
- READ_ONLY_EDIT → DENY, reason "Read authority never grants a write": covers
  `P ∈ read_paths` with write authority absent.
- WRITE_ONLY_EDIT → DENY, reason "Edit also needs its explicit target read authority":
  names the cell `P ∈ edit_paths`, `P ∈ write_paths`, `P ∉ read_paths`. "Also needs"
  presupposes the write/edit basis and identifies the missing element as read.

Consequence: only DECLARED_EDIT is an ALLOW. Every fixture missing at least one of read,
write, or edit is DENY under at least one row. Two cells are not uniquely named by any row
text: read+edit without write, and edit without read or write. Both are DENY by the
absence of an ALLOW, but their row attribution is undecided by the declared text
(section 9, U2). This distinction matters for falsification: verdict and attribution must
be scored separately.

## 4. Smallest literal metadata fixture

The fixture uses only key names already present in the declared material: the v2
seat-binding shape (`name`, `root`, `read_paths`, `write_paths`, `edit_paths`, `commands`,
`fetches`) and S086's request keys (`tool`, `path`, `argument_keys`). It is a metadata
fixture, not an invocation, and it does not assert the unseen manifest/events schema.

Negative instance — triggers WRITE_ONLY_EDIT, expected DENY (all sections literal):

```json
{
  "seat": {
    "name": "F",
    "root": "/r",
    "read_paths": [],
    "write_paths": ["/r/t.md"],
    "edit_paths": ["/r/t.md"],
    "commands": [],
    "fetches": []
  },
  "request": {
    "tool": "edit",
    "path": "/r/t.md",
    "argument_keys": ["path"]
  }
}
```

Positive control — identical fixture with exactly one added array element:

```json
"read_paths": ["/r/t.md"]
```

That single-element delta changes the class to DECLARED_EDIT → ALLOW. The separating
variable is therefore exactly one literal read-authority membership, not any body field,
argument key, or adapter step. Absolute paths, a single target, and empty
`commands`/`fetches` keep the fixture at the smallest size that still carries name, root,
and the three authority lists.

Boundary variants, each one delta from the negative instance, all DENY:

| variant | read_paths | write_paths | edit_paths | row |
|---|---|---|---|---|
| B read-only | `["/r/t.md"]` | `[]` | `[]` | READ_ONLY_EDIT |
| C undeclared | `[]` | `[]` | `[]` | UNDECLARED_EDIT |
| D edit only | `[]` | `[]` | `["/r/t.md"]` | DENY, unnamed cell (U2) |
| E read+edit | `["/r/t.md"]` | `[]` | `["/r/t.md"]` | DENY, unnamed cell (U2) |
| F write only, no edit authority | `[]` | `["/r/t.md"]` | `[]` | UNDECLARED_EDIT [INFERENCE: edit authority is the subject of the row and is absent; precedence is not declared] |

Variant F is the sharp boundary: write membership without edit authority is not
WRITE_ONLY_EDIT, because the row's stated subject is an edit that has its edit basis and
lacks read authority. The DENY in variant F comes from UNDECLARED_EDIT.

## 5. Exact authority preconditions

For the request record `R` with `tool = edit` and single literal `path = P`, under seat
binding `B`:

1. Structured subject. `R` carries exactly one literal `path`. A request with no structured
   target is OPAQUE_PATCH, not WRITE_ONLY_EDIT, and its target is not inferred from patch
   text.
2. Edit authority present. `P ∈ B.edit_paths`. If absent, the row is UNDECLARED_EDIT.
3. Write authority present. `P ∈ B.write_paths`; this is the basis of the row name. The
   element the reason names as missing is read, not write.
4. Read authority absent. `P ∉ B.read_paths`, compared literally. This is the
   discriminating precondition and the only one that separates the negative fixture from
   its ALLOW control.
5. Literal identity only. `P` is an absolute filesystem path compared entry by entry with
   no dot-segment resolution, no alternate spelling or case folding, and no URI. Dot
   segments and alternate spellings do not expand the list (EDIT_TRAVERSAL); remote or
   internal URIs never become filesystem targets (EDIT_EXTERNAL).
6. Per-entry scoping. If a request expands to several recorded adapter reads or writes,
   each is classified separately (EXPANSION, CHECK_EACH); no batch verdict is derivable
   from one member.
7. Audit-only force. The verdict classifies declared authority plus structured target
   metadata. It does not assert native prevention, that the edit did or did not apply,
   that the target was actually read, or that the recorder saw every step. This follows
   both the policy file's `scope` ("no native prevention, opaque patch interpretation,
   effect or reading proof") and the preregister `limits` ("No native per-seat restrictive
   tool interface exists", "No runtime prevention, effect/reading/recorder-completeness or
   universal tool/patch semantics").

## 6. Source-versus-policy separation

Three distinct roles must not be collapsed:

- Source (S086) supplies observed structured request facts: tool name, literal path,
  argument-key set, adapter-step lines. It supplies no authority set and no verdict, and
  its scope explicitly disclaims effects and reading proof.
- Policy (`edit-decision-policy.json`, mirrored by `preregister.json` `edit_decisions`)
  supplies the rule tuples: class name, verdict, reason, evidence id, policy id.
- Binding (the schema-v2 declaration sets) supplies the authority facts the rule consumes:
  which literal paths a seat may read, write, and edit. It is not among this seat's
  declared read paths, so its exact schema is inferred from this seat's binding shape and
  from S086's key vocabulary only.

A verdict is a join of all three. Neither S086 alone nor the policy file alone can assign
WRITE_ONLY_EDIT to any particular request. In particular, the policy cites S086 as
evidence that structured edit requests exist and carry explicit targets; it does not cite
S086 as proof of the DENY. Conversely, an observed read at line 12 before an edit at line
15 (CritRuntime) is a transcript sequence, not read authority, and an observed successful
edit would not overturn an audit classification.

## 7. What would falsify this decision

Verdict falsifiers (would show DENY is wrong):

- Any declared rule that assigns ALLOW to a structured edit whose target is in
  `edit_paths` and `write_paths` but absent from `read_paths`.
- Any declared derivation that read authority follows from write or edit authority
  (implicit closure), which would make the negative fixture ALLOW.
- Any declared row that grants edit permission from write ownership alone and is stated to
  override the WRITE_ONLY_EDIT row for the negative fixture.

Reason falsifiers (would leave DENY but break the stated necessity of read authority):

- Evidence that DECLARED_EDIT is reachable with `P ∉ read_paths`, i.e. that its ALLOW
  precondition is edit+write only. This contradicts the row's own "for both read and
  write" text and would falsify the reason, not necessarily a separate deny rule.

Reachability falsifier (not a verdict falsifier):

- A schema-v2 binding in which `read_paths` is required to contain `write_paths ∪
  edit_paths`, making a write-only-but-editable target unrepresentable. The row would then
  be unreachable rather than wrong, and the operability claim would fail.

Attribution falsifiers (row identity, not always the verdict):

- A request with no structured target → OPAQUE_PATCH / UNKNOWN.
- Multiple targets in one request → EXPANSION / CHECK_EACH.
- A URI or dotted alternate spelling → EDIT_EXTERNAL or EDIT_TRAVERSAL.
- Write membership without edit authority → UNDECLARED_EDIT.
In these cases DENY may persist, so verdict accuracy and row-attribution accuracy are
separate scores.

Non-falsifiers: body content, edit success or failure, actual reads, or recorder
completeness. Bodies are omitted from S086 and explicitly outside its scope; the
preregister limits exclude effect, reading, and recorder-completeness claims. An applied
edit on a write-only path is exactly what an audit-only DENY predicts is possible when no
native enforcement exists; it cannot falsify the classification.

## 8. Confidence

- High: the literal tuple, the ALLOW-only-DECLARED_EDIT structure, the one-element
  separating delta, and the audit-only force. All are stated in the declared policy,
  preregister, and S086 scope.
- Medium: the mapping of variant F to UNDECLARED_EDIT and the requirement that
  `edit_paths` membership is part of WRITE_ONLY_EDIT. This is read from the reason text
  ("also needs") and the row names, not from a declared precedence table.
- Not verified: the exact v2 manifest/events schema, row precedence for overlapping
  cells, and selector-suffix treatment.

## 9. Remaining unknowns

- U1. Exact schema-v2 manifest and event fields, and whether `write_paths` membership is
  mandatory for WRITE_ONLY_EDIT as opposed to merely naming it. Neither
  `bindings.json` nor `events.json` is in this seat's declared read set; the fixture shape
  is [INFERENCE].
- U2. Precedence among rows for read+edit without write, and edit without read or write.
  The declared text gives no ordering; the verdict for those cells is DENY only by the
  absence of an ALLOW.
- U3. Whether an authority entry carrying a selector suffix (S086 shows `:raw` on a
  recorded read path) matches a plain request path for precondition 4. The observation is
  about a recorded step, not a declared authority entry.
- U4. Whether `write`-tool requests fall under any of the eight `*_EDIT` rows. S086's
  observed requests use `tool = edit`; EXPANSION's mention of recorded adapter writes is a
  scoping rule, not an authority grant.
- U5. Whether the eight rows are enforced anywhere or remain declarative audit policy.
  The preregister limit "No native per-seat restrictive tool interface exists" and the
  policy scope both indicate declarative only; this oracle makes no runtime claim.

## 10. Axis check

Axes for this oracle: literal fidelity to declared source, fixture minimality, separation
of source from policy, and falsifiability precision. The report keeps only moves that
improve one axis without weakening another: no fixture field is added beyond what the
decision consumes, no observation is promoted to authority, and falsifiers are split into
verdict, reason, reachability, and attribution so that a failure in one is not misread as
a failure of another.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditwriteonlyedit
Scope: executed=none
