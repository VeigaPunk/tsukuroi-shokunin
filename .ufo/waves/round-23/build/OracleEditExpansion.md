# OracleEditExpansion — EXPANSION ⇒ CHECK_EACH

Round 23, attempt 1 · seat `TsukuroiR23-2.OracleEditExpansion-7` · baseline `ae01e50f582016384e620022be38bf5367000e2e`.
Source-only oracle. No command, checker, example runner, hash, listing, import or subprocess was executed (NO-EXEC; NO-FETCH). The reviewed digest is a supplied declaration, not recomputed here. Nothing in this report asserts that any adapter step occurred, that any byte was read or written, that any write or edit applied, or that any verdict is enforced at runtime.

## Axes (godspeed)

- **A** — fixture minimality and literality: fewest literal fields that still discriminate `CHECK_EACH` from a request-level verdict.
- **B** — authority-precondition exactness: what must hold for the classification to be well-defined.
- **C** — source-vs-policy separation: which facts come from S086, which from the round-23 pre-register, and which links are policy-asserted.
- **D** — falsifiability without body/effect semantics.

Moves kept below improve at least one axis and harm none: no row is re-decided, no other row's scope is widened, no historical record is rewritten.

## 1. The row as declared

`edit-decision-policy.json` `$.decisions[7]` (mirrored verbatim at `preregister.json` `$.edit_decisions[7]`):

| field | value |
|---|---|
| id | `EXPANSION` |
| decision | `CHECK_EACH` |
| reason | "Every recorded adapter read or write remains separately scoped" |
| evidence | `S086` |
| policy | `round23-preregister` |

Supporting policy context, observed:

- `$.scope` — "Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof."
- `$.source_path` — `.ufo/waves/round-23/sources/structured-edit-observations.json`.
- `preregister.json` `$.claims[0]` (C1) counts this row inside "Eight finite source-grounded structured-edit authority decisions"; `$.ordinals.depth = 8`.
- `preregister.json` `$.separability` — C1 reads only the new decision/prose/source contract; C2 reads only explicit v2 authority and captured events. So this oracle may use the *shape* of declared per-mode authority as an interface, but must not lean on C2 production content.
- `preregister.json` `$.limits` — "No native per-seat restrictive tool interface exists"; no runtime prevention, no recorder-completeness claim.
- `preregister.json` `$.sources_opened` — "S086 prospective: observed structured edit request keys and recorded adapter steps."

## 2. Source facts (S086) — observed

`structured-edit-observations.json`, four observation records, schema `tsukuroi-structured-edit-observations-v1`:

| record | seat | tool | `argument_keys` | `path` (rel. root) | `recorded_starts` |
|---|---|---|---|---|---|
| `$.observations[0]` | CritRuntime | `edit` | `path`, `stream_content` | `…/round-22/build/CritRuntime.md` | 2 entries: `{line 12, read, …CritRuntime.md:raw}`, `{line 13, write, …CritRuntime.md}` |
| `$.observations[1]` | OraclePathArtifact | `edit` | `i`, `new_string`, `old_string`, `path` | `…/round-22/build/OraclePathArtifact.md` | 1 entry: `{line 31, edit, same path}` |
| `$.observations[2]` | OraclePathArtifact | `edit` | `i`, `new_string`, `old_string`, `path` | `…/round-22/build/OraclePathArtifact.md` | 1 entry: `{line 34, edit, same path}` |
| `$.observations[3]` | OraclePathArtifact | `edit` | `i`, `new_string`, `old_string`, `path` | `…/round-22/build/OraclePathArtifact.md` | 1 entry: `{line 37, edit, same path}` |

Additional observed facts:

- `request_line` values are 15, 30, 33, 36. Records 1–3 place their single recorded step at `request_line + 1`; record 0 places both recorded steps at lines **12 and 13, before** its `request_line` 15.
- Bodies are absent from the source: `body_fields` = "omitted; no report text copied". Only key names are recorded (`new_string`, `old_string`, `stream_content`).
- Step `tool` values observed: `read`, `write`, `edit`. Request tool is always `edit`.
- One recorded step path is textually different from its request path: `…CritRuntime.md:raw` vs `…CritRuntime.md` (selector suffix).
- Source scope, verbatim: "Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof."

## 3. Derivation of CHECK_EACH

The decision vocabulary in this table is `ALLOW`, `DENY`, `UNKNOWN`, plus this row's `CHECK_EACH`. Exclusion over a single request-level verdict:

1. **Not request-level `ALLOW`.** A request carries one `path`, but a recorded step may carry a *different path string* (`…CritRuntime.md:raw`) and a *different tool* (`edit` request → `read`/`write` steps). A verdict keyed only on the request path therefore does not decide the recorded step text; treating it as `ALLOW` silently extends authority to a string that was never the request's exact target. This is the observed-shaped hazard, independent of whether that particular record is a same-request expansion (§7 G3).
2. **Not request-level `DENY`.** In the same record the write step targets the exact request path, and records 1–3 are identity mappings (`edit`→`edit`, same path). A blanket `DENY` of any request with recorded steps would refuse steps that are themselves the declared exact target, conflicting with `DECLARED_EDIT` (`$.decisions[0]`: "Exact target is predeclared for edit and for both read and write").
3. **Not request-level `UNKNOWN`.** `OPAQUE_PATCH` (`$.decisions[4]`) is the missing-structured-target case ("Missing structured target is not inferred from opaque patch text"). Here the request path and every step path are structured literal strings, so that condition does not hold.
4. **Therefore per-step classification.** `CHECK_EACH` names the *unit of evaluation*, not an outcome: evaluate every recorded step against the authority for that step's own mode, and aggregate conjunctively (`ALLOW` iff all recorded steps are `ALLOW`; otherwise the aggregate is the failing step's `DENY`). `CHECK_EACH` is not itself `ALLOW`, and it is not satisfied by one request-level check.

Scope boundary of the derivation: it concerns **where the verdict is applied** (per recorded step) and **what it is applied to** (literal step `path` under step `tool`). It does not decide selector semantics (`EDIT_TRAVERSAL`), URI semantics (`EDIT_EXTERNAL`), or patch-body semantics (`OPAQUE_PATCH`).

## 4. Smallest literal fixtures

These are metadata fixtures for the C1 decision contract. They are not transcript records: no digest, call id or line number is invented. They are checker-agnostic; the discriminating fields are `tool`, `path`, `recorded_starts`, per-mode `authority`, and `expected`. No checker was invoked.

### 4.1 Positive — expansion where every step is separately authorized

```json
{
  "tool": "edit",
  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md",
  "recorded_starts": [
    {
      "tool": "read",
      "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    },
    {
      "tool": "write",
      "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    }
  ],
  "authority": {
    "read_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    ],
    "write_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    ],
    "edit_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    ]
  },
  "expected": {
    "classification": "CHECK_EACH",
    "per_step": ["ALLOW", "ALLOW"],
    "aggregate": "ALLOW"
  }
}
```

Why this is smallest: one request path; two steps is the minimum that makes the row non-vacuous; the three per-mode lists the seat declares are each required by exactly one actor (request `edit` → `edit_paths`; step `read` → `read_paths`; step `write` → `write_paths`), and each holds the same single literal path. Removing either step collapses the case to 1:1, where `EXPANSION` cannot be distinguished from `DECLARED_EDIT`; removing a mode list leaves one actor undecidable.

### 4.2 Negative — one expanded step outside its own mode's authority

```json
{
  "tool": "edit",
  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md",
  "recorded_starts": [
    {
      "tool": "read",
      "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    },
    {
      "tool": "write",
      "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json"
    }
  ],
  "authority": {
    "read_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json"
    ],
    "write_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    ],
    "edit_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/OracleEditExpansion.md"
    ]
  },
  "expected": {
    "classification": "CHECK_EACH",
    "per_step": ["ALLOW", "DENY"],
    "aggregate": "DENY"
  }
}
```

Discriminator: the request `path` itself is fully authorized for read, write and edit, so any evaluator that checks only the request target returns `ALLOW`; the correct per-step evaluation returns `DENY` at the second step because `preregister.json` is read-authorized but not write/edit-authorized. Both paths are literal and their declarations are literal (this seat's binding). Removing the first step would turn the example into `UNDECLARED_EDIT`, not `EXPANSION`; the pair is the minimum that isolates the expansion effect.

### 4.3 Observed-shape variant — selector-suffixed step path (cross-row)

```json
{
  "tool": "edit",
  "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md",
  "recorded_starts": [
    {
      "tool": "read",
      "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md:raw"
    },
    {
      "tool": "write",
      "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md"
    }
  ],
  "authority": {
    "read_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md"
    ],
    "write_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md"
    ],
    "edit_paths": [
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/CritRuntime.md"
    ]
  },
  "expected": {
    "classification": "CHECK_EACH",
    "per_step": ["DENY", "ALLOW"],
    "aggregate": "DENY"
  }
}
```

This variant is the only one whose path strings are taken verbatim from S086. The `DENY` for the selector read is not this row's decision — non-identical spellings are routed by `EDIT_TRAVERSAL` (`$.decisions[5]`); `EXPANSION` contributes only the requirement that the step be evaluated at all. Whether these two recorded steps are steps *of* the line-15 request is unresolved (§7 G3).

## 5. Exact preconditions

### 5.1 Fixture well-formedness (W)

- **W1** The request has exactly one `path` field whose value is a literal string; no list, glob, URI or missing target. (S086: all four records have a single `path` string.)
- **W2** `recorded_starts` is a finite array; every entry has a literal `tool` and a literal `path`. (S086 shape.)
- **W3** Every step path is a filesystem path string; non-filesystem forms are out of this row (`EDIT_EXTERNAL`).
- **W4** Bodies are absent or opaque; the classification is computable from key names and path strings alone. (S086: bodies omitted; only `argument_keys` recorded.)
- **W5** Step count is data-dependent and is not deduplicated or normalized. (S086 shows 2 and 1.)

### 5.2 Authority preconditions (A)

- **A1** Per-mode authority sets exist and are distinct for read versus write/edit (this seat's binding declares `read_paths`, `write_paths`, `edit_paths` separately; C2 scope is "exact predeclared structured edit targets"). With a single undifferentiated path list, "separately scoped" would have no operational content.
- **A2** Membership is exact literal string equality in the mode's own set. No selector stripping, dot-segment folding, symlink resolution, or case folding is implied by this row; alternate spellings are `EDIT_TRAVERSAL`'s domain.
- **A3** A request-path declaration implies nothing about step authority; step authority is read only from that step's mode set. Conversely, a step being authorized does not require the request path to be authorized (the positive fixture makes them coincide only for minimality).
- **A4** Every recorded step is evaluated and its per-step outcome retained; a first-failure short-circuit would not "check each". The aggregate is the conjunction of step verdicts, and `CHECK_EACH` must not be collapsed into an aggregate token.
- **A5** The row applies only with at least one recorded step. With zero recorded steps, `OPAQUE_PATCH`/`UNKNOWN` (`$.decisions[4]`) applies instead; absence of steps is not a pass.
- **A6** The audited domain is the recorded step list only. S086 explicitly disclaims recorder completeness, and `preregister.json` `$.limits` disclaims runtime prevention; a `DENY` here is an audit verdict over recorded metadata, never enforcement.
- **A7** Separability: the fixture consumes the *interface* of declared per-mode authority, not C2 production artifacts or captured events (`preregister.json` `$.separability`).

## 6. Source versus policy separation

| Element | S086 observation file | Round-23 policy |
|---|---|---|
| Single literal request `path` | observed, all four records | schema requires a predeclared exact target (`DECLARED_EDIT`) |
| One request associated with two recorded steps | observed once (`$.observations[0]`), association ambiguous (G3) | `CHECK_EACH` makes per-step scoping normative |
| Step `tool` values `read`/`write`/`edit` | observed values | reason names "adapter read or write" only (G2) |
| Step path textually different from request path (`:raw`) | observed once | routed to `EDIT_TRAVERSAL`, not this row |
| Per-mode authority lists | not present in source | seat binding v2 interface / C2 scope |
| "separately scoped" | not a source fact | reason text of this row |
| `S086` label | the observation file never self-labels as S086 | `evidence` field plus `source_path` link it (G4) |

**G1 — evidence is not discriminating.** All eight decisions share `evidence: "S086"` (`$.decisions[*].evidence`), so S086 cannot select `EXPANSION` over the other seven. Source-only derivation therefore constrains the *admissible* classification (§3); the policy's reason string selects the token. The row is not "proved" by S086 in isolation.

**G2 — wording quantifier and `edit` steps.** Three of four S086 records have `recorded_starts[0].tool = "edit"`, while the reason says "adapter read or write". Under a strict literal reading, `edit` steps are outside this row's stated quantifier. Resolutions: (a) treat the adapter's edit as a write-class action, or (b) restrict this row to read/write steps and treat edit steps as `DECLARED_EDIT` positives. The positive fixture (§4.1) deliberately uses `read`+`write` to stay inside the literal vocabulary. Observed text: high confidence; interpretation: medium.

**G3 — association ambiguity.** Records 1–3 place one step at `request_line + 1`, consistent with per-request rendering. Record 0 places two steps at lines 12 and 13, *before* its request at line 15. Either (i) the same assistant turn batched `read`, `write`, `edit` and `recorded_starts` covers the turn, or (ii) those are earlier, unrelated calls and record 0 has no post-request step. Reading (ii) would leave every observation 1:1 and remove the only observed 1:many instance. Observed line facts: high confidence; association reading: medium.

**G4 — label linkage is policy-asserted.** `$.sources_opened` calls S086 "prospective"; the observation file carries no S086 identifier. The mapping S086 → `structured-edit-observations.json` exists only through the policy's `source_path`. This report treats S086 as the policy's label for that file, not as a source self-description.

## 7. Falsification (metadata level only)

A falsifier here must be observable in structured path/tool metadata. None of these claims involve bodies, effects, reading proof, recorder completeness, or runtime prevention.

- **F1 — vacuous domain (weakens the evidence, not the rule).** If every recorded structured request had exactly one step with the same `tool` and `path`, `CHECK_EACH` would be extensionally equal to `ALLOW` for declared targets and this row would have no discriminating instance. S086 does not robustly refute this: records 1–3 are identity 1:1 and the only 2-step record is association-ambiguous (G3). A corpus of all-identity records falsifies the row's evidentiary support, not its normative text.
- **F2 — atomic grant (would falsify the classification).** A source-visible policy statement granting all adapter steps of a declared request target transitively from the request declaration would contradict `CHECK_EACH`. Search of the declared policy and pre-register text found none: `DECLARED_EDIT` says "Exact target is predeclared for edit and for both read and write" — the exact target only, with no transitivity to other step paths. Not falsified.
- **F3 — mode collapse (would falsify precondition A1).** An authority schema with one undifferentiated path list would make "separately scoped" unevaluable. This seat's declared v2 binding has `read_paths`, `write_paths`, `edit_paths`; the row is not falsified here. If final v2 collapsed modes, A1 would fail and `CHECK_EACH` would have no decision procedure.
- **F4 — non-literal step target (would degrade the row for that step).** A recorded step path that is a URI, descriptor, glob or otherwise non-literal filesystem string makes exact per-step membership undecidable; the step would have to be `UNKNOWN` or routed to `EDIT_EXTERNAL`. Not observed in S086.
- **F5 — recorder gap (boundary, not falsifier).** A captured adapter read/write for the same request that is absent from `recorded_starts` would show the audited list differs from adapter activity. That falsifies record completeness relative to behavior, which S086 already disclaims; it neither confirms nor refutes per-step scoping, and must not be cited as either.
- **F6 — misapplication (falsifies an implementation, not the text).** A checker that treats `/P` and `/P:raw` as equal, or that returns a request-level `ALLOW` while any step is `DENY`, misapplies the row. No checker was read or invoked; source-only evidence cannot decide checker behavior.

## 8. Residual unknowns

- **U1** Whether `recorded_starts` is defined as the adapter steps of the enclosing request or as the first recorded calls of the seat's sequence; the declared source supplies no field definition (G3).
- **U2** Whether the policy vocabulary counts `edit` as an "adapter write" for the reason string (G2).
- **U3** Whether the final v2 schema exposes three mode lists for every seat, not only for this seat's binding (F3).
- **U4** Completeness of `recorded_starts` relative to adapter activity — out of scope by declaration (F5).
- **U5** The checker envelope for these fixtures — the C1 checker was neither read nor invoked.

## Non-claims

No body content was read or inferred (`new_string`, `old_string`, `stream_content` are names only). No effect, success, reading proof, recorder completeness, universal adapter semantics, or native/runtime enforcement is claimed. `CHECK_EACH` is an audit classification over structured metadata; `DENY` in a fixture is a per-step audit outcome, not prevention.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-oracleeditexpansion
Scope: executed=none
