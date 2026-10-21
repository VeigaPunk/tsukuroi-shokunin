# FxC1Duplicate — duplicate decision ID / duplicate JSON members

Target: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py`
Assigned SHA256: `1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485` (as bound by the seat; not recomputed — NO-EXEC).
Attack: six rows retained while a decision `id` is duplicated, and JSON objects with duplicate members, must be rejected as schema.
Mode: source-only reading of the declared paths; no execution, import, mutation, test, or fetch.

## Axes

1. Acceptance impossibility — can any duplicate-ID fixture reach exit 0 / six validated decisions?
2. Duplicate-member coverage — is every JSON object parsed through the duplicate-key hook?
3. Classification fidelity — does rejection land on exit 2 / `BOUNDARY-SCHEMA`, or on a weaker finding?
4. Masking — can an earlier or later check suppress the schema finding?

## Verdict

Holds for the assigned fixtures. A six-row duplicate **string** decision id and a duplicate **JSON member** (top level or nested in a decision row) both raise inside `evaluate`'s single try block and map to exit 2, status `CANNOT_EVALUATE`, finding `BOUNDARY-SCHEMA`. No duplicate-ID fixture can reach exit 0. One source-visible edge deviates from the exact class: duplicate non-string ids that exploit `NaN != NaN` are still rejected, but at exit 1 / `BOUNDARY-DECISION-MISMATCH` rather than exit 2 / `BOUNDARY-SCHEMA`.

## Evidence chain (all line numbers in the target file)

- `unique` (lines 29–35) walks `object_pairs_hook` pairs and raises `ValueError('duplicate JSON key')` on a repeated key **before** a dict exists, so the last-writer-wins behaviour of plain `json.loads` is not reachable.
- The decision document is parsed with that hook at line 66; the host document at line 74. These are the only two parse sites in the file (no `json.load`, no `object_hook`, no `parse_constant`, no `strict=`), so every object in both documents is covered.
- Line 70–71: `len(rows) != 6 or len({r['id'] for r in rows}) != 6` raises `ValueError('exact six unique decisions required')`. Six retained rows with one repeated id give set cardinality 5, so the right-hand disjunct fires.
- Lines 96–98: the `except (ValueError, TypeError, KeyError, UnicodeError, AttributeError)` appends exactly `{'id': 'BOUNDARY-SCHEMA', 'site': 'corpus/knowledge/seat-boundary-r22.json'}` and sets `code = 2`.
- Lines 99–100: `code == 2` renders `status = 'CANNOT_EVALUATE'`; `validated_boundary_decisions` is the untouched `count = 0`.
- Ordering: the parse and uniqueness checks (66–71) precede host validation (74), source/prose parsing (72–77), and `by_id` construction (89), so no earlier finding can mask a duplicate and no later check can overwrite the schema classification.
- The self-test encodes the same expectation: `duplicate-id` and `duplicate-key` are both declared `(2, 'BOUNDARY-SCHEMA')` at lines 121–122, and the pass predicate at line 134 requires exact exit-code equality plus finding membership.
- For the combined fixture (duplicate member *and* duplicate id), the parse at line 66 raises first, so the outcome is the same exit 2 / `BOUNDARY-SCHEMA`; the two inputs are indistinguishable in the payload.

## Bounded reason acceptance is impossible

`count` increments only when `by_id.get(ident)` is present and its `(id, surface, decision, reason, source)` tuple equals `EXPECTED` (lines 89–95); exit 0 requires `count == 6`.

1. Six retained rows with an exactly duplicated string id yield five distinct set keys → line 70 raises → never reaches the loop.
2. Even without line 70, a six-row duplicate drops at least one `EXPECTED` id from `by_id`, so at least one `BOUNDARY-DECISION-MISMATCH` is appended and `code = 1`. Duplicate ids therefore have no PASS path; the uniqueness check only upgrades the rejection class from FAIL(1) to CANNOT_EVALUATE(2).
3. A duplicate member in any object raises at parse time; an input that is not parseable JSON also raises `JSONDecodeError`, itself a `ValueError`, so malformed syntax lands on the same finding.
4. A row without `id` (`KeyError`), an unhashable `id` (`TypeError`), or non-dict rows (`TypeError`) all fall into the same handler — fail closed rather than skip the check.

## Source-visible edge: `NaN` ids defeat set cardinality, not acceptance

`json.loads` accepts the non-standard constants `NaN`, `Infinity`, and `-Infinity` by default and the file installs no `parse_constant`. Two rows with `"id": NaN` become two distinct float objects; `float('nan') != float('nan')` and distinct NaNs hash alike but stay separate set members, so line 70 computes cardinality 6 and does not fire. `by_id` likewise holds both NaN keys, both `EXPECTED` string ids they replaced are absent, and the loop appends two `BOUNDARY-DECISION-MISMATCH` findings → exit 1. The fixture is rejected, but **not** as schema.

This is a classification counterexample to the strict "reject schema" phrasing, not to rejection itself, and it cannot produce PASS because the missing `EXPECTED` ids force mismatches. Confidence: `[INFERENCE]` from CPython JSON/float/set semantics; no execution was permitted, so this path is unobserved.

Related equality-based artifact, harmless to acceptance: ids `1` and `true` (or `2` and `2.0`) collapse to one set member and would be rejected as schema even though JSON encodes six distinct tokens. That is a false rejection, not a bypass.

## Expected fixture verdict vs observed runtime

Expected, read from source:

| Fixture | Exit | Status | Findings | validated_boundary_decisions |
|---|---|---|---|---|
| duplicate-id, six rows, duplicate string id | 2 | CANNOT_EVALUATE | `[BOUNDARY-SCHEMA @ corpus/knowledge/seat-boundary-r22.json]` | 0 |
| duplicate JSON member (top level or in a row) | 2 | CANNOT_EVALUATE | same single finding | 0 |
| both combined | 2 | CANNOT_EVALUATE | same single finding (member check wins) | 0 |
| duplicate `NaN` ids | 1 | FAIL | `BOUNDARY-DECISION-MISMATCH` for each missing expected id | ≤ 4 |

Observed runtime: none. `executed=none`; the tool was not invoked, so no exit code, payload, or self-test observation exists to compare. Statements above are static derivations from the cited lines.

## Adjacent observations (not part of the assigned predicate)

- On schema rejection the payload still reports the literal `'total_decisions': 6` (line 100) while `validated_boundary_decisions` is 0. The preregistered C1 metric is `validated_boundary_decisions`, so the malformed fixture cannot inflate the count; a consumer reading `total_decisions` alone would overread.
- A `RecursionError` from pathologically deep JSON is a `RuntimeError` and is not in the schema handler's tuple (line 96); in `main` it would be caught by the `RuntimeError` branch and reported as `BOUNDARY-READ` at site `revision` (line 169), still exit 2 but with a different finding id. Duplicate members nested past the recursion limit would take this route rather than `BOUNDARY-SCHEMA`.

## Residual unknowns

- The assigned SHA256 was not recomputed (no command execution allowed); byte identity rests on the seat binding.
- No runtime observation exists for any fixture, including the `NaN` edge and the deep-nesting route; both remain inference from documented interpreter semantics.
- The committed `corpus/SOURCES.md` rows were not in the declared read set, so the S083/S084 source-row branch was not re-derived; it is independent of the duplicate predicate.

## Receipt

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1duplicate
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
