## Attack

Attack C3 (registry coverage) by checking whether the gate's selftest actually rejects missing, orphaned, and duplicate tool-row fixtures. These are falsifiable negative cases: a passing suite must assert a failing gate result and the expected finding ID for each malformed fixture.

## Method

- Cloned revision `8e5916360f2dfe7bc4eb4ba144081af555900116` to `/tmp/tsukuroi-r19-selftest-registry-fxexec-isolated-20261021` with `--no-hardlinks`, checked out that exact revision, and observed its `rev-parse HEAD` output as `8e5916360f2dfe7bc4eb4ba144081af555900116` with empty initial short status.
- Ran from that clone: `python3 tools/check-registry-coverage.py --selftest; rc=$?; printf 'exit=%s\n' "$rc"; exit "$rc"`.
- Afterward ran `git status --porcelain=v1 --untracked-files=all && git diff --exit-code && git diff --cached --exit-code && printf 'WORKTREE_AND_INDEX_CLEAN\n'`; it printed `WORKTREE_AND_INDEX_CLEAN`.
- Queried the clone for `**/__pycache__/` and `**/*.pyc`; the file search returned “No files found matching pattern.”

## Verdict

CONFIRM — C3. The selftest passed all 12 cases with exit 0, including its missing-row, orphan-row, and duplicate-row negative-fixture assertions. This confirms those fixtures are killed by the gate in an isolated scratch clone, without requiring the live working tree during the test.

## Evidence

- Gate output: `PASS (12 cases, 12 passed, 0 failed)` and `exit=0` from the isolated clone.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:403-415` sets `ROOT` to a temporary fixture repository before invoking the gate, so selftest cases use generated fixtures rather than the live lane.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:420-423`: fixture `missing-row` expects `FAIL` and `REGISTRY-ROW-MISSING`.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:431-436`: fixture `orphan-row` expects `FAIL` and both `REGISTRY-ROW-ORPHAN` and `REGISTRY-ROW-MISSING`.
- `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:425-429`: fixture `duplicate-row` expects `FAIL` and `REGISTRY-ROW-DUPLICATE`.
- The actual successful selftest stdout is aggregate-only: it does not print each fixture name or expected ID on pass. The fixture-to-ID mapping above is therefore evidenced by the source assertions, while the 12/12 output confirms those assertions passed.
- Final clone cleanliness: `WORKTREE_AND_INDEX_CLEAN`; no `__pycache__` directory or `.pyc` file was found.

## Residual

The gate's passing stdout does not expose per-fixture names or finding IDs; those are visible in the source assertions cited above, not in the runtime summary. No behavior outside the selftest fixtures was exercised.

Scope: executed=`git clone --quiet --shared --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-selftest-registry-fxexec-20261021 && git -C /tmp/tsukuroi-r19-selftest-registry-fxexec-20261021 checkout --quiet --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-selftest-registry-fxexec-20261021 rev-parse HEAD && git -C /tmp/tsukuroi-r19-selftest-registry-fxexec-20261021 status --short` ; `python3 tools/check-registry-coverage.py --selftest` ; `python3 tools/check-registry-coverage.py --selftest; rc=$?; printf 'exit=%s\n' "$rc"; exit "$rc"` ; `git status --porcelain=v1 --untracked-files=all && git diff --exit-code && git diff --cached --exit-code && printf 'WORKTREE_AND_INDEX_CLEAN\n'` ; `git clone --quiet --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-selftest-registry-fxexec-isolated-20261021 && git -C /tmp/tsukuroi-r19-selftest-registry-fxexec-isolated-20261021 checkout --quiet --detach 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /tmp/tsukuroi-r19-selftest-registry-fxexec-isolated-20261021 rev-parse HEAD && git -C /tmp/tsukuroi-r19-selftest-registry-fxexec-isolated-20261021 status --short` ; `python3 tools/check-registry-coverage.py --selftest; rc=$?; printf 'exit=%s\n' "$rc"; exit "$rc"` ; `git status --porcelain=v1 --untracked-files=all && git diff --exit-code && git diff --cached --exit-code && printf 'WORKTREE_AND_INDEX_CLEAN\n"`