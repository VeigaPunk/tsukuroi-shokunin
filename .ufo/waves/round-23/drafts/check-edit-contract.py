#!/usr/bin/env python3
"""Validate eight finite structured-edit authority decisions against their declared
sources.  The evidence file proves observed structured-target metadata shapes and
recorded adapter steps only; lane policy stays separate (policy=round23-preregister
on every row); there is never native runtime enforcement, opaque-patch
interpretation, effect, or reading proof.

Exits: 0 clean, 1 failed (typed findings), 2 could-not-evaluate (schema/binding).
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
DATA = 'corpus/knowledge/structured-edit-r23.json'
PROSE = 'corpus/knowledge/structured-edit-r23.md'
EVIDENCE = '.ufo/waves/round-23/sources/structured-edit-observations.json'
EVIDENCE_SCHEMA = 'tsukuroi-structured-edit-observations-v1'
EVIDENCE_SCOPE = 'Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof.'
LIMIT = 'Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.'
EXPECTED = (
    ('DECLARED_EDIT', 'ALLOW', 'Exact target is predeclared for edit and for both read and write', 'S086', 'round23-preregister'),
    ('UNDECLARED_EDIT', 'DENY', 'No implicit edit permission from generic report ownership', 'S086', 'round23-preregister'),
    ('READ_ONLY_EDIT', 'DENY', 'Read authority never grants a write', 'S086', 'round23-preregister'),
    ('WRITE_ONLY_EDIT', 'DENY', 'Edit also needs its explicit target read authority', 'S086', 'round23-preregister'),
    ('OPAQUE_PATCH', 'UNKNOWN', 'Missing structured target is not inferred from opaque patch text', 'S086', 'round23-preregister'),
    ('EDIT_TRAVERSAL', 'DENY', 'No dot-segment or alternate spelling expands the target list', 'S086', 'round23-preregister'),
    ('EDIT_EXTERNAL', 'DENY', 'Remote or internal URIs do not become filesystem edit targets', 'S086', 'round23-preregister'),
    ('EXPANSION', 'CHECK_EACH', 'Every recorded adapter read or write remains separately scoped', 'S086', 'round23-preregister'),
)
FIELDS = ('id', 'decision', 'reason', 'evidence', 'policy')


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


def has_controls(value):
    return any(unicodedata.category(char) in ('Cc', 'Cf', 'Cs', 'Zl', 'Zp')
               for char in value)


def _text(value):
    return isinstance(value, str) and bool(value) and not has_controls(value)


def _is_step(step):
    return (isinstance(step, dict)
            and isinstance(step.get('line'), int) and not isinstance(step.get('line'), bool)
            and step['line'] >= 1
            and _text(step.get('tool')) and _text(step.get('path')))


def audit_evidence(evidence_data, add):
    """Shape-only audit of the S086 evidence source: observed metadata shapes and
    recorded adapter steps, with the exact no-enforcement scope.  Never universal
    tool semantics, native enforcement, effects, or reading proof; the lane policy
    lives in the decision rows, not here."""
    if evidence_data.get('schema') != EVIDENCE_SCHEMA:
        add('EDIT-EVIDENCE-SHAPE', 'schema')
        return
    if evidence_data.get('scope') != EVIDENCE_SCOPE:
        add('EDIT-EVIDENCE-SCOPE', 'S086')
    observations = evidence_data.get('observations')
    if not isinstance(observations, list) or not observations:
        add('EDIT-EVIDENCE-SHAPE', 'observations')
        return
    for index, obs in enumerate(observations):
        site = f'observations[{index}]'
        if isinstance(obs, dict) and _text(obs.get('seat')):
            site = obs['seat']
        keys = obs.get('argument_keys') if isinstance(obs, dict) else None
        starts = obs.get('recorded_starts') if isinstance(obs, dict) else None
        if (not isinstance(obs, dict)
                or not _text(obs.get('seat')) or not _text(obs.get('agent'))
                or not isinstance(obs.get('transcript_sha256'), str)
                or not re.fullmatch(r'[0-9a-f]{64}', obs['transcript_sha256'])
                or not isinstance(obs.get('request_line'), int)
                or isinstance(obs.get('request_line'), bool)
                or obs['request_line'] < 1
                or not _text(obs.get('call_id')) or obs.get('tool') != 'edit'
                or not isinstance(keys, list) or not keys
                or any(not _text(key) for key in keys)
                or len(set(keys)) != len(keys)
                or 'path' not in keys
                or not _text(obs.get('path'))
                or obs.get('body_fields') != 'omitted; no report text copied'
                or not isinstance(starts, list) or not starts
                or any(not _is_step(step) for step in starts)):
            add('EDIT-EVIDENCE-SHAPE', site)


def evaluate(raw, prose, sources, evidence):
    findings, count = [], 0
    def add(fid, site):
        findings.append({'id': fid, 'site': site})
    if raw is None or prose is None:
        add('EDIT-CONTRACT-MISSING', DATA)
        return 1, {'status': 'FAIL', 'validated_edit_decisions': 0, 'total_decisions': 8,
                   'findings': findings, 'scope': LIMIT}
    try:
        data = json.loads(raw, object_pairs_hook=unique)
        rows = data['decisions']
        if data.get('schema') != 'tsukuroi-edit-contract-v1' or not isinstance(rows, list):
            raise ValueError('invalid edit contract')
        if len(rows) != 8 or len({r['id'] for r in rows}) != 8:
            raise ValueError('exact eight unique decisions required')
        text = prose.decode('utf-8') if isinstance(prose, bytes) else prose
        source_text = (sources.decode('utf-8') if isinstance(sources, bytes) else sources) or ''
        if evidence is None:
            add('EDIT-EVIDENCE-MISSING', EVIDENCE)
        else:
            evidence_text = evidence if isinstance(evidence, str) else evidence.decode('utf-8')
            audit_evidence(json.loads(evidence_text, object_pairs_hook=unique), add)
        found = [r for r in table_cells(source_text) if r and r[0] == 'S086']
        if (len(found) != 1 or len(found[0]) != 11
                or found[0][1].rsplit(' — ', 1)[-1] != EVIDENCE
                or found[0][2:4] != ['own-work', 'A'] or found[0][7] != 'mined'
                or any('\\' in cell for cell in found[0])):
            add('EDIT-SOURCE', 'S086')
        cells = table_cells(text)
        by_id = {r['id']: r for r in rows}
        for expected in EXPECTED:
            ident = expected[0]
            row = by_id.get(ident)
            correct = row is not None and tuple(row.get(k) for k in FIELDS) == expected
            matches = [r for r in cells if r and r[0] == ident]
            if not correct or matches != [list(expected)]:
                add('EDIT-DECISION-MISMATCH', ident)
            else:
                count += 1
        if data.get('scope') != LIMIT or LIMIT not in '\n'.join(visible(text)):
            add('EDIT-LIMIT-MISSING', 'scope')
        code = 1 if findings else 0
    except (ValueError, TypeError, KeyError, UnicodeError, AttributeError):
        add('EDIT-SCHEMA', DATA)
        code = 2
    if any(f['id'] != 'EDIT-DECISION-MISMATCH' for f in findings):
        count = 0
    return code, {'status': ('PASS', 'FAIL', 'CANNOT_EVALUATE')[code],
                  'validated_edit_decisions': count, 'total_decisions': 8,
                  'findings': findings, 'scope': LIMIT}


def selftest():
    # Independent literal fixture: never synthesize inputs from the evaluator's map.
    limit = 'Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.'
    evidence_scope = 'Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof.'
    literal = [
        ('DECLARED_EDIT', 'ALLOW', 'Exact target is predeclared for edit and for both read and write', 'S086', 'round23-preregister'),
        ('UNDECLARED_EDIT', 'DENY', 'No implicit edit permission from generic report ownership', 'S086', 'round23-preregister'),
        ('READ_ONLY_EDIT', 'DENY', 'Read authority never grants a write', 'S086', 'round23-preregister'),
        ('WRITE_ONLY_EDIT', 'DENY', 'Edit also needs its explicit target read authority', 'S086', 'round23-preregister'),
        ('OPAQUE_PATCH', 'UNKNOWN', 'Missing structured target is not inferred from opaque patch text', 'S086', 'round23-preregister'),
        ('EDIT_TRAVERSAL', 'DENY', 'No dot-segment or alternate spelling expands the target list', 'S086', 'round23-preregister'),
        ('EDIT_EXTERNAL', 'DENY', 'Remote or internal URIs do not become filesystem edit targets', 'S086', 'round23-preregister'),
        ('EXPANSION', 'CHECK_EACH', 'Every recorded adapter read or write remains separately scoped', 'S086', 'round23-preregister'),
    ]
    data = {'schema': 'tsukuroi-edit-contract-v1', 'scope': limit,
            'decisions': [dict(zip(('id', 'decision', 'reason', 'evidence', 'policy'), r)) for r in literal]}
    rows_text = ['| ' + ' | '.join(row) + ' |' for row in literal]
    prose = '\n'.join(rows_text) + '\n' + limit
    sources = ('| S086 | evidence — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry |\n'
               '| S085 | lesson — .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md | own-work | A | scope | anchor | teaches | mined | 2026-10-20 | on-release | entry |')
    evidence_data = {
        'schema': 'tsukuroi-structured-edit-observations-v1', 'accessed': '2026-10-21',
        'observations': [
            {'seat': 'Alpha', 'agent': 'R.Alpha-1', 'transcript_sha256': 'a' * 64,
             'request_line': 15, 'call_id': 'toolu_fixture_alpha', 'tool': 'edit',
             'argument_keys': ['path', 'stream_content'],
             'path': '/repo/.ufo/waves/round-22/build/Alpha.md',
             'body_fields': 'omitted; no report text copied',
             'recorded_starts': [
                 {'line': 12, 'tool': 'read', 'path': '/repo/.ufo/waves/round-22/build/Alpha.md:raw'},
                 {'line': 13, 'tool': 'write', 'path': '/repo/.ufo/waves/round-22/build/Alpha.md'}]},
            {'seat': 'Beta', 'agent': 'R.Beta-2', 'transcript_sha256': '0123456789abcdef' * 4,
             'request_line': 30, 'call_id': 'call_fixture_beta', 'tool': 'edit',
             'argument_keys': ['i', 'new_string', 'old_string', 'path'],
             'path': '/repo/.ufo/waves/round-22/build/Beta.md',
             'body_fields': 'omitted; no report text copied',
             'recorded_starts': [
                 {'line': 31, 'tool': 'edit', 'path': '/repo/.ufo/waves/round-22/build/Beta.md'}]},
        ],
        'scope': evidence_scope,
    }
    evidence = json.dumps(evidence_data)
    cases = [('clean', json.dumps(data), prose, sources, evidence, 0, None),
             ('missing-raw', None, prose, sources, evidence, 1, 'EDIT-CONTRACT-MISSING'),
             ('missing-prose', json.dumps(data), None, sources, evidence, 1, 'EDIT-CONTRACT-MISSING')]
    for i in range(8):
        mutant = copy.deepcopy(data)
        mutant['decisions'][i]['decision'] = 'FORGED'
        cases.append((f'decision-{i}', json.dumps(mutant), prose, sources, evidence, 1, 'EDIT-DECISION-MISMATCH'))
    for name, field, value in (('reason-swap', 'reason', 'FORGED REASON'),
                               ('source-swap', 'evidence', 'S085'),
                               ('policy-swap', 'policy', 'legacy-default')):
        mutant = copy.deepcopy(data)
        mutant['decisions'][0][field] = value
        cases.append((name, json.dumps(mutant), prose, sources, evidence, 1, 'EDIT-DECISION-MISMATCH'))
    duplicate = copy.deepcopy(data)
    duplicate['decisions'][7] = duplicate['decisions'][0]
    extra = copy.deepcopy(data)
    extra['decisions'].append({'id': 'EDIT_NINTH', 'decision': 'ALLOW', 'reason': 'extra row',
                               'evidence': 'S086', 'policy': 'round23-preregister'})
    no_path = copy.deepcopy(evidence_data)
    no_path['observations'][0]['argument_keys'].remove('path')
    body_copy = copy.deepcopy(evidence_data)
    body_copy['observations'][1]['body_fields'] = 'old_string copied verbatim'
    swapped_schema = copy.deepcopy(evidence_data)
    swapped_schema['schema'] = 'tsukuroi-edit-policy-v1'
    cases.extend([
        ('duplicate-id', json.dumps(duplicate), prose, sources, evidence, 2, 'EDIT-SCHEMA'),
        ('extra-row', json.dumps(extra), prose, sources, evidence, 2, 'EDIT-SCHEMA'),
        ('duplicate-json-key', '{"schema":1,"schema":2}', prose, sources, evidence, 2, 'EDIT-SCHEMA'),
        ('malformed-json', '{"schema":', prose, sources, evidence, 2, 'EDIT-SCHEMA'),
        ('hidden', json.dumps(data), '<!--\n' + prose + '\n-->', sources, evidence, 1, 'EDIT-DECISION-MISMATCH'),
        ('fenced', json.dumps(data), '```\n' + prose + '\n```', sources, evidence, 1, 'EDIT-DECISION-MISMATCH'),
        ('wrong-table', json.dumps(data), prose.replace('| DENY |', '| ALLOW |', 1), sources, evidence, 1, 'EDIT-DECISION-MISMATCH'),
        ('missing-row', json.dumps(data), '\n'.join(rows_text[1:]) + '\n' + limit, sources, evidence, 1, 'EDIT-DECISION-MISMATCH'),
        ('indented-duplicate', json.dumps(data), prose + '\n | DECLARED_EDIT | wrong | ALLOW | wrong | S086 |', sources, evidence, 1, 'EDIT-DECISION-MISMATCH'),
        ('quoted-duplicate', json.dumps(data), prose + '\n> | WRITE_ONLY_EDIT | wrong | DENY | wrong | S086 |', sources, evidence, 1, 'EDIT-DECISION-MISMATCH'),
        ('hidden-limit', json.dumps(data), prose.replace(limit, '<!-- ' + limit + ' -->'), sources, evidence, 1, 'EDIT-LIMIT-MISSING'),
        ('json-scope-overclaim', json.dumps({**data, 'scope': 'native preventive enforcement of every edit'}), prose, sources, evidence, 1, 'EDIT-LIMIT-MISSING'),
        ('json-scope-omitted', json.dumps({k: v for k, v in data.items() if k != 'scope'}), prose, sources, evidence, 1, 'EDIT-LIMIT-MISSING'),
        ('evidence-scope-overclaim', json.dumps(data), prose, sources,
         evidence.replace(evidence_scope, 'native permission enforcement proves every decision'), 1, 'EDIT-EVIDENCE-SCOPE'),
        ('evidence-shape-path-key', json.dumps(data), prose, sources, json.dumps(no_path), 1, 'EDIT-EVIDENCE-SHAPE'),
        ('evidence-shape-body-copy', json.dumps(data), prose, sources, json.dumps(body_copy), 1, 'EDIT-EVIDENCE-SHAPE'),
        ('evidence-schema-swap', json.dumps(data), prose, sources, json.dumps(swapped_schema), 1, 'EDIT-EVIDENCE-SHAPE'),
        ('evidence-missing', json.dumps(data), prose, sources, None, 1, 'EDIT-EVIDENCE-MISSING'),
        ('evidence-malformed', json.dumps(data), prose, sources, '{', 2, 'EDIT-SCHEMA'),
        ('source-missing', json.dumps(data), prose, '', evidence, 1, 'EDIT-SOURCE'),
        ('source-decoy-path', json.dumps(data), prose,
         sources.replace('evidence — .ufo/waves/round-23/', 'evidence — /tmp/decoy/.ufo/waves/round-23/'), evidence, 1, 'EDIT-SOURCE'),
        ('source-wrong-status', json.dumps(data), prose, sources.replace('| mined |', '| rejected |', 1), evidence, 1, 'EDIT-SOURCE'),
        ('source-wrong-tier', json.dumps(data), prose, sources.replace('| A |', '| C |', 1), evidence, 1, 'EDIT-SOURCE'),
        ('source-unpiped-duplicate', json.dumps(data), prose,
         sources + '\nS086 | bogus | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry', evidence, 1, 'EDIT-SOURCE'),
    ])
    observations = []
    for name, raw, text, src, authority, expected_code, expected_id in cases:
        code, result = evaluate(raw, text, src, authority)
        ids = [f['id'] for f in result['findings']]
        ok = code == expected_code and (expected_id is None or expected_id in ids)
        if name == 'clean' and result['validated_edit_decisions'] != 8:
            ok = False
        if name == 'wrong-table' and result['validated_edit_decisions'] != 7:
            ok = False
        if name in ('evidence-scope-overclaim', 'evidence-missing', 'source-missing') and result['validated_edit_decisions'] != 0:
            ok = False
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': ok})
    failed = sum(not row['pass'] for row in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(cases),
                      'failed': failed, 'observations': observations}))
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
        code, payload = evaluate(git_read(binding.sha, DATA), git_read(binding.sha, PROSE),
                                 git_read(binding.sha, 'corpus/SOURCES.md'), git_read(binding.sha, EVIDENCE))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'validated_edit_decisions': 0,
                            'total_decisions': 8, 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'validated_edit_decisions': 0,
                            'total_decisions': 8, 'findings': [{'id': 'EDIT-READ', 'site': 'revision'}]}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
