# ConnectPlanner — round-16 data-walk

Planner seat held by L1; this is a bounded walk. Tools installed: none. Static reads only.

**Defects** (baseline db68e62, verified):
- `host-health-report-r3.md:581` "§1 row 5" → `## 0. Verdict board`, `| 5 | update-safety |` (:31, unique).
- `update-safety-v3.md:398` "§7 rank 1" → `## 5. Risk-ordered…`, `| 1 | Do nothing now |` (:216, unique).
- Other R15 notices resolve; leave untouched.

**Measurement:** baseline corrections 0; exit 1 expected with both locators as findings [INFERENCE: precedent locator gate exit1/count0]. Implementation: corrections 2, exit 0. Spec leaves missing-file exit unpinned.

**Side effects:** S050 own-work, no URL (no W04); rows 49→50; A 41→42 if class A (census not run).

**Outside closure:** non-author checks `git show <commit>:` headings, rows, quotes; L1 alone runs gate.

**Concerns:**
- Notices must avoid line-number locators (QUALITY 21).
- SCORECARD :52 adjacency 7 is stale; :295–296 says 8.
- SKILL.md registry edit is shared; coordinate.
- Gate no-argument mode unspecified.

**Limits:** errata JSON, gate, S050 absent at read; nothing executed.
