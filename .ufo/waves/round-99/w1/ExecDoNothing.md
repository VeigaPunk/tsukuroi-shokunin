# ExecDoNothing — r99 w1 — C1 do-nothing control (scoped findings)

Lane `tsukuroi-shokunin`, pre-round tip `f107da3a` (detached HEAD; no mutation run). Full commands, raw
output and receipt inventory: `.ufo/waves/round-99/w1/ExecDoNothing/report.md`.

Instrument integrity: `sha256sum -c .ufo/waves/round-99/before/instruments.sha256` → 16/16 OK, re-run
after the measurement pass (same result). Control identity `8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87`
for `.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py`, `tools/limine-pin-battery-r98.py` and
`git show f107da3a:tools/limine-pin-battery-r98.py` (three-way equal, = manifest pin).

## Readings (engine: the frozen r98 control, `--runs 3`, own `--work` per leg)

| leg | layout | families_passed | verdict | failed_families | error_rows |
|---|---|---|---|---|---|
| landed gate | canonical | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 |
| landed gate | clone | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 |
| N09-y-era | canonical | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 |
| N09-y-era | clone | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 |
| N11-x-era | canonical | 104/105 ×3 | unmet ×3 | `["EXPLICIT-VERSION-ERA"]` ×3 | 0 ×3 |
| N11-x-era | clone | 104/105 ×3 | unmet ×3 | `["EXPLICIT-VERSION-ERA"]` ×3 | 0 ×3 |

`count-runs.py` with the three cap families named reads X 4/0, Y 4/0, Z 4/0 on **every** run of **every**
leg — including N11, where the X family's own cases all pass. The single failing N11 case is
`EXPLICIT-VERSION-ERA` with `limine_version` `999999999.9.9` (`leg-case-structure.txt`): the battery sees
the X lie only through the r96 EXPLICIT family (A5), never through `REFUSAL-VERSIONS-9DIGIT`.

## Why the blindness is real, not an inert bend

`probe-era-live.json` drives the r98 battery's own fixture builder on one Y case (`12.999999999.4`) and one
X case (`999999999.9.9`) against pristine / N09 / N11:

- Y case: pristine `visibility_era=12.9.5+`; N09 → `pre-12.9.5` (pins, rc, verdict, echo unchanged); N11 unchanged.
- X case: pristine `12.9.5+`; N11 → `pre-12.9.5`; N09 unchanged.

So both bends are live one-field lies and the r98 battery still reads `met 105/105` on N09 → blind to the
Y-cap assertion. Structural counterpart (`static-assertion-wiring.txt`): r98 sets `check_echo`/`check_era`
only on `fam_explicit_version_echo/_era`, `fam_refusal_versions_9digit_z`, `fam_leading_zero_normalize`;
`fam_refusal_versions_9digit` (X) and `fam_refusal_versions_9digit_y` (Y) set neither (bytes 79011/79035
and 81662/81686 are the r99 additions). `LIE_KINDS` r98 n=12 with no `limine-version`/`visibility-era`.

## PASS/FAIL

| expected | result |
|---|---|
| control = r98 instrument = manifest = tip blob | PASS |
| gate `met 105/105` ×3 both layouts | PASS |
| N09 `met 105/105` ×3 both layouts (blind) | PASS |
| N11 `unmet 104/105` ×3 both layouts, failed exactly `["EXPLICIT-VERSION-ERA"]` | PASS |
| 0 error rows everywhere (18 runs) | PASS |
| no leg differs from its frozen reading | PASS (nothing to report raw) |

## Receipts (all under `.ufo/waves/round-99/w1/ExecDoNothing/`)

`sha256-control-identity.txt`, `static-assertion-wiring.txt`, `lie-kinds.txt`, `run-all.sh`,
`dn-{gate,n09,n11}-{canonical,clone}.{json,stdout,stderr,exit}`,
`count-{gate,n09,n11}-{canonical,clone}.{json,err}`, `leg-case-structure.txt`,
`probe-era.py`, `probe-era-live.json`, `report.md`.

## Limits

- `case_log` carries no `visibility_era`, so the N09 blindness rests on the leg reading plus the liveness
  probe, not on the log alone.
- The clone layout copies the round's bend bytes into the clone (clone is at `f107da3a`); the copies are
  hash-verified against the manifest, so the legs measure the frozen bytes.
- This seat measures the do-nothing control only; it says nothing about the r99 battery, the C2 checker or
  any axis score.

{"seat":"ExecDoNothing","verdict":"met","notes":"r98 control 8198bd84… three-way identical (control file, tools/limine-pin-battery-r98.py, f107da3a blob) and manifest-pinned; gate met 105/105 x3, N09 met 105/105 x3 (blind to the Y-cap era assertion), N11 unmet 104/105 x3 with failed_families exactly [EXPLICIT-VERSION-ERA]; both canonical and git-clone layouts, 0 error rows in all 18 runs; N09/N11 provably move the gate's visibility_era (one-field lie) while the r98 battery never reads that field for the X/Y families."}
