#!/usr/bin/env bash
# read-only stub: answers -Qkk from $QKK_OUT, delegates everything else to the real pacman
for a in "$@"; do
  if [ "$a" = "-Qkk" ]; then cat -- "$QKK_OUT"; exit "${QKK_RC:-1}"; fi
done
exec /usr/bin/pacman "$@"
