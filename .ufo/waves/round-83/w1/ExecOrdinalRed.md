# ExecOrdinalRed — round 83 w1 — red-before proof, ordinal counter (C2 calibration)

Scope: red-control proof for `tools/check-ordinals-r83.py` at freeze d78b3b3982b5df62286dd65b0a42ae8a91847608. Full commands, sha256s and raw outputs: `ExecOrdinalRed/receipts.txt` and `ExecOrdinalRed/results-raw/`.

## Verdict

- Pristine counter: C2 4/4 at the freeze, selftest 11/11, pinned sha256 `abc7e037…f5f` matches `instrument-sha256.txt`.
- Three mutants, each a RED CONTROL (causes at least one C2 leg to miss):

| Mutant | Edit (scratch copy only) | Selftest | Battery C2 | Failing leg(s) and observed |
|---|---|---|---|---|
| O-GLOBAL | `measure()` line 121 `range(i+1, …)` → `range(len(seen))` | rc3, 10/11 (late-contradiction) | 3/4, rc1 | **C2.a**: rc0 clean where rc1 required |
| O-NOCODE | `assertions()` line 81 `CODE.sub("", line)` → `line` | rc3, 10/11 (quoted-prose-not-assertion) | 2/4, rc1 | **C2.b**: rc1 finding (`depth 8→9` quoted); **C2.c**: rc1 finding on the real SCORECARD |
| O-TRACEBACK | `main()` --revision: `try/except CannotEvaluate` around `read_scorecard_at` (lines 258-263) removed | rc0, 11/11 | 3/4, rc1 | **C2.d**: rc1, empty stdout, Python traceback `CannotEvaluate: absent-at-revision:SCORECARD.md` |

- Pristine battery: `C1 3/3, C2 4/4`, rc0. Expected legs C2.a rc1 / C2.b rc0 / C2.c rc0 / C2.d rc2 JSON all observed.

## Findings for the L1

1. **Selftest blind spot (O-TRACEBACK).** `--selftest` has 11 cases, all calling `measure()`. None reaches `main()` or the `--revision` path, so the R82-V3 traceback class passes `--selftest` rc0. Only battery leg C2.d catches it. Proposed patch for the L1 (not applied, scratch only): add a selftest case that runs `main(["--repo", <no-SCORECARD fixture repo>, "--branch", <br>, "--revision", <head>])` and asserts rc2 and a JSON `cannot-evaluate` line on stdout.
2. **CODE stripping is load-bearing on the real tree.** Without it (O-NOCODE), the real SCORECARD at REV produces a finding (depth 81, ordinals [8,9]) — the round-82 correction-block quotation. The pristine counter is correct here; no patch needed.
3. **O-GLOBAL survives the real tree.** The global-retirement defect is caught only by C2.a (the late-contradiction fixture) and the selftest `late-contradiction` case; C2.c still reads clean (examined 80 vs 81). This confirms C2.a is the only leg that detects R82-V2, as the declaration states.

## Limits
- Mutants O-GLOBAL/O-NOCODE/O-TRACEBACK were produced by minimal single-site edits; other R82-V2/V3-shaped variants were not enumerated.
- Battery run once per variant; no repeat runs (deterministic inputs).
- Lane root not modified; no commits; no tools installed (python3 stdlib, git only).

Refused: none.
