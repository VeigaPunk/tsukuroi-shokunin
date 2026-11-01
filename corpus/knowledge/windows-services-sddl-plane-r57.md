source: S268 S269 S270 (rows in `corpus/SOURCES.md`; S268 opened 2026-11-01, S269/S270 opened 2026-11-01) plus the dated host captures under `.ufo/waves/round-57/services-probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS, bash 5.3.15; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 30d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-57/services-probes/`) — next pass due 2026-11-30; re-run the probe commands of rows T19-T24 (all read-only or refusal-class), compare the observed signatures with the receipts; re-open S269/S270 on upstream content change and S268 on archive-side change (`is_archived: true`); a changed row gets an appended correction, never an in-place edit

# The Windows services plane, security-descriptor and metadata-query surface (round 57)

Scope: the same host-operability province as `windows-services-plane-r54.md` (T1-T8, `schtasks`
and `sc query`), `windows-services-plane-r55.md` (T9-T12, `sc queryex`/`sc qc`) and
`windows-services-config-plane-r56.md` (T13-T16, `sc config`/`sc failure`/`sc qfailure`); this note
extends the plane with the SERVICE SECURITY-DESCRIPTOR query (`sc sdshow`) and the metadata-query
surface (`sc qsidtype`, `sc qdescription`, `sc qtriggerinfo`, `sc enumdepend`). Every probe here is
read-only (all five queries) or refusal-class: `sc sdshow <nonexistent>` is refused by absence
(the 1060/rc-36 family) and `sc sdset <nonexistent>` is blocked by the SCM privilege gate BEFORE
any service could be resolved, so the surface is probed with zero mutation risk; an actual
descriptor change (`sc sdset` on a live service, `SetServiceObjectSecurity`) is operator-owned and
none was executed. All probes ran through the `receipt-run` instrument (each receipt carries its
own rc/argv metadata). Spelled for Git Bash: `MSYS_NO_PATHCONV=1` inside the receipt's bash -c
command string (r54 T1's class).

| id | question | probe (read-only or refusal-class, 2026-11-01) | healthy | error signature | action (operator-owned repair) | source |
|---|---|---|---|---|---|---|
| T19 | What does `sc sdshow` display for a live service, and what shape is the string? | `MSYS_NO_PATHCONV=1 sc sdshow wuauserv` | rc 0 and one `D:` line — the DACL component ONLY: `D:(A;;CCLCSWRPLORC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)` (`t19-sdshow-wuauserv.txt`); three AccessAllowed ACEs (AU, BA, SY), no O:/G:/S: components — S269's "unneeded components can be omitted" sentence is the direct anchor; the tool's own usage ("Displays a service's security descriptor in SDDL format", `t26-sdshow-usage-gate.txt`) matches S268's function sentence | A `D:`-only string is the healthy shape, not a truncation: owner/group components are omitted by design (`t27` decode: Owner/Group empty). The tool usage also names an optional `<showrights>` argument S268 does not document — doc-vs-tool gap recorded (the S266 `userown\|usershare` class) | Read the descriptor with `sdshow` before ANY permission question; treat the SDDL as one line, ACEs in parentheses | S268 (function sentence) + S269 (component grammar) + dated captures |
| T20 | How does the SD query fail on a nonexistent service, and does it stay zero-mutation? | `MSYS_NO_PATHCONV=1 sc sdshow No-Such-Service-r57probe` | (n/a — absence is the finding) | Refused by absence BEFORE any descriptor access: `[SC] OpenService FAILED 1060:` + "The specified service does not exist as an installed service." and process rc **36** (`t20-sdshow-nonexistent.txt`) — the same 1060/rc-36 family as query (T5), qc (T12) and the config/failure forms (T14/T15); function line plain `OpenService` | Probe name-validity of the SD surface with the nonexistent form; a real `sdset` on a live service is operator-owned | dated capture; family anchors S262/T5 |
| T21 | How is a service's SID type queried? | `MSYS_NO_PATHCONV=1 sc qsidtype wuauserv` | rc 0, `[SC] QueryServiceConfig2 SUCCESS`, `SERVICE_NAME: wuauserv`, `SERVICE_SID_TYPE:  UNRESTRICTED` (`t21-qsidtype-wuauserv.txt`) — the QueryServiceConfig2 surface (the same info class as T16's qfailure) carries SID type too | (none observed) — the value is drift-class (a service's SID type is owner-changeable) | Record SID type as evidence; changing it is operator-owned | dated capture |
| T22 | How is the description queried, and does the shorthand `qdesc` work? | `MSYS_NO_PATHCONV=1 sc qdescription wuauserv`; `MSYS_NO_PATHCONV=1 sc qdesc wuauserv` | `sc qdescription <svc>` → rc 0, `[SC] QueryServiceConfig2 SUCCESS` + `DESCRIPTION:` block (`t25-qdescription-wuauserv.txt`) | `sc qdesc` is NOT recognized on this build: full USAGE block at rc **103** (`t22-qdesc-wuauserv.txt`) — the T13 usage-gate class (option-validation precedes OpenService; rc 103 means "unknown command", never "service missing"); the query MUST be spelled `qdescription` | Never read the rc-103 usage dump as a service failure (T13's rule); spell `qdescription` | dated captures |
| T23 | What do the trigger and dependent-enumeration surfaces show for a live service? | `MSYS_NO_PATHCONV=1 sc qtriggerinfo wuauserv`; `MSYS_NO_PATHCONV=1 sc enumdepend wuauserv` | `qtriggerinfo` → rc 0, two `START SERVICE` triggers, both `GROUP POLICY` with GUIDs, flags `[MACHINE POLICY PRESENT]` and `[USER POLICY PRESENT]` (`t23-qtriggerinfo-wuauserv.txt`); `enumdepend` → rc 0, `[SC] EnumDependentServices: entriesread = 0` (`t24-enumdepend-wuauserv.txt`) — zero dependents measured | Trigger GUIDs and flags are drift-class (policy-owned); `entriesread = 0` is a capture, not a structural fact — a service installed later could depend on it | Report triggers/dependents as evidence; changing triggers is operator-owned | dated captures |
| T24 | Can the descriptor be decoded host-side, and how does the CHANGE surface fail for a read-only session? | `ConvertFrom-SddlString` on the T19 line (`t27-convertfrom-sddl-wuauserv.txt`, input `t27-input-sddl-line.txt`); `MSYS_NO_PATHCONV=1 sc sdset No-Such-Service-r57probe "<T19 string>"` (`t28-sdset-nonexistent-refused.txt`) | The decoder returns rc 0 and CONFIRMS the structure: 3 AccessAllowed ACEs (Authenticated Users, SYSTEM, BUILTIN\Administrators), Owner and Group empty — but it names the rights bits in FILESYSTEM/DS vocabulary (CreateDirectories, ExecuteKey, ListDirectory, FullControl), NOT service vocabulary: the host decoder is not an authority for the letter→SERVICE_* mapping | TWO refusal signatures, both BEFORE any service resolution: (a) the decoder's vocabulary mismatch (recorded, see Limits); (b) `sdset` fails at the SCM itself: `[SC] OpenSCManager FAILED 5:` "Access is denied." + rc **5** (`t28`) — the CHANGE surface is PRIVILEGE-GATED for this read-only session (BLOCKED class: the probe cannot run), never reaching OpenService; the assumed 1060 absence-refusal does NOT fire (the T13 assumed-order class again, measured) | Any `sdset` on a live service stays operator-owned twice over: it is a mutation AND it needs an elevated session; a rc-5 OpenSCManager denial is the privilege gate, not a service answer | dated captures; S270 (default-grants table, below) |

## Measured-vs-documented default (T19/T24, recorded as evidence — never judged)

S270 documents what a service object's DEFAULT security descriptor grants per account class
("Access Rights for a Service" → default table): local authenticated users get READ_CONTROL,
SERVICE_ENUMERATE_DEPENDENTS, SERVICE_INTERROGATE, SERVICE_QUERY_CONFIG, SERVICE_QUERY_STATUS,
SERVICE_USER_DEFINED_CONTROL; Administrators get DELETE, READ_CONTROL, SERVICE_ALL_ACCESS,
WRITE_DAC, WRITE_OWNER; LocalSystem gets the read/interrogate set plus SERVICE_START and
SERVICE_STOP. The measured descriptor (`t19`) decodes consistently against that table under the
Sddl.h service-letter mapping [inference — see Limits]: the BA ACE's 13 letters cover exactly the
Administrators grant set; the AU ACE's 6 letters overlap the documented local-authenticated set in
5 of 6 rights and additionally carry a start-class right while lacking the user-defined-control
letter; the SY ACE carries the FULL Administrators-class set where the documented default grants
LocalSystem only the read/control class; and the interactive-user/service ACEs many references show
are ABSENT here. All differences are recorded as measured evidence of THIS host's descriptor
(provenance [unknown] — a descriptor change is persistent, operator-owned and unobserved here;
S270's own warning: granting CHANGE_CONFIG/STOP to untrusted users allows LocalSystem execution).

## Limits

All field values are captures of 2026-11-01 and drift with the host: the descriptor is this
service's current DACL and may have been changed by its owner at any earlier time; SID type,
triggers and description are drift-class. The CC/LC/SW/RP/LO/CR-family letter-to-SERVICE_* mapping
is anchored to the Windows SDK Sddl.h constants and is NOT verifiable on the opened Learn pages —
the ACE-strings page (opened this round during sourcing) documents the SAME letter strings for
DIRECTORY-SERVICE rights (RP=READ PROPERTY, CC=CREATE CHILD, ...), a name collision: that table is
NOT transferred to service objects (the R15 positive-domain rule), and `ConvertFrom-SddlString`
(measured, `t27`) names the bits in filesystem vocabulary, so the mapping stands as [inference]
with the S270 default-grants cross-check as its only doc anchor. S268 is an ARCHIVED page
(`is_archived: true`, `ms.date` 2016-08-31, archive commit `c0efbd18…`) — the current Windows
Server commands reference carries NO sc-sdshow page at all (404 checked 2026-11-01), the same
archive-only grounding as S267; its Remarks pointer for SDDL syntax is a dead go.microsoft
redirect, so the grammar grounding comes from S269 (current Win32 reference) instead. The
`<showrights>` argument in the tool's own usage (T19) is undocumented on S268 and UNEXERCISED
here (its display semantics are operator-facing; exercising it has no diagnosis value this round).
No descriptor, SID type, trigger, description or dependency was changed on any service; every
mutation-class form (`sdset` on a live service) stays operator-owned. This note absorbs no
sibling scope.

## QUALITY check

- 2/3 (measured anchor; observation vs inference separate): every row cites a dated receipt under
  `.ufo/waves/round-57/services-probes/` or an S-row opened 2026-11-01; the letter mapping and the
  default-descriptor comparison are labeled [inference] with their anchors; [unknown] provenance is
  named (who changed the descriptor, if anyone — unobservable read-only).
- 7 (external claims cite S-rows): S268 (archived sdshow page, tier A for the sdshow function
  sentence), S269 (current Win32 SDDL string-format reference, tier A for the component grammar),
  S270 (current Win32 service access-rights reference, tier A for the default-grants table).
- 8 (header duty): the trio above; `recheck:` carries cadence + day-0 date + due date.
- 9 (negative claims carry sweeps): "no sc-sdshow page in the current reference" — `curl -s -o
  /dev/null -w "%{http_code}"` on the sc-sdshow URL → 404, 2026-11-01, while sc-query/sc-config
  → 200 (same session); "no service-rights letter table on the opened pages" — the S268/S269/S270
  fetches this round (ACE-strings opened and rejected as a source row, recorded in SOURCES as a
  rejection with its reason); "qdesc not recognized" — `t22` rc 103.
- 14 (explicit check): this section; performed before the landing commit.
- 21/22 (portable locators; positive domain): quotes anchored to page sections, no line numbers;
  the DS-rights table is NOT claimed to document service rights — the note claims only what each
  page actually says.
