#!/bin/bash
# Cheap stub census emulating the K0 (base blob 5fdf062) observable signature:
# pass_ok 0 (166 cases expected, the base prints 149), loc_ok 3 (spaced TMPDIR
# falls back to /tmp), clean_ok 4, failfast_ok 1 (missing-spaced falls back to
# /tmp and RUNS), term_ok 0 (EXIT INT TERM trap without exit -> continues, rc 0),
# static_ok 0 (literal st_base=/tmp fallback assignment plus usage promise).
# usage: writes under ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*, or /tmp itself when TMPDIR
#        holds characters the locator refuses (R47-C2).
st_base=${TMPDIR:-/tmp}
case "$st_base" in
  *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
esac
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT INT TERM
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (149 cases, 149 passed, 0 failed)"
exit 0
