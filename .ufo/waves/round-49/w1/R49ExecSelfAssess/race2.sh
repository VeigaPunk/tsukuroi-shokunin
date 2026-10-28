#!/bin/bash
set -euo pipefail
pre=$(head -c 400000 /dev/zero | tr '\0' 'a' | fold -w 60)
post=$(head -c 400000 /dev/zero | tr '\0' 'b' | fold -w 60)
PLANE='PLANE update-safety: DEGRADED (status=REQUIRES-PREP; pending=REQUIRES-PREP(candidates=4002 join_behind=0 names=[alpha,beta,pad00000]); qu=rc=0/4002; sup=4002; join=equal=2 behind=0 ahead=0 src=sl+expac; expac=agree)'
out="$pre
$PLANE
$post"
re='^PLANE update-safety: DEGRADED \(status=REQUIRES-PREP; pending=REQUIRES-PREP\(candidates=4002 join_behind=0 names=\[alpha,beta,pad00000\]\); qu=rc=0/4002; sup=4002;'
echo "out bytes: ${#out}"
miss=0
for i in $(seq 1 40); do
  grep -qE -- "$re" <<<"$out" || miss=$((miss+1))
done
echo "herestring arm: false misses $miss / 40"
mis=0
for i in $(seq 1 40); do
  printf '%s\n' "$out" | grep -qE -- "$re" || mis=$((mis+1))
done
echo "pipe arm (pipefail ON): false misses $mis / 40"
