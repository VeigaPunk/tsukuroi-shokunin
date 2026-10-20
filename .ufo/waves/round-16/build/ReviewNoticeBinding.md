# ReviewNoticeBinding — round 16

Static reads only (baseline db68e62 plus working tree). No gate, test, or host probe run. Tools installed: none.

Missing: `tools/check-section-citations.py`. Present, uncommitted: errata JSON/MD, two R16 notices (+16/+17 lines, 0 deletions), SOURCES S050.

## Findings

1. **HIGH — whole-file quote matching is generic.** RANK quote "`-Syu` would be INERT: 0 candidates by three probes" already appears in v3's R15 notice (lines 398–399, wrapped). Match quotes inside the resolved row only.
2. **HIGH — wrong-locator detection must be per-file, resolution-based.** v2's R15 notice "§7 rank 1 row" is correct (v2 §7 row at 253). Pattern-only detection false-fails it.
3. **MED — do not copy R15 gate patterns.** `md14_notice_ok` accepts keyword presence; `section()` returns None and `or ""` fails open; `lines.index` ignores duplicate headings.
4. **MED — S050 linkage conflicts.** Errata MD names S050 as the round-15 lesson; SOURCES S050 names the two target files (self-referential). Pick one.

## Verified

JSON headings, row keys, quotes resolve at baseline (host-health row 31; v3 row 216). Notices are append-only. Only the two routed locators are wrong.

## Gate must

Heading count==1; row count==1 within heading; quote inside row; notice block contains heading/row/quote; path match; exactly two records; baseline prefix preserved; fail closed on missing heading; selftest fixtures.
