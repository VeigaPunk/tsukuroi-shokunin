VERDICT: defect-found

# R51MutC3a — C3 counter mutation test (item C3-A4)

Pinned counter: `tools/check-adjacency-table-r51.py` at 2732ee6c06108c031c4d8043239b994e0504eb2f,
sha256 3d09a8e94a9075f6de12c03fe1f678d77a3af1f23e18ed887c58a700b44cf380 (matches FROZEN-hashes.txt).
Battery: `.ufo/waves/round-51/controls/battery.py`, function `c3_battery`, sha256 12eeffb5…8888 (unmodified; not edited, not run through `main()`, so no summary file was written into the lane).

## Method
- Five fixture clones (`git clone --shared` of the lane, detached at the pin) under `/fast/scratch/hyaku/tsukuroi-r51/R51MutC3a/`: `base`, `M1`..`M4`. Each mutant is one `edit` of that clone's `tools/check-adjacency-table-r51.py`; the diffs are in receipts (`mutant-M<n>.diff`). The counter resolves its round-50 legs and default lane from its own directory, so each clone is self-contained.
- `drive.py` imports `battery.py` (copied to scratch) and calls `c3_battery(REV, scratch)` with `C3` patched to the mutant's file. The lane's battery is unedited.
- Mutants:
  - M1: displayed-commit prefix check dropped (`check-adjacency-table-r51.py:107-108` deleted).
  - M2: displayed-quote check dropped (`:111-112` deleted).
  - M3: `quote_line` test dropped (`:127` condition replaced by `if False:`).
  - M4: `digests_bound` returns constant 10 (`:161` `return n` → `return 10`).
- Verdict mapping: a control is "killed" when its `as_expected` becomes false (expected CONTROL-FAIL becomes CONTROL-PASS, or expected PASS becomes FAIL). "SURVIVES" = all seven controls still as expected.

## Baseline (unmutated pin)
`out-base.jsonl`: 7/7 as expected. It reproduces `battery-summary-r51-freeze-c3.jsonl` exactly (Python equality: True). K0 CONTROL-FAIL (display_bound_ok 9); K1 OVERRIDE-NOT-MEASURED rc 3; K2 CONTROL-FAIL; K3 CONTROL-FAIL; K4 CONTROL-FAIL (quote_specific_ok 9); K5 CONTROL-FAIL (digests_bound_ok 9); K-pass PASS rc 0.

## Results (receipts: `out-M1..M4.jsonl`, run log in this session)

| Mutant | Controls flipped (as_expected false) | Result |
|---|---|---|
| M1 commit prefix dropped | K-pass: PASS → **FAIL** (display_forge_fails 1 → 0) | **Killed**, but only by the measurement control. K0 stays CONTROL-FAIL: its `display_bound_ok` moves 9 → 10 yet the verdict is unchanged, because the verdict is held by `display_forge_fails` (also 0). No CONTROL-FAIL → CONTROL-PASS flip. |
| M2 displayed quote dropped | **none** — K0..K5 and K-pass all as expected; `out-M2.jsonl` is byte-identical to `out-base.jsonl` | **SURVIVES. Control gap.** |
| M3 quote_line test dropped | K4: CONTROL-FAIL → **CONTROL-PASS** (quote_specific_ok 9 → 10, all other legs unchanged) | **Killed** |
| M4 digests always 10 | K5: CONTROL-FAIL → **CONTROL-PASS** (digests_bound_ok 9 → 10) | **Killed** |

Leg-level movement without verdict flip (informational): M4 also changes K2 (digests 0 → 10) and K3 (digests 9 → 10); M1 changes K0's `display_bound_ok` 9 → 10. The battery compares only the verdict string (`battery.py:199-206`, `as_expected` = `got == expect`), so these leg changes are invisible to the battery.

K1 (override short-circuit, rc 3) is unaffected by all four mutants; it cannot kill any mutant that does not touch the override path. Noted, not a gap in M1–M4.

## The M2 gap and a control that closes it
No K-control forges the displayed quote. A naive forgery does not isolate it: replacing the displayed OUT-010 quote with non-pinned text (`receipts/fixture-displayed-quote-altered.md`) also changes the round-50 `quote_at_pin_ok` leg (9 → 8), so the verdict is CONTROL-FAIL under both the pin and M2 — the r50 leg masks M2.

The isolating fixture substitutes a different real line of the pinned tameshi blob (commit `01d586ddbc5f…`, `PROVINCE.md`, line not containing the registry quote) for the displayed OUT-010 quote (`receipts/fixture-displayed-quote-substituted.md`; substitute string in `receipts/substituted-quote.json`). Output (`receipts/probe-substituted-quote.txt`):

- base: CONTROL-FAIL, display_bound_ok 9, quote_at_pin_ok 9, display_forge_fails 0
- **M2: CONTROL-PASS**, display_bound_ok 10, display_forge_fails 1
- M1, M3, M4: CONTROL-FAIL (as expected)

So M2 is killed by a control of the expected form (CONTROL-FAIL → CONTROL-PASS) once this fixture exists. Proposed addition to `c3_battery` (proposal only; battery.py not edited):

```python
    # K6: displayed OUT-010 quote replaced by another line of the pinned blob (quote_at_pin stays 9)
    sub = json.load(open(os.path.join(d, 'substituted-quote.json')))  # or inline the literal:
    # sub = '**Domain:** verification-fixture craft — the reusable method of honest'
    prov6 = prov.replace(REG_OUT010_QUOTE, sub, 1)   # REG_OUT010_QUOTE = registry OUT-010 quote (appears once in the row)
    assert prov6 != prov
    q6 = _w(d, 'substituted-quote', prov6)
    score('K6 displayed OUT-010 quote replaced by a real line of the pinned blob', 'CONTROL-FAIL',
          ['--control', '--province-file', q6], want_rc=1)
```

Recommended hardening (same change): assert the leg, not only the verdict, e.g. `legs['display_bound_ok'] == 9` for K0 and K6, and `legs['digests_bound_ok'] == 9` for K5. This turns the M1 and M4 kills into per-control kills and removes the reliance on the redundant `display_forge_fails` leg.

## Gap check on the probe
Under M2 the K6 verdict is CONTROL-PASS while `display_forge_fails` is 1. The forgery leg is still fine under M2 because M2 keeps the commit check, which is the leg the forgery exercises. This is why the K6 flip is clean. Under the pin the same fixture fails only on display_bound (9).

## Not done / limits
- No selftest, no lane write, no edit of the battery or counter. Scratch removed after copying receipts (see below).
- Mutants are single-point; combined mutants and the r50 legs were not mutated.
- The K6 proposal was validated only against the four mutants above; it was not run through the lane battery (that is the L1's call).
- Tools installed: none.
- Host hygiene (observed, not caused by this seat's commands): `controls/__pycache__/battery.cpython-314.pyc` exists in the lane, mtime 18:17:04 today; this seat imported only its scratch copy of battery.py with bytecode writes disabled, so the source of that file is not established here. `tools/__pycache__/` (18:02) predates this seat. Not removed.

## Receipts
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-51/w1/R51MutC3a/`: `drive.py`, `out-base.jsonl`, `out-M1..M4.jsonl`, `mutant-M1..M4.diff`, `fixture-displayed-quote-altered.md`, `fixture-displayed-quote-substituted.md`, `substituted-quote.json`, `probe-substituted-quote.txt`.
