
# MutDigit10 — held-out mutants of the digit cap and the probe suffix guard (round 94, wave w1)

Seat: mutation-tester (leaf, no dispatch). Lane: `tsukuroi-shokunin`, freeze
`eb3b3e5150a63507a382003fa1a70039b190396b`. Scratch: `/fast/scratch/hyaku/tsukuroi-r94/MutDigit10/`
(deleted on exit; every artifact below is copied into the receipts dir `.ufo/waves/round-94/w1/MutDigit10/`).
Host: `limine --version` = `Limine 12.9.4`; `bwrap` present; 32 cores. Runs executed with `&`/`wait`,
each its own `--work`: 12 r94 batteries `--runs 1` (M00 control + M01–M11), the two survivors
`--runs 2` (4 more runs), and 7 runs of the frozen r93 roster (M00, M01, M02, M03, M06, M09, M10).
Receipts: `.ufo/waves/round-94/w1/MutDigit10/` (this report is its `.md` sibling one level up).

## Instruments (verified read-only, never edited)

| instrument | sha256 | status |
|---|---|---|
| `tools/check-limine-pins.py` | `7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32` | matches tasking |
| `tools/limine-pin-battery-r94.py` | `d66b4a59778f8d5d006259d275875f95f002430b0e41990a111d73b6dc7bb503` | matches tasking |
| `.ufo/waves/round-94/before/controls/do-nothing-gate-r93.py` | `6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa` | matches tasking |
| `.ufo/waves/round-94/before/controls/do-nothing-battery-r93.py` | `ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad` | matches tasking |

`sha256sum -c .ufo/waves/round-94/before/freeze-manifest.sha256` → 12/12 `OK` before and after the seat.
The landed gate was re-hashed after all runs: unchanged. No mutant ever ran from the lane.

## Axes (named before the first run)

- **A1 discrimination** — does a one-clause mutant of the clause a family certifies turn that family
  `unmet` (not merely a non-`met` battery for some other reason)?
- **A2 attribution** — is the killer the *named new* family, with `0` error rows (a real row-level
  disagreement, not a harness error or a bystander family)?
- **A3 load-bearing** — does the pre-r94 roster (96 families, no r94 family) *miss* the same mutant?
  A family that kills nothing the old roster missed is decoration.
- **A4 stability** — every survivor re-run `--runs 2` (`98/98` unmet-or-met must be identical).

Moves kept only if they raised A1–A4 (a mutant that kills nothing is kept as a coverage finding, not
deleted: A3 on survivors is the point of the probe).

## Method

`gen_mutants.py` reads the pristine gate bytes, asserts the tasking hash, applies exactly one textual
clause change per mutant with `assert count(anchor) == 1`, writes a copy, and `compile()`s it. A cheap
in-process pre-flight (`microcheck.py`: `parse_limine_version` on 10 values + a monkeypatched
`probe_limine_version`) confirmed each copy bends its clause *before* spending a 90 s battery.
Each mutant then ran `tools/limine-pin-battery-r94.py --gate <copy> --runs 1 --work <own dir> --json`.
`families_passed`, `failed_families`, `error rows` (case-log entries with non-null `error`) and the
failing row's `want`/`got` were read from the JSON. Survivors: `--runs 2`.

## Results — r94 battery (`--runs 1`, 392 cases = 98 families x 4)

| ID | one-clause bend (copy of the landed gate) | families_passed | failed_families | error rows | r93 roster (96) | verdict |
|---|---|---|---|---|---|---|
| M00 | none (byte-identical control copy) | **98/98 met** | — | 0 | 96/96 met | control OK |
| M01 | digit bound `<= 9` → `<= 10` | 97/98 unmet | `REFUSAL-VERSIONS-10DIGIT` | 0 | **96/96 met** | **KILLED** (new family) |
| M02 | probe suffix guard `(?![\w.-])` removed | 97/98 unmet | `AUTO-PROBE-SHAPES` | 0 | **96/96 met** | **KILLED** (new family) |
| M03 | digit bound `<= 9` → `<= 11` | 97/98 unmet | `REFUSAL-VERSIONS-10DIGIT` | 0 | **96/96 met** | **KILLED** (new family) |
| M04 | `parse_limine_version` deleted (accepts anything) | 91/98 unmet | `REFUSAL-VERSIONS-10DIGIT`, `REFUSAL-VERSIONS`, `AUTO-ERA-B`, `ERA-B-FIRST-BODY`, `ERA-EXACT-125`, `ERA-FLE-MEASURED-B`, `ERA-FLE-PANIC-B` | 0 | n/a | **KILLED** |
| M05 | malformed-version usage refusal `return 64` → `return 1` | 96/98 unmet | `REFUSAL-VERSIONS-10DIGIT`, `REFUSAL-VERSIONS` | 0 | n/a | **KILLED** |
| M06 | probe reads `p.stdout + p.stderr` | 97/98 unmet | `AUTO-PROBE-SHAPES` | 0 | **96/96 met** | **KILLED** (new family) |
| M07 | probe takes the **last** guarded `X.Y.Z` (`findall[-1]`) | **98/98 met** x3 | — | 0 | n/a | **SURVIVED** (see F1) |
| M08 | era split `>=` → `>` (12.9.5 boundary) | 97/98 unmet | `ERA-EXACT-125` | 0 | n/a | **KILLED** (r93 family) |
| M09 | digit bound `<= 9` → `<= 8` (9-digit boundary refused) | **98/98 met** x3 | — | 0 | **96/96 met** | **SURVIVED** (both rosters; see F2) |
| M10 | bound widened so only position 2 is unbounded | 97/98 unmet | `REFUSAL-VERSIONS-10DIGIT` | 0 | **96/96 met** | **KILLED** (new family) |
| M11 | blanket refusal (`parse_limine_version` → `None`) | 3/98 unmet | 95 families, incl. `REFUSAL-VERSIONS-10DIGIT` **on its `12.9.4` row** | 376 | n/a | **KILLED** (see F3) |

Mutant sha256 (full table in `mutants/`): M00 `7d79ac29…`, M01 `a0e116ff…`, M02 `bcb487dc…`,
M03 `2dd63c7c…`, M04 `c2eb0e3e…`, M05 `ddff6cfd…`, M06 `7f8fef45…`, M07 `f8861fdc…`,
M08 `d1f48300…`, M09 `fa807780…`, M10 `105481bd…`, M11 `22bd14a3…`.

### Row-level evidence that the *named* family, not a bystander, is the killer

| mutant | failing row, verbatim from the case log |
|---|---|
| M01 | `REFUSAL-VERSIONS-10DIGIT` want `[64, "usage"]`, got `'1234567890.0.0' rc=0 stdout=349; '0.1234567890.0' rc=0 stdout=352; '0.0.1234567890' rc=0 stdout=352; '1234567890.123456789' rc=0 stdout=367` |
| M02 | `AUTO-PROBE-SHAPES` want `[64, "usage"]`, got `'auto' rc=0 stdout=870` |
| M03 | same four ten-digit rows as M01, all `rc=0` with a verdict on stdout |
| M06 | `AUTO-PROBE-SHAPES` want `[64, "usage"]`, got `'auto' rc=0 stdout=934` |
| M10 | `REFUSAL-VERSIONS-10DIGIT` want `[64, "usage"]`, got `'0.1234567890.0' rc=0 stdout=352` — **only** the second-position value leaks |
| M08 | `ERA-EXACT-125` want `panic`, got `prompt` at version `12.9.5` |
| M04 | `AUTO-ERA-B` want `panic`, got `prompt` at probed `12.9.6` (parser deleted ⇒ 12.9.4 era) |
| M11 | `REFUSAL-VERSIONS-10DIGIT`, got `'12.9.4' rc=64 stdout=0` — the family's own healthy control row |

Every killed mutant: `error rows = 0`. No kill depended on a harness failure.

## Findings (coverage findings; no contract change proposed)

**F1 — M07 SURVIVED: the probe's published "first `X.Y.Z`" clause is unexercised.**
`probe_limine_version`'s docstring says it returns the *first* `X.Y.Z` immediately following `limine`.
M07 returns the *last*. No family (nor the gate selftest: `--selftest` rc 0 on M07) ever feeds two
guarded versions, so the mutant is invisible. Exact counterexample, driven through the real CLI with a
fake `limine` printing `Limine 12.9.4` then `Limine 12.9.6` on stdout, `--limine-version auto` on a
first-line-entry config:

```
pristine: limine_version 12.9.4, source probe, visibility_era pre-12.9.5,
          hash_mismatch_panic {"line": 2, "value": "no"}      rc 0
M07:      limine_version 12.9.6, source probe, visibility_era 12.9.5+,
          hash_mismatch_panic null                            rc 0
```

So M07 is not equivalent: it moves the era and silently drops the visible global key. The clause is
real but no roster member or selftest case pins it. (Not a claim break: C1's families certify the
*refusal* shapes, not "first vs last".)

**F2 — M09 SURVIVED the 98-family roster: the accepted 9-digit boundary lives only in `--usage-check`.**
`REFUSAL-VERSIONS-10DIGIT` deliberately enumerates *only* ten-digit values plus the `12.9.4` control;
the 9-digit accepted boundary `999999999.0.0` is in `usage_check()`'s table, which the family roster
never runs — and the gate selftest passes on M09 (`rc 0`), as does the frozen r93 roster
(`96/96 met`). Counterexample: on the healthy fixture, `--limine-version 999999999.0.0` leaks a
verdict from pristine (`rc 0`) while M09 refuses `rc 64` with empty stdout;
8-digit `123456789.0.0` likewise refused. Cross-check: `battery --usage-check` on M09 → `unmet`, bad row
`('999999999.0.0', rc 64, want 0)`; pristine control `met`, 15/15. `--usage-check` also kills M01
(`1234567890.0.0`, `0.1234567890.0` → rc 0, want 64) and M10 (`0.1234567890.0`), so the boundary is
instrumented — just outside the 98 families the claim counts.

**F3 — `REFUSAL-VERSIONS` alone cannot see blanket refusal; the `12.9.4` control row inside
`REFUSAL-VERSIONS-10DIGIT` is what does.** M11 refuses every version and yet **passes**
`REFUSAL-VERSIONS` (that family's list holds no in-range value), `AUTO-PROBE-FAIL` and
`AUTO-PROBE-SHAPES`; it fails `REFUSAL-VERSIONS-10DIGIT` solely on its healthy control row
(`'12.9.4' rc=64 stdout=0`). The claim's "healthy 12.9.4 control row inside the same family reads a
verdict" is load-bearing, exactly as stated.

**F4 — the r93 roster is blind to all five new-family kills.** M01, M02, M03, M06 and M10 each read
**96/96 `met`, 0 error rows** under `.ufo/waves/round-94/before/controls/do-nothing-battery-r93.py`
(M00 control: 96/96 `met`). The two r94 families therefore add discriminating power the frozen r93
roster lacks — the depth claim's core assertion, measured rather than asserted.

**F5 — `AUTO-PROBE-SHAPES`'s stderr shape is not in the family** (the battery docstring says so
explicitly). M06 (probe reads stdout **and** stderr) is still killed because the two *stdout* shapes
suffice; a probe that read **only** stderr would fail `AUTO-ERA-A`/`AUTO-ERA-B` instead (those fakes
print to stdout). So stderr is covered indirectly, not by the family.

## C2 corroboration (observed, not a mutant probe)

On the pristine copy: flag-free run with `limine` absent from `PATH` → `rc 64`, **stdout 0 bytes**,
stderr `--limine-version auto: \`limine --version\` probe failed`; flag-free run with a fake answering
`Limine 12.9.6` → `limine_version 12.9.6`, `limine_version_source probe`, `visibility_era 12.9.5+`,
`hash_mismatch_panic null`; the same config with `--limine-version 12.9.4` → `source flag`,
`pre-12.9.5`, key visible. `--selftest` prints `selftest PASS 39/39`, rc 0.

## Restoration evidence

Every mutant is a copy under this seat dir (`mutants/`), generated by `gen_mutants.py` from the fixed
pristine hash. The landed `tools/check-limine-pins.py` was hashed before
(`7d79ac29…`) and after (`7d79ac29…`) all runs: byte-identical, and `sha256sum -c` of the freeze
manifest is 12/12 `OK` after the seat. No git/jj mutation was run in the lane; scratch
`/fast/scratch/hyaku/tsukuroi-r94/MutDigit10/` was deleted on exit.

Artifacts: `mutants/*.py` (12 copies), `gen_mutants.py`, `results-r94.json` (per-mutant
`families_passed`/`failed_families`/`error_rows`/failing rows), `results-r93.json` (r93-roster
blindness matrix), `results-usage-check.json` — all in `.ufo/waves/round-94/w1/MutDigit10/`.

## Verdict

Supports **C1 (depth 8)** — the two new families are load-bearing and precisely attributed:
`REFUSAL-VERSIONS-10DIGIT` kills M01/M03/M04/M05/M10/M11 and `AUTO-PROBE-SHAPES` kills
M02/M04/M06, each as the sole or named killer with 0 error rows, while the same mutants read 96/96
`met` under the frozen r93 roster (receipts: this file, `results-r94.json`, `results-r93.json`).
Corroborates **C2**'s probe-default/refusal contract via direct CLI runs and `selftest PASS 39/39`.
Does **not** falsify either claim. Two surviving mutants are coverage findings, not claim breaks:
M07 (probe "first vs last guarded match" is unpinned by every roster and by selftest) and M09
(the accepted 9-digit boundary `999999999.0.0` is certified only by `battery --usage-check`, not by
the 98 families) — `results-usage-check.json`.
