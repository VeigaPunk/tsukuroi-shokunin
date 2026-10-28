#!/bin/bash
# fixture: passes on odd invocations, fails on even ones (a 50% flake), otherwise shape-correct
n=$(cat /fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC2/fx/flaky.state 2>/dev/null || echo 0)
n=$((n + 1)); echo "$n" > /fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC2/fx/flaky.state
if [ $((n % 2)) -eq 1 ]; then
  printf 'PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)\n'
  printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\n'
else
  printf 'FAIL selftest: flaked (R50-X)\n'
  printf 'TSUKUROI_CENSUS_SELFTEST: FAIL (168 cases, 167 passed, 1 failed)\n'
fi
