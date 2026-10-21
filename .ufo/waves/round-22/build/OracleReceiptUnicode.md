# OracleReceiptUnicode — source-only independent oracle

## Axes and result

Axes: delimiter discrimination; exact finding attribution; evidence integrity under NO-EXEC/NO-FETCH.

**Expected finite policy outcome: STRICT_FAIL.** The source-derived evaluator outcome is exit **1**, status **FAIL**, with exactly **REVIEW-SCOPE-MISMATCH** at site **A**. This is a prediction from source, not an observed runtime result. No case, interpreter, command, test, or mutated input was invoked.

## Minimal literal fixture JSON

This envelope represents the two existing `evaluate(raw, read_bytes)` inputs; it is not a new checker input schema. Conceptually serialize `manifest` as JSON for `raw`, and provide `files` values as UTF-8 bytes through the lookup callback, following the existing selftest adapter at lines 224–227. The keys `s` and `r` are virtual byte-map identities, not accessed filesystem paths. The empty string is the empty source byte sequence, whose standard SHA-256 is the literal used below. No hash computation was executed.

```json
{"manifest":{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","source":"s","report":"r","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"}]},"files":{"s":"","r":"Reviewed-SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\nPredicate: p\nScope: executed=none\u2028"}}
```

One review, one empty source, one report, and single-character identities keep the fixture minimal without unrelated failures. There is exactly one Unicode separator, U+2028 LINE SEPARATOR, at the end of the scope receipt. JSON `\u2028` denotes that actual character; the conceptual report bytes end in `E2 80 A8`, not the six ASCII characters backslash-u-2-0-2-8.

**Input mutant:** replace the clean report's terminal LF with U+2028; preserve everything else. This substitution is only described here, not materialized or executed. The clean control is the same JSON with the final report escape `\u2028` replaced by `\n`.

## Exact source-derived verdict

```json
{"exit":1,"policy_verdict":"STRICT_FAIL","payload":{"status":"FAIL","distinct_source_files":1,"pinned_reviews":0,"total_reviews":1,"findings":[{"id":"REVIEW-SCOPE-MISMATCH","site":"A"}],"scope":"primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution"}}
```

`policy_verdict` and `exit` are explanatory envelope fields; the checker itself returns the exit code and payload, and does not emit the string `STRICT_FAIL`.

Derivation from the assigned source:

- Lines 63–81 accept the one-row manifest: required schema, safe nonempty virtual paths, distinct identity, lowercase 64-hex digest, and plain predicate are valid.
- Lines 85–91 compare the empty source against its matching digest; there is no source mismatch.
- Lines 101–107 decode valid UTF-8 and call `physical_lines`.
- Lines 42–44 split **only at LF**, removing at most one terminal CR. U+2028 is retained in the last physical line.
- Lines 108–116 therefore find exactly matching digest and predicate declarations.
- Lines 112 and 117–118 find `Scope: executed=none` followed by U+2028, not the exact required scope string. Only `REVIEW-SCOPE-MISMATCH` is added, with site `A`.
- Lines 119–128 leave pinned reviews at zero and return code 1/status FAIL. Neither malformed UTF-8 nor a read error is present, so this is not CANNOT_EVALUATE.

## Bounded detector and plausible defect

The bounded behavioral detector would evaluate this one fixture and assert the exact exit, status, finding array, and counts above. Its clean control would assert exit 0/status PASS, no findings, and counts distinct=1, pinned=1, total=1.

A plausible smallest parser defect is replacing only `text.split("\n")` at line 44 with `text.splitlines()`. That generic splitter recognizes U+2028 and would remove the counterfeit terminal separator, making all three receipts match. This code mutation was **not applied**: the seat authorizes writing only this report, not a scratch checker.

| Checker bytes / input | Expected evaluator result, not observed | Expected detector result, not observed |
| --- | --- | --- |
| Assigned source / clean LF control | exit 0, PASS, no findings, pinned=1 | Control passes |
| Assigned source / Unicode fixture | exit 1, FAIL, only REVIEW-SCOPE-MISMATCH, pinned=0 | Strict-failure assertion passes |
| Hypothetical `splitlines()` defect / same Unicode fixture | exit 0, PASS, no findings, pinned=1 | Strict-failure assertion fails; would kill this defect |
| Original bytes restored / same Unicode fixture | Same prediction as assigned source | Same strict-failure assertion passes |

**Actual outputs:** no runtime outputs exist for any row. **Mutation verdict: INCONCLUSIVE / NOT RUN**, not empirically killed or survived. The assigned source supports the policy expectation by inspection. The shown selftest already contains form-feed and vertical-tab pseudoline cases (lines 181–190), which also appear capable of detecting this broad splitter defect; absence of an explicitly named Unicode-separator case in the shown case list is not evidence that the defect survives existing tests.

## Ambiguities challenged

1. **EOF is not an exemption.** The checker does not require a final LF, so simply omitting it is allowed. Appending U+2028 is different: it remains part of the scope declaration and breaks exact equality. Replacing a terminal LF isolates one finding, avoiding the two mismatches that can arise when a counterfeit separator joins two required declarations.
2. **Rendering is not physical-line authority.** A viewer may display U+2028 as a new line; the checker deliberately uses LF, not display layout or Unicode's broader line-boundary rules.
3. **Failure IDs depend on placement.** This fixture places U+2028 only in the report's final scope line. Putting it into the manifest predicate would instead trigger manifest validation; placing it between other receipt lines could change the finding set. No universal single ID is asserted for every Unicode placement.
4. **Not a blanket Unicode ban.** The report is not globally rejected merely for containing U+2028. The failure here follows from exact scope-line equality. This probe establishes no policy for unrelated Unicode in free-form report prose and does not cover U+2029 or other separator characters.
5. **Detection is not enforcement.** This is a strict receipt oracle, not proof of actual reading/nonexecution or a native per-seat preventive allowlist. The preregistration and host-boundary source explicitly limit the round to prompt bindings and post-hoc detection/evidence.

## Hash and restoration evidence

- Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py`.
- Before SHA-256: the assignment-supplied value recorded in the final receipt; **not independently measured**.
- Mutated-checker SHA-256: unavailable because no checker mutation was materialized.
- After/restored SHA-256: **not measured**; no byte-restoration claim is made from a hash comparison.
- Restoration action: none required by this source-only probe. No source/scratch bytes were written; the only write is this authorized report. Thus no executable mutation was left behind, but pristine/mutated/restored detector runs and measured before/after hashes are intentionally absent under NO-EXEC.
- Tools installed or updated: none. Network/fetches and delegation: none.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclereceiptunicode
Scope: executed=none
