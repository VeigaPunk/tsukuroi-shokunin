# MutInstruments — round 100 w1 mutation matrix (depth 8 / freshness 9)

Seat: `MutInstruments` (mutation-tester). Lane `tsukuroi-shokunin`, round 100, wave w1.
Scratch: `/fast/scratch/hyaku/tsukuroi-r100/MutInstruments` — created for the seat, **deleted**
before this report was written (`receipts/15-scratch-removed.txt`). Nothing was written into the
lane outside `.ufo/waves/round-100/w1/MutInstruments/`.

Scope: one plausible defect at a time in each of the two new instruments
(`tools/check-registry-content-r100.py`, `tools/make-r100-bends.py`), each on a scratch copy, each
scored against the frozen leg that is supposed to catch it. The lane instruments were never edited
or run in place; `make-r100-bends.py` (the scorer for C1) was never run in the lane.

Axes worked: **depth** (does each frozen leg actually kill the defect it names?) and **freshness**
(the C2 capture's fail-closed branches). Nothing else moved.

## 0. Instruments under test and their pinning

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
... 16 x ": OK"; rc=0                     # receipts/14-manifest-recheck.txt (grep -c ': OK' -> 16)

$ wc -c tools/check-registry-content-r100.py tools/make-r100-bends.py tools/check-limine-pins.py
 38009 tools/check-registry-content-r100.py     sha256 7a23a522871ab5dd33a94ae51b09c70ab182a0d2a53d7380f82bb11a13f3c2d2
  4471 tools/make-r100-bends.py                 sha256 7ccfe69e52604ec5bb8db423e377cf9f0eb468baf03d0ef7be77b3209654e695
 30286 tools/check-limine-pins.py               sha256 7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32
```

Manifest re-check was run **after** all probes and reads 16/16 OK, so no pinned byte moved
(restoration evidence; the probes only ever read lane bytes).

Pristine baselines (the detector must read the frozen value before a mutant can be killed):

```
$ python3 <scratch>/bin/base-checker.py --selftest      # byte-identical copy of the lane tool
selftest PASS 26/26                                      # receipts/00-pristine-selftest.txt, rc 0

$ python3 <lane>/tools/limine-pin-battery-r99.py --gate <pristine gate copy> --runs 1 --work ...
families_passed 105/105 verdict met failed -            # receipts/10-battery-gate-pristine.json
```

Twelve-fixture matrix on the pristine checker (built by the frozen
`.ufo/waves/round-100/before/dev/make-fixtures.py` into scratch) — matches the frozen
`before/dev/c2-fixtures.txt` reading exactly (6 PASS where r99 finds, 5 fail-closed, GAP PASS):

```
SEP-SPACE rc=0 | SEP-SEMICOLON rc=0 | SEP-AND rc=0 | SEP-SLASH rc=0 | SEP-PLUS rc=0 | UNION rc=0
LETTER rc=1 RC-CELL-MISSING | PROSE rc=1 RC-CELL-MISSING | UNION-LIE rc=1 RC-VALUE-MISMATCH
HYBRID rc=1 RC-VALUE-MISMATCH | RESTATED rc=1 RC-CELL-AMBIGUOUS | GAP rc=0
                                                         # receipts/01-pristine-matrix.txt
```

## 1. Method

`w1/MutInstruments/mutate.py <outdir>` builds every mutant from the pristine lane bytes by
**exact-string substitution with a `count == 1` assertion**, so each mutant differs from its
instrument only by the injected defect; it prints the size and sha256 of each mutant
(`receipts/02-mutant-build.txt`). Diff sizes against the pristine instruments are in
`receipts/08-mutant-diffs.txt` (M3/M5/M7/B1/B3 are 2 changed lines, M6 3, M4/M8 6, M2 8, M1 9,
B2 4).

Checker legs run: `--selftest` (the instrument's own 26 frozen cases) and, for every mutant, the
twelve-fixture matrix through `--root` (`receipts/03-*-selftest.txt`,
`receipts/05-checker-matrix.txt`).

Generator legs run: `w1/MutInstruments/probe-generator.py` sets up a throw-away **fake lane**
`<scratch>/probe/<case>/{tools,}` (the generator derives `LANE` from `__file__`, so this is the
lane layout with the same relative `SRC`/`OUT`), runs the generator under test and records rc,
stdout/stderr, every emitted file's sha256 and the changed-line count against the gate
(`receipts/04-generator-probes.txt`). Probe layout faithfulness is itself a case: the pristine
generator run in the fake lane emits articles **byte-equal to the two frozen committed bends**
(`receipts/04-generator-probes.txt` case 01).

Frozen-measurement baseline for the article legs (battery, `--runs 1`, counted with the frozen
`.ufo/waves/round-95/before/controls/count-runs.py`):

| article | verdict | families | failed_families | error rows |
|---|---|---|---|---|
| landed gate (pristine) | met | 105/105 | `[]` | 0 |
| frozen `N12-x-echo` | unmet | 103/105 | `EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT` | 0 |
| frozen `N13-y-echo` | unmet | 104/105 | `REFUSAL-VERSIONS-9DIGIT-Y` | 0 |

(both frozen readings reproduce the C1 development run, so the detector is live on both sides:
`receipts/11-frozen-N12.json`, `11-frozen-N13.json`, `12-count-frozen-*.json`).

## 2. Checker mutants — `tools/check-registry-content-r100.py` (8 mutants)

| id | injected defect | mutant sha256 | `--selftest` | red cases | verdict | killing leg |
|---|---|---|---|---|---|---|
| M1 | skip `parse_label_set` validation, bind the first `N<digits>` of the mention | `25fc3cfc0deccf9d4b89cb9dd411a4986ecb0b6dd8ee6cf153f90481f3834fbb` | **FAIL 6/26** | 20 cases | **killed** | `span-gap` (want `[]`, got `[RC-VALUE-MISMATCH]`), `span-sep-space`, `span-letter-suffix` (want `[RC-CELL-MISSING]`, got `[RC-VALUE-MISMATCH]`), `span-prose` |
| M2 | accept a cell that mentions `VARIANTS` twice | `aa43512d1c0654a46bf0761c5cbe195bcd595024982b70df2d8903a22172c7e4` | **FAIL 25/26** | `span-restated` | **killed** | `span-restated` (want `[RC-CELL-AMBIGUOUS]`, got `[RC-CELL-MISSING]`) |
| M3 | compare only the first label of each set | `a5b9782ee9d80182c663c46fe1dd2a9f4857024f36195476b1c2238ea0b9278d` | **FAIL 22/26** | `span-cell`, `span-gap-lie`, `span-hybrid`, `span-union-lie` | **killed** | all four: want `[RC-VALUE-MISMATCH]`, got `[]` (false green) |
| M4 | drop range expansion (`N01-N03` binds as `N01`) | `ee2e6513799d276abb6c6accdbcfb7f3ff2fcfb4a4075f5e3e8e94eda087b1ce` | **FAIL 13/26** | 13 cases | **killed** | `clean` (want `[]`, got `[RC-VALUE-MISMATCH]`), `span-sep-and`, `span-union` |
| M5 | accept a declared set that is a superset of the derived set | `184d5bd146adb0c5d3fca7f9f0c486e46c0638448da1e420a910413751f40f3e` | **FAIL 23/26** | `span-cell`, `span-gap-lie`, `span-hybrid` | **killed** | all three: want `[RC-VALUE-MISMATCH]`, got `[]` (false green — direction rule: a leg reading *better* is a kill) |
| M6 | `parse_label_set` accepts prose (fall back to the union of `N`-tokens) | `537eef08c14cd71d05edbffc8f81f7fdf552a0ab70622b51858e738bc826c3d2` | **FAIL 24/26** | `span-letter-suffix`, `span-prose` | **killed** | both: want `[RC-CELL-MISSING]`, got `[RC-VALUE-MISMATCH]` |
| M7 | count `VARIANTS` mentions case-insensitively (`variants` also counts) | `ddf2a7be6668d29a1fa4b063fe054411a883aee4515581ea1d54245de949ec06` | **PASS 26/26** | none | **SURVIVED** | *no leg exists* — see §4.1 |
| M8 | skip the `--revision` ancestor refusal (r99 M07, re-probed on the successor) | `e3f68de365018cccbf0f4397ff446412c15b0b2bcc06fff0b1840dcdbd6a51f2` | **FAIL 25/26** | `ancestor` | **killed** | `ancestor`: want rc 2 `CANNOT-EVALUATE`, got `rc=0 registry-content: status PASS bindings 7/7 findings 0` |

Twelve-fixture matrix per mutant (`receipts/05-checker-matrix.txt`), deviation count from the frozen
reading:

| mutant | cells deviating from the frozen matrix |
|---|---|
| M1 | 9/12 (`UNION-LIE`, `HYBRID`, `RESTATED` keep their frozen id; everything else reads `RC-VALUE-MISMATCH`, incl. `GAP` which must PASS) |
| M2 | 1/12 (`RESTATED` → `RC-CELL-MISSING`) |
| M3 | 2/12 (`UNION-LIE`, `HYBRID` → no finding) |
| M4 | 2/12 (`SEP-AND`, `UNION` → `RC-VALUE-MISMATCH`) |
| M5 | 1/12 (`HYBRID` → no finding) |
| M6 | 2/12 (`LETTER`, `PROSE` → `RC-VALUE-MISMATCH`) |
| M7 | **0/12** (identical to pristine, byte for byte on every cell) |
| M8 | 0/12 (correct: its branch is `--revision`, outside `--root`) |

Also exercised on the committed surface through a `git clone --shared` in scratch (read-only on the
lane objects), so the mutants' `ROOT`-derived `git -C` target was the clone:

```
$ git clone --shared tsukuroi-shokunin <scratch>/clone-lane        # toplevel probe: prints the clone
$ python3 <clone>/tools/check-registry-content-r100.py --revision ce73ccaf --json ...
registry-content: status PASS bindings 7/7 findings 0               # {status PASS, bindings 7, rows 163}
$ python3 <clone>/tools/M7.py --revision ce73ccaf --json ...
registry-content: status PASS bindings 7/7 findings 0               # M7 identical on the live table
```

## 3. Generator mutants — `tools/make-r100-bends.py` (3 mutants)

Probes (`receipts/04-generator-probes.txt`):

| id | injected defect | mutant sha256 | probe | observed | verdict | killing leg |
|---|---|---|---|---|---|---|
| B1 | remove the exact-once count guard | `acef7af0e1ffc531ff8701199751b160dbdbb4b2e80709668b453682cfbdda32` | gate whose pattern matches **2×** (an unused duplicate `return` block) | pristine: `rc=1` `pattern ... matched 2 times, expected 1`, nothing emitted. B1: `rc=0`, both articles written, **2 changed lines each** (`{'N12': (2,2), 'N13': (2,2)}`) | **killed** | the one-clause/refusal leg: "exactly one changed line" and "refuse a non-exactly-once pattern" both broken |
| B2 | emit a no-op bend (N12 replacement = the gate line) with the no-op guard gone | `a1eff15513b859cc2206358b9aab2221bea05a72843d2e1925920a4c13ab13fa` | pristine gate | pristine generator carrying the same no-op VARIANTS (`P-B2`, `0f3f53dc…`): `rc=1` `N12-x-echo: substitution changed nothing`, nothing emitted. B2: `rc=0`; emitted `N12-x-echo.py` sha256 `7d79ac29…` = **the gate itself** (0 changed lines) | **killed** | battery on that article reads **met 105/105** where the claim needs **unmet 103/105** (`receipts/11-B2-N12.json`, `12-count-B2-N12.json`) — the article cannot move its frozen family |
| B3 | key the N12 X lie on the **second** version component | `702d3cd5cc970d1a42d80dd84c72be4ff39b28ae4980bbf7175b6b638bb3845a` | pristine gate | `rc=0`; emitted `N12-x-echo.py` sha256 `c9339413…` (≠ frozen `eb247e16…`), 1 changed line, keyed on `split(".")[1]` | **killed** | battery on that article: **unmet 104/105 `[REFUSAL-VERSIONS-9DIGIT-Y]`**, i.e. it reproduces the Y leg and leaves the X family 4/4 green, where N12's frozen reading is **103/105 `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`** (`receipts/11-B3-N12.json`) |

Sub-probe for B1 on a **0-match** pattern: B1 is stopped by the *surviving* no-op guard
(`rc=1`, nothing emitted) — the count guard's removal is **masked** there and is only load-bearing
for ≥2 matches. Recorded as `masked` in the probe receipt, not as a kill.

B1's two-clause article also still moves the frozen family: battery reads **unmet 103/105
`[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]`**, identical to the correct N12 bend, because
the second substitution site is dead code (`_dup_probe` is never called). So B1's defect is caught
by the structural leg (one clause / refusal), **not** by family movement — say so plainly rather
than claiming the battery discriminates it (`receipts/11-B1-N12.json`, `12-count-B1-N12.json`,
error rows 0).

## 4. Survivor and routed defect

### 4.1 M7 survives every leg (freshness gap)

M7 makes the ambiguity mention counter case-insensitive
(`re.findall(r"\bVARIANTS\b", cell, re.IGNORECASE)`) while the extraction regex stays
case-sensitive. No frozen case and no fixture contains the word `variants` in a cell, so all 26
selftest cases pass and all twelve fixtures read exactly as on the pristine checker. The live table
has the same blind spot: the only bound cell (`SKILL.md` `make-r96-bends` pinned values) reads
`r96 VARIANTS N01-N04` with no lowercase mention, so the clone run reads PASS 7/7 for M7 as well.

The defect is a **false finding on a legitimate cell**, shown with a purpose-built fixture built by
the checker's own `build_fixture` in scratch (`receipts/06-M7-lowercase-witness.txt`):

```
fixture cell: r96 variants declared in the generator; VARIANTS N01-N03
PLAIN        base-checker rc=0                      # control: M7 does not reject everything
PLAIN        M7           rc=0
LOWER-PROSE  base-checker rc=0                      # one uppercase VARIANTS mention: correct PASS
LOWER-PROSE  M7           rc=1 FINDING RC-CELL-AMBIGUOUS SKILL.md:10
```

**Leg that should exist** (routed defect): a selftest case that pins the mention counter to the
uppercase token — e.g. `span-lower-mention` with doctor
`("SKILL.md", "VARIANTS N01-N03", "variants declared in the generator; VARIANTS N01-N03")` and
`want_ids == []`. Pristine reads `[]` (confirmed above); M7 reads `[RC-CELL-AMBIGUOUS]` and would
turn that case red. Until such a case lands, a change of `re.IGNORECASE` into the mention count is
invisible to `--selftest`, to the twelve fixtures and to the live table.

### 4.2 Coverage note (not a survivor): the two generator guards overlap

The exact-once guard (B1) and the no-op guard (B2) each cover the other's 0-match case; only the
≥2-match shape isolates the count guard. A future selftest for `make-r100-bends.py` should keep both
probes (0-match and 2-match), since a 0-match-only probe would let B1 live.

## 5. Harm guard

```
$ python3 tools/check-registry-coverage.py --revision ce73ccaf75d0...
{"status":"PASS","counts":{"findings":0,"missing":0,"registered":163,"rows_total":163,"tools_total":163},...}
$ python3 tools/check-registry-coverage.py --revision 69474c55eb38...
{"status":"PASS","counts":{"findings":0,"missing":0,"registered":165,"rows_total":165,"tools_total":165},...}
                                                      # receipts/13-coverage-*.txt, both rc 0
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256   # 16/16 OK, rc 0  (receipts/14-...)
$ git -C <lane> status --porcelain
 M corpus/QUALITY.md                       # sibling seats' writes, not this seat's
 M corpus/lessons/round-100.md             # sibling seats' writes, not this seat's
?? .ufo/waves/round-100/after/             # sibling seat
?? .ufo/waves/round-100/w1.ready.dispatched# L1
?? .ufo/waves/round-100/w1/                # the wave's seat dirs (mine is MutInstruments/)
$ git -C <lane> status --porcelain -- .ufo/waves/round-100/w1/MutInstruments .ufo/waves/round-100/w1/MutInstruments.md
?? .ufo/waves/round-100/w1/MutInstruments.md
?? .ufo/waves/round-100/w1/MutInstruments/
```

The registry coverage gate reads PASS at the freeze tip (163) and at the current `master` tip
`69474c55` (165) as found — I did not change it and did not add landing rows.

One observation, not a defect: the seat's fixture-building import of
`tools/check-registry-content-r100.py` refreshed the gitignored
`tools/__pycache__/check-registry-content-r100.cpython-314.pyc` (mtime 12:03). The directory already
existed from earlier development runs (entries 10:04–10:58), the entry is gitignored
(`.gitignore:2:__pycache__/`) and no tracked file changed; later import runs used
`PYTHONDONTWRITEBYTECODE=1`. No lane file was edited, no git/jj mutation was run in the lane, and
no `make-r100-bends.py`/`make-r9*-bends.py` was executed against lane paths.

## 6. Score

| # | mutant | killed? | killing leg |
|---|---|---|---|
| M1 | first-label binding, no token validation | killed | `span-gap` + `span-sep-space` + `span-letter-suffix` + `span-prose` |
| M2 | two `VARIANTS` mentions accepted | killed | `span-restated` |
| M3 | first-label comparison only | killed | `span-cell`, `span-gap-lie`, `span-hybrid`, `span-union-lie` (all false-green) |
| M4 | no range expansion | killed | `clean`, `span-sep-and`, `span-union` |
| M5 | superset accepted | killed | `span-cell`, `span-gap-lie`, `span-hybrid` (all false-green) |
| M6 | prose fallback | killed | `span-letter-suffix`, `span-prose` |
| M7 | case-insensitive mention count | **SURVIVED** | *missing*: `span-lower-mention` (see §4.1) |
| M8 | ancestor refusal skipped | killed | `ancestor` (rc 0 PASS where rc 2 is required) |
| B1 | exact-once guard removed | killed | 2-match probe: rc 0 with 2 changed lines per article |
| B2 | no-op article emitted | killed | battery 105/105 met where 103/105 is required |
| B3 | X lie keyed on component 2 | killed | battery 104/105 `[REFUSAL-VERSIONS-9DIGIT-Y]` instead of the X pair |

10 of 11 mutants killed by a named leg; 1 survivor named with the leg that should exist. Both
frozen articles and the landed gate re-derive their frozen readings on scratch bytes, so the
detector is live in both directions (no baseline failure).

## 7. Receipts (all under `w1/MutInstruments/`)

`mutate.py`, `probe-generator.py`, and `receipts/00`–`15`:
`00-pristine-selftest.txt`, `00-fixture-paths.txt`, `01-pristine-matrix.txt`,
`02-mutant-build.txt`, `03-M{1..8}-selftest.txt`, `03-selftest-summary.txt`,
`04-generator-probes.txt` (+`.raw`), `05-checker-matrix.txt`, `06-M7-lowercase-witness.txt`,
`07-{check-registry-content-r100,M7}-live.{json,txt}`, `08-mutant-diffs.txt`,
`10-battery-gate-pristine.json`, `11-{frozen-N12,frozen-N13,B1-N12,B2-N12,B3-N12}.{json,out}`,
`12-count-*.json`, `13-coverage-{ce73ccaf,master-tip}.txt`, `14-manifest-recheck.txt`,
`15-scratch-removed.txt`.

Tooling: none installed or upgraded (no pacman transaction; no `uv`/`npx`/binary install); the
probes used the host `python3`, `git` (read-only / clone in scratch) and `diff`.

{"seat":"MutInstruments","verdict":"findings","notes":"8 checker mutants (7 killed by named frozen cases incl. the r99 ancestor branch, M7 survives all 26 selftest cases, all twelve fixtures and the live table); 3 generator mutants killed (B1 by the 2-match one-clause/refusal leg, B2 by battery 105/105 met vs 103/105, B3 by battery 104/105 Y instead of the X pair); survivor M7 (case-insensitive VARIANTS mention count) needs a span-lower-mention selftest case; lane instruments 16/16 OK, coverage PASS at ce73ccaf 163/163 and master 69474c55 165/165, scratch deleted."}
