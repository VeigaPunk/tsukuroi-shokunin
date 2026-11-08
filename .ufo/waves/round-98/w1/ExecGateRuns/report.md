# ExecGateRuns — C1 landed-gate legs (canonical + clone)

Seat: ExecGateRuns. Lane: tsukuroi-shokunin. Round 98 wave w1.
Assignment: measure C1's landed-gate leg twice — canonical lane layout and a
`git clone --shared` — plus roster integrity, `--usage-check`, `--selftest`, and
count-runs parsing of every gate JSON.

## 0. Axes (Godspeed)

The move is measured, not aimed: the frontier walks on two axes —
(1) landed-gate certainty (does the pinned r98 battery read `met 105/105` on the
unchanged gate, in both layouts?), and (2) cross-layout invariance (do canonical
and clone agree byte-for-byte on the instruments and run-for-run on the verdict?).
Cheapest parallel iteration: sha256 manifest + roster AST + usage-check + selftest
run concurrently with the two long batteries; keep moves that improve either axis
and harm none. No instrument was edited; every number below is a run I executed.

## 1. Instruments pinned (sha256sum -c)

Command:

```
sha256sum -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/before/instruments.sha256
```

Raw output (receipt: `01-sha256sum.txt`):

```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/before/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py: OK
.ufo/waves/round-98/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py: OK
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py: OK
.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py: OK
.ufo/waves/round-98/before/registry-baseline-r98.json: OK
.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D1: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2lie: OK
.ufo/waves/round-98/before/dev/c1-gate-runs3.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c2-selftest-r98.txt: OK
.ufo/waves/round-98/before/dev/c2-selftest-r97.txt: OK
.ufo/waves/round-98/before/dev/c2-doctored-summary.txt: OK
rc=0
```

PASS: 27/27 OK. The gate is the frozen unchanged bytes
`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`
(receipt `01-sha256sum.txt`; re-verified after the runs, receipt `11-sha-after.txt`,
also 27/27 OK rc=0). Python: 3.14.8 (receipt `01-python.txt`).

## 2. Canonical layout — landed gate, 3 runs

Command (from the lane root, `cwd=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`):

```
python3 tools/limine-pin-battery-r98.py --gate tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/canon-work --json <SeatDir>/c1-gate-canonical.json
```

Raw output (receipt `03-canonical.txt`):

```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
rc=0
```

Per run (parsed from `c1-gate-canonical.json`, receipt `10-per-run.txt`):

| run | families_passed/families_total | verdict | failed_families | error_rows | REFUSAL-VERSIONS-9DIGIT-Z passed/failed | LEADING-ZERO-NORMALIZE passed/failed | cases |
|---|---|---|---|---|---|---|---|
| 0 | 105/105 | met | [] | 0 | 4/0 | 4/0 | 420 |
| 1 | 105/105 | met | [] | 0 | 4/0 | 4/0 | 420 |
| 2 | 105/105 | met | [] | 0 | 4/0 | 4/0 | 420 |

PASS: each run `105/105 met`, `failed_families []`, 0 error rows, `cases 420`.

## 3. Clone layout — landed gate, 3 runs

Commands:

```
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone
python3 /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone/tools/limine-pin-battery-r98.py --gate /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone/tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone-work --json <SeatDir>/c1-gate-clone.json
```

Clone receipts (`05-clone.txt`): `git -C <clone> rev-parse --show-toplevel` →
`/fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone` (asserted before any run);
`rev-parse HEAD` → `1cfeb5d5089097fdffef761ad0e2b8dfa75a2793`, identical to the
lane HEAD. Battery and gate bytes identical between lane and clone
(`8198bd84…` / `7d79ac29…`, `cmp` identical, receipt `11-agree.txt`).

Raw output (receipt `06-clone-run.txt`):

```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
rc=0
```

Per run (parsed from `c1-gate-clone.json`, receipt `10-per-run.txt`):

| run | families_passed/families_total | verdict | failed_families | error_rows | REFUSAL-VERSIONS-9DIGIT-Z passed/failed | LEADING-ZERO-NORMALIZE passed/failed | cases |
|---|---|---|---|---|---|---|---|
| 0 | 105/105 | met | [] | 0 | 4/0 | 4/0 | 420 |
| 1 | 105/105 | met | [] | 0 | 4/0 | 4/0 | 420 |
| 2 | 105/105 | met | [] | 0 | 4/0 | 4/0 | 420 |

PASS: each run `105/105 met`, `failed_families []`, 0 error rows, `cases 420`.

Canonical/clone agreement: schema `tsukuroi-limine-pin-battery-r97-v1` in all
six runs; verdict `met` in all six; instruments byte-identical (`cmp` receipts
in `11-agree.txt`). The only JSON difference is the `gate` provenance path
(lane vs clone), which is expected: canonical
`gate=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py`,
clone `gate=/fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/clone/tools/check-limine-pins.py`.
Both agree on the frozen target reading.

## 4. Roster integrity

Commands: AST parse of `tools/limine-pin-battery-r98.py` + grep
(receipts `02-roster.txt`, `02-families-block.txt`).

Raw output:

```
FAMILY_ROSTER len = 105
CASES_PER_FAMILY = 4
Z present = True
LZ present = True
```

`FAMILIES` is a dict literal keyed by family name with function values, so a
plain `ast.literal_eval` cannot evaluate it (values are `Name`/`Lambda`
nodes); the literal-eval failure is on `FAMILIES` only (`malformed node …
Name(id='fam_positive')`), never on `FAMILY_ROSTER`. Confirmed statically:

- `FAMILY_ROSTER = (...)` at line 2024, `CASES_PER_FAMILY = 4` at line 2021,
  `FAMILIES = {…}` at line 1914 (receipts `02-roster.txt`,
  `02-families-block.txt`).
- `tuple(FAMILIES) != FAMILY_ROSTER` is a usage error in the battery
  (`main`: exit 2, "FAMILIES differs from FAMILY_ROSTER", line 2507), and
  the selftest's `roster-literal` leg asserts `tuple(FAMILIES) == FAMILY_ROSTER`
  — it reads PASS below, which is the runtime proof of equality.
- `check_echo`/`check_era` set on both r98 families: lines 1822-1823
  (`fam_refusal_versions_9digit_z`) and 1839-1840 (`fam_leading_zero_normalize`);
  the `meta_ok` assertions are at 2163-2165 (receipt `02-roster.txt`).
- LZ docstring corrected per R97-D3/A6: the discriminator is
  `12.000000009.000000005`, ordered era A by a text comparer and era B by
  `int()`; `000000012.9.4` does not discriminate (receipt `02-roster.txt`).

PASS: roster 105, `CASES_PER_FAMILY` 4, every run's `cases` = 420 = 105 × 4
(receipt `10-per-run.txt` asserts `len(case_log) == 420` per run).

## 5. --usage-check

Command:

```
python3 tools/limine-pin-battery-r98.py --usage-check --gate tools/check-limine-pins.py --work /fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns/usage --json <SeatDir>/c1-usage.json
```

Note (raw behaviour, not smoothed): `--usage-check` ignores `--json` and
prints its JSON object to stdout (`usage_check` prints; `main` returns
`usage_check(...)` directly, lines 2517-2521). The stdout bytes were saved to
`c1-usage.json` (receipts `07-usage.txt`, `07-usage-json2.txt`).

Raw JSON (trimmed):

```json
{
 "schema": "tsukuroi-limine-pins-usage-r97-v1",
 "gate": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py",
 "cases": [ …19 rows… ],
 "verdict": "met"
}
```

19/19 rows `ok: true`, verdict `met`, rc=0: `12.9`/`abc`/`12.9.6.1`/`""`/
5000-digit/`1234567890.0.0`/`0.1234567890.0`/`0000000001.0.0` refused rc 64;
`999999999.0.0`, `12.9.4`, `12.9.5`, `13.0.0`, `12.09.4`, `00.00.00`,
`12.9.999999999`, `0.9.999999999`, `000000012.9.4` answer rc 0;
`auto` and the omitted flag probe to `12.9.4` with source `probe`.

PASS: usage-check `met`, 19/19 ok.

## 6. --selftest

`--selftest --reference tools/check-limine-pins.py` runs 17 full batteries
(4 negative gates + reference + 12 lie wrappers, ~40 s each). It did not
complete inside the seat window under fleet load (two attempts stalled past
the 300 s tool deadline; the L1 stopped the reference leg and ordered no
third attempt). Recorded as `not completed — time-bounded` for the reference
leg. The reference leg did not complete inside the seat window under fleet
load; reference behaviour is carried by the landed-gate legs and the r97
analogue (18/18).

`--selftest` WITHOUT `--reference` was then run to completion
(receipt `08-selftest-noref.txt`):

```
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
rc=0
```

PASS (non-reference leg): `selftest PASS 5/5`. The `roster-literal` PASS is
the runtime proof that `tuple(FAMILIES) == FAMILY_ROSTER` (see §4).
`--selftest --reference …` is reported raw as `not completed — time-bounded`,
never smoothed into a pass.

## 7. count-runs parsing of every gate JSON

Command:

```
python3 .ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

Canonical (receipt `09-count-canonical.txt`, rc=0): 3 runs, each
`verdict met`, `families_passed 105`, `families_total 105`,
`failed_families []`, `cases 420`, `error_rows 0`,
`named: REFUSAL-VERSIONS-9DIGIT-Z [4,0], LEADING-ZERO-NORMALIZE [4,0]`.

Clone (receipt `09-count-clone.txt`, rc=0): identical 3-run summary
(each run `met`, 105/105, `[]`, 420, 0 error rows, Z `[4,0]`, LZ `[4,0]`).

PASS: count-runs agrees with the battery's own printed verdicts on both layouts.

## 8. Receipts

All under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-98/w1/ExecGateRuns/`:

- `01-sha256sum.txt` — manifest check, 27/27 OK rc=0
- `01-ls.txt`, `01-python.txt` — tool presence, Python 3.14.8
- `02-roster.txt`, `02-families-block.txt` — roster AST, check_echo/check_era, LZ docstring
- `03-canonical.txt` — canonical battery stdout + rc
- `c1-gate-canonical.json` — canonical 3-run battery JSON
- `05-clone.txt` — clone toplevel/HEAD asserts
- `06-clone-run.txt` — clone battery stdout + rc
- `c1-gate-clone.json` — clone 3-run battery JSON
- `07-usage.txt`, `c1-usage.json` — usage-check stdout JSON (19/19 ok, met)
- `08-selftest.txt`, `08-selftest-full.txt` (empty — first reference attempt,
  killed at 300 s), `08-selftest-rerun.txt`, `08-selftest-noref.txt` —
  selftest without reference, PASS 5/5 rc=0
- `09-count-canonical.txt`, `09-count-clone.txt` — count-runs summaries, rc=0 each
- `10-per-run.txt`, `10-devref.txt` — per-run parse (105/105 met, 420 cases, 0 errors)
- `11-agree.txt`, `11-sha-after.txt` — canonical/clone instrument cmp, manifest still 27/27

Scratch: `/fast/scratch/hyaku/tsukuroi-r98/ExecGateRuns` was deleted before
yield. No tool was installed or upgraded (no pacman; python3 preinstalled and
free). No file outside the seat dir and scratch was written; no instrument
byte was modified (manifest still 27/27 OK after the runs).

## 9. Expected lines — PASS/FAIL

- Manifest 27/27 OK: PASS
- Canonical 3× `105/105 met`, 0 error rows, `cases 420`: PASS
- Clone 3× `105/105 met`, 0 error rows, `cases 420`: PASS
- Canonical/clone agreement (instruments byte-identical, verdicts agree): PASS
- Roster 105, `CASES_PER_FAMILY` 4, Z/LZ `check_echo`+`check_era`, LZ docstring
  corrected: PASS
- Usage-check `met`, 19/19 ok: PASS
- `--selftest` without `--reference` PASS 5/5: PASS
- `--selftest --reference …`: not completed — time-bounded (see §6)

No deviation from the frozen C1 landed-gate target was observed; the only
smoothed-over item would have been the reference leg, which is reported raw.

{"seat":"ExecGateRuns","verdict":"met","notes":"manifest 27/27 OK; canonical 3x105/105 met 0 errors cases 420; clone 3x105/105 met 0 errors cases 420; roster 105 CASES_PER_FAMILY 4; Z/LZ check_echo+check_era on; usage-check met 19/19; --selftest PASS 5/5 without reference; --selftest --reference not completed (time-bounded under fleet load), reference behaviour carried by landed-gate legs and r97 analogue 18/18"}
