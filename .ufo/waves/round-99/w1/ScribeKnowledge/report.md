# ScribeKnowledge — round 99, wave w1 (seat report)

Seat: scribe (leaf member — no subagent dispatch). Scope: draft the round's knowledge entry, "what
the accepted-cap families must assert, and what the two new lie kinds certify"; every number in the
draft paired with the command that produced it; every negative claim paired with its sweep.

## Deliverables (all inside this seat dir; no `corpus/` file was created or modified)

| artifact | path | what it is |
|---|---|---|
| the drafted knowledge entry | `.ufo/waves/round-99/w1/ScribeKnowledge/limine-metadata-cap-families-r99.md` | the entry, provenance trio first, S395 cited, six sections, a `Limits` section |
| the review of the landed corpus draft | `.ufo/waves/round-99/w1/ScribeKnowledge/corpus-draft-review.md` | six findings on the L1's landed `corpus/knowledge/limine-metadata-cap-families-r99.md`, each with its sweep |
| receipts | `.ufo/waves/round-99/w1/ScribeKnowledge/receipts/` | 13 numbered files + the battery JSONs, the lie wrappers and the per-leg stdout/stderr |
| this report | `.ufo/waves/round-99/w1/ScribeKnowledge/report.md` | commands, raw output, PASS/FAIL per expected line |

Scratch root `/fast/scratch/hyaku/tsukuroi-r99/ScribeKnowledge` (deleted before this report; see
§Cleanup). The `--work` and `TMPDIR` of every battery run pointed inside it.

## What this seat measured (own runs, own receipts)

Instrument integrity, run before any measurement below:

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
rc=0
```

(receipt `receipts/01-byte-anchors-measured.txt`.)

### PASS/FAIL per expected line

| # | expected line | command | observed | verdict | receipt |
|---|---|---|---|---|---|
| 1 | landed gate `met` 105/105, `failed_families []`, 0 error rows, x3 | `python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work <scratch> --json OUT` | `met` 105/105 x3, `[]`, 0 error rows; each named family `[4, 0]` | PASS | `receipts/c1-gate-r99.json`, `.stdout` |
| 2 | `N09-y-era` → `unmet` 104/105, failed exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows, x3 | `python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 --work <scratch> --json OUT` | `unmet` 104/105 x3, exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows; that family `[0, 4]` | PASS | `receipts/c1-N09-r99.json`, `.stdout` |
| 3 | the r98 control is blind to `N09` (`met` 105/105) | `python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 --work <scratch> --json OUT` | `met` 105/105 x3, `[]`, 0 error rows | PASS | `receipts/c1-N09-r98ctl.json`, `.stdout` |
| 4 | `N11-x-era` → `unmet` 103/105, failed exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`, 0 error rows, x3 | `python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 3 --work <scratch> --json OUT` | `unmet` 103/105 x3, exactly that pair, 0 error rows; `REFUSAL-VERSIONS-9DIGIT` `[0, 4]`, `EXPLICIT-VERSION-ERA` `[3, 1]` | PASS | `receipts/c1-N11-r99.json`, `.stdout` |
| 5 | the r98 control on `N11` reads `unmet` 104/105 with `[EXPLICIT-VERSION-ERA]` only (the delta) | `python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 3 --work <scratch> --json OUT` | `unmet` 104/105 x3, exactly `[EXPLICIT-VERSION-ERA]`, that family `[3, 1]`, 0 error rows | PASS | `receipts/c1-N11-r98ctl.json`, `.stdout` |
| 6 | the r98 do-nothing battery on the landed gate reads `met` 105/105 | same control battery, `--gate tools/check-limine-pins.py` | `met` 105/105 | PASS | `receipts/c1-gate-r98ctl.json`, `.stdout` |
| 7 | the r98 G6 survivor: the r98 control battery reads `met` 105/105 on a gate that lies in `visibility_era` for the two Y-cap spellings | `python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py --gate .ufo/waves/round-98/w1/ReviewBattery/g6-y-era.py --runs 3 --work <scratch> --json OUT` | `met` 105/105 x3, `[]`, 0 error rows | PASS | `receipts/c1-g6-r98ctl.json`, `.stdout`, `receipts/08-g6-survivor-rederived.txt` |
| 7b | the same G6 attack gate under the **r99** battery now fails | `python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-98/w1/ReviewBattery/g6-y-era.py --runs 3 --work <scratch> --json OUT` | `unmet` 104/105 x3, failed exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows — the r98 survivor is closed by the file that produced it | PASS | `receipts/c1-g6-r99.json`, `.stdout` |
| 7c | the **echo** legs of the X/Y families, witnessed by the r98-carried fixed-echo attack under both batteries | `python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-98/w1/ReviewBattery/g2b-fixed-echo.py --runs 1 --work <scratch> --json OUT` and the same with the r98 control battery | r99: `unmet` 98/105, failed exactly `[AUTO-ERA-A, AUTO-ERA-B, EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT, REFUSAL-VERSIONS-9DIGIT-Y, REFUSAL-VERSIONS-9DIGIT-Z]`, both new families `[0, 4]`; r98 control: `unmet` 100/105, the same list **without** the X and Y families — the echo side's delta is two families | PASS | `receipts/16-g2b-fixed-echo-both-batteries.txt`, `receipts/c1-g2b-fixed-echo-r99.json`, `receipts/c1-g2b-fixed-echo-r98ctl.json` |
| 8 | `--selftest` (no reference) `PASS 5/5` | `python3 tools/limine-pin-battery-r99.py --selftest` | `reference-gate skipped (no --reference)`; `selftest PASS 5/5` | PASS | `receipts/06-selftest-r99-noref.txt` |
| 9 | the two new lie kinds make the battery read `unmet` | `python3 tools/limine-pin-battery-r99.py --gate <wrapper> --runs 3 --work <scratch> --json OUT`, wrapper = the pinned battery's own `LIE_WRAPPER % (gate_src, kind)` | `limine-version` → `unmet` 93/105 x3; `visibility-era` → `unmet` 95/105 x3; 0 error rows | PASS | `receipts/c1-lie-limine-version-r99.json`, `receipts/c1-lie-visibility-era-r99.json`, `receipts/14-lie-composition-own.txt` |
| 9b | the battery's own `--selftest --reference` leg | `python3 tools/limine-pin-battery-r99.py --selftest --reference tools/check-limine-pins.py` | the L1's frozen attempt (`.ufo/waves/round-99/before/dev/c1-selftest-r99-reference.txt`) ended **rc=1** with `FileNotFoundError` on a scratch path under `/fast/scratch/hyaku/tsukuroi-r99/dev/` — the tree a sibling seat deleted at ~11:24; the leg is incomplete and certifies nothing | **INCOMPLETE** (reported, not passed off as a pass) | `receipts/15-selftest-reference-state.txt` |
| 10 | the roster is unchanged at 105 | AST count of `FAMILY_ROSTER` in both batteries | 105 in r98, 105 in r99; the r99-vs-r98 diff touches no roster literal | PASS | `receipts/03-negative-claim-sweeps.txt` §S3 |
| 11 | the gate's two emission sites, at byte level | `bytes.find` on the pinned gate bytes | MAIN 16931/17037 (lines 316/318), EARLY 11230/11344 (lines 200/202), source field 16977/11280 | PASS | `receipts/01-byte-anchors-measured.txt` |
| 12 | the echo is verbatim and the era follows the whole tuple | `python3 tools/check-limine-pins.py --conf <fixture> --esp <esp> --limine-version <spelling>` | `12.09.4`→`12.09.4`/era A, `12.000000009.000000005`→verbatim/era B, `12.999999999.4`→era B, `0.999999999.0`→era A, `999999999.9.9`→era B; source `flag` everywhere | PASS | `receipts/gate-spellings-r99.jsonl` |
| 13 | each bend falsifies the era label only | `diff tools/check-limine-pins.py <bend>` and the gate's own JSON under each bend | one changed expression per bend (the `visibility_era` line); the echo is never touched | PASS | `receipts/03-negative-claim-sweeps.txt` §S1, `receipts/07-bend-field-readings.txt` |
| 14 | C2 context (not this seat's claim): the r99 checker reads `PASS 17/17` on its selftest; hybrid → `RC-CELL-MISSING`, restated → `RC-CELL-AMBIGUOUS`; the r98 control reads `PASS` on both | `python3 tools/check-registry-content-r99.py --selftest` and `--root <fixture>` | `selftest PASS 17/17`; hybrid `FAIL` one `RC-CELL-MISSING`; restated `FAIL` one `RC-CELL-AMBIGUOUS`; r98 control `PASS 7/7` on both | PASS | `receipts/04-c2-checker-legs.txt` |

## Findings (reported; the corpus is the L1's)

1. **The N10 twin receipt does not exist in the tree.** The landed corpus entry's §3 and
   `corpus/lessons/round-99.md` both cite `.ufo/waves/round-99/before/dev/c1-N10-twin-r98-control.json`
   for the dropped bend's r98-control reading; the plan names a third spelling
   (`before/dev/c1-N10-twin-r98.json`). Sweep: `find .ufo/waves/round-99 -name "*N10*"` → no output;
   `ls .ufo/waves/round-99/before/dev/ | grep -i n10` → no output. The reading is asserted in two
   landed files with nothing behind it (the R98-RECEIPT-NAME-MISMATCH class). This seat did not
   re-derive it and does not cite it. Detail: `corpus-draft-review.md` F1.
2. **A blanket lie kind's `unmet` reading is not only the field assertion.** Measured on the two
   lie receipts: of the twelve families the `limine-version` lie fails, **seven** fail because the
   falsified field was read and **five** (`AUTO-PROBE-FAIL`, `AUTO-PROBE-SHAPES`, `EXTRA-COMPONENT`,
   `REFUSAL-VERSIONS`, `REFUSAL-VERSIONS-10DIGIT`) fail because the wrapper does
   `json.loads(p.stdout)` before it can falsify anything and a refusal answers rc 64 with an empty
   stdout — so the wrapper exits 1 and the refusal family sees `rc 1` where it expects `rc 64`. The
   landed entry's §4 reads as if every failing family failed because of the field. Detail:
   `corpus-draft-review.md` F2; the entry's §4 states the split.
3. **The landed `recheck:` line carries no procedure** (`recheck: 180d`), while
   `tools/check-recheck-commands.py` reads the last `recheck:` line as a procedure another agent is
   invited to follow. The seat's draft carries the procedure. Detail: `corpus-draft-review.md` F3.
4. **The landed `source:` line does not carry the gate's byte offsets** (the entry's first
   proposition is about the gate's two emission sites, and the header anchors only the battery).
   Detail: `corpus-draft-review.md` F4.
5. **The landed §3 heading counts three committed bends; two are committed**
   (`ls .ufo/waves/round-99/before/controls/bends/` → `N09-y-era.py`, `N11-x-era.py`; the third row
   is marked "(dropped)"). Detail: `corpus-draft-review.md` F5.
6. **The r98 battery's JSON schema token is still the r97 token.** The r99 battery moved to
   `tsukuroi-limine-pin-battery-r99-v1` (`tools/limine-pin-battery-r99.py` line 2308) while the r98
   control still emits `tsukuroi-limine-pin-battery-r97-v1`
   (`tools/limine-pin-battery-r98.py` line 2290) — measured in this seat's control receipts
   (`receipts/09-schema-tokens.txt`). This is the carried r98 Frontier item ("the r98 battery's
   unchanged JSON schema token"), not a new defect; it is noted because a reader comparing the two
   batteries' receipts by schema token will see `r97-v1` on the control leg.
7. **The L1's `--selftest --reference` leg is incomplete.** The frozen receipt
   `.ufo/waves/round-99/before/dev/c1-selftest-r99-reference.txt` ends with `rc=1` and a
   `FileNotFoundError` on `/fast/scratch/hyaku/tsukuroi-r99/dev/limine-battery-selftest-…/` — the
   shared scratch tree a sibling seat deleted at ~11:24. The leg therefore certifies nothing; the
   equivalent fact this seat established instead is that each of the two new lie kinds, applied to
   the landed gate, makes the battery read `unmet` (§9 above), measured on this seat's own
   wrappers. Receipt: `receipts/15-selftest-reference-state.txt`.

## What this seat did NOT do (out of scope)

- Did not write, edit or delete anything under `corpus/`, `tools/`, `SKILL.md`, `SCORECARD.md`,
  `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-99/before/`, `claims.json`, or any sibling lane. The
  landed `corpus/knowledge/limine-metadata-cap-families-r99.md` is the L1's; this seat reviewed it
  and drafted its own version beside it.
- Did not run `tools/make-r99-bends.py` or any earlier `make-r*-bends.py` (they write into the
  frozen wave dirs). Every bend was used as the committed file, read-only.
- Did not run any mutating git or jj command; `git status --porcelain` and `git diff` (read-only)
  were the only git commands run.
- Did not install or upgrade any tool. Nothing this seat needed was missing: python3, the pinned
  instruments and `bwrap` were present (`command -v bwrap` → `/usr/bin/bwrap`). The `check-recheck-commands.py`
  DEFAULT_FORBID list (`pacman`, `checkupdates`, `yay`, `paru`, `mkinitcpio`, `limine-update`) was
  checked against the entry's `recheck:` line: 7 backtick spans, 0 forbidden invocations
  (`receipts/11-header-conformance.txt`). No pacman transaction was made or attempted (pacman is
  paused host-wide).
- Did not message the fleet (`agent://all` is forbidden); no blocker needed a decision.

## Scratch deletion by a sibling seat (disclosure, not attribution)

At ~11:24 the sibling seat `CriticClaims-21` ran `rm -rf /fast/scratch/hyaku/tsukuroi-r99`, which
removed this seat's scratch tree (its `lies/`, `work/` and `gate-spellings/` subdirectories) while
four battery legs were running. The four legs that died (`c1-g6-r99`,
`c1-lie-limine-version-r99`, `c1-lie-visibility-era-r99`, `c1-gate-r98ctl`) left tracebacks in
`receipts/*.stderr` and no JSON; they were **re-run** by this seat after rebuilding the scratch
(`run-legs2.sh`), and the rebuilt lie wrappers are committed as bytes under
`receipts/lie-wrappers/` (sha256 `4fa10dbe…` for `lie-limine-version.py`, `ff420ace…` for
`lie-visibility-era.py`), so the wrappers are reproducible from the receipt directory alone. The
sibling disclosed the deletion itself and to the L1; this is a seat disclosure, not a trace-based
attribution, and the affected legs were re-run rather than repaired.

## Cleanup

Scratch root `/fast/scratch/hyaku/tsukuroi-r99/ScribeKnowledge` removed before this report; nothing
under `/tmp` is cited. Every receipt cited above lives under
`.ufo/waves/round-99/w1/ScribeKnowledge/receipts/`.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Entry drafted at .ufo/waves/round-99/w1/ScribeKnowledge/limine-metadata-cap-families-r99.md (trio first, S395 + gate byte offsets cited, 6 sections, Limits names the uncertified X/Y echo legs, every number paired with its command); review of the L1's landed corpus draft at corpus-draft-review.md with 6 findings. RUN (own receipts): landed gate met 105/105 x3 (0 error rows); N09 unmet 104/105 x3 failed exactly [REFUSAL-VERSIONS-9DIGIT-Y]; N09 on the r98 control met 105/105 x3 (blind); N11 unmet 103/105 x3 failed exactly [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]; N11 on the r98 control unmet 104/105 x3 failed exactly [EXPLICIT-VERSION-ERA] (the X leg is a delta); r98 G6 survivor re-derived met 105/105 x3; selftest PASS 5/5; lie kinds unmet 93/105 and 95/105; AST roster 105 in both batteries. FINDINGS: (1) the cited before/dev/c1-N10-twin-r98-control.json does not exist (find .ufo/waves/round-99 -name '*N10*' empty) though the landed entry and the lesson both cite its reading; (2) a blanket lie kind's unmet reading is only partly the field assertion - 7 of 12 failures are field-caused and 5 are the wrapper's refusal-path breakage; (3) the landed recheck: line has no procedure; (4) the landed source: line omits the gate byte offsets; (5) the landed heading counts three committed bends where two are committed; (6) the r98 control battery still emits the r97 schema token."}
