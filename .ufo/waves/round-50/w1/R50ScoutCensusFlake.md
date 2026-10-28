VERDICT: supports

S-8 independent flake census of `tools/tsukuroi-census.sh --selftest`. Freeze bytes are `8029cdba1049df25632c91a23c8db4eefb54be5f` (blob `8c2e4888b5107f5695d1a4c4da83515d891b9e6c`, sha256 `aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc`). Base bytes are `b866a1d3d26616119a089f1a69b080136becc17b` (blob `6c944307a3bc474d5f80e38c5dab253c60712803`, sha256 `4e032bcb4a119640e30b6a37d49c5b7f768660d8265bca02c6ee91234beaa4c2`). `git hash-object` on the extracted scripts matched those blob ids.

The fix is visible in the case counts: every freeze run printed 168 cases and the `(R50-C2)` PASS line; every base run printed 167 cases and no `(R50-C2)` line. It is not visible in the fail counts. Both revisions printed `0 failed` on every run. Observed false-fail rate: freeze 0/5, base 0/3.

## How the runs were taken

Scripts were extracted with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <REV>:tools/tsukuroi-census.sh` into scratch, then executed sequentially in one process (one `--selftest` at a time). Each run used `TMPDIR` and `HOME` under `/fast/scratch/hyaku/tsukuroi-r50/R50ScoutCensusFlake/runs/<rev>-<n>/`, `LC_ALL=C`, `PATH=/usr/bin:/bin`, cwd the scratch dir, and `/usr/bin/bash <script> --selftest`. No run timed out and none was retried. Sum of the eight `elapsed_s` values is 252.

A false-fail here is a run that prints a `FAIL` line whose `got:` text matches the pattern that line says is missing. The raw fail rate is a run whose summary is `FAIL` or whose exit status is non-zero. Both were scored from the saved stdout and stderr.

## Freeze (`8029cdba`, five runs)

| run | rc | elapsed_s | summary |
|---|---|---|---|
| freeze-1 | 0 | 33 | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` |
| freeze-2 | 0 | 32 | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` |
| freeze-3 | 0 | 32 | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` |
| freeze-4 | 0 | 30 | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` |
| freeze-5 | 0 | 31 | `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` |

Intervals from each `meta.txt`: freeze-1 `2026-10-28T16:11:25-03:00`–`16:11:58`, freeze-2 `16:11:58`–`16:12:30`, freeze-3 `16:12:30`–`16:13:02`, freeze-4 `16:13:02`–`16:13:32`, freeze-5 `16:13:32`–`16:14:03`.

All five stdout files are byte-identical (sha256 `b4b00839fac725a4ce34c0d55c4b820081c4d5de1c968f0de97c7aa7745c97b0`, 15680 bytes, 171 lines). Each is 168 `PASS` lines, 2 `SKIP` lines, and the summary. stderr is empty on every run (0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

`FAIL` lines: none in any freeze run. Lines containing `got:`: none. No `got:` text matched a reported-missing pattern, because no such text was printed.

The `(R50-C2)` line, present on every freeze run (stdout line 170 of freeze-1):

`PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)`

## Base (`b866a1d3`, three runs)

| run | rc | elapsed_s | summary |
|---|---|---|---|
| base-1 | 0 | 30 | `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` |
| base-2 | 0 | 33 | `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` |
| base-3 | 0 | 31 | `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)` |

Intervals: base-1 `2026-10-28T16:14:03-03:00`–`16:14:33`, base-2 `16:14:33`–`16:15:06`, base-3 `16:15:06`–`16:15:37`.

All three stdout files are byte-identical (sha256 `5f346034c87bb2ac06ef14c55ec82cb91a20fbc54e55c2dcd7f404c24bd456aa`, 15574 bytes, 170 lines). Each is 167 `PASS` lines, the same 2 `SKIP` lines, and the summary. stderr is empty on every run. No `(R50-C2)` line.

`FAIL` lines: none in any base run. Lines containing `got:`: none. No `got:` text matched a reported-missing pattern.

## What the counts show

`diff -u` of base-1 stdout against freeze-1 stdout has one hunk. The shared prefix matches. Freeze inserts one line and changes the summary:

```
 PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)
-TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)
+PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)
+TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)
```

That is the claim's 167 → 168 case movement, and it is the only stdout difference. The two `SKIP` lines are in the identical prefix on both revisions (C1 root-arm skips: non-root-owned fixture needs `CAP_CHOWN`; EACCES metadata case not built). They are not in the summary's case total and they are not `FAIL` lines.

False-fail rate, self-contradicting `got:` and raw summary/`rc` together: freeze 0/5, base 0/3. The round-49 11/20 false-miss figure was not reproduced by these eight census selftests. This sample does not show a fail-count improvement, because the base selftest did not false-fail either.

The matcher change itself is in the extracted blobs (not in the selftest fail counts). At freeze, the must-match arm is `buf_has`/`out_has` (`tools/tsukuroi-census.sh:2236`–`2239` and the `out_has`/`buf_has` calls at `:2396`–`:2413` in `8029cdba`), and `(R50-C2)` is the 20-trial 200 KB case at `:3643`–`:3661`. At base `b866a1d3`, the same arm still pipes into `grep -q` / `head -n1` (`tools/tsukuroi-census.sh:2381`, `:2384`, `:2386`, `:2390`, `:2401`, `:2432`).

## Not done

The C2 counter's separate 200 KB idiom probe (`base_misses` / `full_misses`) was not run. Only the five freeze and three base `--selftest` runs named in S-8 were run. No extra trials were added after the base runs passed.
