# RevSourceS151Reject — review of S151 Gate reject (LWN "Taming the OOM killer")

Verdict: holds — I agree with the reject decision, its stated reason, and its flip
condition. The quote and sha256 in the Gate row are accurate against the wave-1
snapshot; the live page's bytes differ only by a dynamically injected subscriber
ad block.

1. [obs] Quote verified verbatim. `grep -cF 'The badness score is computed using
   the original memory size of the process,'` returns 1 on both the wave-1 snapshot
   (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html`)
   and my fresh `curl -sL` fetch (saved at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevSourceS151Reject/lwn-317814.html`).
   It sits at line 113 of the wave-1 snapshot as the Gate row claims (line 121 in
   today's fetch — the ad block shifts it by 8). 13 words, within the 25-word cap.

2. [obs] Sha256 verified with a caveat that is not a defect. The wave-1 snapshot's
   sha256 is `b988b931cb476b36d93d523f9cd98195f45546930ac61a6657bc3fdf5966bcdc`,
   matching the Gate row (`corpus/lessons/round-29.md:14`) and the SOURCES row
   (`corpus/SOURCES.md:157`). My fresh fetch hashes to
   `1c33c5fabbb7cd15bbaa91355b7e7b15779a9ee26b0c0b7e7065976625a29b61` (105668 vs
   105310 bytes). `diff` shows exactly one change: an 8-line
   `<blockquote class="ad">` "Benefits for LWN subscribers" promo inserted after
   old line 58. Article body is byte-identical. The Gate pins the snapshot hash,
   which is the auditable artifact; the drift is LWN-side dynamic content, not a
   misrecorded hash.

3. [obs] The reject reason is factually correct on both sides. The article (wave-1
   snapshot lines 113–137) describes the 2009 heuristic: original memory size,
   CPU time (utime + stime), run time (uptime − start time), `oom_adj` shift,
   nice>0 doubling, CAP_SYS_RESOURCE/CAP_SYS_RAWIO divisors, cpuset divisor,
   child-memory halving. In v7.2 `oom_badness`
   (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c:199-237`)
   points = `get_mm_rss_sum + MM_SWAPENTS + mm_pgtables_bytes/PAGE_SIZE` plus
   `oom_score_adj * totalpages / 1000`; my own `grep -cE` over lines 199–237 for
   utime/stime, runtime, nice, capability, cpuset/mems_allowed, children, and
   `>>` shift all return 0. Every term the reason names is genuinely absent.

4. [obs] The mechanical part of the reason is accurate: `tools/check-owed-statements-r29.py`
   rule M6 (docstring lines 34–38, code line 172) accepts a basis source only when
   its registry row has status `mined` and its used-by names the target path; M7
   (lines 39–41) additionally requires a source opened 2026-10-22. A `rejected`
   S151 is inert for O01–O04 — which is what `rejected` is for.

5. [obs] Consistent with that, nothing treats S151 as a basis: `grep -rn 'S151'`
   over `corpus/knowledge/` and `SKILL.md` returns no hits; the O01–O04 markers
   cite only S148/S149/S150. The SOURCES row (SOURCES.md:157) has 11 cells,
   status `rejected`, recheck `on-release`, and a teaches cell that openly says
   "REJECTED for this round" rather than laundering content — consistent with the
   v2 battery's refused B5 forgery shape.

6. [inf] Judgment on the decision: reject is right and admit would be wrong. The
   article states no kernel version (SOURCES row: "no version pin"); citing a
   versionless 2009 secondary source against v7.2 mechanism statements would
   import an algorithm that no longer exists — worse than an uncorrected claim.
   Tier C is also never sole support (QUALITY.md:11 per ScribeSrcReject).

7. [inf] Judgment on the flip condition: sound and discriminating, not vacuous.
   It names a concrete re-admission path — an explicitly historical claim
   grounded in a version-pinned pre-`oom_score_adj` kernel file, with the article
   demoted to commentary — which preserves the primary/secondary distinction and
   cannot be triggered accidentally by any current O01–O04 claim (those are
   v7.2-behavior claims). One residual: no era-matched kernel file was fetched,
   so whether the article accurately describes its own era's code remains
   unverified [unk] — correctly flagged as such by the scribe rather than
   asserted.

8. [obs] Minor, non-blocking: the Gate row's "line 113" is snapshot-relative; a
   future verifier fetching live will find the quote at line ~121 due to the ad
   block. The row already guards this by pinning snapshot path plus sha256, so no
   change needed.

Scope: read=corpus/lessons/round-29.md:14, corpus/SOURCES.md:157, tools/check-owed-statements-r29.py:27-41,172-190, .ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html (lines 56-150), .ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c:195-240, .ufo/waves/round-29/w1/ScribeSrcReject/draft.md, corpus/knowledge/* and SKILL.md (S151 grep); wrote=.ufo/waves/round-29/w2/RevSourceS151Reject.md, .ufo/waves/round-29/w2/RevSourceS151Reject/lwn-317814.html; executed=curl -sL https://lwn.net/Articles/317814/, sha256sum, diff, grep -cF/-cE, sed
Model: not exposed
Installs: none
