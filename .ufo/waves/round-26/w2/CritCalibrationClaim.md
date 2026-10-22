# CritCalibrationClaim — round 26, wave 2 (falsify), claim C2

Verdict: C2 partly holds. The figure 0 of 27 at 7dfea924 reproduces, and 21 of the 27 checks (K07 to K27) are real comparisons against observed repository state. K10, K24 and K26 were repaired for real. The six ordinal checks K01 to K06 compare one author-written line with another, so they assert rather than calibrate. Two of the five base mismatches (K02 and K06) came from the post-declaration refinement and were cleared by construction. The lesson gives a false reason for the change from 3 to 5.

Axes impacted: calibration (C2 itself), plus the record's provenance (lesson line 101).

## Findings

1. [obs] The headline value reproduces. I ran the pinned tool (sha256 `77c946a9…`, identical at 4de2b6b, 7dfea924 and the tree) with `python3 tools/check-self-assessment.py --repo <lane> --revision <REV>`. At 7dfea9244a84 it gives exit 0, mismatches 0. At the current tip 7f9f088 it also gives exit 0, mismatches 0. At e9f5356c it gives exit 1, mismatches 5 (K02, K06, K10, K24, K26), which matches `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/measure/c2-e9f5356c.json`. My outputs are in `/fast/scratch/hyaku/tsuku26/w2/CritCalibrationClaim/pin-{e9f,7df,7f9}.json`. The measured-outcome receipt at 7dfea924 showed 7 mismatches at the intermediate commit ef72f10d (K02, K06, K07, K08, K09, K10, K11). Round 26's own C1 commit broke K07 to K09 and K11, and the new table repaired them. The "5 to 0" headline skips that intermediate state.

2. [obs] The refinement did not narrow the target. It enlarged the base, and the lesson's reason for this is false.
   - I made a copy of the pinned tool whose K01 to K06 reference set follows the declaration text at b13e991 (`SCORECARD.md:903`): all lines outside the table, minus sections whose heading names round N, unless that heading contains "measured outcome". The copy is `/fast/scratch/hyaku/tsuku26/w2/CritCalibrationClaim/decl-rule.py`. I ran it with both nesting readings (outer heading excludes; innermost heading decides).
   - At e9f5356c, both readings give exit 1 and mismatches 3: K10, K24 and K26. That is exactly the L1's hand prediction (`SCORECARD.md:892`, "predicts 3 of 27: K10, K24, K26"). Outputs: `declo-e9f.json` and `decli-e9f.json`.
   - At 7dfea924, both readings give mismatches 0 (`declo-7df.json`, `decli-7df.json`). So the declared after-target 0 of 27 was not made easier by the refinement.
   - The refinement at 4de2b6b (`SCORECARD.md:922`) is the only reason the base rose from 3 to 5. Under it, coverage and adjacency have "no dated move record".
   - The round-26 lesson says otherwise. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-26.md:101` reads: "The declared hand prediction for C2's base (3 of 27) was wrong". ScribeMistakes row R26-DECLARED-BASE-PREDICTION-WRONG repeats this (`.ufo/waves/round-26/w1/ScribeMistakes.md:72-84`).
   - This is false provenance. The prediction was correct for the rule as declared; the rule changed afterwards. The refinement commit 4de2b6b records the before-value of 5 in the same commit as the changed rule (`SCORECARD.md:923`).

3. [obs] The refinement was a real strengthening against earlier-round plan prose. Under the declared rule at 7dfea924, K01, K04 and K05 read lines 793, 807 and 792 (`declo-7df.json`). Those are round-25 declaration and refinement lines (`SCORECARD.md:792-793` is the round-25 claim table; `:807` is a round-25 refinement bullet). That reproduces CritC2Construction's counterexample. Restricting the reference to measured-outcome sections removes it, and that part of the change is a correct repair of routed defect 3 (`corpus/lessons/round-25-verifier-spotcheck.md:105`).

4. [obs] K02 and K06 were cleared by construction: the round wrote the dated record that it then reads.
   - At 7dfea924, all six ordinal checks K01 to K06 take their observed value from one line, `SCORECARD.md:960`. The receipt shows `observed_line` 960 for all six.
   - Line 960 is in "### Round 26 measured outcome". It was written in the same commit (7dfea924) as the axes table it certifies, `SCORECARD.md:944-949`.
   - The line describes its own purpose: "Ordinal record, round 26 (dated move record that checks K01 to K06 read; no ordinal moved this round): depth 8 → 8; coverage 9 → 9; …" (`SCORECARD.md:960`).
   - Counterexample B: in a sandbox at 7dfea924 (`git archive` plus `git init`, at `/fast/scratch/hyaku/tsuku26/w2/CritCalibrationClaim/sb`), I deleted only the six arrows on line 960. The tool then exits 1 with mismatches 2 (K02 and K06 `no dated move record`). K01 and K03 to K05 fall back to lines 730, 731, 772 and 771. Output: `cxB.json`.
   - So the K02 and K06 repairs consist entirely of an author-written "X → X" line. No repository state other than that sentence changed.

5. [obs] Any pair of author-written lines satisfies K01 to K06, and the heading test is a substring match.
   - Counterexample A: in the sandbox I set the depth row to 10 (`| depth | 10 |`) and line 960 to "depth 8 → 10". The tool exits 0 with mismatches 0, and K01 matches with stated 10 and observed 10 at line 960 (`cxA.json`). The tool does not check whether the move is a single step, has evidence, or comes from a record the author did not write.
   - Counterexample C (sandbox fixture only; no round 27 was started): I added the heading "## Round 27 plan — what the next measured outcome should say (not measured)" with the line "Planned: depth 8 → 10", and set the table depth to 10. The tool exits 0 with mismatches 0, and K01 matches at line 964 (`cxC.json`).
   - So the refinement's statement that "all declaration, refinement, correction and move-log prose is excluded" (`SCORECARD.md:922`) holds only while authors avoid the words "measured outcome" in other headings. The code is `MEASURED_OUTCOME not in heading[2].lower()` in `tools/check-self-assessment.py`, function `reference_lines`.

6. [obs] Two authorities disagree, and no check sees it.
   - The round-26 table's "Last change" cells name the real dated moves: coverage "post-review correction at `SCORECARD.md:224`" (`SCORECARD.md:945`; line 224 is "B — coverage 8→9") and adjacency "`SCORECARD.md:213`" (`SCORECARD.md:949`; line 213 is "A — adjacency 7→8").
   - Under the refinement, those lines are not dated move records. The checker certifies coverage and adjacency against line 960, which records no move.
   - The table therefore cites one record as the last change while its checker certifies another. K01 to K06 never read the "Last change" cell.
   - [inf] Under the declared rule, K02 matched line 224, the real move, and K06 matched line 620, a round-20 claim-table row ("adjacency 8→8 (0)"). So the refinement fixed K06's plan-prose reference, but it also reclassified the genuine record at line 224 as non-qualifying, and the "repair" replaced it with a no-move line.

7. [obs] K10 is a real but transient match, produced by restating the count.
   - At e9f5356c the round-25 table stated 26 lesson files against 27 present. At 7dfea924 the new round-26 table states 28 against 28 present (`c2-7dfea924.json`, K10).
   - The round-25 cell was not corrected. A new table superseded it, and the counts were filled at the revision that adds the table (`SCORECARD.md:940`). So K07 to K11 pass by design at any revision where the author writes a fresh table.
   - The check still compares the stated number with a real file count, so it counts as calibration under the session rule.
   - [inf] Following the round-25 precedent (`round-25-verifier-spotcheck.md:105`, "this spot-check's own commit makes K10 read 27 files against the stated 26"), the next commit that adds a lesson file will make K10 mismatch again. The declaration discloses this.

8. [obs] K24 and K26 are a real text repair, within the limits of the detector.
   - SHONEN boxes 1 and 3 no longer cite `corpus/knowledge/root-dac-decision-r12.md`, which reads "Superseded after outside rejection." at its line 7. They point to the historical marker at `SKILL.md:1717-1721`, which reads "The round-12 matrix pointer above is a historical entry rejected at outside closure." (`git diff e9f5356c 7dfea92 -- SHONEN.md`; the in-place edits are disclosed at `corpus/lessons/round-26.md:74-80`.)
   - The detector is narrow: the word "superseded" in a note's first 20 lines. The repaired box 1 now cites `corpus/knowledge/aur-risk-plane.md`, whose lines 357 and 365 read "This notice supersedes it for current use only."
   - K24 passes that note because the word is "supersedes" and it appears after line 20.
   - The refinement discloses this limit (`SCORECARD.md:924`: "appended statement-level errata … are not counted").
   - [inf] Whether box 1 relies on the superseded parts of that note (the package-count and orphan-set text) is not established. The box cites the note as the per-plane note for the decision table.

9. [obs] Routed defect 7 is only partly covered by the count, and this is disclosed. Defect 7 names boxes 3 and 4 citing "superseded or untested notes" (`round-25-verifier-spotcheck.md:109`).
   - Box 4's superseded item was a PROVINCE paragraph, which K27 cannot see. The lesson says this repair is not counted (`round-26.md:69`).
   - The "untested" half is not measured by any check. Box 3 now says the retest "remains unexecuted".
   - This is a scope gap that was present at the declaration, not a narrowing after landing.

10. [obs] Other refinement items do not narrow anything.
    - "No match is a mismatch, not exit 2" matches the round-25 tool's behaviour.
    - The K24 to K27 limits paragraph removes no case the declared rule counted.
    - Measuring C2 only at the final revision is a separability correction.
    - The declared after-value (0 of 27, field `mismatches`) is unchanged between b13e991 (`SCORECARD.md:893`) and 4de2b6b (`SCORECARD.md:912`).
    - The tool bytes at 7dfea924 equal the pinned digest.

## Answers to the assigned questions

- **Was any refinement a narrowing?** No. The target, field, command and check set size are unchanged. [obs] Under the declared rule the after-value at 7dfea924 is also 0. The one material change, the K01 to K06 reference set, made the check stricter against earlier-round plan prose, but it also raised the base from 3 to 5 and made the round's own measured-outcome sentence the only authority for all six ordinals.
- **Is 5 to 0 earned?** Partly.
  - K24 and K26 are earned: real text repairs, within the 20-line, single-word detector.
  - K10 is earned but transient: the newest table restates the count at the measured revision.
  - K02 and K06 are by construction: the refinement created them at the base, and line 960 clears them. Removing that one line brings back exactly these two mismatches.
  - Measured under the rule as declared, the delta is 3 to 0.
- **What the 0 proves at 7dfea924 (and at tip 7f9f088):**
  - The numeric and presence cells of the round-26 axes table match counts and files at that revision (K07 to K15).
  - The named registry and SHONEN paths exist, and no box is marked complete (K16 to K23).
  - No SHONEN box cites a `corpus/knowledge/*.md` note with the word "superseded" in its first 20 lines (K24 to K27).
  - The six ordinals equal the after-values on line 960, written by the same author in the same commit (K01 to K06). That shows agreement between two author lines. It does not show that an ordinal is deserved, that a dated move occurred, or that the table's "Last change" cells are consistent.
  - The 0 says nothing about any later revision.

## Smallest safe correction

1. Correct `corpus/lessons/round-26.md:101` (append-only) to say that the hand prediction of 3 was correct under the declared rule, and that the 4de2b6b refinement raised the base to 5.
2. Report C2's earned result as 0 of 21 observed-state checks (K07 to K27). Report K01 to K06 as self-agreement with line 960, cleared by a round-authored record, not as calibration repairs. Alternatively, report the delta as 3 to 0 under the declared base rule.
3. For any later check set, outside this round's measurement:
   - Exclude measured-outcome sections authored by the declaring round, or require the reference record to be in a commit earlier than the table.
   - Anchor the heading match to a form like `^#+ Round \d+ measured outcome` instead of a substring.
   - Add a check that each "Last change" cell points at the record K01 to K06 used.

Scope: read=SCORECARD.md round-26 sections and lines 213-960, SHONEN.md at e9f5356c and 7dfea924, corpus/lessons/round-26.md, corpus/lessons/round-25-verifier-spotcheck.md:95-110, .ufo/waves/round-26/measure/c2-*, .ufo/waves/round-26/w1/ScribeMistakes.md, tools/check-self-assessment.py and its diff from b13e991 to 4de2b6b, SKILL.md:1717-1721, cited corpus/knowledge notes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/CritCalibrationClaim.md, /fast/scratch/hyaku/tsuku26/w2/CritCalibrationClaim/ (decl-rule.py, sandbox sb/, pin-*.json, decl*.json, cx{A,B,C}.json); executed=read-only git log/show/diff/ls-tree/check-ignore on the lane, git archive of 7dfea924 into a scratch sandbox with git init and sandbox-only commits and resets, python3 tools/check-self-assessment.py --revision at e9f5356c, 7dfea924 and 7f9f088 (exit 1, 0, 0), python3 decl-rule.py at e9f5356c and 7dfea924 (exit 1 with 3, exit 0), sandbox counterexamples A, B and C (exit 0, 1, 0), jq, grep, sed
Model: not exposed
Installs: none
