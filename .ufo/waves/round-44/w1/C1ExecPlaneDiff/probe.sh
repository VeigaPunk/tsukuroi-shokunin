#!/usr/bin/env bash
# C1-4 probe: run census at base and impl, alternating 3x each, capture stdout+exit.
set -u
S=/fast/scratch/hyaku/tsukuroi-r44/C1ExecPlaneDiff
export TMPDIR="$S/s"
cd "$S" || exit 9
for round in 1 2 3; do
  for rev in base impl; do
    out="$S/out-$rev-$round.txt"
    err="$S/err-$rev-$round.txt"
    /usr/bin/bash "$S/$rev.sh" >"$out" 2>"$err"
    rc=$?
    printf '%s\n' "$rc" >"$S/rc-$rev-$round.txt"
    printf 'round=%s rev=%s rc=%s lines=%s errbytes=%s\n' "$round" "$rev" "$rc" "$(wc -l <"$out")" "$(wc -c <"$err")"
  done
done
