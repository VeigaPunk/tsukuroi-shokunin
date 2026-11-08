# tsukuroi — round 98 report

Lane: `tsukuroi-shokunin` (operability + freshness; host operability and repair). Campaign: hyaku,
run 15. Round 98, attempt 1. Pre-round tip `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`; freeze
`1cfeb5d5`; wave `WAVE_COMMIT`; settle `SETTLE_COMMIT` (lane tip at filing — `git ls-remote origin
refs/heads/master` prints `LANE_TIP`).

Declared claims — **C1 depth 8** (the tie-lowest non-retired axis): the two r97 families assert the
JSON metadata their own cases emit (the r97 A7 limit closed) and the LZ docstring's text-comparer
sentence is corrected (R97-D3/A6); **C2 freshness 9**: the registry-content checker binds the
comma-span form and its selftest covers the non-contiguous `VARIANTS` branch (the r97 MutRegistry
M08 survivor). Adjacency (8, tied lowest) carried no claim: the kaidoku/revenger
reverse-engineering ownership is operator-owned and unruled.

## Work performed

- **C1 — depth.** `tools/limine-pin-battery-r98.py` keeps the r97 roster at 105 and sets
  `check_echo` + `check_era` on `REFUSAL-VERSIONS-9DIGIT-Z` and `LEADING-ZERO-NORMALIZE`, so each
  case asserts `limine_version` (the flag spelling verbatim, source `flag`) and `visibility_era`
  (the label the whole tuple selects); `fam_leading_zero_normalize`'s docstring now names the real
  text-comparer discriminator (`12.000000009.000000005`, text orders era A while `int()` reads
  12.9.5). `tools/make-r98-bends.py` emits the two one-clause bends `N07-era-field-lie` (label
  swapped only for Z/LZ spellings) and `N08-echo-norm` (echo replaced by the numeric tuple).
  Evidence: `before/dev/c1-gate-runs3.json` (`105/105 met` x3), `w1/ExecBends/` (N07 `103/105` x3
  canonical + x3 clone; N08 `104/105` x3 both layouts; 0 error rows), `w1/ExecDoNothing/` (r97
  control `met 105/105` x3 on the gate and on both bends, byte-identical control `e678c34f…`),
  `w1/ExecGateRuns/` (landed gate x3 canonical + x3 clone), `w1/ReviewBattery/` (five attack gates:
  era-lie-everywhere `102/105`, fixed-echo `93/105`, X-cap-only lie `104/105`, source-lie `102/105`,
  echo-truncation `3/105`).
- **C2 — freshness.** `tools/check-registry-content-r98.py` extends the `RC-BEND-SPAN` capture to
  `N<digits>-N<digits>|N<digits>(,N<digits>)+` and adds `span-gap` / `span-gap-lie` selftest cases
  (12 → 14). Evidence: `before/dev/c2-selftest-r98.txt` (`PASS 14/14`), `before/dev/c2-selftest-r97.txt`
  (`PASS 12/12`), `before/dev/c2-m08-selftest.txt` (M08 `FAIL 12/14`, exactly the two gap cases red),
  `before/dev/c2-doctored-summary.txt` and `w1/ExecRegistry/` (D1 `FAIL` one `RC-VALUE-MISMATCH` vs
  r97 `RC-CELL-MISSING`; D2 `PASS` with M08 `FAIL`; D2lie inverts both; coverage `PASS 157/157
  findings 0` on every doctored revision), `w1/ReviewRegistry/` (independent rebuild of the same
  three revisions from the frozen ids), `w1/MutRegistry/` (checker mutant battery: M08 killed;
  M07 survives — routed).
- **Frontier step.** S394 opened and admitted (own-work: the gate's report contract at its MAIN
  return, bytes 16931/17037, with the early-return copies at 11230/11344 — S394 *supersedes* S393,
  whose anchor labelled the early-return pair as the main return; the ScoutSources seat found it,
  `w1/ScoutSources/report.md` §2); S392 re-opened byte-identical (`d92580dd…`, 331022 bytes, all
  three offsets re-measured with `grep -abo`); one candidate rejected (`limine` v12.9.6 `CONFIG.md`,
  HTTP 200 / 27609 bytes / `f44f3a19…`, zero occurrences of the gate's JSON fields or of `echo`).
  `corpus/lessons/round-98.md` carries `## Gate` (2 admits + 1 reject + the in-place change log),
  three mined mistakes (R98-FIELD-NOT-ASSERTED, R98-ANCHOR-FIRST-SITE, R98-SPAN-BRANCH-UNTESTED),
  the census block and the routed table; `corpus/README.md` gains § "Round 98" and its Frontier.
- **Wave.** One v1 wave, 14 seats under `ufo-wave-policy.json` (band 8-16): 5 executors, 2 scouts,
  2 scribes, 2 reviewers, 1 critic, 1 mutation-tester, 1 connector; attack roles by the prefile
  gate's set = 5/14 = **36 %** (floor 25 %), connector seats 1 (limit 2). Validator counts
  **14 spawn / 0 resume / 14 total**, `w1-validate.err` 0 bytes; `.ready` taken 10:02:04; seats
  settled `WAVE_SETTLE_NOTE`. Residual call: none (14 ≥ the 8 protocol floor).
- **Ledger.** `.ufo/waves/round-98/claim-falsification.tsv`, `LEDGER_COUNT` rows covering C1 and C2
  and every attack seat, with `LEDGER_VERDICTS`; the two wording/number rows name
  `before/plan-amendments-r98.md` A1/A2. Gate output pasted below.
- **Stale-lane:** respawn-per-round driver; no other mission of this lane is open. The wave's
  `.ready` was taken 10:02:04 and every seat settled before filing; nothing stayed open past the
  driver's two-tick window.
- **Inherited state.** No uncommitted lane-authored leftovers from an earlier attempt (the round's
  own work only). No `round-*-aggregator-*` or `round-*-verifier-spotcheck.md` file was edited.
- **Misroot sweep.** `git -C /home/vgpnk/Projects/shokunin status --porcelain` — MISROOT_NOTE.
- **Tool installs:** none (python3 3.14.8, git 2.56.0, curl 8.23.0, bwrap already present; pacman
  untouched and paused).
- **L0:** no new question. The r86 host-incident line stays open (operator-owned repair of the two
  UKI digests); nothing in this round touches /boot.

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| freeze: r98 battery + bends generator + r98 checker, plan, claims, controls, bends, doctored fixtures, dev receipts, S393 + knowledge entry | `Round 98 — freeze` | `1cfeb5d5` |
| wave evidence: spec + dispatch + ready, 14 seat dirs and reports, `w1-results.json`, amendments A1/A2, ledger | `Round 98 — wave` | `WAVE_COMMIT` |
| settle: S394 (supersedes S393) + entry correction + lesson (3 mistakes), README § Round 98, SCORECARD declaration + measured rows, three registry rows, LOG entries | `Round 98 — settle` | `SETTLE_COMMIT` |

Every commit above is a `jj-lane.sh` `landed <hash>` line after remote verification; the lane tip
equals `git ls-remote origin refs/heads/master` (below).

## Before → after measurements

### C1 (depth 8)

Counting command: `python3 tools/limine-pin-battery-r98.py --gate <GATE> --runs 3 --work <scratch>
--json <out>`, parsed by `python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family
REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE`; bends via
`before/controls/bends/<bend>.py`; do-nothing via `before/controls/do-nothing-battery-r97.py`.

| leg | before (r97 instrument `e678c34f…`) | after (r98) | receipt |
|---|---|---|---|
| landed gate, canonical | `met 105/105` x3, 0 error rows | `met 105/105` x3, `[]`, 0 error rows | `before/dev/c1-gate-runs3.json`; `w1/ExecGateRuns/c1-gate-canonical.json` |
| landed gate, clone | — | `met 105/105` x3, 0 error rows | `w1/ExecGateRuns/c1-gate-clone.json` |
| `N07-era-field-lie` | `met 105/105` x3 (blind) | `103/105` x3 both layouts, `[LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]`, 0 error rows | `w1/ExecBends/c1-bend-N07-era-field-lie-{canonical,clone}.json` |
| `N08-echo-norm` | `met 105/105` x3 (blind) | `104/105` x3 both layouts, `[LEADING-ZERO-NORMALIZE]`, 0 error rows | `w1/ExecBends/c1-bend-N08-echo-norm-{canonical,clone}.json` |
| roster | 105 | 105 (`len(FAMILY_ROSTER)=105`, `tuple(FAMILIES)==FAMILY_ROSTER True`, `cases 420`) | `w1/ExecGateRuns/` roster receipt |

### C2 (freshness 9)

Counting command: `python3 tools/check-registry-content-r98.py --revision <REV> --json <out>` and
`--selftest`; the doctored legs are reproduced by
`sh .ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh`.

| leg | before (r97 checker `2daf5926…`) | after (r98) | receipt |
|---|---|---|---|
| landed revision | `PASS 7/7` | `PASS 7/7` | `before/dev/c2-content-landed-{r97,r98}.txt` |
| selftest | `PASS 12/12` | `PASS 14/14` | `before/dev/c2-selftest-{r97,r98}.txt` |
| M08 one-fault mutant | `PASS 12/12` (survives) | `FAIL 12/14` (span-gap + span-gap-lie red) | `before/dev/c2-m08-selftest.txt`; `w1/ExecRegistry/report.md` |
| D1 (row `N01-N04` → `N01,N03`) | `RC-CELL-MISSING` | `FAIL` exactly one `RC-VALUE-MISMATCH` (derives `N01-N04`) | `before/dev/c2-D1-*.txt`; `w1/ReviewRegistry/report.md` |
| D2 (keys `N01,N03`, row `N01,N03`) | `RC-CELL-MISSING` | `PASS 7/7`; M08 `FAIL` one | `before/dev/c2-D2-*.txt`; `w1/ExecRegistry/` |
| D2lie (keys `N01,N03`, row `N01-N03`) | `RC-VALUE-MISMATCH` | `FAIL` one; M08 `PASS` | `before/dev/c2-D2lie-*.txt` |
| coverage on each doctored revision | `PASS 157/157` | `PASS 157/157 findings 0` (blindness leg holds) | `before/dev/c2-D*-coverage.json` |
| settled tip | coverage `PASS 157/157` | content `PASS 7/7`; coverage `PASS 160/160` after the three r98 rows | `after/c2/`; `after/c2/coverage-tip.json` |

Instrument integrity at scoring: `sha256sum -c before/instruments.sha256` → 27 OK (gate
`7d79ac29…`, battery-r98 `8198bd84…`, checker-r98 `5bb1441e…`, bends `2d8f4f6e…` / `45d8d00d…`,
controls `e678c34f…` / `7d79ac29…` / `2daf5926…`). The r97 battery and checker keep their landed
bytes; both are this round's do-nothing controls.

## Sources & frontier

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before `git show b3be3f90:corpus/SOURCES.md` → exit 0, 392 rows
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → 392); after the landed tree → **394 rows, exit 0, 0 E
findings** (57 W04 + 1 W01, the standing warning set). Rows added by tier: two A (S393 own-work,
S394 own-work superseding S393). Rows touched old→new: S393 `status` `mined` → `queued` and
`used-by` `corpus/knowledge/limine-metadata-assertions-r98.md` → `—` (S394 carries the citations);
all three changes are logged in the lesson's in-place table. Frontier rows advanced: the r97
Frontier's A7 (field/echo coverage of the new members) and M08 (selftest case) are closed; the
r97 C2 gaps (150 unbound rows, co-doctoring, printed tally) stay open, and the wave added three
new ones (hybrid comma cell F1, duplicate mention F2, M07's untested ancestor branch) — all in
`corpus/README.md` § "Frontier (round-98 addition)" and routed to r99. Assimilation: none this
round (`merge/tsukuroi/` unchanged; `considerthese/2026-10-26.md` was surveyed by the connector —
"Cross-note correction propagation map" implemented under QUALITY 108, "Downstream patch-offset
check" partial).

## Trend verdicts

- **expansion — improved.** Two admitted own-work rows (S393 and its correction S394) and one new
  knowledge entry (`corpus/knowledge/limine-metadata-assertions-r98.md`, PC1-PC3 + limits) on
  ground the coverage map did not hold (the gate's *reported* metadata, which no lane entry
  covered); S392 re-opened byte-identical; net +2 rows (392 → 394), none removed.
- **quality — improved.** The r97 A7 limit is closed by two bends the r97 instrument is blind to
  (`met 105/105` → `103/105` / `104/105`), the r97 M08 survivor is killed by two selftest cases and
  a doctored revision pair that inverts under the mutant, and the r97 docstring defect (second
  instance of its class in two rounds) is corrected in the successor with its manifest relation
  stated. No admitted entry fails its re-check.
- **discernment — improved.** The lane's own anchor was caught by a seat (S393's byte pair named
  the early return; S394 states both sites), the reviewer found two false-PASS shapes in the new
  capture (F1 hybrid, F2 duplicate) that are recorded as named limits rather than smoothed, and a
  wave receipt that measured a *different* mutant than the one it named is recorded as A2 instead
  of being cited for the M08 kill. Three mistakes are mined with red-before/green-after pairs.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence:
  the health-verdict decision table (`SKILL.md:38-50`), the update-safety checklist
  (`SKILL.md:90-141`), the error-pattern list (`SKILL.md:2028-2036`), the registry section the round
  extends (`SKILL.md:5777-5946`); non-author verification still owed.
- [~] At least one end-to-end domain task executed and logged in LOG.md — evidence: the C1
  certification run (`w1/ExecGateRuns/`, `w1/ExecBends/`) and the C2 doctored legs
  (`w1/ExecRegistry/`) are end-to-end executions of the lane's own gates; `LOG.md` "Round 98"
  entries.
- [~] Instructions executable by an agent without oral context — evidence: the round's instruments
  carry their contract in the registry rows (`SKILL.md:5944-5946`) and their docstrings; the wave
  seats executed them from those instructions alone. Whole-SKILL replay remains unexecuted.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — evidence: `PROVINCE.md` unchanged this
  round; the connector's 20-sibling sweep found no duplicate or contradictory claim
  (`w1/ConnectorOverlap/report.md`); kaidoku/revenger ownership stays operator-owned and unruled.

## Prefile falsification gate

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi
--round 98` → `PREFILE_GATE_LINE` (exit `PREFILE_GATE_RC`).
