# ScribeMarkersOom — C1 draft, O01–O04 (kernel OOM victim selection)

Done: four source-backed markers and two correction sections are drafted, with the verdict split the
L1 relayed from RevOomMechanism (O01/O02/O04 `corrected`, O03 `qualified`); all four pass the real
counter (`ok:true`, `marked` 4) in a sandbox fixture that also carries simulated S148/S149 registry
rows, and the same markers fail exactly at M7 without those rows. The kernel reading they replace
(a "+200 band" visited first) is false, while §2.3's victim conclusion survives unchanged.

1. [obs] Before-value reproduced at the declaration commit. `python3
   tools/check-owed-statements-r29.py --revision 81a061a67466c5e1be812814a895a4b5ed89b4ff --lane
   /fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersOom/repo` → last line `{"items": 12, "marked": 0,
   "unmarked": ["O01", ..., "O12"]}`; counter `counter_sha256
   5b6cf227580ff26e47db5888001febc7ff38b97322bd496121a6aa84c2dc6375`.

2. [obs] Marker shape accepted by the canonical counter in three fixtures. Sandbox fixture commit
   `1298a86f1e9a7e30fa8e955714754e013b90c71c` pairs my two appended sections with the **actual**
   working-tree `corpus/SOURCES.md` (the sibling-drafted S148/S149 rows): O01 `corrected`, O02
   `corrected`, O03 `qualified`, O04 `corrected`, each `"ok": true`, `basis.sources ["S149","S148"]`,
   `basis.unresolved []`; summary `marked 4`, unmarked O05–O12 (sibling seats' items). An earlier
   fixture (`a857461c…`, simulated S148/S149 rows) and my pre-L1 fixture (`c4a2ada…`) also passed, so
   the verdict change is shape-neutral.

3. [obs] The integration dependency is exact, not guessed. Same markers, registry restored to the
   declaration state (no S148/S149 rows): O01–O04 each fail `"why": "M7 no S### reference that passes
   M6 (bad=['S149', 'S148'])"`. The rows are already drafted in the lane working tree —
   `corpus/SOURCES.md:154` (S148) and `:155` (S149), both status cell `mined`, `used-by` cell
   `corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md, SKILL.md,
   corpus/lessons/round-29.md` — so integration only has to land them together with the markers; the
   two note files themselves are unmodified in the working tree (`git status` clean for both).

4. [obs] Kernel mechanism, quoted from the fetched bytes (each verified with `grep -cF` → 1, ≤25 words,
   line numbers in the fetched files):
   - `mm/oom_kill.c:228` — `points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) +`
   - `mm/oom_kill.c:233` — `adj *= totalpages / 1000;`
   - `mm/oom_kill.c:340` — `if (points == LONG_MIN || points < oc->chosen_points)`
   - `mm/oom_kill.c:359` — `Simple selection loop. We choose the process with the highest number of`
     (`select_bad_process` spans 362–377; the global path walks all processes at 371–374, the memcg
     path scans only the failing cgroup at 367)
   - `mm/oom_kill.c:263` — `oc->totalpages = totalram_pages() + total_swap_pages;`
   - `mm/oom_kill.c:367` — `mem_cgroup_scan_tasks(oc->memcg, oom_evaluate_task, oc);`
   - `Documentation/filesystems/proc.rst:1777` — `The value of /proc/<pid>/oom_score_adj is added to the badness score before it`
   Reading: `oom_badness()` returns rss + swap entries + page-table pages + `oom_score_adj *
   (totalpages / 1000)`, and `select_bad_process()` keeps the single largest value over the tasks it
   walks. It is a plain argmax, with no band and no visit order; ties go to the later task because the
   test is `points < chosen_points`.

5. [obs] Bypass paths the reviewer raised are in the correction sections, with code lines: `oom_task_origin()`
   forces `points = LONG_MAX` (`mm/oom_kill.c:334-337`); `task_will_free_mem(current)` selects the
   allocating task before the walk (`mm/oom_kill.c:1122`); `sysctl_oom_kill_allocating_task` kills
   current instead of scanning (`mm/oom_kill.c:1145-1151`, gated on `!is_memcg_oom`). O03's basis cites
   these line ranges under S149.

6. [obs + inf] Quantitative effect of the adjustment, both bases stated because the host's swap total
   changed since event A. Live `/proc/meminfo`: MemTotal 31,721,800 kB, SwapTotal 31,722,876 kB =
   63,444,676 kB = 60.505 GiB → `totalpages / 1000` = 15,861. Event A's recorded SwapTotal
   35,917,176 kB (`corpus/knowledge/oom-event-plane.md:264`, swapfile plus zram) with MemTotal
   31,721,780 kB (`corpus/knowledge/kill-event-deep-r8.md:182`) = 16,909,739 pages = 64.5 GiB →
   `totalpages / 1000` = 16,909. Therefore +100 = 1,586,100 points (6.05 GiB) live or 1,690,900
   (6.45 GiB) at event A; +200 = 3,172,200 (12.1 GiB) / 3,381,800 (12.9 GiB); +300 = 4,758,300
   (18.15 GiB) / 5,072,700 (19.35 GiB); −900 = −14,274,900 (−54.5 GiB) / −15,218,100 (−58.05 GiB), so a
   −900 task only loses if its footprint exceeds that credit. Event A's victim held 6,968,424 rss +
   7,110,160 swapents = 14,078,584 pages (53.7 GiB) = 888 points before any adjustment (833 on event
   A's totalpages), against 301 for the best +300 Chromium helper
   (`corpus/knowledge/oom-event-plane.md:106,111`); it held 97.6 % of the dump's anon RSS and 86.4 % of
   its swap entries. [inf] The +200 credit was roughly a quarter of its raw points and did not decide
   the kill, so §2.3's conclusion survives. The L1's "≈ 60.6 GiB" matches the live reading rounded up
   (60.505 GiB); the 0.1 GiB gap is rounding, not a different measurement.

7. [obs] Verdicts and `now` texts: O01 `corrected` (64 words), O02 `corrected` (59), O03 `qualified`
   (50), O04 `corrected` (52); each `now` states the argmax mechanism, the host quantities and, for
   O01/O02, that the victim reading stands. No `now` repeats an anchor, contains a pipe, or repeats
   another item's `now` (real counter M5 plus a local pre-check both clean).

8. [obs] Append-only discipline: against `81a061a` the sandbox diff is 24 added / 0 removed lines for
   `corpus/knowledge/oom-event-plane.md` and 21 added / 0 removed for
   `corpus/knowledge/kill-event-deep-r8.md`; the anchored sentences remain verbatim (M1 holds).

9. [obs] Deliverable bytes: `.ufo/waves/round-29/w1/ScribeMarkersOom/draft.md` (sha256
   `84bbca987f18460722b6624ad2640d557e583fa22b582691548a432932e852f6`), one fenced block per target file
   with the heading `## Correction (round 29) — kernel OOM victim selection`, a short [obs]/[inf]/[unk]
   paragraph, and the two marker lines as single unbroken lines.

10. [obs] Source bytes saved for the registry drafter, under
    `.ufo/waves/round-29/w1/ScribeMarkersOom/`: `oom_kill.c` (1257 lines, sha256
    `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`), `proc.rst` (2495 lines, sha256
    `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`). The first `proc.rst` fetch
    returned a GitHub 429 page (one line); it was discarded and refetched with a descriptive
    User-Agent. The sibling-drafted registry rows carry exactly these two sha256 values
    (`corpus/SOURCES.md:154-155`), an independent match on the bytes I fetched. The superseded
    `c4a2ada…` fixture carried the stale 429-page sha `6850b0e5…` — registry drafters must not reuse it.

11. [unk] The exact `totalram_pages()` value is not readable read-only here (`dmesg_restrict=1`, per
    `corpus/knowledge/kill-event-deep-r8.md:262`); MemTotal is the notes' stand-in and the integer term
    is insensitive to the reserved-page margin. The S148/S149 rows as drafted name both basenames
    (`corpus/SOURCES.md:154-155`), so M6 is satisfied for both files; if a later edit narrows either
    `used-by` cell to one basename, the marker in the other file fails M6.

Out of scope and untouched: O05–O12 markers (`SKILL.md`, `corpus/knowledge/memory-pressure-r25.json`,
`corpus/knowledge/driver-firmware-plane.md`, `corpus/knowledge/storage-health-r26.json`), the
S148–S151 registry rows, product tools, SCORECARD and all judge artifacts.

Seat containment: every git write ran in
`/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersOom/repo` (clone of the lane at `81a061a`, fixture
commits only) with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`; no git or jj write ran in the
lane or the fleet repo, and nothing was written to the fleet repo.

Report: .ufo/waves/round-29/w1/ScribeMarkersOom.md
Scope: read=SCORECARD.md round-29 declaration; tools/check-owed-statements-r29.py; corpus/knowledge/oom-event-plane.md and kill-event-deep-r8.md (context ranges); corpus/SOURCES.md (S145-S147 rows, header, tail); /proc/meminfo and /proc/swaps (read-only); fetched https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c and .../Documentation/filesystems/proc.rst; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeMarkersOom/{draft.md,oom_kill.c,proc.rst}, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeMarkersOom.md, and /fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersOom/{draftgen.py,repo}; executed=curl -sL (two kernel files, one refetch), git clone/checkout/add/commit/rev-parse/diff/status in the sandbox, cp of the lane working-tree corpus/SOURCES.md into the sandbox, python3 tools/check-owed-statements-r29.py --revision 81a061a... and --revision <fixture HEAD> (five runs), python3 draftgen.py {write,apply,check}, grep/sed/sha256sum reads
Model: opencode-go/deepseek-v4.1-flash
Installs: none
