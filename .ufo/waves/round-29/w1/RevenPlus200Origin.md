# RevenPlus200Origin — where the "+200 band scanned first" reading came from

Verdict: the reading is lane-born, not source-born. It entered tsukuroi in the 2026-10-14
probation commits as an uncited inference from a memory dump, and no committed source in
either lane ever says a band is scanned first — every source that speaks to it says the
opposite.

## Findings

1. **Earliest occurrence — the "scans/chosen first" phrasing.** Commit `dc3436d`
   (probation round 6 / training r5, 2026-10-14 15:17-03) creates
   `corpus/knowledge/oom-event-plane.md` already carrying both variants:
   `oom-event-plane.md:115-116` at that commit — "user workload ran at +200 (and Chromium
   helpers at +300), which is exactly the band the kernel scans first" — and the §8 row-6
   cell "the +200 band is chosen first" (now `oom-event-plane.md:349`).
   Commit `72b038d` (probation round 8 / training r7, 2026-10-14 16:55-03) creates
   `corpus/knowledge/kill-event-deep-r8.md` carrying "[inference] under a kernel OOM the
   scan prefers the higher-scored, larger-RSS tasks first" (now line 147) and the §7 row-6
   cell "the +200 band is scanned first" (now line 260). `git log -S`/`--follow` over both
   files shows the phrasing present at file creation and untouched since; the round-25
   repairs (`c93bd70`) touched neither line. `git log -S 'scans first'`/`'scanned first'`
   over the whole history returns no earlier author.

2. **Sources cited then: none.** Both probation-era notes cite only "live read-only probes
   on host plazir27 — journalctl …" (`dc3436d:corpus/knowledge/oom-event-plane.md:3`);
   there is no `corpus/SOURCES.md` in the `dc3436d` tree (registry begins at `549ec0c`,
   round 1, 2026-10-19), so the claim predates the lane's S### citation regime. The
   evidentiary base was the event-A kernel dump: the `oom_score_adj` histogram
   `-1000`×1 … `200`×120, `300`×15 (`oom-event-plane.md:115`) and the 164-row task dump
   where the python3 victim at +200 held 26.6 GiB anon. Neither dump line describes scan
   order; "the band the kernel scans first" is the author's interpolation of "higher
   oom_score_adj → killed earlier" into a band-scan mechanism, applied to steering advice
   ("a known-huge batch job placed differently changes who dies"). [inf] The original
   intent was actionability — put heavy jobs in a different band — not a kernel
   description; the mechanism was asserted to justify the lever.

3. **No committed source ever said a band is scanned first.** Grep over
   `corpus/SOURCES.md`, the wave source snapshots under `.ufo/waves/*/sources/`, and all
   corpus files finds the phrase only in the two origin notes and in later files quoting
   it as the *disputed* claim (`corpus/knowledge/adjacency-mori-oom-r27.md:34`,
   `corpus/lessons/round-27.md:81`, `round-27-verifier-spotcheck.md:103`, `SCORECARD.md`,
   `tools/check-owed-statements-r29.py:8,49-55`). The only source that adjudicates it,
   `mm/oom_kill.c` (tsukuroi S119/S149 = mori S003, sha256
   `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`), is cited for a
   single full walk that keeps the highest points (`corpus/SOURCES.md:155`, S149 row).
   [obs] The reading was therefore never source-backed on either side.

4. **Mori's round-27 correction.** `mori-shokunin/corpus/knowledge/oom-victim-selection-r27.md`,
   Adjacency section. Wave-1 commit `126e192` (2026-10-22 12:50) already says "the kernel
   does not scan the +200 band first, it makes one pass and keeps the highest adjusted
   score (S003 `mm/oom_kill.c:228-234,340`)"; wave-2 commit `b89ac34` (14:15) hardened the
   tie rule (first task scanned → last) and named the four lane lines. HEAD text:
   `oom-victim-selection-r27.md:195-197` — "`oom-event-plane.md:116,349` and
   `kill-event-deep-r8.md:147,260` say the +200 band is scanned or chosen first: the
   kernel walks every task of the OOM domain once and keeps the highest badness,
   footprint plus `adj * totalpages / 1000` pages, with a tie going to the later task
   (S003 `mm/oom_kill.c:228-234,340-348,358-376`)", followed by "tsukuroi's conclusions at
   those lines still hold" (`:198`). Mori pins tsukuroi `157ee255` (blobs `e5f8b613`,
   `7dc5337f`); at that rev `kill-event-deep-r8.md:147` is the "scan prefers the
   higher-scored … tasks first" inference and `:260` the "scanned first" cell — the
   citations resolve.

5. **Why it survived: no gate ever scanned these files, then explicit deferral.** The two
   notes predate SOURCES.md and sit outside every committed checker — `grep` of
   `tools/*.py` shows the knowledge-file checkers are bounded to their own named records
   (e.g. `check-section-citations.py` checks only the r16 errata file pair); nothing lints
   `oom-event-plane.md`/`kill-event-deep-r8.md` for kernel-mechanism claims. Round 27's C2
   overlap register recorded mori's correction as *inbound* debt without absorbing it
   (`corpus/knowledge/adjacency-mori-oom-r27.md:34`; `corpus/lessons/round-27.md:81` —
   "Not checked this round"). The round-27 verifier spot-check routed it as defect 5
   (`corpus/lessons/round-27-verifier-spotcheck.md:103`, committed at `3b9e043`); the
   round-28 spot-check carried it again (`round-28-verifier-spotcheck.md:91`, item 5).
   [inf] The missed gate is thus twofold: the probation-era authoring gate had no
   source-citation rule at all, and the round-27/28 routing gates only deferred the known
   defect — round-29 C1 (O01–O04, counter `tools/check-owed-statements-r29.py`, rule M7
   demanding a source opened this round) is the first instrument that mechanically binds
   a correction to a cited kernel source.

## Provenance notes

- All lane commands read-only (`git log -S`, `git show`, `git ls-tree`, `grep`); mori
  accessed read-only. No GIT_* set; no writes to lane files outside this report path.
- `kill-event-deep-r8.md:260` also carries the related open item "the +200 origin is
  [unknown]" (Q12, line 295), which mori's Fact 3 answers — same adjacency paragraph.

Scope: read=lane+moro git history, SCORECARD, spot-check lessons, counter docstring, QUALITY 67; wrote=.ufo/waves/round-29/w1/RevenPlus200Origin.md; executed=git log/show/ls-tree (read-only), grep, sed, awk — no writes to repositories
Model: not exposed
Installs: none
