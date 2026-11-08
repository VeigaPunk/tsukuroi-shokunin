# tsukuroi — round 97 report (draft; file only after WAVE-DONE)

Claims: **C1** depth 8 (tied lowest, non-retired) — the Limine version gate's published 1-9-digit
cap certified at its THIRD component and the accepted leading-zero form; **C2** freshness 9 — a
registry row's declared values re-derived from the tool bytes each row names. Frozen at
`a57e88cd57f30bae206d908b534508d9463bf734`; pre-round tip `f48d16428d8bb92fd6cf546a745bff5b624e3f18`.

## Work performed

- **C1 — depth.** `tools/limine-pin-battery-r97.py` (roster 103 → 105) adds
  `REFUSAL-VERSIONS-9DIGIT-Z` (`12.9.999999999` era B, `0.9.999999999` era A) and
  `LEADING-ZERO-NORMALIZE` (`12.09.4`, `000000012.9.4`, `12.000000009.000000005`,
  `000000000.000000000.000000000`); `tools/make-r97-bends.py` emits the two one-clause bends
  `N05-z-cap-8` and `N06-leading-zero-reject`. Evidence: `before/dev/c1-battery-gate.txt`
  (`105/105 met`), `w1/ExecBattery/report.md` (×3 canonical + ×3 clone, `105/105`, 0 error rows),
  `w1/ExecBend.md` (N05 `103/105` two families, 6 rc-64 rows; N06 `104/105` one family, 4 rows;
  ×3 both layouts), `w1/ExecDoNothing.md` (r96 control `f06d90ae…` byte-identical to
  `f48d1642:tools/limine-pin-battery-r96.py`, `met 103/103` ×3 on the gate and on both bends).
- **C2 — freshness.** `tools/check-registry-content.py` binds seven cells over four rows
  (`limine-pins` default/tally/schema; the r96 battery's roster in two cells; the r96 calibration
  checker's tally; the r96 bends generator's span) and re-derives each from the tool's bytes.
  Evidence: `w1/ExecRegistryContent/report.md` (landed `PASS 7/7`; `--selftest PASS 12/12`; doctored
  `FAIL` with six `RC-VALUE-MISMATCH`; coverage `PASS 154/154` on the same revision),
  `w1/ReviewRegistryContent.md` (constant-derivation patch flips `FAIL → PASS`; six fail-closed
  paths), `w1/MutRegistry.md` (6/8 mutants killed).
- **Frontier step.** S392 opened and admitted (CPython `int()` docs); S389/S391 re-opened
  byte-identical; one candidate rejected (`man.archlinux.org/man/python.1`, HTTP 200, 41 788 bytes,
  no `int()` or Limine behaviour). Lesson `corpus/lessons/round-97.md` with `## Gate`, three mined
  mistakes, the census and the routed table.
- **Wave.** One v1 wave, 14 seats under `ufo-wave-policy.json` (band 8-16): 5 executors
  (`ExecBattery`, `ExecBend`, `ExecDoNothing`, `ExecRegistryContent`, `ExecGateHygiene`), 2 scouts
  (`ScoutSources`, `ScoutDrift`), 2 scribes (`ScribeKnowledge`, `ScribeLesson`), 2 reviewers
  (`ReviewBattery`, `ReviewRegistryContent`), 1 critic (`CriticClaims`), 1 mutation-tester
  (`MutRegistry`), 1 connector (`ConnectorOverlap`); attack roles by the prefile gate's set = 5/14 =
  36 % (floor 25 %); connector seats 1 (limit 2). Validator counts 14 spawn / 0 resume / 14 total,
  `w1-validate.err` 0 bytes. Dead/silent seats: <fill>. Residual call: none (14 ≥ the 8 protocol
  floor; no item left outside the wave).
- **Round-97 prefile falsification ledger**: <fill>.
- **Stale-lane**: respawn-per-round driver; no other mission of this lane is open.
- **Tool installs**: none this round (python3 + git + curl already present; pacman untouched and
  paused host-wide).
- **L0**: no new question filed; the r92 GH013 line is already answered in-file, and the r86 host
  incident line stays open (operator-owned repair).

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| freeze: r97 battery, bends generator, registry-content checker, plan, claims, controls, dev receipts, r96 leftover receipt | round-97 freeze | `a57e88cd` |
| wave evidence (spec, dispatch, ready, 14 seat dirs + reports) | round-97 wave | <fill> |
| corpus: S392 row, `knowledge/limine-bound-9digit-z-r97.md`, `lessons/round-97.md` | round-97 corpus | <fill> |
| SKILL.md: three r97 registry rows (`limine-pin-battery-r97`, `make-r97-bends`, `check-registry-content`) | round-97 registry | <fill> |
| SCORECARD round-97 declaration + measured outcome + capability row; LOG entry | round-97 settle | <fill> |
| `tools/limine-pin-battery-r96.py` docstring correction (routed r96 defect 2/3) | round-97 settle | <fill> |

## Before → after measurements

### C1 (depth 8)

Counting command:
`python3 tools/limine-pin-battery-r97.py --gate <GATE> --runs 3 --work <scratch> --json <out>` then
`python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT-Z
--family LEADING-ZERO-NORMALIZE`; bends through `.ufo/waves/round-97/before/controls/bends/<bend>.py`;
do-nothing through `.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`.

| leg | before (r96 instrument, `f06d90ae…`) | after (r97 instrument) | receipt |
|---|---|---|---|
| landed gate, canonical | `met 103/103` ×3, 0 error rows | `met 105/105` ×3, `failed_families []`, 0 error rows | `w1/ExecBattery/c1-gate-canonical.json` |
| landed gate, `git clone --shared` | — | `met 105/105` ×3, 0 error rows | `w1/ExecBattery/c1-gate-clone.json` |
| `N05-z-cap-8` | `met 103/103` ×3 (blind) | `103/105` ×3, `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 6 rc-64 rows | `w1/ExecBend/c1-bend-N05-*-{canonical,clone}.json` |
| `N06-leading-zero-reject` | `met 103/103` ×3 (blind) | `104/105` ×3, `[LEADING-ZERO-NORMALIZE]`, 4 rc-64 rows | `w1/ExecBend/c1-bend-N06-*-{canonical,clone}.json` |
| roster | 103 families | 105 families | `--selftest` `roster-literal PASS families_passed=105` |

Measured against `a57e88cd` (freeze) for the instruments; the landed tip for the settle re-run.

### C2 (freshness 9)

Counting command: `python3 tools/check-registry-content.py --revision <REV> --json <out>` and
`--selftest`; the doctored leg is `sh .ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh`
(base pinned `f48d1642`).

| leg | before | after | receipt |
|---|---|---|---|
| landed revision | no such checker; coverage gate row-presence only | `status PASS`, `bindings 7`, `findings []` | `w1/ExecRegistryContent/01-landed-content.txt` (`a57e88cd`) |
| selftest | — | `PASS 12/12`, each one-cell doctor id-exact | `w1/ExecRegistryContent/02-selftest.txt` |
| doctored revision (base `f48d1642`) | coverage gate `PASS 154/154` on the same doctored table | content `FAIL`, six `RC-VALUE-MISMATCH`, rc 1 | `before/dev/c2-content-doctored.txt` (`46fae1ba`), `w1/ExecRegistryContent/05b-doctored2-content.txt` (`9e052291`) |
| coverage on the doctored revision | `PASS 154/154 findings 0` (blind) | `PASS 154/154 findings 0` (still blind — the blindness leg) | `before/dev/c2-coverage-doctored.json`, `w1/ExecRegistryContent/06b-doctored2-coverage.txt` |
| settled tip | — | content `PASS 7/7`; coverage `PASS 157/157` (the three r97 rows) | <fill: settle receipts> |
| fail-closed | — | missing tool `RC-DERIVE-FAILED`; missing row `RC-ROW-MISSING`; 7-col table rc 2; non-ancestor rc 2 | `w1/ReviewRegistryContent/receipts/04-*` |

## Sources & frontier

`SOURCES.md` rows before → after: 391 → 392
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`; before from `git show
f48d1642:corpus/SOURCES.md`). Rows added by tier: one A (S392). Rows touched old→new: none —
S389/S391 were re-opened byte-identical and their `status`/`used-by` did not change. Frontier rows
advanced: the r96 Frontier's "Z component's 9-digit boundary is uncertified" and "a 9-digit
component with leading zeros is unsent" are now families with their own bends; the r95/r96
"registry certifies row presence, not content" is closed for seven cells and stays a named limit for
the other 150 rows. Census command and both exits:
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → start `exit 0`
(391 rows), end `exit 0` (<fill> rows, 0 E findings).

Assimilation: none — the shokuknow package was not adopted this round (its staged ids still collide
with the lane registry; adoption stays opt-in and none of this round's claims needs it).

## Trend verdicts

- **expansion — <fill>.** S392 admitted on new ground (the `int()` string form) with a located quote;
  the knowledge entry `limine-bound-9digit-z-r97.md` cites S389/S391/S392 and the lane's own tools.
- **quality — <fill>.** The r96 docstring defect is corrected in both the successor and the r96 tool
  with its manifest relation; two families close named Frontier limits; C2 adds a drift gate.
- **discernment — <fill>.** The wave produced <fill> narrowings (A1-A5) and <fill> survivors
  (M07/M08, the three C2 gaps); every one is recorded as a limit or routed, none left silent.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — pointers
  SKILL.md:38 (health-verdict decision table), :90 (update-safety checklist), :2028 (error patterns),
  :179 (Sources); this round adds the three r97 registry rows at SKILL.md:5941-5943, each with its
  entry command, verdict map, self-test and pinned values.
- [~] At least one end-to-end domain task executed and logged in LOG.md — the historical pointer is
  `corpus/knowledge/host-health-report-r3.md` + LOG round 3; this round's executable end-to-end check
  is the doctored-fixture discrimination: `before/fixtures/build-doctored-fixture.sh` runs from a
  clean clone to a `FAIL`/`PASS` pair (doctored `46fae1ba`, receipts `before/dev/c2-*`), and the
  wave reproduced it independently (`w1/ExecRegistryContent`, `9e052291`).
- [~] Instructions executable by an agent without oral context — the round's two recipes
  (`before/dev/run-dev.sh`, `before/fixtures/build-doctored-fixture.sh`) were executed end-to-end
  this round with no oral context and are self-contained (absolute paths, pinned base, asserts); the
  whole-SKILL replay remains unexecuted (unchanged from prior rounds).
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md` ADJ-01..07 unchanged;
  `w1/ConnectorOverlap.md` swept all 20 sibling repos (`registry-content`, `leading zero`,
  `leading-zero`, `9-digit`, `FAMILY_ROSTER`, registry-cell checkers): 0 duplicate claims,
  0 contradictions, and 0 collisions with the open L0 lines it read.
