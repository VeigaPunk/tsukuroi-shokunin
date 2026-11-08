# ExecBend — round 95 wave w1 (C1 near-miss leg: bend N05-strict-8)

Executor seat. Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; lane HEAD and `master`
at run time `884ed06bdc7681ad73e757cf8a02bee21de2c480` (pre-round tip `c0a20cef`; the wave's
untracked receipts were present, 7 porcelain lines, untouched). All commands read-only on the lane;
the only git operation was `git clone --shared` into my scratch.

Axes named: **depth** (C1's near-miss leg — this seat's assigned move) and **operability**
(no-harm only: no lane instrument, registry or gate byte is modified by this seat). No other axis is
read or moved.

Scratch root `/fast/scratch/hyaku/tsukuroi-r95/ExecBend` was deleted before yield; every receipt
below is under this seat dir (`.ufo/waves/round-95/w1/ExecBend/`).

## 0. Instrument freeze check (supporting)

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-95/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: OK
tools/make-r95-bends.py: OK
.ufo/waves/round-95/before/controls/bends/N05-strict-8.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/waves/round-95/before/controls/do-nothing-battery-r94.py: OK
.ufo/waves/round-95/before/controls/do-nothing-gate-r94.py: OK
.ufo/waves/round-95/claims.json: OK
.ufo/waves/round-95/before/plan-frozen.md: OK
sha-check rc=0
```

The clone repeated the same check (`clone-instruments-check.txt`, rc=0, all 9 OK). Receipts:
`instruments-check.txt`, `clone-instruments-check.txt`. Gate `7d79ac29…`, battery `a51dca18…`,
bend `a1dead8b…` — identical to the freeze manifest.

Tooling: nothing installed; used system `python3` 3.14.8, `/usr/bin/bwrap`, `/usr/bin/limine`
(probe reads `Limine 12.9.4`). No pacman transaction; no host mutation.

## 1. The frozen bend differs from the gate by exactly one line

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
diff -u tools/check-limine-pins.py .ufo/waves/round-95/before/controls/bends/N05-strict-8.py > .ufo/waves/round-95/w1/ExecBend/n05-diff.txt
echo "diff rc=$?"
```

```
--- tools/check-limine-pins.py	2026-11-08 03:56:46.703650900 -0300
+++ .ufo/waves/round-95/before/controls/bends/N05-strict-8.py	2026-11-08 06:47:14.691241614 -0300
@@ -96,7 +96,7 @@
     if not isinstance(text, str):
         return None
     parts = text.split(".")
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 8 for p in parts):  # N05 (bound bent to <=8)
         return None
     return tuple(int(p) for p in parts)
```

`diff rc=1` (differences, as expected). Line counts: `minus-lines=1`, `plus-lines=1`,
`hunks=1` (`diff-counts.txt`). **PASS** — exactly one changed line, the `<= 9` → `<= 8` bound (with
the prescribed `# N05 (bound bent to <=8)` trailer), nothing else.

## 2. Re-derivation in scratch is byte-identical to the frozen bend

```
cd /fast/scratch/hyaku/tsukuroi-r95/ExecBend
python3  # read tools/check-limine-pins.py; replace the clause exactly once; write N05-rederived.py
old occurrence count: 1
new occurrence count (pre-replace): 0
written bytes: 30313
sha256 rederived: a1dead8b9aae8ece7e3272607420ead3e4887673f4d4373a926bac381b3d66cb
cmp /fast/scratch/hyaku/tsukuroi-r95/ExecBend/N05-rederived.py <lane>/.ufo/waves/round-95/before/controls/bends/N05-strict-8.py
cmp rc=0
```

Old clause `and len(p) <= 9 for p in parts):` occurs **once**; new clause occurs **0** times before
the substitution; the derivation was asserted on the count. **PASS** — counts 1/0, 30313 bytes,
sha256 matches the frozen bend, `cmp` rc 0. Receipt: `n05-rederive.txt`.

## 3. Canonical layout: r95 battery ×3 against the frozen bend

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
export TMPDIR=/fast/scratch/hyaku/tsukuroi-r95/ExecBend/work-canonical
python3 tools/limine-pin-battery-r95.py \
  --gate /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-95/before/controls/bends/N05-strict-8.py \
  --runs 3 --work "$TMPDIR" \
  --json .ufo/waves/round-95/w1/ExecBend/n05-canonical.json
```

```
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
rc=1   (battery contract: 1 = unmet)
```

Parsed from `n05-canonical.json` (`n05-canonical-analysis.txt`), per run:

| run | verdict | passed | failed_families | cases | error rows | error families | error rows outside digit9 | failed rows outside digit9 |
|---|---|---|---|---|---|---|---|---|
| 0 | `unmet` | 98/99 | `['REFUSAL-VERSIONS-9DIGIT']` | 396 | 4 | `{'REFUSAL-VERSIONS-9DIGIT': 4}` | 0 | `[]` |
| 1 | `unmet` | 98/99 | `['REFUSAL-VERSIONS-9DIGIT']` | 396 | 4 | `{'REFUSAL-VERSIONS-9DIGIT': 4}` | 0 | `[]` |
| 2 | `unmet` | 98/99 | `['REFUSAL-VERSIONS-9DIGIT']` | 396 | 4 | `{'REFUSAL-VERSIONS-9DIGIT': 4}` | 0 | `[]` |

**PASS** — 3/3 `unmet` 98/99, `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]`, every error
row inside the family, 0 failed or error rows in any other family.

## 4. Clone layout: shared clone's battery against the clone's frozen bend

```
cd /fast/scratch/hyaku/tsukuroi-r95/ExecBend
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin lane-clone   # rc=0
cd lane-clone   # git rev-parse --show-toplevel = /fast/scratch/hyaku/tsukuroi-r95/ExecBend/lane-clone
# head=884ed06bdc7681ad73e757cf8a02bee21de2c480  master=884ed06b…  dirty=0
export TMPDIR=/fast/scratch/hyaku/tsukuroi-r95/ExecBend/work-clone
python3 tools/limine-pin-battery-r95.py \
  --gate /fast/scratch/hyaku/tsukuroi-r95/ExecBend/lane-clone/.ufo/waves/round-95/before/controls/bends/N05-strict-8.py \
  --runs 3 --work "$TMPDIR" \
  --json /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-95/w1/ExecBend/n05-clone.json
```

```
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
families_passed 98/99 verdict unmet failed REFUSAL-VERSIONS-9DIGIT
rc=1
```

Clone bytes verified equal to the freeze: battery `a51dca18…`, bend `a1dead8b…`, gate
`7d79ac29…` (`clone-provenance.txt`); the `gate` field of every run names the clone's bend path.
Parsed from `n05-clone.json` (`n05-clone-analysis.txt`): all three runs `unmet` 98/99,
`failed_families ['REFUSAL-VERSIONS-9DIGIT']`, 4 error rows all inside the family, 0 outside.
**PASS**.

## 5. The bend's refusal receipt (four family rows, canonical run 0, verbatim)

From `n05-canonical.json` run index 0, family `REFUSAL-VERSIONS-9DIGIT` (4 rows, all `passed=false`;
`n05-family-errors.txt` carries the same text for all four rows):

```
bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h] [--conf CONF] [--esp ESP] [--secure-boot-enforced {0,1}]
               [--tpm-present {0,1}] [--limine-version LIMINE_VERSION]
               [--live] [--selftest]
check-limine-pins: --limine-version must be X.Y.Z or auto
```

The text is byte-identical across the four rows and across the three runs (`n05-canonical-analysis.txt`
run1/run2 rows). It is the bend's refusal: rc 64, empty stdout, argparse message on stderr — the
gate refuses the in-bound `999999999.9.9`, which is exactly what the family must catch.
**PASS** (this error leg is expected only in the N05 leg per plan A1).

## 6. count-runs against the family target — exit 1 as expected

```
python3 .ufo/waves/round-95/before/controls/count-runs.py \
  .ufo/waves/round-95/w1/ExecBend/n05-canonical.json --family REFUSAL-VERSIONS-9DIGIT
count-runs canonical rc=1
```

Summary parsed (identical for `n05-clone.json`, `count-runs clone rc=1`): three runs, each
`verdict unmet`, `families_passed 98 / families_total 99`,
`failed_families ["REFUSAL-VERSIONS-9DIGIT"]`, `cases 396`, `error_rows 4`, named family
`[passed=0, failed=4]`.

Exit 1 is the control's documented unmet exit (its docstring: "Exit 0 iff every run on the landed
gate meets the frozen targets"). **PASS** — exit code 1 recorded as the measured value, not retried.

## Expected-vs-measured

| expected line | measured | verdict |
|---|---|---|
| diff shows exactly one changed line (the `<= 9` → `<= 8` bound), nothing else | 1 minus / 1 plus line, 1 hunk; only the bound line; **PASS** |
| re-derived bend: old clause once, new 0 before replace, `cmp` byte-equal | old 1, new 0, 30313 bytes, sha256 `a1dead8b…`, `cmp rc=0` | **PASS** |
| 3 canonical runs: `unmet`, 98/99, `failed_families` exactly `["REFUSAL-VERSIONS-9DIGIT"]` | 3/3 exactly that | **PASS** |
| 3 clone runs: same | 3/3 exactly that | **PASS** |
| 0 case rows outside the family with an error | 0 in every run, both layouts | **PASS** |
| four family rows carry the battery `error` text | 4/4 rows, identical `bad-output: JSONDecodeError rc=64 … --limine-version must be X.Y.Z or auto` | **PASS** |
| count-runs exits 1 for both (run is unmet) | rc 1 for canonical and clone | **PASS** |

No finding: `failed_families` never contains any family other than `REFUSAL-VERSIONS-9DIGIT`.

## Receipts (all under `.ufo/waves/round-95/w1/ExecBend/`)

- `n05-diff.txt`, `diff-counts.txt`
- `n05-rederive.txt`
- `n05-canonical.json`, `n05-canonical.stdout`, `n05-canonical.stderr`, `n05-canonical.rc`,
  `n05-canonical-analysis.txt`
- `n05-clone.json`, `n05-clone.stdout`, `n05-clone.stderr`, `n05-clone.rc`,
  `n05-clone-analysis.txt`, `clone-provenance.txt`
- `n05-family-errors.txt`
- `count-runs-canonical.txt`, `count-runs-canonical.rc`, `count-runs-canonical.stderr`,
  `count-runs-clone.txt`, `count-runs-clone.rc`
- `instruments-check.txt`, `clone-instruments-check.txt`

## Risks / limits

- The clone leg is a layout repeat of the same frozen bytes (sha-verified identical instrument and
  bend), not an independent-bytes control; that is what C1's "both layouts" asks for.
- The clone's work tree was clean at `884ed06b`; the lane's 7 untracked receipt files from sibling
  seats were neither read as inputs nor modified.
- The battery's four digit9 rows all fail via one error shape (`rc 64`, empty stdout); the family
  cannot distinguish per-case shapes because the refusal precedes any fixture read. This matches
  plan A1's declared N05 leg.

{"seat":"ExecBend","verdict":"met","notes":"Frozen bend N05-strict-8 differs from the gate by exactly one line (<=9 -> <=8); scratch re-derivation is byte-identical (30313 bytes, sha256 a1dead8b..., cmp rc 0). r95 battery x3 canonical and x3 clone: all six runs unmet 98/99 with failed_families exactly [REFUSAL-VERSIONS-9DIGIT], 4 error rows per run all inside that family, 0 error or failed rows outside it; the four rows carry the rc-64 empty-stdout refusal text (bad-output: JSONDecodeError rc=64 ... --limine-version must be X.Y.Z or auto). count-runs exits 1 for both JSONs as expected for an unmet run. Instrument sha256 verified at lane and clone."}
