VERDICT: supports

# C2-A5 scorer determinism under load (rev 2732ee6c06108c031c4d8043239b994e0504eb2f)

Command (twice, sequentially, TMPDIR=seat scratch, scratch s1/s2): `python3 tools/score-counter-cheats-r51.py --revision 2732ee6c... --scratch <s1|s2>`; census not edited.

| | run1 | run2 |
|---|---|---|
| start load (1/5/15 min) | 40.84 44.59 32.12 | 54.02 49.90 38.89 |
| end load | 54.02 49.90 38.89 | 28.49 40.74 38.59 |
| wall time | 408 s (1793222015->1793222423) | 321 s (1793222423->1793222744) |
| rc | 0 | 0 |
| stderr | empty (0 bytes) | empty (0 bytes) |
| verdict | PASS | PASS |

Host: 32 cores, load 28-54 throughout (about 1-1.7x core count), i.e. loaded. Pre-run `cat /proc/loadavg` = 42.48 44.98 32.18.

Result: `cmp run1.json run2.json` -> IDENTICAL (sha256 6165b9bd06b4c85d2efcda0d9900ff1f2d3c9330b4f0c547a98e739354fa1ff0 both). A flattened key-by-key diff printed no DIFF lines: verdicts and every per-fixture leg identical. No flake, no mut_caught variation.

Top-level: real_pass 1, cheats 4, cheats_rejected 4, r50_cheats_rejected 0, verdict PASS (predicate satisfied in both runs).

Per-fixture legs (both runs identical):
- r51:real       rc0 PASS idiom_sites 0 cases 168 mut_applied 2 mut_caught 2 pass_runs 1
- r51:F1-liar    rc1 FAIL idiom_sites 0 cases 168 mut_applied 0 mut_caught 0 pass_runs 1
- r51:F2-braced  rc1 FAIL idiom_sites 1 cases 168 mut_applied 2 mut_caught 2 pass_runs 1
- r51:F3-echo    rc1 FAIL idiom_sites 1 cases 168 mut_applied 2 mut_caught 2 pass_runs 1
- r51:F4-neutered rc1 FAIL idiom_sites 0 cases 168 mut_applied 2 mut_caught 0 pass_runs 1
- r50:{real,F1..F4} all rc0 PASS idiom_sites 0 cases 168 pass_runs 1 (the r50 matcher is blind to all four cheats => r50_cheats_rejected 0, as predicate requires).

Observations / limits:
- Each fixture ran `pass_runs: 1` (one selftest pass per fixture), so a flake in the green pass would show as a verdict flip; none observed in 2 runs x 10 fixtures. Two samples cannot prove absence of rare flakes; mutant selftests (mut_applied 2 per r51 fixture) were stable across both.
- F1-liar rejection rests on mut_applied 0 (no mutation site applicable) rather than mut_caught; deterministic in both runs.
- Receipts: w1/R51ExecC2Determinism/{run1.json,run2.json,err1.txt,err2.txt,meta.txt}. Scratch s1/s2 were empty after the run (scorer cleans itself).
