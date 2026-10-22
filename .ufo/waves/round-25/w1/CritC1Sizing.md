Verdict: C1 has the right shape for a calibration claim, but as declared it can be satisfied by construction. Six of its 23 checks are circular. One check certifies a wrong ordinal at the base, and four check groups depend on rules nobody has written down. Every defect below can be fixed with an appended refinement that keeps the target at "0 of 23 mismatch, exit 0".

Seat: TsukuroiR25.CritC1Sizing (first C1 falsifier, wave 1). Read at lane HEAD `6c580b155840c8750a7bb5f14dcb8e48913d0073` and at claim base `b9046016831237cd04d38da11ba76e50d5380c53`. `tools/check-self-assessment.py` does not exist at either revision (`git cat-file -e 6c580b15:tools/check-self-assessment.py` exits 128). Every base value below is therefore my own measurement of the declared check text, not output from the tool.

## Answers to the six questions

- **Is it a calibration claim?** [obs] In form, yes. The hyaku sizing rule (`/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-25.md:346-347`) requires a count of mismatches between SCORECARD or SHONEN and observed repository state. AXES.md calibration (`/home/vgpnk/Projects/shokunin/AXES.md:15`) asks that "SHONEN.md/SCORECARD entries match observed repo state". K07 to K23 compare self-assessment with repository bytes. K01 to K06 do not: they compare one self-authored record with another self-authored record (attack 1). As declared, 17 of the 23 checks are calibration checks.
- **Which checks are circular?** [obs] K01 to K06 are fully circular. At HEAD, K01 (depth) and K05 (calibration) even read the round-25 declaration's own rows, `SCORECARD.md:792-793` (attack 1). K23 is partly circular, because the lane names its own "non-author verifier" (attack 8). The case-count part of K17 is the same fact as K13 (attack 11).
- **Can the after-value be reached by construction or by omission?** Yes, through K01 to K06 (attack 2), K14 (attack 6), K16 to K23 (attack 7), unchecked facts (attack 9) and the "last table" location rule (attack 10).
- **Does the rule that an unstated fact counts as a mismatch close the omission hole?** Only for the nine named numeric or statement facts in K07 to K15. It does not cover path lists (K16 to K23 pass vacuously when a row names no path), deleted rows, or any fact the table states that no check reads (attacks 7 and 9).
- **Is any check undecidable from committed bytes?** K13 needs code to be executed, and that code writes to `/tmp` (attack 5). The answers to K12, K14 and K15 depend on how prose polarity is parsed (attack 6). K16 to K23 depend on how paths are tokenized (attack 7). K23 depends on what "named non-author verifier" means (attack 8). K01 to K06 depend on an unspecified transition grammar (attack 1).
- **What hardening keeps the target unchanged?** One appended "Round 25 C1 refinements" block, following the round-24 precedent at `SCORECARD.md:755` ("appended 2026-10-22; targets unchanged"). Its contents are the "Fix" lines below. The check count stays 23, the target stays 0 with exit 0, and the claim is not narrowed.

## Numbered attacks

1. **K04 certifies a wrong freshness ordinal at the base, and K01 to K06 read the claim's own declaration.**
   - [obs] I applied the declared rule ("after-value of the last ordinal transition `<axis> N → M` … on any SCORECARD line outside that table") using the regex `\b(axis) ?\(?N\)? ?(→|->) ?M` over `git show <rev>:SCORECARD.md`. At `b9046016` the last freshness transition is `SCORECARD.md:749`, the round-24 C2 declaration `freshness 8 → 8 (tied lowest)`, which gives freshness = 8. The lane itself retracted that value at `SCORECARD.md:759` ("Freshness was 9 at the base, not 8"), and the round-25 declaration states "freshness 9" at `SCORECARD.md:786`.
   - [obs] As a result, the stale round-11 row `| freshness | 8 |` at `SCORECARD.md:50` passes K04 at the base. A corrected table that says 9 fails K04 unless someone adds a new `freshness … → 9` line.
   - [obs] At `6c580b15` the last depth and calibration transitions are `SCORECARD.md:793` and `:792`, the C2 and C1 rows of this declaration. The check is reading the claim it is supposed to verify.
   - [obs] The last adjacency transition is a declaration row, `SCORECARD.md:620` (round 20, `adjacency 8→8`), not a measured outcome.
   - Impacted axes: calibration (a false pass, and a forced manufactured record).
   - **Fix:** Count a transition only if it sits under a heading that matches `measured outcome` or `post-review claim corrections`. Declaration and refinement rows are plans, not records. I re-ran the same parser under that rule. At both revisions it gives depth 8 (`:730`), coverage 9 (`:224`), operability 9 (`:731`), freshness 9 (`:240`), calibration 9 (`:771`) and adjacency 8 (`:213`), exactly the base ordinals the lane declared at `:786`. Also pin the grammar as `\b(depth|coverage|operability|freshness|calibration|adjacency) ?([0-9]+) ?(?:→|->) ?([0-9]+)`, with "last" meaning the highest line number and the rightmost match on a line.

2. **K01 to K06 can be satisfied by construction, including an ordinal self-grant.**
   - [inf] The L1 writes both the new axes table and every SCORECARD transition line. Counterexample: append a measured-outcome sentence that says `calibration 9 → 10` and put 10 in the table. K05 passes, and the total can still be 0 of 23. That is exactly the overreach AXES calibration is meant to catch, and it would breach the declaration's own "No … ordinal change" (`SCORECARD.md:799`) without the checker noticing.
   - [obs] The declaration admits the circularity itself (`SCORECARD.md:795`: "The ordinal checks test agreement with the lane's own later move records, not an outside judgment").
   - Impacted axes: calibration (false provenance; the lane would be both author and judge).
   - **Fix:** Keep the check count, but add an outside bound. For every transition counted under attack 1, if the round's `corpus/lessons/round-N-verifier-spotcheck.md` exists at `<REV>`, its per-axis verdict for that axis must be `improved` whenever M > N, and otherwise M ≤ N. This applies, for example, to `round-24-verifier-spotcheck.md:52-61`, where all six axes are `unchanged`. If no spot-check exists for that round, M must equal N. A transition that breaks this bound makes the matching K a mismatch. In the report, label K01 to K06 as record-consistency checks and K07 to K23 as repository-state checks, so the 0 is not presented as 23 outside agreements.

3. **The before-value is not preregistered, and the hand count cannot be reproduced without the missing rules.**
   - [obs] The before cell reads "the number the tool reports at `b9046016` (hand count by the L1 predicts 12 of 23)" (`SCORECARD.md:792`). The tool will be written after this declaration, so the author of the tool also sets the before-value.
   - [obs] My per-check measurement at the base under the declared rules, with ✗ meaning mismatch:
     - K01 ✓, K02 ✗ (8 against 9), K03 ✓, K04 ✓ (falsely, see attack 1), K05 ✓, K06 ✗ (7 against 8).
     - K07 ✗ (24 against 46, from `git ls-tree`).
     - K08 ✗ (1631 against 2301, from `git show b9046016:SKILL.md | wc -l`).
     - K09 ✗ (55 against 259, from `grep -c '^[|]'`).
     - K10 ✗ (0 against 25).
     - K11 ✗ (20 against 231).
     - K12 ✗ (the row says "not landed", but `PROVINCE.md` has `## Core` at line 6, `## Adjacent — …` at 35 and `## Frontier` at 75).
     - K13 ✗ (80 against 97; [inf] taken from `.ufo/waves/round-24/w1/ExecCensusLive/selftest.out:100`, recorded after the last census change `70fede2`).
     - K14 ✓ (the string `--identity` is absent and the row says "not landed").
     - K15 ✗ (the row says "no formal overlap table", but `PROVINCE.md:44` starts `| ID | Finding / boundary trigger |`).
     - K16 ✓, K17 ✗, K18 depends on tokenization (attack 7), K19 ✓, K20 to K23 ✓.
   - [inf] The total is 11 if brace paths are expanded and 12 if they are read literally. The L1's 12 probably assumes the literal reading. Under the attack-1 rule, K04 also becomes ✗, giving 12 or 13.
   - Impacted axes: calibration (an unpinned baseline).
   - **Fix:** Commit the 23-entry base vector now, as one line per K with its observed value, under `.ufo/waves/round-25/measure/`. Require the tool's `--revision b9046016` output to reproduce it. Any difference must be explained in `corpus/lessons/round-25.md` before the after-measurement. The target is unchanged.

4. **The claim that C1 and C2 are causally separable is false, so C1 has an ordering hazard.**
   - [obs] `SCORECARD.md:788` says "C1 reads only SCORECARD.md, SHONEN.md and repository state". But C2 writes `corpus/knowledge/memory-pressure-r25.md`, which moves K07, and a SKILL.md decision-table row, which moves K08 and K09 (`SCORECARD.md:797`). The required `corpus/lessons/round-25.md` moves K10. [inf] A corpus README row for the new entry would move K11.
   - [inf] The hyaku closure later adds `corpus/lessons/round-25-verifier-spotcheck.md`, which makes K10 mismatch at the lane tip even if it matched at `<REV>`.
   - Impacted axes: calibration (the result drifts depending on which revision is measured), plus the duplicate-authority question of which revision counts.
   - **Fix:** State that `<REV>` for C1 is the single measured production revision. It must contain every C2 output and the round-25 lesson, and the verifier re-derives at `<REV>`, not at the tip. Drop the word "only" from `:788`, or replace the sentence with "C1 is measured after C2 lands".

5. **K13 cannot be re-derived from committed bytes, and running it breaks the round's temporary-path contract.**
   - [obs] `tools/tsukuroi-census.sh:1713` runs `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX`, so the location is hardcoded and cannot be redirected. The wave contract allows temporary files only under `/fast/scratch/hyaku/tsukuroi-r25/<Seat>/`. I therefore did not execute it.
   - [obs] K13 also means a non-author has to execute lane code. The round-24 verifier explicitly judged "lane tools not executed" (`corpus/lessons/round-24-verifier-spotcheck.md:34`).
   - [obs] The printed summary counts FAIL cases in its total, and FAIL lines go to standard error (`tools/tsukuroi-census.sh:1802`). A table could therefore state "97 cases" for a failing run.
   - Impacted axes: operability (the harness writes outside allowed paths) and calibration (a fact that only a run can produce).
   - **Fix:** Have K13 read a committed receipt `.ufo/waves/round-25/measure/census-selftest.txt` that records the sha256 of `git show <REV>:tools/tsukuroi-census.sh`. The tool checks that digest, parses the `TSUKUROI_CENSUS_SELFTEST:` summary, and requires it to say `PASS` with passed equal to cases. A missing receipt, a digest mismatch or a non-PASS summary counts as a mismatch. Execution becomes optional confirmation, not part of the count.

6. **K12, K14 and K15 depend on parsing prose polarity, and K14 can be satisfied by construction.**
   - [obs] The stale row says "Ceiling: `PROVINCE.md` Core/Frontier/Adjacent not landed" (`SCORECARD.md:48`) and "Ceiling: D12 `--identity` not landed" (`:49`). Deciding whether a row asserts presence or absence requires interpreting free text.
   - [obs] K14 tests whether `tools/tsukuroi-census.sh` "contains `--identity`". A comment such as `# --identity not implemented` makes that true without any mode existing.
   - [obs] K15's prefix `| ID | Finding` happens to match `PROVINCE.md:44`, whose header continues `/ boundary trigger`. That prefix rule is not stated in the declaration.
   - [obs] K12 does not say whether `## Adjacent — finding-to-owner handoffs` counts as the Adjacent heading.
   - [obs] K14 passes at the base only because nothing changed.
   - Impacted axes: calibration (the checks cannot be decided mechanically).
   - **Fix:** Require each of these three facts as a fixed token in its row: `PROVINCE-sections: present|absent`, `identity-mode: present|absent` and `overlap-table: present|absent`. A missing token counts as a mismatch. Define the observations as follows:
     - K12: `^## Core\b`, `^## Frontier\b` and `^## Adjacent\b` each match at least one line.
     - K14: a case arm matching `^\s*--identity\)` exists in the argument parser, not just any substring.
     - K15: a line starts with `| ID | Finding`.

7. **K16 to K23 depend on how paths are tokenized, and they pass vacuously when a row names no path.**
   - [obs] At the base:
     - The host-census-gate row names bare `after.md` and `scout-live.md` after a full `.ufo/evidence/round-1-kaika/` path (`SCORECARD.md:162`). Both bare names are missing at the repository root.
     - The root-metadata-observer row names `.ufo/waves/round-12/resumed/{after,selftest-after,mode-policy-mutant}.json` (`:163`). It is missing if read literally, but all three expanded files exist.
     - The boot-chain-audit row contains `/new_root` (`:164`), which is not a repository path.
   - [obs] Each of these choices flips a check, as shown in attack 3.
   - [obs] "Names only repository paths that exist" is trivially true for a row or box that names no path. The rule about unstated facts does not clearly cover paths. Deleting a Capabilities row is not explicitly a mismatch either.
   - [obs] K20 to K23 pass at the base. SHONEN therefore adds nothing to the move, and the content of each box (for example the SKILL.md claim in box 1, `SHONEN.md:5-6`) is never compared with anything.
   - Impacted axes: calibration (a vacuous pass by omission).
   - **Fix:** Define a path token as a backticked or bare token matching `(\.ufo|corpus|tools|plans|reports)/[^\s`|,;)]+` or one of `SKILL.md|LOG.md|PROVINCE.md|SHONEN.md|SCORECARD.md`. Expand braces. Resolve a bare filename against the directory of the previous full path in the same cell. Ignore tokens that start with `/`.
   - **Fix (continued):** Require at least one path per Capabilities row and per SHONEN box. A missing one of the four named Capabilities rows or four boxes counts as a mismatch of its K.
   - **Fix (continued):** For K20 to K23, also require each box's `[ ]`, `[~]` or `[x]` state to equal the state given by the latest verifier spot-check's SHONEN sentence. `corpus/lessons/round-24-verifier-spotcheck.md:105` says "all four boxes are `[~]`".

8. **K23 says "named non-author verifier", which is undecidable and can be self-certified.**
   - [obs] Any string naming a verifier would satisfy it.
   - [obs] A decidable outside signal already exists. The spot-check files are committed by `protocol-shokunin <protocol@shokunin.local>` (`git log --format='%an <%ae> %h' -- corpus/lessons/round-24-verifier-spotcheck.md` gives `b904601` and `f169b3b`), not by the lane identity `tsukuroi-shokunin`. Each carries an `author: hyaku closure (non-author integrator, …)` line (`corpus/lessons/round-24-verifier-spotcheck.md:3`).
   - [obs] K23 is vacuous today because all four boxes are `[~]` (`SHONEN.md:5,7,9,11`).
   - Impacted axes: calibration (false provenance risk).
   - **Fix:** A `[x]` box must cite a `corpus/lessons/round-*-verifier-spotcheck.md` path that exists at `<REV>`. The commit that added that file must have an author other than `tsukuroi-shokunin`, and its SHONEN sentence must name that box as checked.

9. **Facts the table states but no check reads can stay false while the count reads 0.**
   - [obs] The stale rows state facts no K reads:
     - census `2402 wc -l` and "80 executed cases" in the depth row (`SCORECARD.md:47`)
     - `tools/tsukuroi-census.sh:2377-2382` and `:2392` (`:48`)
     - the README md5 `98bd0066…` (`:48`)
     - `calibration-synthesis.md (463 wc -l)` (`:51`)
     - the selftest rc and passed counts (`:49`)
   - [obs] The table's counting command `grep -c '^\|' SKILL.md` (`:47`) is stored with a markdown escape. Run as stored, GNU BRE treats `\|` as alternation and counts every line: 2301 at the base, not 259.
   - [obs] The capability row states its case count twice, as "80-case" and "PASS 80/80" (`:162`), and K17 does not say which one it reads.
   - [obs] The opening state block (`SCORECARD.md:9-19`) also says notes 24, lessons 0 and 80/80, but it is dated 2026-10-14 and arguably historical.
   - Impacted axes: calibration (overreach through unread claims).
   - **Fix:** Within the existing checks, a row of the new axes table may state no count, line locator, digest or command beyond the K fields for that row. Any extra one counts as a mismatch of that row's first K (K07 for depth, K11 for coverage, K13 for operability). Every numeral attached to "case" in the host-census-gate row must equal K13. Any counting command written in a row must give the K value when run as stored, which means writing `grep -c '^[|]'`.

10. **"The last table under the last heading" can bind the wrong table, and the stale table stays unmarked.**
    - [obs] The rule does not say whether "under" stops at the next `## ` heading. If the round-25 author appends `## Axes — …` and then a measured-outcome section, a tool that searches to the end of the file could bind the outcome table instead.
    - [obs] The round-11 table at `SCORECARD.md:45-52` would remain in place with no superseded marker, so a reader still sees "24 notes".
    - Impacted axes: calibration (two authorities for one fact).
    - **Fix:** Bind the table between the last `^## Axes — ` heading and the next `^#{1,2} ` line. If there is no table in that span, all 15 table checks (K01 to K15) count as mismatches. The new heading text must name the superseded table, for example "supersedes the round-11 table". Apply the same span rule to `## Capabilities`.

11. **Correlated checks and the meaning of exit 0.**
    - [obs] K13 and the case-count part of K17 are one observation, so one stale numeral produces two mismatches. This does not affect the 0 target, but it inflates the size of the before-to-after move.
    - [inf] Nothing in the declaration stops a checker that never flags anything from reporting 0, or from treating a parse failure as 0.
    - Impacted axes: calibration and operability.
    - **Fix:** Exit 0 only when every one of the 23 checks was evaluated and passed. Use exit 1 for one or more mismatches and exit 2 for a check that could not be evaluated, which is never counted as 0. Require `--selftest` with 23 single-fact mutants built from `git archive <REV>`, each of which must raise exactly its own K. Report the K13 and K17 overlap in the outcome instead of double-crediting the move.

## Smallest safe correction

Before any executor writes `tools/check-self-assessment.py`, append a "Round 25 C1 declaration refinements (targets unchanged)" block to SCORECARD.md that carries the fixes in attacks 1, 2, 5, 6, 7, 8, 9, 10 and 11, and commit the base vector from attack 3. Correct the separability sentence as in attack 4. C1 stays "0 of 23 mismatch, exit 0" at one named `<REV>`. Nothing is narrowed, and K01 to K06 become bounded by an outside record instead of resting only on the lane's own statements. This is a fixable defect, not a tradeoff the judge must reject. [inf] Without these fixes, C1 as declared is reachable by construction and would repeat the round-24 sizing rejection in a different form.

Scope: read=SCORECARD.md (header, axes table, Capabilities, round-24 and round-25 sections), SHONEN.md, PROVINCE.md headings, tools/tsukuroi-census.sh selftest region, corpus/lessons/round-24-verifier-spotcheck.md, the round-24 ExecCensusLive receipts, the hyaku round-25 prompt lines 320-350, AXES.md calibration row, round-25 measure and w1 spec; wrote=.ufo/waves/round-25/w1/CritC1Sizing.md; executed=read-only `git rev-parse`, `git log`, `git status --porcelain`, `git ls-tree`, `git show`, `git cat-file -e`, `git diff --name-status` in the lane repo, plus `grep -c`, `wc -l` and `sha256sum` on `git show` output, a read-only python3 parser over `git show <rev>:SCORECARD.md` on stdin, `git ls-files` (read-only) at the fleet root, and `mkdir -p /fast/scratch/hyaku/tsukuroi-r25/CritC1Sizing` (empty; census selftest not executed because it writes to /tmp)
Model: cursor/default (Auto); underlying model identity not exposed
Installs: none
