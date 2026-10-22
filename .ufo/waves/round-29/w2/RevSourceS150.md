# RevSourceS150 — round 29 wave 2, S150 re-open and admit-decision check

Verdict: the S150 Gate row is byte-accurate and the source qualifies as `mined`, but the admit
justification is wrong about who uses it — no O01–O04 marker cites S150, so it was not needed for
the O01–O04 corrections; I partly disagree with the admit decision as recorded (the `mined` status
is defensible only via SKILL.md, and the landed used-by cell overclaims two files).

## Findings

1. [obs] Bytes verify. Fresh `curl -sL` of the Gate-row URL
   `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/admin-guide/sysctl/vm.rst?h=v7.2`
   returned 42424 bytes / 1153 lines, sha256
   `bf8ca0265fefc019250697b6ee47a0679709b2ee45f4d1893b3dfd95c1f8c1ce` — identical to the committed
   snapshot `.ufo/waves/round-29/w1/ScribeSrcSysctlVm/S150-vm.rst` (same sha256 on both files) and
   to the Gate row value (`corpus/lessons/round-29.md:13`). Saved at
   `.ufo/waves/round-29/w2/RevSourceS150/S150-vm.rst`.
2. [obs] Quote verifies verbatim. `grep -cF 'If this is set to zero, the OOM killer will scan
   through the entire'` on my fetched bytes → 1, at line 810 (14 words, under the 25-word cap);
   section heading `oom_kill_allocating_task` at :804; the non-zero branch "simply kills the task
   that triggered the out-of-memory condition" spans :815-817 as the Gate row states; "The default
   value is 0." at :822. The declared raw.githubusercontent.com URL still returns HTTP 429 today —
   body is the recorded 199-byte page (sha256 `6850b0e5d07bed32b3613d4c7da50e0fc36542239a5ff5188b524494e9edda75`,
   `.ufo/waves/round-29/w2/RevSourceS150/vm.rst`), so the documented kernel.org substitution is
   reproducible and honestly recorded in the row.
3. [obs] No O01–O04 marker cites S150. Landed basis cells at lane tip `10d5288f` (HEAD confirmed):
   O01 `corpus/knowledge/oom-event-plane.md:497` basis = "S149 (mm/oom_kill.c lines 228-233, 263,
   340, 359-377) and S148 (...)"; O02 `:499` = S149 + S148; O03
   `corpus/knowledge/kill-event-deep-r8.md:400` = "S149 (mm/oom_kill.c lines 306-377, 1122,
   1145-1151) and S148 (...)"; O04 `:402` = S149 + S148. `grep -n 'S150'` over
   `oom-event-plane.md`, `kill-event-deep-r8.md`, `memory-pressure-r25.json`,
   `driver-firmware-plane.md` and `storage-health-r26.json` returns zero hits (exit 1). M7
   (`tools/check-owed-statements-r29.py:39-41`) needs only "at least one" new S###, which S148/S149
   supply; S150 is mechanically unnecessary for every kernel item.
4. [obs] The lesson's sourced-claim sentence is factually wrong: `corpus/lessons/round-29.md:2`
   says "O01 to O04 cite S148, S149 and S150" — should read "S148 and S149". The S148 Gate row's
   "used-by the O01 to O04 correction markers" claim is accurate only for S148/S149.
5. [obs] The landed registry row `corpus/SOURCES.md:156` (11 cells, status `mined`, opened
   `2026-10-22`) names used-by `corpus/knowledge/oom-event-plane.md,
   corpus/knowledge/kill-event-deep-r8.md, SKILL.md, corpus/lessons/round-29.md`. The two knowledge
   files contain no `S150` string at all (finding 3) — two false used-by entries. `SKILL.md` is a
   real use (`SKILL.md:2545` cites "S150 `vm.rst:810-817`" in section "Kernel OOM victim selection —
   round 29", `SKILL.md:2535`) and `corpus/lessons/round-29.md` cites "S150 lines 810-817" in the
   "What the sources settle" paragraph — those two entries are accurate.
6. [obs] The wave-1 scribe's own landing condition
   (`.ufo/waves/round-29/w1/ScribeSrcSysctlVm/draft.md:128-132`) said: keep `mined` and that
   used-by "only if the landed O01–O04 markers cite `S150` in their `basis` cell. If they cite
   `S149` only, set the status to `queued` and `used-by` to `—`". That condition was not met —
   markers cite S149 only — yet the row landed `mined` with the scribe's original used-by intact.
   [inf] The SKILL.md citation (a row the scribe's condition predated) independently justifies
   `mined`, so the status is defensible; the defect is the stale used-by cell and the lesson's
   "cite … S150" claim, not the status itself.
7. [inf] Substantively, S150 is not needed for O01–O04 either. The corrections establish "no band
   ordering"; S149's code (single running-maximum pass, `select_bad_process`) is the proof — even
   O03's "allocating-task … bypasses" clause grounds on S149:1145-1151 (the
   `sysctl_oom_kill_allocating_task` code path). S150 adds only the documented semantic and the
   default-0 fact, which the scribe itself flagged as overstatement if cited alone
   (`draft.md:117-118,232`).

## Judgment

Disagree with the admit decision as recorded: the Gate row's technical content (URL, sha256,
quote, locations, default, host value) is fully verified, and `mined` is the right status — but
on the strength of `SKILL.md:2545` and the lesson's own use, not on the stated/registered claim
that the O01–O04 markers used it. The lesson claim "O01 to O04 cite S148, S149 and S150" and the
SOURCES used-by entries for the two knowledge files are false and should be corrected to S148 and
S149 for the markers, with S150's used-by reduced to `SKILL.md, corpus/lessons/round-29.md`.

Residual risk [inf]: a future M6-style check would accept an `oom-event-plane.md` or
`kill-event-deep-r8.md` marker citing S150 as used-by-consistent even though no such citation
exists — the stale cell inflates the row's reach but does not break today's count (0 markers cite
it). [unk] Whether the L1 intends a used-by cell to mean "files citing this source" or "files this
round intended to cite" — under the former reading the row is defective, under the latter merely
aspirational.

Scope: read=corpus/lessons/round-29.md, corpus/SOURCES.md:156, tools/check-owed-statements-r29.py:2-63, marker lines in corpus/knowledge/{oom-event-plane,kill-event-deep-r8}.md, SKILL.md:2535-2545, w1 ScribeSrcSysctlVm/ScribeSkillOomRow/CritOwedCounterShapes artifacts, fetched vm.rst:800-824; wrote=.ufo/waves/round-29/w2/RevSourceS150/{vm.rst,S150-vm.rst,RevSourceS150.md}; executed=curl -sL (2 URLs), sha256sum, wc, grep -cF/-n, sed -n, git rev-parse/status (read-only), python3 cell-split
Model: devin/swe-2 (workstation context)
Installs: none
