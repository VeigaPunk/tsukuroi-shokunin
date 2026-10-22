#!/usr/bin/env python3
"""Revision-mode (git) runs of the symlink and path-alias shapes, committed only in the scratch clone.

Usage: gitmode.py <scratch-clone> <outdir>. Every git call drops inherited GIT_* variables.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

CLONE, OUT = sys.argv[1], sys.argv[2]
assert CLONE.startswith('/fast/scratch/hyaku/tsukuroi-r30/CritCounterShapes/'), CLONE
sys.argv = [sys.argv[0], CLONE, OUT]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shapes  # noqa: E402

ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
TIP = '8976ca92ec3c2e6a2aef07b7065a24ff84a1291b'
ID = ['-c', 'user.name=CritCounterShapes', '-c', 'user.email=crit@invalid', '-c', 'commit.gpgsign=false']


def git(*a):
    return subprocess.run(['git', '-C', CLONE, *ID, *a], capture_output=True, text=True, env=ENV, check=True).stdout


def sym_quote(f, rw):
    r = shapes.row(rw, 'D01')
    tgt = 'This fixture sentence explains the unallocated behaviour of the filesystem in detail.'
    f[r['snapshot']] = ('symlink', tgt)
    f['__blob_sha__'] = (r['source'], hashlib.sha256(tgt.encode()).hexdigest())
    r.update(line=1, quote='explains the unallocated behaviour of the filesystem')


def alias(sep):
    def f(files, rw):
        d1, d2 = shapes.row(rw, 'D01'), shapes.row(rw, 'D02')
        text = 'h\nOn ENOSPC the unallocated space and the global reserve are both consulted first.\nt\n'
        shapes.set_snap(files, d1, text, 2, 'On ENOSPC the unallocated space and the global reserve are both consulted')
        files.pop(d2['snapshot'])
        d2.update(source=d1['source'], snapshot=d1['snapshot'].replace('/S900', sep + 'S900'), line=2, quote=d1['quote'])
        shapes.skill_line(files, 'D02', lambda l: [l.replace('S901', 'S900')])
    return f


CASES = [('G0-control', None),
         ('G1-symlink-outside-tree', dict((n, fn) for n, _e, _c, _t, fn in shapes.SH)['A21-snapshot-symlink-outside-tree']),
         ('G2-symlink-to-sibling', dict((n, fn) for n, _e, _c, _t, fn in shapes.SH)['A22-snapshot-symlink-to-sibling-in-evidence']),
         ('G3-dangling-symlink-whose-target-text-is-the-quote', sym_quote),
         ('G4-path-alias-dot', alias('/./')),
         ('G5-path-alias-double-slash', alias('//'))]


def main():
    work = os.path.join(OUT, 'gitwork')
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    bs = None
    for name, fn in CASES:
        git('checkout', '-q', '--detach', '-f', TIP)
        git('clean', '-qfdx', '--', '.ufo/waves/round-30/fixture')
        files, rows = shapes.bat.base_fixture()
        if fn:
            fn(files, rows)
        blob = files.pop('__blob_sha__', None)
        d = os.path.join(work, name)
        shapes.materialize(d, files, rows)
        if blob:
            p = os.path.join(d, 'corpus/SOURCES.md')
            t = open(p).read().split('\n')
            i = next(k for k, l in enumerate(t) if l.startswith('| %s |' % blob[0]))
            t[i] = re.sub(r'sha256 [0-9a-f]{64}', 'sha256 ' + blob[1], t[i])
            open(p, 'w').write('\n'.join(t))
        for root, dirs, fs in os.walk(d):
            for x in fs:
                src = os.path.join(root, x)
                rel = os.path.relpath(src, d)
                dst = os.path.join(CLONE, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.lexists(dst):
                    os.remove(dst)
                if os.path.islink(src):
                    os.symlink(os.readlink(src), dst)
                else:
                    shutil.copyfile(src, dst)
        git('add', '-A', '--', 'SKILL.md', 'corpus/SOURCES.md', shapes.JSON, '.ufo/waves/round-30/fixture')
        git('commit', '-q', '-m', 'crit fixture ' + name)
        rev = git('rev-parse', 'HEAD').strip()
        p = subprocess.run([sys.executable, os.path.join(CLONE, 'tools/check-btrfs-space-r30.py'), '--revision', rev,
                            '--lane', CLONE], capture_output=True, text=True, env=ENV)
        out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith('{')]
        per = {o['id']: o for o in out if 'id' in o}
        summ = out[-1] if out else {}
        tree = shapes.run(d, os.path.join(work, 'bs.md') if bs else _bs(work))
        print(json.dumps({'shape': name, 'git_rev': rev, 'git_verified': summ.get('verified'), 'git_rc': p.returncode,
                          'git_D01': per.get('D01', {}).get('failures'), 'git_D02': per.get('D02', {}).get('failures'),
                          'tree_verified': tree[1].get('verified'),
                          'tree_D01': tree[0].get('D01', {}).get('failures'), 'tree_D02': tree[0].get('D02', {}).get('failures')}))
        bs = True
    git('checkout', '-q', '--detach', '-f', TIP)


def _bs(work):
    p = os.path.join(work, 'bs.md')
    with open(p, 'w') as fh:
        fh.write('# base\n\n' + shapes.bat.HEADER)
    return p


if __name__ == '__main__':
    main()
