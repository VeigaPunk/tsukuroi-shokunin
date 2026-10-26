#!/usr/bin/env bash
# C1ExecLiveLarge: race census of the BASE row :692 pipeline on live-sized buffers.
# Usage: race.sh <buffer> <iterations>
# Each iteration: error token at the head of the buffer, then `printf | grep -q '^error:'`
# under `set -uo pipefail` exactly as the base census evaluates the row.
set -uo pipefail
BUF=$1
N=$2
s_out=$( { printf 'error: probe failure example\n'; cat "$BUF"; } )
bytes=$(printf '%s' "$s_out" | wc -c)
c0=0; c1=0; c141=0; cother=0
i=0
while [ "$i" -lt "$N" ]; do
  printf '%s\n' "$s_out" | grep -q '^error:'
  rc=$?
  case $rc in
    0) c0=$((c0 + 1)) ;;
    1) c1=$((c1 + 1)) ;;
    141) c141=$((c141 + 1)) ;;
    *) cother=$((cother + 1)) ;;
  esac
  i=$((i + 1))
done
printf 'buffer=%s bytes=%s iterations=%s rc0(match->BLOCKED)=%s rc1(no-match)=%s rc141(SIGPIPE->wrong)=%s other=%s\n' \
  "$(basename "$BUF")" "$bytes" "$N" "$c0" "$c1" "$c141" "$cother"
