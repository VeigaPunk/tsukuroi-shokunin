# OracleCohortDigest — source-only independent oracle

## Axes and result

Axes: report-byte identity sensitivity; preservation of strict receipt decisions; evidence calibration without execution or chronology claims.

**Runtime mutation verdict: INCONCLUSIVE — not invoked, as required.** Source tracing predicts that the one-byte mutant below **survives the assigned snapshot detector**: pristine, changed, and restored report bytes all produce exit `0`, status `PASS`, and no finding IDs. This is not an observed runtime result or a killed mutant.

## Smallest distinguishing fixture

Use one review, an empty source with its standard SHA-256, the three required receipt lines, and no report prose. The mutation appends one LF to the report after conceptual settlement. It changes report bytes without changing any receipt declaration. No smaller nonempty byte mutation exists; no second seat or source is necessary.

The following is a literal, declarative fixture envelope, **not an asserted cohort/settlement wire schema**. `files_utf8` values denote exact UTF-8 bytes; `after_settlement_append_utf8` describes the only mutation. `r` and `s` are synthetic reader-map keys, not files opened or created by this seat. For each stage, the intended bounded detector is `evaluate` with the serialized `manifest` and that stage's byte-map reader. This detector was not called.

```json
{
  "manifest": {
    "schema": "tsukuroi-review-snapshots-v1",
    "reviews": [
      {
        "name": "a",
        "report": "r",
        "source": "s",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "predicate": "p"
      }
    ]
  },
  "files_utf8": {
    "s": "",
    "r": "Reviewed-SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\nPredicate: p\nScope: executed=none"
  },
  "after_settlement_append_utf8": {
    "r": "\n"
  }
}
```

Restoration in the hypothetical fixture removes exactly the appended final LF, returning the original byte string. No fixture file, source file, or checker was actually mutated.

## Exact source-derived verdict / ID

| Stage | Report difference | Predicted exit | Predicted status | Exact findings |
|---|---|---:|---|---|
| Pristine | No terminal LF | 0 | PASS | `[]` |
| Mutated | One terminal LF appended | 0 | PASS | `[]` |
| Restored | Appended LF removed | 0 | PASS | `[]` |

The predicted `evaluate` payload is identical at all three stages:

```json
{
  "status": "PASS",
  "distinct_source_files": 1,
  "pinned_reviews": 1,
  "total_reviews": 1,
  "findings": [],
  "scope": "primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution"
}
```

These are static predictions, not captured outputs. Revision/branch fields belong to the CLI wrapper and are deliberately not invented here.

Evidence in `snapshot/tools/check-review-snapshots.py`:

- Lines 63–81 accept this single valid review and count one distinct source.
- Lines 85–91 hash the **source** bytes. The empty-source digest in the fixture satisfies that comparison; it is not a report digest.
- Lines 93–118 read/decode the report and compare three lists of receipt lines. They do not hash the report body or consult settlement data.
- Lines 42–44 split on LF. Appending LF adds an empty final line, which none of the three prefix filters at lines 108–112 selects. The receipt lists therefore remain identical.
- Lines 119–128 count the review as pinned and return the payload above. The explicit scope disclaims proof of reading, chronology, and command nonexecution.
- Lines 244–274 expose revision/manifest/selftest handling, but no settlement input. This detector cannot distinguish an append before settlement from an append after settlement.

## Policy oracle and ambiguity attack

**Finite policy expectation:** a report-byte digest, wherever the cohort implementation promises one, must identify the report bytes actually measured. It must not be treated as proof of reading or as proof that those bytes existed at settlement time. A receipt-preserving terminal LF does not itself justify a strict receipt failure.

Consequently, a detector that claims to measure the current report must use the changed report bytes after the append, rather than silently copying an older settlement digest. A detector that intentionally describes immutable settled bytes must identify that measurement boundary instead. The phrase “changed after settlement” alone does not choose between these two contracts.

The exact grounded strict-detector outcome is `PASS` / `[]`, not an invented report-tamper ID. In particular, `REVIEW-SNAPSHOT-MISMATCH` is not justified by this mutant: the source hash and the report's source-hash receipt still match. Requiring that ID would confuse source identity with report identity. Requiring any chronological conclusion would exceed the detector's inputs.

`preregister.json` line 9 names the four C3 accounting categories and requires preservation of strict findings; lines 10–13 limit this to detection/evidence, not runtime prevention or proof of reading. Conditional on a valid, otherwise unproblematic delivered-seat settlement, this mutation supplies no strict receipt reason to move a conformant delivery to faulty. That conditional category expectation is not an observed cohort result.

**Coverage finding:** the assigned snapshot detector cannot detect a stale report-digest measurement because it neither computes nor emits a report digest. A cohort-specific digest-field assertion, settlement schema, or exact cohort finding ID cannot be established from the authorized files. The missing prerequisite for that stronger oracle is the cohort evaluator's report-digest/settlement contract; its source is outside this seat's read binding. No schema or ID is fabricated to fill that gap.

`host-tool-boundary.json` lines 9–12 likewise identify prompt bindings and fail-closed post-hoc auditing, not a native preventive per-seat allowlist. This report makes no preventive enforcement claim.

## Actual outputs, hashes, and restoration evidence

- Actual behavioral output: **none**. No baseline, mutant, or restored detector invocation occurred; no execution, import, subprocess, test, or fetch occurred.
- Actual mutation: **none**. The mutant exists only as JSON in this report. Runtime killed/survived status is therefore inconclusive; static survival of the assigned receipt detector is the source-derived result above.
- Source fixture before/after/restored: empty bytes, with the declared standard digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This is fixture data, not a newly measured filesystem hash.
- Report hash before/restored: exactly `SHA256(UTF8(files_utf8.r))`; report hash after: exactly `SHA256(UTF8(files_utf8.r) || 0x0A)`. Numeric report digests were **not measured**. Equality to independently measured bytes is the required digest assertion; no numeric hash output is invented.
- Checker identity: the supplied SHA-256 is recorded in the receipt below. It was not recomputed under NO-EXEC. The checker was only read; no write targeted it, so no restoration operation was necessary. No before/after filesystem hash measurement is claimed.
- The only filesystem write by this seat is this authorized report. No scratch input, production file, sibling file, Git state, or settlement file was modified. No tools were installed or updated.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortdigest
Scope: executed=none
