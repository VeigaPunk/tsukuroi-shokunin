# BoardAnchor — host-health-report-r3.md board anchor

[observed] Baseline db68e62 (HEAD; report byte-clean, 599 lines):

- Heading `## 0. Verdict board` at line 23; exactly one occurrence.
- Row key `| 5 | update-safety |` at line 31; exactly one occurrence.
- Row 31: `| 5 | update-safety | \`DEGRADED\` (arm vocabulary) | \`-Syu\` now \`INERT\`; after refresh \`UNKNOWN-UPSTREAM\` + \`REQUIRES-PREP\`; \`-Suu\`/\`-Syyu\` \`DO-NOT\` — detail §2.5 |`
- Proposed quote `` `-Syu` now `INERT` ``: one occurrence, inside row 31. Longer exact receipt fragment through `detail §2.5` also unique.
- Old wrong locator at line 581: `§1 verdict-board row 5`; one occurrence.

§1 misreference: line 65 is `## 1. The gate run (census-v2, four planes)`; lines 65–106 contain zero table rows, so a "verdict-board row 5" cannot resolve in §1. Only the numeral is wrong: quoted content is row 5, and the notice's §2.5 arm pointer is valid (heading line 299; composition lines 353–355). Correction: 1→0, append a new notice after line 599 preserving lines 578–599 (R15 supersession, no-package/service authorization).

[limits] Errata JSON/MD and `tools/check-section-citations.py` were absent at read time; no gate result is claimed. S050 is uncommitted (`SOURCES.md:56`) and absent at baseline, so record/source linkage needs a revision containing it.
