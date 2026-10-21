# C2 exec-log systemctl mutation review

Axes: C2 operability (supporting parser behavior); no direct C1 adjacency or C3 calibration effect. Source-only review; transcript commands were treated as inert data.

## Findings

### High — retained read capture is classified as a violation

The candidate allowlist at `tools/check-recheck-commands.py:272-274` omits `list-dependencies`, and `_systemctl_read_only` rejects any verb outside that set (`:323-326`). The final measurement caller explicitly checks the retained R19 captures as exec logs (`.ufo/waves/round-20/measure/run.py:95-98`); `host-capture-r19.txt:215` contains `$ systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service`. Therefore this existing read-only capture will produce `EXEC-STEER-VIOLATION` and make `exec-log-r19` red. Add this observed read verb and a clean fixture matching the captured form; do not weaken unknown-verb rejection or ban all `systemctl` calls.

## Finite expectations for the five scoped mutations

For inert `$ ...` fixture lines passed to `assess_exec_log`, each of the following must return FAIL with exactly `{EXEC-STEER-VIOLATION}` and `exec_violation_count=1`:

- `systemctl restart example.service`
- `sudo /usr/bin/systemctl enable example.service`
- `sh -c 'systemctl daemon-reload'`
- `systemctl --user kill example.service`
- `systemctl set-property example.service CPUWeight=100`

The candidate selftests at `tools/check-recheck-commands.py:1452-1460` cover the first three only. The classifier's fail-closed verb check appears to reject `kill` and `set-property`, but those two behaviors lack an explicit finite fixture; add them as positive mutation controls.

Negative controls should remain clean (PASS, no findings, `exec_violation_count=0`) for observed read forms such as `systemctl cat ...`, `systemctl show ...`, `systemctl list-timers --all`, and the captured `systemctl list-dependencies --reverse ...`. Preserve inert text such as `echo systemctl restart ...` as clean. The candidate has several read controls (`:1462-1477`) but does not include `cat` or the captured `list-dependencies` form. Its separate `--forbid systemctl` fixture intentionally rejects all systemctl invocations and should remain distinct from the default classifier (`:1478-1481`).

## Residual risk and verification gaps

The checks inspect bounded command text using the existing shell parser, not runtime enforcement or a universal shell interpreter; no transcript command was executed. No LSP device/server was exposed in the available tools, so references/definition/diagnostics could not be checked; cited behavior is from source and caller text, not LSP semantic proof. No tests or measurement were run under the NO-EXEC assignment. This review is limited to `restart`, `enable`, `daemon-reload`, `kill`, `set-property`, their read controls, and the concrete retained-capture compatibility issue above.

Scope: executed=none
