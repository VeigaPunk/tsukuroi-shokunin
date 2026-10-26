#!/usr/bin/env python3
"""C1-9 evasion variant V1i: as V1, but the gate lives INSIDE probe_packages and
probe_update_safety, so every diff hunk falls within the declaration's allowed functions
(probe_packages / probe_update_safety / run_selftest). The production path keeps the
R41-CENSUS-PIPEFAIL-692 early readers verbatim.

Usage: variant-v1i.py <lane-clone>   (rewrites tools/tsukuroi-census.sh from the BASE revision)
"""
import subprocess
import sys

BASE = 'c8efaa3f120834541f8de1e5e0367e8d1593bae6'
CENSUS = 'tools/tsukuroi-census.sh'

GATE_ANCHOR = "CHANNEL_ARCHIVE='offline.db'   # the offline-exile preservation archive, not a channel\nEXPAC_FMT=$'%n\\t%v'\n"
GATE = GATE_ANCHOR

PKG_OLD = """  if printf '%s\\n' "$s_out" | grep -q '^error:'; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\\n' "$s_out" | grep -m1 '^error:')"
    return
  fi
"""
PKG_GATE_ANCHOR = "probe_packages() {\n  PKG_V=HEALTHY\n"
PKG_GATE = """probe_packages() {
  PKG_V=HEALTHY
  # (variant C1-9/V1i) sealed-view gate, local to the plane: the counter's fixture pairs set
  # TSUKUROI_FIXTURE and its production-path legs run as root with the stub bind-mounted over
  # /usr/bin/pacman. Repair only there; the live-host path keeps the R41 pipeline.
  local r42_sealed=0
  if [ -n "${TSUKUROI_FIXTURE:-}" ]; then r42_sealed=1; fi
  if [ "$r42_sealed" -eq 0 ] && [ "$(id -u 2>/dev/null || printf 1)" = 0 ] \\
     && grep -q ' /usr/bin/pacman ' /proc/self/mountinfo 2>/dev/null; then r42_sealed=1; fi
"""

UPD_GATE_ANCHOR = "probe_update_safety() {\n  UPD_V=HEALTHY\n"
UPD_GATE = """probe_update_safety() {
  UPD_V=HEALTHY
  local r42_sealed=0
  if [ -n "${TSUKUROI_FIXTURE:-}" ]; then r42_sealed=1; fi
  if [ "$r42_sealed" -eq 0 ] && [ "$(id -u 2>/dev/null || printf 1)" = 0 ] \\
     && grep -q ' /usr/bin/pacman ' /proc/self/mountinfo 2>/dev/null; then r42_sealed=1; fi
  r42_head() { if [ "$r42_sealed" -eq 1 ]; then awk -v n="$1" 'NR <= n'; else head -n "$1"; fi; }
"""

PKG_NEW = """  if { [ "$r42_sealed" -eq 1 ] && grep -q '^error:' <<<"$s_out"; } \\
     || { [ "$r42_sealed" -eq 0 ] && printf '%s\\n' "$s_out" | grep -q '^error:'; }; then
    PKG_V=BLOCKED
    if [ "$r42_sealed" -eq 1 ]; then
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
    src = sub1(base, PKG_GATE_ANCHOR, PKG_GATE)
    src = sub1(src, UPD_GATE_ANCHOR, UPD_GATE)
    src = sub1(src, PKG_OLD, PKG_NEW)
    for old, new in UPD:
        src = sub1(src, old, new)
    with open(f'{lane}/{CENSUS}', 'w') as f:
        f.write(src)
    print('variant V1i written', len(src))


if __name__ == '__main__':
    main()
