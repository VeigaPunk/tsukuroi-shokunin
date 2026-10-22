# CritRoundHarm — round 28 residual harm sweep, 9a0654ba versus 3b9e0430

Verdict: partly holds. Every selftest passes at both revisions, registry coverage is clean at both, and the append-only files only gained lines. One count got worse: `check-self-assessment.py --revision` finds 3 mismatches at 9a0654ba against 1 at 3b9e0430 (new K08 and K09). The round-28 declaration does not disclose this.

Exports: `git archive` of each revision into /fast/scratch/hyaku/tsuku28/CritRoundHarm/{base,tip}. Raw outputs are under /fast/scratch/hyaku/tsuku28/CritRoundHarm/out/.

## Findings

1. [obs] The self-assessment mismatch count rose from 1 to 3. Command: `python3 tools/check-self-assessment.py --revision <REV> --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, run from both exports. The base-export tool and the tip-export tool give the same result for each revision.
   - At 3b9e0430: exit 1, `checked` 27, `mismatches` 1. The only mismatch is K10 (depth row says 30 lesson files; there are 31).
   - At 9a0654ba: exit 1, `checked` 27, `mismatches` 3.
     - K08: the depth row says 2486 `SKILL.md` lines; `SKILL.md` holds 2531 newline characters.
     - K09: the depth row says 381 table lines; `SKILL.md` holds 416 pipe-prefixed lines.
     - K10: the depth row says 30 lesson files; there are 32.
   - Every check points to `stated_line` 1027, the depth row of SCORECARD.md at 9a0654ba, which this round did not touch.
   - Evidence: /fast/scratch/hyaku/tsuku28/CritRoundHarm/out/base-selfass-3b9e0430.out and /fast/scratch/hyaku/tsuku28/CritRoundHarm/out/R-tip-selfass-9a0654ba.out.
   - [obs] Cause: the round appended 45 lines to `SKILL.md`, a superseding registry table at `SKILL.md:2488` with 35 pipe-prefixed lines. It also added `corpus/lessons/round-28.md`. `git diff --numstat` shows `45 0 SKILL.md` and `39 0 corpus/lessons/round-28.md`.
   - Impacted axes: depth (the depth row's stated evidence is now false on three counts instead of one) and calibration (a self-assessment counter got worse without disclosure).
   - [obs] The declaration's separability line, SCORECARD.md:1063 at 9a0654ba, says "C1 changes only `tools/check-adjacency-overlap.py` and adds its battery; C2 changes only `tools/check-kernel-taint.py` and adds its battery". The same tip also changes `SKILL.md`, which a depth check reads.
   - [obs] The round-28 lesson lists the self-assessment tool's own defects as "still owed; not touched" (`corpus/lessons/round-28.md:23`). It does not mention the 1-to-3 rise.
   - Smallest safe correction: append to SCORECARD.md (append-only) a dated depth-row restatement, or a disclosure line, giving the tip counts (2531 `wc -l`, 416 table lines, 32 lesson files). Then rerun self-assessment and record the result in the round report. [unk] I did not check whether `check-self-assessment.py` picks up an appended later depth row or always reads the first depth row it meets in the ordinal table (`tools/check-self-assessment.py:530`). The appended row has to be one the checker selects, or this stays a disclosure only.

2. [obs] Registry coverage is unchanged in status and grows by the two new tools.
   - Command: `python3 tools/check-registry-coverage.py --revision <REV>`.
   - At 3b9e0430: exit 0, PASS, `registered` 31 of `tools_total` 31, 0 findings.
   - At 9a0654ba: exit 0, PASS, `registered` 33 of `tools_total` 33, 0 findings.
   - The base-tools and tip-tools results are identical.
   - Evidence: /fast/scratch/hyaku/tsuku28/CritRoundHarm/out/SB-{base,tip}-regcov-{3b9e0430,9a0654ba}.out.
   - [obs] Method note: from a bare export, the tool exits 2 with `E-GIT-FAILED` "not a git repository". It has no `--repo` flag: `ROOT = Path(__file__).resolve().parents[1]` at `tools/check-registry-coverage.py:20`. `_revision.clean_env()` strips every `GIT_*` variable (`tools/_revision.py:62-63`), so `GIT_DIR` cannot redirect it. I ran it inside private sandboxes: a copy of each export, plus `git init` with no remote, `objects/info/alternates` pointing at the lane object store (read-only), and sandbox-local `refs/heads/master` set to 9a0654ba, which is the lane master (`git rev-parse master`).

3. [obs] Selftest exit codes and counts at base (3b9e0430) and tip (9a0654ba). No case fails on either side, and no exit code changes.

   | Selftest | Base | Tip |
   |---|---|---|
   | `check-adjacency-overlap.py --selftest` | exit 0, 17 cases, 0 failed | exit 0, 43 cases, 0 failed |
   | `check-kernel-taint.py --selftest` | exit 0, 46 cases, 0 failed, PASS | exit 0, 52 cases, 0 failed, PASS |
   | `check-self-assessment.py --selftest` | exit 0, PASS, 15 cases | exit 0, PASS, 15 cases |
   | `check-storage-health.py --selftest` | exit 0, 44 cases, 0 failed, PASS | exit 0, 44 cases, 0 failed, PASS |
   | `check-registry-coverage.py --selftest` | exit 0, 23 of 23 passed | exit 0, 23 of 23 passed |
   | `bash tools/tsukuroi-census.sh --selftest` | exit 0, 97 of 97 passed | exit 0, 97 of 97 passed |

   - Adjacency-overlap grows by 26 cases, matching the 43 cases named in the commit message. Kernel-taint grows by 6 cases, matching the 52 named in the commit message.
   - [obs] From a bare export, `check-self-assessment.py --selftest` exits 2 with "not a git repository", because `main()` requires `<repo>/.git` before it dispatches the selftest (`tools/check-self-assessment.py:1048-1051`). With `--repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` it exits 0 at both revisions. This is a property of the tool at both revisions, not a change made by the round.

4. [obs] The four named append-only files have no deletions. Command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --numstat 3b9e0430 9a0654ba…`, exit 0.
   - SCORECARD.md: `17 0`. Base 1050 lines, tip 1067 lines, and the first 1050 lines are byte-identical (`cmp` against `head -n 1050`).
   - corpus/SOURCES.md: `2 0`. The S146 and S147 rows are inserted after line 151, at the end of the source table and before `## Paths`. Nothing is removed, but the insertion is not at the end of the file, which is the normal shape for this table.
   - LOG.md and SHONEN.md do not appear in the numstat output, so they are unchanged.

5. [obs] One deletion outside the named set: corpus/QUALITY.md `2 1`. Principle 69 was rewritten in place, with its label "(C2, round 27)" replaced by "(R27-SIBLING-POINTER-DRIFT)". The routed item "QUALITY 69 names its lesson id" (SCORECARD.md:1067) requires that change.
   - [inf] It sits against `corpus/QUALITY.md:7` "4. Errata are append-only blocks." It is a tradeoff rather than a defect if the lane treats id labels as non-errata metadata.
   - [obs] `SKILL.md:176` scopes its own errata-append-only rule to "corrections to this file", meaning SKILL.md only.
   - Smallest safe correction, if the judge treats the label change as an erratum: record in the round report that it was an in-place edit, or append the id as a dated note instead.

6. [obs] The other numstat lines are additions only: wave and measure files, the two batteries, `corpus/lessons/round-28.md`, and SKILL.md `45 0`. The only other deletions are in the two counters: `tools/check-adjacency-overlap.py` `143 29` and `tools/check-kernel-taint.py` `47 6`. Those are the claimed code changes, and their selftests pass (finding 3).

Scope: read=round-28 declaration and ordinal depth row in SCORECARD.md at 9a0654ba (lines 1027, 1051-1067), corpus/QUALITY.md and SKILL.md diffs, SKILL.md:174-177, corpus/QUALITY.md:1-9, corpus/SOURCES.md:146-158, tools/check-registry-coverage.py, tools/_revision.py and tools/check-self-assessment.py argument and repo handling; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/residual/CritRoundHarm.md, /fast/scratch/hyaku/tsuku28/CritRoundHarm/{base,tip,sb-base,sb-tip,out}; executed=git archive of both revisions, git diff --numstat/-U0 and git show/grep/rev-parse (read-only, against the lane), git init plus update-ref inside the private sandboxes only, check-registry-coverage.py --revision at both revisions from both tool trees, check-self-assessment.py --revision --repo at both from both, the five python --selftest runs and bash tools/tsukuroi-census.sh --selftest at both
Model: not exposed
Installs: none
