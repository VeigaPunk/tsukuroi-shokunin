#!/usr/bin/env python3
"""Round-46 C1 pre-data battery: score each census variant with the frozen counter before any seat.
Each variant is committed in its own scratch clone (git clone --shared of the lane, origin removed, toplevel
checked, fixture identity) on top of BASE, then `tools/score-census-identity-r46.py --lane <clone> --revision HEAD`
runs from the LANE working copy (the counter under freeze). Expected: K0 (do-nothing: the base bytes) and every
K1..K9 control FAIL; K8 (the candidate) PASS.
Usage: python3 run_controls_c1.py <scratch dir> [variant ...]   Writes C1-<variant>.jsonl here and
battery-summary-c1.jsonl (one line per variant, appended)."""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '2042117cfb724170772f4c128cc2ddba0b61d817'
COUNTER = os.path.join(LANE, 'tools/score-census-identity-r46.py')
EXPECT = {'K0-donothing': 'FAIL', 'K1-constant': 'FAIL', 'K2-pathhash': 'FAIL', 'K3-nocases': 'FAIL',
          'K5-stderr': 'FAIL', 'K6-grepc': 'FAIL', 'K7-twolines': 'FAIL', 'K8-candidate': 'PASS',
          'K9-noflagcheck': 'FAIL'}
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull}


def g(d, *args):
    subprocess.run(['git', '-C', d, *args], check=True, capture_output=True, env={**ENV, 'HOME': d})


def one(scratch, variant):
    d = os.path.join(scratch, variant, 'clone')
    shutil.rmtree(os.path.join(scratch, variant), ignore_errors=True)
    os.makedirs(os.path.dirname(d))
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', LANE, d], check=True, env={**ENV, 'HOME': d})
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    g(d, 'remote', 'remove', 'origin')
    g(d, 'checkout', '-q', '--detach', BASE)
    cen = os.path.join(d, 'tools/tsukuroi-census.sh')
    if variant != 'K0-donothing':
        name = 'candidate' if variant == 'K8-candidate' else variant
        with open(cen, encoding='utf-8') as fh:
            base = fh.read()
        subprocess.run([sys.executable, os.path.join(HERE, 'make_c1_variant.py'), name, cen, cen], check=True)
        g(d, '-c', 'user.name=r46-control', '-c', 'user.email=r46-control@fixture.invalid', 'commit', '-q', '-am',
          f'r46 C1 control {variant}')
    p = subprocess.run([sys.executable, COUNTER, '--lane', d, '--revision', 'HEAD',
                        '--scratch', os.path.join(scratch, variant, 's')],
                       capture_output=True, text=True, env={**ENV, 'HOME': os.path.join(scratch, variant),
                                                            'TMPDIR': os.path.join(scratch, variant)})
    out = p.stdout.strip()
    with open(os.path.join(HERE, f'C1-{variant}.jsonl'), 'w') as fh:
        fh.write(out + '\n')
    try:
        r = json.loads(out)
    except ValueError:
        r = {'verdict': 'ERROR', 'stderr': p.stderr[-500:]}
    keys = ('identity_ok', 'tracks_ok', 'symlink_ok', 'unverifiable_ok', 'cli_ok', 'nowrite_ok', 'selftest_pass',
            'selftest_r46')
    row = {'control': variant, 'expect': EXPECT[variant], 'verdict': r.get('verdict'), 'exit_code': p.returncode,
           'as_expected': r.get('verdict') == EXPECT[variant], **{k: r.get(k) for k in keys},
           'census_sha256': r.get('census_sha256')}
    shutil.rmtree(os.path.join(scratch, variant), ignore_errors=True)
    return row


def main():
    scratch = os.path.abspath(sys.argv[1])
    variants = sys.argv[2:] or list(EXPECT)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        rows = list(ex.map(lambda v: one(scratch, v), variants))
    with open(os.path.join(HERE, 'battery-summary-c1.jsonl'), 'a') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + '\n')
            print(json.dumps(r, sort_keys=True))
    return 0 if all(r['as_expected'] for r in rows) else 1


if __name__ == '__main__':
    sys.exit(main())
