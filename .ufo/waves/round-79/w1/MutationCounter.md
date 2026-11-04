# MutationCounter — round 79 w1 (attack: selftest mutant battery)

claim=C1+C2
verdict=kill-rate 8/13 single-clause mutants (61.5%); 5 survivors, of which 3 (`c2-accept-shape-one`, `c2-accept-no-code3`, `c2-no-selftest-word`) are live-path false greens the assigned detector cannot see (`shape_ok=1/2` or an uncoded `3`, `met=1`, rc 0) and 2 (`c1-seven-rows-rowcount`, `c1-no-line-check`) are clauses unreachable behind the frozen-equality leg; both neutral renames pass (2/2); no lane byte written.

Seat class: attack item, serves **C1** (depth: eight pinned dependency-propagation
rows with a bound review) and **C2** (operability: zero duplicate current registry
rows and two gate-standard rows). Base `9086589a82f221d130ed6711fbe70b85f0d07aea`,
frozen claim commit `afe1f26128bde87484001cd02ebf11fa524c4059`.

## Method

* Detector (the one my item assigns): the **mutated tool's own `--selftest`**.
  `rc != 0` = killed, `rc == 0` = survived. Assigned execution class:
  EXEC-AUTHORIZED (cp/mkdir/python3 in my scratch only; read-only git).
* Bytes under test are scratch copies, never the lane files:
  * `tools/measure-unit-deps-r79.py` SHA-256 `132be669e367670e8af15d8830443097c6c22f91ce36d1088e7282cf48882d1d`
  * `tools/check-gate-standard-r79.py` SHA-256 `0b32ddbcaf1fcab3721745ef9629d20ff1d249403d0d590655e537b2ad72cfda`
  * `tools/_revision.py` (import-only dependency), `before/expected.json`
    (`0c09c7a4…`, matches the frozen digest), `before/src/systemd.unit.xml`
    (`eb9479be…`, matches the frozen digest).
* Scratch root `/fast/scratch/hyaku/tsukuroi-r79/MutationCounter` with
  `TMPDIR` set inside it; deleted before yield. No `/tmp` use.
* Baseline controls (mine, re-measured, not inherited): C1 `--selftest`
  `SELFTEST total=32 passed=32 failed=0` rc 0; C2 `--selftest`
  `SELFTEST total=8 passed=8 failed=0` rc 0. Both reproduce the frozen
  `before/controls.json` arms byte-for-byte in their total line
  (`selftest-depth` rc 0 `SELFTEST total=32 passed=32 failed=0`;
  `selftest-gate-standard` rc 0 `SELFTEST total=8 passed=8 failed=0`), so a
  mutant kill is a real delta, not a broken baseline. Interpreter:
  `/usr/bin/python3` (3.14.8), the same binary the frozen arms name.
* Every one of the **13 single-clause mutants** is **one hunk and exactly two
  changed lines** (`diff -u` `@@` count 1, `-`/`+` line count 2) and
  **compiles** (`py_compile` rc 0 for all 15 trees) — so kills are
  behavioural, not syntax. The two neutral renames touch 3 and 2 rename sites
  (1 and 2 hunks) by construction. Verified per mutant; `matrix.json` carries
  `hunks`, `changed_lines`, `py_compile_rc`.

### Exact commands

```sh
S=/fast/scratch/hyaku/tsukuroi-r79/MutationCounter
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR"
cp <lane>/tools/{measure-unit-deps-r79.py,check-gate-standard-r79.py,_revision.py} "$S/base/tools/"
cp <lane>/.ufo/waves/round-79/before/expected.json "$S/base/.ufo/waves/round-79/before/"
cp -r <lane>/.ufo/waves/round-79/before/src "$S/base/.ufo/waves/round-79/before/"
python3 "$S/base/tools/measure-unit-deps-r79.py" --selftest   # rc 0, 32/32
python3 "$S/base/tools/check-gate-standard-r79.py" --selftest   # rc 0, 8/8
python3 "$S/drive.py"      # 12 mutants + 2 neutral renames, one copied tree each, --selftest each
python3 "$S/fixtures.py"   # positive fixtures, pristine vs survivor through --root
# 13th single-clause mutant (mirrored wording-conjunct probe), same recipe:
#   copy base -> mutants/c2-no-selftest-word, drop "and 'self-test' in verdict.lower()",
#   py_compile, then `<tree>/tools/check-gate-standard-r79.py --selftest`
# then --root differential on fixture fx/c2-code3-noword
```

`drive.py` copies `base/` to `mutants/<name>/`, asserts the target string
occurs **exactly once**, replaces it, runs `py_compile`, then runs
`<tree>/tools/<tool> --selftest` with `cwd=<tree>`, capturing rc and the
`SELFTEST total=` line. Per-mutant transcripts: `MutationCounter/stdout/`.

## Matrix (15 runs: 13 single-clause mutants + 2 neutral renames)

| # | mutant | tool | claim | clause mutated (single) | hunks | selftest rc | verdict | killed by case(s) |
|---|---|---|---|---|---|---|---|---|
| 1 | `c1-seven-rows-equality` | measure-unit-deps | C1 | row-set equality accepts a 7-row prefix (`data != {…}` → prefix compare) | 1 | 3 | **killed** | `quote-DP8`, `line-DP8`, `seven-rows` |
| 2 | `c1-seven-rows-rowcount` | measure-unit-deps | C1 | row-set leg accepts 7 rows (`len(ids) != 8 …` → `len(ids) > 8 …`) | 1 | 0 | **survived** | — |
| 3 | `c1-no-expected-digest` | measure-unit-deps | C1 | frozen `expected.json` digest check removed | 1 | 3 | **killed** | `expected-drift` |
| 4 | `c1-no-line-check` | measure-unit-deps | C1 | quote token-line-range check removed (`locate(...) != row['line']` → `False`) | 1 | 0 | **survived** | — |
| 5 | `c1-no-source-registry` | measure-unit-deps | C1 | S329 registry-resolution leg removed | 1 | 3 | **killed** | `own-work-source` |
| 6 | `c1-one-nonholds` | measure-unit-deps | C1 | review accepts one non-`holds` verdict (`sum(non-holds) > 1`) | 1 | 3 | **killed** | `failed-row` |
| 7 | `c1-duplicate-result` | measure-unit-deps | C1 | duplicate reviewer seat accepted (`len(seats) != 1` → `< 1`) | 1 | 3 | **killed** | `duplicate-result` |
| 8 | `c2-operative-only` | check-gate-standard | C2 | only the operative table counted (`or not non_operative` dropped) | 1 | 3 | **killed** | `unmarked-continuation-duplicate` |
| 9 | `c2-ignore-nonoperative` | check-gate-standard | C2 | `NON-OPERATIVE` marker ignored (`= False`) | 1 | 3 | **killed** | `control`, `marked-continuation` |
| 10 | `c2-no-tool-source` | check-gate-standard | C2 | tool-blob `--selftest`/`SELFTEST` conjunct removed | 1 | 3 | **killed** | `tool-without-selftest` |
| 11 | `c2-accept-shape-one` | check-gate-standard | C2 | exit rule accepts shape 1/2 (`shape == 2` → `shape >= 1`) | 1 | 0 | **survived** | — |
| 12 | `c2-accept-no-code3` | check-gate-standard | C2 | verdict map without code `3` accepted | 1 | 0 | **survived** | — |
| 13 | `c2-no-selftest-word` | check-gate-standard | C2 | verdict map without the `self-test` wording accepted (mirrored probe of 12) | 1 | 0 | **survived** | — |
| 14 | `neutral-c1-rename` | measure-unit-deps | C1 | NEUTRAL `toks`→`tokens` (3 sites) | 1 | 0 | pass (required) | — |
| 15 | `neutral-c2-rename` | check-gate-standard | C2 | NEUTRAL `counted`→`countable` (2 sites) | 2 | 0 | pass (required) | — |

Totals: **killed 8, survived 5, neutral pass 2** (8/13 single-clause mutants
killed, 61.5%). The two neutrals prove the mutator does not merely break
syntax: both renamed trees still run `32/32` and `8/8` clean.

## Survivors — what each one means

Each survivor was then driven through the tool's **live path** (`--root` on a
positive fixture) against the pristine binary on the **same** fixture, to
separate "selftest blank spot with no consequence" from "acceptance loosened".
Raw runs: `MutationCounter/livepath.tsv` (17 rows: 3 C1 fixtures × (pristine +
2 C1 survivors) + 3 C2 fixtures × (pristine + the relevant C2 survivors)).

| survivor | fixture | pristine | mutant | consequence |
|---|---|---|---|---|
| `c2-accept-shape-one` | one good gate row, `tools/` blobs good | rc 1, `duplicates=0 shape_ok=1/2 met=0` | **rc 0**, `duplicates=0 shape_ok=1/2 met=1` | **false green**: exit code and `met` claim the predicate holds while the same line prints `shape_ok=1/2` |
| `c2-accept-no-code3` | two good rows, one verdict map `0 met; 1 missed; 2 could-not-evaluate; self-test failure uncoded` | rc 1, `shape_ok=1/2 met=0` | **rc 0**, `shape_ok=2/2 met=1` | **false green**: a verdict map that never codes self-test failure is counted as gate-standard |
| `c2-no-selftest-word` | two good rows, one verdict map `0 met; 1 missed; 2 could-not-evaluate; 3 uncoded failure` | rc 1, `shape_ok=1/2 met=0` | **rc 0**, `shape_ok=2/2 met=1` | **false green**: a bare `3` unrelated to self-test is counted as the self-test code |
| `c1-seven-rows-rowcount` | 8-row happy path / 7-row bundle / DP3 line-shifted bundle | rc 0 rows=8 · rc 1 `finite-content-mismatch` · rc 1 `finite-content-mismatch` | **identical in all three** | vacuous: the strict-equality leg rejects every row-set divergence before the relaxed clause is reachable |
| `c1-no-line-check` | same three | as above | **identical in all three** | vacuous: any `line` divergence in `DATA` trips strict equality first; a snapshot divergence trips `snapshot-digest` first |

### Findings

1. **F1 (C2, live-path defect invisible to the selftest).** `main()`'s
   accept rule `ok = duplicates == 0 and shape == len(FROZEN_ROWS)` is never
   executed by `run_selftest()`, which only calls `analyze()`. Mutant 11
   therefore reports `met=1`/rc 0 with `shape_ok=1/2`. The summary text still
   discloses `1/2`, so a reader who parses the line sees the shortfall — the
   `met` field and the exit code are what lie. A CI consumer that trusts rc
   would swallow a shape regression. This is a **selftest binding gap**, not
   a defect in the frozen predicate text.
2. **F2 (C2, conjunct pair exercised only jointly).** The shape clause is an
   AND of the code-`3` conjunct (`'3' in re.findall(...)`) and the wording
   conjunct (`'self-test' in verdict.lower()`). The single case that targets
   them, `verdict-without-code3`, uses `0 met; 1 missed; 2 could-not-evaluate`
   — a string that lacks **both** tokens — so removing either conjunct alone
   leaves the suite green (mutants 12 and 13 both survived, measured, not
   inferred). Each survivor is then a false green on a fixture the other
   conjunct would reject: an uncoded `self-test` word, and a bare `3` that
   means something else. The pair is never exercised independently.
3. **F3 (C1, equality shadows three clauses).** With `expected.json` frozen
   and compared by strict `dict` equality, `row-set`, `quote-location` and
   `row-shape` are unreachable for every `DATA`-side perturbation: the
   `line-DP*`, `quote-DP*`, `seven-rows`, `duplicate-id`, `wrong-source` and
   `quote-absent` cases are all answered by `finite-content-mismatch` from the
   equality leg. Mutants 2 and 4 (survivors) and mutant 1 (killed only for
   `quote-DP8`/`line-DP8`) measure this precisely.
4. **F4 (C1, per-row cases test the wrong clause for DP1–DP7).** Mutant 1
   relaxes equality to a `rows[:7]` prefix; the only deep-leg kills it
   produces are `quote-DP8`, `line-DP8` and `seven-rows`. Therefore the
   14 `quote-DP1…DP7` / `line-DP1…DP7` cases pass on the equality clause, not
   on `locate()`: `locate()` is independently exercised for **one** row
   (DP8) out of eight. A regression in `locate()`'s tag-stripping or token
   indexing that DP8 happens not to cover would survive the suite.
5. **O1 (observation, not a defect claim).**
   `check-gate-standard-r79.py:138` reads
   `if table['operative'] or (table['heading'] and table['heading'] == table['heading']):`
   — the second conjunct is tautological, so the filter is always true for
   yielded tables. It is behaviourally inert for every mutant in this battery
   (no mutant targets it, none changes output). Dead weight, recorded for the
   owner, not scored as harm.

### Limits

* The assigned detector is `--selftest`; the `--revision`/`git` path
  (`_revision.bind`) was not mutated. No git fixture was created — creating
  one is outside my authorized command families — so revision binding is
  unprobed here (it is the round-78 routed defect #1, demonstrated separately).
* Mutants are single-clause **by construction**, so I do not claim what
  combinations do; the row-set and quote-location legs are characterised as
  unreachable, not as "would double-count if equality were also relaxed".
* The C1 positive fixtures (`DATA`, companion, `ReviewDeps/verdict.json`,
  `w1-results.json`, a synthesized 11-column S329 registry row) are **my own
  fixture bytes**, not lane artifacts: at probe time
  `grep -c '^| S329 ' corpus/SOURCES.md` was `0` and
  `corpus/knowledge/systemd-dependency-propagation-r79.json` did not exist.
  The differential therefore proves the mutants' behaviour, not the round's
  artifacts.
* A surviving mutant is a coverage finding here; I make no claim that either
  frozen predicate is unmet, and I did not run either counter at `--revision`
  against the claim commit (not my seat).

## Restoration / no-touch evidence

* Never opened a lane file for write. Only `cp` **from** the lane into scratch,
  then edits inside `mutants/<name>/`.
* `sha256sum` read **after** the battery, lane vs scratch base:
  * `measure-unit-deps-r79.py` — `132be669…` == `132be669…`
  * `check-gate-standard-r79.py` — `0b32ddbc…` == `0b32ddbc…`
* No git/jj command of any kind was run; no repository was created; no
  `/tmp` write; scratch tree deleted before yield.
* Tooling: nothing installed or updated (no pacman, no uv, no npx).

## Evidence files

* `MutationCounter/matrix.json` — 15 runners, clause edits, hunk counts,
  `py_compile_rc`, `selftest_rc`, `killed_by`, verdicts, live-path
  differential (17 runs), exact commands, frozen input digests.
* `MutationCounter/stdout/<mutant>.stdout.txt` — full `--selftest`
  transcript per runner (15 files).
* `MutationCounter/livepath.tsv` — 17 pristine-vs-mutant `--root` runs.
