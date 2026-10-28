#!/bin/bash
# Discriminator for M4 (accepting rc 1 as the term status): on TERM it removes
# the fixture and exits 1 instead of 143. Everything else compliant, so only
# term_ok separates pristine (0 -> FAIL) from m4 (1 -> PASS).
st_base=${TMPDIR:-/tmp}
[ -d "$st_base" ] || { echo "stub: TMPDIR '$st_base' is not a directory" >&2; exit 1; }
work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT
trap 'rm -rf -- "${work:-}"; exit 1' TERM
trap 'exit 130' INT
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
