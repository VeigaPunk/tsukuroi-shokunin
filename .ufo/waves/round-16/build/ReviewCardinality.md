# ReviewCardinality — round 16 (static, baseline db68e62)

**Missing:** errata JSON/MD, `tools/check-section-citations.py`, both notices, and S050 are absent. Only untracked `.ufo/waves/round-16/` exists. No pass claimed.

1. **Corpus-wide baseline is 4, not 0:** `source-scope-correction-r14.json` (2) and `source-locator-clarification-r15.json` (2). The 0→2 metric holds only per-file on `section-citation-errata-r16.json`.
2. **Exactly two wrong locators:** `host-health-report-r3.md:581` (§1→§0) and `update-safety-v3.md:398` (§7→§5). Baseline detections are not resolved corrections. Valid v2 §7 rank 1 (line 253) and note §7 row 2 (line 344) must not count.
3. **Row keys are unique only within their heading:** `| 1 | Do nothing now |` appears at v2:253 and v3:216; `| 5 | update-safety |` also appears in round-15 `mention-sweep.json`. Resolve path→heading→row; fail unless exactly one match.
4. **Require `len(corrections)==2` exactly**, distinct ids and distinct (path, heading, row_key), and each `notice_heading` in its record's own file. Swapped or duplicate records must fail.
5. **S050 absent** (last S049; 49 rows). Count 50 only as own-work, never as external authority.

**Limits:** static git reads only; nothing executed; selftest fixtures unseen.
