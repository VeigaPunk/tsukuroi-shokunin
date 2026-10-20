# ConnectMistakes: section drift and QUALITY21

**Observed (baseline 0db618a):**
- `host-health-report-r3.md:581` cites "§1 verdict-board row 5". The board is `## 0` (l.23), row 5 at l.31. Wrong.
- `update-safety-v3.md:398` cites "§7 rank 1". "Do nothing now" is `## 5` row 1 (l.216). Wrong. v3 §5 itself says "v2 §7's table", so the number was likely copied from v2 [inference].
- `update-safety-note.md:501` and `update-safety-v2.md:371-373` cite correctly.
- QUALITY21 covers external reader line numbers only. `tools/check-locator-clarification.py` LOC_NUM (l.34-36) does not match `§N` or `row N`.

**Draft criterion 23** (QUALITY.md ends at 22):
> 23. **Internal positional locators (R15-SECTION-DRIFT):** a pointer to another note's section, row or rank names the exact heading text plus a unique row_key or quote. Numbers are hints that must agree with that heading. Never copy a predecessor's numbering. Lesson: `corpus/lessons/round-15-verifier-spotcheck.md` § Routed defects 1–2.

**Testable prevention** (R16 gate, not run): resolve number to heading, then row. PASS: v3 `§5` with `| 1 | Do nothing now |`. FAIL: v3 `§7` with the same quote (no such row there). FAIL: host-health `§1` with row 5. Baseline must flag both defects, and the restored-defect check must pass before the repair counts. Scope to the 20 appended Erratum/notice blocks, not the 567 historical `§N` tokens.

**Limits:** headings embed numbers, so renumbering fails closed; match title text as a secondary check. Cause of the host-health `§1` error is [unknown]. Tools installed: none. No tests, gates, or scripts run.
