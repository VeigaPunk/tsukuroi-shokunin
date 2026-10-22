# ResCritVerdicts — round 29 residual, independent verdicts at 06e00dafbbaa4695bc74decf68c816da8151b00a

Verdict: partly holds. C1 (depth) is verified as counted and C2 (operability) is verified. On the trends, expansion improved, quality improved and discernment is unchanged. None of the six ordinal axes is measurably harmed. There is one small calibration defect: the post-wave-2 `SKILL.md` edit in 06e00daf, which no seat reviewed, states an inferred bound as fact.

Sandbox: clone at /fast/scratch/hyaku/tsukuroi-r29/ResCritVerdicts/repo, checked out at 06e00dafbbaa4695bc74decf68c816da8151b00a. Every git call had GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset. The one sandbox commit (7a6cbd2f, the mutation in finding 4) was made only inside that clone, and HEAD was returned to 06e00daf afterwards.

## Per-claim verdicts

- C1 (depth): **verified as counted**. The movable quantity is genuine for O01 to O04 only (finding 2).
- C2 (operability): **verified**. 3 of 8 tools leaked before and 0 of 8 leak after, and each fix is load-bearing. The wording "the eight tools no longer follow" covers 3 tools that actually changed (finding 4).

## Per-trend verdicts

- Expansion: **improved** (finding 6).
- Quality: **improved**, with two residual defects (findings 5 and 7).
- Discernment: **unchanged**. The round shows good judgement and repeats an old process failure, and these offset each other (finding 8).

## Findings

1. [obs] C1 reads 12 of 12 at the tip under all three counter versions, including the declared one. In the sandbox, `python3 tools/check-owed-statements-r29.py --revision 06e00daf…` gave rc 0 with the last line `"items": 12, "marked": 12, "unmarked": []`, counter_sha256 `1c37d492…` (version 3). The declared counter came from `git show 81a061a6:tools/check-owed-statements-r29.py` (sha256 `5b6cf227580ff26e…`, the same as the declared prefix). Version 2 came from `git show 409ceed4:…` (sha256 `c3f9cfe73e980db9…`). Each was run from inside `tools/` at the tip, and each gave rc 0 with `"marked": 12`. The before value is 0 of 12 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/measure/c1-before-81a061a67466c5e1be812814a895a4b5ed89b4ff.jsonl, and measure/final/c1-v3-before-81a061a6….jsonl).
   - [inf] Because the declared counter alone gives the after value, rewriting the counter twice did not move the goalposts in the claim's favour. The two rewrites are re-specifications that refuse hollow shapes. They do not loosen the target. CritClaimFraming2 also found the frozen `ITEMS` tuple byte-identical between v1 and v2 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritClaimFraming2.md, finding 2).

2. [obs] C1's depth substance is partial, and the round discloses this. The measured-outcome row (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md, the "Round 29 measured outcome" C1 row) says only O01 to O04 add new sourced detail (S148, S149). O05 to O12 carry corrections already argued in companion files, or close an `[unk]` from an existing capture. The counter output at the tip shows O11 with `"sources": []` and O12 citing only the pre-round S134. CritClaimFraming2 counts four of the twelve markers citing no `S###` source.
   - [inf] The claim is verified against its declared counting command. Its contribution to the depth axis is about 4 of 12 items, not 12, and the ordinal correctly stays at 8.

3. [obs] The counter-v3 batteries reproduce at the tip.
   - `python3 tools/mutants-owed-statements-r29.py --base 81a061a6… --counter-rev 06e00daf… --lane <clone>`: rc 0, `should_fail_accepted 0` of 29, `should_pass_refused 0` of 7, `control_marked 12`, no crashes.
   - `python3 tools/mutants-owed-statements-r29-landed.py --base 06e00daf… --counter-rev 06e00daf…`: rc 0, `should_fail_accepted 0` of 19, 7 semantic shapes still counted (disclosed).
   - The committed receipts agree: measure/final/c1-battery-v3.jsonl and c1-landed-battery-v3.jsonl.
   - [inf] Both 0-of-N results are in-sample. Version 3 was written after the 19 landed shapes were seen (CritOwedV2Shapes → v3), so the landed battery shows the fix covers its own attack set, not held-out strictness. Version 3 also keeps v2's six format relaxations: the 7 should-pass shapes in the main battery, including the G-family, are still accepted. The lesson's corrected text says this honestly (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-29.md:47).
   - Impacted axis: calibration of the counter's strength, not the C1 verdict, which rests on finding 1.

4. [obs] C2 is verified and load-bearing.
   - At the tip, `python3 tools/probe-git-env-leak.py --revision 06e00daf…` gave rc 0 and `"targets": 8, "leaking": 0, "harness_errors": []`, probe_sha256 `46a55ce7…`. That is the declared probe, the same hash as in the before receipt c2-before-81a061a6….jsonl, which reads `"leaking": 3` (the adjacency selftest helper and both batteries).
   - Mutation: I committed the 81a061a6 bytes of `tools/mutants-kernel-taint.py` onto the tip in the sandbox (7a6cbd2f) and ran `--only tools/mutants-kernel-taint.py`. Result: rc 1, `"leaking": 1`, `"control_rc": 0, "canary_rc": 1, "canary_changed": false`.
   - [obs] The leak is detected by exit-code divergence only; the canary is never written, as disclosed.
   - [inf] Only 3 of the 8 targets could move. The wording "the eight tools no longer follow" states a 3-tool fix as an 8-tool property. The outcome row already says "three leaked ... five never did", so this is a framing note, not a defect.

5. [obs] The post-wave-2 `SKILL.md` edit in 06e00daf (`git diff 75257ea 06e00da -- SKILL.md`: 2 lines) was made after every wave-2 seat had reported, and no seat reviewed it.
   - It applies RevSkillOomSection's two fixes: the floor in the formula, and anchoring 16,909,739 to event A.
   - It also turns the reviewer's unknown into a stated bound. The landed cell reads "event B's swap total is unrecorded, so between 15,861,169 and 16,909,739" (SKILL.md:2543 at the tip).
   - The reviewer's own text marks that range `[unk]` and proposes the honest cell "16,909,739 at event A; event B unrecorded; 15,861,169 at capture" (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RevSkillOomSection.md, finding 1).
   - The figure 15,861,169 appears nowhere in `corpus/`. Its only origin is a wave-1 seat's "today's totalpages" live read (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeSkillOomRow.md:81).
   - [inf] The bound holds only if the removal of zram0 was the single swap change between event A (2026-10-13 23:44) and the r8 capture (2026-10-14 14:38). Nothing records that.
   - [inf] The bullet just above (SKILL.md:2538) still says "Capture-epoch host sum is 16,909,739 pages". The r8 capture epoch read SwapTotal 31,722,876 kB (about 15.86 M pages, per RevSkillOomSection finding 1), so that bullet is now inconsistent with the corrected table row.
   - Impacted axes: calibration and depth precision, both minor. No downstream number changes: the F7 margins keep their GiB-scale verdict at either bound.
   - Smallest safe correction: append a correction, or rewrite this round-29 addition in place, using the reviewer's cell text, and change "Capture-epoch" to "event-A".

6. [obs] Expansion grew.
   - S148, S149 and S150 were admitted as `mined` and S151 was rejected (lesson Gate table, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-29.md:10-15).
   - `SKILL.md` gained the section "Kernel OOM victim selection — round 29". Between 16e9ab2a and 06e00da, `git diff --stat … -- corpus SKILL.md` shows `SKILL.md | 67 +`, with 217 insertions and 2 deletions across 9 files.
   - New tools: the probe, the owed counter and two owed batteries. Registry coverage is 37 of 37 PASS (measure/final-06e00daf…/check-registry-coverage.txt).
   - [obs] A tradeoff, not a harm: sources-census gives W04 because S149 duplicates S119's URL and bytes across scopes (measure/final-06e00daf…/census.txt, last two lines).

7. [obs] Quality improved, and every named gate passes at the tip.
   - Self-assessment at the tip: `"checked": 27, "mismatches": 0, "status": "PASS"` (measure/final-06e00daf…/check-self-assessment.txt; my sandbox run gave rc 0). At 10d5288f it was FAIL with 3 mismatches, and at the base 16e9ab2a FAIL with 1 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritRoundHarm.md, finding 1).
   - Adjacency, kernel-taint, memory, storage and freshness all pass (the final-06e00daf receipts).
   - Append-only sweep `git diff -U0 16e9ab2a 06e00da -- SCORECARD.md LOG.md corpus/ SKILL.md | grep -E '^-[^-]'`: only the S133 and S134 rows, which matches the QUALITY 60 disclosure.
   - Residual defects:
     - The new counter and the new probe have no `--selftest` (CritRoundHarm, finding 2).
     - The finding-5 edit was not reviewed.

8. [inf] Discernment is unchanged on balance.
   - For:
     - S151 rejected with a stated operand-level reason (lesson :15).
     - O03 marked `qualified` rather than corrected (lesson :20).
     - The padding repair reverted on evidence of over-strictness (finding 9).
     - The false "Version 2 can only refuse more" statement corrected in place (lesson :47).
   - Against:
     - The C1 counter was declared without the should-fail battery that QUALITY 73 requires. It was "the third permissive counter in three rounds" (lesson :43, R29-UNBATTERIED-COUNTER).
     - The lesson's false monotonicity claim had to be caught by a wave-2 seat (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/RerunC1Counters.md, verdict).
     - The 06e00daf edit again promoted a reviewer's `[unk]` to a stated bound (finding 5).
   - The error-catching loop worked, but the same error classes recurred, so I see no net movement.

9. [obs] The padding revert did no measurable harm, and none of the attempt survives in the tools.
   - `git diff 409ceed4 06e00da -- tools/check-adjacency-overlap.py | wc -l` gives 0. The tip sha256 is `dc8eb3346dd6a2bd…`, matching the lesson (:51).
   - `python3 tools/check-adjacency-overlap.py --selftest` at the tip gives `"cases": 43, "failed": 0`, the base count.
   - At the tip, `SKILL.md`, `corpus/QUALITY.md` and the tool have no B8 to B15 adjacency rule text. The only "B15" hit is an unrelated memory-arm battery case at SKILL.md:1163, so the revert left no stale documentation.
   - [inf] Adjacency ends where it started: routed defect 4 is still owed, and the round-28 padding shapes are still accepted. The revert was the correct call. CritPaddingOverStrict showed the repair refuses 15 of 19 correct registers and still accepts 24 of 24 new padding shapes (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritPaddingOverStrict.md, verdict). An over-strict gate would have harmed operability.

## Axes named as harmed

None of the six ordinal axes is harmed by measurement.

- Counter rewritten twice: not a harm to C1, because the declared counter alone gives 12 of 12 (finding 1). The residual risk is overstated counter strength, since v3's batteries are in-sample (finding 3).
- Reverted padding repair: neutral (finding 9).
- SKILL section edit: a minor calibration and depth-precision harm, because an inferred range is presented as fact and the adjacent bullet is now inconsistent (finding 5). The fix is two cell edits.

Scope: read=SCORECARD.md round-29 declaration, outcome and axes sections; corpus/lessons/round-29.md; w2 CritRoundHarm, CritClaimFraming2, CritPaddingOverStrict, RerunC1Counters, RevSkillOomSection; w1 ScribeSkillOomRow (grep); measure/ receipts (before, after, final, final-06e00daf); SKILL.md:2525-2550 and corpus/knowledge/oom-event-plane.md (grep) at the tip; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/residual/ResCritVerdicts.md, /fast/scratch/hyaku/tsukuroi-r29/ResCritVerdicts/ (clone, v1.py, v2.py, probe.jsonl, probe-mut.jsonl, bat-v3.jsonl, bat-landed-v3.jsonl); executed=sandbox git clone/checkout/switch/commit (in the scratch clone only, with GIT_* unset), read-only git log/show/diff/status/rev-parse, check-owed-statements-r29.py v1/v2/v3 --revision 06e00daf, probe-git-env-leak.py --revision 06e00daf and --only on mutant 7a6cbd2f, check-self-assessment.py --revision 06e00daf, check-adjacency-overlap.py --selftest, mutants-owed-statements-r29.py and mutants-owed-statements-r29-landed.py against counter 06e00daf, sha256sum, grep
Model: not exposed
Installs: none
