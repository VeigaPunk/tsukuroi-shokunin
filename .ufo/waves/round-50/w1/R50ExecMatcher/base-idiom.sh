#!/bin/bash
# Reproduce the base (b866a1d3) must-match idiom verbatim from tools/tsukuroi-census.sh:2384/2386/2390
set -euo pipefail
trial() { # trial BYTES_PER_LINE  -> 0 = matched, 1 = false miss
  local big probe
  big=$(printf '%*s' "$1" '' | tr ' ' x)
  probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
  if printf '%s\n' "$probe" | grep -q '^TSUKUROI_CENSUS: R50 marker'; then return 0; else return 1; fi
}
for size in 50000 100000 200000; do
  miss=0
  for i in $(seq 20); do
    trial "$size" || miss=$((miss+1))
  done
  printf 'base idiom size=%s bytes(total~%s) false_misses=%s/20\n' "$size" "$((size*2+40))" "$miss"
done
