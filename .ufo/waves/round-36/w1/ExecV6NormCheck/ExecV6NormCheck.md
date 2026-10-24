# ExecV6NormCheck — normalization debt

## Outcome

Created four conformance fixtures, a small classifier/expected-form harness, class analysis, and a results record. The sibling r36 probe was absent at inspection, so no probe-normalizer test was possible. Dependency is recorded in `results.md`; fixtures and expected behavior are ready for wave-2 verification.

## Files changed

- `classes.md` — extracted observed false-positive classes, separated direct evidence from inferences, and documented expected canonicalization.
- `norm-fixtures.txt` — one `NAME=VALUE` fixture per class.
- `classify_norm_fixtures.py` — classifies fixtures and emits expected canonical forms; not an implementation of the probe normalizer.
- `results.md` — per-class outcomes and absent-probe dependency.
- `classifier-output.txt` — retained harness output.

## Exact retained evidence

- `byte-invariance.txt:3-18`: 16 tools are marked `UNCHANGED`, spanning both v6 target sets.
- `r33claim-v6.jsonl:17`: `targets=5`, `pairs=15`, `leaking=8`; the per-pair rows `:2-16` show these as `base-parity` only.
- `regression-v6.jsonl:35`: `targets=11`, `pairs=33`, `leaking=22`; `regression-clause-summary.txt:1-27` records the `GIT_CEILING_DIRECTORIES` any-name-value class and freshness's additional base-parity findings, while `:28-33` records the two owed-statements base-parity targets.
- The old normalizer recognizes only exact 40/64 lowercase-hex strings and only its known TMP component (`probe-child-env-allowlist-r34.py:192-194,379-385`). `check-adjacency-overlap.py:215-227` constructs `GIT_CEILING_DIRECTORIES` from the parent of its own temporary fixture directory.
- The frozen round-36 declaration explicitly names short hashes, fixture paths, and `GIT_CEILING_DIRECTORIES`/HOME-derived normalization as the debt to repay.

## Risks and blockers

- The v6 base-parity records retain only `git_argv_sha256`, not the argv strings, so short-hash, arbitrary fixture-component, and HOME-derived attributions are `[INFERENCE]` from the declaration and old normalizer; they cannot be assigned to individual pairs from these artifacts.
- The 18 regression any-name-value findings (with two overlapping base-parity pairs) name `GIT_CEILING_DIRECTORIES`; target code shows the value is intentional sandbox TMPDIR, not ambient configuration. The normalizer must be narrow: recognize exact run-private values without suppressing unrelated ceiling paths.
- The sibling probe is absent; per-class implementation pass/gap remains unknown until the probe lands and is run against these fixtures.
- No tools were installed or updated.

Report: `.ufo/waves/round-36/w1/ExecV6NormCheck`
