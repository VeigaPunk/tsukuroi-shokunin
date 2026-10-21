# OracleCohortPartial — independent oracle for the C3 partial-report case

Status: source-only derivation. No case invoked, no shell, no network, no cohort tool read.
Read set: the reviewed snapshot tool, the round-22 preregister, and the host tool-boundary
record. `tools/check-review-cohort.py` is **not** in this seat's read paths, so its settlement
schema, output token and finding namespace are recorded below as unresolved, not invented.

## Bottom line

The expected finite policy outcome `delivered_faulty` / `delivered-faulty` is **conditionally
correct**: it is forced only when the seat delivered a report whose bytes are *present and
readable* and whose strict receipt lines are missing, duplicated or mismatched. It is **not
forced** by the case description as written, because "observed error" is equally consistent
with the read/encoding failure paths, which the C3 bound places outside delivery (unresolved
absence). The fixture below pins the surface so the policy label becomes forced.

- Policy label: `delivered-faulty` (preregister token) / `delivered_faulty` (seat token).
  The two spellings are not interchangeable; see attack A8.
- Snapshot-tool verdict for the fixture: status `FAIL`, exit `1`, `pinned_reviews: 0`.
- Preserved receipt IDs (smallest omission fixture): `REVIEW-SNAPSHOT-MISMATCH`,
  `REVIEW-PREDICATE-MISMATCH`, both sited at `OracleCohortPartial`.
- Cohort-tool verdict ID: **unobserved** in this seat's read scope. No literal is claimed.

## Observed rules (source anchors)

Manifest contract and pre-read rejection:

- Schema literal `tsukuroi-review-snapshots-v1`, non-empty `reviews` list, one object per row
  with `name`, `report`, `source`, `sha256`, `predicate`; duplicate name/report, unsafe path,
  non-64-lowercase-hex digest, empty/control-bearing predicate, and duplicate JSON keys all
  raise and become `REVIEW-MANIFEST-SCHEMA` with exit 2 (lines 56-80, 122-124).
- `safe_path` rejects absolute paths, backslashes, empty/`.`/`..` segments, and Unicode
  categories Cc/Cf/Cs/Zl/Zp (lines 21-30). The same control test is applied to the predicate.
- `physical_lines` splits on LF only and strips at most one terminating CR (lines 42-44).
  Trailing LF is therefore optional and CRLF receipts are accepted.

Receipt evaluation order and IDs (lines 92-120):

1. Report surface returns `None` → `REVIEW-REPORT-MISSING`, exit 1.
2. Surface raises OSError/RuntimeError/TimeoutExpired → `REVIEW-READ-FAILED`, exit 2,
   and the row is skipped (`continue`).
3. Bytes fail UTF-8 decode → `REVIEW-REPORT-ENCODING`, exit 2; no receipt-line checks run.
4. Decoded lines are filtered by literal prefixes and compared by exact list equality:
   - digest lines must equal exactly `["Reviewed-SHA256: " + row.sha256]`, else
     `REVIEW-SNAPSHOT-MISMATCH`;
   - predicate lines must equal exactly `["Predicate: " + row.predicate]`, else
     `REVIEW-PREDICATE-MISMATCH`;
   - scope lines must equal exactly `["Scope: executed=none"]`, else `REVIEW-SCOPE-MISMATCH`.
5. The row counts as pinned only if no finding was added for it (lines 119-120).
6. Process exit is 2 if any row had a read or encoding error, else 1 if any findings exist,
   else 0 (line 121). Exit 2 therefore dominates unrelated receipt failures in other rows.

The selftest independently confirms the omission/duplication semantics: missing and duplicate
predicate lines both yield `REVIEW-PREDICATE-MISMATCH` (lines 171-177), invalid UTF-8 yields
`REVIEW-REPORT-ENCODING` with exit 2 (lines 191-193), and a read failure after a missing
report retains both IDs (lines 214-222). The harness compares only the *set* of finding IDs,
so duplicate occurrences of one ID are not distinguished (lines 224-238).

## Smallest literal fixture JSON

One manifest row is minimal because the schema rejects an empty `reviews` list. Source is the
reviewed file itself, so the declared digest is the seat-supplied literal; no hash needs to be
computed (execution is forbidden in this seat). The fixture is declarative and must not be
invoked.

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"OracleCohortPartial","report":"wave/OracleCohortPartial.md","source":"tools/check-review-snapshots.py","sha256":"b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8","predicate":"r22-oraclecohortpartial"}]}
```

Fixture surface map (the case, not run):

- `read_bytes("tools/check-review-snapshots.py")` → the reviewed bytes whose digest is the
  declared `sha256` above.
- `read_bytes("wave/OracleCohortPartial.md")` → the literal report bytes
  `b"Scope: executed=none\n"` (21 bytes; the final LF is optional per lines 42-44).

The report deliberately retains exactly one receipt line and omits the other two. This is the
smallest non-empty report that is unambiguously *delivered* (bytes returned, not `None`) and
strictly non-conformant.

Derived result, exactly:

```json
{"distinct_source_files":1,"findings":[{"id":"REVIEW-SNAPSHOT-MISMATCH","site":"OracleCohortPartial"},{"id":"REVIEW-PREDICATE-MISMATCH","site":"OracleCohortPartial"}],"pinned_reviews":0,"scope":"primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution","status":"FAIL","total_reviews":1}
```

Exit code `1`. Finding order follows the check order at lines 113-117. `REVIEW-SNAPSHOT-MISMATCH`
here means the report's digest line is absent, not that the source bytes differ; the source
surface matches the declared digest, so that ID appears once.

### Single-defect control fixture (fully literal, one ID)

If the intent is "one partial receipt line" rather than two omissions, keep the same manifest
and supply report bytes consisting of the exact digest line for the declared hash, the exact
predicate line, and a truncated scope line `b"Scope: executed=no\n"`. Derived result: status
`FAIL`, exit `1`, one finding `REVIEW-SCOPE-MISMATCH`, `pinned_reviews: 0`. Every byte of this
variant is constructible from observed literals.

## Policy expectation vs observed runtime result

| Layer | Value for this fixture | Basis |
|---|---|---|
| C3 policy partition | `delivered-faulty` (seat spelling `delivered_faulty`) | preregister `C3_bound` prose: delivered-faulty, absent-dead, absent-unresolved, delivered-conformant, "preserving strict receipt findings" |
| Snapshot receipt verdict | `FAIL`, exit `1`, two preserved IDs | lines 107-121, direct source |
| Observed runtime "error" in the case | **not reproduced** | this fixture has no read or encoding failure, so exit is 1, not 2 |
| Cohort tool verdict/ID | unresolved | `check-review-cohort.py` outside this seat's read paths; NO-EXEC forbids running it |

The case phrase "failed outcome observed error" belongs to the runtime/observability layer, not
to the receipt layer. A report can be receipt-faulty while the runtime result is a clean
`FAIL`; conversely, a runtime `CANNOT_EVALUATE` (exit 2) does not by itself prove a faulty
delivery. The policy expectation and the observed runtime status must be reported separately
and never substituted for one another.

## Attacks on the expectation

A1. **Error source.** If "observed error" is exit 2 from a report/source read failure
(`REVIEW-READ-FAILED`) or invalid UTF-8 (`REVIEW-REPORT-ENCODING`), the C3 outcome is not
forced to delivered-faulty: a read failure is unresolved absence, and an encoding failure
preserves only `REVIEW-REPORT-ENCODING`, not the two omission IDs. The expectation is wrong
unless the runtime error is disambiguated from the receipt failure.

A2. **Quoted receipts.** The checker only filters lines by prefix anywhere in the file. A
report that merely quotes the three required lines once each passes (`pinned_reviews: 1`,
exit 0) regardless of how empty or partial the actual work is. A "partial report" containing
an intact receipt block is therefore `delivered-conformant`, contradicting the expectation.
This is also a self-reference hazard for any report checked by this tool.

A3. **Truncation outside the receipt block.** The checker has no completeness notion beyond
the three lines. A report truncated after the receipts is a PASS. "Partial" must mean
partial *in the receipt lines*, not a short report.

A4. **Present vs absent boundary.** `None` yields `REVIEW-REPORT-MISSING` and policy absence;
zero-length bytes `b""` are present and yield all three receipt IDs with exit 1. The policy
outcome therefore hinges on a surface distinction (`None` vs bytes) that "partial report" does
not mention. The fixture pins non-empty bytes.

A5. **Manifest rejection pre-empts classification.** Any invalid row (duplicate name/report,
unsafe path, malformed digest, empty or control-bearing predicate, duplicate JSON key) yields
`REVIEW-MANIFEST-SCHEMA`, exit 2, and no per-seat evaluation at all. A partial report under an
invalid declaration cannot be delivered-faulty.

A6. **Source read masks the report.** A failing source read `continue`s before the report is
read (lines 85-89); the partial report is never inspected and the row becomes
`REVIEW-READ-FAILED`/exit 2. The fixture requires a readable source matching the declared hash.

A7. **ID conflation.** `REVIEW-SNAPSHOT-MISMATCH` is emitted both for source-byte tamper
(line 90) and for an absent/mismatched/duplicated report digest line (line 113). Finding IDs
alone cannot prove "partial report"; the report bytes are required evidence. If the source also
mismatches, the same ID is appended twice, and the selftest's set comparison would not notice.

A8. **Verdict token spelling.** The preregister writes `delivered-faulty`; the seat assignment
writes `delivered_faulty`. If the cohort checker compares exact strings, one of the two fails.
The exact emitted token is unobserved here; do not normalize without evidence.

A9. **Outcome-fault vs receipt-fault.** The readable source evaluates receipts only; it cannot
see a seat's failed work outcome. Whether C3 classifies a failed seat with a conformant receipt
as delivered-faulty or delivered-conformant is not decidable from the declared read paths. In
this case both dimensions happen to agree, which hides the ambiguity.

A10. **Per-row vs per-process status.** Exit 2 dominates when *any* row has a read/encoding
error (line 121). A whole-run "error" observation does not reclassify a different seat whose
row was a clean receipt failure. Accounting must be per declared seat, not per process exit.

A11. **Multiplicity.** Missing, duplicated and mismatched lines all collapse to one ID per
receipt category, and the selftest compares sets. "Preserving strict receipt findings" must
state whether multiplicity and site are preserved; the source tool preserves both in its list
(`add(fid, name)` per occurrence), so a cohort ledger that deduplicates loses information.

A12. **CRLF and trailing LF.** `physical_lines` accepts CRLF and a missing final LF, so
"three physical lines" is a convention the parser does not enforce. Fixture minimality may drop
the trailing LF without changing the verdict.

A13. **Predicate exactness.** Matching is exact string equality including case and spacing; a
line with a lower-case prefix or an extra space is a `REVIEW-PREDICATE-MISMATCH`, not a
schema error. A predicate that is only whitespace or contains Cf/Zl/Zp is a schema error
instead. These are different policy outcomes (faulty delivery vs cannot-evaluate).

## Confidence and remaining unknowns

- High: receipt finding IDs, evaluation order, presence/absence/encoding distinctions, and
  exit aggregation, all read directly from the source.
- Medium: the mapping of receipt failure to the C3 label `delivered-faulty`; it rests on the
  preregister's prose bound, not on an observed cohort implementation.
- Unresolved: the cohort checker's exact verdict token and finding namespace; the settlement
  schema and whether it stores per-seat outcomes or raw events; whether C3 classifies on
  outcome, receipt, or both; whether the cohort manifest reuses the reviewed schema (only the
  `--manifest` flag name suggests it). These require reading `tools/check-review-cohort.py`,
  which is outside this seat's declared read paths.
- Not done by design: the fixture was not invoked; no bytes were hashed by execution; the
  reviewed file's digest is taken from the seat declaration.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortpartial
Scope: executed=none
