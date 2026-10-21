# SysctlUserReads — four user-scoped read controls

## Scope and confidence

Axes: exact read preservation, option-placement fidelity, and retained-command parity. This is static inspection of the inherited execscope candidate identified by `.ufo/waves/round-20/worktree-bindings.json:2-7`. Below, `candidate` means `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py` (observed read snapshot `E248`); lane paths are relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

Confidence is high for the observed source and fixture contents. Predictions below are source-level inferences, not executed results. No LSP device is exposed in this seat's permitted read/grep/glob/write-only tool set; definition/caller tracing therefore uses literal source inspection, not semantic-index proof.

## Observed fixture and allowlist evidence

All four requested controls are now present in `systemctl_reads["exec.log"]`:

| Candidate line | Exact inert command | Source-level expectation |
|---|---|---|
| 1480 | `$ systemctl --user cat example.service` | No systemctl policy hit |
| 1481 | `$ systemctl --user show example.service` | No systemctl policy hit |
| 1482 | `$ systemctl --user list-timers --all` | No systemctl policy hit |
| 1483 | `$ systemctl --user is-active example.service` | No systemctl policy hit |

The exact verb allowlist is `cat`, `show`, `status`, `list-units`, `list-unit-files`, `list-timers`, `list-dependencies`, `is-active`, `is-enabled`, and `is-system-running` (`candidate:276-278`). Thus all four requested spellings are explicitly represented; none depends on the no-verb default.

Option placement is handled without consuming the verb as a scope argument. `_systemctl_read_only` recognizes `--user`/`--system` in a dedicated branch, remembers scope, rejects conflicting scopes, and advances exactly one token (`candidate:289-303`). The next non-option token becomes the verb (`candidate:328-331`). For `list-timers --all`, `--all` belongs to `SYSTEMCTL_READ_FLAGS` (`candidate:279-282`); option processing remains enabled after the verb, so the trailing switch is recognized by `candidate:308-312`. The fixture places `--user` before each verb and `--all` after `list-timers`; these placements agree with the classifier's control flow. This does not establish runtime systemctl behavior.

The common test case declares `PASS`, an empty finding set, and `exec_violation_count=0` (`candidate:1489-1492`). Its helper checks exit/status, exact finding IDs, and requested count fields (`candidate:1018-1043`). Those are encoded expectations, not an observed passing run.

## Definition/caller trace and policy boundary

`simple_commands` tokenizes each segment, selects the command word, strips a path prefix, and passes the remaining arguments onward (`candidate:242-247`). `systemctl_violations` applies `_systemctl_read_only` only when that parsed command word is `systemctl` and appends a hit only on rejection (`candidate:334-345`). `assess_exec_log` inspects only lines starting with `$ `, combines generic forbidden-command hits with this classifier, and emits `EXEC-STEER-VIOLATION` only when a hit exists (`candidate:654-668`). The revision-mode caller reads the selected committed exec log before calling it (`candidate:857-864`).

The four predictions apply to the finite classifier under the default generic policy. `systemctl` is absent from `DEFAULT_FORBID` (`candidate:62`), but an explicit generic ban bypasses the read exception (`candidate:661-663`); the separate explicit-ban fixture deliberately expects violations (`candidate:1493-1496`). User scope is not a blanket exemption from verb classification.

## Captured-command parity and remaining limits

The four simple controls are not exact replicas of retained capture syntax:

- R19 has `cat UNIT --no-pager` and a two-unit `cat` (`.ufo/waves/round-19/l1-capture/host-capture-r19.txt:153,220`), repeated short `-p PROPERTY` options after `show UNIT` plus trailing `--no-pager` (`:208`), and `list-timers --all --no-pager "snapper*"` (`:262`). R18 likewise has repeated `-p` after `show` and a semicolon-chained `is-active`/`is-enabled` pair (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:16,20`).
- **[INFERENCE] These inspected spellings are supported by the current source:** `--no-pager` and `--all` are finite read flags; `-p` is a value-taking flag consuming one following non-option argument; the loop continues through operands and subsequent options (`candidate:279-285,308-331`). Quote removal preserves the timer pattern as an operand (`candidate:174-211`), and top-level semicolons split command segments (`candidate:164-171,242-247`). No unsupported token was identified in these cited forms.
- **Residual coverage risk:** the four requested fixtures alone do not pin repeated short-property options, multi-unit `cat`, trailing `--no-pager`, or a quoted timer pattern. Their zero-hit expectation therefore must not be presented as proof of exact capture parity. The R20 measurement source separately names R19/R19b/R19c exec-log checks (`.ufo/waves/round-20/measure/run.py:95-98`); that is check configuration, not a result, and it does not name the R18 capture.
- The earlier build report records missing user-scoped controls and missing `list-dependencies`/`--reverse` support (`.ufo/waves/round-20/build/ExecReadOnly.md:5-7`). Those specific omissions are absent from the inspected candidate: the four controls are at `candidate:1480-1483`, `list-dependencies` and `--reverse` are allowlisted at `:278,281`, and the exact retained R19 list-dependencies command is included at `:1484` (capture source `host-capture-r19.txt:215`). The earlier findings are not evidence that these omissions still exist in the current snapshot.

No commands, tests, builds, linters, formatters, host probes, or external requests were run; no tools were installed or updated. Shell equivalence, actual user-manager behavior, later candidate changes, and exercised capture results remain unestablished. No host or boot-safety conclusion follows; boot images remain UNKNOWN.

Scope: executed=none
