set -euo pipefail
CAP=$(awk 'BEGIN { for (i = 0; i < 20000; i++) printf "pad line %05d ................................................\n", i }')
x=$(printf '%s\n' "$CAP" | head -n1)
printf 'survived: [%s]\n' "$x"
