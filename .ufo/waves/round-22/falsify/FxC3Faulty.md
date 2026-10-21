# FxC3Faulty — wrong scope/predicate/digest classification and accounting separation

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3faulty
Scope: executed=none

Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py` (164 lines), declared digest 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0. That digest is accepted as assigned, **not recomputed**: NO-EXEC forbids hash commands and no declared file records this tool's digest. Semantics dependency read in the same candidate tree: `check-review-snapshots.py` (`strict.evaluate`, `physical_lines`, `has_controls`).

Method: static source/byte derivation only. No execution, import, test, mutation, example, subprocess or network. The wave's `build/reviews.json` and `build/settlement.json` are not in this seat's declared read paths, so the actual cohort verdict for the landed revision is **not observed** here; only fixture expectations and code-derived behavior are reported, kept separate below.

## Claim attacked

A wrong receipt scope, predicate or digest must classify the seat `delivered_faulty`, keep the strict evaluator red, and keep the overall accounting verdict separate from the strict verdict.

## Why the triple holds inside the declared scope

- Strict receipt identity (`check-review-snapshots.py` lines 107–118): after UTF-8 decode and LF-only `physical_lines` (42–44), the report must contain exactly one line equal to `Reviewed-SHA256: <manifest sha256>`, exactly one equal to `Predicate: <manifest predicate>`, and exactly one equal to the literal scope line. A wrong, missing, duplicated or reordered declaration yields `REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH` or `REVIEW-SCOPE-MISMATCH`, and the strict code becomes 1 (findings); an undecodable or unreadable report makes it 2.
- Source identity (lines 90–91): the bytes read from the manifest's `source` path must hash to the same declared digest; otherwise `REVIEW-SNAPSHOT-MISMATCH` (strict 1).
- Cohort classification (`check-review-cohort.py` 57–61): the per-seat one-review strict code is the only classification input; `delivered_conformant` iff that code is 0, else `delivered_faulty`. The row keeps `strict_exit` and `strict_findings` (63–65).
- Accounting (`check-review-cohort.py` 66–73): exit = 2 if the aggregate strict code is 2, else 1 iff there is an `absent_unresolved` finding, else 0; the strict code, all strict findings and the strict conformance label are retained as payload fields while the exit code remains the accounting verdict.

Invariant closing both directions: every strict finding other than `REVIEW-MANIFEST-SCHEMA` is emitted inside the per-row loop (91–120), and the only non-row finding is converted to `COHORT-SCHEMA` at cohort lines 33–35. Therefore the aggregate strict code is 0 iff every per-seat strict code is 0. A strictly red delivered report cannot be counted `delivered_conformant`, and an all-conformant cohort cannot carry a red aggregate. The one exemption is exact CRLF tolerance (one trailing CR removed per line, 42–44), which does not accept any changed value.

Consequence for the named triple: a wrong scope, predicate or receipt digest yields a red per-seat code, category `delivered_faulty`, aggregate strict FAIL, and accounting exit 0. The exit 0 is the fixture-encoded "accounting separate" behavior, not a strict pass: `strict_conformance` is FAIL and the findings are preserved.

## Expected fixture verdict vs static derivation

No execution: the "static" column is derived by reading the code paths above. The fixture's own expectations are quoted from `check-review-cohort.py` 93–110.

| Case | Expected fixture verdict | Static derivation |
|---|---|---|
| clean | exit 0, conformant 1, strict 0 | same |
| dead-missing | exit 0, absent_dead 1, strict 1 | same (report missing, outcome failed) |
| partial-failed | exit 0, faulty 1, strict 1 | same (three receipt findings) |
| missing-unresolved | exit 1, unresolved 1, COHORT-UNRESOLVED, strict 1 | same |
| period (wrong scope) | exit 0, faulty 1, strict 1 | scope mismatch → same |
| predicate (wrong predicate) | exit 0, faulty 1, strict 1 | predicate mismatch → same |
| digest (wrong receipt digest) | exit 0, faulty 1, strict 1 | snapshot mismatch → same |
| duplicate-receipt | exit 0, faulty 1, strict 1 | two digest lines → mismatch → same |
| crlf | exit 0, conformant 1, strict 0 | one CR removed per line → same |
| unicode | exit 0, faulty 1, strict 1 | U+2028 stays inside the final physical line (split is LF-only) → scope mismatch → same |
| encoding | exit 2, faulty 1, COHORT-STRICT-UNAVAILABLE, strict 2 | decode failure → same |
| dropped / duplicate / unknown / false-death | exit 2, COHORT-SCHEMA | set mismatch / duplicate name / unknown name / empty error string → same |
| manifest-missing | exit 1, COHORT-MANIFEST-MISSING | early return at 23–24 → same |
| duplicate-manifest | exit 2, COHORT-SCHEMA | strict schema finding → raise at 33–35 → same |
| duplicate-json-key | exit 2, COHORT-SCHEMA | `unique_object` raises → same |

All 18 expectations are consistent with the code by static derivation. Observed runtime: **none** (no execution permitted).

## Counterexamples and bounds

1. **Manifest-as-reference (concrete, outside the declared reading of "wrong").** Build `reviews:[{name:"A", source:"s", report:"r", sha256:H(s), predicate:"not-the-assigned-predicate"}]`, a report whose three lines cite `H(s)` and that same predicate, and a completed settlement. Static result: strict 0, `delivered_conformant`, exit 0, strict PASS. Nothing in either tool holds an expected predicate or an expected digest: the manifest's own declarations are the reference (strict docstring: "declared review byte/predicate identity"). A predicate or source/digest pair that is wrong relative to the seat's assignment but internally self-consistent is classified conformant. This is intentional for the declared scope ("primary snapshot and predicate declarations only") but is the counterexample for any unqualified "wrong predicate/digest" reading.

2. **`delivered_faulty` is not receipt-faulty.** Category is `one_code != 0` (61), so it also covers a source pin that does not hash to the declared digest while the receipt is perfectly formed (strict 90–91), and an undecodable report whose strict verdict is CANNOT_EVALUATE rather than FAIL (fixture `encoding`). Expected fixture verdict for `encoding` is `delivered_faulty` with strict exit 2, so the conflation is fixture-encoded, not accidental. No false green results because an aggregate strict code 2 forces exit 2 (68–70); the per-row finding ids remain the discriminating evidence.

3. **The failed-error gate accepts an invisible, non-whitespace error (concrete fail-open).** Cohort line 44 requires `row['error'].strip()` to be non-empty for `outcome == "failed"`. `str.strip()` removes Unicode whitespace but not format characters: an error string of U+200B (Cf) or any zero-width/format character survives. Strict's own `has_controls` rejects Cc/Cf/Cs/Zl/Zp for predicates and paths (strict 21–23, 76–78), but is never applied to settlement errors. Static result for `{outcome:"failed", error:"\u200b"}` with a missing report: accepted, bucketed `absent_dead` (59), no finding (66–69), exit 0. The fixture's negative `false-death` case only uses the empty string (104–106) and does not cover this. This is outside the scope/predicate/digest triple but is a source-visible counterexample to "failure without observed error" being rejected.

4. **Unknown outcome with a delivered report passes with no finding.** With `outcome:"unknown"`, `error:""` and a conformant present report: `delivered_conformant` (61), no finding, exit 0. Only the row's `outcome` field records the unknown settlement; the top-level status does not. This does not contradict the four-bucket definition (the seat did deliver), but it is a visibility gap for evidence-only accounting. The fail-closed direction is preserved: unknown plus absent report becomes `absent_unresolved` and exit 1.

5. **Cross-seat substitution is undetectable within receipt scope.** Receipts carry no seat identity (only digest, predicate, literal scope line, 113–118). Only duplicate names and duplicate report paths are rejected; two reviews may pin the same source and predicate. Their required receipts are byte-identical, so a report copied from one seat to the other is conformant for both. Outside the declared scope ("not request-scope conformity"), but it bounds receipt conformance as non-identity conformance.

6. **One unreadable report aborts accounting and drops strict findings.** Cohort line 55 reads the report outside a per-seat try; a read error propagates to the outer handler (78) and returns `COHORT-READ` with no seats or counts, although the aggregate strict pass had already recorded `REVIEW-READ-FAILED` for that row. Absent paths return None (not an error) and still account normally, so this needs an actual read failure. The result is fail-closed (exit 2), but "account for every declared seat" and "preserve strict receipt findings" are not satisfied on that path.

## Verdict

For the declared-scope reading, no source-visible counterexample exists to the triple: wrong receipt scope, predicate or digest each force a red per-seat strict verdict, `delivered_faulty`, and a preserved aggregate strict FAIL, while the accounting exit stays separate (0 for a fully accounted cohort). The expected fixture verdicts are statically consistent with the code; observed runtime is none. Unqualified readings are bounded by counterexamples 1 and 3: the manifest is the only reference for predicate/digest correctness, and the failed-error gate accepts format-only error strings.

Remaining unknowns: the actual wave manifest/settlement contents and the landed cohort verdict (outside this seat's read paths); independent recomputation of the target digest (NO-EXEC).

Report: .ufo/waves/round-22/falsify/FxC3Faulty.md
