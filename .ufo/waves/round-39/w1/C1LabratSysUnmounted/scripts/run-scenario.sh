#!/usr/bin/env bash
# Runs both census revisions in the current environment; writes raw output per revision.
set -u
S=$1
for v in impl base; do
  out="$S/rec/$v.out"
  TMPDIR="$S/tmp" bash "$S/bin/census-$v.sh" > "$out" 2>"$S/rec/$v.err"
  printf '%s rc=%d\n' "$v" "$?" >> "$S/rec/rc.txt"
done
