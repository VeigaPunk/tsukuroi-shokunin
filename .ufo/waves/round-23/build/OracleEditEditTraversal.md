# OracleEditEditTraversal — `EDIT_TRAVERSAL` → `DENY`

Source-only derivation. No checker, example, test, formatter, or command was invoked; no
digest was recomputed. The policy digest `f6f73a1a…f96c805` is taken as supplied identity.
NO-EXEC / NO-FETCH was honored: only the bound local reads below were performed.

Sources opened:

- `.ufo/waves/round-23/sources/edit-decision-policy.json` (declared SHA-256 `f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805`)
- `.ufo/waves/round-23/preregister.json`
- `.ufo/waves/round-23/sources/structured-edit-observations.json` (cited by the policy as `source_path`)
- `skill://godspeed`

Labels: **observed** = literally present in an opened file; **derived** = forced by the
opened text; **inference** = plausible but not enumerated by the sources.

---

## 1. Observed source facts (S086 layer)

The observations file (`tsukuroi-structured-edit-observations-v1`, `accessed: 2026-10-21`)
contains four records:

| `request_line` | seat | `tool` | `argument_keys` | `path` |
|---|---|---|---|---|
| 15 | CritRuntime | `edit` | `path`, `stream_content` | `…/round-22/build/CritRuntime.md` |
| 30 | OraclePathArtifact | `edit` | `i`, `new_string`, `old_string`, `path` | `…/round-22/build/OraclePathArtifact.md` |
| 33 | OraclePathArtifact | `edit` | `i`, `new_string`, `old_string`, `path` | `…/round-22/build/OraclePathArtifact.md` |
| 36 | OraclePathArtifact | `edit` | `i`, `new_string`, `old_string`, `path` | `…/round-22/build/OraclePathArtifact.md` |

Observed in every record:

- `tool` is the literal string `edit`; `path` appears in `argument_keys` and is a literal
  absolute path under
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/`.
- `body_fields` is `"omitted; no report text copied"` — no body data exists in this layer.
- `recorded_starts` lists adapter steps with `line`, `tool`, and literal `path`; the tools
  observed there are `read`, `write`, and `edit`.
- One read step records `…/CritRuntime.md:raw`. `:raw` is an adapter read selector inside a
  `read` step; it is not part of any `edit` `path` value.
- Every recorded path is a literal, already-normalized absolute string: no `.` segment, no
  `..` segment, no doubled separator, no trailing separator, no relative spelling, and no
  variant of an adjacent record's path.
- The file's own `scope` says: observed structured path metadata and recorded adapter steps
  only — "not universal tool semantics, native permission enforcement, effects, or reading
  proof."

**Derived:** S086 supplies the *shape* of a structured edit target (an `edit` call with a
string `path` argument) and literal path values. It supplies **no** traversal instance and
**no** decision vocabulary: the strings `ALLOW`, `DENY`, `UNKNOWN`, `CHECK_EACH`, and
`EDIT_TRAVERSAL` do not occur in this file.

## 2. Observed policy facts (normative layer)

`edit-decision-policy.json` (`schema: tsukuroi-edit-policy-v1`) has eight rows. The sixth
(`decisions[5]`) is, verbatim:

```json
{
  "id": "EDIT_TRAVERSAL",
  "decision": "DENY",
  "reason": "No dot-segment or alternate spelling expands the target list",
  "evidence": "S086",
  "policy": "round23-preregister"
}
```

All eight rows carry `evidence: "S086"` and `policy: "round23-preregister"`. The policy
file also declares `source_path: ".ufo/waves/round-23/sources/structured-edit-observations.json"`
and `scope: "Declared audit authority for structured target metadata only; no native
prevention, opaque patch interpretation, effect or reading proof."`

`preregister.json` `edit_decisions[5]` is the identical triple:

```json
["EDIT_TRAVERSAL", "DENY", "No dot-segment or alternate spelling expands the target list"]
```

The preregister's C1 claim binds the metric `validated_edit_decisions` to target `8`, scope
"Eight finite source-grounded structured-edit authority decisions"; its `limits` state "No
native per-seat restrictive tool interface exists" and "No runtime prevention,
effect/reading/recorder-completeness or universal tool/patch semantics."

**Derived:** the rule's *authority* is the `(id, decision, reason)` triple duplicated
verbatim in the policy file and the preregister. The shared `evidence: "S086"` does not
discriminate this row from the other seven; the reason string is what selects it. The
policy and preregister copies agree at the opened revision, so there is no divergence to
reconcile.

## 3. Decision content — literal reading

**Derived, strictly from the reason text plus the `DECLARED_EDIT`/`UNDECLARED_EDIT` rows:**

1. The declared edit targets are a set of **literal strings**. `DECLARED_EDIT`'s ALLOW
   requires the exact target to be "predeclared for edit and for both read and write".
2. A request path that reaches a declared target only by inserting/removing a dot-segment or
   substituting an alternate spelling is **not** that declared string. Because such a
   variant does not "expand the target list", the request is not authorized by the declared
   target and the row's verdict is `DENY`.
3. The rule is a **literal-string non-expansion rule**, not a path-normalization rule and
   not an effect rule. It does not assert that the variant resolves to the declared file; it
   does not assert that resolution would be refused by the operating system, the adapter, or
   the harness; it does not assert anything about bytes written or read.

**Inference (not stated):** the reason's phrase "target list" most naturally denotes the
seat's declared write/edit path set (the same list `DECLARED_EDIT` consults). No other list
is named anywhere in the two opened files.

## 4. Exact authority preconditions

For the verdict `EDIT_TRAVERSAL → DENY` to be attributable to this row (rather than to
another row or to no rule), all of the following must hold.

| # | Precondition | Basis |
|---|---|---|
| P1 | A policy row exists with `id = EDIT_TRAVERSAL` and `decision = DENY`, reason "No dot-segment or alternate spelling expands the target list". | policy `decisions[5]`, observed |
| P2 | The preregister's `edit_decisions` contains the same triple, so the row's `policy: "round23-preregister"` binding is satisfied. Both opened copies agree. | preregister `edit_decisions[5]`, observed |
| P3 | The event is a **structured** edit request: `tool = edit` and an argument key `path` whose value is a string. | S086 record shape, observed |
| P4 | A declared per-seat target list exists for the same revision, and the **base** target is declared for **both** read and write. This isolates traversal from `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, and `WRITE_ONLY_EDIT`. | `DECLARED_EDIT` reason, derived |
| P5 | The requested `path` string is not byte-identical to any declared edit target, and the difference is a dot-segment or alternate-spelling variant of exactly one declared target. | row reason, derived |
| P6 | No policy rule or preregister clause admits normalization/canonical equivalence for edit targets. None does at this revision. | policy + preregister, observed absence |
| P7 | The verdict is recorded at the declared-audit level only: structured target metadata, no native prevention, no opaque-patch interpretation, no effect or reading proof. | policy `scope`, observed |
| P8 | The evidence binding `S086` is respected as *support for event shape and literal path metadata only*, never as the source of the norm. | observations `scope`, derived |

Preconditions that would route the same event to a **different** row instead:

- `path` absent or unparseable (opaque patch text) → `OPAQUE_PATCH` → `UNKNOWN`; the row
  cannot fire because there is no target string to compare (P3 fails).
- `path` exact-matches a declared write target **and** an exact declared read target →
  `DECLARED_EDIT` → `ALLOW`; this is the positive control (P5 fails).
- `path` exact-matches a declared write target but not any declared read target →
  `WRITE_ONLY_EDIT` → `DENY`; already denied without traversal reasoning.
- `path` is a URI / non-filesystem scheme → `EDIT_EXTERNAL` → `DENY`; the row's "alternate
  spelling" wording does not reach URI schemes because that row is apposite.

**Overlap note (derived):** a traversal variant of a path that is declared nowhere is both
"not literal" and "undeclared"; `EDIT_TRAVERSAL` and `UNDECLARED_EDIT` then yield the same
`DENY`, so the outcome is stable but the attribution is not unique. Attribution to
`EDIT_TRAVERSAL` specifically requires P4 — the base target must be declared, so spelling is
the only defect — and P5.

## 5. Smallest literal valid fixture (declarative only, not executed)

Not passed to any checker and not "invoked"; it is a literal metadata record pair for a
reviewer to inspect. Body fields are omitted exactly as S086 omits them. `D` is this seat's
declared edit path, taken verbatim from the binding.

**Positive control (does not trigger the row; `DECLARED_EDIT` ALLOW is available because
read and edit are both exactly declared):**

```json
{
  "declared": {
    "read": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditTraversal.md"],
    "edit": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditTraversal.md"]
  },
  "event": {
    "tool": "edit",
    "argument_keys": ["path"],
    "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditEditTraversal.md"
  }
}
```

**Negative (minimal `EDIT_TRAVERSAL` → `DENY` instance):** same declared pair, event path
with the single two-character insertion `/./`:

```json
{
  "tool": "edit",
  "argument_keys": ["path"],
  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/./OracleEditEditTraversal.md"
}
```

Why this is the smallest *valid* negative:

- It differs from `D` by exactly two characters (`.` and `/`), the minimum insertion that
  creates a **dot-segment**, which the reason names explicitly.
- A one-character insertion such as `build//OracleEditEditTraversal.md` (doubled separator)
  is smaller, but "alternate spelling" is not enumerated in the policy, so its membership in
  the row is **inference**, not derived. The `/./` form is inside the explicitly named
  "dot-segment" family.
- A `..` form costs at least three inserted characters (`…/build/../build/…`) and adds no
  distinguishing authority, so it is not smaller.
- The fixture carries no transcript digest, line number, body field, or adapter step: those
  do not participate in the decision, so including them would enlarge the fixture without
  adding validity.

## 6. Source-vs-policy separation

| Layer | File | Carries | Does not carry |
|---|---|---|---|
| Observation (source) | `sources/structured-edit-observations.json` | seat/agent, transcript digest, request line, call id, tool name, argument keys, literal `path`, omitted-body marker, adapter steps | any decision id or verdict; any norm; any traversal instance; any effect, reading, or enforcement fact |
| Policy (norm) | `sources/edit-decision-policy.json` | the eight `(id, decision, reason)` rows, shared evidence pointer, `policy` pointer, `source_path`, scope ceiling | event instances; proof that any instance occurred; body data; enforcement capability |
| Binding (preregister) | `preregister.json` | the same eight triples under `edit_decisions`, C1 metric/target/scope, separability, limits | event instances; policy semantics beyond the reason strings |

Consequences:

1. **Neither layer alone yields the verdict.** S086 cannot produce `DENY`: it has no verdict
   vocabulary and no traversal record. The policy cannot produce an *instance*: it names no
   event, seat, request line, or path. The verdict is the policy row applied to a structured
   metadata shape; a confirming instance requires an S086-shaped event record, and the
   opened S086 contains none.
2. **Evidence is non-discriminating.** Because all eight rows cite `S086`, the row's specific
   authority is its `(id, reason)` pair plus the preregister duplication, not the evidence
   code.
3. **No effect claim may cross the boundary.** The policy scope explicitly withholds native
   prevention, opaque-patch interpretation, effect, and reading proof; the observation scope
   explicitly withholds universal tool semantics, native enforcement, effects, and reading
   proof. Therefore:
   - the `DENY` means "the literal target list is not expanded", not "the write was
     blocked";
   - it is not evidence that the file was or was not modified;
   - it is not evidence that any body was or was not read;
   - it is not evidence of how any adapter or filesystem resolves the spelling.

## 7. What would falsify `EDIT_TRAVERSAL → DENY`

Each is a falsifier of the *decision as bound at this revision*, stated without touching
body or effect semantics.

**F1 — Binding divergence.** If `preregister.json` `edit_decisions` did not contain the same
triple (different decision, or a reason admitting normalization), the policy row would lack
the authority it cites and the `DENY` would not be the declared round-23 decision. (At the
opened revision both copies agree verbatim, so this is not the case.)

**F2 — A declared target whose own literal string is the "variant".** If the seat's declared
edit target were literally
`…/round-23/build/./OracleEditEditTraversal.md`, then an event carrying exactly that string
is a literal `DECLARED_EDIT` match; the premise that spelling would expand the list fails,
and `DENY` would be wrong for that event. This falsifies the verdict for the instance, not
the general non-expansion statement.

**F3 — An admitted equivalence rule.** A policy/preregister clause defining edit-target
equality up to dot-segment normalization, or otherwise admitting an alternate spelling,
would make `DENY` false for normalized-equal paths.

**F4 — A recorded ALLOW instance of the forbidden shape.** An S086-style structured record
whose `path` is a dot-segment/alternate-spelling variant of a declared target, with the base
target declared for read and write, adjudicated `ALLOW` under this same policy. None exists
in the opened file; the row currently has no confirming *or* disconfirming instance.

**F5 — Row absence or mutation.** If `decisions[5]` were absent, renamed, or carried
`ALLOW`/`UNKNOWN`/`CHECK_EACH`, the derived verdict would not exist. A policy file whose
schema is not `tsukuroi-edit-policy-v1` would not be this authority at all.

**F6 — Evidence misbinding.** If `S086` did not denote the opened observations (or those
observations lacked the `path`-bearing structured edit shape), the row's cited support for
P3 would fail, leaving the verdict unsupported at the audit level even if the reason string
still read `DENY`.

**Non-falsifiers (explicitly out of scope):**

- Proof that the variant resolves to the same inode or an in-root path.
- Proof that a write through the variant would be a no-op, or that the file's bytes were
  unchanged before/after.
- Proof that the adapter, OS, or harness would accept or reject the spelling.
- Any body-content, side-effect, or read-completeness observation.
- A different tool's behavior with dot-segments.

These test resolution/effect, which both layers' scopes exclude; they cannot confirm or
overturn a literal-target-list verdict.

## 8. Residual unknowns

1. **"Alternate spelling" is unenumerated.** Doubled separators, trailing separators,
   relative forms, `..` segments, and adapter-selector suffixes are not classified by the
   policy. Only the "dot-segment" family is named. Any application of the row to those forms
   is inference, not derivation.
2. **Row precedence is undefined.** The policy is an unordered table of eight ids with no
   arbitration rule. Overlapping cases (traversal variant of an undeclared path; traversal
   variant lacking read authority) are outcome-stable (`DENY` either way) but
   attribution-ambiguous.
3. **No confirming instance.** S086 contains four exact, already-normalized edit paths (all
   the same round-22 build directory) and one `read` step with a `:raw` selector. The
   `EDIT_TRAVERSAL` row is therefore a forward rule at this revision, not an induced
   observation.
4. **Whether `path` may be non-string** (e.g. a list) is not covered by S086 or the policy;
   a non-string target would fall outside P3 and cannot be adjudicated by this row as
   written.
5. **Selector-vs-spelling boundary.** `:raw` is observed only on a `read` path. Whether the
   policy would treat an edit `path` carrying an adapter selector as an "alternate spelling"
   is unstated; the row's wording is about filesystem spellings, but the policy does not say
   so explicitly.
6. **Enforcement status.** Per the preregister limits, no native per-seat restrictive tool
   interface exists. This report derives an audit decision only and makes no runtime
   enforcement claim.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditedittraversal
Scope: executed=none
