# FxC3Predicate — wrong/missing/duplicated predicate line, source-only probe

Reviewed-SHA256: 736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e
Predicate: C3-predicate mismatch

## Axes and bounds

- **Calibration (C3):** distinguish an exact predicate receipt from a wrong, missing, duplicated, or position-shifted predicate declaration; distinguish source predictions from measured detector results.
- **Operability:** the predicate receipt detector must have an explicit non-clean path (`REVIEW-PREDICATE-MISMATCH`) independent of the digest and scope receipt paths, and a missing report must keep the gate red regardless of predicate text.
- **Historical preservation:** dead-seat manifest rows whose reports are absent must remain findings; no predicate text on a surviving report may compensate for them.

This is one leaf, source-only falsification probe of candidate revision `0a14952b59d20179e1c813af58befaecd6992a17`, against round21 baseline `82e519203e676c532b1dc5ea91a85671f2286e7b`. No subagents, runtime, imports, commands, tests, actual mutants, installations, production edits, or historical-report writes were used. Only this assigned report is written. No outside closure, admission, promotion, or ordinal gain is asserted.

## Snapshot identity and auxiliary dependencies

All candidate evidence below comes from immutable copies beneath `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate/`. The primary receipt above binds only `tools/check-review-snapshots.py`, not these auxiliary files. SHA-256 values are the **observed predispatch declarations** in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/candidate-files.json`, not independently recomputed hashes.

- Primary `tools/check-review-snapshots.py`: `736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e` (inventory lines 94–98).
- Auxiliary executable source `tools/_revision.py`: `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf` (inventory lines 64–68); supplies `bind()` and `clean_env()` used by the CLI path at primary lines 89–100, 154–160.

The live wave manifest `.ufo/waves/round-21/reviews.json` was read for row-shape context only (e.g., the `ExecReview` row declaring predicate `C3-pinned-review-receipt-contract`); it is a moving wave file, not a copied candidate input, and supplies no verdict evidence. Every listed inventory entry declares the same candidate revision. No moving draft or production checker supplied the verdict.

## Detector mechanism (observed source)

Manifest-side validation, `tools/check-review-snapshots.py:43–52`: each row's `predicate` must be a `str`, non-empty, and free of `\r`/`\n`; any violation raises `ValueError`, caught at lines 80–82 as `REVIEW-MANIFEST-SCHEMA`, code 2.

Report-side check, lines 57–79: per row, `read_bytes` fetches source and report. Missing source or digest inequality adds `REVIEW-SNAPSHOT-MISMATCH` (lines 59–62). Missing report adds `REVIEW-REPORT-MISSING` and skips text checks (lines 63–64). Otherwise the report is UTF-8 decoded, split with `splitlines()`, and every column-zero `Predicate:` line is collected (lines 66–70). The collected list must equal exactly `["Predicate: " + row["predicate"]]` or `REVIEW-PREDICATE-MISMATCH` is added (lines 73–74). Any finding withholds `pinned` and yields code 1/`FAIL` (lines 77–79).

In-source fixture assertions: the `predicate` case at line 115 swaps the fixture predicate value and expects code 1 with `{REVIEW-PREDICATE-MISMATCH}`; the `duplicate-digest` case at line 117 proves the same exact-list construction fails duplicated receipts. Lines 126–130 compare both code and finding-ID set. These are **observed fixture assertions, not an observed passing selftest**.

## Variant analysis (source predictions, not executions)

Using the single-review fixture at lines 104–109 as the bounded detector input:

| Report predicate surface | Predicted result |
|---|---|
| Exact `Predicate: fixed-five-decisions` | code 0, `PASS`, pinned 1/1 |
| Wrong value (`Predicate: other`) | code 1, `FAIL`, `REVIEW-PREDICATE-MISMATCH` (line 115 fixture asserts this) |
| Missing line entirely | `predicate_lines == []` ≠ expected → code 1, `REVIEW-PREDICATE-MISMATCH` |
| Duplicated identical line | list length 2 ≠ 1 → code 1, `REVIEW-PREDICATE-MISMATCH` (mirrors line 117 digest-duplicate assertion) |
| Right + wrong line both present | length 2 list ≠ expected → code 1 |
| Wrong-case label (`predicate:`/`PREDICATE:`) | `startswith("Predicate:")` excludes them → treated as missing → code 1 |
| Leading whitespace before label | not column-zero → treated as missing → code 1 |
| Trailing whitespace/value after expected text | strict list equality fails → code 1 |
| Missing report file | `REVIEW-REPORT-MISSING`, code 1, pinned withheld — dead-report red preserved (lines 63–64, 77–79) |

**[INFERENCE]** All listed variants land on nonzero exit; the wrong/missing/duplicated trident has no acceptance path, and the assigned "C3-predicate mismatch" mutant predicts code 1/`FAIL` with findings `[{"id":"REVIEW-PREDICATE-MISMATCH","site":<row name>}]`, no digest or scope IDs.

## Findings

**Minor — receipt lines need not be standalone physical lines.** `str.splitlines()` at line 67 splits on `\v`, `\f`, `\x1c`–`\x1e`, `\x85`, `\u2028`, `\u2029` in addition to `\n`/`\r\n`, and silently discards those boundary characters. Consequently `Predicate: fixed-five-decisions\fjunk` splits into an exact expected line plus `junk`, and `garbage\vPredicate: fixed-five-decisions` lets a receipt begin mid-physical-line; both pass the exact-list test. This cannot falsify the declared predicate *value* (the bytes before the boundary must still spell `Predicate: <value>` exactly), so the assigned mismatch attack remains red — but under a strict "exact standalone lines" contract the gate accepts receipts that share a byte line with invisible or sibling text. Severity: minor robustness gap, not a falsification channel.

**Minor — one undecodable report collapses the whole wave verdict to `CANNOT_EVALUATE`.** The `try` at lines 36–82 wraps the entire per-row loop; `report.decode("utf-8")` raising `UnicodeError` inside row processing is caught by the manifest-level handler at line 80 and labeled `REVIEW-MANIFEST-SCHEMA`, code 2. A single malformed report byte thus discards all other per-row findings and reports a manifest-schema site rather than a report-content site. Still red (nonzero), but status `CANNOT_EVALUATE` and the finding ID are misleading for a report-side defect and reduce diagnostic saturation across rows.

**Non-blocking — `safe_path` admits control characters in `source`/`report`.** Lines 20–23 reject absolute paths, backslashes, and empty/dot/dotdot segments but not `\n` or other control bytes. In real mode `git show` fails closed into `E-READ`/`CANNOT_EVALUATE` (lines 89–100, 161–163); in `selftest`'s dict-backed `read_bytes` a newline-bearing key could match. Unreachable on the production path; cosmetic.

**Non-blocking — whitespace-only predicates validate.** `not row["predicate"]` at line 50 rejects only the empty string; `" "` passes, making `Predicate:  ` (double space) the required receipt. Declared-predicate semantics stay literal; cosmetic oddity.

**Confirmed limitation (by design):** the gate compares declared strings only — the predicate is never validated against source content, and the docstring at line 2 plus the `scope` field at line 86 state it is "not proof of reading, chronology or command nonexecution". Disclosed predicate strings do not prove actual reading; this matches the assignment's stated expectation.

## Output and verdict

**Actual behavioral output:** none. No evaluator, selftest, CLI, baseline, mutant, or restored case was run; the observations are the pinned source lines cited above.

Predicted detector table (single-report bounded inputs):

| Report state | Predicted |
|---|---|
| Pristine exact predicate receipt | code 0 / `PASS`, pinned 1/1 |
| Value mutated, missing, duplicated, or case/position shifted | code 1 / `FAIL`, `REVIEW-PREDICATE-MISMATCH` |
| Report absent | code 1 / `FAIL`, `REVIEW-REPORT-MISSING` |

**Verdict:** the assigned predicate-mismatch attack and its missing/duplicated siblings expose no source-level acceptance path; the exact-list comparison at lines 69–74 rejects each with a dedicated finding ID, and missing dead reports hold the gate red independently. The two minor findings (splitlines boundary looseness, per-loop exception collapsing to `CANNOT_EVALUATE`) weaken exactness/diagnostics but not falsification resistance. **Runtime mutation verdict: inconclusive/unexecuted** — no clean baseline or detector output was exercised. L1 alone owns final authorized measurements.

## Restoration and hash evidence

No actual mutation was written; nothing to restore. The before identity is the supplied primary SHA-256 `736c5dc85c527ac673b5fa9a6276a295e475cf3c2d2c007bea8c2e7d6de7e60e`; auxiliary `_revision.py` identity `06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf`. No after/mutant hash is produced under NO-EXEC. The tool record contains read calls plus this unique report write only. **[INFERENCE]** Candidate hashes remain the before identities because this seat wrote nothing to them; not a rehash claim.

No tool was installed or updated; none was needed for source review. The host-wide pacman pause was not exercised.

Scope: executed=none