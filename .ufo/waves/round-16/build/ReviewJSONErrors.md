# ReviewJSONErrors (round 16, static)

**Status:** gate and errata JSON absent at `db68e62` and in worktree. Findings come from predecessor gates, read not run. Installs: none.

**Findings**
1. Root-DAC gate crashes on non-object JSON (unguarded `.get` in `json_sites`/`json13_issues`; `main` has no catch-all). `[]` exits 1 by traceback, like FAIL.
2. R14/R15 exit 1 for non-object roots and unknown schema; R14 selftest `top-level-array` pins this.
3. `measure-update-recheck.py` L503/L419 maps every finding to 2.
4. Absence conflicts: root-DAC→2, R14/R15→1, measure→0.
5. R14/R15/root-DAC `json.loads` silently keeps last duplicate key.
6. R14 accepts extra keys; R15 rejects them.
7. No selftest removes a required key or sends a non-object record.

**Requirement:** 2 = unparseable, duplicate/NaN keys, non-object root, missing/unknown schema, unresolvable revision, uncaught error. 1 = v1 object violating rules, including absent errata (red baseline). Copy measure's loader; reject extra keys; selftest each exit and ID.

**Baseline:** S050 absent at `db68e62` (worktree-only); linkage must read the pinned revision.
