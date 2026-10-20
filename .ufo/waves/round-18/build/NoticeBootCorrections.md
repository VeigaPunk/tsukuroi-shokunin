# NoticeBootCorrections — R18 C1 corrections for boot-chain-r17.md

Behavior: drafted four `R18-CORR` correction records for `corpus/knowledge/boot-chain-r17.md`, matching closure defect 3 in `corpus/lessons/round-17-verifier-spotcheck.md:189-200`. Target not modified; no production file touched.

| id | baseline line | baseline quote (842a5312, count 1) | corrected reference | capture check |
|---|---|---|---|---|
| R18-CORR-01 | :19 | `plus 13 named packages (B:59, B:82)` | 12 named packages | `boot-chain-capture.txt:59` lists 12 names [obs] |
| R18-CORR-02 | :41-42 | `and equals the installed /usr/lib/initcpio/init` | adds B:198 (linux-lts init) | :198 sha `62fcc3a9…` = :182, :251 [obs] |
| R18-CORR-03 | :45 | `byte-identical to the installed hooks (B:183–184, 252–253)` | adds B:199–200 | :199–200 = :252–253 [obs] |
| R18-CORR-04 | :88 | `The image file (mtime 09:26:22) is byte-identical to` | mtime is B:124; B:115 is the 09:29:18 history copy | :124 mtime 09:26:22 [obs] |

Drafts (only files written):
- `.ufo/waves/round-18/build/drafts/NoticeBootCorrections.append.txt` — four `## R18-CORRECTION —` sections, each with exact `now`, `capture_ref`, scope sentence (historical snapshot preserved; current-use only; no package/reboot clearance), source S051 (`corpus/SOURCES.md:57`).
- `.ufo/waves/round-18/build/drafts/NoticeBootCorrections.records.json` — 4 records, exact eight keys.

Validation (Python, read-only inputs): baseline quotes unique in `git show 842a5312…:…`; headings absent from baseline and unique; `now` and `capture_ref` inside each section; each `capture_quote` a substring of the cited line of S051 (working file equals HEAD `dd15c18`). All pass.

Findings [inf]:
- `BootChainTruthR17` report is not in the repository (grep of `corpus/` and `.ufo/` finds only the closure and round-18 build references). The fourth slip is taken from the closure's defect 3 breakdown, which splits `:40-42` and `:43-46` as separate slips.
- CORR-01's 12 count rests on B:59 alone; the sudo journal line B:82 names 11 (omits `linux-lts-headers`) and is cited only as the transaction record.
- Verdicts, `.json` twin, and historical bytes unchanged; no freshness records; no S060 citation (the corrected lines are S051 lines, not the R18 capture).
- Only the four cited lines were checked; the rest of the entry was not audited.

Scope: executed=`git show 842a5312…:corpus/knowledge/boot-chain-r17.md`; `git ls-files`/`git log -1`/`git show HEAD:` on the S051 capture; `grep`/`sed -n` reads of the entry, closure, S051 capture, and round-18 spec; Python (read-only validation plus writes to `build/drafts/` and this report). No installs, no pacman, no sudo, no production edits.
