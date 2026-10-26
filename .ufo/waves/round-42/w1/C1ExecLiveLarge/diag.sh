#!/usr/bin/env bash
# C1ExecLiveLarge diag: replay the BASE early-reader shapes on a live-sized buffer.
# Data: a real `pacman -Qkk` sample from this host, 65567 bytes (> 65536 pipe capacity).
# Case A/D feed the same buffer with one line-start `error:` token prepended (the shape the
# R42-C1 selftest fixture builds); cases B/C use the unmodified live buffer.
set -uo pipefail
S=$(cd "$(dirname "$0")" && pwd)
BUF=$S/$1
sz=$(wc -c < "$BUF")
echo "buffer=$BUF bytes=$sz pipe_capacity=65536 (fcntl F_GETPIPE_SZ)"
err_at_head=$( { printf 'error: probe failure example\n'; cat "$BUF"; } )

# A: base row :692 ( `printf | grep -q` ) on a >64KiB buffer whose first line is an error token
( set -euo pipefail
  s_out=$err_at_head
  set +e
  printf '%s\n' "$s_out" | grep -q '^error:'; rc=$?
  set -e
  echo "A_pipeline_rc=$rc"
  if printf '%s\n' "$s_out" | grep -q '^error:'; then echo "A_verdict=BLOCKED"; else echo "A_verdict=NOT-BLOCKED (correct=BLOCKED)"; fi
)

# B: base row :692 on the unmodified live buffer (no error token at all)
( set -euo pipefail
  s_out=$(cat "$BUF")
  set +e
  printf '%s\n' "$s_out" | grep -q '^error:'; rc=$?
  set -e
  echo "B_pipeline_rc=$rc (1 = no match, correct verdict path)"
)

# C: impl rows :692/:694 (here-string) on the error-at-head buffer
( set -euo pipefail
  s_out=$err_at_head
  set +e
  grep -q '^error:' <<<"$s_out"; rc=$?
  set -e
  echo "C_herestring_rc=$rc (0 = error seen)"
  if grep -q '^error:' <<<"$s_out"; then echo "C_verdict=BLOCKED"; else echo "C_verdict=NOT-BLOCKED"; fi
)

# D: base row :694 in an assignment (`$(printf | grep -m1)`): does the census survive?
( set -euo pipefail
  s_out=$err_at_head
  note=$(printf '%s\n' "$s_out" | grep -m1 '^error:')
  echo "D_survived note=$note"
)
echo "D_subshell_rc=$? (141 = killed by SIGPIPE)"
