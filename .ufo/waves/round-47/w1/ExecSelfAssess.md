VERDICT: defect-found

# F-7 — self-assessment run at the freeze revision (counted read only; nothing in the lane was written)

Counter: `tools/check-self-assessment.py`, blob at `77e9e2b2` is byte-identical to the worktree file
(`git show 77e9e2b2…:tools/check-self-assessment.py | sha256sum` = worktree `sha256sum`
= `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6`).

`--help` read first; the tool has `--revision`, `--repo`, `--selftest`, `--scratch` and no other mode.

Receipts (copied out of scratch; every claim below is one of these files):
`.ufo/waves/round-47/w1/ExecSelfAssess/{out-main.json, out-base.json, out-r46outcome.json,
out-selftest.json, census-clean.txt, census-space.txt, SHA256SUMS}`.

## 1. Headline

```
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py \
  --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611
=> checked 27, mismatches 3, status FAIL, exit code 1
   declaring_round 46, axes_heading "## Axes — current self-assessment (round 46 final measured surface)",
   reference_lines 618        (receipt out-main.json)
```

Three cells of SCORECARD's self-assessment surface are stale against the frozen tree: **K10, K13, K17**.
24 of 27 checks match.

Same counter at the three reference points (receipts `out-base.json`, `out-r46outcome.json`, `out-main.json`):

| revision | what it is | checked | mismatches | status | exit |
|---|---|---|---|---|---|
| `b313963c` | round-46 measured-outcome commit | 27 | 0 | PASS | 0 |
| `9160190` | round-47 base (lane tip at round start) | 27 | **1** (K10 68 vs 69) | FAIL | 1 |
| `77e9e2b2` | the frozen freeze revision (this read) | 27 | **3** (K10, K13, K17) | FAIL | 1 |

So the calibration gate was **already red at the round-47 base** (K10) and the freeze revision added two
more reds (K13, K17) — both caused by this round's own C2 change.

## 2. All 27 checks at `77e9e2b2` (stated → observed, from out-main.json)

| id | subject (short) | stated | observed | status |
|---|---|---|---|---|
| K01 | depth score = last recorded depth transition after-value | 8 | 8 (`SCORECARD.md:2250`) | match |
| K02 | coverage score = last coverage transition | 9 | 9 (`:2171`) | match |
| K03 | operability score = last operability transition | 9 | 9 (`:2249`) | match |
| K04 | freshness score = last freshness transition | 9 | 9 (`:1560`) | match |
| K05 | calibration score = last calibration transition | 9 | 9 (`:1560`) | match |
| K06 | adjacency score = last adjacency transition | 8 | 8 (`:1560`) | match |
| K07 | depth row note count vs `corpus/knowledge/*.md` | 67 | 67 | match |
| K08 | depth row `SKILL.md` line count | 4546 | 4546 | match |
| K09 | depth row `SKILL.md` table lines | 1323 | 1323 | match |
| **K10** | **depth row `corpus/lessons/` file count** | **68** | **70** | **mismatch** |
| K11 | coverage row `corpus/README.md` lines | 480 | 480 | match |
| K12 | coverage row PROVINCE Core/Frontier/Adjacent | present | present | match |
| **K13** | **operability row census case count** | **162** | **164** | **mismatch** |
| K14 | operability row `--identity` mode | present | present | match |
| K15 | adjacency row formal overlap table | present | present | match |
| K16 | sources-registry row paths exist | 2 paths | 2 paths | match |
| **K17** | **host-census-gate row paths + case count** | 3 paths / **162 cases** | 3 paths / **164 cases** | **mismatch** |
| K18 | root-metadata-observer row paths exist | 3 paths | 3 paths | match |
| K19 | boot-chain-audit row paths exist | 3 paths | 3 paths | match |
| K20 | SHONEN box 1 paths exist | 5 paths | 5 paths | match |
| K21 | SHONEN box 2 paths exist | 3 paths | 3 paths | match |
| K22 | SHONEN box 3 paths exist | 3 paths | 3 paths | match |
| K23 | SHONEN box 4 paths exist | 6 paths | 6 paths | match |
| K24 | SHONEN box 1 cited notes present, not superseded | 4 notes | 4 notes | match |
| K25 | SHONEN box 2 cited notes | 2 notes | 2 notes | match |
| K26 | SHONEN box 3 cited notes | 2 notes | 2 notes | match |
| K27 | SHONEN box 4 cited notes | 3 notes | 3 notes | match |

Counter integrity: its own hermetic fixture selftest passes —
`--selftest` => `selftest PASS, cases 19, failures 0`, with the expected exits 0/1/2 (2 for the two
`CANNOT_EVALUATE` fixtures), receipt `out-selftest.json`. The counter is not the defect.

## 3. Exactly which cells fail, and why (attribution with history)

**(a) K13 — operability row, `SCORECARD.md:3031` (the newest red; caused by this round's C2)**

Stated: ``bash tools/tsukuroi-census.sh --selftest` prints PASS (162 cases, 162 passed, 0 failed)``.
Observed at `77e9e2b2`: `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`, rc 0 —
the counter's own archive run and my two independent runs agree (see §4).
Cause: round-47 commit `3629c46a` added two `(R47-C2)` cases at
`tools/tsukuroi-census.sh:3473-3482` ("selftest: the fixture base classifies absolute even when TMPDIR
contains a space", "a space in a root override stays unsafe by design"). 162 + 2 = 164.
The cell was accurate at the base (`9160190`: K13 match, 162 = 162) and at the round-46 outcome.
Note the internal disagreement: the round-47 declaration row of the *same* SCORECARD already states the
new number — `SCORECARD.md:3066` target cell: "case count 164 = 162 + 2 new" — so the tables say 162
while the declaration three lines below says 164.

**(b) K17 — host-census-gate capability row, `SCORECARD.md:3041` (same cause)**

Stated: "selftest prints PASS (162 cases, 162 passed, 0 failed)". Observed: 164. All three named paths
exist, so the path leg is green; only the case-count clause fails.
Reporting caveat for the L1: in the JSON, `stated` and `observed` for K17 are the **identical path
lists** (both 3 paths) — the case-count failure is visible only in `reason`
("host-census-gate row states 162 cases; the census selftest at this revision prints 164 cases"). A gate
that reads `stated == observed` would call K17 green. The check's subject text ("names only repository
paths that exist at the revision") also does not describe its case-count clause.

**(c) K10 — depth row, `SCORECARD.md:3029` (inherited at base, worsened this round)**

Stated: "`corpus/lessons/` 68 files (`find corpus/lessons -type f | wc -l`)". Observed: 70.
Two separate additions after the round-46 table was written:

| commit | change | count |
|---|---|---|
| `3c738a87` round-46 verifier spot-check | `A corpus/lessons/round-46-verifier-spotcheck.md` | 68 → 69 |
| `3629c46a` round-47 C2 | `A corpus/lessons/round-47.md` | 69 → 70 |

`3c738a87` is an ancestor of the round-47 base (`git merge-base --is-ancestor 3c738a87 9160190…` →
true), which is why the base read is already FAIL (68 vs 69). This is the known recurrence pattern:
rounds 38/39, 40/41 and 44/45 each carried a K10 red in the declaration text
(`SCORECARD.md:2272`, `:2433`, `:2857`).

**(d) The calibration cell itself (`SCORECARD.md:3033`) is not falsified — but it is not a live gate**

"…`mismatches 0 required at the round-46 outcome commit`". Verified literally true: at `b313963c` the
counter prints `checked 27, mismatches 0, PASS`, exit 0 (`out-r46outcome.json`). K05 stays `match`
because the round-46 outcome records unchanged ordinals. Read as "the tree is green now", it is false:
red at base (1) and red at the freeze (3).

## 4. Independent confirmation of the 164 figure (not the counter's word)

`git archive 77e9e2b2 | tar -x` into scratch, then
`env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=<clean> bash tools/tsukuroi-census.sh --selftest`:
`TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`, `rc=0` (`census-clean.txt`), and with
`TMPDIR="…/sp 2"`: same line, `rc=0` (`census-space.txt`). Two runs, serialized (cost rule).

## 5. Structural finding for the closure (why no seat can repair this inside w1)

* The round-47 declaration (`SCORECARD.md:3053`) appends **no** `## Axes — …` section; the last one is the
  round-46 table (`:3023`), which is what the counter measures (`declaring_round 46`, `axes_heading`
  "round 46 final measured surface"). So *any* round-47 tree drift lands on the round-46 cells, and only
  the round-47 outcome table can clear it.
* The round-47 declaration's round-start receipts list sources census + C1 before + C2 before
  (`SCORECARD.md:3059-3061`, `LOG.md:1678-1682`) but **no self-assessment receipt**, although the
  calibration counter was already FAIL (1 mismatch) at that base. Round 45 disclosed exactly this class
  at its own base (`SCORECARD.md:2857`: "self-assessment FAIL 1 mismatch (K10, the closure's spot-check
  file makes 65 lessons)"). Recording the base red would keep the round-47 outcome honest about what it
  repairs vs what it inherits.
* Ordering hazard at the outcome: K10 tracks a *file count*, so a spot-check/closure lesson file
  committed after the outcome table is written re-reds K10 (the pattern above). Write the depth count
  from the outcome commit itself, or re-run the counter after the closure lesson lands.

## 6. Exact replacement values if the outcome table is written (suggestion, not a draft request)

* `SCORECARD.md:3029` depth cell: `corpus/lessons/` **70** files at `77e9e2b2` (re-derive with
  `find corpus/lessons -type f | wc -l` at the outcome commit).
* `SCORECARD.md:3031` operability cell and `SCORECARD.md:3041` host-census-gate cell: `PASS (164 cases,
  164 passed, 0 failed)`.
* Acceptance at closure: `check-self-assessment.py --revision <outcome REV>` ⇒ `mismatches 0`, exit 0
  (that is the only form of the calibration claim that has held before, e.g. `b313963c`).

## 7. What I did not do

* Did not run the C1 admission counter (`check-scrub-admission-r47.py`) or C2's frozen counting command in
  its declared shape — other seats own those; the census selftest was run only to settle K13/K17's
  observed value.
* Did not write anywhere in the lane except this report and my seat receipt dir; no git/jj mutation, no
  host change. No tools installed, so nothing to record under the tooling directive.
