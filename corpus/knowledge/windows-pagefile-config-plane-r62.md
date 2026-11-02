source: S277 (row in `corpus/SOURCES.md`, opened 2026-11-01, this round) plus the dated host captures under `.ufo/waves/round-62/probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-62/probes/`) — next pass due 2026-12-01; re-run the probe commands of rows PF1-PF6 (all read-only), compare the observed SHAPES with the receipts (values are drift-class); re-open S277 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows pagefile / commit-charge config read plane (round 62)

Scope: the CONFIG READ contract of the pagefile on this host — where the pagefile lives, whether its
size is system-managed or explicit, what the usage counters mean, and which legacy tool is GONE. This
is the r61 planned candidate ("a Windows pagefile/commit-charge memory CONFIG read ... memory
PRESSURE evidence stays mori's (ADJ-04), the config surface is this lane's"): every probe here is a
read-only config/state read; the values are DRIFT-CLASS captures — recorded as evidence, never judged;
the shapes, instance counts, empty-result behavior and refusal lines are the invariants. Boundary
(ADJ-04, PROVINCE): commit-charge numbers in PF5 say nothing about which fleet wave caused pressure or
whether an endpoint works — attribution requests go to mori; this note is the config plane only.
Per S277 (Microsoft Learn `Win32_PageFileUsage`, Win32/CIMWin32 provider; frontmatter
`ms.date` 2018-05-31, `updated_at` 2021-01-06T23:44:00Z,
`git_commit_id f2fe29cc5eff117e10d2c47a87e00ea55507cc96`, fetched live 2026-11-01) the class
"represents the file used for handling virtual memory file swapping on a Win32 system." All probes ran
under Git Bash on 2026-11-01 through `tools/receipt-run.py` (receipts
`.ufo/waves/round-62/probes/`, dated 2026-11-01); the PowerShell legs carry no forward-slash switches,
so the RG5/DQ5 MSYS path-conversion class did not arise on this plane (a scope observation, not an
invariant — a future leg adding `/flags` re-arms it).

| Row | Surface (read-only) | Invariant (the judged signature) | Drift-class (never judged) | Receipt |
|---|---|---|---|---|
| PF1 | `powershell -NoProfile -Command "Get-CimInstance Win32_PageFileUsage \| Select-Object Name,AllocatedBaseSize,CurrentUsage,PeakUsage \| Format-List"` | rc 0; exactly ONE instance in the result set; `Format-List` renders each property as `Name : value` lines; S277 documents the three uint32 counters each with units ("megabytes") — AllocatedBaseSize (per S277 "Actual amount of disk space allocated for use with this page file", "corresponds to the range established in Win32_PageFileSetting under the InitialSize and MaximumSize properties, set at system startup"), CurrentUsage ("Amount of disk space currently used by the page file"), PeakUsage ("Highest use page file.") | the Name path (`C:\pagefile.sys` at capture) and the three MB values (18035 / 4570 / 5287 at capture) | `.ufo/waves/round-62/probes/pf1-usage.txt` |
| PF2 | `powershell -NoProfile -Command "Get-CimInstance Win32_PageFileSetting \| Select-Object Name,InitialSize,MaximumSize \| Format-List"` | rc 0 with an EMPTY result set — under automatic management there is NO Win32_PageFileSetting instance at all (an empty `Select-Object` pipeline prints nothing); a triage reader must treat "rc 0 + zero instances" as the system-managed indicator, not a probe failure — S277's AllocatedBaseSize cross-reference names the class but the page does not document the zero-instance behavior | none — the emptiness is the invariant under automatic management (re-judge if PF3 flips) | `.ufo/waves/round-62/probes/pf2-setting-empty.txt` |
| PF3 | `powershell -NoProfile -Command "(Get-CimInstance Win32_ComputerSystem).AutomaticManagedPagefile"` | rc 0; stdout is exactly `True` (plus the receipt's own framing) — the authoritative automatic-management flag and the triage pair with PF2: True here means PF2's emptiness is expected, not a broken probe | none | `.ufo/waves/round-62/probes/pf3-automatic-managed.txt` |
| PF4 | `reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v PagingFiles` | rc 0; the value exists, type `REG_MULTI_SZ`, data `?:\pagefile.sys` — the system-managed wildcard form (drive wildcard `?:`, NO explicit Initial/Maximum sizes; an explicit config would read `C:\pagefile.sys 4096 8192`-shaped); the config STORE leg — the registry plane's r60 read contract applies | none — the wildcard form is the invariant under automatic management | `.ufo/waves/round-62/probes/pf4-registry-pagingfiles.txt` |
| PF5 | `powershell -NoProfile -Command "Get-CimInstance Win32_OperatingSystem \| Select-Object TotalVirtualMemorySize,FreeVirtualMemory \| Format-List"` | rc 0; both KB-scale fields render — the commit-limit / available-commit pair (S277 does not cover these; the fields are host-identified, the values never judged here) | TotalVirtualMemorySize 35161444 / FreeVirtualMemory 1710148 at capture (KB) — ADJ-04: pressure attribution is mori's; this row is a capture point, not a judgment | `.ufo/waves/round-62/probes/pf5-commit-charge-fields.txt` |
| PF6 | `wmic pagefile list /format:list` (the r61 planned command's literal form) | the bare spawn FAILS at the CreateProcess layer — WinError 2, file not found: `wmic.exe` is ABSENT from this host (the D8 tool-absence class — the Store-alias stub was the first entry, a removed legacy binary is the second); the spawn failure crashes `tools/receipt-run.py` itself with an unhandled traceback, rc 1 and NO receipt (the R62-RECEIPT-RUN-SPAWN-FAIL class, mined in the round-62 lesson); the receiptable form wraps the command: `cmd /c wmic pagefile list /format:list` → cmd spawns, prints `'wmic' is not recognized as an internal or external command` rc 1 | none — absence is the invariant on this host | `.ufo/waves/round-62/probes/pf7-bare-spawn-crash-metareceipt.txt` (the crash, captured by redirecting the instrument's own stderr), `.ufo/waves/round-62/probes/pf6-wmic-absent-via-cmd.txt` (the receipted refusal) |

## PF1 — the usage counters are MB and one instance per pagefile

`Get-CimInstance Win32_PageFileUsage` (pf1 receipt, rc 0): one instance — `Name : C:\pagefile.sys`,
`AllocatedBaseSize : 18035`, `CurrentUsage : 4570`, `PeakUsage : 5287`. Per S277 every counter is
uint32 with units ("megabytes"): allocated ~17.6 GiB, current ~4.5 GiB, peak ~5.2 GiB at capture.
S277's AllocatedBaseSize text ties the value to Win32_PageFileSetting's InitialSize/MaximumSize range
"set at system startup" — which on THIS host is the automatic-management range (PF2/PF3/PF4), so the
number moves as the system grows the file; values are drift-class, the one-instance shape and the
MB-unit rendering are the invariants.

## PF2 + PF3 — the system-managed triad (the empty class S277 does not document)

The config question "is the pagefile system-managed?" is answered by a THREE-leg agreement: PF3
`AutomaticManagedPagefile` prints `True`; PF2 `Win32_PageFileSetting` returns rc 0 with an EMPTY
instance set; PF4 `PagingFiles` carries the `?:\pagefile.sys` wildcard with no explicit sizes. The
trap for a triage reader is PF2's shape: a naive probe treats an empty result as failure. S277 names
Win32_PageFileSetting in its cross-reference but documents nothing about the zero-instance behavior,
the AutomaticManagedPagefile flag or the registry store — the S274/S275/S276 documentation-gap class,
fourth appearance: the host contract is measured, the doc anchors the vocabulary only.

## PF5 — commit-charge fields, captured not judged

`TotalVirtualMemorySize` / `FreeVirtualMemory` (KB) render via the same CIM leg. These are the
commit-limit and available-commit counters a pressure investigation STARTS from; per ADJ-04 the
attribution work (which wave, which endpoint) is mori's — this row exists so the config plane's
receipts carry the fields beside the pagefile geometry, with values recorded and never judged here.

## PF6 — wmic is gone, and the absence has two layers

Layer one is the host: `wmic.exe` does not exist (bare spawn → WinError 2), so the r61 planned
command's literal form (`wmic pagefile list /format:list`) cannot run. Layer two is the instrument:
`receipt-run.py` does not catch the child-spawn failure — it crashes with an unhandled
`FileNotFoundError` traceback, exits rc 1 (outside its documented 0/1/2 exit map, which reserves 1 for
budget expiry) and writes NO receipt (pf7 meta-receipt, captured by redirecting the instrument's own
stderr). The receiptable form is the `cmd /c` wrapper (pf6): cmd itself spawns fine, prints the
`'wmic' is not recognized` refusal, rc 1. Rule for this host: legacy-Windows commands are probed
through a `cmd /c` wrapper FIRST (their absence becomes a receipted refusal), and the receipt-run
spawn-map gap is a planned repair, not something to route around silently.
