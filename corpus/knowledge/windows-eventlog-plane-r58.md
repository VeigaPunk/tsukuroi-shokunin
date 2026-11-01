source: S272 S273 (rows in `corpus/SOURCES.md`, both opened 2026-11-01) plus the dated host captures under `.ufo/waves/round-58/eventlog-probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-58/eventlog-probes/`) — next pass due 2026-11-30; re-run the probe commands of rows E1-E6 (all read-only or refusal-class), compare the observed signatures with the receipts; re-open S272/S273 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows event-log triage plane (round 58)

Scope: the current host's Windows event-log surface — the operable analog of the journal/boot triage plane
this lane owns in Core on its Linux host class (drift register rows D2/D3 name `journalctl`/`systemd` ABSENT
here; PROVINCE round-53 host-transition record). `wevtutil` is the Event Log service's command-line reader:
per S272 it "Enables you to retrieve information about event logs and publishers" (Gate quote, 10 words by
`wc -w`); a channel — what the tool enumerates — is, per S273, "basically a sink that collects events"
(Gate quote, 9 words by `wc -w`), of one of four types Admin/Operational/Analytic/Debug. Detection and
report only: clearing, configuring, exporting or archiving logs stays operator-owned and none was executed
(the clear-log gate is measured refusal-class, see Repair plans). All probes are read-only and were spelled
for Git Bash (MSYS) — whose slash-option conversion is this plane's first finding (E2).

| id | question | probe (read-only, 2026-11-01) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| E1 | How many event channels does the host carry? | `MSYS_NO_PATHCONV=1 wevtutil el \| wc -l` | rc 0, one channel name per line | n/a — enumeration does not fail on content | Parse the list for plane scope (339 of the 1164 names carry `Analytic`/`Debug` — S273's disabled-by-default classes live here as channels, not as a fault); the count is a capture that drifts with the host (1162 pre-declaration, 1164 at the probe, same day) | dated capture `e1-el-inventory.txt`; S272 `{el \| enum-logs}` "Displays the names of all logs" |
| E2 | How are the newest events of a log read as text, and how must the options be spelled? | `MSYS_NO_PATHCONV=1 wevtutil qe System /c:3 /rd:true /f:text` | rc 0, `Event[0]` blocks newest-first (Log Name / Source / Date / Event ID / Level / Opcode), newest = the most recent System record (S272's own example shape, `qe Application /c:3 /rd:true /f:text`; S272 `/rd`: "If true, the most recent events are returned first") | THE SPELLING TRAP (the T1 class, one gate deeper): MSYS rewrites each slash-led option as a bare word (`/c:3` → `c:3`), so bare `wevtutil qe System /c:3 …` fails rc **87** `Too many arguments are specified.` (`e2-qe-mangled-spelling-rc87.txt`) — a usage error that reads like a tool fault but is a shell-quoting fault; and when the probe is routed through a python spawn (receipt-run), setting `MSYS_NO_PATHCONV=1` inside the CHILD argv does NOT protect it — the conversion happens at the bash→python boundary, so the variable must be set on the python spawn itself (`e2b-env-in-child-argv-still-mangled-rc87.txt`); also stdout lines are CRLF (`tr '\r' '\n'` before line-oriented parsing, the journal-plane line-count trap) | Spell `MSYS_NO_PATHCONV=1` on the process spawn (bash→native, or bash→python); never read rc 87 as a scheduler-class incident; count events by `Event[N]` blocks, not lines | S272 qe example + /rd, /c, /f option rows; dated captures |
| E3 | What does a query on a nonexistent channel return? | `MSYS_NO_PATHCONV=1 wevtutil qe No-Such-Channel-r58probe /c:1` | rc 0 plus the event blocks for an existing name | Query-leg refusal: `Failed to open event query.` + `The specified channel could not be found.` with process rc **15007** through a python spawn — 15007 mod 256 = **159**, the rc the same probe reports when spawned from bash directly (the T5 truncation class: bash reports the win32 code modulo 256, python the full value; scripts keying on rc alone must match the message line, not the number) | Fix the channel name (the full provider path, e.g. `Microsoft-Windows-…/Operational`); absence of a channel is a probe result, not an incident to repair | dated capture `e3-qe-nonexistent.txt` (+ the mangled-spelling pair `e3-qe-mangled-spelling-rc87.txt`, `e3b-env-in-child-argv-still-mangled-rc87.txt`); rc arithmetic [inference] per the T5 class |
| E4 | What metadata does the log itself expose? | `MSYS_NO_PATHCONV=1 wevtutil gli System` | rc 0 with `creationTime` / `lastAccessTime` / `lastWriteTime` / `fileSize` / `attributes` / `numberOfLogRecords` / `oldestRecordNumber` (System: 4 852 records, 3 215 360 B at capture — drift-class values) | n/a — the status read does not fail on content | Use `numberOfLogRecords`/`fileSize` as the journal-disk-usage analog (the old plane's `journalctl --disk-usage`); every timestamp is a capture, never quoted as current | dated capture `e4-gli-system.txt`; S272 `{gli \| get-loginfo}` "Displays status information about an event log or log file" |
| E5 | How are recent ERRORS read (the `journalctl -p err` analog)? | `MSYS_NO_PATHCONV=1 wevtutil qe System '/q:*[System[(Level=1 or Level=2)]]' /c:5 /rd:true /f:text` | rc 0, newest Level 1/2 events first (top capture: WindowsUpdateClient Event ID 20, `Level: Error`) — S272 `/q`: "Defines the XPath query to filter the events that are read or exported" | The XPath must be quoted as ONE argument (spaces + brackets); a mangled split lands in the E2 rc-87 class, not in an error-events answer — an empty result is a valid answer (no recent errors), never proof the filter failed; cross-check rc 0 and the `Event[N]` header | Filter levels in the query (`Level=1` critical, `Level=2` error); report the matched events with dates; volume triage over more history is a wider `/c:` or a structured query (operator-class analysis, same read-only form) | S272 /q option row; dated capture `e5-qe-level-filter.txt` |
| E6 | Does the metadata leg refuse absence like the query leg? | `MSYS_NO_PATHCONV=1 wevtutil gli No-Such-Channel-r58probe` | rc 0 plus the status block for an existing name | Metadata-leg refusal: `Failed to read log status information for log <name>.` + the SAME `The specified channel could not be found.` message and the SAME rc family (15007/159) as E3 — the FUNCTION LINE is leg-specific (`Failed to open event query.` vs `Failed to read log status information`), so a classifier must key on the message line or accept both function lines per leg | Same as E3; the leg-specific function line is the classifier's hint about WHICH read failed | dated capture `e6-gli-nonexistent.txt` |

## Repair plans (operator-gated; none executed this round)

- RP6 (log-state change): `wevtutil cl <Logname>` clears a log, `sl` reconfigures one — operator-owned
  (S272: cl "Clears events from the specified event log."). The lane never issues them. Measured refusal
  gate only: bare `wevtutil cl` (no log name) is refused at the usage gate with rc **87**
  `Required argument(s) is/are not specified.` — no log can be cleared by accident without naming it
  (`e6b-cl-usage-refusal.txt`).
- RP7 (export/archive): `epl`/`al` write files — a lane-tree export into scratch is possible read-only for
  the log, but any archive stays operator-owned; not probed this round.

## Limits

All counts, timestamps and sizes are captures of 2026-11-01 and drift with the host (channels, records and
file size change continuously). S272 is the current Windows Server commands reference (frontmatter
`updated_at` 2026-05-15, `git_commit_id f63a32ea…`) — client behavior treated as the same class except where
measured here; S273 is the Win32 instrumentation concept page (frontmatter `updated_at` 2025-03-11,
`git_commit_id 03b700b5…`) — it documents MANIFEST-defined channels, not the `wevtutil` CLI; the direct
`event-channels` URL returned 404 on 2026-11-01 (recorded in S273's row, nothing opened there). The rc
15007↔159 relation is arithmetic inference per the T5 class, not a sourced fact. E1's Analytic/Debug count
is a name-substring count (339), not the Event Log service's own channel-type classification — the service
does not expose type per channel through this CLI surface [bounded by S272's option table, which defines no
type query]. The `cl` usage-gate probe (rc 87) demonstrates the argument gate only; the behavior of `cl` WITH
a log name under a read-only session is UNTESTED by design (it would clear a log — operator territory).

## Limits correction (appended r58, same round — the two probe receipts are binary-flagged)

Post-commit sweep finding: the E2 and E5 receipt files (`.ufo/waves/round-58/eventlog-probes/
e2-qe-recent-text.txt`, `e5-qe-level-filter.txt`) carry embedded **NUL bytes** (0x00 in the
`wevtutil /f:text` event text — git diff-tree numstat flags both files binary). The committed
bytes are the receipts as captured; nothing was cleaned. Parsing consequence: a NUL-containing
file is treated as binary by grep (use `-a` or strip `\r\0` first — the `tr '\r' '\n'` class in
E2's cell extends to `tr -d '\0'`); a byte-level evidence check (sha256) is unaffected.
