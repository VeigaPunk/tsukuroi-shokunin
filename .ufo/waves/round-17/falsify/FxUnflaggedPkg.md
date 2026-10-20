# FxUnflaggedPkg — C2 completeness wording
**Verdict: SURVIVES as a registry count; FAILS as stale-statement coverage.**

[obs] `freshness-recheck-r17.json` = 48 records over six files; **0** for package-state-plane (PSP), aur-risk-plane (ARP), foreign-provenance-r6 (FPR6). No `R17-FRESHNESS` heading: PSP:331/FPR6:317 are `R17-RECHECK` procedures; ARP none. Unflagged stale current-use claims (FC=fresh-capture.txt, BC=boot-chain-capture.txt):

- **PSP** :44 "1188" installed→1394 (FC:31); :75 "All four configured sync dbs"→five (FC:10-14); :82 "`offline.db` … Dead leftover file"→absent; :90 last local-db write 2026-10-13→09:39:21 (BC:67); :112 keyring "last data update ≈ Oct 11"→09:16:31 (sweep PL:2581); :143 "`paccache` not installed"→pacman-contrib 07:45:36 (BC:55); :277-279 "no rollback net is configured"→root+home (FC:42-45); :310 "No stale pin"→7.2.11 (BC:5).
- **ARP** :47 orphans→removed (BC:57,67); :48 "None of the 16 has ever been upgraded"→13 elephant →2.22.1 via `pacman -U` (BC:63); :98 "no … 'pacman -U' line anywhere"→BC:63; :103 "1275 entries"→db absent; :197 R1 "16/16"→13 moved.
- **FPR6** :29-37 "entire pacman history … 2109 lines … complete from install day to now"→line 3092 today (BC:63); :47 "No foreign package has ever been updated"→BC:63; :55 "`offline.db` — 304318 B"→absent; :194 "an `-Syu` cannot move any of them"→13 moved.

Wording: SCORECARD:505 says "stale current-use host statements carrying a dated R17 notice … Count `resolved_records`" — qualifier-scoped, no "all". No round-17 report is landed (`reports/` at dd15c18 has none); ConnPlannerWalk:18 discloses eight swept files with "no notice writer". [unk] final measured-outcome wording.

Scope: executed=none
