# C1 counter environment matrix — commands and measured results

Counter: tools/score-selftest-mounts-r41.py at revision 568c397da11339aed65181be598414f268835555
(sha256 8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c; also the sha at freeze
e479fdc5 and at lane tip 71851d63). Census read inside the counter via `git show <REV>:tools/tsukuroi-census.sh`
(sha256 646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95).

## Exact invocations (both from cwd /, caller TMPDIR unset, env -u TMPDIR enforced)
run 1: cd / && env -u TMPDIR /usr/bin/python3 <lane>/tools/score-selftest-mounts-r41.py \
         --revision 568c397da11339aed65181be598414f268835555 \
         --scratch /fast/scratch/hyaku/tsukuroi-r41/C1ExecEnvMatrix/s --jobs 1
run 2: same with --jobs 6
Caller TMPDIR check before run 1: `env | grep -c '^TMPDIR='` -> 0 (shell printed TMPDIR=<unset>).

## Results (stdout JSON kept as jobs1.json / jobs6.json in this directory)
| field | --jobs 1 | --jobs 6 |
|---|---|---|
| exit | 0 | 0 |
| result | PASS | PASS |
| baseline | PASS (128 cases, 128 passed, 0 failed), exit 0 | identical |
| capture_pass | 1 | 1 |
| neutral_pass | 3/3 | 3/3 |
| decoy_pass | 1/1 | 1/1 |
| mutants_applied | 13/13 | 13/13 |
| survivors | 0 | 0 |
| params | 4/4 (one PASSing baseline case each) | 4/4 |
| retried | none (`retried` key absent in every row) | none |
| kill confirmations | 13/13 killed and confirmed | 13/13 killed and confirmed |
| wall (file timestamps) | 15:05:07.27 -> 15:24:02.72 = 1135.4 s | 15:25:08.42 -> 15:28:17.83 = 189.4 s |
| wall (harness-reported) | 1121.9 s | 189.4 s |
| load average at start | 48.57 (32 cpus) | 21.67 |

Each run executes 32 census selftest scripts: baseline, capture, 13 mutants, 3 neutrals, 1 decoy, 13 kill
confirmations. 1135.4/32 = 35.5 s per script at --jobs 1; 189.4 s x 6 / 32 = 35.5 s per script at --jobs 6, so
the per-script cost is the same and the 6x difference is the job pipe, not load.

## Determinism between the two runs
Raw stdout sha256: jobs1 9b667833a88ae17f8bc62902148fd34fefd644be77241052a279b76b12cd26ac,
jobs6 12cbe65a84c5537aa09b211849e981651e21380349582aca2bcfbfafbd17c382.
After normalising the mktemp scratch names (`r41c1.<rand>`, `tsukuroi-r3-2-selftest.<rand>`, which appear only
inside `first_fails` text) and the `branch_tip` field, the two JSON documents are equal. Per-mutant
`killed`/`confirmed`/`fail_count`/`confirm_labels` are identical between the two runs; param_cases are identical
(P1 one case, P2 one, P3 one, P4 one).

The only non-legal difference is `branch_tip`: 71851d63 for run 1, 20c327b3 for run 2 (the lane advanced by the
C2 corrections commit `20c327b3 round-41: append wave corrections to PA2, PA3, PA5, PA6, PA7; S220 anchor note
on the round-40 entry` while the matrix ran). The census content is pinned by --revision, so this does not change
the measurement; it is a note for anyone diffing receipts.

## Declared after receipt differs on a field that is not the predicate
See after-receipt-diff.md: the committed after receipt (.ufo/waves/round-41/after/c1-after-568c397.jsonl,
finished 2026-10-26T17:23:56Z) has one extra stderr FAIL in each of M2, M4, M5, M9, H9 (fail_count +1 vs both of
my runs), every one with the text `hostname override not honoured — possible host read`. Neither of my runs has a
single such FAIL (0 occurrences of that string in jobs1.json and jobs6.json). Verdicts, survivors, params and every
kill's confirm_labels are unchanged; in the after receipt all 13 kills are confirmed on storage-arm labels only
(0 hostname-guard labels), so kill attribution does not depend on the flake.

## Deviation from the declaration's run budget
SCORECARD.md round-41 declaration says the C1 counter is slow and is run "at most once per item, with --jobs 4".
This item ordered two runs (--jobs 1 and --jobs 6); both were run serially, one at a time, as the host rule requires.
Cost measured: 1135 s + 189 s of process wall time.
