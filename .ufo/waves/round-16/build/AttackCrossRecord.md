# AttackCrossRecord — R16 critic (static only)

Status: deliverables absent (`tools/check-section-citations.py`, `corpus/knowledge/section-citation-errata-r16.{json,md}` not found). Pre-implementation concerns; nothing executed or passed.

Falsifiers the gate must reject (add as fixed selftest cases):

1. **ID-only swap:** exchange the two `id` values; all other fields still resolve. Caught only by a hardcoded id→(path, heading, row_key, old_locator) table plus `notice_heading == "## <id> — citation-only erratum"`.
2. **Cross-file notices:** BOARD notice appended to `update-safety-v3.md`, RANK notice to `host-health-report-r3.md`. Require each notice in its own record's `path`, after `## R15-UPDATE-STATE`.
3. **Bare-token locators:** some valid citations use the same tokens: host-health:425 `§1's`, :526–547 `§5` (Provenance); update-safety:210/366 `v2 §7`, :271 `§1`. If :581 or :398 is deleted, a bare-token check still matches one of these. Match the full phrases `§1 verdict-board row 5` and `§7 rank 1 row “Do nothing now”` only inside the R15 section, count==1.
4. **File-scoped quote:** ``"`-Syu` would be INERT: 0"`` also appears at update-safety:398, and ``now `INERT` `` at host-health:353/582. The quote must be a substring of the resolved row. Reject `` `-Syu` `` (it appears in both rows).
5. A `## 5.` prefix also matches host-health:392. Require an exact full-line heading match.

Axes: depth (a false 0→2 count) and calibration.
