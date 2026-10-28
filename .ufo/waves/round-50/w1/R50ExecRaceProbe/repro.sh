#!/usr/bin/env bash
set -euo pipefail
mkbuf() {
  local n=$1 half=$(( $1 / 2 ))
  { head -c "$half" /dev/zero | tr '\0' 'a'; printf '\nmidstream\n'; head -c "$(( n - half ))" /dev/zero | tr '\0' 'b'; }
}
for size in 102400 204800 409600; do
  buf=$(mkbuf "$size")
  miss=0; hits=0; rcs=""
  for i in $(seq 20); do
    set +e
    printf '%s\n' "$buf" | grep -qE 'midstream'
    rc=$?
    set -e
    if [ "$rc" -eq 0 ]; then hits=$((hits+1)); else miss=$((miss+1)); rcs="$rcs $rc"; fi
  done
  printf 'requested=%d buflen=%d misses=%d hits=%d nonmatch_rcs:%s\n' "$size" "${#buf}" "$miss" "$hits" "${rcs:- none}"
done
