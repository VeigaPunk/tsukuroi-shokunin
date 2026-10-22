# MutSelfAssessPlan — pre-design of the round-26 C2 (check set v2) mutation test

Verdict: holds, with one contract question for the integrator. The mutation test for claim C2's v2 check set is designed, implemented and exercised: 31 mutants are catalogued against the declared v2 rules, the runner applies them in an isolated sandbox with byte-exact restoration, all 31 edits applied without error, and the whole catalogue was measured against a v2 implementation in a scratch copy. That measurement produced two findings the L1 has to settle: the implementation reads ordinal transitions only from measured-outcome sections, which is narrower than the declared K01 to K06 rule, and it accepts an axes heading of the form `(Round26)`, which the declared heading text does not name.

Scope of this seat: a pre-design only. No lane file outside this seat's own paths was written, no lane git or jj write command was run, and no host state was changed. The round-26 axes table does not exist yet, so every catalogue entry that needs it is written against the heading text the declaration fixes (`## Axes — current self-assessment (round 26)`) and is guarded by a precondition that is checked at run time.

## What was produced

1. [obs] `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/MutSelfAssessPlan/catalogue.json` — sha256 `82a9fcaae31e76cd395a89eda6f00d19654de02e6ea49495b97eee9a689b5fe4` — 31 mutants, each with its declared rule, the target checks, the file edits, a precondition list and the expected detector outcome. Five mutants (M03, M15, M19, M21, M22) also carry an `alt_expected` block for the second reading of the contract, because the measurement exposed an ambiguity (finding 18). The catalogue is a machine-readable contract between this design and the run.
2. [obs] `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/MutSelfAssessPlan/run-mutants.py` — sha256 `b3215125aa3f9d813fef679b4b47cb83e0554d2387f3fd4b839e45cec5d0ba93` — the runner.
3. [obs] Scratch material (never in the lane): `/fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/` holds the two synthetic state builders (`make-synth.py`, `make-synth-v2.py`), the scratch repositories, the run records `synth-run.json`, `v2-run-9.json`, `v2-run-22.json`, `v2-run-4.json`, `lane-run-4de2b6b.json` and the baseline captures.

## The rules the catalogue targets

4. [obs] K01 to K06 as declared for round 26 (`SCORECARD.md:903`): the declaring round N is the number in the heading of the current axes table, which must read `## Axes — current self-assessment (round N)`; a heading without a round number exits 2. The ordinal reference is the last match of the round-25 refinement regex (`SCORECARD.md:807`) on SCORECARD lines outside that table, excluding every line inside a section whose heading (any level) names round N (`Round N` or `round N` as a whole number), unless that heading also contains `measured outcome`.
5. [obs] K07 to K23 are unchanged from round 25 (`SCORECARD.md:795`, `SCORECARD.md:807`), and K24 to K27 are new (`SCORECARD.md:904`): for SHONEN boxes 1 to 4, every `corpus/knowledge/*.md` path the box names exists at the revision and carries no supersession marker, meaning none of its first 20 lines matches the case-insensitive word `superseded`.
6. [obs] The catalogue's 31 mutants cover eight groups: the v2 section-exclusion rule (M01, M02, M05), the round number in the axes heading (M03, M04), stale counts in the round-26 table for K07 to K11 (M06 to M10), the new supersession clause for K24 to K27 (M11 to M14), the round-25 ordinal survivors from `.ufo/waves/round-25/w2/MutC1Ordinals.md` (M15 to M22, replayed against the round-26 table), and the round-25 count survivors from `.ufo/waves/round-25/w2/MutC1Counts.md` (M23 to M31). Expected outcomes under the declared rule: 22 killed, 7 survived, 2 cannot-evaluate.

## Runner method

7. [obs] The runner builds each sandbox exactly as the round-25 mutation seats did: `git -C <lane repo> archive <rev> | tar -x -C <sandbox>`, then `git init` with no remote, then `git add -A` and a sandbox-local base commit. Each mutant's edits are applied to the working tree, committed, and measured with `python3 tools/check-self-assessment.py --revision HEAD --repo <sandbox>`; afterwards `git reset --hard <base>` and `git clean -fd` restore the tree, and a sha256 tree digest (over every path and its file sha256) is compared with the pristine digest.
8. [obs] The verdict rule is mechanical: killed means the detector's exit code differs from the baseline exit code, survived means it equals it, and inconclusive covers a baseline that is not clean, a tool that is not the v2 check set, and an unmet precondition. The runner refuses to declare a kill when the baseline fails, and it refuses to declare a verdict at all when the tool reports fewer than 27 checks unless `--allow-non-v2` is given.
9. [obs] Every catalogue edit is guarded: a precondition names a file and a literal string that must be present in the sandbox before the mutant runs, and an edit that cannot be applied is recorded as an error rather than silently skipped. In the measured runs, 0 of 31 mutants were skipped or errored.

## Base value observed

10. [obs] At the round-26 declaration commit `b13e991fb96972b423b868ba122187f75357368c` the committed tool is still the v1 set: run against a sandbox archived from that commit, `python3 tools/check-self-assessment.py --revision HEAD --repo <sandbox>` returned exit 1 with `"checked": 23` and one mismatch, `K10` (reason: `depth row states 26 lesson files; corpus/lessons holds 27 files`). The v1 base therefore shows the lesson-file count only; the declaration's hand count of 3 of 27 (K10, K24, K26) needs the v2 tool to see K24 and K26.
11. [obs] The lane's current revision carries the committed v2 tool (`4de2b6b1c0cde1f7c7ca9e5727965bcf6aa6ba9e`, "round-26: pin counting tools (check-storage-health.py new, check-self-assessment.py v2)"). Measured against a sandbox archived from it, the v2 tool returns exit 1 with `"checked": 27` and 5 mismatches: `K02` (`no dated move record for coverage: no coverage ordinal transition in any measured-outcome section`), `K06` (the same for adjacency), `K10` (`depth row states 26 lesson files; corpus/lessons holds 27 files`), `K24` (`SHONEN box 1 cites 1 corpus/knowledge note(s), 1 of them unusable: corpus/knowledge/root-dac-decision-r12.md carries a supersession marker at its line 7`) and `K26` (SHONEN box 3, the same note). The declaration's hand count for the base was 3 of 27 (K10, K24, K26); the two extra are K02 and K06, which report a missing move record because the round-26 axes table and the round-26 measured-outcome section do not exist yet. The synthetic state of finding 13, which has both, measures 0 of 27 with exit 0.
12. [inf] The catalogue is therefore written for the round-26 measured revision, where the declared target is 0 of 27 with exit 0. Running the catalogue against the round-26 base would make every mutant inconclusive, because the base baseline is not clean; the runner does exactly that and reported M01 as `inconclusive` with the reason `the baseline is not clean (exit 1, failing ['K02', 'K06', 'K10', 'K24', 'K26'])`.

## Mechanics validation

13. [obs] Because the round-26 axes table does not exist yet, a synthetic round-26 state was built in a scratch copy of the declaration commit: the round-25 axes table copied under `## Axes — current self-assessment (round 26)` with the one stale count corrected (27 lesson files), a `### Round 26 measured outcome` section recording the six ordinal transitions, and — for the v2 run only — the SHONEN boxes reworded so no box cites a superseded note. The synthetic state is scratch material, never lane content.
14. [obs] Against the synthetic state with the v1 tool, all 31 mutants applied cleanly: baseline exit 0 with 0 of 23, 22 killed and 9 survived, 0 errors, 0 skipped, and the pristine tree digest `abc2baeb343867b3b248fced27174c892d3f96476f5889e360e2ed56b7f1fed6` reproduced exactly after every restoration and at the end of the run (record `/fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/synth-run.json`).

## The nine v2-only mutants, measured against a v2 implementation

15. [obs] A v2 tool exists in the lane working tree as well as in the lane's current revision (`git status` shows `M tools/check-self-assessment.py`; the file's header reads "Round 26, claim C2 (calibration). Fixed check set v2, K01 to K27"). It was copied into a scratch copy of the synthetic state and the catalogue was run there. Baseline: exit 0, `"checked": 27`, 0 mismatches. These results are provisional: the tool was unreviewed when the run was made and the run itself was not a lane revision.
16. [obs] Results for the nine v2-dependent mutants (`/fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/v2-run-9.json`):

| Mutant | Change | Expected by the declared rule | Observed | Verdict |
|---|---|---|---|---|
| M01 | `depth 8 → 7` inside the round-26 declaration section | K01 to K06 unchanged (excluded) | exit 0, 0 mismatches, no failing check | expectation met |
| M02 | `depth 8 → 7` inside `### Round 26 measured outcome` | K01 mismatch | exit 1, 1 mismatch, failing `K01` | expectation met |
| M03 | axes heading `(Round26)` without a space | exit 2 (no round number in the declared form) | exit 0, 0 mismatches | expectation not met — finding 18 |
| M04 | axes heading with no round number | exit 2 | exit 2, `CANNOT_EVALUATE`, reason `no round number in the axes heading` | expectation met |
| M05 | `### Round26 measured outcome` (no space) with `depth 8 → 7` inside | the section does not name round 26, so the transition counts: K01 mismatch | exit 1, 1 mismatch, failing `K01` | expectation met |
| M11 | SHONEN box 1 cites a superseded note | K24 mismatch | exit 1, 1 mismatch, failing `K24` | expectation met |
| M12 | SHONEN box 1 cites a note that does not exist | K20 and K24 mismatch | exit 1, 2 mismatches, failing `K20`, `K24` | expectation met |
| M13 | SHONEN box 1 cites an existing, unmarked note | no change | exit 0, 0 mismatches | expectation met |
| M14 | SHONEN box 1 cites a note whose `superseded` marker is below line 20 | no change | exit 0, 0 mismatches | expectation met |

## The twenty-two round-25 survivors, measured against the v2 implementation

17. [obs] The same scratch run measured the remaining 22 mutants (`/fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/v2-run-22.json`): baseline exit 0 with 0 of 27, 22 of 22 mutants applied without error, 16 killed and 6 survived, and the pristine tree digest `aa05058e5eecc0c41a684d73fbfdcd07a885838b39f82115654729f210eb7e3d` reproduced exactly after every restoration and at the end of the run. 18 of the 22 declared expectations held; the four that did not are M15, M19, M21 and M22, and all four fail for the same reason (finding 18).

## The contract question this measurement exposed

18. [obs] The measured v2 implementation and the declared K01 to K06 rule disagree about where an ordinal transition may be recorded. The declared rule (`SCORECARD.md:903`) reads the ordinal reference as the last match of the round-25 refinement regex on SCORECARD lines outside the current axes table, excluding every line inside a section whose heading names round N unless that heading also contains `measured outcome`. The implementation's own reason strings describe a narrower search: on the synthetic baseline, and again on the lane's current revision, K02 and K06 reported `no dated move record for coverage: no coverage ordinal transition in any measured-outcome section`.
19. [obs] The four affected mutants, with the declared rule on the left and the measured implementation on the right (record `/fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/v2-run-4.json`, which shows both expectation columns):

| Mutant | Change | Declared rule | Measured v2 |
|---|---|---|---|
| M15 | later `depth 8 → 9` in an appendix section | killed (K01) | survived |
| M21 | later `calibration 9 → 8` in an appendix section | killed (K05) | survived |
| M22 | later `adjacency 8 → 7` in an appendix section | killed (K06) | survived |
| M19 | depth score cell raised to 9 plus `depth 8 → 9` in an appendix | survived (the prose agrees with itself) | killed (K01) |

20. [inf] Two readings are possible and the choice is the integrator's, not this seat's. The narrow reading is that only a measured-outcome section records a move, which makes the four mutants above behave as measured and makes M19 a real detector of an unsupported score. The declared reading is that any line outside the current axes table, apart from the declaring round's own non-outcome sections, is an ordinal record, which is what the round-25 checks were built on and what the round-25 mutation report measured. Either way the L1 should say which one the contract means, because the two differ on what a lane may write outside a measured-outcome section. [inf] The implementation is also stricter than the round-25 regex in a second way: it rejects `(Round26)` as a section name (M05 killed) while accepting `(Round26)` as the axes heading (M03 survived), so the two naming rules inside one sentence of the declaration are applied with different strictness.
21. [obs] This seat changed no contract. Each of the five affected mutants carries an `alt_expected` block with the value under the other reading, and the runner reports `expectation_met` (the declared rule) and `expectation_met_alt` (the narrower rule) separately, so the catalogue stays usable under either ruling. The catalogue's `v2_divergence` block records the same summary in machine-readable form.

## Round-25 survivors carried forward

22. [obs] The mapping from the two round-25 mutation reports to the new catalogue, with the round-25 verdict, the expected round-26 verdict under the declared rule, and what the measured v2 implementation did:

| Round-25 case | Source | New mutant | Expected (declared rule) | Measured v2 |
|---|---|---|---|---|
| m1 depth score 8 → 6 in the axes table | MutC1Ordinals.md:4 | M16 | killed (K01) | killed (K01) |
| m2 later `depth 8 → 9` | MutC1Ordinals.md:5 | M15 | killed (K01) | survived |
| m4 later `coverage rows 10 → 15` | MutC1Ordinals.md:7 | M17 | survived | survived |
| m5 arrow inside the axes row | MutC1Ordinals.md:8 | M18 | survived | survived |
| m6 later glued `operability9→9` | MutC1Ordinals.md:9 | M20 | survived | survived |
| m8 later `calibration 9 → 8` | MutC1Ordinals.md:11 | M21 | killed (K05) | survived |
| m9 later `adjacency 8 → 7` | MutC1Ordinals.md:11 | M22 | killed (K06) | survived |
| m10 self-consistent pair (score 9 plus `depth 8 → 9`) | MutC1Ordinals.md:12 | M19 | survived (coverage finding) | killed (K01) |
| M1 add one knowledge note | MutC1Counts.md K07 | M23 | killed (K07) | killed (K07) |
| M6 remove the `notes` phrase | MutC1Counts.md K07 | M24 | killed (K07, stated value none) | killed (K07) |
| M2 add one SKILL.md line | MutC1Counts.md K08 | M25 | killed (K08) | killed (K08) |
| M3 add one pipe line | MutC1Counts.md K09 | M26 | killed (K08 and K09) | killed (K08, K09) |
| M3c pipe line with the line count compensated | MutC1Counts.md K09 | M27 | killed (K09 only) | killed (K09) |
| M4 add one lesson file | MutC1Counts.md K10 | M28 | killed (K10) | killed (K10) |
| M5 stated README count off by one | MutC1Counts.md K11 | M29 | killed (K11) | killed (K11) |
| M5b append one line to corpus/README.md | MutC1Counts.md K11 | M30 | killed (K11) | killed (K11) |
| M7 `97 cases` → `96 cases` | MutC1Counts.md K13 | M31 | killed (K13) | killed (K13) |

23. [obs] The two round-25 findings that the catalogue deliberately keeps as survivors are coverage findings, not defects: a score that no move record supports still passes when the prose agrees with itself (M19 under the declared rule), and a transition whose after-value is out of range is not an ordinal (M17). The catalogue records both as survivors on purpose, so a later tool change that kills them shows up as a change in the contract rather than as a silent tightening. M19's row above shows that this finding is exactly the one the narrower reading changes.

## What the L1 has to do to run this

24. [obs] The runner takes the measured revision as an argument and needs no change: `python3 .ufo/waves/round-26/w1/MutSelfAssessPlan/run-mutants.py --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --revision <measured-rev> --catalogue .ufo/waves/round-26/w1/MutSelfAssessPlan/catalogue.json --out <record>.json`. It needs the v2 tool at that revision (27 checks) and the round-26 axes table and measured-outcome section in the tree; every mutant that needs either carries that as a precondition, and a missing precondition is reported as skipped rather than as a pass.
25. [unk] The exact wording of the round-26 axes table and of the round-26 measured-outcome section is not fixed yet, so the anchor strings in the catalogue (the heading `## Axes — current self-assessment (round 26)`, the heading `### Round 26 measured outcome`) are the declared forms from `SCORECARD.md:903` and from the round-25 layout at `SCORECARD.md:863`. If the L1 words them differently, the catalogue's `preconditions` and `section` fields are the only places to adjust; the edits themselves are written against the table rows and the heading names, not against fixed line numbers.

## Lane read-only evidence

26. [obs] The lane repository was never written to by this seat: no git or jj write command was run against it, and the only paths this seat created inside the lane are `.ufo/waves/round-26/w1/MutSelfAssessPlan/catalogue.json`, `.ufo/waves/round-26/w1/MutSelfAssessPlan/run-mutants.py` and this report. The lane HEAD moved from `b13e991fb96972b423b868ba122187f75357368c` to `4de2b6b1c0cde1f7c7ca9e5727965bcf6aa6ba9e` during this seat, by the L1's own commit that pins the v2 tool; the `M SKILL.md`, `M corpus/SOURCES.md` and `?? tools/check-storage-health.py` entries in `git status` belong to concurrent seats.
27. [obs] Every sandbox was built with `git archive` plus `git init` with no remote; no remote was added, no push URL was changed, and nothing was pushed. The scratch repositories and every run record live under `/fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/`.
28. [obs] No host action was taken: no package transaction, no service start or stop, no configuration write, no scrub, no counter reset. The tool was read through git only, and the concurrent v2 tool was copied out of the lane working tree into a scratch directory and never written back.

Scope: read=SCORECARD.md (the round-26 declaration at lines 874 to 908, the round-25 axes and capabilities tables, the round-25 declaration and refinements), tools/check-self-assessment.py (the v1 tool at the declaration commit and the v2 tool from the lane working tree and from revision 4de2b6b, read only), SHONEN.md, the round-25 mutation reports .ufo/waves/round-25/w2/MutC1Ordinals.md and .ufo/waves/round-25/w2/MutC1Counts.md, corpus/knowledge/ note heads for the supersession markers, and the git archives of b13e991fb96972b423b868ba122187f75357368c and 4de2b6b1c0cde1f7c7ca9e5727965bcf6aa6ba9e; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/MutSelfAssessPlan/catalogue.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/MutSelfAssessPlan/run-mutants.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/MutSelfAssessPlan.md and scratch files under /fast/scratch/hyaku/tsuku26/MutSelfAssessPlan/; executed=git archive and git init in scratch only, 76 detector invocations of python3 tools/check-self-assessment.py (six baselines and 68 mutant runs across six scratch sandboxes, plus two direct runs inside scratch repositories), sha256sum and tree digests, and read-only git rev-parse, git status and git diff --stat in the lane
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
