# RevSkillOomSection — SKILL.md "Kernel OOM victim selection — round 29" review (Tsukuroi R29, wave 2)

**Verdict: partly holds.** Every printed number and every cited source line in the section
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:2535-2547` at 10d5288fc1051364e711203855e7c53710dfcc21)
recomputes or matches the sha256-pinned v7.2 snapshots; the F7 verdict agrees with wave-1
RevF7Quant ("holds"). No wrong number. One low-severity overclaim (event-B totalpages is a
projection, not a recorded value) plus formula/citation precision defects.

## Findings

1. **[low] Decision table projects event-A totalpages onto event B without recorded support.**
   Row "global OOM" claims `16,909,739 pages at event A/B` (SKILL.md:2543). The 16,909,739 figure
   is anchored only to event A: event A's dump records `Total swap 35,917,176 kB`
   (`corpus/knowledge/oom-event-plane.md:82`) and 31,721,780 kB of MemTotal gives
   7,930,445 + 8,979,294 = 16,909,739 pages. Event B (2026-10-14 13:10:59) has no kernel record
   and no recorded SwapTotal; the recorded swap plane *changed* between event A and the r8
   capture — live SwapTotal read 31,722,876 kB (`kill-event-deep-r8.md:391-392`,
   `oom-event-plane.md:487-489`), 4,194,300 kB below event A's, because zram0 no longer existed
   at capture (`.ufo/waves/round-29/w1/ScribeSkillOomRow.md:79-83`). The capture is ~26 h after
   event B and zram removal timing is unrecorded, so event-B totalpages could be anywhere between
   15,861,169 and 16,909,739 [unk]. The honest cell is "16,909,739 at event A; event B unrecorded;
   15,861,169 at capture" [obs]. No downstream number changes: the F7 margins at either bound
   keep their GiB-scale verdict.

2. **[nit] The printed formula is left-associative and does not reproduce the section's own
   numbers.** SKILL.md:2537 writes `oom_score_adj × totalpages/1000`, which reads as
   adj·totalpages/1000 = 200·16,909,739/1000 = 3,381,947.8 → 3,381,947 pages, while the table
   prints 3,381,800. The kernel computes `adj *= totalpages / 1000`
   (S149 snapshot `.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c:233`, i.e.
   ⌊16,909,739/1000⌋·200 = 16,909·200 = 3,381,800 — the printed value. All section numbers use
   the kernel parenthesization; the formula text should read
   `oom_score_adj × ⌊totalpages/1000⌋` [obs].

3. **[nit] "keeps the strict maximum in task-list order" omits the LONG_MAX override in the same
   function.** S149:334-336: `if (oom_task_origin(task)) { points = LONG_MAX; goto select; }` —
   a task carrying the internal `oom_flag_origin` (oom.h:59-72, set only by in-kernel
   `set_current_oom_origin()`) wins unconditionally regardless of the scalar rule. Internal
   flag, not userspace-steerable [obs]; also `tsk_is_oom_victim` forces `points = 0` at :324-327.
   Additionally the "equal score replaces the earlier pick" claim is proven by the replacement
   at :344-348 (`oc->chosen = task; oc->chosen_points = points;` reached because :340 skips only
   `points < oc->chosen_points`), which sits *outside* the cited `:339-341`, `:362-375` —
   the cites cover the guard and the scan, not the replacement itself [obs].

4. **[nit] F7 row: strict-vs-tie edge.** SKILL.md:2547 "beats a +200 app only if it holds
   1,690,900 pages (6.45 GiB) more" — at *exactly* +1,690,900 pages the points tie, and per
   :340/:347-348 the later task in `for_each_process` order wins; so the true condition is
   "≥ 1,690,900 more, with scan order breaking ties". A one-page edge case only [obs].

5. **[nit] Badness-scale shorthand and memcg gloss are looser than the sources.** "the 0-1000
   badness scale" is S148's nominal doc range (proc.rst:1761-1766) but the exported oom_score
   "includes oom_score_adj so it is effectively in range [0,2000]" (proc.rst:1811-1812) — the
   section's sentence is doc-faithful yet elides that a +1000-adj task exports up to 2000
   [obs]. The memcg gloss "`memory.max` + `swap.max`" (SKILL.md:2544) omits
   `min(swap.max, total_swap_pages)` and the `mem_cgroup_swappiness()` guard
   (`mem_cgroup_get_max`, `.ufo/waves/round-29/w1/RevOomMechanism/memcontrol.c:1835-1851`);
   outcome on this host unchanged since all path files read `max` (trigger closed —
   `kill-event-deep-r8.md:244`, `:257`) [obs].

## Recomputation record (all verified)

- totalpages global = totalram + total_swap (S149:263); memcg = mem_cgroup_get_max ?: 1 (:258).
- Pages per adj unit: MemTotal 31,721,780 kB (kill-event-deep-r8.md:182) → 7,930,445 pg;
  event-A SwapTotal 35,917,176 kB (oom-event-plane.md:82) → 8,979,294 pg; sum 16,909,739;
  ⌊/1000⌋ = 16,909 pg = 66.05 MiB (16,909·4096/2^20) — matches SKILL.md:2538 and :2543.
- +200 → 16,909·200 = 3,381,800 pg = 12.90 GiB; +300 → 5,072,700 pg = 19.35 GiB; +100-vs-+200
  gap 1,690,900 pg = 6.45 GiB; +100-vs-+300 gap 3,381,800 pg — all match SKILL.md:2543/:2547.
- Live today: 31,721,800 + 31,722,876 kB → 15,861,169 pg, ⌊/1000⌋ = 15,861 — matches ":2543
  (15,861,169 today)" and oom-event-plane.md:489-490.
- Cited lines verified verbatim in pinned snapshots: S149.c (sha256 452f1348…) :216-222
  (−1000 → LONG_MIN), :228-236 (formula), :258/:263 (totalpages), :339-341 (tie guard),
  :362-375 (for_each_process scan), :1040-1052 (oom_group cgroup kill), :1145-1152
  (oom_kill_allocating_task, `current`, global-only, `!= OOM_SCORE_ADJ_MIN`); S148 proc.rst
  (sha256 e760f716…) :1761-1766 (0-1000 proportion), :1777-1783 (adj added; −1000 disables);
  S150 vm.rst (sha256 bf8ca026…) :810-817 (zero → tasklist scan, non-zero → kill triggering
  task; default 0 at :822, panic_on_oom precedence at :819-820).
- F7 verdict: consistent with `.ufo/waves/round-29/w1/RevF7Quant.md` — "holds" with the same
  6.45 GiB-per-100 margin; SKILL.md:2547 correctly shifts the no-kernel-kill conclusion onto
  F1's `oom_kill` ledger (F1 = `/proc/vmstat oom_kill` = 1, SKILL.md:1088) and cites F5
  (SKILL.md:1092) for unmeasured event-B per-process sizes. F1/F5/F7 rows verified at
  SKILL.md:1088-1094.

## Residual risk / verification gaps

- No LSP server applies (prose + fetched C/rst files); line citations verified by direct reads
  of the sha256-pinned snapshots — text anchors only, recorded as the fallback, not semantic
  proof [obs].
- `totalram_pages()` ≈ MemTotal/PAGE_SIZE is [inf] (scales in [unk] kernel counters); error is
  sub-1 % and moves no entry, as ScribeSkillOomRow noted.
- Snapshot copies across seat dirs are byte-identical (sha256 checked: 4× oom_kill.c,
  3× proc.rst, 2× vm.rst) — citations resolve in any copy.

Scope: read=SKILL.md:2530-2593 and :1080-1100, corpus/SOURCES.md:154-157, corpus/knowledge/oom-event-plane.md and kill-event-deep-r8.md (totals/memcg/marker lines), .ufo/waves/round-29/w1/{RevF7Quant.md,ScribeSkillOomRow.md}, snapshots S149.c, S148-proc.rst, S150-vm.rst, oom.h, memcontrol.c; wrote=.ufo/waves/round-29/w2/RevSkillOomSection.md; executed=sha256sum, grep -n, sed line reads, read-only git (rev-parse, status --porcelain, diff --stat) — no git writes, no lane edits outside this report
Model: devin/swe-2 (per project context)
Installs: none
