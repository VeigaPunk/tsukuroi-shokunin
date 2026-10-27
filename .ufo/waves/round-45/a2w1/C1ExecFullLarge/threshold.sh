#!/usr/bin/env bash
# Observed SIGPIPE threshold for the base S1 statement (bash -c child, SIGPIPE at default).
set +e
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecFullLarge
for lines in 0 1000 1200 1300 1500 2000 4000; do
  awk -v n="$lines" 'BEGIN{printf "running\n"; for(i=0;i<n;i++) printf "pad-line %05d ..................................................\n", i}' > "$S/thr.txt"
  bytes=$(wc -c < "$S/thr.txt")
  out=$(bash -c "set -euo pipefail; CAP_OUT=\$(cat '$S/thr.txt'); state=\$(printf '%s\n' \"\$CAP_OUT\" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+\$//'); printf '%s' \"\$state\"" 2>&1); rc=$?
  printf 'pad_lines=%-5s bytes=%-7s rc=%s out=%s\n' "$lines" "$bytes" "$rc" "$(printf '%s' "$out" | head -c 40)"
done
