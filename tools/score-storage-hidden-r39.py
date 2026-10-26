#!/usr/bin/env python3
"""Round-39 C1 counter (operability): does the census STORAGE arm at <REV> refuse a false all-clear when
btrfs is mounted but its sysfs root is hidden, and does it still read production-path views?

Frozen before any seat scored (SCORECARD.md "Round 39 — declaration"). Routed defects it answers:
R38-ABSENT-ROOT (round-38 closure §6.2: an absent /sys/fs/btrfs read HEALTHY 0/0/0 while btrfs was mounted)
and R38-Q82-LEAK (§6.1: the round-38 Q82 views were host directories bind-mounted into the child, so an arm
could read the view through a leaked host path). Here every view is a tmpfs mounted INSIDE the child's
unprivileged user+mount namespace (`unshare -rm`) and filled from data the child reads on stdin, so no host
path, no bind source and no argv carries the view; the census then runs with stdin at /dev/null.

Legs (census bytes from `git show <REV>:tools/tsukuroi-census.sh`; child env PATH=/usr/bin:/bin LC_ALL=C,
private HOME and TMPDIR):

  H1 hidden-empty   ns: tmpfs over /sys/fs/btrfs (empty root), no TSUKUROI_* override
  H2 hidden-absent  ns: tmpfs over /sys/fs (no btrfs directory), no override
     expected line, both: STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0
                          detail=mounts:btrfs-without-sysfs
     (/proc/self/mounts inside the child still lists the host's btrfs mounts)
  V0..V2 views      ns: tmpfs over /sys/fs/btrfs filled with a random tree (modes zero, nonzero, any);
     expected (state, filesystems, devices, nonzero) from this counter's own model, and no `mounts:` token
  F1..F5 fixtures   TSUKUROI_BTRFS_SYSFS + TSUKUROI_PROC_MOUNTS overrides (exact expected lines below)
  L  live           no namespace, no override; expected from this counter's own read of /sys/fs/btrfs,
     and no `mounts:` token

Predicate (same sentence in the declaration, here and in the receipt):

    hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1
    and six_planes_all == 1                                                      -> PASS, exit 0

six_planes_all: every run printed exactly six PLANE lines, one STORAGE line and one TSUKUROI_CENSUS line.
Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, unshare unavailable). Read-only: the tmpfs
mounts exist only inside the child namespace. Scratch: --scratch DIR (default mkdtemp under $TMPDIR);
removed on exit.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _revision  # noqa: E402

COUNTER_ID = 'score-storage-hidden-r39'
CENSUS = 'tools/tsukuroi-census.sh'
PROD = '/sys/fs/btrfs'
KEYS = ('write_errs', 'read_errs', 'flush_errs', 'corruption_errs', 'generation_errs')
CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
LINE_RE = re.compile(r'^STORAGE btrfs-device-stats state=(HEALTHY|DEGRADED|BLOCKED) filesystems=(\d+) '
                     r'devices=(\d+) nonzero=(\d+)(?: detail=(\S+))?$')
HIDDEN_LINE = ('STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 '
               'detail=mounts:btrfs-without-sysfs')
FSID = '1d02a454-c549-4a35-b567-89d60902af8e'
ZERO = ''.join('%s 0\n' % k for k in KEYS)
M_BTRFS = '/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0\nproc /proc proc rw 0 0\n'
M_NONE = 'proc /proc proc rw 0 0\n/dev/nvme0n1p2 / ext4 rw,relatime 0 0\n'
# name: (sysfs tree spec or None for an absent root, mounts text or None for an unreadable mounts file,
#        exact expected STORAGE line)
FIXTURES = {
    'F1-absent-root-no-btrfs-mounted': (None, M_NONE,
                                        'STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0'),
    'F2-absent-root-btrfs-mounted': (None, M_BTRFS, HIDDEN_LINE),
    'F3-absent-root-mounts-unreadable': (None, None,
                                         'STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 '
                                         'nonzero=0 detail=mounts:unreadable'),
    'F4-populated-root-no-btrfs-mounted': ([(f'{FSID}/devinfo/1/error_stats', ZERO)], M_NONE,
                                           'STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'),
    'F5-empty-root-btrfs-mounted': ([('features', None)], M_BTRFS, HIDDEN_LINE),
}
VIEW_MODES = ('zero', 'nonzero', 'any')
# runs inside the child after the tmpfs is mounted: reads the tree as JSON on stdin, writes it under PROD
BUILDER = ('import json,os,sys\n'
           'spec=json.load(sys.stdin)\n'
           'for rel,content in spec:\n'
           '    p=os.path.join("/sys/fs/btrfs",rel)\n'
           '    if content is None:\n'
           '        os.makedirs(p,exist_ok=True); continue\n'
           '    os.makedirs(os.path.dirname(p),exist_ok=True)\n'
           '    open(p,"w").write(content)\n')


def draw_view(rng: random.Random, mode: str):
    spec = [('features', None)]
    for name in ('mixed_backref', 'big_metadata', 'extended_iref', 'skinny_metadata', 'no_holes'):
        spec.append((f'features/{name}', '0\n'))
    devs_first = True
    fss = []
    for _ in range(rng.randint(1, 3)):
        fsid = '%08x-%04x-4%03x-%x%03x-%012x' % (rng.getrandbits(32), rng.getrandbits(16), rng.getrandbits(12),
                                                 8 + rng.getrandbits(2), rng.getrandbits(12), rng.getrandbits(48))
        fss.append(fsid)
        for devid in rng.sample(range(1, 9), rng.randint(1, 3)):
            vals = {k: (0 if mode == 'zero' or rng.random() < 0.6 else rng.randint(1, 99999)) for k in KEYS}
            if mode == 'nonzero' and devs_first:
                vals[KEYS[rng.randrange(5)]] = rng.randint(1, 99999)
            devs_first = False
            spec.append((f'{fsid}/devinfo/{devid}/error_stats', ''.join('%s %d\n' % (k, vals[k]) for k in KEYS)))
    return spec


def model_from_spec(spec):
    """Expected (state, filesystems, devices, nonzero) of a well-formed view tree."""
    fss, devs, nz = set(), 0, 0
    for rel, content in spec:
        parts = rel.split('/')
        if len(parts) == 4 and UUID_RE.match(parts[0]) and parts[1] == 'devinfo' and parts[3] == 'error_stats':
            fss.add(parts[0])
            devs += 1
            nz += sum(1 for line in content.splitlines() if int(line.split()[1]) > 0)
    return ('DEGRADED' if nz else 'HEALTHY', len(fss), devs, nz)


def model_live(root: str):
    """Own reading of the production root (well-formed kernel files assumed; anything else is BLOCKED)."""
    if not os.path.isdir(root):
        return None
    fss, devs, nz, blocked = 0, 0, 0, False
    for name in sorted(os.listdir(root)):
        if not UUID_RE.match(name):
            continue
        fss += 1
        dv = os.path.join(root, name, 'devinfo')
        ids = sorted(os.listdir(dv)) if os.path.isdir(dv) else []
        if not ids:
            blocked = True
        for d in ids:
            devs += 1
            try:
                vals = dict(l.split() for l in open(os.path.join(dv, d, 'error_stats')).read().splitlines())
            except (OSError, ValueError):
                blocked = True
                continue
            if set(vals) != set(KEYS):
                blocked = True
                continue
            nz += sum(1 for v in vals.values() if int(v) > 0)
    return ('BLOCKED' if blocked else 'DEGRADED' if nz else 'HEALTHY', fss, devs, nz)


def parse(stdout: str):
    lines = stdout.splitlines()
    st = [l for l in lines if l.startswith('STORAGE ')]
    six = (len([l for l in lines if l.startswith('PLANE ')]) == 6 and len(st) == 1
           and len([l for l in lines if l.startswith('TSUKUROI_CENSUS:')]) == 1)
    return st, six


def fields(line: str):
    m = LINE_RE.match(line)
    if not m:
        return None, None
    return (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))), m.group(5)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument('--revision', required=True)
    ap.add_argument('--branch', default='master')
    ap.add_argument('--scratch', default=None)
    a = ap.parse_args(argv)
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    unshare = shutil.which('unshare', path=CHILD_ENV_BASE['PATH'])
    if unshare is None or shutil.which('bash', path=CHILD_ENV_BASE['PATH']) is None:
        print(json.dumps({'counter': COUNTER_ID, 'error': 'unshare or bash missing', 'exit': 2}))
        return 2
    base = Path(a.scratch) if a.scratch else Path(tempfile.mkdtemp(prefix='tsk-r39-c1-'))
    base.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='run-', dir=str(base)))
    try:
        show = subprocess.run(['git', '-C', a.repo, 'show', f'{b.sha}:{CENSUS}'], env=_revision.clean_env(),
                              capture_output=True, timeout=60)
        if show.returncode != 0:
            raise RuntimeError('census unreadable at revision')
        script = work / 'census.sh'
        script.write_bytes(show.stdout)
        (work / 'home').mkdir()
        (work / 'tmp').mkdir()
        env = dict(CHILD_ENV_BASE, HOME=str(work / 'home'), TMPDIR=str(work / 'tmp'))
        six_all = True

        def ns_run(target: str, spec):
            inner = ('mount -t tmpfs tsk "$1" && python3 -c "$2" && exec bash "$3" </dev/null')
            p = subprocess.run([unshare, '-rm', 'sh', '-c', inner, 'r39', target, BUILDER, str(script)],
                               env=env, input=json.dumps(spec), capture_output=True, text=True, timeout=600)
            return p

        hidden, hidden_matched = [], 0
        for name, target in (('H1-hidden-empty', PROD), ('H2-hidden-absent', '/sys/fs')):
            p = ns_run(target, [])
            st, six = parse(p.stdout)
            six_all = six_all and six
            ok = st == [HIDDEN_LINE] and six
            hidden_matched += int(ok)
            hidden.append({'leg': name, 'expected': HIDDEN_LINE, 'got': st, 'six_planes': six,
                           'census_exit': p.returncode, 'stderr_tail': p.stderr[-300:], 'match': ok})
        if not any(h['got'] for h in hidden):
            raise RuntimeError('namespace legs produced no STORAGE line: ' + hidden[0]['stderr_tail'])

        seed = os.urandom(16).hex()
        rng = random.Random(seed)
        views, views_matched = [], 0
        for i, mode in enumerate(VIEW_MODES):
            spec = draw_view(rng, mode)
            exp = model_from_spec(spec)
            p = ns_run(PROD, spec)
            st, six = parse(p.stdout)
            six_all = six_all and six
            got, detail = fields(st[0]) if len(st) == 1 else (None, None)
            ok = got == exp and six and 'mounts:' not in (detail or '')
            views_matched += int(ok)
            views.append({'view': i, 'mode': mode, 'expected': list(exp), 'got': st, 'six_planes': six,
                          'census_exit': p.returncode, 'match': ok})

        fixtures, fixtures_matched = [], 0
        for name, (tree, mounts, exp_line) in FIXTURES.items():
            fx = work / 'fx' / name
            fx.mkdir(parents=True)
            root = fx / 'sys-fs-btrfs'
            if tree is not None:
                root.mkdir()
                for rel, content in tree:
                    q = root / rel
                    if content is None:
                        q.mkdir(parents=True, exist_ok=True)
                    else:
                        q.parent.mkdir(parents=True, exist_ok=True)
                        q.write_text(content)
            mf = fx / 'mounts'
            if mounts is not None:
                mf.write_text(mounts)
            fenv = dict(env, TSUKUROI_BTRFS_SYSFS=str(root), TSUKUROI_PROC_MOUNTS=str(mf))
            p = subprocess.run(['bash', str(script)], env=fenv, stdin=subprocess.DEVNULL, capture_output=True,
                               text=True, timeout=600)
            st, six = parse(p.stdout)
            six_all = six_all and six
            ok = st == [exp_line] and six
            fixtures_matched += int(ok)
            fixtures.append({'fixture': name, 'expected': exp_line, 'got': st, 'six_planes': six,
                             'census_exit': p.returncode, 'match': ok})

        exp = model_live(PROD)
        p = subprocess.run(['bash', str(script)], env=env, stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, timeout=600)
        st, six = parse(p.stdout)
        six_all = six_all and six
        got, detail = fields(st[0]) if len(st) == 1 else (None, None)
        live_match = int(exp is not None and got == exp and six and 'mounts:' not in (detail or ''))
        live = {'expected': list(exp) if exp else None, 'got': st, 'six_planes': six,
                'census_exit': p.returncode, 'match': bool(live_match)}

        verdict = (hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1
                   and six_all)
        rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip, 'seed': seed,
               'predicate': 'hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and '
                            'live_match == 1 and six_planes_all == 1',
               'hidden_matched': hidden_matched, 'views_matched': views_matched,
               'fixtures_matched': fixtures_matched, 'live_match': live_match, 'six_planes_all': int(six_all),
               'result': 'PASS' if verdict else 'FAIL', 'exit': 0 if verdict else 1,
               'hidden': hidden, 'views': views, 'fixtures': fixtures, 'live': live}
        print(json.dumps(rec, indent=1))
        return rec['exit']
    except (RuntimeError, OSError, subprocess.SubprocessError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'revision': b.sha, 'error': str(e), 'exit': 2}))
        return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)
        if not a.scratch:
            shutil.rmtree(base, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
