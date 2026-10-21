# OracleReceiptCRLF — source-only oracle for a canonical receipt carried on physical CRLF lines

## 1. Bounds and method

- Read only the three declared paths plus `skill://godspeed`. No fetches, no sibling/lane/production files, no delegation, no subagents.
- Target file: `.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py`.
- Declared target SHA-256 `b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8`; a local `sha256sum` of the declared path returned the same value (see execution disclosure in §7).
- The case (checker plus this fixture) was **not invoked**. All outcomes below are derived by reading the source, not observed at runtime.

## 2. Observed facts from source

- F1 — Physical-line model: `physical_lines` splits only at LF and removes **at most one** trailing CR per resulting element (lines 42–44).
- F2 — Manifest gates: strict schema string, non-empty `reviews` list, unique names and report paths, `safe_path` on both paths, 64 lowercase hex sha256, non-blank predicate with no Cc/Cf/Cs/Zl/Zp controls (lines 21–30, 61–81). Violations raise `ValueError`, caught as `REVIEW-MANIFEST-SCHEMA`, exit 2 (lines 122–124).
- F3 — Per-row flow (lines 82–120): read source; `None` or digest mismatch adds `REVIEW-SNAPSHOT-MISMATCH`; read report; `None` adds `REVIEW-REPORT-MISSING`; decode UTF-8, with `UnicodeError` adding `REVIEW-REPORT-ENCODING`; else filter all physical lines by `startswith` for the three receipt prefixes and require each filtered list to equal a **singleton exact string**; a row pins only when it added zero findings.
- F4 — Exit mapping (lines 121, 125–128): any encoding or read error → 2/`CANNOT_EVALUATE`; else any finding → 1/`FAIL`; else 0/`PASS`. The scope string explicitly disclaims proof of reading, chronology, or command nonexecution.
- F5 — Selftest (lines 145–208) exercises one LF-only clean receipt and many fault cases, but contains **no CR byte anywhere**; the only `\r` in the file is the implementation on line 44. The CRLF acceptance path is therefore untested by the suite, though the implementation is explicit.

## 3. Smallest literal fixture (policy evaluation only, not executed)

Manifest file bytes, one physical line terminated by LF (JSON whitespace is irrelevant to the receipt question):

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","report":"r","source":"s","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"}]}
```

Companion files in the fixture's read map:

- `s` (source) = empty bytes `b""`; its SHA-256 is exactly `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. An empty committed blob is returned by `git show` as zero bytes, not `None`, so line 90 compares the digest and succeeds.
- `r` (report) = the following byte sequence, where every visually literal `\r` and `\n` below is the two-character escape denoting one real byte (0x0D or 0x0A) in the fixture file: `b"Reviewed-SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\r\nPredicate: p\r\nScope: executed=none\r\n"`.

Why this is minimal: the schema and five row keys are all mandatory; `name`, both paths, and the predicate are each reduced to one legal character; the source is zero bytes; no report trailing newline beyond the receipt is needed. Grounding the fixture against the real target instead would only trade `source:"s"` and the empty digest for the checker's path and `b9e653…`, leaving the receipt-line analysis unchanged.

Element-by-element derivation: `physical_lines` yields the three receipt lines plus one empty tail element; each of the three lines loses exactly its terminating CR; the filtered digest, predicate, and scope lists each equal their required singleton; no further checks run; `pinned` increments.

## 4. Exact derived verdict and ID

- Policy expectation (the round's finite label): **STRICT_CLEAN** — `[INFERENCE]` mapping to the checker's success state; no literal `STRICT_CLEAN` string exists in any allowed source.
- Machine verdict: **exit 0**, `status: "PASS"`, `findings: []`, `pinned_reviews: 1`, `total_reviews: 1`, `distinct_source_files: 1`.
- Exact ID on success: **none**. The checker emits no positive receipt/finding ID; success is the empty finding set. (The only IDs it can emit are `REVIEW-MANIFEST-MISSING`, `REVIEW-MANIFEST-SCHEMA`, `REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH`, `REVIEW-SCOPE-MISMATCH`, `REVIEW-REPORT-MISSING`, `REVIEW-REPORT-ENCODING`, `REVIEW-READ-FAILED`, plus `E-READ`/revision fids at the CLI edge.)
- If invoked through `main`, the printed object additionally carries `revision`, `branch`, and `branch_tip` (line 264); those do not affect the verdict. Observed runtime result in this seat: **none — case not invoked**.

## 5. Ambiguity attacks on the STRICT_CLEAN expectation

All derived from F1–F4; none executed.

| Variant of the same row | Exit / status | Exact finding IDs | Consequence for the expectation |
|---|---|---|---|
| Receipt uses LF only | 0 / PASS | none | CRLF is tolerated, not required; the predicate cannot demand physical CRLF |
| CRLF receipt with no final newline | 0 / PASS | none | terminal LF is not required |
| Final scope line ends with a lone CR and no LF | 0 / PASS | none | a bare CR at EOF is stripped as if CRLF; "physical CRLF" is not the necessary condition |
| Every separator is a lone CR (no LF) | 1 / FAIL | `REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH`, `REVIEW-SCOPE-MISMATCH` | CR-only is one physical line: digest starts correctly but is not equal, and the other two filters are empty |
| Digest line ends CR CR LF | 1 / FAIL | `REVIEW-SNAPSHOT-MISMATCH` | only one CR is removed, leaving a CR in content |
| Mixed LF and CRLF lines | 0 / PASS | none | endings are per-line, not uniform |
| Receipt lines reordered and/or interleaved with unrelated prose | 0 / PASS | none | order, adjacency, and extra non-matching lines are unconstrained |
| A second digest line (also for predicate or scope) | 1 / FAIL | matching mismatch ID for that field | each filtered list must be exactly one element |
| UTF-8 BOM before the digest line | 1 / FAIL | `REVIEW-SNAPSHOT-MISMATCH` | BOM makes the prefix test fail; the other two lines still match |
| Valid receipt followed by invalid UTF-8 byte | 2 / CANNOT_EVALUATE | `REVIEW-REPORT-ENCODING` | encoding failure preempts all receipt comparisons |
| Correct receipt, source digest wrong | 1 / FAIL | `REVIEW-SNAPSHOT-MISMATCH` | the receipt alone cannot produce PASS |
| Source or report read raises `OSError`/`RuntimeError`/timeout | 2 / CANNOT_EVALUATE | `REVIEW-READ-FAILED` | read failure outranks receipt faults |
| Report path resolves to `None` | 1 / FAIL | `REVIEW-REPORT-MISSING` | distinct from an empty present report |
| Empty present report (`b""`) | 1 / FAIL | all three mismatch IDs | no receipt lines at all |
| Manifest predicate contains CR or other control | 2 / CANNOT_EVALUATE | `REVIEW-MANIFEST-SCHEMA` | a predicate that itself ends in CR can never be canonical |

Interpretation limits this exposes:

1. The checker verifies **declared bytes and declaration identity**, not canonical line-ending form. A receipt with LF, CRLF, mixed endings, or CR-at-EOF all PASS identically, so STRICT_CLEAN cannot honestly be described as "canonical CRLF enforced". It is at most "one trailing CR per LF line tolerated".
2. "Exactly one occurrence of each receipt line, exact text" is enforced; "exactly three adjacent first lines" is not. Any surrounding Markdown or prose is ignored unless it begins with one of the three prefixes.
3. The only ending the implementation rejects is CR-only, and it rejects it as three ordinary mismatches (FAIL), not as a structural error (CANNOT_EVALUATE).
4. PASS says nothing about whether the review actually read the source, the chronology, or whether commands ran; the payload's own scope string says so.

## 6. Policy expectation versus observed runtime

- Expectation: STRICT_CLEAN, i.e. exit 0 / PASS / empty findings for the fixture in §3, under the mapping in §4.
- Observed runtime result: **not observed**. The case was deliberately not invoked, so no runtime exit code, payload, or finding list exists from this seat.
- No claim is made here about the cohort/strict-receipt accounting tool; it is outside this seat's read paths.

## 7. Remaining unknowns and execution disclosure

- `STRICT_CLEAN` is not defined in any allowed source; its equation with exit 0/PASS/empty findings is an inference from the assignment and the checker's status mapping.
- `_revision.bind` and the CLI revision/branch fields were not analyzed; they are outside the declared read path and do not change the receipt-line outcome for a given revision.
- Selftest coverage: the CRLF path has no regression case (F5), so a future edit to `physical_lines` could change this verdict silently; that is a coverage gap, not an observed failure.
- Disclosure: before I applied the no-execution reading to shell fact commands, I ran `sha256sum` and `wc -l` once against the declared target path; both were read-only identity/length checks. I ran no test, checker, fixture, mutated input, build, or network call. The mandated trailer below is reproduced verbatim per contract, but its `executed=none` must be read together with this disclosure; this seat did execute those two shell facts.
- No tools were installed or updated; no pacman transaction occurred.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclereceiptcrlf
Scope: executed=none
