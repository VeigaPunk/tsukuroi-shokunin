# DraftReportBounds — R16 C1/depth (draft wording)

Static reads only. No gate, selftest, build, or host probe run; no tools installed.

**Verified at HEAD db68e62:**
- `corpus/knowledge/host-health-report-r3.md:581` cites "§1 verdict-board row 5"; the board is §0 (heading :23, row :31).
- `corpus/knowledge/update-safety-v3.md:398` cites "§7 rank 1"; the table is §5 (heading :208, row :216).
- `corpus/knowledge/section-citation-errata-r16.json` and `tools/check-section-citations.py` are absent; all wording below is conditional.

**Draft wording**
- Depth (C1, tied lowest at 8): "Resolved section-citation corrections 0→2 (R16-BOARD-SECTION, R16-RANK-SECTION); gate verification pending at the implementation commit. Ordinal 8→8; no uplift."
- Quality: "Improved, provisional: two wrong locators superseded by notices; historical R15 bytes preserved."
- Expansion: "Unchanged; no admitted entries."
- Discernment: "Unchanged; no outside spot-check this round. R15 outside observations are not claimed here."
- Freshness, coverage, operability, calibration, adjacency: "Unchanged; no new surface, capability, host probe, or score."
- No-harm: "No axis harmed, conditional on gate exit 0 and selftest. R15 current-use supersession and no-package/service authorization unchanged. Package, pending-update, and host-state claims excluded."

**Concerns**
1. No-harm and depth wording cannot be verified until the errata JSON and gate exist.
2. "Quality improved" depends on LEARNING.md's supersession rule; L1 should confirm it or relabel as unprovable-but-better.
3. R15's 413-pending snapshot and source re-opens are R15 evidence; do not cite them as R16 observations.
