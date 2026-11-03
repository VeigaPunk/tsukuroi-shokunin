# M1MutBattery — MUT-BATTERY (mutation probe of the cited-receipt landing gate)

Seat M1MutBattery, round 65 (hyaku run 15), wave w1. Execution class READ-ONLY.
Target: `tools/check-cited-receipts-r62.py` (sha256 `04e9703d5c57909303df930c39ca610c2212af54c87cc0ef5d0bd998f4fdadba`, 351 lines,
PASS 0 / FAIL 1 / CANNOT 2, 4 selftest cases). Lane HEAD `37c74e27`. Python 3.14.8.
Deliverable: `.ufo/waves/round-65/w1-artifacts/M1/mutation-report.txt` (+ `receipts/`).

## What I did

Copied the gate byte-for-byte into scratch, established both controls, built five single-line
mutants (one per file), ran one fixed detector suite over pristine + each mutant, then built and
exercised two candidate selftest patches (patch text only — **not applied**) to prove they close
the two gaps the mutants exposed. The lane tool was never edited or executed as a mutant.

## Operability facts established first (they change how the gate is invoked)

- **O1** `--revision` is mandatory with `--round`: `--round 61` alone exits **2** via argparse; it does
  not default to HEAD. The red expectation must spell the revision (`bcf1af18`, as the r62 receipt pins).
- **O2** `--lane` defaults to the *script's* grandparent dir, not the cwd. A scratch/temp copy cannot bind
  a revision unless `--lane <lane>` is passed: without it, `--revision 37c74e27 --round 65` → `CANNOT` rc 2.

## Controls (pristine)

| # | command (rc) | output |
|---|---|---|
| C1 | `--selftest` (rc 0) | `selftest PASS`, 4 ok cases |
| C2 | `--lane <lane> --revision bcf1af18 --round 61` (rc 1) | `FAIL`, finding_count **3**, exact set matches `.ufo/waves/round-62/before/cited-receipts-at-base-round61.json` |
| C3 | `--lane <lane> --revision 37c74e27 --round 61` (rc 0) | `PASS`, 0 findings, cited_paths 5 |
| C4 | `--lane <lane> --revision 37c74e27 --round 65` (rc 0) | `PASS`, 0 findings, **cited_paths 0** (green by emptiness) |

## Mutants — one line each, scratch copies only

| mutant | mutation | D1 selftest | D2 red (exact) | D3 green | verdict |
|---|---|---|---|---|---|
| M1 allow-all | `findings = []` | FAIL (ghost case) | FAIL (PASS, 0) | PASS | **KILLED** |
| M2 selftest-blind | `ok = True` | PASS | PASS (scan intact) | PASS | **SURVIVED** — killed only by meta-detector |
| M3 exit-inversion | `return ..., FAIL if not findings else PASS` | FAIL | FAIL (JSON FAIL, rc 0) | FAIL (rc 1) | **KILLED** |
| M4 tree-scope hole | skip `p.startswith(".ufo/waves/")` | FAIL | FAIL (PASS, 0) | PASS | **KILLED** |
| M5 batch-partial | `findings[:1]` | PASS (1-ghost fixture) | FAIL (count **1**) | PASS | **KILLED only by count+set assertion** |

Kill tally: D2 red-exact 4/5, D1 2/5, **D3 green 1/5**. A PASS-only evidence style distinguishes only M3.

Meta probe: M2 stacked on M1 (`ok = True` over allow-all scan) → `--selftest` **PASS rc 0** while its own
`head-finds-ghost` case prints `ok:false`. The suite has no teeth against its own blindness.

## Gap-closing patches (validated on scratch copies, NOT applied)

- **P1 `--mutate-selftest`** (closes M2): copies the file, injects the allow-all line, runs `--selftest`
  on the copy, requires RED. Measured: pristine → `mutation_selftest PASS` (mutant_exit 1) rc 0;
  M2 → `FAIL` (mutant_exit 0) rc 1; M3 → PASS; M1/M4/M5 → `CANNOT` (anchor reshaped — fails closed).
- **P2 Case 5 `batch-complete`** (closes M5): three-ghost fixture asserting `finding_count == 3` **and** the
  exact path set. Measured: pristine → PASS 5 cases rc 0; M5 → FAIL, `batch-complete ok:false` rc 1.
  If landed, the suite becomes **5** cases, so any "PASS 4 cases" landing row must move to 5.

## Defects / coverage findings (no contract change proposed)

- **F1** The selftest cannot detect its own blindness (`ok = True` leaves D1–D3 green). Must be closed by
  test-the-test (P1), not by another internal case — the mutation sits downstream of `results`.
- **F2** Batch completeness is held only by an out-of-band revision run; the fixture has one ghost, so a
  truncation is invisible to `--selftest` (P2 closes it internally).
- **F3** A green-only check kills 1/5; the r59 count rule is exactly what M5 breaks, so a round that
  reports only "PASS at the final tree" has near-zero discriminating evidence.
- **F4** At `37c74e27 --round 65` the gate is green with `cited_paths 0`, byte-identical to M1's output:
  until this round's committed bytes cite a `.ufo/waves/round-65/` file, the round's own PASS carries
  no information. Not a tool defect — a limit on using round-local PASS as evidence.
- **F5** Mirrors the docstring's honest limit: a citation *set* can be under-reported with no single
  citation wrong, on exactly the single-ghost fixture shape.

## Commands run (rc)

`cp`+`sha256sum` (0, hashes equal) · `python3 work.py --selftest` (0, PASS 4) ·
`python3 work.py --round 61` (**2**, argparse — O1) · `--revision 37c74e27 --round 65` w/o `--lane`
(**2**, CANNOT — O2) · `--lane … --revision bcf1af18 --round 61` (**1**, FAIL 3) ·
`--lane … --revision 37c74e27 --round 65` (0, PASS cited 0) · `--lane … --revision 37c74e27 --round 61`
(0, PASS cited 5) · `build_mutants.py` (0) · `drive.py` (0, matrix) · `diff -u work.py mut-*.py`
(1 = differences, expected) · `patch_case5.py` + runs (pristine 0 / M5 1) · `patch_meta.py` + runs
(pristine 0 / M2 1 / M3 0 / M1,M4,M5 2 CANNOT) · `sha256sum` before/after lane tool (identical) ·
`git status --porcelain` (only pre-existing entries) · `rm -rf` scratch, verified absent (0).

## Files written (lane)

- `.ufo/waves/round-65/w1-artifacts/M1/mutation-report.txt`
- `.ufo/waves/round-65/w1-artifacts/M1/receipts/` — pristine + 5 mutants + matrix + 3 control JSONs + 2 patched copies
- `.ufo/waves/round-65/w1/M1MutBattery.md` (this file)

No tracked lane file modified; no mutating git/jj command; no host write; no network; no delegation.
Scratch `/fast/scratch/hyaku/tsukuroi-r65/M1MutBattery` removed after receipts were copied out.
