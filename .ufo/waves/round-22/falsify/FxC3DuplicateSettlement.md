# FxC3DuplicateSettlement — duplicate and unknown settlement identity rejection

**Target bytes**: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`
**Declared digest**: `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0` (seat-supplied pin; not recomputed, since hashing requires execution and this seat is NO-EXEC)
**Co-reads**: `.ufo/waves/round-22/candidate/tools/check-review-snapshots.py` (strict evaluator and manifest schema), `.ufo/waves/round-22/preregister.json` (C3 bound), `.ufo/waves/round-22/sources/host-tool-boundary.json`, `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.json`, `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`
**Method**: static reading and literal grep of bound local paths only. No import, test, mutation, subprocess, compile, or network. No target-file instruction was followed.

## Attack

The candidate must reject a settlement seat that (a) reuses an already-settled name, (b) reuses an already-settled agent, or (c) names a review absent from the manifest, and must not turn any of those into a passing or partially credited cohort.

## Result

No source-visible counterexample. All three identity faults are rejected by one validation condition before any seat row or count exists, and every rejection lands in the fail-closed code-2 `COHORT-SCHEMA` path rather than in a category count.

## Source trace

1. Both inputs are parsed with the strict duplicate-key hook (lines 30-31: `json.loads(..., object_pairs_hook=strict.unique_object)`). `unique_object` (check-review-snapshots.py:36-41) raises on a repeated JSON key, so a settlement seat that repeats `name` or `agent` inside one object raises before identity validation and maps to code 2.
2. Manifest names are already unique and ASCII-constrained. The strict evaluator requires `name` to match `[A-Za-z0-9][A-Za-z0-9._-]{0,127}` and rejects a repeated name or report path (check-review-snapshots.py:70-79); that `ValueError` becomes `REVIEW-MANIFEST-SCHEMA` (122-124). Cohort re-raises whenever that finding is present (lines 33-35), so `names` (line 37) is a set of unique, regex-valid strings. A JSON spelling difference such as `"\u0041"` versus `A` parses to the same `str` and cannot manufacture two manifest identities.
3. Settlement admission is a single disjunction (lines 40-43):
   - `row.get('name') not in names` rejects every name absent from the manifest; a missing `name` yields `None` and also rejects here, so `row['name']` is never reached with an absent key;
   - `row['name'] in by_name` rejects the second registration of an already-settled name;
   - `not isinstance(row.get('agent'), str) or not row['agent'] or row['agent'] in agents` rejects a non-string, empty, or already-registered agent.
   An unhashable name (JSON array or object) raises `TypeError` from the membership test instead of being admitted.
4. Registration (`by_name[row['name']] = row`, `agents.add(row['agent'])`) happens only after the entire condition and the outcome/error consistency checks (44-47) pass. A duplicate row aborts at 42-43 before either registry changes (48-49).
5. Completeness (`set(by_name) != names`, 50-51) rejects a settlement that drops a manifest seat, after unknown-name rejection has excluded extras. Seat names are therefore exactly the manifest cohort, with no extra and no repeated identity.
6. The accounting loop that increments `counts` and emits per-seat rows (52-65) sits below all of that validation. A rejected settlement cannot produce `delivered_conformant`, `delivered_faulty`, `absent_dead`, or `absent_unresolved` counts.
7. Each raise in steps 3-5 is a `ValueError` caught at lines 75-76: exit 2, status `CANNOT_EVALUATE`, finding `COHORT-SCHEMA`, `cohort_accounting_mode: 1`, and no `seats`, `total`, or category keys.

## Counterexample attempts, source-only

| Attempt | Disposition | Anchor |
|---|---|---|
| Settle name `A` twice under different agents | second row trips `row['name'] in by_name` | 42-43 |
| Settle agent `X` under two different names `A`, `B` | second row trips `row['agent'] in agents` | 42, 49 |
| Settle name `B` absent from manifest | first disjunct `not in names` | 42 |
| Unknown name spelled with JSON escapes or lookalike code points | parses to a distinct `str`, never in the ASCII manifest set | 37, 42 |
| Unknown name as `true`, `1`, `1.0`, or NaN | no equality with a manifest string | 42 |
| Unknown name as JSON array or object | `TypeError` from set membership, caught as code 2 | 42, 75-76 |
| Duplicate `name` key inside one seat object | `strict.unique_object` raises before validation | 30-31 |
| Settlement drops a manifest seat | completeness equality fails | 50-51 |
| Manifest repeats a review name | strict `REVIEW-MANIFEST-SCHEMA`, cohort re-raise | 33-35; strict 70-79, 122-124 |
| Agent duplicated only by formatting: `agent-X` versus `agent-X` + U+200B (Cf) | both are non-empty unequal `str`; both admitted | 42, 48-49; see G1 |

## Fixtures: expected verdict versus observed runtime

Observed runtime is **not executed** for every fixture: this seat is NO-EXEC, so no fixture was run and no output is reported as observed. Expected verdicts below are static predictions from the cited anchors, not measurements. The tool's own selftest declares some of these expectations in source (104-109); those declarations are also not executed results.

| Fixture | Setup | Expected verdict (static) | Support |
|---|---|---|---|
| F1 duplicate name | manifest `{A}`; seats `A/agent-A/completed/""`, `A/agent-B/completed/""` | exit 2, `CANNOT_EVALUATE`, `COHORT-SCHEMA`, mode 1, no seat rows | 42-43, 48, 75-76; declared at 104-106 |
| F2 duplicate agent | manifest `{A,B}`; seats `A/agent-X`, `B/agent-X` | exit 2, `CANNOT_EVALUATE`, `COHORT-SCHEMA`, no seat rows | 42 (agent disjunct), 49 |
| F3 unknown name | manifest `{A}`; seats `A/agent-A`, `B/agent-B` | exit 2, `CANNOT_EVALUATE`, `COHORT-SCHEMA`, no seat rows | 42; declared at 104-106 |
| F4 dropped seat | manifest `{A,B}`; seat `A` only | exit 2, `CANNOT_EVALUATE`, `COHORT-SCHEMA`, no seat rows | 50-51; declared at 104-106 |
| F5 clean control | manifest `{A}`; seat `A/agent-A`; conformant receipt | exit 0, `PASS`, `delivered_conformant` 1 | 52-65; declared at 93 |
| F6 formatted-agent lookalike | manifest `{A,B}`; seats `A/agent-X`, `B/agent-X` + U+200B | exit 0, `PASS`, both `delivered_conformant` if both receipts conform | 42, 48-49; see G1 |

Fixture-attribution note: the `duplicate`, `unknown`, and `dropped` selftest cases (104-106) assert the same exit 2 and the same `COHORT-SCHEMA` id. A passing selftest would therefore not distinguish which disjunct fired; branch attribution here rests on reading lines 40-43 and 50-51, not on the fixture's finding id.

## Bounds and residual unknowns

- **G1 — exact identity only (bounded counterexample to a broad reading).** Duplicate and unknown checks compare exact code-point strings. The seat's `agent` value is not screened for control or format characters, although strict applies `has_controls` (Cc/Cf/Cs/Zl/Zp) to manifest paths and predicates (check-review-snapshots.py:21-30, 77). Two agent labels that render identically but differ by Unicode normalization or an injected format character are admitted as distinct identities. Under byte-exact semantics the predicate holds; under a human-identity or confusable-label reading, F6 is an acceptance rather than a rejection. No manifest field exists for an agent, so this is not an unknown-agent check, only a duplicate check.
- **G2 — untested branch.** Duplicate-agent rejection has no selftest coverage: the selftest manifest declares one name, and its `duplicate` case trips the name disjunct first. Support for F2 is static reading of line 42 only.
- **G3 — denominator loss on bad settlement.** A settlement with a duplicate, unknown, or dropped seat is rejected wholesale as `CANNOT_EVALUATE` with no `seats`, `total`, or counts. This is fail-closed, but it abandons the declared denominator instead of accounting the offending seat as faulty or unresolved. Cohort accounting therefore applies only to settlements that already pass identity validation; it is not a residual ledger for malformed settlement input.
- **G4 — metric degeneracy.** `cohort_accounting_mode: 1` is emitted both on the success result (line 71) and on the schema-failure handler (line 76). Preregister C3's target value 1 therefore cannot by itself distinguish an accounted cohort from a rejected settlement; `status` and `findings` carry that distinction, not the metric.
- **G5 — [INFERENCE, outside attack scope].** `RecursionError` from deeply nested settlement JSON is not in the handler tuple at line 75, and `main` (151-158) catches only revision, OS, runtime, and subprocess errors. That would escape as a nonzero interpreter failure rather than a code-2 `COHORT-SCHEMA` result: fail-closed, but un-attributed. Not observed, not tested.

## Answer

The duplicate-name, duplicate-agent, and unknown-name rejection predicate holds on the named bytes. Every source-visible variant of those three faults is rejected before accounting, with code 2 and `COHORT-SCHEMA`. The one source-visible way past the letter of the predicate is definitional: agent identity is exact-string, so formatting-variant duplicates are not duplicates to this code (F6, G1). No runtime behavior is claimed; nothing was executed.

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3duplicatesettlement
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
