#!/usr/bin/env python3
"""Trivial-baseline fixtures for check-btrfs-space-r30.py (CritClaimFraming, round 30).

Variant A ("self"): the snapshot is the counter's own source file; each quote is taken from its
ROWS comment; host captures reuse the same file; statements are 12 filler words.
Variant B ("r26"): the snapshot is the round-26 committed ch-sysfs.rst (unregistered supporting
read); only rows whose token appears in it are filled; the rest reuse variant A lines from a
second snapshot.
"""
import hashlib, json, os, shutil, sys

S = os.path.dirname(os.path.abspath(__file__))
FILLER = 'alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu'


def build(root, snaps, picks, hosts):
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, 'corpus/knowledge'))
    base = open(os.path.join(S, 'base-SOURCES.md'), encoding='utf-8').read()
    reg = base.rstrip('\n') + '\n'
    sid_of = {}
    for i, (name, data) in enumerate(snaps.items()):
        rel = '.ufo/waves/round-30/w1/X/' + name
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), 'wb').write(data)
        sid = 'S9%02d' % i
        sid_of[name] = (sid, rel)
        reg += ('| %s | filler — file:%s | docs | A | q | sha256 %s | f | mined | 2026-10-22 | on-release | x |\n'
                % (sid, name, hashlib.sha256(data).hexdigest()))
    open(os.path.join(root, 'corpus/SOURCES.md'), 'w', encoding='utf-8').write(reg)
    rows, skill = [], ['# fixture', '']
    for rid, (name, line, quote) in picks.items():
        sid, rel = sid_of[name]
        r = {'id': rid, 'statement': FILLER, 'source': sid, 'snapshot': rel, 'line': line, 'quote': quote}
        mark = '| [R30-%s] %s |' % (rid, sid)
        if rid in hosts:
            cname, cline, val = hosts[rid]
            r.update(capture=sid_of[cname][1], capture_line=cline, value=val)
            r['statement'] = FILLER + ' ' + val
            mark = '| [R30-%s] %s %s |' % (rid, sid, val)
        rows.append(r)
        skill.append(mark)
    json.dump({'rows': rows}, open(os.path.join(root, 'corpus/knowledge/btrfs-space-r30.json'), 'w'), indent=1)
    open(os.path.join(root, 'SKILL.md'), 'w').write('\n'.join(skill) + '\n')


counter = open(os.path.join(S, 'counter.py'), 'rb').read()
cl = counter.decode().splitlines()


def ln(prefix):
    return next(i + 1 for i, l in enumerate(cl) if l.startswith(prefix))


self_picks = {
    'D01': ('counter.txt', ln("    'D01'"), 'unallocated space vs chunk allocation'),
    'D02': ('counter.txt', next(i + 1 for i, l in enumerate(cl) if '`Global reserve`' in l), '`Global reserve`, `unallocated` and the'),
    'D03': ('counter.txt', ln("    'D03'"), 'balance usage filters return partly used chunks'),
    'D04': ('counter.txt', ln("    'D04'"), 'metadata DUP profile on a single device'),
    'D05': ('counter.txt', ln("    'D05'"), 'automatic block-group reclaim'),
    'D06': ('counter.txt', ln("    'D06'"), 'the per-filesystem allocation sysfs directory'),
    'D07': ('counter.txt', ln("    'D07'"), 'snapshots keep shared extents allocated'),
    'D08': ('counter.txt', ln("    'D08'"), 'host metadata used vs total at capture'),
    'D09': ('counter.txt', ln("    'D09'"), 'host data / unallocated at capture'),
    'D10': ('counter.txt', ln("    'D10'"), 'host global reserve size at capture'),
}
# host value: an integer on an arbitrary line of the same non-sysfs file
r3 = ln(' R3 `statement` has at least 12')
hosts = {'D08': ('counter.txt', r3, '12'), 'D09': ('counter.txt', r3, '12'), 'D10': ('counter.txt', r3, '12')}
build(os.path.join(S, 'fx/self'), {'counter.txt': counter}, self_picks, hosts)

r26 = open(os.path.join(S, 'ch-sysfs-r26.rst'), 'rb').read()
rl = r26.decode().splitlines()


def rln(sub):
    return next(i + 1 for i, l in enumerate(rl) if sub in l)


mixed = dict(self_picks)
mixed.update({
    'D02': ('ch-sysfs.rst', rln('global_rsv_reserved'), 'global_rsv_reserved (RO, since: 3.14)'),
    'D04': ('ch-sysfs.rst', rln('*dedupe* ioctls'), 'The bytes alignment for *clone* and *dedupe* ioctls.'),
    'D05': ('ch-sysfs.rst', rln('Reclaimable space percentage'), "Reclaimable space percentage of block group's size"),
    'D06': ('ch-sysfs.rst', rln('UUID/allocation/ '), 'UUID/allocation/ Space allocation info'),
    'D08': ('ch-sysfs.rst', rln('Show the metadata UUID'), 'Show the metadata UUID of the mounted filesystem.'),
    'D09': ('ch-sysfs.rst', rln('Show the reserved bytes for data'), 'Show the reserved bytes for data.'),
    'D10': ('ch-sysfs.rst', rln('global_rsv_size'), 'global_rsv_size (RO, since: 3.14)'),
})
build(os.path.join(S, 'fx/r26'), {'counter.txt': counter, 'ch-sysfs.rst': r26}, mixed, hosts)
print('built')
