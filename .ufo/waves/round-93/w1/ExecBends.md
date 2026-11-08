# ExecBends — round 93 w1 — independent canonical re-run (six bends + do-nothing legs)

Seat: ExecBends, executor (leaf). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` at freeze
`c633f49aa512e1c8a0e0464b7fb5d354c70096cf`. Scratch `/fast/scratch/hyaku/tsukuroi-r93/ExecBends` (deleted on
exit). Axes read: depth (C1 bends) and the C2 do-nothing/reachability legs. All runs are `--runs 1`: one
independent canonical run per item — the claim's ×3 / two-layout counts remain the claim owner's.

## Environment and exact commands

- Python 3.14.8; bubblewrap 0.13.1 (`/usr/bin/bwrap`); 32 cores; `TMPDIR` = scratch. Eight battery runs
  launched in parallel with `&` + `wait`, each with its own `--work`; wall time 53 s.
- cwd = scratch; lane instruments addressed by absolute path. The runs wrote only `--work`/`--json` under
  scratch (the battery copies gate bytes into its private case dirs).

```
S=/fast/scratch/hyaku/tsukuroi-r93/ExecBends; L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
for n in N01-exact-split N02-first-body N03-era-b-u1 N04-accept-any N05-auto-ignore N06-auto-fallback; do
  python3 "$L/tools/limine-pin-battery-r93.py" --gate "$L/.ufo/waves/round-93/before/controls/bends/$n.py" \
    --runs 1 --work "$S/w-$n" --json "$S/$n.json"          # six, in parallel
done
python3 "$L/tools/limine-pin-battery-r93.py" \
  --gate "$L/.ufo/waves/round-93/before/controls/do-nothing-gate-r92.py" \
  --runs 1 --work "$S/w-DNG" --json "$S/do-nothing-gate.json"
python3 "$L/.ufo/waves/round-93/before/controls/do-nothing-battery-r92.py" \
  --gate "$L/tools/check-limine-pins.py" \
  --runs 1 --work "$S/w-DNB" --json "$S/do-nothing-battery.json"
```

## Freeze / instrument bytes

`sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` from the lane root: **13 of 14 entries
verify**. Executable instruments all OK (full log in `w1/ExecBends/freeze-check.txt`): gate `6b4c53d1…b6260aa`,
battery `ddd7e955…75e1aad`, make-r93-bends `d0c3d3e7…7746b623`, six bends `088057d4…`, `91fb6edb…`,
`6ed2f6fa…`, `d9909896…`, `4c4f434f…`, `f9fe76f3…`, count helper `666eace6…`, do-nothing battery
`aef33925…`, do-nothing gate `35c1088b…`, claims `99baf139…`.

One mismatch: `.ufo/plans/round-93.md` — manifest `4600cfa32563d267ca2ded47168e55b63f4d2c60e4b11aadfb87ecb706d28002`,
actual `3668f0e8d264142b9e314c48cdcc156742777f872391bf88e1fb02d0eb049c87`; plan mtime
2026-11-08 03:10:09 -0300 vs manifest mtime 03:04:56. The delta is the post-freeze **Amendment A1** appended at
plan line 125: it narrows the C2 do-nothing control sentence; the C1/C2 predicate, target and kill rules are
unchanged.

The do-nothing copies are byte-identical to the pre-freeze instruments: do-nothing gate = pre-freeze
`tools/check-limine-pins.py` hash `35c1088b…`; do-nothing battery = `tools/limine-pin-battery-r92.py` hash
`aef33925…` (see `pre-freeze-shas.txt` lines 1–2).

**Kill-rule boundary (flagged, not authored here):** the seat card lists the declaration among the
instruments, while the kill rule says "void if any instrument byte differs from the freeze manifest at scoring
time". Read literally against `.ufo/plans/round-93.md`, that would void C1/C2; SCORECARD's *Instruments*
paragraph names only the battery, candidate gate, bends and do-nothing controls, and the plan's own amendment
slot sanctions post-data appends. No executable instrument differs. Adjudication belongs to the
reviewer/sentinel; this seat did not modify the plan.

## 1. Six bends — one independent canonical run each

All six: 384 cases (96 families × 4), exit rc 1, **0 non-null-error rows**. Receipts: `N0*.json`, `N0*.out`,
`N0*.rc`.

| Bend | families_passed | named family | named pass/fail | all failed_families (each 0/4) | error rows |
|---|---|---|---|---|---|
| N01-exact-split | 95/96 | ERA-EXACT-125 | 0/4 | ERA-EXACT-125 | 0 |
| N02-first-body | 88/96 | ERA-B-FIRST-BODY | 0/4 | AUTO-ERA-B, ERA-B-FIRST-BODY, ERA-EXACT-125, ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B, GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN | 0 |
| N03-era-b-u1 | 95/96 | ERA-B-U1 | 0/4 | ERA-B-U1 | 0 |
| N04-accept-any | 95/96 | REFUSAL-VERSIONS | 0/4 | REFUSAL-VERSIONS | 0 |
| N05-auto-ignore | 95/96 | AUTO-ERA-B | 0/4 | AUTO-ERA-B | 0 |
| N06-auto-fallback | 95/96 | AUTO-PROBE-FAIL | 0/4 | AUTO-PROBE-FAIL | 0 |

Clause-level evidence (first failing case per named family; `want`/`got` are the battery's tuples):

- **N01** `want` pins consequence `panic` at line 3; `got` `prompt`, `limine_version 12.9.5`, source `flag` —
  the exact 12.9.5 boundary reads as era A, so a first-line entry's `hash_mismatch_panic: no` is visible.
- **N02** `want` line 4 `panic`; `got` line 4 `prompt`, `12.9.6`, source `flag` — the cut lands one line late,
  so the first body line stays global.
- **N03** rc/verdict/pins/on_panic match the expectation; the battery's `u1_ok` predicate is the (unlogged)
  discriminator and `ERA-B-U1` is 0/4. The battery is frozen, so this is localized by family + the U1 clause
  the bend deletes, not by re-instrumentation.
- **N04** the ten out-of-range values return rc 1 (not 64) with empty stdout — `12.9`, `12.9.5.1`, `abc`, ``,
  ` 12.9.5`, `12.9.5 `, `+12.9.5`, `12..5`, `12.9.5-rc1`, 40-digit — the refusal is deleted.
- **N05** `want` line 3 `panic`; `got` `prompt`, `12.9.6`, source `probe` — the probe ran and was recorded but
  is not used for era selection.
- **N06** `auto` with the failing fake `limine` returns rc 0, stdout 878 B (a verdict) instead of rc 64 /
  empty stdout — the probe failure falls back to 12.9.4.

Primary cross-check: for every bend, this seat's `families_passed` and `failed_families` are identical to all
three runs in `.ufo/waves/round-93/after/bend-*.json`, each of which has 0 non-null error rows.

Scope notes: N02's single `first_entry + 1` clause moves the shared era-B cut, so it flips eight families (each
0/4), not only the named one — one syntactic clause, family-broad by construction; the named-family kill still
fires. N03's failure is the unlogged `u1_ok` predicate (see above).

## 2. Do-nothing legs

### 2a. r92 gate through the r93 battery — 94/96 `unmet`, rc 1, 8 error rows

- Failed exactly: `AUTO-ERA-A` 0/4 and `AUTO-ERA-B` 0/4; all eight rows are `bad-output: JSONDecodeError
  rc=64` with `--limine-version must be X.Y.Z` on stderr.
- `AUTO-PROBE-FAIL` **passes 4/4**: rows `{"version":"auto","rc":64,"stdout_bytes":0,"ok":true}` ×4.
- C1 families all pass 4/4: `ERA-EXACT-125`, `ERA-B-FIRST-BODY`, `ERA-B-U1`, `REFUSAL-VERSIONS`.
- The other 90 families pass (94 = 96 − 2).

So the seat-card expectation "the three AUTO-* families failed" is **falsified by measurement**: only two
fail. `AUTO-PROBE-FAIL` is satisfied by a gate that refuses every `auto` with rc 64/empty stdout — exactly the
probe-failure refusal shape — so a refusal-shaped control cannot distinguish "refuses because the probe failed"
from "refuses `auto` always". This does not weaken C2's declared predicate/target (they never claim the
do-nothing fails all three auto families); it falsifies only the frozen control sentence. Amendment A1
(post-freeze) records the same 94/96 and 8 error rows and narrows that sentence; this independent run
reproduces it exactly, including the error-row count, and matches `after/c2-donothing-r92-gate.json`.

### 2b. r92 battery (do-nothing battery) against the landed gate

- `grep -c 'ERA-EXACT-125\|ERA-B-FIRST-BODY\|ERA-B-U1\|REFUSAL-VERSIONS\|AUTO-ERA-A\|AUTO-ERA-B\|AUTO-PROBE-FAIL' .ufo/waves/round-93/before/controls/do-nothing-battery-r92.py` = **0**.
- Rosters: r92 89 families, r93 96; set difference exactly `{ERA-EXACT-125, ERA-B-FIRST-BODY, ERA-B-U1,
  REFUSAL-VERSIONS, AUTO-ERA-A, AUTO-ERA-B, AUTO-PROBE-FAIL}`; nothing in r92 is missing from r93; no
  duplicates in either.
- Run against the landed gate: **89/89 `met`**, rc 0, 356 cases, 0 error rows.
- Reading: the pre-change instrument cannot reach the target — it never constructs any of the seven target
  families, yet reads `met` on the landed gate. Its met verdict certifies only the 89 inherited families; a
  roster that does not sample a clause cannot fail on it.

## 3. The bends are valid one-clause gates

- `python3 -m py_compile` OK for all six. Compiled from scratch copies (`bends-copy/`) so the frozen `bends/`
  directory received no `__pycache__` write (its pre-existing cache mtime remains 03:03:20, before this seat).
- Manifest hashes of the six bends verify, so these are the frozen bytes.
- `diff -u tools/check-limine-pins.py <bend>`: exactly one hunk per bend, one clause each (full `diffs.txt` in
  receipts). Hunks:

N01-exact-split (`@@ -186,7 +186,7 @@`):
```
     version = parse_limine_version(limine_version)
     if version is None:
         raise ValueError("bad limine version: %r" % (limine_version,))
-    era_b = version >= VISIBILITY_ERA_SPLIT
+    era_b = version > VISIBILITY_ERA_SPLIT  # N01: one V2 clause bent
     try:
         with open(conf, "rb") as f:
             text = f.read().decode("utf-8", "surrogateescape")
```

N02-first-body (`@@ -218,7 +218,7 @@`):
```
     for lineno, raw in enumerate(lines, 1):
         stripped = raw.replace("\r", "").strip(" \t")
         if stripped.startswith("/"):
-            if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
+            if first_entry is not None and lineno == first_entry + 1 and (era_b or first_entry != 1):  # N02
                 in_global = False
             entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry
             body = {}
```

N03-era-b-u1 (`@@ -245,6 +245,8 @@`):
```
     # unverified_image_lines. It changes no pin verdict.
     unverified = []
     for img_ln in sorted(image_lines):
+        if era_b and first_entry is not None and img_ln > first_entry:
+            continue  # N03: one U1 clause bent
         kv = split_key(lines[img_ln - 1])
         if kv is None:
             continue
```

N04-accept-any (`@@ -508,7 +508,7 @@`):
```
                   file=sys.stderr)
             return 64
         version, version_source = probed, "probe"
-    if parse_limine_version(version) is None:
+    if False:  # N04: the version refusal is deleted
         ap.print_usage(sys.stderr)
         print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
         return 64
```

N05-auto-ignore (`@@ -186,7 +186,7 @@`):
```
     version = parse_limine_version(limine_version)
     if version is None:
         raise ValueError("bad limine version: %r" % (limine_version,))
-    era_b = version >= VISIBILITY_ERA_SPLIT
+    era_b = version >= VISIBILITY_ERA_SPLIT and limine_version_source != "probe"  # N05
     try:
         with open(conf, "rb") as f:
             text = f.read().decode("utf-8", "surrogateescape")
```

N06-auto-fallback (`@@ -503,10 +503,7 @@`):
```
     if version == "auto":
         probed = probe_limine_version()
         if probed is None:
-            ap.print_usage(sys.stderr)
-            print("check-limine-pins: --limine-version auto: `limine --version` probe failed",
-                  file=sys.stderr)
-            return 64
+            probed = "12.9.4"  # N06: one V3 clause bent
         version, version_source = probed, "probe"
     if parse_limine_version(version) is None:
         ap.print_usage(sys.stderr)
```

## Receipts

`w1/ExecBends/` (all sha256 in `SHA256SUMS`, verified after copy): `N01…N06 .json/.out/.rc`,
`do-nothing-gate .json/.out/.rc`, `do-nothing-battery .json/.out/.rc`, `summary.json` (compact readings +
clause samples + roster set difference), `diffs.txt`, `compile.txt`, `freeze-check.txt`. Scratch
`/fast/scratch/hyaku/tsukuroi-r93/ExecBends` removed at exit. No lane writes outside `w1/ExecBends/` and this
report; no git/jj mutation; no `sudo`, boot, pacman, limine, efibootmgr or objcopy.

## Tooling

No install or upgrade was needed or performed (Python 3.14.8, bubblewrap 0.13.1 already present); no pacman
was run (host transactions paused).

## Verdict

**C1 (depth) bend half supported:** N01→`ERA-EXACT-125`, N02→`ERA-B-FIRST-BODY`, N03→`ERA-B-U1`,
N04→`REFUSAL-VERSIONS`; each reads `unmet` with its named family at 0/4 and **0 error rows** in this independent
canonical x1 run, matching the primary x3 summaries byte-for-byte in family counts. **C2 (operability) auto
half supported:** N05→`AUTO-ERA-B` (probe recorded, era not selected) and N06→`AUTO-PROBE-FAIL` (rc 0/878 B
instead of rc 64/empty), each 0/4, 0 error rows. **Do-nothing reachability supported:** the r92 gate fails
`AUTO-ERA-A`/`AUTO-ERA-B`, and the r92 battery (89 families, 0 occurrences of the seven new names) reads
`89/89 met` on the landed gate without sampling the target. **Falsified:** the seat-card do-nothing control
sentence that all three AUTO families fail on the r92 gate — `AUTO-PROBE-FAIL` passes 4/4 by refusal-shape
coincidence (rc 64 / 0 B stdout); Amendment A1 already narrows this and does not change C2's predicate, target
or kill. **Flagged:** `.ufo/plans/round-93.md` differs from the freeze manifest solely by that post-freeze
amendment; executable instruments all verify. Receipts: `w1/ExecBends/summary.json`, per-run JSONs,
`diffs.txt`, `compile.txt`, `freeze-check.txt`.
