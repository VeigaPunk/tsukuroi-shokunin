#!/usr/bin/env python3
"""R42-BATTERY-SUMMARY-COLLISION — do the two control runners still write one summary path?

Seat MistakesFixFail, round 42 w2, item F-21 (the row appears twice: w1/MistakesSweep.md row 4 and
the integration's own mistake list).

The fix under test is "suffix the summary by battery in the runners". The check reads the write
expression out of each runner (`open(os.path.join(a.out, EXPR), 'w')`), evaluates it for the
battery that runner emits (`last['battery']`), and then performs that write twice in one directory —
the C1 battery then the C2 battery — and counts the files left behind. Red = one file (the C2
summary overwrote the C1 summary); green = two distinct files.

Usage: w1r4_summary_collision.py <c1-runner.py> <c2-runner.py>
"""
import os
import re
import sys

PAT = re.compile(r"open\(os\.path\.join\(a\.out,\s*(.+?)\),\s*'w'\)")
BATTERY = {'c1': 'C1', 'c2': 'C2'}


def expression(path, battery):
    hits = [h for h in PAT.findall(open(path, errors='replace').read()) if 'battery-summary' in h]
    if len(hits) != 1:
        raise SystemExit(f'{path}: expected exactly one battery-summary write, found {len(hits)}')
    ns = {'last': {'battery': battery}}
    return hits[0], eval(hits[0], {'__builtins__': {}}, ns)     # the row's own expression


def main():
    c1, c2 = sys.argv[1], sys.argv[2]
    e1, n1 = expression(c1, BATTERY['c1'])
    e2, n2 = expression(c2, BATTERY['c2'])
    print(f'c1 runner      : {c1}')
    print(f'  expression   : {e1.strip()}   -> {n1}')
    print(f'c2 runner      : {c2}')
    print(f'  expression   : {e2.strip()}   -> {n2}')
    out = os.path.join(os.environ['TMPDIR'], 'summary-out')
    os.makedirs(out, exist_ok=True)
    for name, payload in ((n1, 'C1 summary\n'), (n2, 'C2 summary\n')):
        with open(os.path.join(out, name), 'w') as f:    # exactly the write the runner performs
            f.write(payload)
    files = sorted(os.listdir(out))
    print(f'after both writes in one --out: {files}')
    if len(files) == 1:
        print('CHECKS         : FAIL (red) — one summary path survives; the first battery\'s summary is lost')
        return 1
    print('CHECKS         : PASS (green) — one summary per battery, no overwrite')
    return 0


if __name__ == '__main__':
    sys.exit(main())
