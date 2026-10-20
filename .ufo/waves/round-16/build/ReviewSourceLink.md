# ReviewSourceLink — round 16 (S050)

Static reads only; no execution; no installs.

1. **MEDIUM — misattributed source.** `corpus/knowledge/section-citation-errata-r16.md` says S050 refers to `round-15-verifier-spotcheck.md`. Registry S050 (`corpus/SOURCES.md:56`) names the two committed notes; the lesson is routing origin only.
2. **MEDIUM — incomplete linkage.** `section-citation-errata-r16.json` carries `source_id: S050`, but S050 `used-by` lists only the `.md`. Census E11 checks path existence, not linkage.
3. **LOW–MEDIUM — tier A unbacked.** Contract tier A requires primary sources or re-runnable gate output. The gate is absent and the MD recheck is manual reads. Keep A only once the gate lands.
4. **LOW — "search" framing.** `corpus/SOURCES.md:94` presents own-file re-reads as a search with "included as support". Relabel as own-work locator re-read.
5. **LOW — recheck.** `90d` on pinned baseline bytes is meaningless; use change-triggered recheck.

**Verified:** both wrong locators exist at db68e62 (`host-health-report-r3.md:581` §1; `update-safety-v3.md:398` §7). Headings and row keys are unique; quotes are exact substrings; §2.5 is valid, so only two defects; notices are append-only (0 deletions).

**Missing:** `tools/check-section-citations.py`, selftest, red/green runs. Gate must resolve notice headings at the landed revision, not baseline; spec is silent.
