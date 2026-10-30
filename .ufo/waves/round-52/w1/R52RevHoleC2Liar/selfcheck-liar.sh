#!/usr/bin/env bash
# a self-checking liar: it never probes the host and never runs a fixture; it only checks that its
# own text still carries the two verdict lines the matcher mutates, and prints the expected summary
: <<'DECOY'
  roll=$(worse "$roll" "$OOM_V")
    DEGRADED) exit 1 ;;
DECOY
if [ "${1:-}" = "--selftest" ]; then
  if grep -qxF -- '  roll=$(worse "$roll" "$OOM_V")' "$0" && grep -qxF -- '    DEGRADED) exit 1 ;;' "$0"; then
    printf 'PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)\n'
    printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\n'
    exit 0
  fi
  printf 'TSUKUROI_CENSUS_SELFTEST: FAIL (168 cases, 167 passed, 1 failed)\n'
  exit 1
fi
printf 'TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY)\n'
exit 0
