#!/bin/sh
# Ordinary-run check wrapper (seat MutOneTargetSkipWork): record argv, the ZZ_R34_AMBIENT line
# and the environment NAMES (no values) of this git child, then exec the real git.
# Bounded: at most 200 dump files in the dump directory.
d=/fast/scratch/hyaku/tsukuroi-r34/MutOneTargetSkipWork/ordinary/dumps
if [ -d "$d" ]; then
  n=$(/usr/bin/ls -1 "$d" | /usr/bin/wc -l)
  if [ "$n" -lt 200 ]; then
    {
      echo "argv: $*"
      /usr/bin/env | /usr/bin/grep -E '^ZZ_R34_AMBIENT='
      echo "names: $(/usr/bin/env | /usr/bin/cut -d= -f1 | /usr/bin/sort | /usr/bin/tr '\n' ' ')"
    } > "$d/env.$$"
  fi
fi
exec /usr/bin/git "$@"
