# Seat ExecBend — round 96 w1 — C1 near-miss leg (four frozen bends, both layouts)

Seat: `ExecBend`. Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
All receipts below are written by this seat under
`.ufo/waves/round-96/w1/ExecBend/`. Scratch: `/fast/scratch/hyaku/tsukuroi-r96/ExecBend`
(deleted at seat close). No lane file outside the seat dir was written; no instrument was modified.

## 0. Instrument freeze state

```
$ sha256sum -c .ufo/waves/round-96/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r96.py: OK
tools/make-r96-bends.py: OK
tools/check-r96-calibration.py: FAILED          <- at seat start (in-flight C2 edit)
tools/check-registry-coverage.py: OK
...
.ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py: OK
... N02/N03/N04 .py: OK
```

At seat start (before any battery run) `tools/check-r96-calibration.py` differed from the freeze
manifest; at report time it matches again (`hash-check-at-report.txt`, 2026-11-08T07:59:07-03:00):

```
2026-11-08T07:59:07-03:00
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r96.py: OK
tools/make-r96-bends.py: OK
tools/check-r96-calibration.py: OK
tools/check-registry-coverage.py: OK
...
7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4  tools/check-r96-calibration.py
```

C1's void clause names *any* instrument byte in the manifest; the final state is clean, but the
transient mismatch is recorded here because it names `check-r96-calibration.py`, a C2 instrument.

## 1. One-clause diffs (expected: exactly one changed line per bend)

```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py > .ufo/waves/round-96/w1/ExecBend/diff-N01-echo-wrong.txt
@@ -313,7 +313,7 @@
-            "limine_version": limine_version,
+            "limine_version": "99.9.9" if limine_version_source == "flag" else limine_version,  # N01 (echo bent)

$ diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py > .../diff-N02-y-cap-8.txt
@@ -96,7 +96,7 @@
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (len(p) <= 8 or p is not parts[1])) for p in parts):  # N02 (Y bound bent to <=8)

$ diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py > .../diff-N03-era-label-flip.txt
@@ -315,7 +315,7 @@
-            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",
+            "visibility_era": "pre-12.9.5" if era_b else "12.9.5+",  # N03 (label bent)

$ diff -u tools/check-limine-pins.py .ufo/waves/round-96/before/controls/bends/N04-extra-components.py > .../diff-N04-extra-components.txt
@@ -96,7 +96,7 @@
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) < 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):  # N04p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
```

Each diff contains exactly one `-`/`+` pair inside one `@@` hunk (verified by counting
`^[+-][^+-]` lines: 2 per file) — **PASS** ×4. `N04-extra-components.py` parses (`ast.parse` ok).

## 2. Canonical lane — battery, 3 runs per bend

Command form (one per bend, cwd = lane root; `--json` under the seat dir):

```
python3 tools/limine-pin-battery-r96.py \
  --gate .ufo/waves/round-96/before/controls/bends/<bend>.py \
  --runs 3 --work /fast/scratch/hyaku/tsukuroi-r96/ExecBend/work-canon-<bend> \
  --json .ufo/waves/round-96/w1/ExecBend/bend-<bend>.json
```

Raw stdout (one line per run):

```
N01  families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ECHO      (x3)  rc=1
N02  families_passed 102/103 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y  (x3)  rc=1
N03  families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ERA       (x3)  rc=1
N04  families_passed 101/103 verdict unmet failed EXTRA-COMPONENT,REFUSAL-VERSIONS  (x3)  rc=1
```

Per-run JSON (`counts-summary.txt`, count-runs on each receipt; 412 cases = 103 families × 4):

```
N01 canonical  run0..2: unmet 102/103 failed ['EXPLICIT-VERSION-ECHO']                   cases 412 errors 0
N02 canonical  run0..2: unmet 102/103 failed ['REFUSAL-VERSIONS-9DIGIT-Y']               cases 412 errors 4
N03 canonical  run0..2: unmet 102/103 failed ['EXPLICIT-VERSION-ERA']                    cases 412 errors 0
N04 canonical  run0..2: unmet 101/103 failed ['EXTRA-COMPONENT','REFUSAL-VERSIONS']      cases 412 errors 0
```

## 3. Clone layout — `git clone --shared` at 38adc4ed

```
$ cd /fast/scratch/hyaku/tsukuroi-r96/ExecBend
$ git clone --shared --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin clone-r96
$ cd clone-r96 && test "$(git rev-parse --show-toplevel)" = "$(pwd)" && echo TOPLEVEL-OK
TOPLEVEL-OK
$ git checkout --detach 38adc4ed
HEAD is now at 38adc4ed round-96: freeze — C1 metadata/per-component/extra-component families (roster 103) and C2 calibration checker; ...
$ git rev-parse HEAD
38adc4edbf7818093d8f3754df4b697bf9eea199
$ sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r96.py .ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  tools/limine-pin-battery-r96.py
f78798c0d5ec7ec72fe01b14d6b13ae4c69ccc4c4af34179492171e28cbc71f4  .ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py
```

Same battery invocation from the clone (gate path inside the clone, `--json <seat>/bend-<bend>-clone.json`):

```
N01 clone  families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ECHO      (x3)  rc=1
N02 clone  families_passed 102/103 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y  (x3)  rc=1
N03 clone  families_passed 102/103 verdict unmet failed EXPLICIT-VERSION-ERA       (x3)  rc=1
N04 clone  families_passed 101/103 verdict unmet failed EXTRA-COMPONENT,REFUSAL-VERSIONS  (x3)  rc=1
```

Per-run JSON:

```
N01 clone  run0..2: unmet 102/103 failed ['EXPLICIT-VERSION-ECHO']                cases 412 errors 0
N02 clone  run0..2: unmet 102/103 failed ['REFUSAL-VERSIONS-9DIGIT-Y']            cases 412 errors 4
N03 clone  run0..2: unmet 102/103 failed ['EXPLICIT-VERSION-ERA']                 cases 412 errors 0
N04 clone  run0..2: unmet 101/103 failed ['EXTRA-COMPONENT','REFUSAL-VERSIONS']   cases 412 errors 0
```

## 4. Raw deviations

- **N01** (`deviations-fields.txt`): each of the 4 `EXPLICIT-VERSION-ECHO` cases fails only on the
  echoed version — `got[8]` (logged as `limine_version`) is `"99.9.9"`, `limine_version_source`
  `"flag"`, while rc/verdict/pins/on_panic match `want`. Detection is a parseable mismatch
  (`error: null`).
- **N03** (`n03-era-raw.json`, built with the battery's own `EXPLICIT-VERSION-ERA` fixture builder
  and run with the unbent frozen gate vs the N03 bend):

  ```
  12.9.4        control visibility_era pre-12.9.5 (rc 1)  |  bend 12.9.5+ (rc 1)
  12.9.5        control 12.9.5+                (rc 1)  |  bend pre-12.9.5 (rc 1)
  12.9.6        control 12.9.5+                (rc 1)  |  bend pre-12.9.5 (rc 1)
  999999999.9.9 control 12.9.5+                (rc 1)  |  bend pre-12.9.5 (rc 1)
  ```

  The logged case rows show rc/verdict/pins equal for want/got; the failing field
  (`visibility_era`) is not serialised in `case_log`, hence the direct probe above.
- **N04** (`bend-N04-extra-components.json`): 8 failed rows, `error: null`, `got` a readable row
  string, e.g. `"'12.9.6.1' rc=0 stdout=867; '12.9.6.1.0' rc=0 stdout=869; '12.9.6.99' rc=0
  stdout=868; '12.9.6.7' rc=0 stdout=867"` against `want [64,"usage"]`, plus the pre-existing
  `'12.9.5.1' rc=0 stdout=343` row twice per run in `REFUSAL-VERSIONS`.
- **N02** (`bend-N02-y-cap-8.json`, `n02-raw.json`): all 4 family cases carry a **non-null** `error`:

  ```
  error='bad-output: JSONDecodeError rc=64 stderr=usage: gate.py ... check-limine-pins:
  --limine-version must be X.Y.Z or auto\n'
  ```

  Direct probe: unbent gate accepts both values (`12.999999999.4` → rc 1 DEGRADED era
  `12.9.5+`; `0.999999999.0` → rc 1 DEGRADED era `pre-12.9.5`); the N02 bend refuses both with
  rc 64 and 0 stdout bytes.

## 5. PASS/FAIL per expected line

| # | Expected line | Result |
|---|---|---|
| 1 | Each bend diff shows exactly one changed line | **PASS** ×4 (`diff-*.txt`) |
| 2 | N01 canonical+clone, 3 runs each: `unmet`, 102/103, `["EXPLICIT-VERSION-ECHO"]`, 0 error rows | **PASS** |
| 3 | N02 canonical+clone, 3 runs each: `unmet`, 102/103, `["REFUSAL-VERSIONS-9DIGIT-Y"]`, 0 error rows | **FAIL on error rows** — verdict/count/family exact, but 4 non-null `error` rows per run in both layouts |
| 4 | N03 canonical+clone, 3 runs each: `unmet`, 102/103, `["EXPLICIT-VERSION-ERA"]`, 0 error rows | **PASS** |
| 5 | N04 canonical+clone, 3 runs each: `unmet`, 101/103, `["EXTRA-COMPONENT","REFUSAL-VERSIONS"]`, 0 error rows | **PASS** |

Raw error-row counts per bend, all three runs in both layouts: **N01 0, N02 4, N03 0, N04 0**.

The run wins over the expected value: the frozen C1 target's "0 error rows" clause for *bend* runs
is contradicted by the frozen instrument + frozen N02 bend pair. C1's kill rule as filed reads
"unmet if ... any bend run ... carries a non-null `error` row", and N02 does (deterministically,
4 rows/run, both layouts). Amendment **A3** (2026-11-08, before the round report;
`.ufo/waves/round-96/before/plan-amendments-A1-A2.md`, datum `w1/ExecBend/bend-N02*.json`,
`w1/ExecBattery/c1-bend-N02-y-cap-8.json`) narrows the clause to "0 error rows on every landed-gate
and do-nothing leg; on a bend leg, only the bend's own refusal rows, named and counted (N02: 4 per
run; N01/N03/N04: 0)" and records the miss as `R96-N02-ERRORROWS`; the frozen numbers, exact
`failed_families` and every other clause stand. The raw counts above are that datum. The battery records the bend's correct refusal as
`bad-output: JSONDecodeError rc=64` because `run_gate` only clears `error` for parseable JSON;
`REFUSAL-VERSIONS-9DIGIT-Y` is an accepted-leg family driven through `run_gate`, so a bend that
turns it into a refusal necessarily lands in the error channel. N01/N03/N04 fail through parseable
mismatches and carry `error: null`. No instrument byte was edited and no run was retried.

## 6. Receipts (all under `.ufo/waves/round-96/w1/ExecBend/`)

- `diff-N01-echo-wrong.txt`, `diff-N02-y-cap-8.txt`, `diff-N03-era-label-flip.txt`,
  `diff-N04-extra-components.txt`
- `bend-N01-echo-wrong.json`, `bend-N02-y-cap-8.json`, `bend-N03-era-label-flip.json`,
  `bend-N04-extra-components.json` (canonical, 3 runs each)
- `bend-N01-echo-wrong-clone.json`, `bend-N02-y-cap-8-clone.json`,
  `bend-N03-era-label-flip-clone.json`, `bend-N04-extra-components-clone.json` (clone at 38adc4ed)
- `count-<bend>[-clone].txt` (count-runs.py per receipt), `counts-summary.txt`,
  `deviations.txt`, `deviations-fields.txt`, `n02-raw.json`, `n03-era-raw.json`,
  `hash-check-at-report.txt`

Tooling: no installs or upgrades (python3 3.x + `bwrap` already present; pacman untouched).

```json
{"seat":"ExecBend","verdict":"findings","notes":"N01/N03/N04: unmet 102/103 (N04 101/103) in 3 runs x2 layouts with exactly the frozen failed_families, 0 error rows; diffs each one changed line. N02: verdict/count/family exact (102/103, [REFUSAL-VERSIONS-9DIGIT-Y]) and refusal confirmed rc=64 empty stdout in both layouts, with 4 non-null error rows per run (bad-output JSONDecodeError rc=64); amendment A3 narrows the clause to bend-own refusal rows named and counted (R96-N02-ERRORROWS). Raw error-row counts: N01 0, N02 4, N03 0, N04 0. No instrument edited, no retry. Instrument freeze manifest read OK at 07:59:07 (check-r96-calibration.py was mid-edit FAILED at seat start)."}
```
