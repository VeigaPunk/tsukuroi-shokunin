#!/usr/bin/env python3
"""Run one lane tool from a committed revision and write a receipt that names that revision
(round 30; the round-28 and round-29 spot-checks routed "Gates at <rev>" rows and selftest
receipts that named no revision).

The tool is executed from a private sandbox clone of the lane (`git clone --no-local`, detached
at TOOL-REV, default REV) in a scratch directory, never from the working copy, with every
inherited GIT_* variable removed; tools that read their own repository (e.g. registry
coverage, memory pressure) therefore see a git repository at TOOL-REV. (Round-30 wave-1
ExecGatesStart showed a `git archive` export made three live gates exit 2.) `{rev}` in the
tool arguments is replaced by the full REV hash and `{lane}` by the lane path.

Receipt layout (JSON lines): a header line {"receipt": 1, "revision", "tool_revision",
"tool", "lane_branches", "tool_sha256", "argv", "started_utc"}, then the tool's stdout lines (decoded as UTF-8
with replacement), then a footer line {"receipt_end": 1, "exit_code", "timed_out",
"stderr_tail", "finished_utc"}. The tool must be a tracked file at the tool revision; it runs
with HOME and XDG_CONFIG_HOME at a private empty directory and global/system git config off.
Receipts are meant to be written into the lane's `.ufo/waves/` evidence, so `--out` may name
a lane path.

Usage: python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE>
       [--lane <repo>] [--timeout <seconds, default 3600>] -- <tools/NAME> [args...]
Exit: the tool's exit code (124 on timeout); 2 when a revision or the tool cannot be read.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile


def env(home=None):
    """Every GIT_* dropped, global and system git config off; with `home`, HOME and
    XDG_CONFIG_HOME point at a private empty directory (round-30 wave-1 RevReceiptRunner M5)."""
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull})
    if home:
        e.update({'HOME': home, 'XDG_CONFIG_HOME': os.path.join(home, '.config')})
    return e


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def resolve(lane, rev):
    p = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', rev + '^{commit}'],
                       capture_output=True, text=True, env=env())
    return p.stdout.strip() if p.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--revision', required=True)
    ap.add_argument('--tool-revision')
    ap.add_argument('--out', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--timeout', type=int, default=3600)
    ap.add_argument('cmd', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == '--' else a.cmd
    if not cmd:
        ap.error('missing tool after --')
    lane = os.path.realpath(a.lane)
    rev = resolve(lane, a.revision)
    trev = resolve(lane, a.tool_revision or a.revision)
    if not rev or not trev:
        print(json.dumps({'error': 'revision unreadable', 'revision': a.revision,
                          'tool_revision': a.tool_revision}))
        return 2
    parent = '/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None
    root = tempfile.mkdtemp(prefix='run-receipt-', dir=parent)
    home = tempfile.mkdtemp(prefix='run-receipt-home-', dir=parent)
    os.makedirs(os.path.join(home, '.config'))
    try:
        subprocess.run(['git', 'clone', '-q', '--no-local', '--no-checkout', lane, root],
                       capture_output=True, env=env(), check=True)
        subprocess.run(['git', '-C', root, '-c', 'advice.detachedHead=false', 'checkout', '-q', trev],
                       capture_output=True, env=env(), check=True)
        rel = os.path.normpath(cmd[0])
        tracked = subprocess.run(['git', '-C', root, 'ls-files', '--error-unmatch', '--', rel],
                                 capture_output=True, env=env())
        if os.path.isabs(cmd[0]) or rel.startswith('..') or tracked.returncode != 0:
            print(json.dumps({'error': 'tool is not a tracked file at the tool revision', 'tool': cmd[0]}))
            return 2
        tool = os.path.join(root, rel)
        with open(tool, 'rb') as fh:
            sha = hashlib.sha256(fh.read()).hexdigest()
        args = [x.replace('{rev}', rev).replace('{lane}', lane) for x in cmd[1:]]
        argv = ([sys.executable, tool] if tool.endswith('.py') else ['bash', tool]) + args
        refs = subprocess.run(['git', '-C', lane, 'for-each-ref', '--format=%(refname) %(objectname)',
                               'refs/heads'], capture_output=True, text=True, env=env()).stdout.split('\n')
        # round-30 wave-2 RevRunnerV2: branch-binding tools read the clone's branches, which mirror
        # the lane's at run time; the header records them so the verdict's branch state is pinned.
        header = {'receipt': 1, 'revision': rev, 'tool_revision': trev, 'tool': rel, 'lane_branches': [r for r in refs if r],
                  'tool_sha256': sha, 'argv': [rel] + args, 'started_utc': now()}
        try:
            p = subprocess.run(argv, cwd=root, capture_output=True, env=env(home), timeout=a.timeout)
            rc, out, err, timed_out = p.returncode, p.stdout, p.stderr, False
        except subprocess.TimeoutExpired as exc:
            rc, out, err, timed_out = 124, exc.stdout or b'', exc.stderr or b'', True
        out = out.decode('utf-8', 'replace')
        footer = {'receipt_end': 1, 'exit_code': rc, 'timed_out': timed_out,
                  'stderr_tail': err.decode('utf-8', 'replace')[-400:], 'finished_utc': now()}
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(header) + '\n')
            fh.write(out if out.endswith('\n') or not out else out + '\n')
            fh.write(json.dumps(footer) + '\n')
        print(json.dumps({'out': a.out, 'revision': rev, 'tool': rel, 'exit_code': rc}))
        return rc
    finally:
        shutil.rmtree(root, ignore_errors=True)
        shutil.rmtree(home, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
