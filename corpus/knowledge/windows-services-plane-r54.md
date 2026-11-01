source: S261 S262 (rows in `corpus/SOURCES.md`, both opened 2026-10-31) plus the dated host captures under `.ufo/waves/round-54/after/services-probes/` of this repo
verified-at: 2026-10-31 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-10-31, read-only)
recheck: 30d — re-run the probe commands of rows T1-T8 (all read-only), compare the observed signatures with the captures in `.ufo/waves/round-54/after/services-probes/`; re-open S261/S262 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows services and scheduled-tasks plane (round 54)

Scope: the current host's Windows service state and Task Scheduler state — the operable analog of
the systemd user-units + timers plane this lane instrumented on its Linux host class (drift register
rows D2/D3 name that plane ABSENT here). This is the lane's own host-operability domain on the host
it now runs on (PROVINCE round-53 host-transition record); it absorbs no sibling scope. Detection and
report only — starting, stopping, changing or deleting any service or task stays operator-owned and
none was executed. All probes are read-only and were spelled for Git Bash (MSYS), whose path
conversion is itself row T1's finding.

| id | question | probe (read-only, 2026-10-31) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| T1 | How must `schtasks /query` be spelled under Git Bash? | bare `schtasks /query /fo CSV /nh` vs `MSYS_NO_PATHCONV=1 …`, `schtasks //query //fo CSV //nh`, `cmd //c "schtasks /query …"` | rc 0 with CSV rows (`t1t2-schtasks-all.csv`) | MSYS path conversion rewrites the slash-option before the tool sees it: bare `schtasks /query` fails with `ERROR: Invalid argument/option - 'C:/Program Files/Git/query'.` (`t1-msys-mangled-error.txt`) — a mangled error that reads like a scheduler fault but is a shell-quoting fault | Spell MSYS-safe (`MSYS_NO_PATHCONV=1`, doubled slashes, or `cmd //c`); never read the mangled error as a scheduler incident; all three workarounds measured identical output (rc 0, 246 rows) | dated capture `t1-msys-mangled-error.txt`, `t1-workarounds.txt`; option syntax S261 |
| T2 | How many scheduled tasks, in which format? | `MSYS_NO_PATHCONV=1 schtasks /query /fo CSV /nh \| wc -l` → 246; per-task detail `schtasks /query /tn <path> /fo LIST /v` | rc 0, CSV rows one per task; LIST /v shows TaskName / Next Run Time / Status / Last Run Time / Run As User (`t2-verbose-task.txt`) | `/v` is valid only with LIST or CSV output (S261), so `/fo TABLE /v` degrades or errors — verbose state must be read through LIST/CSV | Parse CSV for inventories, LIST /v for one task's state; counts drift with the host (246 is a 2026-10-31 capture) | S261 + dated capture |
| T3 | What does a nonexistent task return? | `MSYS_NO_PATHCONV=1 schtasks /query /tn "No-Such-Task-r54probe"` | rc 0 plus the task block for an existing name | `ERROR: The system cannot find the path specified.` rc 1 (`t3-nonexistent-task.txt`) — note: path, not "file"; `/tn` takes the full path-and-name (`\Microsoft\…`) and accepts no wildcards (S261) | Fix the `/tn` path and re-query; absence of a task is a probe result, not an incident to repair | dated capture; S261 /tn contract |
| T4 | What does a service query enumerate by default? | `MSYS_NO_PATHCONV=1 sc query` → 110 SERVICE_NAME blocks; `sc query state= all` → 273 (`t4-sc-active.txt`, `t4-sc-all.txt`) | rc 0; per-service block carries SERVICE_NAME, TYPE, STATE, WIN32_EXIT_CODE, SERVICE_EXIT_CODE, CHECKPOINT, WAIT_HINT (S262) | Two named traps: (a) a bare `sc query` is **active-only** (state= active is the S262 default) — reading 110 as the inventory undercounts (163 more with state= all); (b) S262's option rule "Each command-line option … must include the equal sign as part of the option name" with a space before the value — `type=own` fails where `type= own` works | Use `state= all` for inventories; parse STATE lines (`4  RUNNING`, `1  STOPPED` — measured on wuauserv, `t4-wuauserv-stopped.txt`), never block counts alone | S262 + dated captures |
| T5 | What does a nonexistent service return? | `MSYS_NO_PATHCONV=1 sc query No-Such-Service-r54probe` | rc 0 plus the service block | `[SC] EnumQueryServicesStatus:OpenService FAILED 1060:` + `The specified service does not exist as an installed service.` and process rc **36** (`t5-nonexistent-service.txt`) — [inference: the win32 code truncated to 8 bits, 1060 mod 256 = 36; scripts keying on rc alone collide with unrelated codes] | Match on the `FAILED 1060` line (or the message), not on rc; absence of a service is a probe result | dated capture |
| T6 | Does S262's `type= interact` error fire on this host? | `MSYS_NO_PATHCONV=1 sc query type= interact` | (per S262's server-era text, an error) | Divergence: the page says using `type= interact` by itself "will generate an error"; measured here rc 0 with Spooler listed (TYPE `110  WIN32_OWN_PROCESS  (interactive)`, STATE `4  RUNNING`, `t6-interact-type.txt`) — the documented error does not fire on this client build | Treat S262's sentence as server-class until a client-contradiction source opens; the probe's parser must accept the interactive-listing output; row rechecks on S262's next update | S262 (contradicted sentence) + dated capture |
| T7 | Is `sc` safe inside powershell.exe? | `powershell -NoProfile -Command "sc query wuauserv"` | (n/a — the hazard is the point) | Silent failure: rc 0, empty stdout, and a file named `query` containing `wuauserv` appears in the CWD (`t7-powershell-sc-alias-stdout.txt`, `t7-stray-setcontent-file.txt`) — in PowerShell `sc` is the Set-Content alias, so the "query" wrote a file instead | Run sc probes from bash, or spell `sc.exe` inside PowerShell; remove the stray file; treat silent rc 0 from a PowerShell sc alias as a no-op, not a query | dated capture |
| T8 | Does the documented Enum more-data overflow fire here? | `MSYS_NO_PATHCONV=1 sc query state= all` over 273 services, searched for `Enum: more data` | documented path: the message plus a bufsize=/ri= resumption recipe (S262) | Measured negative: the enumeration completed rc 0 with **no** Enum message on this build (`t4-sc-all.txt`) — the 1024-byte default buffer did not truncate visibly, so S262's resumption path is unverified here | None; if a future probe prints `Enum: more data`, follow S262's bufsize=/ri= recipe; until then treat bufsize=/ri= as doc-only on this host | S262 + dated negative capture |

## Repair plans (operator-gated; none executed this round)

- RP4 (service-state change): starting a stopped service (e.g. wuauserv, measured `1  STOPPED` on
  2026-10-31) or changing startup type is an operator decision; verification after such a change is
  the same read-only probe (`sc query <name>`, STATE line).
- RP5 (task-state change): `schtasks /run`, `/end`, `/change`, `/delete` are operator-owned (S261's
  operations list); this plane never issues them.

## Limits

All counts and state lines are captures of 2026-10-31 and drift with the host (tasks and services
come and go). S261/S262 are Windows Server reference pages (frontmatter `updated_at` 2026-02-16,
`git_commit_id 48fd0532…`); client behavior is treated as the same class except where measured
divergent here — T6 records the one measured contradiction, T7 a client-side alias hazard the pages
do not cover. T5's rc-36 arithmetic is labeled inference, not a sourced fact. The PowerShell alias
hazard was demonstrated with `-NoProfile`; a profile adding an sc.exe alias first is possible and
unprobed.
