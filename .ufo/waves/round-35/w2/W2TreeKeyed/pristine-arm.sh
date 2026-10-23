
r35_arm() {
  local etc=${TSUKUROI_ETC_DIR:-/etc} log=${PACMAN_LOG:-/var/log/pacman.log} t
  t=$(mktemp -d)
  find "$etc" ! -type d \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacsave.[0-9]*' -o -name '*.pacorig' \) -print 2>"$t/err" >"$t/fs" || true
  local unr pn po ps lpn lps unl gone=0 tg l under
  unr=$(grep -c 'Permission denied' "$t/err" || true)
  pn=$(grep -c '\.pacnew$' "$t/fs" || true)
  po=$(grep -c '\.pacorig$' "$t/fs" || true)
  ps=$(( $(wc -l < "$t/fs") - pn - po ))
  { grep -E '^\[[^]]*\] \[ALPM\] warning: (/etc/.+) installed as \1\.pacnew$' "$log" 2>/dev/null || true; } | sed -E 's/^.* installed as //' > "$t/ln"
  { grep -E '^\[[^]]*\] \[ALPM\] warning: (/etc/.+) saved as \1\.pacsave$' "$log" 2>/dev/null || true; } | sed -E 's/^.* saved as //' > "$t/ls"
  lpn=$(wc -l < "$t/ln"); lps=$(wc -l < "$t/ls")
  while IFS= read -r l; do printf '/etc/%s\n' "${l#"$etc"/}"; done < "$t/fs" | sort -u > "$t/host"
  cat "$t/ln" "$t/ls" | sort -u > "$t/tg"
  unl=$(while IFS= read -r l; do printf '/etc/%s\n' "${l#"$etc"/}"; done < "$t/fs" | sort | comm -23 - "$t/tg" | wc -l)
  sed -nE "s#^find: '$etc/(.*)': Permission denied#/etc/\1/#p" "$t/err" > "$t/lk"
  while IFS= read -r tg; do
    grep -qxF -- "$tg" "$t/host" && continue
    under=0; while IFS= read -r l; do case "$tg" in "$l"*) under=1 ;; esac; done < "$t/lk"
    [ "$under" -eq 1 ] || gone=$((gone+1))
  done < "$t/tg"
  rm -rf "$t"
  printf 'DRIFT pacnew-plane pacnew=%s pacsave=%s pacorig=%s unreadable=%s log_pacnew=%s log_pacsave=%s unlogged=%s gone=%s\n' "$pn" "$ps" "$po" "$unr" "$lpn" "$lps" "$unl" "$gone"
}
