#!/bin/bash
# PATH-shadowed mktemp used by every run in this seat's matrix. It logs the fd table of
# its own process and of its parent (the census bash) before delegating to the real mktemp,
# which is how the alias descriptor and its target directory were read out.
# Activated with PATH="<dir containing this file as 'mktemp'>:/usr/bin:/bin".
S=/fast/scratch/hyaku/tsukuroi-r48/TExecFdHold
{
  printf '== mktemp argv: %s\n' "$*"
  printf -- '-- self fds (%s):\n' "$$"
  ls -l /proc/self/fd 2>&1 | sed 's/^/   /'
  printf -- '-- parent %s fds:\n' "$PPID"
  ls -l "/proc/$PPID/fd" 2>&1 | sed 's/^/   /'
  printf -- '-- fdinfo high (>=10):\n'
  for f in /proc/$PPID/fdinfo/*; do n=${f##*/}; [ "$n" -ge 10 ] 2>/dev/null && { printf '   fd %s: ' "$n"; grep -E '^flags:' "$f" 2>/dev/null || echo missing; }; done
} >> "$S/logs/mktemp.log" 2>&1
exec /usr/bin/mktemp "$@"
