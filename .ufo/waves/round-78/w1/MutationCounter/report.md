# MutationCounter — Round 78 C1 actual CLI probe

Axes: depth and operability. Synthetic fixtures only; no actual seat evidence or outside verdict is claimed.

## Frozen detector and execution

Read SCORECARD Round 78 and before/expected.json. The actual CLI is `python3 tools/measure-journal-usage-r78.py --root <fixture>`: there is no literal `actual` subcommand.

Frozen claim commit: `07a607df1a5157daafc91bb5c26858af14415f43`. Its counter blob and the executed working-tree counter both SHA256 `cffc3e9d9c04cecd3f98810117cd92fe429261483308b58e3f539ca51de449f1`. At initial inspection HEAD equalled that commit. Source snapshots matched both expected pins before and after the probes.

Final runner exited 0. Twenty cases, two passes, each with the same detector run on pristine, mutated, and byte-restored fixtures: 120 actual CLI invocations. All 40 pristine and 40 restored invocations returned rc0/count6. All 40 mutated observations matched the expected rc/reason/count; both passes were identical. Every fixture restored exact file membership and SHA256 hashes. `matrix.json` records all outputs and before/mutated/restored per-file hashes.

## Observed mutation outputs

Every rejection below returned rc1/count0/met0; every acceptance returned rc0/count6/met1. Reason strings were identical across passes.

| Case | Reason | Probe verdict |
|---|---|---|
| Exact expected rows, synthetic review/results | finite-content-and-review | Positive control |
| Wholesale fabricated self-consistent review/results | finite-content-and-review | Survived: declared non-authentication limit |
| Wrong reviewer output digest string | result-digest | Killed |
| U1 `used` incremented by one | finite-content-mismatch | Killed |
| Source S327 replaced by S999 | finite-content-mismatch | Killed |
| Snapshot bytes replaced by `tampered` | snapshot-tampered | Killed |
| Missing review file | unreadable:FileNotFoundError | Killed |
| Wrong artifact digest | review-not-bound | Killed |
| U4 verdict `partly-holds` | review-not-bound | Killed |
| Missing results file | unreadable:FileNotFoundError | Killed |
| Reviewer role replaced by scribe | result-identity | Killed |
| Reviewer name replaced by ReviewUsage2 | result-identity | Killed |
| Digest final JSON-wrapped inside output string | finite-content-and-review | Accepted by explicit design |
| Output changed to JSON object instead of string | result-digest | Killed |
| Null output | result-digest | Killed |
| DATA whitespace-only change, stale review | review-not-bound | Killed |
| Same whitespace change, refreshed digest chain | finite-content-and-review | Positive recontrol |
| Duplicate DATA source key | unreadable:ValueError | Killed |
| Duplicate results lane key | unreadable:ValueError | Killed |
| Poisoned fixture-local expected.json | finite-content-and-review | Ignored by design; production expected remains authoritative |

Fourteen rejection mutants were killed; none were inconclusive. The forgery survives specifically as a provenance/authentication coverage finding, not permission to change the frozen contract. The JSON-wrapper and fixture-expected acceptances are intentional boundaries, not newly established defects.

## Depth findings and limits

- Binding covers raw DATA bytes, not only decoded JSON: adding a newline invalidated the review; refreshing both digest links re-passed.
- Duplicate keys fail even when their values agree, in both DATA and result bundle.
- JSON-wrapped final text passes because output is a string containing the digest token; a typed JSON object fails. This does not establish structured parsing or semantic review of final text.
- A fabricated report plus fabricated orchestrator bundle passes. This reproduces the explicit SCORECARD non-authentication limit; no real reviewer or orchestrator evidence was forged or modified.
- Missing-path reason taxonomy depends on the reader: actual filesystem `--root` returns `unreadable:FileNotFoundError`; source selftest uses a dictionary and expects `unreadable:KeyError`. The initial probe expectation incorrectly predicted OSError; actual outputs corrected that prediction, not the counter. Final receipts retain the corrected expectations.
- Fixture-local expected.json cannot retarget the detector: expected.json is loaded from the executable's production ROOT. No production expected/counter bytes were changed.
- This is bounded finite-fixture testing, not upstream semantics validation, authenticity proof, general mutation coverage, C2 registry testing, or claim admission.

## Reproduction and restoration

Durable artifacts in this directory: `runner.py`, `matrix.json`, this report. Recreate own scratch and run:

```sh
mkdir -p /fast/scratch/hyaku/tsukuroi-r78/MutationCounter
env TMPDIR=/fast/scratch/hyaku/tsukuroi-r78/MutationCounter PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-78/w1/MutationCounter/runner.py
rm -rf /fast/scratch/hyaku/tsukuroi-r78/MutationCounter
```

Synthetic baseline chain:
- DATA: `13fc82d4cd0756f05b997c7f7a8f64a6976c61aa34d601611a0c73a86a06bd1d`
- REVIEW: `1f97e601de625cbd13749d8d70a2545fe6c3d6ffda76e584467b30e052153453`
- RESULTS: `a966e942b5eb91b9845ac3a4b290edb0ca719720d82c1d85c7f93e39ee550429`

The runner restores pristine bytes in a finally block around each mutation detector invocation. Restoration hashes and restored detector outcomes are recorded in matrix.json. Production counter and snapshot hashes stayed unchanged. ReviewUsage independently landed its real verdict during this probe; it was never used as fixture evidence or modified. Existing tools pycache entries predated this probe; no pycache cleanup was performed. No registry checker/selftest, git mutation, host change, installs, clone, or production-data write was performed. Python 3.14.8 was already installed.
