VERDICT: draft

# Lesson-to-Criterion Recurrence Review and Quality Criterion 94 Draft (Item X-4)

Seat: `ConnLessonQuality`
Target: Analysis of recurring mistake classes across `corpus/lessons/round-41.md` through `round-45.md` `## Mistakes` and `corpus/QUALITY.md:167-183` (criteria 85–93); determination of gate fail-capability; and drafting the single most valuable next quality gate.

---

## 1. Declared Axes (godspeed posture)

Under the round-46 declaration (`SCORECARD.md:2968-2970`), the lane operates on six declared axes:
1. **Operability:** Census reliability, standalone flag contracts, and execution-environment reflection (`tools/tsukuroi-census.sh --identity`).
2. **Depth:** Rigorous source grounding verified by counted, independent reviewer/critic verdicts against pinned source snapshots (`corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1–GR3).
3. **Coverage:** Verified test-surface breadth without monoculture or unexercised branches.
4. **Freshness:** Current kernel/tooling alignment and accurate temporal premises.
5. **Calibration:** Discriminative ability of counters, predicates, and controls to reject defect mutants and evasions while passing genuine candidates.
6. **Adjacency / Registry / Census Integrity:** Preservation of cross-lane pointers, source registry consistency (`corpus/SOURCES.md`), and strict line/hash anchors.

This inquiry evaluates how lessons from rounds 41–45 translate into admission criteria that strengthen **Calibration**, **Depth**, and **Round Governance** without harming **Operability** or **Adjacency**.

---

## 2. Recurrence Analysis Across Rounds 41–45

Across rounds 41 through 45, the lane recorded 38 distinct mistake rows in `## Mistakes`. Analyzing these alongside criteria 85–93 in `corpus/QUALITY.md` reveals four primary recurring mistake classes:

### Class 1: Binding channel failures
- **Mechanism:** Verdicts produced by counted reviewer/critic seats are lost, dropped, or corrupted because the counter binds through an indirect, fragile, or mismatched channel (orchestrator results JSON, unanchored mention matching, or unhandled output serializations).
- **Recurrence:**
  - *Round 41:* `R41-GUARD-BYPASS` (`round-41.md:78`) showed relation-literal writers with planted verdict files passed C2 predicates, necessitating dispatch-record binding (`QUALITY 89`, `QUALITY.md:175`).
  - *Round 42:* `R42-VERDICT-MENTION` (`round-42.md:74`) showed unanchored regexes (`ROW SC<n> VERDICT:`) bound critic sentences quoting the line to dispute it (`QUALITY 90`, `QUALITY.md:177`).
  - *Round 43:* `R43-VERDICT-JSON-UNBOUND` (`round-43.md:105`) showed plain first-line binding failed to bind JSON outputs with `"verdict": "holds"`.
  - *Round 44:* `Item 2 disposition` (`round-44.md:55-58`) closed padded/blank lines, but SR7 was still lost to a JSON-string output (`round-45.md:85`).
  - *Round 45:* `R45-C2-BINDING-CHANNEL` (`round-45.md:85`) caused complete C2 collapse (`verdicts_ok 0`) when 3 seats yielded JSON objects with `verdict` key, 2 yielded preambles, and an orchestrator restart lost 41 results records.
- **Governing Gates:** `QUALITY 89`, `QUALITY 90`, `QUALITY 93`. In round 46, `tools/check-scrub-admission-r46.py` binds directly to the seat's own report file (first two lines), bypassing orchestrator results entirely (`SCORECARD.md:3001-3003`).
- **Able-to-Fail Status:** **SHOWN ABLE TO FAIL**. Controls C2-K13/K6 in round 43 (`round-43.md:105`), C2-K14/K15/K16 in round 44 (`round-44.md:55`), five recovered yield shapes in round 45 (`round-45.md:85`), and C2 controls K6, K7, K12, K20 in round 46 (`battery-summary-c2.jsonl`) all demonstrated fail-capability.

### Class 2: Counters bound to retireable names
- **Mechanism:** A frozen evaluation counter hardcodes an ephemeral orchestrator/dispatch identifier (such as wave name `w1` or run `r1`) that the dispatcher retires upon partial failure or respawn, locking the evaluation out and requiring post-freeze edits.
- **Recurrence:**
  - *Round 42:* `R42-BATTERY-SUMMARY-COLLISION` (`round-42.md:77`) hardcoded a single filename across multiple runners.
  - *Round 44:* Disposition noted residual seats were forgeable like main path due to fixed naming (`round-44.md:58`).
  - *Round 45:* `R45-A2-COUNTER-WAVE-NAME` (`round-45.md:86`): C2 counter at freeze `ea6e0ee3` hardcoded `w1`/`r1`; when wave 1 died, the dispatcher retired `.ready`, requiring post-freeze edit `057c1804` (`w1` → `a2w1`).
- **Governing Gates:** `QUALITY 93` (`QUALITY.md:183`) mandates declaring the wave name in one constant.
- **Able-to-Fail Status:** **SHOWN ABLE TO FAIL**. Round 45 control battery showed forged records under old name `w1` failed the rebound counter (`round-45.md:86`); round 46 tested controls K10 (`two-waves`) and K15 (`any-wave-name`) (`battery-summary-c2.jsonl`).

### Class 3: Receipts that do not back their numbers (evidence divergence)
- **Mechanism:** A report, scorecard row, or intake seat asserts specific inventory counts, line numbers, or set intersections, but the companion receipts in the seat directory omit raw files, contain phantom IDs, miss real items, or cite non-existent git paths.
- **Recurrence:**
  - *Round 42:* `R42-FREEZE-CENSUS-LIVE-PATH` (`round-42.md:78`): receipt ran on live tree, not exported commit.
  - *Round 43:* `R43-MORI-ARITH` (`round-43.md:104`): handoff cited arithmetic (+6, +3) without starting referent; `R43-SIB-PIN-UNREPORTED` (`round-43.md:103`) missed moved tameshi pin.
  - *Round 44:* `R44-D7-CITATION-HALF-CLOSED` (`round-44.md:52`, `round-45.md:84`): report cited `strace-rev-live1.log` (`rc=128`) while committed file was `.log.gz`.
  - *Round 45:* `R45-ASMGATE-IDCENSUS` (`round-45.md:83`): `a2w1/AsmGate.md` reported "183 registry ids, 147 staged ids, 30 intersections"; true counts were 249, 147, 50. Kept receipt `id-collisions.txt` had 5 non-registry phantom IDs and omitted 25 real collisions; raw `reg-ids` and `staged-ids` files were absent.
- **Governing Gates:** `QUALITY 21`, `QUALITY 54`, `QUALITY 77` exist for historical summaries and revision citations, but for in-wave seat reports, `round-45.md:83` explicitly states: **`Captured-by: none in-wave; recomputed by the round-45 lesson seat`**.
- **Able-to-Fail Status:** **NONE IN-WAVE**. While post-hoc checks in subsequent lessons demonstrated the failure (e.g. AsmGate recount in `asmgate-recount-check.txt`, `git cat-file -e` in `d7-citation-check.txt`), there has been **no automated in-wave gate shown able to fail** prior to round closure.

### Class 4: Pre-data controls that a weak counter passes
- **Mechanism:** A counter draft or predicate contains flaws (e.g. unvaried literal fixtures, unanchored regexes, unseparated execution paths) allowing defective mutant variants to pass pre-data controls.
- **Recurrence:**
  - *Round 41:* `R41-LABEL-SUFFIX` (`round-41.md:73`): counter compared stderr FAIL with stdout PASS; 13 of 13 mutants survived. `R41-GUARD-BYPASS` (`round-41.md:78`): guards bypassed by reading the guard.
  - *Round 42:* `R42-OBSERVED-CHANNEL` (`round-42.md:70`): uid 0 namespace legs let evasive censuses pass; `R42-C1-SELFTEST-UNMEASURED` (`round-42.md:75`): K6 passed without declared selftest cases.
  - *Round 44:* `R44-C2-CONTROL-K17-CATCH` (`round-44.md:48`): counter searched whole line, letting mutant K17 pass until counter fixed.
  - *Round 45:* `R45-C2-BINDING-CHANNEL` (`round-45.md:85`): controls omitted actual yield shapes.
  - *Round 46:* Pre-freeze C1 counter draft passed control K2 (`K2-pathhash`: exit 0 PASS, `as_expected: false`, `battery-summary-c1-draft1.jsonl:3`; `SCORECARD.md:2994-2999`) because `${BASH_SOURCE[0]:-}` on stdin/pipes never named a file.
- **Governing Gates:** `QUALITY 73`, `QUALITY 80`, `QUALITY 87`, `QUALITY 88`, `QUALITY 89`, `QUALITY 90`, `QUALITY 93`.
- **Able-to-Fail Status:** **SHOWN ABLE TO FAIL**. Demonstrated repeatedly: round 41 candidate run kills 13 (`round-41.md:73`); round 44 C2-K17 red (`round-44.md:48`); round 45 K3 red (`round-45.md:86`); round 46 draft1 K2 caught red before freeze (`c1-k2-predata-check.txt`).

---

## 3. Recurrence Table

| Class | Rounds Observed | Governing Gate(s) | Able-to-Fail Evidence | File:Line Evidence |
|---|---|---|---|---|
| **Binding channel failures** | 41, 42, 43, 44, 45 | `QUALITY 89`, `90`, `93`; R46 report-file first-line binding | **Shown able to fail** (C2-K13/K6 in r43; C2-K14/15/16 in r44; recovered yields in r45; K6/K7/K12/K20 in r46) | `round-41.md:78`<br>`round-42.md:74`<br>`round-43.md:105`<br>`round-44.md:55`<br>`round-45.md:85`<br>`SCORECARD.md:3001` |
| **Counters bound to retireable names** | 42, 44, 45 | `QUALITY 93` (single declared wave constant) | **Shown able to fail** (r45 forged all-holds under old `w1` failed rebound counter; r46 battery K10/K15) | `round-42.md:77`<br>`round-44.md:58`<br>`round-45.md:86`<br>`SCORECARD.md:2987` |
| **Receipts that do not back their numbers** | 42, 43, 44, 45 | `QUALITY 21`, `54`, `69`, `77`; **none in-wave for seat reports** | **None in-wave** (Caught post-hoc: AsmGate recount found 5 phantom IDs & 25 missed collisions; git cat-file -e rc=128 on uncompressed log) | `round-42.md:78`<br>`round-43.md:103-104`<br>`round-44.md:52`<br>`round-45.md:83-84` |
| **Pre-data controls passed by weak counter** | 41, 42, 44, 45, 46 | `QUALITY 73`, `80`, `87`, `88`, `89`, `90`, `93` | **Shown able to fail** (r41 13 kills; r44 C2-K17 red; r45 K3 red; r46 draft1 K2 red with exit 0 PASS, as_expected: false) | `round-41.md:73,78`<br>`round-42.md:70,75`<br>`round-44.md:48`<br>`round-45.md:85`<br>`SCORECARD.md:2994` |
| *Secondary: Host scratch / misroot pollution* | 41, 42, 43, 44, 45 | Host prompt guards; `--scratch` discipline; `seat-harm-log.py` | **Shown able to fail** (fleet root git status red at r44 21:14Z; stray ls red in r43; 15/15 mutant kills in r45) | `round-41.md:80`<br>`round-42.md:79-80`<br>`round-43.md:108`<br>`round-44.md:44`<br>`round-45.md:126-156` |
| *Secondary: Coordinate & line-anchor drift* | 41, 42, 43, 45 | `QUALITY 21`, `60`; C1 adjacency kill rule | **Shown able to fail** (Control C1-K7 comment insertion scores adjacency_ok 0, status FAIL, exit 1) | `round-41.md:79`<br>`round-42.md:78`<br>`round-43.md:107`<br>`round-45.md:80` |

---

## 4. The Single Most Valuable Next Gate

### Gap Identification
Comparing the four recurring classes identifies **"Receipts that do not back their numbers"** as the single most critical vulnerability remaining in the lane's verification regime:
1. **Binding channels** are now gated by `QUALITY 93` and the direct report-file binding adopted in round 46 (`SCORECARD.md:3001-3003`), supported by fail-capable controls K6/K7/K12/K20.
2. **Retireable wave names** are stabilized by declared constants (`QUALITY 93`) and multi-wave controls K10/K15.
3. **Weak counters passing controls** are actively caught before freeze by the pre-data control battery runner (`battery-summary-*.jsonl`), as demonstrated by K2 in round 46 (`battery-summary-c1-draft1.jsonl:3`).
4. **Receipts that do not back their numbers**, however, has **ZERO IN-WAVE AUTOMATED GATES**. In round 45 (`round-45.md:83`), seat `AsmGate` declared 183 registry IDs and 30 collisions when the real figures were 249 and 50, kept a receipt with 5 phantom IDs and omitted 25 real collisions, and omitted raw lists from its directory—yet no wave check or gate failed.

### Exact Proposed Text: Quality Criterion 94

```markdown
94. **A seat report or gate evaluation asserting a count, set, or file existence retains the exact raw lists in its seat directory, and citations resolve in Git (R45-ASMGATE-IDCENSUS / R45-D7-CITATION-HALF-CLOSED):**
when a seat report, intake gate, or scorecard receipt asserts an inventory count, ID list, set intersection, or artifact existence (such as registry rows, staged IDs, collisions, or mutant tallies), the seat's receipt directory (`.ufo/waves/round-<N>/<wave>/<seat>/`) contains the exact newline-delimited raw list files from which those numbers were derived; every file path cited in the report or receipt resolves in Git at the measured revision (`git cat-file -e <REV>:<path>` exits 0); and any set operation (such as collision detection or intake intersection) is verifiable by re-running the canonical extractor over those raw files. An unbacked count, an omitted input list, a phantom identifier, or a citation to an uncommitted or renamed file (such as citing an uncompressed path when only a `.gz` archive is committed) is an evidence failure that invalidates the report and prevents admission.
Failing examples:
(1) `a2w1/AsmGate.md` (round 45) reported "183 registry ids, 147 staged ids, 30 intersections" while the revision held 249 registry IDs and 50 collisions, its `id-collisions.txt` listed 5 non-registry IDs and omitted 25 real collisions, and its input list files (`reg-ids`, `staged-ids`) were absent from the seat directory (`corpus/lessons/round-45.md:83`).
(2) `w1/C1ExecLiveRead/commands.txt:26,81` and `w2/SkillReview.md:55` cited `strace-rev-live1.log` (`rc=128`) while evidence was committed as `strace-rev-live1.log.gz` (`rc=0`) (`corpus/lessons/round-45.md:84`).
(3) `R43-MORI-ARITH` (round 43) cited "+6" and "+3" offsets without base coordinate referents (`corpus/lessons/round-43.md:104`).
Shown able to fail: `python3 tools/check-seat-receipts.py --report .ufo/waves/round-45/a2w1/AsmGate.md --seat-dir .ufo/waves/round-45/a2w1/AsmGate --revision 18389f44` flags five verification failures (3 unresolved git citations, 2 missing receipt files; exit 1, receipt `.ufo/waves/round-46/w1/ConnLessonQuality/gate-prototype-test.txt`).
Lesson: `corpus/lessons/round-45.md` Mistakes R45-ASMGATE-IDCENSUS, R45-D7-CITATION-HALF-CLOSED.
```

---

## 5. UFO-FSD Connector Synthesis (Single Bounded Move)

- **Evidence:**
  - `corpus/lessons/round-45.md:83` (`R45-ASMGATE-IDCENSUS`): AsmGate reported 183 vs 249 registry IDs, 30 vs 50 collisions, 5 phantom IDs, 25 omitted collisions, and missing raw files (`Captured-by: none in-wave`). Verified in `.ufo/waves/round-46/w1/ConnLessonQuality/asmgate-recount-check.txt`.
  - `corpus/lessons/round-45.md:84` (`R45-D7-CITATION-HALF-CLOSED`): Citations to `strace-rev-live1.log` fail `git cat-file -e` with `rc=128`. Verified in `.ufo/waves/round-46/w1/ConnLessonQuality/d7-citation-check.txt`.
  - `SCORECARD.md:2994-2999`: Pre-freeze C1 counter draft passed K2 (`K2-pathhash`) as `as_expected: false` (`controls/battery-summary-c1-draft1.jsonl:3`). Verified in `.ufo/waves/round-46/w1/ConnLessonQuality/c1-k2-predata-check.txt`.
- **Affected Axes:**
  - **Calibration (+):** Closes the unverified declaration gap for intake/seat reports; eliminates phantom findings and unbacked summaries.
  - **Round Governance / Documentation (+):** Ensures evidence cited in reports and scorecards actually exists in git.
  - **Depth (+):** Protects grounding rows from relying on phantom citations.
  - **Operability (Neutral):** Zero runtime overhead or impact on `tools/tsukuroi-census.sh`.
  - **Adjacency (Neutral):** Does not alter cross-lane anchors or registry definitions.
- **Proposed Move:**
  Formalize **Quality Criterion 94** in `corpus/QUALITY.md` and commit the lightweight validator `tools/check-seat-receipts.py` (prototype delivered in `.ufo/waves/round-46/w1/ConnLessonQuality/check-seat-receipts.py`), enabling the L1 or integration watchdog to verify seat receipts and git citations before wave settlement.
- **Risks & Mitigations:**
  - *Risk:* Overly aggressive regex parsing could flag conversational prose numbers.
  - *Mitigation:* The validator targets explicit evidence patterns (e.g. `\d+ registry ids`, `\d+ collisions`, backticked repo paths) and companion files in the seat's directory, ignoring non-evidential prose.
- **Verification:**
  Tested against historical round-45 artifacts:
  - Fails on `round-45/a2w1/AsmGate.md` with exit 1, reporting 3 missing git objects and 2 missing raw list files (`.ufo/waves/round-46/w1/ConnLessonQuality/gate-prototype-test.txt`).
  - Passes on properly receipted seats containing matching newline-delimited lists.

---

## 6. Scope Limitation & Discipline

- Leaf member execution: no subagents dispatched, no swarm invoked, no messages sent to `agent://all`.
- Read-only on lane code: no tracked files modified, no git mutation commands executed.
- All scratch operations conducted under `/fast/scratch/hyaku/tsukuroi-r46/ConnLessonQuality/` and cleaned up; receipts preserved in `.ufo/waves/round-46/w1/ConnLessonQuality/`.
