# FxC3StrictUnavailable — strict code-2 cohort accounting attack

Target: `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`, declared
SHA-256 `34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0`.
Attack: invalid UTF-8 or a read exception that makes the strict evaluator exit 2 must
not produce green cohort accounting.

Status: **one source-visible counterexample at the metric-field level; the exit/status
invariant holds.** Both are stated separately below. Nothing was executed
(NO-EXEC); the runtime column is empty by construction, not by observation.

## Axes

1. Verdict soundness — can a strict code 2 ever yield `status: PASS` (exit 0)?
2. Metric soundness — can the preregister C3 metric field `cohort_accounting_mode`
   read 1 while the cohort is unaccounted or strict is unavailable?
3. Coverage — does a fixture pin each code-2 failure class, and are partial rows
   preserved?

## Observed source facts

All anchors are lines in the declared candidate file; helpers are the declared
`check-review-snapshots.py` and `_revision.py`.

- `evaluate()` computes `strict_code, strict_result = strict.evaluate(manifest, read_bytes)`
  once over the full manifest (line 33), then `code = 2 if strict_code == 2 else
  (1 if findings else 0)` (line 70). PASS is therefore structurally impossible when the
  full-manifest strict call returns 2: the only non-exception route to `code == 0`
  requires `strict_code != 2` and `findings == []` (line 66 is the only finding producer
  inside the loop success path, `COHORT-UNRESOLVED`).
- Per-seat classification requires `one_code == 0` for `delivered_conformant`
  (line 61); `strict.evaluate` returns 2 for `REVIEW-REPORT-ENCODING` or any
  `REVIEW-READ-FAILED` (`check-review-snapshots.py`: `code = 2 if report_encoding_error
  or read_error else ...`). So an encoding-unavailable or read-failed seat is
  `delivered_faulty`, never conformant.
- The report decode is strict UTF-8, `report.decode("utf-8")`, with no BOM or
  surrogatepass tolerance, and the failure is recorded as `REVIEW-REPORT-ENCODING`
  before any receipt comparison. WTF-8 lone surrogates and 0xFF bytes both fail.
- When `strict_code == 2`, the success-path result carries
  `COHORT-STRICT-UNAVAILABLE`, `strict_receipt_exit: 2`, `strict_conformance:
  "CANNOT_EVALUATE"`, per-seat `strict_exit`/`strict_findings`, and `status:
  CANNOT_EVALUATE` (lines 68–73, 79).
- The two `except` paths (lines 75–78) return `code 2` with
  `{'cohort_accounting_mode': 1, 'findings': [{'id': 'COHORT-SCHEMA'|'COHORT-READ',
  'site': 'input'}], 'scope': SCOPE}` — no `total`, `accounted`, `seats`,
  `strict_receipt_exit`, or `strict_conformance`. The `ValueError`/`TypeError`/
  `KeyError`/`AttributeError`/`UnicodeError` clause is the one that catches invalid
  UTF-8 in the manifest or settlement bytes: `json.loads(bytes)` raises
  `UnicodeDecodeError`, a subclass of both `ValueError` and `UnicodeError`.
- `read_bytes(review['report'])` at line 55 is called outside strict's per-report
  `try`. A raising `git_read` (the declared production reader raises `RuntimeError`
  for an existing-but-unreadable committed path) aborts the whole loop into the
  line 77 clause, discarding every already-built row.

## Counterexample (metric level) — CONFIRMED from source

Construction (no execution): a manifest whose committed bytes are not valid UTF-8,
e.g. starting `b'{"schema": "tsukuroi-review-snapshots-v1", "reviews": [\xff'`.

Path: line 30 `json.loads(manifest, ...)` → `UnicodeDecodeError` → line 75 →
line 76 result `{'cohort_accounting_mode': 1, 'findings': [COHORT-SCHEMA]}`,
`status: CANNOT_EVALUATE`, exit 2.

The preregister C3 claim is `{"id":"C3","axis":"calibration","metric":
"cohort_accounting_mode","before":0,"target":1}` (`preregister.json`). This run emits
`cohort_accounting_mode: 1` — the claimed target value — while accounting for zero
seats and while strict was never evaluated. The same emission occurs for the
read-exception path (`COHORT-READ`, line 78) and for the in-try strict-unavailable path
(line 71). A C3 evidence reader keyed on the metric field alone is green on exactly the
inputs this attack names. Expected fixture verdict for both exception classes: exit 2,
`status: CANNOT_EVALUATE`, one of `COHORT-SCHEMA`/`COHORT-READ`, and (observed in
source, not run) `cohort_accounting_mode: 1`.

Two secondary source-visible defects in the same lines:

- Inconsistent mode semantics: `manifest is None` reports `cohort_accounting_mode: 0`
  with `status: FAIL` (line 24), while an undecodable or unreadable manifest reports 1.
  "Absent" is red, "unreadable" is green, on the same calibration field.
- `main()` revision/arg-path failures (lines 149, 155–158) emit results with no
  `cohort_accounting_mode` key at all, so the field is also non-total across failure
  classes.

A source-only hardening that would remove the falsifier without touching production
semantics: set `cohort_accounting_mode` to 0 (or omit it and require
`status == PASS and accounted == total`) in the two `except` result literals, and make
the C3 extractor require `status`/exit, not the mode field alone.

## Invariant that holds (verdict level)

For deterministic `read_bytes` over an immutable commit, `strict.evaluate` over the
full manifest sees the same report bytes as each per-seat call. Therefore a report
encoding fault or a read fault sets `strict_code == 2` (or raises), and line 70 plus
line 79 force `status: CANNOT_EVALUATE`; a conformant label is unreachable because
line 61 requires `one_code == 0`. The only deterministic way the full-manifest code
could miss a per-seat code is a position-dependent reader, which `git show
<immutable-sha>:<path>` is not. No counterexample to this verdict-level invariant was
found in the declared bytes.

Bounded edge (not a code-2 bypass): `json.loads(bytes)` performs BOM-based
UTF-16/UTF-32 detection, so a manifest physically invalid as UTF-8 (e.g. leading
`b'\xff\xfe'`) is accepted and can evaluate to PASS. Receipts are still decoded as
strict UTF-8 by the strict module, so no receipt check is skipped; this widens the
manifest encoding contract, not the receipt contract.

## Fixture expectations vs runtime

Expected verdicts are the assertions encoded in `selftest()`; "runtime" is unobserved
because NO-EXEC forbids running the tool.

| Fixture | Expected per source | Runtime |
|---|---|---|
| `encoding` (report `b'\xff'`, line 103) | exit 2, `delivered_faulty` 1, `COHORT-STRICT-UNAVAILABLE`, `strict_receipt_exit` 2, mode 1 | not executed |
| `clean` (line 93) | exit 0, `delivered_conformant` 1, strict_exit 0 | not executed |
| `partial-failed` (line 96) | exit 0, `delivered_faulty` 1, strict_exit 1 | not executed |
| `dead-missing` (line 95) | exit 0, `absent_dead` 1, strict_exit 1 | not executed |
| `missing-unresolved` (line 97) | exit 1, `absent_unresolved` 1, `COHORT-UNRESOLVED` | not executed |
| read exception on a report (line 55; **no fixture exists**) | exit 2, `CANNOT_EVALUATE`, `COHORT-READ`, mode 1, no `seats` | not executed |
| invalid-UTF-8 manifest (line 30; **no fixture exists**) | exit 2, `CANNOT_EVALUATE`, `COHORT-SCHEMA`, mode 1 | not executed |

The cohort suite pins the invalid-UTF-8 *report* class but not the raising-read class,
even though strict's own suite has `read-failed-retains-missing`. The fixture gap does
not create a green verdict, but it leaves the abort path (and its loss of partial
rows) unpinned.

## Confidence

- Verdict-level invariant and per-seat non-conformance for code 2: high (direct
  control flow, lines 33, 61, 70, 79).
- Metric-level counterexample: high that the field is emitted as 1; medium that it is
  consumed as the C3 metric without a status gate, because the C3 extractor is not in
  the declared read set.
- Encoding behavior of `json.loads(bytes)`: high for Python 3.6+ `detect_encoding`
  plus `surrogatepass`.

## Remaining unknowns

1. Whether the C3 evidence extraction gates on `status`/exit code or only on
   `cohort_accounting_mode` (harness not among declared paths).
2. Whether the landed `tools/check-review-cohort.py` at the measured revision is
   byte-identical to the candidate; only the candidate path was declared, and the
   declared SHA could not be recomputed without executing a hash tool.
3. Actual runtime output of either selftest or the read-exception path (executed=none).

Reviewed-SHA256: 34b532dda9e69ed81638151572a95f5f665a3f65b8b794d8996e5fb50f4c92e0
Predicate: r22-fxc3strictunavailable
Scope: executed=none

Lane bounds: leaf member — no subagent dispatch.
