#!/usr/bin/env python3
"""Produce the round-79 revision-bound claim receipts.

Usage: python3 after/run-measure.py --before <REV> --after <REV>
Writes after/{before,after}-{C1,C2}.txt, after/support-*.txt and after/commands.json
inside /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-79/.
Every receipt binds the revision, the tool path and its sha256, the argv, the
tool's stdout and its exit code. Read-only against the lane.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
TOOLS = {
    'C1': ROOT / 'tools/measure-unit-deps-r79.py',
    'C2': ROOT / 'tools/check-gate-standard-r79.py',
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(argv):
    proc = subprocess.run(argv, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def receipt(path, revision, tool, argv, rc, out):
    lines = [f'revision={revision}',
             f'tool={tool.relative_to(ROOT)} sha256={digest(tool)}',
             'argv=' + ' '.join(argv),
             '--- stdout ---', out.rstrip(), '--- end ---', f'exit={rc}', '']
    path.write_text('\n'.join(lines))
    return {'file': path.name, 'revision': revision, 'tool': str(tool.relative_to(ROOT)),
            'tool_sha256': digest(tool), 'argv': argv, 'exit': rc,
            'summary': [line for line in out.splitlines() if line.strip()][-1:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--before', required=True)
    ap.add_argument('--after', required=True)
    ap.add_argument('--branch', default='master')
    args = ap.parse_args()
    commands = []
    for claim in ('C1', 'C2'):
        tool = TOOLS[claim]
        for label, revision in (('before', args.before), ('after', args.after)):
            argv = [sys.executable, str(tool), '--revision', revision, '--branch', args.branch]
            rc, out = run(argv)
            out_path = HERE / f'{label}-{claim}.txt'
            commands.append(receipt(out_path, revision, tool, argv, rc, out))
            print(out_path.name, 'rc=', rc, commands[-1]['summary'])
        argv = [sys.executable, str(tool), '--selftest']
        rc, out = run(argv)
        out_path = HERE / f'selftest-{claim}.txt'
        commands.append(receipt(out_path, 'worktree', tool, argv, rc, out))
        print(out_path.name, 'rc=', rc, commands[-1]['summary'])
    support = [
        ('registry-coverage', [sys.executable, str(ROOT / 'tools/check-registry-coverage.py'),
                               '--revision', args.after, '--branch', args.branch]),
        ('knowledge-header', [sys.executable, str(ROOT / 'tools/check-knowledge-header.py'),
                              '--revision', args.after]),
        ('knowledge-refs', [sys.executable, str(ROOT / 'tools/check-knowledge-refs-r68.py'),
                            '--revision', args.after, '--branch', args.branch]),
        ('line-endings', [sys.executable, str(ROOT / 'tools/check-line-endings-r64.py'), '--check']),
    ]
    for name, argv in support:
        rc, out = run(argv)
        out_path = HERE / f'support-{name}.txt'
        tool = Path(argv[1])
        commands.append(receipt(out_path, args.after, tool, argv, rc, out))
        print(out_path.name, 'rc=', rc, commands[-1]['summary'])
    (HERE / 'commands.json').write_text(json.dumps(
        {'before': args.before, 'after': args.after, 'commands': commands}, indent=1) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
