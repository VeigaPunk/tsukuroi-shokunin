#!/bin/bash
# Discriminator for M6 (static regex dropped): identical to stub_pass but with
# a dead non-comment `idle_base=/tmp` assignment, which the pristine static leg
# flags and m6 accepts. Only static_ok separates pristine (FAIL) from m6 (PASS).
idle_base=/tmp
st_base=${TMPDIR:-/tmp}
[ -d "$st_base" ] || { echo "stub: TMPDIR '$st_base' is not a directory" >&2; exit 1; }
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
