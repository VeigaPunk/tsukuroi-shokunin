# OracleCohortBiject — r22 independent oracle, source-only

Seat: OracleCohortBiject (leaf, NO-EXEC / NO-FETCH honored; no invocation, no network, no installs).
Target: `.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py` (278 lines, declared SHA-256 `b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8`; read in full via declared read path only; SHA equality was not recomputed — no execution permitted — identity is taken from the assignment and the tool's own receipt contract).

Godspeed axes: (1) verdict fidelity — derived exit/status/finding IDs vs the stated expectation; (2) fixture minimality; (3) ambiguity surface of the expectation; (4) scope discipline.

## 1. Case statement

Oracle case: "settlement silently omits failed seat." Stated expectation: the finite policy outcome is CANNOT_EVALUATE. This seat derives, from source only, the smallest literal fixture and the exact verdict + finding IDs the checker produces, and attacks where that expectation is underdetermined or false. The case was NOT invoked; every result below is source-derived, not observed.

## 2. Smallest literal fixture

Schema `tsukuroi-review-snapshots-v1` (check :66-68) requires: dict, exact schema string, non-empty `reviews` list; each row needs `name` matching `[A-Za-z0-9][A-Za-z0-9._-]{0,127}` (:70-72), relative safe `report`/`source` (:23-28), 64-lowercase-hex `sha256`, non-empty control-free `predicate` (:73-78). One row is minimal. The `sha256` constant below is the well-known digest of the empty byte string, so an empty source blob in the tree satisfies the snapshot byte check without any computed material:

```json
{"schema": "tsukuroi-review-snapshots-v1", "reviews": [
  {"name": "A", "report": "r.md", "source": "s.py",
   "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "predicate": "p"}]}
```

Surfaces (the tool's own selftest models these as a `read_bytes` callable, :153-165; in `main` the surface is `git_read` at :263-264, which returns `None` for a tree-absent path and raises `RuntimeError` for a present-but-unreadable one, :132-141):

- **World R (failed read — the intended "failed seat"):** `s.py` readable as empty bytes; reading `r.md` raises `RuntimeError`.
- **World A (absent seat):** `r.md` simply absent from the revision (`git_read` → `None`).
- **World E (undecodable report):** `r.md` present with bytes `b"\xff"`.
- **World S (shrunken settlement):** the failed seat is dropped from `reviews[]` entirely; only conformant seats remain.

## 3. Derived verdicts (source-traced, not executed)

evaluate() runs :58-128; the verdict selector is `("PASS", "FAIL", "CANNOT_EVALUATE")[code]` with `code = 2 if report_encoding_error or read_error else (1 if findings else 0)` (:122-124).

- **World R** → exit **2**, status **CANNOT_EVALUATE**. Trace: report read raises at :97-101 → finding `{"id": "REVIEW-READ-FAILED", "site": "A"}`, `read_error = True`, `continue` (this row is excluded from `pinned`, and its report-receipt checks are skipped). Payload: `{"status": "CANNOT_EVALUATE", "distinct_source_files": 1, "pinned_reviews": 0, "total_reviews": 1, "findings": [{"id": "REVIEW-READ-FAILED", "site": "A"}], "scope": "primary snapshot and predicate declarations only; ..."}`. `main()` additionally injects `revision`/`branch`/`branch_tip` (:265). **Matches the expectation.**
- **World A** → exit **1**, status **FAIL**, finding `REVIEW-REPORT-MISSING` at site `A` (:103-104). `read_error` stays false; the failure is evaluable, so the tool judges it, not defers it. **Expectation falsified here.**
- **World E** → exit **2**, CANNOT_EVALUATE, finding `REVIEW-REPORT-ENCODING` at site `A` (:106-108). Matches the expectation's *status* but with a different ID than World R.
- **World S** → exit **0**, status **PASS**. The checker validates only declared rows; it has no seat registry to diff against, so a partially shrunken manifest is clean. **Expectation maximally falsified: the omitted failed seat is invisible; the oracle says PASS, not CANNOT_EVALUATE.**
- Corollary: dropping *all* seats (`"reviews": []`) violates the non-empty-shape check → `REVIEW-MANIFEST-SCHEMA`, exit 2, CANNOT_EVALUATE (:66-70, :125-127). Total omission is CANNOT_EVALUATE; partial omission is PASS.

## 4. Ambiguity attack on the expectation

1. **"Failed seat" is three disjoint failure classes with two different verdicts.** Read-transport failure (OSError/RuntimeError/timeout, :84-88, :97-101) and undecodable report bytes → CANNOT_EVALUATE (exit 2). Absent report, byte/predicate/scope-line mismatch, or snapshot digest mismatch (:103-121) → FAIL (exit 1). The blanket expectation "failed seat ⇒ CANNOT_EVALUATE" is true only for the unreadable/undecodable classes.
2. **The verdict is not a function of the fixture JSON alone.** Identical JSON yields FAIL in World A and CANNOT_EVALUATE in World R; the outcome depends on tree state (present-but-unreadable vs absent). A fixture that states only the manifest underdetermines the expected verdict; the surface behavior must be part of the oracle spec.
3. **If "silently omits" means removal from the manifest (World S), this oracle cannot fire at all.** No cross-check exists between `reviews[]` and any seat registry; the only per-seat accounting is `total_reviews`/`pinned_reviews`/`findings` over declared rows. The expected CANNOT_EVALUATE implicitly requires the failed seat to remain *declared* and fail a read.
4. **Inside evaluate() there is no silent omission of a declared seat.** Every failure path adds a finding whose `site` is the seat name (:60-63 helper; all branches), and the `start`-length guard / `continue` (:84-101, :121) keep failed seats out of `pinned_reviews`. The selftest case `read-failed-retains-missing` (:212-217) pins that a read failure retains the other seat's `REVIEW-REPORT-MISSING` and zeroes `pinned_reviews`. So the "silent" in the case name cannot originate in this tool; it can only live in the settlement aggregation layer (`check-review-cohort.py`), which is outside this seat's read paths.
5. **Verdict-class inversion at the edges.** Manifest file absent from the tree → FAIL (exit 1, `REVIEW-MANIFEST-MISSING`, :62-64); manifest unreadable → CANNOT_EVALUATE (exit 2, `E-READ`, :269-271); manifest with zero seats → CANNOT_EVALUATE (schema). "Nothing declared" is deferral, "manifest missing" is judgment — the inverse of the naive reading of the expectation.
6. **Secondary ID split for the same failure.** If instead the *source* read fails (:84-88), the finding is the same `REVIEW-READ-FAILED` but the `continue` also skips the report check, so any coexisting report defect of that seat is unreported. One finding per seat-max in that path; exact-ID prediction must name which surface failed.
7. **Schema-level CANNOT_EVALUATE is reachable from seat content too.** A control character in `predicate` or `report` (selftest cases `control-predicate`, `control-path`, :224-231) or a duplicate JSON key (:237-243) → `REVIEW-MANIFEST-SCHEMA`, exit 2. If the settlement's "failed seat" is expressed as a malformed row, the expected verdict holds but the exact ID is `REVIEW-MANIFEST-SCHEMA` with a truncated message as `site`, not `REVIEW-READ-FAILED`.

## 5. Policy expectation vs observed runtime result

- **Policy expectation** (assignment): failed seat in settlement ⇒ CANNOT_EVALUATE. As derived above this holds for World R (and E, and schema-violating rows) and fails for World A and, decisively, World S.
- **Observed runtime result:** none. The seat forbids invocation (NO-EXEC; "DO NOT INVOKE THE CASE"); `Scope: executed=none` in the receipt is literal. Every verdict in §3 is a source trace of :55-128 and :246-277, not an observation. If main later runs the fixture through `--selftest`-style injection, the predicted payloads above are the falsifiable claims.

## 6. Residual risk and verification gaps

- `_revision` module (imported :18-19; `RevisionError.fid` used at :266-268) is not in this seat's read paths: the exact revision-error finding IDs (e.g. bad-revision vs bad-branch) are unverified.
- `check-review-cohort.py` / `settlement.json` semantics (the actual aggregator named in preregister C3) are outside the declared read paths; the claim that a settlement "silently omits" a failed seat is unverifiable here and is left as a gap for the seat that owns that file.
- The empty-string SHA-256 constant is cited from well-known prior knowledge; this seat could not recompute it without execution.
- Line cites use the declared snapshot copy; only byte-identity to the declared digest would make them authoritative for other copies.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortbiject
Scope: executed=none
