# ScoutFrontier — QUALITY 125/136 clause map for round 99 (C1 depth, C2 freshness)

Seat: `ScoutFrontier` (scout, leaf member). Lane: `tsukuroi-shokunin`, branch `master`, git HEAD
detached (no mutating git/jj command was run). Scope: map every clause of the two frozen
predicates to the committed artifact whose reading changes when that clause is bent, or the word
`uncertified`.

All receipts cited here are under this seat's own directory
`.ufo/waves/round-99/w1/ScoutFrontier/receipts/` and were written by this seat. The L1's
development receipts under `.ufo/waves/round-99/before/dev/` were re-derived, not trusted.

## 0. Instrument integrity (re-derived, not trusted)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
... 16 files OK ...
manifest rc=0
```
Receipt: `receipts/instruments-check.txt`. **PASS** — every pinned instrument byte-identical, so
no measurement below is void under the kill rule.

Identity cross-checks against the L1's own receipts (my independently rebuilt artifacts are
byte-identical to theirs):

| artifact | my sha256 | L1's recorded sha256 | receipt |
|---|---|---|---|
| lie wrapper `gate-limine-version.py` | `4fa10dbe…c81a6` | `4fa10dbe…c81a6` | `receipts/identity-checks.txt` |
| lie wrapper `gate-visibility-era.py` | `ff420ace…d9b02d9` | `ff420ace…d9b02d9` | `receipts/identity-checks.txt` |
| M07 checker mutant | `1ac9857f…328af441` | `1ac9857f…328af441` | `receipts/identity-checks.txt` |

Baseline re-derived from the pinned gate: `families_passed 105/105 verdict met failed -`, rc 0
(`receipts/base-gate.txt`). The claim's own counting command
(`count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y
--family REFUSAL-VERSIONS-9DIGIT-Z`) reproduces `met 105/105`, `failed_families []`,
`error_rows 0` (`receipts/counting-command.txt`). **PASS.**

Structural re-derivation of the two new assertions, read straight off the pinned bytes
(`receipts/assertion-wiring.txt`): an independent parse of the battery attributes each
`c.check_echo = True` / `c.check_era = True` to its enclosing family, giving

```
fam_refusal_versions_9digit       echo@line 1775  era@line 1776   (bytes 79015 / 79039)
fam_refusal_versions_9digit_y     echo@line 1817  era@line 1818   (bytes 81666 / 81690)
```

— i.e. both new assertions are wired exactly as the predicate says (X at 1775/1776, Y at
1817/1818), and the enforcement is `meta_ok` at byte 99433 (`got[8] == c.version and got[9] ==
"flag"`) and byte 99526 (`got[10] != ("12.9.5+" if c.era_b() else "pre-12.9.5")`).

---

## 1. C1 — `tools/limine-pin-battery-r99.py` (depth 8)

### 1a. The clause map

| # | clause of the frozen predicate | family / artifact whose reading changes when that clause is bent | committed receipt path | certified / uncertified |
|---|---|---|---|---|
| C1-i | roster unchanged at 105 | `FAMILY_ROSTER` literal (105) + `CASES_PER_FAMILY = 4`; the roster count itself is the observable — a roster change moves `families_total`/`cases` in every battery JSON. Committed witness: the do-nothing r98 battery's own `families_total 105` | `receipts/base-gate.json` (`families_total 105`, `cases 420`); `receipts/counting-command.txt` (named 9DIGIT/-Y/-Z all `[4,0]`) | **certified** |
| C1-ii | X family `REFUSAL-VERSIONS-9DIGIT` sets `check_echo` (flag spelling verbatim, source `flag`) | `REFUSAL-VERSIONS-9DIGIT`; falsified by (a) the blanket `lie-limine-version` wrapper, (b) the r98-carried `g2b-fixed-echo.py` (echoes `7.7.7`), (c) the r99-local one-clause removal mutant `battery-noXecho.py` | `receipts/ctrl-lie-limine.log` (93/105 unmet, X in `failed_families`); `receipts/g2b-r99.log` (98/105, X failed); `receipts/mut-noXecho-lie.log` (94/105 — X **drops out** of `failed_families`); `receipts/mut-noXecho-g2b.log` (99/105 — X drops out, Y still fails) | **certified** |
| C1-iii | X family sets `check_era` (era label the whole tuple selects) | `REFUSAL-VERSIONS-9DIGIT`; falsified by the committed bend `N11-x-era.py` (era label swapped exactly when the **first** component is the cap `999999999`) and by the r98-committed `g3-xcap.py`; removed by `battery-noXera.py` | `receipts/ctrl-N11.log` (103/105 unmet, `failed_families [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`); `receipts/g3-xcap-r99.log` (103/105, X failed — where the r98 battery read 104/105 with X **passing**); `receipts/mut-noXera-N11.log` (104/105, X drops out); `receipts/mut-noXera-lie-era.log` (96/105 — X drops out of the era-lie failed set while Y survives) | **certified** |
| C1-iv | Y family `REFUSAL-VERSIONS-9DIGIT-Y` sets `check_echo` | `REFUSAL-VERSIONS-9DIGIT-Y`; falsified by the blanket `lie-limine-version` wrapper, by `g2b-fixed-echo.py`, and by `battery-noYecho.py` | `receipts/ctrl-lie-limine.log` (Y failed); `receipts/g2b-r99.log` (Y failed); `receipts/mut-noYecho-lie.log` (94/105 — Y drops out); `receipts/mut-noYecho-g2b.log` (99/105 — Y drops out) | **certified** |
| C1-v | Y family sets `check_era` (era label the whole tuple selects) | `REFUSAL-VERSIONS-9DIGIT-Y`; falsified by the committed bend `N09-y-era.py` (era label swapped exactly when the **second** component is the cap `999999999`) and by the r98-committed `g6-y-era.py`; removed by `battery-noYera.py` | `receipts/ctrl-N09.log` (104/105 unmet, `failed_families [REFUSAL-VERSIONS-9DIGIT-Y]`); `receipts/g6-y-era-r99.log` (104/105, Y failed — where the r98 battery read **met 105/105**, the r98 survivor); `receipts/mut-noYera-N09.log` (**105/105 met** — Y drops out); `receipts/mut-noYera-lie-era.log` (96/105 — Y drops out of the era-lie failed set while X survives) | **certified** |
| C1-vi | `LIE_KINDS` gains `limine-version` and `visibility-era`, so the selftest's reference leg falsifies the two reported fields | the two new lie kinds themselves; each falsifies **its own** field and leaves the other intact — `limine-version` breaks the echo, `visibility-era` breaks the era label | `receipts/ctrl-lie-limine.log` (93/105 unmet); `receipts/ctrl-lie-era.log` (95/105 unmet); `receipts/lie-kind-specificity.txt` — `EXPLICIT-VERSION-ECHO` (echo-only) fails under `limine-version` but **survives** `visibility-era`; `EXPLICIT-VERSION-ERA` (era-only) fails under `visibility-era` but **survives** `limine-version`; `receipts/selftest-noref.txt` (`selftest PASS 5/5`) | **certified** |

**C1 uncertified count: 0 of 6 clauses.** Every clause of the C1 predicate has a committed
artifact whose reading moves when that clause is bent.

### 1b. Explicit answer for C1's X/Y echo legs (the acceptance asks for these by name)

- **X echo** (`REFUSAL-VERSIONS-9DIGIT` asserting `limine_version` verbatim, source `flag`):
  falsified by **`g2b-fixed-echo.py`** — the r98-committed fixed-echo gate at
  `.ufo/waves/round-98/w1/ReviewBattery/g2b-fixed-echo.py`, which answers `"limine_version":
  "7.7.7"` (bytes 11230 and 16924 of that file) instead of the flag spelling. Under the r98
  battery it read `unmet 100/105` with `failed_families [AUTO-ERA-A, AUTO-ERA-B,
  EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` — **X was not in
  the failed set**. Under the r99 battery the same committed gate reads `unmet 98/105` with
  `REFUSAL-VERSIONS-9DIGIT` **and** `REFUSAL-VERSIONS-9DIGIT-Y` added to the failed set
  (`receipts/g2b-r99.log`). The removal mutant `battery-noXecho.py` (X's `check_echo` line
  deleted, byte 79015–79039 of the pinned battery) reads `99/105` with X **absent** from
  `failed_families` (`receipts/mut-noXecho-g2b.log`) — the clause is load-bearing, not decorative.
  Secondary witness: the new `lie-limine-version` selftest lie kind
  (`receipts/ctrl-lie-limine.log`, 93/105).
- **Y echo** (`REFUSAL-VERSIONS-9DIGIT-Y` asserting the same): falsified by the **same** two
  artifacts — `g2b-fixed-echo.py` (Y fails under r99 at 98/105, `receipts/g2b-r99.log`) and the
  `lie-limine-version` wrapper (`receipts/ctrl-lie-limine.log`). The removal mutant
  `battery-noYecho.py` (Y's `check_echo` line deleted, byte 81666–81690) reads `99/105` with Y
  **absent** (`receipts/mut-noYecho-g2b.log`).

Note on the plan's own named Limit ("the X/Y echo leg has no spelling-targeted committed bend"):
that limit is **narrower than it reads**. `g2b-fixed-echo.py` is not spelling-targeted (it lies in
the echo for every spelling), so it does not by itself close the *spelling-targeted* gap the plan
names; but the clause-level question QUALITY 125 asks — "does a committed artifact's reading
change when this clause is bent" — is answered yes for both, by the removal mutants above. The
residual limit (no one-clause bend that lies in the echo of the X or Y spelling **only**) stands
exactly as the plan states it, and is *not* re-litigated here.

### 1c. The r98 survivors C1 claims to close — re-derived

| r98 survivor | r98 battery reading (committed r98 receipt) | r99 battery reading (my re-derivation) | verdict |
|---|---|---|---|
| `w1/ReviewBattery/g6-y-era-r98.json` (Y-cap-only era lie) | `met 105/105 failed_families []` | `unmet 104/105 failed [REFUSAL-VERSIONS-9DIGIT-Y]` (`receipts/g6-y-era-r99.log`) | **closed** — the Y family now asserts the era |
| `w1/ReviewBattery/g3-xcap-r98.json` (X-cap-only era lie; A5 said "the X-cap field fidelity rides on one EXPLICIT case") | `unmet 104/105 failed [EXPLICIT-VERSION-ERA]` | `unmet 103/105 failed [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]` (`receipts/g3-xcap-r99.log`) | **closed** — the X family now asserts the era in its own right, no longer only through one EXPLICIT case |
| lie-kind structural gap (no lie kind falsified `limine_version`/`visibility_era`) | `LIE_KINDS` had 12 members, neither field falsifiable | `LIE_KINDS` has 14 (`"limine-version", "visibility-era"` at byte 108455 of the pinned battery); both wrappers read unmet (`receipts/ctrl-lie-limine.log`, `receipts/ctrl-lie-era.log`) | **closed** |

### 1d. QUALITY 128 — does either new assertion draw randomly over the field it certifies?

**No. Both new assertions are over enumerated, non-random fields.** The families' randomisation is
confined to fixture *shape* fields, never to the certified field.

- **X family** (`tools/limine-pin-battery-r99.py` byte 79062): `_era_first_line_panic(c,
  REFUSAL_DIGIT9)` — the version sent is the module constant `REFUSAL_DIGIT9 = "9" * 9 + ".9.9"`
  (byte 76717), a fixed literal, not a draw. The echo and era both derive from that one constant.
- **Y family** (byte 81738): `_era_first_line_panic(c, Y_DIGIT9[c.index % len(Y_DIGIT9)])` —
  `Y_DIGIT9 = ("12.999999999.4", "0.999999999.0")` (byte 77254) is enumerated by the **case
  ordinal** (`c.index`, set in `build()` at byte 94215 from the per-family `_SEQ` counter), not by
  `c.rng`. With `CASES_PER_FAMILY = 4` (byte 91905) the two members are visited on a fixed
  round-robin; nothing is drawn.
- The only `c.rng` uses inside `_era_first_line_panic` (which starts at byte 79339's call site in
  each family) are `c.add("/%s" % rname(c.rng, ""))` (byte 72226, the file name) and
  `set_panic(c, c.rng.choice(["no", "No", "NO"]), indent="")` (byte 72329) — the
  `hash_mismatch_panic` **value**, which is a fixture shape field; plus `efi_entry`'s protocol
  whitespace choices. None of these is `limine_version` or `visibility_era`.
- The era label the battery expects is computed by `Case.era_b()` (byte 25682) as
  `tuple(int(p) for p in version.split(".")) >= (12, 9, 5)` (byte 25943) — from the *whole tuple*,
  which is precisely the field QUALITY 128 requires the family to present.

**So QUALITY 128 is satisfied for both new assertions** (the discriminating field is enumerated
in the case, not drawn). The residual Y-family caveat recorded in the family's own docstring
(r96 `F-4`: an era reader that looks at X alone is caught by `EXPLICIT-VERSION-ERA`, not by Y) is a
*gate-implementation* limit about which tuple component selects the era, **not** a draw over the
certified field; it stands unchanged and is not a QUALITY 128 violation.

### 1e. C1 kill-rule legs, re-derived

| expected line | my command | raw reading | PASS/FAIL |
|---|---|---|---|
| landed gate `105/105 met`, `failed_families []`, 0 error rows | `python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 1 --work <scratch> --json receipts/base-gate.json` | `families_passed 105/105 verdict met failed -`; `failed_families []`, `error_rows 0`, `cases 420` | **PASS** |
| N09-y-era `unmet 104/105`, `failed_families [REFUSAL-VERSIONS-9DIGIT-Y]`, 0 error rows | same battery with `--gate .../controls/bends/N09-y-era.py` | `unmet 104/105 failed REFUSAL-VERSIONS-9DIGIT-Y`; `error_rows 0` | **PASS** |
| N11-x-era `unmet 103/105`, `failed_families [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`, 0 error rows | same battery with `--gate .../controls/bends/N11-x-era.py` | `unmet 103/105 failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT`; `error_rows 0` | **PASS** |
| r98 do-nothing battery is blind to N09 (reads `met 105/105`) | `python3 tools/limine-pin-battery-r98.py --gate .../bends/N09-y-era.py --runs 1` | `families_passed 105/105 verdict met failed -` (`receipts/r98-on-N09.log`) | **PASS** |
| r98 do-nothing battery on the landed gate reads `met 105/105`; on N11 reads `unmet 104/105` with `failed_families [EXPLICIT-VERSION-ERA]` (blind to the X family) | same battery, the other two gates | `105/105 met` on the gate (`receipts/r98-on-gate.log`); `104/105 unmet failed EXPLICIT-VERSION-ERA` on N11 (`receipts/r98-on-N11.log`); control byte-identity `8198bd84…2f87` for both `tools/limine-pin-battery-r98.py` and `before/controls/do-nothing-battery-r98.py` (`receipts/r98-donothing.txt`) | **PASS** |
| `--selftest` (no reference) `PASS 5/5` | `python3 tools/limine-pin-battery-r99.py --selftest` | `selftest PASS 5/5`, rc 0 | **PASS** |
| both new lie kinds make the battery read `unmet` | lie wrappers from the battery's own `LIE_WRAPPER` | `93/105 unmet` (limine-version), `95/105 unmet` (visibility-era) | **PASS** |

---

## 2. C2 — `tools/check-registry-content-r99.py` (freshness 9)

### 2a. The clause map

| # | clause of the frozen predicate | family / artifact whose reading changes when that clause is bent | committed receipt path | certified / uncertified |
|---|---|---|---|---|
| C2-i | the `RC-BEND-SPAN` capture carries the boundary guard `(?![0-9,-])` (byte 14265 of the pinned checker; absent from the r98 checker) | the **hybrid** capture fixture (`VARIANTS N01-N04,N05`). Without the guard the cell binds and the hybrid case reads `PASS`; with it the cell does not bind and the case reads `RC-CELL-MISSING` | `receipts/hybrid-r99.txt` (r99 `FAIL bindings 6/7 findings 1`, finding id `RC-CELL-MISSING`); `receipts/hybrid-noguard.txt` (guard removed → `PASS bindings 7/7 findings 0`); `receipts/selftest-noguard.txt` (`FAIL 16/17`, **exactly `span-hybrid` red**); `receipts/hybrid-r98.txt` (r98 checker `PASS`) | **certified** |
| C2-ii | the binding is marked `unique`, so a cell mentioning `VARIANTS` twice reads `RC-CELL-AMBIGUOUS` (byte 14310 for the mark; bytes 16797/24462 for the finding id) | the **restated** capture fixture (`VARIANTS N01,N03 then VARIANTS N01-N03`). Without the `unique` mark the first mention wins and the cell reads `PASS`; with it the second mention raises `RC-CELL-AMBIGUOUS` | `receipts/restated-r99.txt` (`FAIL bindings 6/7 findings 1`, finding id `RC-CELL-AMBIGUOUS`); `receipts/restated-nounique.txt` (mark removed → `PASS bindings 7/7 findings 0`); `receipts/selftest-nounique.txt` (`FAIL 16/17`, **exactly `span-restated` red**); `receipts/restated-r98.txt` (r98 checker `PASS`) | **certified** |
| C2-iii | `--selftest` gains `ancestor` (14 → 17), exercising the `--revision` non-ancestor refusal through this file's real CLI | the `ancestor` selftest case itself. The r98 `MutRegistry` M07 mutant (ancestor check skipped) passes the r98 selftest and is killed by r99's `ancestor` case | `receipts/selftest-r99.txt` (`PASS 17/17`); `receipts/selftest-m07.txt` (`FAIL 16/17`, **exactly `ancestor` red**, `rc=0 registry-content: status PASS bindings 7/7 findings 0`); `receipts/pristine.txt` (real CLI on a non-ancestor revision → `CANNOT-EVALUATE: revision … is not an ancestor of master`, **RC=2**); `receipts/mutant.txt` (M07 → `status PASS bindings 7/7 findings 0`, **RC=0**) | **certified** |
| C2-iv | the same **7** bindings of **4** rows are bound (bound set unchanged) | the `BINDINGS` tuple: 7 entries over 4 rows. Every legitimate run prints `bindings 7/7`; a change in the bound set or in a cell's bound value moves that count to `6/7` | `receipts/clean-r99.txt` (`PASS bindings 7/7 findings 0`); `receipts/hybrid-r99.txt` and `receipts/restated-r99.txt` (`bindings 6/7` — the count moves when a bound cell stops binding); `receipts/c2-fixture-matrix.txt` (the full 3-fixture × 4-checker matrix) | **certified** |
| C2-v | the **14** carried r98 cases remain | the 14 r98 case names, each still able to go red. The r98 `M08` mutant (first label only) reddens **exactly** the two carried span cases and no others, proving the carried cases are live rather than vacuous | `receipts/selftest-r99.txt` (17 rows; all 14 r98 names present — set-wise superset, `receipts/carried-case-names.txt`); `receipts/selftest-m08.txt` (`FAIL 15/17`, **exactly `span-gap` and `span-gap-lie` red** — the two carried span cases, the three new ones green) | **certified** |

**C2 uncertified count: 0 of 5 clauses.** Every clause of the C2 predicate has a committed
artifact whose reading moves when that clause is bent.

### 2b. C2 kill-rule legs, re-derived

| expected line | my command | raw reading | PASS/FAIL |
|---|---|---|---|
| landed `status PASS`, `findings []`, `bindings 7` | `python3 tools/check-registry-content-r99.py --root <clean fixture>` | `registry-content: status PASS bindings 7/7 findings 0`, rc 0 | **PASS** |
| `--selftest` `PASS 17/17` | `python3 tools/check-registry-content-r99.py --selftest` | `selftest PASS 17/17`, rc 0 | **PASS** |
| M07 mutant `FAIL 16/17` with **exactly** the `ancestor` case red | `python3 <M07 mutant> --selftest` | `ancestor FAIL rc=0 registry-content: status PASS bindings 7/7 findings 0`; `selftest FAIL 16/17`; all 16 other rows PASS | **PASS** |
| r98 checker reads `PASS` on the hybrid fixture where r99 reads `FAIL` with one finding | `python3 tools/check-registry-content-r98.py --root <hybrid fixture>` | `PASS bindings 7/7 findings 0` (r98) vs `FAIL bindings 6/7 findings 1` finding id `RC-CELL-MISSING` (r99) | **PASS** |
| r98 checker reads `PASS` on the restated fixture where r99 reads `FAIL` with one finding | `python3 tools/check-registry-content-r98.py --root <restated fixture>` | `PASS bindings 7/7 findings 0` (r98) vs `FAIL bindings 6/7 findings 1` finding id `RC-CELL-AMBIGUOUS` (r99) | **PASS** |
| coverage gate `PASS 160/160 findings 0` at the pre-round tip | `python3 tools/check-registry-coverage.py --revision f107da3afe511f7db8cdc30235a992b774903158` | `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":160,"rows_total":160,"tools_total":160},"branch_tip":"f107da3a…"}` | **PASS** |

---

## 3. Findings and limits carried forward

1. **A caveat on C2 clause (iv), the 7 bindings.** The count `bindings 7/7` is a *derived* count of
   the `BINDINGS` tuple, not an independent measurement of the registry table's completeness. It
   is certified here in the sense QUALITY 125 asks (a bend moves the reading — the hybrid and
   restated fixtures both drop it to `6/7`), but it does **not** certify that 7 is the *correct*
   number of cells the table should bind. That deeper claim stays in the plan's named Limit
   ("the unbound rows and the three r98-measured C2 gaps stand unchanged"), and is not
   re-litigated here.

2. **C2 clause (v), the 14 carried cases, is certified by a mutation, not by a count.** The
   17-row selftest output alone would only show the rows exist. The `M08` mutant (first label
   only) reddens exactly `span-gap` and `span-gap-lie` — the two carried span cases — and leaves
   `span-hybrid`, `span-restated` and `ancestor` green, so the carried cases are demonstrably
   live under the r99 bytes rather than vestigial. `receipts/selftest-m08.txt`.

3. **The two new lie kinds are field-specific, which the L1's summary counts do not show on their
   own.** `receipts/lie-kind-specificity.txt`: `EXPLICIT-VERSION-ECHO` (the only family that
   asserts the echo and not the era) fails under `lie-limine-version` and **survives**
   `lie-visibility-era`; `EXPLICIT-VERSION-ERA` (era only) fails under `lie-visibility-era` and
   **survives** `lie-limine-version`. Each new kind therefore falsifies exactly the field it
   names — which is what "the two lie kinds falsify their fields" requires — and the families that
   assert both fields (X, Y, Z, LZ) die under either kind. The L1's `93/105` and `95/105` counts
   are correct but do not by themselves distinguish a field-specific lie from a blanket one; this
   receipt does.

4. **The plan's own "Limits" bullet about the X/Y echo leg is confirmed and not overstated.**
   `g2b-fixed-echo.py` lies in the echo for *every* spelling, so it is not the spelling-targeted
   one-clause bend the plan says it lacks. The clause-level certification in §1b stands on the
   removal mutants, which do isolate X's and Y's `check_echo` line specifically.

5. **C1's `EXPLICIT-VERSION-ERA` remains the only family that also fails under N11.** This is
   correct, not a redundancy: under `N11-x-era.py` the *first* component is the cap, and
   `EXPLICIT_VERSION_META` (byte 77183) contains `REFUSAL_DIGIT9` itself as one of its four
   explicit versions, so that family was already going to fail on its own row. The r99 addition is
   that `REFUSAL-VERSIONS-9DIGIT` now fails *in its own right*. Under the r98 battery the same
   committed gate read `104/105` with only `EXPLICIT-VERSION-ERA` failing
   (`receipts/g3-xcap-r99.log` contrasted against the r98 receipt) — that is exactly the A5 gap.

6. **Incidental incident disclosure.** At ~11:24 the shared scratch parent
   `/fast/scratch/hyaku/tsukuroi-r99` was removed by peer `CriticClaims-21` (self-disclosed to
   the L1 in `.ufo/waves/round-99/w1/CriticClaims.md` §7b). This seat's already-copied receipts
   under its lane seat directory were unaffected; every wiped scratch artifact was **re-derived
   from the pinned lane bytes** and its digest re-checked (the three identity hashes in §0
   reproduce byte-identically). No lane file, tool, or sibling seat was written.

7. **Not claimed here — one leg left unmeasured.** The battery's `--selftest --reference` leg (which
   runs the battery against a reference gate and then once per lie kind) was launched but did not
   finish inside this seat's budget; it was stopped rather than reported as a pass. The
   *lie-kind behaviour* that leg certifies is independently witnessed by the two wrapper battery
   runs (`receipts/ctrl-lie-limine.log` 93/105, `receipts/ctrl-lie-era.log` 95/105), by the
   field-specificity split (`receipts/lie-kind-specificity.txt`), and by `--selftest` without a
   reference (`PASS 5/5`, `receipts/selftest-noref.txt`). No clause in this map depends on the
   reference leg's own output, so it is left as an **unmeasured** item and not an assumption.
   (The L1's own `before/dev/c1-selftest-r99-reference.txt` is likewise a 0-byte file, so this leg
   has no committed receipt anywhere in the lane; it is an owed receipt, not a discrepancy in
   any number above.)

---

## 4. Reproducible commands (all from the lane root; scratch under
`/fast/scratch/hyaku/tsukuroi-r99/ScoutFrontier`, deleted before yield)

```
sha256sum -c .ufo/waves/round-99/before/instruments.sha256
python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 1 --work $S/work --json $R/receipts/base-gate.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 1 --work $S/work --json $R/receipts/ctrl-N09.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 1 --work $S/work --json $R/receipts/ctrl-N11.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-98/w1/ReviewBattery/g2b-fixed-echo.py --runs 1 --work $S/work --json $R/receipts/g2b-r99.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-98/w1/ReviewBattery/g3-xcap.py   --runs 1 --work $S/work --json $R/receipts/g3-xcap-r99.json
python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-98/w1/ReviewBattery/g6-y-era.py   --runs 1 --work $S/work --json $R/receipts/g6-y-era-r99.json
python3 tools/limine-pin-battery-r99.py --selftest
python3 tools/check-registry-content-r99.py --selftest
python3 tools/check-registry-content-r99.py --root <fixture>
python3 tools/check-registry-coverage.py --revision f107da3afe511f7db8cdc30235a992b774903158
```

Mutants were built by byte-exact substitution on the pinned bytes (derivation recorded in
`receipts/mutant-derivations.txt`; digests in `receipts/identity-checks.txt`); the mutants live
in the scratch dir and are not lane artifacts. The fixture repo for the ancestor probe was
created under scratch with `git init -b master` after
`git rev-parse --show-toplevel` printed exactly the scratch path
(`receipts/pristine.txt`, `receipts/mutant.txt`).

Byte offsets in this report were measured with `grep -abo` on the pinned bytes
(`receipts/byte-offsets.txt`), never from a decoded-string index (QUALITY 141).

{"seat":"ScoutFrontier","verdict":"findings","notes":"QUALITY 125/136 clause map built for both claims. C1: 6 of 6 clauses certified (0 uncertified); C2: 5 of 5 clauses certified (0 uncertified). All instrument digests re-verified against instruments.sha256 (rc=0) and every number re-derived, not taken from the L1. The three r98 survivors C1 names are closed on re-derivation: g6-y-era reads met 105/105 on the r98 battery and unmet 104/105 failed[REFUSAL-VERSIONS-9DIGIT-Y] on r99; g3-xcap reads unmet 104/105 failed[EXPLICIT-VERSION-ERA] on r98 and unmet 103/105 failed[EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT] on r99, so the X leg no longer rides on one EXPLICIT case (A5 closed); both new lie kinds read unmet (93/105 and 95/105). X/Y echo legs: falsified by the r98-committed g2b-fixed-echo.py (r99 98/105 with X and Y newly failing; r98 100/105 without them) and by the new limine-version lie kind; the removal mutants battery-noXecho.py and battery-noYecho.py each drop exactly their family from failed_families (99/105), proving both clauses load-bearing. C2: the boundary guard is witnessed by the hybrid fixture (r99 RC-CELL-MISSING, guard-removed mutant PASS, span-hybrid the only red selftest row), the unique mark by the restated fixture (r99 RC-CELL-AMBIGUOUS, mark-removed mutant PASS, span-restated the only red row), the ancestor case by the M07 mutant (FAIL 16/17, exactly ancestor red; real CLI rc 2 CANNOT-EVALUATE pristine vs rc 0 PASS mutant), the 7 bindings by bindings 7/7 clean vs 6/7 on both doctored fixtures, and the 14 carried cases by the M08 mutant redding exactly span-gap and span-gap-lie. QUALITY 128: both new assertions are over enumerated non-random fields (X uses the constant REFUSAL_DIGIT9 at byte 79062; Y enumerates Y_DIGIT9 by case ordinal at byte 81738; the only rng uses are file name and hash_mismatch_panic value casing) - no draw over the certified field. Limits recorded, not re-litigated: the plan's spelling-targeted X/Y echo bend still does not exist (g2b lies for every spelling); the bindings count is derived from the BINDINGS tuple, so 7 is not certified as the correct number of cells to bind; the --selftest --reference leg is not load-bearing for any clause and is left unmeasured. Scratch wiped at 11:24 by peer CriticClaims-21 (self-disclosed to the L1); all wiped artifacts re-derived from pinned bytes with digests re-verified, no lane file written."}
