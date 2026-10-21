#!/usr/bin/env python3
"""Validate eight finite structured-edit authority decisions; never native runtime enforcement."""
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
DATA = 'corpus/knowledge/structured-edit-r23.json'
PROSE = 'corpus/knowledge/structured-edit-r23.md'
EVIDENCE = '.ufo/waves/round-23/sources/structured-edit-observations.json'
PREREGISTER = '.ufo/waves/round-23/preregister.json'
POLICY = 'round23-preregister'
EXPECTED = (
    ('DECLARED_EDIT', 'ALLOW', 'Exact target is predeclared for edit and for both read and write', 'S086', POLICY),
    ('UNDECLARED_EDIT', 'DENY', 'No implicit edit permission from generic report ownership', 'S086', POLICY),
    ('READ_ONLY_EDIT', 'DENY', 'Read authority never grants a write', 'S086', POLICY),
    ('WRITE_ONLY_EDIT', 'DENY', 'Edit also needs its explicit target read authority', 'S086', POLICY),
    ('OPAQUE_PATCH', 'UNKNOWN', 'Missing structured target is not inferred from opaque patch text', 'S086', POLICY),
    ('EDIT_TRAVERSAL', 'DENY', 'No dot-segment or alternate spelling expands the target list', 'S086', POLICY),
    ('EDIT_EXTERNAL', 'DENY', 'Remote or internal URIs do not become filesystem edit targets', 'S086', POLICY),
    ('EXPANSION', 'CHECK_EACH', 'Every recorded adapter read or write remains separately scoped', 'S086', POLICY),
)
LIMIT = 'Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.'
PROSE_LIMIT = 'It is not native permission enforcement'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'
SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})


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


def evidence_ok(evidence):
    """S086 proves only observed metadata shapes and adapter steps; lane policy is separate."""
    data = json.loads(evidence, object_pairs_hook=unique)
    rows = data['observations']
    if data.get('schema') != 'tsukuroi-structured-edit-observations-v1' or not isinstance(rows, list) or not rows:
        return False
    shapes = set()
    for row in rows:
        keys = row['argument_keys']
        if (row.get('tool') != 'edit' or not isinstance(keys, list) or len(keys) != len(set(keys))
                or row.get('body_fields') != 'omitted; no report text copied'
                or not isinstance(row.get('path'), str) or not row['path'].startswith(LANE) or '/../' in row['path']
                or not isinstance(row.get('recorded_starts'), list) or not row['recorded_starts']
                or not re.fullmatch(r'[0-9a-f]{64}', row.get('transcript_sha256', ''))):
            return False
        shapes.add(frozenset(set(keys) - {'i'}))
    return shapes == {frozenset(s) for s in SHAPES}


def evaluate(raw, prose, sources, evidence, preregister):
    findings, count = [], 0
    def add(fid, site):
        findings.append({'id': fid, 'site': site})
    if raw is None or prose is None:
        add('EDIT-CONTRACT-MISSING', DATA)
        return 1, {'status': 'FAIL', 'validated_edit_decisions': 0, 'total_decisions': len(EXPECTED), 'findings': findings, 'scope': LIMIT}
    try:
        data = json.loads(raw, object_pairs_hook=unique)
        rows = data['decisions']
        if set(data) != {'schema', 'decisions', 'source_path', 'scope'} or data.get('schema') != 'tsukuroi-edit-policy-v1' or not isinstance(rows, list):
            raise ValueError('invalid edit policy')
        if len(rows) != len(EXPECTED) or len({r['id'] for r in rows}) != len(EXPECTED):
            raise ValueError('exact eight unique decisions required')
        text = prose.decode('utf-8') if isinstance(prose, bytes) else prose
        source_text = sources.decode('utf-8') if isinstance(sources, bytes) else sources
        if data.get('source_path') != EVIDENCE or evidence is None or not evidence_ok(evidence):
            add('EDIT-EVIDENCE', 'S086')
        pre = json.loads(preregister, object_pairs_hook=unique) if preregister is not None else None
        declared = pre.get('edit_decisions') if isinstance(pre, dict) else None
        if declared != [list(e[:3]) for e in EXPECTED]:
            add('EDIT-POLICY-SOURCE', PREREGISTER)
        found = [r for r in table_cells(source_text or '') if r and r[0] == 'S086']
        if (len(found) != 1 or len(found[0]) != 11 or found[0][1].rsplit(' — ', 1)[-1] != EVIDENCE
                or found[0][2:4] != ['own-work', 'A'] or found[0][7] != 'mined' or any('\\' in cell for cell in found[0])):
            add('EDIT-SOURCE', 'S086')
        cells = table_cells(text)
        by_id = {r['id']: r for r in rows}
        for expected in EXPECTED:
            ident = expected[0]
            row = by_id.get(ident)
            correct = (row is not None and set(row) == {'id', 'decision', 'reason', 'evidence', 'policy'}
                       and tuple(row.get(k) for k in ('id', 'decision', 'reason', 'evidence', 'policy')) == expected)
            matches = [r for r in cells if r and r[0] == ident]
            if not correct or matches != [list(expected)]:
                add('EDIT-DECISION-MISMATCH', ident)
            else:
                count += 1
        if data.get('scope') != LIMIT or PROSE_LIMIT not in '\n'.join(visible(text)):
            add('EDIT-LIMIT-MISSING', 'scope')
        code = 1 if findings else 0
    except (ValueError, TypeError, KeyError, UnicodeError, AttributeError):
        add('EDIT-SCHEMA', DATA)
        code = 2
    if any(f['id'] != 'EDIT-DECISION-MISMATCH' for f in findings):
        count = 0
    return code, {'status': ('PASS', 'FAIL', 'CANNOT_EVALUATE')[code], 'validated_edit_decisions': count,
                  'total_decisions': len(EXPECTED), 'findings': findings, 'scope': LIMIT}


def selftest():
    # Independent literal fixture: never synthesized from the evaluator's EXPECTED map.
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
    data = {'schema': 'tsukuroi-edit-policy-v1',
            'decisions': [dict(zip(('id', 'decision', 'reason', 'evidence', 'policy'), r)) for r in literal],
            'source_path': '.ufo/waves/round-23/sources/structured-edit-observations.json',
            'scope': 'Declared audit authority for structured target metadata only; no native prevention, opaque patch interpretation, effect or reading proof.'}
    prose = '| ID | Decision | Reason | Evidence | Policy |\n|---|---|---|---|---|\n' + '\n'.join('| ' + ' | '.join(r) + ' |' for r in literal) + '\nIt is not native permission enforcement, a sandbox.'
    sources = '| S086 | edit metadata — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry |'
    lane = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'
    obs = {'schema': 'tsukuroi-structured-edit-observations-v1', 'observations': [
        {'tool': 'edit', 'argument_keys': ['path', 'stream_content'], 'path': lane + 'x/A.md', 'body_fields': 'omitted; no report text copied',
         'recorded_starts': [{'tool': 'write'}], 'transcript_sha256': 'a' * 64},
        {'tool': 'edit', 'argument_keys': ['i', 'new_string', 'old_string', 'path'], 'path': lane + 'x/B.md', 'body_fields': 'omitted; no report text copied',
         'recorded_starts': [{'tool': 'edit'}], 'transcript_sha256': 'b' * 64}]}
    pre = {'edit_decisions': [list(r[:3]) for r in literal]}
    ev, pr = json.dumps(obs), json.dumps(pre)
    def mut(fn, base=obs):
        m = copy.deepcopy(base)
        fn(m)
        return json.dumps(m)
    cases = [('clean', json.dumps(data), prose, sources, ev, pr, 0, None),
             ('missing', None, prose, sources, ev, pr, 1, 'EDIT-CONTRACT-MISSING'),
             ('missing-prose', json.dumps(data), None, sources, ev, pr, 1, 'EDIT-CONTRACT-MISSING')]
    for i in range(8):
        for field, forged in (('decision', 'ALLOW' if literal[i][1] != 'ALLOW' else 'DENY'), ('reason', 'FORGED'), ('evidence', 'S085'), ('policy', 'operator')):
            mutant = copy.deepcopy(data)
            mutant['decisions'][i][field] = forged
            cases.append((f'{field}-{i}', json.dumps(mutant), prose, sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'))
        cases.append((f'table-{i}', json.dumps(data), prose.replace('| ' + literal[i][0] + ' |', '| X' + literal[i][0] + ' |', 1), sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'))
    swapped = copy.deepcopy(data)
    swapped['decisions'][0], swapped['decisions'][1] = dict(swapped['decisions'][0], decision='DENY'), dict(swapped['decisions'][1], decision='ALLOW')
    duplicate = copy.deepcopy(data)
    duplicate['decisions'][7] = duplicate['decisions'][0]
    extra = copy.deepcopy(data)
    extra['decisions'][0]['native'] = True
    cases.extend([
        ('allow-deny-swap', json.dumps(swapped), prose, sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'),
        ('extra-row-field', json.dumps(extra), prose, sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'),
        ('duplicate-id', json.dumps(duplicate), prose, sources, ev, pr, 2, 'EDIT-SCHEMA'),
        ('duplicate-key', '{"schema":1,"schema":2}', prose, sources, ev, pr, 2, 'EDIT-SCHEMA'),
        ('extra-top-key', json.dumps(dict(data, native_enforcement=True)), prose, sources, ev, pr, 2, 'EDIT-SCHEMA'),
        ('hidden', json.dumps(data), '<!--\n' + prose + '\n-->', sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'),
        ('fenced', json.dumps(data), '```\n' + prose + '\n```', sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'),
        ('quoted-duplicate', json.dumps(data), prose + '\n> | READ_ONLY_EDIT | ALLOW | wrong | S086 | round23-preregister |', sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'),
        ('limit-omitted', json.dumps(data), prose.replace('It is not native permission enforcement', 'It is native permission enforcement'), sources, ev, pr, 1, 'EDIT-LIMIT-MISSING'),
        ('scope-overclaim', json.dumps(dict(data, scope='Native runtime enforcement of edit targets.')), prose, sources, ev, pr, 1, 'EDIT-LIMIT-MISSING'),
        ('hidden-limit', json.dumps(data), prose.replace('It is not native permission enforcement', '<!-- It is not native permission enforcement -->'), sources, ev, pr, 1, 'EDIT-LIMIT-MISSING'),
        ('source-missing', json.dumps(data), prose, '', ev, pr, 1, 'EDIT-SOURCE'),
        ('source-wrong-path', json.dumps(data), prose, sources.replace('— .ufo/', '— /tmp/decoy/.ufo/'), ev, pr, 1, 'EDIT-SOURCE'),
        ('source-wrong-tier', json.dumps(data), prose, sources.replace('| A |', '| C |'), ev, pr, 1, 'EDIT-SOURCE'),
        ('source-rejected', json.dumps(data), prose, sources.replace('| mined |', '| rejected |'), ev, pr, 1, 'EDIT-SOURCE'),
        ('source-duplicate', json.dumps(data), prose, sources + '\n' + sources, ev, pr, 1, 'EDIT-SOURCE'),
        ('evidence-missing', json.dumps(data), prose, sources, None, pr, 1, 'EDIT-EVIDENCE'),
        ('evidence-body-copied', json.dumps(data), prose, sources, mut(lambda m: m['observations'][0].update(body_fields='report text here')), pr, 1, 'EDIT-EVIDENCE'),
        ('evidence-unknown-key', json.dumps(data), prose, sources, mut(lambda m: m['observations'][0]['argument_keys'].append('patch')), pr, 1, 'EDIT-EVIDENCE'),
        ('evidence-one-shape', json.dumps(data), prose, sources, mut(lambda m: m['observations'].pop()), pr, 1, 'EDIT-EVIDENCE'),
        ('evidence-outside-path', json.dumps(data), prose, sources, mut(lambda m: m['observations'][0].update(path='/etc/passwd')), pr, 1, 'EDIT-EVIDENCE'),
        ('evidence-wrong-tool', json.dumps(data), prose, sources, mut(lambda m: m['observations'][1].update(tool='write')), pr, 1, 'EDIT-EVIDENCE'),
        ('source-path-swap', json.dumps(dict(data, source_path='.ufo/waves/round-23/sources/r22-rough-census.txt')), prose, sources, ev, pr, 1, 'EDIT-EVIDENCE'),
        ('policy-source-swap', json.dumps(data), prose, sources, ev, json.dumps({'edit_decisions': [list(r[:3]) for r in literal[::-1]]}), 1, 'EDIT-POLICY-SOURCE'),
        ('policy-source-missing', json.dumps(data), prose, sources, ev, None, 1, 'EDIT-POLICY-SOURCE'),
    ])
    observations = []
    for name, raw, text, src, evid, prereg, expected_code, expected_id in cases:
        code, result = evaluate(raw, text, src, evid, prereg)
        ids = [f['id'] for f in result['findings']]
        ok = code == expected_code and (expected_id is None or expected_id in ids) and (expected_code != 0 or result['validated_edit_decisions'] == 8)
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': ok})
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
        code, payload = evaluate(git_read(binding.sha, DATA), git_read(binding.sha, PROSE), git_read(binding.sha, 'corpus/SOURCES.md'), git_read(binding.sha, EVIDENCE), git_read(binding.sha, PREREGISTER))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'EDIT-READ', 'site': 'revision'}]}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
