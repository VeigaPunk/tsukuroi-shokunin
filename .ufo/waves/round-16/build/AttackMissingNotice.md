# AttackMissingNotice — critic, round 16

Status: `tools/check-section-citations.py` and `section-citation-errata-r16.json` were absent when I read the tree. Nothing was executed. These are falsifiers the gate must exit 1 on.

- **F1 pre-existing heading:** set `notice_heading` to `## 0. Verdict board` or `## R15-UPDATE-STATE (2026-10-20) — current-use supersession` (host-health:23/578, v3:395). The JSON is valid, the heading already exists at baseline, and nothing is appended.
- **F2 wrong file/id:** append the board notice to v3, or swap the R16 headings between the records.
- **F3 bare pointer:** the exact heading plus only `See section-citation-errata-r16.md`.
- **F4 not appended:** insert the notice above line 578. Every baseline line survives, but R15's "bytes above" changes meaning.
- **F5 fake heading:** the heading appears inside a ``` fence, appears twice, or appears as `###`.
- **F6 copied matcher:** prior `section()` uses `lines.index` (first hit, no fences). `md14_notice_ok` uses `^## R15 supersession\b`, which also accepts suffixed headings.

**Axes:** depth, calibration.

**Fix:** pin both id→heading→path literals. The heading must be absent at baseline. At the revision it must be a single unfenced line after the baseline-byte prefix. The body must contain `old_locator`, `heading`, `row_key`, R15-UPDATE-STATE/partial-upgrade-recheck-r15 and no-package/service authorization. Add F1–F5 selftests.
