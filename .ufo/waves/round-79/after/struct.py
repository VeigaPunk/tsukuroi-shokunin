#!/usr/bin/env python3
"""Round-79 structural record: frozen-input identity, record removals, source counts.

Usage: python3 after/struct.py --base <REV> --head <REV>
Writes after/structural.json and after/record-sweep.json. Read-only.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
FROZEN = {
    '.ufo/waves/round-79/before/expected.json':
        '0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21',
    '.ufo/waves/round-79/before/src/systemd.unit.xml':
        'eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6',
}
RECORDS = ['SCORECARD.md', 'LOG.md', 'SKILL.md', 'PROVINCE.md', 'SHONEN.md',
           'corpus/QUALITY.md', 'corpus/SOURCES.md', 'corpus/README.md']
ROW = re.compile(r'^\s{0,3}\|[ \t]*S([0-9]{3,})[ \t]*\|')


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args],
                          capture_output=True, text=True).stdout


def blob(rev, path):
    proc = subprocess.run(['git', '-C', str(ROOT), 'show', f'{rev}:{path}'],
                          capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def registry_counts(text):
    rows = [line for line in text.splitlines() if ROW.match(line)]
    tiers = {tier: 0 for tier in ('A', 'B', 'C')}
    status = {'mined': 0, 'queued': 0, 'rejected': 0}
    for line in rows:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != 11:
            continue
        if cells[3] in tiers:
            tiers[cells[3]] += 1
        if cells[7] in status:
            status[cells[7]] += 1
    return {'rows': len(rows), 'tiers': tiers, 'status': status}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', required=True)
    ap.add_argument('--head', required=True)
    args = ap.parse_args()
    base, head = args.base, args.head
    structural = {'base': base, 'head': head, 'frozen': {}, 'counts': {}, 'diffs': {}}
    for path, want in FROZEN.items():
        raw = blob(head, path)
        got = hashlib.sha256(raw).hexdigest() if raw is not None else None
        structural['frozen'][path] = {'expected': want, 'observed': got, 'ok': got == want}
    for label, rev in (('base', base), ('head', head)):
        text = (blob(rev, 'corpus/SOURCES.md') or b'').decode('utf-8', 'replace')
        structural['counts'][f'registry-{label}'] = registry_counts(text)
        notes = git('ls-tree', '-r', '--name-only', rev, 'corpus/knowledge/')
        structural['counts'][f'notes-{label}'] = len(
            [n for n in notes.splitlines() if n.endswith('.md')])
        tools = git('ls-tree', '-r', '--name-only', rev, 'tools/')
        structural['counts'][f'tools-{label}'] = len(
            [n for n in tools.splitlines() if n.endswith(('.py', '.sh'))])
    changed = git('diff', '--name-status', base, head).splitlines()
    structural['diffs']['changed'] = changed
    structural['diffs']['tools_deleted_or_modified'] = [
        line for line in changed
        if line.startswith(('D\t', 'M\t')) and line.split('\t', 1)[1].startswith('tools/')]
    (HERE / 'structural.json').write_text(json.dumps(structural, indent=1) + '\n')
    sweep = {'rule': 'git diff -U0 <a> <b> over the record files; removed lines listed',
             'pairs': []}
    revs = git('rev-list', '--reverse', f'{base}..{head}').split()
    chain = [base] + revs
    for old, new in zip(chain, chain[1:]):
        removed = []
        for path in RECORDS:
            diff = git('diff', '-U0', old, new, '--', path)
            for line in diff.splitlines():
                if line.startswith('-') and not line.startswith('---'):
                    removed.append({'path': path, 'line': line})
        sweep['pairs'].append({'from': old, 'to': new, 'removed': removed})
    (HERE / 'record-sweep.json').write_text(json.dumps(sweep, indent=1) + '\n')
    print(json.dumps(structural['counts'], indent=1))
    print('frozen_ok', all(v['ok'] for v in structural['frozen'].values()))
    print('tools_touched', structural['diffs']['tools_deleted_or_modified'])
    print('removed_total', sum(len(p['removed']) for p in sweep['pairs']))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
