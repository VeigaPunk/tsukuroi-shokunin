# FxC3MissingSettlement: source-only falsification of check-review-cohort.py

Target: `candidate/tools/check-review-cohort.py`. Assigned pin `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0`.
Method: source reading of declared paths only. NO-EXEC and NO-FETCH: nothing run, imported, tested, mutated or fetched; no subagents.
Pin: taken as assigned and not recomputed. The read tool's `#ADD3` tag is a hashline, not SHA-256.
Read: target; `check-review-snapshots.py`; `_revision.py`; `preregister.json`; `sources/host-tool-boundary.json`; `seat-boundary-r22.json` and `.md`; `skill://godspeed`.
Not declared, not read: `build/reviews.json`, `build/settlement.json`, `build/bindings.json`, `build/events.json`, `check-seat-bindings.py`, `check-boundary-contract.py`.

## 1. Verdict

Attack: an omitted declared seat must not shrink the denominator; bijection must be exact.

| Variant | Verdict |
|---|---|
| Settlement omits, renames, duplicates, or adds a seat | Holds, bounded (section 2). No denominator is emitted. The same path still emits `cohort_accounting_mode: 1` (F1). |
| Seat missing from the committed manifest (the population itself) | Succeeds for C3 standing alone (F2). |
| Older landed revision used as the population | Succeeds unless the operator chooses REV correctly (F3). |

## 2. Why the settlement-side bijection holds

- `by_name` keys are unique (line 42) and drawn only from manifest names (line 42, membership).
- Manifest names are a subset of keys: `set(by_name) != names` raises at lines 50-51.
- Settlement agents are unique (line 42), so seat-to-agent is injective over settlement rows.
- Manifest names are unique only because `strict.evaluate` rejects duplicate `name` and `report` values (check-review-snapshots.py 72-73, reached through lines 33-35). The cohort does not assert this itself (F9).
- Each review goes through the loop at lines 52-65 exactly once, adding one category (61-62) and one row (63). So `len(rows) == total == len(reviews)` and `accounted == total` on every path that reaches line 71.
- The loop has no `continue`. An exception inside it replaces the whole result (75-78), so no partial counts are emitted.

## 3. Fixture verdict, kept separate from runtime

Expected [INFERENCE: derived by tracing, not observed]: `--selftest` prints one JSON line with `status` PASS, `cases` 18, `failed` 0, and exits 0.

Expected exit per case, traced against the code:
- 0: clean, dead-missing, partial-failed, period, predicate, digest, duplicate-receipt, crlf, unicode
- 1: missing-unresolved, manifest-missing
- 2: encoding, dropped, duplicate, unknown, false-death, duplicate-manifest, duplicate-json-key

Observed runtime: none (NO-EXEC).

Blind spots, so a PASS does not clear F1-F8: the observation tuple (line 118) never reads `cohort_accounting_mode`, `total` or `accounted`. No fixture has two valid seats, so partial omission is never exercised. `dropped` removes all seats. There is no per-seat read-fault case. A population cross-check is not expressible in this checker.

## 4. Findings, by severity

### F1 - High: failure results carry `cohort_accounting_mode: 1`
- Line 24 emits `0` for a missing manifest (nothing accounted). Lines 71, 76 and 78 emit `1` for success, COHORT-SCHEMA and COHORT-READ. Line 79 sets status CANNOT_EVALUATE for code 2. The strict-unavailable path (68-70) also reaches line 71 with `1`. Revision-level failures (156, 158) omit the key entirely.
- Counterexample: manifest lists {A,B}, settlement lists {A}. Line 51 raises, line 76 returns exit 2 with status CANNOT_EVALUATE, `cohort_accounting_mode: 1`, and finding COHORT-SCHEMA.
- preregister.json line 7 defines C3's metric as this key, with `before: 0` and `target: 1`. A scorecard keyed on the metric would record C3 as achieved for a cohort with zero accounted seats.
- The selftest does not catch it, because line 118 never reads the key.
- Severity depends on how the metric is read, and that reader is outside declared paths [INFERENCE].
- Direction: emit the mode only on accounted results, or assert `cohort_accounting_mode == 0` on exit-2 fixtures. Not applied.

### F2 - High against the checklist's denominator guarantee; Medium against C3's literal bound: population is self-declared
- The only population is `reviews = data['reviews']` (line 36), with `total = len(reviews)` (line 71).
- `main` accepts only `--manifest`, `--settlement` and `--branch` (139-141), and reads both files from the bound commit (152-153). There is no expected count, no bindings or events read, and no comparison with the preregistered seat list. preregister.json line 7 passes only the two build files.
- Counterexample: declared seats {A,B,C}. The committed manifest and settlement both list {A,B}, and both are conformant. Output: total 2, accounted 2, mode 1, status PASS, exit 0 (lines 70, 79). Seat C disappears with no finding.
- Mitigation outside C3: seat-boundary-r22.md line 22 says the request auditor "fails closed on ... unmatched seats". That is C2 (`check-seat-bindings.py`, not read). C3 does not reference it.
- Checklist item 1 (seat-boundary-r22.md line 28) requires the declared population to be frozen before dispatch. Nothing in this file checks the freeze or chronology. Checklist item 4 (line 31) forbids dropping a denominator, and this checker cannot enforce that alone.
- C3_bound (preregister line 9) says "every declared seat". This checker satisfies that only if "declared" means manifest-declared.

### F3 - Medium: revision choice is unbounded
- `bind` (_revision.py 184-191) accepts any commit that is an ancestor of `refs/heads/<branch>`, and of `origin/<branch>` when present. There is no tip, latest, or frozen-population check. `--branch` (139) changes the reference branch.
- `<REV>` is operator-supplied (preregister line 7). Counterexample: an older landed commit whose reviews.json lists {A,B} gives PASS with total 2, while a later landed commit lists {A,B,C}. Output includes `revision` (line 154), so an audit is possible, but the checker does not enforce one.

### F4 - Medium (design-consistent; trust gap): `absent_dead` is self-attested
- An absent report plus settlement `outcome == 'failed'` gives `absent_dead` (line 59). The only check on the failure is non-blank error text (44-45). `absent_dead` adds no finding (66-70), so exit is 0.
- Fixture `dead-missing` (line 95) encodes exit 0 as expected, so this is intentional. The checker still grants a non-failure class to a missing receipt on a text field it cannot verify. There is no dispatch-event or chronology check.
- Asymmetry: `outcome` is consulted only when the report is absent (58-61). A `failed` or `unknown` row with a conformant report counts as delivered_conformant with no finding. The row keeps `outcome` (63), but the counts do not.

### F5 - Medium: top-level status is PASS over faulty receipts
- With strict_code 1 and no absent_unresolved: code 0 (line 70), `strict_conformance` FAIL (line 73), status PASS (line 79).
- The module docstring (line 2) says strict receipt faults must not be converted to passes. Per-row categories and `strict_conformance` do keep the fault, and C3_bound frames C3 as accounting, not conformance; the SCOPE string (line 19) says the same. The risk is a consumer reading `status` alone.

### F6 - Low: second-pass read fault is absorbed
- `one_code` (line 57) only chooses `delivered_faulty` (line 61). The top-level code (line 70) reads `strict_code` only. The per-review strict re-read catches OSError, RuntimeError and TimeoutExpired, and returns 2 (strict 84-97, 121).
- A transient fault in that re-read yields `strict_exit: 2` and delivered_faulty while the full pass succeeded, so exit can be 0. The full pass escalates the same condition to exit 2 (68-69). The result depends on which pass hit the transient fault.

### F7 - Low: fixture gaps (see section 3)

### F8 - Low: content and type gaps
- `git_read` (cohort 124-131, strict 131-142) returns stdout for any object type. A committed symlink would yield its link-target text as content, and there is no regular-blob mode check. This requires commit authority, and Main is the integrator, so it is hardening [INFERENCE on `git show` symlink behavior].
- Strict uniqueness is by path (check-review-snapshots.py 73). Two seats with byte-identical reports, the same source and the same predicate both count delivered_conformant. `report_sha256` (line 65) supports external comparison only. Detection is C2's job. The SCOPE string (line 19) bounds delivered to receipt well-formedness.
- `RecursionError` is a `RuntimeError`, so pathological JSON nesting reports COHORT-READ (77-78), not COHORT-SCHEMA. It is still exit 2.

### F9 - Residual: bijection depends on strict's duplicate check
- The cohort has no `len(names) == len(reviews)` assertion. Strict's check at 72-73 supplies that guarantee. Without it, duplicate names would count one settlement row twice. Holds today; fragile. Not applied.

## 5. Residual risk and verification gaps
- Pin not recomputed; the assigned digest is taken as given.
- Not read: build/*.json, `check-seat-bindings.py`, `check-boundary-contract.py`. F2's C2 mitigation and F4's settlement provenance remain unverified.
- The cohort loads strict and `_revision` from the working tree (lines 13, 15-18), not from REV. Verdicts depend on working-tree checker code. This is a reproducibility note, not a denominator defect.
- The scorecard reader is outside declared paths, so F1's severity is [INFERENCE].
- The fixture verdict is derived by tracing, not observed.

## Receipt

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3missingsettlement
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
