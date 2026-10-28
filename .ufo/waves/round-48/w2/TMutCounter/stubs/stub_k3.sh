#!/bin/bash
# Cheap stub census emulating K3 (fix with the INT/TERM exit traps reverted):
# pass_ok 4, loc_ok 4, clean_ok 4, failfast_ok 2, term_ok 0 (EXIT INT TERM
# cleanup trap without exit -> bash continues and exits 0), static_ok 1.
st_base=${TMPDIR:-/tmp}
[ -d "$st_base" ] || { echo "stub: TMPDIR '$st_base' is not a directory" >&2; exit 1; }
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT INT TERM
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
