# DebtSixReceipts — six named receipt faults and their preserving checks

Seat: TsukuroiR22.DebtSixReceipts-3. Round-22 C3 (calibration) is bounded strict-receipt cohort accounting: classify every declared seat as delivered-conformant, delivered-faulty, absent-dead, or absent-unresolved, "preserving strict receipt findings" (round-22 `preregister.json`, claim C3, `C3_bound`). Command: `python3 tools/check-review-cohort.py --revision <REV> --manifest .ufo/waves/round-22/build/reviews.json --settlement .ufo/waves/round-22/build/settlement.json`. This report enumerates the six named receipt faults left standing by round 21 and the exact check that preserves each finding.

## Source of the six

Round-21 lessons (`corpus/lessons/round-21.md`, Final Gate decisions and measured outcome): "Six strict receipt mismatches persist; original reports/manifests are not rewritten or weakened. … C3 strict faults: build scope-line mismatches Oracle05TagTree, Oracle06TagBlob, Oracle08NestedTag; falsify scope-line mismatches Fx05TagTree, Fx06TagBlob and predicate mismatch FxC3Report. These are exact-line conformance findings, not source-hash mismatch or proof of forgery." Cohort denominator context: build 60/64, falsify 51/64; 111 fully conforming of 117 retained reports.

## The six named faults and the exact check that preserves each

| # | Seat (wave) | Fault class | Exact preserving check |
|---|---|---|---|
| 1 | Oracle05TagTree (build) | Scope-line mismatch: receipt line 3 is not exact `Scope: executed=none` | Scope-line exact conformance check: split the report into physical lines (LF only), strict UTF-8 per-row decode, and require the third physical line to byte-equal `Scope: executed=none` — no period-appended variant (`executed=none.`), no Unicode/pseudo-line surrogate (R21-TRAILER20 gate; R21-REPORT-ENCODING physical-LF/per-row/UTF-8 fixtures). Round-22 cohort accounting must classify this seat delivered-faulty and keep the round-21 strict finding red |
| 2 | Oracle06TagBlob (build) | Scope-line mismatch (same class) | Same scope-line exact conformance check as #1 |
| 3 | Oracle08NestedTag (build) | Scope-line mismatch (same class) | Same scope-line exact conformance check as #1 |
| 4 | Fx05TagTree (falsify) | Scope-line mismatch (same class) | Same scope-line exact conformance check as #1, applied to the falsify-wave retained report |
| 5 | Fx06TagBlob (falsify) | Scope-line mismatch (same class) | Same scope-line exact conformance check as #1, applied to the falsify-wave retained report |
| 6 | FxC3Report (falsify) | Predicate mismatch: receipt line 2 does not match the report's declared predicate binding | Predicate-line exact conformance check: same physical-LF/strict-UTF-8 per-row read, requiring the second physical line to byte-equal `Predicate: <declared predicate>` for that report's preregistered predicate; Unicode splitlines and report-encoding gaps must not let a pseudo-line pass (R21-REPORT-ENCODING). Round-22 cohort accounting must classify this seat delivered-faulty |

Preserve means: the findings stay named, stay red, and keep their class (exact-line conformance, not source-hash mismatch, not proof of forgery). No rewrite of original reports/manifests, no placeholder, no substitute report, no revival of failed seats (R21-MISSING13; round-22 `limits`: original round-21 reports and manifests remain immutable, no replacement seats).

## Cross-cutting checks the cohort accounting must keep separate

- Missing-report control stays red: 1 build and 10 falsify declared seats have no report (absent-dead/absent-unresolved); Fx09Nested's retained partial report is not a completion. A missing or dead seat never implies `executed=none`.
- Receipt conformance checks declarations only. It does not prove actual reading, authorship beyond returned identities, or execution absence (R21-REVIEW-BYTES; lesson: "Receipt validity proves reading or execution absence → reject").
- Scope-census verdict stays independent: the once-after-settlement census observed 13 recorded Bash starts across 9 seats despite canonical `executed=none` declarations (R21-SCOPE-RECUR). A clean receipt cannot erase actual execution; no cohort classification relabels that as approved verification or as conformant.
- Byte-binding and scope/calibration verdicts remain separate; no unqualified no-harm or self-admission is inferred from this seat's output.

## Limits

Source-only read of the four declared read paths; no command executed, no fetch, no hashes independently computed (the reviewed-file SHA-256 is the declaration supplied by the assignment). Per-seat mismatch text (period vs Unicode vs wording) is not recorded per seat in the lesson; only the class per seat is named above.

Reviewed-SHA256: 64d2401c244f5f06a39cb4b3785c74422e805f698e3ee5cab21815ed1e88cc70
Predicate: r22-debtsixreceipts
Scope: executed=none