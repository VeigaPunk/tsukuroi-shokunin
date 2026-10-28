#!/usr/bin/env python3
"""Round-48 pre-data control battery for C3 (calibration: self-assessment mismatches), scored with the
existing counter `python3 tools/check-self-assessment.py --revision <REV>` (27 fixed checks; frozen: the
counter file is not edited this round). Fixtures are sandbox clones under $HYAKU_SCRATCH.
Usage: python3 battery-c3.py <out.jsonl> <impl-revision>
  K0  base 5fdf062f (do-nothing)                      -> mismatches 1 (K10)   FAIL
  K0b implementation revision, no SCORECARD edit      -> mismatches 3 (K10, K13, K17)  FAIL
  K1  sandbox: only the lesson count fixed (70->71)   -> mismatches 2 (K13, K17)       FAIL
  K2  sandbox: only the case count fixed (164->166)   -> mismatches 1 (K10)            FAIL
  K9  sandbox: both fixed                             -> mismatches 0                  PASS
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '5fdf062f969292736e36513e39f98b1b8de43635'


def git(d, *a):
    return subprocess.run(['git', '-C', d, '-c', 'user.name=ctl', '-c', 'user.email=ctl@sandbox.invalid', *a],
                          capture_output=True, check=True).stdout


def measure(lane, rev):
    p = subprocess.run(['python3', LANE + '/tools/check-self-assessment.py', '--repo', lane, '--revision', rev],
                       capture_output=True)
    d = json.loads(p.stdout.decode())
    return {'mismatches': d['mismatches'], 'checked': d['checked'], 'status': d['status'],
            'failed': [c['id'] for c in d['checks'] if c['status'] != 'match']}


def sandbox(root, name, rev, subs):
    d = os.path.join(root, name)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, check=True).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d)
    git(d, 'checkout', '-q', '--detach', rev)
    p = os.path.join(d, 'SCORECARD.md')
    s = open(p, encoding='utf-8').read()
    for a, b in subs:
        assert a in s, a
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
    git(d, 'add', 'SCORECARD.md')
    git(d, 'commit', '-q', '-m', name)
    return d, git(d, 'rev-parse', 'HEAD').decode().strip()


def main():
    out, impl = sys.argv[1], sys.argv[2]
    root = tempfile.mkdtemp(dir=os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tsukuroi-r48'))
    lessons = ('`corpus/lessons/` 70 files', '`corpus/lessons/` 71 files')
    cases = ('(164 cases, 164 passed, 0 failed)', '(166 cases, 166 passed, 0 failed)')
    try:
        rows = [('K0 do-nothing: base', LANE, BASE, 'FAIL')]
        rows.append(('K0b implementation revision, SCORECARD untouched', LANE, impl, 'FAIL'))
        for name, subs, want, label in (
                ('k1', [lessons], 'FAIL', 'K1 only the lesson count fixed'),
                ('k2', [cases], 'FAIL', 'K2 only the case counts fixed'),
                ('k9', [lessons, cases], 'PASS', 'K9 both fixed (synthetic; the live final is the claim)')):
            try:
                d, rev = sandbox(root, name, impl, subs)
            except AssertionError as e:
                rows.append((f'{label}: substitution anchor missing {e}', None, None, want))
                continue
            rows.append((label, d, rev, want))
        bad = []
        with open(out, 'w') as f:
            for label, lane, rev, want in rows:
                if lane is None:
                    r = {'status': 'ERROR', 'mismatches': None, 'failed': ['anchor']}
                else:
                    r = measure(lane, rev)
                row = {'case': label, 'expected': want, 'status': r['status'], 'mismatches': r['mismatches'],
                       'failed': r['failed'], 'as_expected': r['status'] == want}
                f.write(json.dumps(row) + '\n')
                if not row['as_expected']:
                    bad.append(label)
        print('as_expected', len(rows) - len(bad), 'of', len(rows), 'unexpected:', bad)
        return 1 if bad else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
