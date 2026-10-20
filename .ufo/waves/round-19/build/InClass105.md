# InClass105 — C1 inbound IN-105..IN-114

Counts: RESOLVES 7, DRIFTED 3, UNRESOLVABLE 0 [obs]. All 10 records operative (sibling_path `corpus/knowledge/service-optin-protocol.md` or `plans/round-9.plan.md`); owner lane tameshi-shokunin, sibling commit 01d586ddbc5f [obs: `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json`]. Draft: `drafts/InClass105.inbound.json`.

DRIFTED — owner handoffs (sibling files read-only):
- **IN-107** → tameshi, protocol.md:47, points `SKILL.md:558-568`. Content now `SKILL.md:570`; at landing da95290 it was 564 [obs: `git show da95290:SKILL.md`]. Replacement: heading `### Own-gate mutation — two revisions, never conflated (TSUKUROI-S5-1)` (`SKILL.md:563`) + quote "resolved as **fit, not gap**: the gate's `--selftest` satisfies the suite contract" (`SKILL.md:570`).
- **IN-109** → tameshi, protocol.md:153, points `tools/tsukuroi-census.sh:915-970`. Block moved: :915-970 now probe_drivers ring code [obs] (`tools/tsukuroi-census.sh:915`); round-5 marker now 2173, D14/D15 case 2216. Replacement: heading `# ---- hermetic selftest` (`tools/tsukuroi-census.sh:1710`) + marker `# ---- round-5 mutation hardening (lane S5-1, 2026-10-14): one case per survivor class` (`:2173`) + quote "check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED" (`:2216`).
- **IN-111** → tameshi, protocol.md:55, points `SKILL.md:599-609`. Rate line now 611 (605 at landing); range still holds sha aae45531 (`:605`) [obs]. Replacement: heading `### Own-gate mutation — two revisions, never conflated (TSUKUROI-S5-1)` (`SKILL.md:563`) + quote "MUTATE: DONE (target=tsukuroi-census-hardened defects=23 killed=23 survived=0 inconclusive=0 kill-rate=100%)" (`:611`).

RESOLVES: IN-105/106/113 `plans/round-5.plan.md:3-11` intact; IN-108 `plans/round-5-record-draft.md:76`; IN-110 `:316-319`; IN-112 `SKILL.md:616` inside [611,617] though the block tail now runs 618-619; IN-114 `plans/round-8.plan.md:45-47` [obs].

Undecided: none. Rejections: none. Model: commandcode/deepseek/deepseek-v4.1-flash [inf]. Shell: authorized git show/blame plus read-only JSON inspection (ls, wc, python3); no writes outside drafts [obs]. No admission authority; author-side draft only.

Scope: executed=ls, wc -l, python3 -c (census JSON x2), git show tameshi (x2) | sed, git blame (x3), git show da95290 (x2) | grep -n
