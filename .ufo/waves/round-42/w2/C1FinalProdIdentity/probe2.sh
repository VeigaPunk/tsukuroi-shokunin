#!/bin/bash
# Mechanism probe at production identity: is the base census's verdict flip really
# pipefail+SIGPIPE on the early reader, and where is the size boundary?
set -euo pipefail

err='error: alpha: /usr/bin/x-PROBE (Permission denied)'
pad() { printf 'warning: pkg-%06d: /usr/share/doc/p.txt (Size mismatch)\n' $(seq 1 "$1"); }

probe() { # $1 label, $2 buffer
  ( set +e
    printf '%s\n' "$2" | grep -q '^error:'
    st="${PIPESTATUS[*]}"
    printf 'PLANE packages: PIPE %-9s len=%7d pipestatus=[%s]\n' "$1" "${#2}" "$st"
  )
}

small=$(printf '%s\nalpha: 10 total files, 0 altered files\n' "$err")
mid=$(printf '%s\n%s\n' "$err" "$(pad 900)")     # ~ 50 KiB
big=$(printf '%s\n%s\n' "$err" "$(pad 12000)")   # ~ 700 KiB
for c in small mid big; do probe "$c" "${!c}"; done

# control: the tip's awk reader over the same big buffer (must be status 0 and find the line)
( set +e
  line=$(printf '%s\n' "$big" | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }')
  rc=$?
  printf 'PLANE packages: AWK  big       len=%7d rc=%d first=%s\n' "${#big}" "$rc" "${line:0:40}"
)
