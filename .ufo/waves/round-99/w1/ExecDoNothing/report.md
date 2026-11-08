# ExecDoNothing — r99 w1 — C1 do-nothing control

Seat: `ExecDoNothing` (leaf executor, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Pre-round tip / git HEAD: `f107da3afe511f7db8cdc30235a992b774903158` (detached; no git/jj mutation run).
Scratch: `/fast/scratch/hyaku/tsukuroi-r99/ExecDoNothing` (created, used, deleted before yield).
Disk at start: `/fast/scratch/hyaku` 60% use, 328.0G free (`scripts/hyaku/disk-guard.sh status`).
No tool install/upgrade was needed or performed (python3 3.14.8, bubblewrap 0.13.1, git present).

**Task.** Prove the r98 battery is blind to the Y-cap era assertion and only partly sighted on the X one —
the C1 do-nothing control.

**Verdict: met.** All six legs (3 gates × 2 layouts, `--runs 3`) read exactly the frozen do-nothing readings;
0 error rows everywhere; the bend liveness probe confirms the blindness is real (the gate's `visibility_era`
does move under the bends, and only the r98 battery fails to look).

---

## 1. Control identity — PASS

Command (`sha256-control-identity.txt`):

```
sha256sum .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py tools/limine-pin-battery-r98.py
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  .ufo/waves/round-99/before/controls/do-nothing-battery-r98.py
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  tools/limine-pin-battery-r98.py
git show f107da3a...:tools/limine-pin-battery-r98.py | sha256sum
8198bd848effc4aa2b8f8d800f688ee131e2afe9b61bcac6c663ba71543f2a87  -
```

Manifest lines (`.ufo/waves/round-99/before/instruments.sha256`) name the same digest for both paths.
`sha256sum -c` the manifest: **16/16 OK, rc=0**, run before the measurement pass and re-run after it
(receipt `sha256-control-identity.txt`; second run tail OK).

| expected | reading | result |
|---|---|---|
| control digest == `tools/limine-pin-battery-r98.py` | both `8198bd84…` | PASS |
| control digest == manifest pin | `8198bd84…` in manifest | PASS |
| control digest == `f107da3a:tools/limine-pin-battery-r98.py` | `8198bd84…` | PASS |
| manifest `sha256sum -c` | 16 OK / 0 FAIL, rc 0 | PASS |

## 2. Static wiring — the r98 assertion gap, measured on the bytes

Receipt `static-assertion-wiring.txt` (`re.finditer` over the pinned bytes; owner = preceding `def fam_*`):

| battery | families asserting `check_echo` | families asserting `check_era` |
|---|---|---|
| `limine-pin-battery-r98.py` (115812 B) | explicit_version_echo (byte 78753), 9digit_z (81743), leading_zero_normalize (82960) | explicit_version_era (79274), 9digit_z (81767), leading_zero_normalize (82984) |
| `limine-pin-battery-r99.py` (117542 B) | the above **+ 9digit X (79011), 9digit_y (81662)** | the above **+ 9digit X (79035), 9digit_y (81686)** |

```
fam_refusal_versions_9digit      sets check_echo=False check_era=False   # r98
fam_refusal_versions_9digit_y    sets check_echo=False check_era=False   # r98
fam_refusal_versions_9digit      sets check_echo=True  check_era=True    # r99
fam_refusal_versions_9digit_y    sets check_echo=True  check_era=True    # r99
```

Roster unchanged: `FAMILY_ROSTER` len 105, `CASES_PER_FAMILY` 4 in both files. Lie kinds
(`lie-kinds.txt`): r98 `LIE_KINDS` n=12, no kind falsifying `limine_version` or `visibility_era`;
r99 n=14 with `limine-version` and `visibility-era`. These are the structural facts; the readings below
are the behavioural ones.

## 3. Canonical layout — 3 legs × `--runs 3`

Engine: `.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py` (byte-identical control, §1),
`--work <scratch>/work-<leg>` per leg, `TMPDIR=<scratch>/tmp`, `--json <receipt>`.
Driver preserved verbatim at `run-all.sh`; all six legs ran concurrently (single `wait`).

```
EXIT gate canonical 0
EXIT n09  canonical 0
EXIT n11  canonical 1        # 1 = unmet, the expected r98 reading
```
`dn-gate-canonical.stdout`:
```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
```
`dn-n09-canonical.stdout`:
```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
```
`dn-n11-canonical.stdout`:
```
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ERA
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ERA
families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ERA
```

All six `.stderr` files are 0 bytes.

## 4. Clone layout — `git clone --shared`, same 3 legs × `--runs 3`

```
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin <scratch>/clone/tsukuroi-shokunin
git -C <clone> rev-parse --show-toplevel → /fast/scratch/hyaku/tsukuroi-r99/ExecDoNothing/clone/tsukuroi-shokunin
git -C <clone> rev-parse HEAD → f107da3afe511f7db8cdc30235a992b774903158
```
Clone bytes: `tools/limine-pin-battery-r98.py` `8198bd84…`, `tools/check-limine-pins.py` `7d79ac29…`.
The clone is at the pre-round tip, so it does not carry the round's `before/controls/`; the two bend files
were copied from the lane's frozen bytes into the clone at the same relative path and re-hashed there:
`N09-y-era.py` `22c3449f…`, `N11-x-era.py` `28392f3b…` — both equal to the manifest pins. No commit was made
(the clone is only read from; `git rev-parse --show-toplevel` was asserted to be the scratch path first).

```
EXIT gate clone 0
EXIT n09  clone 0
EXIT n11  clone 1
```
`dn-gate-clone.stdout` / `dn-n09-clone.stdout`: three lines each `families_passed 105/105 verdict met failed -`.
`dn-n11-clone.stdout`: three lines each `families_passed 104/105 verdict unmet failed EXPLICIT-VERSION-ERA`.
All `.stderr` 0 bytes.

## 5. `count-runs.py` parse — per leg and layout

Command (per file; three cap families named as the claim's counting command does):
```
python3 .ufo/waves/round-95/before/controls/count-runs.py <receipt>.json \
  --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family REFUSAL-VERSIONS-9DIGIT-Z
```
`count-runs.py` exits 0 iff every run is `met` with 0 error rows, so gate/n09 print `COUNT_EXIT … 0`
and n11 prints `COUNT_EXIT … 1` — the documented unmet status, not a harness error.

| leg | layout | families_passed | verdict | failed_families | error_rows | named cap families (pass/fail per run) |
|---|---|---|---|---|---|---|
| gate | canonical | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 | X 4/0, Y 4/0, Z 4/0 |
| gate | clone | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 | X 4/0, Y 4/0, Z 4/0 |
| N09-y-era | canonical | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 | X 4/0, Y 4/0, Z 4/0 |
| N09-y-era | clone | 105/105 ×3 | met ×3 | `[]` ×3 | 0 ×3 | X 4/0, Y 4/0, Z 4/0 |
| N11-x-era | canonical | 104/105 ×3 | unmet ×3 | `["EXPLICIT-VERSION-ERA"]` ×3 | 0 ×3 | X 4/0, Y 4/0, Z 4/0 |
| N11-x-era | clone | 104/105 ×3 | unmet ×3 | `["EXPLICIT-VERSION-ERA"]` ×3 | 0 ×3 | X 4/0, Y 4/0, Z 4/0 |

The `named` block is the load-bearing one for "only partly sighted": on N11 the **X family passes all 4
cases** while `EXPLICIT-VERSION-ERA` fails exactly 1 of 4 (`leg-case-structure.txt`):

```
FAILED CASE family=EXPLICIT-VERSION-ERA
   want=[1, "DEGRADED", [[3,"LP-MISMATCH","panic"],[7,"OK","none"]], "menu"]
   got =[1, "DEGRADED", [[3,"LP-MISMATCH","panic"],[7,"OK","none"]], 1, "menu", "999999999.9.9", "flag"]
```
rc, verdict, pins, rc-field, on_panic, echo and source all match; the case's only divergence is the unlogged
`visibility_era` (the battery never records that field in `case_log` — the blindness, visible in the schema
of the log itself). The failing version is `999999999.9.9`, i.e. the X-cap member sent by the r96 EXPLICIT
families (`EXPLICIT_VERSION_META[3]`), exactly the A5 "rides on one EXPLICIT case" shape.

## 6. Liveness probe — the bends actually move the gate

`probe-era-live.json` (+ driver `probe-era.py`): the r98 battery's own fixture builder (imported read-only)
built one Y case (`12.999999999.4`) and one X case (`999999999.9.9`); each ran against the pristine gate and
both bends, outside the sandbox, same conf/esp.

| fixture | gate | rc | verdict | `visibility_era` | pins match expected | field differs from expected |
|---|---|---|---|---|---|---|
| Y `12.999999999.4` (expect `12.9.5+`) | pristine | 1 | DEGRADED | `12.9.5+` | yes | no |
| Y `12.999999999.4` | N09-y-era | 1 | DEGRADED | **`pre-12.9.5`** | yes | **yes** |
| Y `12.999999999.4` | N11-x-era | 1 | DEGRADED | `12.9.5+` | yes | no |
| X `999999999.9.9` (expect `12.9.5+`) | pristine | 1 | DEGRADED | `12.9.5+` | yes | no |
| X `999999999.9.9` | N09-y-era | 1 | DEGRADED | `12.9.5+` | yes | no |
| X `999999999.9.9` | N11-x-era | 1 | DEGRADED | **`pre-12.9.5`** | yes | **yes** |

So N09 is live (it corrupts the Y-cap label and nothing else) and the r98 battery still reads `met 105/105`
on it → the battery is blind, not the bend inert. Fixture paths recorded in that JSON are scratch paths
(deleted at yield); the JSON is the measurement, the paths are not citable.
Bend clause position, byte-level: `grep -abo 'N09 (era label lies'` → 17191 in `N09-y-era.py`; the same
offset 17191 in `N11-x-era.py`; each file differs from the pristine gate by exactly one changed line
(`diff -u | grep -c '^[-+][^-+]'` → 2). Gate `visibility_era` emission sites: bytes 11345, 17038, 19206.

## 7. PASS/FAIL against the assignment's expected lines

| expected (assignment) | reading | result |
|---|---|---|
| control digest = `tools/limine-pin-battery-r98.py` = manifest = `f107da3a` blob | `8198bd84…` all three | PASS |
| gate canonical `met 105/105` ×3 | yes, 0 error rows | PASS |
| gate clone `met 105/105` ×3 | yes, 0 error rows | PASS |
| N09 canonical `met 105/105` ×3 (blind) | yes, 0 error rows | PASS |
| N09 clone `met 105/105` ×3 (blind) | yes, 0 error rows | PASS |
| N11 canonical `unmet 104/105` ×3, failed exactly `["EXPLICIT-VERSION-ERA"]` | yes, 0 error rows | PASS |
| N11 clone `unmet 104/105` ×3, failed exactly `["EXPLICIT-VERSION-ERA"]` | yes, 0 error rows | PASS |
| 0 error rows everywhere | 0 in all 18 runs (6 legs × 3) | PASS |
| no leg differs from its frozen reading | none differed | PASS |

No leg differed, so nothing is reported raw-as-an-exception.

## 8. Receipts (all written by this seat, all under this seat dir)

- `sha256-control-identity.txt` — control/instrument/tip digests + `sha256sum -c` (16 OK).
- `static-assertion-wiring.txt` — per-family `check_echo`/`check_era` byte offsets, r98 vs r99.
- `lie-kinds.txt` — `LIE_KINDS` membership, r98 vs r99; roster/case counts.
- `run-all.sh` — the exact six-leg driver (per-leg `--work`, `TMPDIR`).
- `dn-{gate,n09,n11}-{canonical,clone}.json` — battery receipts (`--runs 3` → 3-run list).
- `dn-*.stdout`, `dn-*.stderr`, `dn-*.exit` — raw stdout/stderr/exit per leg.
- `count-{gate,n09,n11}-{canonical,clone}.json`, `count-*.err` — `count-runs.py` parse.
- `leg-case-structure.txt` — per-run case tallies and the one failing case's want/got.
- `probe-era.py`, `probe-era-live.json` — bend liveness on the same fixtures.

## 9. Limits and notes

- The r98 battery's `case_log` does not record `visibility_era` (`run_battery` logs
  `[rc, verdict, pins, rc-field, on_panic, limine_version, source]`), so the N09 blindness is provable
  behaviourally (leg reading) and by liveness probe, but not from the receipt log alone. Stated, not glossed.
- The probe in §6 runs the gates unsandboxed by design (it measures the field, not isolation); the battery
  legs run under the instrument's own bwrap launcher.
- The clone layout necessarily carries the round's bend bytes copied in from the lane's frozen files
  (the clone is at `f107da3a`); the copy is hash-verified against the manifest, so the leg measures the
  frozen bytes. The clone's `tools/` bytes are the tip's own.
- Scope: this seat measures the do-nothing control only. It makes no statement about the r99 battery's own
  readings, the C2 checker, the coverage gate, or any axis score.

{"seat":"ExecDoNothing","verdict":"met","notes":"r98 control 8198bd84… (== tools/limine-pin-battery-r98.py == manifest == f107da3a blob); gate met 105/105 x3 and N09 met 105/105 x3 (blind to the Y era assertion) and N11 unmet 104/105 x3 with failed_families [EXPLICIT-VERSION-ERA] only, in both canonical and clone layouts, 0 error rows in all 18 runs; liveness probe shows N09/N11 do move the gate's visibility_era on the Y/X cap cases, so the blindness is the battery's assertion gap (r98 sets check_echo/check_era on Z/LZ/EXPLICIT only, r99 adds X and Y)."}
