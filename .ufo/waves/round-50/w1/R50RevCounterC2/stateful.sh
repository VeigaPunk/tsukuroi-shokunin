#!/bin/bash
# fixture: run1 loses a case (167, no R50-C2 line); run2 has it (168). cases/case_ok are
# taken from the LAST run and from ANY run respectively, so the counter cannot see run1.
n=$(cat /fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC2/fx/stateful.state 2>/dev/null || echo 0)
n=$((n + 1)); echo "$n" > /fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC2/fx/stateful.state
if [ "$n" -eq 1 ]; then
  printf 'TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)\n'
else
  printf 'PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)\n'
  printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\n'
fi
exit 0
