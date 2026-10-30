VERDICT: defect-found

# R52MutAdj — W-C3c

Axes: adjacency, C3 detector sensitivity, frozen-byte provenance/restoration.

## Result

**Three of the nine named round-51 counter mutants were killed; six survived the round-52 frozen C3 battery.** Survival is a disclosed detector limit, not evidence that an input bypass exists or permission to change the claim. The pristine real-data measurement was PASS; all 15 baseline controls matched their declared outcomes. Evidence: `R52MutAdj/results.json`, keys `baseline` and `mutants`.

## Bytes and detector

Revision: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`.

- Counter SHA256: `cfe3ee233fde7600d95df14ace4421d7a55914f98483934e26078a6504eda3be`.
- Round-52 battery SHA256: `48356a8ae7cce5544dd72740ced845d09d59547141c41459e69a6c147d4b300c`.
- Round-50 dependency SHA256: `d571adc9562b2832baf270086181c770b25eea6c5147d49b27a1525564e00a8b`.

These were observed with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <revision>:<path> | sha256sum`; working copies used for extraction had matching hashes. The round-51 pin counter was different (`3d09a8e94a9075f6de12c03fe1f678d77a3af1f23e18ed887c58a700b44cf380`), so the old mutations were mapped to the corresponding behavior points in the freeze counter, not applied at stale line numbers.

Detector: frozen `.ufo/waves/round-52/controls/battery.py:222-319`, function `c3_battery`; 15 rows K0–K13 plus K-pass. Only that function was invoked, not `main()` (which writes lane control summaries). `driver.py:1-15` documents the harness; the complete driver is preserved beside this report.

Per mutant: a private shared clone, detached at the freeze, held the mutant in `tools/check-adjacency-table-r51.py`. Its default lane was its own clone root. Province/registry were the real git objects at the freeze; sibling resolution used the real read-only fleet repos. Direct measurement command:

```
python3 <private-clone>/tools/check-adjacency-table-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0
```

The baseline observed all full-leg values: `adj_rows=7`, `anchors_ok=7`, `registry_ok=7`, `anchors_checker_rc=0`, `quote_at_pin_ok=9`, `live_quote_ok=9`, `stub_fails=1`, `display_bound_ok=10`, `quote_specific_ok=10`, `digests_bound_ok=10`, `display_forge_fails=1`, `override_blocked=1`, `r50_blind=1`, `anchor_rows_exact=1`, `adj_exact=1`, `bare_all=0`, `checker_rev_bytes=1`, `ancestry_ok=10`, `recipient_ok=7`, `verdict=PASS`. Receipt: `R52MutAdj/pristine-measurement.json`.

“Killed” below means at least one frozen battery row became **not as expected**, following the convention of R51MutC3a. The direct real-data verdict is separately shown; all original real-data verdicts were PASS. A baseline failure would have made a kill inconclusive; none occurred.

## Required mutant table

Freeze source locations refer to `tools/check-adjacency-table-r51.py` at the named revision. Each exact edit is preserved in `R52MutAdj/mutant-<name>.diff`; each full detector output is in the corresponding `.json` and in `results.json`.

| Mutant | Freeze location / defect | Original real verdict | Mutant real verdict | Killed? / observed detector change |
|---|---|---|---|---|
| M1 | :133-134 commit-prefix check removed | PASS | FAIL | **Yes** — K-pass PASS → FAIL, rc 1 |
| M2 | :137-138 displayed-quote equality removed | PASS | PASS | **No — survived**, 15/15 controls as expected |
| M3 | :153 quote_line condition → `if False:` | PASS | PASS | **Yes** — K4 CONTROL-FAIL → CONTROL-PASS, rc 0 |
| M4 | :294 digest result forced to 10 | PASS | PASS | **Yes** — K5 and K7 CONTROL-FAIL → CONTROL-PASS, rc 0 |
| M5 | :369-376 self-run removed; override_blocked=1 | PASS | PASS | **No — survived**, 15/15 |
| M6 | :386 r50_blind=1 | PASS | PASS | **No — survived**, 15/15 |
| M7a | :160-161 heading-section test removed | PASS | PASS | **No — survived**, 15/15 |
| M7b | :155-161 whole heading block removed | PASS | PASS | **No — survived**, 15/15 |
| M8 | :357 display_forge_fails=1 | PASS | PASS | **No — survived**, 15/15 |

M4 maps the old `return n → return 10` mutation onto the freeze function's `return n if sorted(ids) == EXPECTED_OUT else 0 → return 10`: same forced-passing-leg defect. M5/M7a/M7b match the exact block meanings in `round-51/w1/R51MutC3b/driver.py:44-50`.

The six named survivors remain limits of this frozen detector. This probe did not rerun the proposed extra controls from the round-51 reports; it makes no claim that no stronger detector can kill those mutants.

## Supplementary amendment-leg probes

These are additional probes, not replacements for the required set. All original and mutant real-data verdicts were PASS. Evidence: `results.json` entries N1–N6 and their individual diffs/JSON receipts.

| Mutant | Frozen battery result |
|---|---|
| N1 anchor_rows_exact=1 | **Survived**, 15/15 as expected |
| N2 recipient_ok returns 7 | **Killed** — K13 `(7, 6)` → `(7, 7)` |
| N3 ancestry_ok returns 10 | **Killed** — K12 `(10, 9)` → `(10, 10)` |
| N4 environment-redirection guard removed | **Killed** — K11 OVERRIDE-NOT-MEASURED → FAIL, rc 2 |
| N5 no-base-check override guard removed | **Killed** — K10 OVERRIDE-NOT-MEASURED → PASS, rc 0 |
| N6 bare_all=0 | **Survived**, 15/15 as expected |

N1 survival does not establish duplicate-row acceptance: it means the verdict-only battery did not distinguish disabling that particular leg. Likewise N6 survival is not an observed bare-locator bypass.

## Round-49 stub condition

Neither named R51 mutant report names `R49CritAdjA` (search for `R49CritAdj|round-49|R49` returned no matches). Therefore no separate historical A3 registry-rewrite fixture was replayed. The frozen battery's existing K2 synthetic shape-valid stub ran on baseline, every mutant, and restored bytes; it remained CONTROL-FAIL. This does **not** establish rejection of every historical R49 fixture. No closure claim is made for the R49 A3 or E fixtures.

## Hashes, restoration, and hygiene

`results.json` records each mutant's full SHA256 and the before/after lane counter hash. The lane counter hash remained the frozen `cfe3ee23…eda3be` throughout; no tracked lane source was edited.

After mutant runs, each same private clone path was re-created with the exact frozen counter bytes. The same 15-row detector was rerun at each restored path. `R52MutAdj/restored.json` records all 15 restored hashes equal to the before hash and **15/15 controls as expected for every restored variant**. These are re-materialized restored copies, not an assertion of in-place restoration of the removed mutant files.

All receipts and reproducible drivers were copied into `R52MutAdj/`; all scratch clones and the seat scratch root were removed after jobs completed. No tools installed. No census selftest, C1, C2, proposed counter repair, integration, or commit was run.

Host-guard deviation: preliminary counter/battery inspection briefly materialized four files under `/tmp` (`c3_r51pin.py`, `c3_r52freeze.py`, `c3_freeze.py`, `battery52.py`) rather than the required scratch root. They were explicitly removed. Behavioral probe temp files used TMPDIR under the assigned scratch root. This deviation is disclosed, not claimed compliant.
