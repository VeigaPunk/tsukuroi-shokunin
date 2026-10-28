VERDICT: defect-found

# R51MutC2 — mutation test of the C2 counter and scorer (item C2-A3)

Revision under test: 2732ee6c06108c031c4d8043239b994e0504eb2f. Bytes taken with `git show`:
- `tools/check-selftest-matcher-r51.py` sha256 3a9af76b4ecc06dcc502659708f2c80f6dbdae3f4cb379d50651f4c4efea30b9 (matches FROZEN-hashes.txt:3)
- `tools/score-counter-cheats-r51.py` sha256 746f4ddac15f7a7ebf301744aeec492e961a11b1d75d425d9c1de2529d40dfe3 (matches FROZEN-hashes.txt:4)

Method: each mutant is a one-line change in a scratch copy (diffs in `R51MutC2/mutants/*.diff`). Every counter mutant was scored by the scorer at REV with `--counter <mutant> --skip-r50 --runs 1 --lane <lane>`. Every scorer mutant was run with the unmutated counter at REV. Two always-PASS / always-FAIL control counters (`mutants/fake_pass.py`, `fake_fail.py`) were added to show what the scorer predicate does in the cases the frozen gate never builds. Receipts: `R51MutC2/<name>.json` (scorer stdout) and `.stderr.txt`. Scratch removed.

## Results

| Mutant | Target | Scorer result (cheats_rejected / real_pass / verdict) | Rejected cheats | Verdict |
|---|---|---|---|---|
| M1 | counter: `mut_applied = mut_caught = 2` forced (inserted before counter `ok =` line 182) | 2 / 1 / FAIL | F2, F3 rejected; F1 liar and F4 neutered PASS | KILLED by scorer predicate |
| M2 | counter: idiom regex no longer matches `${out}` (IDIOM_RE line 61) | 3 / 1 / FAIL | F2 braced-spell PASSes; F1, F3, F4 rejected | KILLED |
| M3 | counter: `pass_runs == a.runs` → `pass_runs >= 0` (line 183) | 4 / 1 / **PASS** | all four rejected by other legs | SURVIVES |
| M4 | counter: `base_misses > 0` leg dropped (line 182) | 4 / 1 / **PASS** | all four rejected by other legs | SURVIVES |
| M5 | scorer: `cheats_rejected` counts every r51 cheat (line 134) | 4 / 1 / **PASS** (real counter) | n/a | SURVIVES |
| M6 | scorer: `real_pass = 1` forced (line 133) | 4 / 1 / **PASS** (real counter) | n/a | SURVIVES |
| C0 (baseline, unmutated) | — | 4 / 1 / PASS | F1-F4 all FAIL rc 1; real PASS rc 0 | predicate holds at REV |
| C1 control: always-PASS counter, unmutated scorer | — | 0 / 1 / FAIL | none rejected | scorer catches it |
| C2 control: always-FAIL counter, unmutated scorer | — | 4 / 0 / FAIL | all rejected, real FAIL | scorer catches it |
| C3 control: always-PASS counter, M5 scorer | — | 4 / 1 / **PASS** | none rejected | M5 hole exposed |
| C4 control: always-FAIL counter, M6 scorer | — | 4 / 1 / **PASS** | real counter FAILs | M6 hole exposed |

Per-cheat verdicts for each counter mutant are in the receipts (`M1-…json`, `M2-…json`, `M3-…json`, `M4-…json` under `rejected_detail`). Example, M1 (`R51MutC2/M1-counter-forced-applied-caught.json`): `"r51:F1-liar": ["PASS", 0]`, `"r51:F4-neutered": ["PASS", 0]`, `"r51:F2-braced-spell": ["FAIL", 1]`, `"r51:F3-echo-spell": ["FAIL", 1]`.

Mutation-kill inventory: M1, M2 killed by the scorer predicate. M3, M4 survive. M5, M6 survive the frozen gate and both controls.

## Which mutant the scorer's own predicate catches

- **M1 (caught):** forcing the mutation legs to 2 frees the liar (F1) and the neutered census (F4); the scorer reports `cheats_rejected 2` and FAILs. The only cheats the frozen mutation legs stop are F1 and F4, so those legs are load-bearing.
- **M2 (caught):** the respelled braced arm F2 is only seen by the idiom leg (the `${out}` form). Narrowing the regex lets F2 through; scorer reports `cheats_rejected 3` and FAILs. Only F2 exercises the brace path.
- **M3 (not caught):** `pass_runs` relaxation changes behaviour only when the single run does not print `PASS … 0 failed`. None of F1-F4 has that property (all four print PASS summaries), and the scorer runs `--runs 1`, so no cheat or control exercises the leg. Candidate control (not built, not run): a census that honestly FAILs its one run with otherwise-intact markers must be rejected. [INFERENCE: such a census would pass M3's counter, since its other legs are unaffected.]
- **M4 (not caught):** `base_misses` depends only on the counter's own probe (lines ~ PROBE block), not on the census, so no cheat moves it. The frozen gate has no control with a broken probe. Candidate control (not built, not run): the counter must FAIL when the probe reports `base_misses == 0` or `-1`.
- **M5 (not caught by frozen gate; caught only by a control that does not exist):** the scorer only counts cheats; nothing in the frozen gate checks that a counter which PASSes everything is rejected. C3 shows the mutant scorer PASSes an always-PASS counter. The unmutated scorer does catch that counter (C1, `cheats_rejected 0`), but C1 is not part of the frozen gate. The r50 leg (`r50_cheats_rejected == 0`) does not catch it either: M5 is scoped to the r51 count.
- **M6 (not caught by frozen gate; caught only by a control that does not exist):** `real_pass` is never checked against a counter that FAILs the real census. C4 shows the mutant scorer PASSes an always-FAIL counter. The unmutated scorer catches it (C2, `real_pass 0`), but C2 is not in the frozen gate. None of the four cheat censuses is a real-census-fails case.

## Operability findings (observed)

1. **Predicate text disagrees with the code under the scorer.** The counter's docstring and output predicate read `pass_runs == 2` (counter source lines 31-32), but the leg is `pass_runs == a.runs` (line 183), the counter defaults `--runs` to 2 (line 205), and the scorer always passes `--runs 1`. So the printed predicate is not the predicate that is evaluated in the scorer run.
2. **`cheats == 4` in the scorer is a tautology.** The scorer checks `len(fx) == 4` (line 141). `fixtures()` always returns exactly four keys or raises `SystemExit`, so this leg cannot fail. The `cheats` value in the output is a constant, not a count of built cheats.
3. **Scorer default `--lane` is script-relative.** A scorer copy outside the lane (as used here) needs an explicit `--lane`, or it scores the wrong repo. The counter's `--counter` argument is joined to `--lane` with `os.path.join`; an absolute path overrides that and works.
4. **Runtime.** Baseline scorer run (`--skip-r50 --runs 1`): 410.9 s. Mutant scorer runs: 173.8-254.4 s (`R51MutC2/*.json` `secs` in the run log). Control runs with fake counters: 0.1 s. `--skip-r50` was used throughout, so the frozen r50 leg was not run.
5. **Scorer swallows counter errors as "not rejected."** `score()` maps a crashing counter to `verdict ERROR` and the rejection test requires `rc == 1`. This is the right direction for cheats, and it means a crashing counter on a cheat correctly does not count as rejection; no defect found here, noted for the L1.

## Proposed amendment text (for the L1's pre-w2 commit; not applied by me)

- Add the two control counters (always-PASS, always-FAIL) as scorer controls with predicates: always-PASS → `cheats_rejected < 4` (FAIL), always-FAIL → `real_pass == 0`. These close M5 and M6.
- Add a census that honestly FAILs one case as a counted cheat (rejected) and a probe-broken control (counter rejects `base_misses ∈ {0,-1}`). These close M3 and M4.
- Replace `cheats == 4` with a count of successfully built cheat censuses, not `len(fx)`.
- Print the evaluated predicate (with the actual `--runs`) in the counter output.

## Not done

- No r50 counter run (`--skip-r50` used throughout, as the item specifies).
- The M3 and M4 candidate controls above were described, not built or run; the [INFERENCE] tags mark them.
- No tools installed. Python 3.14.8 used as-is. No git writes; no lane file touched. Scratch dir `/fast/scratch/hyaku/tsukuroi-r51/R51MutC2` removed after copying receipts.
