VERDICT: draft

# Seat ScribeLog — item F-5, round-48 LOG.md entry (report text only)

Draft for the L1 to append to `LOG.md` at integration. Nothing here is a measurement of the
wave: every number is either quoted from a frozen receipt or a placeholder the L1 fills. No
counter, selftest, battery, wave or git-writing command was run by this seat; the only commands
were reads (`git show` at the freeze, `sha256sum`, `grep`, `wc`, `sed`).

## Provenance and what I verified

- Freeze under test: `ae99f021b76f8eb1c8805d32d80644464afb1ff6`; base
  `5fdf062f969292736e36513e39f98b1b8de43635` (`git -C … show ae99f02…:SCORECARD.md`, section
  "Round 48 — declaration", line 1; `.ufo/waves/round-48/frozen/FROZEN.md`, "Base:" line). "Declaration line N" below
  counts lines within that section (`git show ae99f02…:SCORECARD.md | awk '/Round 48 — declaration/,0' | nl`), not
  `SCORECARD.md` line numbers.
- The three cited control summaries are byte-identical at the freeze and in the working tree
  (`sha256sum` 015aa0c04aa7… / 1167d1a46cc2… / aa5bc01201c7… on both sides), and `LOG.md` is
  unchanged since the freeze (7d59f90b47da… both sides). The draft therefore quotes the frozen
  bytes.
- House format read from the last three entries: `LOG.md:1615-1686` (`## Round 44`, `## Round 45`,
  `## Round 46`, `## Round 47`); entries are separated by a blank line and the file ends with a
  newline (`tail -c 40 LOG.md | xxd` → `…none.\n`). Rounds 45-47 end with the standing
  "Tool installs/updates: none." line.
- `corpus/lessons/round-48.md` does not exist at the freeze (`git ls-tree -r --name-only
  ae99f02… corpus/lessons | tail -8` ends at `round-47-verifier-spotcheck.md`), so the
  declaration's pointer for the two first-draft counter defects ("lesson `round-48.md`
  `## Mistakes`", declaration line 19) has no landed section yet. The two defect descriptions
  below come from the L1's own dispatch text for seat F-4 (`.ufo/waves/round-48/w2-spec.json`,
  item `ScribeLesson`): the suspension is disclosed in the draft rather than papered over.
- Frozen predicate code confirmed: `tools/score-selftest-tmpdir-r48.py:25,56-57,227-228` and
  `tools/check-scrub-admission-r48.py:81,365` carry the exact predicate strings; the C2 universe
  is `R48RevGR<n>{a,b,c}` + `R48CritGR<n>{a,b,c}` (`:86-87`); the wave has 71 items and exactly 18
  counted names (parsed from `.ufo/waves/round-48/w2-spec.json`, `items`).
- Not read, by rule: nothing under `.ufo/waves/round-48/w1/` was opened; only the SCORECARD
  declaration paragraph describing the incident is cited.

## Traceability of each number used in the draft

| Number / text | Source |
|---|---|
| base `5fdf062f…`, freeze `ae99f021…` | declaration line 1; `FROZEN.md` Base line; `git log -1 --format=%H` |
| four rejected closures r44-r47 | declaration line 3 |
| ordinals 8/9/9/9/9/8, saturation 9 / window 3 | declaration line 4 |
| attempt-1 details (32-seat `w1`, base `76819197`, no counter, empty `frozen/src`, seats stopped, void) | declaration lines 5-8 |
| sources census exit 0 | declaration line 9; `.ufo/waves/round-48/before/sources-census-start.txt` last line `tsukuroi ok …/corpus/SOURCES.md` |
| C1/C2 before FAIL, C3 before mismatches 1 (K10) | declaration lines 9-11; the quoted K0 lines below |
| C1 blob `375aa737…2426`, 166 cases | C1 K-pass line; declaration C1 row; counter `CASES_DEFAULT = 166` (`:54`) |
| C1 base blob `adb1b4ce…ceb41`, 164 cases | C1 K0 line; declaration C1 row |
| C2 row hashes GR1/GR2/GR3 | `FROZEN.md` row-hash line; frozen `gr-section-hashes.json`; counter run K0 (`structural_ok 1, quotes_ok 3`) |
| 18 counted seats, one wave | declaration C2 row; counter `universe()` `:86-87`; spec parse (18 matches) |
| C3 27 fixed checks, K10/K13/K17 | declaration C3 row; C3 K0/K0b lines in `battery-summary-r48-c3.jsonl` |
| battery totals 5/5, 14/14, 5/5 | `wc -l` 5/14/5; every line `"as_expected": true` |
| two first-draft counter defects | declaration line 19 (pointer); `w2-spec.json` F-4 dispatch text; fixes at `tools/check-scrub-admission-r48.py:167-215,341-353` and `tools/score-selftest-tmpdir-r48.py:55,81,110,139` |
| wave spec 71 seats | `git log -1 --format=%s 23f85377` → "round-48: w2 spec + validated dispatch (71 seats, policy v2)" |
| assimilation text (53 collisions S200-S252, one considerthese proposal) | declaration line 21 |

## Proposed LOG entry (append after `LOG.md:1686`, preceded by one blank line; exact text)

## Round 48 — 2026-10-28 (hyaku run 10; L1 TsukuroiR48a2, attempt 2)

Base `5fdf062f969292736e36513e39f98b1b8de43635`; freeze `ae99f021b76f8eb1c8805d32d80644464afb1ff6` (claims C1-C3, frozen
counters, pre-data control batteries, void-w1 incident record; `FROZEN.md` and the frozen digests under
`.ufo/waves/round-48/frozen/`). Fresh-start round after `rejected-harmed` (r44), `rejected-honest-stop` (r45),
`rejected-harmed` (r46), `rejected-honest-stop` (r47). Ordinals at base: depth 8, coverage 9, operability 9, freshness 9,
calibration 9, adjacency 8 (depth and adjacency tied lowest); saturation 9 / window 3. Round-start receipts: sources census
exit 0 (`.ufo/waves/round-48/before/sources-census-start.txt`); C1 and C2 before at base FAIL on their counters (K0 lines
below); C3 before mismatches 1 (K10).

**Attempt-1 incident (disclosed, void).** Attempt 1 dispatched a 32-seat `w1` before any freeze — wrong base `76819197` in
its context against the lane tip `5fdf062f`, no counter file, empty `frozen/src`; the orchestrator stopped its seats.
`.ufo/waves/round-48/w1*` are incident evidence only and are never scored (`SCORECARD.md`, "Round 48 — declaration").
Attempt 2 froze claims, counters and controls first and dispatches ONE v2 wave `w2` (71 items, 18 counted seats).

Claims (frozen predicates; measured only at the round's final lane revision):

| Claim | Axis | Counter (frozen) | Predicate | Before at base |
|---|---|---|---|---|
| C1 | operability (sourced: `proc_pid_fd(5)`, Bash manual, opened this round) | `python3 tools/score-selftest-tmpdir-r48.py --revision <REV>` | `pass_ok == 4 and loc_ok == 4 and clean_ok == 4 and failfast_ok == 2 and term_ok == 1 and static_ok == 1` | FAIL: `pass_ok 0, loc_ok 3, clean_ok 4, failfast_ok 1, term_ok 0, static_ok 0` on blob `adb1b4ce…ceb41` (164 cases) |
| C2 | depth (lowest-tied; sourced: S237, S240, S242-S249) | `python3 tools/check-scrub-admission-r48.py --revision <REV>` | `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3` | FAIL: `structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0` |
| C3 | calibration | `python3 tools/check-self-assessment.py --revision <REV>` (27 fixed checks) | status PASS, `checked` 27, `mismatches == 0` | FAIL: mismatches 1 (K10); 3 (K10, K13, K17) at the implementation commit |

C1's surface: the census selftest reaches a TMPDIR with refused characters through a `/proc/self/fd/24x` alias INSIDE that
TMPDIR (the r47 `st_base=/tmp` fallback, R47-C2-TMPDIR-FALLBACK, is removed); INT/TERM exit 130/143 with the fixture
removed; a nonexistent TMPDIR fails fast; two `(R48-C2)` cases; 166 cases on blob `375aa737…2426`. C2's surface: rows
GR1-GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` admitted by the 18 counted seats of this wave
(`R48RevGR<n>{a,b,c}`, `R48CritGR<n>{a,b,c}`), bound through their report files; GR2 carries the r47 correction; the K22
snapshot map gains S240 `ioctl.c`; a negative on the current row hash blocks the row whatever its citations; row hashes
GR1 `fe77ac76…9ca8`, GR2 `e0b391e1…52ce`, GR3 `43430a14…c32c`. C3's surface: the SCORECARD self-assessment restated at round
end — lesson-file count 70→71 and census case count 164→166. Frozen digests: census blob `375aa737…2426`, C1 counter
`8eead161…5640`, C2 counter `eab29058…84d4`, C3 counter `44b474fb…38e6` (`frozen/FROZEN.md`).

Pre-data controls (frozen counters, before any seat; `.ufo/waves/round-48/controls/`; all as expected: C1 5/5, C2 14/14,
C3 5/5). K0 and pass lines, verbatim:

```jsonl
{"case": "K0 do-nothing: base blob", "expected": "FAIL", "verdict": "FAIL", "legs": {"pass_ok": 0, "loc_ok": 3, "clean_ok": 4, "failfast_ok": 1, "term_ok": 0, "static_ok": 0}, "census_sha256": "adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41", "as_expected": true}
{"case": "K-pass: the fix revision", "expected": "PASS", "verdict": "PASS", "legs": {"pass_ok": 4, "loc_ok": 4, "clean_ok": 4, "failfast_ok": 2, "term_ok": 1, "static_ok": 1}, "census_sha256": "375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426", "as_expected": true}
{"case": "K0 do-nothing base", "expected": "FAIL", "verdict": "FAIL", "legs": {"structural_ok": 1, "quotes_ok": 3, "verdicts_ok": 0, "marks_ok": 0}, "as_expected": true}
{"case": "K9 full valid synthetic cohort + marks (counter can pass; fixture, not the live integration)", "expected": "PASS", "verdict": "PASS", "legs": {"structural_ok": 1, "quotes_ok": 3, "verdicts_ok": 3, "marks_ok": 3}, "as_expected": true}
{"case": "K0 do-nothing: base", "expected": "FAIL", "status": "FAIL", "mismatches": 1, "failed": ["K10"], "as_expected": true}
{"case": "K9 both fixed (synthetic; the live final is the claim)", "expected": "PASS", "status": "PASS", "mismatches": 0, "failed": [], "as_expected": true}
```

`battery-summary-r48-c3.jsonl` also carries `K0b` (implementation revision, SCORECARD untouched): `mismatches 3, failed
["K10", "K13", "K17"]`, the state C3's restatement clears; `K1` (lesson count only) reads 2 and `K2` (case counts only)
reads 1, so neither half alone passes.

Pre-data counter defects caught by the batteries (declaration; detail owed to the lesson's `## Mistakes`): the C2
counter's first draft dropped a format-thin `partly` in `bind` once the report's citations failed to resolve, so a bound
negative laundered itself away; the K3/K3b/K3c/K3d cases (bad citation, clean citations, self-contradiction, two-byte body)
now hold `verdicts_ok 2` and FAIL, and the fix binds the verdict before credit gates (`tools/check-scrub-admission-r48.py:167-215,341-353`).
The C1 counter's first draft searched the whole stdout for `PASS`, which every case line contains, so the term leg read a
clean exit as a surviving run; the K-pass run caught it, and the fix matches the full summary prefix and the last line
(`tools/score-selftest-tmpdir-r48.py:55,81,110,139`). The batteries otherwise fix these sensitivities pre-data: a candidate
that restores the `/tmp` fallback still passes `pass_ok 4, clean_ok 4, failfast_ok 2, term_ok 1` and is killed only by
`loc_ok 3` + `static_ok 0` (C1 K2); a candidate with the INT/TERM traps reverted is killed only by `term_ok 0` (C1 K3);
C2 K2 stale hash, K4 identical bodies, K5 missing critic, K6 unpinned citation, K7 no dispatch, K8 negating README mark and
F1a stray header all FAIL as designed.

**Measured — the L1 fills this block after the wave; no value below is measured yet.**

- C1: `python3 tools/score-selftest-tmpdir-r48.py --revision <FINAL>` → `<PASS|FAIL>`; `pass_ok <n>/4, loc_ok <n>/4,
  clean_ok <n>/4, failfast_ok <n>/2, term_ok <n>/1, static_ok <n>/1`; receipt `.ufo/waves/round-48/after/<file>`.
- C2: `python3 tools/check-scrub-admission-r48.py --revision <FINAL>` → `<PASS|FAIL>`; `structural_ok <n>, quotes_ok <n>/3,
  verdicts_ok <n>/3, marks_ok <n>/3`; per row `<GR1|GR2|GR3> <holds/partly/fails>`; receipt `<file>`.
- C3: `python3 tools/check-self-assessment.py --revision <FINAL>` → status `<…>`, `checked <n>`, mismatches `<n>`
  (`<ids>`); receipt `<file>`.
- Round shape: `w2` `<n>` seats dispatched / `<n>` settled / `<n>` dead / `<n>` unreported (`w2-results.json`); residual
  `<n>` (`<names>`); counted cohort 18/18 (`<n>` holds, `<n>` partly, `<n>` fails); `<n>` witnesses PASS / `<n>` FAIL;
  claims admitted `<C1/C2/C3 list>`; lesson `corpus/lessons/round-48.md`, report `.ufo/reports/round-48/tsukuroi.md`
  (fleet repo).

Assimilation: none this round (claims frozen before assimilation could be scoped; the staged `merge/tsukuroi` package keeps
its 53 id collisions S200-S252 — `.ufo/waves/round-48/assimilation/collisions`; `considerthese/`: one proposal mined by a
wave scout, landed only if the lane's own bar grounds it). Tool installs/updates: none.

## Notes for the L1 before appending

1. The six JSONL lines are copied byte-for-byte from the three summaries; re-quote from the files if the L1 reformats.
2. Reconcile the two first-draft defect sentences with `corpus/lessons/round-48.md` `## Mistakes` rows once that section
   is written (the freeze pointer is declaration line 19; the mechanisms above come from the F-4 dispatch).
3. The `Measured` block must stay placeholder text until each counter has been run at the final revision; do not let the
   draft's `C1/C2/C3` before-values stand in for measured outcomes.
4. `w2` is the only wave; if a residual wave is dispatched, the "Round shape" line gains one clause rather than a new
   heading, per rounds 45-46.
5. Cleanliness observation (not used as evidence): `git -C … status --porcelain` shows untracked
   `.ufo/waves/round-48/w1/R48Attack19.md` and `w1/R48Attack19-receipts/`, plus untracked `w2.ready` and
   `w2.ready.dispatched`. The w1 paths are outside the freeze commit; per the incident rule I did not open them. The
   report file itself is the only path this seat wrote.
