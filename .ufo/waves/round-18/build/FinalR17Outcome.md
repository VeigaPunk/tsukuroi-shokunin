# Round 17 falsify final outcome

[obs] Immutable census at `842a5312b704b5cda10fd80ec1fdee5fb381ba97`: 81 dispatched; **37 report files present, 44 absent**. Role mix (dispatch tasks, matching interim tally): reviewer 42, critic 7, sentinel 3, mutation-tester 4, scout 13, simplifier 2, connector 7, revenger 3. Exact lists are in `drafts/round17-outcome-final.json`.

**Present (37):** FxAuditMutants, FxAuditPrivilege, FxBindMutants, FxBindSectCita, FxBootedObserved, FxC2Rerun, FxC3Gameability, FxConnUnknowns, FxCritCalibration, FxFreshMutants, FxGateMutants, FxGodspeedW2, FxMdJsonAgree, FxNoHarm, FxOperatorChecks, FxOwnS052, FxOwnS055, FxPathAliased, FxSandboxSafety, FxScoutArchNewsDelta, FxScoutFindmnt, FxScoutLimineDocs, FxScoutMountMove, FxSentinelL0Advice, FxSimplifyBind, FxSourcesContract, FxSrcS021, FxSrcS022, FxSrcS053, FxSrcS054, FxSrcS057, FxSteerScopeFix, FxTypeBlindFix, FxUnflaggedBoot, FxUnflaggedMem, FxUnflaggedPkg, FxUnflaggedSkill.

**Absent (44):** FxAuditLiveAgree, FxAuditSelftest, FxBindLocaClar, FxBindRootDacCorr, FxBindSourScopCorr, FxBindUpdaRech, FxC1Rerun, FxC3Rerun, FxConnPlannerGap, FxConnSibling, FxConsistentPre42, FxEntryEfifallback, FxEntryLinux, FxEntryLinuxlts, FxEntrySnapshot1Linux, FxEntrySnapshot2Linux, FxEntrySnapshot2Linuxlts, FxFreshArchNewsGate, FxFreshDrivFirmPlan, FxFreshInitV42Sysr, FxFreshOverreach, FxFreshPartUpgrRech, FxFreshSnapEaccMech, FxFreshUpdaSafeV3, FxFrozenMarker, FxL0Correction, FxLessonGate, FxLogEntry, FxOwnS051, FxOwnS056, FxQuality2527, FxReadmeFrontier, FxRecheckBlocks, FxRecheckRerun, FxRejectedReadings, FxRevengerPlymouth, FxRevengerSnapperCopy, FxRevengerSwitchRoot, FxScorecardRound17, FxSeatScopeRerun, FxSeparability, FxSimplifyAudit, FxSkillContract, FxW04.

[obs] Frozen `outcome.json:14-73` says 29 delivered, 36 provider-429 dead, 16 running. Eight running seats later have files; eight remain absent. Closure confirms 29+8 / 36+8 and corrects the “39/43” brief (`round-17-verifier-spotcheck.md:89-95`). FxGodspeedW2 was already in the 29, not late (c53adee). Provider basis is the frozen aggregate error at `outcome.json:71`; registry entries contain only `item:null`, so the eight later-absent seats have no individual committed 429 receipts. Absence is confirmed; individual cause is not.

[obs] Uncited post-addendum changes: `cca3343` adds FxMdJsonAgree/FxSimplifyBind/FxSourcesContract, fixes S051/S055/S056 used-by and S057 search provenance (`SOURCES.md:57,61-63,105`; lesson:35). `661020f` changes only `SCORECARD.md:528` (shared binding plan) and `tools/check-revision-binding.py:2-5,334` (nine-gate wording); FxSimplifyBind itself landed in cca3343.

Sources: dispatch task census `dispatch.json:16-19,524-927`; final committed report-path census; interim `outcome.json:1-74`; closure cited above.

Scope: executed=read-only git/Python census at immutable revision; no host actions.


L1 integration provenance correction (round18): original outcome.json citations in this report name its immutable842a531 bytes, now preserved byte-for-byte at `.ufo/waves/round-17/falsify/outcome-interim-144309.json`. Mutable outcome.json is the reconciled37/44/0 summary, not the frozen interim. The36 names have a single aggregate429 label; they are not36 independent per-seat receipts. Final summary source pointers now use the retained interim path.

Scope: executed=read-only git/Python census at immutable revision; no host actions.
