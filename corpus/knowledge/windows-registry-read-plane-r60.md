source: S275 (row in `corpus/SOURCES.md`, opened 2026-11-01, this round) plus the dated host captures under `.ufo/waves/round-60/registry-probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-60/registry-probes/`) — next pass due 2026-11-30; re-run the probe commands of rows RG1-RG5 (all read-only), compare the observed signatures with the receipts; re-open S275 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows registry read plane (round 60)

Scope: the READ contract of `reg.exe query` — what a registry triage query returns, what its exit codes
and messages mean, and where the MSYS/bash boundary mangles it on this host. The r54-r59 planes read the
service and task state THROUGH `sc`/`schtasks`; this plane reads the store those surfaces sit on:
service configuration values (Start type, ErrorControl, FailureActions) live under
`HKLM\SYSTEM\CurrentControlSet\Services\<name>`, and the Task Scheduler service's own configuration key
(`Services\Schedule`) is the RG4 census target — the lane's own host-operability province, read directly.
Per S275 (Microsoft Learn `reg query`, Windows Commands; frontmatter `ms.date` 2022-11-02, `updated_at`
2025-10-22, `git_commit_id 4282dd47a285a65de44c1512e8e9abd2384582a8`, fetched live 2026-11-01) the
command "Returns a list of the next tier of subkeys and entries that are located under a specified
subkey in the registry." All probes are read-only `reg query` legs through `tools/receipt-run.py`
(receipts `.ufo/waves/round-60/registry-probes/`, dated 2026-11-01). Counts and data values are
DRIFT-CLASS captures — recorded as evidence, never judged; the exit codes, message lines and column
shapes are the invariants.

| Row | Surface (read-only) | Invariant (the judged signature) | Drift-class (never judged) | Receipt |
|---|---|---|---|---|
| RG1 | `reg query <key> /v <name>` | rc 0; blank line, key echo, then ONE three-column entry line `Name Type Data` | the data column's value | rg1 |
| RG2 | missing key or missing value | rc 1 + exactly one stderr line, `ERROR: The system was unable to find the specified registry key or value.` (S275 documents 0/1 only — the text is measured) | which of key/value was missed (same class) | rg2, rg2b |
| RG3 | `reg query <key> /s` (bounded target) | rc 0; key echo lines interleaved with RG1-shaped entry lines | subkey/entry counts; output size | rg3 |
| RG4 | type census vs the documented `/t` set | rc 0; observed type tokens are second-column tokens of entry lines; REG_QWORD exists AND `/t REG_QWORD` is ACCEPTED (S275's six-type set is the stale side) | per-type counts | rg4, rg4b, rg4c |
| RG5 | the bash/MSYS boundary + the `/ve` leg | bare `/v` fails `Invalid syntax.` rc 1 (conversion boundary); forward-slash key refuses `Invalid key name.` rc 1; with `MSYS_NO_PATHCONV=1` on the receipt-run invocation the probe passes; `/ve` returns the `(Default)` line with the literal `(value not set)` sentinel | the sentinel's value column; channel counts | rg5a, rg5b, rg5c |

## RG1 — the named-value query shape

`reg query <key> /v <valuename>` (rg1 receipt, rc 0): stdout is a blank line, the key echo line
(`HKEY_LOCAL_MACHINE\...`), then one ENTRY line of exactly three whitespace-separated columns —
`ProductName    REG_SZ    Windows 10 Home` — name, type, data. The data column is drift-class. Per S275:
"`/v <valuename>` — Specifies the registry value name that is to be queried. If omitted, all value names
for keyname are returned." The `/ve` leg (rg5c receipt, rc 0) queries the empty value name and returns
`(Default)    REG_SZ    (value not set)` — the same three-column shape with the literal sentinel text
`(value not set)` in the data column (drift-class value; the sentinel STRING is the signature). Triage
decision: a value's type is the second column, never guessed from the data's shape.

## RG2 — the absence class: one message for two different misses

A missing KEY (rg2: `...\No-Such-Key-r60probe /v Nope`) and a missing VALUE in an existing key (rg2b:
`...CurrentVersion /v No-Such-Value-r60probe`) are the SAME observable: exit code 1 and exactly one
stderr line, `ERROR: The system was unable to find the specified registry key or value.` S275's
"Remarks" return-value table documents only `0 | Success` and `1 | Failure` — no message text — so the
message line is a host-measured signature, not a documented one (the S274 API-vocabulary-vs-CLI-display
boundary class). Triage decision: rc 1 WITH this single line means "the queried path does not exist";
rc 1 with a DIFFERENT message is a different class — rg5a/rg5b show the refusal class (`Invalid syntax.`,
`Invalid key name.`) and S275 documents no third message, so any new absence-shaped text is a recheck
trigger, not a known class.

## RG3 — the recursion leg

`reg query <key> /s` (rg3 receipt, rc 0, on the bounded service key `SamSs`): stdout interleaves key
echo lines (each nested subkey path) with the same three-column entry lines of RG1; per S275 "`/s` —
Specifies to query all subkeys and value names recursively." Output size is unbounded a priori — the
same `/s` on `CurrentVersion` measured ~3.0 MB in this round's sizing recon (scratch, not receipted) —
so a census leg bounds its target key first; the receipt keeps the whole verbatim output only for a
bounded key. Counts of subkeys and entries are drift-class.

## RG4 — the type vocabulary: documented set vs host set

Census on the Task Scheduler service's own config key `HKLM\SYSTEM\CurrentControlSet\Services\Schedule`
(rg4 receipt, rc 0): five types observed — REG_SZ, REG_DWORD, REG_EXPAND_SZ, REG_MULTI_SZ, REG_BINARY
(counts drift-class). S275's `/t` parameter row documents the search-type set as REG_SZ, REG_MULTI_SZ,
REG_EXPAND_SZ, REG_DWORD, REG_BINARY, REG_NONE — six types, no REG_QWORD. The host disagrees on both
sides: REG_QWORD exists as a stored type on this host (rg4b receipt, rc 0:
`LastLogOffEndTimePerfCounter    REG_QWORD    0x363bab1` under Winlogon), AND the `/t REG_QWORD` filter
is ACCEPTED by the CLI (rg4c receipt, rc 0, `End of search: 1 match(es) found.`) — the documented set is
narrower than the CLI's live behavior (the r59 J3 `/hresult` divergence class; here the DOCUMENTATION is
the stale side, measured). Triage decision: a type token outside the documented six is not an error nor
an unknown — the /t filter accepts it; S275's row carries this divergence for its next re-open.

## RG5 — the bash/MSYS boundary and the /ve leg on this host

Three receipts bound the boundary: (a) with `MSYS_NO_PATHCONV=1` set on the receipt-run invocation, the
`/v` switch and the backslash key path cross the bash→python→native chain verbatim (rg1, rc 0 — the
j-probe convention); (b) WITHOUT it, the same command fails `ERROR: Invalid syntax.` rc 1 (rg5a) — the
switch is rewritten at the bash→python boundary before any child environment could matter (the r54 T1 /
r58 E2s conversion class, measured on reg.exe); (c) the forward-slash key path
`HKLM/SOFTWARE/Microsoft/Windows NT/CurrentVersion` refuses `ERROR: Invalid key name.` rc 1 even with
path conversion disabled (rg5b) — reg.exe does not normalize slashes in key paths; S275's examples use
the backslash form exclusively, and the refusal text is measured, not documented. Triage decision: on
this host every registry probe runs with `MSYS_NO_PATHCONV=1` on the receipt-run invocation and backslash
key paths, and a bare-spelling rerun is the conversion-class falsifier, not evidence about the registry.

## Boundary

Read-only: this plane invokes `reg query` only. The write surfaces — `reg add`, `reg delete`, `reg copy`,
`reg save`, `reg restore`, `reg load`, `reg unload`, `reg import` — are operator-owned and are never
invoked; `reg export`/`reg compare` and `reg save`-based capture are out of scope (the plane reads, it
does not stage copies). The plane reads documented OS-configuration keys (CurrentVersion, Services\<name>,
Winlogon); it does not read credential-bearing hives (SAM, SECURITY) or mine value CONTENT beyond the
triage shapes above — value data columns in the receipts are drift-class captures of configuration state,
not material. Registry repair (permission changes, hive loads, value writes) is a report, never an
action: detection and report; the operator remediates.
