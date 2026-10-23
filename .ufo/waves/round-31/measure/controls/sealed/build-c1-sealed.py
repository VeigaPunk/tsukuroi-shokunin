#!/usr/bin/env python3
"""Sealed round-31 C1 controls K1 and K5 (kept out of the lane until after data; its sha256 is
committed with the receipts before data, and the file itself lands after data).

  K1 sourceless-forged  the counter's own bytes are the snapshot (`.ufo/waves/round-31/fixture/
                        S900.txt`), a made-up `mined` row S900 that copies the frozen URL and
                        pin, quotes taken from the counter's question lines, statements equal to
                        K5's (every answer key present), SKILL.md lines with the token.
  K5 reader-ceiling     the real pinned snapshots and registry rows of K3, statements written
                        by the L1 after reading the sources (the positive control).

Usage: python3 build-c1-sealed.py --lane <lane> --toolrev <REV> --snapdir <dir> --work <dir>
       --open-builder <path to build-c1-controls.py>
"""
import argparse
import importlib.util
import json
import os

K5 = {
    'Q01': 'Running btrfs filesystem defragment on files whose extents are shared with snapshots or reflink copies rewrites them unshared, so data space consumption grows; check unallocated space first.',
    'Q02': 'btrfs rescue zero-log clears the log tree and fits only a mount that fails during log replay (open_ctree with replay or log_tree frames); changes since the last commit, up to 30 seconds, are lost.',
    'Q03': 'Never run btrfs check --repair on your own judgement: upstream says to use it only when a developer or experienced user advises it, and to accept that it may not fix the damage.',
    'Q04': 'The autodefrag mount option, off by default, detects small random writes of about 64KiB and queues those files for defragmentation; upstream warns it may not suit large database workloads.',
    'Q05': 'The commit= mount option sets the periodic transaction commit interval, default 30 seconds; raising it lets more unwritten data sit in memory and be lost in a crash, and values above 300 print a warning.',
    'Q06': 'Mounting with nodatacow also turns off data checksums (nodatasum) and compression for new files, so those files lose corruption detection and a crash mid-write can leave a partial update.',
    'Q07': 'Swap a failing disk with btrfs replace start, which copies the data to the target and then drops the source; if the source is gone, pass its devid, and the target must be the same size or larger.',
    'Q08': 'On SSDs prefer a periodic fstrim run or discard=async; synchronous discard (discard or discard=sync) trims right after extents are freed and can hurt performance badly.',
}


def main():
    ap = argparse.ArgumentParser()
    for k in ('--lane', '--toolrev', '--snapdir', '--work', '--open-builder'):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location('ob', a.open_builder)
    ob = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ob)
    repo = os.path.join(a.work, 'c1-controls')
    if not os.path.isdir(repo):
        raise SystemExit('run the open builder first: ' + repo)
    base = ob.git(repo, 'rev-parse', a.toolrev)
    out = {}
    out['K5-reader-ceiling'] = ob.real_layout(repo, base, a.snapdir, {q: (lambda quote, q=q: K5[q]) for q in K5},
                                              'K5 reader-ceiling')
    ob.git(repo, 'checkout', '-q', '--detach', base)
    counter = open(os.path.join(repo, 'tools/check-btrfs-repair-r31.py'), 'rb').read()
    lines = counter.decode().splitlines()
    rows, skill_add = [], []
    for q in sorted(K5):
        tok = ob.TOKEN[q]
        ln = next((i for i, l in enumerate(lines, 1) if f"'{q}': dict(q=" in l), 1)
        text = lines[ln - 1].split("q='", 1)[-1].rstrip("',")
        rows.append({'id': q, 'question': q, 'statement': K5[q], 'source': 'S900',
                     'snapshot': '.ufo/waves/round-31/fixture/S900.txt', 'line': ln, 'quote': text})
        skill_add.append(f'| [R31-{q}] | {tok} forged line | fixture | S900 line {ln} |')
    reg = open(os.path.join(repo, 'corpus/SOURCES.md')).read().rstrip('\n') + '\n'
    pins = ' '.join(f'{ob.URL}{f}' for f in ob.SIDS)
    import re
    pinvals = ' '.join(sorted(set(re.findall(r"pin='([0-9a-f]{64})'", counter.decode()))))
    reg += f'| S900 | forged — {pins} | docs | A | forged | sha256 {pinvals} | forged | mined | 2026-10-22 | on-release | forged |\n'
    skill = open(os.path.join(repo, 'SKILL.md')).read().rstrip('\n') + '\n\n' + '\n'.join(skill_add) + '\n'
    out['K1-sourceless-forged'] = ob.commit(repo, base, {
        '.ufo/waves/round-31/fixture/S900.txt': counter,
        'corpus/knowledge/btrfs-repair-r31.json': json.dumps({'rows': rows}, indent=1) + '\n',
        'corpus/SOURCES.md': reg, 'SKILL.md': skill}, 'K1 sourceless-forged')
    for k, v in out.items():
        print(json.dumps({'control': k, 'commit': v, 'clone': repo}))


if __name__ == '__main__':
    main()
