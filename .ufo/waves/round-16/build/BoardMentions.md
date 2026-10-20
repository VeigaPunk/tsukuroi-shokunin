# BoardMentions — r3 board/current-use sweep

Baseline `db68e62` (static reads):

- `host-health-report-r3.md` (599 lines) has one verdict-board citation: line 581 (R15-UPDATE-STATE notice), "§1 verdict-board row 5". Wrong: heading `## 0. Verdict board` is line 23; row 5 is line 31, row_key `| 5 | update-safety |` (unique; heading unique).
- Line 425 "§1's 14:57:13Z capture" valid (§1 holds the gate run); 442 "§0.1's index" valid. No rank/§7 text here — rank defect is `update-safety-v3.md:398` — one notice only.
- Current-use refs: 578 heading, 583 "not current-use", 586 "For current use … read". Notice ends line 599; no-agent-package/service authorization at 596–599.
- S050 exists only uncommitted (`SOURCES.md:56`); baseline has 49 source rows, no S050. Errata JSON/MD and `check-section-citations.py` absent; no gate output observed.

Bound: append one unique-heading notice at EOF citing `## 0. Verdict board`, row 5/line 31, quote "`-Syu` now `INERT`" (unique); supersede citation only; preserve R15 current-use supersession and authorization; R16-BOARD-SECTION links S050.

Concern: the notice necessarily contains "§1"; gate old-locator detection must stay history-scoped and require notice resolution. Limits: no script/test execution; concurrent sibling edits to SOURCES/QUALITY observed.
