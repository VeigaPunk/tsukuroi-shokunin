# ReviewMDJSON — round-16 (static)

**Blocking:** errata JSON/MD, gate tool, and R16 notices are absent; MD/JSON agreement is untestable.

**Verified bytes:**
- `host-health-report-r3.md:581` cites “§1 verdict-board row 5”; actual `## 0. Verdict board` L23, row L31.
- `update-safety-v3.md:398` cites “§7 rank 1 row”; actual `## 5.` table L208, row L216.
- S050 exists (`SOURCES.md:56`); its used-by names the absent MD.

**Findings:**
1. JSON `quote` values are unspecified; fix one exact substring per record, shared by MD, JSON, gate.
2. Lesson shorthand “row5”/“rank1” is not file text; `old_locator` must copy “§1 verdict-board row 5” and “§7 rank 1 row”.
3. No contract check ties MD headings, quotes, row keys, recheck to JSON and S050; add one.
4. Do not flag `update-safety-v2.md:371–372`; its “§6”/“§7 rank 1” are correct. A bare “rank 1” detector false-positives.
5. “Citation-only” is not machine-checkable; require a fixed scope sentence per notice.
6. Entry `verified-at:` must cite static reads, not host probes.

**Limits:** static reads only; nothing executed; em-dash headings must match byte-for-byte. Tools: none installed.
