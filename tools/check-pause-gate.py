#!/usr/bin/env python3
"""Count verified premises in the round-24 pause-lift update-safety gate entry.

A premise counts only if its verdict is one of cleared, still-holds, changed or
unverified; it has at least one evidence pointer and every pointer names a line
that exists at the revision and contains its exact substring; and it lists at
least one source id, each a row of corpus/SOURCES.md at the revision whose
`opened` cell contains the gate's `sources_opened` date. All bytes are read
from the bound git revision; nothing on the host is probed.

Scope: a count of evidence links in committed bytes. It does not re-measure the
host, authorize lifting the pacman pause or prove any package state now.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import _revision  # noqa: E402

GATE = 'corpus/knowledge/pause-lift-gate-r24.json'
SOURCES = 'corpus/SOURCES.md'
SCHEMA = 'tsukuroi-pause-gate-v1'
IDS = ('P1', 'P2', 'P3', 'P4', 'P5')
VERDICTS = ('cleared', 'still-holds', 'changed', 'unverified')
ROW = re.compile(r'^\| (S\d{3}) \|')


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def reader(repo, sha):
    def read(path):
        if not isinstance(path, str) or not path or path.startswith('/') or '..' in path.split('/'):
            return None
        proc = subprocess.run(['git', '--no-pager', '-C', str(repo), 'show', f'{sha}:{path}'],
                              capture_output=True, env=_revision.clean_env(), timeout=30)
        return proc.stdout.decode('utf-8', 'replace') if proc.returncode == 0 else None
    return read


def source_dates(text):
    """Map S### -> opened cell from the registry table (11 columns)."""
    out = {}
    for line in (text or '').splitlines():
        match = ROW.match(line)
        if not match:
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 11:
            out.setdefault(match.group(1), cells[8])
    return out


def evaluate(read):
    findings = []
    raw = read(GATE)
    if raw is None:
        return 1, {'premises_total': 0, 'premises_verified': 0, 'premises': [],
                   'findings': [{'id': 'GATE-MISSING', 'site': GATE}]}
    try:
        gate = json.loads(raw, object_pairs_hook=unique)
    except ValueError as exc:
        return 1, {'premises_total': 0, 'premises_verified': 0, 'premises': [],
                   'findings': [{'id': 'GATE-JSON', 'site': str(exc)}]}
    date = gate.get('sources_opened') if isinstance(gate, dict) else None
    if (not isinstance(gate, dict) or gate.get('schema') != SCHEMA or not isinstance(gate.get('premises'), list)
            or not isinstance(date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date)):
        return 1, {'premises_total': 0, 'premises_verified': 0, 'premises': [],
                   'findings': [{'id': 'GATE-SCHEMA', 'site': GATE}]}
    dates = source_dates(read(SOURCES))
    cache, results, seen = {}, [], set()
    for premise in gate['premises']:
        pid = premise.get('id') if isinstance(premise, dict) else None
        problems = []
        if pid not in IDS or pid in seen:
            problems.append('id')
        seen.add(pid)
        if not isinstance(premise, dict):
            results.append({'id': pid, 'verified': False, 'problems': ['shape']})
            continue
        if premise.get('verdict') not in VERDICTS:
            problems.append('verdict')
        evidence = premise.get('evidence')
        if not isinstance(evidence, list) or not evidence:
            problems.append('evidence-empty')
            evidence = []
        for pointer in evidence:
            if not isinstance(pointer, dict) or set(pointer) != {'path', 'line', 'contains'}:
                problems.append('evidence-shape')
                continue
            path, line, needle = pointer['path'], pointer['line'], pointer['contains']
            if path not in cache:
                cache[path] = read(path)
            text = cache[path]
            if text is None:
                problems.append(f'evidence-file:{path}')
                continue
            lines = text.splitlines()
            if type(line) is not int or not 1 <= line <= len(lines):
                problems.append(f'evidence-line:{path}:{line}')
            elif not isinstance(needle, str) or len(needle.strip()) < 3 or needle not in lines[line - 1]:
                problems.append(f'evidence-substring:{path}:{line}')
        sources = premise.get('sources')
        if not isinstance(sources, list) or not sources or len(set(map(str, sources))) != len(sources):
            problems.append('sources-empty')
            sources = []
        for sid in sources:
            if sid not in dates:
                problems.append(f'source-missing:{sid}')
            elif date not in dates[sid]:
                problems.append(f'source-not-opened:{sid}')
        results.append({'id': pid, 'verdict': premise.get('verdict'), 'verified': not problems,
                        'problems': problems})
        findings.extend({'id': 'GATE-PREMISE', 'site': f'{pid}:{p}'} for p in problems)
    verified = sum(r['verified'] for r in results)
    total = len(results)
    if sorted(seen) != list(IDS):
        findings.append({'id': 'GATE-PREMISE-SET', 'site': ','.join(sorted(map(str, seen)))})
    ok = total == len(IDS) and verified == len(IDS) and sorted(seen) == list(IDS)
    return (0 if ok else 1), {'premises_total': total, 'premises_verified': verified,
                              'premises': results, 'findings': findings}


def selftest():
    sources = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
               '|---|---|---|---|---|---|---|---|---|---|---|\n'
               '| S100 | a | docs | A | s | a | t | active | 2026-10-22 | r | u |\n'
               '| S101 | b | docs | A | s | a | t | active | 2026-10-19 | r | u |\n')
    capture = 'alpha line\nbeta pending 3\ngamma\n'
    def gate(**over):
        premises = [{'id': p, 'premise': p, 'verdict': 'changed', 'evidence': [{'path': 'cap.txt', 'line': 2, 'contains': 'pending 3'}],
                     'sources': ['S100'], 'limits': 'x'} for p in IDS]
        body = {'schema': SCHEMA, 'sources_opened': '2026-10-22', 'premises': premises}
        mutate = over.get('mutate')
        if mutate:
            mutate(body)
        return over.get('raw') or json.dumps(body)
    def files(text):
        return {GATE: text, SOURCES: sources, 'cap.txt': capture}.get
    def set_(key, value, index=0):
        def f(body):
            body['premises'][index][key] = value
        return f
    cases = [
        ('pristine', gate(), 0, 5),
        ('missing-premise', gate(mutate=lambda b: b['premises'].pop()), 1, 4),
        ('duplicate-premise', gate(mutate=lambda b: b['premises'].__setitem__(4, dict(b['premises'][0]))), 1, 4),
        ('bad-verdict', gate(mutate=set_('verdict', 'safe')), 1, 4),
        ('line-out-of-range', gate(mutate=set_('evidence', [{'path': 'cap.txt', 'line': 9, 'contains': 'pending 3'}])), 1, 4),
        ('substring-absent', gate(mutate=set_('evidence', [{'path': 'cap.txt', 'line': 1, 'contains': 'pending 3'}])), 1, 4),
        ('trivial-substring', gate(mutate=set_('evidence', [{'path': 'cap.txt', 'line': 2, 'contains': ' '}])), 1, 4),
        ('evidence-file-missing', gate(mutate=set_('evidence', [{'path': 'nope.txt', 'line': 1, 'contains': 'abc'}])), 1, 4),
        ('no-evidence', gate(mutate=set_('evidence', [])), 1, 4),
        ('source-missing', gate(mutate=set_('sources', ['S999'])), 1, 4),
        ('source-other-date', gate(mutate=set_('sources', ['S101'])), 1, 4),
        ('no-sources', gate(mutate=set_('sources', [])), 1, 4),
        ('duplicate-key', '{"schema":"x","schema":"' + SCHEMA + '","sources_opened":"2026-10-22","premises":[]}', 1, 0),
        ('wrong-schema', gate(mutate=lambda b: b.__setitem__('schema', 'v0')), 1, 0),
        ('absolute-evidence-path', gate(mutate=set_('evidence', [{'path': '/etc/passwd', 'line': 1, 'contains': 'root'}])), 1, 4),
    ]
    obs = []
    for name, text, want_code, want_verified in cases:
        code, result = evaluate(files(text))
        obs.append({'case': name, 'exit': code, 'verified': result['premises_verified'],
                    'pass': code == want_code and result['premises_verified'] == want_verified})
    failed = sum(not o['pass'] for o in obs)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(obs), 'failed': failed, 'observations': obs}))
    return int(bool(failed))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--revision')
    mode.add_argument('--selftest', action='store_true')
    parser.add_argument('--branch', default='master')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
    except _revision.RevisionError as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}))
        return 2
    code, result = evaluate(reader(ROOT, binding.sha))
    result.update(revision=binding.sha, branch=binding.branch, status=('PASS', 'FAIL')[code])
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
