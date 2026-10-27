set -euo pipefail
CAP=$(awk 'BEGIN { for (i = 0; i < 20000; i++) printf "pad line %05d ................................................\n", i }')
x=${CAP%%$'\n'*}
printf 'survived: [%s]\n' "$x"
