# MT1Guard — C1-MUTATION (lane round 64, wave w1)

UTC: 2026-11-03T18:44:35Z
Role: mutation-tester (L2 seat).
**Verdict: killed 5/5, survivors: none.**
Target: `tools/check-line-endings-r64.py` (written concurrently by seat E1LineEnd).
Full receipt: `.ufo/waves/round-64/after/mutation/mutation-report.txt`

## Axes

| axis | pristine | worst mutant | verdict |
|---|---|---|---|
| guard detects CR at any position | yes | M1 blind to all | killed |
| guard / allowlist boundary | `.ufo` top-level only | M2 inverted | killed |
| exit-code contract | 0 clean / 1 dirty | M3 inverted | killed |
| CR-at-EOF without newline | flagged via case 4 | M4 blind | killed |
| guarded-set membership | `tools/*.py` included | M5 dropped | killed |
| **tool's own `--selftest` as the gate** | green | **M3, M5 stay green** | **gap** |

## Target identity — the repo file was never written

E1LineEnd rewrote the target while I worked. Observed hashes:

```
18:39:55Z  ff4b655262eec441…  11965   session start (transient)
18:40:50Z  75108a81a0248abd…  11600
18:41:40Z  75108a81a0248abd…  11600   stable, 6 x 10 s samples
18:43:04Z  5a42b4c8c6ab2083…  12417   moved again after my first full run
18:43:24Z  15f0e65c889acc3b…  12858
18:44:35Z  15f0e65c889acc3b…  12858   stable at session end
```

A complete first run against `75108a81` also killed 5/5, but the file then changed **shape**
(`check_paths()` 4-tuple → 3-tuple, missing-file raises instead of counting, `guarded_set()`
returns `(paths, allowlisted_count)`, `is_allowlisted()` anchored to the leading component,
`report()` gained the allow-list disclosure line). So every receipt here is **re-derived from
the settled `15f0e65c` bytes**; the earlier run is not cited.

```
$ sha256sum tools/check-line-endings-r64.py
15f0e65c889acc3b591ca44c7e52fe16fa14d79c367e743ebcc905b17d50c030  tools/check-line-endings-r64.py
rc=0                                          # identical at snapshot and session end
$ cmp tool-pristine-snapshot.py <lane>/tools/check-line-endings-r64.py ; rc=0
```

The snapshot kept beside the report (`tool-pristine-snapshot.py`) is byte-identical to the
repo file. The file is untracked (`?? tools/check-line-endings-r64.py`), so the sha is the
identity anchor.

## Method

Copies only, under `/fast/scratch/hyaku/tsukuroi-r64/MT1Guard/`. Three detectors, each run
against pristine, mutated and restored bytes:

- **D1** `--selftest --work <scratch>/work` — the tool's own five-case suite (the gate L1 runs).
- **D2** `--check --root <scratch>/fixtures/dirty` — default guarded set over a hermetic
  fixture tree; `git` is shimmed (a PATH wrapper answers `ls-files -z` from a fixed list), so
  no real repo is read and no git state is touched.
- **D3** `--check --root <scratch>/fixtures/clean` — same tree, all clean → exit contract.

Fixture, 9 tracked paths: `corpus/ok.md`, `corpus/bad.md` CRLF, `plans/ok.md`,
`plans/eof.md` CR-at-EOF, `tools/good.py`, `tools/bad.py` CRLF, `SKILL.md`,
`.ufo/waves/cap.txt` CRLF (must skip), `docs/notes.txt` CRLF (unguarded, must ignore).

Baseline green on all three, so the run is conclusive:

```
D1 rc=0  CHECK_LINE_ENDINGS_SELFTEST: PASS (5 cases, 5 passed, 0 failed)
D2 rc=1  3 violation(s) -> corpus/bad.md:1, plans/eof.md:2, tools/bad.py:1
         CHECK_LINE_ENDINGS: FAIL (7 file(s) checked, 3 violation(s))
         check-line-endings-r64: 1 allow-listed .ufo path(s) skipped (upstream captures)
D3 rc=0  CHECK_LINE_ENDINGS: PASS (7 file(s) checked, 0 violation(s))
```

## Results

| mutant | patch | D1 selftest | D2 dirty set | D3 clean exit | verdict |
|---|---|---|---|---|---|
| **M1** allow-all | `hit = first_cr(path)` → `hit = None` | FAIL 2/5 | rc 0, PASS (was FAIL) | unchanged | **KILLED** |
| **M2** allowlist-inversion | `is_guarded`/`is_allowlisted` bodies swapped | FAIL 4/5 | rc 1, only `.ufo/waves/cap.txt:1` | rc 1 on clean tree | **KILLED** |
| **M3** exit-inversion | `return FAIL if violations else PASS` → reversed | **PASS 5/5** | prints FAIL, rc 0 | prints PASS, rc 1 | **KILLED** (D2+D3) |
| **M4** cr-at-eof-blindness | swallow CR when `idx == len(chunk)-1` | FAIL 4/5 | drops `plans/eof.md:2` | unchanged | **KILLED** |
| **M5** guard-set-shrink | delete `tools/*.py` branch of `is_guarded` | **PASS 5/5** | 5 checked / 2 violations | 5 checked (was 7) | **KILLED** (D2+D3) |

Evidence files: `mutant-diffs.txt` (all five unified diffs), `mutation-results.json` (machine
output incl. full stdout/stderr per detector), `tool-M1.py … tool-M5.py` (mutant sources),
`tool-pristine-snapshot.py`, `harness.py` (the rig that produced all of it).

Restoration: no-op by construction. No mutant targeted the repo path; the repo sha256 is
unchanged (`15f0e65c…` → `15f0e65c…`), and the working copy is `cmp`-verified against it.

## Routed coverage finding (not a contract change)

All five mutants die — but two die **only** under D2/D3. The tool's own `--selftest` stays
green under M3 and M5. Structural proof from the settled bytes:

```
selftest cases            : lf-file-passes, crlf-file-fails-naming-path,
                            allowlisted-ufo-path-ignored, cr-at-eof-without-newline-flagged,
                            cr-midline-flagged
check_paths() calls in run_selftest : 5
is_guarded  references in run_selftest : 0
report(     references in run_selftest : 0
```

- **M3 survives the selftest** — no case asserts a return code; every case calls
  `check_paths()` and inspects the violations list. Missing case: `exit-code-contract`
  (`main(["--check", dirty]) == 1`, `main(["--check", clean]) == 0`).
- **M5 survives the selftest** — `is_guarded()` is never called: cases 1–2 pass explicit
  paths (`guarded/lf.md`), so only `is_allowlisted()` is consulted. Missing case:
  `tools-python-is-guarded` (`is_guarded("tools/x.py") is True` + a default-set scan that
  flags a CR there). CANONICAL membership is unexercised for the same reason.

C1's operability claim still holds: real detection comes from `guarded_set()`, so D2/D3 killed
both mutants on checked-file counts and violation lists. The exposure is future regression —
an edit to `report()`'s return value or to `is_guarded()` would ship green through the
selftest gate. Recommendation for E1LineEnd: add the two named cases. I did not edit the tool.

## Tooling / scratch

No installs — nothing needed (Python 3.14.8, git 2.56.0 present); no pacman, no PATH-dir
writes. Scratch `/fast/scratch/hyaku/tsukuroi-r64/MT1Guard/` removed after receipts landed
under `.ufo/waves/round-64/after/mutation/`. No commit, no push, no git/jj mutation.
