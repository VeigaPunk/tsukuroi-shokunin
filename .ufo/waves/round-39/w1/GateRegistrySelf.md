VERDICT: defect-found

Item G-2: re-ran the two fixed gates at the round-39 tip and at the base. `check-registry-coverage.py`
PASSes at both; `check-self-assessment.py` FAILs at both (base 1 mismatch, tip 6). Five of the six tip
reds are round-39 content that the round-38 axes/capabilities rows were never updated for; the sixth (K10)
is a pre-existing red introduced by the round-38 verifier spot-check commit, not by round 39. The
calibration row's own claim (`SCORECARD.md:2191`, "mismatches 0 required at the round-38 tip") is already
false at the base.

## 1. Runs (TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/GateRegistrySelf, cwd = lane root)

Both revisions are commits in the lane and ancestors of `master` at `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`
(the tool reports `branch_tip` itself; `revs.json` names the same tip). Both tools read through Git, never
the working tree. The working tree carried concurrent sibling edits during these runs (`PROVINCE.md`,
`SKILL.md` shown modified by others); because both tools resolve every input with `git show`/`git ls-tree`/
`git archive` at the named revision, those edits cannot influence any number below.

| command | exit | summary |
|---|---|---|
| `python3 tools/check-registry-coverage.py --revision 2e1c2a40…` | 0 | status PASS, findings 0, missing 0, registered 60, rows_total 60, tools_total 60 |
| `python3 tools/check-registry-coverage.py --revision 0eff65b2…` | 0 | status PASS, findings 0, missing 0, registered 58, rows_total 58, tools_total 58 |
| `python3 tools/check-self-assessment.py --revision 2e1c2a40…` | 1 | checked 27, mismatches 6, FAIL: K07 K08 K09 K10 K13 K17 |
| `python3 tools/check-self-assessment.py --revision 0eff65b2…` | 1 | checked 27, mismatches 1, FAIL: K10 |

Tool sources are identical at both revisions (`git show <rev>:tools/check-self-assessment.py | sha256sum`
→ `1e1ab6113d665684…` at both; `check-registry-coverage.py` → `6fcb2d0a5f1b2493…` at both), so the
difference between the two runs is lane content only.

## 2. Registry coverage — no red at either revision

`registered` rises 58 → 60 because round-39's freeze commit `6a08925` added two rows to the gate registry:
`SKILL.md:3116` (`storage-hidden-r39` → `tools/score-storage-hidden-r39.py`) and `SKILL.md:3117`
(`transaction-order-r39` → `tools/check-transaction-order-r39.py`); both tools exist at the tip and every
other row's tool exists, so `missing 0`. This is the correctly-updated surface; nothing to attribute.

## 3. Self-assessment reds at the tip, with round-39 cause

`stated_line` values are SCORECARD lines at the tip; observed values are the tool's own measurement at that
revision (transcripts: `selfassess-2e1c2a40….json`).

| ID | stated → observed | round-39 cause |
|---|---|---|
| K07 | 59 → 60 `corpus/knowledge/*.md` (`SCORECARD.md:2187`) | `4078eb2` added `corpus/knowledge/pacman-transaction-order-r39.md` (58 new lines; `source:` line cites S208/S213–S218). Depth row still says 59. |
| K08 | 3201 → 3203 SKILL.md newlines (`SCORECARD.md:2187`) | `6a08925` added the two registry rows at `SKILL.md:3116-3117` (+2 lines). |
| K09 | 861 → 863 pipe-prefixed lines (`SCORECARD.md:2187`) | Same two registry rows (`SKILL.md:3116-3117`). |
| K10 | 52 → 53 `corpus/lessons/` files (`SCORECARD.md:2187`) | **Not round 39.** Already red at the base: `0eff65b` (round-38 verifier spot-check) added `corpus/lessons/round-38-verifier-spotcheck.md`, taking lessons 52 → 53 (`fc931bd` 52, `f8b4df2` 52, `0eff65b` 53). Round 39 changed nothing under `corpus/lessons/`. |
| K13 | 113 → 117 census selftest cases (`SCORECARD.md:2189`) | C1 commit `49cc53c7` added four `probe_storage_arm` selftest cases — `tools/tsukuroi-census.sh:2974` `storage-hidden-absent`, `:2979` `storage-hidden-empty`, `:2984` `storage-mounts-unreadable`, `:2989` `storage-mounted-populated`. Measured: base archive prints `PASS (113 cases…)`, tip archive `PASS (117 cases…)`. |
| K17 | host-census-gate row 113 → 117 cases (`SCORECARD.md:2199`) | Same four cases from `49cc53c7`; the capabilities row also states 113. |

K17's subject line is the path-existence check, but for `host-census-gate` the implementation
(`tools/check-self-assessment.py:702-712`) also compares that row's case count against the census count
measured for K13; the named paths themselves are identical and all exist, so the red is purely the stale
113.

## 4. Calibration finding (pre-existing, no round-39 cause)

- `SCORECARD.md:2191` (calibration row): "mismatches 0 required at the round-38 tip". At the round-38 tip
  used as this round's base (`0eff65b`), the tool reports **checked 27, mismatches 1, FAIL, exit 1** (K10).
- Provenance run: `f8b4df2` ("round-38: final gate receipts (self-assessment 27/0, nine lane gates PASS …)")
  → **checked 27, mismatches 0, exit 0**; the very next commit `0eff65b` → 1 mismatch. The intervening
  commit added one lesson file and did not update the depth row or re-run the gate, so the round-38
  "27/0" receipt no longer describes the round-38 tip. Transcripts: `selfassess-f8b4df2.json`,
  `selfassess-0eff65b2….json`.
- Consequence for adjudication: the base's self-assessment surface is already red, so "self-assessment
  red at the tip" cannot by itself be charged to round 39; five of the six tip reds are round-39
  additions (K07/K08/K09/K13/K17) and one (K10) is inherited. All six are stale-count rows; none
  indicates a counter, census or registry behavioural defect.

## 5. What was not done

- Did not run either tool's `--selftest` mode (item asked for `--revision` runs at two revisions).
- Did not run the C1/C2 counters or judge the TO rows; that is other seats' scope.
- Did not edit any lane file (no SCORECARD row fixed here). The closure edits implied by §3 are:
  `SCORECARD.md:2187` depth row 59→60 notes / 3201→3203 lines / 861→863 table lines / 52→53 lessons;
  `SCORECARD.md:2189` and `SCORECARD.md:2199` 113→117 cases; and a calibration row (`SCORECARD.md:2191`)
  that states the measured revision and its actual mismatch count.
- No tool installed or upgraded; no host, sysfs, service, mount or git state touched (read-only git
  plumbing only); scratch removed after receipts were copied.

## 6. Receipts (this seat dir)

`registry-2e1c2a40….json`, `registry-0eff65b2….json`, `selfassess-2e1c2a40….json`,
`selfassess-0eff65b2….json` (the four requested runs); `selfassess-f8b4df2.json`,
`selfassess-b0005ae.json` (provenance); `census-selftest-x-base.log`, `census-selftest-x-tip.log`
(113 vs 117 cases from `git archive` extracts); `run-commands.txt` (exact commands, exit codes, hashes).
