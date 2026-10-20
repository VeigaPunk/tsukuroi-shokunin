# InClass040 — C1 inbound IN-040..IN-047

All eight records are `scope: historical` (sibling path begins `.ufo/`), so no owner handoff is exposed. Counts: RESOLVES 8 · DRIFTED 0 · UNRESOLVABLE 0. Draft: `.ufo/waves/round-19/build/drafts/InClass040.inbound.json` (8 objects).

Lane HEAD 452a054 = census `.lane_tip` [obs] (`git log -1`; `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:4`). Sibling prefix: `../mado-shokunin/.ufo/waves/`.

- IN-040 `round-16/w1/reports/SiblingBoundary.md:93` → `PROVINCE.md:59-60` RESOLVES [obs] `PROVINCE.md:59`: step 2 still keys the matching row on the question, not the binary.
- IN-041 `round-16/w1/reports/SiblingBoundary.md:98` → `PROVINCE.md:44-52` RESOLVES [obs] `PROVINCE.md:44,46,52`: ADJ packet header plus ADJ-01..ADJ-07 intact.
- IN-042 `round-17/w1/reports/SiblingOverlap.md:135` → `SKILL.md:101,404,427,734-756` RESOLVES [obs] `SKILL.md:427` root-exec clause; `:101` foreign deps and `:734-756` offline-exile inert.
- IN-043 `round-18/w1/reports/SiblingOverlap18.md:317` → `SKILL.md:734-756` RESOLVES [obs] `SKILL.md:734`: tension only — `:739` asserts "No update path and no repair path" while the sibling reports a `pacman.log:3095` elephant upgrade [inf]; claim conflict is mado/operator, locator sound.
- IN-044 `round-18/w2/reports/ConnProvinceScope.md:50` → `PROVINCE.md:48` RESOLVES [obs]: ADJ-03 routes "Desktop rendering, bindings, menu or idle behavior" to mado.
- IN-045 `round-19/w1/reports/ConnProvinceRoster.md:21` → `PROVINCE.md:48` RESOLVES [obs], same row.
- IN-046 `round-19/w2/reports/AtkProvinceLine.md:25` → `SKILL.md:47,50,108` RESOLVES [obs]: `:50`/`:108` carry the `[omarchy]` repo/SigLevel facts; cited `:47` holds only `omarchy-*` user-unit names, so that sub-pointer is mis-cited.
- IN-047 `round-20/w1/reports/ConnCriteriaFleet.md:37` → `corpus/QUALITY.md:40` RESOLVES [obs]: rule 30 count-correction sentence verbatim.

Rejected: none; undecided: none. No operative DRIFTED/UNRESOLVABLE exists, so there is no portable replacement or owner correction to propose; the IN-046 sub-pointer note is for reuse only.

Model: commandcode/deepseek/deepseek-v4.1-flash (runtime metadata).

Scope: executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log -1 --format='%H %d'
