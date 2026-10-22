#!/usr/bin/env python3
"""Count verified premises in the round-24 pause-lift update-safety gate entry.

A premise counts only if its verdict is one of cleared, still-holds, changed or
unverified; it has at least one evidence pointer and every pointer names a line
that exists at the revision and contains its exact substring; and it lists at
least one source id, each a row of corpus/SOURCES.md at the revision whose
`opened` cell contains the round date 2026-10-22. At least one pointer per
premise must name the pinned round-24 capture, whose sha256 must equal the
gate's `capture_sha256`; no pointer may name the gate files themselves. All
bytes are read from the bound git revision; nothing on the host is probed.

Scope: a count of evidence links in committed bytes. It does not re-measure the
host, authorize lifting the pacman pause or prove any package state now.
"""
from __future__ import annotations
import argparse
import hashlib
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
COUNTED = ('cleared', 'still-holds', 'changed')
BOILERPLATE = ('### ', '$ ', 'exit=')
ROUND_DATE = '2026-10-22'
CAPTURE = '.ufo/waves/round-24/capture/l1-4/capture.txt'
SELF_PATHS = (GATE, 'corpus/knowledge/pause-lift-gate-r24.md')
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
        return proc.stdout.decode('utf-8', 'surrogateescape') if proc.returncode == 0 else None
    return read


def source_rows(text):
    """Map S### -> (opened, status, used-by) from the 11-column registry; count duplicates."""
    out, dups = {}, set()
    for line in (text or '').splitlines():
        match = ROW.match(line)
        if not match:
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 11:
            if match.group(1) in out:
                dups.add(match.group(1))
            out.setdefault(match.group(1), (cells[8], cells[7], cells[10]))
    return out, dups


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
    date = ROUND_DATE
    if not isinstance(gate, dict) or gate.get('schema') != SCHEMA or not isinstance(gate.get('premises'), list):
        return 1, {'premises_total': 0, 'premises_verified': 0, 'premises': [],
                   'findings': [{'id': 'GATE-SCHEMA', 'site': GATE}]}
    capture_text = read(CAPTURE)
    capture_ok = (gate.get('capture') == CAPTURE and capture_text is not None
                  and hashlib.sha256(capture_text.encode('utf-8', 'surrogateescape')).hexdigest() == gate.get('capture_sha256'))
    if not capture_ok:
        findings.append({'id': 'GATE-CAPTURE-PIN', 'site': CAPTURE})
    dates, dup_ids = source_rows(read(SOURCES))
    findings.extend({'id': 'GATE-SOURCE-DUPLICATE', 'site': sid} for sid in sorted(dup_ids))
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
        elif premise.get('verdict') not in COUNTED:
            problems.append('verdict-unverified-not-counted')
        for field in ('premise', 'limits'):
            if not isinstance(premise.get(field), str) or len(premise[field].strip()) < 10:
                problems.append(f'{field}-empty')
        evidence = premise.get('evidence')
        if not isinstance(evidence, list) or not evidence:
            problems.append('evidence-empty')
            evidence = []
        if not capture_ok:
            problems.append('capture-pin')
        anchors = [p for p in evidence if isinstance(p, dict) and p.get('path') == CAPTURE
                   and isinstance(p.get('contains'), str) and not p['contains'].startswith(BOILERPLATE)
                   and capture_text is not None and capture_text.count(p['contains']) == 1]
        if not anchors:
            problems.append('no-unique-capture-pointer')
        for pointer in evidence:
            if not isinstance(pointer, dict) or set(pointer) != {'path', 'line', 'contains'}:
                problems.append('evidence-shape')
                continue
            path, line, needle = pointer['path'], pointer['line'], pointer['contains']
            if path in SELF_PATHS:
                problems.append(f'self-evidence:{path}')
                continue
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
            elif date not in dates[sid][0]:
                problems.append(f'source-not-opened:{sid}')
            elif dates[sid][1] != 'mined' or 'pause-lift-gate-r24' not in dates[sid][2]:
                problems.append(f'source-not-mined-for-gate:{sid}')
            elif sid in dup_ids:
                problems.append(f'source-duplicate:{sid}')
        results.append({'id': pid, 'verdict': premise.get('verdict'), 'sources': sources, 'verified': not problems,
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
               '| S100 | a | docs | A | s | a | t | mined | 2026-10-22 | r | corpus/knowledge/pause-lift-gate-r24.json |\n'
               '| S101 | b | docs | A | s | a | t | mined | 2026-10-19 | r | corpus/knowledge/pause-lift-gate-r24.json |\n'
               '| S102 | c | docs | A | s | a | t | rejected | 2026-10-22 | r | corpus/knowledge/pause-lift-gate-r24.json |\n'
               '| S103 | d | docs | A | s | a | t | mined | 2026-10-22 | r | corpus/knowledge/other.md |\n')
    capture = '### a\nbeta pending 3\ngamma\n'
    capture_sha = hashlib.sha256(capture.encode()).hexdigest()
    def gate(**over):
        premises = [{'id': p, 'premise': p + ' premise text', 'verdict': 'changed', 'evidence': [{'path': CAPTURE, 'line': 2, 'contains': 'pending 3'}],
                     'sources': ['S100'], 'limits': 'limits text here'} for p in IDS]
        body = {'schema': SCHEMA, 'capture': CAPTURE, 'capture_sha256': capture_sha, 'premises': premises}
        mutate = over.get('mutate')
        if mutate:
            mutate(body)
        return over.get('raw') or json.dumps(body)
    def files(text):
        return {GATE: text, SOURCES: sources, CAPTURE: capture, 'other.txt': capture,
                'corpus/knowledge/pause-lift-gate-r24.md': capture}.get
    def set_(key, value, index=0):
        def f(body):
            body['premises'][index][key] = value
        return f
    cases = [
        ('pristine', gate(), 0, 5),
        ('missing-premise', gate(mutate=lambda b: b['premises'].pop()), 1, 4),
        ('duplicate-premise', gate(mutate=lambda b: b['premises'].__setitem__(4, dict(b['premises'][0]))), 1, 4),
        ('bad-verdict', gate(mutate=set_('verdict', 'safe')), 1, 4),
        ('line-out-of-range', gate(mutate=set_('evidence', [{'path': CAPTURE, 'line': 9, 'contains': 'pending 3'}])), 1, 4),
        ('substring-absent', gate(mutate=set_('evidence', [{'path': CAPTURE, 'line': 1, 'contains': 'pending 3'}])), 1, 4),
        ('trivial-substring', gate(mutate=set_('evidence', [{'path': CAPTURE, 'line': 2, 'contains': ' '}])), 1, 4),
        ('no-capture-pointer', gate(mutate=set_('evidence', [{'path': 'other.txt', 'line': 2, 'contains': 'pending 3'}])), 1, 4),
        ('self-evidence', gate(mutate=set_('evidence', [{'path': CAPTURE, 'line': 2, 'contains': 'pending 3'},
                                                        {'path': 'corpus/knowledge/pause-lift-gate-r24.md', 'line': 2, 'contains': 'pending 3'}])), 1, 4),
        ('capture-hash-mismatch', gate(mutate=lambda b: b.__setitem__('capture_sha256', '0' * 64)), 1, 0),
        ('capture-path-other', gate(mutate=lambda b: b.__setitem__('capture', 'other.txt')), 1, 0),
        ('evidence-file-missing', gate(mutate=set_('evidence', [{'path': 'nope.txt', 'line': 1, 'contains': 'abc'}])), 1, 4),
        ('no-evidence', gate(mutate=set_('evidence', [])), 1, 4),
        ('source-missing', gate(mutate=set_('sources', ['S999'])), 1, 4),
        ('source-other-date', gate(mutate=set_('sources', ['S101'])), 1, 4),
        ('no-sources', gate(mutate=set_('sources', [])), 1, 4),
        ('duplicate-key', '{"schema":"x","schema":"' + SCHEMA + '","premises":[]}', 1, 0),
        ('unverified-not-counted', gate(mutate=set_('verdict', 'unverified')), 1, 4),
        ('empty-limits', gate(mutate=set_('limits', '')), 1, 4),
        ('boilerplate-only', gate(mutate=set_('evidence', [{'path': CAPTURE, 'line': 1, 'contains': '### a'}])), 1, 4),
        ('source-rejected', gate(mutate=set_('sources', ['S102'])), 1, 4),
        ('source-other-entry', gate(mutate=set_('sources', ['S103'])), 1, 4),
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
    binder_digest = hashlib.sha256((ROOT / 'tools' / '_revision.py').read_bytes()).hexdigest()
    if binder_digest != '06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf':
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [
            {'id': 'GATE-BINDER-BYTES', 'site': 'tools/_revision.py'}]}))
        return 2
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
    except _revision.RevisionError as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}))
        return 2
    own = reader(ROOT, binding.sha)('tools/check-pause-gate.py')
    if own is None or own.encode('utf-8', 'surrogateescape') != (ROOT / 'tools' / 'check-pause-gate.py').read_bytes():
        site = 'tool absent at this revision' if own is None else 'working-tree checker differs from the revision blob'
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'revision': binding.sha,
                          'findings': [{'id': 'GATE-SELF-BINDING', 'site': site}]}))
        return 2
    code, result = evaluate(reader(ROOT, binding.sha))
    attachment = '.ufo/waves/round-24/capture/l1-4/checkupdates.out'
    attachment_text = reader(ROOT, binding.sha)(attachment)
    attachment_ok = (attachment_text is not None and hashlib.sha256(
        attachment_text.encode('utf-8', 'surrogateescape')).hexdigest()
        == '0a33e3e4a7dae15910e4f914089bb3d7259e16e177da433cfbecc2ca9cfccee7')
    result['checkupdates_attachment_pinned'] = attachment_ok
    if not attachment_ok:
        code = 1
        result['premises_verified'] = 0
        result['findings'].append({'id': 'GATE-ATTACHMENT-PIN', 'site': attachment})
    result.update(revision=binding.sha, branch=binding.branch, status=('PASS', 'FAIL')[code])
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
