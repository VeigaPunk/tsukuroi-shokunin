#!/usr/bin/env python3
"""Regenerate the five round-39 storage-block mutants used by seat SimplifyArm (R-4).

usage: mutants.py CENSUS_SOURCE OUTDIR
  CENSUS_SOURCE = tools/tsukuroi-census.sh at 49cc53c (e.g. `git show 49cc53c:tools/tsukuroi-census.sh > at49.sh`)

Each mutant changes ONE clause of the round-39 block (lines 1903-1914 at 49cc53c); the selftest is then run on
each (`bash OUTDIR/mN.sh --selftest`) and the failing case names are the evidence that the corresponding
selftest case is not redundant. m5 is the proposed minimal diff (mt counter removed): it must stay green.
"""
import pathlib
import sys

src = pathlib.Path(sys.argv[1]).read_text()
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

start = src.index('  if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then')
end = src.index('  local state=HEALTHY', start)
block = src[start:end]
assert block.count('mounts:') == 2, 'block shape changed; re-derive the mutants'

(out / 'm1.sh').write_text(src[:start] + src[end:])                       # whole block removed
b = block.replace("detail+='mounts:btrfs-without-sysfs,'", "detail+='mounts:XX,'")
assert b != block
(out / 'm2c.sh').write_text(src[:start] + b + src[end:])                   # hidden token renamed (code only)
b = block.replace("detail+='mounts:unreadable,'", "detail+='mounts:YY,'")
assert b != block
(out / 'm3c.sh').write_text(src[:start] + b + src[end:])                   # unreadable token renamed (code only)
m4 = src.replace('if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then',
                 'if [ "$blocked" -eq 0 ]; then')
assert m4 != src
(out / 'm4.sh').write_text(m4)                                            # fsn==0 guard dropped
m5 = src.replace('''    local mtab mt=0 _src _mp fst _rest
    if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then
      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
      done <<< "$mtab"
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
    else''', '''    local mtab _src _mp fst _rest
    if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then
      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; break; fi
      done <<< "$mtab"
    else''')
assert m5 != src
(out / 'm5.sh').write_text(m5)                                            # proposed minimal diff
print('wrote m1.sh m2c.sh m3c.sh m4.sh m5.sh to', out)
