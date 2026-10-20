# ReviewHeading — round-16 heading-to-row isolation (static)

**Status: implementation absent. No pass claimed; nothing executed.**

Missing: `tools/check-section-citations.py`, `corpus/knowledge/section-citation-errata-r16.{md,json}`, and notices `## R16-BOARD-SECTION` / `## R16-RANK-SECTION` (grep finds the names only in `.ufo/waves/round-16/build` spec/dispatch text).

Baseline anchors (verified by read):
- `host-health-report-r3.md`: `## 0. Verdict board` L23; child `### 0.1` L37; next `## 1.` L65; row `| 5 | update-safety |` unique at L31.
- `update-safety-v3.md`: `## 5. Risk-ordered…` L208; row `| 1 | Do nothing now |` unique at L216; next `## 6.` L229.

Concerns before deliverable:
1. `section()` in `tools/check-source-scope-correction.py:54-64` ends only at `"## "`, so `### 0.1` rows leak into §0. Current keys do not collide; the gate must end at any ATX heading and needs a child-leak fixture.
2. `lines.index(heading)` takes first match; duplicate exact headings must FAIL.
3. Heading detection must skip fenced lines: host-health Appendix A fence contains `# ` comment lines.
4. Row uniqueness counts only the exact heading body.

Gaps: gate, selftest, and notice output unseen; no claim of passing.
