# OracleReceiptDigest — source-only oracle: wrong exact SHA-256

Target: `.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py` (pinned SHA-256 given by assignment; not independently recomputed — NO-EXEC).
Reads: the target, `preregister.json`, `sources/host-tool-boundary.json`. `skill://godspeed` was declared but not resolvable through the available local read tool; axes were taken from the assignment text.
Executed: nothing. No case, selftest, or CLI was invoked. Everything below is **policy expectation derived from source**, not observed runtime output.

## Axes

- correctness of expected finding ID and exit code
- ambiguity of "wrong exact SHA256" (which surface is wrong)
- blind spots where a wrong digest is present but not detected
- independence from the existing selftest

## Smallest literal fixture (evaluate(raw, read_bytes) level)

The source is the empty byte string, so the correct digest is the well-known SHA-256 of empty input and no hash computation is needed. The report receipt carries 64 zeros as the wrong digest. All fixture text is JSON-escaped so that no receipt-prefixed line appears at column 0 of this report.

Fixture A (wrong digest in report receipt; matches selftest case `report-digest`):

    {
      "manifest": {"schema": "tsukuroi-review-snapshots-v1", "reviews": [
        {"name": "A", "report": "r", "source": "s",
         "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
         "predicate": "p"}]},
      "files": {
        "s": "",
        "r": "Reviewed-SHA256: 0000000000000000000000000000000000000000000000000000000000000000\nPredicate: p\nScope: executed=none\n"}
    }

Fixture B (wrong digest in manifest, report agrees with manifest; source-side path, line 90):

    same as A, but manifest "sha256" = "0"*64 and report "r" unchanged (zeros).

## Policy expectation (both fixtures)

- exit code `1`, `status` `"FAIL"`
- `findings` = `[{"id": "REVIEW-SNAPSHOT-MISMATCH", "site": "A"}]` — exactly one entry
- `total_reviews` 1, `pinned_reviews` 0, `distinct_source_files` 1

Derivation: schema/identity checks pass (`name` matches the regex, `r`/`s` are safe paths, sha is 64 lowercase hex, predicate non-blank). Fixture A: source digest equals the manifest (line 90 silent); `digest_lines` = the zeros line, which is not equal to `["Reviewed-SHA256: e3b0…b855"]` → one mismatch (line 113–114). Predicate and scope lines match. Fixture B: `sha256(b"")` ≠ zeros → mismatch at line 90; report line equals `"Reviewed-SHA256: " + zeros` → silent.

## Ambiguity attacks on the expectation

1. **Duplicate ID, same site.** If manifest sha is wrong and the report carries the true source digest, both line 90 and line 113 fire: two identical `{"id":"REVIEW-SNAPSHOT-MISMATCH","site":"A"}` entries. The selftest compares `set` of IDs and ignores site and multiplicity, so "exactly one finding" is not tested anywhere. An oracle MUST state whether it asserts the ID set or the findings list.
2. **One ID, three causes.** `REVIEW-SNAPSHOT-MISMATCH` is emitted for source-digest mismatch, missing source (`source is None`, line 90), and report receipt mismatch/absence/duplication. The finding cannot distinguish "wrong digest" from "source blob absent" or "no receipt line"; site is only the row name.
3. **Malformed "wrong" digest is not a mismatch.** A manifest sha that is uppercase, 63/65 chars, or non-hex raises `ValueError` → `REVIEW-MANIFEST-SCHEMA`, exit `2`, `CANNOT_EVALUATE`. "Wrong SHA256" yields the expected outcome only for well-formed 64-lowercase-hex values. In the report line, by contrast, uppercase or any malformed digest is a plain string mismatch → exit 1.
4. **Exit code can be overridden.** The same mismatch with an undecodable report (`REVIEW-REPORT-ENCODING`) or a report read failure gives exit `2` / `CANNOT_EVALUATE` while still listing the mismatch (or, for a report read failure, skipping receipt checks via `continue`).
5. **Invisible wrong digest (strongest counterexample — undetected).** Only lines starting at column 0 with `Reviewed-SHA256:` are collected. A report holding a correct column-0 receipt line plus a wrong digest in a line prefixed by a space, `>`, a backtick, a list marker, a BOM, or a lowercase/Unicode-hyphen variant of the key yields exit `0` / PASS. Likewise, a correct line hidden behind such a prefix with no column-0 line yields a mismatch for "missing", not "wrong". Splitting happens only at LF, so a wrong digest after U+2028/VT/FF in the same physical line is also invisible (the selftest covers this for `Predicate:` only, not for the digest key).
6. **Whitespace edges.** One trailing CR is stripped (CRLF receipt passes); a trailing space, tab, or a second CR makes the correct digest a mismatch. A missing space after the colon is a mismatch.
7. **Independence.** Fixture A is the selftest's own `report-digest` case (selftest uses `"0"*64` replacement too), so it is not independent evidence. Fixture B is equivalent to selftest `source-tamper`. The uncovered behaviors are items 1, 3 (report side), 5, and 6.

## Impacted axes and smallest safe correction

- Correctness: unaffected for fixtures A/B — expectation REVIEW-SNAPSHOT-MISMATCH, exit 1 holds by source.
- Calibration: items 1–2 make the ID non-diagnostic; item 5 is a fixable defect if the policy intends "no wrong digest anywhere in the report", and a tradeoff (accepted blind spot) if it intends "exactly one column-0 receipt line".
- Smallest safe correction (for the owner, not applied): add selftest cases asserting the full findings list (ID+site+count) for the double-mismatch case, and decide/document whether near-miss digest keys (leading whitespace, case, BOM) should be flagged; if yes, collect lines whose `strip().casefold()` starts with `reviewed-sha256:` and require that set to equal the exact receipt.

## Policy expectation vs observed runtime

- Policy expectation: REVIEW-SNAPSHOT-MISMATCH, exit 1, status FAIL, one finding at site `A`.
- Observed runtime result: none — not invoked (NO-EXEC).

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclereceiptdigest
Scope: executed=none
