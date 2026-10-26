#!/usr/bin/env python3
"""W1 row R42-FREEZE-CENSUS-LIVE-PATH — is a receipt named for a revision actually read at it?

Fix under test (w1/MistakesSweep.md row 5): re-run the registry census on a `git archive <REV>`
export with the start receipt's header, so the receipt named for the freeze commit names the
revision it read. The check is what such a receipt must carry:
  (a) line 1 is a header naming REV;
  (b) the `ok` line's path resolves under the export root;
  (c) the registry at that path is byte-identical to `git show REV:corpus/SOURCES.md`.

Usage: w1r5_freeze_receipt.py --receipt R --root EXPORT --rev REV --lane LANE
  exit 0 green, 1 red, 2 usage
"""
import argparse
import os
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--receipt', required=True)
    ap.add_argument('--root', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--lane', required=True)
    a = ap.parse_args()
    text = open(a.receipt, errors='replace').read()
    lines = text.splitlines()
    problems = []

    head = lines[0] if lines else ''
    if not head.startswith('#'):
        problems.append('(a) line 1 is not a header')
    elif a.rev[:8] not in head:
        problems.append(f'(a) line 1 does not name {a.rev[:8]}: {head[:120]!r}')
    print(f'(a) header     : {head[:140]!r}')

    ok = [ln.split('\t') for ln in lines if '\tok\t' in ln]
    if len(ok) != 1:
        problems.append(f'(b) expected one ok line, found {len(ok)}')
        path = ''
    else:
        path = ok[0][2] if len(ok[0]) > 2 else ''
    root = os.path.realpath(a.root)
    print(f'(b) ok path    : {path}')
    if not path:
        problems.append('(b) no ok path')
    elif os.path.commonpath([root, os.path.realpath(path)]) != root:
        problems.append(f'(b) ok path is outside the export root {root}')
    elif not os.path.isfile(path):
        problems.append('(b) ok path does not exist')

    want = subprocess.run(['git', '-C', a.lane, 'show', f'{a.rev}:corpus/SOURCES.md'],
                          capture_output=True)
    if want.returncode != 0:
        problems.append('(c) cannot read the registry at the revision')
    elif path and os.path.isfile(path):
        have = open(path, 'rb').read()
        same = have == want.stdout
        print(f'(c) registry   : {len(have)} B at the path vs {len(want.stdout)} B at {a.rev[:8]}: '
              f'{"identical" if same else "DIFFERENT"}')
        if not same:
            problems.append('(c) the registry read is not the revision\'s registry')
    print('CHECK          : ' + ('PASS (green)' if not problems else 'FAIL (red)'))
    for p in problems:
        print('  - ' + p)
    return 0 if not problems else 1


if __name__ == '__main__':
    sys.exit(main())
