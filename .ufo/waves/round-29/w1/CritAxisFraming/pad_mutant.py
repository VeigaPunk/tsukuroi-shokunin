#!/usr/bin/env python3
"""Build an all-padding C1 mutant in the seat's sandbox clone (never the lane).

Every `now` is content-free filler; O01-O04 cite a fabricated registry row S999 (no snapshot,
no URL, no quote); O05 cites S010 (Arch Linux News archive, unrelated to systemd-oomd);
O06/O07 cite S115 (a source already behind the statement being corrected); O08-O12 cite
`SKILL.md:1` (the skill title line).
"""
import json
import sys

sys.path.insert(0, sys.argv[1] + '/tools')
import importlib.util
spec = importlib.util.spec_from_file_location('c', sys.argv[1] + '/tools/check-owed-statements-r29.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
root = sys.argv[1]

BASIS = {'O01': 'S999', 'O02': 'S999', 'O03': 'S999', 'O04': 'S999', 'O05': 'S010',
         'O06': 'S115', 'O07': 'S115'}


def filler(iid):
    return f'this item is hereby addressed by the marker shown here as required item {iid}'


md_lines, js = {}, {}
for iid, path, row, field, anchor in c.ITEMS:
    basis = BASIS.get(iid, '`SKILL.md:1`')
    if path.endswith('.json'):
        js.setdefault(path, []).append({'id': 'R29-OWED-' + iid, 'row': row, 'field': field,
                                        'withdrawn_text': anchor, 'verdict': 'qualified',
                                        'now': filler(iid), 'basis': [basis]})
    else:
        md_lines.setdefault(path, []).append(
            f'[R29-OWED-{iid}] verdict: rebutted | original: "{anchor}" | now: {filler(iid)} | basis: {basis}')
for path, lines in md_lines.items():
    with open(f'{root}/{path}', 'a') as fh:
        fh.write('\n' + '\n'.join(lines) + '\n')
for path, items in js.items():
    with open(f'{root}/{path}') as fh:
        doc = json.load(fh)
    doc['corrections_r29'] = items
    with open(f'{root}/{path}', 'w') as fh:
        json.dump(doc, fh, indent=1)
        fh.write('\n')
row = '| S999 | x | docs | A | x | x | x | mined | 2026-10-22 | x | corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md |'
with open(f'{root}/corpus/SOURCES.md', 'a') as fh:
    fh.write(row + '\n')
