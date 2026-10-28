#!/usr/bin/env bash
set -euo pipefail
mkbuf() { local n=$1 half=$(( $1 / 2 )); { head -c "$half" /dev/zero | tr '\0' 'a'; printf '\nmidstream\n'; head -c "$(( n - half ))" /dev/zero | tr '\0' 'b'; }; }
for size in 65536 81920 98304 102400 131072 204800 409600; do
  buf=$(mkbuf "$size"); miss=0; hits=0
  for i in $(seq 20); do
    if printf '%s\n' "$buf" | grep -qE 'midstream'; then hits=$((hits+1)); else miss=$((miss+1)); fi
  done
  printf 'bytes=%d buflen=%d misses=%d/20 hits=%d\n' "$size" "${#buf}" "$miss" "$hits"
done
