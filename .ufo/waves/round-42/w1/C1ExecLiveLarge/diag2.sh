#!/usr/bin/env bash
# C1ExecLiveLarge diag2: replay the BASE and IMPL packages-plane early readers on a
# captured live pacman buffer (no TSUKUROI_* overrides, real local DB).
# Usage: diag2.sh <captured-buffer-file>
set -uo pipefail
BUF=$(cat "$1")
CAP_OUT=$BUF
printf 'buffer bytes=%s lines=%s error_lines=%s first_error_line_no=%s\n' \
  "$(printf '%s' "$CAP_OUT" | wc -c)" "$(printf '%s\n' "$CAP_OUT" | wc -l)" \
  "$(printf '%s\n' "$CAP_OUT" | grep -c '^error:' || true)" \
  "$(printf '%s\n' "$CAP_OUT" | grep -n '^error:' | head -n1 | cut -d: -f1 || true)"

# BASE rows :692/:694 exactly as committed at c8efaa3
s_out=$(printf '%s\n' "$CAP_OUT" | tr '\r' '\n')
set +e
printf '%s\n' "$s_out" | grep -q '^error:'
base_q_rc=$?
set -e
set +e
if printf '%s\n' "$s_out" | grep -q '^error:'; then
  base_verdict=BLOCKED
  base_note="pacman -Qkk sample probe error: $(printf '%s\n' "$s_out" | grep -m1 '^error:')"
else
  base_verdict=NOT-BLOCKED
  base_note=''
fi
set -e
printf 'BASE grep-q pipeline rc=%s -> verdict=%s note=%q\n' "$base_q_rc" "$base_verdict" "$base_note"

# IMPL rows :692/:694 exactly as committed at 44766208
set +e
grep -q '^error:' <<<"$s_out"
impl_q_rc=$?
set -e
if grep -q '^error:' <<<"$s_out"; then
  impl_verdict=BLOCKED
  impl_note="pacman -Qkk sample probe error: $(grep -m1 '^error:' <<<"$s_out")"
else
  impl_verdict=NOT-BLOCKED
  impl_note=''
fi
printf 'IMPL here-string rc=%s -> verdict=%s note=%q\n' "$impl_q_rc" "$impl_verdict" "$impl_note"
