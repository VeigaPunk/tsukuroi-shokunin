#!/usr/bin/env python3
"""C1-9 evasion variant V2: the early readers stay for every buffer that fits a pipe; only
buffers over the 64 KiB pipe capacity take the consuming path.

Usage: variant-v2.py <lane-clone>   (rewrites tools/tsukuroi-census.sh from the BASE revision)
"""
import subprocess
import sys

BASE = 'c8efaa3f120834541f8de1e5e0367e8d1593bae6'
CENSUS = 'tools/tsukuroi-census.sh'

GATE_ANCHOR = "CHANNEL_ARCHIVE='offline.db'   # the offline-exile preservation archive, not a channel\nEXPAC_FMT=$'%n\\t%v'\n"
GATE = GATE_ANCHOR + """
# ---- (variant C1-9/V2) size gate ----------------------------------------------------
# Keep the R41 early readers for any buffer that fits a pipe; only a sample larger than the
# 64 KiB pipe capacity is read through a consuming filter. No environment or namespace sniff.
r42_head() { # r42_head N : first N lines of $CAP_OUT; the small branch keeps the early reader
  if [ "${#CAP_OUT}" -gt 65536 ]; then awk -v n="$1" 'NR <= n'; else head -n "$1"; fi
}
"""

PKG_OLD = """  if printf '%s\\n' "$s_out" | grep -q '^error:'; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\\n' "$s_out" | grep -m1 '^error:')"
    return
  fi
"""
PKG_NEW = """  if { [ "${#s_out}" -gt 65536 ] && grep -q '^error:' <<<"$s_out"; } \\
     || { [ "${#s_out}" -le 65536 ] && printf '%s\\n' "$s_out" | grep -q '^error:'; }; then
    PKG_V=BLOCKED
    if [ "${#s_out}" -gt 65536 ]; then
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
    print('variant V2 written', len(src))


if __name__ == '__main__':
    main()
