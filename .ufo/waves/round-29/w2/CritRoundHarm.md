# CritRoundHarm — round 29 wave 2, owned-axis harm scan (10d5288f vs base 16e9ab2a)

Verdict: partly holds — none of the six axes is harmed, but the self-assessment gate has three stale counts, not only the expected one. The only red gate at 10d5288f is `check-self-assessment.py` (status FAIL, 3 mismatches: K08, K09, K10). At the base 16e9ab2a only K10 was red. K08 and K09 are newly red because round 29 grew SKILL.md. All three come from the same cause: the round-28 axes table has not been restated for round 29. So this counts as expected staleness, but the round-29 axes table must fix all three numbers, not only the lesson count.

Sandbox: clones at /fast/scratch/hyaku/tsukuroi-r29/CritRoundHarm/repo (HEAD 10d5288fc1051364e711203855e7c53710dfcc21) and /fast/scratch/hyaku/tsukuroi-r29/CritRoundHarm/base (HEAD 16e9ab2abfac430b4e960e8ce64b90420f602342). Every git call was prefixed `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`. Evidence copies are in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritRoundHarm/.

## Findings

1. [obs] Self-assessment is the only red gate. `python3 tools/check-self-assessment.py --revision 10d5288f… --repo <clone>` exited 1 with `"checked": 27, "mismatches": 3, "status": "FAIL"`, and the axes heading it checked is `## Axes — current self-assessment (round 28)`. The three mismatches, all against the depth row at SCORECARD.md:1090:
   - K08: the row states 2531 SKILL.md lines; the file has 2597.
   - K09: the row states 416 table lines; the file has 459.
   - K10: the row states 32 lesson files; corpus/lessons has 34.

   Evidence: .ufo/waves/round-29/w2/CritRoundHarm/gates/check-self-assessment.out. At the base the same gate exited 1 with only `K10 32 vs 33` (gates-base/check-self-assessment.out). So K10 was already stale before round 29 (round 28 did not restate it), and round 29 adds one more lesson file, corpus/lessons/round-29.md. K08 and K09 are new reds caused by the +66 lines in SKILL.md (`git diff --stat 16e9ab2a 10d5288f`: `SKILL.md | 66 +`), which include the section "Kernel OOM victim selection — round 29".
   - [inf] This is calibration bookkeeping, not real harm to any axis: K01–K06 (the six ordinal scores) all match. The fix is the pending round-29 axes table.
   - Smallest safe correction: the round-29 axes depth row states `SKILL.md` 2597 lines, 459 table lines and 34 lesson files, recounted at the final tip if later commits touch SKILL.md or corpus/lessons. An axes table that updates only the lesson count would leave K08 and K09 red.

2. [obs] Every lane tool that has a selftest passes at head, and no selftest lost cases. Exit codes are in .ufo/waves/round-29/w2/CritRoundHarm/selftest-head/rc.txt and selftest-base/rc.txt; tail lines are in casecmp.txt.
   - 31 tools exit 0 at head, including tools/tsukuroi-census.sh, which reports `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)` (gates/census-selftest.out).
   - Case counts only grew between base and head: check-adjacency-overlap 43→55, check-kernel-taint 55→56, check-self-assessment 15→19. No tool's count went down.
   - Five tools exit 2 under `--selftest` because they have no selftest mode; argparse rejects the call:
     - mutants-adjacency-overlap.py and mutants-kernel-taint.py ("required: --base"), same as at the base.
     - Three new round-29 tools: check-owed-statements-r29.py ("required: --revision"), mutants-owed-statements-r29.py ("required: --base") and probe-git-env-leak.py ("required: --revision").
   - [inf] The three new tools are not red gates, because the mutants tools set the precedent and check-owed-statements-r29 has its own committed battery. Still, the new counter and the new probe have no built-in selftest. That is an operability gap, not a regression.

3. [obs] The other named revision gates pass at head and at the base. Each one exited 0 with status PASS or no findings (gates/*.out and gates-base/*.out):
   - check-registry-coverage: `"registered":36,"tools_total":36,"missing":0`
   - check-memory-pressure: `findings: []`, 6 rows
   - check-storage-health: `findings: []`, 6/6 rows
   - check-kernel-taint: `findings: []`, 6/6 rows
   - check-adjacency-overlap: `anchored_rows 6/6, sibling-verified, PASS`
   - check-freshness-r17: `48/48 resolved, PASS`

   [obs] As an extra depth check, the C1 counter `check-owed-statements-r29.py --revision 10d5288f… --lane <clone>` exited 0 and reported `"items": 12, "marked": 12`, counter sha256 c3f9cfe7… (gates/owed.out).

4. [obs] `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exited 0 with `tsukuroi ok`. Lane HEAD is 10d5288f, and its corpus/SOURCES.md is byte-identical to the clone's (`cmp` was silent).
   - Running validate directly against the base and head clones, the only new line is `W04 S149 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes` (gates/sources-validate.out against gates-base/sources-validate.out).
   - S149 (SOURCES.md:155) has the same URL and the same raw sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e as S119 (SOURCES.md:125). S119's scope is where the kernel counts an OOM kill; S149's is how it selects the victim.
   - [inf] This is a tradeoff, not a defect: W04 is a warning, and the lane has 25 earlier W04 rows that use the same one-row-per-scope pattern. It does create a second registry id for one byte-identical artifact. The judge may want S149's row to point to S119 explicitly.

5. [obs] Running the selftests did not dirty the sandbox. After all runs, `git status --porcelain` is empty and HEAD is unchanged in both clones. [obs] The lane working tree was only read (rev-parse, and cmp of SOURCES.md).

## Axes

- Depth: not harmed. C1 is 12 of 12 marked, and the K08/K09/K10 counts are stale only until the axes table is restated (finding 1).
- Coverage: not harmed. Registry coverage is 36 of 36, and sources validate is ok.
- Operability: not harmed. Every selftest passes and case counts grew. The gap is that the new counter and probe have no selftest (finding 2).
- Freshness: not harmed. 48 of 48 records resolve.
- Calibration: red gate, with three stale self-assessment counts instead of the expected one (finding 1). This is staleness, not a wrong score.
- Adjacency: not harmed. 6 of 6 rows are anchored and sibling-verified, and the selftest grew from 43 to 55 cases.

Scope: read=lane tools, SCORECARD.md depth row and headings, SOURCES.md rows S119/S149, sources-census.sh write paths, both sandbox clones; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritRoundHarm.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritRoundHarm/ (gates, gates-base, selftest-head, selftest-base, casecmp.txt), /fast/scratch/hyaku/tsukuroi-r29/CritRoundHarm/; executed=sandbox clone and checkout of both revisions, every tools/* --selftest at head and base, the seven named --revision gates at head and base, check-owed-statements-r29.py --revision, bash tools/tsukuroi-census.sh --selftest, sources-census.sh validate (fleet root, and per clone), read-only git rev-parse/status/diff --stat
Model: not exposed
Installs: none
