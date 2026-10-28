#!/bin/bash
set -euo pipefail
PLANE='PLANE update-safety: DEGRADED (status=REQUIRES-PREP; pending=REQUIRES-PREP(candidates=4002 join_behind=0 names=[alpha,beta,pad00000]); qu=rc=0/4002; sup=4002; join=equal=2 behind=0 ahead=0 src=sl+expac; expac=agree)'
re='^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=0/4002; sup=4002;'
for kb in 8 32 64 96 128; do
  n=$(( kb * 1024 / 2 ))
  pre=$(head -c $(( kb * 512 )) /dev/zero | tr '\0' 'a' | fold -w 60)
  post=$(head -c $(( kb * 512 )) /dev/zero | tr '\0' 'b' | fold -w 60)
  out="$pre
$PLANE
$post"
  miss=0
  for i in $(seq 1 20); do printf '%s\n' "$out" | grep -qE -- "$re" || miss=$((miss+1)); done
  hs=0
  for i in $(seq 1 20); do grep -qE -- "$re" <<<"$out" || hs=$((hs+1)); done
  echo "buffer ${kb} KiB: pipe-arm false misses $miss/20, herestring false misses $hs/20"
done
