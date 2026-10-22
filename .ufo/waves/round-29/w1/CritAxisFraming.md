Verdict: partly holds. C1 is not a clean depth claim: its counter rewards marker shape, accepts content-free markers at 12 of 12, and 7 of its 12 items only copy corrections that already exist into companion files. C2 is framed as operability, but its universal clause ("every tool with a sandbox git write") is false: a ninth tool that writes to git leaks and is outside the frozen set.

Revision under attack: `81a061a67466c5e1be812814a895a4b5ed89b4ff` (declaration at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1097-1110`). All runs were in the sandbox clone `/fast/scratch/hyaku/tsukuroi-r29/CritAxisFraming/repo`, with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. Evidence copies are in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/CritAxisFraming/`.

## Verdict per claim

- C1 (depth): partly holds. O01 to O04 are real depth work: a kernel mechanism, a required `S###` source, and new cited detail. O05 to O12 are calibration and freshness work counted as depth. The counter cannot tell a source-backed correction from padding. The after-value is concrete and can be re-derived; the lowest-axis duty is met only through O01 to O04.
- C2 (operability): partly holds. Behaviour under an inherited environment is a runnable-artifact property, so the axis fits. Before = 3 reproduces exactly. However, the "every tool with a git write" clause is false (finding 6), and the routed requirement "add a selftest that can fail" was dropped without saying so (finding 8). Widening the set from the two batteries to eight tools found one real extra leaker, but it also adds five tools that never leaked to the denominator, and it misses a leaker outside the set.

## Findings

1. [obs] Both before-values reproduce at `81a061a`.
   - C1: `python3 tools/check-owed-statements-r29.py --revision 81a061a… --lane <clone>` gives exit 1 and `"marked": 0`, with counter_sha256 `5b6cf227…`.
   - C2: `python3 tools/probe-git-env-leak.py --revision 81a061a… --lane <clone> --scratch <seat>/probe` gives exit 1, `"targets": 8, "leaking": 3`, and the same three tools and probe_sha256 `46a55ce7…` as the L1 receipt `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/measure/c2-before-81a061a67466c5e1be812814a895a4b5ed89b4ff.jsonl:9`. My copy is `.ufo/waves/round-29/w1/CritAxisFraming/declared-probe-81a061a.jsonl` (sha256 `f015b4c2…`).
   - Each after-value is one concrete value from one command over committed bytes. C1 reads only `git show REV:path`. C2 runs tools from `git archive REV`. Caveat [inf]: C2 also depends on host git and global git config, because the probe sets only `GIT_CONFIG_NOSYSTEM`.

2. [obs] Counterexample to C1 measuring depth: an all-padding mutant scores 12 of 12 with exit 0.
   - Built by `pad_mutant.py` (sha256 `749129ea…`) on a sandbox branch.
   - Every `now` is the filler "this item is hereby addressed by the marker shown here as required item Oxx".
   - O01 to O04 carry verdict `rebutted`, which asserts the "+200 band scanned first" reading that mori says is false. Their basis is a fabricated `corpus/SOURCES.md` row `S999` with status `mined`, no URL, no snapshot and no quote.
   - O06 and O07 cite `S115`, which is already behind the statement being corrected.
   - O05 and O08 to O12 cite `SKILL.md:1`.
   - Result at sandbox commit `9c803092`: `{"items": 12, "marked": 12, "unmarked": []}`, exit 0 (`c1-pad-mutant2.jsonl`, sha256 `78700fc1…`).
   - Rules at fault (`tools/check-owed-statements-r29.py:24-31,108-127`):
     - M5 checks only word count and uniqueness.
     - M6 accepts any `path:LINE` that exists in any file.
     - M6 and M7 check a source row only for status `mined` plus a substring of the item file's basename in the used-by cell. They do not check the opening date, a snapshot, a quote, or that the row is one of S148 to S150.
   - The declaration's phrase "need an `S###` source opened this round" (`SCORECARD.md:1103`) is a universal clause the counter does not enumerate.
   - Impacted axes: depth (the measured quantity is marker shape, not verifiable detail) and calibration (a 12 can be reached by overreach).

3. [obs] Seven of the twelve items only copy existing corrections into companion files. They add no new technical detail.
   - Routed defect 4 says "Mark each in its companion (QUALITY 67)" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-27-verifier-spotcheck.md:102`).
   - QUALITY 67 is titled "A correction reaches every companion of the entry it corrects" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:135`).
   - The MP4 qualifier is already in `memory-pressure-r25.md` with sources (`corpus/lessons/round-27.md:80`: "without the `OOMRules=` and `systemd-oomd.socket` qualifiers that `memory-pressure-r25.md` lines 387-390 carry").
   - The four storage-health statements are already corrected in the Markdown file: md:128, md:135, md:133 and md:129 (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/RevRoutedDefects.md:20`).
   - O08 resolves an `[unk]` from an existing capture (`corpus/lessons/round-27.md:82`). That is re-verification against a live surface, which is AXES freshness.
   - AXES.md calibration reads "gaps named honestly, confidence graded, overreach caught". The lane's own calibration row cites "errata stay visible instead of being rewritten" as calibration evidence (`SCORECARD.md:1094`). C1's M1 rule (anchor kept verbatim, marker appended) is that errata pattern.
   - [inf] By the lane's own row, O05 to O12 are calibration and freshness work; only O01 to O04 are depth.

4. [inf] The lowest-axis duty is met only if C1 is depth. Depth and adjacency are tied at 8; calibration is at 9.
   - If the operator reads C1 by its majority of items (8 of 12 not depth), then no claim works an axis at 8, and the duty fails as it was contested in round 28.
   - The declaration's sentence "each claim is placed on the axis its counting command measures" (`SCORECARD.md:1099`) does not settle this. C1's counting command counts marker shape (finding 2), not depth.

5. [obs] Duplicate authority: the declaration settles a question that was reserved for the operator.
   - Round-28 routed item 7 says "This is for the operator; it does not change the verdict" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-28-verifier-spotcheck.md:95`). The round-28 outcome repeats "the operator rules" (`SCORECARD.md:1080`).
   - Round 29 states "7 is answered by the framing above" (`SCORECARD.md:1110`). That is an author rule standing in for the operator ruling.
   - Smallest correction: state the framing as the author's reading, with "operator ruling pending".

6. [obs] C2's universal clause is false: a ninth git-writing tool leaks and is outside the frozen set.
   - Why the set is incomplete:
     - The frozen grep `'(init|commit|add)'|git (init|commit|add)` (`tools/probe-git-env-leak.py:11-13`) matches only single-quoted Python strings.
     - Re-running it at base `16e9ab2a` reproduces exactly the eight targets.
     - A wider read of `git show 16e9ab2a:tools/<f>` finds 14 more tools that run `init`, `add`, `commit`, `checkout`, `update-ref` or `config` in sandboxes, written with double quotes or helper wrappers. Examples are `tools/_revision.py:220-227` and `tools/check-self-assessment.py:975`.
   - Extended probe: the same harness over the 14 tools (`probe-ext.py`, sha256 `daceb8ca…`; output `ext-probe-81a061a.jsonl`, sha256 `7028f408…`) gives 12 clean and 2 harness errors. Both errors are control failures, because those tools need a git repository and the probe's `git archive` export is not one.
   - Direct canary from the clone checkout (`canary1.sh` with `tools/check-self-assessment.py --selftest`): `control_rc=0`, `canary_rc=1`. That is a leak by the probe's own rule at `tools/probe-git-env-leak.py:156`.
   - Cause: `tools/check-self-assessment.py:975` runs `subprocess.run(["git", "init", "-q", repo], check=True)` without its `git_env()`. With an inherited `GIT_DIR`, the init goes to the canary, and the next call fails with `fatal: not a git repository` (`canary-check-self-assessment.out:1`) and a `CalledProcessError` on `git -C … add -A` (`canary-check-self-assessment.out:17`).
   - `tools/check-appended-notices.py --selftest` is clean under the canary (control 0, canary 0).
   - Consequence: C2 can land "0 of 8" while a git-writing lane tool still follows an inherited `GIT_DIR`. This is the round-28 incident class, which the claim says it closes (`SCORECARD.md:1104`, "widened ... to every tool with a sandbox git write").
   - Smallest correction, either of:
     - Narrow the wording to "the eight tools matched by the frozen grep".
     - Add `tools/check-self-assessment.py` to the set and run targets from a non-bare clone checkout, so tools that need a repository can be measured.

7. [obs] On the widening from two batteries to eight tools with before = 3:
   - What it gained: one real extra leaker beyond the routed two batteries, `tools/check-adjacency-overlap.py --selftest` (control 0, canary 1).
   - What it inflated: five of the eight targets never leaked. "the eight lane tools ... no longer follow" (`SCORECARD.md:1104`) implies all eight did, but the movable quantity is 3.
   - The not-verified guard "below 2" (`SCORECARD.md:1106`) is tied to the battery count, not to the widened set.
   - [obs] All three before-leaks are exit-code differences with `canary_changed` false. Under the canary, the batteries fail at their first read of the lane (`git -C <lane> rev-parse --verify …` returned 128; the GIT_DIR-only canary run of `tools/mutants-kernel-taint.py` also gives rc 1 with the canary's commits unchanged).
   - [inf] So the probe detects reads that follow the inherited variables, not the round-28 write into a foreign repository. The canary never holds the revision, so the incident path (reads succeed, then writes land) is not exercised. A partial fix that scrubs only the reads would still be caught, because the later writes then change the canary. This is a framing limit, not a false count.
   - [inf] The fingerprint (`tools/probe-git-env-leak.py:67-81`) leaves out `.git/config`, hooks and work-tree files. A leak that writes only there, with an unchanged exit code, would not count.
   - Honest wording: "3 of 8 leak; 0 of 8 after".

8. [obs] Part of the routed requirement was dropped without saying so. Routed defect 2 asks to "Scrub `GIT_*` in both batteries, and add a selftest that can fail" (`corpus/lessons/round-28-verifier-spotcheck.md:90`). C2's after-value has no selftest component; the external probe stands in for it. That is acceptable only if stated.

9. [obs] Separability holds. C1's counter reads only corpus, `SKILL.md` and `SOURCES.md` objects (`tools/check-owed-statements-r29.py:130-200`). C2's probe reads only the tool tree and the canary.

10. [obs] Axis framing of C2 holds as operability. AXES.md defines it as "commands that exist, scripts that run". The measured property is that a lane script produces its stated outcome regardless of the caller's environment.
    - [inf] The targets are the lane's meta-tools (counters and batteries), not the census that the operability row scores (`SCORECARD.md:1092`). The 9 → 9 ordinal is therefore fitting, and C2 cannot carry the lowest-axis duty.

## Smallest safe corrections

- C1, choose one:
  - Narrow C1 to O01 to O04 as the depth claim, and move O05 to O12 to a separate calibration claim or report them as routed items.
  - Keep C1, but strengthen the counter. M6 should require an `S###` for every item. M7 should require one of S148, S149 or S150 with an opening date of 2026-10-22, a `sources/S###.*` snapshot and a verbatim quote. M5 should reject content-free `now` text, for example by requiring a token from the cited source quote.
- C2: replace "every tool with a sandbox git write" with the frozen-grep wording, or extend the set to include `tools/check-self-assessment.py` and run from a clone checkout. Disclose that routed defect 2's selftest half is dropped, and state the movable quantity as 3.
- Framing: replace "7 is answered by the framing above" with "author reading; operator ruling pending".

Scope: read=SCORECARD.md r27-r29 sections, /home/vgpnk/Projects/shokunin/AXES.md, tools/check-owed-statements-r29.py, tools/probe-git-env-leak.py, tools/mutants-adjacency-overlap.py, tools/mutants-kernel-taint.py and tools/check-self-assessment.py excerpts, git show of 22 tools at 16e9ab2a, round-27/28 spot-check routed defects, corpus/lessons/round-27.md:78-83, corpus/QUALITY.md:135, RevRoutedDefects.md:18-22, corpus/SOURCES.md rows, the round-29 measure receipts; wrote=.ufo/waves/round-29/w1/CritAxisFraming.md, .ufo/waves/round-29/w1/CritAxisFraming/{c1-pad-mutant2.jsonl,canary-check-self-assessment.out,canary1.sh,declared-probe-81a061a.jsonl,ext-probe-81a061a.jsonl,pad_mutant.py,probe-ext.py}, scratch under /fast/scratch/hyaku/tsukuroi-r29/CritAxisFraming/; executed=sandbox git clone/checkout/commit in the seat scratch clone (with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset), read-only git log/show/diff/ls-tree/archive in the lane, python3 tools/check-owed-statements-r29.py at 81a061a and at sandbox 9c803092, python3 tools/probe-git-env-leak.py at 81a061a (exit 1, 3 of 8), python3 probe-ext.py over 14 tools (exit 2), canary1.sh on check-self-assessment and check-appended-notices, a GIT_DIR-only canary on mutants-kernel-taint
Model: not exposed
Installs: none
