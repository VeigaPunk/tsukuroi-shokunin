VERDICT: supports

# C1-12 — conversion mutation probe

**Mutation scope:** single-site mutants, one syntax change applied to one S1–S5 production statement per variant. The frozen counter defines S1–S5 and the equivalence procedure (`tools/score-census-readers-r45.py:15-40,169-207`). I applied each requested mutation at every site where its syntax occurs; thus 30 mutants total, plus four fixed seeds per mutant. Site lines below are from implementation commit `18389f44cf6ce414d7be205998b29c79fb0b490c`: S1 `probe_systemd/state` line 965; S2 `probe_systemd/r` line 1003; S3 `probe_drivers/driver` line 1085; S4 `probe_journal/t_word` line 1460; S5 `probe_journal/r` line 1535 (`tools/tsukuroi-census.sh`, extracted and hashed in scratch).

Frozen-counter SHA-256 was verified as `fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`. Implementation census SHA-256: `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`. The imported harness first scored pristine S1–S5: zero mismatches for each site under each seed. The counter's deterministic draw loop was replicated exactly (same shared RNG, S1→S5 order; four seeds `a2w1-seed-1` through `-4`). Detailed per-seed mismatch counts and draw kinds are in `C1MutSites/mutants-equivalence.json` (SHA-256 `91d41909f5949075b82a07c3e31ea0c2f67864f436df3258a2a36b0909c7ede9`).

## Equivalence results

`K` = mutant differed from the frozen base oracle on at least one of the eight draws for **each** of the four seeds; counts are mismatching draws per seed in the order `-1/-2/-3/-4`. All 30 mutants were killed for every seed except the noted equivalent cases. Draw kinds are `none`, `small`, or `large`, as supplied by frozen `draws()`.

| Mutant | Sites | Mismatches per seed; detecting draw kinds |
|---|---|---|
| (a) `%%`→`%` | S1 | 5/6/6/6; large+small / large+small / large / large+small |
| (a) | S2 | 6/4/5/6; large+small / large+small / large / large+small |
| (a) | S3 | 6/6/5/7; large+small / large+small / large+small / large+small |
| (a) | S4 | 5/4/5/7; large / large+small / large+small / large+small |
| (a) | S5 | 6/6/5/7; large+small / large+small / large+small / large+small |
| (b) drop CR removal | S1,S4,S5 | 0/0/0/0 each: survives equivalence but is equivalent here, since each same statement's trailing `[[:space:]]` trim removes CR. Not a behavior-changing survivor. |
| (b) | S2 | 5/5/3/3; large+small / large+small+none / large / large+small |
| (c) `//`→`/` | S1,S4,S5 | 0/0/0/0 each: survives equivalence but is equivalent here, since the later trailing whitespace trim removes the remaining CR. Not a behavior-changing survivor. |
| (c) | S2 | 2/2/1/1; large+small / none / large / large |
| (d) strip leading instead of trailing | S1 | 6/4/4/4; large+none+small / large+small / large+none / large+none+small |
| (d) | S4 | 4/4/5/3; large+none / large+none+small / large+none+small / large+small |
| (d) | S5 | 5/4/2/3; large+none+small / large+small / large+none / large+small |
| (e) `[![:space:]]`→`[! ]` | S1 | 2/4/2/1; none+small / large+small / large+none / none |
| (e) | S4 | 1/3/5/2; none / none+small / large+none+small / small |
| (e) | S5 | 3/3/3/2; large+none+small / large / large+none / large+none |
| (f) S3 awk FS `', *'`→`','` | S3 | 5/5/5/4; large+none+small / large+none / large+none+small / large+small |
| (g) take last line | S1 | 6/7/6/6; large+small / large+small / large / large+small |
| (g) | S2 | 6/5/5/6; large+small / large+small / large / large+small |
| (g) | S3 | 6/6/5/7; large+small / large+small / large+small / large+small |
| (g) | S4 | 5/6/6/7; large / large+small / large+small / large+small |
| (g) | S5 | 7/6/5/7; large+small / large+small / large+small / large+small |
| (h) literal `\\n` pattern in place of `$'\\n'` | S1 | 6/7/6/6; large+small / large+small / large / large+small |
| (h) | S2 | 6/5/5/6; large+small / large+small / large / large+small |
| (h) | S3 | 6/6/5/7; large+small / large+small / large+small / large+small |
| (h) | S4 | 5/6/6/7; large / large+small / large+small / large+small |
| (h) | S5 | 7/6/5/7; large+small / large+small / large+small / large+small |

(h) was my own plausible quoting defect: use the literal backslash-n pattern `\\n` rather than Bash ANSI-C `$'\\n'`, so a multiline capture is not split. Its multi-line `small`/`large` draws detect it. The requested behavior-changing mutants all have equivalence mismatches; there is no behavior-changing equivalence survivor and therefore no counter gap identified.

## Full counter runs

I ran the full frozen counter sequentially on two representative variants, using isolated shared fixture clones, removing origin, asserting each clone's `--show-toplevel`, committing with the fixture identity, setting `refs/remotes/origin/master` to the variant revision, and using fixed seed `a2w1-seed-1`:

* (a) S1: variant revision `49a36b75ad05a0bb219525274a891655487c2484`; counter output: `verdict=FAIL`, `equiv_ok=4`, S1 had 5/8 mismatches (first `large`, length 138069; oracle `running`, mutated result begins `running  ` plus tail); selftest `FAIL (154 cases, 153 passed, 1 failed)`, `selftest_r45=5`; `revert_killed=6`. Thus conversion mutant is killed by equivalence and selftest. The adjacency subcheck returned `CANNOT_EVALUATE`, `E-REVISION-NOT-LANDED`, `adjacency_ok=0`.
* (f) S3: variant revision `8d6d71902967b7a3cb647cdb62eaf47d3d9fe9c5`; counter output: `verdict=FAIL`, `equiv_ok=4`, S3 had 5/8 mismatches (first `large`, length 179676; oracle `z\t`, mutated result `   z\t`); selftest `FAIL (154 cases, 153 passed, 1 failed)`, `selftest_r45=5`; `revert_killed=6`. The adjacency subcheck likewise returned `CANNOT_EVALUATE`, `E-REVISION-NOT-LANDED`, `adjacency_ok=0`.

Both full runs were failures as expected for deliberately mutated revisions; the independent cause of full-counter failure is the expected equivalence/selftest kill. The adjacency leg did not pass and must not be represented as passing: despite setting the required fixture ref, the actual observed adjacency output was `E-REVISION-NOT-LANDED`. Full outputs are preserved in the tool artifacts from this run; detailed equivalence receipt is in `C1MutSites/mutants-equivalence.json`. No full-counter run was made for the other mutants.

## Commands / environment / limits

* `sha256sum tools/score-census-readers-r45.py` → frozen hash above.
* `git ... merge-base --is-ancestor 18389f44... HEAD` and `git ... merge-base --is-ancestor 5bbd5ff... 18389f44...` → `IMPL-IN-TIP`, `BASE-IN-IMPL`; base-to-implementation diff of `tools/check-adjacency-anchors.py` and `tools/_revision.py` was empty (`ADJDEPS-UNCHANGED-BASE-TO-IMPL`).
* Tool versions observed: git 2.56.0, Python 3.14.8, Bash 5.3.20. No tools installed.
* Only the declared scratch tree and this report/receipt directory were written. Fixture clones are disposable scratch; scratch is removed after receipt copying. No host operations or lane source edits were performed.