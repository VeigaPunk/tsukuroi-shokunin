cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
BASE=2f3061ef; REV=2f3061ef; fail=0
while read -r F ea er; do
  got=$(git --no-pager diff --no-index --numstat \
        <(git show "$BASE":"$F" | tr -d '\r') <(git show "$REV":"$F") 2>/dev/null || true)
  a=$(printf '%s\n' "$got" | awk 'NF{print $1; exit}'); a=${a:-0}
  r=$(printf '%s\n' "$got" | awk 'NF{print $2; exit}'); r=${r:-0}
  printf '%-18s added=%-4s removed=%-3s (expected %s/%s)\n' "$F" "$a" "$r" "$ea" "$er"
  { [ "$a" = "$ea" ] && [ "$r" = "$er" ]; } || fail=1
done <<'EOF'
corpus/SOURCES.md 3 0
SKILL.md 120 1
SCORECARD.md 0 0
EOF
echo "gate rc=$fail"; exit "$fail"
