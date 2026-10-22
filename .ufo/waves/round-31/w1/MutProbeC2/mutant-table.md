# Mutant results table — C2 frozen probe `tools/probe-git-child-env-r31.py`

Pristine probe sha256 `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0`.
Lane states: `base` = `8cff9e7cfb034b49c645d548801ac3185a827cb4` (unmodified
`tools/check-kernel-taint.py`), `H1` = hollow control (exits 0 when `LD_PRELOAD` is set),
`H2` = genuine control (drops `LD_`/`PYTHON` names from the git child env).

Outcome triple per lane state = (`leaking`, sorted `leaking_pairs`, `harness_errors`).
Reference (pristine): base `1`/`loader-env`/`[]`, H1 `1`/`loader-env`/`[]`, H2 `0`/`[]`/`[]`.

| mutant | base | H1 | H2 | killed? | note |
|---|---|---|---|---|---|
| M01 drop-parity-check | 1 loader-env | **0** | 0 | killed | H1 hollow reads clean: the parity comparison was the only detector of the hollow fix |
| M02 drop-stdout-comparison | 1 loader-env | 1 loader-env | 0 | **survivor** | stdout term is redundant with the git-exec-count term on all three lanes |
| M03 drop-git-exec-count | 1 loader-env | 1 loader-env | 0 | **survivor** | git-exec-count term is redundant with the stdout term on all three lanes |
| M04 skip-first-exec-exclusion | 1 loader-env | **2** (loader-env + dotgit-pointer) | **1** loader-env | killed | false positives on H1 and H2 |
| M05 injection-by-variable-name | 1 loader-env | 1 loader-env | 0 | **survivor** | same verdicts on all three lanes |
| M06 no-LD_LIBRARY_PATH in injection | 1 loader-env | 1 loader-env | 0 | **survivor** | LD_PRELOAD alone still carries the path |
| M07 no-PYTHONPATH in injection | 1 loader-env | 1 loader-env | 0 | **survivor** | LD_PRELOAD alone still carries the path |
| M08 drop-control-B-determinism-check | 1 loader-env | 1 loader-env | 1 dotgit-pointer | killed (flaky) | the H2 difference is a flake, see the report; on 8 rechecks M08-H2 read 0 |
| M09 no-require-git-child | 1 loader-env | 1 loader-env | 0 | **survivor** | the harness-error branch never fires for this target |
| M10 (supplementary) drop stdout AND exec count | 1 loader-env | **0** | 0 | killed | confirms stdout+exec-count are jointly needed for H1 |

## Exit codes

| mutant | base | H1 | H2 |
|---|---|---|---|
| pristine | 1 | 1 | 0 |
| M01 | 1 | 0 | 0 |
| M02 | 1 | 1 | 0 |
| M03 | 1 | 1 | 0 |
| M04 | 1 | 1 | 1 |
| M05 | 1 | 1 | 0 |
| M06 | 1 | 1 | 0 |
| M07 | 1 | 1 | 0 |
| M08 | 1 | 1 | 1 (flaky; 0 on 8 rechecks) |
| M09 | 1 | 1 | 0 |
| M10 | 1 | 0 | 0 |
