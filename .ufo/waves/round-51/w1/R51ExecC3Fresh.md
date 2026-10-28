VERDICT: supports

# R51ExecC3Fresh — C3 fresh-clone reproduction (uncounted w1 seat)

Fresh clone: `git clone --shared` of the lane into `/fast/scratch/hyaku/tsukuroi-r51/R51ExecC3Fresh/fx.dmyZQn`, detached at 2732ee6c06108c031c4d8043239b994e0504eb2f. `rev-parse --show-toplevel` equalled the clone dir; HEAD equalled the freeze.

## Counter, freeze (rc=0)
`python3 $D/tools/check-adjacency-table-r51.py --revision 2732ee6c… --lane $D` → one JSON line, verdict PASS, exit code 0.
Legs: adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7, anchors_checker_rc 0, quote_at_pin_ok 9, live_quote_ok 9 (>=8), stub_fails 1, display_bound_ok 10, quote_specific_ok 10, digests_bound_ok 10, display_forge_fails 1, override_blocked 1, r50_blind 1 (r50_problems []), mode "measurement", base c0ad548a…. Per-row detail OUT-001..OUT-010 all bound true, specific true, why [].
Every predicate term is met. Full JSON: w1/R51ExecC3Fresh/out-2732ee6c….txt (legs-2732ee6c.json is the detail-less form).

## Counter, base (rc=0)
Same command with `--revision c0ad548a… --lane $D` → the same 15 legs with identical values, PASS, rc=0 (the JSON differs only in `revision`). So the counter does not distinguish the base from the freeze on these legs; the file-level difference between them is not exercised by this counter's predicate [INFERENCE: not diffed here].

## Battery C3 section (rc=0)
`battery.py --freeze 2732ee6c… --only c3 --tag R51ExecC3Fresh --scratch …/b` → stdout `c3: 7 controls, 7 as expected, 0 not`. Written: controls/battery-summary-r51-R51ExecC3Fresh-c3.jsonl (2267 B, 7 lines).
| control | expected | got | rc |
|---|---|---|---|
| K0 false displayed OUT-009 commit | CONTROL-FAIL | CONTROL-FAIL | 1 (display_bound_ok 9) |
| K1 override without --control | OVERRIDE-NOT-MEASURED | OVERRIDE-NOT-MEASURED | 3 |
| K2 shape-valid stub | CONTROL-FAIL | CONTROL-FAIL | 1 (all legs 0) |
| K3 registry digest mutated | CONTROL-FAIL | CONTROL-FAIL | 1 (digests_bound_ok 9, quote_at_pin_ok 8) |
| K4 registry quote_line moved | CONTROL-FAIL | CONTROL-FAIL | 1 (quote_specific_ok 9) |
| K5 displayed OUT-010 digest altered | CONTROL-FAIL | CONTROL-FAIL | 1 (digests_bound_ok 9) |
| K-pass real province+registry | PASS | PASS | 0 |
Every control scored as declared.

## Not done
No re-run for timing/flakiness (each command run once, no timeouts). The battery passes `--no-base-check` and no `--lane`, so it reads revisions from the default lane, not the fresh clone; only the direct counter runs used the clone. Live-quote leg (live_quote_ok 9) depends on external fetches/reads [INFERENCE: not inspected]. No tools installed.
Scratch removed at end.
