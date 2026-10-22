# Round 29 wave 1 — S149 source draft (Linux v7.2 mm/oom_kill.c)

Seat: ScribeSrcOomKill. Claim: C1 (depth), the O01–O04 kernel victim-selection anchors.
Revision of record: lane branch tip `81a061a67466c5e1be812814a895a4b5ed89b4ff` (declaration commit).
Fetched 2026-10-22T19:58Z by plain `curl -sL` from
`https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` (HTTP body, no bot challenge).
Raw bytes sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`, 1257 lines.
Snapshot: `.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c` (byte-identical copy of the fetched file;
sha256 re-checked after copy, same digest).

Everything below is a *draft*. Nothing here is a registry edit; the L1 integrates. This file is the
only artifact this seat writes besides its report.

## 1. Registry row (exact 11-column shape of S140–S147)

Header of the table for reference (`corpus/SOURCES.md`, line 7):
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

Row to append after S148 (or immediately after the last S-row if S148 lands elsewhere — the id is
reserved for this round, so keep numeric order):

| S149 | Linux v7.2 mm/oom_kill.c — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | How the kernel scores and selects an OOM victim: the `oom_badness` point sum (RSS, swap entries, page tables), the `oom_score_adj` scaling by `totalpages / 1000`, the single full scan that keeps the highest points, the memcg-scoped scan and the `oom_kill_allocating_task` bypass, for the host kernel 7.2.11 | tag v7.2, mm/oom_kill.c lines 199, 216, 228, 233, 263, 306, 340, 348, 362, 367, 372, 710, 1145; raw bytes sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e; snapshot .ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c (1257 lines) | Points are rss plus swap entries plus page-table pages, then `oom_score_adj * (totalpages / 1000)` is added; `select_bad_process` visits every eligible task once and keeps the highest points, with no band or class scanned first; under `oom_kill_allocating_task` the allocating task dies without any scan | mined | 2026-10-22 | on-release | corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md |

Column notes for the integrator:
- `kind` = `code` (kernel C source, same as S141/S143); `tier` = `A` (primary upstream at the tag
  matching the host kernel 7.2.11); `status` = `mined`; `recheck` = `on-release` (matches S140–S145).
- `used-by` names both target basenames, so M6 resolves for O01–O04 whichever file cites it.
- The `anchor` cell gives a line set plus the sha256 and snapshot, matching the S140–S147 form.

## 2. Lesson Gate row (round-29 lesson, `## Gate` table shape of `corpus/lessons/round-28.md`)

Table header for reference: `| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |`

| S149 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 2026-10-22 | "Simple selection loop. We choose the process with the highest number of" | `.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c` line 359, sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | admit, `mined`, tier A (primary upstream source at the tag of the running kernel 7.2.11; it settles the O01–O04 question by showing a single highest-points scan and no band. The 2009 LWN reject candidate S151 is not this seat's row) |

Quote check on the saved bytes (required verbatim form):
`grep -cF "Simple selection loop. We choose the process with the highest number of" S149.c` → `1`.
The line is a two-line comment; the quoted span is exactly line 359, 12 words, inside one line.

Secondary quotes used in the body below, each verified with `grep -cF` → 1 on `S149.c`:
- line 228: `points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) +`
- line 233: `	adj *= totalpages / 1000;`
- line 340: `	if (points == LONG_MIN || points < oc->chosen_points)`
- line 367: `		mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc);`

## 3. Mechanism, line-located (file = S149.c, Linux v7.2 mm/oom_kill.c)

### 3.1 `oom_badness()` — how points are computed (lines 199–236)

```
199  long oom_badness(struct task_struct *p, unsigned long totalpages)
...
204  	if (oom_unkillable_task(p))
205  		return LONG_MIN;
...
216  	adj = (long)p->signal->oom_score_adj;
217  	if (adj == OOM_SCORE_ADJ_MIN ||
218  			mm_flags_test(MMF_OOM_SKIP, p->mm) ||
219  			in_vfork(p)) {
...
228  	points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) +
229  		mm_pgtables_bytes(p->mm) / PAGE_SIZE;
230  	task_unlock(p);
231
232  	/* Normalize to oom_score_adj units */
233  	adj *= totalpages / 1000;
234  	points += adj;
```

Reading, in words:
- The score is a **sum of three memory terms measured in pages**: resident set (`get_mm_rss_sum`),
  swap entries (`MM_SWAPENTS`), and page tables (`mm_pgtables_bytes / PAGE_SIZE`). Lines 228–229.
- `oom_score_adj` is **added after scaling**, not multiplied into the memory terms: `adj` is
  multiplied by the integer quotient `totalpages / 1000` (division happens first, line 233) and the
  product is added to points (line 234). So one adj unit buys `floor(totalpages/1000)` pages of
  score. [inf] on this host that is roughly one-thousandth of RAM+swap per unit, so +200 ≈ 20% of
  RAM+swap worth of pages — a large additive term, but still an additive term.
- `totalpages` is the normaliser: line 258 `oc->totalpages = mem_cgroup_get_max(oc->memcg) ?: 1;`
  for a memcg OOM, else line 263 `oc->totalpages = totalram_pages() + total_swap_pages;`, with the
  nodemask variants at 285–287 and 298–300 (swap plus present pages of the allowed nodes).
- A task is excluded (`LONG_MIN`, never selected) when `oom_unkillable_task`, no `mm`
  (`find_lock_task_mm` fails), `oom_score_adj == OOM_SCORE_ADJ_MIN` (−1000), `MMF_OOM_SKIP`, or
  `in_vfork`. Lines 204–222.

### 3.2 `oom_evaluate_task()` and `select_bad_process()` — one scan, highest points

```
306  static int oom_evaluate_task(struct task_struct *task, void *arg)
...
310  	if (oom_unkillable_task(task))
311  		goto next;
...
314  	if (!is_memcg_oom(oc) && !oom_cpuset_eligible(task, oc))
315  		goto next;
...
334  	if (oom_task_origin(task)) {
335  		points = LONG_MAX;
336  		goto select;
337  	}
338
339  	points = oom_badness(task, oc->totalpages);
340  	if (points == LONG_MIN || points < oc->chosen_points)
341  		goto next;
342
343  select:
344  	if (oc->chosen)
345  		put_task_struct(oc->chosen);
346  	get_task_struct(task);
347  	oc->chosen = task;
348  	oc->chosen_points = points;
349  next:
350  	return 0;
```

```
358  /*
359   * Simple selection loop. We choose the process with the highest number of
360   * 'points'. In case scan was aborted, oc->chosen is set to -1.
361   */
362  static void select_bad_process(struct oom_control *oc)
363  {
364  	oc->chosen_points = LONG_MIN;
365
366  	if (is_memcg_oom(oc))
367  		mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc);
368  	else {
369  		struct task_struct *p;
370
371  		rcu_read_lock();
372  		for_each_process(p)
373  			if (oom_evaluate_task(p, oc))
374  				break;
375  		rcu_read_unlock();
376  	}
377  }
```

Reading, in words — this is the decisive answer for O01–O04:
- There is **exactly one pass over the task set**, either `for_each_process` (line 372) or, for a
  cgroup/memcg OOM, `mem_cgroup_scan_tasks(oc->memcg, …)` (line 367). The scan starts from
  `chosen_points = LONG_MIN` (line 364) and is a running maximum: a candidate replaces the current
  choice only when its points are not lower than the incumbent's (`points < oc->chosen_points` →
  skip, line 340; assign at 347–348). Strictly greater-or-equal wins; no sorting, no second pass.
- **There is no band, class or `oom_score_adj`-bucket pre-scan anywhere in the file**: `grep -n
  "band\|class"` on S149.c returns nothing. Nothing scans +200 (or +300) tasks first. A +200 task
  is not selected because of its band; it is selected only if its total points are the maximum. The
  "+200 band is scanned first" sentence is therefore false as a description of the kernel's
  selection order, and the observation that the +100 manager died while +200 clients lived is
  consistent with the code, not a contradiction of it (the manager's total points were the
  maximum).
- The only shortcut past scoring is `oom_task_origin(task)` → `points = LONG_MAX` (lines 334–337),
  i.e. the allocating task when it is marked as the OOM origin. `oom_task_origin()` is not defined
  in this translation unit [unk] (it lives in `include/linux/oom.h`); it is not an `oom_score_adj`
  band.
- An aborted scan (an existing OOM victim without `MMF_OOM_SKIP`) sets `oc->chosen = (void *)-1UL`
  and returns 1, which stops `for_each_process` (line 373–374) — not a banding mechanism.

### 3.3 The memcg-scoped path and `oom_kill_allocating_task`

- Memcg OOM: `select_bad_process` uses `mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc)`
  (line 367), so the same single running-maximum evaluation is applied to the memcg's tasks only,
  with `totalpages = mem_cgroup_get_max(oc->memcg) ?: 1` (line 258). The memcg member ctx is also
  used by `dump_tasks` (line 428) and by the group-oom kill walk (`oom_kill_memcg_member`, line
  1050). `mem_cgroup_scan_tasks` itself is defined in `mm/memcontrol.c`, not here [unk] on its
  internal iteration order; its contract as used here is "call the callback for each task of that
  memcg".
- `oom_kill_allocating_task` sysctl: declared at line 57 (`static int
  sysctl_oom_kill_allocating_task;`), exposed as a `proc_dointvec` entry in `vm_oom_kill_table`
  (lines 710–714, mode 0644). Its effect is in `out_of_memory()`:
  ```
  1145  	if (!is_memcg_oom(oc) && sysctl_oom_kill_allocating_task &&
  1146  	    current->mm && !oom_unkillable_task(current) &&
  1147  	    oom_cpuset_eligible(current, oc) &&
  1148  	    current->signal->oom_score_adj != OOM_SCORE_ADJ_MIN) {
  1149  		get_task_struct(current);
  1150  		oc->chosen = current;
  1151  		oom_kill_process(oc, "Out of memory (oom_kill_allocating_task)");
  1152  		return true;
  1153  	}
  1154
  1155  	select_bad_process(oc);
  ```
  So when the sysctl is nonzero and the allocating task is killable, **the allocating task is
  killed with no scoring scan at all** (1155 is skipped). It does not apply to a memcg OOM
  (`!is_memcg_oom(oc)`). Default value is not stated in this file; the sysctl is initialised to
  zero by C static storage [inf] unless set elsewhere, and it is writable at runtime.

## 4. What this means for O01–O04 (for the marker author, not a marker)

The anchors (from `tools/check-owed-statements-r29.py:48-55`) and their files:
- O01 `corpus/knowledge/oom-event-plane.md` — "exactly the band the kernel scans first" (line 116).
- O02 `corpus/knowledge/oom-event-plane.md` — "the +200 band is chosen first" (line 349).
- O03 `corpus/knowledge/kill-event-deep-r8.md` — "under a kernel OOM the scan prefers the
  higher-scored, larger-RSS tasks first" (line 147). NOTE: this one is *partly* right (the scan does
  prefer the highest-scored task), but it is not a band and not "larger-RSS first" as a separate
  ordering; the score sums RSS, swap and page tables plus the scaled adj.
- O04 `corpus/knowledge/kill-event-deep-r8.md` — "the +200 band is scanned first" (line 260).

Suggested verdict `corrected` for all four, with `now` text along these lines (marker author may
reword; M5 needs ≥12 words, no anchor substring, distinct per item):
- "The kernel makes one pass over eligible tasks and keeps the highest `oom_badness` points, where
  points are RSS plus swap entries plus page-table pages plus `oom_score_adj * (totalpages/1000)`;
  no oom_score_adj band is scanned or chosen first (S149)."
Basis cell: `S149` (passes M6: status `mined`, used-by names both files) — M7 satisfied by the
`S###` alone.

The provenance claim in oom-event-plane.md that the killed manager was +100 while +200 clients
lived is *consistent* with this code: selection is by total points, and the manager's total
exceeded the clients'. That is an inference this seat draws from the code [inf]; the event's own
numbers are in the corpus.

## 5. Provenance and limits

- URL: `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c`; fetched 2026-10-22
  ~19:58Z with `curl -sL`; 1257 lines; sha256
  `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`; no `404: Not Found` body
  (`grep -c` → 0); first line is the oom_kill.c copyright header.
- Snapshot: `.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c` (same bytes, same sha256).
- [unk] `get_mm_rss_sum` expansion (rss_anon + rss_file + rss_shmem) is not defined in this file;
  the dump header at line 425 prints exactly those three rss columns, so the three-component
  reading is inferred, not read. [unk] `oom_task_origin` and `mem_cgroup_scan_tasks` bodies.
- Not measured here: the live host's `/proc/sys/vm/oom_kill_allocating_task` value, and the
  `oom_score` userspace normalisation (fs/proc/base.c, S148's territory). This seat ran no
  counter, no git command beyond the read-only tools above, and wrote no lane file.

## 6. Files written by this seat

- `.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c` (fetched snapshot)
- `.ufo/waves/round-29/w1/ScribeSrcOomKill/linux-v7.2-mm-oom_kill.c` (first copy of the fetch)
- `.ufo/waves/round-29/w1/ScribeSrcOomKill/draft.md` (this file)
- `.ufo/waves/round-29/w1/ScribeSrcOomKill.md` (report)
