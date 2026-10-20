# ReviewSchema — R16 correction schema binding and types

Status: implementation absent. Working tree shows only untracked `.ufo/waves/round-16/`; errata JSON/MD, `tools/check-section-citations.py`, and notices do not exist. Nothing passes.

1. **High:** S050 absent (`corpus/SOURCES.md` ends at S049). No owner writes it, so record→source linkage cannot pass.
2. **High:** `## 5.` also exists in `host-health-report-r3.md`; `## 0.` exists in `update-safety-v3.md`. Bind headings by exact line, scoped to each record's `path`.
3. **Medium:** Lesson forms "§1 verdict-board row5" and "§7 rank1" are absent on disk. Use `host-health-report-r3.md:581` ("§1 verdict-board row 5") and `update-safety-v3.md:398` ("§7 rank 1").
4. **Medium:** `| 5 | update-safety |` (host:31) and `| 1 | Do nothing now |` (v3:216) are unique. "Do nothing now" also occurs at v3:398, so scope quotes to the keyed row.
5. **Medium:** Require typed FAIL for non-object entries, non-string/null fields, unknown keys, duplicate ids, and shared path/row_key/notice_heading. R15 `plain()` turns None into "None"; avoid that coercion.
6. **Medium:** R15 maps malformed JSON to exit 2. Committed malformed JSON is a defect: FAIL(1). Reserve 2 for git/read failure.

Limits: static reads and read-only git (`cat-file`, `merge-base`, `status`, `rev-parse`). No tests, executions, or installs. Tools installed: none.
