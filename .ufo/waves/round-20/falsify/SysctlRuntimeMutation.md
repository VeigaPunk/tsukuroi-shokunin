# `systemctl --runtime restart show` — runtime mutation finding

## Observed source

In the inspected candidate `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py`, `--runtime` is a member of `SYSTEMCTL_READ_FLAGS` (lines 279–282) and is absent from `SYSTEMCTL_VALUE_FLAGS` (lines 283–285). `_systemctl_read_only()` advances only past `--runtime` when it is a read flag without `=` (lines 308–312); the next token therefore remains the candidate verb. It assigns the first non-option token to `verb` (lines 328–331) and accepts only `SYSTEMCTL_READ_VERBS` (lines 276–278).

For argv `systemctl --runtime restart show`, the parser skips `--runtime`, assigns `restart` as the verb, and does not replace it with `show`. Since `restart` is outside the finite read-verb allowlist, `_systemctl_read_only()` returns false; `systemctl_violations()` records the command (lines 334–345). `assess_exec_log()` converts that hit to `EXEC-STEER-VIOLATION` (lines 654–668).

The candidate selftest contains this exact command as a negative fixture at line 1505 and expects the combined ambiguous/effectful fixture to fail with `EXEC-STEER-VIOLATION` and `exec_violation_count=9` at lines 1509–1513. **Exact expected result for this command in isolation:** one `EXEC-STEER-VIOLATION` hit (`exec_violation_count=1`). The combined fixture expectation is 9 because it contains nine negative command lines; no test was run here.

## Artifact discrepancy

The lane review `.ufo/waves/round-20/build/ExecOptions.md:3–5,9` describes an earlier/different candidate state in which `--runtime` was in the value-taking set and recommends adding this negative control. That description does not match the inspected candidate source: the current source puts `--runtime` in the no-argument read-flag set and already includes the negative fixture above. This finding is therefore **no reproducing parser loophole in the inspected candidate snapshot**; the historical review artifact should not be treated as evidence that the current source still consumes `restart` as a value.

## Limits

Static source inspection only; no selftest, command, or runtime behavior was exercised. No LSP device was available in the assigned tool set, so no LSP semantic references were queried. The existing review artifact records the systemctl(1) `--runtime` switch semantics at `.ufo/waves/round-20/build/ExecOptions.md:5`.

Scope: executed=none
