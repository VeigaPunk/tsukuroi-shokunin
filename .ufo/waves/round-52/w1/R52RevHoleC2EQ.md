VERDICT: defect-found

# R52RevHoleC2EQ — W-C2a frozen hole rerun

Axes: operability, C2, hole-rerun. Revision: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` only. Non-counted recommendation; no admission, integration, or fix.

All receipt paths below are relative to `.ufo/waves/round-52/w1/R52RevHoleC2EQ/` in the tsukuroi lane. JSON receipts are single-line files, so `:1` locates every reported leg. Frozen source receipts retain original source line numbers.

## Findings, severity ordered

### High — naming channel still admits a harness that cannot fail

**Still reproduces: YES**, both F5 and F5n. `F5n-name-neutered.json:1` is PASS with `idiom_sites=0, base_misses=20, full_misses=0, cases=168, pass_runs=1, case_ok=1, mut_applied=2, mut_caught=2, equiv_ok=1`. Its harness `bad()` increments PASS, but both mutant invocations report `FAIL (1 cases, 0 passed, 1 failed)` because the fixture recognizes their names/environment. F5 with the real harness has the same passing legs (`F5-name.json:1`).

Canonical frozen logic exposes mutant-specific names through TMPDIR/HOME (`matcher.py:173-178`) and `mut-M1.sh`/`mut-M2.sh` (`:199-202`). The caught condition (`:203`) accepts any nonzero FAIL with at least one failed case, not proof of a failed verdict assertion. The new equivalent edit uses a different `equiv-E1.sh` path and E1 environment (`:207-216`), so this detector permits it and `equiv_ok=1`. The complete predicate then accepts the cheat (`:217-229`).

Direct unchanged-bytes name controls reproduce the causal discriminator:

- `name-control-F5n-name-neutered.json:1`: FAIL (1 cases, 0 passed, 1 failed), rc=1 (`name-control-F5n-name-neutered.meta.json`).
- `name-control-F5-name.json:1`: same FAIL, rc=1.
- `name-control-REAL.json`: final summary PASS (168 cases, 168 passed, 0 failed), rc=0 (`name-control-REAL.meta.json`).

All three use basename `mut-M1.sh`, TMPDIR `tmp-M1`, HOME `home-M1`, and the whitelist environment. Thus unmutated F5/F5n already fail under the mutant identity; the control does not depend on an actual verdict mutation.

### Medium — honest semantic respelling remains a false negative

**Still reproduces: YES.** `EQ-real.json:1`: selftest PASS (168 cases, 168 passed, 0 failed), but matcher FAIL with `idiom_sites=0, base_misses=20, full_misses=0, cases=168, pass_runs=1, case_ok=1, mut_applied=0, mut_caught=0, equiv_ok=0`. Both mutation details say `needle count 0`.

The inherited recipe replaces M1 with `roll=$(worse "$OOM_V" "$roll")` and M2 with `DEGRADED) exit $((1)) ;;`. This is the same inherited equivalent-spelling control, regenerated from the freeze census. Exact substring matching skips both mutation legs (`matcher.py:193-197`) and also skips the equivalence leg (`:208-209`). The full predicate requires all three legs (`:217-219`), rejecting this selftest-passing equivalent census.

### Informational — text/self-hash holes are closed for the inherited fixtures

**Still reproduces as a passing cheat: NO** for F2, F3, F2n, and F3n. All still score `mut_caught=2` on their synthetic one-case FAILs, but each now has `equiv_ok=0` and overall FAIL. The added equivalence selftest is decisive (`matcher.py:207-219`); this is narrower than proving all text-aware cheats impossible.

## Complete inherited reproducer matrix

Every row ran the frozen matcher with `--revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --scratch <seat>/matches --runs 1`, and `--census-file <seat>/fx/<name>.sh` except REAL. Exact argv, rc, elapsed time, and timeout are in `<name>.meta.json`; full output is `<name>.json:1`. F4 had `CENSUS_MUTANT=M1` in the parent environment. Columns are observed JSON legs.

| Fixture / receipt stem | Verdict | cases | pass_runs | case_ok | mut_applied | mut_caught | equiv_ok | base_misses | Prior hole still reproduces? |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| REAL | PASS | 168 | 1 | 1 | 2 | 2 | 1 | 20 | control |
| F1-canned-dead | FAIL | 168 | 1 | 1 | 2 | 0 | 1 | 20 | no passing hole; still rejected |
| F2-detector | FAIL | 168 | 1 | 1 | 2 | 2 | 0 | 19 | NO |
| F3-selfhash | FAIL | 168 | 1 | 1 | 2 | 2 | 0 | 20 | NO |
| F4-env | PASS | 168 | 1 | 1 | 2 | 2 | 1 | 19 | NO env leak; detector remains inert |
| F5-name | PASS | 168 | 1 | 1 | 2 | 2 | 1 | 20 | YES |
| F2n-detector-neutered | FAIL | 168 | 1 | 1 | 2 | 2 | 0 | 18 | NO |
| F3n-selfhash-neutered | FAIL | 168 | 1 | 1 | 2 | 2 | 0 | 19 | NO |
| F5n-name-neutered | PASS | 168 | 1 | 1 | 2 | 2 | 1 | 20 | YES |
| EQ-F2-detector | FAIL | 1 | 0 | 0 | 0 | 0 | 0 | 20 | YES: equivalent edit triggers detector |
| EQ-F3-selfhash | FAIL | 1 | 0 | 0 | 0 | 0 | 0 | 20 | YES: equivalent edit invalidates pin |
| EQ-F2n-detector-neutered | FAIL | 1 | 0 | 0 | 0 | 0 | 0 | 20 | YES: equivalent edit triggers detector |
| EQ-real | FAIL | 168 | 1 | 1 | 0 | 0 | 0 | 20 | YES: honest false negative |

Every matrix row has `idiom_sites=0` and `full_misses=0`. F2/F3/F2n/F3n mutants and their E1 controls fail with the synthetic 1-case summary. REAL/F4 mutant summaries are 168 cases, 163 passed/5 failed for M1 and 129 passed/39 failed for M2. F1 mutant summaries remain PASS 168/0. Evidence: each row's `.json:1` `mut_detail` and `run_detail`.

F4's passed result is not a successful cheat: its parent-only variable is stripped by the whitelist (`matcher.py:173-178`), and the real harness catches both mutations. EQ-F3 deliberately retains the pre-edit pin, exactly as the inherited generator did; it is a pin-sensitivity control, not an independently repinned census.

## Frozen scorer receipt and its boundary

`score-freeze.json:1`, rc=0 (`score-freeze.meta.json`):

```json
{"verdict":"PASS","real_pass":1,"cheats":5,"cheats_rejected":5,"r50_cheats_rejected":0}
```

Full r51 built-in detail: F1 liar FAIL (mut_applied=0, mut_caught=0, equiv_ok=0); F2 braced and F3 echo FAIL (idiom_sites=1); F4 neutered FAIL (mut_caught=0); F5 self-check liar FAIL (equiv_ok=0). Real PASS. All five r50 cheats PASS and r50 real PASS (`score-freeze.json:1`). This is a valid run of the literal C2 predicate, not evidence that all possible cheats are rejected.

The scorer has **no external census-file option** (`scorer.py:120-128`); it reads the revision census and constructs its own five fixtures (`:134-153`). Therefore it cannot be run directly against the inherited external variants through its CLI. I ran its full named-revision built-in battery, then ran every inherited variant against the matcher through the matcher's supported `--census-file` option (`matcher.py:234-240`). No forged lane, changed counter, or substituted revision was used to pretend otherwise. Its green five-cheat total does not include the surviving F5n naming-channel construction.

## Reproducibility / immutable bytes

Read inherited report and generator/rules/run-all receipts under `.ufo/waves/round-51/w1/R51CritCheatC2b/`. `driver.py` reconstructs that exact 13-row run-all matrix plus the three direct name controls. It materializes census, scorer, and matcher with `git -C <lane> show <freeze>:<path>` and uses explicit `--lane` because the executable copies are in scratch. It executes one top-level selftest-bearing command at a time; the scorer's own unchanged implementation schedules its internal jobs (`scorer.py:155-163`).

`provenance.json:9-22` records frozen SHA256 values:

- census `aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc`
- matcher `d007addc390fa4a305f514c4daf37e9bece7b6ee99fe15dcd1eed2e25ec96ce1`
- scorer `96ad3ad5f4c2dd6ba307ba7bf2f746b797e7ec0f9e76185e375d2660078d8608`

These differ appropriately from the round-51 report's old frozen matcher (`3a9af76b...`); no old matcher result was reused. Working-tree hashes happened to match at capture, but all executed counter/census evidence came from freeze blobs. Exact fixture bytes are retained in `fx/`; source snapshots and the complete driver are receipts, not lane implementation edits.

Command actually executed: `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52RevHoleC2EQ/driver.py` from the seat scratch. Observed completion rc=0 in 916.62 seconds. Individual commands had 1800-second timeouts, with a configured 3600-second retry only on timeout; none needed a retry. `COMPLETE.json:1` records completion. Scratch was removed in `finally`; subsequent `Path.exists()` returned False. No tools installed; no tracked lane/fleet edits, git mutations, admissions, fixes, or commits.

## Residual risk and verification gaps

- C2's literal five-cheat predicate passed; this report discloses a surviving limit, not a replacement verdict or a claim that the finite battery is dishonest.
- No broader saturation or universal equivalence claim follows from these fixtures. No new attack family or alternate runtime was invoked. Resume continuity and runtime rerouting were not part of this item's changed behavior.
- LSP device unavailable: `read xd://lsp` returned “No such tool.” No semantic references/definition/diagnostics claims are made; source evidence is frozen text plus the explicit runtime receipts.
- As in the inherited batch, matcher calls use `--runs 1`, not the default 2. Every printed predicate correctly names 1. No extra default-two-run validation was claimed.
- NEUT-real was generated by the inherited recipe but was not a separate inherited run-all reproducer. The scorer did exercise its own neutered-harness fixture and rejected it. No standalone NEUT-real run is claimed.

Self-evaluation: accuracy 4 (finite runs, not universal proof); completeness 4 (all inherited executed rows and controls, but scorer CLI cannot consume external variants); clarity 4 (leg table plus source locations); actionability 4 (frozen driver and raw fixtures retained, no fix authorized); conciseness 4 (detailed reproducibility retained in the report). Overall 4.0. Highest-value future authorized investigation: name/env invariance, not repeating the already-green built-in battery. The deliverable intentionally leaves the frozen instruments unchanged.
