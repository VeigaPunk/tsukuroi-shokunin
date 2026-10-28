#!/bin/bash
set -euo pipefail
# buf_has verbatim from freeze 2236-2239
buf_has() { printf '%s\n' "$1" | RE="$2" awk '$0 ~ ENVIRON["RE"] { f = 1 } END { exit(f ? 0 : 1) }'; }
trial() {
  local big probe
  big=$(printf '%*s' "$1" '' | tr ' ' x)
  probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
  buf_has "$probe" '^TSUKUROI_CENSUS: R50 marker'
}
for size in 50000 100000 200000 1000000; do
  miss=0
  for i in $(seq 20); do trial "$size" || miss=$((miss+1)); done
  printf 'buf_has size=%s bytes(total~%s) false_misses=%s/20\n' "$size" "$((size*2+40))" "$miss"
done
# absent-pattern arm: must reject
big=$(printf '%*s' 100000 '' | tr ' ' x); probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
if buf_has "$probe" '^TSUKUROI_CENSUS: absent marker'; then echo 'absent-arm: WRONGLY MATCHED'; else echo 'absent-arm: rejected (rc=1) as expected'; fi
