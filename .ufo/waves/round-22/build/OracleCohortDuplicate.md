# OracleCohortDuplicate — source-only oracle (round 22)

Target: `.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py` (declared SHA-256 b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8; I did not recompute the digest because this seat is NO-EXEC).
Inputs read: the target, `.ufo/waves/round-22/preregister.json`, `.ufo/waves/round-22/sources/host-tool-boundary.json`. The godspeed skill text came inline in the assignment. Nothing else was read, and nothing was executed or fetched.

## Verdict

The policy expectation holds: a duplicated review/settlement seat row yields **CANNOT_EVALUATE**, exit code **2**, with exactly one finding, **REVIEW-MANIFEST-SCHEMA**. This is derived from reading the source only. **Observed runtime result: none.** The case was not invoked.

## Smallest literal fixture (canonical form: two identical rows)

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","report":"r","source":"s","sha256":"0000000000000000000000000000000000000000000000000000000000000000","predicate":"p"},{"name":"A","report":"r","source":"s","sha256":"0000000000000000000000000000000000000000000000000000000000000000","predicate":"p"}]}
```

The checker needs no source or report files for this case. `read_bytes` is never called, because the validation loop raises before the reading loop starts. So the sha256 can be any 64-character lowercase hex value.

## Expected `evaluate()` payload (derived, not observed)

```json
{"status":"CANNOT_EVALUATE","distinct_source_files":0,"pinned_reviews":0,"total_reviews":2,"findings":[{"id":"REVIEW-MANIFEST-SCHEMA","site":"invalid/duplicate review identity, path, or predicate"}],"scope":"primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution"}
```

How the code gets there:
- Row 1 passes every check, and `names` and `reports` record its name and report path.
- Row 2 fails at `row["name"] in names`. That raises `ValueError("invalid/duplicate review identity, path, or predicate")`.
- The `except (ValueError, TypeError, UnicodeError)` handler adds the finding with `site=str(exc)[:100]`. The message is 54 characters, so it is not truncated. It then sets `code = 2`.
- `total` is assigned before the loop runs, so `total_reviews` is 2.
- `distinct` is assigned after the loop, so it stays 0. `pinned_reviews` is 0.

Through `main --revision` the same payload comes out with `revision`, `branch` and `branch_tip` added, printed with `sort_keys=True`, exit 2. This assumes `_revision.bind` and `git_read` of the manifest both succeed; I did not inspect `_revision`. If either fails first, the result is still CANNOT_EVALUATE but the finding ID is `exc.fid` or `E-READ`. The in-tree selftest case `duplicate`, which appends a copy of `reviews[0]`, asserts the same exit code and ID set.

## Problems with the expectation

1. **The verdict cannot tell a duplicate seat from a malformed row.** An even smaller second row, `{"name":"A"}`, hits the same short-circuit and produces the same ID and site. A second row with a bad sha256 also produces the same ID and site. The finding proves "row rejected", not "duplicate". Impacted axis: calibration. Smallest fix: give the duplicate-name and duplicate-report checks their own `ValueError` message, and have the oracle assert on that site.
2. **A different kind of duplicate gives a different verdict.** Duplicate JSON keys raise inside `json.loads` (the `unique_object` hook). That also yields REVIEW-MANIFEST-SCHEMA and CANNOT_EVALUATE, but with `total_reviews=0` and the site `duplicate JSON key '…'`. An expectation of just "CANNOT_EVALUATE / REVIEW-MANIFEST-SCHEMA" accepts both cases. It should also pin `total_reviews` and the site.
3. **Duplicates inside one report are FAIL, not CANNOT_EVALUATE.** A second `Reviewed-SHA256:` line gives REVIEW-SNAPSHOT-MISMATCH. A second `Predicate:` line gives REVIEW-PREDICATE-MISMATCH. A second `Scope:` line gives REVIEW-SCOPE-MISMATCH. All are exit 1, FAIL. If "duplicate settlement seat" means a seat that delivered twice into the same report, the expected CANNOT_EVALUATE is wrong.
4. **A seat duplicated under another name is not detected (strongest counterexample).** Seat identity is only the `name` string and the `report` path. Two rows such as `{"name":"A","report":"r",…}` and `{"name":"a","report":"r2",…}` can pass with the same source, sha256 and predicate. Names are compared case-sensitively, and source duplication is only counted in `distinct_source_files`, never rejected. Each row's report then reaches PASS on its own trailer. This is a detection gap for C3 cohort accounting ("every declared seat"), not a fault in this oracle. Smallest fix: reject names that collide after case-folding, and leave the rest to `check-review-cohort.py`. I could not review that tool because it is not in this seat's read_paths.
5. **The preregistered claim belongs to a different tool.** C3 names `tools/check-review-cohort.py --settlement`, not this file, and this file's `DEFAULT` manifest still points at round-21. This oracle therefore only covers the review-snapshot duplicate path. The settlement-level duplicate seat in the cohort tool still needs its own oracle. Impacted axes: calibration and freshness.

None of these points invalidate the expected outcome for the canonical fixture. Points 1, 2 and 4 are fixable precision defects. Point 3 is a definitional ambiguity the canonical judge should settle explicitly. No runtime enforcement is claimed: per host-tool-boundary.json there is no native per-seat allowlist.

Tool installs or updates: none.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclecohortduplicate
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
