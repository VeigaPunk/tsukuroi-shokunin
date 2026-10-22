# RevOomMechanism — C1 premise check, O01–O04 (kernel OOM victim selection, v7.2)

Verdict: the C1 premise holds — the reading "the +200 band is scanned first / chosen first" is
FALSE for the running kernel (7.2.11-arch1-1; upstream tag v7.2 verified as the source base).
There is no band ordering, no scan priority by `oom_score_adj`, and no "first" of any kind:
victim selection is a single argmax over one scalar score.

## 1. The exact selection rule (mm/oom_kill.c, v7.2)

Fetched bytes: `oom_kill.c` sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`
(1257 lines), `proc.rst` sha256 `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`
(2495 lines), `oom.h` and `memcontrol.c` (googlesource mirror, 6068 lines) saved beside this file.

Entry — `out_of_memory()` (oom_kill.c:1103):

1. `task_will_free_mem(current)` fast path (1122–1126): if the allocating task is already
   exiting/SIGKILLed it is marked victim directly — **score never consulted**.
2. `constrained_alloc(oc)` (1140, impl 249–304) sets `oc->totalpages`:
   - memcg OOM → `mem_cgroup_get_max(oc->memcg)` (257–259);
   - cpuset → sum of allowed nodes (297–301);
   - global → `totalram_pages() + total_swap_pages` (263).
3. `sysctl_oom_kill_allocating_task` path (1145–1153): kills `current` unconditionally —
   **score never consulted**.
4. `select_bad_process(oc)` (1155, impl 362–377): the only scoring path.
   - memcg OOM: `mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc)` (366–367).
   - global OOM: `for_each_process(p)` over the whole task list (371–375) — plain task-list
     iteration, unsorted.

Per candidate — `oom_evaluate_task()` (306–356):
- skip unkillable / cpuset-ineligible (311–316); abort scan if another task is already an
  OOM victim (324–328);
- `oom_task_origin(task)` → `points = LONG_MAX`, wins outright (334–337; `oom_task_origin`
  is just the `signal->oom_flag_origin` flag, oom.h:69–72);
- else `points = oom_badness(task, oc->totalpages)` (339); strictly greater `points`
  replaces `oc->chosen` (340–348). Note `points < oc->chosen_points` keeps scanning — on an
  exact tie the LATER-scanned task wins, so even tie order is "last", never "first".

`oom_badness()` (199–237) — the entire scoring rule:

    points = get_mm_rss_sum(mm) + swapents + pgtables_bytes/PAGE_SIZE   (228–229)
    adj    = oom_score_adj * (totalpages / 1000)                      (216, 233)
    points += adj                                                     (234)

`oom_score_adj == -1000` (OOM_SCORE_ADJ_MIN), `MMF_OOM_SKIP`, or vfork → `LONG_MIN`,
i.e. excluded (217–222). That is the only place `oom_score_adj` gates anything, and it is a
kill-exemption gate, not a band sort.

Memcg scan order — `mem_cgroup_scan_tasks` (memcontrol.c:1362–1386): iterates the memcg
tree, and within each cgroup a `css_task_iter` (1374–1375). Cgroup-tree order then
css-set order. No sorting, no adj-aware ordering anywhere.

Documentation contract — proc.rst §3.1 (1755–1801): `oom_score_adj` "is added to the
badness score before it" is used to pick the victim (1777–1778); it lets userspace
"polarize the preference" (1780–1781). Additive bias to one scalar, range −1000..+1000.
§3.2 (1804–1812): `oom_score` = badness including adj, range [0,2000].

Conclusion: there is **no ordering by `oom_score_adj`**. Every eligible task is evaluated
in one pass; the largest `footprint + adj·totalpages/1000` wins. On this host
(MemTotal 30.3 GiB + SwapTotal 30.3 GiB ⇒ totalpages ≈ 15.9 M for a global OOM), each +100
of adj contributes ≈ 6.1 GiB-equivalent points — a bias, not a "band" and never a scan order.
Three paths (`task_will_free_mem`, `oom_kill_allocating_task`, `oom_task_origin`) bypass
scoring entirely; a −1000 adj exempts.

## 2. Verdicts per anchored passage

O01 — oom-event-plane.md:115–118. Two claims:
- :116 "which is exactly the band the kernel scans first" → **corrected**. No band is
  scanned; +200 tasks were simply the largest population and one of them held ~53.7 GiB of
  counted footprint — that is why the victim came from the band, not because it was scanned
  first. Scan order is task-list order (oom_kill.c:372–374); score is argmax (340–348).
- :117–118 "[inference] the victim was the dominant anonymous-memory holder (26.6 GiB anon +
  27.1 GiB swapped)" → **rebutted** (the reading is right). The mechanism agrees: footprint
  dominates the score (228–229); at 53.7 GiB footprint the victim's ≈ +200 bonus
  (≈ 12 GiB-equiv.) was not even needed to win. The trigger being a page fault is also
  consistent — `out_of_memory` is invoked from the allocator and page-fault path, and the
  invoker plays no role in victim choice (only `current`'s adj is even logged, :458–460).

O02 — oom-event-plane.md:349 (prevention table row 6, mechanism column):
"the +200 band is chosen first" → **corrected**. The kernel chooses the single highest
badness; a +200 task is chosen only when `footprint + 200·totalpages/1000` is the maximum.
The row's operational advice survives only in weakened form: `OOMScoreAdjust=` shifts a
task's score by a fixed memory-equivalent (≈ 6.1 GiB per +100 here), so it reorders
near-equal footprints but cannot protect (or doom) a task whose footprint dominates by more
than the adj delta; −1000 is the only absolute protection (oom_kill.c:217–218,
proc.rst:1781–1783).

O03 — kill-event-deep-r8.md:145–152:
"under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first" →
**rebutted** (substantively right). "Prefers the higher-scored" *is* the rule: argmax of
badness = footprint + adj·totalpages/1000 (oom_kill.c:228–234, 339–348). The word "scan …
first" is loose but harmless here because the sentence asserts preference, not band order.
The follow-on inference (a kernel pick of the +100 manager while +300 Chromium clients lived
contradicts the class picture → argues against H1) is also sound *if* the manager's
footprint did not exceed the helpers' by ≳ 12 GiB-equiv (the +300-vs-+100 adj gap on this
host); with ordinary helper footprints it is a genuine anomaly. Only caveat worth a marker:
three bypass paths exist (task_will_free_mem :1122, oom_kill_allocating_task :1145,
oom_task_origin :334), and an already-exiting manager could have been picked by the first
one with zero scoring — the doc's §8 row 9 (KillMode/TimeoutStopSec teardown) is the right
place to rule that out.

O04 — kill-event-deep-r8.md:260 (prevention table row 6):
"the +200 band is scanned first" → **corrected**. Same defect as O01: no band scan exists;
the sentence's own tail ("a known-huge batch job placed differently changes who dies — but
this event killed the *manager*") shows the intended claim is preference/steering, which the
additive-adj rule supports, while "scanned first" asserts a nonexistent mechanism.

## 3. Bottom line for C1

The premise is confirmed: O01, O02, O04 contain a false mechanism claim ("band … scanned
first" / "chosen first") and owe a source-backed correction marker. O03's core claim is
correct and warrants `rebutted` — or `qualified` if the scribes want to fix the "scan
first" phrasing and add the bypass-path caveat. Correct rule for the marker text: victim =
argmax over all eligible tasks of `rss_sum + swapents + pgtables/PAGE_SIZE +
oom_score_adj·totalpages/1000` (oom_kill.c:199–237, 306–377); `oom_score_adj` is an
additive bias and −1000 exemption, never an ordering (proc.rst:1755–1801); on this host
+100 ≈ 6.1 GiB score-equivalent.

Scope: read=lane files oom-event-plane.md, kill-event-deep-r8.md, tools/check-owed-statements-r29.py; fetched v7.2 oom_kill.c, oom.h, proc.rst (github raw), memcontrol.c (kernel.googlesource mirror); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/RevOomMechanism.md plus fetched sources under .ufo/waves/round-29/w1/RevOomMechanism/; executed=curl fetches, grep/read of fetched files, /proc/meminfo read, sha256sum — no git writes, no lane writes outside seat paths.
Model: devin/swe-2 (workstation model label; answering model identity not further exposed)
Installs: none
