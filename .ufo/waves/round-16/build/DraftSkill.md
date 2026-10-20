# DraftSkill — round-16 section-citation errata (draft; SKILL.md not edited)

Status: pre-implementation draft for L1 integration. `tools/check-section-citations.py`, `corpus/knowledge/section-citation-errata-r16.{md,json}` and both target notices do not exist in the worktree (checked by listing). No gate, selftest, build or git-history command was run by this seat. Tools installed or updated: none.

## Verified static findings

- Wrong locators exist exactly where routed: `host-health-report-r3.md:581` ("§1 verdict-board row 5") and `update-safety-v3.md:398` ("§7 rank 1 row").
- Targets resolve uniquely: `## 0. Verdict board` (:23) holds `| 5 | update-safety |` only at :31, quote "`-Syu` now `INERT`". `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` (:208) holds `| 1 | Do nothing now |` only at :216, quote "`-Syu` would be INERT: 0 candidates by three probes".
- Scope trap: `update-safety-v2.md:253` has an identical `| 1 | Do nothing now |` row; the gate must resolve within v3 §5 only. v2's own "§7 rank 1 row" notice (:372) is correct and not a defect.
- `host-health-report-r3.md:582` "§2.5" is correct (`### 2.5 update-safety`, :299); out of scope.
- S050 exists only as an uncommitted worktree row (`SOURCES.md` modified; absent from HEAD `db68e62`). `--revision` linkage fails until it is committed.
- `SKILL.md` (1834 lines) has no trailing newline; the append must begin with a blank line.

## Draft SKILL append (for L1 to paste at end of SKILL.md)

```
## Round 16 — section-citation errata

Two additive errata correct section numbers in the R15 current-use notices. They correct citations only; cited statements, R15 current-use supersession and the no-package/service authorization stand. Read `corpus/knowledge/section-citation-errata-r16.md` / `.json` (schema `tsukuroi-section-citation-errata-v1`) first.

- **R16-BOARD-SECTION** — `corpus/knowledge/host-health-report-r3.md`: the R15 notice's "§1 verdict-board row 5" is `## 0. Verdict board`, row `| 5 | update-safety |`.
- **R16-RANK-SECTION** — `corpus/knowledge/update-safety-v3.md`: the R15 notice's "§7 rank 1 row" is `## 5. Risk-ordered operations table (recommendation only — nothing here was run)`, row `| 1 | Do nothing now |`.

Wrong locators remain as historical text; each target gains one appended R16 notice. Current-use decision stays `corpus/knowledge/partial-upgrade-recheck-r15.md` (`BLOCKED_FOR_AGENT_PACKAGE_ACTION`). No package, service, host or repair action is authorized.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| section-citation | gate | `python tools/check-section-citations.py` or `--revision <REV>` (REV = `HEAD` or 4–64 hex) | 0 clean; 1 failed (bounded `R16-*` findings); 2 could-not-evaluate (`E-CLI`, `E-REVISION-INVALID`, `E-READ-FAILED`, `E-GIT-READ-FAILED`, `E-JSON-PARSE`) | `python tools/check-section-citations.py --selftest` (exit 0 pass, 1 fail; case count from measured run) | `tools/check-section-citations.py` constants: errata JSON/MD paths, schema `tsukuroi-section-citation-errata-v1`, `R16-BOARD-SECTION`/`R16-RANK-SECTION`, S050, baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5`, headings, row keys, quotes, old locators, notice headings | None; `git show <rev>:<path>` reads only; selftest in memory | tsukuroi |

The gate checks only committed citation predicates: two corrections, heading → unique row → exact quote at the named revision, R16 notices, S050 linkage, and old wrong locators accepted as history only when a valid notice resolves. It does not establish source truth, host state or current package status.
```

## Draft registry-row fields (gate and JSON, implementer reference)

- Errata JSON (`tsukuroi-section-citation-errata-v1`), `corrections[]` fields: `id`, `source_id`, `path`, `old_locator`, `heading`, `row_key`, `quote`, `notice_heading`.
- `R16-BOARD-SECTION`: S050; `corpus/knowledge/host-health-report-r3.md`; `§1 verdict-board row 5`; `## 0. Verdict board`; `| 5 | update-safety |`; "`-Syu` now `INERT`"; `## R16-BOARD-SECTION (2026-10-20) — section citation correction`.
- `R16-RANK-SECTION`: S050; `corpus/knowledge/update-safety-v3.md`; `§7 rank 1 row`; `## 5. Risk-ordered operations table (recommendation only — nothing here was run)`; `| 1 | Do nothing now |`; "`-Syu` would be INERT: 0 candidates by three probes"; `## R16-RANK-SECTION (2026-10-20) — section citation correction`.
- Proposed finding IDs (unimplemented): `R16-SCHEMA`, `R16-RECORD-COUNT`, `R16-HEADING`, `R16-ROW`, `R16-QUOTE`, `R16-NOTICE`, `R16-LOCATOR-UNNOTICED`, `R16-HISTORY`, `R16-SOURCE-LINK`, `R16-SUPERSESSION`.
- Notice bodies must name the wrong locator verbatim, the corrected heading and row, state citation-only supersession, and keep the R15 current-use and no-authority text.

## Limits and concerns

- Registry case count is deliberately unset: no selftest exists; L1 fills it from a measured run.
- Finding IDs are proposals until the gate exists; selftest expected IDs must be fixed by the implementer.
- Commit ordering: S050 and the notices must be committed before a `--revision` verdict can be comparable.
