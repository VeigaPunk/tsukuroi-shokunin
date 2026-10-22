# ScribeSrcReject — S151 LWN "Taming the OOM killer" reject draft

Verdict: done — S151 is drafted as a rejected source row and a Gate reject row; the 2009 heuristic the article describes diverges from v7.2 `oom_badness` on every scoring term, so admit is not the better reading.

1. [obs] The article opened by plain `curl -sL` with HTTP 200, 105310 bytes, no challenge, saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html`, sha256 `b988b931cb476b36d93d523f9cd98195f45546930ac61a6657bc3fdf5966bcdc`. Identity: `<h1>Taming the OOM killer</h1>` line 56, `<p>February 4, 2009</p>` line 60, `<p>This article was contributed by Goldwyn Rodrigues</p>` line 61, `<h3>Who's Bad?</h3>` line 104. The page states no kernel version, so only the hash pins its bytes.

2. [obs] The v7.2 counterpart was fetched the same way: HTTP 200, 34311 bytes, 1257 lines, saved at `.../ScribeSrcReject/oom_kill-v7.2.c`, sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`; `long oom_badness(...)` is at line 199.

3. [obs] The 2009 score, as the article states it: original memory size, CPU time `utime + stime`, run time `uptime - start time`, and `oom_adj` (saved HTML lines 113-115); longer life lowers the score (117); swapoff first (120-122); half of each child's memory added to the parent (124); nice > 0 doubles (131); `CAP_SYS_ADMIN`/`CAP_SYS_RESOURCE`/`CAP_SYS_RAWIO` divide by 4, cumulative to 16 (134-137); cpuset mismatch divides by 8 (138-140); final shift by `oom_adj` (142-145); highest score selected and children killed (149-150).

4. [obs] v7.2 `oom_badness` (`oom_kill-v7.2.c`) returns `LONG_MIN` for global init or `PF_KTHREAD` (lines 160-167 called at 204) and for `OOM_SCORE_ADJ_MIN`, `MMF_OOM_SKIP` or `in_vfork` (216-222); its score is `get_mm_rss_sum + MM_SWAPENTS + mm_pgtables_bytes/PAGE_SIZE` (228-229) plus `oom_score_adj` scaled by `totalpages/1000` (233-234). Whole-file `grep -cE` counts are 0 for `nice`, `utime`, `stime`, `uptime`, `start_time`, `CAP_SYS_ADMIN`, `CAP_SYS_RESOURCE` and `CAP_SYS_RAWIO`; `children` counts 1 and that hit is an unrelated comment at line 1017.

5. [obs] Divergence is total on the scoring terms: eight compared rows change outright (base quantity, CPU time, run time, nice doubling, capability division, cpuset division, child-memory halving, exponential shift), a ninth changes partly (the highest-score goal survives at 196-197, child-killing does not), and the only overlap is the unkillable marker (`oom_adj` −17 vs `OOM_SCORE_ADJ_MIN` at 217), already carried by the round's primary sources S148 and S149.

6. [obs] Reject is also required by the claim mechanics: rule M6 of `tools/check-owed-statements-r29.py:27-28` accepts a basis source only when its registry row has `status mined` and its used-by names the target basename, so a rejected S151 can mark none of O01-O04. Tier C is never sole support (`corpus/QUALITY.md:11`).

7. [obs] The drafted rows verify mechanically: the SOURCES row has 11 cells in the header order of `corpus/SOURCES.md:5`, status `rejected`, recheck `on-release`; the Gate row has 6 cells under the `corpus/lessons/round-28.md:9` header, decision reject with reason and flip. The Gate quote "The badness score is computed using the original memory size of the process," is 13 words and `grep -cF` → 1 at line 113.

8. [obs] A stronger-looking 24-word candidate was rejected during verification: the sentence joined across the page's line wrap gives `grep -cF` → 0 because the HTML breaks at line 113 and has two spaces before `the run time` on line 114. This is the same class of defect as round-28's non-verbatim S147 quote, disclosed in the draft so it cannot recur.

9. [obs] S151 is unregistered at both revisions (`git show 81a061a:corpus/SOURCES.md | grep -c '^| S151'` → 0; same at HEAD `3c94d7308e561832a0df0981cbc39dda270e32d8` → 0; last row S147), so the append is clean. The lane working tree is at the receipts commit 3c94d730, not at the declaration commit 81a061a under attack.

10. [obs] `S151` had been proposed in round 27 for an Arch `nvidia-open` PKGBUILD that never landed (`.ufo/waves/round-27/w2a2/RevRowKT4.md:21`); there is no registry collision, but the id is contested if that source is ever mined.

11. [inf] The draft row's used-by is `corpus/lessons/round-29.md`, which does not exist at 81a061a (`git cat-file -e 81a061a:corpus/lessons/round-29.md` → exit 128); it is the file the Gate row lands in, and the cell needs updating if the lesson lands under another name.

12. [inf] Tier C is assigned because the piece is a secondary contributed article with no version pin; `corpus/SOURCES.md` carries no explicit A/B/C legend, so C follows the usage of S030, S033, S036 and S037.

13. [unk] Whether the article described its own era's code cannot be settled here: no pre-`oom_score_adj` kernel file was fetched and the article names no version. Nothing in the draft asserts either way.

14. Admit was tested as an alternative and does not fit: the only value would be historical texture, the round carries no historical claim, and the article cannot anchor even a history statement without a version-pinned kernel file of that era. The flip condition records exactly that path.

15. [obs] The lane working tree is dirty from sibling seats, not from this seat: `git status --porcelain` lists `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/driver-firmware-plane.md`, `corpus/knowledge/memory-pressure-r25.json`, `corpus/knowledge/storage-health-r26.json`, `tools/check-kernel-taint.py` and the untracked round-29 wave directory. The `corpus/SOURCES.md` diff rewrites only rows S133 and S134 in place (2 insertions, 2 deletions), so S147 remains the last row and the drafted append point is unchanged; this seat wrote only under `.ufo/waves/round-29/w1/ScribeSrcReject/` and the report path.

16. No counter, selftest or battery was run and no product file edited; this seat is a source-gate draft only, so C1 and C2 values are untouched.

Artifacts: `.ufo/waves/round-29/w1/ScribeSrcReject/draft.md` (rows, comparison, verification), `.ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html` (saved article), `.ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.txt` (tag-stripped extraction used for reading), `.ufo/waves/round-29/w1/ScribeSrcReject/oom_kill-v7.2.c` (saved kernel file).

Scope: read=SCORECARD.md:1097-1110 (round-29 declaration), corpus/SOURCES.md (header and rows S140-S147), corpus/lessons/round-28.md:1-16, corpus/QUALITY.md:11, tools/check-owed-statements-r29.py:1-60, .ufo/waves/round-27/w2a2/RevRowKT4.md:21, .ufo/waves/round-27/w1-spec.json (S151 mentions), .ufo/waves/round-29/w1-spec.json (seat prompt), fetched lwn-317814.html (full, via extraction) and oom_kill-v7.2.c (badness region 40-240, token sweep over all 1257 lines); wrote=.ufo/waves/round-29/w1/ScribeSrcReject.md, .ufo/waves/round-29/w1/ScribeSrcReject/draft.md, .ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html, .ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.txt, .ufo/waves/round-29/w1/ScribeSrcReject/oom_kill-v7.2.c; executed=curl -sL (2 fetches, HTTP 200), sha256sum, wc, grep -n/-cF/-cE, python3 (HTML tag strip, cell-count and word-count checks), read-only git: rev-parse HEAD, show 81a061a:corpus/SOURCES.md, show HEAD:corpus/SOURCES.md, cat-file -e 81a061a:corpus/lessons/round-29.md (all with env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE)
Model: opencode-go/deepseek-v4.1-flash
Installs: none
