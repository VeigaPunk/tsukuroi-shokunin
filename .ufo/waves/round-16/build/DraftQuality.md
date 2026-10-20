# DraftQuality: QUALITY23 draft (additive, not applied)

Baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5`. Static reads only; no QUALITY.md edit; no tests, gates, or host probes run. Tools installed or updated: none.

## Draft text (append as item 23 after item 22 in `corpus/QUALITY.md`)

23. **Section+row citations (R16-SECTION-ROW):** `path §N row K` (or `rank K`) resolves only if, at the named revision, exactly one Markdown heading equals the cited heading and exactly one table row under it contains the row key and a quoted stable substring. Line numbers are hints, never locators. A wrong section number stays as history; an appended, uniquely headed notice names the old locator verbatim, the resolvable heading, row key, quote and source, and supersedes only that citation (R15 current-use supersession unchanged). A claim that no other citation is wrong requires a recorded sweep command, scope and date (QUALITY9, QUALITY22). Admitted corrections record their resolver run in `## QUALITY check` (QUALITY14). Lesson: `corpus/lessons/round-15-verifier-spotcheck.md` § Routed defects and adjudication, items 1–2.

## Evidence (baseline)

- `host-health-report-r3.md:581` cites "§1 verdict-board row 5". Actual: `## 0. Verdict board` at :23; `| 5 | update-safety |` at :31.
- `update-safety-v3.md:398` cites "§7 rank 1". Actual: `## 5. Risk-ordered operations table…` at :208; `| 1 | Do nothing now |` at :216. v3 §7 is "Observation / inference / unknown".
- Trap: `| 1 | Do nothing now |` also appears at `update-safety-v2.md:253` under `## 7.`, and v2's notice (:372) cites it correctly. Resolution must be file-local, not corpus-wide.
- Other `§N row/rank` notices (`update-safety-note.md:501`, `update-safety-v2.md:371-372`) resolve by reading. This is not an exhaustive sweep.

## Proposed errata quotes (verify on the fixed revision)

- Board: `` `DEGRADED` (arm vocabulary) `` within `| 5 | update-safety |`.
- Rank: `Do nothing now`.

## Limits and blockers

- `corpus/knowledge/section-citation-errata-r16.json` does not exist yet; field names follow the spec contract.
- No `corpus/lessons/round-16.md` exists; the pointer targets the round-15 spotcheck.
- The criterion proves locator resolution only, not row truth.
