# SourceReopen84 — outside admit S084 and additive-only tool semantics

Scoped scout report. Root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. NO-EXEC / NO-FETCH: no commands, no subprocess, no hashing, no installs, no production/VCS/ref/route writes. The declared source digest is supplied identity, not independently computed.

## Axes

- A1 Authority fidelity: quote the admission and the boundary record; do not widen "additive extras" into runtime guarantees.
- A2 Immutability: reopen/use is append-only; identity, provenance, digest, and admission history stay byte-identical.
- A3 Traceability: every proposed use names its consumer and the exact evidence pointer.
- A move is kept only if it improves one axis without harming the other two.

## Observed evidence

1. `r22-closure.json` (declared SHA-256 `e13cde76422140a13284f730950f2bf36d308d55e30ce956bc59ff5af7d9e68c`, not recomputed), `verification.spotcheck`:
   > Admit S084: agree; host-tool-boundary.json records native_per_seat_allowlist=false and tools as eval-defined additive extras, matching the closure agent's own exposed task schema (tools param has no restriction semantics).
   The same field states the review is "Recorded in this MANIFEST entry only (no lane writes)". `notes` adds: "Native per-seat enforcement remains absent and routed to kumitate/operator (PROVINCE ADJ-05; inherited r21 NO-EXEC L0 question)."
2. `round-22/sources/host-tool-boundary.json` (`tsukuroi-host-tool-boundary-v1`, date 2026-10-21):
   - `tools_semantics`: "Eval-defined additive extras; not an allowlist or replacement of native tools."
   - `native_per_seat_allowlist`: `false`.
   - `authority`: "Main message to TsukuroiR22: Confirmed: no host-native per-seat allowlist exists in the task dispatch path".
   - `approved_scope`: "prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence not preventive enforcement".
   - `task_fields` exposes `tasks[{task,solutionSpace,name?,agent?,tools?,sourceSession?,model?}]`; `tools` is optional.
3. `round-23/preregister.json`:
   - `outside_round22`: entry 422, `admitted: true`, verifier `CloseKaidoku22`, commit `4482c275f9381f219ee4d092e0324d417c3cb1e7`; scope treats outside observations as ground truth and r23 as explaining classifier/unit differences rather than rerunning closure.
   - C2 scope: "New explicit schema-v2 audit authority for exact predeclared structured edit targets; legacy schema-v1 policy and historical reds unchanged. Body data opaque, no native enforcement/effects claim."
   - `limits`: "No native per-seat restrictive tool interface exists"; "No runtime prevention, effect/reading/recorder-completeness or universal tool/patch semantics"; "No historical manifest/report rewrite or retrospective authorization".
   - `sources_opened` lists only S085 and S086. S084 is not declared open for round 23, so reuse needs an explicit reopen/used-by record rather than silent citation.

## Check result

**Supported, narrowly.** The outside admit records that the task `tools` field is evaluated as additive extras and is not an allowlist or replacement, and that no host-native per-seat allowlist exists in the dispatch path. That is additive-only in the restrictive direction: listing tools cannot be read as narrowing native tool access, and the exposed `tools` parameter carries no restriction semantics. The closure reviewer agreed from the exposed task schema.

**Not supported by this evidence:**

- runtime prevention or enforcement of any per-seat tool policy (recorded absent; approved scope is prompt-level bindings plus post-hoc audit);
- availability, privilege, or effects of any listed extra tool — "additive extras" does not assert that every listed extra is admitted, nor that extras are effect-free;
- universal harness behavior: the basis is a documentary authority statement plus one schema-level spotcheck, not an executed fleet census;
- retrospective authorization or re-admission of S084's original content.

Confidence: high that the admit text supports additive/non-restrictive tool semantics; medium that the single schema-level observation generalizes to every dispatch path; runtime behavior unknown to this NO-EXEC seat.

## Draft: S084 reopen/used-by change note (not applied)

No ledger, manifest, or production file was changed by this seat; the note below is a draft for L1. It assumes the existing ledger may have mutable usage/state fields but treats identity and history as immutable.

Intent:

- Reopen S084 for round-23 citation without re-admission and without touching any immutable field.
- Record the narrow use: additive-only / non-restrictive `tools` semantics as an interface premise, never as enforcement evidence.

Immutable (preserve byte-for-byte, including key order and quoting):

- S084 identity and provenance exactly as recorded in its existing row: source id `S084`, its recorded path/locator, its declared digest, capture date/authority. The declared read set identifies `.ufo/waves/round-22/sources/host-tool-boundary.json` as the evidence the closure cites for S084; it is not asserted here to be the row's stored path or digest.
- Original admission: verdict/state admitted, verifier `CloseKaidoku22`, admission rationale, and the outside record named by preregister `outside_round22` (entry 422, commit `4482c275f9381f219ee4d092e0324d417c3cb1e7`, trends, path counts). The closure states its S084 sentence is recorded in "this MANIFEST entry only (no lane writes)"; preserve that string verbatim rather than reconstructing it.
- `r22-closure.json` in full, including `verification.spotcheck`, `verification.rechecks`, `notes`, `commit`, `closed_at`: historical evidence, do not edit.
- Every existing field and value of S084's row, including ones not enumerated here.

Append-only additions (proposed names; map onto the ledger's actual append-only fields, never rename existing fields):

- `reopened_in_round`: 23
- `reopened_by`: `SourceReopen84` (scout, report-only)
- `used_by` append: `round23:C2` (candidate consumer; L1/canonical planner to fix, or move to C1 if that is the actual consumer)
- `use_scope`: interface premise only — task tools are eval-defined additive extras, not an allowlist or replacement of native tools; no native per-seat allowlist; no enforcement claim
- `use_basis`: [`r22-closure.json#/verification/spotcheck`, `host-tool-boundary.json#/tools_semantics`, `#/native_per_seat_allowlist`, `#/authority`, `#/approved_scope`]
- `not_supported`: runtime prevention/enforcement; availability, privilege, or effects of any tool; universal dispatch behavior; retrospective authorization
- if the schema has a mutable state field: transition only that field to its local reopen value; identity fields stay untouched

Schema-neutral draft:

```json
{
  "_draft": true,
  "_not_applied": "report-only; L1 applies",
  "source_id": "S084",
  "op": "reopen_and_mark_used",
  "preserve_verbatim": "all existing fields and values, including id, recorded path/locator, declared digest, capture/authority, admission verdict and verifier, and the outside record's identity",
  "append": {
    "reopened_in_round": 23,
    "reopened_by": "SourceReopen84",
    "used_by": ["round23:C2"],
    "use_scope": "additive-only/non-restrictive task tools semantics; interface premise, no enforcement",
    "use_basis": [
      ".ufo/waves/round-23/sources/r22-closure.json#/verification/spotcheck",
      ".ufo/waves/round-22/sources/host-tool-boundary.json#/tools_semantics"
    ],
    "not_supported": [
      "runtime prevention or enforcement",
      "tool availability, privilege, or effects",
      "universal harness behavior",
      "retrospective authorization"
    ]
  },
  "forbidden": [
    "editing r22-closure.json",
    "recomputing or replacing S084's declared digest",
    "changing admission verdict, verifier, trends, or path counts",
    "renaming or reordering existing fields",
    "round24"
  ]
}
```

Apply rules:

- If `used_by` already exists, append one unique `round23:C2` entry; do not replace, re-sort, or rewrite existing entries.
- If the ledger has no `used_by` field, record the usage in the round-23 append-only manifest and leave S084's row untouched.
- If the local state vocabulary differs, use its reopen value; never rewrite the admission record.
- Do not copy the boundary JSON's assertion as a runtime guarantee; the use note must keep the `not_supported` bounds.

## Residual unknowns

- S084's actual row body, schema, and exact immutable key names are not in this seat's declared read set; only the closure's S084 admission sentence and the boundary JSON are. The draft preserves by reference rather than guessing values.
- The final consumer is not fixed by the preregister; C2 is proposed because its scope explicitly bounds v2 authority to "no native enforcement/effects claim", but L1 may anchor the use to C1's source contract.
- Runtime dispatch behavior was not observed (NO-EXEC); this report makes no native-enforcement claim.

## No-harm

- Wrote only this report at the declared path; no commands, no hashing, no production/VCS/ref/route changes, no installs.

Reviewed-SHA256: e13cde76422140a13284f730950f2bf36d308d55e30ce956bc59ff5af7d9e68c
Predicate: r23-sourcereopen84
Scope: executed=none
