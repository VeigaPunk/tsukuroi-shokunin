# C1 planner data walk — independent hand oracle for K01 to K23

Verdict: at `b9046016831237cd04d38da11ba76e50d5380c53` the lane's self-assessment mismatches observed repository state on 12 of the 23 fixed checks, and matches on 11; this equals the 12 of 23 the round 25 declaration predicts.

## Findings

1. [obs] The current axes table is the only table under the only heading that starts `## Axes — `. The heading is at `/fast/scratch/hyaku/tsukuroi-r25/ScoutPlanWalk/base/SCORECARD.md:39`, the header at `:45` and the six rows at `:47` to `:52`. Command: `grep -c '^## Axes — ' SCORECARD.md` returned 1.

2. [obs] The last `## Capabilities` heading is at `SCORECARD.md:157`, and its only table has its header at `:159` with the four rows at `:161` to `:164`. Command: `grep -c '^## Capabilities' SCORECARD.md` returned 1.

3. [obs] The base bytes are reproducible from the revision. I extracted the whole tree with `git archive b9046016 | tar -x -C /fast/scratch/hyaku/tsukuroi-r25/ScoutPlanWalk/base`, exit 0, and every count below was taken from that extraction. The working tree differs from the base only by 19 inserted lines at the end of `SCORECARD.md` (`git diff --stat b9046016 -- SCORECARD.md SHONEN.md` shows `SCORECARD.md | 19 +++++++++++++++++++` and no `SHONEN.md` entry), so lines 1 to 782 of `SCORECARD.md` and all of `SHONEN.md` are identical between the base and the working tree.

4. [obs] The six ordinal checks were read by hand from the claim and move tables. Counting rule used: a transition is an ordinal written `N → M` in the row that names the axis, either in the same cell as the axis name or in the ordinal cell immediately after it; the transition with the greatest base line number wins; the axes table lines 45 to 52 are excluded. Command used to enumerate candidates: `grep -nE '<axis>[^|]{0,24}[0-9]+[[:space:]]*→[[:space:]]*[0-9]+' SCORECARD.md`, then each hit read in context.

5. [obs] Observed ordinals: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. The base also states all six in one prose line: `SCORECARD.md:481` reads `Ordinal depth8→8 (0); retained coverage9/operability9/freshness9/calibration9/adjacency8`. This agrees with the ordinals the round 25 declaration names at its line 786.

6. [obs] Baseline selftest. `bash tools/tsukuroi-census.sh --selftest` inside the extracted base tree exited 0 and printed `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)`. Two of the printed lines are `SKIP` (the two CAP_CHOWN root-arm fixtures); the summary counts 97 cases, and the check reads the printed case count.

7. [obs] All repository paths named by the four Capabilities rows and the four SHONEN boxes exist at the base revision. Command: `git cat-file -e b9046016:<path>` for each of 18 paths, all `EXISTS`, no `MISSING`. The tracked tree contains 3119 paths under `.ufo/`.

8. [obs] No SHONEN box is `[x]`; all four are `[~]`. Command: `grep -c '^- \[x\]' SHONEN.md` returned 0 and `grep -c '^- \[' SHONEN.md` returned 4. The second half of K20 to K23 (no tick without a named non-author verifier) therefore holds trivially; the path half is what those checks actually test here.

## Check table

Stated values are quoted from the base bytes; line numbers are base line numbers. Observed values were produced with the listed read-only command.

| Check | Stated value (base line) | Observed value at `b9046016` | Read-only command | Verdict |
|---|---|---|---|---|
| K01 depth score | 8 (`SCORECARD.md:47`) | 8; last transition `depth 8 → 8` at `:759`, corroborated at `:481` | hand read plus `grep -nE 'depth[^|]{0,24}[0-9]+ *→ *[0-9]+' SCORECARD.md` | match |
| K02 coverage score | 8 (`:48`) | 9; last transition `coverage ... 8 → 9` at `:192`, restated at `:224` | same pattern for `coverage` | mismatch |
| K03 operability score | 9 (`:49`) | 9; last transition `operability9→9` at `:731`; `:255`, `:519` and `:573` also 9 → 9 | same pattern for `operability` | match |
| K04 freshness score | 8 (`:50`) | 9; last transition `freshness (actual 9 → 9)` at `:772`; the `freshness 8 → 8` at `:749` is retracted at `:759` (`Freshness was 9 at the base, not 8`) | same pattern for `freshness` | mismatch |
| K05 calibration score | 9 (`:51`) | 9; last transition `calibration 9 → 9` at `:771` | same pattern for `calibration` | match |
| K06 adjacency score | 7 (`:52`) | 8; last transition `adjacency 8→8` at `:620`, raised `7 → 8` at `:191` and `:213` | same pattern for `adjacency` | mismatch |
| K07 depth row note count | 24 notes (`:47`) | 46 | `ls corpus/knowledge/*.md \| wc -l` in the extraction; confirmed by `git ls-tree b9046016 corpus/knowledge/ \| grep -c '\.md$'` = 46 | mismatch |
| K08 depth row SKILL.md line count | 1631 (`:47`) | 2301 | `wc -l < SKILL.md` | mismatch |
| K09 depth row table lines | 55 (`:47`) | 259 | `grep -c '^|' SKILL.md` | mismatch |
| K10 depth row corpus/lessons count | 0 files (`:47`) | 25 | `find corpus/lessons -type f \| wc -l`; confirmed by `git ls-tree -r b9046016 corpus/lessons/ \| wc -l` = 25 | mismatch |
| K11 coverage row corpus/README.md line count | 20 (`:48`) | 231 | `wc -l < corpus/README.md` | mismatch |
| K12 coverage row PROVINCE.md Core, Frontier, Adjacent statement | `PROVINCE.md` Core/Frontier/Adjacent not landed (`:48`) | all three headings exist: `## Core` at `PROVINCE.md:6`, `## Adjacent — finding-to-owner handoffs` at `:35`, `## Frontier` at `:75`, `## Adjacent — portable ownership anchors (round 19)` at `:108` | `grep -nE '^#{1,4} .*(Core\|Frontier\|Adjacent)' PROVINCE.md` | mismatch |
| K13 operability row selftest case count | 80 cases (`:49`) | 97 cases, exit 0 | `bash tools/tsukuroi-census.sh --selftest` on the extraction, printed `PASS (97 cases, 97 passed, 0 failed)` | mismatch |
| K14 operability row `--identity` statement | D12 `--identity` not landed (`:49`) | the string is absent from `tools/tsukuroi-census.sh` | `grep -c -- '--identity' tools/tsukuroi-census.sh` returned 0 | match |
| K15 adjacency row formal overlap table statement | no formal overlap table (`:52`) | `PROVINCE.md` holds the table header `| ID | Finding / boundary trigger | Tsukuroi retains | ...` at `:44` | `grep -n '^| ID | Finding' PROVINCE.md`, exit 0 | mismatch |
| K16 sources-registry paths | `corpus/SOURCES.md`, `.ufo/evidence/round-1-kaika/after.md` (`:161`) | both exist at the revision | `git cat-file -e b9046016:<path>` for each | match |
| K17 host-census-gate paths and case count | `tools/tsukuroi-census.sh`, `.ufo/evidence/round-1-kaika/scout-live.md`, `.ufo/evidence/round-1-kaika/after.md`, stated `80-case` and `PASS 80/80` (`:162`) | all three paths exist; case count is 97, not 80 | `git cat-file -e` for each path; selftest as in K13 | mismatch |
| K18 root-metadata-observer paths | `.ufo/waves/round-12/resumed/after.json`, `selftest-after.json`, `mode-policy-mutant.json` (`:163`) | all three exist at the revision | `git cat-file -e` for each | match |
| K19 boot-chain-audit paths | `tools/boot-chain-audit.sh`, `.ufo/waves/round-17/l1-capture/audit-live.txt` (`:164`) | both exist at the revision | `git cat-file -e` for each | match |
| K20 SHONEN box 1 | `SKILL.md`, `corpus/knowledge/root-dac-decision-r12.md`; box is `[~]` | both exist; no `[x]` | `git cat-file -e` for each; `grep -c '^- \[x\]' SHONEN.md` = 0 | match |
| K21 SHONEN box 2 | `corpus/knowledge/host-health-report-r3.md`, `LOG.md`, `corpus/knowledge/adjacency-handoffs-fleet-r1.md`; box is `[~]` | all three exist; no `[x]` | same as K20 | match |
| K22 SHONEN box 3 | `corpus/knowledge/adjacency-handoffs-fleet-r1.md`, `corpus/knowledge/root-dac-decision-r12.md`, `corpus/knowledge/executor-test-sufficiency.md`; box is `[~]` | all three exist; no `[x]` | same as K20 | match |
| K23 SHONEN box 4 | `PROVINCE.md`, `.ufo/waves/round-12/resumed/OverlapHostR.md`; box is `[~]` | both exist; no `[x]` | same as K20 | match |

## Total

| Measure | Count | Checks |
|---|---|---|
| mismatch | 12 | K02, K04, K06, K07, K08, K09, K10, K11, K12, K13, K15, K17 |
| match | 11 | K01, K03, K05, K14, K16, K18, K19, K20, K21, K22, K23 |
| total | 23 | K01 to K23 |

Any tool implementing the fixed check set and agreeing with this oracle must report `mismatches` = 12 at `b9046016` and exit 1 there.

## Parsing sensitivities the comparison should expect

1. [inf] K04 is the one check whose value depends on reading order. The base contains `freshness 8 → 8 (tied lowest)` at `:749` and `freshness (actual 9 → 9)` at `:772`. Line 759 withdraws the first reading in prose (`Freshness was 9 at the base, not 8`), and line 772 is the later transition by line number, so this oracle takes 9. A tool that stops at the first match after the axes table, or that ignores a transition written with the word `actual` inside parentheses, will report 8 and a total of 11. I regard 9 as correct because the rule selects the last recorded transition and line 772 is later than line 749.

2. [inf] K02 and K06 also depend on whether cross-cell rows count. In those rows the axis name sits in one cell and the ordinal in the next (`| A | adjacency | 7 → 8 |` at `:191`; `| C1 | operability / capability ... | 9 → 9 |` at `:255`). Every reading of both axes still yields coverage 9 and adjacency 8, because the same-cell and later rows agree, so only K04 is sensitive.

3. [obs] K12 depends on reading `not landed` as an assertion of absence. The row is the coverage ceiling cell, not a claim about file presence, but the check text makes the test mechanical: the statement must match whether all three headings exist. All three do exist, so the row's `not landed` wording is false under that test.

4. [obs] K15 depends on prefix matching the header. `PROVINCE.md:44` reads `| ID | Finding / boundary trigger | Tsukuroi retains | Next analysis recipient | Minimum handoff evidence | Ownership source |`; it begins with the checked literal `| ID | Finding`, so the check fires.

5. [unk] Whether the round 25 tool treats a brace group such as `{after,selftest-after,mode-policy-mutant}.json` in the root-metadata-observer row as three named paths or as one literal path. I resolved it as three paths, all of which exist, so K18 is a match either way unless the tool requires literal single-path spelling.

6. [unk] The check set does not name a value for the depth row's `2402 wc -l` census figure, so no check tests it. If the tool adds one, it is outside the fixed K01 to K23 set and should be reported separately rather than folded into the count.

7. [inf] Two printed `SKIP` lines in the baseline selftest are counted inside the 97-case summary. If a tool recomputes cases by counting only `PASS` lines it will get 95 and should not be used as the K13 denominator; the check says the case count printed, and the printed summary says 97.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md, SHONEN.md, PROVINCE.md, corpus/README.md, SKILL.md, tools/tsukuroi-census.sh, corpus/knowledge/*.md listing and the git archive of b9046016 (read-only git show, archive, cat-file, ls-tree, diff); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ScoutPlanWalk.md and scratch under /fast/scratch/hyaku/tsukuroi-r25/ScoutPlanWalk/; executed=grep, wc, ls, find, git archive, tar, git cat-file, git ls-tree, git diff, bash tools/tsukuroi-census.sh --selftest
Model: opencode-go/deepseek-v4.1-flash
Installs: none
