# NoticeAur — round 18 aur-risk-plane notice draft

Target: `corpus/knowledge/aur-risk-plane.md` (baseline 842a531, unchanged at 51dd9ee).

## Behavior
- `.ufo/waves/round-18/build/drafts/NoticeAur.append.txt`: ten `## R18-FRESHNESS` sections plus one `## R18-RECHECK — steer-safe procedure` section. Historical bytes untouched; append-only.
- `.ufo/waves/round-18/build/drafts/NoticeAur.records.json`: ten records, `R18-FRESH-NoticeAur-01..10`. No `R18-CORR` records: no aur-risk statement was wrong at its own date.
- Checked in-process: every `baseline_quote` is a unique baseline substring; every heading is absent from baseline and occurs once in the appended suffix; each section contains its `now` and `capture_ref`; each `capture_quote` is a substring of its cited line.

## Evidence
- Orphans (:47): R17 `boot-chain-capture.txt:57` and `:67` (S051). Not re-measured at R18.
- Upgrades (:48, :98): R18 `host-capture-r18.txt:72` (elephant-2.22.1 `pacman -U`, 09:31:03) and `:73` (zcode, 13:23:08) (S060).
- Offline db (:103): R18 `:49-54` lists no offline.db.
- R1 (:197) and R2 (:198): `[unk]`; no sync-db or validation read at R18. The "13 moved" figure is R17-sourced.

## Findings
1. S060 is not in `corpus/SOURCES.md` at baseline. The sources lane must add it before any gate reads these records.
2. `check-freshness-r17.py` admits only R17 captures and uses `stale_reason`/`observed_now`. These R18 records need an R18 gate.
3. `check-recheck-commands.py` matches only `## R17-RECHECK — steer-safe procedure`. The R18 section is invisible to it, and line :347 has no backticks, so the gate stays green. Defect 6 is not closed by the gate.
4. Not reproduced: the R17 sweep's "sixth repo db" tally (FC:14). R18 lists five `.db` files. FC:14 was not re-read.
5. `zcode` is not in the 16-row register; its foreign status is `[unk]`.
6. The host-capture file is in the index; I did not verify its commit status.
7. No pointer-line or `pacman` argv0 appears in the RECHECK backtick spans.

Scope: executed=read-only lane git (show, ls-files) and file reads; in-process Python string checks; writes limited to the two drafts and this report. No host probes, no installs, no lane git mutation.
