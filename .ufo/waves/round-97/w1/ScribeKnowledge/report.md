# ScribeKnowledge — round 97, wave w1 (seat report)

Seat: scribe (leaf member, no subagent dispatch). Scope: draft the round's knowledge entry
(prose + provenance) and carry the receipts every number in it rests on.

- **Draft:** `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md` — the draft of
  `corpus/knowledge/limine-bound-9digit-z-r97.md`: the CORPUS provenance trio (`source:`,
  `verified-at:`, `recheck:`), three proposition sections (PC1 the third component's cap, PC2 the
  leading-zero form, PC3 a registry row's declared values), each naming its family and its bend,
  and a Limits section with the two required disclosures plus four more.
- **Receipts:** `.ufo/waves/round-97/w1/ScribeKnowledge/receipts/` (60 files, 4.5 MB).
- **Scratch:** `/fast/scratch/hyaku/tsukuroi-r97/ScribeKnowledge` (deleted before this report).

No instrument was edited, no `make-r*-bends.py` was run, no git/jj mutation was made outside a
scratch clone, no tool was installed or upgraded, no lane file outside this seat dir was written.

## Frozen-instrument check (run before every measurement cited below)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
```

Raw output (receipt `receipts/instruments-sha256-check.txt`, 20 lines):

```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r97.py: OK
tools/make-r97-bends.py: OK
tools/check-registry-content.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-97.md: OK
.ufo/waves/round-97/before/plan-frozen.md: OK
.ufo/waves/round-97/claims.json: OK
.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py: OK
.ufo/waves/round-97/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py: OK
.ufo/waves/round-97/before/controls/do-nothing-r96-calibration.py: OK
.ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py: OK
.ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py: OK
.ufo/waves/round-97/before/registry-baseline.json: OK
.ufo/waves/round-97/before/fixtures/doctored.diff: OK
.ufo/waves/round-97/before/fixtures/doctored-recipe.txt: OK
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
```

**19 OK, 1 FAILED.** The FAILED line is `before/fixtures/build-doctored-fixture.sh` — the *recipe*,
not an instrument the claims read. It was corrected after the freeze (the L1's amendment A1 records
this and pins the corrected set in `before/instruments-r97-after-fixture-pin.sha256`, 20/20 OK).
Every instrument the two claims read (`check-limine-pins.py`, `limine-pin-battery-r97.py`,
`make-r97-bends.py`, `check-registry-content.py`, `check-registry-coverage.py`,
`check-r96-calibration.py`, both bend files, both do-nothing controls) is `OK`. I did not edit the
recipe and did not run it; I re-derived the doctored table in my own scratch (below).

## C1 — measured legs

### 1. Landed gate, three runs

```
$ python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 \
    --work /fast/scratch/hyaku/tsukuroi-r97/ScribeKnowledge/work-gate \
    --json <seat>/receipts/c1-gate-landed.json
```

Raw output (receipt `receipts/c1-gate-landed.txt`):

```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
rc=0
```

```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py <seat>/receipts/c1-gate-landed.json \
    --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

Raw output (receipt `receipts/c1-gate-landed-count-runs.json`, condensed):

```
met 105 / 105 [] error_rows 0 {'REFUSAL-VERSIONS-9DIGIT-Z': [4, 0], 'LEADING-ZERO-NORMALIZE': [4, 0]}
met 105 / 105 [] error_rows 0 {'REFUSAL-VERSIONS-9DIGIT-Z': [4, 0], 'LEADING-ZERO-NORMALIZE': [4, 0]}
met 105 / 105 [] error_rows 0 {'REFUSAL-VERSIONS-9DIGIT-Z': [4, 0], 'LEADING-ZERO-NORMALIZE': [4, 0]}
```

Roster size by AST (receipt `receipts/pc1-roster-size.txt`): `FAMILY_ROSTER length: 105`; last four
`['REFUSAL-VERSIONS-9DIGIT-Y', 'EXTRA-COMPONENT', 'REFUSAL-VERSIONS-9DIGIT-Z',
'LEADING-ZERO-NORMALIZE']`.

### 2. Per-case answers of the two new families (run 0 of the landed gate)

Receipt `receipts/pc1-pc2-case-rows.txt` (from `receipts/c1-gate-landed.json`):

```
REFUSAL-VERSIONS-9DIGIT-Z    version=12.9.999999999          rc=1 verdict=DEGRADED era-answer=panic  passed=True error=None
REFUSAL-VERSIONS-9DIGIT-Z    version=0.9.999999999           rc=1 verdict=DEGRADED era-answer=prompt passed=True error=None
LEADING-ZERO-NORMALIZE       version=12.09.4                 rc=1 verdict=DEGRADED era-answer=prompt passed=True error=None
LEADING-ZERO-NORMALIZE       version=000000012.9.4           rc=1 verdict=DEGRADED era-answer=prompt passed=True error=None
LEADING-ZERO-NORMALIZE       version=12.000000009.000000005  rc=1 verdict=DEGRADED era-answer=panic  passed=True error=None
LEADING-ZERO-NORMALIZE       version=000000000.000000000.000000000 rc=1 verdict=DEGRADED era-answer=prompt passed=True error=None
```

### 3. Parser probe (era follows the numeric tuple)

```
$ python3 <scratch>/probe/parse-probe.py tools/check-limine-pins.py
```

Raw output (receipt `receipts/pc2-parse-probe.txt`):

```
12.9.999999999                   -> (12, 9, 999999999) era 12.9.5+
0.9.999999999                    -> (0, 9, 999999999) era pre-12.9.5
12.09.4                          -> (12, 9, 4)       era pre-12.9.5
000000012.9.4                    -> (12, 9, 4)       era pre-12.9.5
12.000000009.000000005           -> (12, 9, 5)       era 12.9.5+
000000000.000000000.000000000    -> (0, 0, 0)        era pre-12.9.5
999999999.9.9                    -> (999999999, 9, 9) era 12.9.5+
12.999999999.4                   -> (12, 999999999, 4) era 12.9.5+
12.9.5                           -> (12, 9, 5)       era 12.9.5+
12.9.4                           -> (12, 9, 4)       era pre-12.9.5
rc=0
```

The probe imports the **frozen** `tools/check-limine-pins.py` read-only and calls its own
`parse_limine_version()` and `VISIBILITY_ERA_SPLIT`; it edits nothing.

### 4. Bend `N05-z-cap-8`, three runs

```
$ python3 tools/limine-pin-battery-r97.py --gate \
    .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py --runs 3 --work <scratch>/work-n05 \
    --json <seat>/receipts/c1-bend-N05.json
```

Raw output (receipt `receipts/c1-bend-N05.txt`):

```
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
rc=1
```

count-runs (receipt `receipts/c1-bend-N05-count-runs.json`):

```
unmet 103 / 105 ['LEADING-ZERO-NORMALIZE', 'REFUSAL-VERSIONS-9DIGIT-Z'] error_rows 6 {'LEADING-ZERO-NORMALIZE': [2, 2], 'REFUSAL-VERSIONS-9DIGIT-Z': [0, 4]}
unmet 103 / 105 ['LEADING-ZERO-NORMALIZE', 'REFUSAL-VERSIONS-9DIGIT-Z'] error_rows 6 {'REFUSAL-VERSIONS-9DIGIT-Z': [0, 4], 'LEADING-ZERO-NORMALIZE': [2, 2]}
unmet 103 / 105 ['LEADING-ZERO-NORMALIZE', 'REFUSAL-VERSIONS-9DIGIT-Z'] error_rows 6 {'LEADING-ZERO-NORMALIZE': [2, 2], 'REFUSAL-VERSIONS-9DIGIT-Z': [0, 4]}
```

The six error rows of run 0 (receipt `receipts/c1-bend-N05.json`) are all the bend's own rc-64
refusal: `bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h] … check-limine-pins:
--limine-version must be X.Y.Z or auto` — four in `REFUSAL-VERSIONS-9DIGIT-Z`, two in
`LEADING-ZERO-NORMALIZE`.

### 5. Bend `N06-leading-zero-reject`, three runs

```
$ python3 tools/limine-pin-battery-r97.py --gate \
    .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py --runs 3 --work <scratch>/work-n06 \
    --json <seat>/receipts/c1-bend-N06.json
```

Raw output (receipt `receipts/c1-bend-N06.txt`):

```
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
rc=1
```

count-runs (receipt `receipts/c1-bend-N06-count-runs.json`):

```
unmet 104 / 105 ['LEADING-ZERO-NORMALIZE'] error_rows 4 {'LEADING-ZERO-NORMALIZE': [0, 4], 'REFUSAL-VERSIONS-9DIGIT-Z': [4, 0]}
```

### 6. Do-nothing blindness legs (the r96 battery, frozen control)

```
$ python3 .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py --gate <gate> --runs 3 \
    --work <scratch>/work-dn-* --json <seat>/receipts/c1-dn-*.json
```

Raw output (receipts `receipts/c1-dn-gate.txt`, `receipts/c1-dn-bend-N05.txt`,
`receipts/c1-dn-bend-N06.txt`):

```
c1-dn-gate:        families_passed 103/103 verdict met failed -   (×3)   rc=0
c1-dn-bend-N05:    families_passed 103/103 verdict met failed -   (×3)   rc=0
c1-dn-bend-N06:    families_passed 103/103 verdict met failed -   (×3)   rc=0
```

The r96 roster carries neither new family (receipt `receipts/limits-r96-instrument-level.txt`:
`grep -n 'Z_DIGIT9\|LEADING_ZERO' …/do-nothing-battery-r96.py` → no match).

### 7. Instrument-level scope (the `--usage-check` mode)

- The r97 battery's `--usage-check` on the landed gate reads `verdict met`; on `N05-z-cap-8` it
  reads `unmet` with `12.9.999999999` and `0.9.999999999` refused rc 64 (receipt
  `receipts/c1-usage-N05.txt`); on `N06-leading-zero-reject` it reads `unmet` with `12.09.4`,
  `00.00.00` **and** `000000012.9.4` refused rc 64 (receipt `receipts/c1-usage-N06.txt`).
- The r96 battery's `--usage-check` on `N06-leading-zero-reject` reads `unmet` with `12.09.4` and
  `00.00.00` refused rc 64 (receipt `receipts/c1-dn-usage-N06.txt`); on the landed gate and on
  `N05-z-cap-8` it reads `met` (receipts `receipts/c1-dn-usage-landed.txt`,
  `receipts/c1-dn-usage-N05.txt`).

**Finding (scope, not a defect):** the leading-zero class was already sampled at *instrument*
level before this round (the r96 `--usage-check` sends `12.09.4` and `00.00.00`), so
`LEADING-ZERO-NORMALIZE` is new at **roster** level only; the **Z** class is unsampled by both legs
of the r96 instrument. The draft states this in PC2's scope note and in Limits. The L1's amendment
A3 records the same narrowing.

## C2 — measured legs

### 1. Landed revision

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master
a57e88cd57f30bae206d908b534508d9463bf734
$ python3 tools/check-registry-content.py --revision a57e88cd57f30bae206d908b534508d9463bf734 \
    --json <seat>/receipts/c2-content-landed.json
```

Raw output (receipt `receipts/c2-content-landed.txt` / `.json`):

```
registry-content: status PASS bindings 7/7 findings 0
rc=0
{"bindings": 7, "findings": [], "revision": "a57e88cd57f30bae206d908b534508d9463bf734",
 "rows": 154, "schema": "tsukuroi-registry-content-r97-v1", "status": "PASS"}
```

```
$ python3 tools/check-registry-content.py --selftest
```

Raw output (receipt `receipts/c2-content-selftest.txt`, 12 case lines):

```
clean PASS / default-cell PASS / fixtures-cell PASS / schema-cell PASS / roster-pinned-cell PASS /
roster-verdict-cell PASS / cases-cell PASS / span-cell PASS / row-missing PASS / tool-missing PASS /
derivation-lie PASS / tally-lie PASS
selftest PASS 12/12
rc=0
```

### 2. Coverage gate at the landed revision

```
$ python3 tools/check-registry-coverage.py --revision a57e88cd57f30bae206d908b534508d9463bf734
```

Raw output (receipt `receipts/c2-coverage-landed.json`):

```
{"branch":"master","branch_tip":"a57e88cd…","counts":{"findings":3,"missing":3,"registered":154,
 "rows_total":154,"tools_total":157},
 "findings":[REGISTRY-ROW-MISSING tools/check-registry-content.py,
             REGISTRY-ROW-MISSING tools/limine-pin-battery-r97.py,
             REGISTRY-ROW-MISSING tools/make-r97-bends.py],
 "revision":"a57e88cd…","status":"FAIL"}
```

**Reading, not a defect:** at the landed commit the round's three new tools are committed while
their three registry rows land only at settle, so the coverage gate itself reads `FAIL` with three
`REGISTRY-ROW-MISSING` findings there. This is the state the L1's amendment A4 describes. It does
not affect the blindness leg, which is measured on a doctored revision (below).

### 3. The doctored table (re-derived in scratch; the frozen recipe was NOT run)

Recipe (identical substitutions to `before/fixtures/doctored-recipe.txt`, asserted to match exactly
once each): `default `auto`` → `default `12.9.4``; `(39 fixtures` → `(88 fixtures`; `roster 103 (`
→ `roster 99 (`; `FAMILY_ROSTER, 103,` → `FAMILY_ROSTER, 99,`; ``--selftest` (7 cases`` →
``--selftest` (29 cases``; `r96 VARIANTS N01-N04` → `r96 VARIANTS N01-N05``.

Two scratch clones, each `git clone --shared` of the lane (read-only), each with one commit made
**in the clone** with the fixture identity after asserting
`git -C <clone> rev-parse --show-toplevel` equals the clone path:

- **A — pinned pre-round base `f48d1642`** (receipts `receipts/c2-doctored-r96tip.txt`,
  `receipts/c2-content-doctored-r96tip.txt`, `receipts/c2-coverage-doctored-r96tip.json`):

```
FINDING RC-VALUE-MISMATCH SKILL.md:5923 RC-ENTRY-DEFAULT states '12.9.4', tools/check-limine-pins.py derives 'auto'
FINDING RC-VALUE-MISMATCH SKILL.md:5923 RC-SELFTEST-COUNT states '88', tools/check-limine-pins.py derives '39'
FINDING RC-VALUE-MISMATCH SKILL.md:5938 RC-ROSTER-VERDICT states '99', tools/limine-pin-battery-r96.py derives '103'
FINDING RC-VALUE-MISMATCH SKILL.md:5938 RC-ROSTER-PINNED states '99', tools/limine-pin-battery-r96.py derives '103'
FINDING RC-VALUE-MISMATCH SKILL.md:5940 RC-CAL-SELFTEST states '29', tools/check-r96-calibration.py derives '7'
FINDING RC-VALUE-MISMATCH SKILL.md:5939 RC-BEND-SPAN states 'N01-N05', tools/make-r96-bends.py derives 'N01-N04'
registry-content: status FAIL bindings 1/7 findings 6
content rc=1
coverage rc=0
{"status":"PASS","counts":{"findings":0,"missing":0,"registered":154,"rows_total":154,"tools_total":154},"findings":[]}
```

- **B — the working-tree `SKILL.md` on the lane master base** (receipts
  `receipts/c2-content-doctored-master.txt`, `receipts/c2-coverage-doctored-master.json`): the same
  six `RC-VALUE-MISMATCH` findings, `content rc=1`, and coverage
  `{"status":"PASS","counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157},"findings":[]}`.

A third clone (base = lane master with the *committed* `SKILL.md`, i.e. without the round's three
uncommitted rows) reads coverage `FAIL` with the three `REGISTRY-ROW-MISSING` findings — receipt
`receipts/c2-coverage-doctored.json`; the content leg is the same six findings (receipt
`receipts/c2-content-doctored.txt`).

### 4. The "before" leg

```
$ git ls-tree -r --name-only f48d1642 -- tools/check-registry-content.py
(empty)
```

Receipt `receipts/pc3-before-leg.txt`: the checker does not exist at the pre-round tip, and the
operative table there carries 154 rows.

### 5. Binding inventory

Receipt `receipts/pc3-binding-inventory.txt` (printed from the frozen checker's own `BINDINGS`):

```
bindings: 7 rows bound: 4 ['check-r96-calibration', 'limine-pin-battery-r96', 'limine-pins', 'make-r96-bends']
  RC-ENTRY-DEFAULT row limine-pins cell 2 tool tools/check-limine-pins.py
  RC-SELFTEST-COUNT row limine-pins cell 4 tool tools/check-limine-pins.py
  RC-SCHEMA row limine-pins cell 5 tool tools/check-limine-pins.py
  RC-ROSTER-VERDICT row limine-pin-battery-r96 cell 3 tool tools/limine-pin-battery-r96.py
  RC-ROSTER-PINNED row limine-pin-battery-r96 cell 5 tool tools/limine-pin-battery-r96.py
  RC-CAL-SELFTEST row check-r96-calibration cell 4 tool tools/check-r96-calibration.py
  RC-BEND-SPAN row make-r96-bends cell 5 tool tools/make-r96-bends.py
```

## PASS / FAIL per expected line (the draft's claims)

| expected line | measured | receipt | verdict |
|---|---|---|---|
| Landed gate 105/105 met, `failed_families []`, 0 error rows, three runs | 105/105 met ×3, `failed []`, 0 error rows | `c1-gate-landed.txt`, `c1-gate-landed-count-runs.json` | PASS |
| Roster 103 → 105, two families added | AST `FAMILY_ROSTER length: 105`; last two are the new families | `pc1-roster-size.txt` | PASS |
| `12.9.999999999` in-bound, era B, answered `panic`, rc 1 | case row: rc 1, `DEGRADED`, era-answer `panic` | `pc1-pc2-case-rows.txt` | PASS |
| `0.9.999999999` in-bound, era A, answered `prompt`, rc 1 | case row: rc 1, `DEGRADED`, era-answer `prompt` | `pc1-pc2-case-rows.txt` | PASS |
| Z family 4 cases, all passed, per run | `[4, 0]` per run ×3 | `c1-gate-landed-count-runs.json` | PASS |
| `N05-z-cap-8` → 103/105 unmet, failed exactly the two families | 103/105 unmet, `['LEADING-ZERO-NORMALIZE','REFUSAL-VERSIONS-9DIGIT-Z']` ×3 | `c1-bend-N05.txt`, `c1-bend-N05-count-runs.json` | PASS |
| `N05` carries exactly 6 non-null error rows, the bend's own rc-64 refusal | 6 per run ×3; 4 Z + 2 LZ; all `JSONDecodeError rc=64` | `c1-bend-N05-count-runs.json`, `c1-bend-N05.json` | PASS |
| `N06-leading-zero-reject` → 104/105 unmet, failed exactly `LEADING-ZERO-NORMALIZE` | 104/105 unmet, `['LEADING-ZERO-NORMALIZE']` ×3 | `c1-bend-N06.txt`, `c1-bend-N06-count-runs.json` | PASS |
| `N06` carries exactly 4 non-null error rows, same rc-64 class | 4 per run ×3, all `JSONDecodeError rc=64` | `c1-bend-N06-count-runs.json`, `c1-bend-N06.json` | PASS |
| r96 do-nothing battery blind to both new families | 103/103 met ×3 on the landed gate and on both bends | `c1-dn-gate.txt`, `c1-dn-bend-N05.txt`, `c1-dn-bend-N06.txt` | PASS |
| `parse_limine_version` normalizes by `int()`, era follows the numeric tuple | `000000012.9.4`→(12,9,4) A; `12.000000009.000000005`→(12,9,5) B | `pc2-parse-probe.txt` | PASS |
| Content checker at the landed revision: `status PASS`, `findings []`, `bindings 7` | `PASS bindings 7/7 findings 0`, 154 rows | `c2-content-landed.txt`, `.json` | PASS |
| Content checker `--selftest` 12/12 | `selftest PASS 12/12` | `c2-content-selftest.txt` | PASS |
| Doctored table: content `FAIL`, exactly six `RC-VALUE-MISMATCH`, one per doctor, each naming its row | 6 findings, ids all `RC-VALUE-MISMATCH`, sites `SKILL.md:5923/5938/5939/5940` | `c2-content-doctored-r96tip.txt` | PASS |
| Coverage gate on that doctored revision: `PASS 154/154`, findings 0 | `PASS registered 154 rows_total 154 tools_total 154 findings []` | `c2-coverage-doctored-r96tip.json` | PASS |
| Before: no such checker exists; the coverage gate certifies the doctored table | `git ls-tree … tools/check-registry-content.py` → empty at `f48d1642` | `pc3-before-leg.txt` | PASS |
| Content checker binds 4 of 154 rows (7 cells) | `bindings: 7 rows bound: 4`; `rows: 154` | `pc3-binding-inventory.txt`, `c2-content-landed.json` | PASS |
| Families sample a bounded set of spellings, not every form | `CASES_PER_FAMILY = 4`; Z cycles 2 spellings (×2 each), LZ cycles 4 (×1 each) | `limits-family-shapes.txt`, `limits-distinct-versions.txt` | PASS |
| Instruments byte-identical to the freeze manifest | 19 OK, 1 FAILED — the FAILED line is the *recipe* (amendment A1), not an instrument the claims read | `instruments-sha256-check.txt` | PASS (with the recipe caveat stated) |

## Findings (reported, not edited)

1. **The r96 do-nothing battery's blindness is a roster-level statement, not an instrument-level
   one.** The r96 `--usage-check` mode already sends `12.09.4` and `00.00.00` and reads `unmet` on
   `N06-leading-zero-reject` on exactly those two rows (receipt `c1-dn-usage-N06.txt`). So
   `LEADING-ZERO-NORMALIZE` is a roster-level closure and the Z class is unsampled by both r96 legs
   (receipt `limits-r96-instrument-level.txt`). The L1's amendment A3 records the same narrowing;
   the draft carries it as PC2's scope note and as a Limits bullet.
2. **The coverage gate reads `FAIL` at the landed commit `a57e88cd`** with three
   `REGISTRY-ROW-MISSING` findings for the round's three new tools (receipt
   `c2-coverage-landed.json`): they are committed while their registry rows land only at settle.
   The blindness leg therefore has to be read on a doctored revision (or after settle), which the
   draft states in PC3's scope note. Same ground as amendment A4.
3. **The freeze manifest's one FAILED line is the recipe, not an instrument** (A1). The instruments
   every claim reads are `OK`. I re-derived the doctored table in scratch rather than running the
   corrected recipe, so the recipe's bytes never entered a measurement.
4. **The new SOURCES row's byte anchors do not match the pinned copy.** The row added to
   `corpus/SOURCES.md` in the worktree (`S392`) claims "`int` heading (`id="int"` at byte 153028)"
   and "quoted phrase at byte 157622". Measured against the same pin (331022 B, sha256
   `d92580dd…`, receipt `pc2-s392-row-bytes.txt`): the only `id="int"` occurrence is at byte
   **153202** (byte 153028 is inside `builtins.input/result`), and the phrase "An explicit base
   accepts a radix string with leading zeros" occurs **0 times** in the file — the phrase
   "radix string" occurs 0 times. The two real anchors are "have leading zeros" at byte
   **157767** and "Base 0 also disallows leading zeros: `int('010', 0)` is not legal, while
   `int('010')` and `int('010', 8)` are." at byte **159303** (receipt
   `pc2-int-doc-anchors.txt`). My draft cites the corrected bytes and quotes the source verbatim;
   the corpus row's own anchor cells need the L1's correction (the row is a corpus file — not
   mine to edit).
5. **The plan's Limits sentence about the families' spelling sample is looser than the
   measurement.** The plan reads "The two new families sample four spellings per class … the
   four-member `LEADING-ZERO-NORMALIZE` cycle covers one member per case ordinal". Measured
   (receipt `limits-distinct-versions.txt`, three runs of the landed-gate battery JSON): each
   family sends **four cases** per run (`CASES_PER_FAMILY = 4`), but the Z family draws them from
   **two** distinct spellings (`12.9.999999999` and `0.9.999999999`, each sent twice per run),
   while the leading-zero family draws its four cases from **four** distinct spellings, one per
   ordinal. So "four spellings per class" holds for `LEADING-ZERO-NORMALIZE` and not for
   `REFUSAL-VERSIONS-9DIGIT-Z`. The draft states the measured shape ("four cases per member
   class": two spellings for Z, four for leading-zero) instead of repeating the plan's phrasing,
   so no universal is claimed that the instrument does not send.

## Relation to the entry the L1 already wrote

The L1 wrote `corpus/knowledge/limine-bound-9digit-z-r97.md` in the worktree while this seat
worked. My draft agrees with it on every clause I could measure (the three propositions, the two
families, the two bends, the seven bindings, the limits). Two differences for the L1's eye: (a) the
draft cites the S-id as `S### (new row this round)` per the seat brief, with the corrected byte
anchors, so the L1 substitutes the assigned id and the anchor cells; (b) the draft states the
r96-instrument-level scope of the leading-zero class and the coverage gate's landed-commit
reading explicitly (findings 1 and 2 above), which the worktree entry compresses.

## Constraints honoured

Only `.ufo/waves/round-97/w1/ScribeKnowledge/` (this report, the draft and `receipts/`) and the
scratch root `/fast/scratch/hyaku/tsukuroi-r97/ScribeKnowledge` were written; the scratch tree was
deleted before this report. No lane file was edited: `tools/`, `SKILL.md`, `corpus/`,
`SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-97/before/`, `claims.json` are all
untouched by this seat. `tools/make-r97-bends.py` and every earlier `make-r*-bends.py` were **not**
run; every bend used is the frozen copy under `before/controls/bends/`, and the doctored table was
re-derived in scratch with the six substitutions asserted to match exactly once. The only commits
made were inside two scratch clones, each after `git -C <clone> rev-parse --show-toplevel` printed
that clone's path, with the fixture identity only. No git/jj mutation in the lane repo. No tool was
installed or upgraded (no pacman transaction, no `uv tool`, no `~/.local/bin` write) — the round
needed only `python3` 3.14.8, `git`, `bwrap` and `python3 -I`, all present.

{"seat": "ScribeKnowledge", "verdict": "findings", "notes": "Draft at .ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md; seat report and 60 receipts under the seat dir. Own measurements: landed gate 105/105 met x3 with 0 error rows and each new family [4,0]; N05-z-cap-8 103/105 unmet with failed_families exactly [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z] and 6 rc-64 refusal rows per run; N06-leading-zero-reject 104/105 unmet with failed_families [LEADING-ZERO-NORMALIZE] and 4 rc-64 rows per run; r96 do-nothing battery 103/103 met x3 on the landed gate and on both bends (blindness); parser probe confirms parse_limine_version normalizes by int() so 000000012.9.4 = 12.9.4 (era A) and 12.000000009.000000005 = 12.9.5 (era B); content checker PASS bindings 7/7 findings 0 at a57e88cd, selftest 12/12; doctored table in two scratch clones gives exactly six RC-VALUE-MISMATCH findings while the coverage gate reads PASS 154/154 findings 0 (pinned base) and PASS 157/157 (settled rows). Five findings: (1) the r96 battery's --usage-check already sent 12.09.4 and 00.00.00, so the leading-zero class is new at roster level only and the Z class is unsampled by both r96 legs (L1 amendment A3 agrees); (2) the coverage gate reads FAIL with three REGISTRY-ROW-MISSING at the landed commit because the round's three tools land before their registry rows (amendment A4 agrees); (3) the freeze manifest's single FAILED line is the doctored-fixture recipe, not an instrument any claim reads, and I re-derived the fixture in scratch instead of running it; (4) the new SOURCES row's byte anchors do not match its own pin (id=\"int\" is at 153202 not 153028; the quoted phrase occurs 0 times; the real anchors are 157767 and 159303) and the draft cites the corrected bytes; and the plan's 'four spellings per class' limit is looser than the measurement (the Z family draws its four cases from two spellings, the leading-zero family from four), so the draft states the measured shape instead. The new row's id is left as S### for the L1 to substitute."}
