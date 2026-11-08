# ExecBend — round 97 w1: the two one-clause bends N05 / N06

Seat: `ExecBend`. Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch `/fast/scratch/hyaku/tsukuroi-r97/ExecBend` — deleted before yield (verified absent).
Tooling: no installs, no upgrades. `python3 3.14.8` (system), `git` (system). Nothing added to any PATH dir.
No mutating git/jj command was run in the lane; the only repository created was a `git clone --shared`
under scratch, and no commit was made anywhere (`git -C <clone> rev-parse --show-toplevel` printed
`/fast/scratch/hyaku/tsukuroi-r97/ExecBend/clone` before use).

Axes named: depth (C1), freshness (C2). This seat measures **C1 depth** only — the discrimination
of the two new families by their own one-clause bends, in two layouts.

## 1. Instrument freeze

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-97/before/instruments.sha256
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

20/20 OK, 0 FAILED. **PASS** — the measurement below is taken with the frozen instrument bytes.

Bend file hashes, explicitly against the manifest lines 14-15:

```
$ sha256sum .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py \
             .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py
8a570b3a3c2966bdc14181322ab5a83165db877aeefd219cef8a579c07e60f57  .../bends/N05-z-cap-8.py
f89f9967ad92694d20206bd328643e7725cebaf1c4613c49aaeaf5faf27ad7ad  .../bends/N06-leading-zero-reject.py
```

Expected (manifest): `8a570b3a…e60f57` and `f89f9967…ad7ad`. **PASS** for both, byte-for-byte.

## 2. Exactly one clause per bend

```
$ diff -u tools/check-limine-pins.py .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py
@@ -96,7 +96,7 @@
     parts = text.split(".")
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (len(p) <= 8 or p is not parts[2])) for p in parts):  # N05 (Z bound bent to <=8)
         return None
N05 diff rc=1  (differences exist, as expected)

$ diff -u tools/check-limine-pins.py .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py
@@ -96,7 +96,7 @@
     parts = text.split(".")
-    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):
+    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 and (len(p) == 1 or p[0] != "0") for p in parts):  # N06 (leading zeros refused)
         return None
N06 diff rc=1
```

Both diffs are **one hunk of one removed line / one added line** in the single helper that parses
`--limine-version`; no other line of the gate changes. **PASS** — single-clause hunk each.

N05 bends the cap on the third component only (`len(p) <= 9` kept globally, `<= 8` when `p is parts[2]`).
N06 refuses any multi-digit component whose first character is `0` (`len(p) == 1 or p[0] != "0"`).

## 3. Battery runs — canonical layout

Commands (lane root cwd):

```
python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py \
  --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBend/N05-z-cap-8-canonical \
  --json .ufo/waves/round-97/w1/ExecBend/c1-bend-N05-z-cap-8-canonical.json
rc=1
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
```

```
python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py \
  --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBend/N06-leading-zero-reject-canonical \
  --json .ufo/waves/round-97/w1/ExecBend/c1-bend-N06-leading-zero-reject-canonical.json
rc=1
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
```

## 4. Battery runs — clone layout

```
$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r97/ExecBend/clone
$ git -C /fast/scratch/hyaku/tsukuroi-r97/ExecBend/clone rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r97/ExecBend/clone
$ ls <clone>/.ufo/waves/round-97/before/controls/bends/
N05-z-cap-8.py
N06-leading-zero-reject.py
$ ls <clone>/tools/limine-pin-battery-r97.py
/fast/scratch/hyaku/tsukuroi-r97/ExecBend/clone/tools/limine-pin-battery-r97.py
```

Run from the clone root with the clone's own battery and gate paths:

```
python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py \
  --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBend/N05-z-cap-8-clone \
  --json .ufo/waves/round-97/w1/ExecBend/c1-bend-N05-z-cap-8-clone.json
rc=1
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
families_passed 103/105 verdict unmet failed LEADING-ZERO-NORMALIZE,REFUSAL-VERSIONS-9DIGIT-Z
```

```
python3 tools/limine-pin-battery-r97.py --gate .ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py \
  --runs 3 --work /fast/scratch/hyaku/tsukuroi-r97/ExecBend/N06-leading-zero-reject-clone \
  --json .ufo/waves/round-97/w1/ExecBend/c1-bend-N06-leading-zero-reject-clone.json
rc=1
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
families_passed 104/105 verdict unmet failed LEADING-ZERO-NORMALIZE
```

## 5. Parsed receipts (count-runs.py) + error-row census

```
python3 .ufo/waves/round-95/before/controls/count-runs.py <receipt> \
  --family REFUSAL-VERSIONS-9DIGIT-Z --family LEADING-ZERO-NORMALIZE
```

All four receipts parse identically to the frozen C1 target. Every run reads `cases 420`,
`families_total 105`, and the `named` map shows the ordinal split `[a, b]` = (passed, failed):
N05 `REFUSAL-VERSIONS-9DIGIT-Z` `[0,4]` and `LEADING-ZERO-NORMALIZE` `[2,2]`; N06
`REFUSAL-VERSIONS-9DIGIT-Z` `[4,0]` and `LEADING-ZERO-NORMALIZE` `[0,4]`.

Per-run scan of every `case_log` row with a non-null `error` (own scan over the four receipts):

| receipt | run | families_passed | failed_families | error_rows | non-null error classes |
|---|---|---|---|---|---|
| N05 canonical | 0,1,2 | 103/105 | `["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]` | 6 | 4× REFUSAL-VERSIONS-9DIGIT-Z, 2× LEADING-ZERO-NORMALIZE |
| N06 canonical | 0,1,2 | 104/105 | `["LEADING-ZERO-NORMALIZE"]` | 4 | 4× LEADING-ZERO-NORMALIZE |
| N05 clone | 0,1,2 | 103/105 | `["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]` | 6 | 4× REFUSAL-VERSIONS-9DIGIT-Z, 2× LEADING-ZERO-NORMALIZE |
| N06 clone | 0,1,2 | 104/105 | `["LEADING-ZERO-NORMALIZE"]` | 4 | 4× LEADING-ZERO-NORMALIZE |

Raw `error` text, byte-identical on all 60 non-null rows (one string, newlines shown as `\n`):

```
bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h] [--conf CONF] [--esp ESP] [--secure-boot-enforced {0,1}]\n               [--tpm-present {0,1}] [--limine-version LIMINE_VERSION]\n               [--live] [--selftest]\ncheck-limine-pins: --limine-version must be X.Y.Z or auto\n
```

That is the bend's own refusal (`rc=64`, argparse rejecting a version string the bent parser
returns `None` for), exactly the class the freeze names (`bad-output: JSONDecodeError rc=64`) — the
bends refuse, so these rows are expected and are counted, not required zero. The `family` field is
non-null on every one of them; there is no unclassified row.

## PASS/FAIL per expected line

| expectation (claims.json C1 target) | measured | verdict |
|---|---|---|
| N05 canonical `failed_families` exactly `["LEADING-ZERO-NORMALIZE","REFUSAL-VERSIONS-9DIGIT-Z"]`, 3/3 runs | exact, 3/3 | **PASS** |
| N05 canonical `103/105` in each of 3 runs | 103/105 ×3 | **PASS** |
| N05 canonical exactly 6 non-null error rows/run (4 Z + 2 leading-zero) | 6/run, 4+2 | **PASS** |
| N05 clone: same family set, 103/105, 6 rows/run | exact, 3/3 | **PASS** |
| N06 canonical `failed_families` exactly `["LEADING-ZERO-NORMALIZE"]`, 3/3 | exact, 3/3 | **PASS** |
| N06 canonical `104/105` in each of 3 runs | 104/105 ×3 | **PASS** |
| N06 canonical exactly 4 non-null error rows/run | 4/run | **PASS** |
| N06 clone: same family set, 104/105, 4 rows/run | exact, 3/3 | **PASS** |
| error class is the bend's own rc-64 refusal | `JSONDecodeError rc=64`, argparse usage, 60/60 | **PASS** |
| N05 is a single-clause hunk | one hunk, one line swapped | **PASS** |
| N06 is a single-clause hunk | one hunk, one line swapped | **PASS** |
| both bend bytes match the freeze manifest | `8a570b3a…`, `f89f9967…` | **PASS** |
| instrument manifest verifies before measuring | 20 OK, 0 FAILED | **PASS** |
| no bend fails a family outside the frozen set | none observed | **PASS** |

**No finding against C1.** Neither bend fails a family outside its frozen set; each diff is a
single-clause hunk; the two layouts agree run-for-run.

## Receipts (written by this seat, under the seat dir)

- `.ufo/waves/round-97/w1/ExecBend/c1-bend-N05-z-cap-8-canonical.json` (740134 B)
- `.ufo/waves/round-97/w1/ExecBend/c1-bend-N06-leading-zero-reject-canonical.json` (739581 B)
- `.ufo/waves/round-97/w1/ExecBend/c1-bend-N05-z-cap-8-clone.json` (740192 B)
- `.ufo/waves/round-97/w1/ExecBend/c1-bend-N06-leading-zero-reject-clone.json` (739189 B)
- this report

## Observation routed to L1 — RESOLVED as amendment A1 (L1 adjudication, 08:5x)

The drift below is **explained and pinned by the L1**, not a sibling-lane write: the C2 fixture *recipe*
`before/fixtures/build-doctored-fixture.sh` was corrected **by the L1** after the freeze (08:52) to pin its
clone base to the pre-round tip `f48d1642` (a clone of post-freeze `master` reads `tools_total 157`
against a 154-row table, so the blindness leg returned the coverage gate's own `REGISTRY-ROW-MISSING`
FAIL instead of `PASS 154/154`). Corrected bytes `e4cf82a0…` (was `c2ecf729…`). The corrected set is
pinned in `before/instruments-r97-after-fixture-pin.sha256` (20/20 OK) and C2's void clause is evaluated
on that file, with A1 in `before/plan-amendments-r97.md` as the narrowing pointer. The four scoring
instruments, both bends and the three do-nothing copies are unchanged from the original freeze, so
**this seat's measurement stands as taken**. The `before/dev/` modifications are the L1's own do-nothing
receipts completing after the commit and the fixture re-run rewriting its receipts.

Original raw observation (kept for the record):

At the **start** of this seat (08:49 local) `sha256sum -c .ufo/waves/round-97/before/instruments.sha256`
printed **20 OK, 0 FAILED**; the measurement above was taken on those bytes. A re-check after the last
run printed:

```
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match
```

Evidence collected read-only:

```
manifest line: c2ecf729a68078c0f39642ae04c3cc038cded206a6ff334cf32ffa3142677641  .../fixtures/build-doctored-fixture.sh
actual now:    e4cf82a0f4c6307e057fd0b75c7bcadb21eb6c972859cd3ba1c837eccc74081f
mtime:         2026-11-08 08:52:21 -0300   (size 5686)
git HEAD blob: c2ecf729a68078c0f39642ae04c3cc038cded206a6ff334cf32ffa3142677641   -> the frozen bytes are intact in HEAD
git status --porcelain -- .ufo/waves/round-97/before/
 M .ufo/waves/round-97/before/dev/c1-dn-bend-N05-z-cap-8.txt
 M .ufo/waves/round-97/before/dev/c2-content-doctored.json
 M .ufo/waves/round-97/before/dev/c2-coverage-doctored.json
 M .ufo/waves/round-97/before/dev/c2-nonancestor.txt
 M .ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh
 M .ufo/waves/round-97/before/fixtures/doctored-revision.txt
?? .ufo/waves/round-97/before/dev/c1-dn-bend-N05-z-cap-8.json
?? .ufo/waves/round-97/before/dev/c1-dn-bend-N06-leading-zero-reject.json
?? .ufo/waves/round-97/before/dev/c1-dn-bend-N06-leading-zero-reject.txt
?? .ufo/waves/round-97/before/fixtures/doctored-checker.sha256
```

The mutation is dated 08:52:21, i.e. **after** all four of this seat's battery runs (08:50–08:51) and
after the manifest verified. It is confined to the C2 doctored-fixture script and C2 `dev/` receipts;
**none of my four legs read that file**. The four instruments my legs did read still hash to the
freeze right now:

```
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8  tools/limine-pin-battery-r97.py
8a570b3a3c2966bdc14181322ab5a83165db877aeefd219cef8a579c07e60f57  .../bends/N05-z-cap-8.py
f89f9967ad92694d20206bd328643e7725cebaf1c4613c49aaeaf5faf27ad7ad  .../bends/N06-leading-zero-reject.py
```

I did **not** restore, revert or touch it: `before/` is outside my write scope and fixing it would be a
write to a frozen artifact. Routed to the L1 (`agent://TsukuroiR97`) as a scoring-time hazard: while the
working-tree manifest is dirty, the round's void clause ("void if any instrument byte differs from
`.ufo/waves/round-97/before/instruments.sha256` at scoring time") is live for every seat. HEAD bytes
are clean, so a scoring read of the committed blob is unaffected.

## Risks / notes

- The seat measures the bends only. The landed-gate `105/105` leg and the r96 do-nothing blindness
  legs are other seats' assignments; nothing here is evidence about those.
- The `count-runs.py` process exited 1 while still printing complete JSON for both families on all
  four receipts (its nonzero exit is its own convention for a failed-verdict receipt, not a parse
  failure — the parsed body above is its full output). Recorded as observed; the instrument was not
  edited and no retry-to-pass was performed.
- Scratch `/fast/scratch/hyaku/tsukuroi-r97/ExecBend` (including the `git clone --shared` fixture)
  was removed after the last read; the receipts live only under the seat dir.
- No files outside `.ufo/waves/round-97/w1/ExecBend.md` and the seat-dir receipts were written.

{"seat":"ExecBend","verdict":"met","notes":"Both bends reproduce the frozen C1 target exactly in both layouts: N05 103/105 with failed_families [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z] and 6 non-null error rows/run (4+2), 3/3 runs canonical and in git clone --shared; N06 104/105 with failed_families [LEADING-ZERO-NORMALIZE] and 4 non-null error rows/run, 3/3 runs both layouts. Every non-null row is the bend's own bad-output: JSONDecodeError rc=64 refusal with a non-null family. Each bend is a single-clause one-hunk diff (N05 caps the third component at 8, N06 refuses multi-digit components starting with 0). Before measuring, sha256sum -c instruments.sha256 read 20 OK 0 FAILED; the four instruments my legs read still match the freeze. Routed observation (not a C1 finding): at 08:52:21, after my runs, a sibling changed before/fixtures/build-doctored-fixture.sh (worktree e4cf82a0 vs manifest c2ecf729; HEAD blob still c2ecf729), so the worktree manifest is dirty at scoring time for all seats; I did not touch before/."}
