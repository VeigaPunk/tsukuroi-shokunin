set -euo pipefail
base_txt=$(printf 'foo 1.0\n'; head -c 100000 /dev/zero | tr '\0' 'x' | fold -w 40)
bn=$(printf '%s\n' "$base_txt" | awk -v n=foo '$1 == n {print $2; exit}')
echo "survived bn=$bn"
