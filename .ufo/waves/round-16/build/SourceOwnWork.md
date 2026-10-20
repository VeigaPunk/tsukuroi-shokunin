# SourceOwnWork

Verified via `git show` at db68e62065885b3f7463eb0a436c41f0dc3bcde5; targets unchanged.

- `host-health-report-r3.md:23` = `## 0. Verdict board`; row5 `:31`.
- `update-safety-v3.md:208` = `## 5. Risk-ordered operations table (recommendation only — nothing here was run)`; rank1 `:216`.
- Wrong locators preserved: `§1 verdict-board row 5` (`:581`), `§7 rank 1 row` (`:398`).

Quotes (exact, unique):

```
R16-BOARD-SECTION (10 words): `-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM` + `REQUIRES-PREP`; `-Suu`/`-Syyu` `DO-NOT`
R16-RANK-SECTION (15 words): No update action is owed today; the gate is the **next refresh**, not a run
```

Row-prefix fallbacks (9 words): `| 5 | update-safety |`; `| 1 | Do nothing now | official |`.

S050 proposal, 11 cells: source `Committed section anchors — corpus/knowledge/host-health-report-r3.md; corpus/knowledge/update-safety-v3.md`; own-work; A; scope `table locations the R15 notices mis-cite; locator only, not host, package or service authority`; anchor `exact headings above, rows 5/1; baseline db68e62; opened 2026-10-20`; teaches `board row §0, v3 row §5; §1/§7 wrong`; mined; 2026-10-20; 90d; used-by `corpus/knowledge/section-citation-errata-r16.md`.

Draft at `corpus/SOURCES.md:56` agrees; tighten its anchor to these exact headings.

Limits: `tools/check-section-citations.py` absent; no gate output observed. Pipe quotes need table escaping.
