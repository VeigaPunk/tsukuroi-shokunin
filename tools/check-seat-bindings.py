#!/usr/bin/env python3
"""Audit recorded requests against frozen prompt scopes; not preventive enforcement."""
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
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
SCOPE = 'Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def controls(value):
    return any(unicodedata.category(c) in ('Cc', 'Cf', 'Cs', 'Zl', 'Zp') for c in value)


def local(path):
    return (isinstance(path, str) and bool(path) and path.startswith(LANE + '/') and '\\' not in path
            and not controls(path) and not any(c in path for c in '*?[];:')
            and all(p not in ('', '.', '..') for p in path.split('/')[1:]))


def repo_path(path):
    return isinstance(path, str) and bool(path) and not path.startswith('/') and not controls(path) and '\\' not in path and all(p not in ('', '.', '..') for p in path.split('/'))


def requested_path(value, selector=False):
    if not isinstance(value, str):
        raise ValueError('path argument must be a string')
    if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
        return value, 'SCOPE-FETCH-DENIED'
    if value == 'skill://godspeed':
        return value, None
    if selector and ':' in value:
        base, *tokens = value.split(':')
        def valid_token(token):
            return token in ('raw', 'img', 'conflicts') or all(re.fullmatch(r'\d+(?:[-+]\d*)?|-\d+', part) for part in token.split(','))
        if tokens and all(valid_token(token) for token in tokens):
            value = base
    if not local(value):
        return value, 'SCOPE-PATH-DENIED'
    return value, None


def classify(tool, args, binding, depth=0, allow_structured_edit=False):
    """Return finite post-hoc findings; never execute the requested operation.

    allow_structured_edit is set only by evaluate() from a validated top-level v2 schema,
    never from a row field or event marker.
    """
    if not isinstance(tool, str) or not tool or depth > 8:
        raise ValueError('malformed tool name or excessive wrapper nesting')
    if tool.startswith('functions.'):
        tool = tool[len('functions.'):]
    # A known forbidden tool remains evidence even when its payload is missing.
    if tool in ('bash', 'eval', 'task'):
        return ['SCOPE-EXEC-DENIED']
    if tool in ('web_search', 'browser') or tool.startswith('browser.'):
        return ['SCOPE-FETCH-DENIED']
    if tool == 'edit' and allow_structured_edit:
        return classify_edit(args, binding)
    if tool not in ('read', 'grep', 'glob', 'write', 'multi_tool_use.parallel', 'parallel'):
        return ['SCOPE-TOOL-UNKNOWN']
    if not isinstance(args, dict):
        raise ValueError('malformed tool arguments')
    if tool in ('multi_tool_use.parallel', 'parallel'):
        children = args.get('tool_uses')
        if set(args) != {'tool_uses'} or not isinstance(children, list) or not children:
            raise ValueError('malformed parallel request')
        findings = []
        for child in children:
            try:
                if not isinstance(child, dict) or set(child) != {'recipient_name', 'parameters'}:
                    raise ValueError('malformed parallel child')
                findings.extend(classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1, allow_structured_edit))
            except (ValueError, TypeError, KeyError, AttributeError):
                findings.append('SCOPE-SCHEMA')
        return findings
    allowed_keys = {
        'read': {'i', 'path'},
        'grep': {'i', 'pattern', 'path', 'case', 'gitignore', 'skip'},
        'glob': {'i', 'path', 'hidden', 'gitignore', 'limit'},
        'write': {'i', 'path', 'content'},
    }
    unknown_keys = bool(set(args) - allowed_keys[tool])
    value = args.get('path')
    if not isinstance(value, str) or not value:
        raise ValueError('missing explicit path')
    values = value.split(';') if tool in ('grep', 'glob') else [value]
    findings = ['SCOPE-SCHEMA'] if unknown_keys else []
    for value in values:
        path, denial = requested_path(value, selector=tool in ('read', 'grep'))
        if denial:
            findings.append(denial)
        elif path not in binding['write_paths' if tool == 'write' else 'read_paths']:
            findings.append('SCOPE-PATH-DENIED')
    return findings


EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})


def classify_edit(args, binding):
    """v2 structured edit: exact declared target, finite observed key shapes; bodies stay opaque."""
    if not isinstance(args, dict) or set(args) - {'i'} not in EDIT_SHAPES:
        raise ValueError('unstructured or unknown edit arguments')
    value = args.get('path')
    if not isinstance(value, str) or not value:
        raise ValueError('missing explicit edit target')
    if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
        return ['SCOPE-FETCH-DENIED']
    if value not in binding['edit_paths']:
        return ['SCOPE-EDIT-DENIED']
    return []


def evaluate(manifest, events):
    findings, rows = [], []
    def add(fid, site):
        findings.append({'id': fid, 'site': site})
    if manifest is None:
        return 1, {'status': 'FAIL', 'request_audit_mode': 0, 'seats_bound': 0, 'requests_total': 0, 'findings': [{'id': 'SCOPE-BINDINGS-MISSING', 'site': 'manifest'}], 'scope': SCOPE}
    total = violations = incomplete = 0
    v2 = False
    try:
        data = json.loads(manifest, object_pairs_hook=unique) if isinstance(manifest, (str, bytes)) else manifest
        v2 = isinstance(data, dict) and data.get('schema') == 'tsukuroi-seat-bindings-v2'
        trace = json.loads(events, object_pairs_hook=unique) if isinstance(events, (str, bytes)) else events
        if not isinstance(data, dict) or set(data) != {'schema', 'seats'} or data.get('schema') not in ('tsukuroi-seat-bindings-v1', 'tsukuroi-seat-bindings-v2') or not isinstance(data.get('seats'), list) or not data['seats']:
            raise ValueError('binding schema')
        bound = {}
        for seat in data['seats']:
            if not isinstance(seat, dict) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', seat.get('name', '')) or seat['name'] in bound or seat.get('root') != LANE or seat.get('commands') != [] or seat.get('fetches') != []:
                raise ValueError('binding identity/root/allowlist')
            for field in ('read_paths', 'write_paths'):
                paths = seat.get(field)
                if not isinstance(paths, list) or not paths or any(not local(p) and not (field == 'read_paths' and p == 'skill://godspeed') for p in paths) or len(paths) != len(set(paths)):
                    raise ValueError('binding paths')
            if v2:
                # Explicit v2 authority: every exact edit target is also literally readable and writable.
                edits = seat.get('edit_paths')
                if (set(seat) != {'name', 'root', 'read_paths', 'write_paths', 'edit_paths', 'commands', 'fetches'}
                        or not isinstance(edits, list) or len(edits) != len(set(edits))
                        or any(not local(p) or p not in seat['read_paths'] or p not in seat['write_paths'] for p in edits)):
                    raise ValueError('v2 edit authority')
            bound[seat['name']] = seat
        if not isinstance(trace, dict) or set(trace) - {'schema', 'seats', 'coverage'} or trace.get('schema') != 'tsukuroi-seat-events-v1' or not isinstance(trace.get('seats'), list):
            raise ValueError('events schema')
        by_name, agents = {}, set()
        for seat in trace['seats']:
            if not isinstance(seat, dict) or seat.get('name') not in bound or seat['name'] in by_name or not isinstance(seat.get('agent'), str) or not seat['agent'] or seat['agent'] in agents or type(seat.get('complete')) is not bool or not isinstance(seat.get('events'), list):
                raise ValueError('trace identity or shape')
            by_name[seat['name']] = seat
            agents.add(seat['agent'])
        for name, binding in bound.items():
            seat = by_name.get(name)
            if seat is None:
                incomplete += 1
                add('SCOPE-TRACE-MISSING', name)
                continue
            if not seat['complete']:
                incomplete += 1
                add('SCOPE-TRACE-INCOMPLETE', name)
            seat_findings = []
            for index, event in enumerate(seat['events']):
                total += 1
                try:
                    if not isinstance(event, dict):
                        raise ValueError('event shape')
                    ids = classify(event.get('tool'), event.get('args'), binding, allow_structured_edit=v2)
                except (ValueError, TypeError, KeyError, AttributeError, UnicodeError):
                    ids = ['SCOPE-SCHEMA']
                for fid in ids:
                    add(fid, f'{name}:{index}')
                    seat_findings.append(fid)
                violations += sum(fid != 'SCOPE-SCHEMA' for fid in ids)
            rows.append({'name': name, 'agent': seat['agent'], 'requests': len(seat['events']), 'complete': seat['complete'], 'violations': seat_findings})
        code = 2 if incomplete or any(f['id'] == 'SCOPE-SCHEMA' for f in findings) else (1 if findings else 0)
    except (ValueError, TypeError, KeyError, AttributeError, UnicodeError, RecursionError):
        add('SCOPE-SCHEMA', 'input')
        code = 2
        bound = locals().get('bound', {})
    result = {'status': ('PASS', 'FAIL', 'CANNOT_EVALUATE')[code], 'request_audit_mode': int(code != 2),
              'seats_bound': len(bound), 'requests_total': total, 'violations': violations,
              'incomplete_seats': incomplete,
              'missing_seats': sum(f['id'] == 'SCOPE-TRACE-MISSING' for f in findings),
              'present_incomplete_seats': sum(f['id'] == 'SCOPE-TRACE-INCOMPLETE' for f in findings),
              'seats': rows, 'findings': findings, 'scope': SCOPE}
    if v2:
        result['structured_edit_mode'] = int(code != 2)
    return code, result


def selftest():
    src, report = LANE + '/source', LANE + '/report'
    binding = {'schema': 'tsukuroi-seat-bindings-v1', 'seats': [{'name': 'A', 'root': LANE, 'read_paths': [src, 'skill://godspeed'], 'write_paths': [report], 'commands': [], 'fetches': []}]}
    def trace(tool='read', args=None):
        return {'schema': 'tsukuroi-seat-events-v1', 'seats': [{'name': 'A', 'agent': 'agent-A', 'complete': True, 'events': [{'tool': tool, 'args': {'path': src} if args is None else args}]}]}
    cases = []
    def case(name, tool, args, code, fid=None):
        cases.append((name, binding, trace(tool, args), code, fid))
    case('clean-read', 'read', {'path': src}, 0)
    case('qualified', 'functions.read', {'path': src}, 0)
    case('selector', 'read', {'path': src + ':1-5:raw'}, 0)
    case('skill', 'read', {'path': 'skill://godspeed'}, 0)
    case('write-exact', 'write', {'path': report}, 0)
    for tool in ('bash', 'eval', 'task'):
        case(tool, tool, {}, 1, 'SCOPE-EXEC-DENIED')
    for path in ('https://example.invalid', 'HTTPS://EXAMPLE.INVALID/:1-5', 'http://127.0.0.1/', 'localhost:9222/'):
        case('fetch-' + path, 'read', {'path': path}, 1, 'SCOPE-FETCH-DENIED')
    for tool in ('web_search', 'browser', 'browser.navigate'):
        case(tool, tool, {}, 1, 'SCOPE-FETCH-DENIED')
    for path in (src + '-extra', src + '/child', LANE + '/../sibling/file', LANE + '/x/../source', LANE + '/./source', 'source', 'xd://tool', 'artifact://a', LANE + '/**'):
        case('path-' + path, 'read', {'path': path}, 1, 'SCOPE-PATH-DENIED')
    for path in (report + '.extra', report + '/child', LANE + '/production'):
        case('write-' + path, 'write', {'path': path}, 1, 'SCOPE-PATH-DENIED')
    case('semicolon', 'grep', {'path': src + ';/outside'}, 1, 'SCOPE-PATH-DENIED')
    case('unknown', 'edit', {}, 1, 'SCOPE-TOOL-UNKNOWN')
    case('bad-args', 'read', {}, 2, 'SCOPE-SCHEMA')
    case('parallel-exec', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'functions.bash', 'parameters': {}}]}, 1, 'SCOPE-EXEC-DENIED')
    case('parallel-fetch', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'functions.read', 'parameters': {'path': 'https://example.invalid'}}]}, 1, 'SCOPE-FETCH-DENIED')
    case('parallel-local', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'functions.read', 'parameters': {'path': src}}]}, 0)
    case('parallel-malformed', 'multi_tool_use.parallel', {'tool_uses': [None]}, 2, 'SCOPE-SCHEMA')
    missing = trace(); missing['seats'] = []
    incomplete_trace = trace(); incomplete_trace['seats'][0]['complete'] = False
    duplicate = trace(); duplicate['seats'].append(copy.deepcopy(duplicate['seats'][0]))
    unknown = trace(); unknown['seats'][0]['name'] = 'B'
    empty = trace(); empty['seats'][0]['events'] = []
    badbinding = copy.deepcopy(binding); badbinding['seats'][0]['fetches'] = ['https://example.invalid']
    cases.extend([('missing-trace', binding, missing, 2, 'SCOPE-TRACE-MISSING'), ('incomplete', binding, incomplete_trace, 2, 'SCOPE-TRACE-INCOMPLETE'), ('duplicate', binding, duplicate, 2, 'SCOPE-SCHEMA'), ('unknown-seat', binding, unknown, 2, 'SCOPE-SCHEMA'), ('empty-trace', binding, empty, 0, None), ('nonempty-fetch-allowlist', badbinding, trace(), 2, 'SCOPE-SCHEMA'), ('missing-manifest', None, trace(), 1, 'SCOPE-BINDINGS-MISSING'), ('duplicate-json-key', '{"seats":[],"seats":[]}', trace(), 2, 'SCOPE-SCHEMA')])
    case('read-write-only', 'read', {'path': report}, 1, 'SCOPE-PATH-DENIED')
    case('write-read-only', 'write', {'path': src}, 1, 'SCOPE-PATH-DENIED')
    case('qualified-write', 'functions.write', {'path': report}, 0)
    case('skill-write', 'write', {'path': 'skill://godspeed'}, 1, 'SCOPE-PATH-DENIED')
    case('skill-other', 'read', {'path': 'skill://other'}, 1, 'SCOPE-PATH-DENIED')
    case('skill-selector', 'read', {'path': 'skill://godspeed:raw'}, 1, 'SCOPE-PATH-DENIED')
    case('extra-argument', 'glob', {'path': src, 'pattern': '/outside/*'}, 2, 'SCOPE-SCHEMA')
    case('qualified-parallel', 'functions.multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'functions.read', 'parameters': {'path': src}}]}, 0)
    case('null-exec-args', 'bash', None, 1, 'SCOPE-EXEC-DENIED')
    case('mixed-parallel', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'read', 'parameters': {}}, {'recipient_name': 'bash', 'parameters': {}}]}, 2, ('SCOPE-SCHEMA', 'SCOPE-EXEC-DENIED'))
    combined = trace('bash', {}); combined['seats'][0]['complete'] = False
    cases.append(('incomplete-exec', binding, combined, 2, ('SCOPE-TRACE-INCOMPLETE', 'SCOPE-EXEC-DENIED')))
    continued = trace(); continued['seats'][0]['events'] = [{'tool': 'read', 'args': {}}, {'tool': 'bash', 'args': {}}]
    cases.append(('malformed-before-exec', binding, continued, 2, ('SCOPE-SCHEMA', 'SCOPE-EXEC-DENIED')))
    dup_paths = copy.deepcopy(binding); dup_paths['seats'][0]['read_paths'].append(src)
    cases.append(('duplicate-bound-path', dup_paths, trace(), 2, 'SCOPE-SCHEMA'))
    dup_names = copy.deepcopy(binding); dup_names['seats'].append(copy.deepcopy(dup_names['seats'][0]))
    cases.append(('duplicate-bound-name', dup_names, trace(), 2, 'SCOPE-SCHEMA'))
    bad_name = copy.deepcopy(binding); bad_name['seats'][0]['name'] = '-A'
    bad_trace = trace(); bad_trace['seats'][0]['name'] = '-A'
    cases.append(('bad-bound-name', bad_name, bad_trace, 2, 'SCOPE-SCHEMA'))
    cases.append(('duplicate-valid-json', '{"schema":"bad",' + json.dumps(binding)[1:], trace(), 2, 'SCOPE-SCHEMA'))
    dup_trace = trace(); dup_trace['seats'].append(dict(dup_trace['seats'][0], agent='agent-B'))
    cases.append(('duplicate-trace-name-only', binding, dup_trace, 2, 'SCOPE-SCHEMA'))
    case('grep-nonvacuity', 'grep', {'path': src + ';' + src}, 0)
    case('glob-nonvacuity', 'glob', {'path': src}, 0)
    case('semicolon-first-denied', 'grep', {'path': '/outside;' + src}, 1, 'SCOPE-PATH-DENIED')
    case('grep-selector', 'grep', {'path': src + ':1-5'}, 0)
    case('linear-invalid-selector', 'read', {'path': src + ':' + '1-' * 1000 + '#'}, 1, 'SCOPE-PATH-DENIED')
    case('double-slash', 'read', {'path': LANE + '//source'}, 1, 'SCOPE-PATH-DENIED')
    case('extra-url-key', 'read', {'path': src, 'url': 'https://example.invalid'}, 2, 'SCOPE-SCHEMA')
    case('fetch-with-extra-key', 'read', {'path': 'https://example.invalid', 'url': 'https://example.invalid'}, 2, ('SCOPE-SCHEMA', 'SCOPE-FETCH-DENIED'))
    nested = {'recipient_name': 'bash', 'parameters': {}}
    for _ in range(3):
        nested = {'recipient_name': 'multi_tool_use.parallel', 'parameters': {'tool_uses': [nested]}}
    case('nested-exec', 'multi_tool_use.parallel', {'tool_uses': [nested]}, 1, 'SCOPE-EXEC-DENIED')
    for _ in range(8):
        nested = {'recipient_name': 'multi_tool_use.parallel', 'parameters': {'tool_uses': [nested]}}
    case('depth-exhausted', 'multi_tool_use.parallel', {'tool_uses': [nested]}, 2, 'SCOPE-SCHEMA')
    bad_root = copy.deepcopy(binding); bad_root['seats'][0]['root'] = '/outside'
    cases.append(('foreign-root', bad_root, trace(), 2, 'SCOPE-SCHEMA'))
    commands = copy.deepcopy(binding); commands['seats'][0]['commands'] = ['true']
    cases.append(('nonempty-commands', commands, trace(), 2, 'SCOPE-SCHEMA'))
    null_args = trace('bash', {}); null_args['seats'][0]['events'][0]['args'] = None
    cases.append(('actual-null-exec-args', binding, null_args, 1, 'SCOPE-EXEC-DENIED'))
    extra_trace = trace(); extra_trace['sidecar_requests'] = [{'tool': 'bash', 'args': {}}]
    cases.append(('trace-sidecar', binding, extra_trace, 2, 'SCOPE-SCHEMA'))
    # Schema-v2 structured edit controls: literal fixtures, independent of production manifests.
    target, other = LANE + '/drafts/A.md', LANE + '/drafts/B.md'
    v2 = {'schema': 'tsukuroi-seat-bindings-v2', 'seats': [{'name': 'A', 'root': LANE, 'read_paths': [src, target, other, 'skill://godspeed'],
                                                          'write_paths': [target, LANE + '/w-only.md'], 'edit_paths': [target], 'commands': [], 'fetches': []}]}
    v2_cases = []
    def v2case(name, tool, args, code, fid=None, manifest=None, mode=None, events=None):
        v2_cases.append((name, v2 if manifest is None else manifest, trace(tool, args) if events is None else events, code, fid, (int(code != 2) if mode is None else mode)))
    v2case('v2-stream-edit', 'edit', {'path': target, 'stream_content': None}, 0)
    v2case('v2-replace-edit', 'edit', {'i': None, 'path': target, 'old_string': None, 'new_string': None}, 0)
    v2case('v2-qualified-edit', 'functions.edit', {'path': target, 'stream_content': None}, 0)
    v2case('v2-read-only-target', 'edit', {'path': other, 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
    v2case('v2-write-only-target', 'edit', {'path': LANE + '/w-only.md', 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
    v2case('v2-undeclared-target', 'edit', {'path': LANE + '/production', 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
    for spelling in (target + '/', LANE + '/drafts/./A.md', LANE + '/x/../drafts/A.md', LANE + '//drafts/A.md', target + ':raw', 'drafts/A.md', 'skill://godspeed', 'xd://edit', target.upper()):
        v2case('v2-spelling-' + spelling, 'edit', {'path': spelling, 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED')
    v2case('v2-url-target', 'edit', {'path': 'https://example.invalid/A.md', 'stream_content': None}, 1, 'SCOPE-FETCH-DENIED')
    v2case('v2-opaque-patch', 'edit', {'input': None}, 2, 'SCOPE-SCHEMA')
    v2case('v2-unknown-key', 'edit', {'path': target, 'stream_content': None, '__unknown_argument__': None}, 2, 'SCOPE-SCHEMA')
    v2case('v2-mixed-shapes', 'edit', {'path': target, 'stream_content': None, 'old_string': None, 'new_string': None}, 2, 'SCOPE-SCHEMA')
    v2case('v2-half-replace', 'edit', {'path': target, 'old_string': None}, 2, 'SCOPE-SCHEMA')
    v2case('v2-missing-path', 'edit', {'stream_content': None}, 2, 'SCOPE-SCHEMA')
    v2case('v2-nested-edit', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'functions.edit', 'parameters': {'path': target, 'stream_content': None}}]}, 0)
    v2case('v2-nested-denied', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': other, 'stream_content': None}}]}, 1, 'SCOPE-EDIT-DENIED')
    after_bad = trace(); after_bad['seats'][0]['events'] = [{'tool': 'edit', 'args': {'input': None}}, {'tool': 'bash', 'args': {}}]
    v2case('v2-malformed-then-bash', None, None, 2, ('SCOPE-SCHEMA', 'SCOPE-EXEC-DENIED'), events=after_bad)
    v2case('v2-read-still-scoped', 'read', {'path': LANE + '/w-only.md'}, 1, 'SCOPE-PATH-DENIED')
    v2case('v2-write-target', 'write', {'path': target}, 0)
    # Authority declarations: subset, presence, no forged markers, v1 continuity.
    def v2mut(fn):
        m = copy.deepcopy(v2)
        fn(m['seats'][0])
        return m
    v2case('v2-edit-not-readable', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.update(edit_paths=[LANE + '/w-only.md'])))
    v2case('v2-edit-not-writable', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.update(edit_paths=[other])))
    v2case('v2-edit-paths-missing', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.pop('edit_paths')))
    v2case('v2-edit-paths-duplicate', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.update(edit_paths=[target, target])))
    v2case('v2-edit-paths-skill', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.update(edit_paths=['skill://godspeed'])))
    v2case('v2-row-marker', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=v2mut(lambda s: s.update(allow_structured_edit=True)))
    v2case('v2-empty-edit-paths', 'edit', {'path': target, 'stream_content': None}, 1, 'SCOPE-EDIT-DENIED', manifest=v2mut(lambda s: s.update(edit_paths=[])))
    v1_with_edit_field = copy.deepcopy(v2); v1_with_edit_field['schema'] = 'tsukuroi-seat-bindings-v1'
    v2case('v1-extra-edit-field-no-grant', 'edit', {'path': target, 'stream_content': None}, 1, 'SCOPE-TOOL-UNKNOWN', manifest=v1_with_edit_field, mode=-1)
    v2case('v1-edit-continuity', 'edit', {'path': report, 'stream_content': None}, 1, 'SCOPE-TOOL-UNKNOWN', manifest=binding, mode=-1)
    v2case('v2-schema-typo', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=dict(v2, schema='tsukuroi-seat-bindings-v3'), mode=-1)
    v2case('v2-events-trace-marker', 'edit', {'path': other, 'stream_content': None, 'allow_structured_edit': True}, 2, 'SCOPE-SCHEMA')
    v2case('v2-malformed-events-json', None, None, 2, 'SCOPE-SCHEMA', events='{')
    v2case('v2-top-extra-field', 'read', {'path': src}, 2, 'SCOPE-SCHEMA', manifest=dict(v2, extra=[]))
    v2case('v2-write-only-write', 'write', {'path': LANE + '/w-only.md'}, 0)
    v2case('v2-replace-denied-readonly', 'edit', {'path': other, 'old_string': None, 'new_string': None}, 1, 'SCOPE-EDIT-DENIED')
    v2case('v2-replace-denied-outside', 'edit', {'path': LANE + '/production', 'old_string': None, 'new_string': None}, 1, 'SCOPE-EDIT-DENIED')
    v2case('v1-nested-edit-no-grant', 'parallel', {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': target, 'stream_content': None}}]}, 1, 'SCOPE-TOOL-UNKNOWN', manifest=binding, mode=-1)
    v2case('v2-empty-target', 'edit', {'path': '', 'stream_content': None}, 2, 'SCOPE-SCHEMA')
    v2case('v2-uppercase-url', 'edit', {'path': 'HTTPS://EXAMPLE.INVALID/', 'stream_content': None}, 1, 'SCOPE-FETCH-DENIED')
    v2case('v2-host-port', 'edit', {'path': 'localhost:9222/', 'stream_content': None}, 1, 'SCOPE-FETCH-DENIED')
    for extra_tool in ('read', 'write'):
        expanded = trace(); expanded['seats'][0]['events'] = [
            {'tool': 'edit', 'args': {'path': target, 'stream_content': None}},
            {'tool': extra_tool, 'args': {'path': LANE + '/production'}, 'origin': 'additional-recorded-start'}]
        v2case('v2-expansion-other-' + extra_tool, None, None, 1, 'SCOPE-PATH-DENIED', events=expanded)
    observations = []
    for name, manifest, events, expected, fid in cases:
        code, result = evaluate(manifest, events)
        ids = [f['id'] for f in result['findings']]
        required = () if fid is None else (fid if isinstance(fid, tuple) else (fid,))
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': code == expected and all(item in ids for item in required)})
    for name, manifest, events, expected, fid, mode in v2_cases:
        code, result = evaluate(manifest, events)
        ids = [f['id'] for f in result['findings']]
        required = () if fid is None else (fid if isinstance(fid, tuple) else (fid,))
        mode_ok = ('structured_edit_mode' not in result) if mode == -1 else result.get('structured_edit_mode') == mode
        observations.append({'case': name, 'exit': code, 'ids': ids, 'mode': result.get('structured_edit_mode'),
                             'pass': code == expected and all(item in ids for item in required) and (expected != 0 or not ids) and mode_ok})
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations), 'v1_cases': len(cases), 'v2_cases': len(v2_cases), 'failed': failed, 'observations': observations}))
    return int(bool(failed))


def git_read(rev, path):
    proc = subprocess.run(['git', '--no-pager', '-C', str(ROOT), 'show', f'{rev}:{path}'], capture_output=True, env=_revision.clean_env(), timeout=30)
    if proc.returncode == 0:
        return proc.stdout
    check = subprocess.run(['git', '--literal-pathspecs', '-C', str(ROOT), 'ls-tree', '-z', rev, '--', path], capture_output=True, env=_revision.clean_env(), timeout=30)
    if check.returncode == 0 and not check.stdout:
        return None
    raise RuntimeError('committed read failed')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--revision')
    mode.add_argument('--selftest', action='store_true')
    parser.add_argument('--branch', default='master')
    parser.add_argument('--manifest', default='.ufo/waves/round-22/build/bindings.json')
    parser.add_argument('--events', default='.ufo/waves/round-22/build/events.json')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    if not all(repo_path(p) for p in (args.manifest, args.events)):
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'SCOPE-SCHEMA', 'site': 'input path'}]}))
        return 2
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, result = evaluate(git_read(binding.sha, args.manifest), git_read(binding.sha, args.events))
        result.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, result = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        code, result = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'SCOPE-READ', 'site': 'revision'}]}
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
