# StaleMetadata Scout Report — Round 14 Repair

- Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` | Agent: `TsukuroiR14.StaleMetadata`
- Axis focus: Depth (claim C1 fidelity), Calibration (truthful contract documentation)
- Target: Audit r13 JSON metadata (`sources`, `gate_contract`), contrast with `tools/check-root-dac-correction.py` predicates, and specify minimum truthful supersession facts.

## 1. Grounded Evidence: Stale Metadata in root-dac-correction-r13.json

In `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.json`:
1. `sources[0].status` = `"reserved"`: Stale pre-integration draft artifact. In truth, S041 joined as `mined` on 2026-10-20 in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:47`, affirmed as `mined` in `root-dac-correction-r13.md:161,173` and `LOG.md:598` ("joined, not reserved").
2. `sources[0].registry_owner` = `"SourceRegistry"`: Stale swarm task seat identity from round-13 drafting, not an enduring registry entity or field in `SOURCES.md`.
3. `gate_contract` (lines 204-245) & `historical_bytes_check` (lines 187-203): Oversized residual specification from an abandoned 1568-line checker prototype (`corpus/lessons/round-13.md:99-102`), wholly unconsumed by the deployed checker.

## 2. Checker Predicate Contrast (tools/check-root-dac-correction.py)

The actual executable checker (`tools/check-root-dac-correction.py`, 375 lines) diverges from `gate_contract`:
- Headings mismatch: `gate_contract.required_md_headings` lists 10 headings; checker lines 100-105 check only 5 (`# Root-DAC...`, `## Corrected claim...`, `## Retained alternate...`, `## Historical cause...`, `## QUALITY check`). The other 5 headings are uninspected.
- Field scan unread: `gate_contract.corrected_field_scan` defines 13 JSON field paths; checker lines 127-154 inspect a hardcoded Python list of 8 variables plus alternative effects.
- Unexecuted rule & markers: `gate_contract.rule` asserts markers must exist at historical revision `70fede2a...` and be absent in r13. The checker never reads `historical_revision`, never checks git blobs at `70fede2a...`, and ignores `historical_bytes_check.markers` (8 strings). It tests 3 regex sites (`CURRENT-HOST`, `R13`, `B2-LIMIT`).
- Sources uninspected: Checker line 146 checks only `"S041" in universal.get("source_ids")`. It never parses `$.sources`, ignoring `status` and `registry_owner` completely.

## 3. Minimum Truthful Supersession Facts (Additive Architecture)

To resolve round-13 verifier spot-check defects #3 and #4 without rewriting historical bytes:
1. Preserve historical bytes: Historical bytes in `root-dac-correction-r13.json` and `.md` remain untouched.
2. Additive `r14_supersession` in `root-dac-correction-r13.json`:
   - `R14-S041-METADATA`: Records that `sources[0].status: "reserved"` and `sources[0].registry_owner: "SourceRegistry"` were superseded at round-13 integration when S041 joined `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:47` as `mined` under tsukuroi lane ownership.
   - `R14-GATE-CONTRACT`: Records that `gate_contract` and `historical_bytes_check` are unconsumed legacy draft specifications. The 375-line `tools/check-root-dac-correction.py` is the sole authoritative narrow conformance gate for round 13; no broader theorem or 10-heading enforcement is claimed.
3. Separation of Claims: These metadata repairs are supporting errata, not measured depth claims. Measured depth remains bounded to R14-VALUE-DOMAIN and R14-COMMENT-ATTRIBUTION in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/source-scope-correction-r14.{md,json}`.
4. Round 14 Gate Scope: `tools/check-source-scope-correction.py` must check the active r14 pair and supersession notices, treating r13 gate documentation as historical context rather than an active dependency.

## 4. Concrete Recommendations for Round 14 Implementation

1. `ActiveRefs` seat: Append an additive `r14_supersession` object to `root-dac-correction-r13.json` documenting errata `R14-S041-METADATA` and `R14-GATE-CONTRACT`. Do not mutate existing keys.
2. `CorrectEntry` seat: In `source-scope-correction-r14.md` and `.json`, cite `R14-S041-METADATA` and `R14-GATE-CONTRACT` under supporting metadata repairs, strictly distinct from the two measured depth corrections.
3. `CorrectionGate` seat: In `check-source-scope-correction.py`, evaluate the r14 active pair directly; do not couple r14 gate logic to `r13.json`'s unconsumed `gate_contract`.

## 5. Limitations

Read-only scout audit. No gate execution, selftest invocation, git commit, or write outside assigned report.

## 6. Tooling Record

Installed or updated: none. Used existing read tools. All operations strictly read-only within lane bounds.
