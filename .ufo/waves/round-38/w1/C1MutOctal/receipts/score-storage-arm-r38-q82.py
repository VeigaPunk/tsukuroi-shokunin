#!/usr/bin/env python3
"""Round-38 C1 supplementary counter (QUALITY 82, R32-FIXTURE-GATEABLE): production-path views.

Added by the pre-seat amendment (SCORECARD.md "Round 38 — pre-seat amendment"), after the author's
own C1 after-receipt at 52ffd65 and before any wave seat scored. It only adds a kill condition to C1;
it can never turn a failing C1 into a pass. The frozen v1 counter (tools/score-storage-arm-r38.py)
drives the census through TSUKUROI_BTRFS_SYSFS fixtures, which code could detect; its live leg has a
constant answer on this host (HEALTHY 1/1/0), which code could cache. This counter therefore runs the
census at <REV> WITHOUT any TSUKUROI_* override, inside an unprivileged user+mount namespace
(`unshare -rm`) in which a fresh tree is bind-mounted over the production path /sys/fs/btrfs. Each of
VIEWS runs gets a tree drawn from os.urandom (1-3 filesystems, 1-3 devices each, every counter 0 or a
random 1-99999 value, one view forced all-zero and one forced nonzero), so neither the path nor a
cached answer distinguishes a view from production use. Expected fields are computed by the frozen
v1 model (`expected_from_sysfs`, loaded from the freeze commit's bytes, sha256 pinned below).

Predicate (same sentence in the amendment, here and in the receipt):

    ns_views_matched == VIEWS and ns_available == 1  -> PASS, exit 0

Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, unshare unavailable, v1 model digest mismatch).
Scratch: --scratch DIR (default mkdtemp under $TMPDIR); removed on exit. No host write: the bind
mount exists only inside the child namespace and disappears with it.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _revision  # noqa: E402

COUNTER_ID = 'score-storage-arm-r38-q82'
CENSUS = 'tools/tsukuroi-census.sh'
V1 = 'tools/score-storage-arm-r38.py'
V1_FREEZE = '7cbaeb6317cb9f7323d2619eec02db4e4da29449'
V1_SHA256 = 'e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218'
PROD = '/sys/fs/btrfs'
VIEWS = 3
KEYS = ('write_errs', 'read_errs', 'flush_errs', 'corruption_errs', 'generation_errs')
CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], env=_revision.clean_env(), capture_output=True, timeout=60)


def load_v1(repo, work: Path):
    p = git(repo, 'show', f'{V1_FREEZE}:{V1}')
    if p.returncode != 0 or hashlib.sha256(p.stdout).hexdigest() != V1_SHA256:
        raise RuntimeError('v1 model missing or digest mismatch')
    f = work / 'v1.py'
    f.write_bytes(p.stdout)
    spec = importlib.util.spec_from_file_location('v1', f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def draw_tree(root: Path, rng: random.Random, mode: str):
    root.mkdir(parents=True)
    (root / 'features').mkdir()
    first = True
    for _ in range(rng.randint(1, 3)):
        fsid = '%08x-%04x-%04x-%04x-%012x' % (rng.getrandbits(32), rng.getrandbits(16), rng.getrandbits(16),
                                              rng.getrandbits(16), rng.getrandbits(48))
        for devid in rng.sample(range(1, 9), rng.randint(1, 3)):
            d = root / fsid / 'devinfo' / str(devid)
            d.mkdir(parents=True)
            vals = {k: (0 if mode == 'zero' or rng.random() < 0.6 else rng.randint(1, 99999)) for k in KEYS}
            if mode == 'nonzero' and first:
                vals[KEYS[rng.randrange(5)]] = rng.randint(1, 99999)
            first = False
            (d / 'error_stats').write_text(''.join('%s %d\n' % (k, vals[k]) for k in KEYS))


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
    base = Path(a.scratch) if a.scratch else Path(tempfile.mkdtemp(prefix='tsk-r38-q82-'))
    base.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='run-', dir=str(base)))
    try:
        v1 = load_v1(a.repo, work)
        show = git(a.repo, 'show', f'{b.sha}:{CENSUS}')
        if show.returncode != 0 or unshare is None:
            raise RuntimeError('census unreadable at revision or unshare missing')
        script = work / 'census.sh'
        script.write_bytes(show.stdout)
        (work / 'home').mkdir()
        (work / 'tmp').mkdir()
        seed = os.urandom(16).hex()
        rng = random.Random(seed)
        modes = ['zero', 'nonzero'] + ['any'] * (VIEWS - 2)
        views, matched, available = [], 0, 1
        for i, mode in enumerate(modes):
            tree = work / f'view{i}'
            draw_tree(tree, rng, mode)
            exp = v1.expected_from_sysfs(str(tree))
            env = dict(CHILD_ENV_BASE, HOME=str(work / 'home'), TMPDIR=str(work / 'tmp'))
            inner = 'mount --bind "$1" ' + PROD + ' && exec bash "$2"'
            p = subprocess.run([unshare, '-rm', 'sh', '-c', inner, 'q82', str(tree), str(script)], env=env,
                               capture_output=True, text=True, timeout=300)
            got, lines, six = v1.parse(p.stdout)
            if not any(l.startswith('TSUKUROI_CENSUS:') for l in p.stdout.splitlines()):
                available = 0
            ok = got == exp and six
            matched += 1 if ok else 0
            views.append({'view': i, 'mode': mode, 'expected': list(exp), 'got': list(got) if got else None,
                          'storage_lines': lines, 'six_planes': six, 'census_exit': p.returncode,
                          'stderr_tail': p.stderr[-300:], 'match': ok})
        verdict = matched == VIEWS and available == 1
        rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip, 'seed': seed,
               'predicate': 'ns_views_matched == VIEWS and ns_available == 1',
               'views_expected': VIEWS, 'ns_views_matched': matched, 'ns_available': available,
               'result': 'PASS' if verdict else 'FAIL', 'exit': 0 if verdict else 1, 'views': views}
        print(json.dumps(rec, indent=1))
        return rec['exit']
    except (RuntimeError, OSError, subprocess.SubprocessError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)
        if not a.scratch:
            shutil.rmtree(base, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
