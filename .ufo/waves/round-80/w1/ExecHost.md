# Seat ExecHost — Round80 W1 — Restart policies for installed system units (read-only diagnosis)

- Execution class: **EXEC-AUTHORIZED**. Four directly assigned read-only host commands, all rc=0.
- Base 467a9b7891a5939dab8460ec6f591fbb16bd82e9; frozen 61ec89ec6e6f284b6fba2127721359e6931a5789.
- Axes: depth + operability. Leaf seat: no subagent dispatch, no git/jj mutation, no production edit, no restart, no sudo, no pacman, no logs/config/env/argv reads.
- Scratch `/fast/scratch/hyaku/tsukuroi-r80/ExecHost` was used for receipts, copied to the report directory, then deleted.
- Report outputs: `ExecHost/handoff.md`, `ExecHost/receipt-1-systemctl-failed.txt`, `ExecHost/receipt-2-systemctl-user-failed.txt`, `ExecHost/receipt-3-systemctl-show-restart.txt`, `ExecHost/receipt-4-date-u.txt`.
- Installs/updates: none.

## Commands executed (exact)
| # | Command | rc |
|---|---|---|
| 1 | `systemctl --failed --no-pager` | 0 |
| 2 | `systemctl --user --failed --no-pager` | 0 |
| 3 | `systemctl show systemd-journald.service dbus.service -p Id -p ActiveState -p Result -p Restart -p NRestarts -p RestartUSec -p StartLimitBurst -p StartLimitIntervalUSec --no-pager` | 0 |
| 4 | `date -u` | 0 |

Also observed: `mkdir -p /fast/scratch/hyaku/tsukuroi-r80/ExecHost` (scratch creation, rc=0; not a host-state change).

## Findings
- System bus failed units: 0.
- User bus failed units: 2 transient `.scope` units (`systemd-run` wrappers around a background image CLI; argv not reproduced here). Scope units are not `.service` units; the six-cause `.service` matrix does not directly apply.
- journald: `Restart=always`, `RestartUSec=0`, `NRestarts=0`, `StartLimitBurst=5`/`10s`, active, Result=success.
- dbus (resolves to `dbus-broker.service`): `Restart=no`, `RestartUSec=100ms`, `NRestarts=0`, same limits, active, Result=success.
- Matrix comparison (frozen `before/expected.json`): `always` → true in all six cause classes; `no` → false in all six. Actual automatic restart additionally depends on overrides (not inspected) and the rate limit; not concluded here.
- Cause of the user-scope failures: **not determined**, by design.

## Verification boundary
- Corroboration only: the four receipts. Binding files remain authoritative.
- No restart, no fault injection, no drop-in/config inspection, no log reads. `[INFERENCE]` labels in the handoff mark non-observed semantics.

Scope: executed=`systemctl --failed --no-pager`; `systemctl --user --failed --no-pager`; `systemctl show systemd-journald.service dbus.service -p Id -p ActiveState -p Result -p Restart -p NRestarts -p RestartUSec -p StartLimitBurst -p StartLimitIntervalUSec --no-pager`; `date -u`; plus scratch `mkdir -p /fast/scratch/hyaku/tsukuroi-r80/ExecHost`
