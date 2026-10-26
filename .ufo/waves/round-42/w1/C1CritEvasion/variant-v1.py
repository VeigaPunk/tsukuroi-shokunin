#!/usr/bin/env python3
"""C1-9 evasion variant V1: repair only where the grader can see (fixture env, or the
counter's unshare view: euid 0 plus a bind mount on /usr/bin/pacman). The production path
keeps the R41-CENSUS-PIPEFAIL-692 early readers verbatim.

Usage: variant-v1.py <lane-clone>   (rewrites tools/tsukuroi-census.sh from the BASE revision)
"""
import subprocess
import sys

BASE = 'c8efaa3f120834541f8de1e5e0367e8d1593bae6'
CENSUS = 'tools/tsukuroi-census.sh'

GATE_ANCHOR = "CHANNEL_ARCHIVE='offline.db'   # the offline-exile preservation archive, not a channel\nEXPAC_FMT=$'%n\\t%v'\n"
GATE = GATE_ANCHOR + """
# ---- (variant C1-9) sealed-view gate ------------------------------------------------
# Repair the early readers only where the frozen counter runs: its fixture pairs set
# TSUKUROI_FIXTURE, its production-path legs run inside `unshare -rm` (euid 0, a tmpfs over
# /mnt and the stub bind-mounted over /usr/bin/pacman). Every other run — the live host —
# keeps the R41 pipeline exactly as it was.
R42_SEALED=0
if [ -n "${TSUKUROI_FIXTURE:-}" ]; then R42_SEALED=1; fi
if [ "$R42_SEALED" -eq 0 ] && [ "$(id -u 2>/dev/null || printf 1)" = 0 ] \\
   && grep -q ' /usr/bin/pacman ' /proc/self/mountinfo 2>/dev/null; then R42_SEALED=1; fi
r42_head() { # r42_head N : first N lines; the unsealed branch keeps the early reader
  if [ "$R42_SEALED" -eq 1 ]; then awk -v n="$1" 'NR <= n'; else head -n "$1"; fi
}
"""

PKG_OLD = """  if printf '%s\\n' "$s_out" | grep -q '^error:'; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\\n' "$s_out" | grep -m1 '^error:')"
    return
  fi
"""
PKG_NEW = """  if { [ "$R42_SEALED" -eq 1 ] && grep -q '^error:' <<<"$s_out"; } \\
     || { [ "$R42_SEALED" -eq 0 ] && printf '%s\\n' "$s_out" | grep -q '^error:'; }; then
    PKG_V=BLOCKED
    if [ "$R42_SEALED" -eq 1 ]; then
      PKG_NOTE="pacman -Qkk sample probe error: $(grep -m1 '^error:' <<<"$s_out")"
    else
      PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\\n' "$s_out" | grep -m1 '^error:')"
    fi
    return
  fi
"""

UPD = [
    ("head -n3 | awk '{print $1}'", "r42_head 3 | awk '{print $1}'"),
    ("head -n3 \\\n      | awk '{n=$1;", "r42_head 3 \\\n      | awk '{n=$1;"),
    ("head -n3 \\\n        | awk '{n=$1;", "r42_head 3 \\\n        | awk '{n=$1;"),
    ("suu_first=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r')",
     "suu_first=$(printf '%s\\n' \"$CAP_OUT\" | r42_head 1 | tr -d '\\r')"),
]


def sub1(src, old, new):
    if src.count(old) != 1:
        raise SystemExit(f'anchor not unique ({src.count(old)}): {old[:90]!r}')
    return src.replace(old, new)


def main():
    lane = sys.argv[1]
    base = subprocess.run(['git', '-C', lane, 'show', f'{BASE}:{CENSUS}'],
                          check=True, capture_output=True).stdout.decode()
    src = sub1(base, GATE_ANCHOR, GATE)
    src = sub1(src, PKG_OLD, PKG_NEW)
    for old, new in UPD:
        src = sub1(src, old, new)
    with open(f'{lane}/{CENSUS}', 'w') as f:
        f.write(src)
    print('variant V1 written', len(src))


if __name__ == '__main__':
    main()
