# ReviewBattery — round 96 / wave w1 / attack on C1 (depth)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
HEAD at first measurement `59cbfe2f4b96a73c2697cf81eb989e1d72e276fd`; HEAD when the report was written
`a814f24dc31270bca4e8999ac3cd907ecd72f100`. The five round instruments are byte-identical at both
revisions and in the working tree (see §0), so every receipt below transfers to `a814f24d`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r96/ReviewBattery` (all fixtures/bwrap dirs; deleted before yield).
Seat receipts: `.ufo/waves/round-96/w1/ReviewBattery/`.

**Verdict headline.** The four new families exist, are wired into the verdict, and each carries its
discriminating element per case; the landed gate reads `103/103 met` in three canonical runs and in
three runs from a `git clone --shared` (0 error rows); N01/N03/N04 fail exactly the frozen family
lists at the frozen counts; the r95 do-nothing battery is blind to `EXPLICIT-VERSION-ECHO`,
`EXPLICIT-VERSION-ERA` and `REFUSAL-VERSIONS-9DIGIT-Y` and reads `98/99` on N04 with exactly
`["REFUSAL-VERSIONS"]`. **But** the frozen target's "*each bend … 0 error rows*" clause is false for
N02 by construction: the bend's rc-64 refusal yields four non-null `error` rows, and the frozen kill
rule says "*unmet if any bend run … carries a non-null `error` row*". C1 is therefore **unmet as
written** at N02 unless an amendment carves the bend's own refusal rows out (r95's A1 did exactly
that for N05). Two lie classes also survive the *whole* instrument set (battery 103, `--usage-check`,
gate selftest 39/39); they do not falsify the frozen predicate but they bound what the four families
certify. Details and raw bytes below.

## 0. Freeze / identity of the instruments and controls

```
$ sha256sum -c .ufo/waves/round-96/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r96.py: OK
tools/make-r96-bends.py: OK
tools/check-r96-calibration.py: OK
tools/check-registry-coverage.py: OK
.ufo/plans/round-96.md: OK        … (17 entries, all OK)
EXIT=0
```

Receipt: `receipts-freeze-check.txt` (also carries `git show HEAD:tools/check-r96-calibration.py |
sha256sum` = `7ff63524…` and an empty `git diff` for that file). At HEAD `a814f24d` the five
instruments read `7d79ac29 / f06d90ae / efd1b2a1 / 7ff63524 / 6fcb2d0a` — identical to the manifest.

Control identity (item 3, second half):

```
$ git show b8f878c8:tools/limine-pin-battery-r95.py | sha256sum
a51dca18d3c7641664a2f64476a7abc2bb14ff1133772f109ac73490828b9ebb  -
$ sha256sum .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py
a51dca18…  (IDENTICAL)
$ git show b8f878c8:tools/check-limine-pins.py | sha256sum    → 7d79ac29…
$ sha256sum .ufo/waves/round-96/before/controls/do-nothing-gate-r95.py  → 7d79ac29…  (IDENTICAL)
```

So `before/controls/do-nothing-battery-r95.py` is byte-identical to the r95 landed battery, and the
gate is unchanged this round. **PASS.**

## 1. Roster parse — expected 103 (item 1)

Command (independent AST parse, no import of the roster from the battery's own checker):

```
$ python3 .ufo/waves/round-96/w1/ReviewBattery/derive-roster.py
```

Raw (trimmed):

```
"r95_roster": 99, "r95_unique": 99,
"r96_roster": 103, "r96_unique": 103,
"r95_families_table": 99, "r96_families_table": 103,
"r96_families_equals_roster_order": true,
"new_names": ["EXPLICIT-VERSION-ECHO","EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT-Y","EXTRA-COMPONENT"],
"removed_names": [],
"new_family_first_index": {"EXPLICIT-VERSION-ECHO":99,"EXPLICIT-VERSION-ERA":100,"REFUSAL-VERSIONS-9DIGIT-Y":101,"EXTRA-COMPONENT":102},
"cases_per_family": 4
```

Per-case discriminators (each family built 4× with a cleared `_SEQ`, `receipts/roster-parse.json`
holds the JSON):

```
EXPLICIT-VERSION-ECHO      case0..3 versions 12.9.4, 12.9.5, 12.9.6, 999999999.9.9; check_echo=True each; expected DEGRADED
EXPLICIT-VERSION-ERA       case0..3 same four versions; check_era=True each
REFUSAL-VERSIONS-9DIGIT-Y  case0..3 versions 12.999999999.4, 0.999999999.0, 12.999999999.4, 0.999999999.0 (era_b True,False,True,False)
EXTRA-COMPONENT            case0..3 usage = 12.9.6.1, 12.9.6.1.0, 12.9.6.99, 12.9.6.7 + positive 12.9.6 each
```

Expected line: roster size 103. **PASS.** Expected line: four new names present and no removals.
**PASS.** Expected line: every new family has at least one case carrying its discriminating element —
stronger here: all four cases of each explicit family enumerate the four frozen versions exactly once
(`index % 4`), the Y family enumerates both Y-cap values, and every EXTRA-COMPONENT case sends all
five values. **PASS.**

## 2. The four requested forgers (item 2)

Forgers are the landed gate bytes with one clause changed; rebuilt idempotently by
`build-forgers.py` (replacement count asserted; hashes in `receipts-forger-build.txt`).

| forger | clause changed | battery (r96, 1 run) | families_passed | failed_families |
|---|---|---|---|---|
| F-A-source-probe | both `limine_version_source` emissions → `"probe"` (2 sites) | unmet | 102/103 | `["EXPLICIT-VERSION-ECHO"]` |
| F-B-era-first-component | `era_b = (version[0],0,0) >= split` | unmet | 95/103 | `AUTO-ERA-B, ERA-B-FIRST-BODY, ERA-EXACT-125, ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B, EXPLICIT-VERSION-ECHO, EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT-Y` |
| F-B2-era-max-component | `era_b = max(version) >= 12` | unmet | 95/103 | `AUTO-ERA-A, ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, EXPLICIT-VERSION-ECHO, EXPLICIT-VERSION-ERA, FIRST-LINE-ENTRY, REFUSAL-VERSIONS-9DIGIT-Y` |
| F-C-blanket-refusal | `parse_limine_version` returns None for every input | unmet | 3/103 | 100 families (all but `AUTO-PROBE-FAIL`, `AUTO-PROBE-SHAPES`, `REFUSAL-VERSIONS`) |
| F-D-echo-12.9.6 | explicit flag echoes `12.9.6` (2 sites) | unmet | 102/103 | `["EXPLICIT-VERSION-ECHO"]` |

Receipts: `forge-F-A-source-probe-1run.json`, `forge-F-B-era-first-component-1run.json`,
`forge-F-B2-era-max-component-1run.json`, `forge-F-C-blanket-refusal-1run.json`,
`forge-F-D-echo-12.9.6-1run.json`. **No assigned forger reads `met`.**

Micro-fixture matrix (one era-sensitive conf, every version through every gate;
`receipts/micro-fixture-matrix.json`) — the landed gate's own answers, which the families encode:

| version | landed `visibility_era` / pin consequence | F-A source | F-B era / pin | F-B2 era / pin | F-D echo |
|---|---|---|---|---|---|
| 12.9.4 | pre-12.9.5 / prompt | probe | pre / prompt | **12.9.5+ / panic** | **12.9.6** |
| 12.9.5 | 12.9.5+ / panic | probe | **pre / prompt** | 12.9.5+ / panic | **12.9.6** |
| 12.9.6 | 12.9.5+ / panic | probe | **pre / prompt** | 12.9.5+ / panic | 12.9.6 |
| 999999999.9.9 | 12.9.5+ / panic | probe | 12.9.5+ / panic | 12.9.5+ / panic | **12.9.6** |
| 12.999999999.4 | 12.9.5+ / panic | probe | **pre / prompt** | 12.9.5+ / panic | **12.9.6** |
| 0.999999999.0 | pre-12.9.5 / prompt | probe | pre / prompt | **12.9.5+ / panic** | **12.9.6** |
| 12.9.6.1 | rc 64, stdout 0 | rc 64 | rc 64 | rc 64 | rc 64 |

Which family catches what: `EXPLICIT-VERSION-ECHO` alone catches F-A and F-D (the only family that
reads `limine_version` + `limine_version_source` for an explicit flag). The two era forgers are caught
by the new `EXPLICIT-VERSION-ECHO`/`ERA`/`9DIGIT-Y` families **and** by five pre-existing era families,
i.e. the era-selector bug class was already partly covered; the new families add the *label* and the
Y-cap accepted leg. The blanket refuser is caught by 100 families, but **not** by `REFUSAL-VERSIONS`
(see F4).

## 3. The four bends (item 3)

```
$ for n in N01-echo-wrong N02-y-cap-8 N03-era-label-flip N04-extra-components; do
    diff -u tools/check-limine-pins.py .ufo/.../bends/$n.py | grep -c '^@@' ; …
```

Each diff is exactly one hunk with one `-` and one `+` line. **PASS.** The changed lines:

```
N01: -            "limine_version": limine_version,
     +            "limine_version": "99.9.9" if limine_version_source == "flag" else limine_version,  # N01 (echo bent)
N02: -    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
     +    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (len(p) <= 8 or p is not parts[1])) for p in parts):  # N02 (Y bound bent to <=8)
N03: -            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",
     +            "visibility_era": "pre-12.9.5" if era_b else "12.9.5+",  # N03 (label bent)
N04: -    if len(parts) != 3 or not all(...):
     +    if len(parts) < 3 or not all(...):  # N04p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
```

Authoring notes (no reading changes): N02's `p is not parts[1]` is an identity test (it only matters
when a 9-digit component is duplicated, which no family sends; my parse probe shows N02 accepts
`999999999.9.9` and refuses both Y-cap values, i.e. the intended one-clause bend). N04's inserted line
carries a mangled trailing comment (leftover source text after `#`); cosmetic.

Bend readings, 1 run each, canonical lane (receipts `bend-N0*-1run.json`; N02 also 3 runs,
`bend-N02-y-cap-8-3runs.json`):

| bend | verdict | passed | failed_families | error rows |
|---|---|---|---|---|
| N01 | unmet | 102/103 | `["EXPLICIT-VERSION-ECHO"]` | 0 |
| N02 | unmet ×1 and ×3 | 102/103 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | **4** (4 in every one of the four runs) |
| N03 | unmet | 102/103 | `["EXPLICIT-VERSION-ERA"]` | 0 |
| N04 | unmet | 101/103 | `["EXTRA-COMPONENT","REFUSAL-VERSIONS"]` | 0 |

Do-nothing (r95) battery, run by me (the committed `after/`/wave receipts did not exist at my first
run; `ExecDoNothing/*.log` were 0 bytes then):

| gate | r95 battery | passed | failed_families | error rows |
|---|---|---|---|---|
| landed gate | met ×3 (+1) | 99/99 | `[]` | 0 |
| N01 | met | 99/99 | `[]` | 0 |
| N02 | met ×3 (+1) | 99/99 | `[]` | 0 |
| N03 | met | 99/99 | `[]` | 0 |
| N04 | unmet ×3 (+1) | 98/99 | `["REFUSAL-VERSIONS"]` | 0 |

Receipts: `dn-gate-3runs.json`, `dn-N0*-1run.json`, `dn-N02-y-cap-8-3runs.json`,
`dn-N04-extra-components-3runs.json`. The blindness claim (three new families + the four-component
correction invisible to the r95 roster; the pre-existing `12.9.5.1` row is the only thing that bites)
is confirmed in every leg I ran. **PASS.**

## 4. N04 and the frozen "each bend fails exactly …" sentence (item 4)

`bend-N04-extra-components-1run.json`:

```
verdict unmet  passed 101/103  failed ['EXTRA-COMPONENT', 'REFUSAL-VERSIONS']  error_rows 0
```

This matches the frozen sentence exactly (count, both members, order-independent). **PASS.**

**Distance found — N02.** The frozen target says "*each bend: 102/103 (N04 101/103) unmet … with
exactly the frozen failed_families and **0 error rows***" and the frozen kill rule says "*unmet if any
bend run is not `unmet`, **carries a non-null `error` row**, or its `failed_families` is not exactly
the frozen list*". N02 carries four non-null error rows (`receipts-N02-error-rows.txt`):

```
error_rows 4
 family= REFUSAL-VERSIONS-9DIGIT-Y passed= False want= [1,'DEGRADED',[[3,'LP-MISMATCH','panic'],[7,'OK','none']],'menu']
 error= bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h] [--conf CONF] …
 (×4: both Y-cap values, twice each, all refused rc 64 with empty stdout)
```

This is structural, not a flake: the Y family is a *normal* family (not a `usage` family), so the
bend's rc-64 refusal has no JSON for `run_gate` to parse and the battery records
`bad-output: JSONDecodeError rc=64` — a non-null `error` row — for every refused case. The r95 claim
knew this and carved it out: "*its four N05 case rows carry the battery's error text (the bend refuses
rc 64 and emits no JSON — the bend's refusal receipt, expected in this leg only)*", and r95's kill
rule did **not** count error rows on the bend leg. Round 96's sentence dropped that carve-out, so the
same measurement that makes the family list exact makes the error-row clause false.

Calibrated effect: **the substantive readings are all correct** (102/103, exact `failed_families`,
0 error rows everywhere else, 4 refusal rows on N02 only); **the sentence as frozen is not
satisfiable** by its own instrument. After this receipt the L1 filed the distance as **A3** (not A1,
which is this round's id-narrowing): "*0 error rows on every landed-gate and do-nothing leg; on a bend
leg only the bend's own refusal rows, named and counted (N02: 4/run)*"; the frozen sentence stays as
filed and the closure judges the narrowing. This is the r95 A1 precedent applied to N05's four
rc-64 rows.

## 5. Findings

**F1 (HIGH, claim-level, C1).** The frozen C1 target and kill rule are contradicted by the N02 leg's
four non-null `error` rows (rc-64 refusal, no JSON). C1 is unmet as written unless amended (§4).
Evidence: `receipts-N02-error-rows.txt`, `bend-N02-y-cap-8-1run.json`, `bend-N02-y-cap-8-3runs.json`,
`bend-N01/N03/N04-1run.json` (0 rows each).

**F2 (MEDIUM, instrument coverage; does not falsify the frozen predicate).** Two lie classes pass the
entire instrument set — r96 battery `103/103 met`, `--usage-check met`, gate `--selftest 39/39`:

- **F-E `label-boundary-only`** (receipt `forge-F-E-label-boundary-only-1run.json`): `visibility_era`
  is `pre-12.9.5` only when the tuple is exactly `(12,9,4)`, else `12.9.5+`; pins stay correct. It
  mislabels every version below 12.9.4 (e.g. `0.999999999.0` gets `12.9.5+` although the gate's pins
  answer era A), and nothing reads the label for a below-split version other than 12.9.4: the four
  frozen versions are `12.9.4, 12.9.5, 12.9.6, 999999999.9.9`, Y's `0.999999999.0` is checked for
  pins only, and the gate selftest's `want_era` cases are 12.9.4/12.9.5/12.9.6 only.
- **F-G `trailing-zero-accepted`** (receipt `forge-F-G-trailing-zero-accepted-1run.json`): a fourth
  component that is all zeros (`12.9.6.0`) is accepted; the published grammar is `X.Y.Z`. Nothing
  sends a zero-valued extra component: `EXTRA-COMPONENT` sends `.1/.1.0/.99/.7`, `REFUSAL-VERSIONS`
  sends `12.9.5.1`, `--usage-check` sends `12.9.6.1`.

Both survivors are bounded — they do not make a *wrong* gate pass the four versions the predicate
names — but they show the families certify "these four values", not "the era field"/"the
four-component shape". Next-round frontier candidates: a below-split label case (e.g. `0.9.9` or
`12.0.0`) and a `.0`/`.0.0` extra-component refusal.

**F3 (LOW, frozen docstring).** `fam_refusal_versions_9digit_y`'s docstring says a gate that "reads
the era from X alone answers era B for `0.999999999.0`". F-B (`era_b = (version[0],0,0) >= split`)
answers **era A** for that value — correctly — and is still caught (on the `12.999999999.4` row and by
the pre-existing era families). The only simple one-component reading that makes `0.999999999.0` era B
is "largest component" (F-B2), which also mislabels `12.9.4`. The sentence's parenthetical mechanism
is wrong as written; the family's discriminating claim (an X-only era selector fails) still holds.
Frozen bytes — recorded, not edited.

**F4 (LOW, anti-blanket control).** `REFUSAL-VERSIONS` never sends its documented positive control:
`REFUSAL_VERSIONS` has no `"12.9.4"` member, so `positives = {"12.9.4"}` is never exercised and a gate
that refuses *every* version passes the family (F-C: 3/103, the three passes are `AUTO-PROBE-FAIL`,
`AUTO-PROBE-SHAPES`, `REFUSAL-VERSIONS`). The anti-blanket pair lives in `REFUSAL-VERSIONS-10DIGIT`
(appends `"12.9.4"`) and `EXTRA-COMPONENT` (positive `12.9.6`), both of which F-C does fail. The
family docstring's "positive control" sentence therefore describes the generic runner, not this
family. Not introduced this round; worth a one-line correction in a later commit.

**F5 (process note, not a defect at report time).** At ~07:54 the working tree carried an
uncommitted 6-insertion/4-deletion edit of `tools/check-r96-calibration.py` (sha256
`ad894667f951d2cc900ca240509c56207f7dee486448ac8782a2808fc13aa1d9`) that made `sha256sum -c` fail on
that entry (the edit flattened whitespace before the F3/F4 phrase searches). By my freeze receipt the
file is back to the frozen `7ff63524…` (HEAD `59cbfe2f`/`a814f24d` both carry the frozen bytes). If a
later commit lands the flattened-whitespace version, C2 voids under its own clause; at measurement
time the freeze holds. My only action was observation; I wrote no lane byte.

**F6 (info).** Control identity and the do-nothing blindness are as frozen (§0, §3); the landed gate
and battery are byte-unchanged from the r95 gate and frozen r96 battery in both layouts.

## 6. Verification gaps (what these receipts do *not* cover)

- I ran the canonical lane once per bend (N02 three times) and the clone leg only for the **landed
  gate** (3 runs at `59cbfe2f`; instrument bytes identical at `a814f24d`). The claim's
  "both layouts" for each bend and for the r95 do-nothing N04 leg is ExecBend/ExecDoNothing's
  evidence; I did not replicate those clone legs.
- The r95 do-nothing legs I ran are canonical only (1 run for N01/N02/N03; 3 runs for the landed gate
  and N04).
- Freshness of fixtures per run follows from the code (`secrets.randbits`, `mkdtemp`, `rname`), not
  from a per-run diff; the battery does not record fixture names.
- I did not execute the C2 checker, registry gate or the lane's own selftests beyond the gate's
  `--selftest` on the two survivor forgers; C2 is ReviewCalibration's surface.

## Receipts index (all written by this seat)

```
receipts-freeze-check.txt                 sha256sum -c manifest + git show HEAD + git diff
receipts-forger-build.txt                 seven forgers rebuilt, replacement counts + sha256
receipts/roster-parse.json                independent roster parse + per-case discriminators
receipts-count-runs.txt                   count-runs.py over the landed 3 runs, four families, EXIT=0
receipts-landed-extract.txt               per-run verdicts + echo/source/usage rows
receipts/micro-fixture-matrix.json        landed + 4 forgers × 7 versions on one era-sensitive conf
receipts-N02-error-rows.txt               N02's four non-null error rows, raw
selftest-survivors.txt                    gate --selftest 39/39 on F-E and F-G
usagecheck-F-E/…, usagecheck-F-G/…        --usage-check met for both survivors
c1-landed-3runs.json                      103/103 met ×3 canonical (0 error rows)
c1-clone-59cbfe2f-3runs.json              103/103 met ×3 clone (0 error rows)
bend-N01/N02/N03/N04-1run.json            bend readings (N02: 4 error rows)
bend-N02-y-cap-8-3runs.json               N02 ×3 (same four error rows each run)
dn-gate-3runs.json, dn-N0*-1run.json, dn-N02-y-cap-8-3runs.json, dn-N04-*-3runs.json  do-nothing legs
receipts-summary-table.txt                every battery run under this seat, verdict/passed/failed/errors
forge-F-A…F-G-1run.json                   forger battery readings
forgers/*.py                              seven forgers (one clause each)
derive-roster.py, build-forgers.py, summarise.py   the derivation/rebuild scripts
```

{"seat": "ReviewBattery", "verdict": "findings", "notes": "C1's four new families are present, wired and discriminating (roster 99->103, per-case enumeration verified; landed gate 103/103 met x3 canonical + x3 clone at 59cbfe2f with identical instrument bytes at a814f24d, 0 error rows; N01/N03/N04 exactly the frozen families at 102/102/101 of 103; r95 do-nothing battery blind to ECHO/ERA/Y (99/99) and 98/99 [REFUSAL-VERSIONS] on N04; both layouts for bends not replicated here). Distance from the frozen sentence: N02 carries 4 non-null error rows (bad-output: JSONDecodeError rc=64 for the bend's own refusals), while the target demands 0 error rows per bend and the kill rule reads 'unmet if any bend run carries a non-null error row' -> C1 unmet as written unless the clause is narrowed; L1 filed it as A3 after this receipt (bend legs carry only the bend's own named/counted refusal rows, N02 4/run). Two lie classes survive the whole instrument set (label correct only at 12.9.4+; trailing .0 extra component accepted): both met 103/103, usage-check met, gate selftest 39/39 - scope limit, not a predicate falsification. Also: fam_refusal_versions_9digit_y docstring misdescribes its own X-only counterexample; REFUSAL-VERSIONS has no positive control so a blanket refuser passes it; a transient uncommitted edit of the frozen C2 checker was observed at ~07:54 and is gone (freeze holds at receipt)."}
