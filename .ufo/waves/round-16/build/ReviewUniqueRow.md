# ReviewUniqueRow — round 16 (static; baseline db68e62)

**Missing:** `tools/check-section-citations.py`, `corpus/knowledge/section-citation-errata-r16.{json,md}`, all R16 notices. Nothing executed. Tools installed: none.

**Baseline (read-only `git show`):** targets unique (host-health-report-r3.md:23/31; update-safety-v3.md:208/216). Wrong locators: host:581, v3:398.

**Findings:**
1. HIGH — Duplicate headings: legacy `section()` takes first match (check-root-dac-correction.py:49). Require exactly one.
2. HIGH — Duplicate JSON keys: plain `json.loads` is last-wins (check-locator-clarification.py:380). Use the measure-update-recheck.py:84 `object_pairs_hook`.
3. MED — Distinct ids, same path/heading/row_key: legacy id-only checks miss it. Require tuple uniqueness.
4. MED — Row: exactly one line-anchored match inside the section; quote must sit inside that row, not anywhere in the section.
5. MED — Section end undefined; §0 contains `### 0.1` (line 37). State the rule.
6. MED — Detector traps: v3:366 "v2's §7 ranks" is legitimate; the new notice re-quotes old locators.

**Gaps:** duplicate exit code (1 vs 2) unspecified; measure-update-recheck.py maps duplicates to CANNOT (2). S050 used-by targets the missing MD; census E11 likely [INFERENCE].
