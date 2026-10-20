# DraftLog — round 16 draft LOG entry (not appended to LOG.md)

Static reads only; no tests, gates, probes, package or service actions, no installs.

## Draft entry (to append to LOG.md after the gate and notices land)

## 2026-10-20 — round16 C1/depth section-citation errata

- **Motivation:** the independent round-15 closure (`corpus/lessons/round-15-verifier-spotcheck.md:133-134`, commit `db68e62`) routed two wrong section locators in round-15 notices. `corpus/knowledge/host-health-report-r3.md:581` cites "§1 verdict-board row 5"; the board is §0, row 5 at `:31`. `corpus/knowledge/update-safety-v3.md:398` cites "§7 rank 1"; the v3 table is §5, row 1 at `:216`. Both verified by static read.
- **Claim:** one, C1/depth. Corrections 0→2 (`R16-BOARD-SECTION`, `R16-RANK-SECTION`). Depth 8→8; adjacency 8 stays tied lowest; no ordinal uplift claimed.
- **Causal scope:** append-only. New `corpus/knowledge/section-citation-errata-r16.{md,json}`; appended notices in the two notes; new read-only `tools/check-section-citations.py` (reads `git show <revision>`); frozen selftest cases; one S050 SOURCES row. Historical bytes kept. R15 current-use supersession and no-package/service authorization preserved. Notices supersede citation only.
- **Checks pending (none run here):** gate red at baseline `db68e62` (expected exit 1, actual locator findings); green at the committed revision (exit 0); `--selftest` exit and finding ids; restored-defect runs; historical byte preservation; SOURCES census; non-author spot-check. No output is claimed passed.
- **Host action:** none. No pacman, package, service, or host probe; `~/.omp/agent/agent.db*` untouched. Notices make no fresh host-health claim. Host recovery and tooling-policy L0 stay operator-owned.

## Notes for the scribe (not part of the entry)

- At read time, `corpus/knowledge/section-citation-errata-r16.json` and `tools/check-section-citations.py` were absent; the entry must wait for them.
- SCORECARD terminal table (lines 47, 52) still shows adjacency 7; the round-13 text (about lines 294-296) and fleet-r1 corrections state adjacency 8. Cite the later text.
- Tree at read: only `.ufo/waves/round-16/` untracked; `db68e62` is an ancestor of HEAD `75d9f4f`.
