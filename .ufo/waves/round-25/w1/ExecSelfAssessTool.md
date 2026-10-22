# ExecSelfAssessTool — round 25, wave 1, C1 build

Verdict: the C1 checker is built and measured under the L1's fixed path grammar; it reports 13 of 23 mismatches at the claim base `b9046016` and at `0cd9b28`, and at the integrated revision `5e7c04e` it reports **0 of 23 with exit 0**, which is the declared after-value; the hermetic selftest passes 7 of 7 cases.

## 1. What was built

`tools/check-self-assessment.py`, 882 lines, in my clone at `/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py`. A byte-identical copy (sha256 `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`) is placed at `.ufo/waves/round-25/w1/ExecSelfAssessTool/check-self-assessment.py` in the lane so the L1 can integrate it without reaching into my scratch clone. I did not write into any lane production file.

It implements exactly the C1 check set K01 to K23 fixed in the round-25 declaration, on the contract the L1 fixed over the wave: `--revision <REV>` reads SCORECARD.md, SHONEN.md, PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge, corpus/lessons and tools/tsukuroi-census.sh only through `git show` and `git ls-tree` at `REV`, never the working tree; `--repo <path>` defaults to the repository containing the script. K13 runs `bash tools/tsukuroi-census.sh --selftest` inside a temporary directory populated by `git archive REV` and parses `(N cases`.

Output is one JSON object on stdout: `revision`, `checks` (23 records with `id`, `subject`, `stated`, `observed`, `status` of `match` or `mismatch`, `reason`, and the `stated_line` the value was read from; K01 to K06 also carry `observed_line`), `mismatches`, `checked` (23), `status` of `PASS` or `FAIL`, plus `repo` and `requested_revision`. Exit 0 when `mismatches` is 0, exit 1 when it is above 0, exit 2 when the check set cannot be evaluated.

Git is read with a cleaned environment: every `GIT_*` variable is dropped, `GIT_NO_REPLACE_OBJECTS=1` and `GIT_CONFIG_NOSYSTEM=1` are set, and `--no-replace-objects`, `core.attributesFile=/dev/null` and `core.excludesFile=/dev/null` are passed, so no worktree attribute can influence a read.

## 2. Measured results

| revision | command | exit | status | mismatches |
|---|---|---|---|---|
| `b9046016831237cd04d38da11ba76e50d5380c53` | `python3 tools/check-self-assessment.py --revision b9046016 --repo <lane>` | 1 | FAIL | 13 of 23 |
| `0cd9b28bee5fd5a50d991e6dee0c0d0f48b15935` | `python3 tools/check-self-assessment.py --revision 0cd9b28 --repo <lane>` | 1 | FAIL | 13 of 23 |
| `5e7c04ecb02735491456de2b8bc44550d0db4609` (integrated) | `python3 tools/check-self-assessment.py --revision 5e7c04e` | 0 | PASS | **0 of 23** |
| hermetic fixtures | `python3 tools/check-self-assessment.py --selftest` | 0 | PASS | 7 cases, 0 failures |

The mismatching check ids are the same thirteen at both revisions: K02, K04, K06, K07, K08, K09, K10, K11, K12, K13, K15, K17, K21. The L1's hand count for the base predicted 12 of 23 before the path grammar was fixed; with the declared grammar applied literally the count is 13, because K21 gains the prose token `observation/request` and K17 names two absent paths. The L1 confirmed 13 as the expected literal-grammar count.

One evidence difference between the two revisions: K04's last recorded freshness transition moves from `SCORECARD.md:772` to `SCORECARD.md:807`, because the refined declaration added a later freshness transition. The stale table still states 8 against the recorded 9.

Saved outputs, under `.ufo/waves/round-25/w1/ExecSelfAssessTool/`:

| file | sha256 |
|---|---|
| `c1-base-b9046016.json` | `0bcb96a276dfa6b26b0c49fc8d809acdced3801a5889f4a1509ce98c25429d2e` |
| `c1-decl-0cd9b28.json` | `e528d71b82bb65d89a78fb45ab6b57d74710f64077be96d26617d686cb8552bf` |
| `c1-after-5e7c04e.json` | `9ca76e796957c1c12e855afd397d5b2ada2ae967950a0c19006c7b1d496e6cfb` |
| `selftest.json` | `dd1a760c08c618c26a69ab687f86db7736c01c03bb6890a3b6186bd3461f9f11` |
| `check-self-assessment.py` | `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f` |

The earlier `c1-decl-6c580b15.json` receipt was removed rather than left stale beside the current one; it can be regenerated on request.

## 3. Per-check before table, at `b9046016`

Stated values come from the lane's own rows; observed values are measured at the revision. The stated line is the SCORECARD.md or SHONEN.md line the stated value was read from; the observed line, where present, is the SCORECARD.md line of the last recorded ordinal transition.

| id | subject | stated | observed | status | stated line | observed line | reason |
|---|---|---|---|---|---|---|---|
| K01 | depth score equals the after-value of the last recorded depth ordinal transition | 8 | 8 | match | 47 | 759 | axes table depth score 8 equals the after-value 8 of the last recorded transition (SCORECARD.md:759) |
| K02 | coverage score equals the after-value of the last recorded coverage ordinal transition | 8 | 9 | mismatch | 48 | 224 | axes table coverage score 8 differs from the after-value 9 of the last recorded transition (SCORECARD.md:224) |
| K03 | operability score equals the after-value of the last recorded operability ordinal transition | 9 | 9 | match | 49 | 731 | axes table operability score 9 equals the after-value 9 of the last recorded transition (SCORECARD.md:731) |
| K04 | freshness score equals the after-value of the last recorded freshness ordinal transition | 8 | 9 | mismatch | 50 | 772 | axes table freshness score 8 differs from the after-value 9 of the last recorded transition (SCORECARD.md:772) |
| K05 | calibration score equals the after-value of the last recorded calibration ordinal transition | 9 | 9 | match | 51 | 771 | axes table calibration score 9 equals the after-value 9 of the last recorded transition (SCORECARD.md:771) |
| K06 | adjacency score equals the after-value of the last recorded adjacency ordinal transition | 7 | 8 | mismatch | 52 | 620 | axes table adjacency score 7 differs from the after-value 8 of the last recorded transition (SCORECARD.md:620) |
| K07 | depth row note count equals the corpus/knowledge/*.md count at the revision | 24 | 46 | mismatch | 47 | - | depth row states 24 notes; corpus/knowledge holds 46 .md files |
| K08 | depth row SKILL.md line count equals the line count of SKILL.md | 1631 | 2301 | mismatch | 47 | - | depth row states 1631 SKILL.md lines; SKILL.md holds 2301 newline characters |
| K09 | depth row table-line count equals the pipe-prefixed line count of SKILL.md | 55 | 259 | mismatch | 47 | - | depth row states 55 table lines; SKILL.md holds 259 pipe-prefixed lines |
| K10 | depth row corpus/lessons file count equals the file count under corpus/lessons/ | 0 | 25 | mismatch | 47 | - | depth row states 0 lesson files; corpus/lessons holds 25 files |
| K11 | coverage row corpus/README.md line count equals the line count of corpus/README.md | 20 | 231 | mismatch | 48 | - | coverage row states 20 corpus/README.md lines; the file holds 231 newline characters |
| K12 | coverage row statement about PROVINCE.md Core/Frontier/Adjacent matches the headings | "absent" | "present" | mismatch | 48 | - | coverage row states the sections are absent; PROVINCE.md holds Core=True Frontier=True Adjacent=True |
| K13 | operability row case count equals the census selftest case count at the revision | 80 | 97 | mismatch | 49 | - | operability row states 80 cases; the census selftest at this revision prints 97 cases (TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)) |
| K14 | operability row statement about a --identity mode matches tools/tsukuroi-census.sh | "absent" | "absent" | match | 49 | - | operability row states the mode is absent; the census script holds a --identity case arm: False |
| K15 | adjacency row statement about a formal overlap table matches PROVINCE.md | "absent" | "present" | mismatch | 52 | - | adjacency row states the table is absent; PROVINCE.md holds a `\| ID \| Finding` table: True |
| K16 | sources-registry row names only repository paths that exist at the revision | ["corpus/SOURCES.md", ".ufo/evidence/round-1-kaika/after.md"] | both present | match | 161 | - | sources-registry row names 2 path(s), all present at the revision |
| K17 | host-census-gate row names only repository paths that exist at the revision | ["HEALTHY/DEGRADED/BLOCKED", "tools/tsukuroi-census.sh", ".ufo/evidence/round-1-kaika/scout-live.md", "after.md"] | 2 of 4 present | mismatch | 162 | - | host-census-gate row names 2 path(s) absent at the revision: HEALTHY/DEGRADED/BLOCKED, after.md; states 80 cases; the census selftest at this revision prints 97 cases |
| K18 | root-metadata-observer row names only repository paths that exist at the revision | [".ufo/waves/round-12/resumed/after.json", ".ufo/waves/round-12/resumed/selftest-after.json", ".ufo/waves/round-12/resumed/mode-policy-mutant.json"] | all three present | match | 163 | - | root-metadata-observer row names 3 path(s), all present at the revision |
| K19 | boot-chain-audit row names only repository paths that exist at the revision | ["tools/boot-chain-audit.sh", ".ufo/waves/round-17/l1-capture/audit-live.txt"] | both present | match | 164 | - | boot-chain-audit row names 2 path(s), all present at the revision |
| K20 | SHONEN box 1 names only repository paths that exist at the revision | ["SKILL.md", "corpus/knowledge/root-dac-decision-r12.md"] | both present | match | 5 | - | SHONEN box 1 names 2 existing path(s) and is not marked complete |
| K21 | SHONEN box 2 names only repository paths that exist at the revision | ["LOG.md", "corpus/knowledge/host-health-report-r3.md", "observation/request", "corpus/knowledge/adjacency-handoffs-fleet-r1.md"] | 3 of 4 present | mismatch | 7 | - | SHONEN box 2 names 1 path(s) absent at the revision: observation/request |
| K22 | SHONEN box 3 names only repository paths that exist at the revision | ["corpus/knowledge/adjacency-handoffs-fleet-r1.md", "corpus/knowledge/root-dac-decision-r12.md", "corpus/knowledge/executor-test-sufficiency.md"] | all three present | match | 9 | - | SHONEN box 3 names 3 existing path(s) and is not marked complete |
| K23 | SHONEN box 4 names only repository paths that exist at the revision | ["PROVINCE.md", ".ufo/waves/round-12/resumed/OverlapHostR.md"] | both present | match | 11 | - | SHONEN box 4 names 2 existing path(s) and is not marked complete |

### What the thirteen mismatches are

All thirteen are stale-statement defects inside the lane's own files:

- Three ordinal rows. The table states coverage 8, freshness 8, adjacency 7 (SCORECARD.md:48, :50, :52); the lane's own later move records carry coverage 8→9 (SCORECARD.md:224), freshness 9→9 (SCORECARD.md:772 at the base, :807 at `0cd9b28`) and adjacency 8→8 (SCORECARD.md:620). The other three ordinals (depth 8, operability 9, calibration 9) agree and match.
- Five counts the table's own counting commands would contradict if they were re-run: 24 notes against 46 .md files under corpus/knowledge, 1631 SKILL.md lines against 2301, 55 table lines against 259, 0 corpus/lessons files against 25, 20 corpus/README.md lines against 231.
- Two presence statements: the coverage row says the PROVINCE.md Core/Frontier/Adjacent sections are "not landed" when all three headings are present, and the adjacency row says there is "no formal overlap table" when PROVINCE.md:44 carries a `| ID | Finding` table.
- Two case counts: the operability row states 80 census cases and the host-census-gate capabilities row states 80, where the census selftest at the revision prints 97.
- Three named paths that do not exist at the revision: `HEALTHY/DEGRADED/BLOCKED` and the bare `after.md` in the host-census-gate row (K17), and `observation/request` in SHONEN box 2 (K21). Under the declared grammar each is a path, because each holds a slash, and none names anything in the repository.

## 4. Reachability of the target, and the finding that gated it

The declared target is 0 of 23 with exit 0. It is met: at the integrated revision `5e7c04e` the tool reports `status` PASS, `mismatches` 0, `checked` 23, exit 0, with every one of K01 to K23 `match`. The integrated `tools/check-self-assessment.py` at `5e7c04e` is byte-identical to the file I built (sha256 `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`), so the measured after-value comes from the tool as written.

Before the integration I established what the target required. In a scratch repository built with `git init` (no lane remote) from the lane bytes at `0cd9b28`, with the round-25 draft's two blocks appended and the five counts filled, the tool reported exactly one mismatch: K21, for the token `observation/request`. Changing only that phrase in SHONEN.md box 2 and nothing else took the whole set to 0 of 23, exit 0. The L1 resolved that question in scope, in the lane, with the single line `git diff b9046016 5e7c04e -- SHONEN.md` showing box 2's phrase become "current sanitized observation and request TSUKUROI-F1-MEM-01". The K17 tokens needed the same treatment and the draft already carried it: the capabilities row writes "HEALTHY, DEGRADED or BLOCKED" without slashes and cites the full `.ufo/evidence/round-1-kaika/after.md` rather than the bare `after.md`.

The measured counts at the integrated revision are K07 47 notes, K08 2355 SKILL.md lines, K09 297 table lines, K10 26 lesson files, K11 231 corpus/README.md lines, K13 97 census cases, and K20 to K23 report 2, 3, 3 and 2 existing paths. The scratch tree used for the pre-integration check is at `/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/after-sim2` and is not a lane artifact.

One operational note for anyone re-running the tool: it needs the Git repository, not an extracted tree. Run it from the lane repository, or pass `--repo` pointing at one. A `git archive` extraction has no `.git` and the tool answers `CANNOT_EVALUATE` with "not a git repository", exit 2.

## 5. Selftest

`--selftest` builds hermetic fixtures as temporary Git repositories in a temp directory (`git init`, no remote), commits them with a committed `expected-findings.json` holding the expected finding ids, and compares the tool's actual exit code and actual mismatching ids against the expectation. Seven cases, all passing, unchanged by the grammar ruling:

| case | expected | exercises |
|---|---|---|
| clean | exit 0, no mismatch | a consistent table passes |
| stale-ordinal | exit 1, K02 | a score disagreeing with its recorded transition |
| stale-count | exit 1, K07 | a note count disagreeing with the corpus |
| unstated-fact | exit 1, K12 | a row that states nothing about the fact is a mismatch |
| missing-capability-path | exit 1, K16 | a capabilities row naming an absent path |
| shonen-x-without-verifier | exit 1, K20 | a `[x]` box with no named non-author verifier |
| missing-axes-table | exit 2 | the CANNOT_EVALUATE path, never a 0-mismatch PASS |

## 6. Exit-2 paths, each with a named finding

Each was exercised on a purpose-built fixture; none can produce a 0-mismatch PASS.

| condition | error | detail |
|---|---|---|
| unknown revision | `unknown revision` | the revision asked for |
| blob absent at the revision | `missing file` | the path |
| no `## Axes — ` heading | `no axes table` | the heading searched for |
| axes table missing one of the six rows | `missing axis row` | the axis |
| no `## Capabilities` heading | `no capabilities table` | the heading searched for |
| capabilities table missing one of the four rows | `missing capability row` | the capability |
| fewer than four `- [` boxes in SHONEN.md | `fewer than four SHONEN boxes` | the count found |
| census selftest printed no case count | `census selftest produced no case count` | the exit code |
| `--repo` is not a repository | `not a git repository` | the path |

## 7. Method notes

1. **Ordinal reference.** K01 to K06 use the L1's fixed regex `\b<axis>\b[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})` with both numbers in 0..10, taking the last match by line order on SCORECARD lines outside the axes table, and comparing the row's own score cell against the after-value. The `|` character is excluded from the filler class, so a row like `| C1 ... | adjacency 8→8 (0) |` matches, prose such as `adjacency 7→8` and `depth8→8` also match, and a pair such as `10 → 15` is rejected because 15 is out of range. The observed line is reported for every ordinal check.
2. **Table resolution is section-scoped**, as the L1 confirmed: the last `## Axes — ` heading is scanned forward to the next `## ` heading and the last table in that range is taken; likewise for `## Capabilities`. This lets the round-25 draft append its two sections in either order, and it keeps the capabilities table out of the axes scan.
3. **A fact the row does not state is a mismatch.** For K12, K14 and K15 the stated value is `unstated` when the row carries neither the literal absent-form nor the present-form token, and `unstated` never matches an observed value.
4. **Path grammar, as the L1 ruled it.** Backticked spans of a capabilities row are split on whitespace; a token is a repository path exactly when it matches `[A-Za-z0-9_.{},/-]+`, holds `/` or ends in `.md`/`.json`/`.py`/`.sh`/`.txt`, does not start with `/` or `-`, after stripping a trailing `.,;:)`; one `{a,b,c}` group is expanded. No path-shape filter is applied, and a bare filename is not resolved against a preceding directory, so a token that holds a slash but names nothing in the repository is still a path and is reported as absent. Each row and each box must name at least one path or it is a mismatch.
5. **Line counts.** K08 and K11 count newline characters, which is `wc -l` semantics; K09 counts SKILL.md lines starting with `|`. K07 counts the `.md` files directly in corpus/knowledge/; K10 counts the files under corpus/lessons/.
6. **Reading the row.** Each stated number is read from the evidence-pointer cell of its row, with a fallback to the whole row, so a draft that places a count in a different column is still read rather than reported as unstated.

## 8. Scope, safety and residual risk

- I wrote one tool file in my own clone and a byte-identical copy in the lane's `.ufo/waves/round-25/w1/ExecSelfAssessTool/` seat directory, plus four JSON outputs and this report in that seat directory. I did not write to any lane production file; the L1 integrated the tool and the two tables into the lane.
- No Git or jj write command was run against the lane repository. My clone's push URL is `/nonexistent/no-push-to-lane`, so no push to the lane is possible from it; I ran only `git show`, `git ls-tree`, `git archive`, `git rev-parse` and read-only `git log`. The scratch trees under `/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/` were built with `git init` and carry no lane remote.
- Host actions were read-only. The census selftest runs inside a temporary directory over `git archive`; it is the lane's own read-only tool and writes nothing outside that temp directory.
- **Residual risk, disclosed.** The declared after-value is measured at the integrated revision `5e7c04e`, where the tool reports 0 of 23 with exit 0, so the claim's after-value rests on a measurement rather than on my scratch simulation. The base count of 13 is a measurement under the declared grammar, not a hand count, and it supersedes the earlier 12. Two limits of what I measured remain worth stating. First, K01 to K06 read the last recorded ordinal transition anywhere in SCORECARD.md outside the axes table, so the after-value depends on the file's transition history rather than on the axes table alone; a later appended transition for any axis would move that axis's observed value and could reintroduce a mismatch. Second, the tool reports what the lane's own rows state, not whether the statements are true in the world; K12 and K15 check a row's claim against the presence of a heading or table, and K13 and K17 check a stated case count against the census selftest, but nothing here audits the prose for accuracy.
- No install, upgrade or package transaction was performed; `Installs: none`.

Scope: read=SCORECARD.md, SHONEN.md, PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge/, corpus/lessons/, tools/tsukuroi-census.sh at b9046016, 0cd9b28 and 5e7c04e (all through git show/git ls-tree); wrote=/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecSelfAssessTool.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecSelfAssessTool/{check-self-assessment.py,c1-base-b9046016.json,c1-decl-0cd9b28.json,c1-after-5e7c04e.json,selftest.json}; executed=python3 tools/check-self-assessment.py --revision b9046016 --repo <lane> (exit 1, 13 of 23), python3 tools/check-self-assessment.py --revision 0cd9b28 --repo <lane> (exit 1, 13 of 23), python3 tools/check-self-assessment.py --revision 5e7c04e (exit 0, 0 of 23), python3 tools/check-self-assessment.py --selftest (exit 0, 7 cases), python3 tools/check-self-assessment.py --revision HEAD --repo /fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/after-sim2 (exit 0 with the SHONEN reword; exit 1 with the original SHONEN, K21 only), plus fixture builds for the exit-2 paths.

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
