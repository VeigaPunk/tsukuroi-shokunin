# Draft — SKILL.md appended subsection (round 29, ScribeSkillOomRow)

Insertion point: append at end of file. Block below is 13 lines (limit 15), heading included; contains
no `|` inside table cells. Sources fetched and hashed by this seat, see §Provenance.

```markdown
### Kernel OOM victim selection — round 29

- **Rule** (S149 `mm/oom_kill.c:228-236`): one scalar per task, `points = rss + swapents + pgtables` in pages `+ oom_score_adj × totalpages/1000`; `select_bad_process` keeps the strict maximum in task-list order and an equal score replaces the earlier pick (`:339-341`, `:362-375`). One adj unit is 0.1 % of allowed memory, i.e. exactly one point on the 0-1000 badness scale (S148 `proc.rst:1761-1766`, `:1777-1783`).
- **totalpages** (S149 `:258`, `:263`): `totalram_pages() + total_swap_pages` for a global OOM, `mem_cgroup_get_max()` for a memcg OOM. Capture-epoch host sum is 16,909,739 pages, so one adj unit is 16,909 pages (66.05 MiB); `-1000` is not a low score but removal from candidacy (`:216-222`, S148 `proc.rst:1781-1783`).
- **Decision table**:

| trigger | totalpages used | effect of the control |
|---|---|---|
| global OOM | 16,909,739 pages at event A/B (15,861,169 today) | −1000 excluded; 0 no offset; +200 adds 3,381,800 pages (12.90 GiB) |
| memcg OOM | the memcg's `memory.max` + `swap.max`; all `max` on this host's path, so the trigger is closed | same formula at that smaller max; `memory.oom.group=1` would kill the whole cgroup (`:1040-1052`), it is 0 here |
| `oom_kill_allocating_task=1` (S150 `vm.rst:810-817`) | not consulted | kills `current` with no score at all, global path only, skipped when adj is −1000 (`:1145-1152`) |

- **Row F7 check** (`SKILL.md:1094`): the argument holds as a magnitude condition, not as a class order. A +100 manager beats a +200 app only if it holds 1,690,900 pages (6.45 GiB) more `rss+swapents+pgtables`, and 3,381,800 pages (12.9 GiB) more than each +300 Chromium; event B's per-process sizes are unmeasured (F5), so the no-kernel-kill conclusion rests on F1's `oom_kill` ledger, not on the adj class.
```

## F7 evaluation (support material, not part of the block)

Statement under test, `SKILL.md:1094` and `corpus/knowledge/kill-event-deep-r8.md:36`:
the OOM-score class argues against a kernel kill because what died was the +100 manager, not a
+200 big-RSS app (§4 of that file, `:143-150`).

Derivation under the v7.2 formula. In badness-scale units (`score = 1000 × points / totalpages`,
S148 `proc.rst:1761-1766`, `:1811-1812`), selection is
`score_i = 1000 × mem_i / totalpages + adj_i`, with `mem_i = rss + swapents + pgtables` and
`totalpages = 16,909,739`. So a +200 task with zero memory already scores 200, and the +100
manager scores `100 + 1000 × mem_mgr / totalpages`. The manager is picked only when
`mem_mgr − mem_app ≥ 0.1 × totalpages = 1,690,900 pages (6.45 GiB)` against **every** +200 task,
and `≥ 0.2 × totalpages = 3,381,800 pages (12.9 GiB)` against **every** +300 Chromium. The claim
"the class argues against a kernel kill" is therefore not implied by the class labels: it is a
quantitative gap condition that event B cannot test, because no per-process size survived
(`kill-event-deep-r8.md` F5, `:28`; §5.1 `:156-180`: only slice/service lifetime maxima, 28.5 GiB
memory peak over the whole old session). Verdict: `qualified` — direction plausible for a
`systemd --user` manager (a small daemon rarely holds 6.45 GiB more than every app), but
[inference], not an argument from the adj class, and it is not needed: F1's `/proc/vmstat
oom_kill = 1` ledger already carries "no kernel kill at event B" independently.

Counter-observation that matters more than F7's direction: event A's own dump
(`corpus/knowledge/oom-event-plane.md:101-113`) shows the +200 victim winning with 17,460,384
points against a +300 chromium at 5,091,048 — a 100-unit adj deficit bought nothing because the
memory gap was 12.37M pages, 7.3× the 1,690,900-page break-even. Any claim that a higher adj band
"wins first" fails on that row alone.

## Marker drafts for O01-O04 (append to the corpus files, not to SKILL.md)

Append to `corpus/knowledge/oom-event-plane.md` (EOF):

```
[R29-OWED-O01] verdict: rebutted | original: "exactly the band the kernel scans first" | now: No band is scanned first; `oom_badness` adds `oom_score_adj` times `totalpages/1000` to each task's rss, swapents and pagetable pages and `select_bad_process` takes the single strict maximum, so this file's own event-A dump has the +200 victim at 17,460,384 points over the +300 chromium's 5,091,048. | basis: S149, S148
[R29-OWED-O02] verdict: rebutted | original: "the +200 band is chosen first" | now: Selection is a maximum over weighted page counts, never a band order; on this host one adj unit buys 16,909 pages (66.05 MiB), so +200 buys 3,381,800 pages of credit and still loses to any task 6.45 GiB larger. | basis: S149, S148
```

Append to `corpus/knowledge/kill-event-deep-r8.md` (EOF):

```
[R29-OWED-O03] verdict: qualified | original: "under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first" | now: The scan picks the highest points, where memory in pages and `oom_score_adj` trade at `totalpages/1000` pages per point (16,909 here); a higher score is not scanned first and only shifts the weighted sum by 0.1 % of allowed memory per unit. | basis: S149, S148
[R29-OWED-O04] verdict: rebutted | original: "the +200 band is scanned first" | now: The victim is the task with the largest rss plus swapents plus pgtables plus adj-scaled points, scanned once in task-list order; event A's +200 python3 won on 14.1M pages of memory, 12.4M pages clear of the +300 chromium. | basis: S149, S148
```

Anchors verified present at the round-29 base: `oom-event-plane.md:116` and `:349`;
`kill-event-deep-r8.md:147` and `:260`. Verdict split: O03 is `qualified` because the v7.2 rule is
monotone in both memory and adj (a higher score and larger RSS do raise the chance) while the
word "first" and the implicit lexicographic priority are wrong; O01/O02/O04 claim a band scan that
does not exist and are `rebutted`.

## Notes for the integrator

1. **Registry rows required** (M6): `corpus/SOURCES.md` needs S148, S149 and S150 with `status = mined`
   and a `used-by` cell naming `oom-event-plane.md`, `kill-event-deep-r8.md` **and** `SKILL.md`
   (substring test per file). S151 (LWN "Taming the OOM killer", 2009) is not used: its formula
   predates the current `oom_score_adj` scaling and would be a reject row.
2. S148 = Linux v7.2 `Documentation/filesystems/proc.rst`; S149 = Linux v7.2 `mm/oom_kill.c`;
   S150 = Linux v7.2 `Documentation/admin-guide/sysctl/vm.rst`.
3. `mm/oom_kill.c` line anchors used above: 216-222 (`-1000` → `LONG_MIN`), 228-236 (badness sum and
   `adj *= totalpages / 1000`), 258 (memcg totalpages), 263 (global totalpages), 339-341 (max with
   strict-less skip), 362-375 (scan loops), 425 and 945-951 (dump/`Killed process` print carry
   `oom_score_adj`), 1040-1052 (`memory.oom.group` group kill), 1145-1152 (allocating-task path).
4. A fourth fetched file, `include/linux/oom.h:59-72`, defines `oom_task_origin` as the per-signal
   `oom_flag_origin` set only by the in-kernel `set_current_oom_origin()`; neither helper has a
   caller in the fetched `mm/oom_kill.c`, and the corpus dumps show no forced `LONG_MAX` pick
   (`:334-337`), so the flag does not affect the table [inf, no userspace writer observed].
5. Host drift: `/proc/meminfo` today is MemTotal 31,721,800 kB, SwapTotal 31,722,876 kB, and
   `/proc/swaps` lists only `/swap/swapfile` — `/sys/block/zram0` is gone, so today's totalpages is
   15,861,169 (unit 15,861 pages, 61.96 MiB) against the capture epoch's 16,909,739. Use the
   capture-epoch number when writing about events A and B; the table prints both.
6. Live sysctls read for the table: `oom_kill_allocating_task=0`, `panic_on_oom=0`,
   `oom_dump_tasks=1`, `overcommit_memory=0`.

## Provenance (fetched bytes in this directory)

| id | file | URL | lines | sha256 |
|---|---|---|---|---|
| S149 | `oom_kill.c` | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | 1257 | 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e |
| S148 | `proc.rst` | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/filesystems/proc.rst | 2495 | e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126 |
| S150 | `vm.rst` | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.2 | 1153 | bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce |
| — | `oom.h` | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/oom.h | 114 | 42e8e17f6eda1a48e8455a55fe6aa4114ae121c35e665bfd19e474dacf77b7fd |

`vm.rst` came from the kernel.org cgit plain endpoint because raw.githubusercontent.com answered
HTTP 429 on that file twice; cgit serves the same tagged tree. Quotable substrings were verified
with `grep -cF` (each returned 1): `adj *= totalpages / 1000;`, `oc->totalpages = totalram_pages() + total_swap_pages;`,
`oc->totalpages = mem_cgroup_get_max(oc->memcg) ?: 1;`, `The value of /proc/<pid>/oom_score_adj is added to the badness score before it`,
`If this is set to zero, the OOM killer will scan through the entire`.
