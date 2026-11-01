source: S276 (row in `corpus/SOURCES.md`, opened 2026-11-01, this round) plus the dated host captures under `.ufo/waves/round-61/driver-probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-61/driver-probes/`) — next pass due 2026-11-30; re-run the probe commands of rows DQ1-DQ5 (all read-only), compare the observed signatures with the receipts; re-open S276 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows driver query plane (round 61)

Scope: the READ contract of `driverquery.exe` — what the installed-device-driver inventory returns, which
columns carry triage state, what its refusal messages mean, and where the MSYS/bash boundary mangles it on
this host. This is the lane's driver/firmware province (PROVINCE Core: "driver/firmware plane (kernel
modules, nvidia driver + GSP firmware presence, nvidia-smi shape)") on the Windows host class — the analog
of the Linux lsmod/dkms/nvidia-smi plane, and the inventory behind the r54-r59 service/task surfaces.
Per S276 (Microsoft Learn `driverquery`, Windows Commands; frontmatter `ms.date` 2017-10-16, `updated_at`
2026-02-16T18:34:00Z, `git_commit_id 1dde3f071fa8b65476a0f278d15ed67c19b07896`, fetched live 2026-11-01)
the command "Enables an administrator to display a list of installed device drivers and their
properties." All probes are read-only `driverquery` legs through `tools/receipt-run.py` (receipts
`.ufo/waves/round-61/driver-probes/`, dated 2026-11-01); local reads only — the remote `/S /U /P` legs
are out of scope, and driverquery has no write verbs, so nothing beyond scope exists to fence. Counts and
data values are DRIFT-CLASS captures — recorded as evidence, never judged; the exit codes, message lines
and column shapes are the invariants.

| Row | Surface (read-only) | Invariant (the judged signature) | Drift-class (never judged) | Receipt |
|---|---|---|---|---|
| DQ1 | `driverquery /FO csv` (the default inventory; per S276 `/fo table` is the default and `/fo csv` formats CSV) | rc 0; ONE header line of 4 quoted columns `"Module Name","Display Name","Driver Type","Link Date"` then one quoted 4-column row per driver; the Driver Type cell carries a trailing space inside the quotes (`"Kernel "`) — a naive CSV/consumer parse reads a different token than the display shows | driver count (411 rows at capture) and the Link Date cells (many empty strings) | dq1 |
| DQ2 | `driverquery /FO csv /V` (verbose) | rc 0; the header widens to 15 quoted columns ending `"Link Date","Path","Init(bytes)"`; Start Mode / State / Status / Accept Stop / Accept Pause are the triage columns (S276 documents only "/v Displays verbose output." — the column set is host-measured, the page names none) | per-driver values (pool/code/BSS/init sizes, link dates, states, paths) | dq2 |
| DQ3 | refusal classes | invalid `/FO` value → exactly one stderr error line `ERROR: Invalid syntax. '<val>' value is not allowed for '/FO' option.` + the usage line, rc 1; `/FO LIST /NH` → exactly one stderr error line `ERROR: Invalid syntax. /NH option is valid only for "TABLE" and "CSV" format.` rc 1 — S276's "/nh … Not valid if the /fo parameter is set to list" MEASURED (docs and host agree; the message TEXT is host-measured, S276 documents no message text and no return-value table) | none — both legs deterministic | dq3, dq3b |
| DQ4 | `driverquery /SI` (the signed-drivers view; S276: "/si Provides information about signed drivers.", and `/v | /si` is a documented alternative pair) | rc 0; a plain-text 4-column table — header `DeviceName InfName IsSigned Manufacturer`, a `====` ruler row, then rows whose IsSigned cells are `TRUE`/`FALSE`; the `/V /SI` combination refuses `ERROR: Invalid syntax. The verbose option is invalid for signed drivers.` rc 1 (S276's "/v is not valid for signed drivers" MEASURED) | device rows (159 at capture) and their InfName/Manufacturer cells | dq4, dq4b |
| DQ5 | the bash/MSYS boundary | bare `/FO` on the receipt-run spawn is path-converted at the bash→python boundary → `ERROR: Invalid argument/option - 'C:/Program Files/Git/FO'.` rc 1 (the mangled argv recorded verbatim in the receipt's `command=` line); the `//FO` double-slash escape passes rc 0 (MSYS strips it to `/FO` at the same boundary); `MSYS_NO_PATHCONV=1` set on the receipt-run INVOCATION (not the child argv — the e2b class) passes rc 0 — the r60 RG5 class recurring on a SECOND Windows command: a two-command pattern, not a one-off | none — deterministic | dq5a, dq5b, dq5c |

## DQ1 — the default CSV inventory

`driverquery /FO csv` (dq1 receipt, rc 0, 412 stdout lines): the first line is the 4-column header, then
one quoted-CSV row per driver. Two measured traps live in the ordinary rows: (a) the Driver Type cell is
`"Kernel "` — a trailing space INSIDE the quotes, so a consumer comparing the cell to `Kernel` on raw
bytes mismatches every kernel row; (b) Link Date cells are frequently empty strings (`""`), so date-parse
consumers must expect the empty cell as a normal value, not a fault (drift-class which rows carry which).
Per S276 the table format is the default and csv is one of the three documented `/fo` values; the header
column set is host-measured (the page documents no columns).

## DQ2 — the verbose column set is host-measured

`driverquery /FO csv /V` (dq2 receipt, rc 0): the header widens to 15 quoted columns — Module Name,
Display Name, Description, Driver Type, Start Mode, State, Status, Accept Stop, Accept Pause, Paged
Pool(bytes), Code(bytes), BSS(bytes), Link Date, Path, Init(bytes). The triage columns are Start Mode
(boot/system/auto/manual/demand vocabulary at capture), State (Stopped/Running), Status (OK) and the two
Accept booleans; the size cells carry thousands separators (`4,096`) and the Path cell is a native
backslash path. S276's `/v` row says only "Displays verbose output." — every column name above is a
host-measured signature, the S274/S275 documentation-gap class. (`/V` without `/FO` emits the same 15
columns in the fixed-width TABLE shape — same columns, different renderer.)

## DQ3 — the refusal class: one message line, rc 1, and the docs agree on the restriction

Both refusal legs are deterministic. An invalid format value (dq3, rc 1):
`ERROR: Invalid syntax. 'bogus' value is not allowed for '/FO' option.` — the offending value echoed
between single quotes inside the message. The documented /nh-list restriction (dq3b, rc 1):
`ERROR: Invalid syntax. /NH option is valid only for "TABLE" and "CSV" format.` — S276's parameter table
says "/nh … Not valid if the /fo parameter is set to list"; the host enforces exactly that, with a
measured message S276 does not document. S276 documents no return-value table at all (the S274/S275
absence class): rc 0/rc 1 and every message line above are host-measured. Triage decision: a refusal is
rc 1 plus ONE error line plus the usage line — a silent rc 1 with no message would be a different,
unmeasured class.

## DQ4 — the signed-drivers view and the /v|/si exclusivity

`driverquery /SI` (dq4 receipt, rc 0): a plain-text table, NOT csv — header `DeviceName InfName
IsSigned Manufacturer`, a `====` ruler row, then whitespace-separated columns (truncation at column
width applies to DeviceName). The `/V /SI` combination (dq4b, rc 1) refuses with `ERROR: Invalid syntax.
The verbose option is invalid for signed drivers.` — S276's "/v is not valid for signed drivers"
MEASURED; the syntax's `/v | /si` alternative pair is enforced by the host, not just documented.

## DQ5 — the MSYS boundary generalizes (RG5 class, second command)

`driverquery /FO csv` invoked with a bare `/FO` on the receipt-run spawn (dq5a, rc 1): MSYS path
conversion fired at the bash→python boundary and the receipt's own `command=` line records the mangled
argv — `driverquery 'C:/Program Files/Git/FO' csv` — with the host refusing `ERROR: Invalid
argument/option - 'C:/Program Files/Git/FO'.` The escapes: the `//FO` double-slash form (dq5b, rc 0 —
MSYS strips it to `/FO` at the same boundary, the receipt showing the clean `command=driverquery /FO
csv`), and `MSYS_NO_PATHCONV=1` set on the receipt-run INVOCATION (dq5c, rc 0; on the child argv via
`env` it is the e2b class — the conversion has already happened before the child env can matter).
Round 60 measured this class on `reg query` (RG5); round 61 measures the identical signature on
`driverquery` — the boundary rule is per-host, not per-command, and any lane probe of a native
Windows CLI through this host must spawn with the var on the invocation or the `//` escape.

## QUALITY check

- Q1 source: every row's documented side cites S276 (tier A, current reference, opened 2026-11-01; the
  lede quote is 14 words by `wc -w`); every host-side signature cites a dated receipt under
  `.ufo/waves/round-61/driver-probes/` (QUALITY 2, 7).
- Q2 observation/inference/unknown separation: rc values, message lines, column sets and cell shapes are
  observations (receipts); the "boundary rule is per-host" reading is [inference] from two measured
  commands (RG5, DQ5) — two points, not proof of universality; unknown: whether other MSYS option shapes
  (`/nh`, `/si` bare on the spawn) mangle identically (not probed — dq5a is the representative leg).
- Q3 negative claims: "S276 documents no return-value table and no message text" — grounded by reading
  the opened page (parameter table, syntax, examples, related links; no returns section). "No write
  verbs" — grounded by the opened page's complete parameter table (no write surface exists to fence);
  the local-only scope is a lane decision recorded in the note header, not a host measurement.
- Q4 errata policy: this note is append-only; a changed signature gets an appended correction naming the
  receipt it supersedes (QUALITY 4, 5).
- Q5 recheck duty: executable in the note's `recheck:` header (30d, day 0 2026-11-01, due 2026-11-30);
  the C2 instrument of this round (`tools/recheck-registry-r61.sh`) covers the REGISTRY plane's rows —
  the DQ rows' own executable arm is a candidate only if a DQ-probe drift fires (the r59 planned-item
  pattern).
