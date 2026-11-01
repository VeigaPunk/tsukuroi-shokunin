source: S261 (row in `corpus/SOURCES.md`, opened 2026-10-31) plus S274 (opened 2026-11-01, this round) and the dated host captures under `.ufo/waves/round-59/task-probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-59/task-probes/`) — next pass due 2026-11-30; re-run the probe commands of rows J1-J5 (all read-only), compare the observed signatures with the receipts; re-open S274 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows scheduled-task status plane (round 59)

Scope: the VALUE grammar of the scheduled-task read-only surface — what the Status column and the verbose
fields MEAN once `schtasks /query` succeeds. The r54 services plane owns the spelling/count/absence rows
T1-T3 (bare-vs-`MSYS_NO_PATHCONV=1` spelling, `/fo CSV /nh` census, nonexistent-task refusal) and T2 named
the verbose FIELD NAMES; this plane extends the same surface with the fields' DECISION GRAMMAR: which
Status strings exist, what `Last Result` values mean (the triage column), how `Scheduled Task State` differs
from `Status`, and what `/hresult` actually does on this host. Per S261 the query surface's formats are
TABLE/LIST/CSV with `/v` valid only for LIST/CSV; per S274 the Task Scheduler status vocabulary is the
HRESULT constant set "in WinError.h": "The constants that begin with SCHED\_S\_ are success constants, and
the constants that begin with SCHED\_E\_ are error constants" (Gate quote, 19 words by `wc -w`). Detection
and report only: `/run /end /change /delete /create` are operator-owned and none was executed. All probes
are read-only and spelled `MSYS_NO_PATHCONV=1` on the process spawn (the T1/E2 class).

| id | question | probe (read-only, 2026-11-01) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| J1 | Which Status values exist on this host, and in which column? | `MSYS_NO_PATHCONV=1 schtasks /query /fo CSV /nh`, Status = 3rd CSV field (`awk -F'","' '{print $3}'`) | rc 0, one CSV row per task (246 here, the r54 capture count — drift-class), Status vocabulary observed: **Ready 206 / Disabled 37 / Running 3** | n/a — enumeration does not fail on content | Triage by class: `Running` = an instance is live now; `Ready` = registered and waiting for its trigger; `Disabled` = configured off (J4) — none of the three is an incident by itself; an EMPTY or unknown Status value would be the finding | dated capture `j1-status-census.txt`; S261 `/fo CSV /nh` parameter rows; the string↔constant correspondence below is measured, not sourced [inference] |
| J2 | What do the verbose triage fields mean for ONE task (the `journalctl -u <unit> -l` analog)? | `MSYS_NO_PATHCONV=1 schtasks /query /tn "<task>" /fo LIST /v` | rc 0; invariant = the six triage FIELDS are present (`Status`, `Last Run Time`, `Last Result`, `Next Run Time`, `Logon Mode`, `Scheduled Task State`); values drift-class | `ERROR: The system cannot find the path specified.` rc 1 for a bad `/tn` (the r54 T3 class — not re-probed) | THE DECISION TABLE: `Last Result: 0` = the last run SUCCEEDED (J2b: Ready task Autochk\Proxy ran 9/23/2026, result 0); `Last Result: 267009` on a task whose `Status: Running` = the STATUS constant SCHED\_S\_TASK\_RUNNING 0x00041301 in decimal (0x41301 = 267009, arithmetic [inference]), i.e. "currently running", NOT an exit code — a nonzero Last Result is a FAILURE only when the task is not Running and the value is outside the 0x413xx informational class (S274: 0x00041300-0x00041325 success constants; 0x800413xx error constants); `Scheduled Task State: Enabled/Disabled` is the CONFIGURATION field, distinct from `Status` | dated captures `j2-verbose-fields.txt`, `j2b-ready-task-fields.txt`; S274 constant rows (0x00041301 "The task is currently running.", 0x00041303 "The task has not yet run."); S261 `/v` row |
| J3 | What does `/hresult` actually reshape on this host? | `MSYS_NO_PATHCONV=1 schtasks /query /tn "<task>" /fo LIST /v /hresult` | rc 0; measured DIVERGENCE (the r54 T6 class): on this build (10.0.26200) the `/hresult` switch left the `Last Result` display UNCHANGED — still decimal `267009`, not `0x41301`; S261 documents `/hresult` as reshaping the PROCESS EXIT CODE, which this rc-0 probe cannot exercise | a future reading of `Last Result: 0x…` (hex) is the S274 vocabulary verbatim; a decimal 267xxx value is the same constants mod nothing — decimal 267009 = 0x41301 | Read Last Result on this host as DECIMAL; convert before consulting S274 (`printf '0x%x' 267009`); never read 267009/267011 as the task's own exit code — they are status constants | dated capture `j3-hresult-hex.txt`; S261 `/hresult` row ("reshapes the process exit code" — exit-code effect UNTESTED here, rc was 0); S274 0x00041301 row |
| J4 | How large is the Disabled class, and is Disabled an incident? | `bash -c "MSYS_NO_PATHCONV=1 schtasks /query /fo CSV /nh \| grep -ic disabled"` | rc 0, count **37** here (J1's Disabled rows; drift-class) | grep exits 1 on count 0 — a zero count is a VALID answer, never a probe failure (the E5 class) | `Disabled` is configuration (S274 SCHED\_S\_TASK\_DISABLED 0x00041302: "The task will not run at the scheduled times because it has been disabled."), not a health fault; flag only when a task the operator expects to run sits Disabled | dated capture `j4-disabled-census.txt`; S274 0x00041302 row |
| J5 | Which shape does each format switch yield for the SAME task? | `bash -c` composite: `/fo CSV` (with header) then `/fo LIST` (no `/v`) on one `/tn` | rc 0; CSV = 3-column header `TaskName,Next Run Time,Status` + quoted row; LIST (no /v) = compact `Folder:/HostName:/TaskName:/Next Run Time:/Status:/Logon Mode:` block; LIST /v adds the J2 field set | `/fo TABLE /v` degrades or errors (the r54 T2 rule — valid-with-LIST/CSV only; not re-probed) | Machine parsing → CSV (`awk -F'","'`); human triage of one task → LIST /v; the compact LIST is the receipt-friendly middle; never mix `/fo TABLE` with `/v` | dated capture `j5-format-shapes.txt`; S261 `/fo` + `/nh` rows (CSV/TABLE may carry `/nh`, LIST may not) |

## Repair plans (operator-gated; none executed this round)

- RP8 (state change): `/run /end` force a task's lifecycle, `/change` rewrites schedule/account/enabled,
  `/delete` removes a task, `/create` registers one — operator-owned (S261's overview-page operations list;
  the r54 plane's operator-owned rule for the same surface). The lane never issues them; a disabled task
  the operator wants live is an operator `/change /ENABLE`, not a lane action.
- RP9 (failure triage): a nonzero Last Result outside the 0x413xx class on a non-Running task is the
  incident record to investigate (scheduler history/event-log plane r58, then the task's own command);
  investigation is report-only — the lane captures, the operator repairs.

## Limits

All counts, times and the task inventory (246 rows) are captures of 2026-11-01 and drift with the host.
S274 is the Win32 API constant reference (WinError.h; frontmatter `ms.date` 2024-10-29, `updated_at`
2024-10-29T23:32:00Z, `git_commit_id 008b6856…`): it documents the API's HRESULT vocabulary, NOT the
`schtasks.exe` display columns — the Status-string ↔ constant correspondence and the decimal display are
MEASURED on this host (J1-J3), the arithmetic 267009 = 0x41301 is inference, and a Windows build could
display differently (the J3 divergence class is the precedent). The direct URL
`.../task-scheduler-error-and-success-codes` returned HTTP 404 on 2026-11-01; the live page is
`.../task-scheduler-error-and-success-constants` (recorded, the S267/S273 precedent — nothing opened at the
404). Some Task Scheduler APIs "can return system and network error codes" per S274's own note — so a Last
Result outside 0x413xx/0x800413xx is not decodable from S274 alone (S274 names `net helpmsg` for that
class). J4's count is a name-substring census (`grep -ic disabled`), not the scheduler's own disabled-state
query. `/hresult`'s exit-code effect is untested here (both probes rc 0).

## QUALITY check

1. Falsifiable/measured: every row's probe is a pasteable read-only command with a dated receipt (J1-J5 +
   J2b, rc 0 each). 2. Source anchors: S261 (parameter rows, opened 2026-10-31) and S274 (constant table,
   opened 2026-11-01, Gate quote 19 words) carry the propositions; measured display facts cite receipts;
   inference is marked ([inference] on the decimal↔hex arithmetic and the string↔constant mapping). 3.
   Observation vs inference vs unknown separated (J3's divergence observation; the API↔CLI mapping
   inference; the /hresult exit-code effect untested). 4-5. Errata/rejections: the `-codes` URL 404 is
   recorded here and in S274's row; nothing rejected this round. 8. Header carries source/verified-at/
   recheck with ISO dates and a 30d cadence. 9. Negative claims (no prior status-vocabulary coverage) are
   the at-base sweeps in the SCORECARD declaration, receipt `.ufo/waves/round-59/before/c1-c2-c3-at-base.txt`.
