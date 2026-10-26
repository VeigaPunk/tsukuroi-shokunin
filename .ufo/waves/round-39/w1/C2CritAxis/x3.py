#!/usr/bin/env python3
"""C2-X3 sourceless control: no order statement, no semantic reading of the sources.
Each TO row cites lines 1-30 of its REQUIRED file and quotes the copyright line that sits
there; the host cells carry only the two numbers the counter itself prints. If the frozen
predicate passes this, it counts citation shape, not the claimed order."""
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
ENTRY = 'corpus/knowledge/pacman-transaction-order-r39.md'
SID = {'TO1': 'S217', 'TO2': 'S214', 'TO3': 'S213', 'TO4': 'S213', 'TO5': 'S208',
       'TO6': 'S213', 'TO7': 'S215', 'TO8': 'S216'}
FILE = {'TO1': 'trans.c', 'TO2': 'sync.c', 'TO3': 'add.c', 'TO4': 'add.c', 'TO5': 'hook.c',
        'TO6': 'add.c', 'TO7': 'remove.c', 'TO8': 'util.c'}
QUOTE = {'hook.c': 'Copyright (c) 2015-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>',
         'default': 'Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>'}
RULE = 'RULE NOT SUPPLIED — this control states no transaction order'


def main(dest):
    entry = subprocess.run(['git', '-C', LANE, 'show', f'2e1c2a4:{ENTRY}'],
                           capture_output=True, check=True).stdout.decode()
    out, hit = [], 0
    for line in entry.splitlines(keepends=True):
        m = re.match(r'^\| (TO\d+) \|', line)
        if not m:
            out.append(line)
            continue
        to = m.group(1)
        parts = line.rstrip('\n').split('|')
        assert len(parts) == 6, (to, len(parts))
        parts[2] = f' {RULE} '
        parts[3] = f' {SID[to]} {FILE[to]}:1-30 “{QUOTE.get(FILE[to], QUOTE["default"])}” '
        parts[4] = ' control host cell, no host evidence: 60 transactions ' if to == 'TO1' else \
                   ' control host cell, no host evidence: 252 of 441 ' if to == 'TO8' else \
                   ' control host cell, no host evidence '
        out.append('|'.join(parts) + '\n')
        hit += 1
    assert hit == 8, hit
    open(dest, 'w').write(''.join(out))


if __name__ == '__main__':
    main(sys.argv[1])
