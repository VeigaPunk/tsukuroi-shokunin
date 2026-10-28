set -o pipefail
big=$(printf '%*s' 100000 '' | tr ' ' x)
probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
b=0 f=0 t=0
while [ "$t" -lt 20 ]; do
  t=$((t + 1))
  if ! printf '%s\n' "$probe" | grep -q '^TSUKUROI_CENSUS: R50 marker'; then b=$((b + 1)); fi
  if ! printf '%s\n' "${probe}" | grep -q '^TSUKUROI_CENSUS: R50 marker'; then f=$((f + 1)); fi
done
printf 'PLAIN_MISSES %d\nBRACED_MISSES %d\n' "$b" "$f"
