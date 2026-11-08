# MutRegistry — round 99, wave w1 (mutation tester)

Seat: `MutRegistry` (leaf, no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; scratch
`/fast/scratch/hyaku/tsukuroi-r99/MutRegistry` (deleted before yield).
No tool was installed or upgraded this seat; no `sudo`, no pacman, no git/jj mutation.

Instruments mutated (pinned bytes, `sha256sum -c .ufo/waves/round-99/before/instruments.sha256` →
**16/16 OK**, exit 0, re-run after the last measurement):
`tools/limine-pin-battery-r99.py` (c2e8c8fc…) and `tools/check-registry-content-r99.py` (b489f5b8…).
Mutants live only in scratch; the seat dir holds diffs and readings, never a mutant file
(`find .ufo/waves/round-99/w1/MutRegistry -name '*.py'` → empty).

Raw outputs are under `receipts/`; every quoted number below was produced by a run this seat made,
and each run's own file is named. Byte-level rule (QUALITY 141): no byte offset is claimed in this
report; all locations are diff line numbers from the pinned source, so no decoded-index offset is
recorded anywhere.

## 0. Scratch-loss disclosure (evidence class: peer seat disclosure)

At ~11:24 -0300 seat `CriticClaims-21` removed the shared scratch parent
`/fast/scratch/hyaku/tsukuroi-r99` (disclosed to me by IRC at that time, and recorded in
`.ufo/waves/round-99/w1/CriticClaims.md` §7b). It deleted my scratch mutants, fixtures and driver
scripts mid-pass. Authoritative readings already written to this seat's `receipts/` survived. I
regenerated the eight battery mutants with the generator, and the regeneration **asserts each
sha256 equals the value the surviving `receipts/M*.diff` were produced from** (all eight matched;
`receipts/mutants.sha256`). Only one leg was lost and re-run: pristine N11, re-read as
`unmet 103/105 [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`, 0 error rows — identical to the
L1's measurement and to CriticClaims' receipt 03 (two independent seats).

## 1. Baselines re-derived (pristine instruments)

```
python3 tools/limine-pin-battery-r99.py --selftest
python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 1 --work <scratch> --json receipts/pristine-gate.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 1 --work <scratch> --json receipts/pristine-N09.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 1 --work <scratch> --json receipts/pristine-N11.json
python3 tools/check-registry-content-r99.py --selftest
python3 tools/check-registry-content-r99.py --root /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --json receipts/pristine-landed-root.json
python3 tools/check-registry-content-r99.py --root <fixtures>/hybrid  --json receipts/pristine-hybrid.json
python3 tools/check-registry-content-r99.py --root <fixtures>/restated --json receipts/pristine-restated.json
```

Fixtures were built by the committed dev tool
`python3 .ufo/waves/round-99/before/dev/make-fixtures.py <scratch>/fixtures` (exit 0, four dirs).

| expected (claims.json / plan) | measured (raw receipt) | call |
|---|---|---|
| landed gate `met 105/105`, `failed_families []`, 0 error rows | `families_passed 105/105 verdict met failed -`, cases 420, error_rows 0 (`pristine-gate.json`) | PASS |
| N09 `unmet 104/105`, `[REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows | `unmet 104/105 failed REFUSAL-VERSIONS-9DIGIT-Y`, 420 cases, 0 error rows (`pristine-N09.json`) | PASS |
| N11 `unmet 103/105`, `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`, 0 error rows | `unmet 103/105 failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT`, 420 cases, 0 error rows (`pristine-N11.json`) | PASS |
| battery `--selftest` (no reference) `PASS 5/5` | `reference-gate skipped (no --reference)` / `selftest PASS 5/5` (`pristine-selftest-noref.txt`) | PASS |
| both new lie kinds make the battery read unmet | wrapper `limine-version` → `unmet 93/105` (12 families); wrapper `visibility-era` → `unmet 95/105` (10 families); 0 error rows each (`pristine-wrap-lv.json`, `pristine-wrap-era.json`) | PASS |
| checker `--selftest PASS 17/17` | `selftest PASS 17/17`, 17/17 case lines PASS (`pristine-checker-selftest.txt`) | PASS |
| r99 hybrid fixture `FAIL` exactly one `RC-CELL-MISSING` | `FINDING RC-CELL-MISSING SKILL.md:10 …`, `status FAIL bindings 6/7 findings 1` (`pristine-hybrid.json`) | PASS |
| r99 restated fixture `FAIL` exactly one `RC-CELL-AMBIGUOUS` | `FINDING RC-CELL-AMBIGUOUS SKILL.md:10 … mentions 'VARIANTS' 2 times`, 1 finding (`pristine-restated.json`) | PASS |
| r99 M07 mutant `--selftest FAIL 16/17`, exactly `ancestor` red | `ancestor FAIL rc=0 registry-content: status PASS …` / `selftest FAIL 16/17`, all other 16 PASS (`M07-selftest.txt`) | PASS |
| landed content `PASS`, 0 findings, bindings 7 | `registry-content: status PASS bindings 7/7 findings 0` (`pristine-landed-root.txt`) | PASS |

All N09/N11/mutant legs in this seat are **one run each** (the seat item allows one; three-run
repetition remains the L1's and executors' evidence). Every battery run this seat made reported
`cases 420` (105 families × 4) and `error_rows 0`, so no reading is an infrastructure artefact.

## 2. Battery table — single-clause mutants of `tools/limine-pin-battery-r99.py`

Method: byte-identical copy of the pinned file in scratch; one clause deleted per mutant; the
deletion is asserted to occur exactly once (in the named function body for M1–M4, in the template or
tuple literal for M5–M8). Diffs are `receipts/M1.diff` … `M8.diff`; hashes `receipts/mutants.sha256`.
Each mutant was run as `python3 <mutant> --selftest` and
`python3 <mutant> --gate <N09|N11> --runs 1 --work <per-mutant scratch> --json receipts/<M>-N0x.json`.

Frozen expectations the legs are read against: selftest `PASS 5/5`; N09 `unmet 104/105 [Y]`;
N11 `unmet 103/105 [EXPLICIT-VERSION-ERA, X]` (all 0 error rows).

| mutant | diff (hunk only, line numbers = pinned source) | `--selftest` (no ref) | N09 | N11 | assigned-leg verdict | witness that moves the reading |
|---|---|---|---|---|---|---|
| M1 | `fam_refusal_versions_9digit` (X): delete `c.check_echo = True` (line 1775) | PASS 5/5 | `unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y]` unchanged | `unmet 103/105 [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]` unchanged | **SURVIVED** | E1 (constructed): pristine 103/105 `[EXPLICIT-VERSION-ECHO, X]` → M1 **104/105** `[EXPLICIT-VERSION-ECHO]`; the X family drops out → KILLED by E1 |
| M2 | X family: delete `c.check_era = True` (line 1776) | PASS 5/5 | unchanged 104/105 [Y] | **104/105 [EXPLICIT-VERSION-ERA]** (frozen 103/105 [E, X]) | **KILLED** (N11; the X family drops out and the count moves 103→104) | — |
| M3 | `fam_refusal_versions_9digit_y`: delete `c.check_echo = True` (line 1817) | PASS 5/5 | unchanged | unchanged | **SURVIVED** | E2 (constructed): pristine 104/105 `[Y]` → M3 **met 105/105** → KILLED by E2 |
| M4 | Y family: delete `c.check_era = True` (line 1818) | PASS 5/5 | **met 105/105 `[]`** (frozen unmet 104/105 [Y]) | unchanged 103/105 [E, X] | **KILLED** (N09; met where the claim needs unmet — the r98 g6 shape) | — |
| M5 | remove the `limine-version` arm from `LIE_WRAPPER` (3 lines, 2356–2358) | PASS 5/5 | unchanged | unchanged | **SURVIVED** | see §4: its own reference-leg case still passes (wrapper reads `unmet 100/105`), so no committed or reference leg kills it |
| M6 | remove the `visibility-era` arm (3 lines, 2359–2361) | PASS 5/5 | unchanged | unchanged | **SURVIVED** | see §4: reference-leg case still passes (wrapper `unmet 100/105`) |
| M7 | drop `"limine-version"` from `LIE_KINDS` (14 → 13) | PASS 5/5 | unchanged | unchanged | **SURVIVED** | reference leg prints one case fewer; witness = a frozen case set/tally (see §4) |
| M8 | drop `"visibility-era"` from `LIE_KINDS` (14 → 13) | PASS 5/5 | unchanged | unchanged | **SURVIVED** | same |

Direction note (R98-MUTANT-DIRECTION-READ): M4 is the decisive direction (`met` where the frozen leg
is `unmet`). M2 and M1's witness move the reading the other way in the family set and count
(103→104, the asserted family disappears from `failed_families`) while the verdict stays `unmet`;
that is still a move **away from the frozen expectation**, i.e. a detection, and per the round rule a
mutant that makes a leg read better than frozen is killed, not surviving.

### 2b. Witness bends E1/E2 actually exercised (constructed by this seat, scratch only)

Single-line substitutions on the gate's CLI output echo line
(`"limine_version": limine_version,`, line 316): E1 falsifies the echo exactly when the FIRST
component is `999999999`; E2 exactly when the SECOND is. Both keep `limine_version_source` = `flag`
and the pins unchanged, so they are pure field lies. Diffs `receipts/E1.diff`, `receipts/E2.diff`;
hashes `receipts/mutants.sha256`.

| leg | pristine battery | mutant battery | reading |
|---|---|---|---|
| E1 (X-cap echo lie) | `unmet 103/105 [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` (`witness-E1-pristine.json`) | M1: `unmet 104/105 [EXPLICIT-VERSION-ECHO]` (`witness-E1-M1.json`) | M1 detected (count + family set move) |
| E2 (Y-cap echo lie) | `unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y]` (`witness-E2-pristine.json`) | M3: `met 105/105 []` (`witness-E2-M3.json`) | M3 detected (met where witness is unmet) |

Consequence: the two echo legs are **causal** when a spelling-targeted lie is sent, but no committed
round-99 control sends one — the plan's Limits already name this ("the X/Y echo leg has no
spelling-targeted committed bend"), and M1/M3 are exactly that limit made executable.

## 3. Checker table — single-clause mutants of `tools/check-registry-content-r99.py`

Method: same copy-and-assert-once discipline; diffs `receipts/C1.diff` … `C5.diff`. Each mutant run
as `--selftest` and `--root <fixtures>/hybrid` / `--root <fixtures>/restated` (the fixtures are the
committed dev tool's bytes; the table bytes are not hand-written). Pristine readings above.

| mutant | diff (hunk only) | `--selftest` | which cases change | hybrid fixture | restated fixture | verdict | class / note |
|---|---|---|---|---|---|---|---|
| C1 | drop the `(?![0-9,-])` boundary guard from the `RC-BEND-SPAN` capture (line 281) | **FAIL 16/17** | `span-hybrid` only, `FAIL []` (stays green on all 16 others) | **PASS** (pristine: FAIL `RC-CELL-MISSING`) | FAIL `RC-CELL-AMBIGUOUS` (unchanged) | **KILLED** | the hybrid refusal is exactly the guard's work |
| C2 | drop `"unique": True` (line 282) | **FAIL 16/17** | `span-restated` only, `FAIL []` | FAIL `RC-CELL-MISSING` (unchanged) | **PASS** (pristine: FAIL `RC-CELL-AMBIGUOUS`) | **KILLED** | flag + branch are jointly the ambiguity clause |
| C3 | remove the `RC-CELL-AMBIGUOUS` branch, keep the flag | **FAIL 16/17** | `span-restated` only, `FAIL []` | FAIL `RC-CELL-MISSING` (unchanged) | **PASS** | **KILLED** | observationally identical to C2 on every leg — the two halves are inert alone |
| C4 | drop `results.append(ancestor_case(base))` from `selftest()` | **PASS 16/16** (case absent) | `ancestor` disappears; no case goes red | FAIL `RC-CELL-MISSING` (unchanged) | FAIL `RC-CELL-AMBIGUOUS` (unchanged) | **KILLED by the denominator only** | the status token is unchanged `PASS`; only the frozen `17/17` count detects it must be met |
| C5 | make `ancestor_case` always return `ok = True` | **PASS 17/17** (unchanged) | none | FAIL `RC-CELL-MISSING` (unchanged) | FAIL `RC-CELL-AMBIGUOUS` (unchanged) | **SURVIVED** | coverage gap: a selftest case that cannot fail |

### 3b. C5 witness, measured

`M07` (the r98 survivor: delete `tree.check_revision()` in `main`) read
`selftest FAIL 16/17` with exactly `ancestor FAIL rc=0 registry-content: status PASS bindings 7/7
findings 0` (`M07-selftest.txt`) — so the r99 case is causal **while its assertion is intact**.
Composing the single clause of C5 onto M07 (`C5M07`, both diffs in `receipts/`) reads
`selftest PASS 17/17` (`C5M07-selftest.txt`) — the same doctored CLI that the pristine case kills is
now accepted. Witness that kills C5: a metatest that runs the ancestor probe against a doctored copy
of the CLI and requires the case to be red (the `M07` / `C5M07` pair above is that witness's two
arms; no committed leg contains it today).

## 4. Survivals — class and exact witness

| survivor | class | exact witness that kills it (what would have to be committed) |
|---|---|---|
| M5 (no `limine-version` arm) | **coverage gap — non-discriminating predicate** | The reference-leg case is `("lie-"+kind, r["verdict"] == "unmet")`. The wrapper cannot parse a refusal (rc 64, empty stdout), so the five usage families (`AUTO-PROBE-FAIL`, `AUTO-PROBE-SHAPES`, `EXTRA-COMPONENT`, `REFUSAL-VERSIONS`, `REFUSAL-VERSIONS-10DIGIT`) fail under **any** wrapper: measured `unmet 100/105` for a wrapper with no field arm at all (`M5-wrap.json`, `M6-wrap.json`), vs `93/105` for the arm-bearing `limine-version` wrapper (`pristine-wrap-lv.json`). Witness: assert the case's tally/family set (e.g. `families_passed == 93` or `failed_families ⊇ {EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT…}`) instead of only `verdict == "unmet"`. |
| M6 (no `visibility-era` arm) | **coverage gap — non-discriminating predicate** | same mechanism; measured `unmet 100/105` without the arm vs `95/105` with it (`pristine-wrap-era.json`). Witness: assert `families_passed == 95` / the era-family set. |
| M7 (`limine-version` dropped from `LIE_KINDS`) | **coverage gap — self-referential case list** | `for kind in LIE_KINDS` means removing a member removes both the check and its denominator, so the leg prints `PASS 19/19` instead of `PASS 20/20` (measured inputs: `len(LIE_KINDS)` 14→13 by import; 6 non-lie result lines with a reference). Witness: a frozen reference-leg case set/tally (`PASS 20/20` containing `lie-limine-version`, 14 `lie-*` lines). |
| M8 (`visibility-era` dropped) | **coverage gap — self-referential case list** | same; `len(LIE_KINDS)` 14→13, expected `PASS 19/19`. Witness: frozen case set with `lie-visibility-era`. |
| M1 (X echo removed) | **coverage gap — no committed spelling-targeted echo bend** | already measured: the E1 bend (gate echoes a wrong `limine_version` only for `999999999.9.9`, source stays `flag`) drops the X family: 103/105→104/105. A committed copy of E1 as a fourth control is the witness. |
| M3 (Y echo removed) | **coverage gap — same** | already measured: the E2 bend (wrong echo only for `12.999999999.4`/`0.999999999.0`) reads `met 105/105` on M3 vs `unmet 104/105 [Y]` on pristine. A committed copy of E2 is the witness. |
| C5 (`ancestor_case` always ok) | **coverage gap — assertion cannot fail** | the measured `M07` / `C5M07` pair: the doctored CLI is `FAIL 16/17` under the pristine case and `PASS 17/17` under C5. Witness: a metatest case that requires the ancestor probe against a no-ancestor-check CLI to be red. |

No survival implies a contract change; none is proposed. The two survivors the round set out to close
are closed **as instruments**, with one caveat worth the L1's attention: the reference-leg `lie-*`
cases (M5/M6) do not discriminate an arm from no arm, because the wrapper's own crash on rc-64
refusals already forces `unmet`. C1's frozen target does not measure the reference leg (`--selftest`
without a reference is what is frozen), so this caveat does not falsify C1; it means the r98
"lie-kind coverage" gap is closed in name and only partly in discriminating power.

## 5. Findings for the L1 (reported, not acted on)

1. **Non-discriminating lie-kind predicate (M5/M6).** Every one-field wrapper reads `unmet`
   (`100/105` with no arm, `93/105`/`95/105` with an arm) because the wrapper cannot parse a
   refusal's empty stdout; the selftest assertion `verdict == "unmet"` therefore cannot see an arm
   removal. Evidence: `pristine-wrap-lv.json`, `pristine-wrap-era.json`, `M5-wrap.json`,
   `M6-wrap.json`.
2. **Observational equivalence of C2 and C3.** Neither half of the ambiguity clause (the `unique`
   flag, the `RC-CELL-AMBIGUOUS` branch) changes any reading alone; both mutants produce the same
   four readings. The clause is correctly joint, but the mutation table cannot distinguish which
   half a future regression removes — the restated fixture kills either.
3. **C4's kill is count-only.** `--selftest` prints `PASS 16/16` after the ancestor case is deleted;
   the status token is unchanged. Only the frozen denominator (`17/17`) detects the removal, so any
   reader that greps for `PASS` alone would miss it. The claim's kill rule does freeze `17/17`, so
   the mutant is killed by the claim as written.
4. **No mutant is written into the lane tree.** Mutants and witness gates lived in scratch; the seat
   dir holds only diffs (`M*.diff`, `C*.diff`, `M07.diff`, `C5M07.diff`, `E1.diff`, `E2.diff`),
   hashes (`mutants.sha256`) and raw run output.

## 6. Receipts (all under `.ufo/waves/round-99/w1/MutRegistry/receipts/`)

Baselines: `pristine-selftest-noref.txt`, `pristine-gate.{txt,json}`, `pristine-N09.{txt,json}`,
`pristine-N11.{txt,json}`, `pristine-checker-selftest.txt`, `pristine-landed-root.{txt,json}`,
`pristine-hybrid.{txt,json}`, `pristine-restated.{txt,json}`.
Mutants: `M1..M8.diff`, `M1..M8-selftest.txt`, `M1..M8-N09-run.txt`, `M1..M8-N09.json`,
`M1..M8-N11-run.txt`, `M1..M8-N11.json`, `mutants.sha256`.
Wrappers / witnesses: `pristine-wrap-lv-run.txt`, `pristine-wrap-lv.json`,
`pristine-wrap-era-run.txt`, `pristine-wrap-era.json`, `M5-wrap-lv-run.txt`, `M5-wrap.json`,
`M6-wrap-era-run.txt`, `M6-wrap.json`, `E1.diff`, `E2.diff`,
`witness-E1-pristine.{txt,json}`, `witness-E1-M1.{txt,json}`, `witness-E2-pristine.{txt,json}`,
`witness-E2-M3.{txt,json}`.
Checker: `C1..C5.diff`, `C1..C5-selftest.txt`, `C1..C5-hybrid.{txt,json}`,
`C1..C5-restated.{txt,json}`, `M07.diff`, `M07-selftest.txt`, `C5M07.diff`, `C5M07-selftest.txt`.

```json
{"seat":"MutRegistry","verdict":"findings","notes":"battery M1-M8 on pinned r99: M2 killed by N11 (104/105 [EXPLICIT-VERSION-ERA] vs frozen 103/105 [EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT]), M4 killed by N09 (met 105/105 vs frozen unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y]); M1/M3 survive the assigned legs and are killed by constructed spelling-targeted echo bends E1 (103/105->104/105) and E2 (104/105->met); M5/M6 survive all legs and even their own reference-leg case because any wrapper reads unmet (100/105 with no arm vs 93/105 and 95/105 with the arms) so the 'unmet' predicate cannot see an arm removal; M7/M8 survive (the reference case list is derived from LIE_KINDS, 14->13). checker: C1 killed by the hybrid fixture/selftest span-hybrid, C2 and C3 killed by the restated fixture/selftest span-restated and are observationally equivalent, C4 killed only by the frozen 17/17 denominator (PASS 16/16), C5 survives (PASS 17/17) with the measured M07/C5M07 pair as its witness. No mutant written into the lane tree; scratch deleted; no tool installs."}
