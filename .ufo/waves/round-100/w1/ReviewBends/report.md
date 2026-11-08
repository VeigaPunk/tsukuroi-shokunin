# Seat report — ReviewBends (round 100, w1)

Scope: attack C1's **stated wording** (not only its numbers). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; HEAD `69474c55` (detached; no mutating git/jj was run).
No instrument, frozen file, plan or corpus file was edited. Scratch:
`/fast/scratch/hyaku/tsukuroi-r100/ReviewBends` (removed before yield; disk-guard read `status` before the
heavy pass, no ENOSPC).

## 1. Pinned bytes (before any measurement)

Command (lane):

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-100/before/instruments.sha256
```

Raw (trimmed to the first/last lines; full output in `receipts/clone-identity.txt`):

```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK
…
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK
.ufo/plans/round-100.md: OK
```

PASS: 16/16 manifest entries OK (`rc=0`).

## 2. Bends re-derived without running the generator

`tools/make-r100-bends.py` was NOT run (it writes the frozen wave dir). Its `VARIANTS` dict was extracted
with `ast.literal_eval` and applied to the pinned gate in scratch; bytes compared.

Command:

```
python3 /fast/scratch/hyaku/tsukuroi-r100/ReviewBends/rederive.py
```

Raw:

```
N12-x-echo matches=1 rederived=eb247e1646d1b421cf047f2b2edeb34423227b5ca056edcaf0712924b3f0331a committed=eb247e1646d1b421cf047f2b2edeb34423227b5ca056edcaf0712924b3f0331a IDENTICAL
N13-y-echo matches=1 rederived=e1e5916fad0ee545a0571c852ebf658269322a138e802bcff5e875ab868bebee committed=e1e5916fad0ee545a0571c852ebf658269322a138e802bcff5e875ab868bebee IDENTICAL
```

`diff -u tools/check-limine-pins.py <bend>` shows exactly one `-`/`+` pair for each bend; the changed
entry is at BYTE 16931 (the final verdict return). The early `conf unreadable` emission at BYTE 11230 is
untouched. Full diffs: `receipts/bend-diffs.txt`.

PASS: two one-clause bends, one changed line each, byte-identical to the committed files.

## 3. Clone layout

```
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  /fast/scratch/hyaku/tsukuroi-r100/ReviewBends/clone
git -C <clone> rev-parse --show-toplevel HEAD
cd <clone> && sha256sum -c .ufo/waves/round-100/before/instruments.sha256
```

Raw (`receipts/clone-identity.txt`):

```
toplevel=/fast/scratch/hyaku/tsukuroi-r100/ReviewBends/clone
clone_HEAD=69474c55eb38632f3e740923b58029dc43e01300
lane_HEAD=69474c55eb38632f3e740923b58029dc43e01300
… 16/16 OK …
rc=0
```

PASS: clone identity asserted; every pinned byte identical inside the clone.

## 4. Battery legs (the four frozen legs, ×3, both layouts)

Per-leg command (the exact form in `run_leg.sh`; `--work` unique per leg):

```
python3 <battery> --gate <gate-or-bend> --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r100/ReviewBends/work/<tag> \
  --json .ufo/waves/round-100/w1/ReviewBends/receipts/<tag>.json
```

`<battery>` = `tools/limine-pin-battery-r99.py` (or the clone's copy) for the gate/N12/N13; the r98 control
is `tools/limine-pin-battery-r98.py` (or the clone's copy). The 15 legs were run with
`cat jobs.txt | xargs -P 6 -L 1 run_leg.sh`; each `.log` carries the same summary line three times (one per
run) plus `rc=`; one line per leg is shown here:

```
canon-gate      families_passed 105/105 verdict met    failed -
canon-N13       families_passed 104/105 verdict unmet  failed REFUSAL-VERSIONS-9DIGIT-Y
canon-N12       families_passed 103/105 verdict unmet  failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
canon-r98-N13   families_passed 105/105 verdict met    failed -
canon-r98-N12   families_passed 104/105 verdict unmet  failed EXPLICIT-VERSION-ECHO
clone-gate      families_passed 105/105 verdict met    failed -
clone-N13       families_passed 104/105 verdict unmet  failed REFUSAL-VERSIONS-9DIGIT-Y
clone-N12       families_passed 103/105 verdict unmet  failed EXPLICIT-VERSION-ECHO,REFUSAL-VERSIONS-9DIGIT
clone-r98-N13   families_passed 105/105 verdict met    failed -
clone-r98-N12   families_passed 104/105 verdict unmet  failed EXPLICIT-VERSION-ECHO
```

Every leg's three runs agreed exactly (verdict, families, failed list, error rows). Named-family counts and
the per-run census: `receipts/census.json`. The frozen counting command was run per receipt:

```
python3 .ufo/waves/round-95/before/controls/count-runs.py <receipt>.json \
  --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
```

Full output: `receipts/count-runs-core.txt` (exit 0 for the gate met legs, 1 for the unmet legs).

PASS: landed gate 105/105 met ×3 canonical + ×3 clone, `[]`, 0 error rows. N13 104/105 `[Y]` ×3 + ×3.
N12 103/105 `[E, X]` ×3 + ×3. r98 control N13 met 105/105 ×3 + ×3; N12 104/105 `[E]` ×3 + ×3.

## 5. Counterexample bends (wording attack)

Built in scratch with one exact-once substitution each (`make_attacks.py`), `compile()`d, diffed:
E1 = Y echo + Y era (2 changed lines), E1b = Y era only (1), E2 = leading-zero-normalizing echo (1),
E3 = Z-keyed echo (1), E4 = echo lie only for `012.999999999.4` (1). Each was run with the r99 battery
`--runs 3` from the lane (`canon-E1`, `canon-E1b`, `canon-E2`, `canon-E3`, `canon-E4`).

| bend | verdict | failed_families | failed rows/run | named (X / Y / Z / E / LZ) |
|---|---|---|---|---|
| E1 Y echo + Y era | unmet 104/105 | `[REFUSAL-VERSIONS-9DIGIT-Y]` | 4 | 4/4, 0/4, 4/4, 4/4, 4/4 |
| E1b Y era only | unmet 104/105 | `[REFUSAL-VERSIONS-9DIGIT-Y]` | 2 | 4/4, 2/4, 4/4, 4/4, 4/4 |
| E2 leading-zero echo | unmet 104/105 | `[LEADING-ZERO-NORMALIZE]` | 4 | 4/4, 4/4, 4/4, 4/4, 0/4 |
| E3 Z-keyed echo | unmet 104/105 | `[REFUSAL-VERSIONS-9DIGIT-Z]` | 4 | 4/4, 4/4, 0/4, 4/4, 4/4 |
| E4 `012.999999999.4` only | met 105/105 | `[]` | 0 | all 4/4 |

E1b's failed rows carry the TRUE echo (`got[5] == "12.999999999.4"`): the failure is the era conjunct
only. E4 is a Y-cap lie on an accepted spelling the roster does not carry; it survives.

Direct probes (no battery): `direct_probe.py`, `direct_paths.py`, `direct_cap_spellings.py`.

- `012.999999999.4` is accepted by the landed gate (rc 0, echo verbatim, era `12.9.5+`); N13 fires on it
  (`12.999999998.4`), N12 does not. `0999999999.9.9` is refused rc 64.
- On a readable conf, the field set differing from the landed gate is exactly `["limine_version"]` for the
  cap-keyed bend and `[]` otherwise; `rc`, `verdict`, `visibility_era`, `limine_version_source` identical.
- On `--conf` = a directory (the early return), N12/N13 return the TRUE echo for both caps
  (`999999999.9.9`, `12.999999999.4`), rc 2 — the bends do not falsify that path.

Receipts: `receipts/canon-E{1,1b,2,3,4}.json`, `receipts/direct-leading-zero-probe.json`,
`receipts/direct-path-and-field-probe.json`, `receipts/direct-cap-spellings-probe.json`.

## 6. Blanket `limine-version` lie wrapper (plan-wording evidence)

The r99 `LIE_WRAPPER` template was materialised in scratch around the pinned gate (one field falsified
globally, not a source bend) and run once:

```
python3 tools/limine-pin-battery-r99.py --gate <scratch>/instr/lie-limine-version.py --runs 1 …
```

Raw:

```
families_passed 93/105 verdict unmet failed AUTO-ERA-A,AUTO-ERA-B,AUTO-PROBE-FAIL,AUTO-PROBE-SHAPES,
EXPLICIT-VERSION-ECHO,EXTRA-COMPONENT,LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS,REFUSAL-VERSIONS-10DIGIT,
REFUSAL-VERSIONS-9DIGIT,REFUSAL-VERSIONS-9DIGIT-Y,REFUSAL-VERSIONS-9DIGIT-Z
error_rows 0   named X 0/4, Y 0/4, Z 0/4, LZ 0/4
```

This reproduces the r99 reading (`unmet 93/105`) and shows the `check_echo` flags ARE exercised, but only
by a non-spelling-targeted wrapper. Receipt: `receipts/lie-limine-version-r99.json` + `.count.txt`.

## 7. Selftest

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
python3 tools/limine-pin-battery-r99.py --selftest
```

Raw (`receipts/selftest-no-reference.txt`):

```
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
```

PASS: 5/5, rc 0.

## 8. Error-row census

15 legs × `--runs 3` = 45 runs, 420 case rows each = **18,900 rows**. Non-null `error` rows: **0 in
every run** (45/45). `got is None`: 20 per run (900 total), all `kind: "usage"` rows, all passed (not
errors). Failed rows/run: gate 0, N13 4, N12 5, r98-N12 1, r98-N13 0, E1 4, E1b 2, E2 4, E3 4, E4 0.
The blanket-lie run adds 1 run × 420 rows, 0 error rows. Machine-readable: `receipts/census.json`.

## 9. PASS/FAIL against the frozen target

| expected clause | measured | verdict |
|---|---|---|
| gate met 105/105 `[]`, 0 errors, ×3 canonical + ×3 clone | exactly | PASS |
| N13 unmet 104/105 ×3 both, exactly `[Y]`, 0 errors | exactly | PASS |
| N12 unmet 103/105 ×3 both, exactly `[E, X]`, 0 errors | exactly | PASS |
| r98 N13 met 105/105 ×3 both | exactly | PASS |
| r98 N12 unmet 104/105 ×3 both, exactly `[E]` | exactly | PASS |
| one changed line per bend | one `-`/`+` pair each; re-derived bytes identical | PASS |
| selftest PASS 5/5 | PASS 5/5 | PASS |
| "exactly when the component is the cap" over all returns | false on the conf-unreadable return | **FAIL (wording; A1)** |
| "a one-family delta, never a met-to-unmet flip" | family E flips met→unmet under the control | **FAIL (wording; A2)** |
| plan "no bend has ever exercised" the echo flags | blanket wrapper reads 93/105, X/Y/Z/LZ | **FAIL (wording; A3)** |

The three wording failures do not change any number; they are recorded in `ReviewBends.md` with proposed
A1/A2/A3 lines and receipts.

## 10. Receipts index

`receipts/clone-identity.txt`, `bend-diffs.txt`, `selftest-no-reference.txt`,
`canon-*.json` + `.log`, `clone-*.json` + `.log`, `canon-E*.json` + `.log`,
`count-runs-core.txt`, `census.json`, `lie-limine-version-r99.json` + `.log` + `.count.txt`,
`direct-leading-zero-probe.json`, `direct-path-and-field-probe.json`, `direct-cap-spellings-probe.json`.
Scoped findings: `.ufo/waves/round-100/w1/ReviewBends.md`.

Tooling: none installed or upgraded (pacman paused; not used). `bwrap` already at `/usr/bin/bwrap`.
Scratch was deleted after the last probe and the deletion verified (`SCRATCH_DELETED`; the directory no
longer exists). The receipts in this seat dir are the remaining evidence.

{"seat":"ReviewBends","verdict":"findings","notes":"Numbers reproduce: gate met 105/105 x3 canonical + x3 clone; N13 104/105 [REFUSAL-VERSIONS-9DIGIT-Y] x3+x3; N12 103/105 [EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT] x3+x3; r98 control N13 met 105/105, N12 104/105 [EXPLICIT-VERSION-ECHO] x3+x3; selftest 5/5; 0 error rows in 45 runs / 18,900 rows. Three wording defects: (A1) 'falsifies exactly when the component is the cap' omits the readable-conf conjunct — the early conf-unreadable return (BYTE 11230) still echoes the true value, so a cap spelling there is not falsified; (A2) 'never a met-to-unmet flip' contradicts the same sentence's family-level reading (the r98 control flips EXPLICIT-VERSION-ECHO from the landed gate's met to unmet); (A3) the plan attributes 'no bend has ever exercised' to the round-99 Frontier, which says 'no spelling-targeted committed bend' — the re-run blanket lie wrapper reads 93/105 with X/Y/Z/LZ named. Clause attribution is carried by the one-line diff at BYTE 16931, not by the family count: a Y-era-only bend and a Y-echo+Y-era bend both read 104/105 [Y]. Z-keyed bend hits Z not Y; N12 never includes Y and always includes E; check_echo fails leading-zero normalization (E2 104/105 [LEADING-ZERO-NORMALIZE]); a Y-cap lie on the roster-absent spelling 012.999999999.4 survives 105/105."}
