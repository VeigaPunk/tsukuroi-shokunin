# DraftIndex — round 16 README appendix (draft, not applied)

Scope: `corpus/README.md` draft only. No repo file was edited; `corpus/README.md` is unchanged. Read-only static reads of `corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-15-verifier-spotcheck.md:133-134`, `corpus/knowledge/host-health-report-r3.md:23,31,578-600`, `corpus/knowledge/update-safety-v3.md:208,216,366,395-410`, `.ufo/waves/round-16/build/spec.json`. No tests, builds, probes, or installs. Tools installed: none.

Findings:
- Both routed locator defects are real. `host-health-report-r3.md:581` says "§1 verdict-board row 5"; the board is `## 0. Verdict board` (line 23), row 5 at line 31. `update-safety-v3.md:398` says "§7 rank 1"; the table is `## 5. Risk-ordered operations table` (line 208), row 1 at line 216.
- The planned artifacts are absent at baseline `db68e62`: `corpus/knowledge/section-citation-errata-r16.{md,json}` and `tools/check-section-citations.py`. The appendix below says "planned" and must be reworded to "landed" only after L1 verifies them.
- Existing README convention (Rounds 13–15) puts correction pairs in a `## Round N` table section, not the Coverage map. Follow it.
- `update-safety-v3.md:366` refers to "v2's §7 ranks" as a legitimate v2 reference. Do not touch it.
- Appendix body exceeds the 180-word report bound because it is the deliverable; this cover note stays short.

## Draft appendix (append after the Round 15 section of `corpus/README.md`)

```markdown
## Appendix — citation-only repair versus new domain coverage

**Citation-only repair** changes where an already-held proposition is located
(section number, heading, table row or source pointer), keeps the proposition's
quoted text, and leaves the original bytes in place under an appended notice.
**New domain coverage** adds a plane, probe, measured anchor or claim the README
did not already hold, which shows up as a new Coverage-map row, an extended
`Holds` cell, or a graduated Frontier item.

| Test | Citation-only repair | New domain coverage |
|---|---|---|
| Change | locator fields of existing records, plus an appended notice | new note, plane, probe or measured anchor |
| Coverage map (top table) | no row added | row added or `Holds` extended |
| Frontier | unchanged | item closed or added |
| Sources | at most an own-work registry row pointing at committed corpus sections | new external rows for new claims |
| Host observation | none; no snapshot is retaken | dated read-only snapshot, if probed |
| Axes | depth and quality may move; coverage and expansion do not | coverage and expansion may move |
| Current use | unchanged; earlier supersessions stay in force | may add a current-use statement, which needs its own recheck |

Both kinds: neither refreshes host health, authorizes package or service
action, or closes the operator-owned pending partial-upgrade assessment
(`knowledge/partial-upgrade-recheck-r15.md`, `BLOCKED_FOR_AGENT_PACKAGE_ACTION`).
A citation notice carries no freshness claim. Before the correction commit,
sweep for superseded text (QUALITY criterion 10) and append the LOG entry
(criterion 11).

**Round 16 instance (citation-only).** Two routed locator defects from
`lessons/round-15-verifier-spotcheck.md` items 1–2:

- `knowledge/host-health-report-r3.md`: "§1 verdict-board row 5" → the board is
  `## 0. Verdict board`; row 5 is `| 5 | update-safety |`.
- `knowledge/update-safety-v3.md`: "§7 rank 1" → the table is
  `## 5. Risk-ordered operations table`; row 1 is `| 1 | Do nothing now |`.

The planned repair is two appended notices (`## R16-BOARD-SECTION — citation-only
erratum`, `## R16-RANK-SECTION — citation-only erratum`) and the pair
`knowledge/section-citation-errata-r16.{md,json}`. Corrections move 0→2 when the
gate passes. It is depth and quality, not coverage: no new surface, no host
repair, and no change to the R15 current-use notices. Register it in a
`## Round 16` table section, not the Coverage map. v2 `§7` references (for
example `update-safety-v3.md:366`) name v2 and stay as written.
```

## Limits
- Draft only; not appended to the README.
- Gate, JSON and MD targets are not yet on disk, so their "planned" status is unverified.
- Exact numbers (0→2, line numbers) are from the baseline and the spotcheck; re-check after the landing commit.
