# ExecDoNothing report — r97 do-nothing battery (C1 blindness control)

## Axes
Blindness (r97 battery vs field-lie bends) · byte-identity (control = r97 landed) · reverse-blindness (lie is real, gate is right) · usage-check.

## Commands & raw output

### 0. Instruments manifest
```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-98/before/instruments.sha256
```
→ 27 files all `OK` (gate `7d79ac29…`, battery-r98 `8198bd84…`, do-nothing-battery-r97 `e678c34f…`, benders N07 `2d8f4f6e…`, N08 `45d8d00d…`). Receipt: `sha256-instruments.txt`. **PASS**

### 1. Control byte-identity
```
git show b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a:tools/limine-pin-battery-r97.py > $SCRATCH/r97-landed.py
cmp .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py $SCRATCH/r97-landed.py   # rc 0
sha256sum .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py $SCRATCH/r97-landed.py
```
Raw:
```
battery+landed:
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  .../controls/do-nothing-battery-r97.py
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  $SCRATCH/r97-landed.py
---
gate (do-nothing copy):
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  .../controls/do-nothing-gate.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
---
cmp: identical, rc=0
```
Receipt: `sha256-battery-identity.txt`. (L1 correction honored: the battery's identity is `e678c34f…` ≠ gate hash `7d79ac29…`; gate and its do-nothing copy share `7d79ac29…`.) Expected `e678c34f…` both and `cmp` rc 0 → **PASS**

### 2. Control on landed gate (×3)
```
python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate tools/check-limine-pins.py --runs 3 --work /fast/scratch/hyaku/tsukuroi-r98/ExecDoNothing --json <SeatDir>/dn-gate.json
```
Raw:
```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
```
JSON check: 3 runs `families_passed 105`, `verdict met`, `failed_families []`, `cases 420`, `error_rows 0`. Expected `met 105/105` ×3, 0 error rows → **PASS**. Receipts: `dn-gate.json`, `dn-gate.out.txt`

### 3. Control on N07 era-field-lie bend (×3)
```
python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate .ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py --runs 3 --work .../w-n07 --json <SeatDir>/dn-N07-era-field-lie.json
```
Raw: `families_passed 105/105 verdict met failed -` ×3. Error rows 0/run. Expected `met 105/105` ×3, 0 errors (blind to era lie) → **PASS**. Receipts: `dn-N07-era-field-lie.json`, `dn-N07.out.txt`

### 4. Control on N08 echo-norm bend (×3)
```
python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --gate .ufo/waves/round-98/before/controls/bends/N08-echo-norm.py --runs 3 --work .../w-n08 --json <SeatDir>/dn-N08-echo-norm.json
```
Raw: `families_passed 105/105 verdict met failed -` ×3. Error rows 0/run. Expected `met 105/105` ×3, 0 errors (blind to echo normalization) → **PASS**. Receipts: `dn-N08-echo-norm.json`, `dn-N08.out.txt`

### 5. Reverse blindness (lie is real, gate is right)
(a) Source diff (from `diff -u`): N07 changes ONE line — the main-return `visibility_era` expression swaps the era label exactly when the spelling has a 9-digit third component or a leading-zero component; N08 inserts ONE line `limine_version = ".".join(str(x) for x in version)` normalizing the echo. Receipt: `direct-Z.txt` header.
(b) Direct `check()` concatenation (landed gate vs bends, same minimal conf):
```
landed-gate  v=12.9.999999999          visibility_era='12.9.5+'  limine_version='12.9.999999999'
landed-gate  v=000000012.9.4           visibility_era='pre-12.9.5'  limine_version='000000012.9.4'
landed-gate  v=12.000000009.000000005  visibility_era='12.9.5+'  limine_version='12.000000009.000000005'
landed-gate  v=12.9.4                  visibility_era='pre-12.9.5'  limine_version='12.9.4'
N07          v=12.9.999999999          visibility_era='pre-12.9.5'  limine_version='12.9.999999999'   <- era inverted
N07          v=000000012.9.4           visibility_era='12.9.5+'  limine_version='000000012.9.4'        <- era inverted
N07          v=12.000000009.000000005  visibility_era='pre-12.9.5'  limine_version='12.000000009.000000005' <- era inverted
N07          v=12.9.4                  visibility_era='pre-12.9.5'  limine_version='12.9.4'            <- untouched (non-Z/LZ)
N08          v=12.9.999999999          visibility_era='12.9.5+'  limine_version='12.9.999999999'
N08          v=000000012.9.4           visibility_era='pre-12.9.5'  limine_version='12.9.4'           <- echo normalized
N08          v=12.000000009.000000005  visibility_era='12.9.5+'  limine_version='12.9.5'              <- echo normalized
N08          v=12.9.4                  visibility_era='pre-12.9.5'  limine_version='12.9.4'
```
Expected: gate's era right on landed gate, wrong on N07; N08's echo normalized on Z/LZ spellings. Gate right on all four (era by numeric tuple; echo verbatim = flag spelling). N07 inverts era on Z/LZ only, leaves `12.9.4` untouched. N08 normalizes `limine_version` echo (`000000012.9.4`→`12.9.4`, `12.000000009.000000005`→`12.9.5`), era unchanged. Lie is real, not a no-op → **PASS**. Receipt: `direct-Z.txt`

### 6. `--usage-check`
```
python3 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py --usage-check
```
Raw:
```
usage: do-nothing-battery-r97.py [-h] [--gate GATE] [--runs RUNS]
                                 [--work WORK] [--json JSON] [--selftest]
                                 [--reference REFERENCE] [--isolation-check]
                                 [--usage-check]
```
Receipt: `usage-check.txt`. (The r97 battery's `--usage-check` prints this usage line; no separate machine summary is emitted.)

### Cross-check (context only, not the frozen instrument)
`diff <(git show b3be3f90:...r97.py) tools/limine-pin-battery-r98.py` confirms the r98 battery is exactly r97 + `check_echo`/`check_era` on the two families + corrected LZ docstring (A6/R97-D3) — the only delta this control is blind to.

## Verdict
Blindness leg **HOLDS**: the r97 do-nothing battery reads `met 105/105` ×3 with 0 error rows on the landed gate and on both bends (N07 era-field lie and N08 echo normalization), i.e. it is blind to both new metadata assertions, exactly as the r97 A7 limit predicts. The bends are not no-ops (N07 inverts `visibility_era` on Z/LZ spellings, N08 normalizes the echoed version), and the landed gate's era/echo are right on all four probed spellings. No control leg deviates from its frozen reading → no finding against C1's do-nothing clause.

## Receipts
- `sha256-instruments.txt`, `sha256-battery-identity.txt`, `usage-check.txt`, `direct-Z.txt`
- `dn-gate.json` / `dn-gate.out.txt`, `dn-N07-era-field-lie.json` / `dn-N07.out.txt`, `dn-N08-echo-norm.json` / `dn-N08.out.txt`
(all under `.ufo/waves/round-98/w1/ExecDoNothing/`; scratch clone dir deleted before yield.)

## Tooling
No installs/upgrades needed. No pacman (paused). No sudo. Lessons consulted: r97 spotcheck R97-D3/A6 lineage, A7 field/echo limit; QUALITY.md 139‑141 (byte-level offsets — none recorded here beyond hashes; consumed as orientation).

{"seat":"ExecDoNothing","verdict":"met","notes":"r97 battery blind on landed gate and both bends (105/105 x3, 0 error rows each); byte-identity e678c34f cmp rc0; reverse-blindness shown (N07 era inverted on Z/LZ, N08 echo normalized); usage-check recorded"}
