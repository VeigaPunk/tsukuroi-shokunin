VERDICT: defect-found

# R52RevLesson51 — W-D4

Axes: calibration (historical claims match immutable evidence); lesson (resolvable mistake pointers, existing rules, checkable rejection flip).

Reviewed `corpus/lessons/round-51.md` at `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` only. Lane paths below refer to that revision unless another revision is named. Fleet report/prompt references refer to fleet commit `daf5b626f0d45eb34b01957bc7d629d62c7cc243`, not its mutable working tree.

## Findings by severity

### LOW — wrong section in the misroot evidence pointer

`corpus/lessons/round-51.md:41` points to round-51 report §“Landed changes” for the misroot paragraph. The actual paragraph is in **Work performed**, fleet `.ufo/reports/round-51/tsukuroi.md:54-56`; **Landed changes** starts at line 58. The alternate spot-check pointer resolves, so this does not invalidate the incident, but the specifically named report locator is wrong.

Exact fix: replace `round-51 report §"Landed changes" (misroot paragraph)` with `fleet .ufo/reports/round-51/tsukuroi.md at daf5b626f0d45eb34b01957bc7d629d62c7cc243, §Work performed, lines 54-56 (misroot paragraph)`.

Observed command: `git -C /home/vgpnk/Projects/shokunin grep -n -E 'Misroot:|## Landed changes|## Work performed' daf5b626f0d45eb34b01957bc7d629d62c7cc243 -- .ufo/reports/round-51/tsukuroi.md` locates Work performed at 19, Misroot at 54, Landed changes at 58.

## Per-item disposition

### (a) Historical factual claims — holds, except the locator above

- Lesson lines 3-8: the original fleet report introduction, lines 7-17, explicitly records the interrupted round, no w2 dispatch, and incomplete filing. Executed `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c 6d051ef0 6abef5d0 91227829 --stat`: observed FREEZE (21 files), w1 spec/dispatch (54 seats; 6 files), pre-w2 AMENDMENT 1 (13 files), and final incomplete evidence landing (412 files). `git ... show b4d7d9d5 --stat` identifies the 90-line non-author spot-check landing.
- Lines 12-17: `6abef5d0:.ufo/waves/round-51/frozen/FROZEN.md` declares the three candidates and the counted w2 18-seat cohort; its Amendment 1 changes C2 from four to five cheats. `91227829:.ufo/waves/round-51/before/c1-at-base.json:1` has `marks_ok:0`, `seats_ok:0`, `verdicts_ok:0`. The committed C1 amend1 battery's final K-pass row has 18 synthetic seats and marks 3; the lesson correctly distinguishes that capability control from actual admission. The original report says no integrated measurement occurred.
- Lines 18-24: `git ... show 91227829:.ufo/waves/round-51/before/c2-cheats-at-amend1.json` emits no bytes, matching the final commit's zero-line stat. The original report's Work performed explicitly admits deleting scratch while the scorer was executing. Frozen `.ufo/waves/round-52/inherited/c2-cheats-at-amend1.json:1` preserves the later failed output: revision `6abef5d0...`, `real_pass:0`, `cheats:5`, `cheats_rejected:1`, `r50_cheats_rejected:0`, all six r50 rows ERROR/rc2, and r51 F1 FAIL/rc1 with mutation/equivalence legs zero. The companion `.rc:1` says `exit 1`.
- Lines 33-35: executed `git ... diff c0ad548a 91227829 -- corpus/SOURCES.md corpus/lessons LOG.md`; output empty. The committed start and end census receipts both end `ok .../corpus/SOURCES.md`, `exit 0`; spot-check lines 56 and 71 supply the unchanged 256-row count. No new-row Gate quote obligation is invented or waived for a changed row.
- Lines 44-48: frozen `LOG.md:1836` starts the explicitly post-hoc round-51 record, and QUALITY 95 exists at `corpus/QUALITY.md:186`. The lesson labels the remaining round-52 green checks as obligations rather than achieved round-51 fixes.

### (b) Spot-check summary — holds

Lesson lines 25-31 match `corpus/lessons/round-51-verifier-spotcheck.md:9-11` (ruling `rejected-honest-stop`, admitted=false, no harm), lines 53-58 (C1/depth unprovable-but-better, C2/operability unprovable, C3/adjacency unprovable-but-better), and lines 68-71 (Gate sample n/a/unprovable; S237 agree; S240 agree; 256-row census agree/exit0). No verdict is promoted.

Important distinction retained correctly: spot-check line 29 calls the broken 1157-byte output “committed”; the actual round-51 committed blob is empty. The lesson does not repeat that mistake: it separates committed empty bytes from later working-copy bytes now preserved under inherited/.

### (c) Every Mistakes row — dispositions

1. **Misroot: defect in locator only**, exact fix above. Incident otherwise supported by original report lines 54-56 and spot-check lines 31-32. Captured-by `none` is an allowed value and specifically says no rule caught the edit at write time; it does not claim there was no later sweep. Proposed QUALITY 95 is present at frozen QUALITY line 186.
2. **Shared-scratch deletion: holds.** Both inherited pointers resolve, with failed values above, and original report Work performed records the L1's action. The cited rule exists in the fleet round-51 prompt, §7.2 at `.ufo/prompts/tsukuroi-round-51.md:673-676`: delete on exit, receipts copied first. This is a prompt rule, not a numbered QUALITY criterion.
3. **Early filing/seat band: holds.** Original report lines 10-17 records no WAVE-DONE and 54 dispatched seats; spot-check lines 25-26 agrees. Existing prompt rules are `File only after WAVE-DONE` at lines 191-193 and round total 64–128 at lines 217-219. QUALITY need not contain duplicates of those prompt rules. Round-52 filing remains a future obligation, not verified by this review.
4. **Missed frontier: holds.** Spot-check lines 26-27 and original report §Sources & frontier establish missing Gate/lesson/LOG. Existing prompt §2b begins at line 42 and requires the mistake lesson; QUALITY criterion 11 at frozen QUALITY line 15 independently requires the matching LOG entry. Frozen lesson and LOG are marked post-hoc, not passed off as original round-51 work.

Exact fixes for rows 2-4: none required.

### (d) Gate rejection flip — holds (checkable, not exercised)

Lesson lines 22-24 names a revision, undisturbed scratch, and four exact conjuncts. Canonical `tools/score-counter-cheats-r51.py:26` states the same predicate; its lines 165-184 derive real_pass from PASS/rc0, count cheat rejection only for FAIL/rc1, and compute the final result. A valid run with all four stated fields is distinguishable from the inherited broken run, which fails real_pass and cheats_rejected. Validity also requires inspecting detail: r50_cheats_rejected=0 alone is not a successful r50 sensitivity run, as the inherited all-ERROR r50 rows demonstrate. The lesson already says VALID/undisturbed rather than crediting that zero alone.

Exact fix: none required. I did not run the scorer or admit a receipt.

## Residual risk and verification gaps

- Historical scratch deletion and byte-exact fleet rollback are supported by the L1's recorded disclosure; the non-author spot-check explicitly did not re-diff the fleet SCORECARD. I did not turn those disclosures into an independent process trace or repeat a present-day sweep as historical proof.
- No live upstream fetches, census/selftests, scorer, runtime, or current-wave completion checks were run; this assignment reviews the post-hoc lesson, not round-52 measurements. No saturation or resume-continuity claim is made here.
- `read xd://lsp` returned “No such tool”; no LSP server/status/references/definition/diagnostics device was available. Used immutable git show/diff and literal git grep instead; grep is locator evidence, not semantic caller proof.
- No tracked files edited; no scratch tree created; no tools installed or updated.

Self-evaluation: accuracy 4/5 (historical mutation causation remains disclosure-backed); completeness 4/5 (future green obligations intentionally unexercised); clarity 4/5 (revision convention necessary); actionability 5/5 (exact locator replacement supplied); conciseness 4/5 (per-item evidence retained for audit). Overall 4.2/5. Highest-impact improvement is the one-line locator fix; historical process proof would require evidence not asserted here. User agreement check: this supports the honest-stop lesson while preserving its concrete pointer defect.
