#!/usr/bin/env bash
S=/fast/scratch/hyaku/tsukuroi-r48/TExecEdgeChars
. "$S/values.sh"
for i in "$@"; do
  entry=${vals[$i]}
  name=${entry%%|*}; val=${entry#*|}
  mark=$S/mark.$name; : > "$mark"
  out=$S/out.$name.log
  t0=$(date +%s)
  ( cd "$S" && env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$val" timeout 300 bash "$S/census.sh" --selftest ) >"$out" 2>&1
  rc=$?
  t1=$(date +%s)
  last=$(tail -1 "$out")
  leaked=$(find /tmp -maxdepth 1 -name 'tsukuroi-r3-2-selftest.*' -newer "$mark" | wc -l)
  remain=$(find -L "$val" -maxdepth 1 -name 'tsukuroi-r3-2-selftest.*' 2>/dev/null | wc -l)
  printf '%-12s rc=%-3s %3ss | last=%s | tmp_new=%s | remain=%s\n' "$name" "$rc" "$((t1-t0))" "$last" "$leaked" "$remain" | cat -v
done
