# ExecGateRuns — round 99 w1 — C1 landed-gate + lie-kind legs, canonical and clone

Seat: `ExecGateRuns` (leaf executor, no dispatch). Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns` (deleted after the receipts were copied here).
Seat receipt dir: `.ufo/waves/round-99/w1/ExecGateRuns/` (all files cited below live there; all written by this seat).

Inputs read before measuring: `.ufo/waves/round-99/claims.json`, `.ufo/plans/round-99.md`,
`.ufo/waves/round-99/before/instruments.sha256`, `corpus/lessons/round-98-verifier-spotcheck.md`,
`corpus/lessons/round-98.md` (mistakes + scoreboard), `corpus/QUALITY.md` 136-141.

## 1. Instrument integrity (both layouts)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-99/before/instruments.sha256 ; echo RC=$?
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
RC=0
```
16/16 OK, 0 non-OK, at the start and again after every run (`NONOK=0`).
Receipts: `instruments-sha256-canonical.txt`. Gate bytes measured 30286, sha256
`7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` (`lie-wrapper-roundtrip.txt`).

## 2. Clone layout (deviation reported raw)

```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns/clone
$ cd clone && git rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns/clone
$ git rev-parse HEAD
f107da3afe511f7db8cdc30235a992b774903158
```

**Deviation (raw).** The clone is a clone of the *committed* tip `f107da3a`; the r99 instruments and the whole
`round-99` wave dir are uncommitted in the lane (`git status`: `?? tools/limine-pin-battery-r99.py`, …), so the clone
does not carry them and the first `sha256sum -c` there read 9 `FAILED open or read` lines. The pinned paths were
therefore copied byte-for-byte from the lane into the clone (instrument, gate, `make-r99-bends.py`,
`check-registry-content-r99.py`, `before/`, `plans/round-99.md`), and the clone re-verified:

```
$ cd <clone> && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
<16 lines, all OK; NONOK=0>
```
Receipts: `clone-pins.txt`. The executed bytes in the clone leg are the clone's own copies of those pinned bytes
(not the lane's files), and the clone working tree was otherwise clean.

## 3. Landed gate, canonical — `--runs 3`

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 \
    --work /fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns/canon \
    --json .ufo/waves/round-99/w1/ExecGateRuns/c1-gate-canonical.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
RC=0
```
Receipts: `c1-gate-canonical.json`, `c1-gate-canonical.stdout`.

## 4. Landed gate, clone — `--runs 3`

```
$ cd /fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns/clone
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 \
    --work /fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns/clone-work \
    --json .../w1/ExecGateRuns/c1-gate-clone.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
RC=0
```
The `gate` field of every clone run reads the clone path
`/fast/scratch/hyaku/tsukuroi-r99/ExecGateRuns/clone/tools/check-limine-pins.py`.
Receipts: `c1-gate-clone.json`, `c1-gate-clone.stdout`.

## 5. Per layout, per run (count-runs receipts)

`python3 .ufo/waves/round-95/before/controls/count-runs.py <json> --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family REFUSAL-VERSIONS-9DIGIT-Z`
(exit 1 on an unmet run; the three landed runs exit 0).
Receipts: `count-runs-canonical.txt`, `count-runs-clone.txt`.

| layout | run | families_passed/total | verdict | failed_families | cases | error_rows | X / Y / Z (passed,failed) |
|---|---|---|---|---|---|---|---|
| canonical | 0 | 105/105 | met | [] | 420 | 0 | 4,0 / 4,0 / 4,0 |
| canonical | 1 | 105/105 | met | [] | 420 | 0 | 4,0 / 4,0 / 4,0 |
| canonical | 2 | 105/105 | met | [] | 420 | 0 | 4,0 / 4,0 / 4,0 |
| clone | 0 | 105/105 | met | [] | 420 | 0 | 4,0 / 4,0 / 4,0 |
| clone | 1 | 105/105 | met | [] | 420 | 0 | 4,0 / 4,0 / 4,0 |
| clone | 2 | 105/105 | met | [] | 420 | 0 | 4,0 / 4,0 / 4,0 |

Agreement (verdict, families_passed, total, failed set, cases, schema, error rows, all six runs):
`canonical == clone` → **True**. Receipt: `agreement.txt`.

## 6. Roster / cases / schema

```
$ python3 -c '<import module; print constants>'      # receipt: roster-integrity.txt
len(FAMILY_ROSTER) = 105
tuple(FAMILIES) == FAMILY_ROSTER = True
CASES_PER_FAMILY = 4
len(FAMILIES) = 105
X in roster = True   Y in roster = True   Z in roster = True
LIE_KINDS = ('exit-code','rc-field','line','consequence','status','verdict','entry','panic-line',
             'panic-value','on-panic','bad-resource','missing-panic','limine-version','visibility-era')
new lie kinds present = (True, True)
```
Every run of all six gate runs carries `"schema": "tsukuroi-limine-pin-battery-r99-v1"` and `cases = 420`
(= 105 × 4). Assertion substance (fresh build per family, 4 cases each; `field-assert-probe.txt`):

```
REFUSAL-VERSIONS-9DIGIT    [(0,'999999999.9.9',echo=True,era=True,era_b=True) ×4]
REFUSAL-VERSIONS-9DIGIT-Y  [(0,'12.999999999.4',True,True,True), (1,'0.999999999.0',True,True,False), …]
REFUSAL-VERSIONS-9DIGIT-Z  [(0,'12.9.999999999',True,True,True), (1,'0.9.999999999',True,True,False), …]
```

## 7. `--usage-check`

```
$ python3 tools/limine-pin-battery-r99.py --usage-check --gate tools/check-limine-pins.py \
    --work .../usage > .ufo/waves/round-99/w1/ExecGateRuns/c1-usage.json
RC=0
{"schema": "tsukuroi-limine-pins-usage-r97-v1", ..., "verdict": "met"}   # 19 cases, all "ok": true
```
Raw deviation: `--json` does not apply to `--usage-check` (the tool prints to stdout and ignores `--json`), so the
JSON was captured from stdout into `c1-usage.json`. Receipt: `c1-usage.json`.

## 8. `--selftest` (no `--reference`)

```
$ python3 tools/limine-pin-battery-r99.py --selftest
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
RC=0
```
Receipt: `c1-selftest.txt`.

## 9. Lie kinds (built exactly as the instrument's own selftest does)

```
import importlib.util
m = load('tools/limine-pin-battery-r99.py')
gate = open('tools/check-limine-pins.py').read()
for kind in ('limine-version','visibility-era'):
    open('gate-%s.py' % kind,'w').write(m.LIE_WRAPPER % (gate, kind))
```
Round-trip check (`lie-wrapper-roundtrip.txt`): each wrapper's `GATE_SRC` literal equals the 30286 gate bytes
(`embedded == gate bytes: True` for both). Wrapper sha256: `4fa10dbe…` (limine-version), `ff420ace…`
(visibility-era) — `lie-wrapper-sha256.txt`.

```
$ python3 tools/limine-pin-battery-r99.py --gate <wrapper> --runs 1 --work ... --json .../c1-lie-<kind>.json
limine-version   RC=1  families_passed 93/105 verdict unmet failed AUTO-ERA-A,AUTO-ERA-B,AUTO-PROBE-FAIL,
                 AUTO-PROBE-SHAPES,EXPLICIT-VERSION-ECHO,EXTRA-COMPONENT,LEADING-ZERO-NORMALIZE,
                 REFUSAL-VERSIONS,REFUSAL-VERSIONS-10DIGIT,REFUSAL-VERSIONS-9DIGIT,
                 REFUSAL-VERSIONS-9DIGIT-Y,REFUSAL-VERSIONS-9DIGIT-Z
visibility-era   RC=1  families_passed 95/105 verdict unmet failed AUTO-PROBE-FAIL,AUTO-PROBE-SHAPES,
                 EXPLICIT-VERSION-ERA,EXTRA-COMPONENT,LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS,
                 REFUSAL-VERSIONS-10DIGIT,REFUSAL-VERSIONS-9DIGIT,REFUSAL-VERSIONS-9DIGIT-Y,
                 REFUSAL-VERSIONS-9DIGIT-Z
```

| kind | families_passed/105 | verdict | error_rows | X (`REFUSAL-VERSIONS-9DIGIT`) in failed | Y (`REFUSAL-VERSIONS-9DIGIT-Y`) in failed |
|---|---|---|---|---|---|
| limine-version | 93 | unmet | 0 | YES | YES |
| visibility-era | 95 | unmet | 0 | YES | YES |

Failed-case detail, raw, from a `REFUSAL-VERSIONS-9DIGIT-Y` case:

```
limine-version   want=[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],"menu"]
                 got =[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","0.0.0","flag"]
visibility-era   want=[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],"menu"]
                 got =[1,"DEGRADED",[[3,"LP-MISMATCH","panic"],[7,"OK","none"]],1,"menu","12.999999999.4","flag"]
```

Direct field observation (a fresh X case and a fresh Y case, `era-echo-direct.txt`):

```
# REFUSAL-VERSIONS-9DIGIT version= 999999999.9.9 check_echo=True check_era=True era_b=True
  pristine           rc=1 limine_version='999999999.9.9'  source='flag' visibility_era='12.9.5+'
  lie-limine-version rc=1 limine_version='0.0.0'          source='flag' visibility_era='12.9.5+'
  lie-visibility-era rc=1 limine_version='999999999.9.9'  source='flag' visibility_era='pre-12.9.5'
# REFUSAL-VERSIONS-9DIGIT-Y version= 12.999999999.4 ...
  pristine           rc=1 limine_version='12.999999999.4' source='flag' visibility_era='12.9.5+'
  lie-limine-version rc=1 limine_version='0.0.0'          source='flag' visibility_era='12.9.5+'
  lie-visibility-era rc=1 limine_version='12.999999999.4' source='flag' visibility_era='pre-12.9.5'
```
Each wrapper flips exactly one field and the pristine gate passes both families; X and Y each read 0/4 passed under
both kinds (`count-runs-lie-*.txt`).

**Observation (advisory, not a defect claim).** The case log's `got` is a 7-field projection
`[got[0],got[1],pins,got[3],got[6],got[8],got[9]]` (instrument line 2296) — it carries `limine_version` and
`limine_version_source` but not `visibility_era` (`got[10]`), which `meta_ok` asserts. So for a `visibility-era`
lie the logged `got` is field-identical to a passing case's and only `passed:false` carries the kill; the era value
itself is not in the receipt (it is shown here only by the direct observation above).
Receipts: `c1-lie-limine-version.json`, `c1-lie-limine-version.stdout`, `count-runs-lie-limine-version.txt`;
`c1-lie-visibility-era.json`, `c1-lie-visibility-era.stdout`, `count-runs-lie-visibility-era.txt`.

## 10. PASS/FAIL per expected line

| # | Expected (seat item) | Observed | Verdict |
|---|---|---|---|
| 1 | every `instruments.sha256` line OK | 16/16 OK, rc 0, twice | PASS |
| 2 | canonical landed gate `105/105 met`, `failed_families []`, 0 error rows, ×3 | 3/3 exactly that | PASS |
| 3 | clone landed gate same | 3/3 exactly that | PASS |
| 4 | roster 105, `tuple(FAMILIES)==FAMILY_ROSTER` True, `CASES_PER_FAMILY` 4 | 105 / True / 4 | PASS |
| 5 | every run `cases` = 105×4 | 420 in all six runs | PASS |
| 6 | schema token `tsukuroi-limine-pin-battery-r99-v1` | present in all six runs | PASS |
| 7 | `--usage-check` JSON | `met`, 19/19 ok | PASS |
| 8 | `--selftest` without `--reference` | `PASS 5/5` | PASS |
| 9 | both lie kinds `unmet` with X and Y in `failed_families` | 93/105 and 95/105, X+Y both failed, 0 error rows | PASS |
| 10 | canonical and clone agree | `AGREE: True` over all six runs | PASS |

Deviations reported, not smoothed: (a) the clone had no r99 bytes — pinned files were copied in and re-verified
(§2); (b) `--usage-check` ignores `--json`, stdout captured instead (§7). Neither changes a measured number.

Lane hygiene: no tracked lane file was written by this seat (`git diff --stat` shows only the five files other
actors already had modified: `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md` — these
changed during this session by other seats, not by this one). Nothing under `tools/`, `corpus/`, `SKILL.md`,
`SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-99/before/` or `claims.json` was modified; no git/jj
mutation was run. Tooling: none installed (no pacman, no uv/npx); scratch deleted after the receipts were copied.

{"seat":"ExecGateRuns","verdict":"met","notes":"C1 landed gate 105/105 met x3 canonical and x3 clone (cases 420, schema tsukuroi-limine-pin-battery-r99-v1, 0 error rows, X/Y/Z 4-0 each); 16/16 instrument pins OK in both layouts; roster 105, tuple(FAMILIES)==FAMILY_ROSTER True, CASES_PER_FAMILY 4; usage-check met 19/19; selftest PASS 5/5 without reference; lie limine-version unmet 93/105 and visibility-era unmet 95/105, both with REFUSAL-VERSIONS-9DIGIT and REFUSAL-VERSIONS-9DIGIT-Y in failed_families, 0 error rows. Deviations: r99 instruments are uncommitted at f107da3a so the clone's pinned files were copied in and sha256-verified; --usage-check ignores --json so stdout was captured."}
