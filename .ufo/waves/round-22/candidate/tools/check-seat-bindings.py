#!/usr/bin/env python3
"""Audit recorded requests against frozen prompt scopes; not preventive enforcement."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path, PurePosixPath
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
    if selector:
        match = re.fullmatch(r'(.+?)(?::(?:raw|img|conflicts|[0-9]+(?:[-+][0-9]*)?|-[0-9]+|[0-9,-]+))*', value)
        if match:
            value = match[1]
    if not local(value):
        return value, 'SCOPE-PATH-DENIED'
    return value, None


def classify(tool, args, binding, depth=0):
    """Return finite post-hoc findings; never execute the requested operation."""
    if not isinstance(tool, str) or not tool or not isinstance(args, dict) or depth > 8:
        raise ValueError('malformed tool request or excessive wrapper nesting')
    if tool in ('multi_tool_use.parallel', 'parallel'):
        children = args.get('tool_uses')
        if not isinstance(children, list) or not children:
            raise ValueError('malformed parallel request')
        findings = []
        for child in children:
            if not isinstance(child, dict):
                raise ValueError('malformed parallel child')
            findings.extend(classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1))
        return findings
    if tool.startswith('functions.'):
        tool = tool[len('functions.'):]
    if tool in ('bash', 'eval', 'task'):
        return ['SCOPE-EXEC-DENIED']
    if tool in ('web_search', 'browser') or tool.startswith('browser.'):
        return ['SCOPE-FETCH-DENIED']
    if tool not in ('read', 'grep', 'glob', 'write'):
        return ['SCOPE-TOOL-UNKNOWN']
    value = args.get('path')
    if not isinstance(value, str) or not value:
        raise ValueError('missing explicit path')
    values = value.split(';') if tool in ('grep', 'glob') else [value]
    findings = []
    for value in values:
        path, denial = requested_path(value, selector=tool == 'read')
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
    try:
        data = json.loads(manifest, object_pairs_hook=unique) if isinstance(manifest, (str, bytes)) else manifest
        trace = json.loads(events, object_pairs_hook=unique) if isinstance(events, (str, bytes)) else events
        if not isinstance(data, dict) or data.get('schema') != 'tsukuroi-seat-bindings-v1' or not isinstance(data.get('seats'), list) or not data['seats']:
            raise ValueError('binding schema')
        bound = {}
        for seat in data['seats']:
            if not isinstance(seat, dict) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', seat.get('name', '')) or seat['name'] in bound or seat.get('root') != LANE or seat.get('commands') != [] or seat.get('fetches') != []:
                raise ValueError('binding identity/root/allowlist')
            for field in ('read_paths', 'write_paths'):
                paths = seat.get(field)
                if not isinstance(paths, list) or not paths or any(not local(p) and not (field == 'read_paths' and p == 'skill://godspeed') for p in paths) or len(paths) != len(set(paths)):
                    raise ValueError('binding paths')
            bound[seat['name']] = seat
        if not isinstance(trace, dict) or trace.get('schema') != 'tsukuroi-seat-events-v1' or not isinstance(trace.get('seats'), list):
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
                if not isinstance(event, dict):
                    raise ValueError('event shape')
                total += 1
                ids = classify(event.get('tool'), event.get('args'), binding)
                for fid in ids:
                    add(fid, f'{name}:{index}')
                    seat_findings.append(fid)
                violations += len(ids)
            rows.append({'name': name, 'agent': seat['agent'], 'requests': len(seat['events']), 'complete': seat['complete'], 'violations': seat_findings})
        code = 2 if incomplete else (1 if findings else 0)
    except (ValueError, TypeError, KeyError, AttributeError, UnicodeError):
        add('SCOPE-SCHEMA', 'input')
        code = 2
        bound = locals().get('bound', {})
    return code, {'status': ('PASS', 'FAIL', 'CANNOT_EVALUATE')[code], 'request_audit_mode': 1,
                  'seats_bound': len(bound), 'requests_total': total, 'violations': violations,
                  'incomplete_seats': incomplete, 'seats': rows, 'findings': findings, 'scope': SCOPE}


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
    observations = []
    for name, manifest, events, expected, fid in cases:
        code, result = evaluate(manifest, events)
        ids = [f['id'] for f in result['findings']]
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': code == expected and (fid is None or fid in ids)})
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(cases), 'failed': failed, 'observations': observations}))
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
