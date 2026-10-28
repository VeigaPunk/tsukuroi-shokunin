
set -o pipefail
big=$(printf '%*s' 100000 '' | tr ' ' x)
probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
b=0 f=0 t=0
while [ "$t" -lt 20 ]; do
  t=$((t + 1))
  if ! printf '%s\n' "$probe" | grep -qE '^TSUKUROI_CENSUS: R50 marker'; then b=$((b + 1)); fi
  if ! printf '%s\n' "$probe" | RE='^TSUKUROI_CENSUS: R50 marker' awk '$0 ~ ENVIRON["RE"] { m = 1 } END { exit(m ? 0 : 1) }'; then f=$((f + 1)); fi
done
printf 'BASE_MISSES %d\nFULL_MISSES %d\n' "$b" "$f"
