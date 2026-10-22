# S151 reject draft — LWN "Taming the OOM killer" (2009) vs v7.2 `oom_badness`

Verdict: reject S151. The article describes a 2009 badness heuristic whose every scoring term is
absent from the v7.2 rule, so it has no operand in this round's kernel victim-selection statements;
a rejected row is also inert for C1 because rule M6 of the owed-statement counter accepts only
`status mined` rows. Admit is not better (evidence in §5).

Round-29 seat ScribeSrcReject. Revision under attack 81a061a67466c5e1be812814a895a4b5ed89b4ff
(the declaration commit); the lane working tree sits at HEAD 3c94d7308e561832a0df0981cbc39dda270e32d8
(the receipts commit). Absence checks below were run at both revisions and agree.
No lane file is edited by this draft; the integrator appends the rows in §6 and §7.

## 1. Fetch record

| item | value |
|---|---|
| URL | https://lwn.net/Articles/317814/ |
| fetch | plain `curl -sL`, HTTP 200, 105310 bytes, 2026-10-22; no challenge encountered |
| snapshot | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html` |
| sha256 | `b988b931cb476b36d93d523f9cd98195f45546930ac61a6657bc3fdf5966bcdc` |
| identity | title `<h1>Taming the OOM killer</h1>` (line 56); `<p>February 4, 2009</p>` (line 60); `<p>This article was contributed by Goldwyn Rodrigues</p>` (line 61); section `<h3>Who's Bad?</h3>` (line 104) |
| pin | none: the page carries no kernel-version statement and LWN pages are mutable, so only the hash pins the bytes |

Counterpart opened for the comparison:

| item | value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c |
| fetch | plain `curl -sL`, HTTP 200, 34311 bytes, 1257 lines, 2026-10-22 |
| snapshot | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSrcReject/oom_kill-v7.2.c` |
| sha256 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` |
| identity | tag `v7.2` in the raw URL; `long oom_badness(struct task_struct *p, unsigned long totalpages)` at line 199 |

## 2. What the 2009 article says the score is (all lines in `lwn-317814.html`)

- `oom_adj` range −17 to +15; −17 removes the process from consideration (lines 94-101).
- Score inputs: "The badness score is computed using the original memory size of the process,"
  plus `its CPU time (utime + stime),  the run time (uptime - start time) and` plus
  `its <tt>oom_adj</tt> value.` (lines 113-115). A longer-lived process scores lower (line 117).
- A task inside `swapoff()` is killed first (lines 120-122); "Half of each child's memory size is
  added to the parent's score" (line 124).
- Multipliers: nice > 0 doubles (line 131); `CAP_SYS_ADMIN`, `CAP_SYS_RESOURCE` or
  `CAP_SYS_RAWIO` divide by 4, cumulative to 16 (lines 134-137); a cpuset mismatch divides by 8
  (lines 138-140); then the score is shifted by `oom_adj`, `points <<= oom_adj` positive and
  `points >>= -(oom_adj)` otherwise (lines 142-145).
- "The task with the highest badness score is then selected and its children are killed."
  (lines 149-150).

## 3. What v7.2 `oom_badness` actually does (lines in `oom_kill-v7.2.c`)

- Signature and purpose: return the highest value for the task consuming the most memory
  (lines 190-199).
- `oom_unkillable_task()` (definition lines 160-167: global init or `PF_KTHREAD` → `LONG_MIN`)
  at line 204.
- `adj = (long)p->signal->oom_score_adj;` (line 216); `adj == OOM_SCORE_ADJ_MIN`,
  `MMF_OOM_SKIP` or `in_vfork(p)` → `LONG_MIN` (lines 217-222).
- `points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) + mm_pgtables_bytes(p->mm) / PAGE_SIZE;`
  (lines 228-229).
- `adj *= totalpages / 1000; points += adj;` (lines 233-234), i.e. the adjustment is linear in
  units of 0.1 % of allowed pages, not a power-of-two shift.
- Whole-file token counts (`grep -cE` over all 1257 lines): `nice` 0, `utime` 0, `stime` 0,
  `uptime` 0, `start_time` 0, `CAP_SYS_ADMIN` 0, `CAP_SYS_RESOURCE` 0, `CAP_SYS_RAWIO` 0,
  `children` 1 — and that single hit is the unrelated comment at line 1017.

## 4. Divergence

| 2009 article term | v7.2 status | evidence |
|---|---|---|
| original memory size as the base | replaced by RSS + swapents + page tables | `oom_kill-v7.2.c:228-229` |
| CPU time `utime + stime` | absent | token count 0 |
| run time `uptime - start_time` | absent | token counts 0 and 0 |
| nice > 0 doubles the score | absent | token count 0 |
| capability divisors 4 and 16 | absent | token counts 0 |
| cpuset divisor 8 in the score | absent (cpuset appears only in `oom_cpuset_eligible`, lines 90-126, an eligibility filter) | lines 90-126 and token count |
| half of each child's memory | absent | `children` 1, line 1017 comment only |
| shift by `oom_adj` (×2^adj) | replaced by `oom_score_adj` scaled linearly by `totalpages/1000` | lines 232-234 |
| −17 excludes the task | analogue is `OOM_SCORE_ADJ_MIN` → `LONG_MIN` | lines 217-222 |
| highest score, children killed | highest value is the goal; no child-killing code in this file | lines 196-197, `children` count |

Consequence: an article-only statement about the current rule would be wrong on eight rows outright,
partly wrong on a ninth (the highest-score goal survives at lines 196-197 but child-killing has no
counterpart), and only the unkillable marker overlaps, already carried by the primary sources S148
and S149 that this round reserves.

## 5. Why reject, not admit

- No shared rule: the 2009 text cannot ground any v7.2 behaviour statement; admitting it would
  invite exactly the cross-era transfer the lane's source rules forbid.
- Claim mechanics: C1 rule M6 counts a basis reference only when the `S###` row has
  `status mined` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-owed-statements-r29.py:27-28`).
  A rejected row cannot mark O01-O04, so the row is honest bookkeeping, not support.
- Tier: secondary contributed article with no kernel-version statement, so tier C; QUALITY 7
  says tier C is never sole support (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:11`).
- The admit case would be historical texture (the pre-`oom_score_adj` era). The round has no
  historical claim, and the article does not state which kernel it describes, so it cannot even
  anchor a history statement without a version-pinned kernel file for that era. Reject stands.

## 6. Draft SOURCES.md row (append after S147; 11 columns)

```
| S151 | LWN.net — Taming the OOM killer (Goldwyn Rodrigues, 2009-02-04) — https://lwn.net/Articles/317814/ | docs | C | The 2009 out-of-memory badness heuristic (original memory size, CPU time, run time, oom_adj, nice and capability and cpuset divisors, child-memory halving) as candidate historical context for the OOM victim-selection statements O01 to O04; the article states no kernel version | § "Who's Bad?" line 113; plain curl HTTP 200 2026-10-22, 105310 bytes, sha256 b988b931cb476b36d93d523f9cd98195f45546930ac61a6657bc3fdf5966bcdc; snapshot .ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html; dated 2009-02-04; no version pin | REJECTED for this round: every scoring term it lists is absent from the v7.2 rule (S149), which scores RSS plus swapents plus page tables and adds oom_score_adj scaled to 0.1% of totalpages, and whole-file token counts for nice, utime, stime, uptime, start_time and the three CAP_SYS names are 0; a 2009 secondary article cannot ground a v7.2 behaviour statement, and C1 rule M6 accepts only mined rows; flip: a claim is explicitly historical (the pre-oom_score_adj rule as predecessor) and is grounded in a version-pinned kernel file of that era, with this article cited only as commentary | rejected | 2026-10-22 | on-release | corpus/lessons/round-29.md |
```

## 7. Draft Gate row (round-29 `## Gate`, six-column header of `corpus/lessons/round-28.md:9`)

```
| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |
|---|---|---|---|---|---|
| S151 | https://lwn.net/Articles/317814/ | 2026-10-22 | "The badness score is computed using the original memory size of the process," | `.ufo/waves/round-29/w1/ScribeSrcReject/lwn-317814.html` line 113, sha256 `b988b931cb476b36d93d523f9cd98195f45546930ac61a6657bc3fdf5966bcdc` | **reject**: the 2009 heuristic it describes has no surviving operand in v7.2 `oom_badness` (S149:199-237) — the score's CPU-time, run-time, nice, capability, cpuset, child-memory and shift terms all read 0 by `grep -cE` — so it cannot ground O01-O04, and C1 rule M6 accepts only `mined` rows. Flip: a version-pinned pre-`oom_score_adj` kernel file grounds the historical claim and this article is cited only as commentary |
```

## 8. Quote and shape verification

- `grep -cF "The badness score is computed using the original memory size of the process," lwn-317814.html` → `1`; the quoted string is 13 whitespace-separated words (limit 25).
- Rejected earlier candidate: the full sentence joined across the line wrap, "The badness score is computed using the original memory size of the process, its CPU time (utime + stime), the run time", `grep -cF` → `0`, because the page wraps at line 113 and has two spaces before `the run time` on line 114. It is not verbatim and must not be quoted.
- SOURCES row: 11 pipe-separated cells, order `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`, `status` = `rejected`.
- Gate row: 6 cells, matching the header `| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |`.

## 9. Limits and notes for the integrator

- [obs] `corpus/SOURCES.md` has no `S151` row at either revision (`git show 81a061a:corpus/SOURCES.md | grep -c '^| S151'` → 0 and the same at HEAD 3c94d730 → 0; last row is S147), so the append is clean.
- [obs] `.ufo/waves/round-27/w1-spec.json` had proposed `S151` for an Arch `nvidia-open` PKGBUILD source that never landed (`.ufo/waves/round-27/w2a2/RevRowKT4.md:21`, "The wave-1 plan registered S150 ... and S151 ... but those seats died at spawn"); no registry collision exists, but the id is contested if that source is ever mined.
- [inf] The `used-by` cell names `corpus/lessons/round-29.md`, which does not exist at 81a061a (`git cat-file -e 81a061a:corpus/lessons/round-29.md` → exit 128); it is the file this Gate row lands in. If the lesson lands under another name, update the cell.
- [unk] Whether the article matched its own era's kernel code: no pre-`oom_score_adj` kernel file was fetched, and the article names no version. Nothing here asserts it did or did not.
- [inf] Tier C rests on the row being a secondary contributed article with no version pin; `corpus/SOURCES.md` carries no explicit A/B/C legend, so C follows the community/secondary usage of S036, S037, S030 and S033.
- [obs] The lane working tree is dirty from sibling seats: `git status --porcelain` shows `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, three corpus knowledge files and `tools/check-kernel-taint.py` modified plus the untracked round-29 wave directory. The `corpus/SOURCES.md` diff is `2 insertions(+), 2 deletions(-)` and rewrites only rows S133 and S134 in place; no new row exists and S147 is still last, so the append point above is unchanged in the edited file.
- This draft changes no counter value: C1 stays at its before-count because a rejected row cannot satisfy M6.
