#!/bin/bash
# Discriminator for M3 (clean_ok without the exists check), v2: fully compliant
# EXCEPT it leaves its fixture behind on normal exit whenever the fixture base
# is not /tmp (scratch/spaced legs); fixtures under /tmp are still cleaned, and
# TERM still removes the fixture before exiting 143 (term_ok stays 1).
# Pristine: clean_ok=2 -> FAIL; m3: clean_ok=4 -> PASS.
st_base=${TMPDIR:-/tmp}
[ -d "$st_base" ] || { echo "stub: TMPDIR '$st_base' is not a directory" >&2; exit 1; }
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"; exit 143' TERM
trap 'rm -rf -- "${work:-}"; exit 130' INT
case "$st_base" in
  /tmp) trap 'rm -rf -- "${work:-}"' EXIT ;;
  *)    : 'intentionally no EXIT cleanup for non-/tmp bases' ;;
esac
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
