#!/usr/bin/env python3
"""F-24 anchor cost: fate of every live wave-2 citation of the entry under P1/P2/P3."""
import glob
import re
import sys

S = sys.argv[1]
PAT = re.compile(r'btrfs-scrub-record-r42\.md[:`]+\s*(\d+)(?:[-\u2013](\d+))?')

rows = set()
for f in glob.glob('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/w2/*.md'):
    if f.endswith('/SimplifierLesson.md'):
        continue
    for ln in open(f, errors='replace'):
        for m in PAT.finditer(ln):
            rows.add((f.split('/w2/')[1], int(m.group(1)), int(m.group(2) or m.group(1))))

out = ['# F-24 anchor cost — fate of each live wave-2 citation of',
       '# corpus/knowledge/btrfs-scrub-record-r42.md at pin 78abb8b5', '',
       '$ grep -rn "btrfs-scrub-record-r42\\.md[:`]\\+[0-9]\\+" .ufo/waves/round-42/w2/', '',
       '| seat report | span | S (scope, 9 lines -> 9) | T (triage, 7 lines -> 2) |',
       '|---|---|---|---|']
deleted = shifted = 0
for seat, lo, hi in sorted(rows):
    p1 = 'unchanged' if not (lo <= 15 and hi >= 8) else \
        'span partly rewrapped (:8-15), no line moves; the SH4 name-pattern credit it cites is kept'
    if hi < 144:
        p2 = 'unchanged'
    elif lo <= 150 and hi >= 144:
        p2 = 'TEXT DELETED'
        deleted += 1
    else:
        p2 = f'shift -5 (: {lo} -> {lo - 5})'
        shifted += 1
    out.append(f'| {seat} | :{lo}{"-" + str(hi) if hi != lo else ""} | {p1} | {p2} |')
out += ['', f'=> S (scope) moves no line number: 0 of {len(rows)} citations affected.',
        f'=> T (triage) deletes the text of {deleted} citations and shifts {shifted} more by 5 lines.',
        '   The reports name their pin (e.g. w2/C2CritSC4.md:11 "git show 78abb8b5..."),',
        '   so their citations stay true of 78abb8b5; only tip-following breaks.',
        '=> E (errata) appends after the last line (168) and moves nothing.']
open(f'{S}/anchor-cost.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
