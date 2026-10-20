# RevRegistryHistory — r17 registry 53/44/23 + capability 44/44 vs measured 61/45/28

## Commit sequence ([obs], bytes at cited commit)
- **dd15c18** 13:55:01 — creates tools and registry/capability rows; counts then correct: boot-chain 53 (`len(cases)`=37 +11 +5; `tools/check-boot-chain.py:1017-1020`), audit 44 (`st_check` calls), binding 23 (24 textual checks, `absent-tool` dual branch → 23 executed; `tools/check-revision-binding.py:36-43,388-473`, five legacy gates; `RevBindMeasure.md`: 23 [obs selftest]).
- **90037c2** 14:34:30 — wave-2 repairs grow all three without touching SKILL.md/SCORECARD → drift begins. boot-chain cases 37→44, binding 11→12 → 61; audit +1 `e5-empty-uname-not-kernel` → 45; binding: dual branch collapsed, +4 stub-loop checks + `legacy-count` → 28; denominator five→nine (`R17_GATES` `:45-55`). Measured `.ufo/waves/round-17/measure/final/selftests.txt:1-11` (61/53/40/42/28/45); `c3-after.json` 9/9, legacy 5/5.
- **c53adee** 14:43:15 — SCORECARD section 45/45 (`:520`); dd15c18 capability row stays 44/44 (`:164`) — same-file contradiction.
- **ed2ddd4** 14:56:07 — +1 boot-chain case → 62; author-reported only (fleet report `:109`).
- **3bce4d7** 15:06:38 — appends SKILL.md:1916 "recheck … selftest 43"; row `:1900` still 40.
- **661020f** 15:23:18 — binding docstring now "nine gates"; SKILL.md:1902 still "all five"; SCORECARD `_revision.py` planned line.
- **51dd9ee** (r18) — SKILL.md:1897/1898/1902 still 53/44/23 "all five"; SCORECARD.md:164 44/44 vs :520 45/45. Drift persists.

## Failure cause
[inf] No reconciliation bound measurement to registry: rows were authored once at tool creation, never re-derived; wave-2 repairs changed counts and the binding denominator, measurements flowing only into the new SCORECARD section. Late additions entered as prose notes (SKILL.md:1916), institutionalizing divergence; 62/43 author-reported only. revision-binding row stale on three axes: count 23 vs 28, scope "all five" vs nine, exit-map "all five bound" vs 9/9. Stale at 51dd9ee: boot-chain 53 vs 61/62, audit 44 vs 45, binding 23 vs 28+five→nine, recheck 40 vs 43; freshness 53 and seat-scope 42 match.

Scope: executed=read-only git (log/show/diff/ls-tree/grep counts) in tsukuroi-shokunin and fleet; wrote this report only; no tool execution, no production edits.
