# ExecBattery — C1 landed-gate leg (canonical vs clone)

## Axes
- depth: C1 landed gate reads 105/105 in both layouts (two new families pass).
- agreement: canonical and clone readings identical.
- usage: new rows read rc 0 / rc 64 as frozen.

## Commands and raw output (trimmed)

### 1. sha256sum -c instruments
```
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
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
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: OK
.ufo/waves/round-97/before/dev/run-dev.sh: OK
rc=0
```
PASS (20/20 OK).

### 2. Canonical battery
```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBattery --json <SeatDir>/c1-gate-canonical.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
rc=0
```
PASS.

### 3. Clone battery
```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone
Cloning into '/fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone'... done. (32223 files)
$ git -C /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone rev-parse master
a57e88cd57f30bae206d908b534508d9463bf734
$ git -C /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone
$ cd /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone && python3 tools/limine-pin-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/clone-work --json <SeatDir>/c1-gate-clone.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
clone_rc=0
```
PASS.

### 4. Usage check
```
$ python3 tools/limine-pin-battery-r97.py --usage-check --gate tools/check-limine-pins.py --work /fast/scratch/hyaku/tsukuroi-r97/ExecBattery/usage
{"schema": "tsukuroi-limine-pins-usage-r97-v1", "verdict": "met", ...}
  "12.9.999999999"  want_rc 0  rc 0  ok true
  "0.9.999999999"   want_rc 0  rc 0  ok true
  "000000012.9.4"   want_rc 0  rc 0  ok true
  "0000000001.0.0"  want_rc 64 rc 64 ok true
rc=0
```
PASS (all 19 cases ok; the four named rows read as frozen).

### 5. count-runs parsing
Canonical and clone both:
```
{"runs": [{"verdict":"met","families_passed":105,"families_total":105,"failed_families":[],"cases":420,"error_rows":0,"named":{"LEADING-ZERO-NORMALIZE":[4,0],"REFUSAL-VERSIONS-9DIGIT-Z":[4,0]}} x3], "families": ["REFUSAL-VERSIONS-9DIGIT-Z","LEADING-ZERO-NORMALIZE"]}
```
rc=0 both. PASS.

## Per-layout per-run table (from count-runs output)

| layout | run | families_passed/families_total | verdict | failed_families | error_rows | REFUSAL-VERSIONS-9DIGIT-Z passed/failed | LEADING-ZERO-NORMALIZE passed/failed |
|---|---|---|---|---|---|---|---|
| canonical | 1 | 105/105 | met | [] | 0 | 4/0 | 4/0 |
| canonical | 2 | 105/105 | met | [] | 0 | 4/0 | 4/0 |
| canonical | 3 | 105/105 | met | [] | 0 | 4/0 | 4/0 |
| clone | 1 | 105/105 | met | [] | 0 | 4/0 | 4/0 |
| clone | 2 | 105/105 | met | [] | 0 | 4/0 | 4/0 |
| clone | 3 | 105/105 | met | [] | 0 | 4/0 | 4/0 |

Canonical and clone readings agree exactly.

## Receipts (all under .ufo/waves/round-97/w1/ExecBattery/)
- sha256sum.txt
- c1-gate-canonical.json, c1-gate-canonical.txt
- c1-gate-clone.json
- count-canonical.txt, count-clone.txt
- usage-check.txt
- report.md (this file)

## Tooling
No installs. python3 + git already present; pacman untouched (paused host-wide, none attempted).

## Scratch
/fast/scratch/hyaku/tsukuroi-r97/ExecBattery (clone + work dirs) removed after receipts written.

{"seat":"ExecBattery","verdict":"met","notes":"C1 landed gate 105/105 met in all 3 runs in both canonical and git clone --shared layouts; 0 error rows; REFUSAL-VERSIONS-9DIGIT-Z 4/0 and LEADING-ZERO-NORMALIZE 4/0 per run; usage rows 12.9.999999999/0.9.999999999/000000012.9.4 rc 0, 0000000001.0.0 rc 64; instruments sha256 20/20 OK; canonical==clone."}
