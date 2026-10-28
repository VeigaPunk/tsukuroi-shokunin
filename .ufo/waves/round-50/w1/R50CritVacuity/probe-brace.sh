set -o pipefail
big=$(printf '%*s' 100000 '' | tr ' ' x)
out=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
b=0 t=0
while [ "$t" -lt 20 ]; do
  t=$((t + 1))
  if ! printf '%s\n' "${out}" | grep -qE '^TSUKUROI_CENSUS: R50 marker'; then b=$((b + 1)); fi
done
printf 'BRACE_MISSES %d\n' "$b"
