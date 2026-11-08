# ExecRegistry — C2 landed + doctored legs (D1, D2, D2lie) + coverage blindness

Seat: ExecRegistry. Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Scratch: /fast/scratch/hyaku/tsukuroi-r98/ExecRegistry (deleted before yield).
Tools installed/upgraded: none (python3 stdlib only; no new tool — see Tooling). pacman untouched (PAUSED rule respected; no `sudo`).

## Axes
- correctness: every number below was run by this seat; run wins over frozen text.
- discrimination: r98 vs r97 vs M08 on D1/D2/D2lie (each leg records ids + sites + details).
- blindness: coverage gate PASS 157/157 on each doctored revision.
- provenance: byte-level M08 derivation offset and instrument manifest recorded.

## Exact commands + raw output (trimmed)

### 1. Instruments
```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-98/before/instruments.sha256
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-limine-pins.py: OK
tools/check-r96-calibration.py: OK
... (all 27 lines OK, rc=0)
```
Receipt: 00-sha256sum.txt. **PASS** — frozen instruments intact.

### 2. Landed legs (base b3be3f90)
```
$ python3 tools/check-registry-content-r98.py --revision b3be3f90 --json <SEAT>/c2-content-landed.json
registry-content: status PASS bindings 7/7 findings 0
rc=0
$ python3 tools/check-registry-content-r98.py --selftest
... 14 lines PASS (clean, default-cell, fixtures-cell, schema-cell, roster-pinned-cell, roster-verdict-cell, cases-cell, span-cell, span-gap, span-gap-lie, row-missing, tool-missing, derivation-lie, tally-lie)
selftest PASS 14/14
rc=0
$ python3 tools/check-registry-content.py --revision b3be3f90
registry-content: status PASS bindings 7/7 findings 0
rc=0
$ python3 tools/check-registry-content.py --selftest | tail -2
selftest PASS 12/12
rc=0
```
Receipts: 01-landed.txt, c2-content-landed.json (`{"bindings":7,"findings":[],"status":"PASS"}`), 06-selftest-r97.txt.
**PASS** — landed PASS 7/7 both checkers; selftest 14/14 (r98) and 12/12 (r97).

### 3. M08 re-derivation (own scratch, never the frozen trees)
Pinned description (plan): "derive_variant_span checks only the first label" — one-line first-label-only change, FAILS r98 --selftest 12/14 (both gap cases red). The r98 function (tools/check-registry-content-r98.py:181) is:

```
    if numbers != list(range(numbers[0], numbers[0] + len(numbers))):
        return ",".join(labels)
```

Byte-level (bytes.find on pinned bytes, not decoded index):
- old byte offset in src: 8897, len 102
- new byte offset in mutant: 8897, len 95
- change: `numbers` → `numbers[:1]` and `len(numbers)` → `1`, i.e. the contiguity test only examines the first label; `numbers[:1] != range(first, first+1)` is always False, so the mutant always returns the contiguous form `N01-N03` and never the comma form. sha256 src `5bb1441e…` (matches instruments), mutant `2669fdd8…`.
```
$ python3 <scratch>/check-registry-content-r98-m08.py --selftest
span-gap             FAIL ['RC-VALUE-MISMATCH']
span-gap-lie         FAIL []
selftest FAIL 12/14
```
Receipts: 02-m08-source.txt, 07-m08-selftest.txt. **PASS** — matches frozen `before/dev/c2-m08-selftest.txt` exactly (same two red cases, same 12/14). M08 derivation: python `str.replace` of the single line `    if numbers != list(range(numbers[0], numbers[0] + len(numbers))):` → `    if numbers[:1] != list(range(numbers[0], numbers[0] + 1)):` on the pinned r98 bytes.

### 4. Doctored fixtures — re-derived in scratch (builder NOT run: it writes into the frozen wave dir)
Builder `.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh` was read but NOT executed (seat scope forbids writes outside seat dir; it hardcodes `$LANE/.ufo/...` output). Its doctor steps were mirrored verbatim in a scratch `git clone --shared` off base `b3be3f90` (asserted `git -C <clone> rev-parse --show-toplevel` == clone path), with `fixture/` copies of the r98 + r97 checkers, plus one extra "fixture base" commit that also carries my M08 copy and a copied coverage gate (deviation D-S1/D-S2 below — doctor semantics identical; see 06).

Scratch revisions (receipt 03-fixture-revisions.txt — *not* the frozen revision ids; run wins, so these are cited):
```
base b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a
fixture-base 685ba9ef0af3b8c28bec1812f601ffdb13d9f4c0
D1 4fcd80e887af0ed1b25afa689c52dcf946961ffd
D2 85aa5ab9afc937d7bf1819df9262eb4562b93270
D2lie 685a71886456c6f545bdd13678045d8799df4a13
```
Frozen ids for comparison: D1 aab954f1…, D2 d17ebc56…, D2lie 3155fd3d…. Difference = the extra fixture-base commit (frozen builder copies checkers in the same clone session; equivalent tree-wise modulo the commit split). Doctor diffs confirmed byte-identical in kind: D1 SKILL-only one-line change (`N01-N04` → `N01,N03`, 08-D1-doctor-diff.txt); D2 additionally drops 8 deletions from tools/make-r96-bends.py (matches frozen `doctored-r98-d2-diffstat.txt`: `tools/make-r96-bends.py | 8 -`).

### 5. Doctored legs — per-revision checker runs (all inside the scratch clone, `cd $C && python3 fixture/<chk> --revision <REV> --json <SEAT>/<tag>-<chk>.json`)

D1 (4fcd80e8):
```
D1 check-registry-content-r98.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-VALUE-MISMATCH SKILL.md:5939 | RC-BEND-SPAN states 'N01,N03', tools/make-r96-bends.py derives 'N01-N04'
D1 check-registry-content-r97.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-CELL-MISSING SKILL.md:5939 | make-r96-bends cell 5 no longer states 'VARIANTS (N\d+-N\d+)'
D1 check-registry-content-r98-m08.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-VALUE-MISMATCH SKILL.md:5939 | RC-BEND-SPAN states 'N01,N03', tools/make-r96-bends.py derives 'N01-N04'
```
Receipts: D1-check-registry-content-r98.py.json/.txt/.rc, D1-check-registry-content-r97.py.*, D1-check-registry-content-r98-m08.py.* **PASS** — D1 r98 FAIL exactly one RC-VALUE-MISMATCH; r97 RC-CELL-MISSING (claim text says "r97 RC-CELL-MISSING" ✓; binding id is RC-CELL-MISSING, not in RC-BEND-SPAN, expected: r97 has no comma capture).

Hmm — note: the acceptance line said "D1 r98 FAIL exactly one RC-VALUE-MISMATCH and r97 RC-CELL-MISSING". Measured exactly that. **PASS.**

D2 (85aa5ab9):
```
D2 check-registry-content-r98.py checker_rc=0 :: registry-content: status PASS bindings 7/7 findings 0
D2 check-registry-content-r97.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-CELL-MISSING SKILL.md:5939 | make-r96-bends cell 5 no longer states 'VARIANTS (N\d+-N\d+)'
D2 check-registry-content-r98-m08.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-VALUE-MISMATCH SKILL.md:5939 | RC-BEND-SPAN states 'N01,N03', tools/make-r96-bends.py derives 'N01-N03'
```
Receipts: D2-check-registry-content-*.json/.txt/.rc. **PASS** — D2 r98 PASS; M08 FAIL exactly one RC-VALUE-MISMATCH (derives N01-N03, row states N01,N03).

D2lie (685a7188):
```
D2lie check-registry-content-r98.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-VALUE-MISMATCH SKILL.md:5939 | RC-BEND-SPAN states 'N01-N03', tools/make-r96-bends.py derives 'N01,N03'
D2lie check-registry-content-r97.py checker_rc=1 :: registry-content: status FAIL bindings 6/7 findings 1
  RC-VALUE-MISMATCH SKILL.md:5939 | RC-BEND-SPAN states 'N01-N03', tools/make-r96-bends.py derives 'N01,N03'
D2lie check-registry-content-r98-m08.py checker_rc=0 :: registry-content: status PASS bindings 7/7 findings 0
```
Receipts: D2lie-check-registry-content-*.json/.txt/.rc. **PASS** — D2lie r98 FAIL one; M08 PASS (invert of D2). Note: r97 on D2lie reads RC-VALUE-MISMATCH (not RC-CELL-MISSING) because N01-N03 matches r97's N\d+-N\d+ capture — the frozen summary (before/dev/c2-doctored-summary.txt) shows the same r97 RC-VALUE-MISMATCH for D2lie only via `before/dev/c2-doctored-summary.txt` line 9-11. Consistent.

### 6. Coverage gate blindness (PASS 157/157 findings 0 on each doctored revision)
Deviation D-S1/D-S2 (recorded, not hidden): `tools/check-registry-coverage.py` has no `--json` flag (it always prints JSON to stdout) and binds `ROOT = Path(__file__).resolve().parents[1]` — i.e. it must be run from a checkout whose `tools/` is the revision under test. It also requires the revision to be an ancestor of BOTH `refs/heads/master` and `refs/remotes/origin/master` (tools/_revision.py `bind`). My scratch clone's `origin/master` predated the doctored commits, so I ran the gate (copied from the frozen lane bytes, sha256 6fcb2d0a per instruments) from inside the clone's `tools/` after deleting the clone's stale `refs/remotes/origin/master` ref (local scratch only; pushed-check vacuous via `_exists` guard). Local branches master tip = D2lie; D1, D2, D2lie all ancestors (linear history). All three reads:

```
D1 coverage checker_rc=0 :: {"status":"PASS","counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157}}
D2 coverage checker_rc=0 :: {"status":"PASS","counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157}}
D2lie coverage checker_rc=0 :: {"status":"PASS","counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157}}
```
Receipts: D1-coverage.txt/.rc, D2-coverage.txt/.rc, D2lie-coverage.txt/.rc. **PASS** — coverage PASS 157/157 findings 0 on each revision (the blindness leg: the coverage gate cannot see the content doctors).

Deviation D-S2 (cosmetic): 04-doctored-summary.txt shows `coverage checker_rc=2` for the first attempt (run from the lane with a `--json` flag the gate doesn't take → E-CLI). Superseded by the re-run above; kept as record.

### 7. Doctor-only scope
```
$ git -C <scratch clone> diff --name-only b3be3f90 <rev>
D1: SKILL.md, fixture/check-registry-content-r97.py, fixture/check-registry-content-r98-m08.py, fixture/check-registry-content-r98.py
D2: + tools/make-r96-bends.py
D2lie: + tools/make-r96-bends.py
```
Receipt: 05-diff-names.txt. **PASS** — D1 and D2 are content/tool doctors only: one SKILL.md row (make-r96-bends pinned cell) plus, for D2/D2lie, the make-r96-bends VARIANTS keys; `fixture/*` is the checker copy mechanism (identical in frozen diffstats). No other content rows touched.

## Acceptance check (expected vs measured)
| expected | measured | verdict |
|---|---|---|
| landed PASS 7/7 both checkers | r98 PASS + r97 PASS (bindings 7, findings 0) | PASS |
| selftest 14/14 (r98), 12/12 (r97) | 14/14, 12/12; M08 12/14 span-gap/span-gap-lie red | PASS |
| D1 r98 FAIL exactly one RC-VALUE-MISMATCH | FAIL 1× RC-VALUE-MISMATCH SKILL.md:5939 | PASS |
| D1 r97 RC-CELL-MISSING | RC-CELL-MISSING SKILL.md:5939 | PASS |
| D2 r98 PASS, M08 FAIL exactly one RC-VALUE-MISMATCH | PASS; FAIL 1× RC-VALUE-MISMATCH | PASS |
| D2lie r98 FAIL one, M08 PASS | FAIL 1× RC-VALUE-MISMATCH; PASS | PASS |
| coverage PASS 157/157 findings 0 each | 157/157, findings 0, rc 0 ×3 | PASS |
| D1/D2 doctors only | SKILL(+tool) + fixture/ only | PASS |

Deviations (not C2 findings): D-S1 scratch revision ids differ from frozen (extra fixture-base commit; doctor semantics byte-equivalent, diffstats match); D-S2 04-doctored-summary.txt coverage lines from the superseded lane-run attempt (rc=2 E-CLI) vs final clone-run receipts (rc=0 PASS). D-S1 does not move any measured verdict: the doctored trees are identical in the doctor files (SKILL.md single-line; make-r96-bends 8-line deletion).

Risks: the coverage-gate clone run copied the frozen gate into the clone's `tools/` (ROOT follows `__file__`). The gate bytes used were the pinned ones (sha256 6fcb2d0a…), so the 157/157 receipts are valid, but the lane's `tools/` copy at b3be3f90 would have given the same read (coverage tool unchanged by round). The scratch clone's `origin/master` ref deletion is scratch-local and deleted with the scratch.

Blockers: none.

Receipts (all under .ufo/waves/round-98/w1/ExecRegistry/): 00-sha256sum.txt, 01-landed.txt, c2-content-landed.json, 02-m08-source.txt, 03-fixture-revisions.txt, 05-diff-names.txt, 06-selftest-r97.txt, 07-m08-selftest.txt, 08-D1-doctor-diff.txt, D1-check-registry-content-{r98,r97,m08}.json, D2-check-registry-content-{r98,r97,m08}.json, D2lie-check-registry-content-{r98,r97,m08}.json, D1-coverage.txt, D2-coverage.txt, D2lie-coverage.txt (each with .rc sidecar).

{"seat":"ExecRegistry","verdict":"met","notes":"C2 fully re-derived: landed PASS 7/7 both checkers, selftest 14/14 (M08 12/14 span-gap red), D1 FAIL one RC-VALUE-MISMATCH / r97 RC-CELL-MISSING, D2 r98 PASS / M08 FAIL one, D2lie r98 FAIL / M08 PASS, coverage PASS 157/157 on all three doctored revs; D-S1/D-S2 recorded (scratch rev ids + superseded coverage attempt)"}
