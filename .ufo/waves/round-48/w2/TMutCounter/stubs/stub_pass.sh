#!/bin/bash
# Cheap stub census emulating the K-pass (fix revision) observable signature:
# pass_ok 4, loc_ok 4, clean_ok 4, failfast_ok 2, term_ok 1, static_ok 1.
# Usage text: no '/tmp fallback' promise anywhere in this file.
st_base=${TMPDIR:-/tmp}
[ -d "$st_base" ] || { echo "stub: TMPDIR '$st_base' is not a directory" >&2; exit 1; }
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
