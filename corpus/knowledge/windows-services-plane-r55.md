source: S263 S264 S265 (rows in `corpus/SOURCES.md`; S263/S264 opened 2026-10-31, S265 is the same-day correction note on S262) plus the dated host captures under `.ufo/waves/round-55/services-probes/` of this repo
verified-at: 2026-10-31 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-10-31 via `tools/receipt-run.py`, read-only)
recheck: 30d — re-run the probe commands of rows T9-T12 (all read-only), compare the observed signatures with the receipts in `.ufo/waves/round-55/services-probes/`; re-open S263/S264 on upstream content change (both pages carry `is_archived: true` — archive-side edits are the drift risk); a changed row gets an appended correction, never an in-place edit
recheck: 30d from day 0 2026-11-01 (the r56 first executable pass, receipt `.ufo/waves/round-56/receipts/recheck-services-t1t12.txt`: rows=12 matched=12 drift=0; instrument `tools/recheck-services-r56.sh [--receipt PATH] [--raw-dir DIR]`) — next pass due 2026-11-30; a late pass is observable from this line (operative; appended r57, supersedes the cadence-only line above, which stays)

# The Windows services plane, extended query and config surface (round 55)

Scope: the same host-operability province as `windows-services-plane-r54.md` (rows T1-T8 cover
`schtasks` and `sc query`); this note extends the plane with the service-control EXTENDED query
(`sc queryex`) and CONFIGURATION query (`sc qc`) surfaces, each probed through the round-54
`receipt-run` instrument so every capture carries its own rc/argv metadata (the r54 routed-defect-2
rule, applied to new probes from the start). Detection and report only — starting, stopping,
changing or deleting any service stays operator-owned and none was executed. All probes are
read-only and spelled for Git Bash: the receipt's `command=` line records the exact inner bash
command including the `MSYS_NO_PATHCONV=1` prefix (T1 of the r54 plane is why it is needed).

| id | question | probe (read-only, 2026-10-31) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| T9 | What does `sc queryex` add to `sc query`? | `MSYS_NO_PATHCONV=1 sc queryex wuauserv` | rc 0; the r54 T4 field set (SERVICE_NAME, TYPE, STATE, WIN32_EXIT_CODE, SERVICE_EXIT_CODE, CHECKPOINT, WAIT_HINT) PLUS `PID` and `FLAGS`, and a wait-hint states line under STATE (`(STOPPABLE, NOT_PAUSABLE, ACCEPTS_PRESHUTDOWN)`) — S263's Remarks field list matches the measured output for every name EXCEPT the exit-code names (see the S263/S265 typo note: the page reads "WIN32_EXIT_B, SERVICE_EXIT_B"; the tool prints `WIN32_EXIT_CODE` / `SERVICE_EXIT_CODE`, receipts `t9-queryex-wuauserv.txt`) | same failure class as `sc query`: nonexistent service → `[SC] EnumQueryServicesStatus:OpenService FAILED 1060:` + process rc **36** (`t10-queryex-nonexistent.txt`; 1060 mod 256 = 36, [inference] as in r54 T5) | Use queryex (not query) when a probe needs the hosting PID (e.g. to pair with tasklist before any operator-owned stop); match the `FAILED 1060` line, never rc alone | S263 + dated capture |
| T10 | Does queryex's nonexistent-service signature match query's? | `MSYS_NO_PATHCONV=1 sc queryex No-Such-Service-r55probe` | rc 0 plus the extended service block | Identical text class and rc to r54 T5: `FAILED 1060` + "The specified service does not exist as an installed service." rc 36 (`t10-queryex-nonexistent.txt`) | Same handling as r54 T5: absence is a probe result; key on the 1060 line | dated capture; S263 (equal-sign/space Remarks) |
| T11 | What does `sc qc` return, and does it match the page's field list? | `MSYS_NO_PATHCONV=1 sc qc wuauserv` | rc 0 with `[SC] QueryServiceConfig SUCCESS` and the configuration block: TYPE `20 WIN32_SHARE_PROCESS`, START_TYPE `3 DEMAND_START`, ERROR_CONTROL `1 NORMAL`, BINARY_PATH_NAME `C:\WINDOWS\system32\svchost.exe -k netsvcs -p`, LOAD_ORDER_GROUP, TAG, DISPLAY_NAME `Windows Update`, DEPENDENCIES `rpcss`, SERVICE_START_NAME `LocalSystem` (`t11-qc-wuauserv.txt`) | Two named doc-vs-host facts: (a) S264's Remarks field list OMITS `START_TYPE`, which the measured output displays right after TYPE — the list is incomplete, not the tool wrong; (b) the SAME service's TYPE reads `30 WIN32` under query/queryex (r54 T6 Spooler: `110 … (interactive)`) but `20 WIN32_SHARE_PROCESS` under qc — the two displays code TYPE differently, so a parser must not compare TYPE across the two commands | Read START_TYPE/BINARY_PATH_NAME from qc (it is the only one of the three probes that shows the binary path); never diff TYPE values between query and qc displays | S264 + dated capture |
| T12 | What does `sc qc` return for a nonexistent service? | `MSYS_NO_PATHCONV=1 sc qc No-Such-Service-r55probe` | rc 0 plus the config block | Same 1060 family, DIFFERENT function line: `[SC] OpenService FAILED 1060:` (qc) vs `[SC] EnumQueryServicesStatus:OpenService FAILED 1060:` (query/queryex), same rc 36 (`t12-qc-nonexistent.txt`) | Key the parser on the `FAILED 1060` suffix, not the full line: the function name differs per subcommand while the win32 code and rc match | dated capture |

## Limits

All counts and field values are captures of 2026-10-31 and drift with the host (PID values change
every boot; service state came and went since r54 — wuauserv measured `1 STOPPED` on 2026-10-31 in
`.ufo/waves/round-54/after/services-probes/t4-wuauserv-stopped.txt` and `4 RUNNING` in this round's
`t4-wuauserv-state.txt` re-derivation, same day-class drift the r54 plane names). S263/S264 are
ARCHIVED Microsoft pages (`is_archived: true`, `ms.date` 2016-08-31, archive commit
`5327995a…`): the current Windows Server commands reference carries only `sc config`, `sc create`,
`sc delete` and `sc query` (TOC checked 2026-10-31), so queryex/qc documentation exists only in the
2012-R2 archive — treated as the same doc family as S262 (S263 shares its `WIN32_EXIT_B`
exit-code-name typo; S264's field list omits START_TYPE). The 1060→rc 36 truncation arithmetic is
labeled inference, as in r54 T5. This note absorbs no sibling scope; repair of any service state
stays operator-owned (r54 plane RP4/RP5 still stand).
