# NoticeForeign — round-18 freshness notice drafts for foreign-provenance-r6.md

Seat: TsukuroiR18-2.NoticeForeign (scribe). Target: `corpus/knowledge/foreign-provenance-r6.md` (baseline 842a5312, sha256 835d1b60… at HEAD; unchanged, no production write).

## Drafts written
- `.ufo/waves/round-18/build/drafts/Foreign.append.txt`: four `## R18-FRESHNESS —` sections.
- `.ufo/waves/round-18/build/drafts/Foreign.records.json`: four records, `R18-FRESH-Foreign-01..04`, zero `R18-CORR` records.

| Record | Baseline line | Now (capture) |
|---|---|---|
| 01 | 29-37 "entire history", 2109 lines | log 3169 lines (host-capture-r18.txt:60) [obs] |
| 02 | 47 "never updated" | log 3092 `pacman -U` elephant 2.22.1-1 (:72); log 3161 `pacman -U` zcode (:73) [obs] |
| 03 | 55 offline.db present (304318 B) | offline.db absent from sync dir (:48-54) [obs]; removal time [unk] |
| 04 | 194 "-Syu cannot move any" | omarchy.db mtime 2026-10-20 09:09:26 (:45) [obs]; current reachability [unk] |

## Checks run (read-only)
- Baseline quotes: each exactly once in `git show 842a5312:…`.
- Capture quotes: exact substring at the stated line of the tracked capture (committed 51dd9ee).
- `notice_heading` absent from baseline and present as a section; `now` and `capture_ref` appear inside each section.

## Findings and limits
- Line 47's "no update" is not current: `elephant-2.22.1-1` is the only base elephant dir in the local db (:30); its per-member ALPM event class is [unk] (log lines not read).
- zcode is not in the 16 of 2026-10-14; its foreign class is [unk].
- Line 194's "-Syu cannot move any" is superseded as current use only. The elephant update was `pacman -U`, not `-Syu`. Foreign class is not immutable; current repo reachability is [unk] because `pacman -Si` was not run (steer).
- **Blocker for production:** `S060` (fresh R18 capture) has no row in `corpus/SOURCES.md` in the current working tree (grep count 0). The planner or source-row owner must add it before the append. I did not add it.
- Capture was not hashed, so no new md5 is asserted for the log.

## Tools
None installed, updated or removed.

Scope: executed=read-only `git cat-file`, `git show`, `git ls-files`, `git status`, `git log`; `sha256sum`; python3 string and JSON checks on committed bytes and the capture file.
