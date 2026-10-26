#!/bin/bash
# Reproduces the base expression (6951ead, tools/boot-chain-audit.sh:481-483) under set -uo pipefail.
set -uo pipefail
T=$(mktemp -d "$TMPDIR/repro.XXXXXX")
mkdir -p "$T/d/sub"; : >"$T/old"; : >"$T/d/sub/f"
touch -d @1000 -- "$T/old" "$T/d/sub/f" "$T/d/sub" "$T/d"
touch -d @3000 -- "$T/d/sub/f"
base_case() { # epoch, then paths
  local btime=$1; shift
  if find "$@" -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then printf '1\n'; else printf '0\n'; fi
}
a=$(base_case 2000 "$T/missing" "$T/old" "$T/d" 2>/dev/null)
new=$(find "$T/missing" "$T/old" "$T/d" -newermt "@2000" -print -quit 2>/dev/null); frc=$?
echo "BASE missing-start+deep-newer => $a (want 1); find_stdout='$new' find_rc=$frc"
b=$(base_case 2000 "$T/old" "$T/d" 2>/dev/null)
echo "BASE all-present+deep-newer  => $b (want 1)"
touch -d @1000 -- "$T/d/sub/f"
c=$(base_case 2000 "$T/missing" "$T/old" "$T/d" 2>/dev/null)
echo "BASE missing-start+none-newer=> $c (want 0)"
rm -rf -- "$T"
