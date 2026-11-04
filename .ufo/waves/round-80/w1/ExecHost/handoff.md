# Handoff — Restart policies of installed system units, read-only (Round80 W1, seat ExecHost)

Execution class: EXEC-AUTHORIZED. Exactly four host commands were run; nothing was restarted, no unit state was mutated, no logs, unit files, drop-ins, environment, or argv were read. Claims below are either observed in the four receipts or are marked `[INFERENCE]`.

## Trigger
An operator asks, without restarting anything: "What restart policy are the two core services running with, and is anything currently failed on the system or user bus?"

## Checks (all rc=0)
1. `systemctl --failed --no-pager`
2. `systemctl --user --failed --no-pager`
3. `systemctl show systemd-journald.service dbus.service -p Id -p ActiveState -p Result -p Restart -p NRestarts -p RestartUSec -p StartLimitBurst -p StartLimitIntervalUSec --no-pager`
4. `date -u` → `Wed Nov  4 08:13:46 PM UTC 2026`

## Outcome
- System bus: **0 failed units** (observed).
- User bus: **2 failed units** (observed), both transient `[systemd-run]` `.scope` units from a background image-matting CLI invocation (argv and paths sanitized here). LOAD=loaded, ACTIVE=failed, SUB=failed.
- Restart policy as reported by the manager (observed; effective state, no config read):

| Property | systemd-journald.service | dbus-broker.service (queried as `dbus.service`, alias) |
|---|---|---|
| ActiveState | active | active |
| Result | success | success |
| Restart | always | no |
| RestartUSec | 0 | 100ms |
| NRestarts | 0 | 0 |
| StartLimitBurst | 5 | 5 |
| StartLimitIntervalUSec | 10s | 10s |

- Comparison against the six Restart= cause classes in the frozen expected matrix (`before/expected.json`, systemd v262 `systemd.service.xml`, observed as a frozen artifact, not re-fetched this seat):
  - `Restart=always` (journald): the matrix marks restart **true for all six cause classes** (clean exit, unclean exit, unclean signal, timeout, watchdog, OOM). Whether journald actually restarts on a given failure additionally depends on overrides and the rate limit below; this seat did not check either.
  - `Restart=no` (dbus-broker): the matrix marks restart **false for all six cause classes**. `RestartUSec=100ms` is reported but `[INFERENCE]` has no effect while `Restart=no`.
  - Rate limit (both units, observed): `StartLimitBurst=5` within `StartLimitIntervalUSec=10s`. `[INFERENCE]` exhausting the limit prevents further automatic restarts and leaves the unit failed, regardless of the `Restart=` value.

## Operator boundary — what this table does NOT license
1. Do not infer **why** the two user scopes failed. The receipts show state, not cause. `[INFERENCE]` transient scope units are not `.service` units, so the six-cause `.service` matrix does not directly apply to them.
2. Do not predict **whether** journald or dbus-broker will restart on the next failure. Drop-in overrides were not inspected, and the rate limit can veto `Restart=always`.
3. `NRestarts=0` and `Result=success` are current counters and state, not evidence of historical reliability.
4. `dbus.service` resolves to `dbus-broker.service` (observed). Follow-up queries should target the real unit name, or they may be ambiguous.
5. The Restart= matrix documents policy semantics, not installed-build or live-restart behavior. This seat performed no restart, suppression, or fault-injection check.

Raw command outputs are retained verbatim as receipts beside this file (`receipt-1` … `receipt-4`).
