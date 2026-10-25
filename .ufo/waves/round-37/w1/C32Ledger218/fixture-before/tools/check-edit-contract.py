#!/usr/bin/env python3
"""Validate eight finite structured-edit authority decisions; never native runtime enforcement."""
from __future__ import annotations
import argparse
import copy
import hashlib
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
PROSE_LIMIT = 'This is declared post-hoc audit authority only. It is not native permission enforcement, a sandbox, body/patch interpretation, actual reading or effects proof, complete recorder coverage, or permission for host/package/service/boot actions. The task API still has no restrictive per-seat allowlist. Numeric mode availability is not compliance.'
EVIDENCE_SCOPE = 'Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof.'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'
SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})
# Closed finite document carrier: these literals are not a Markdown renderer or a prose theorem.
PROSE_SHA256 = '4bf5433b57e7491024ce466b831c19a9879cfd8c79858fb88908ea8edaab746f'
C1_DECLARATION = {'id': 'C1', 'axis': 'depth', 'metric': 'validated_edit_decisions', 'before': 0, 'target': 8, 'command': 'python3 tools/check-edit-contract.py --revision <REV>', 'scope': 'Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors.'}
SOURCE_ROW = ['S086', 'Structured edit request metadata and adapter steps — .ufo/waves/round-23/sources/structured-edit-observations.json', 'own-work', 'A', 'Observed finite path/argument-key shapes and recorded native steps, not universal editor semantics, actual effects or runtime permission enforcement', 'observations argument_keys/path/recorded_starts and transcript SHA-256; baseline provenance at .ufo/waves/round-23/preregister.json baseline (ae01e50f582016384e620022be38bf5367000e2e); opened2026-10-21', 'Structured edit metadata exposes two finite target/body-key shapes and producer-attributed read/write/edit starts, not permission outcomes; authority is declared separately and prospectively for each exact target', 'mined', '2026-10-21', 'on-release', 'corpus/knowledge/structured-edit-r23.md, corpus/lessons/round-23.md']


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


def prose_limit_ok(text):
    # Finite visible-carrier rule, not arbitrary Markdown rendering or synonym detection.
    lines = visible(text)
    return (lines.count(PROSE_LIMIT) == 1
            and all(not ("<" in line and not line.startswith("recheck:")) for line in lines)
            and all(not re.search(r'enforc|sandbox|prevent', line, re.I) for line in lines if line != PROSE_LIMIT))

def evidence_ok(evidence):
    """Validate a finite metadata sample; nesting is producer attribution, not causal/effect proof."""
    data = json.loads(evidence, object_pairs_hook=unique)
    if (not isinstance(data, dict) or set(data) != {'schema', 'accessed', 'observations', 'scope'}
            or data.get('scope') != EVIDENCE_SCOPE or data.get('accessed') != '2026-10-21'
            or data.get('schema') != 'tsukuroi-structured-edit-observations-v1'):
        return False
    rows = data.get('observations')
    if not isinstance(rows, list) or not rows:
        return False
    shapes, calls, agents = set(), set(), {}
    fields = {'seat', 'agent', 'transcript_sha256', 'request_line', 'call_id', 'tool', 'argument_keys', 'path', 'body_fields', 'recorded_starts'}
    for row in rows:
        if not isinstance(row, dict) or set(row) != fields:
            return False
        keys, path, starts = row['argument_keys'], row['path'], row['recorded_starts']
        if (row['tool'] != 'edit' or not isinstance(keys, list) or not all(isinstance(k, str) for k in keys)
                or len(keys) != len(set(keys)) or row['body_fields'] != 'omitted; no report text copied'
                or not isinstance(path, str) or not path.startswith(LANE) or path == LANE
                or any(p in ('', '.', '..') for p in path.split('/')[1:]) or re.search(r'[:;*?\[\]\\\x00-\x20]', path)
                or not isinstance(starts, list) or not starts
                or not isinstance(row['seat'], str) or not row['seat'] or not isinstance(row['agent'], str) or not row['agent']
                or not re.fullmatch(r'[0-9a-f]{64}', row['transcript_sha256'])
                or type(row['request_line']) is not int or row['request_line'] <= 0
                or not isinstance(row['call_id'], str) or not row['call_id'] or row['call_id'] in calls):
            return False
        calls.add(row['call_id'])
        identity = (row['seat'], row['transcript_sha256'])
        if row['agent'] in agents and agents[row['agent']] != identity:
            return False
        agents[row['agent']] = identity
        for start in starts:
            if (not isinstance(start, dict) or set(start) != {'line', 'tool', 'path'}
                    or type(start['line']) is not int or start['line'] <= 0 or start['tool'] not in ('read', 'write', 'edit')
                    or start['path'] not in ((path, path + ':raw') if start['tool'] == 'read' else (path,))):
                return False
        # Start ordering is intentionally not required: the sample includes starts before the request line.
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
        if (not isinstance(pre, dict) or pre.get('schema') != 'tsukuroi-round23-preregister-v1'
                or pre.get('baseline') != 'ae01e50f582016384e620022be38bf5367000e2e'
                or [c for c in pre.get('claims', []) if isinstance(c, dict) and c.get('id') == 'C1'] != [C1_DECLARATION]):
            add('EDIT-CLAIM-BINDING', PREREGISTER)
        found = [r for r in table_cells(source_text or '') if r and re.sub(r'[^A-Za-z0-9]', '', r[0]).upper() == 'S086']
        if found != [SOURCE_ROW]:
            add('EDIT-SOURCE', 'S086')
        cells = table_cells(text)
        if cells != [['ID', 'Decision', 'Reason', 'Evidence', 'Policy'], ['---'] * 5, *[list(e) for e in EXPECTED]]:
            add('EDIT-TABLE', PROSE)
        if hashlib.sha256(text.encode('utf-8')).hexdigest() != PROSE_SHA256:
            add('EDIT-PROSE', PROSE)
        visible_text = '\n'.join(visible(text))
        by_id = {r['id']: r for r in rows}
        for expected in EXPECTED:
            ident = expected[0]
            row = by_id.get(ident)
            correct = (row is not None and set(row) == {'id', 'decision', 'reason', 'evidence', 'policy'}
                       and tuple(row.get(k) for k in ('id', 'decision', 'reason', 'evidence', 'policy')) == expected)
            matches = [r for r in cells if r and r[0] == ident]
            if not correct or matches != [list(expected)] or len(re.findall(r"(?<![A-Za-z0-9_])" + re.escape(ident) + r"(?![A-Za-z0-9_])", visible_text)) != 1:
                add('EDIT-DECISION-MISMATCH', ident)
            else:
                count += 1
        if data.get('scope') != LIMIT or not prose_limit_ok(text):
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
    prose = "source: S086 — .ufo/waves/round-23/sources/structured-edit-observations.json, observations argument_keys/path/recorded_starts; policy: .ufo/waves/round-23/preregister.json edit_decisions\nverified-at: 2026-10-21; round23 source packet derived from round22 transcripts at baseline ae01e50f582016384e620022be38bf5367000e2e; landed gate measurements in SCORECARD.md Round23\nrecheck: python3 tools/check-edit-contract.py --revision <landed-hex>\n\n# Structured edit authority for this lane's evidence files\n\nThe source is a finite sample of four structured `edit` requests from two round22 seats, with a `path` field and either `stream_content` or `old_string`/`new_string` argument keys. Body values are deliberately omitted. The producer nests recorded starts under each request, but those starts do not carry their own call IDs; one read/write pair precedes its request line and three other requests have edit-only starts. Nesting is producer attribution, not independent causal, reading or effects proof. The sample witnesses metadata shapes, not any permission outcome or a denial instance.\n\nAuthority is separately declared lane policy. A source-only report writer can be granted exact prospective report-read/write/edit targets before dispatch; report ownership alone never grants extra reads or an edit. Schema-v1 historical bindings remain unchanged and retain all earlier violations. No grant is retroactive.\n\nAll eight table rows are prospective lane-policy decisions; S086 supplies the metadata vocabulary, not normative permission. Any missing leg of the read/write/edit conjunction is non-authorizing, including an edit-only declaration with neither read nor write. In the v2 auditor a malformed authority declaration or an unstructured edit is could-not-evaluate (exit2); a supported edit with a non-declared target is a finding (exit1). This does not enlarge the frozen eight-row target.\n\nThese decisions are tsukuroi's finite audit convention for bindings this lane declares and its own recorded steps, not a fleet binding-schema definition or a rule for sibling-owned tools. Supported edit keys are exactly `{path,stream_content}` or `{path,old_string,new_string}`, optionally `i`; body values remain opaque.\n\n## Decision table\n\n| ID | Decision | Reason | Evidence | Policy |\n|---|---|---|---|---|\n| DECLARED_EDIT | ALLOW | Exact target is predeclared for edit and for both read and write | S086 | round23-preregister |\n| UNDECLARED_EDIT | DENY | No implicit edit permission from generic report ownership | S086 | round23-preregister |\n| READ_ONLY_EDIT | DENY | Read authority never grants a write | S086 | round23-preregister |\n| WRITE_ONLY_EDIT | DENY | Edit also needs its explicit target read authority | S086 | round23-preregister |\n| OPAQUE_PATCH | UNKNOWN | Missing structured target is not inferred from opaque patch text | S086 | round23-preregister |\n| EDIT_TRAVERSAL | DENY | No dot-segment or alternate spelling expands the target list | S086 | round23-preregister |\n| EDIT_EXTERNAL | DENY | Remote or internal URIs do not become filesystem edit targets | S086 | round23-preregister |\n| EXPANSION | CHECK_EACH | Every recorded adapter read or write remains separately scoped | S086 | round23-preregister |\n\n## Bounded procedure\n\n1. Freeze explicit schema-v2 `edit_paths` as canonical literal subsets of both read and write targets. A malformed authority declaration is non-clean before interpreting an event.\n2. For a recorded structured edit, require the exact declared target and one of the two observed finite argument-key shapes, with only separately allowed metadata keys. Opaque body data is not interpreted or executed by the auditor.\n3. Missing structured targets, freeform patches, unknown keys, URI targets and alternate path spellings never gain authority by inference. Unknown means could-not-evaluate or rejection, never permission.\n4. Audit every captured native read/write expansion against its own authority. A valid frontend target cannot clear an out-of-binding backend step or a forbidden command/fetch.\n\nThis is declared post-hoc audit authority only. It is not native permission enforcement, a sandbox, body/patch interpretation, actual reading or effects proof, complete recorder coverage, or permission for host/package/service/boot actions. The task API still has no restrictive per-seat allowlist. Numeric mode availability is not compliance.\n\n## QUALITY check\n\nThe eight finite policy decisions are falsifiable, with observed source metadata separated from normative authority (QUALITY1/3/7/19/45). Independent literal positive/negative controls must check every row, source/policy mapping and refusal class; source-only opinions are not empirical runs. QUALITY42/46–48 require frozen inputs, actual request precedence and honest incomplete evidence. This deepens held evidence-operability ground, not an uncovered frontier, repertoire addition or outside promotion. Final admitted/rejected decisions and actual measurements belong to the round23 lesson and SCORECARD; no unrun result is asserted here.\n"
    sources = '| S086 | Structured edit request metadata and adapter steps — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | Observed finite path/argument-key shapes and recorded native steps, not universal editor semantics, actual effects or runtime permission enforcement | observations argument_keys/path/recorded_starts and transcript SHA-256; baseline provenance at .ufo/waves/round-23/preregister.json baseline (ae01e50f582016384e620022be38bf5367000e2e); opened2026-10-21 | Structured edit metadata exposes two finite target/body-key shapes and producer-attributed read/write/edit starts, not permission outcomes; authority is declared separately and prospectively for each exact target | mined | 2026-10-21 | on-release | corpus/knowledge/structured-edit-r23.md, corpus/lessons/round-23.md |'
    lane = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/'
    obs = {'schema': 'tsukuroi-structured-edit-observations-v1', 'accessed': '2026-10-21', 'scope': 'Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof.', 'observations': [
        {'tool': 'edit', 'argument_keys': ['path', 'stream_content'], 'path': lane + 'x/A.md', 'body_fields': 'omitted; no report text copied',
         'seat': 'A', 'agent': 'Agent.A', 'request_line': 15, 'call_id': 'callA', 'transcript_sha256': 'a' * 64,
         'recorded_starts': [{'tool': 'read', 'line': 12, 'path': lane + 'x/A.md:raw'}, {'tool': 'write', 'line': 13, 'path': lane + 'x/A.md'}]},
        {'tool': 'edit', 'argument_keys': ['i', 'new_string', 'old_string', 'path'], 'path': lane + 'x/B.md', 'body_fields': 'omitted; no report text copied',
         'seat': 'B', 'agent': 'Agent.B', 'request_line': 20, 'call_id': 'callB', 'transcript_sha256': 'b' * 64,
         'recorded_starts': [{'tool': 'edit', 'line': 21, 'path': lane + 'x/B.md'}]}]}
    pre = {'schema': 'tsukuroi-round23-preregister-v1', 'baseline': 'ae01e50f582016384e620022be38bf5367000e2e', 'claims': [{'id': 'C1', 'axis': 'depth', 'metric': 'validated_edit_decisions', 'before': 0, 'target': 8, 'command': 'python3 tools/check-edit-contract.py --revision <REV>', 'scope': 'Eight finite source-grounded structured-edit authority decisions; new document contract, not eight repaired runtime behaviors.'}], 'edit_decisions': [list(r[:3]) for r in literal]}
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
    # Falsify-wave controls: exact visible limit carrier and exact shape-only source metadata.
    for name, changed in [
        ('later-enforcement-overclaim', prose + '\nThe checker provides native permission enforcement.'),
        ('inverted-limit', prose.replace('It is not native permission enforcement,', 'It is not native permission enforcement that is missing;')),
        ('struck-limit', prose.replace('This is declared post-hoc audit authority only.', '~~This is declared post-hoc audit authority only.')),
        ('link-reference-limit', prose.replace('This is declared post-hoc audit authority only.', '[This is declared post-hoc audit authority only.')),
        ('enforced-title', '# Native-enforced edits\n' + prose),
        ('missing-companion-limits', prose.replace(' The task API still has no restrictive per-seat allowlist.', '')),
    ]:
        cases.append((name, json.dumps(data), changed, sources, ev, pr, 1, 'EDIT-LIMIT-MISSING'))
    for carrier in ('**READ_ONLY_EDIT**', '`READ_ONLY_EDIT`', '[READ_ONLY_EDIT](x)', 'read_only_edit'):
        cases.append(('duplicate-carrier-' + carrier, json.dumps(data), prose + '\n| ' + carrier + ' | ALLOW | wrong | S086 | round23-preregister |', sources, ev, pr, 1, 'EDIT-TABLE'))
    cases.append(('prose-contradiction', json.dumps(data), prose + '\nREAD_ONLY_EDIT is ALLOW.', sources, ev, pr, 1, 'EDIT-DECISION-MISMATCH'))
    cases.append(('html-hidden-table', json.dumps(data), '<div>\n' + prose + '\n</div>', sources, ev, pr, 1, 'EDIT-LIMIT-MISSING'))
    for name, fn in [
        ('scope-overclaim', lambda m: m.update(scope='Native prevention')),
        ('extra-top-key', lambda m: m.update(new_string='report body')),
        ('extra-row-key', lambda m: m['observations'][0].update(new_string='report body')),
        ('missing-call-id', lambda m: m['observations'][0].pop('call_id')),
        ('duplicate-call-id', lambda m: m['observations'][1].update(call_id='callA')),
        ('request-line-zero', lambda m: m['observations'][0].update(request_line=0)),
        ('request-line-bool', lambda m: m['observations'][0].update(request_line=True)),
        ('invalid-start', lambda m: m['observations'][0].update(recorded_starts=[None])),
        ('start-exec', lambda m: m['observations'][0]['recorded_starts'][0].update(tool='bash')),
        ('start-other-target', lambda m: m['observations'][0]['recorded_starts'][0].update(path=lane + 'x/B.md')),
        ('start-extra-key', lambda m: m['observations'][0]['recorded_starts'][0].update(content='body')),
        ('start-line-zero', lambda m: m['observations'][0]['recorded_starts'][0].update(line=0)),
        ('row-dot-path', lambda m: m['observations'][0].update(path=lane + 'x/../A.md')),
        ('row-trailing-dot', lambda m: m['observations'][0].update(path=lane + 'x/..')),
        ('row-selector', lambda m: m['observations'][0].update(path=lane + 'x/A.md:raw')),
        ('agent-digest-drift', lambda m: m['observations'][1].update(agent='Agent.A')),
    ]:
        cases.append(('evidence-' + name, json.dumps(data), prose, sources, mut(fn), pr, 1, 'EDIT-EVIDENCE'))
    for name, changed in [('prose-grant', prose.replace('report ownership alone never grants', 'report ownership alone grants')), ('unknown-grant', prose.replace('Unknown means could-not-evaluate or rejection, never permission.', 'Unknown is provisional permission.')), ('added-prose', prose + '\nAn extra authority assertion.'), ('ninth-row', prose + '\n| NATIVE_ENFORCE | ALLOW | x | S086 | round23-preregister |')]:
        cases.append((name, json.dumps(data), changed, sources, ev, pr, 1, 'EDIT-PROSE'))
    changed_pre = copy.deepcopy(pre); changed_pre['claims'][0]['target'] = 4
    cases.append(('claim-target-move', json.dumps(data), prose, sources, ev, json.dumps(changed_pre), 1, 'EDIT-CLAIM-BINDING'))
    cases.append(('source-teaches-forgery', json.dumps(data), prose, sources.replace('not permission outcomes', 'permission outcomes'), ev, pr, 1, 'EDIT-SOURCE'))
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
