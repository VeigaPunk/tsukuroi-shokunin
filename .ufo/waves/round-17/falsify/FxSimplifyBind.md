# FxSimplifyBind — C3 binding-copy divergence

**C3 SURVIVES** its probed surface; copies diverge off-probe. [obs]

All nine copies reject HEAD/@/refs and 6-hex (E-REVISION-INVALID exit 2); unlanded/landed agree. Judge counts 9 tools now, not 5 (check-revision-binding.py:36-54; stale "five" :2). tools/ clean, 3bce4d7-era tree.

Same input, different behavior:
1. Bad branch: locator E-CLI (check-locator-clarification.py:485); section E-BRANCH-INVALID (check-section-citations.py:925-928); measure E-REVISION-INVALID@branch (measure-update-recheck.py:475-477); root-dac/source-scope no validation → E-REVISION-NOT-LANDED (check-root-dac-correction.py:280-281; check-source-scope-correction.py:405-406).
2. rev=HEAD+bad branch: branch-first locator:484-487, section:925-931; rev-first root-dac:500, source-scope:402, measure:536+475.
3. merge-base rc≥2: E-GIT-FAILED (judge:110; check-seat-scope.py:184-189; check-recheck-commands.py:401-406; check-boot-chain.py:600-606; root-dac:272-276; section:446-451) vs silent "not ancestor" (locator:494-501; source-scope:392-393; measure:478-491; check-freshness-r17.py:374-375).
4. root-dac alone returns BOTH NOT-LANDED+NOT-PUSHED (root-dac:282-290; selftest :430); others raise first-only.
5. Missing branch: judge/seat E-BRANCH-MISSING (check-revision-binding.py:119-120; check-seat-scope.py:211-212); legacy five say NOT-LANDED.
6. `a..b`: recheck regex admits it (:39) → NOT-LANDED:416-425, elsewhere E-BRANCH-INVALID; trailing `a/` admitted (locator:36, section:64, boot-chain:91) → NOT-LANDED vs rejected by measure/seat/freshness.

Unverified: runtime (no execution); rc≥2 mapping code-read [inf]; origin-ref test variants (locator:498-499, source-scope:397, root-dac:286) equivalent for commits [inf].

L1-owned tools/_revision.py would collapse 1-5; judge text stays independent.

Scope: executed=date, git rev-parse, git log, git status --porcelain, stat
