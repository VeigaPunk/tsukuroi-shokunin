# ExecBends — round 99 w1: N09-y-era and N11-x-era one-clause bends (C1 depth)

Seat `ExecBends`. Axes named: **depth** (C1 — the X/Y accepted-cap families now assert echo+era) and **freshness** (C2 — checker capture/selftest), re-read from `claims.json:5-30` and `.ufo/plans/round-99.md:20-74`. This seat measures **only** the two C1 bends the target names; C2 is outside this seat and no C2 receipt is cited here. All numbers below were produced by the commands shown, in this seat, on the pinned bytes.

## 1. Instruments (before any measurement)

Lane cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Scratch `/fast/scratch/hyaku/tsukuroi-r99/ExecBends` (deleted at the end of this seat). Seat receipts dir `.ufo/waves/round-99/w1/ExecBends/`.

```bash
sha256sum .ufo/waves/round-99/before/controls/bends/N09-y-era.py \
          .ufo/waves/round-99/before/controls/bends/N11-x-era.py \
          tools/limine-pin-battery-r99.py tools/check-limine-pins.py | tee $SD/sha.txt
sha256sum -c .ufo/waves/round-99/before/instruments.sha256 > $SD/instruments-check.txt 2>&1; echo "manifest rc=$?" >> $SD/instruments-check.txt
```

Observed (`sha.txt`): N09 `22c3449fac4257c0045e733c5c9fcae899e74ecc973c02a4729f46d3f8cefdf7`, N11 `28392f3bb1c7912ff00ce9a7bbf3cdb27f9acfeab2dfbd5ff2ca9a397f5a4752`, battery `c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99`, gate `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32`. Manifest `sha256sum -c` → every one of the 16 lines `OK`, `manifest rc=0` (`instruments-check.txt`). Both bend digests equal `instruments.sha256:12-13`; the gate equals `instruments.sha256:4` (unchanged this round).

## 2. Canonical layout — commands and raw output

```bash
python3 tools/limine-pin-battery-r99.py \
  --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r99/ExecBends/N09-canonical \
  --json .ufo/waves/round-99/w1/ExecBends/c1-bend-N09-y-era-canonical.json > $SD/run-N09-canonical.log 2>&1; echo "rc=$?" >> …
python3 tools/limine-pin-battery-r99.py \
  --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r99/ExecBends/N11-canonical \
  --json .ufo/waves/round-99/w1/ExecBends/c1-bend-N11-x-era-canonical.json > $SD/run-N11-canonical.log 2>&1; echo "rc=$?" >> …
```

`run-N09-canonical.log` (raw, trimmed to the run lines):

```
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
rc=1
```

`run-N11-canonical.log` (raw, trimmed):

```
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT
rc=1
```

## 3. Clone layout — commands and raw output

```bash
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  /fast/scratch/hyaku/tsukuroi-r99/ExecBends/clone
git -C /fast/scratch/hyaku/tsukuroi-r99/ExecBends/clone rev-parse --show-toplevel HEAD   # → clone path, f107da3afe511f7db8cdc30235a992b774903158
mkdir -p clone/.ufo/waves/round-99/before/controls/bends
cp tools/limine-pin-battery-r99.py clone/tools/limine-pin-battery-r99.py
cp .ufo/waves/round-99/before/controls/bends/{N09-y-era.py,N11-x-era.py} clone/.ufo/waves/round-99/before/controls/bends/
cd /fast/scratch/hyaku/tsukuroi-r99/ExecBends/clone
python3 tools/limine-pin-battery-r99.py \
  --gate .ufo/waves/round-99/before/controls/bends/N09-y-era.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r99/ExecBends/N09-clone \
  --json $SD/c1-bend-N09-y-era-clone.json > $SD/run-N09-clone.log 2>&1
python3 tools/limine-pin-battery-r99.py \
  --gate .ufo/waves/round-99/before/controls/bends/N11-x-era.py --runs 3 \
  --work /fast/scratch/hyaku/tsukuroi-r99/ExecBends/N11-clone \
  --json $SD/c1-bend-N11-x-era-clone.json > $SD/run-N11-clone.log 2>&1
```

Clone identity (`clone-identity.txt`): toplevel `/fast/scratch/hyaku/tsukuroi-r99/ExecBends/clone`, HEAD `f107da3afe511f7db8cdc30235a992b774903158`. The round-99 freeze is uncommitted at that HEAD (`git status --porcelain` shows `.ufo/waves/round-99/` and `tools/*-r99.py` untracked), so the clone's copy of the r99 battery and the two bends was **copied from the lane tree** into the clone; no commit was made. Their digests in the clone (`clone-sha.txt`) are byte-identical to the canonical ones (N09 `22c3449f…`, N11 `28392f3b…`, battery `c2e8c8fc…`), and the clone's own committed gate is `7d79ac29…` (`clone/tools/check-limine-pins.py`), i.e. the clone leg runs the clone's gate bytes and the clone's battery bytes.

`run-N09-clone.log` (raw, trimmed):

```
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
families_passed 104/105 verdict unmet failed REFUSAL-VERSIONS-9DIGIT-Y
rc=1
```

`run-N11-clone.log` (raw, trimmed):

```
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT
families_passed 103/105 verdict unmet failed EXPLICIT-VERSION-ERA,REFUSAL-VERSIONS-9DIGIT
rc=1
```

## 4. Counts (count-runs.py, three cap families named)

```bash
for f in c1-bend-N09-y-era-canonical c1-bend-N09-y-era-clone \
         c1-bend-N11-x-era-canonical c1-bend-N11-x-era-clone; do
  python3 .ufo/waves/round-95/before/controls/count-runs.py \
    .ufo/waves/round-99/w1/ExecBends/$f.json \
    --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y \
    --family REFUSAL-VERSIONS-9DIGIT-Z > $SD/count-$f.txt 2>&1
done
```

All four count commands exit `rc=1` (expected: every run is `unmet`; count-runs.py exits 0 only when all runs are `met`).

| bend / layout | run | verdict | families | failed_families (instrument order) | cases | error_rows | named passed/failed |
|---|---|---|---|---|---|---|---|
| N09 canonical | 1 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 420 | 0 | X 4/0, Y 0/4, Z 4/0 |
| N09 canonical | 2 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 420 | 0 | X 4/0, Y 0/4, Z 4/0 |
| N09 canonical | 3 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 420 | 0 | X 4/0, Y 0/4, Z 4/0 |
| N09 clone | 1 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 420 | 0 | X 4/0, Y 0/4, Z 4/0 |
| N09 clone | 2 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 420 | 0 | X 4/0, Y 0/4, Z 4/0 |
| N09 clone | 3 | unmet | 104/105 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | 420 | 0 | X 4/0, Y 0/4, Z 4/0 |
| N11 canonical | 1 | unmet | 103/105 | `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 420 | 0 | X 0/4, Y 4/0, Z 4/0 |
| N11 canonical | 2 | unmet | 103/105 | `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 420 | 0 | X 0/4, Y 4/0, Z 4/0 |
| N11 canonical | 3 | unmet | 103/105 | `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 420 | 0 | X 0/4, Y 4/0, Z 4/0 |
| N11 clone | 1 | unmet | 103/105 | `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 420 | 0 | X 0/4, Y 4/0, Z 4/0 |
| N11 clone | 2 | unmet | 103/105 | `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 420 | 0 | X 0/4, Y 4/0, Z 4/0 |
| N11 clone | 3 | unmet | 103/105 | `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | 420 | 0 | X 0/4, Y 4/0, Z 4/0 |

Set order: the battery emits `failed_families = sorted(...)` over `FAMILY_ROSTER` (`tools/limine-pin-battery-r99.py:2306`), so the N11 order is lexicographic (`EXPLICIT-VERSION-ERA` < `REFUSAL-VERSIONS-9DIGIT`); the table above is the instrument's sorted order, not a seat re-sort. Per-run per-family counts come from each run's own `case_log`; the counts printed in `count-*.txt` are the named `[passed, failed]` pairs.

Failure-set exactness, every run: N09 fails exactly one family, `REFUSAL-VERSIONS-9DIGIT-Y` (no other family, none missing; X and Z pass 4/4). N11 fails exactly two, `EXPLICIT-VERSION-ERA` and `REFUSAL-VERSIONS-9DIGIT` (Y and Z pass 4/4). Within N11's `EXPLICIT-VERSION-ERA` family exactly 1 of 4 cases fails — the `999999999.9.9` row, i.e. the X-cap spelling — and the four X-family cases all fail. The two bends therefore fail **different** sets; N09 adds only the Y family to the landed gate's empty set.

## 5. Single-clause diffs

```bash
diff -u tools/check-limine-pins.py .ufo/waves/round-99/before/controls/bends/N09-y-era.py > $SD/diff-N09.txt   # rc=1
diff -u tools/check-limine-pins.py .ufo/waves/round-99/before/controls/bends/N11-x-era.py > $SD/diff-N11.txt   # rc=1
```

Each file has exactly one hunk, `@@ -315,7 +315,7 @@`, with one removed and one added line (`grep -c '^@@'` = 1, `^-[^-]` = 1, `^+[^+]` = 1 in `diff-N09.txt` and `diff-N11.txt`). Both replace the single `"visibility_era"` expression at gate **line 318, byte offset 17037** (byte-measured with `bytes.find`; `grep -n` confirms line 318). The identical `"visibility_era"` copy in the CANNOT-EVALUATE early return at **line 202, byte offset 11344** is untouched in both bends — the bends change exactly one clause, the main return's era-label expression. N09 guards it on `limine_version.split(".")[1] == "999999999"` (second component), N11 on `limine_version.split(".")[0] == "999999999"` (first component); pins, echo and every other line are unchanged.

## 6. Failure-field corroboration

`failed-case-field-corroboration.txt` re-reads every failed case in all four receipts: for every failed case the `pins` list, exit code, `rc` field and `on_panic` equal the case's frozen `want`, and `limine_version`/`limine_version_source` equal the flag spelling verbatim with source `flag`. The only asserted leg left that can move `meta_ok` is `visibility_era` — exactly the field the bend falsifies. N09's 4 failed Y cases are the two spellings (`12.999999999.4`, `0.999999999.0`) twice; N11's 5 failed cases are 4 X-cap cases plus 1 of 4 `EXPLICIT-VERSION-ERA` cases, all carrying the X-cap spelling.

## 7. PASS/FAIL per expected line

| expected (target / acceptance) | observed | verdict | receipt |
|---|---|---|---|
| bend digests match `instruments.sha256` | both match; manifest 16/16 OK, rc 0 | PASS | `sha.txt`, `instruments-check.txt` |
| N09 canonical `104/105` unmet ×3 | exactly, rc 1 | PASS | `c1-bend-N09-y-era-canonical.json`, `run-N09-canonical.log` |
| N09 canonical failed set exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` | exactly, all 3 runs | PASS | `count-c1-bend-N09-y-era-canonical.txt` |
| N09 clone `104/105` unmet ×3, exact set | exactly, rc 1 | PASS | `c1-bend-N09-y-era-clone.json`, `run-N09-clone.log`, `count-…-clone.txt` |
| N11 canonical `103/105` unmet ×3 | exactly, rc 1 | PASS | `c1-bend-N11-x-era-canonical.json`, `run-N11-canonical.log` |
| N11 canonical failed set exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]` | exactly, sorted order, all 3 runs | PASS | `count-c1-bend-N11-x-era-canonical.txt` |
| N11 clone `103/105` unmet ×3, exact set | exactly, rc 1 | PASS | `c1-bend-N11-x-era-clone.json`, `run-N11-clone.log`, `count-…-clone.txt` |
| 0 error rows, all 12 runs | 0 in every run; every failure is a verdict refusal | PASS | `count-*.txt` (`error_rows: 0`), §6 receipt |
| single-clause diff each | 1 hunk, 1−/1+, one `visibility_era` line each | PASS | `diff-N09.txt`, `diff-N11.txt` |
| bends fail different sets | N09 only Y; N11 X + EXPLICIT-VERSION-ERA | PASS | §4 table |

No finding against C1: no bend fails an extra or a missing family, and neither diff is more than one clause.

## 8. Tooling, risks, blockers

- Tooling changes: none installed (no pacman; nothing needed beyond in-repo `python3`, `git`, `bwrap` already present at `/usr/bin/bwrap`).
- Risk / disclosure: the clone leg's r99 battery and bends are copied-in bytes (the round-99 freeze is uncommitted at clone HEAD `f107da3a`); digests verify they are the pinned bytes, and the clone gate is the clone's own committed file. No commit was made anywhere.
- Blockers: none. Scratch `/fast/scratch/hyaku/tsukuroi-r99/ExecBends` was deleted after the receipts were written; receipt sizes total ~3 MB.

Receipts (all under `.ufo/waves/round-99/w1/ExecBends/`): `sha.txt`, `instruments-check.txt`, `diff-N09.txt`, `diff-N11.txt`, `clone-identity.txt`, `clone-sha.txt`, `c1-bend-N09-y-era-canonical.json`, `c1-bend-N09-y-era-clone.json`, `c1-bend-N11-x-era-canonical.json`, `c1-bend-N11-x-era-clone.json`, `run-N09-canonical.log`, `run-N09-clone.log`, `run-N11-canonical.log`, `run-N11-clone.log`, `count-c1-bend-N09-y-era-canonical.txt`, `count-c1-bend-N09-y-era-clone.txt`, `count-c1-bend-N11-x-era-canonical.txt`, `count-c1-bend-N11-x-era-clone.txt`, `failed-case-field-corroboration.txt`.

{"seat":"ExecBends","verdict":"met","notes":"N09-y-era and N11-x-era measured against tools/limine-pin-battery-r99.py in canonical and git-clone layouts, 3 runs each: N09 104/105 unmet failed exactly [REFUSAL-VERSIONS-9DIGIT-Y] x6 runs; N11 103/105 unmet failed exactly [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT] (instrument's sorted order) x6 runs; 0 error rows in all 12 runs; each bend differs from the gate by exactly one visibility_era expression line (one hunk, 1-/1+, gate line 318/byte 17037; early-return copy line 202/byte 11344 untouched); failed cases match want on pins/rc/rc-field/on_panic and echo verbatim with source flag, leaving only the era leg to fail; bend and battery digests match instruments.sha256 (16/16 OK); clone HEAD f107da3a with copied-in pinned r99 bytes, no commit made."}
