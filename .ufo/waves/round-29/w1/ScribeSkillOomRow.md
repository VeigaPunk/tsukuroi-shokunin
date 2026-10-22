# ScribeSkillOomRow — round 29, depth content for SKILL.md (C1 support)

done — the SKILL.md subsection is drafted at 13 lines (limit 15) with the v7.2 selection rule and its
source lines, a three-row decision table and the F7 check; four marker drafts for O01-O04 pass the C1
checker's own marker regex and M2-M6 rule logic offline, but nothing is landed, so `marked` still
reads 0 of 12.

1. [obs] The selection rule, from the fetched v7.2 bytes. `oom_badness` computes
   `points = rss + swapents + pgtables` in pages, then `adj *= totalpages / 1000; points += adj`
   (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSkillOomRow/oom_kill.c:228-234`,
   quote verified `grep -cF 'adj *= totalpages / 1000;'` = 1); `select_bad_process` keeps the strict
   maximum over `for_each_process`, and because the skip is `points < oc->chosen_points` an equal
   score replaces the earlier pick (`:339-341`, `:362-375`). There is no band order anywhere in the
   path, which is what O01-O04 assert.

2. [obs] The scale, from the same file plus S148. Global OOM uses
   `totalram_pages() + total_swap_pages`, memcg OOM `mem_cgroup_get_max(oc->memcg) ?: 1`
   (`oom_kill.c:263`, `:258`); `adj == OOM_SCORE_ADJ_MIN` returns `LONG_MIN`, i.e. −1000 is exclusion
   from candidacy, not a low score (`:216-222`), matching S148
   (`proc.rst:1781-1783`, quote "The value of /proc/<pid>/oom_score_adj is added to the badness score
   before it" at `proc.rst:1777`). `oom_kill_allocating_task` defaults to 0 (BSS-initialized,
   `oom_kill.c:57`, sysctl table `:710-715`; host reads 0), and when set it kills `current` with no
   score at all on the global path only (`:1145-1152`; S150
   `vm.rst:810-817`, quote "If this is set to zero, the OOM killer will scan through the entire"
   verified by `grep -cF`).

3. [obs] The page arithmetic for this host. Capture-epoch totals MemTotal 31,721,780 kB and SwapTotal
   35,917,176 kB (`corpus/knowledge/kill-event-deep-r8.md:26-37` §5.1/§5.2) give
   `totalpages = 16,909,739`, so one adj unit = 16,909 pages = 66.05 MiB, +200 = 3,381,800 pages =
   12.90 GiB, +300 = 5,072,700 pages = 19.35 GiB (`python3`, integer page math, PAGE_SIZE 4096).
   `totalram_pages()` is the managed-page count and may sit slightly under MemTotal/PAGE_SIZE;
   the gap is under 1 % and moves no table entry [inf].

4. [obs] The corpus's own event-A dump refutes the band reading numerically, so the marker for O01/O04
   rests on the lane's own data and not only on the source. Replaying the formula over
   `corpus/knowledge/oom-event-plane.md:105-113`: victim python3 at +200 →
   6,968,424 + 7,110,160 + 3,381,800 = 17,460,384 points, top +300 chromium →
   8,845 + 9,503 + 5,072,700 = 5,091,048 points. Every other task is bounded by the dump totals
   (rss_anon 7,140,787 and swapents 8,228,965 pages over 164 rows) at ≤ 1,291,168 + 5,072,700 =
   6,363,868 pages, so the victim was necessarily the maximum and the 100-unit adj deficit cost the
   Chromium nothing beyond a 12.37M-page gap it could not close. Break-even for +300 to beat +200 is
   1,690,900 pages.

5. [inf] F7 (`SKILL.md:1094`) is qualified, not refuted. Under the formula the +100 manager beats a
   +200 app only if its `rss+swapents+pgtables` exceeds that app's by 1,690,900 pages (6.45 GiB) and
   each +300 Chromium's by 3,381,800 pages (12.9 GiB); event B has no per-process size at all
   (`kill-event-deep-r8.md:26-37` F5 and §5.1: only slice/service lifetime maxima, 28.5 GiB over the
   whole 26 h session), so the class labels do not settle it. The conclusion "no kernel kill at event
   B" is still carried, but by F1's `/proc/vmstat oom_kill = 1` ledger, not by the adj class. The
   draft states the condition instead of asserting the argument.

6. [obs] Deliverable and its offline validation. The subsection is 13 fenced lines
   (`.ufo/waves/round-29/w1/ScribeSkillOomRow/draft.md:8-20`), table cells carry no stray pipes
   (pipes only on the five table lines). Marker drafts are at `draft.md:54-55` (O01/O02, appended to
   `oom-event-plane.md`) and `draft.md:61-62` (O03/O04, appended to `kill-event-deep-r8.md`). I
   imported the checker module and applied its own `MD_MARKER` regex and constants: all four parse,
   verdicts are in `VERDICTS`, `now` is 38-43 words, contains no copy of the anchor, all four differ,
   one marker per id, and every anchor is present verbatim in its file (M1/M3/M5 hold). M7 holds
   because S149 is cited. O03 is `qualified` (the rule is monotone in memory and adj but "first" and
   the implied priority are wrong); O01/O02/O04 are `rebutted`.

7. [obs] The gate will not move until the registry rows exist. `tools/check-owed-statements-r29.py`
   M6 needs an `S###` row with status `mined` whose used-by cell names the target basename, so S148,
   S149 and S150 must be entered in `corpus/SOURCES.md` with a used-by cell naming
   `oom-event-plane.md`, `kill-event-deep-r8.md` and `SKILL.md`; with the current registry
   (`corpus/SOURCES.md:153` is S147, the last row) the markers would count 0. S151 (LWN, 2009) is
   left unused — a reject row, not a basis.

8. [obs] Provenance of the fetched bytes, all saved in the seat directory with sha256:
   `oom_kill.c` 1257 lines `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`
   (raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c); `proc.rst` 2495 lines
   `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`; `vm.rst` 1153 lines
   `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce`; `oom.h` 114 lines
   `42e8e17f6eda1a48e8455a55fe6aa4114ae121c35e665bfd19e474dacf77b7fd`. raw.githubusercontent.com
   answered HTTP 429 ("Too Many Requests") to `proc.rst` and `vm.rst` on first fetch; `proc.rst`
   succeeded on retry, `vm.rst` came from the kernel.org cgit plain endpoint at `?h=v7.2` (same tag,
   same tree) and is labelled as such in the draft.

9. [obs] Own change to the host's picture, recorded rather than smoothed: `/proc/swaps` today lists
   only `/swap/swapfile` and `/sys/block/zram0` no longer exists, so SwapTotal fell by 4,194,300 kB
   to 31,722,876 kB (MemTotal 31,721,800 kB) and today's totalpages is 15,861,169 (15,861 pages per
   adj unit, 61.96 MiB). The subsection prints both figures so the capture-epoch arithmetic stays
   readable against current probes.

10. [unk] Event B per-process RSS (the F7 condition's missing term); event A's `rss_file`, `rss_shmem`
    and `pgtables` per task (the dump table records rss_anon and swapents only, hence the ceiling
    argument above rather than exact points); why zram0 disappeared; whether `oom_task_origin` has a
    userspace writer (no caller in the fetched `mm/oom_kill.c`, helper only in `include/linux/oom.h:59-72`).

Out of scope and untouched: no landing of the subsection or markers, no `corpus/SOURCES.md` edit, no
run of `tools/check-owed-statements-r29.py` or `tools/probe-git-env-leak.py` at a revision, no lane or
fleet write, no git or jj write command, no pacman.

Scope: read=SCORECARD.md declaration tail region, SKILL.md:1070-1130, corpus/knowledge/kill-event-deep-r8.md (1-300), corpus/knowledge/oom-event-plane.md:95-116 and :345-352, corpus/SOURCES.md:5-12 and :141-152, tools/check-owed-statements-r29.py:1-120, /proc/meminfo, /proc/swaps, /proc/sys/vm/{oom_kill_allocating_task,panic_on_oom,oom_dump_tasks,overcommit_memory}, /sys/block/zram0 probe, kernel v7.2 mm/oom_kill.c, Documentation/filesystems/proc.rst, Documentation/admin-guide/sysctl/vm.rst, include/linux/oom.h; wrote=.ufo/waves/round-29/w1/ScribeSkillOomRow/draft.md, .ufo/waves/round-29/w1/ScribeSkillOomRow/{oom_kill.c,proc.rst,vm.rst,oom.h}, .ufo/waves/round-29/w1/ScribeSkillOomRow.md; executed=curl fetches (raw.githubusercontent.com, git.kernel.org cgit), sha256sum, wc, grep -cF quote checks, awk/sed line extraction, python3 arithmetic and checker-rule simulation, cat/sed/grep on /proc
Model: opencode-go/deepseek-v4.1-flash (per project context, not self-reported)
Installs: none
