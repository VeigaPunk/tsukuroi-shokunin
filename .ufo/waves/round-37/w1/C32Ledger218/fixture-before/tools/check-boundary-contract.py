#!/usr/bin/env python3
"""Validate six finite lane-policy decisions; never native runtime enforcement."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
DATA = 'corpus/knowledge/seat-boundary-r22.json'
PROSE = 'corpus/knowledge/seat-boundary-r22.md'
EXPECTED = (
    ('NO_EXEC', 'bash/eval/task', 'DENY', 'No execution or delegation in source-only seats', 'S083'),
    ('NO_FETCH', 'URL read/web_search/browser', 'DENY', 'Local source reads never authorize network fetches', 'S083'),
    ('LOCAL_READ', 'read/grep/glob declared local paths', 'ALLOW', 'Only literal bound source paths and approved skill URI', 'S084'),
    ('REPORT_WRITE', 'write exact report path', 'ALLOW', 'No other write; executor draft exception must be explicit', 'S083'),
    ('UNKNOWN', 'unrecognized tool or malformed arguments', 'DENY', 'Fail closed; incomplete metadata is not command absence', 'S083'),
    ('DEAD', 'missing final or provider death', 'UNKNOWN', 'No report is not evidence of no earlier tool calls', 'S083'),
)
LIMIT = 'Prompt policy and post-hoc request classification only; no native preventive enforcement or effects/reading proof.'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def visible(text):
    """Finite Markdown table carrier rules, not a general rendered-prose theorem."""
    lines, fence, comment = [], None, False
    for line in text.split('\n'):
        if fence is not None:
            marker, length = fence
            if re.fullmatch(r' {0,3}' + re.escape(marker) + '{' + str(length) + r',}[ \t]*', line):
                fence = None
            continue
        pieces, cursor = [], 0
        while cursor < len(line):
            if comment:
                end = line.find('-->', cursor)
                if end < 0:
                    break
                cursor, comment = end + 3, False
            else:
                start = line.find('<!--', cursor)
                if start < 0:
                    pieces.append(line[cursor:])
                    break
                pieces.append(line[cursor:start])
                cursor, comment = start + 4, True
        line = ''.join(pieces)
        opener = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if opener and not (opener[1][0] == '`' and '`' in opener[2]):
            fence = (opener[1][0], len(opener[1]))
        elif not line.startswith('    '):
            lines.append(line)
    return lines


def table_cells(text):
    rows = []
    for line in visible(text):
        if line.startswith('    '):
            continue
        line = line.lstrip(' ')
        while line.startswith('>'):
            line = line[1:].lstrip(' ')
        if '|' not in line:
            continue
        cells = line.split('|')
        if line.startswith('|'):
            cells = cells[1:]
        if line.endswith('|'):
            cells = cells[:-1]
        rows.append([cell.strip() for cell in cells])
    return rows


def evaluate(raw, prose, sources, host):
    findings, count = [], 0
    def add(fid, site):
        findings.append({'id': fid, 'site': site})
    if raw is None or prose is None:
        add('BOUNDARY-CONTRACT-MISSING', DATA)
        return 1, {'status': 'FAIL', 'validated_boundary_decisions': 0, 'findings': findings}
    try:
        data = json.loads(raw, object_pairs_hook=unique)
        rows = data['decisions']
        if data.get('schema') != 'tsukuroi-boundary-contract-v1' or not isinstance(rows, list):
            raise ValueError('invalid boundary contract')
        if len(rows) != 6 or len({r['id'] for r in rows}) != 6:
            raise ValueError('exact six unique decisions required')
        text = prose.decode('utf-8') if isinstance(prose, bytes) else prose
        source_text = sources.decode('utf-8') if isinstance(sources, bytes) else sources
        host_data = json.loads(host, object_pairs_hook=unique)
        if (host_data.get('native_per_seat_allowlist') is not False
                or host_data.get('tools_semantics') != 'Eval-defined additive extras; not an allowlist or replacement of native tools.'
                or host_data.get('approved_scope') != 'prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence not preventive enforcement'
                or not isinstance(host_data.get('authority'), str)
                or not host_data['authority'].startswith('Main message to TsukuroiR22: Confirmed: no host-native per-seat allowlist')):
            add('BOUNDARY-HOST-LIMIT', 'S084')
        source_rows = table_cells(source_text)
        for sid, path in [('S083', '.ufo/waves/round-22/snapshot/corpus/lessons/round-21.md'), ('S084', '.ufo/waves/round-22/sources/host-tool-boundary.json')]:
            found = [r for r in source_rows if r and r[0] == sid]
            if len(found) != 1 or len(found[0]) != 11 or found[0][1].rsplit(' — ', 1)[-1] != path or found[0][2:4] != ['own-work', 'A'] or found[0][7] != 'mined' or any('\\' in cell for cell in found[0]):
                add('BOUNDARY-SOURCE', sid)
        cells = table_cells(text)
        by_id = {r['id']: r for r in rows}
        for expected in EXPECTED:
            ident = expected[0]
            row = by_id.get(ident)
            correct = row is not None and tuple(row.get(k) for k in ('id', 'surface', 'decision', 'reason', 'source')) == expected
            matches = [r for r in cells if r and r[0] == ident]
            if not correct or matches != [list(expected)]:
                add('BOUNDARY-DECISION-MISMATCH', ident)
            else:
                count += 1
        if data.get('scope') != LIMIT or 'post-hoc detection, not preventive runtime enforcement' not in '\n'.join(visible(text)):
            add('BOUNDARY-LIMIT-MISSING', 'scope')
        code = 1 if findings else 0
    except (ValueError, TypeError, KeyError, UnicodeError, AttributeError):
        add('BOUNDARY-SCHEMA', DATA)
        code = 2
    if any(f['id'] != 'BOUNDARY-DECISION-MISMATCH' for f in findings):
        count = 0
    return code, {'status': ('PASS', 'FAIL', 'CANNOT_EVALUATE')[code], 'validated_boundary_decisions': count,
                  'total_decisions': 6, 'findings': findings, 'scope': LIMIT}


def selftest():
    # Independent literal fixture: never synthesize inputs from the evaluator's map.
    literal = [
        ('NO_EXEC', 'bash/eval/task', 'DENY', 'No execution or delegation in source-only seats', 'S083'),
        ('NO_FETCH', 'URL read/web_search/browser', 'DENY', 'Local source reads never authorize network fetches', 'S083'),
        ('LOCAL_READ', 'read/grep/glob declared local paths', 'ALLOW', 'Only literal bound source paths and approved skill URI', 'S084'),
        ('REPORT_WRITE', 'write exact report path', 'ALLOW', 'No other write; executor draft exception must be explicit', 'S083'),
        ('UNKNOWN', 'unrecognized tool or malformed arguments', 'DENY', 'Fail closed; incomplete metadata is not command absence', 'S083'),
        ('DEAD', 'missing final or provider death', 'UNKNOWN', 'No report is not evidence of no earlier tool calls', 'S083'),
    ]
    data = {'schema': 'tsukuroi-boundary-contract-v1', 'scope': 'Prompt policy and post-hoc request classification only; no native preventive enforcement or effects/reading proof.',
            'decisions': [dict(zip(('id', 'surface', 'decision', 'reason', 'source'), r)) for r in literal]}
    prose = '\n'.join('| ' + ' | '.join(r) + ' |' for r in literal) + '\npost-hoc detection, not preventive runtime enforcement'
    sources = ('| S083 | lesson — .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry |\n'
               '| S084 | host — .ufo/waves/round-22/sources/host-tool-boundary.json | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry |')
    host = json.dumps({'native_per_seat_allowlist': False, 'tools_semantics': 'Eval-defined additive extras; not an allowlist or replacement of native tools.',
                       'approved_scope': 'prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence not preventive enforcement',
                       'authority': 'Main message to TsukuroiR22: Confirmed: no host-native per-seat allowlist exists in the task dispatch path'})
    cases = [('clean', json.dumps(data), prose, sources, host, 0, None), ('missing', None, prose, sources, host, 1, 'BOUNDARY-CONTRACT-MISSING')]
    for i in range(6):
        mutant = copy.deepcopy(data)
        mutant['decisions'][i]['decision'] = 'FORGED'
        cases.append((f'decision-{i}', json.dumps(mutant), prose, sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'))
    for field in ('reason', 'surface', 'source'):
        mutant = copy.deepcopy(data)
        mutant['decisions'][0][field] = 'FORGED'
        cases.append((field, json.dumps(mutant), prose, sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'))
    duplicate = copy.deepcopy(data)
    duplicate['decisions'][5] = duplicate['decisions'][0]
    cases.extend([
        ('duplicate-id', json.dumps(duplicate), prose, sources, host, 2, 'BOUNDARY-SCHEMA'),
        ('duplicate-key', '{"schema":1,"schema":2}', prose, sources, host, 2, 'BOUNDARY-SCHEMA'),
        ('hidden', json.dumps(data), '<!--\n' + prose + '\n-->', sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'),
        ('fenced', json.dumps(data), '```\n' + prose + '\n```', sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'),
        ('wrong-table', json.dumps(data), prose.replace('| DENY |', '| ALLOW |', 1), sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'),
        ('indented-duplicate', json.dumps(data), prose + '\n | NO_EXEC | wrong | DENY | wrong | S083 |', sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'),
        ('quoted-duplicate', json.dumps(data), prose + '\n> | REPORT_WRITE | wrong | ALLOW | wrong | S083 |', sources, host, 1, 'BOUNDARY-DECISION-MISMATCH'),
        ('hidden-limit', json.dumps(data), prose.replace('post-hoc detection, not preventive runtime enforcement', '<!-- post-hoc detection, not preventive runtime enforcement -->'), sources, host, 1, 'BOUNDARY-LIMIT-MISSING'),
        ('source-no-leading-pipe-duplicate', json.dumps(data), prose, sources + '\nS083 | bogus | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry', host, 1, 'BOUNDARY-SOURCE'),
        ('source-decoy-path', json.dumps(data), prose, sources.replace('lesson — .ufo/', 'lesson — /tmp/decoy/.ufo/'), host, 1, 'BOUNDARY-SOURCE'),
        ('source-wrong-status', json.dumps(data), prose, sources.replace('| mined |', '| rejected |', 1), host, 1, 'BOUNDARY-SOURCE'),
        ('source-wrong-tier', json.dumps(data), prose, sources.replace('| A |', '| C |', 1), host, 1, 'BOUNDARY-SOURCE'),
        ('source-missing', json.dumps(data), prose, '', host, 1, 'BOUNDARY-SOURCE'),
        ('host-overclaim', json.dumps(data), prose, sources, '{"native_per_seat_allowlist":true}', 1, 'BOUNDARY-HOST-LIMIT'),
        ('host-isolated-boolean', json.dumps(data), prose, sources, json.dumps(dict(json.loads(host), native_per_seat_allowlist=True)), 1, 'BOUNDARY-HOST-LIMIT'),
        ('host-scope-forgery', json.dumps(data), prose, sources, json.dumps(dict(json.loads(host), approved_scope='native preventive enforcement')), 1, 'BOUNDARY-HOST-LIMIT'),
        ('limit', json.dumps(data), prose.replace('post-hoc detection, not preventive runtime enforcement', ''), sources, host, 1, 'BOUNDARY-LIMIT-MISSING'),
    ])
    observations = []
    for name, raw, text, src, authority, expected_code, expected_id in cases:
        code, result = evaluate(raw, text, src, authority)
        ids = [f['id'] for f in result['findings']]
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': code == expected_code and (expected_id is None or expected_id in ids)})
    failed = sum(not r['pass'] for r in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(cases), 'failed': failed, 'observations': observations}))
    return int(bool(failed))


def git_read(rev, path):
    proc = subprocess.run(['git', '--no-pager', '-C', str(ROOT), 'show', f'{rev}:{path}'], capture_output=True, env=_revision.clean_env(), timeout=30)
    if proc.returncode == 0:
        return proc.stdout
    check = subprocess.run(['git', '--literal-pathspecs', '-C', str(ROOT), 'ls-tree', '-z', rev, '--', path], capture_output=True, env=_revision.clean_env(), timeout=30)
    if check.returncode == 0 and not check.stdout:
        return None
    raise RuntimeError('committed read unavailable')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--revision')
    group.add_argument('--selftest', action='store_true')
    parser.add_argument('--branch', default='master')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, payload = evaluate(git_read(binding.sha, DATA), git_read(binding.sha, PROSE), git_read(binding.sha, 'corpus/SOURCES.md'), git_read(binding.sha, '.ufo/waves/round-22/sources/host-tool-boundary.json'))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'BOUNDARY-READ', 'site': 'revision'}]}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
