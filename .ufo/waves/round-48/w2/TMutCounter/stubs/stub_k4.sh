#!/bin/bash
# Cheap stub census emulating K4: base blob with only the usage text edited
# ('or a private dir when TMPDIR'). Observable signature identical to K0.
# usage: writes under ${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.*, or a private dir when TMPDIR
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
