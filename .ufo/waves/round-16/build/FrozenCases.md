# FrozenCases — round-16 build report

Files changed: `.ufo/waves/round-16/build/frozen-cases.json` (new). Report: `.ufo/waves/round-16/build/FrozenCases.md`.

Behavior: 40 static expected vectors for `tools/check-section-citations.py` — each with mutation, expected exit (0/1/2), fixed finding-id set, and expected correction count. Covers clean/positive cases, baseline actual defects, missing/malformed/wrong-schema errata, count/id/field mutations, swapped path, mutated old_locator/heading/row_key/quote, notice-heading mismatch, correction-notice removal (x2), unlinked notice, notice scope overreach, R15-supersession deletion, defect laundering, history-prefix rewrite, restored locator, missing target, missing openers/headings, S050 source-row linkage, invalid revision/CLI probes, and a delivered-revision positive run.

Evidence (static reads only; no execution, no host probe):
- Baseline `db68e62`: defect text at `host-health-report-r3.md:581` ("§1 verdict-board row 5"; true `## 0. Verdict board` L23, row `| 5 | update-safety |` L31) and `update-safety-v3.md:398` ("§7 rank 1"; true `## 5. Risk-ordered…` L208, row `| 1 | Do nothing now |` L216). Baseline sha256: bfd1c422…e2dc3b / 84b3d6c5…69aa4.
- False-positive guards: legit §7 mentions v3:210,366; §1 mentions r3:262,425,442.
- Delivered errata pair + both `## R16-*-SECTION — citation-only erratum` notices verified present; S050 row added.

Reconciled with CitationGate post-delivery: 38/40 vectors adopted verbatim; `worktree-clean` renamed `revision-delivered` (gate is `--revision`-only per L1); `invalid-revision`/`invalid-cli` reclassified `gate-probe` (hermetic `revision_finding`/`cli_finding`); `board-field-missing` corrected to delivered semantics — FIELD/SOURCE defects leave notice binding intact, so no SECTION-CITATION-WRONG re-open, count 1.

Risks/limits: no execution; all vectors static. `R16-SOURCE-ROW` confirmed non-optional by CitationGate (SOURCES.md absent or `| S050 |` row not naming both targets; shared blocker, count 0). All 40 vectors now match delivered semantics.
