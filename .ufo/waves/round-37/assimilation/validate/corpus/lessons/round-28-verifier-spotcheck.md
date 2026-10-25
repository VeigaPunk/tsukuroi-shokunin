author: hyaku closure (non-author integrator, @m_opus)

# tsukuroi round 28 — verifier spot-check (non-author)

Closure seat: HyakuCloseTsukuroi28, dispatched by the hyaku orchestrator. No reviewer seats were spawned. No model parameter was passed, and nothing was installed. Judged against the **current** lane tip `d9727e98c9595ddee6372d5d8a8116d4d526c85a` and the fleet report `dbe21095`, per an orchestrator input update at 19:23Z. The prompt rendered with `d824884a` and `b06816fc`. The only commit after `d824884a` is the correction `d9727e98`, which touches 2 files: it adds `.ufo/waves/round-28/w1/SentinelBattery.md` (394 lines) and appends 4 lines to `corpus/lessons/round-28.md`. Claim base: `3b9e0430b88d01415c241dd5a18b8939b8a520ac`.

Driver digest (`.ufo/watchdog.log`): `2026-10-22T15:50:22-03:00 launch tsukuroi round=28 pgid=3542973 driver=hyaku-inline attempt=1`; `2026-10-22T16:19:53-03:00 complete tsukuroi round=28; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %h %s' -- .ufo/reports/round-28/tsukuroi.md` | `tsukuroi-shokunin dbe2109`, `b06816f`, `55eadae` | pass |
| SHONEN heading, one line per box | `## SHONEN` in report; `git show d9727e98:SHONEN.md \| grep -c '^- \['` | 4 report lines, 4 boxes, all `[~]` | pass |
| Cited commits on the branch | `merge-base --is-ancestor <h> master` for 3b9e0430 f8e3a8f2 79d4264d bd5bd683 9a0654ba 938ca8ec ca6b1499 d824884a d9727e98 | all ok | pass |
| Pushed, no leftovers | `jj-lane.sh state` | `local=remote=d9727e98… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `status --porcelain` lists 0 lines | pass |
| HEAD equals master equals origin | `git rev-parse HEAD master origin/master`; `ls-remote origin refs/heads/master` | all four are `d9727e98…` | pass |
| No sandbox commit in branch history | `merge-base --is-ancestor <h> master` for a330fb0 ee430cd f92e181 db56413 2f2db7a a080e4e | all `out` | pass |
| Report records the violation | report "Lane HEAD repair" paragraph and lesson correction (`d9727e98`) | records the `update-ref --no-deref HEAD 938ca8ec…` repair with before and after values; attribution corrected to SentinelBattery (`GIT_DIR`) | pass |
| Prompt carries the template contract | `grep '^#' .ufo/prompts/tsukuroi-round-28.md` | sections 1, 2, 2b, 3, 4, 5, and 6 (hyaku addendum) | pass |
| Inert jj keep-refs | `for-each-ref refs/jj/keep`; `ls-remote origin 'refs/jj/*' \| wc -l` gives 0 | `refs/jj/keep/ee430cdf6f8c181b615c81da7d7c61c4636b3359` and `refs/jj/keep/a080e4efd961ece8871921942188b92989b6a2a9` exist locally only. Neither is on master. They are residue for the operator and were not touched. | noted |

This is not a marker report: there are 9 lane commits and real tool, test and corpus bytes.

## 2. Claims: re-check against `d9727e98`

C1 and C2 both rest on lane-registered batteries (the `SKILL.md` registry round28 rows). Under PROTOCOL §Gate standard (Closure consequence), their committed evidence was **evidence-verified**: jq over the receipts, plus sha256 of the counter bytes at each revision. Neither battery was executed. The counter-byte digests, the census, and the source quotes were **re-measured**.

Counter digests, from `git show <rev>:<file> | sha256sum`:

| Rev | `check-kernel-taint.py` | `check-adjacency-overlap.py` |
|---|---|---|
| 938ca8ec | `26fac8d9…` | `7b58652a…` |
| ca6b1499 | `99f35675…` | `7b58652a…` |
| d824884a / d9727e98 | `99f35675…` | `7b58652a…` |

**C1 (adjacency counter, axis adjacency): 19 of 24 → 0 of 24, control 6. Verdict: verified.**
- Before: `jq` on `measure/final2/c1-before-dd94cb1f.json` gives `counter_rev dd94cb1f`, `should_fail_total 24`, `should_fail_accepted 19`, `control_live_anchored_rows 6`.
- After: the summary line of `measure/final2/c1-after.jsonl` gives `counter_sha256 7b58652a…`, `should_fail_accepted 0`, `control_live_anchored_rows 6`, `should_pass_accepted 4`. This digest equals the tip counter, so the receipt covers the landed bytes.
- Selftest receipt `final2/check-adjacency-overlap-selftest.json`: 43 observations, `failed 0`. This matches "17 → 43 cases".

**C2 (kernel-taint counter, axis depth): 5 of 5 → 0 of 5, control 6. Verdict: verified, with a revision defect.**
- Before: `c2-before-75f410c8.json` gives `should_fail_accepted 5` of 5. The accepted set is exactly the five declared mutants.
- After: the summary line of `final2/c2-after.jsonl` gives `should_fail_accepted 0`, `control_verified_rows 6`, `harness_errors []`. However, its `counter_sha256` is `26fac8d9…`, the counter at `938ca8ec`. The tip counter is `99f35675…`, changed in `ca6b1499` by the residual CritC2OverStrict repair.
- No committed battery receipt measures the tip counter. The report's sentence "Gates at `ca6b1499`: … C2 battery 0 of 5, control 6" therefore has no committed receipt naming that revision.
- The selftest receipt `final2/check-kernel-taint-selftest.json` (`PASS`, 55 cases, `failed 0`) does reflect the tip counter, but it records no revision.
- I closed the gap by reading the delta (`git diff 938ca8ec ca6b1499 -- tools/check-kernel-taint.py`, 16 lines). It makes two changes:
  - `MIN_QUOTE_CHARS` drops from 16 to 10. The 2-word half of R4a is unchanged, so the one-word mutants `kernel` and `the` (`tools/mutants-kernel-taint.py:155-171`) still fail it.
  - An `Id`/`Source id` Gate column, if present, is read before `Source`. The live Gate header has no such column (the selftest builds one by replacing `| Source | URL |`), so `gate_source_from_location_cell` and `gate_heading_investigate` are unaffected. R4b, which covers `quote_from_uncited_rejected_source`, is untouched.
  - [INFERENCE] By code reading, 0 of 5 holds at the tip counter. This is not a battery run.

**Owned-axis harm.**
- `git diff 3b9e0430 d9727e98 -- SCORECARD.md` shows 53 lines, and the only `-` line is the diff header, so the file was append-only.
- The axes scores in the round-28 table equal the round-27 values: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
- `final2/self-assessment.json` at `938ca8ec`: `PASS`, `checked 27`, `mismatches 0`. This clears residual CritRoundHarm's 1 → 3 mismatch rise at `9a0654ba` (K08, K09, K10).
- `final2/registry.json`: 33 of 33, `PASS`.
- No axis is harmed.

| Axis | Verdict | Basis |
|---|---|---|
| adjacency | improved | C1 counter refuses 24 of 24 declared shapes (was 5); control unchanged; evidence-verified at the tip digest |
| depth | improved | C2 counter refuses 5 of 5 (was 0); evidence-verified at `938ca8ec`, with the tip delta checked by code reading |
| coverage | unchanged | score 9 → 9; no PROVINCE or README regression seen |
| operability | unchanged | score 9 → 9; both selftests green |
| freshness | unchanged | score 9 → 9 |
| calibration | unchanged | score 9 → 9; self-assessment 0 mismatches |

## 3. Discernment spot-check (LEARNING.md)

Sources were re-opened by plain `curl -sL` on 2026-10-22.

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S146 Stryker "Mutant states and metrics" | admit, `mined`, tier A | https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ | agree | Live page: `grep -cF "the mutant survived. You're missing a test for it."` gives 1, and `grep -oF "When all tests passed while this mutant was active, the mutant survived"` matches. The snapshot sha256 `5295e9bb…` equals the Gate row. The project documents its own vocabulary, which supports tier A, and the batteries do use the accepted/survived vocabulary. |
| S147 pitest "Basic concepts" | reject, with reason and flip | https://pitest.org/quickstart/basic_concepts/ | agree | The live page is about bytecode mutation (lines 99 and 102: "mutate the bytecode", debug info "in the bytecode"; line 184: non-viable mutants "could not be loaded by the JVM"). That mechanism has no operand in a JSON-data gate, and mutation-testing method is tameshi ground (OUT-010). The corrected located quote "means a test caught the mutation successfully." matches 1 time live (`grep -cF`). The snapshot sha256 `c51d8423…` equals the Gate row. The original tag-stripped quote was correctly disclosed and fixed in `d824884a`. |

`corpus/SOURCES.md:152` (S146 row): the located quote "When all tests passed while this mutant was active, the mutant survived. You're missing a test for it." is 18 words, within the ≤25 limit, and is verbatim on the live page. Row S147 (`:153`) carries no located quote, only the REJECTED reason and flip, which fits a rejected row.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0, last line `tsukuroi ok …/corpus/SOURCES.md`, 25 W04 advisories. The same count was recorded at the start of the round.

## 4. Trend verdicts

- **expansion: unchanged.** No new domain ground; the two sources added are method vocabulary (S146) and a reject (S147).
- **quality: improved.** Two counters refuse their routed should-fail shapes (19 → 0 of 24, 5 → 0 of 5) with live controls intact. Selftests went from 17 to 43 and from 46 to 55 cases.
- **discernment: improved.** The round-27 routed "no reject" defect is answered by S147, a reject I agree with. The wave-1 attacks changed both counters before closing. The lane self-corrected the S147 quote and, after the freeze, the contamination attribution.

## 5. Routed defects (lane fixes next round)

1. **C2 receipt revision gap.** Commit a C2 battery receipt whose `counter_sha256` is the tip counter (`99f35675…`), and record a revision in the selftest receipts. The report must not state "Gates at `<rev>`" without a committed receipt for that revision.
2. **Battery environment leak.** SentinelBattery finding 3 (`.ufo/waves/round-28/w1/SentinelBattery.md:141`): `tools/mutants-adjacency-overlap.py` calls `subprocess.run` with the caller's environment, so `GIT_*` reaches its git calls. That is how the sandbox commits `a330fb0`, `ee430cd`, `f92e181`, `db56413` and `2f2db7a` landed in the lane `.git`. Scrub `GIT_*` in both batteries, and add a selftest that can fail.
3. **R4a 2-word half unanchored.** MutC2Counter mutants m1 and m7 survive both instruments.
4. **C1 padding shapes.** 15 of 22 wave-1 padding shapes still score 6 (RevC1Repairs). CritC1NewShapes lists more: duplicated anchors, PROVINCE-mirror lane quotes, withdrawn markers, clipped words.
5. **Carried round-27 defects:** 4 (companion debt), 5 (`oom-event-plane.md` and `kill-event-deep-r8.md`, shown to be this lane's files) and 6 (self-assessment tool).
6. **Seat findings outside the report.** RevFamilyB2 was cancelled on a wrong suspicion, so its findings are lost. MutC1Counter is absent by design, frozen while still running. SentinelBattery is now committed in `d9727e98` but not folded into the claims.
7. **Lowest-axis duty contested.** CritClaimSizing argues both claims are operability-style moves while one axis sits at 9. This is for the operator; it does not change the verdict.

## 6. SHONEN

All four boxes stay `[~]` with author evidence only, and none of them is fully checkable by a non-author this round. Promotion is not suggested.
