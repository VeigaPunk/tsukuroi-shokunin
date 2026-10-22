# CritC1Construction — round 25, falsify wave 2, claim C1

Verdict: partly holds. The count of 0 of 23 at `5e7c04ecb02735491456de2b8bc44550d0db4609` reproduces, and no declaration line or tool rule was loosened after measurement. But the zero is reached by construction: the L1 transcribed the tool's own outputs into the table, and four of the six ordinal checks compare the table against the L1's own plan text, one of them a regex example. The before-value of 13 includes two counts that are not stale self-assessment facts, and the pushed evidence carries two contradictory before-values (12 and 13). The honest statement is "11 distinct stale facts repaired to 0 at one revision", not "calibration 13 → 0".

Seat: TsukuroiR25.CritC1Construction (wave 2). Tool under test: `git show 5e7c04ec:tools/check-self-assessment.py`, blob `eb2778660fc8f295e768f7098048afbe2bfff57b`, sha256 `343367fb…6242f`. It is byte-identical in the commits `4578e53`, `1fbd8be` and `5e7c04e`, and to `.ufo/waves/round-25/w1/ExecSelfAssessTool/check-self-assessment.py`. All mutants ran on `git archive 5e7c04ec` copies in `/fast/scratch/hyaku/tsukuroi-r25/w2/CritC1Construction/sb/<case>` (`git init`, no remote, deleted after each run). Script: `.ufo/waves/round-25/w2/CritC1Construction/mutants.sh` (sha256 `2170885a…1b84`). Outputs: `.ufo/waves/round-25/w2/CritC1Construction/mutants/*.json`.

## Numbered attacks

1. **The 0 of 23 reproduces.** [obs]
   - Mutant M0 (unmodified archive of `5e7c04ec`) gives exit 0, `mismatches` 0. It uses the same ordinal reference lines as the L1's receipt `.ufo/waves/round-25/measure/c1-5e7c04ec.json`: K01 at :793, K04 at :807 and K05 at :792.
   - The before receipt `.ufo/waves/round-25/measure/c1-b9046016.json` lists the 13 ids K02, K04, K06 to K13, K15, K17 and K21. The wave-1 receipt `.ufo/waves/round-25/w1/ExecSelfAssessTool/c1-base-b9046016.json` agrees.
   - Impacted axes: none. This is the part of C1 that holds.

2. **Four of the six ordinal checks compare the table against plan text, one of them a regex example.** [obs]
   - At `5e7c04ec` the references are:
     - K01 depth: `SCORECARD.md:793`, the round-25 declaration's C2 row "depth 8 → 8 (tied lowest)".
     - K05 calibration: `SCORECARD.md:792`, the round-25 declaration's C1 row "calibration 9 → 9".
     - K04 freshness: `SCORECARD.md:807`. This is the refinement bullet's own illustration of the regex, "`freshness (actual 9 → 9` is", not a move record.
     - K06 adjacency: `SCORECARD.md:620`, the round-20 declaration table "adjacency 8→8 (0)".
   - Counterexample M1 edits only that illustration to "`freshness (actual 7 → 7` is". It touches no move record and no table cell, and K04 flips to mismatch (stated 9, observed 7, line 807, exit 1).
   - So K04's "observed" value is set by a syntax example the L1 wrote in commit `0cd9b28`.
   - Wave-1 CritC1Sizing had already flagged this circularity at `6c580b15` (`.ufo/waves/round-25/w1/CritC1Sizing.md:17-22`). Its proposed fix, counting only lines under `measured outcome` or `post-review claim corrections` headings, was not adopted. The refinement at `SCORECARD.md:806` keeps "SCORECARD lines outside the current axes table" and labels the six checks as record agreement instead.
   - Impacted axes: calibration (false provenance; the author is both the stated value and the reference).

3. **Ordinal self-grant passes with 0 of 23.** [obs]
   - Counterexample M2 raises all six axis scores in the round-25 table to 10. It then appends one sentence at the end of SCORECARD.md: "Planned next round: depth 8 → 10, coverage 9 → 10, operability 9 → 10, freshness 9 → 10, calibration 9 → 10, adjacency 8 → 10."
   - Result: exit 0, `mismatches` 0, with every ordinal reference at line 863 (the appended "Planned" line).
   - A one-line plan sentence certifies a six-axis uplift, and C1 does not notice. The same round declares "No … ordinal change" (`SCORECARD.md:799`).
   - Impacted axes: calibration (overreach the axis is meant to catch).
   - This is a design defect of K01 to K06, not an implementation bug: the tool follows the refined text.

4. **The count, token and path checks agree because the L1 typed in the tool's outputs.** [obs]
   - `SCORECARD.md:824` says: "The counts were filled by the L1 at the measured revision with the command named in the same cell."
   - The three state facts were worded to emit the exact fixed tokens the tool greps:
     - "Core, Frontier and Adjacent sections present" (`:829`).
     - "D12 `--identity` not landed" (`:830`).
     - "`PROVINCE.md` carries the formal overlap table present" (`:833`), which is ungrammatical and exists only to contain the K15 literal.
   - The wave-1 tool builder listed these as "Three wording facts the draft must carry" (working-tree `.ufo/waves/round-25/w1/ExecSelfAssessTool.md`, section 4).
   - [inf] For K07 to K23 the zero therefore measures whether the transcription is fresh at one revision. It does not measure calibration judgement. Any later commit that adds a knowledge note or lesson file breaks K07 or K10 again.
   - Impacted axes: calibration (sizing). The repair of a stale table is real; calling it a calibration gain is not supported by this instrument.

5. **Facts outside the 23 checks can be false while the count stays 0.**
   - [obs] Counterexample M3 changes four statements and still scores exit 0, `mismatches` 0:
     - `## Frontier` at `PROVINCE.md:75` becomes `PROVINCE.md:999`.
     - The depth row's `SCORECARD.md:30` becomes `SCORECARD.md:1`.
     - "125 rows at round 25" becomes "999 rows at round 25".
     - The boot-chain-audit claim "its selftest prints PASS total=45 failed=0" becomes "FAIL total=45 failed=45".
   - [obs] One counting command is wrong as stored. The depth row gives 297 with the command `grep -c '^\|' SKILL.md` (`SCORECARD.md:828`). Run byte-for-byte on `git show 5e7c04ec:SKILL.md`, it prints 2355, because GNU BRE reads `\|` as alternation. Only the rendered `grep -c '^|'` prints 297.
   - The table's own preamble says "each evidence pointer carries the command that re-derives the number it quotes" (`:821-822`). CritC1Sizing attack 9 raised this exact defect and its fix (`'^[|]'`); it was not applied.
   - [obs] K13 parses only `\((\d+) cases` (`tools/check-self-assessment.py:148`). It never checks PASS, the passed count or the exit code, so a failing 97-case selftest still matches the row's "prints PASS (97 cases, 97 passed, 0 failed) with exit 0". CritC1Sizing attack 5 proposed requiring PASS; this was not adopted.
   - Impacted axes: calibration (unread claims carry no check).

6. **The before-value 13 is honestly reproduced, but 2 of the 13 are not stale self-assessment facts.**
   - [obs] K21 at `b9046016` fails only on the prose token `observation/request` (`c1-b9046016.json`, K21). Mutant M5 restores that slash in SHONEN.md at `5e7c04ec`, and K21 alone comes back (exit 1, 1 mismatch).
   - The SHONEN box was never miscalibrated. The token is a grammar artifact, and the round "repaired" it by rewording the measured file (`git diff b9046016 5e7c04e -- SHONEN.md`, one phrase).
   - [obs] K17 at the base repeats the 80-versus-97 fact that K13 already counts. Its path part names `HEALTHY/DEGRADED/BLOCKED`, another prose artifact, and the bare `after.md`.
   - [inf] The distinct stale facts at the base are 11:
     - K02, K04 and K06 (ordinals).
     - K07 to K11 (counts).
     - K12, K13 and K15 (state facts).
   - That is CritC1Sizing's 11 (`CritC1Sizing.md:44`). The 13 → 0 move overstates the repair by 2, one double count and one artifact.
   - [obs] The L1's 12 was not independently confirmed. The first tool build added a prose-token filter that the declared grammar does not have. The committed tool-builder report says so: "I chose the reading that reproduces the declared 12" (`git show 5e7c04ec:.ufo/waves/round-25/w1/ExecSelfAssessTool.md`, line 122).
   - That build's 12 was re-run and committed as `.ufo/waves/round-25/w1/DraftLessonMistakes/checker-red-before-b9046016.json` (12, no K21) and quoted in `DraftLessonMistakes.md:46`.
   - The later literal-grammar build gives 13. The direction of that change was stricter, toward the declaration, not looser.
   - Impacted axes: calibration (size of the move).

7. **The pushed evidence contradicts itself on the before-value and the tool identity.** [obs]
   - At `5e7c04ec`, the committed `.ufo/waves/round-25/w1/ExecSelfAssessTool.md` says:
     - "12 of 23 mismatches at both `b9046016` and `6c580b15`" (line 3).
     - Tool sha256 `970e3efb…4a33` (line 7).
     - A receipt `c1-decl-6c580b15.json` (line 30).
   - The same commit contains:
     - The tool with sha256 `343367fb…6242f`.
     - `c1-decl-0cd9b28.json`, not `c1-decl-6c580b15.json` (`git ls-tree 5e7c04ec .ufo/waves/round-25/w1/ExecSelfAssessTool/`).
     - Receipts that say 13.
   - The corrected report saying 13 exists only as an uncommitted working-tree edit: `git diff 5e7c04ec --stat` shows 15 wave-1 files modified after the commit, among them `ExecSelfAssessTool.md` (+67/−…) and `DraftAxesTable.md`.
   - That report also records that the 6c580b15 receipt "was removed rather than left stale".
   - `LOG.md:1215` at `5e7c04ec` points to a SCORECARD section "Round 25 measured outcome", which does not exist at that revision. The last `##` heading is `## Capabilities — current (round 25)` at `SCORECARD.md:840`.
   - The lesson `corpus/lessons/round-25.md` states no C1 before or after number.
   - Impacted axes: calibration (duplicate authorities for one number), freshness (the committed narrative is stale against the committed receipts).

8. **Were rules loosened after measurement? No declaration text was; the tool has three small deviations, none used to reach 0.** [obs]
   - `git diff 6c580b1 0cd9b28 -- SCORECARD.md` and `git diff 0cd9b28 5e7c04e -- SCORECARD.md` contain no removed lines. Both the declaration and the refinements are append-only.
   - The tool deviates from the committed text in three places:
     - **(a) Ordinal regex boundary.** The refinement pins `\b<axis>\b`; the tool uses `\b<axis>(?![A-Za-z])` (`tools/check-self-assessment.py:391`). On "A note on depth_5 → 5 naming." the declared regex finds nothing and the tool finds (5, 5). Mutant M4 appends that line and K01 flips to mismatch (observed 5, line 863). The deviation is wider than declared; at `5e7c04ec` it changes no result.
     - **(b) Table choice.** The declaration says "the last table under the last heading". `pick_table` (`:216-224`) prefers the last table whose first header cell is `Axis` or `Capability`, then falls back. There is no effect at `5e7c04ec`, where each section has one table.
     - **(c) Contradictory tokens.** If a row contains both the absent and the present token, the absent token wins silently (`:506-511`, `:532-537`, `:546-551`). Mutant M6 writes "`--identity` not landed and `--identity` landed" in the operability row and gets exit 0, 0 mismatches. The declaration does not define precedence; a contradictory row should be a mismatch.
   - K08 and K10 also fall back to looser patterns than the declared tokens (`:466-469`, `:484-486`). Both are unused at `5e7c04ec`, where the declared forms are present.
   - The refinement says it "was fixed before either tool was run on a round-25 revision" (`SCORECARD.md:805`). LOG line 1211 says refined "before any measurement". [unk] The first build was run on `6c580b15` (committed report, line 19-21), but its receipt was deleted and the run time is not recorded, so ordering against `0cd9b28` (07:27:19 -0300) cannot be decided from committed bytes.
   - Impacted axes: calibration (instrument fidelity), all minor.

9. **The selftest is too thin to back "implements exactly".** [obs]
   - `--selftest` has 7 cases (`tools/check-self-assessment.py:791-792`, `.ufo/waves/round-25/measure/c1-selftest.txt`). They exercise K02, K07, K12, K16, K20 and one exit-2 path.
   - The other 18 checks have no mutant, so none of the deviations in attack 8 can be detected by the selftest. CritC1Sizing attack 11 asked for 23 single-fact mutants.
   - Impacted axes: operability and calibration (unverified instrument).

## Impacted axes

- Calibration: attacks 2 to 7, 8 and 9.
- Freshness: attack 7, through the stale committed narrative.
- Operability: attack 9.
- No ordinal moved; C1 declared none.

## Fixable defect or tradeoff

- The stale-table repair is real and reproducible.
- The defects in attacks 5, 7, 8 and 9 are fixable without changing the target.
- Attacks 2 to 4 are design properties of the declared check set. As committed, K01 to K06 cannot distinguish a record from a plan, and K07 to K23 can be met by transcription. The canonical judge should therefore reject C1 as evidence of a calibration improvement beyond "the stale round-11 self-assessment was replaced by one that agrees with repository state at `5e7c04ec` on 17 transcribed facts".
- The judge should also reject the move size 13 → 0.

## Smallest safe correction

Do not move the target.

1. In the round-25 measured outcome, report C1 as 11 distinct stale facts → 0. Name K21 as a grammar artifact removed by rewording SHONEN.md, and K17's count as a double count of K13.
2. Label K01 to K06 "record agreement against plan text (lines 620, 792, 793, 807)", not repository-state checks, and claim no calibration credit from them.
3. Commit the updated wave-1 reports, or append a correction naming the 12-versus-13 history and the deleted `c1-decl-6c580b15.json`. Fix the LOG pointer to the missing "Round 25 measured outcome" section, or add that section.
4. Store the depth-row command as `grep -c '^[|]' SKILL.md`.
5. Optionally, for the next round:
   - Scope ordinal references to measured-outcome and post-review headings.
   - Make contradictory tokens a mismatch.
   - Match the declared `\b`.
   - Require PASS in K13.
   - Add one mutant per K.

Scope: read=SCORECARD.md (lines 740-861 and pointer lines 30, 36, 37, 213, 224, 240, 614-622 at 5e7c04ec), SHONEN.md, tools/check-self-assessment.py, PROVINCE.md headings, SKILL.md (via git show), corpus/SOURCES.md row count, LOG.md lines 1157-1216, corpus/lessons/round-25.md, corpus/QUALITY.md item 57, .ufo/waves/round-25/measure/{exits.txt,c1-b9046016.json,c1-5e7c04ec.json,c1-selftest.txt}, .ufo/waves/round-25/w1/{CritC1Sizing.md,ExecSelfAssessTool.md (committed and working tree),ExecSelfAssessTool/*.json,DraftLessonMistakes.md,DraftLessonMistakes/{red-before.txt,checker-red-before-b9046016.json},DraftAxesTable.md,RevOrdinals.md,w1-spec.json}, file mtimes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/CritC1Construction.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/CritC1Construction/mutants.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/CritC1Construction/mutants/M0-unmodified.json … M6-contradicting-tokens.json, /fast/scratch/hyaku/tsukuroi-r25/w2/CritC1Construction/{mutants.sh,tool/check-self-assessment.py,out/*.json}; executed=read-only git (log, show, diff, ls-tree, rev-parse, hash-object, status, archive) on the lane, git init/add/commit only inside private scratch sandboxes, bash mutants.sh (seven runs of python3 check-self-assessment.py --revision HEAD --repo <sandbox>, each running the census selftest in a temporary directory; exit codes 0,1,0,0,1,1,0), grep -c on git show output, sha256sum, stat, a python3 regex comparison
Model: not exposed (Cursor Auto)
Installs: none
