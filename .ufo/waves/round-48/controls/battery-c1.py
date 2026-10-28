#!/usr/bin/env python3
"""Round-48 pre-data control battery for C1 (census selftest TMPDIR contract), scored with the frozen
counter tools/score-selftest-tmpdir-r48.py. Mutants are built from the committed fix blob in scratch
(never in the lane). The counters run concurrently, each in its own --work dir under $HYAKU_SCRATCH.
Usage: python3 battery-c1.py <out.jsonl> <fix-revision>
Expected: K0 base -> FAIL; K2 fallback restored -> FAIL; K3 signal fix reverted -> FAIL;
K4 usage-text-only edit of base -> FAIL; K-pass the fix revision -> PASS.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '5fdf062f969292736e36513e39f98b1b8de43635'
COUNTER = LANE + '/tools/score-selftest-tmpdir-r48.py'


def show(rev):
    return subprocess.run(['git', '-C', LANE, 'show', f'{rev}:tools/tsukuroi-census.sh'],
                          capture_output=True, check=True).stdout.decode()


def mutate(fix):
    k2 = fix.replace("  st_base=$ST_BASE_DIR\n",
                     "  st_base=$ST_BASE_DIR\n  case \"${TMPDIR:-}\" in *[!A-Za-z0-9._/+-]*) st_base=/tmp ;; esac\n", 1)
    assert k2 != fix
    k3 = fix.replace("  trap 'exit 130' INT\n  trap 'exit 143' TERM\n", "", 1)
    k3 = k3.replace("rm -rf -- \"${work:-}\" 2>/dev/null || true' EXIT\n",
                    "rm -rf -- \"${work:-}\" 2>/dev/null || true' EXIT INT TERM\n", 1)
    assert k3 != fix and k3.count('EXIT INT TERM') >= 1
    return k2, k3


def run(label, work, extra):
    p = subprocess.run(['python3', COUNTER, '--work', work, *extra], capture_output=True)
    try:
        r = json.loads(p.stdout.decode().strip().splitlines()[-1])
    except Exception as e:
        r = {'verdict': 'ERROR', 'error': str(e)}
    return label, r


def main():
    out, fixrev = sys.argv[1], sys.argv[2]
    root = tempfile.mkdtemp(dir=os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tsukuroi-r48'))
    try:
        fix = show(fixrev)
        base = show(BASE)
        k2, k3 = mutate(fix)
        k4 = base.replace('or /tmp itself when TMPDIR', 'or a private dir when TMPDIR')
        assert k4 != base
        files = {}
        for name, text in (('k2', k2), ('k3', k3), ('k4', k4)):
            path = os.path.join(root, f'{name}.sh')
            with open(path, 'w') as f:
                f.write(text)
            files[name] = path
        jobs = [('K0 do-nothing: base blob', ['--revision', BASE], 'FAIL'),
                ('K2 fix with the /tmp fallback restored', ['--census', files['k2']], 'FAIL'),
                ('K3 fix with the INT/TERM exit traps reverted', ['--census', files['k3']], 'FAIL'),
                ('K4 base with only the usage text edited', ['--census', files['k4']], 'FAIL'),
                ('K-pass: the fix revision', ['--revision', fixrev], 'PASS')]
        with ThreadPoolExecutor(len(jobs)) as ex:
            futs = [ex.submit(run, lab, os.path.join(root, f'w{i}'), extra) for i, (lab, extra, _) in enumerate(jobs)]
            res = [f.result() for f in futs]
        bad = []
        with open(out, 'w') as f:
            for (lab, r), (_, _, want) in zip(res, jobs):
                legs = {k: r.get(k) for k in ('pass_ok', 'loc_ok', 'clean_ok', 'failfast_ok', 'term_ok', 'static_ok')}
                row = {'case': lab, 'expected': want, 'verdict': r.get('verdict'), 'legs': legs,
                       'census_sha256': r.get('census_sha256'), 'as_expected': r.get('verdict') == want}
                f.write(json.dumps(row) + '\n')
                if not row['as_expected']:
                    bad.append(lab)
        print('as_expected', len(jobs) - len(bad), 'of', len(jobs), 'unexpected:', bad)
        return 1 if bad else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
