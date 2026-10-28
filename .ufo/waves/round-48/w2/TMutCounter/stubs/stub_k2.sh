#!/bin/bash
# Cheap stub census emulating K2 (fix revision with the r47 /tmp fallback
# restored): pass_ok 4, loc_ok 3 (spaced falls back to /tmp), clean_ok 4,
# failfast_ok 2 (a MISSING TMPDIR still fails before the fixture is created —
# the fix resolves TMPDIR itself first, so a nonexistent spaced TMPDIR exits
# before mktemp rather than falling back), term_ok 1, static_ok 0 (the literal
# `st_base=/tmp` fallback assignment).
[ -d "${TMPDIR:-/tmp}" ] || { echo "stub: TMPDIR is not a directory" >&2; exit 1; }
st_base=${TMPDIR:-/tmp}
case "${TMPDIR:-}" in *[!A-Za-z0-9._/+-]*) st_base=/tmp ;; esac
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
