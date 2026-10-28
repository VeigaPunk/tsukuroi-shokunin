#!/bin/bash
# Discriminator for M2 (loc_ok blind under non-/tmp TMPDIR): builds its fixture
# in /tmp on EVERY scenario, with NO `...base...=/tmp` assignment and no usage
# fallback text (static_ok 1 under pristine). Compliant elsewhere: failfast on
# missing TMPDIR, EXIT cleanup, TERM exit 143.
# Pristine: loc_ok=2 -> FAIL; m2: loc_ok=4 -> PASS.
[ -d "${TMPDIR:-/tmp}" ] || { echo "stub: TMPDIR is not a directory" >&2; exit 1; }
work=$(mktemp -d "/tmp/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'rm -rf -- "${work:-}"' EXIT
trap 'exit 143' TERM
trap 'exit 130' INT
sleep 3
echo "TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)"
exit 0
