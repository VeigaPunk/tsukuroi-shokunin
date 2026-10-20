# R18 ReviewReportCoverage — falsifier: r17 report vs uncited cca3343/661020f

**1. FAILS — tip coverage.** Report final bytes (fleet `e8645e9` 15:06:57) call `c53adee` "final evidence; lane tip" (`.ufo/reports/round-17/tsukuroi.md:3`) and `ed2ddd4` "lane tip" (:107). Real chain: `119d8bf` 15:06:55 → `cca3343` 15:17:23 → `661020f` 15:23:18 [obs, lane git log]. Zero grep hits for `cca3343|661020f` in all 120 report lines [obs]. Uncited, confirmed.

**2. FAILS — final wave counts.** `falsify/outcome.json` frozen 14:43:09: 81 dispatched, 29 delivered, 36 dead-429, 16 running [obs]; report :42 repeats 29/36/16. Committed tip bytes at `661020f`: 37 `Fx*.md`, all ⊆ 81 registry members, ∩ outcome-dead = ∅. Late delivered 8 (`still_running`∩tip): `ed2ddd4` ×4 (FxBindSectCita, FxC2Rerun, FxConnUnknowns, FxOwnS055), `3bce4d7` ×1 (FxSteerScopeFix), `cca3343` ×3 (FxMdJsonAgree, FxSimplifyBind, FxSourcesContract) [obs]. 8 running seats have no committed report (late dead: FxBindSourScopCorr, FxFreshUpdaSafeV3, FxFrozenMarker, FxReadmeFrontier, FxRecheckRerun, FxRevengerSnapperCopy, FxRevengerSwitchRoot, FxSeparability) [obs]. **Corrected final: 37 delivered / 44 dead / 0 running.** Report narrates late survivors (:104-107,:117-118) but never updates :42. "39/43" provenance UNPROVEN (no r18 prompt in lane) [unk].

**3. FAILS — message misattribution.** `661020f` message claims "FxSimplifyBind report"; its diff is only SCORECARD.md +1 and tools/check-revision-binding.py +7/−2 (docstring/description five→nine gates, comment-only); FxSimplifyBind.md was introduced by `cca3343` [obs].

**4. FAILS (minor).** Report :68 "Rows: 50 → 58"; tip grep −c = 59 (S059, `ed2ddd4`) [obs].

**Change classification (all uncited):** `cca3343`: three late Fx reports; SOURCES.md used-by S051/S055/S056 + S057 search-log wording — makes report :73 ("touched used-by S015/S016/S021/S022") incomplete; lessons/round-17.md correction log. `661020f`: SCORECARD planned C3 consolidation (`tools/_revision.py`, r18 prerequisite `51dd9ee`); tool docstring, no logic change — C3 census carries to tip [inf].

Residual risk: the 8 late deaths rest on `outcome.json` dead_error + report :107/:120, not a harness trace. `842a531` adds no falsify artifact [obs].

Scope: executed=git show/log/ls-tree (read-only), grep, sed -n, python3 json reads, cat
