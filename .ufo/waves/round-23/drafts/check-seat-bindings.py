#!/usr/bin/env python3
"""Audit recorded requests against frozen prompt scopes; not preventive enforcement.

Schema tsukuroi-seat-bindings-v2 adds explicit predeclared structured-edit (``edit``)
target authority: the allow flag comes only from the validated top-level v2 schema,
edit targets must be exact members of a mandatory per-seat ``edit_paths`` list that is
a canonical subset of both ``read_paths`` and ``write_paths``, and structured-edit body
field values stay opaque (redacted by the collector, never interpreted). Schema v1
inputs keep their exact legacy classification and output shape.
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
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
SCOPE = 'Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness.'
V2_SCHEMA = 'tsukuroi-seat-bindings-v2'
EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'stream_content', 'i'},
               {'path', 'old_string', 'new_string'}, {'path', 'old_string', 'new_string', 'i'})


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
    """Return finite post-hoc findings; never execute the requested operation."""
    if not isinstance(tool, str) or not tool or depth > 8:
        raise ValueError('malformed tool name or excessive wrapper nesting')
    if tool.startswith('functions.'):
        tool = tool[len('functions.'):]
    # A known forbidden tool remains evidence even when its payload is missing.
    if tool in ('bash', 'eval', 'task'):
        return ['SCOPE-EXEC-DENIED']
    if tool in ('web_search', 'browser') or tool.startswith('browser.'):
        return ['SCOPE-FETCH-DENIED']
    if tool == 'edit':
        # Structured edits exist only under the validated top-level v2 schema flag;
        # no marker carried in a binding row or recorded event can enable them.
        if not allow_structured_edit:
            return ['SCOPE-TOOL-UNKNOWN']
        if not isinstance(args, dict):
            raise ValueError('malformed structured edit arguments')
        # Body field values (stream_content / old_string / new_string / i) are opaque:
        # presence and key shape only, never interpreted content or generic semantics.
        if set(args) not in EDIT_SHAPES:
            raise ValueError('malformed structured edit shape')
        target, denial = requested_path(args['path'])
        if denial:
            return [denial]
        # The exact target must be predeclared for edit AND hold read and write authority.
        if (target not in binding.get('edit_paths', ()) or target not in binding['read_paths']
                or target not in binding['write_paths']):
            return ['SCOPE-EDIT-DENIED']
        return []
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


def evaluate(manifest, events):
    findings, rows = [], []
    def add(fid, site):
        findings.append({'id': fid, 'site': site})
    if manifest is None:
        return 1, {'status': 'FAIL', 'request_audit_mode': 0, 'seats_bound': 0, 'requests_total': 0, 'findings': [{'id': 'SCOPE-BINDINGS-MISSING', 'site': 'manifest'}], 'scope': SCOPE}
    total = violations = incomplete = 0
    structured = False
    try:
        data = json.loads(manifest, object_pairs_hook=unique) if isinstance(manifest, (str, bytes)) else manifest
        structured = isinstance(data, dict) and data.get('schema') == V2_SCHEMA
        trace = json.loads(events, object_pairs_hook=unique) if isinstance(events, (str, bytes)) else events
        if not isinstance(data, dict) or set(data) != {'schema', 'seats'} or data.get('schema') not in ('tsukuroi-seat-bindings-v1', V2_SCHEMA) or not isinstance(data.get('seats'), list) or not data['seats']:
            raise ValueError('binding schema')
        bound = {}
        for seat in data['seats']:
            if not isinstance(seat, dict) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', seat.get('name', '')) or seat['name'] in bound or seat.get('root') != LANE or seat.get('commands') != [] or seat.get('fetches') != []:
                raise ValueError('binding identity/root/allowlist')
            for field in ('read_paths', 'write_paths'):
                paths = seat.get(field)
                if not isinstance(paths, list) or not paths or any(not local(p) and not (field == 'read_paths' and p == 'skill://godspeed') for p in paths) or len(paths) != len(set(paths)):
                    raise ValueError('binding paths')
            if structured:
                # Mandatory v2 edit authority: canonical spellings, exact subset of both
                # read_paths and write_paths. Extra v1-style fields never grant edits.
                edits = seat.get('edit_paths')
                if (not isinstance(edits, list) or any(not local(p) for p in edits) or len(edits) != len(set(edits))
                        or any(p not in seat['read_paths'] or p not in seat['write_paths'] for p in edits)):
                    raise ValueError('binding edit paths')
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
                    ids = classify(event.get('tool'), event.get('args'), binding, allow_structured_edit=structured)
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
    # structured_edit_mode exists only for v2 manifests: 1 when fully evaluated (0/1),
    # 0 on CANNOT_EVALUATE. v1/unsupported/missing keep the legacy shape (reads as 0).
    if structured:
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
    # v2 structured-edit fixtures: independent literal in-memory inputs with exact
    # expected exits, finding IDs and structured_edit_mode values (None = field absent).
    binding_v2 = {'schema': V2_SCHEMA, 'seats': [{'name': 'A', 'root': LANE, 'read_paths': [src, report], 'write_paths': [report], 'edit_paths': [report], 'commands': [], 'fetches': []}]}
    cases_v2 = []
    def case2(name, tool, args, code, fid=None, mode=1):
        cases_v2.append((name, binding_v2, trace(tool, args), code, fid, mode))
    case2('v2-stream-edit', 'edit', {'path': report, 'stream_content': 'x'}, 0)
    case2('v2-patch-edit', 'edit', {'path': report, 'old_string': 'a', 'new_string': 'b'}, 0)
    case2('v2-stream-edit-intent', 'edit', {'path': report, 'stream_content': 'x', 'i': 'rewrite report'}, 0)
    case2('v2-patch-edit-intent', 'edit', {'path': report, 'old_string': 'a', 'new_string': 'b', 'i': 'swap anchor'}, 0)
    case2('v2-qualified-edit', 'functions.edit', {'path': report, 'stream_content': 'x'}, 0)
    case2('v2-opaque-redacted-stream', 'edit', {'path': report, 'stream_content': {'redacted': True}}, 0)
    case2('v2-opaque-null-patch', 'edit', {'path': report, 'old_string': None, 'new_string': None}, 0)
    parallel_edit = {'recipient_name': 'edit', 'parameters': {'path': report, 'old_string': 'a', 'new_string': 'b'}}
    case2('v2-parallel-edit', 'multi_tool_use.parallel', {'tool_uses': [parallel_edit]}, 0)
    deep = parallel_edit
    for _ in range(2):
        deep = {'recipient_name': 'multi_tool_use.parallel', 'parameters': {'tool_uses': [deep]}}
    case2('v2-deep-parallel-edit', 'multi_tool_use.parallel', {'tool_uses': [deep]}, 0)
    case2('v2-edit-undeclared-target', 'edit', {'path': src, 'stream_content': 'x'}, 1, 'SCOPE-EDIT-DENIED')
    case2('v2-edit-prefix-spelling', 'edit', {'path': report + '.extra', 'stream_content': 'x'}, 1, 'SCOPE-EDIT-DENIED')
    case2('v2-edit-skill-target', 'edit', {'path': 'skill://godspeed', 'stream_content': 'x'}, 1, 'SCOPE-EDIT-DENIED')
    case2('v2-edit-dot-segment', 'edit', {'path': LANE + '/./report', 'stream_content': 'x'}, 1, 'SCOPE-PATH-DENIED')
    case2('v2-edit-traversal', 'edit', {'path': LANE + '/../sibling/report', 'stream_content': 'x'}, 1, 'SCOPE-PATH-DENIED')
    case2('v2-edit-internal-uri', 'edit', {'path': 'xd://tool', 'stream_content': 'x'}, 1, 'SCOPE-PATH-DENIED')
    case2('v2-edit-selector-spelling', 'edit', {'path': report + ':1-5', 'old_string': 'a', 'new_string': 'b'}, 1, 'SCOPE-PATH-DENIED')
    case2('v2-edit-external-url', 'edit', {'path': 'https://example.invalid', 'stream_content': 'x'}, 1, 'SCOPE-FETCH-DENIED')
    case2('v2-edit-unknown-key', 'edit', {'path': report, 'stream_content': 'x', 'replace_all': True}, 2, 'SCOPE-SCHEMA', 0)
    case2('v2-edit-mixed-shape', 'edit', {'path': report, 'stream_content': 'x', 'old_string': 'a'}, 2, 'SCOPE-SCHEMA', 0)
    case2('v2-edit-missing-replacement', 'edit', {'path': report, 'old_string': 'a'}, 2, 'SCOPE-SCHEMA', 0)
    case2('v2-edit-unstructured-target', 'edit', {'path': report}, 2, 'SCOPE-SCHEMA', 0)
    case2('v2-edit-nested-dict-path', 'edit', {'path': {'path': report}, 'stream_content': 'x'}, 2, 'SCOPE-SCHEMA', 0)
    case2('v2-parallel-edit-denied', 'multi_tool_use.parallel', {'tool_uses': [{'recipient_name': 'edit', 'parameters': {'path': src, 'stream_content': 'x'}}]}, 1, 'SCOPE-EDIT-DENIED')
    malformed_then_bash = trace(); malformed_then_bash['seats'][0]['events'] = [{'tool': 'edit', 'args': {'path': report}}, {'tool': 'bash', 'args': {}}]
    cases_v2.append(('v2-malformed-then-bash', binding_v2, malformed_then_bash, 2, ('SCOPE-SCHEMA', 'SCOPE-EXEC-DENIED'), 0))
    v2_incomplete = trace(); v2_incomplete['seats'][0]['complete'] = False
    cases_v2.append(('v2-incomplete-mode-zero', binding_v2, v2_incomplete, 2, 'SCOPE-TRACE-INCOMPLETE', 0))
    subset_read = copy.deepcopy(binding_v2); subset_read['seats'][0]['read_paths'] = [src]
    cases_v2.append(('v2-edit-paths-not-read-subset', subset_read, trace(), 2, 'SCOPE-SCHEMA', 0))
    subset_write = copy.deepcopy(binding_v2); subset_write['seats'][0]['write_paths'] = [src]
    cases_v2.append(('v2-edit-paths-not-write-subset', subset_write, trace(), 2, 'SCOPE-SCHEMA', 0))
    dup_edits = copy.deepcopy(binding_v2); dup_edits['seats'][0]['edit_paths'] = [report, report]
    cases_v2.append(('v2-edit-paths-duplicate', dup_edits, trace(), 2, 'SCOPE-SCHEMA', 0))
    nonlocal_edits = copy.deepcopy(binding_v2); nonlocal_edits['seats'][0]['edit_paths'] = [LANE + '/./report']
    cases_v2.append(('v2-edit-paths-nonlocal-spelling', nonlocal_edits, trace(), 2, 'SCOPE-SCHEMA', 0))
    missing_edits = copy.deepcopy(binding_v2); missing_edits['seats'][0].pop('edit_paths')
    cases_v2.append(('v2-edit-paths-missing-field', missing_edits, trace(), 2, 'SCOPE-SCHEMA', 0))
    no_edits = copy.deepcopy(binding_v2); no_edits['seats'][0]['edit_paths'] = []
    cases_v2.append(('v2-empty-edit-paths-denied', no_edits, trace('edit', {'path': report, 'stream_content': 'x'}), 1, 'SCOPE-EDIT-DENIED', 1))
    v3_manifest = {'schema': 'tsukuroi-seat-bindings-v3', 'seats': copy.deepcopy(binding_v2['seats'])}
    cases_v2.append(('v3-schema-unsupported', v3_manifest, trace(), 2, 'SCOPE-SCHEMA', None))
    cases_v2.append(('v2-missing-manifest-mode-absent', None, trace(), 1, 'SCOPE-BINDINGS-MISSING', None))
    v1_extra_edit = copy.deepcopy(binding); v1_extra_edit['seats'][0]['edit_paths'] = [report]
    cases_v2.append(('v1-extra-edit-field-no-grant', v1_extra_edit, trace('edit', {'path': report, 'old_string': 'a', 'new_string': 'b'}), 1, 'SCOPE-TOOL-UNKNOWN', None))
    v1_forged_marker = trace('edit', {'path': report, 'old_string': 'a', 'new_string': 'b', 'allow_structured_edit': True})
    cases_v2.append(('v1-forged-row-marker-no-grant', binding, v1_forged_marker, 1, 'SCOPE-TOOL-UNKNOWN', None))
    observations = []
    for name, manifest, events, expected, fid in cases:
        code, result = evaluate(manifest, events)
        ids = [f['id'] for f in result['findings']]
        required = () if fid is None else (fid if isinstance(fid, tuple) else (fid,))
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': code == expected and all(item in ids for item in required)})
    for name, manifest, events, expected, fid, expected_mode in cases_v2:
        code, result = evaluate(manifest, events)
        ids = [f['id'] for f in result['findings']]
        required = () if fid is None else (fid if isinstance(fid, tuple) else (fid,))
        mode = result.get('structured_edit_mode')
        observations.append({'case': name, 'exit': code, 'ids': ids, 'structured_edit_mode': mode,
                             'pass': code == expected and all(item in ids for item in required) and mode == expected_mode})
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(cases) + len(cases_v2), 'failed': failed, 'observations': observations}))
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
