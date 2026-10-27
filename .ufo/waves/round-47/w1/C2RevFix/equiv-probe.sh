#!/usr/bin/env bash
# Equivalence probe: st_base guard fallback decision must equal root_locator_class refusal
# on the derived work path (suffix "tsukuroi-r3-2-selftest.<alnum>" is always in-charset).
. /fast/scratch/hyaku/tsukuroi-r47/C2RevFix/rlc-fn.sh
fail=0
probe() {
  local t="$1" cls guard
  cls=$(root_locator_class "$t/suf")
  guard=keep
  case "$t" in
    *[!A-Za-z0-9._/+-]*) guard=/tmp ;;
  esac
  if [ "$cls" = 'unsafe' ] && [ "$guard" != '/tmp' ]; then printf 'MISMATCH %q cls=%s guard=keep\n' "$t" "$cls"; fail=1; fi
  if [ "$cls" != 'unsafe' ] && [ "$guard" = '/tmp' ]; then printf 'MISMATCH %q cls=%s guard=/tmp\n' "$t" "$cls"; fail=1; fi
}
probe '/x y'; probe '/x=y'; probe "$(printf '/x\ty')"; probe "$(printf '/x\ny')"
probe '/x@y'; probe '/x#y'; probe '/x%y'; probe '/x,y'; probe '/x:y'
probe '/x"y'; probe "/x'y"; probe '/x\y'; probe "$(printf '/x\x7fy')"; probe '/xéy'
probe '/x*y'; probe '/x?y'; probe '/x[y'; probe '/x]y'; probe '/x(y'; probe '/x)y'
probe '/x!y'; probe '/x~y'; probe '/x`y'; probe '/x$y'; probe '/x&y'; probe '/x;y'
for i in $(seq 33 126); do
  c=$(printf "\\$(printf '%03o' "$i")")
  probe "/aa${c}bb"
done
# in-charset controls: must stay keep/absolute
for ok in /tmp /var/tmp /fast/scratch/hyaku/tsukuroi-r47 '/x.y_z-+/a'; do
  cls=$(root_locator_class "$ok/suf")
  [ "$cls" = 'absolute' ] || { printf 'KEEP-MISMATCH %q cls=%s\n' "$ok" "$cls"; fail=1; }
done
[ "$fail" -eq 0 ] && echo "EQUIVALENCE: guard fallback == locator refusal on all 104 probes; in-charset controls stay absolute"
