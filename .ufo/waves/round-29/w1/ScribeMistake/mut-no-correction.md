# Round 28 — lesson (tsukuroi, attempt 1, 2026-10-22)

Claims (declaration `SCORECARD.md` section "Round 28 — declaration, attempt 1"): C1 the adjacency counter `tools/check-adjacency-overlap.py` refuses the 24 should-fail register shapes of round-27 CritC2Tool (battery `tools/mutants-adjacency-overlap.py`); C2 the kernel-taint counter `tools/check-kernel-taint.py` refuses the five routed should-fail shapes (battery `tools/mutants-kernel-taint.py`). Both batteries cite S146 for the outcome vocabulary they count: an accepted should-fail mutant is the "survived" case.

## Gate

Candidates considered: the Stryker Mutator documentation page on mutant states and metrics, and the pitest "Basic concepts" page, both fetched by plain curl on 2026-10-22 by wave-1 scribes (ScribeSourceStryker, ScribeSourcePitest); snapshots committed under `.ufo/waves/round-28/w1/`.

| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |
|---|---|---|---|---|---|
| S146 | https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ | 2026-10-22 | "When all tests passed while this mutant was active, the mutant survived. You're missing a test for it." | `.ufo/waves/round-28/w1/ScribeSourceStryker/S146.html` line 14, sha256 `5295e9bb464367c8287d4d56d822b01710edd744a2445fd73a222f405e4cc450` | admit, `mined`, tier A (the project documents its own vocabulary); used-by both batteries and this lesson |
| S147 | https://pitest.org/quickstart/basic_concepts/ | 2026-10-22 | "Killed means a test caught the mutation successfully." | `.ufo/waves/round-28/w1/ScribeSourcePitest/S147.html` line 175, sha256 `c51d8423f5a75e00c7039463f8a5992ef8f1f92b994d69f67d212ff7bfd92b3a` | **reject** (routed defect 1: the Gate records a reject decision): its mechanism (bytecode operators, coverage, per-test selection, JVM non-viable mutants) has no operand in a JSON-data gate, and S146 already carries the vocabulary; mutation-testing method is tameshi ground (`PROVINCE.md` OUT-010). Flip: the lane lands a code-mutation battery over its own checker source |

Registry changes (old → new): S146 absent → `mined` (recheck `180d`, no version pin offered by the page); S147 absent → `rejected` (recheck `on-release`). No existing row's status, recheck or used-by changed.

## Routed defects from the round-27 spot-check (`corpus/lessons/round-27-verifier-spotcheck.md:97-106`)

1. No reject in the round-27 Gate: this Gate records S147 as a reject with reason and flip.
2. Adjacency counter accepts 19 of 24 should-fail shapes: claim C1 (rules B1 to B7, 36-case selftest, battery).
3. Kernel-taint counter accepts one-word quotes and quotes from uncited sources; docstring R4 said "appears in": claim C2 (rules R4a to R4c, docstring R4 corrected, selftest 46 → 52 cases, battery).
4. Owed companion debt (MP4 qualifier in `SKILL.md`, MP4 JSON action, `driver-firmware-plane.md:276` `[unk]`, further storage-JSON statements): still owed; not touched this round (wave-1 ScoutLaneState confirms which parts remain).
5. Mori's "+200 band" reading: mori's item per the orchestrator; not touched.
6. `tools/check-self-assessment.py` hyphenated headings, docstring, missing cases: still owed; not touched.
7. QUALITY 69 now names its lesson id R27-SIBLING-POINTER-DRIFT.
8. Cross-lane items for mori and the operator: unchanged, not absorbed.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R28-RUN-BEFORE-DECLARATION | process | `SCORECARD.md:1065` records a counting run before the declaring commit: "the L1 ran the uncommitted C1 counter through the battery once during development at about 18:56Z (0 of 24 accepted, control 6)". The declaration commit `f8e3a8f` has committer time `2026-10-22T15:56:59-03:00` (that is 18:56:59Z) and is the same commit that changes `tools/check-adjacency-overlap.py` and adds `tools/mutants-adjacency-overlap.py` (`git show --stat f8e3a8f`: `SCORECARD.md` +17, `tools/check-adjacency-overlap.py` +135/-24, `tools/mutants-adjacency-overlap.py` +397) | none. No QUALITY criterion binds a declaration to postdate its own counting run: 42 (`corpus/QUALITY.md:87`) pins review bytes before dispatch, 63 (`:127`) pins pre-source mechanism wording, 72 (`:140`) pins should-fail counter cases; none orders declaration against run | Rule: the round's declaration commit precedes every run of the declared counting command, and the counter under test is not changed in the declaration commit, so the after-value cannot be fitted to an observed result. Demonstrated at record level with `python3 /fast/scratch/hyaku/tsuku28/ScribeMistake/check-order.py`: `round 27 PASS declaration=db9eecf all three rules hold` and `round 28 FAIL declaration=f8e3a8f R1 pre-declaration run recorded; R2 no measurement receipt commit after the declaration; R3 counter under test changed in the declaration commit` (exit 1). Same code path passes on round 27 (declaration `db9eecf` 12:56:35-03:00; counters `75f410c` 14:05:11 and `dd94cb1f` 14:11:09; first receipt commit `4c487fc` 14:09:44/-03:00), so the rule is not vacuously red |

The ordering check that shows the fix able to fail is committed at `.ufo/waves/round-28/w1/ScribeMistake/check-order.py` (fixture `order-fixture.json`): it prints `round 27 PASS` and `round 28 FAIL … R1 pre-declaration run recorded; R2 no measurement receipt commit after the declaration; R3 counter under test changed in the declaration commit`. Criterion: QUALITY 73 (R28-BATTERY-MEASURE) states that a run of uncommitted counter bytes is development output, never the measured value; the declared values of this round are the ones re-measured at the round's commits.

## C2 rule refinement after wave-1 CritC2RuleDesign (targets unchanged)

- CritC2RuleDesign showed that a per-quote floor of 4 words would drop the live control to 2 rows; the landed R4a floor (2 words and 16 non-whitespace characters per quote) keeps all live quotes (shortest live quote 25 characters) and refuses both one-word shapes. The landed rule was chosen before the critic's report and is unchanged.
- It also showed that R4b compared the quote source against the raw `sources` list, so a row whose sources are `{"id": "S140"}` objects would be wrongly refused. Fixed after 79d4264d by comparing against the normalised ids, with a should-pass selftest case `r4b-pass-source-items-as-objects` (52 cases). The fix can only accept rows that R3 already accepts; the battery still refuses all five declared shapes.
- Left open and disclosed (not C2's declared scope): a `## Gate` table inside a fenced code block, a second `## Gate` section, `### Gate` (the section parser drops heading level), a generic quote of 2 or more words and 16 or more characters, and eight more CritC1Tool shapes (capture pointers, SKILL rows, withdrawn rows), listed as `other_accepted` by the battery.

## Residual repair and lane contamination (appended 2026-10-22, before closure)

- Residual CritC2OverStrict (`.ufo/waves/round-28/residual/CritC2OverStrict.md`): the R4a floor refused short but specific quotes (`Tainted: P        W  O`, `return -EPERM;`) and a Gate table with an `Id` column was refused. Repaired in `tools/check-kernel-taint.py`: floor 16 → 10 non-whitespace characters, a Gate `Id` or `Source id` column is read before `Source`; three should-pass selftest cases (55 cases, exit 0); the C2 battery still reads 0 of 5 with control 6. Residual MutC2Counter: the R4a "at least 2 words" half has no independent anchor (mutants m1, m7 survive) — owed.

### Mistakes added before closure

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R28-SEAT-COMMITTED-IN-LANE | seat scope breach | At 16:13 -03 a wave-1 seat's sandbox driver committed battery mutants inside the lane repository: sandbox commit `a330fb0dfad349c0a3d6583cf1f64f4cc45ca241` ("base export f8e3a8f2…", author `t`) and children `ee430cd` `sibling-path-double-slash`, `f92e181` `sibling-path-dot-segment`, `db56413` `fabricated-snapshot-other-path`, `2f2db7a` `fabricated-snapshot-pin-name-variant` (lane `git reflog`), leaving git HEAD detached at `a330fb0` and the jj helper refusing ("working copy has changes on a non-tip base"). The mutant names are the B2 family assigned to seat RevFamilyB2 (cancelled by the L1 at 19:15Z); attribution is by assignment and timing, not by a process trace. Branch and remote stayed at `938ca8ec`; working-tree bytes were checked equal to `master` | the wave contract ("never run git write commands against the lane"; sandboxes via `git archive` + `git init`) — stated, not enforced | Repair (orchestrator-approved, 19:17Z): before `master`=`origin/master`=`938ca8ec`, HEAD=`a330fb0`; ran once `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin update-ref --no-deref HEAD 938ca8ec564f911df22162cec64ae3c48a9f1eb5`; after HEAD=`master`=`origin/master`=`938ca8ec`; sandbox chain untouched. Prevention owed: a wave context line telling seats that copy a kept battery sandbox to verify `git -C <dir> rev-parse --show-toplevel` is not the lane before any commit |

### Corrections from residual RevFrontierRows (appended before closure)

- The S147 Gate located quote above, "Killed means a test caught the mutation successfully.", is a tag-stripped rendering, not a verbatim substring of the saved bytes (`grep -F` exit 1). Line 175 of `.ufo/waves/round-28/w1/ScribeSourcePitest/S147.html` reads `<p><strong>Killed</strong> means a test caught the mutation successfully.</p>`. Corrected located quote (verbatim, `grep -cF` → 1): "means a test caught the mutation successfully." The reject decision, reason and flip are unchanged.
- QUALITY 60 disclosure: this round changed one existing QUALITY line in place, criterion 69 (`corpus/QUALITY.md:137`, between `bd5bd683` and `9a0654ba`): "(C2, round 27)" became "(R27-SIBLING-POINTER-DRIFT)" (routed defect 7); every other change to `corpus/QUALITY.md` is the appended criterion 73.

