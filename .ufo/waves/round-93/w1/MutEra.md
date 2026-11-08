# MutEra — round 93, wave w1: held-out mutants of V2 / U1 / refusal

Seat: `MutEra` (mutation tester). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; freeze commit
`c633f49aa512e1c8a0e0464b7fb5d354c70096cf`; host `linux 7.2.11-arch1-1`.

Axes named before the work: **(1) kill specificity** — does each of the four new families own a
clause nothing older owns; **(2) cut breadth** — how many physical lines one clause change moves;
**(3) cost** — one battery run per mutant, all mutant runs in parallel, one `--work` per run;
**(4) fidelity** — lane read-only, every mutant a COPY with an exact diff and hash, restoration by
non-modification.

Detector for every row (frozen, hashes below):

```
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r93.py --gate <COPY> --runs 1 \
        --work <own-dir> --json <own-dir>.json
```

Each run scores the literal 96-family roster × 4 cases = 384 cases through the r93 ISOLATION
launcher. Scratch: `/fast/scratch/hyaku/tsukuroi-r93/MutEra/` (removed after the receipts were
copied to this seat directory).

## Positive control (pristine bytes)

A byte-identical copy of the frozen gate (`sha256 6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa`,
same as the lane instrument) read:

```
families_passed 96/96 verdict met failed -
```

384 cases, **0 error rows**. A warning/error row count of 0 and 384/384 executed cases in every
run below is the baseline that makes a survivor a *detector* finding, not a broken fixture.

## Mutant table (16 one-clause mutants)

| Mutant | Clause changed (one clause each) | passed | failed families | verdict |
|---|---|---|---|---|
| M01 | era split at 12.9.4 (`VISIBILITY_ERA_SPLIT = (12, 9, 4)`) | 91/96 | `AUTO-ERA-A`, `ERA-DEFAULT`, `ERA-FLE-MEASURED-A`, `ERA-FLE-PANIC-A`, `FIRST-LINE-ENTRY` | **KILLED** (20 case rows) |
| M02 | era split at 12.9.6 (`VISIBILITY_ERA_SPLIT = (12, 9, 6)`) | 95/96 | `ERA-EXACT-125` | **KILLED** (4 case rows) |
| M03 | era split strict (`version > VISIBILITY_ERA_SPLIT`; 12.9.5 becomes era A) | 95/96 | `ERA-EXACT-125` | **KILLED** (4 case rows) |
| M04 | cut applied one line late (first body line still read as global) | 95/96 | `ERA-B-FIRST-BODY` | **KILLED** (4 case rows) |
| M05 | cut applied one line early (line before the first entry treated as body) | 76/96 | `ALL-PIN-KEYS`, `EMPTY-PIN-LIST`, `ERA-GLOBAL-KEY-A`, `ERA-GLOBAL-KEY-B`, `GLOBAL-VS-ENTRY`, `MEASURED-FIRST`, `MEASURED-GLOBAL-ONLY`, `MEASURED-TPM-ABSENT`, `MEASURED-TPM1`, `MULTI-FAULT`, `PANIC-FIRST`, `PANIC-GLOBAL-ONLY`, `PANIC-KEY-CASE`, `PANIC-METADATA`, `PANIC-NO-ONLY`, `PANIC-NON-NO`, `PANIC-RAW-DECOY`, `PANIC-VALUE-BLANKS`, `SB-FLAG-ZERO`, `SECUREBOOT` | **KILLED** (71 case rows) |
| M06 | first-line exception kept in era B (`first_entry != 1` only) | 91/96 | `AUTO-ERA-B`, `ERA-B-FIRST-BODY`, `ERA-EXACT-125`, `ERA-FLE-MEASURED-B`, `ERA-FLE-PANIC-B` | **KILLED** (20 case rows) |
| M07 | U1 computed on the global section only in era B (`img_ln >= first_entry` skipped) | 95/96 | `ERA-B-U1` | **KILLED** (4 case rows) |
| M08 | U1 computed on the global section only in both eras | 85/96 | `EMPTY-PIN-LIST`, `ERA-B-U1`, `FIRST-PATH`, `HOST-SHAPE`, `NO-PAREN`, `UNHASHED-DECOYS`, `UNVERIFIED-IMAGE`, `UNVERIFIED-IMAGE-PATH`, `UNVERIFIED-MIXED`, `UNVERIFIED-NON-EFI`, `UNVERIFIED-SORTED` | **KILLED** (44 case rows) |
| M09 | U1 skips image lines after the first entry | 88/96 | `EMPTY-PIN-LIST`, `FIRST-PATH`, `HOST-SHAPE`, `UNVERIFIED-IMAGE`, `UNVERIFIED-IMAGE-PATH`, `UNVERIFIED-MIXED`, `UNVERIFIED-NON-EFI`, `UNVERIFIED-SORTED` | **KILLED** (31 case rows) |
| M10 | refusal accepts `12.9` as 12.9.0 | 95/96 | `REFUSAL-VERSIONS` | **KILLED** (4 case rows) |
| M11 | refusal accepts `12.9.5.1` (4 components) | 95/96 | `REFUSAL-VERSIONS` | **KILLED** (4 case rows) |
| M12 | refusal accepts `""` as 12.9.4 | 95/96 | `REFUSAL-VERSIONS` | **KILLED** (4 case rows) |
| M13 | refusal accepts a 10-digit component (`len(p) <= 10`) | 96/96 | (none) | **SURVIVED** (0 failing cases) |
| M14 | refusal accepts a leading-space value (`text.strip()`) | 95/96 | `REFUSAL-VERSIONS` | **KILLED** (4 case rows) |
| M15 | refusal exits 1 instead of 64 | 95/96 | `REFUSAL-VERSIONS` | **KILLED** (4 case rows) |
| M16 | refusal prints a JSON verdict before exiting 64 | 95/96 | `REFUSAL-VERSIONS` | **KILLED** (4 case rows) |

All 16 mutants ran to completion (`cases 384/384`, `error_rows 0`, no timeouts); none is
inconclusive. 15 killed, 1 survived.

A second independent run of the two decisive rows (fresh random seed, separate `--work`,
`--runs 1`) reproduced both: **M02** `95/96 unmet, failed ERA-EXACT-125`; **M13** `96/96 met`.
So the M02 kill and the M13 survivor are stable, not a draw of one run's random fixtures
(`receipts/battery-results-run2.txt`).

### Which of the four new families does the killing

| New family (C1) | mutants it kills | uniquely? |
|---|---|---|
| `ERA-EXACT-125` | M02, M03 (also M06 together with 4 older era families) | **yes** for M02 and M03 — no other family moves |
| `ERA-B-FIRST-BODY` | M04 (also M06) | **yes** for M04 — the only family that fires |
| `ERA-B-U1` | M07 (also M08/M09 together with the r91 U1 families) | **yes** for M07 — the only family that fires |
| `REFUSAL-VERSIONS` | M10, M11, M12, M14, M15, M16 | **yes** for all six |

The two boundary directions are split across generations, which is what depth should look like:
a split moved **later** (M02) or made **strict** (M03) is caught only by `ERA-EXACT-125`; a split
moved **earlier** (M01, 12.9.4 → era B) is caught by the pre-existing era families
(`ERA-FLE-PANIC-A`, `ERA-FLE-MEASURED-A`, `ERA-DEFAULT`, `FIRST-LINE-ENTRY`, `AUTO-ERA-A`) — correct,
because the lower boundary was already pinned by the r92 roster.

Exact first failing row for the new-family kills (battery `case_log`; `want` → `got`):

- **M02** / `ERA-EXACT-125`: want [1, "DEGRADED", [[3, "LP-MISMATCH", "panic"], [7, "OK", "none"]], "menu"]; got [1, "DEGRADED", [[3, "LP-MISMATCH", "prompt"], [7, "OK", "none"]], 1, "menu", "12.9.5", "flag"]
- **M03** / `ERA-EXACT-125`: want [1, "DEGRADED", [[3, "LP-MISMATCH", "panic"], [7, "OK", "none"]], "menu"]; got [1, "DEGRADED", [[3, "LP-MISMATCH", "prompt"], [7, "OK", "none"]], 1, "menu", "12.9.5", "flag"]
- **M04** / `ERA-B-FIRST-BODY`: want [1, "DEGRADED", [[4, "LP-MISMATCH", "panic"], [7, "OK", "none"]], "menu"]; got [1, "DEGRADED", [[4, "LP-MISMATCH", "prompt"], [7, "OK", "none"]], 1, "menu", "12.9.6", "flag"]
- **M06** / `AUTO-ERA-B`: want [1, "DEGRADED", [[3, "LP-MISMATCH", "panic"], [7, "OK", "none"]], "menu"]; got [1, "DEGRADED", [[3, "LP-MISMATCH", "prompt"], [7, "OK", "none"]], 1, "menu", "12.9.6", "probe"]
- **M07** / `ERA-B-U1`: want [0, "HEALTHY", [[5, "OK", "none"]], "menu"]; got [0, "HEALTHY", [[5, "OK", "none"]], 0, "menu", "12.9.6", "flag"]
- **M10** / `REFUSAL-VERSIONS`: want rc64/empty-stdout; got '12.9' rc=0 stdout=342
- **M11** / `REFUSAL-VERSIONS`: want rc64/empty-stdout; got '12.9.5.1' rc=0 stdout=343
- **M12** / `REFUSAL-VERSIONS`: want rc64/empty-stdout; got '' rc=0 stdout=338
- **M14** / `REFUSAL-VERSIONS`: want rc64/empty-stdout; got ' 12.9.5' rc=0 stdout=342; '12.9.5 ' rc=0 stdout=342
- **M15** / `REFUSAL-VERSIONS`: want rc64/empty-stdout; got '12.9' rc=1 stdout=0; '12.9.5.1' rc=1 stdout=0; 'abc' rc=1 stdout=0; '' rc=1 stdout=0; ' 12.9.5' rc=1 stdout=0; '12.9.5 ' rc=1 stdout=0; '+12.9.5' rc=1 stdout=0; '12..5' rc=1 stdout=0; '12.9.5-rc1' rc=1 stdout=0; '99999999999999999999' rc=1 stdout=0
- **M16** / `REFUSAL-VERSIONS`: want rc64/empty-stdout; got '12.9' rc=64 stdout=45; '12.9.5.1' rc=64 stdout=45; 'abc' rc=64 stdout=45; '' rc=64 stdout=45; ' 12.9.5' rc=64 stdout=45; '12.9.5 ' rc=64 stdout=45; '+12.9.5' rc=64 stdout=45; '12..5' rc=64 stdout=45; '12.9.5-rc1' rc=64 stdout=45; '99999999999999999999' rc=64 stdout=45

`ERA-B-U1`'s kill is not visible in the pin tuple; reproduced directly on the family's shape
(header, `12.9.6`, efi entry, unhashed image line, then a good pin):

```
pristine  rc=0 unverified_image_lines=[5] era=12.9.5+
M07       rc=0 unverified_image_lines=[]  era=12.9.5+   (U1 restricted to the pre-cut section)
M08       rc=0 unverified_image_lines=[]  era=12.9.5+   (U1 restricted to the pre-cut section)
```

## Survivor: M13 — the 9-digit component bound is unobserved

Clause: `len(p) <= 9` → `len(p) <= 10` in `parse_limine_version`. Battery result:
`families_passed 96/96 verdict met`, 384 cases, 0 error rows — **SURVIVED**. This is **not
equivalent**; the clause is observable and the mutant changes the gate's answer:

```
pristine  --limine-version 1234567890.9.5  -> rc 64, stdout 0 bytes   (refused, per contract)
M13       --limine-version 1234567890.9.5  -> rc 0, JSON HEALTHY, limine_version "1234567890.9.5",
                                              visibility_era "12.9.5+", stdout 813 bytes
```

`parse_limine_version`'s docstring fixes the contract at **1-9 digits per component**; a value the
contract refuses is answered with a verdict. **Coverage gap**, not an equivalence.

Which family would have to change: **`REFUSAL-VERSIONS`** (battery line 1621). Its finite set
contains `"9" * 5000 + ".0.0"`, which exercises the *existence* of the cap (without it `int()`
would raise) but not the 9-vs-10-digit **boundary**. Add one row with a component of exactly ten
digits, e.g. `"1234567890.9.5"`; keep a nine-digit sibling (`"123456789.9.5"` accepted, rc 0) to
pin the other side of the boundary. `usage_check`'s case list carries the same hole (it also has
only the 5000-digit row) but is outside `run_battery`'s score.

## Exact bytes changed (one hunk per mutant, from the frozen source)

### M01
```diff
--- check-limine-pins.py
+++ M01.py
@@ -98,7 +98,7 @@
     return tuple(int(p) for p in parts)
 
 
-VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut
+VISIBILITY_ERA_SPLIT = (12, 9, 4)   # M01: split one release early
 
 
 def probe_limine_version(executable="limine"):
```
### M02
```diff
--- check-limine-pins.py
+++ M02.py
@@ -98,7 +98,7 @@
     return tuple(int(p) for p in parts)
 
 
-VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut
+VISIBILITY_ERA_SPLIT = (12, 9, 6)   # M02: split one release late
 
 
 def probe_limine_version(executable="limine"):
```
### M03
```diff
--- check-limine-pins.py
+++ M03.py
@@ -186,7 +186,7 @@
     version = parse_limine_version(limine_version)
     if version is None:
         raise ValueError("bad limine version: %r" % (limine_version,))
-    era_b = version >= VISIBILITY_ERA_SPLIT
+    era_b = version > VISIBILITY_ERA_SPLIT   # M03: strict comparison
     try:
         with open(conf, "rb") as f:
             text = f.read().decode("utf-8", "surrogateescape")
```
### M04
```diff
--- check-limine-pins.py
+++ M04.py
@@ -215,11 +215,12 @@
             first_entry = i
             break
     in_global = True
+    cut_pending = False   # M04
     for lineno, raw in enumerate(lines, 1):
         stripped = raw.replace("\r", "").strip(" \t")
         if stripped.startswith("/"):
             if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
-                in_global = False
+                cut_pending = True   # M04: cut after the next key line
             entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry
             body = {}
             bodies.append(body)
@@ -238,6 +239,9 @@
             uri = parse_uri(value)
             if uri is not None:
                 raw_pins.append((lineno, key, written, entry, value, uri))
+        if cut_pending:
+            in_global = False   # M04: the first body line was still read as global
+            cut_pending = False
     image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}
     image_lines.discard(None)
     # U1 (r91): an image line whose value Limine still uri_opens but which is not a parseable pin
```
### M05
```diff
--- check-limine-pins.py
+++ M05.py
@@ -217,6 +217,8 @@
     in_global = True
     for lineno, raw in enumerate(lines, 1):
         stripped = raw.replace("\r", "").strip(" \t")
+        if first_entry is not None and lineno == first_entry - 1:
+            in_global = False   # M05: last global line treated as body
         if stripped.startswith("/"):
             if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
                 in_global = False
```
### M06
```diff
--- check-limine-pins.py
+++ M06.py
@@ -218,7 +218,7 @@
     for lineno, raw in enumerate(lines, 1):
         stripped = raw.replace("\r", "").strip(" \t")
         if stripped.startswith("/"):
-            if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
+            if first_entry is not None and lineno == first_entry and (first_entry != 1):   # M06
                 in_global = False
             entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry
             body = {}
```
### M07
```diff
--- check-limine-pins.py
+++ M07.py
@@ -245,6 +245,8 @@
     # unverified_image_lines. It changes no pin verdict.
     unverified = []
     for img_ln in sorted(image_lines):
+        if era_b and first_entry is not None and img_ln >= first_entry:
+            continue   # M07: U1 sees the global section only in era B
         kv = split_key(lines[img_ln - 1])
         if kv is None:
             continue
```
### M08
```diff
--- check-limine-pins.py
+++ M08.py
@@ -245,6 +245,8 @@
     # unverified_image_lines. It changes no pin verdict.
     unverified = []
     for img_ln in sorted(image_lines):
+        if first_entry is not None and img_ln >= first_entry:
+            continue   # M08: U1 sees the global section only
         kv = split_key(lines[img_ln - 1])
         if kv is None:
             continue
```
### M09
```diff
--- check-limine-pins.py
+++ M09.py
@@ -245,6 +245,10 @@
     # unverified_image_lines. It changes no pin verdict.
     unverified = []
     for img_ln in sorted(image_lines):
+        if first_entry is not None and sum(
+                1 for r in lines[:img_ln - 1]
+                if r.replace("\r", "").strip(" \t").startswith("/")) > 1:
+            continue   # M09: only the first entry is considered
         kv = split_key(lines[img_ln - 1])
         if kv is None:
             continue
```
### M10
```diff
--- check-limine-pins.py
+++ M10.py
@@ -93,6 +93,8 @@
     if not isinstance(text, str):
         return None
     parts = text.split(".")
+    if len(parts) == 2:
+        parts = parts + ["0"]   # M10: X.Y means X.Y.0
     if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
         return None
     return tuple(int(p) for p in parts)
```
### M11
```diff
--- check-limine-pins.py
+++ M11.py
@@ -93,7 +93,7 @@
     if not isinstance(text, str):
         return None
     parts = text.split(".")
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) not in (3, 4) or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):   # M11
         return None
     return tuple(int(p) for p in parts)
 
```
### M12
```diff
--- check-limine-pins.py
+++ M12.py
@@ -92,6 +92,8 @@
     raises above 4300 digits (round-92 ReviewGate F1)."""
     if not isinstance(text, str):
         return None
+    if text == "":
+        return (12, 9, 4)   # M12: empty value silently means the host default
     parts = text.split(".")
     if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
         return None
```
### M13
```diff
--- check-limine-pins.py
+++ M13.py
@@ -93,7 +93,7 @@
     if not isinstance(text, str):
         return None
     parts = text.split(".")
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 10 for p in parts):   # M13
         return None
     return tuple(int(p) for p in parts)
 
```
### M14
```diff
--- check-limine-pins.py
+++ M14.py
@@ -92,6 +92,7 @@
     raises above 4300 digits (round-92 ReviewGate F1)."""
     if not isinstance(text, str):
         return None
+    text = text.strip()   # M14: surrounding blanks accepted
     parts = text.split(".")
     if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
         return None
```
### M15
```diff
--- check-limine-pins.py
+++ M15.py
@@ -511,7 +511,7 @@
     if parse_limine_version(version) is None:
         ap.print_usage(sys.stderr)
         print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
-        return 64
+        return 1   # M15
     tpm = None if a.tpm_present is None else a.tpm_present == "1"
     if a.live:
         conf, esp = a.conf or "/boot/limine.conf", a.esp or "/boot"
```
### M16
```diff
--- check-limine-pins.py
+++ M16.py
@@ -511,6 +511,7 @@
     if parse_limine_version(version) is None:
         ap.print_usage(sys.stderr)
         print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
+        print(json.dumps({"verdict": "HEALTHY", "rc": 64, "pins": []}))   # M16
         return 64
     tpm = None if a.tpm_present is None else a.tpm_present == "1"
     if a.live:
```
## Lane integrity and restoration evidence

I never wrote the lane instrument; every mutant is a copy under scratch, and the copies were
removed with the scratch tree after the receipts below were written. Before **and** after all
19 battery runs (17 first pass + 2 repeat):

```
lane gate    6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa  (before = after)
lane battery ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad  (before = after)
pristine copy 6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa (before = after)
```

Per-mutant sha256: `receipts/hashes.txt`; per-mutant diffs and full mutant sources:
`receipts/M01.py … M16.py` and `receipts/M01.diff … M16.diff`; battery summaries and the parsed
`case_log` digest: `receipts/summary.json`; raw one-line verdicts: `receipts/battery-results.txt`;
the deterministic generator that rebuilds every mutant from the frozen bytes:
`receipts/make_mutants.py`.

`sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` from the lane root (14 lines):
**13 lines OK**; the only **FAILED** line is `.ufo/plans/round-93.md` — the other 13 are the gate,
the battery, `make-r93-bends.py`, the six bends, `count-runs.py`, both do-nothing controls and
`claims.json`. The plan line fails because the working tree carries *Amendment A1* (14 appended
lines, `git diff --stat` = `14 insertions(+)`,
current sha256 `3668f0e8d264142b9e314c48cdcc156742777f872391bf88e1fb02d0eb049c87` vs the frozen
`4600cfa32563d267ca2ded47168e55b63f4d2c60e4b11aadfb87ecb706d28002`, `git status` = ` M`). The plan's
own convention is "Amendments (appended after data; never an in-place rewrite)", so this is the
sanctioned post-freeze amendment, not instrument drift — but it makes the bare `sha256sum -c`
exit non-zero, so a reviewer running that command must expect exactly this one FAILED line.

## Verdict

**Supports C1 (depth).** The four r93 families are non-vacuous and each owns a clause the r92
roster does not: `ERA-EXACT-125` is the sole killer of the later split (M02) and the strict split
(M03); `ERA-B-FIRST-BODY` is the sole killer of the cut-one-line-late mutant (M04);
`ERA-B-U1` is the sole killer of U1-restricted-to-the-global-section-in-era-B (M07); and
`REFUSAL-VERSIONS` is the sole killer of six refusal mutants (accept `12.9`, accept `12.9.5.1`,
accept `""`, accept surrounding blanks, rc 1 instead of 64, JSON verdict before 64). The landed
gate's 96/96 is reproduced on pristine bytes as my positive control (1 run, 384 cases, 0 error
rows).

**One coverage boundary remains (coverage finding, not a contract change):** the 9-digit
component cap (M13) survives the whole battery; `REFUSAL-VERSIONS` must add a ten-digit component
row. This does not falsify any clause C1 states — every enumerated REFUSAL-VERSIONS value kills —
and it does not touch C2.

Receipts: `.ufo/waves/round-93/w1/MutEra/receipts/` (summary.json, battery-results.txt,
M01–M16 .py/.diff, make_mutants.py, hashes.txt).
