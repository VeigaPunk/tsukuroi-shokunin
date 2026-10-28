set -euo pipefail
old_has() { printf '%s\n' "$1" | grep -qE -- "$2"; }
sz=98304
big=$(printf '%*s' "$sz" '' | tr ' ' x)
probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
for batch in 1 2 3 4 5; do
  m=0; t=0
  while [ "$t" -lt 20 ]; do t=$((t+1)); old_has "$probe" '^TSUKUROI_CENSUS: R50 marker' || m=$((m+1)); done
  printf 'batch%d 96KiB old-idiom false-misses=%d/20\n' "$batch" "$m"
done
