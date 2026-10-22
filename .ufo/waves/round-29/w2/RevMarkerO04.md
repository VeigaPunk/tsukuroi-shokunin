# RevMarkerO04 — attack on R29-OWED-O04 at 10d5288fc1051364e711203855e7c53710dfcc21

Verdict: holds — marker O04 in corpus/knowledge/kill-event-deep-r8.md is honest, the original
statement stands unchanged, the `corrected` verdict is right, and both cited sources resolve and
support the `now` text. One low-severity wording imprecision noted, not a falsification.

## Findings

1. (a) Original statement unchanged in place. [obs] The anchor `the +200 band is scanned first`
   still sits at line 260 of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md`
   inside §8 prevention row 6 (`oom_score_adj` steering). The md5 of line 260 at claim base
   16e9ab2a and at tip 10d5288f is identical (`47aa1bd7f083a284793cee374d683ad0`), and
   `git diff 16e9ab2a..10d5288f` on this file shows 21 insertions, 0 deletions — pure append.
   The marker at line 402 quotes the anchor verbatim (`original: "the +200 band is scanned first"`,
   `grep -cF` = 2 occurrences total: original + marker quote).

2. (b) Verdict `corrected` is the right verdict. [obs] The original asserts a mechanism that does
   not exist in v7.2: `oom_evaluate_task` keeps a running maximum (`points < oc->chosen_points`
   skips, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c:339-348`)
   and the `select_bad_process` doc comment says "We choose the process with the highest number of"
   (S149.c:359, `grep -nF` count 1). There is no band ordering to scan "first", so the statement is
   false, not merely imprecise — `corrected`, consistent with siblings O01/O02 (both `corrected`).

3. (c) Both basis references resolve and support the `now` text. [obs] SOURCES.md rows:
   `| S149 | Linux v7.2 mm/oom_kill.c ...` (SOURCES.md:155) and `| S148 | ...
   Documentation/filesystems/proc.rst` (SOURCES.md:154), both status `mined`, opened `2026-10-22`,
   used-by cell `corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md,
   SKILL.md, corpus/lessons/round-29.md` — M6/M7 satisfied. Cited S149 lines 362-377 are exactly
   `select_bad_process`: line 366-367 `is_memcg_oom(oc)` →
   `mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc)` (`grep -cF` = 1), else
   `for_each_process` single pass (368-375) — supports "keeps one maximum" (with the argmax logic
   at 339-348, immediately before the cited range) and the memcg-scope clause. Cited S148 lines
   1777-1789 carry "is added to the badness score before it" (line 1777, `grep -cF` = 1) — supports
   "the steering lever survives because the adjustment is additive", plus the +500 proportion
   example at 1785-1789. Mechanically: `python3 tools/check-owed-statements-r29.py --revision
   10d5288f...` prints `{"id":"O04","ok":true,"verdict":"corrected",...,"sources":["S148","S149"]}`
   and summary `marked 12/12`, counter_sha256 `c3f9cfe73e98...` (the declared v2 counter).

4. Correction (round 29) section recomputes cleanly. [obs] Lines 383-398: with live MemTotal
   31,721,800 kB + SwapTotal 31,722,876 kB → totalpages 15,861,169 → unit 15,861; event-A
   SwapTotal 35,917,176 kB → 16,909,744 → unit 16,909. Recomputed: +100 = 1,586,100 (6.05 GiB),
   +200 = 3,172,200 (12.1 GiB), +300 = 4,758,300 (18.15 GiB), -900 = -14,274,900 (-54.5 GiB) live,
   and event-A 1,690,900 / 3,381,800 / 5,072,700 / -15,218,100 — all match lines 391-395 exactly,
   consistent with `adj *= totalpages / 1000` at S149.c:233 (multiplicative RHS, no approximation
   issue). Every cited line number verified: 367 (memcg scan), 263 (`totalpages = totalram_pages()
   + total_swap_pages`), 334-337 (`oom_task_origin` → `points = LONG_MAX`), 1122
   (`task_will_free_mem(current)`), 1145-1151 (`oom_kill_allocating_task` bypass).

5. Low-severity imprecision (not a defect of verdict or basis). [obs] `now` says "for a cgroup OOM
   it scans only that cgroup's tasks". v7.2 `mem_cgroup_scan_tasks` "iterates over tasks attached
   to @memcg or to any of its" descendants (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevMarkerO04/memcontrol-v7.2.c:1355-1356`,
   `for_each_mem_cgroup_tree` at :1370; fetched bytes sha256
   `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e`). So the scan covers the
   OOM'd memcg's whole subtree, not just its direct tasks. [inf] Harmless here: the conclusion the
   sentence serves — tasks in scopes outside the OOM'd subtree "never enter the comparison" — is
   correct, and the cited S149 range is honest for what it shows. At worst a reader could take
   "that cgroup's tasks" as excluding descendants.

6. Fetch note. [obs] First fetch of memcontrol.c from raw.githubusercontent.com was rate-limited
   (HTTP 429 page, sha256 `ed34c600de6e952234b278d7c8b8d05ec4790c0e1dec2ea2a86e5b3bfaa5b0a1`,
   1 line); retried via the kernel.googlesource.com public mirror, 6068 lines, sha256 as in
   finding 5. No bot challenge passed.

Residual risk: none material. [inf] The marker's strongest load-bearing phrase (single max over
eligible tasks; scoped scan; additive steering) is exactly what the v7.2 source shows; the only
gap is the single-cgroup-vs-subtree wording in finding 5.

Scope: read=corpus/knowledge/kill-event-deep-r8.md, corpus/SOURCES.md rows S148-S151, tools/check-owed-statements-r29.py docstring+ITEMS, corpus/lessons/round-29.md, SCORECARD.md round-29 declaration, w1 snapshots S149.c + S148-proc.rst, v7.2 memcontrol.c; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevMarkerO04.md, .ufo/waves/round-29/w2/RevMarkerO04/memcontrol-v7.2.c; executed=read-only git (show, diff --stat), python3 tools/check-owed-statements-r29.py --revision 10d5288f... (marked 12/12), grep/md5sum/sha256sum checks, curl of v7.2 memcontrol.c (github rate-limited → googlesource mirror)
Model: devin/swe-2
Installs: none
