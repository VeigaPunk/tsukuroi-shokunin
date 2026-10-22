#!/usr/bin/env python3
"""Run one lane tool from a committed revision and write a receipt that names that revision
(round 30; the round-28 and round-29 spot-checks routed "Gates at <rev>" rows and selftest
receipts that named no revision).

The tool is executed from a `git archive` export of TOOL-REV (default: REV) in a private scratch
directory, never from the working copy, with every inherited GIT_* variable removed. `{rev}`
in the tool arguments is replaced by the full REV hash and `{lane}` by the lane path.

Receipt layout (JSON lines): a header line {"receipt": 1, "revision", "tool_revision",
"tool", "tool_sha256", "argv", "started_utc"}, then the tool's stdout lines unchanged, then
a footer line {"receipt_end": 1, "exit_code", "stderr_tail", "finished_utc"}.

Usage: python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE>
       [--lane <repo>] -- <tools/NAME> [args...]
Exit: the tool's exit code; 2 when a revision or the tool cannot be read.
"""
import argparse
import datetime
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e['GIT_CONFIG_NOSYSTEM'] = '1'
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
    try:
        tar = subprocess.run(['git', '-C', lane, 'archive', trev], capture_output=True, env=env()).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(root, filter='data')
        tool = os.path.join(root, cmd[0])
        if not os.path.isfile(tool):
            print(json.dumps({'error': 'tool absent at tool revision', 'tool': cmd[0]}))
            return 2
        with open(tool, 'rb') as fh:
            sha = hashlib.sha256(fh.read()).hexdigest()
        args = [x.replace('{rev}', rev).replace('{lane}', lane) for x in cmd[1:]]
        argv = ([sys.executable, tool] if tool.endswith('.py') else ['bash', tool]) + args
        header = {'receipt': 1, 'revision': rev, 'tool_revision': trev, 'tool': cmd[0],
                  'tool_sha256': sha, 'argv': [cmd[0]] + args, 'started_utc': now()}
        p = subprocess.run(argv, cwd=root, capture_output=True, text=True, env=env())
        footer = {'receipt_end': 1, 'exit_code': p.returncode,
                  'stderr_tail': p.stderr[-400:], 'finished_utc': now()}
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(header) + '\n')
            fh.write(p.stdout if p.stdout.endswith('\n') or not p.stdout else p.stdout + '\n')
            fh.write(json.dumps(footer) + '\n')
        print(json.dumps({'out': a.out, 'revision': rev, 'tool': cmd[0], 'exit_code': p.returncode}))
        return p.returncode
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
