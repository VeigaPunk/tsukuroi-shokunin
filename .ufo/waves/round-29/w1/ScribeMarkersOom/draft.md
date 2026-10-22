# Round 29 C1 — O01–O04 marker draft (`+200 band` kernel OOM reading)

Append each block below verbatim at end of file (append-only; the anchored sentences stay). Marker lines are single lines, one per owed item.

## `corpus/knowledge/oom-event-plane.md`

```markdown
## Correction (round 29) — kernel OOM victim selection

[obs] Linux v7.2 `mm/oom_kill.c` has no ordered band walk. `oom_badness()` returns rss plus
`MM_SWAPENTS` plus page-table pages plus `oom_score_adj * (totalpages / 1000)` (lines 228-233),
with `totalpages = totalram_pages() + total_swap_pages` for a global OOM (line 263), and
`oom_evaluate_task()` keeps the single largest value over every eligible task (line 340);
`select_bad_process()` is a plain walk of that test (lines 359-377). `proc.rst` 3.1 states the
adjustment is added to the badness score before the kill decision (line 1777). The argmax has
three bypasses: `oom_task_origin()` forces `LONG_MAX` (lines 334-337), `task_will_free_mem(current)`
selects the allocating task before the walk (line 1122), and `oom_kill_allocating_task` kills
current instead of scanning (lines 1145-1151). [obs] Totals: live `/proc/meminfo` reads MemTotal
31,721,800 kB and SwapTotal 31,722,876 kB = 60.5 GiB, while event A's dump records SwapTotal
35,917,176 kB (swapfile plus 4 GiB zram) = 64.5 GiB. The integer term `totalpages / 1000` is
15,861 live and 16,909 at event A, so +200 is worth 3,172,200 points (12.1 GiB) now and 3,381,800
(12.9 GiB) then; +300 is 18.15 GiB now. [obs] Event A's victim held 6,968,424 rss + 7,110,160
swapents = 14,078,584 pages (53.7 GiB) = 888 points before any adjustment (833 on event A's
totalpages), against 301 for the best +300 helper: the +200 credit was roughly a quarter of its
raw points and did not decide the kill. [inf] §2.3's conclusion — the dominant anonymous-memory
holder died, returning the budget — survives unchanged; only the band wording above is wrong.

[R29-OWED-O01] verdict: corrected | original: "exactly the band the kernel scans first" | now: No band is scanned: oom_badness scores every eligible task as resident pages plus swap entries plus page-table pages plus oom_score_adj times totalpages over 1000, and select_bad_process keeps the single highest value; +200 adds 3,381,800 points, about 12.9 GiB, at event A's 64.5 GiB RAM plus swap, or 3,172,200 points, 12.1 GiB, at the live 60.5 GiB, and the 53.7 GiB victim wins either way. | basis: S149 (mm/oom_kill.c lines 228-233, 263, 340, 359-377) and S148 (/proc/<pid>/oom_score_adj, lines 1777-1789)

[R29-OWED-O02] verdict: corrected | original: "the +200 band is chosen first" | now: The killer walks each task once and retains the maximum points, so no adjustment band is ordered at all; the +200 credit is 3.17 million points live, about 12.1 GiB, against the victim's own 14.08 million points from 53.7 GiB of footprint, so the adjustment was roughly a quarter of the evidence and not the reason for the pick. | basis: S149 (mm/oom_kill.c lines 228-233, 340, 359-377) and S148 (/proc/<pid>/oom_score_adj, lines 1777-1789)
```

## `corpus/knowledge/kill-event-deep-r8.md`

```markdown
## Correction (round 29) — kernel OOM victim selection

[obs] Linux v7.2 `mm/oom_kill.c` selects no band: `oom_badness()` sums rss, `MM_SWAPENTS` and
page-table pages, adds `oom_score_adj * (totalpages / 1000)` (lines 228-233), and the walk keeps
the single highest value (line 340, lines 359-377). For a memcg OOM only that cgroup's tasks are
scanned (line 367); otherwise `totalpages = totalram_pages() + total_swap_pages` (line 263). The
walk is bypassed when `task_will_free_mem(current)` selects the allocator (line 1122), when
`oom_kill_allocating_task` is set (lines 1145-1151), or when `oom_task_origin()` forces `LONG_MAX`
(lines 334-337). [obs] Totals: live MemTotal 31,721,800 kB plus SwapTotal 31,722,876 kB = 60.5 GiB
(`totalpages / 1000` = 15,861), event A's recorded SwapTotal 35,917,176 kB makes 64.5 GiB (16,909).
So +100 is 1,586,100 points (6.05 GiB) live or 1,690,900 (6.45 GiB) then, +200 3,172,200 (12.1 GiB)
or 3,381,800 (12.9 GiB), +300 4,758,300 (18.15 GiB) or 5,072,700 (19.35 GiB), and -900
-14,274,900 (-54.5 GiB) or -15,218,100 (-58.05 GiB): a -900 task only loses if its footprint
exceeds that credit. [inf] The §8 row 6 lever therefore still changes who dies, because the
adjustment is additive; the ordering claim above does not hold. [unk] Event B left no kernel OOM
record (F1), so which walk produced its kill remains undecided.

[R29-OWED-O03] verdict: qualified | original: "under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first" | now: The rule is a single argmax over eligible tasks of resident pages plus swap entries plus page-table pages plus the adjustment term; higher-scored and larger-RSS tasks do win, but nothing is visited first, ties fall to iteration order, and the allocating-task, free-memory and origin bypasses can skip the comparison entirely. | basis: S149 (mm/oom_kill.c lines 306-377, 1122, 1145-1151) and S148 (/proc/<pid>/oom_score_adj, lines 1761-1789)

[R29-OWED-O04] verdict: corrected | original: "the +200 band is scanned first" | now: There is no ordered band walk: select_bad_process keeps one maximum over every eligible task, and for a cgroup OOM it scans only that cgroup's tasks, which is how a +100 manager can be chosen while other scopes' +200 clients never enter the comparison; the steering lever survives because the adjustment is additive. | basis: S149 (mm/oom_kill.c lines 362-377) and S148 (/proc/<pid>/oom_score_adj, lines 1777-1789)
```
