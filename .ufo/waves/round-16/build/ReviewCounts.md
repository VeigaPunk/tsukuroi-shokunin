# ReviewCounts — R16 count 0→2

**Verdict:** not reproducible yet. At db68e62 the errata JSON, gate, both notices and S050 are absent (SOURCES ends at S049). Static reads only; nothing run or installed.

**Baseline:** `host-health-report-r3.md:581` cites "§1 verdict-board row 5"; actual `## 0. Verdict board` at :23, row at :31. `update-safety-v3.md:398` cites "§7 rank 1"; actual `## 5. Risk-ordered…` at :208, row at :216. Row keys are unique in their sections.

**Reproduction:** `--revision db68e62` → exit 1, count 0 (absent file; red evidence is the two wrong locators). `--revision C_impl` → exit 0, count 2. Log measurements in a later commit; C_impl cannot cite its own hash.

**Concerns:**
1. Count verified records (R15 rule: valid and not blocked), not `len(corrections)`. Baseline 0 reflects absence only.
2. Ordinal: log `depth 8→8 (0)`; SCORECARD:248 forbids count-to-score mapping.
3. Restored-defect proof needs selftest fixtures or a dangling `git commit-tree`; the worktree default is not blob-based.
4. Detector must match file bytes ("row 5", "rank 1"), not the lesson's "row5".
5. Spec is silent on absent-JSON exit; R15 recorded exit 1. Pin it.
6. S050 can be an own-work local row (precedents S031, S040) and must be appended.

**Limits:** no implementation or gate output exists to inspect; nothing is claimed passed.
