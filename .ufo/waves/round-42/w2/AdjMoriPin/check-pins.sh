#!/usr/bin/env bash
# AdjMoriPin F-18: check whether pinned lane content moved between base and dispatch tip.
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
BASE=c8efaa3f120834541f8de1e5e0367e8d1593bae6
TIP=78abb8b5cdc9da511b4fc523e661517a68dd33d3

check() {
  local file="$1" line="$2"
  local b t
  b=$(git -C "$LANE" show "$BASE:$file" 2>/dev/null | sed -n "${line}p")
  t=$(git -C "$LANE" show "$TIP:$file" 2>/dev/null | sed -n "${line}p")
  if [ "$b" = "$t" ]; then
    printf 'SAME   %s:%s\n' "$file" "$line"
  else
    printf 'MOVED  %s:%s\n  base: %s\n  tip : %s\n' "$file" "$line" "$b" "$t"
  fi
}

# mado r12 evidence -> SKILL.md
for L in 101 404 755 842; do check SKILL.md "$L"; done
# mori PROVINCE.md live pins
for L in 8 14 30 33; do check PROVINCE.md "$L"; done
# mori SKILL.md live pin
check PROVINCE.md 19
# revenger knowledge pin
check PROVINCE.md 51
# souji r12 connector
for L in 3 18; do check PROVINCE.md "$L"; done
# souji r32 pins
for L in 50 95 96 219 3452; do check SKILL.md "$L"; done
check corpus/README.md 7
check corpus/SOURCES.md 105
# souji r33 pins
for L in 2870 2940 3001 3106; do check SKILL.md "$L"; done
# tameshi knowledge pins
for L in 558 568 599 609 611 617 1059 1063; do check SKILL.md "$L"; done
for L in 915 970; do check tools/tsukuroi-census.sh "$L"; done
