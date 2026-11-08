# Round 96 w1 — MutBound (mutation tester) — seat report

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Seat dir: `.ufo/waves/round-96/w1/MutBound/`.
Scratch root used and deleted: `/fast/scratch/hyaku/tsukuroi-r96/MutBound/`.
No lane byte was written: the gate, the battery, the emitter and the four frozen bends were opened read-only;
`tools/make-r96-bends.py` and `tools/make-r95-bends.py` were **not** run.

## Contract and method

- Mutation unit: one clause of `tools/check-limine-pins.py` (frozen sha256
  `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`).
- 8 mutants were derived (M01–M08), each by a substitution asserted to match **exactly once** and to change
  exactly one line; the emitter is `w1/MutBound/make_mutants.py`, the manifest with per-mutant sha256 and
  the two-line unified diff is `w1/MutBound/mutants-manifest.json`. The seat brief's ninth example
  ("four components accepted") is the exact clause of frozen N04, so it is exercised as N04 in §4 rather
  than duplicated; M05 (`Y <= 8`) and N02 are the same behavioral point with different implementation
  strings and serve as an independent reproduction of that family's kill.
- Detector (assigned): `python3 tools/limine-pin-battery-r96.py --gate <GATE> --runs 1 --work <scratch>
  --json <seat>/receipts/<name>.json`, exit 0 iff `met`. Batteries are run by `w1/MutBound/run_gates.py`.
- "error rows" is counted the way the round's own counting command counts it:
  `.ufo/waves/round-95/before/controls/count-runs.py:26` — a `case_log` entry whose `error` is not null.
- Order: pristine copy → 8 mutants → the four frozen bends → restored bytes. The restored leg re-copies the
  lane gate over the scratch copy, re-hashes, and re-runs the battery.
- Environment: Python 3.14.8, `/usr/bin/bwrap`, `/usr/bin/limine`, no installs or upgrades
  (`w1/MutBound/environment.txt`). End-state `sha256sum -c .ufo/waves/round-96/before/instruments.sha256`
  reads **17/17 OK**, including the gate and all four bend files.

## Commands and raw output

### 1. Mutant derivation (exactly-one-match assertions inside the emitter)

```
$ python3 .ufo/waves/round-96/w1/MutBound/make_mutants.py --out /fast/scratch/hyaku/tsukuroi-r96/MutBound/mutants
M01-source-flag-always sha256=cad2f916eb5f63366c93ca139565dd4c1d2c854adb98e13a3171d140e0e3dbb7 diff=-            "limine_version_source": limine_version_source, | +            "limine_version_source": "flag",  # M01 (source always flag)
M02-source-probe-always sha256=287766dd93e66b8887256a3665aa6b5bea62186a4c779d0029b97eb250123e2d diff=-            "limine_version_source": limine_version_source, | +            "limine_version_source": "probe",  # M02 (source always probe)
M03-era-from-x-only sha256=62cbc213da7ed824ee35580dda8d5d981cb6624f21e4a196688b3b7f9701a9ed diff=-    era_b = version >= VISIBILITY_ERA_SPLIT | +    era_b = version[0] >= VISIBILITY_ERA_SPLIT[0]  # M03 (era from X only)
M04-era-split-12-10-0 sha256=3f2c1b376ad7e12285a08cae07a0de6b304fa0fbce5455fcdf7416199d4fc54b diff=-VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut | +VISIBILITY_ERA_SPLIT = (12, 10, 0)   # M04 (split bent)
M05-y-cap-8 sha256=410d005e724247c54d7a5bc1fa12a0f4c1db37f8069459d10ad85d4176085cab diff=-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts): | +    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (i != 1 or len(p) <= 8)) for i, p in enumerate(parts)):  # M05 (Y cap bent)
M06-z-cap-8 sha256=d433f0de4e08eb9b6fa7772e77a4a3faab56534e803aac1603804e137f0e03f3 diff=-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts): | +    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (i != 2 or len(p) <= 8)) for i, p in enumerate(parts)):  # M06 (Z cap bent)
M07-echo-lower sha256=ccc03aba3fdcd46c2e860dfe2502b6bf09637105e28df6700dc1e66d79d9a600 diff=-            "limine_version": limine_version, | +            "limine_version": limine_version.lower(),  # M07 (echo lowered)
M08-refusal-9digit-below-1e8 sha256=7f51f6d6652a0548effae81b560896fff6890996486511abbff80b806060c7b9 diff=-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts): | +    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 and (len(p) != 9 or int(p) >= 100000000) for p in parts):  # M08 (9-digit values below 1e8 refused)
wrote 8 mutants; pristine sha256=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
```

### 2. Pristine baseline (before any mutant)

```
$ cp tools/check-limine-pins.py /fast/scratch/hyaku/tsukuroi-r96/MutBound/pristine.py
$ sha256sum /fast/scratch/hyaku/tsukuroi-r96/MutBound/pristine.py tools/check-limine-pins.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  /fast/scratch/hyaku/tsukuroi-r96/MutBound/pristine.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
$ python3 tools/limine-pin-battery-r96.py --gate /fast/scratch/hyaku/tsukuroi-r96/MutBound/pristine.py --runs 1 --work /fast/scratch/hyaku/tsukuroi-r96/MutBound/work-pristine --json .ufo/waves/round-96/w1/MutBound/receipts/baseline-pristine.json
families_passed 103/103 verdict met failed -
ELAPSED 40.51 s
EXIT=0
```

Receipt: `receipts/baseline-pristine.json` — 412 cases, `failed_families []`, `error_rows 0` (frozen
`count-runs.py` on the same file: `"verdict": "met"`, `"error_rows": 0`, exit 0).

### 3. The eight mutants (`--runs 1` each; runner receipts)

```
M01-source-flag-always exit=1 families_passed 101/103 verdict unmet failed AUTO-ERA-A,AUTO-ERA-B
M02-source-probe-always exit=1 families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ECHO
M03-era-from-x-only exit=1 families_passed 96/103 verdict unmet failed AUTO-ERA-A,ERA-DEFAULT,ERA-FLE-MEASURED-A,ERA-FLE-PANIC-A,EXPLICIT-VERSION-ECHO,EXPLICIT-VERSION-ERA,FIRST-LINE-ENTRY
M04-era-split-12-10-0 exit=1 families_passed 96/103 verdict unmet failed AUTO-ERA-B,ERA-B-FIRST-BODY,ERA-EXACT-125,ERA-FLE-MEASURED-B,ERA-FLE-PANIC-B,EXPLICIT-VERSION-ECHO,EXPLICIT-VERSION-ERA
M05-y-cap-8 exit=1 families_passed 102/103 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
M06-z-cap-8 exit=0 families_passed 103/103 verdict met failed -
M07-echo-lower exit=0 families_passed 103/103 verdict met failed -
M08-refusal-9digit-below-1e8 exit=0 families_passed 103/103 verdict met failed -
```

Receipts: `receipts/mutA-M01-source-flag-always.json` … `receipts/mutD-M08-refusal-9digit-below-1e8.json`
(+ matching `.log` files, `receipts/results-mutA.tsv` … `results-mutD.tsv`). Error rows (count-runs
definition, `summary.json`): M05 = **4** (its four `REFUSAL-VERSIONS-9DIGIT-Y` cases are rc-64
refusals with empty stdout, recorded as `bad-output: JSONDecodeError rc=64`), every other mutant = 0.

### 4. The four frozen bends (own runs, `--runs 1` each)

```
N01-echo-wrong exit=1 families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ECHO
N02-y-cap-8 exit=1 families_passed 102/103 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
N03-era-label-flip exit=1 families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ERA
N04-extra-components exit=1 families_passed 101/103 verdict unmet failed EXTRA-COMPONENT,REFUSAL-VERSIONS
```

Frozen r95 counter on the bend receipts (`receipts/countruns-*.txt`), the round's own counting command
with the four named families:

| bend | verdict | families_passed | failed_families (frozen counter) | error_rows | named family passed/failed |
|---|---|---|---|---|---|
| N01 | unmet | 102/103 | `["EXPLICIT-VERSION-ECHO"]` | 0 | ECHO 0/4; ERA 4/0; Y 4/0; EXTRA 4/0 |
| N02 | unmet | 102/103 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | **4** | ECHO 4/0; ERA 4/0; Y 0/4; EXTRA 4/0 |
| N03 | unmet | 102/103 | `["EXPLICIT-VERSION-ERA"]` | 0 | ECHO 4/0; ERA 0/4; Y 4/0; EXTRA 4/0 |
| N04 | unmet | 101/103 | `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]` | 0 | ECHO 4/0; ERA 4/0; Y 4/0; EXTRA 0/4 |

**N04 set exactly: `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]`** — 8 failed cases, 4 in each family.

### 5. Kill matrix (case counts from the receipts; empty = family passed)

```
| family | baseline | N01 | N02 | N03 | N04 | M01 | M02 | M03 | M04 | M05 | M06 | M07 | M08 | restored |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXPLICIT-VERSION-ECHO |  | 4 |  |  |  |  | 4 | 1 | 2 |  |  |  |  |  |
| EXPLICIT-VERSION-ERA |  |  |  | 4 |  |  |  | 1 | 2 |  |  |  |  |  |
| REFUSAL-VERSIONS-9DIGIT-Y |  |  | 4 |  |  |  |  |  |  | 4 |  |  |  |  |
| EXTRA-COMPONENT |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |
| AUTO-ERA-A |  |  |  |  |  | 4 |  | 4 |  |  |  |  |  |  |
| AUTO-ERA-B |  |  |  |  |  | 4 |  |  | 4 |  |  |  |  |  |
| ERA-B-FIRST-BODY |  |  |  |  |  |  |  |  | 4 |  |  |  |  |  |
| ERA-DEFAULT |  |  |  |  |  |  |  | 4 |  |  |  |  |  |  |
| ERA-EXACT-125 |  |  |  |  |  |  |  |  | 4 |  |  |  |  |  |
| ERA-FLE-MEASURED-A |  |  |  |  |  |  |  | 4 |  |  |  |  |  |  |
| ERA-FLE-MEASURED-B |  |  |  |  |  |  |  |  | 4 |  |  |  |  |  |
| ERA-FLE-PANIC-A |  |  |  |  |  |  |  | 4 |  |  |  |  |  |  |
| ERA-FLE-PANIC-B |  |  |  |  |  |  |  |  | 4 |  |  |  |  |  |
| FIRST-LINE-ENTRY |  |  |  |  |  |  |  | 4 |  |  |  |  |  |  |
| REFUSAL-VERSIONS |  |  |  |  | 4 |  |  |  |  |  |  |  |  |  |
```

Source: `w1/MutBound/matrix.md` (generated by `w1/MutBound/analyze.py` from the 14 receipts; also
`summary.json`, `summary-table.txt`).

**Which new family kills which mutant.** `EXPLICIT-VERSION-ECHO` kills M02 (all 4 cases: source
`probe` where `flag` is required) and N01 (all 4: echo `99.9.9`); it also flags M03 (1 case) and M04
(2 cases) because its fixture is era-sensitive and the era bends change the pin consequence — the
metadata assertion itself is exercised only by M02/N01 (`got`/`want` case dumps in the receipts).
`EXPLICIT-VERSION-ERA` kills M03 (1 case: 12.9.4), M04 (2 cases: 12.9.5, 12.9.6) and N03 (4 cases:
inverted label). `REFUSAL-VERSIONS-9DIGIT-Y` kills M05 and N02 (4 rc-64 refusals each).
`EXTRA-COMPONENT` kills N04 (4 cases; the pre-existing `REFUSAL-VERSIONS` family kills the other 4).
M01 is killed only by the pre-existing `AUTO-ERA-A`/`AUTO-ERA-B` families (4 cases each).

### 6. Restored bytes

```
before-restore scratch=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
lane=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
after-restore scratch=7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
pristine exit=0 families_passed 103/103 verdict met failed -
```

Receipt: `receipts/restore-pristine.json` (`met`, 103/103, 0 error rows, 0 failed cases).

### 7. Survivor probes (diagnostic, not a rescore)

`w1/MutBound/probe_survivors.py` builds one healthy fixture and compares the landed gate with each
survivor (`receipts/survivor-probes.json`):

```
M06 version=12.9.999999999     landed_rc=0 mutant_rc=64 identical_stdout=False
M08 version=000000001.0.0      landed_rc=0 mutant_rc=64 identical_stdout=False
M07 version=12.9.4             landed_rc=0 mutant_rc=0 identical_stdout=True
M07 version=12.09.4            landed_rc=0 mutant_rc=0 identical_stdout=True
```

## PASS/FAIL per expected line

| id | expected | observed | verdict |
|---|---|---|---|
| E1 | 8 mutants, each substitution matches exactly once and changes text | emitter asserts `count == 1` and a two-line diff for all 8; would have aborted otherwise; manifest records sha256 + diff | **PASS** |
| E2 | one battery run per mutant, `--runs 1`, verdict/families/failed/errors recorded | 8/8 receipts with exact raw lines above | **PASS** |
| E3 | N01 failed_families exactly `["EXPLICIT-VERSION-ECHO"]` | exactly that (4 cases, 0 errors) | **PASS** |
| E4 | N02 failed_families exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]` | exactly that (4 cases) | **PASS** |
| E4b | frozen C1 target: each bend carries **0 error rows** | N02 carries **4** error rows under `count-runs.py`'s own count (M05, same clause, also 4) | **FAIL** (finding F4) |
| E5 | N03 failed_families exactly `["EXPLICIT-VERSION-ERA"]` | exactly that (4 cases, 0 errors) | **PASS** |
| E6 | N04 failed_families exactly `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]` | exactly that set, 101/103, 8 cases, 0 errors | **PASS** |
| E7 | pristine gate: 103/103 met, 0 error rows | `met 103/103`, 412 cases, 0 errors | **PASS** |
| E8 | restored bytes equal before-hash and re-run met | sha256 `7d79ac29…` before and after; `met 103/103`, 0 errors | **PASS** |
| E9 | each new family has at least one own-run kill | ECHO→N01/M02; ERA→N03/M03/M04; Y→N02/M05; EXTRA→N04 | **PASS** |
| E10 | survivors disclosed | M06, M07, M08 reported below, no silent pass | **PASS** |

## Findings (Frontier rows, not hidden)

1. **F1 — the Z component's 9-digit boundary is not certified by any family (M06 SURVIVED).**
   M06 applies the `<= 8` cap to the third component only; the battery reads `103/103 met` in all 412
   cases. The landed gate accepts the in-bound `12.9.999999999` (probe: rc 0, JSON echoes it, era B)
   and M06 refuses it (rc 64, empty stdout), so this is a real behavior delta the roster never sends.
   r95 added the X-boundary accepted leg, r96 added the Y leg; the Z leg remains open, and QUALITY 139
   ("a numeric bound … certified at its boundary") is satisfied per-component only for X and Y.

2. **F2 — a 9-digit component with leading zeros is not sent (M08 SURVIVED).**
   M08 refuses 9-digit components whose integer value is < 100000000 (e.g. `000000001.0.0`), which the
   gate's own contract accepts ("leading zeros are accepted and normalized by `int()`"). The landed
   gate answers rc 0 for `000000001.0.0`; M08 refuses rc 64; the battery is blind (103/103). A
   leading-zero 9-digit accepted member would close it. This is distinct from F1 (digit count, not the
   Z position).

3. **F3 — M07 (`limine_version.lower()`) is an equivalent mutant, not a coverage gap.**
   `parse_limine_version` admits only ASCII digits and two dots, the CLI rejects everything else with
   rc 64 before `check()`, and `probe_limine_version` returns the regex's digits-and-dots group; on
   every reachable accepted version `limine_version.lower() == limine_version`. Probe: identical
   stdout for `12.9.4` and `12.09.4`. [INFERENCE from the parser/probe code, backed by the two probe
   runs.] No black-box family can kill it; it is reported as equivalent rather than as a gap.

4. **F4 — N02's 4 error rows contradict the frozen "each bend … 0 error rows" clause.**
   The four `REFUSAL-VERSIONS-9DIGIT-Y` cases of N02 are rc-64 refusals with empty stdout, which the
   battery records as `"error": "bad-output: JSONDecodeError rc=64 …"`; the frozen
   `.ufo/waves/round-95/before/controls/count-runs.py` therefore prints `"error_rows": 4`. This is the
   same accounting relation round 95 recorded in its A1 amendment (0 on the landed leg, 4 on the
   over-strict-refusal bend); round 96 froze the unamended "0 error rows" sentence and the kill rule
   "unmet if any bend run … carries a non-null `error` row". The family kill itself is exact
   (`failed_families` as frozen); what cannot be met as written is the error-row clause. An amendment
   (or the reading "no unexpected error rows") is owed by the L1; the instrument and the frozen text
   were not edited here.

Not a defect, recorded for attribution: `EXPLICIT-VERSION-ECHO`'s fixture is era-sensitive, so era
bends also fail it on the cases whose expected pin consequence changes (1 of 4 for M03, 2 of 4 for
M04). Its declared metadata assertion is exercised by M02 and N01.

## Receipts (all under `.ufo/waves/round-96/w1/MutBound/`)

- 14 battery receipts: `receipts/baseline-pristine.json`, `receipts/mutA-M01…json`, `receipts/mutA-M02…`,
  `receipts/mutB-M03…`, `receipts/mutB-M04…`, `receipts/mutC-M05…`, `receipts/mutC-M06…`,
  `receipts/mutD-M07…`, `receipts/mutD-M08…`, `receipts/bendA-N01-echo-wrong.json`,
  `receipts/bendA-N02-y-cap-8.json`, `receipts/bendB-N03-era-label-flip.json`,
  `receipts/bendB-N04-extra-components.json`, `receipts/restore-pristine.json` (+ matching `.log`).
- Frozen-counter receipts: `receipts/countruns-baseline-pristine.txt`,
  `receipts/countruns-bendA-N01-echo-wrong.txt`, `receipts/countruns-bendA-N02-y-cap-8.txt`,
  `receipts/countruns-bendB-N03-era-label-flip.txt`, `receipts/countruns-bendB-N04-extra-components.txt`.
- Derived summaries: `summary.json`, `summary-table.txt`, `matrix.md`,
  `mutants-manifest.json`, `survivor-probes.json`, `environment.txt`, `frozen-manifest-check.txt`.
- Mutant bytes (seat copies, sha256 in the manifest): `mutants/M01-source-flag-always.py` …
  `mutants/M08-refusal-9digit-below-1e8.py`.
- Emitters/runners: `make_mutants.py`, `run_gates.py`, `analyze.py`, `probe_survivors.py`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r96/MutBound/` was removed after the runs; every cited receipt
  lives under this seat dir.

{"seat":"MutBound","verdict":"findings","notes":"8/8 one-clause mutants scored with the assigned --runs 1 battery: 5 killed (M01 by pre-existing AUTO-ERA-A/B; M02 by new EXPLICIT-VERSION-ECHO; M03/M04 by new EXPLICIT-VERSION-ERA plus pre-existing era families; M05 by new REFUSAL-VERSIONS-9DIGIT-Y), 3 survive (M06 9-digit-Z cap, M07 lower() equivalent mutant, M08 9-digit leading-zero refusal). Frozen bends re-run from own runs: N01->[EXPLICIT-VERSION-ECHO], N02->[REFUSAL-VERSIONS-9DIGIT-Y], N03->[EXPLICIT-VERSION-ERA], N04->[EXTRA-COMPONENT,REFUSAL-VERSIONS] exactly (101/103, 8 cases). Pristine baseline and restored bytes both 103/103 met, 0 error rows, sha256 7d79ac29 identical. Finding F4: N02 carries 4 error rows under count-runs.py's own count (rc-64 refusal recorded as bad-output), contradicting the frozen 'each bend ... 0 error rows' clause (r95-A1 relation); family kill is exact. Receipts under .ufo/waves/round-96/w1/MutBound/."}
