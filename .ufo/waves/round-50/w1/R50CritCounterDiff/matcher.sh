set -euo pipefail
buf_has() { printf '%s\n' "$1" | RE="$2" awk '$0 ~ ENVIRON["RE"] { f = 1 } END { exit(f ? 0 : 1) }'; }
old_has() { printf '%s\n' "$1" | grep -qE -- "$2"; }
for sz in 65536 98304 100000; do
  big=$(printf '%*s' "$sz" '' | tr ' ' x)
  probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
  om=0; nm=0; t=0
  while [ "$t" -lt 20 ]; do
    t=$((t+1))
    old_has "$probe" '^TSUKUROI_CENSUS: R50 marker' || om=$((om+1))
    buf_has "$probe" '^TSUKUROI_CENSUS: R50 marker' || nm=$((nm+1))
  done
  printf 'size=%d old_idiom_false_misses=%d/20 new_matcher_false_misses=%d/20\n' "$sz" "$om" "$nm"
done
