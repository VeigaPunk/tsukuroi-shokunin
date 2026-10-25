source: S050 (`corpus/SOURCES.md`, row written by L1) — the committed target sections themselves at baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5`: `corpus/knowledge/host-health-report-r3.md` `## 0. Verdict board` row `| 5 | update-safety |` and `corpus/knowledge/update-safety-v3.md` `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` row `| 1 | Do nothing now |`; defect routing (motivation only): `corpus/lessons/round-15-verifier-spotcheck.md` § Routed defects and adjudication items 1–2.
verified-at: 2026-10-20 — static repository reads of the committed bytes at baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5` only; the locator predicates are evaluated against that pinned revision. No host probe, package transaction, service change, script execution or fresh host-health observation was performed.
recheck: 90d and on any change to either target file; procedure: confirm each named `## R16-*-SECTION — citation-only erratum` notice remains appended to its file, and that the JSON records' `heading`/`row_key`/`quote` still resolve in `corpus/knowledge/host-health-report-r3.md` §0 and `corpus/knowledge/update-safety-v3.md` §5; no host mutation.

This pair resolves only the two citation errata routed by the round-15 verifier spot-check. It edits no historical byte, makes no fresh host-health claim, and authorizes no package or service action. Machine-readable records: `corpus/knowledge/section-citation-errata-r16.json` (schema `tsukuroi-section-citation-errata-v1`).

## R16-BOARD-SECTION

**Defect routed by the verifier:** `corpus/knowledge/host-health-report-r3.md` `## R15-UPDATE-STATE` writes “The §1 verdict-board row 5 (`update-safety` `DEGRADED`, “`-Syu` now `INERT`”)”. The verdict board is **§0** (`## 0. Verdict board`), not §1; the cited row is `| 5 | update-safety |`, which reads “`-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM` + `REQUIRES-PREP`; `-Suu`/`-Syyu` `DO-NOT` — detail §2.5”. The quoted “`INERT`” wording is 2026-10-14 capture history.

**Correction:** the stable citation is §0 row 5 at `db68e62065885b3f7463eb0a436c41f0dc3bcde5`. A `## R16-BOARD-SECTION — citation-only erratum` notice is appended to `corpus/knowledge/host-health-report-r3.md` stating this; the R15 notice bytes are preserved.

**Supersession scope:** the section citation only. The quoted row content, the R15-UPDATE-STATE current-use supersession routing readers to `corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json`, and the no-package/service authorization boundary all stand.

## R16-RANK-SECTION

**Defect routed by the verifier:** `corpus/knowledge/update-safety-v3.md` `## R15-UPDATE-STATE` writes “The §7 rank 1 row “Do nothing now” (“`-Syu` would be INERT: 0 candidates by three probes”)”. In v3 the risk-ordered operations table is **§5** (`## 5. Risk-ordered operations table (recommendation only — nothing here was run)`), not §7 — §7 was the v2 table location the v3 text re-measured. The cited row is `| 1 | Do nothing now |`, which reads “`-Syu` would be INERT: 0 candidates by three probes; the only effect is the refresh mutation itself, which invalidates the emptiness”. The quoted “now”/“would be” wording is 2026-10-14 capture history.

**Correction:** the stable citation is §5 rank 1 at `db68e62065885b3f7463eb0a436c41f0dc3bcde5`. A `## R16-RANK-SECTION — citation-only erratum` notice is appended to `corpus/knowledge/update-safety-v3.md` stating this; the R15 notice bytes are preserved.

**Supersession scope:** the section citation only. The quoted row content, the R15-UPDATE-STATE current-use supersession, and the no-package/service authorization boundary all stand.

## QUALITY check

Performed on the bytes above at authoring, 2026-10-20. Author-side check only; the R16 gate (`tools/check-section-citations.py`, CitationGate-owned) has not been run by this seat and no gate verdict is claimed.

| # | Criterion | Evaluation |
|---|---|---|
| 1 | Falsifiable | Each correction is bound to one resolvable heading + unique row_key + quote at a named revision; wrong-locator predicates are checkable at `db68e62`. No host-state claim. |
| 2 | Measured anchor | Anchors are committed-byte coordinates: file paths, exact heading strings, row keys, quotes, and pinned revision `db68e62065885b3f7463eb0a436c41f0dc3bcde5`; no oral knowledge. |
| 3 | Observation / inference / unknown | Row/heading/quote locations are observations over committed bytes; defect causes (v2 numbering carried into v3) are stated as description of bytes, not host inference; no unknowns asserted. |
| 4 | Append-only | No r15 or older byte edited; both notices and this pair are additive. Verified at authoring: only `PUT >$` tail appends and new-file writes were issued. |
| 5 | Rejection kept | The wrong locators remain readable verbatim at `host-health-report-r3.md:581` and `update-safety-v3.md:398` as preserved history; nothing is silently dropped. |
| 6 | Pacman advice | Not applicable as advice; the notices quote package-command text only as historical table content and repeat the standalone authorization boundary. |
| 7 | S### citation | `source_id` S050 refers to the L1-owned `corpus/SOURCES.md` row naming the committed target sections at `db68e62`; this seat did not write or validate that row. |
| 10 | Mention sweep / tables | The superseded locators are intentionally unedited history in append-only files; a sweep that “fixed” them would violate criterion 4. Table-column integrity: this pair adds no tables besides this checklist. README/SKILL/corpus-index edits are L1-owned. |
| 14 | Performed check | This table evaluates the bytes of this entry and its pointers resolve to the named files, headings, rows and revision; it does not claim the R16 gate passed. |
| 21 | Portable locators | Corrections use stable heading text + row key + quote + pinned revision; no reader line number is used as a locator in the JSON. |
| 23 | Section/table citation resolution | Each record resolves `heading` → unique `row_key` → `quote` inside the cited file at the pinned baseline; the actual wrong-section locators are preserved as history and resolved only by the appended named notices. |

## Scope notes

- Neither correction asserts current host state; both notices restate that the R15 supersession and the `BLOCKED_FOR_AGENT_PACKAGE_ACTION` posture are unchanged. The quoted “now”/“today” wording inside the cited rows is 2026-10-14 capture history, not a fresh observation.
- `source_id` S050 names the committed target sections at baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5` (own-work row written by L1 in `corpus/SOURCES.md`). `corpus/lessons/round-15-verifier-spotcheck.md` is the motivation routing these defects, not the source.
