source: S266 S267 (rows in `corpus/SOURCES.md`; both opened 2026-11-01) plus the dated host captures under `.ufo/waves/round-56/services-probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d — re-run the probe commands of rows T13-T16 (all read-only or absence-refused), compare the observed signatures with the receipts in `.ufo/waves/round-56/services-probes/`; re-open S266 on its 180d refresh class and S267 on upstream content change (S267 is an archived page — archive-side edits are the drift risk, `is_archived: true`); a changed row gets an appended correction, never an in-place edit
recheck: 30d from day 0 2026-11-01 (the r56 first executable pass, receipt `.ufo/waves/round-56/receipts/recheck-services-t1t12.txt`: rows=12 matched=12 drift=0; this note's rows T13-T16 re-check against `.ufo/waves/round-56/services-probes/` on the same cadence; instrument `tools/recheck-services-r56.sh [--receipt PATH] [--raw-dir DIR]` covers T1-T12, T13-T16 stay receipt-compared) — next pass due 2026-11-30; a late pass is observable from this line (operative; appended r57, supersedes the cadence-only line above, which stays)

# The Windows services plane, configuration-change and failure-action surface (round 56)

Scope: the same host-operability province as `windows-services-plane-r54.md` (T1-T8, `schtasks`
and `sc query`) and `windows-services-plane-r55.md` (T9-T12, `sc queryex`/`sc qc`); this note
extends the plane with the CONFIGURATION-CHANGE (`sc config`) and FAILURE-ACTION (`sc failure`,
`sc qfailure`) surfaces. Every probe here is read-only or absence-refused: the nonexistent-service
forms fail at `[SC] OpenService FAILED 1060:` BEFORE any value could be written, so the surface
can be probed with zero mutation risk; an actual config/failure change on a live service is
operator-owned and none was executed. All probes ran through the `receipt-run` instrument (each
receipt carries its own rc/argv metadata). Spelled for Git Bash: `MSYS_NO_PATHCONV=1` inside the
receipt's bash -c command string (r54 T1's class).

| id | question | probe (read-only or absence-refused, 2026-11-01) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| T13 | What does `sc config`/`sc failure <svc>` do with a service name but NO options? | `MSYS_NO_PATHCONV=1 sc config No-Such-Service-r56probe`; `MSYS_NO_PATHCONV=1 sc failure wuauserv` | (n/a — the usage gate is the finding) | Neither reaches the service: both print the command's USAGE block and exit rc **103** (`t13-config-usage-gate.txt`, `t14-failure-usage-gate.txt`, `t18-failure-bare-wuauserv.txt`) — option-validation precedes OpenService, so absence is not yet refused at this stage. The usage text confirms the equal-sign/space rule ("The option name includes the equal sign. A space is required between the equal sign and the value") and, for config, the start= domain `boot|system|auto|demand|disabled|delayed-auto` — matching S266's six values; the tool's usage also lists type= `userown|usershare`, which S266's page does not (doc-vs-tool gap recorded) | Never read a usage dump (rc 103) as a service failure — it means an option was missing, before the service name was ever validated; spell `qfailure` for the failure query (T16) | S266 (start= domain, option rules) + dated captures |
| T14 | Can the config surface be probed without mutation risk? | `MSYS_NO_PATHCONV=1 sc config No-Such-Service-r56probe start= demand` | rc 0 plus the changed-start block for an existing name | The change is REFUSED BY ABSENCE before any write: `[SC] OpenService FAILED 1060:` + "The specified service does not exist as an installed service." and process rc **36** (`t15-config-nonexistent-start.txt`) — the same 1060/rc-36 family as query (T5) and qc (T12), function line plain `OpenService` (like qc's, without query's `EnumQueryServicesStatus:` prefix) | Probe name-validity of the config surface with the nonexistent-service form; a real `sc config` change on a live service is operator-owned (RP4/RP5 class) | S266 (option contract) + dated capture |
| T15 | Same question for the failure-action surface, and what is its option contract? | `MSYS_NO_PATHCONV=1 sc failure No-Such-Service-r56probe reset= 30 actions= restart/5000` | rc 0 plus the new failure actions for an existing name | Also refused by absence: `[SC] OpenService FAILED 1060:` + rc **36** (`t16-failure-nonexistent-actions.txt`). S267's contract, confirmed by the tool's usage text: actions= takes up to three slash-separated actions (valid: `run`, `restart`, `reboot`; delays in milliseconds) and MUST be used with reset=; reboot= broadcasts a message; command= runs a command on failure | Recovery actions on a live service are operator-owned (a wrong actions= row can reboot the host); probe with the absence-refused form only | S267 (actions=/reset= contract) + dated capture |
| T16 | How is the failure configuration QUERIED on this build? | `MSYS_NO_PATHCONV=1 sc qfailure wuauserv`; bare `MSYS_NO_PATHCONV=1 sc failure wuauserv` | `sc qfailure <svc>` → rc 0, `[SC] QueryServiceConfig2 SUCCESS`, block: RESET_PERIOD (in seconds), REBOOT_MESSAGE, COMMAND_LINE, FAILURE_ACTIONS (`t17-qfailure-wuauserv.txt`; wuauserv measured: RESET_PERIOD 86400, FAILURE_ACTIONS `RESTART -- Delay = 60000 milliseconds.` — the host's own recovery config) | Two signatures: (a) bare `sc failure <svc>` does NOT query on this build — it prints the usage block at rc 103 (T13 class; `t18-failure-bare-wuauserv.txt`), so the query MUST be spelled `qfailure`; (b) S267's archived page documents SET semantics only — no query form — and the tool agrees (doc family and tool consistent; the query behavior is measured here, not documented) | Read a service's recovery config with `qfailure` (never bare `failure`); a recovery change stays operator-owned | S267 (set-only syntax) + dated captures |

## Limits

All field values are captures of 2026-11-01 and drift with the host (wuauserv's failure actions
are the host's current recovery configuration and may be changed by its owner; RESET_PERIOD and
delay values are drift-class). T14/T15's rc-36 arithmetic stays labeled inference (1060 mod 256),
as in T5/T10/T12. S266 is the CURRENT reference (180d refresh class); S267 is an ARCHIVED page
(`is_archived: true`, `ms.date` 2016-08-31, archive commit `5327995a…`) — the current Windows
Server commands reference carries no sc-failure page at all (404 checked 2026-11-01), so the
failure-action documentation exists only in the 2012-R2 archive, the same doc family as S263/S264.
No config or failure value was changed on any service; every mutation-class form stays
operator-owned. This note absorbs no sibling scope.
