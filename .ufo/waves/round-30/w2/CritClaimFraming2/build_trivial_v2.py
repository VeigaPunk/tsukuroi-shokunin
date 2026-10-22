#!/usr/bin/env python3
"""Trivial-baseline fixture for counter v2 of check-btrfs-space-r30.py (CritClaimFraming2, round 30 w2).

Snapshot: the v2 counter's own source bytes (no btrfs documentation). Quotes: its ROWS comments and
docstring. Statements: 12 filler words that contain the row's frozen token (so a future R3' token
rule would also pass). Host capture: a hand-written three-line text file under .ufo/waves/round-30/,
each line naming the v2 CAPTURE_KEYS key and a made-up integer. Registry: the base SOURCES.md with
one new mined row appended inside the registry table.
Usage: build_trivial_v2.py <counter.py> <base-SOURCES.md> <out-dir>
"""
import hashlib, json, os, shutil, sys

counter_path, base_path, root = sys.argv[1:4]
counter = open(counter_path, 'rb').read()
cl = counter.decode().split('\n')


def ln(sub):
    return next(i + 1 for i, l in enumerate(cl) if sub in l)


picks = {
    'D01': (ln("'D01': ('source'"), 'unallocated space vs chunk allocation; ENOSPC with free data space', 'unallocated'),
    'D02': (ln("'D02': ('source'"), "('global reserve', 'global_rsv')),   # what the global block reserve is", 'global reserve'),
    'D03': (ln("'D03': ('source'"), 'balance usage filters return partly used chunks', 'usage'),
    'D04': (ln("'D04': ('source'"), 'metadata DUP profile on a single device', 'dup'),
    'D05': (ln("'D05': ('source'"), 'automatic block-group reclaim (bg_reclaim_threshold)', 'reclaim'),
    'D06': (ln("'D06': ('source'"), 'the per-filesystem allocation sysfs directory', 'allocation'),
    'D07': (ln(' R5 `snapshot` is a regular file'), '`snapshot` is a regular file (v2: not a symlink) under', 'snapshot'),
    'D08': (ln("'D08': ('host'"), 'host metadata used vs total at capture', 'metadata'),
    'D09': (ln("'D09': ('host'"), 'host data / unallocated at capture', 'unallocated'),
    'D10': (ln("'D10': ('host'"), "('global_rsv', 'global reserve')),     # host global reserve size at capture", 'global_rsv'),
}
capture = b'allocation/metadata/bytes_used: 7\nunallocated: 8\nallocation/global_rsv_size: 9\n'
hosts = {'D08': (1, '7'), 'D09': (2, '8'), 'D10': (3, '9')}

if os.path.exists(root):
    shutil.rmtree(root)
snap_rel = '.ufo/waves/round-30/w9/X/counter.txt'
cap_rel = '.ufo/waves/round-30/w9/X/capture.txt'
for rel, data in ((snap_rel, counter), (cap_rel, capture)):
    os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
    open(os.path.join(root, rel), 'wb').write(data)
os.makedirs(os.path.join(root, 'corpus/knowledge'))

base = open(base_path, encoding='utf-8').read().split('\n')
hdr = next(i for i, l in enumerate(base) if l.startswith('| id | source |'))
end = hdr + 1
while end < len(base) and base[end].startswith('|'):
    end += 1
row = ('| S900 | filler — the counter source | docs | A | q | sha256 %s | f | mined | 2026-10-22 | on-release | x |'
       % hashlib.sha256(counter).hexdigest())
open(os.path.join(root, 'corpus/SOURCES.md'), 'w', encoding='utf-8').write('\n'.join(base[:end] + [row] + base[end:]))

rows, skill = [], ['# fixture', '', '| Row | Source |', '|---|---|']
for rid, (line, quote, tok) in picks.items():
    st = 'alpha beta gamma delta epsilon zeta eta theta iota kappa %s mu' % tok
    r = {'id': rid, 'statement': st, 'source': 'S900', 'snapshot': snap_rel, 'line': line, 'quote': quote}
    mark = '| [R30-%s] S900 |' % rid
    if rid in hosts:
        cline, val = hosts[rid]
        r.update(capture=cap_rel, capture_line=cline, value=val)
        r['statement'] = st + ' ' + val
        mark = '| [R30-%s] S900 %s |' % (rid, val)
    rows.append(r)
    skill.append(mark)
json.dump({'rows': rows}, open(os.path.join(root, 'corpus/knowledge/btrfs-space-r30.json'), 'w'), indent=1)
open(os.path.join(root, 'SKILL.md'), 'w').write('\n'.join(skill) + '\n')
print('built', root)
