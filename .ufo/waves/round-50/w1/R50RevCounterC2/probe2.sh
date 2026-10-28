set -o pipefail
big=$(printf '%*s' 100000 '' | tr ' ' x)
buf=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
RE='^TSUKUROI_CENSUS: R50 marker'
m=0; for t in $(seq 20); do printf '%s\n' "$buf" | grep -qE "$RE" || m=$((m+1)); done; echo "A banned (\"\$out\")            misses=$m/20"
m=0; for t in $(seq 20); do printf '%s\n' "${buf}" | grep -qE "$RE" || m=$((m+1)); done; echo "B braced (\"\${out}\")           misses=$m/20"
m=0; for t in $(seq 20); do printf "%s\n" "$buf" | grep -qE "$RE" || m=$((m+1)); done; echo "C dq format string           misses=$m/20"
m=0; for t in $(seq 20); do printf '%s\n' "$buf" | grep -m1 -E "$RE" >/dev/null || m=$((m+1)); done; echo "D grep -m1                   misses=$m/20"
m=0; for t in $(seq 20); do grep -qE "$RE" <<<"$buf" || m=$((m+1)); done; echo "E here-string (no writer)    misses=$m/20"
m=0; for t in $(seq 20); do printf '%s\n' "$buf" | RE="$RE" awk '$0 ~ ENVIRON["RE"] { f=1 } END { exit(f?0:1) }' || m=$((m+1)); done; echo "F full-read awk (the fix)    misses=$m/20"
