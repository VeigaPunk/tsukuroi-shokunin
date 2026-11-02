source: S278 (row in `corpus/SOURCES.md`, opened 2026-11-01, this round) plus the dated host captures under `.ufo/waves/round-63/probes/` of this repo
verified-at: 2026-11-01 (host: Windows 10.0.26200 x64 under Git Bash / MSYS; probes run 2026-11-01 via `tools/receipt-run.py`, read-only)
recheck: 180d from day 0 2026-11-01 (this note's own probes, receipts `.ufo/waves/round-63/probes/`) — next pass due 2027-04-30; re-run the probe commands of rows PW1-PW6 (all read-only), compare the observed SHAPES with the receipts (GUIDs, scheme lists, AC/DC indices and alias counts are drift-class config values, never judged); re-open S278 on upstream content change; a changed row gets an appended correction, never an in-place edit

# The Windows power-scheme config read plane (round 63)

Scope: the CONFIG READ contract of the power-scheme plane on this host — which scheme is active, what
else is installed, whether the machine can sleep at all, what the idle-timeout thresholds actually
are, and how the Git Bash / MSYS argv boundary mangles the tool's slash-form flags before spawn. This
is the r62 planned candidate ("a Windows power/battery CONFIG read (powercfg /q scheme/substring
read-only legs) ... with the MSYS boundary re-armed for its forward-slash flags"): every probe here is
a read-only config/state read; the values are DRIFT-CLASS captures — recorded as evidence, never
judged; the shapes, exit codes, refusal lines and the boundary conversions are the invariants. No
state-mutating leg (/change, /setactive, /hibernate, /import, /export, /energy, /batteryreport — the
report writers create files) was executed; every repair on this plane stays operator-owned. Boundary
(ADJ-04 discipline, same shape as r62): nothing here attributes host behavior to any fleet wave or
sibling lane — the plane is config reads only, and pressure/usage attribution stays with its owners.

Per S278 (Microsoft Learn "Powercfg command-line options", Windows hardware design; frontmatter
`ms.date` 2017-10-27, `updated_at` 2021-12-15T11:54:00Z,
`git_commit_id f99c5cba1552cac5708d338a2fae940b9aad202e`, fetched live 2026-11-01) powercfg "use[s]
the available sleep states, ... control[s] the power states of individual devices, and ... analyze[s]
the system for common energy-efficiency and battery-life problems", with the option table, the
`/query [scheme_GUID] [sub_GUID]` syntax and the alias mechanism ("These aliases may be used instead
of a GUID in any command"). All probes ran under Git Bash on 2026-11-01 through
`tools/receipt-run.py` (receipts `.ufo/waves/round-63/probes/`, dated 2026-11-01); unlike the r62
PowerShell legs, THIS plane's native flags carry forward slashes, so the MSYS path-conversion class
measured at RG5/DQ5 is not just re-armed here — it fires (PW5).

| Row | Surface (read-only) | Invariant (the judged signature) | Drift-class (never judged) | Receipt |
|---|---|---|---|---|
| PW1 | active power scheme identity | `powercfg -getactiveScheme` rc 0, one line of the shape `Power Scheme GUID: <guid>  (<name>)` | `cccd38e9-2d6d-48f3-9b5d-2266ea1b7d76  (Ultimate Performance)` at capture | `.ufo/waves/round-63/probes/pw1-active-scheme.txt` |
| PW2 | scheme inventory | `powercfg -list` rc 0; a BLANK FIRST LINE, then the `Existing Power Schemes (* Active)` header block, one `Power Scheme GUID: <guid>  (<name>)` line per scheme, `*` marking the active one (the marker agrees with PW1) | 4 schemes at capture: Balanced `381b4222-...`, High performance `8c5e7fda-...`, Power saver `a1841308-...`, Ultimate Performance `cccd38e9-...` * | `.ufo/waves/round-63/probes/pw2-scheme-list.txt` |
| PW3 | available sleep states | `powercfg -a` rc 0; the page's /availablesleepstates sentence — "Reports the sleep states available on the system. Attempts to report reasons why sleep states are unavailable." — matches the output shape: per-state unavailability WITH a reason line. On THIS host every listed state is unavailable: Standby S1/S2 (firmware does not support + internal system component disabled → `Graphics`), Standby S3 (internal component disabled → `Graphics`), Hibernate (`Hibernation has not been enabled.`), Standby S0 Low Power Idle (firmware does not support), Hybrid Sleep (S3 + hibernation + hypervisor), Fast Startup (hibernation) — the zero-available-states shape is the always-on-workstation invariant | none — the unavailability set IS the current state; re-judge if any state flips available | `.ufo/waves/round-63/probes/pw3-sleep-states-dash.txt` |
| PW4 | sleep/disk idle thresholds (the decision table) | `powercfg -q SCHEME_CURRENT SUB_SLEEP STANDBYIDLE` / `... HIBERNATEIDLE` / `... SUB_DISK DISKIDLE` each rc 0; every row renders the same skeleton: scheme + subgroup + setting GUID lines with `GUID Alias:` names, `Minimum Possible Setting: 0x00000000`, `Maximum Possible Setting: 0xffffffff`, `Possible Settings increment: 0x00000001`, `Possible Settings units: Seconds`, then `Current AC Power Setting Index` and `Current DC Power Setting Index` — the alias-form three-argument query (scheme + subgroup + setting) is the working read shape | at capture: STANDBYIDLE AC `0x00000000` / DC `0x00000258` (=600 s — the AC never-sleep / DC 10-minute asymmetry); HIBERNATEIDLE AC/DC `0x00000000`; DISKIDLE AC/DC `0x00000000` (consistent with PW3: hibernation disabled, never-idle workstation profile) | `.ufo/waves/round-63/probes/pw4-standbyidle.txt`, `.ufo/waves/round-63/probes/pw4b-hibernateidle.txt`, `.ufo/waves/round-63/probes/pw4c-diskidle.txt` |
| PW5 | MSYS slash-flag boundary (bash view) | bare `powercfg /list` and bare `powercfg /a` from Git Bash FAIL rc 1 with `Invalid Parameters -- try "/?" for help` — but the failure is MSYS argv rewriting BEFORE spawn, visible in the receipt's own `command=` line (shlex-quoted): `/list` arrived as `C:/Program Files/Git/list` (Git-root heuristic), `/a` as `A:/` (single-letter → drive-letter heuristic); `MSYS_NO_PATHCONV=1 powercfg /a` rc 0 with stdout byte-shape identical to the dash run (806 bytes) — the two workarounds are the dash aliases (host-measured, PW1/PW2/PW3/PW4) and MSYS_NO_PATHCONV=1. A bash-host boundary, not a powercfg defect: the same argv from cmd would arrive unconverted | none — the conversion signatures and the 41-byte refusal text are the invariants | `.ufo/waves/round-63/probes/pw5-list-slashform.txt`, `.ufo/waves/round-63/probes/pw5b-a-slashform.txt`, `.ufo/waves/round-63/probes/pw5c-a-noconv.txt` |
| PW6 | alias inventory | `powercfg -aliases` rc 0; GUID-pattern grep counts **33** alias rows on this host; the page documents the /aliases command ("Displays a list of aliases and their corresponding GUIDs") but enumerates NO names — the names are host-enumerated only | first alias rows at capture: `SCHEME_MAX`, `SCHEME_MIN`, `SCHEME_BALANCED`, `SUB_BATTERY`, `BATACTIONCRIT`, `BATACTIONLOW`, `BATFLAGSCRIT`, `BATFLAGSLOW` (the SCHEME_/SUB_/BATACTION_/BATFLAGS_ families; count 33) | `.ufo/waves/round-63/probes/pw6-alias-inventory.txt` |

## S278 documentation gaps (host-measured — the S274-S277 absence class, fifth appearance)

- The page documents ONLY slash-form options (`/list, /L`, `/query, /Q`, ...). It never states that
  dash aliases exist; every dash form used here is host-measured working (pw1/pw2/pw3/pw4 receipts).
- The page never mentions MSYS/Git Bash argv conversion. On this host the slash form of a flag is
  UNUSABLE from bash without `MSYS_NO_PATHCONV=1` (PW5/PW5b/PW5c) — the conversion happens before
  spawn, and the two failure argv shapes differ (`C:/Program Files/Git/list` vs `A:/`).
- Plain-scheme `/query` syntax on the page stops at subgroup granularity
  (`powercfg /query [scheme_GUID] [sub_GUID]`); the three-argument form appears only under overlay
  schemes. The measured `powercfg -q SCHEME_CURRENT SUB_SLEEP STANDBYIDLE` (scheme + subgroup +
  setting, ALIAS names) rc 0 — and the alias names themselves (SCHEME_CURRENT, SUB_SLEEP,
  STANDBYIDLE, ...) are not enumerated anywhere on the page; the host's `-aliases` output is the
  only name source here (PW6).

## Limits

Values are drift-class config state, recorded never judged (GUIDs, the scheme list, the AC/DC
indices, the 33-alias count). PW3's per-state reason lines are the tool's own wording (the
`Graphics` attribution is powercfg's, quoted not diagnosed). PW5's boundary is a bash/MSYS view
fact — the r56/r57 worktree-vs-bytes class in a different costume: the receipt's `command=` line is
the evidence that the mangled argv is what actually spawned. No sibling surface touched: power-scheme
config is this lane's host-operability ground; memory-pressure attribution remains mori's (ADJ-04,
restated in the scope paragraph, untouched here).
