# Seat ExecGateRuns — C1 landed-gate leg, roster integrity, usage-check and selftest, in BOTH layouts

Round 100, wave w1, lane `tsukuroi-shokunin`. Seat dir: `.ufo/waves/round-100/w1/ExecGateRuns/`
(this file is the seat's report; every cited receipt is a file I wrote under the seat dir).

Scope actually measured: the landed-gate leg of C1 (`tools/check-limine-pins.py` under the
unchanged r99 battery), roster/schema integrity, `--usage-check`, `--selftest` without
`--reference`, and `count-runs.py` parsing — each in the canonical (lane worktree) layout and in a
`git clone --shared` layout. Not measured by this seat (no claim made): the N12/N13 bends, the r98
do-nothing control, the `--selftest --reference` leg (a named r100 limit), and anything under C2.

## 1. Instrument integrity (harm guard, run first and again after the landing tip moved)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-100/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r99.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r99.py: OK
tools/check-registry-content-r100.py: OK
tools/make-r100-bends.py: OK
tools/make-r96-bends.py: OK
tools/check-registry-coverage.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-100/before/controls/do-nothing-battery-r99.py: OK
.ufo/waves/round-100/before/controls/do-nothing-checker-r99.py: OK
.ufo/waves/round-100/before/controls/bends/N12-x-echo.py: OK
.ufo/waves/round-100/before/controls/bends/N13-y-echo.py: OK
.ufo/waves/round-100/before/dev/make-fixtures.py: OK
.ufo/waves/round-100/claims.json: OK
.ufo/plans/round-100.md: OK
RC=0
```

Every line `OK` (16/16), rc 0, at `2026-11-08T12:15:54-03:00`. Receipt:
`receipts/18-instrument-manifest-and-tips.txt`.

Tips recorded at the same moment: lane worktree `HEAD=69474c55eb38632f3e740923b58029dc43e01300`,
`master=69474c55…`, `origin/master=69474c55…`, clone `HEAD=69474c55…`. At my **first** read (before
the canonical run) the lane worktree `HEAD` was `c450cd68a18a666f7bc835bcb2e8d76119f8aff6`;
`c450cd68` is an ancestor of `69474c55` and `git diff --stat c450cd68 69474c55 -- tools/` is
**empty**, so every bite of instrument I ran is byte-identical across the two tips, and the
manifest re-check above was taken *after* the move. The move is the L1's landing work, not mine.

## 2. Layouts

- Canonical: the lane worktree `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (`$PWD` of the run;
  `cwd` recorded in `receipts/00-canonical-header.txt`).
- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
  /fast/scratch/hyaku/tsukuroi-r100/ExecGateRuns/clone`; `git rev-parse --show-toplevel` printed
  `/fast/scratch/hyaku/tsukuroi-r100/ExecGateRuns/clone` before any command ran there, the tree was
  clean (`git status --porcelain | wc -l` → `0`) and the clone's own instruments re-digest to the
  pinned values:
  `c2e8c8fc…` (`tools/limine-pin-battery-r99.py`) and `7d79ac29…` (`tools/check-limine-pins.py`).
  Receipt: `receipts/03-clone-header.txt`.

## 3. Battery runs — 3 runs per layout

Canonical (rc 0):

```
$ python3 tools/limine-pin-battery-r99.py --gate tools/check-limine-pins.py --runs 3 \
    --work /fast/scratch/hyaku/tsukuroi-r100/ExecGateRuns/work \
    --json .ufo/waves/round-100/w1/ExecGateRuns/c1-gate-canonical.json
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
RC=0
```

Clone (rc 0, `cwd=/fast/scratch/hyaku/tsukuroi-r100/ExecGateRuns/clone`, the clone's own
`tools/limine-pin-battery-r99.py` and `tools/check-limine-pins.py`):

```
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
families_passed 105/105 verdict met failed -
RC=0
```

Receipts: `receipts/01-canonical-stdout.txt`, `receipts/04-clone-stdout.txt`,
`c1-gate-canonical.json`, `c1-gate-clone.json`.

### Per layout, per run (read from the JSON, `receipts/24-spellings-and-agreement.txt`)

| layout | run | families_passed/total | verdict | failed_families | error_rows | cases | schema | EXPLICIT-VERSION-ECHO | REFUSAL-VERSIONS-9DIGIT | REFUSAL-VERSIONS-9DIGIT-Y |
|---|---|---|---|---|---|---|---|---|---|---|
| canonical | 1 | 105/105 | met | `[]` | 0 | 420 | `tsukuroi-limine-pin-battery-r99-v1` | 4 passed / 0 failed | 4 / 0 | 4 / 0 |
| canonical | 2 | 105/105 | met | `[]` | 0 | 420 | `tsukuroi-limine-pin-battery-r99-v1` | 4 / 0 | 4 / 0 | 4 / 0 |
| canonical | 3 | 105/105 | met | `[]` | 0 | 420 | `tsukuroi-limine-pin-battery-r99-v1` | 4 / 0 | 4 / 0 | 4 / 0 |
| clone | 1 | 105/105 | met | `[]` | 0 | 420 | `tsukuroi-limine-pin-battery-r99-v1` | 4 / 0 | 4 / 0 | 4 / 0 |
| clone | 2 | 105/105 | met | `[]` | 0 | 420 | `tsukuroi-limine-pin-battery-r99-v1` | 4 / 0 | 4 / 0 | 4 / 0 |
| clone | 3 | 105/105 | met | `[]` | 0 | 420 | `tsukuroi-limine-pin-battery-r99-v1` | 4 / 0 | 4 / 0 | 4 / 0 |

`error_rows` = non-null `case_log[].error` entries (0 in all six runs). `cases` = `len(case_log)`
= 420 in all six runs; `distinct_families` = 105 and every family carries exactly 4 cases in all
six runs (`receipts/17-run-shape.txt`).

Canonical summary set **==** clone summary set (`canonical run set == clone run set: True`, same
receipt): the two layouts agree on verdict, counts, failed set, cases, error rows, schema and the
three named families' (passed, failed) pairs.

### Named-family spellings actually exercised on the landed gate

`receipts/24-spellings-and-agreement.txt` (constant across all six runs, both layouts):

```
EXPLICIT-VERSION-ECHO     ["12.9.4", "12.9.5", "12.9.6", "999999999.9.9"]
REFUSAL-VERSIONS-9DIGIT   ["999999999.9.9" x4]
REFUSAL-VERSIONS-9DIGIT-Y ["0.999999999.0", "0.999999999.0", "12.999999999.4", "12.999999999.4"]
```

So the X-cap family sends the first-component cap only, the Y-cap family sends the second-component
cap only, and the echo family carries one `999999999.9.9` member — the shape a first-component bend
(N12) must move and a second-component bend (N13) must not.

## 4. Roster / schema integrity (both layouts)

Canonical (`receipts/10-roster-schema-derived.txt`) and clone
(`receipts/12-clone-roster-integrity.txt`) — same numbers in both:

```
len(FAMILY_ROSTER) = 105
tuple(FAMILIES) == FAMILY_ROSTER = True
CASES_PER_FAMILY = 4
len(FAMILIES) = 105 unique keys = 105
schema literal byte 105731 = tsukuroi-limine-pin-battery-r99-v1
schema literal byte 115432 = tsukuroi-limine-pins-usage-r97-v1
FAMILY_ROSTER = ( at byte 92103
CASES_PER_FAMILY =  at byte 91905
```

The schema token is **derived from the module source bytes** (`re.finditer(rb'"schema":\s*"([^"]+)"')`
over the pinned file, byte offsets as shown), and cross-checked against the runtime payload:
`c1-gate-canonical.json -> schemas ['tsukuroi-limine-pin-battery-r99-v1'] cases [420] case_log lens [420]`.

Guard probe (same receipt as `receipts/11-roster-guard-order.txt`): reversing `FAMILIES` to the
same key set in a different order makes `main()` refuse before any work —

```
probe: tuple(FAMILIES) == FAMILY_ROSTER -> False
probe rc = 2
probe stderr = FAMILIES differs from FAMILY_ROSTER
```

## 5. `--usage-check` (both layouts)

Canonical, rc 0 (`c1-usage.json`, `receipts/05-usage-stderr.txt` empty, `receipts/06-usage-rc.txt`):

```
{"schema": "tsukuroi-limine-pins-usage-r97-v1",
 "gate": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py",
 "cases": [ {"version": "12.9", "want_rc": 64, "rc": 64, "ok": true}, … ],
 "verdict": "met"}
```

Parsed: `schema=tsukuroi-limine-pins-usage-r97-v1 cases=19 all_ok=True verdict=met`, rc 0.
The 19 pairs measured (`(version-head, want_rc, rc)`), all `ok`:

`('12.9',64,64) ('abc',64,64) ('12.9.6.1',64,64) ('',64,64) ('9'*5000+'.0.0',64,64)
('1234567890.0.0',64,64) ('0.1234567890.0',64,64) ('999999999.0.0',0,0) ('12.9.4',0,0)
('12.9.5',0,0) ('13.0.0',0,0) ('12.09.4',0,0) ('00.00.00',0,0) ('12.9.999999999',0,0)
('0.9.999999999',0,0) ('000000012.9.4',0,0) ('0000000001.0.0',64,64) ('auto',None,0)
(omitted,None,0)`.

Clone, rc 0 (`c1-usage-clone.json`, `receipts/13-clone-usage-stderr.txt` empty,
`receipts/14-clone-usage-rc.txt`):

```
schema=tsukuroi-limine-pins-usage-r97-v1 cases=19 all_ok=True verdict=met
gate=/fast/scratch/hyaku/tsukuroi-r100/ExecGateRuns/clone/tools/check-limine-pins.py
```

Note on the tool's shape (measured, not assumed): the `--usage-check` branch of `main()` never
consults `--json`; its JSON goes to stdout only, so I redirected stdout to `c1-usage.json` and
stdout/stderr are otherwise empty. Its payload schema is the *usage* token
`tsukuroi-limine-pins-usage-r97-v1` (byte 115432), not the battery token.

## 6. `--selftest` WITHOUT `--reference` (both layouts)

Canonical, rc 0 (`receipts/09-selftest-no-reference.txt`):

```
reference-gate      skipped (no --reference)
roster-literal     PASS families_passed=105
absent             PASS families_passed=0
constant-healthy   PASS families_passed=0
non-json           PASS families_passed=0
constant-degraded  PASS families_passed=0
selftest PASS 5/5
RC=0
```

Clone, rc 0 (`receipts/15-clone-selftest-no-reference.txt`): byte-identical six lines +
`selftest PASS 5/5`, rc 0.

The `--reference` leg was **not** run; that is a named r100 limit, and this seat claims nothing
about it.

## 7. `count-runs.py` per layout

```
$ python3 .ufo/waves/round-95/before/controls/count-runs.py \
    .ufo/waves/round-100/w1/ExecGateRuns/c1-gate-canonical.json \
    --family REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO
RC=0
```

Both layouts print the same three-run structure (full JSON: `receipts/07-count-runs-canonical.json`,
`receipts/16-count-runs-clone.json`): every run `"verdict": "met"`, `"families_passed": 105`,
`"families_total": 105`, `"failed_families": []`, `"cases": 420`, `"error_rows": 0`, and
`"named": {"EXPLICIT-VERSION-ECHO": [4,0], "REFUSAL-VERSIONS-9DIGIT": [4,0],
"REFUSAL-VERSIONS-9DIGIT-Y": [4,0]}` (the key order inside `named` varies per run; the values do
not). `count-runs.py` exit 0 is its own predicate (`verdict == met` and no error rows on every
run); the 105/420 figures are read from its JSON, not inferred from its rc.

## 8. PASS/FAIL against the seat's expected lines

| # | expected | measured | verdict |
|---|---|---|---|
| 1 | `sha256sum -c before/instruments.sha256` — all lines OK | 16/16 OK, rc 0; run once before the batteries and captured again after the tip moved (`receipts/18-…`), same 16 `OK` lines both times | PASS |
| 2 | canonical: 3 runs `met 105/105`, rc 0 | 3× `met 105/105`, rc 0 | PASS |
| 3 | clone: 3 runs `met 105/105`, rc 0 | 3× `met 105/105`, rc 0 (clone's own bytes, `c2e8c8fc…`/`7d79ac29…` re-digested) | PASS |
| 4 | roster 105, `tuple(FAMILIES) == FAMILY_ROSTER`, `CASES_PER_FAMILY`, schema token | 105, True, 4, `tsukuroi-limine-pin-battery-r99-v1` (both layouts) | PASS |
| 5 | each run `cases` 420, schema `…-r99-v1` | 420 and the r99 token in all six runs | PASS |
| 6 | `--usage-check` rc 0, JSON recorded | rc 0, `verdict met`, 19/19 cases ok, both layouts | PASS |
| 7 | `--selftest` (no `--reference`) `PASS 5/5`, rc 0 | `PASS 5/5`, rc 0, both layouts; `reference-gate skipped` | PASS |
| 8 | `count-runs.py` per layout recorded | identical 3-run summaries per layout, 105/105, named `[4,0]` | PASS |
| 9 | canonical and clone agree | summary sets equal (`canonical run set == clone run set: True`) | PASS |

No expected line deviated. Nothing was retried to a pass; each command above was run once per
layout and its bytes kept.

## 9. Observations / disclosures (not deviations from the target)

1. **The battery is not byte-deterministic across runs by design.** `run_battery` seeds
   `random.Random(secrets.randbits(64))` and calls `rng.shuffle(plan)`, and `build(fam, rng, root)`
   draws per-case decorations from the same rng. Measured consequence
   (`receipts/21-nondeterminism-scope.txt`, `receipts/20-run-multiset-identity.txt`,
   `receipts/19-run-to-run-diffs.txt`): case *order* differs in every run, and only **6/105**
   families have byte-identical case content across the three canonical runs; 99/105 vary in
   sbflag/tpm/line-number decoration. Verdict-level determinism still holds (six `met` runs, all
   named-family counts `[4,0]`), and the three named families' **version spellings are constant**
   across all six runs (`receipts/24-spellings-and-agreement.txt`). Any later seat that diffs two
   battery JSONs byte-wise will see noise; diff verdicts, families and spellings instead.
2. **The lane worktree HEAD moved mid-round** (`c450cd68` → `69474c55`, the commit
   `round-100: fix — the check-registry-content-r100 registry row was missing its write-scope
   cell`). `tools/` is byte-identical between them (`git diff --stat … -- tools/` empty) and the
   instrument manifest re-verifies after the move, so the canonical run's bytes are the pinned
   bytes. Recorded, not repaired.
3. **The clone tracks `master` (`69474c55`), not the detached worktree HEAD** the lane had at my
   start (`c450cd68`). Both carry the same `tools/` bytes, so the clone leg measures the same
   instruments; the clone is a `--shared` clone in my scratch dir, never a source of truth.
4. **`--usage-check` ignores `--json`** and always prints to stdout; its schema token is
   `tsukuroi-limine-pins-usage-r97-v1` with 19 cases.
5. **Harm guard, coverage gate, as found** at the landing tip:
   `python3 tools/check-registry-coverage.py --revision 69474c55` →
   `{"branch":"master","branch_tip":"69474c55…","counts":{"findings":0,"missing":0,"registered":165,
   "rows_total":165,"tools_total":165},"findings":[],"revision":"69474c55…","status":"PASS"}`, rc 0
   (`receipts/23-coverage-gate.txt`). Reported as found; not my claim to score.
6. **No tooling was installed or upgraded** (pacman is paused host-wide; nothing was needed).
   `bwrap` 0.13.1 present, so the battery's isolation launcher ran (`main()` refuses rc 2 without
   it — it did not).

## 10. Receipts (all under `.ufo/waves/round-100/w1/ExecGateRuns/`)

| path | content |
|---|---|
| `c1-gate-canonical.json` | 3-run battery JSON, canonical layout (sha256 `2b732d93…`) |
| `c1-gate-clone.json` | 3-run battery JSON, clone layout (sha256 `873601fc…`) |
| `c1-usage.json` | `--usage-check` stdout, canonical (sha256 `68b10b7b…`) |
| `c1-usage-clone.json` | `--usage-check` stdout, clone (sha256 `68a8e0c3…`) |
| `receipts/00-canonical-header.txt` | date, command, cwd, HEAD, instrument digests |
| `receipts/01-canonical-stdout.txt` | canonical battery stdout + `RC=0` |
| `receipts/03-clone-header.txt` | clone toplevel/HEAD/master/cleanliness/instrument digests |
| `receipts/04-clone-stdout.txt` | clone battery stdout + `RC=0` |
| `receipts/05-usage-stderr.txt`, `receipts/06-usage-rc.txt` | usage-check stderr (empty) and rc |
| `receipts/07-count-runs-canonical.json` | `count-runs.py` output, canonical |
| `receipts/08-canonical-shape.txt` | canonical run shape (schema/cases/errors) |
| `receipts/09-selftest-no-reference.txt` | canonical selftest, 5 lines + tally + rc |
| `receipts/10-roster-schema-derived.txt` | roster, `CASES_PER_FAMILY`, schema literals + byte offsets, runtime agreement, usage parse |
| `receipts/11-roster-guard-order.txt` | `main()` refuses rc 2 when `FAMILIES` order differs |
| `receipts/12-clone-roster-integrity.txt` | clone roster/schema derivation |
| `receipts/13-clone-usage-stderr.txt`, `receipts/14-clone-usage-rc.txt` | clone usage-check stderr/rc |
| `receipts/15-clone-selftest-no-reference.txt` | clone selftest lines + tally + rc |
| `receipts/16-count-runs-clone.json` | `count-runs.py` output, clone |
| `receipts/17-run-shape.txt` | per-run shape for both layouts |
| `receipts/18-instrument-manifest-and-tips.txt` | `sha256sum -c` output and the four tips |
| `receipts/19-run-to-run-diffs.txt` | raw first-differing entries, run1 vs run2/run3 |
| `receipts/20-run-multiset-identity.txt` | per-family content multiset comparison (False, with order heads) |
| `receipts/21-nondeterminism-scope.txt` | 6/105 byte-stable, 99/105 varying families |
| `receipts/22-named-family-cases.txt` | every named-family case row, six runs |
| `receipts/23-coverage-gate.txt` | coverage gate at `69474c55` |
| `receipts/24-spellings-and-agreement.txt` | spelling multisets, six per-run summaries, cross-layout equality |
| `receipts/25-artifact-digests.txt` | sha256 of the four seat JSON artifacts |

Scratch `/fast/scratch/hyaku/tsukuroi-r100/ExecGateRuns` (clone + work dirs) was removed before
yield; the shared parent `/fast/scratch/hyaku/tsukuroi-r100` was **not** touched.

{"seat":"ExecGateRuns","verdict":"met","notes":"Both layouts: landed gate met 105/105 x3 (cases 420, schema tsukuroi-limine-pin-battery-r99-v1, 0 error rows, failed_families []); EXPLICIT-VERSION-ECHO/REFUSAL-VERSIONS-9DIGIT/REFUSAL-VERSIONS-9DIGIT-Y each 4 passed/0 failed per run; canonical run set == clone run set. Roster 105, tuple(FAMILIES)==FAMILY_ROSTER True, CASES_PER_FAMILY 4, schema literal tsukuroi-limine-pin-battery-r99-v1 at byte 105731 (re-derived, both layouts); main() refuses rc 2 on roster-order drift. --usage-check rc 0 verdict met 19/19 ok both layouts (schema tsukuroi-limine-pins-usage-r97-v1; --json is not consulted on this branch). --selftest without --reference PASS 5/5 rc 0 both layouts; --reference leg not run (named limit). Instruments sha256sum -c 16/16 OK after the tip moved c450cd68->69474c55 (tools/ byte-identical, git diff empty). Observations: battery randomizes order and per-case decoration per run (only 6/105 families byte-stable across runs; named-family version spellings constant) so only verdict-level determinism holds; coverage gate at 69474c55 reads PASS registered 165/165 rows_total 165/165; no tooling installed."}
