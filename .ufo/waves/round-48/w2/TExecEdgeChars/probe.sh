#!/usr/bin/env bash
S=/fast/scratch/hyaku/tsukuroi-r48/TExecEdgeChars
. "$S/resolver.sh"
probe() {
  local name=$1 val=$2 rc base fd real
  ( cd "$S" || exit 9
    TMPDIR="$val" selftest_base_dir; rc=$?
    base=$ST_BASE_DIR; fd=$ST_BASE_FD
    real=; if [ -n "$base" ]; then real=$(readlink -f -- "$base" 2>&1); fi
    printf '%-10s rc=%s fd=<%s> base=<%s> real=<%s>\n' "$name" "$rc" "$fd" "$base" "$real" | cat -v
  )
}
probe e1tab   $'e1tab\tx'
probe e2nl    $'e2nl\nx'
probe e3sq    "e3sq'uote"
probe e4dq    'e4dq"uote'
probe e5dollar 'e5$HOME'
probe e6btick 'e6`bt'
probe e7star  'e7st*ar'
probe e8dash  "$S/e8/-x"
probe e9eq    'e9eq=1'
probe e10slash 'e10slash/'
probe e11link 'e11link'
probe e12rel  'e12 rel dir'
probe e13long "$(printf 'e13%s' "$(printf 'a%.0s' $(seq 200))")"
probe e14uni  'e14üñí'
echo "--- injection payloads ---"
mkdir -p 'inj-a"; touch '"$S"'/PWNED-A; echo "' 'inj-b$(touch '"$S"'/PWNED-B)' 'inj-c`touch '"$S"'/PWNED-C`'
probe inja 'inj-a"; touch '"$S"'/PWNED-A; echo "'
probe injb 'inj-b$(touch '"$S"'/PWNED-B)'
probe injc 'inj-c`touch '"$S"'/PWNED-C`'
ls "$S"/PWNED-* 2>/dev/null || echo 'no PWNED files: no injection'
