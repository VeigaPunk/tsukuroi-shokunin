source: `corpus/SOURCES.md` S395 (own-work: `tools/limine-pin-battery-r99.py`, sha256
`c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99` — `def meta_ok` at BYTE 99305
(line 2179), its echo assertion at BYTE 99430 (line 2181), its era assertion at BYTE 99523
(line 2183), the five `c.check_echo = True` sites at BYTEs 79015, 79893, 81666, 83173, 84390, the
five `c.check_era = True` sites at BYTEs 79039, 80414, 81690, 83197, 84414, the two new `LIE_KINDS`
members at BYTE 108455 (line 2370)) and S394 (own-work: `tools/check-limine-pins.py`, sha256
`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` — the gate's MAIN return emits
`"limine_version": limine_version` at BYTE 16931 (line 316) and `"visibility_era": "12.9.5+" if
era_b else "pre-12.9.5"` at BYTE 17037 (line 318), the CANNOT-EVALUATE early return's copies at
BYTE 11230 (line 200) and BYTE 11344 (line 202), `"limine_version_source"` at BYTE 16977
(line 317), `era_b = version >= VISIBILITY_ERA_SPLIT` at BYTE 10910 (line 193), the docstring
phrase at BYTE 4425 (line 47)) and S392 (CPython `int()`: an explicit base accepts leading zeros,
so a leading-zero component is a legal decimal spelling).
verified-at: 2026-11-08 (round 99; the instruments are pinned in
`.ufo/waves/round-99/before/instruments.sha256`).
recheck: 180d — `python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work <scratch> --json OUT` (verdict `met`, `families_passed 105`, `families_total 105`, 0 error rows); `python3 tools/limine-pin-battery-r99.py --selftest` (`selftest PASS 5/5`); `python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family REFUSAL-VERSIONS-9DIGIT-Z --family EXPLICIT-VERSION-ECHO --family EXPLICIT-VERSION-ERA --family LEADING-ZERO-NORMALIZE`

# The accepted-cap families must read the fields they certify

The lane's Limine path-pin gate reports, for an explicit `--limine-version`, the version it acted
on (`limine_version`), where that value came from (`limine_version_source`: `flag` for an explicit
flag, `probe` for the installed-version probe), and the visibility era it selected
(`visibility_era`: `pre-12.9.5` or `12.9.5+`). A battery family that sends a boundary version and
reads only the pin answer certifies the pins and nothing about those three fields. Round 99 gives
the two accepted-cap families — the X-cap and the Y-cap — the same field assertions the Z-cap and
leading-zero families already had, and gives the battery's selftest one lie kind per field.

## 1. What the gate reports on an explicit flag

Two fields are emitted at two sites each, measured at the BYTE level on the pinned bytes
(`python3 -c "b=open('tools/check-limine-pins.py','rb').read(); off=b.find(LITERAL.encode()); line =
b[:off].count(b'\n')+1"`; receipt
`.ufo/waves/round-99/w1/ScribeKnowledge/receipts/01-byte-anchors-measured.txt`):

| site | field | byte | line |
|---|---|---|---|
| MAIN return (after parsing) | `"limine_version": limine_version` | 16931 | 316 |
| MAIN return | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"` | 17037 | 318 |
| MAIN return | `"limine_version_source": limine_version_source` | 16977 | 317 |
| CANNOT-EVALUATE early return | `"limine_version": limine_version` | 11230 | 200 |
| CANNOT-EVALUATE early return | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"` | 11344 | 202 |
| CANNOT-EVALUATE early return | `"limine_version_source": limine_version_source` | 11280 | 201 |

The third `visibility_era` occurrence in the file, BYTE 19205 (line 361), is the gate's own
selftest expectation (`and (want_era is None or r["visibility_era"] == want_era)`), not an
emission site; the third `limine_version` occurrence, BYTE 18866 (line 357), is a consumer line.
Sweep for both: `python3 -c "…b.find(s.encode())…"` over the literals `"visibility_era"` and
`"limine_version"` (receipt 01).

**The echo is the flag's spelling, verbatim, and it names its source.** The emitted value is the
string the flag was given, not a re-rendered tuple: `12.09.4` echoes `12.09.4`, never `12.9.4`.
The source token is a separate field, and it is `flag` for an explicit flag: `main()` sets
`version, version_source = a.limine_version, "flag"` (BYTE 28898, line 510), `check()`'s own
parameter default is `limine_version_source="flag"` (BYTE 10531, line 187), and the field is
emitted at BYTE 11280/16977. Measured on the gate's own JSON, with the seat's fixture (first
physical line an entry, `hash_mismatch_panic: no`, one mismatch pin; receipt
`receipts/gate-spellings-r99.jsonl`):

```
$ python3 tools/check-limine-pins.py --conf <fixture> --esp <esp> --limine-version <spelling>
```

| flag | `limine_version` | `limine_version_source` | `visibility_era` |
|---|---|---|---|
| `999999999.9.9` | `999999999.9.9` | `flag` | `12.9.5+` |
| `12.999999999.4` | `12.999999999.4` | `flag` | `12.9.5+` |
| `0.999999999.0` | `0.999999999.0` | `flag` | `pre-12.9.5` |
| `12.9.999999999` | `12.9.999999999` | `flag` | `12.9.5+` |
| `0.9.999999999` | `0.9.999999999` | `flag` | `pre-12.9.5` |
| `12.09.4` | `12.09.4` | `flag` | `pre-12.9.5` |
| `12.000000009.000000005` | `12.000000009.000000005` | `flag` | `12.9.5+` |
| `12.9.4` | `12.9.4` | `flag` | `pre-12.9.5` |
| `12.9.5` | `12.9.5` | `flag` | `12.9.5+` |

**The era follows the whole numeric tuple, not the first component.** The gate parses each
component with `int()` and compares the tuple against `VISIBILITY_ERA_SPLIT = (12, 9, 5)` (BYTE
7399, line 104); the decision is `era_b = version >= VISIBILITY_ERA_SPLIT` (BYTE 10910, line 193).
So `12.09.4` is era A (the tuple is 12.9.4) while `12.000000009.000000005` is era B (the tuple is
12.9.5) — the spelling's leading zeros do not move the era, and a text comparison would (S392:
`int(x, base)`'s string form accepts leading zeros for an explicit base). The X-cap family
(`999999999.9.9`) and the Y-cap family (`12.999999999.4` era B, `0.999999999.0` era A) are the
accepted-cap cases where "whole tuple" is load-bearing: the Y family's two members put the cap in
the second component, so an era reader that looked at the first component alone would answer era B
and era A correctly for both of them and would pass.

## 2. A family that answers its pins certifies nothing about the fields

A battery family is a list of expectations over a case. If its expectations name only the pin
list, the exit code and the verdict, then a gate that answers every pin correctly while reporting
a wrong `limine_version` or a wrong `visibility_era` satisfies it completely. Sending the
spelling is not reading the answer.

Round 98's wave measured the consequence on the Y-cap spellings: a gate that lies in
`visibility_era` exactly for `12.999999999.4` and `0.999999999.0` read `met 105/105` on the r98
battery — 105 of 105 families, `failed_families []`, 0 error rows. Re-derived by this seat
(receipt `receipts/c1-g6-r98ctl.json`, `.stdout` and `receipts/08-g6-survivor-rederived.txt`):

```
$ python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py --gate \
      .ufo/waves/round-98/w1/ReviewBattery/g6-y-era.py --runs 3 --work <scratch> --json <out>
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
```

(the attack gate is the r98 wave's own artifact
`.ufo/waves/round-98/w1/ReviewBattery/g6-y-era.py`; its only changed line swaps the era label for
those two literals). The **same** attack gate under the r99 battery now reads `unmet` 104/105 with
`failed_families` exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, x3, 0 error rows (receipt
`receipts/c1-g6-r99.json`, `.stdout`) — the survivor is closed by the same file that produced it.
That survivor was the r98 scoreboard's "lie-kind coverage" gap in another guise: the field was
reported by the instrument under test, and the instrument that certified it never read it.

The rule the round generalizes: **a family certifies a reported field only if it reads that field
on its own cases.** Round 98 applied it to the two r97 families (`REFUSAL-VERSIONS-9DIGIT-Z`,
`LEADING-ZERO-NORMALIZE`); round 99 applies it to the two accepted-cap families
(`REFUSAL-VERSIONS-9DIGIT`, `REFUSAL-VERSIONS-9DIGIT-Y`), which are the remaining families that
send a 9-digit boundary member.

Measured on the pinned r99 battery (`tools/limine-pin-battery-r99.py`, sha256 `c2e8c8fc…`), five
family functions set `check_echo`, five set `check_era`, and 99 of the 105 roster families set
neither (receipt `receipts/03-negative-claim-sweeps.txt`, §S4):

| family (roster name) | family function | `c.check_echo = True` | `c.check_era = True` |
|---|---|---|---|
| `REFUSAL-VERSIONS-9DIGIT` (X cap, r99) | `fam_refusal_versions_9digit` | BYTE 79015 (line 1775) | BYTE 79039 (line 1776) |
| `REFUSAL-VERSIONS-9DIGIT-Y` (Y cap, r99) | `fam_refusal_versions_9digit_y` | BYTE 81666 (line 1817) | BYTE 81690 (line 1818) |
| `REFUSAL-VERSIONS-9DIGIT-Z` (r98) | `fam_refusal_versions_9digit_z` | BYTE 83173 (line 1840) | BYTE 83197 (line 1841) |
| `LEADING-ZERO-NORMALIZE` (r98) | `fam_leading_zero_normalize` | BYTE 84390 (line 1857) | BYTE 84414 (line 1858) |
| `EXPLICIT-VERSION-ECHO` | `fam_explicit_version_echo` | BYTE 79893 (line 1792) | — |
| `EXPLICIT-VERSION-ERA` | `fam_explicit_version_era` | — | BYTE 80414 (line 1801) |

The two fields are asserted by two separate lines of `meta_ok` (BYTE 99430 and 99523): the echo
leg requires `got[8] == c.version and got[9] == "flag"` — the echoed spelling **and** the source
token — and the era leg requires `got[10]` to equal the label the case's own tuple selects
(`"12.9.5+" if c.era_b() else "pre-12.9.5"`).

## 3. The two committed bends and their exact readings

Two one-clause bends are committed with the round
(`.ufo/waves/round-99/before/controls/bends/N09-y-era.py`, `N11-x-era.py`; sweep:
`ls .ufo/waves/round-99/before/controls/bends/` → two files). Each is the landed gate with exactly
one expression changed — the `visibility_era` line at line 318 — so each lies in the era label and
in nothing else. The gate's own field readings under each bend (the seat's own run, receipt
`receipts/07-bend-field-readings.txt`):

| spelling | landed gate | `N09-y-era` (second component is the cap) | `N11-x-era` (first component is the cap) |
|---|---|---|---|
| `999999999.9.9` | era `12.9.5+` | era `12.9.5+` (unchanged) | era `pre-12.9.5` (swapped) |
| `12.999999999.4` | era `12.9.5+` | era `pre-12.9.5` (swapped) | era `12.9.5+` (unchanged) |
| `0.999999999.0` | era `pre-12.9.5` | era `12.9.5+` (swapped) | era `pre-12.9.5` (unchanged) |

The echo is never touched by either bend: `grep -c '"limine_version": limine_version'` returns 2
for the gate and 2 for each bend (receipt `receipts/03-negative-claim-sweeps.txt`, §S1).

The readings, from this seat's own runs of the pinned instruments (receipts
`receipts/c1-*.json`, `.stdout`, and the `count-runs.py` summaries):

| leg | battery | runs | reading | failed families | error rows |
|---|---|---|---|---|---|
| landed gate | r99 (`tools/limine-pin-battery-r99.py`) | 3 | `met` 105/105 | `[]` | 0 |
| `N09-y-era` | r99 | 3 | `unmet` 104/105 | exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` | 0 |
| `N09-y-era` | r98 control (`before/controls/do-nothing-battery-r98.py`) | 3 | `met` 105/105 | `[]` | 0 |
| `N11-x-era` | r99 | 3 | `unmet` 103/105 | exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]` | 0 |
| `N11-x-era` | r98 control | 3 | `unmet` 104/105 | exactly `[EXPLICIT-VERSION-ERA]` | 0 |

Commands (the battery's own `--work` scratch is the seat's; `TMPDIR` is passed explicitly):

```
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 \
      --work <scratch> --json <out>
$ python3 tools/limine-pin-battery-r99.py --gate \
      .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 --work <scratch> --json <out>
$ python3 .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py --gate \
      .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 --work <scratch> --json <out>
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family REFUSAL-VERSIONS-9DIGIT \
      --family REFUSAL-VERSIONS-9DIGIT-Y --family REFUSAL-VERSIONS-9DIGIT-Z \
      --family EXPLICIT-VERSION-ECHO --family EXPLICIT-VERSION-ERA --family LEADING-ZERO-NORMALIZE
```

Two things the table says that a summary of "the bends kill" would hide:

- **The Y leg is a flip; the X leg is a delta.** The r98 control is blind to `N09` (`met 105/105`,
  no family named) because no r98 family asserted the era on the Y-cap spellings. On `N11` the
  r98 control already reads `unmet 104/105` with `EXPLICIT-VERSION-ERA` named: the X-cap spelling
  `999999999.9.9` is one of that family's four members (`EXPLICIT_VERSION_META` at BYTE 77183,
  line 1749: `("12.9.4", "12.9.5", "12.9.6", REFUSAL_DIGIT9)`), so the era lie was already caught
  through one EXPLICIT case. Round 99 adds exactly one more failed family there — the X-cap
  family's own four cases (`count-runs.py` names it `[0, 4]`, i.e. 0 passed and 4 failed, while
  `EXPLICIT-VERSION-ERA` reads `[3, 1]`). Counting the X leg as a met-to-unmet closure would
  overstate the round by one family.
- **The per-case counts locate the assertion.** Under `N09` the only failing family is
  `REFUSAL-VERSIONS-9DIGIT-Y` with `[0, 4]`; under `N11` it is `REFUSAL-VERSIONS-9DIGIT` with
  `[0, 4]` beside `EXPLICIT-VERSION-ERA` at `[3, 1]`. `count-runs.py` prints those pairs per run.
- **The echo side has the same shape, witnessed by the r98-carried attack.** The r98 wave's own
  fixed-echo gate `.ufo/waves/round-98/w1/ReviewBattery/g2b-fixed-echo.py` reads `unmet` 100/105
  under the r98 control battery with `failed_families` exactly `[AUTO-ERA-A, AUTO-ERA-B,
  EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` — the X-cap and
  Y-cap families are absent, because on that battery they asserted no echo. Under the r99 battery
  the same gate reads `unmet` 98/105 and names both, `REFUSAL-VERSIONS-9DIGIT` and
  `REFUSAL-VERSIONS-9DIGIT-Y`, each at `[0, 4]`, 0 error rows (receipt
  `receipts/16-g2b-fixed-echo-both-batteries.txt`). The echo side's delta is therefore two
  families, exactly like the era side's.

## 4. What the two new selftest lie kinds certify

The r99 battery's `LIE_KINDS` tuple (BYTE 108277, line 2369) grew from 12 members to 14: the new
`"limine-version"` at BYTE 108455 and `"visibility-era"` at BYTE 108473, both on line 2370. The
wrapper clauses that falsify them are at BYTE 107815 (line 2356) and BYTE 107920 (line 2359):
`limine-version` replaces the echoed value with `0.0.0`, `visibility-era` swaps the label
(`pre-12.9.5` ↔ `12.9.5+`). Roster size: `LIE_KINDS` 14 in r99, 12 in r98 (AST count of the two
tuple literals; receipt `receipts/02-lie-kinds-and-roster.txt`).

With `--selftest --reference <gate>` the battery wraps a scored gate in each lie kind and requires
the battery to read `unmet` for each. The two kinds are therefore the **per-field adversaries**
the r98 scoreboard recorded as missing: before them, no selftest lie falsified `limine_version` or
`visibility_era`, so removing an assertion from a family was invisible to the selftest.

Measured on this seat's own rebuild of the wrappers — the wrapper bytes come from the pinned
battery's own `LIE_WRAPPER` template (`importlib` loads `tools/limine-pin-battery-r99.py`, then
`LIE_WRAPPER % (gate_src, kind)`), so they are the instrument's own bytes, not a hand-written
adversary; the two wrappers are committed as bytes under `receipts/lie-wrappers/`
(sha256 `4fa10dbe…` for `lie-limine-version.py`, `ff420ace…` for `lie-visibility-era.py`) so the
run is reproducible from the receipt directory alone:

```
$ python3 tools/limine-pin-battery-r99.py --gate receipts/lie-wrappers/lie-<kind>.py \
      --runs 3 --work <scratch> --json OUT
families_passed 93/105 verdict unmet failed AUTO-ERA-A,AUTO-ERA-B,AUTO-PROBE-FAIL,AUTO-PROBE-SHAPES,EXPLICIT-VERSION-ECHO,EXTRA-COMPONENT,LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS,REFUSAL-VERSIONS-10DIGIT,REFUSAL-VERSIONS-9DIGIT,REFUSAL-VERSIONS-9DIGIT-Y,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 95/105 verdict unmet failed AUTO-PROBE-FAIL,AUTO-PROBE-SHAPES,EXPLICIT-VERSION-ERA,EXTRA-COMPONENT,LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS,REFUSAL-VERSIONS-10DIGIT,REFUSAL-VERSIONS-9DIGIT,REFUSAL-VERSIONS-9DIGIT-Y,REFUSAL-VERSIONS-9DIGIT-Z
```

(each line x3, 0 error rows; receipts `receipts/c1-lie-limine-version-r99.json`,
`receipts/c1-lie-visibility-era-r99.json`, `.stdout`, and the decomposition in
`receipts/14-lie-composition-own.txt`.)

| lie kind | battery | reading | failing families caused by the falsified field |
|---|---|---|---|
| `limine-version` | r99 | `unmet` 93/105 (12 families failed) | 7 — AUTO-ERA-A, AUTO-ERA-B, EXPLICIT-VERSION-ECHO, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT, REFUSAL-VERSIONS-9DIGIT-Y, REFUSAL-VERSIONS-9DIGIT-Z |
| `visibility-era` | r99 | `unmet` 95/105 (10 families failed) | 5 — EXPLICIT-VERSION-ERA, LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT, REFUSAL-VERSIONS-9DIGIT-Y, REFUSAL-VERSIONS-9DIGIT-Z |

**The limit this section exists for.** A lie kind proves the battery **sees** the field, not that
every family asserts it. Two readings are in the same number and must not be merged:

- The **field-caused** column above is the field's real coverage: those families read the field
  and therefore fail when it is falsified. For `visibility-era` it is exactly the five families
  that set `check_era`; for `limine-version` it is the five that set `check_echo` **plus** the two
  AUTO-era families, whose `auto_ok` leg compares the *probed* version — a different assertion
  (source `probe`), not the flag's echo. So the count of families that read the **flag's** echo
  is five (`check_echo`), and the count that reads the **era label** is five (`check_era`); the
  two AUTO-era families read a probed version and an era label that the era lie also falsifies.
- The remaining failing families — `AUTO-PROBE-FAIL`, `AUTO-PROBE-SHAPES`, `EXTRA-COMPONENT`,
  `REFUSAL-VERSIONS`, `REFUSAL-VERSIONS-10DIGIT` — fail for a **wrapper** reason, not a field
  reason. The wrapper does `out = json.loads(p.stdout)` before it can falsify anything, and a
  refusal answers rc 64 with an **empty** stdout, so `json.loads("")` raises and the wrapper exits
  1. The refusal families then see `rc 1` where they expect `rc 64` (the failing rows read
  `{"version": "12.9", "rc": 1, "stdout_bytes": 0, "ok": false}` against the landed gate's
  `{"version": "12.9", "rc": 64, "stdout_bytes": 0, "ok": true}`).

So the lie kind certifies the *existence* of a per-field adversary and the *visibility* of the
field to the battery; the per-family coverage is carried by the bends in §3, and the five
wrapper-side failures carry no information about either field. A reader who takes `93/105` as
"93 families read the echo" is wrong; the correct count of families that read the echo is five.

## 5. How to re-check this entry

The `recheck:` line above is runnable as written (with a scratch directory substituted for
`<scratch>`); this seat ran it, and the readings are its receipts:

| procedure | observed | receipt |
|---|---|---|
| `python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 --work <scratch> --json OUT` | `met` 105/105 x3, `failed_families []`, 0 error rows, each named family `[4, 0]` | `receipts/c1-gate-r99.json`, `receipts/c1-gate-r99.stdout` |
| `python3 tools/limine-pin-battery-r99.py --selftest` | `selftest PASS 5/5` (`reference-gate skipped (no --reference)`) | `receipts/06-selftest-r99-noref.txt` |
| `python3 .ufo/waves/round-95/before/controls/count-runs.py OUT --family …` on that JSON | per-run `verdict`, `families_passed`, `failed_families`, `error_rows 0`, per-family `[passed, failed]` | `receipts/c1-gate-r99.json` + the table in §3 |
| `sha256sum -c .ufo/waves/round-99/before/instruments.sha256` | 17 files OK, exit 0 (run before any measurement above) | `receipts/01-byte-anchors-measured.txt` |

The bend legs and the r98 control legs are run by substituting the bend path for the gate path
and the control battery for the battery; their readings are in §3.

## Limits

- **The X/Y echo legs have no spelling-targeted bend.** The round's committed bends falsify
  `visibility_era` only; `grep -c '"limine_version": limine_version'` is 2 for the gate and 2 for
  each bend (receipt `receipts/03-negative-claim-sweeps.txt`, §S1), and the whole committed bend
  set is two files (§S2). The echo legs are witnessed instead by two blanket adversaries — the
  `lie-limine-version` wrapper (§4) and the r98-carried fixed-echo attack
  (`.ufo/waves/round-98/w1/ReviewBattery/g2b-fixed-echo.py`), which under the r99 battery reads
  `unmet` 98/105 and names **both** `REFUSAL-VERSIONS-9DIGIT` and `REFUSAL-VERSIONS-9DIGIT-Y`
  with each at `[0, 4]` (receipt `receipts/16-g2b-fixed-echo-both-batteries.txt`). The same
  attack under the r98 control battery reads `unmet` 100/105 and names neither, because on that
  battery those two families asserted no echo at all — which is the delta this round buys on the
  echo side. What is still missing is a **spelling-targeted** echo bend for the X or Y family: the
  witnesses above falsify the echo for *every* explicit flag at once, so they cannot say which
  spelling the family covers.
- **A lie kind is a visibility witness, not a coverage census.** See §4: of the twelve families the
  `limine-version` lie fails, seven fail because of the falsified field and five because the
  wrapper cannot reproduce a refusal's empty stdout. Which families assert which field is carried
  by the assignment sites in §2 and by the bends in §3.
- **The roster is unchanged at 105.** `FAMILY_ROSTER` has 105 entries in both the r98 and the r99
  battery (AST count; receipt §S3), and the r99-vs-r98 diff touches no roster literal
  (`diff tools/limine-pin-battery-r98.py tools/limine-pin-battery-r99.py | grep -E '^[<>]' | grep
  'FAMILY_ROSTER\|FAMILIES ='` → empty). The round sharpens two families; it adds none.
- **Nothing here re-certifies the r92-r98 families.** This entry's propositions are about the
  accepted-cap families and the two new lie kinds. The 99 roster families that set neither
  `check_echo` nor `check_era` (99 = 105 − 6, receipt §S4) are untouched by this round and keep
  exactly the standing they had.
- **The echo assertion fixes the gate's current contract** (verbatim spelling). A gate that
  canonicalizes the echoed value fails the leading-zero family by design; that is a decision to
  re-make, not a family to bend.
- **The bends target the cap spellings by construction.** A field lie on a version whose
  components are all short lies outside both bends' clauses; the era label of such a version is
  still certified by `EXPLICIT-VERSION-ERA` on its own members.
- **No host state is read.** Every reading above comes from the gate's bytes, the battery's bytes
  and generated fixtures; nothing on this host was repaired, upgraded or restarted.
