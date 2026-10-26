#!/bin/bash
set -uo pipefail
# Base semantics (find|grep -q .) under the SAME three R43-C1 cases, run verbatim otherwise.
inputs_newer_than_base() {
  local epoch=$1; shift
  if find "$@" -newermt "@$epoch" -print -quit 2>/dev/null | grep -q .; then printf '1\n'; else printf '0\n'; fi
}
T=$(mktemp -d "$TMPDIR/cases.XXXXXX")
bi="$T/bootinputs"; mkdir -p -- "$bi/d/sub"; : >"$bi/old"; : >"$bi/d/sub/f"
touch -d @1000 -- "$bi/old" "$bi/d/sub/f" "$bi/d/sub" "$bi/d"
pass=0; fail=0
chk(){ if [ "$2" = "$3" ]; then echo "PASS $1 (want $2 got $3)"; pass=$((pass+1)); else echo "FAIL $1 (want $2 got $3)"; fail=$((fail+1)); fi; }
got=$(inputs_newer_than_base 2000 "$bi/missing" "$bi/old" "$bi/d"); chk R43-C1-missing-start-point-none-newer 0 "$got"
touch -d @3000 -- "$bi/d/sub/f"
got=$(inputs_newer_than_base 2000 "$bi/missing" "$bi/old" "$bi/d"); chk R43-C1-missing-start-point-deep-newer 1 "$got"
got=$(inputs_newer_than_base 2000 "$bi/old" "$bi/d"); chk R43-C1-all-present-deep-newer 1 "$got"
echo "BASE-SEMANTICS: pass=$pass fail=$fail"
rm -rf -- "$T"
