#!/bin/bash
# Reproduce the check() pipeline shape (census:2372) and map the SIGPIPE/pipefail race zone.
set -uo pipefail
pat="root_status=ok root_mode=0755 root_uid=[0-9]+ root_gid=[0-9]+"
for tail_kb in 1 8 32 48 60 63 64 65 80 128 300; do
  out=$( { printf "HEAD\nroot_status=ok root_mode=0755 root_uid=1000 root_gid=1000 root_euid=1000\n"; head -c $((tail_kb*1024)) /dev/zero | tr "\0" "Z"; printf "\n"; } )
  fails=0; rcs=""
  for i in $(seq 1 10); do
    printf "%s\n" "$out" | grep -qE -- "$pat"; rc=$?
    [ "$rc" -ne 0 ] && fails=$((fails+1)); rcs="$rcs$rc"
  done
  printf "tail_kb=%-4s len=%-7s fails=%s/10 rcs=%s\n" "$tail_kb" "${#out}" "$fails" "$rcs"
done
