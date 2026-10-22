# CritC2Construction — round 26, wave 1, claim C2 check set v2

Verdict: fails as a repair of routed defects 3 and 7. The predicted base value of 3 of 27 reproduces under a literal model of the declared rules. But the K01 to K06 exclusion only blocks the round named in the axes-table heading, so earlier rounds' plan prose still certifies ordinals. At the declaration commit itself, two checks resolve to the round-26 declaration's own rows. At a realistic final revision, three checks resolve to the same round-25 plan lines the round-25 critique attacked. K24 to K27 can be passed by citing the `.json` companion, by dropping the citation, or by rewording or moving the banner in the cited note. They also miss late supersession notices and false-flag notes that only mention supersession. None of the three base mismatches is an assessed value (score or box mark) being wrong, and no repair path changes one.

Seat: TsukuroiR26.CritC2Construction. Declaration under test: `SCORECARD.md:900-905` at `b13e991fb96972b423b868ba122187f75357368c` (file sha256 `cf03b266…b137a`, identical to the working tree). No v2 tool exists yet: the ExecSelfAssessV2 clone `/fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/repo` is at `b13e991` with a clean status [obs]. I therefore built a literal reference model of the two changed rules, `.ufo/waves/round-26/w1/CritC2Construction/refv2.py` (sha256 `62c76739…d667`). It reads only through `git show`/`git ls-tree` and implements two readings of "section":

- flat: a section runs to the next heading of any level;
- tree: a section runs to the next heading of the same or higher level.

K07 to K23 come from the unchanged v1 tool (`git show e9f5356:tools/check-self-assessment.py`, sha256 `343367fb…6242f`). The mutant harness is `.ufo/waves/round-26/w1/CritC2Construction/mutants.py` (sha256 `45e60a74…d047`). Every mutant is a `git archive b13e991` copy in `/fast/scratch/hyaku/tsuku26/CritC2Construction/sb/<name>` with `git init` and no remote, deleted after each run. Outputs are in `.ufo/waves/round-26/w1/CritC2Construction/out/`: `summary-M.json`, `summary-S.json` and one `<mutant>.json` each.

A note on that output directory: the first run used a table picker that took the last table in the axes section. That reading broke only the M series, where a second table follows; the M series was re-run after the model was fixed to prefer the table headed `Axis`, as the v1 `pick_table` does. The S series has a single table, and its results agree with the fixed model's `out/ref-b13e991.json`. The whole first run is kept as `out/summary-run1-superseded.json`: its M rows show stated `null` and 6 mismatches, are stale, and must not be cited. `out/summary-S.json` holds only its S rows.

## Findings

1. **The base value reproduces: 3 of 27 (K10, K24, K26).** [obs]
   - v1 at `e9f5356`: exit 1, the only mismatch is K10, "depth row states 26 lesson files; corpus/lessons holds 27 files" (`out/v1-e9f5356.json`).
   - Model at `e9f5356`: K01 to K06 give 0 mismatches under both readings; K24 and K26 flag `corpus/knowledge/root-dac-decision-r12.md`, "superseded marker at line 7" (`out/ref-e9f5356.json`).
   - So the L1's hand count is reproduced. Findings 7 and 8 explain why that number is not a fair before-value for "self-assessment mismatches".

2. **K01 to K06 at the base still resolve to plan prose, just from older rounds.** [obs]
   - References at `e9f5356` (N = 25):
     - K01 → `SCORECARD.md:759`, round-24 *declaration refinements*: "C2 is recorded against **depth 8 → 8 (tied lowest)**".
     - K03 → `:621` and K06 → `:620`, the round-20 *declaration* table: "operability 9→9 (0)" and "adjacency 8→8 (0)".
     - K02 → `:224` (fleet round-1 post-review correction), K04 → `:772` and K05 → `:771` (round-24 measured outcome). These three are records.
   - The declaration says "only its measured outcome can record a move" (`SCORECARD.md:903`). That holds only for round N. Every earlier round's declaration and refinement prose stays eligible. Three of the six base references are plan text.
   - Impacted axes: calibration (false provenance).

3. **At the declaration commit, K01 and K05 resolve to the round-26 declaration itself.** [obs]
   - At `b13e991` the newest axes heading is still `## Axes — current self-assessment (round 25)` (`SCORECARD.md:815`), so N = 25 and the round-26 section is not excluded.
   - K01 → `SCORECARD.md:892` (C1 row "depth 8 → 8 (tied lowest)") and K05 → `:893` (C2 row "calibration 9 → 9"), under both readings (`out/ref-b13e991.json`).
   - N is read from a heading the author writes, not from the round being measured. That stays true at every round-26 revision until a "(round 26)" table lands. Mutant M7 labels the new table "(round 27)" with all scores set to 10 and adds one "Planned:" line in the round-26 section. Result: 0 mismatches in both readings, every reference at line 910.
   - Impacted axes: calibration (routed defect 3 recurs at the declaring commit).

4. **At a realistic final revision, the round-25 counterexample returns unchanged.** [obs]
   - Mutant M0 appends a "(round 26)" axes table with the round-25 scores and a `### Round 26 measured outcome` with no arrows, the shape round 25 used.
   - K01 → `:793`, K04 → `:807`, K05 → `:792` and K06 → `:620`. These are the exact lines of round-25 CritC1Construction attack 2 (`.ufo/waves/round-25/w2/CritC1Construction.md:14-19`).
   - Mutant M1 edits only the round-25 regex illustration at `:807`, from "`freshness (actual 9 → 9` is" to "`freshness (actual 7 → 7` is". K04 flips to a mismatch (stated 9, observed 7, line 807) in both readings (`out/M1-final-r25-regex-example-7.json`).
   - The moving exclusion window just hands the self-reference to the next round. Routed defect 3 asked to "exclude the declaring round's lines, or bind to dated move records" (`corpus/lessons/round-25-verifier-spotcheck.md:103`). The first option, as built, does not bind anything.

5. **Self-grant: the round-25 one-line uplift still passes, through several doors.** [obs] Each mutant below sets all six scores to 10 in a "(round 26)" table and adds the line "depth 8 → 10, coverage 9 → 10, operability 9 → 10, freshness 9 → 10, calibration 9 → 10, adjacency 8 → 10". The flat and tree columns give the mismatch count under each reading.

| Mutant | Where the line goes | flat | tree |
|---|---|---|---|
| M2 | `## Planned next round` (heading names no round) | 0 | 0 |
| M3 | `### Round26 declaration refinements` (no space) | 0 | 6 |
| M5 | `### round-26 post-review corrections (appended)` | 0 | 6 |
| M4 | inside `### Round 26 measured outcome` (the declared exemption) | 0 | 6 |
| M6 | `### Declaration refinements after wave 1 …` nested under `## Round 26 — declaration` | 0 | 6 |
| M7 | the round-26 section, with the table labelled "(round 27)" | 0 | 0 |
| M9 | `## Post-review claim corrections`, calibration only set to 10 | 0 | 0 |

   - The spelling gap is not hypothetical. The lane's own headings use `Round-13`, `Round14` to `Round19`, `Round21`, `Round22` and `Round23` (`SCORECARD.md:320, 384, 442, 488, 511, 548, 566, 600, 606, 610, 646, 652, 672, 686, 692, 708, 724`). Under the declared `Round N` / `round N` match, none of those eleven rounds' headings would have excluded anything.
   - Tree reading side effect [obs]: the axes heading itself names round N, so every `###` appended after the table is excluded, including a `### Round N measured outcome` placed there, which is where round 25 put its own (`SCORECARD.md:863`, under `## Capabilities — current (round 25)`). The declared exemption is then unreachable. The text does not fix which reading applies, and four mutants (M3 to M6) change result between them.
   - Impacted axes: calibration (the overreach the axis exists to catch).

6. **Depth and operability have no dated arrow record anywhere outside plan prose.** [obs]
   - If only `measured outcome` and `post-review` sections are counted (my allow-list probe in the shell, any heading level), K01 depth and K03 operability have no reference at `e9f5356` or `b13e991`.
   - The move log (`SCORECARD.md:21-37`) names axes without numbers.
   - The only arrow forms for those two axes are declaration rows such as `:621` and `:759`.
   - [inf] So K01 and K03 can only be satisfied by plan text. This is by construction under any deny-list rule, which is the core reason the exclusion approach cannot fix routed defect 3.

7. **K24 to K27 can be gamed and miss the routed box-4 defect.** [obs] Each S mutant edits the `b13e991` tree. v1 was also run on S0, S1, S2, S3, S5 and S8. In S1, S2, S3 and S5 it still reports only K10, so those edits are not caught elsewhere; S8's extra v1 hits are listed under S8. S4, S6 and S7 only change note bytes or add existing paths.

   - **S1, cite the `.json` companion.** `corpus/knowledge/root-dac-decision-r12.json` exists. Boxes 1 and 3 changed from `.md` to `.json` give K24 to K27 = 0, and v1 still reports only K10. Same superseded content, no flag.
   - **S2, box naming no corpus note.** Boxes 1 and 3 cite `SKILL.md` instead: K24 to K27 = 0 (vacuous), v1 only K10.
     - Box 4 already cites no `corpus/knowledge/` note (`SHONEN.md:12`), so K27 is vacuously green at the base.
     - Routed defect 7 named boxes 3 and 4 (`corpus/lessons/round-25-verifier-spotcheck.md:107`). Box 4's superseded evidence is the round-12 refinement in `PROVINCE.md:85-90`, superseded by `:92-96` (`.ufo/waves/round-25/w2/RevShonen.md:38`), which K27 cannot see by design.
   - **S3, reword the marker in the cited note.** The banner `> **Superseded after outside rejection.**` (`corpus/knowledge/root-dac-decision-r12.md:7`) changed to "Replaced …" gives K24 to K27 = 0. Nothing freezes cited notes, and the round may edit `corpus/knowledge/`.
   - **S4, push the banner past line 20.** Adding 14 metadata lines above the banner gives K24 to K27 = 0.
   - **S5, late notice is a false negative.** Box 4 cites `corpus/knowledge/oom-event-plane.md`: K27 stays green.
     - That note has no `superseded` in lines 1-20.
     - Its round-25 notice at `:473-475` says its line 344 is "contradicted" and calls it "The same superseded claim".
     - This in-place, deep-in-file notice is the lane's normal convention: 24 notes carry `superseded` only after line 20, for example `package-state-plane.md` (16 hits) and `update-safety-note.md` (5). Survey command in Scope.
   - **S6 and S7, a mention is a false positive.** Box 4 cites `closeout-r11.md` (line 18: "Errata are append-only: a superseded …") or `source-locator-clarification-r15.md` (line 19: "only the supplemental locator is superseded, in `…source-scope-correction-r14.md`"). K27 becomes a mismatch, yet neither note is superseded. The r15 note is the superseding one.
   - **S8, double and triple counting.** Deleting `corpus/knowledge/executor-test-sufficiency.md` raises K07, K22 and K26: one defect, three mismatches.
   - `supersedes` versus `superseded`: the word test does not fire on "Supersedes / narrows" headers (`memory-pressure-r25.md:88`), which is right for the superseding note. But it also does not fire on "Replaced", "Retracted", "contradicted" or "withdrawn", so S3 generalises.

8. **3 of 27 is a fair count of what the tool flags, not a fair before-value of self-assessment mismatch.** [obs]
   - **K10 is drift caused by the reviewer, not the lane.** The 27th lesson file `corpus/lessons/round-25-verifier-spotcheck.md` was added by the non-author spot-check commit `e9f5356` (`git diff --name-status 157ee25 e9f5356 -- corpus/lessons/` gives `A`). The table was right at its measured revision.
     - [inf] Every round whose base follows a spot-check commit starts with this mismatch built in.
     - The round-26 C1 entry and lesson will move K07, K08, K09 and K10 again. So C2's zero can only be reached by re-transcribing after C1 lands, and the two claims are not causally separable at the measured revision (compare round-25 refinement, `SCORECARD.md:811`).
   - **K24 is a proxy hit on a partial supersession.** The r12 banner scopes itself to "active B2 unit-path reasoning" (`root-dac-decision-r12.md:7-11`). RevShonen finding 5 says the r13 correction does "not touch the root-metadata observation" that box 1 cites it for (`RevShonen.md:55`). Swapping the citation is a wording repair.
   - **K26 is a real citation defect, but not the substantive one.** Box 3 does cite a superseded note for executability (`RevShonen.md:46`). Its real defect is that the only executability test ran on a 444-line SKILL.md against 2355 lines now (`RevShonen.md:47`), and K26 does not test that.
   - **Real defects count 0.** These carry no check:
     - box 2's "current" and "delivery" claims (RevShonen finding 1, rated high);
     - box 4's superseded PROVINCE refinement and missing "contested ownership remains unresolved" clause (finding 3, medium-high);
     - box 3's untested instructions (finding 4).
   - **No assessed value moves.** All four boxes are `[~]` and stay `[~]`. All six scores stay the same ordinals.
     - [inf] The 3 → 0 move would consist of one re-transcribed count and two citation edits. None of them changes a stated assessment.
     - This matches round 25's K21: "one of the 13 flips is a wording change, not a repaired fact" (`RevShonen.md:33`).
   - Impacted axes: calibration (size and meaning of the move).

## Fixable defect or tradeoff

- Findings 3, 5 (spelling, reading ambiguity, binding of N) and 7 (`.json`, freeze, double count) are fixable by stricter text appended before any v2 measurement. The target is unchanged.
- Findings 2, 4 and 6 are design properties of a deny-list. Removing the current round cannot make plan prose stop counting.
- Finding 8 is a tradeoff the canonical judge should reject as a calibration gain. A 3 → 0 under v2 should be credited at most as "one stale count and two box citations updated". It is not evidence that the lane's self-assessment became truer.

## Smallest safe correction

Do not move the target. Append, before the v2 tool is first run on a round-26 revision:

1. **K01 to K06, allow-list instead of deny-list.**
   - The reference is the last arrow transition inside a section whose heading contains `measured outcome` or `post-review claim corrections` and names a round strictly less than the round being measured. Sections are hierarchical, and the round spelling is `(?i)round[\s-]?<N>` or `r<N>`.
   - If no such transition exists, the reference is the score in the previous `## Axes — ` table, which is the dated round-11 record at `SCORECARD.md:39-50`.
   - N is the number in the last `## Round N — declaration` heading, not the axes-table heading.
   - [obs from my probe] At `e9f5356` this gives depth 8 (round-11 table), coverage 9 (`:224`), operability 9 (round-11 table), freshness 9 (`:772`), calibration 9 (`:771`) and adjacency 8 (`:213`). All match, so the base stays 3. No plan line, and no line of round 26's own outcome, can satisfy a check.
2. **K24 to K27.**
   - Count `corpus/knowledge/*.json` citations against their `.md` twin.
   - A box that names no `corpus/knowledge/` note is unstated, which is a mismatch, or the check is dropped for that box and labelled so.
   - Skip absent paths, which K20 to K23 already count.
   - Treat any change between the claim base and `<REV>` to lines 1-20 of a note cited at the base as a mismatch unless the lesson logs it. This closes S3 and S4.
   - Scan the whole note for a notice that names a cited line as superseded or contradicted, or record the word test's known false positives and negatives (S5 to S7) beside the count.
3. **Labelling.** Report K10 as reviewer-induced drift, and K24 to K27 as citation hygiene that covers none of RevShonen's three substantive box findings. Claim no calibration movement beyond that.

Scope: read=SCORECARD.md (lines 1-60, 209-240, 600-905 at e9f5356 and b13e991), SHONEN.md, tools/check-self-assessment.py, corpus/lessons/round-25-verifier-spotcheck.md (lines 95-110), .ufo/waves/round-25/w2/CritC1Construction.md, .ufo/waves/round-25/w2/RevShonen.md, corpus/knowledge/root-dac-decision-r12.md (lines 1-20) and grep of supersession words across corpus/knowledge/*.md in a git archive of e9f5356, ~/.agents/skills/godspeed/SKILL.md, /fast/scratch/hyaku/tsuku26/ExecSelfAssessV2/repo (ls, git log, git status only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/CritC2Construction.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/CritC2Construction/{refv2.py,mutants.py,out/*.json}, /fast/scratch/hyaku/tsuku26/CritC2Construction/{base/,v1tool.py,sb/ (sandboxes, deleted)}; executed=read-only git (log, show, ls-tree, cat-file, diff --name-status, rev-parse, archive) on the lane, git init/add/commit only inside private sandboxes, python3 v1tool.py --revision e9f5356 --repo <lane> (exit 1, 1 mismatch; ran the census selftest in a temporary directory), python3 refv2.py at e9f5356 and b13e991 (exit 0), python3 mutants.py (19 mutants; six v1 runs exit 1), a shell head/grep survey loop for `superseded` in lines 1-20 versus later lines of corpus/knowledge/*.md, sha256sum
Model: not exposed (Cursor Auto)
Installs: none
