VERDICT: defect-found
Seat R51MutLintB, item C1-L4. Non-counted wave-1 seat. Counter: `tools/check-scrub-admission-r51.py` at 2732ee6c06108c031c4d8043239b994e0504eb2f. Battery: `.ufo/waves/round-51/controls/battery.py` (same rev, byte-identical to the worktree copy).

## Method
- Clone `git clone --shared` of the lane into scratch, `checkout --detach 2732ee6c…`; `rev-parse --show-toplevel` asserted. The lane itself was not written.
- Each mutant was applied to the clone's `tools/check-scrub-admission-r51.py` with an exact-once string substitution (asserted `count == 1`). The battery's `c1_battery()` was imported and run with `battery.L` and `battery.C1` pointed at the clone. Its `main()` was not called, so no summary file was written to the lane.
- The `BASE` (unmutated) run reproduces the frozen `battery-summary-r51-freeze-c1.jsonl` on every control's verdict and leg values (compared by eye from printed output).
- Restored counter bytes verified identical to the frozen sha256 (`b4165c17…` is the BASE file's sha256; the restore check passed).
- Two added probes (not in the battery), run under every variant: **K8b** (distinct GR2 bodies citing only `entry.md`) and **K9** (GR2 with its quote lines removed; gap block regenerated with `LINT.emit`, because removed quote lines change the cited-line set, `k9_gap_changed = True`).
- 13 counter runs per variant × 6 variants = 78 counter runs; no selftest, no installs.

## Mutants (counter lines at 2732ee6c)
- M5 `lint_ok` forced to 3: inserted `lint_ok = 3` after line 338 (`lint_legs` call).
- M6 `quotes_ok` counts rows with zero quotes: line 211 `per[r]['quotes'] > 0 and` removed.
- M7 blocking rule dropped: line 370 `and not blocking` removed (a `partly` seat is still uncredited, but no longer blocks its row).
- M8 distinct-bodies leg disabled: line 368 `distinct = len(bodies) == len(credited)` → `distinct = True`.
- M9 citation leg accepts no-row-source body: line 243 `if len({f…} & set(CITE[row])) < 2:` → `if False:`.

## Results (FAIL→PASS = mutant lets a should-FAIL control through)
K-pass stayed PASS in all five mutants (verified per variant).

| Mutant | Killed by (battery) | Killed by (probe) | Survives |
|---|---|---|---|
| M5 lint forced 3 | K3 undeclared range gap: FAIL→PASS (lint_ok 0→3) | — | K2, K3b stay FAIL via quotes_ok=2 (they are not lint kills) |
| M6 zero-quote rows count | **none** | K9 GR2 no quotes: FAIL→PASS (quotes_ok 2→3) | **all 10 battery K controls** |
| M7 partly does not block | K4 one bound partly: FAIL→PASS (verdicts_ok 2→3) | — | none |
| M8 distinct leg off | K5 whitespace-identical bodies: FAIL→PASS (verdicts_ok 2→3) | — | none |
| M9 citation row-source leg off | **none** (K8 still FAIL, see below) | K8b distinct lane-only bodies: FAIL→PASS (verdicts_ok 2→3) | K8 |

Notes per mutant:
- M9: K8's bodies are all byte-identical, so after M9 the GR2 row still fails on the distinct-bodies leg (verdicts_ok stays 2). The control that should catch the citation leg is therefore killed by a different leg. Under BASE, K8b fails with `fewer than 2 distinct row source files cited` (seat notes), confirming the probe isolates the citation leg.
- M6: no battery row has zero quotes (`quotes > 0` guard at line 211 is untested). The probe K9 is the only kill.
- M5: lint is the sole gap gate, so K3 is its kill; quote defects (K2, K3b) are still caught by quotes_ok, so M5 is only partly tested by the quote controls.

## Proposed additions for the battery (exact text, ran as probes)
Insert in `c1_battery()` after the K8 line (battery.py line 158):
```python
    lane_distinct = {s: f'Lane-only evidence for {s}: entry.md:{5 + i} and entry.md:{20 + i} state the row clause as written. ' + 'Padding sentence for the report body. ' * 12 for i, s in enumerate(ROLES['GR2'])}
    score('K8b distinct bodies, lane artifacts only', 'FAIL', 'k8b', entry, bodies=lane_distinct)
```
K9 (zero quotes in one row): remove the GR2 quote lines (`LINT.QUOTE_RE` matches inside `## GR2`), regenerate `### Range gaps (R51)` with `lint-grounding-r51.py --emit-gaps` (required, since removed quote lines change the cited-line set), then score all-holds as K2 with `hashes_used=section_hashes(...)` on that text. Expected FAIL on BASE (quotes_ok=2); flips to PASS under M6. Receipt: `R51MutLintB/K9-entry-gr2-no-quotes.md`.

## Receipts
`.ufo/waves/round-51/w1/R51MutLintB/`: `results.json` (per-variant battery rows and probe rows, mutant sha256s, restore check), `mutants/{BASE,M5..M9}.py` and `.diff`, `K9-entry-gr2-no-quotes.md`. Scratch clone removed.
Verified: `git status --porcelain -- tools corpus SKILL.md` empty in the lane.

## Not done
- The partly-as-credited variant of M7 was not run (only the blocking removal); a different M7 variant could behave differently.
- Frozen-summary equality is by eye, not by a diff script.
- No changes proposed to frozen tools; additions above are for the pre-w2 amendment only if the L1 chooses them.
