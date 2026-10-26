#!/usr/bin/env python3
"""W1 row R42-C1-CLASS-UNSWEPT — the lint gate over the census bytes.

Fix under test (w1/MistakesSweep.md row 6): "add a lint gate over the census bytes (no
`printf … | (head|grep -q|grep -m1)` outside `run_selftest`)". The rule the round-42 fix follows is
written at tools/tsukuroi-census.sh:692-696 ("never `printf | grep -q` / `| grep -m1` / `| head`
under pipefail on a probe buffer").

Scope of the gate, stated so it can be argued with: printf-fed early readers (`head`, `grep -q`,
`grep -qE`, `grep -m1`) in logical lines (backslash continuations joined), comments skipped, and any
site inside `run_selftest() { … }` excluded — the selftest pipes its own small buffers, and the
round-42 fix itself added a here-string there.

Usage: w1r6_class_gate.py <census.sh>   exit 0 = clean (green), 1 = sites present (red)
"""
import re
import sys

PAT = re.compile(r'\bprintf\b.*\|\s*(head\b|grep\s+-(?:q\b|qE\b|m1\b))')


def selftest_range(lines):
    start = next(i for i, ln in enumerate(lines, 1) if ln.startswith('run_selftest() {'))
    for i in range(start, len(lines)):
        if lines[i] == '}':
            return start, i + 1
    raise SystemExit('no run_selftest end')


def sites(lines):
    lo, hi = selftest_range(lines)
    logical, buf, start = [], '', None
    for i, ln in enumerate(lines, 1):
        if start is None:
            start = i
        if ln.endswith('\\'):
            buf += ln[:-1] + ' '
            continue
        buf += ln
        logical.append((start, buf))
        buf, start = '', None
    out = []
    for s, text in logical:
        if text.lstrip().startswith('#'):
            continue
        if PAT.search(text):
            out.append((s, text.strip(), lo <= s <= hi))
    return out, (lo, hi)


def main():
    path = sys.argv[1]
    lines = open(path).read().split('\n')
    found, (lo, hi) = sites(lines)
    outside = [(s, t) for s, t, internal in found if not internal]
    print(f'census         : {path}')
    print(f'run_selftest   : :{lo}-:{hi} (excluded: the selftest pipes its own small buffers)')
    for s, t in outside:
        print(f'  :{s}  {t[:140]}')
    print(f'SITES OUTSIDE  : {len(outside)} of {len(found)} printf-fed early readers')
    print('GATE           : ' + ('PASS (green)' if not outside else 'FAIL (red)'))
    return 0 if not outside else 1


if __name__ == '__main__':
    sys.exit(main())
