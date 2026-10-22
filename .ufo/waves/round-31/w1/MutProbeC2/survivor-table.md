# Survivor table — mutants that change no outcome on base / H1 / H2

Outcome = (`leaking`, sorted `leaking_pairs`, `harness_errors`). Reference (pristine probe):
base `1` / `{loader-env}` / `[]`, H1 `1` / `{loader-env}` / `[]`, H2 `0` / `{}` / `[]`.
Where a (mutant, lane) pair was run more than once, the **majority** verdict is used; the
spurious dotgit-pointer reading is documented in §5 of the report.

| mutant | base | H1 | H2 | runs (b/H1/H2) | verdict |
|---|---|---|---|---|---|
| pristine | 1 loader-env | 1 loader-env | 0 | 8 / 25 / 38 | reference (never flaky) |
| M01 drop-parity-check | 1 loader-env | **0** | 0 | 1 / 1 / 1 | **killed** (H1) |
| M02 drop-stdout-comparison | 1 loader-env | 1 loader-env | 0 | 1 / 1 / 1 | **survivor** |
| M03 drop-git-exec-count | 1 loader-env | 1 loader-env | 0 | 1 / 1 / 1 | **survivor** |
| M04 skip-first-exec-exclusion | 1 loader-env | 1 loader-env (1 of 5 runs also dotgit-pointer — flake) | **1 loader-env** | 1 / 5 / 5 | **killed** (H2, 5/5) |
| M05 injection-by-variable-name | 1 loader-env | 1 loader-env | 0 | 1 / 1 / 1 | **survivor** |
| M06 no-LD_LIBRARY_PATH in injection | 1 loader-env | 1 loader-env | 0 | 1 / 1 / 1 | **survivor** |
| M07 no-PYTHONPATH in injection | 1 loader-env | 1 loader-env | 0 | 1 / 1 / 1 | **survivor** |
| M08 drop-control-B determinism | 1 loader-env | 1 loader-env | 0 (1 of 13 runs dotgit-pointer — flake) | 1 / 1 / 13 | **survivor** |
| M09 no-require-git-child | 1 loader-env | 1 loader-env | 0 | 1 / 1 / 1 | **survivor** |
| M10 drop stdout AND exec-count | 1 loader-env | **0** | 0 | 1 / 1 / 1 | **killed** (H1) |

**Killed: M01, M04, M10. Survivor: M02, M03, M05, M06, M07, M08, M09.**
