# DraftScorecard — round 16 template (unapplied)

Baseline `db68e62065885b3f7463eb0a436c41f0dc3bcde5` (HEAD verified). SCORECARD.md not edited. Tools installed: none.

## Declaration (paste before runs)

## Round 16 — citation correction C1/depth (2026-10-20)

| Claim | Axis | Delta | Before → after (declared) | Counting command |
|---|---|---|---|---|
| C1 R16-BOARD-SECTION / R16-RANK-SECTION | depth | 8→8 (0) | corrections 0→2; exit 1→0 | `python tools/check-section-citations.py --revision <commit>` (absent at baseline) |

Depth and adjacency tied lowest at 8; no ordinal uplift. Citation-only; R15 supersession and no-package/service authority unchanged. Planned: independent closure. Retired: none.

## Outcome template (fill from observed output only)

### Round16 measured outcome

| Claim | Axis | Delta | Measured before → after | Verdict |
|---|---|---|---|---|
| C1 R16-BOARD-SECTION / R16-RANK-SECTION | depth | 8→8 (0) | corrections `<n0>`→`<n1>`; exit `<e0>`→`<e1>`; findings `<f0>`→`<f1>`; `db68e62`→`<impl>`; selftest `<exit>` `<passed>/<cases>` | `<pending>` |

`improved, author-verified` only if: baseline exit 1 / count 0 names both wrong locators; implementation exit 0 / count 2 / findings 0; selftest and restored-defect finding ids match; history bytes preserved. Failed arm → `not improved`. Exit 2 → `could-not-evaluate`. Never `admitted`.

## Findings (static reads only)

- Board row `| 5 | update-safety |` sits under §0 (`host-health-report-r3.md:23,31`); R15 notice `:581` cites §1.
- Rank row `| 1 | Do nothing now |` sits under §5 (`update-safety-v3.md:208,216`); notice `:398` cites §7 (heading `:269`).
- Concern: a missing errata file at baseline must exit 1, not 2, or the red run is not defect proof.
- Concern: the counting command does not exist yet; no value above is measured.
