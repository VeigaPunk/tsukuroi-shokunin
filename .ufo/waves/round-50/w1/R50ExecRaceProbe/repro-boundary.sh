#!/usr/bin/env bash
set -euo pipefail
gen() { awk -v n="$1" 'BEGIN{ total=0; i=0; target=int(n/2); done=0
  while (total < n) { l=sprintf("line %06d abcdefghijklmnopqrstuvwxyz 0123456789", i)
    if (!done && total>=target) { l="midstream"; done=1 }
    print l; total += length(l)+1; i++ } }'; }
for kb in 60 64 96; do
  buf=$(gen $(( kb * 1024 ))); miss=0
  for i in $(seq 20); do if printf '%s\n' "$buf" | grep -qE 'midstream'; then :; else miss=$((miss+1)); fi; done
  printf 'multi-line bytes=%d (nominal %d KiB) buflen=%d misses=%d/20\n' $(( kb * 1024 )) "$kb" "${#buf}" "$miss"
done
