# ExecBend — round 96 w1 — scoped findings (C1 near-miss leg)

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Full receipt set and report:
`.ufo/waves/round-96/w1/ExecBend/` (`report.md`). Scratch deleted after the runs.

## Commands and raw results

1) One-clause diffs — each saved to `.ufo/waves/round-96/w1/ExecBend/diff-<bend>.txt`:

```
diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py
diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py
diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py
diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N04-extra-components.py
```

Each file: one `@@` hunk, exactly one `-`/`+` pair (N01 echo, N02 Y bound `<=8`, N03 era label
flip, N04 `< 3` components). **PASS ×4.**

2) Battery, canonical lane (`--runs 3`, `--json` in seat dir), one line per run:

```
N01  families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ECHO              rc=1
N02  families_passed 102/103 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y          rc=1
N03  families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ERA               rc=1
N04  families_passed 101/103 verdict unmet failed EXTRA-COMPONENT,REFUSAL-VERSIONS   rc=1
```

3) `git clone --shared --no-hardlinks <lane> clone-r96`, `git checkout --detach 38adc4ed`
(toplevel asserted inside the clone) → `38adc4edbf7818093d8f3754df4b697bf9eea199`; gate and
battery sha256 identical to the canonical/frozen bytes. Same battery from the clone
(gate path inside the clone, bend bytes byte-identical):

```
N01 clone  unmet 102/103 failed EXPLICIT-VERSION-ECHO
N02 clone  unmet 102/103 failed REFUSAL-VERSIONS-9DIGIT-Y
N03 clone  unmet 102/103 failed EXPLICIT-VERSION-ERA
N04 clone  unmet 101/103 failed EXTRA-COMPONENT,REFUSAL-VERSIONS
```

4) `count-runs.py <receipt> --family <expected>` per receipt → `verdict unmet`, `cases 412`
(103×4), counts exactly as above, in every run of both layouts.

## PASS/FAIL

| Expected | Result |
|---|---|
| diffs: one changed line each | PASS ×4 |
| N01, 3 runs ×2 layouts: unmet 102/103 `["EXPLICIT-VERSION-ECHO"]`, 0 error rows | PASS (raw deviation: echo `99.9.9`) |
| N02, 3 runs ×2 layouts: unmet 102/103 `["REFUSAL-VERSIONS-9DIGIT-Y"]`, 0 error rows | **FAIL on error rows**: 4 non-null `error` rows per run in both layouts |
| N03, 3 runs ×2 layouts: unmet 102/103 `["EXPLICIT-VERSION-ERA"]`, 0 error rows | PASS (raw probe: era label flipped on all four versions) |
| N04, 3 runs ×2 layouts: unmet 101/103 `["EXTRA-COMPONENT","REFUSAL-VERSIONS"]`, 0 error rows | PASS (raw `got`: four extra-component values rc 0; pre-existing `12.9.5.1` row) |

## Finding (run wins over expected)

N02's detection is correct at family level (verdict `unmet`, 102/103, exact `failed_families`;
direct probe shows the unbent gate accepts `12.999999999.4` era `12.9.5+` and `0.999999999.0` era
`pre-12.9.5`, the bend refuses both rc 64 with empty stdout). But because
`REFUSAL-VERSIONS-9DIGIT-Y` is an accepted-leg family driven through `run_gate`, a refusal is
recorded as

```
error='bad-output: JSONDecodeError rc=64 stderr=usage: ... check-limine-pins: --limine-version must be X.Y.Z or auto'
```

for all 4 cases, in every run, in both layouts. Raw error-row counts per bend (3 runs x2 layouts):
**N01 0, N02 4, N03 0, N04 0**. The frozen C1 target says bend runs carry 0 error rows and the
frozen kill rule reads "unmet if ... any bend run ... carries a non-null `error` row"; amendment
**A3** (`.ufo/waves/round-96/before/plan-amendments-A1-A2.md`, datum `w1/ExecBend/bend-N02*.json`)
narrows it to bend-own refusal rows named and counted (`R96-N02-ERRORROWS`), frozen numbers and
`failed_families` standing. N01/N03/N04 fail through parseable mismatches (`error: null`). No
instrument byte was edited; no run was retried to a pass.

Freeze manifest: `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` read
`tools/check-r96-calibration.py: FAILED` at seat start (in-flight C2 edit) and all-OK at
`2026-11-08T07:59:07-03:00` (`hash-check-at-report.txt`).

Receipts: `.ufo/waves/round-96/w1/ExecBend/{diff-*.txt,bend-*.json,count-*.txt,counts-summary.txt,deviations.txt,deviations-fields.txt,n02-raw.json,n03-era-raw.json,hash-check-at-report.txt,report.md}`.

```json
{"seat":"ExecBend","verdict":"findings","notes":"N01/N03/N04: unmet 102/103 (N04 101/103) in 3 runs x2 layouts, exact failed_families, 0 error rows; each bend diff one changed line. N02: verdict/count/family exact and refusal confirmed rc=64 empty stdout both layouts, with 4 non-null error rows per run (bad-output JSONDecodeError rc=64); amendment A3 narrows the clause to bend-own refusal rows named and counted (R96-N02-ERRORROWS). Raw error-row counts N01 0, N02 4, N03 0, N04 0. No instrument edited, no retry."}
```
