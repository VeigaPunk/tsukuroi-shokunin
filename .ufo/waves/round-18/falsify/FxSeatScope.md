# FxSeatScope

## FAILS — P2: R18 build scope/auth mismatch

R18 `spec.json:3` says both “Read-only git allowed” and “Execute NOTHING unless item says EXEC-AUTHORIZED”; the scoped-marker rule controls this review, not retroactive broad permission. JSON query finds 17 marked item prompts; outcome `:16-23` records 80/81 reports and un-replaced invalid_prompt death. Static review of the delivered report trailers finds 42 non-`none` declarations without an item marker (not an executed gate result): `ConnL0:17, ConnMistakes:29, ConnSibling:29, CritDepth:29, CritOperability:23, NoticeAur:25, NoticeBootCorrections:24, NoticeForeign:31, NoticeHealth:24, NoticeJournal:24, NoticeKill:28, NoticeOom:20, NoticePackages:39, NoticeSkill:44, RevRegistryHistory:15, ReviewFrozen:14, ReviewIndependence:14, ReviewJudge:17, ReviewModule:14, ReviewMtime:24, ReviewReadme:15, ReviewReportCoverage:15, ReviewSeparability17:12, ReviewSourceImmutability:11, ReviewSources5156:8, SrcEarlyoom:18, SrcGitMerge:20, SrcSar:13, SrcSnapper:21, SrcZswap:22, Sweep01:22, Sweep02:18, Sweep03:33, Sweep05:24, Sweep06:28, Sweep07:17, Sweep08:29, Sweep09:24, Sweep10:28, Sweep11:18, Sweep13:17, SimplifyShared:32.` Examples: `NoticeForeign:31` discloses Git/Python reads; `SrcZswap:22` and `SrcGitMerge:20` disclose shell reads, despite prompts `spec.json:90,190,185` lacking authorization. Read-only commands remain execution. The four `none (...)` trailers at `CritDepth:29`, `CritOperability:23`, `SimplifyShared:32`, `Sweep07:17` also disclose commands; do not treat the `none` prefix as permission.

`MigFresh:10` uses `**Scope:**`; it is authorized (`spec.json:40`) but fails the gate’s exact `Scope: executed=` format (landed `patches/MigSeat.patch:41`; report line is not a valid declaration). `RerunExecLog` remains missing, not replaced (`outcome.json:19-23`). Static expected gate findings: 42 unauthorized, 1 undeclared, 1 missing; gate/exit not run. Required: retain deviations, normalize report syntax for future dispatches, clarify the conflicting spec sentence; do not add retroactive authorizations or replace the dead seat.

## SURVIVES — R17 pinned counts

`round-18.md:70` is correct: pinned `RerunSeats-build-output.txt:1-2` = 30 unauthorized, exit 1; falsify output `:1-2` = 19 unauthorized / 44 missing, exit 1. Lesson retains these as deviations, never retrospective authorization.

## UNPROVEN — residual / verification gaps

Self-reported trailers cannot prove absence of unreported execution; lesson `:85` says so, and the final immutable ledger is pending. `xd://lsp` is unavailable; read/grep were used for location only, with direct reads/JSON query for findings. No execution.

Scope: executed=none