## Attack
Independently test whether the boot-writer selftest rejects an added, unclaimed event line and a writer signature mismatch, and whether its run leaves clone residue. These fixture checks are falsifiable from their expected failure codes/findings and the selftest result.

## Method
1. Cloned the lane into `/tmp/tsukuroi-r19-writers-selftest-fxexec-8`, detached at the target revision, and captured HEAD plus initial status.
2. Ran the requested selftest twice (the second invocation captured the exit code explicitly).
3. Captured final HEAD/status, listed `__pycache__` directories and leftover selftest fixture directories.

Exact commands:
```sh
git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-writers-selftest-fxexec-8 && git -C /tmp/tsukuroi-r19-writers-selftest-fxexec-8 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && printf 'HEAD=' && git -C /tmp/tsukuroi-r19-writers-selftest-fxexec-8 rev-parse HEAD && printf 'STATUS_BEFORE\n' && git -C /tmp/tsukuroi-r19-writers-selftest-fxexec-8 status --short --untracked-files=all
python3 tools/check-boot-writers.py --selftest
python3 tools/check-boot-writers.py --selftest; rc=$?; printf 'SELFTEST_EXIT=%s\n' "$rc"; exit "$rc"
printf 'HEAD_AFTER=' && git rev-parse HEAD && printf 'STATUS_AFTER\n' && git status --short --untracked-files=all && printf 'PYCACHE_DIRS\n' && find . -type d -name __pycache__ -print
find . -maxdepth 1 -type d -name 'check-boot-writers-*' -print
```

## Verdict
CONFIRM — C2 selftest behavior only. This confirms the two negative fixture cases are asserted and pass within the selftest; it does not independently validate the production 13-event attribution claim.

## Evidence
- The selftest has 11 fixtures (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:658-663`). Its helper requires the actual exit code and reported status to match the expected code, and requires the expected finding ID (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:681-690`).
- The added event fixture is checked as `FAIL` with `EVENT-UNATTRIBUTED` (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:700-702`). The wrong-signature fixture is checked as `FAIL` with `EVENT-SIGNATURE-MISMATCH` (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:717-720`). The selftest emits aggregate PASS only when no case failed and case accounting matches (`8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-boot-writers.py:742-750`).
- Initial clone output: `HEAD=8e5916360f2dfe7bc4eb4ba144081af555900116`; `STATUS_BEFORE` had no following paths.
- Both selftest runs printed exactly `PASS (11 cases, 11 passed, 0 failed)`. The exit-capturing run additionally printed `SELFTEST_EXIT=0`.
- Final clone output: `HEAD_AFTER=8e5916360f2dfe7bc4eb4ba144081af555900116`; `STATUS_AFTER` had no following paths; `PYCACHE_DIRS` had no following paths. The fixture-directory search also returned no output.

## Residual
The selftest verifies the fixtures and verifier behavior, not the correctness of the recorded boot captures or all 13 production writer attributions. No `--revision` production gate was run. Residue evidence is limited to unchanged Git status, no `__pycache__` directories, and no top-level selftest fixture directory in the clone.

Scope: executed=[git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-writers-selftest-fxexec-8 && git -C /tmp/tsukuroi-r19-writers-selftest-fxexec-8 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && printf 'HEAD=' && git -C /tmp/tsukuroi-r19-writers-selftest-fxexec-8 rev-parse HEAD && printf 'STATUS_BEFORE\n' && git -C /tmp/tsukuroi-r19-writers-selftest-fxexec-8 status --short --untracked-files=all]; [python3 tools/check-boot-writers.py --selftest]; [python3 tools/check-boot-writers.py --selftest; rc=$?; printf 'SELFTEST_EXIT=%s\n' "$rc"; exit "$rc"]; [printf 'HEAD_AFTER=' && git rev-parse HEAD && printf 'STATUS_AFTER\n' && git status --short --untracked-files=all && printf 'PYCACHE_DIRS\n' && find . -type d -name __pycache__ -print]; [find . -maxdepth 1 -type d -name 'check-boot-writers-*' -print]"