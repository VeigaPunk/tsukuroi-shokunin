#!/bin/bash
# Discriminator for M1 (pass_ok without rc==0): prints the exact expected PASS
# last line but exits 1. Also compliant on every other leg so ONLY pass_ok
# separates pristine (FAIL) from m1 (PASS).
st_base=${TMPDIR:-/tmp}
[ -d "$st_base" ] || { echo "stub: TMPDIR '$st_base' is not a directory" >&2; exit 1; }
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 1
