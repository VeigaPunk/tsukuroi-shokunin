## Attack
Attack the shared revision binder and seat-scope selftest contract in a pristine clone. This is falsifiable if either selftest fails, any required typed refusal is missing from the binder fixtures, the annotated-`none` malformed scope fixture is absent, or a `__pycache__` directory appears after the runs.

## Method
Commands run:

```text
git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-selftest-revision-8 && git -C /tmp/tsukuroi-r19-selftest-revision-8 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116
python3 tools/_revision.py --selftest
python3 tools/check-seat-scope.py --selftest
git rev-parse HEAD && git status --short --untracked-files=all
```

Inspected the binder fixture code and refusal constants, the seat-scope annotated-`none` fixture and bytecode guard, and searched the clone for `**/__pycache__/` after both tests.

## Verdict
INCONCLUSIVE — C3 (registry-to-tools calibration). The requested binder and seat-scope selftests pass, but they do not run `check-registry-coverage.py` and therefore cannot establish C3. The bounded selftest assertions themselves are confirmed.

## Evidence
- Clone identity: `git rev-parse HEAD` printed `8e5916360f2dfe7bc4eb4ba144081af555900116`; `git status --short --untracked-files=all` printed no changes.
- Binder selftest: `REVISION_SELFTEST: PASS (39 cases, 39 passed, 0 failed)`; exit 0.
- Scope selftest: `CHECK_SEAT_SCOPE_SELFTEST: PASS (54 cases, 54 passed, 0 failed)`; exit 0.
- `/tmp/tsukuroi-r19-selftest-revision-8/tools/_revision.py:42-48` defines the five refusal IDs. Fixture expectations exercise revision-invalid at `:200-205`, landed-refusal at `:206`, branch-invalid at `:207-210`, branch-missing at `:211-215`, and not-pushed at `:219-225`.
- `/tmp/tsukuroi-r19-selftest-revision-8/tools/check-seat-scope.py:362-364` contains `annotated-none-with-command-not-verified-execution`, expected to fail with `SCOPE-TRAILER-MALFORMED`; line 35 sets `sys.dont_write_bytecode = True` before importing the shared module.
- The clone-wide `**/__pycache__/` search returned no matches after both selftests.

## Residual
This attack did not run the registry coverage gate or establish the broader C3 registry/tool counts. No production code or host state was changed; no tools were installed.

Scope: executed=git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r19-selftest-revision-8 && git -C /tmp/tsukuroi-r19-selftest-revision-8 checkout --detach 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 tools/_revision.py --selftest; python3 tools/check-seat-scope.py --selftest; git rev-parse HEAD && git status --short --untracked-files=all