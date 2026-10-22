#!/usr/bin/env python3
"""Per-cause report of the frozen round-23 falsify red cohort (claim C1, round 24).

Repairs the routed defects at corpus/lessons/round-23-verifier-spotcheck.md lines 52
and 64: every finding of the unchanged round-23 seat checker is attributed to a named
cause and to the recorded tool operation at its site, while the checker status, its
exit 2, the incomplete seat and the retained unknown extra key stay visible. Nothing
is re-graded: no grammar widening, no erased unknown key, no dropped seat, no dropped
finding. The author-written `schema_original_keys` list in
.ufo/waves/round-23/measure/post-falsify/falsify-limit.json is labelled as author
recollection for every name that is absent from the retained events.

Usage (from the lane root, after this file is installed as tools/report-red-causes.py):

    python3 tools/report-red-causes.py --revision <REV>
    python3 tools/report-red-causes.py --selftest

Scope: arithmetic over committed round-23 bytes only. Not runtime prevention, not a
no-harm proof, not a claim about what any seat actually did.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

CHECKER = 'tools/check-seat-bindings.py'
REVISION_TOOL = 'tools/_revision.py'
MANIFEST = '.ufo/waves/round-23/falsify/bindings.json'
EVENTS = '.ufo/waves/round-23/falsify/events.json'
LIMIT = '.ufo/waves/round-23/measure/post-falsify/falsify-limit.json'
UNKNOWN_TOKEN = '__unknown_argument__'
LABEL = 'author recollection, not recoverable from retained events'
SEAT_LEVEL = 'seat-level trace state (no recorded request at this site)'
SCOPE = ('Attribution of the frozen round-23 seat-checker findings to a named cause and '
         'to the recorded tool operation at each site; not runtime prevention, not effect '
         'proof, not a no-harm certificate, not a claim about what any seat did.')

# Request argument keys accepted by the frozen checker, copied from
# tools/check-seat-bindings.py at revision 674891dfbcb853432a863a6eb82e7b2a9bdb3958
# (the `allowed_keys` table inside classify()).  A key outside this table is the
# retained unknown extra key.
ALLOWED_KEYS = {
    'read': frozenset({'i', 'path'}),
    'grep': frozenset({'i', 'pattern', 'path', 'case', 'gitignore', 'skip'}),
    'glob': frozenset({'i', 'path', 'hidden', 'gitignore', 'limit'}),
    'write': frozenset({'i', 'path', 'content'}),
}
# The v2 structured-edit shapes of the frozen checker (EDIT_SHAPES plus the optional
# `i`).  A v1 manifest never reaches classify_edit: `edit` is then an unknown tool.
EDIT_KEYS_V2 = frozenset({'i', 'path', 'stream_content', 'old_string', 'new_string'})


def allowed_keys(manifest):
    """The request argument keys the frozen checker accepts, per tool, for this manifest."""
    table = {tool: frozenset(keys) for tool, keys in ALLOWED_KEYS.items()}
    schema = manifest.get('schema') if isinstance(manifest, dict) else None
    table['edit'] = EDIT_KEYS_V2 if schema == 'tsukuroi-seat-bindings-v2' else frozenset()
    return table

# The numeric suffix of a checker site is the ordinal of the recorded request inside
# that seat's `events` list (the frozen checker emits f'{name}:{index}' where index is
# the enumerate() position over seat['events']).  `request_line` is a different field:
# the transcript line on which the request was issued.  The join therefore keys on the
# request ordinal and reports the request_line of the joined event; a site whose
# ordinal is out of range falls back to a unique event whose request_line equals the
# site number, and a site that matches neither stays unattributed.
CROSS_DRIVER = '''import importlib.util, json, sys
tmp = sys.argv[1]
sys.path.insert(0, tmp)
spec = importlib.util.spec_from_file_location("frozen_check_seat_bindings", tmp + "/check-seat-bindings.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with open(sys.argv[2], "rb") as handle:
    manifest = handle.read()
with open(sys.argv[3], "rb") as handle:
    events = handle.read()
code, result = module.evaluate(manifest, events)
print(json.dumps({"exit": code, "result": result}, sort_keys=True))
'''


class ReportError(Exception):
    """A finding id, a site and a detail for one read or shape failure."""


def unique(pairs):
    """Reject duplicate JSON keys instead of silently keeping the last one."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def find_root():
    """The lane root: the ancestor that holds tools/_revision.py and .ufo/waves."""
    seen, candidates = set(), []
    here = Path(__file__).resolve()
    candidates.extend(here.parents)
    cwd = Path.cwd().resolve()
    candidates.append(cwd)
    candidates.extend(cwd.parents)
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if (candidate / REVISION_TOOL).is_file() and (candidate / '.ufo' / 'waves').is_dir():
            return candidate
    raise ReportError('E-ROOT-NOT-FOUND', 'root', 'no ancestor of %s holds %s and .ufo/waves'
                      % (here, REVISION_TOOL))


def load_revision_tool(root):
    """Import tools/_revision.py from the lane root (the shared landed-revision binder)."""
    path = root / 'tools' / '_revision.py'
    spec = importlib.util.spec_from_file_location('tsukuroi_revision_tool', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git_blob(root, sha, path, env):
    """Read one committed blob at `sha`; never the working tree."""
    proc = subprocess.run(['git', '--no-pager', '-C', str(root), 'show', f'{sha}:{path}'],
                          capture_output=True, env=env, timeout=60)
    if proc.returncode != 0:
        raise ReportError('E-COMMITTED-READ', path, 'git show exited %d' % proc.returncode)
    return proc.stdout


def run_checker_cli(root, sha, env):
    """The recorded command: python3 tools/check-seat-bindings.py --revision <sha> ... ."""
    cmd = [sys.executable, CHECKER, '--revision', sha, '--manifest', MANIFEST, '--events', EVENTS]
    proc = subprocess.run(cmd, cwd=str(root), capture_output=True, env=env, timeout=600)
    entry = {'command': ['python3', CHECKER, '--revision', sha, '--manifest', MANIFEST, '--events', EVENTS],
             'exit': proc.returncode, 'stderr': proc.stderr.decode('utf-8', 'replace')[:400]}
    try:
        entry['result'] = json.loads(proc.stdout.decode('utf-8', 'replace'))
    except ValueError:
        entry['result'] = None
        entry['error'] = 'checker stdout is not JSON'
    return entry


def run_checker_from_revision(root, checker_bytes, revision_bytes, manifest_bytes, events_bytes, env):
    """Evaluate the revision's own checker bytes over the revision's own inputs."""
    with tempfile.TemporaryDirectory(prefix='red-causes-') as tmp:
        tmp_path = Path(tmp)
        (tmp_path / 'check-seat-bindings.py').write_bytes(checker_bytes)
        (tmp_path / '_revision.py').write_bytes(revision_bytes)
        (tmp_path / 'manifest.json').write_bytes(manifest_bytes)
        (tmp_path / 'events.json').write_bytes(events_bytes)
        (tmp_path / 'driver.py').write_text(CROSS_DRIVER, encoding='utf-8')
        proc = subprocess.run([sys.executable, str(tmp_path / 'driver.py'), tmp,
                               str(tmp_path / 'manifest.json'), str(tmp_path / 'events.json')],
                              cwd=str(root), capture_output=True, env=env, timeout=600)
        entry = {'exit': proc.returncode, 'stderr': proc.stderr.decode('utf-8', 'replace')[:400]}
        try:
            payload = json.loads(proc.stdout.decode('utf-8', 'replace'))
            entry['exit'] = payload.get('exit')
            entry['result'] = payload.get('result')
        except ValueError:
            entry['result'] = None
            entry['error'] = 'revision checker stdout is not JSON'
        return entry


def native_completed_flag(limit, seats):
    """The native-completed flag for an incomplete seat, when it is derivable."""
    total = limit.get('native_completed') if isinstance(limit, dict) else None
    traced = len(seats)
    if isinstance(total, int) and total == traced:
        return True, ('falsify-limit.json native_completed=%d equals the %d traced seats, so this seat '
                      'is inside the natively completed cohort' % (total, traced))
    return None, ('not derivable: falsify-limit.json native_completed=%r against %d traced seats; the '
                  'per-seat native exit line is not retained in the trace' % (total, traced))


def attribute(result, trace, limit, cross=None, exit_code=None, manifest=None, allowed=None):
    """Pure attribution step; the selftest drives it with literal fixtures."""
    allowed = allowed_keys(manifest) if allowed is None else allowed
    findings = list(result.get('findings') or [])
    seats = {seat['name']: seat for seat in (trace.get('seats') or [])
             if isinstance(seat, dict) and isinstance(seat.get('name'), str)}
    retained_keys = set()
    for seat in seats.values():
        for event in seat.get('events') or []:
            if isinstance(event, dict) and isinstance(event.get('args'), dict):
                retained_keys.update(event['args'].keys())

    causes = collections.Counter()
    cause_seats = collections.defaultdict(set)
    attributed, unattributed, unknown_sites, sites = 0, [], [], []
    for finding in findings:
        fid = finding.get('id')
        site = finding.get('site') or ''
        name, sep, number = site.rpartition(':')
        event, join = None, None
        if sep and name in seats and number.isdigit():
            recorded = seats[name].get('events') or []
            ordinal = int(number)
            if 0 <= ordinal < len(recorded):
                event, join = recorded[ordinal], 'event_ordinal'
            else:
                matches = [item for item in recorded
                           if isinstance(item, dict) and item.get('request_line') == ordinal]
                if len(matches) == 1:
                    event, join = matches[0], 'request_line'
        if event is not None:
            operation = event.get('tool')
            if not isinstance(operation, str) or not operation:
                unattributed.append(finding)
                continue
            seat_name, request_line = name, event.get('request_line')
        elif fid in ('SCOPE-TRACE-INCOMPLETE', 'SCOPE-TRACE-MISSING') and site:
            operation, seat_name, request_line, join = SEAT_LEVEL, site, None, 'seat_level'
        else:
            unattributed.append(finding)
            continue
        attributed += 1
        causes[(fid, operation)] += 1
        cause_seats[(fid, operation)].add(seat_name)
        sites.append({'finding': fid, 'site': site, 'seat': seat_name, 'operation': operation,
                      'join': join, 'request_line': request_line})
        if fid == 'SCOPE-SCHEMA':
            args = event.get('args') if isinstance(event, dict) else None
            args = args if isinstance(args, dict) else {}
            unknown = sorted(set(args) - set(allowed.get(operation, frozenset())))
            unknown_sites.append({
                'site': site, 'finding': fid, 'seat': seat_name, 'operation': operation,
                'retained_key_token': unknown[0] if len(unknown) == 1 else None,
                'retained_unknown_tokens': unknown, 'retained_keys': sorted(args),
                'request_line': request_line, 'join': join})

    total = len(findings)
    trace_incomplete = sorted(name for name, seat in seats.items() if seat.get('complete') is False)
    native, native_basis = native_completed_flag(limit, seats)
    incomplete = []
    for name in trace_incomplete:
        seat = seats[name]
        terminal = seat.get('terminal_evidence') or {}
        incomplete.append({
            'name': name, 'trace_complete': False, 'native_completed': native,
            'native_completed_basis': native_basis,
            'native_terminal_evidence': {'session_exit_line': terminal.get('session_exit_line'),
                                         'native_failure': terminal.get('native_failure')},
            'recorded_requests': len(seat.get('events') or [])})

    names = limit.get('schema_original_keys') if isinstance(limit, dict) else None
    recollection = []
    for key in names if isinstance(names, list) else []:
        present = key in retained_keys
        recollection.append({'name': key, 'in_retained_events': present,
                             'label': None if present else LABEL})

    reported_incomplete = sorted(item['name'] for item in incomplete)
    checker_incomplete = result.get('present_incomplete_seats')
    incomplete_findings = sorted(finding.get('site') for finding in findings
                                 if finding.get('id') == 'SCOPE-TRACE-INCOMPLETE')
    cross_findings = cross.get('findings') if isinstance(cross, dict) else None
    cross_ok = (cross_findings is not None and list(cross_findings) == findings
                and cross.get('exit') == exit_code)
    per_seat = collections.Counter()
    for row in sites:
        if row['join'] in ('event_ordinal', 'request_line'):
            per_seat[row['seat']] += 1
    reconciliation = True
    rows = result.get('seats') or []
    for row in rows:
        name = row.get('name')
        seat = seats.get(name)
        if seat is None:
            continue
        if row.get('requests') != len(seat.get('events') or []):
            reconciliation = False
        if len(row.get('violations') or []) != per_seat.get(name, 0):
            reconciliation = False

    checks = {
        'all_findings_attributed': total > 0 and attributed == total and not unattributed,
        'checker_exit_is_2': exit_code == 2,
        'checker_status_cannot_evaluate': result.get('status') == 'CANNOT_EVALUATE',
        'incomplete_seat_preserved': (bool(reported_incomplete)
                                      and reported_incomplete == trace_incomplete
                                      and checker_incomplete == len(trace_incomplete)
                                      and incomplete_findings == trace_incomplete),
        'unknown_key_visible': (bool(unknown_sites)
                                and all(item['retained_key_token'] == UNKNOWN_TOKEN for item in unknown_sites)
                                and UNKNOWN_TOKEN in retained_keys),
        'recollection_labelled': (all(item['label'] == LABEL for item in recollection
                                      if not item['in_retained_events'])
                                  and all(item['label'] is None for item in recollection
                                          if item['in_retained_events'])),
        'recollection_names_absent_from_events': all(
            item['name'] not in retained_keys for item in recollection
            if item['label'] == LABEL),
        'cross_check_identical': cross_ok,
        'seat_reconciliation': bool(rows) and reconciliation,
    }
    preserved = all(checks.values())
    report = {
        'checker_status': result.get('status'),
        'checker_exit': exit_code,
        'total_findings': total,
        'attributed_findings': attributed,
        'unattributed': unattributed,
        'causes': [{'finding': fid, 'operation': operation, 'count': count,
                    'seats': sorted(cause_seats[(fid, operation)]),
                    'seat_count': len(cause_seats[(fid, operation)])}
                   for (fid, operation), count in sorted(causes.items())],
        'incomplete_seats': incomplete,
        'unknown_argument_sites': unknown_sites,
        'schema_original_keys': recollection,
        'retained_argument_keys': sorted(retained_keys),
        'sites': sites,
        'checks': checks,
        'preserved': preserved,
        'scope': SCOPE,
    }
    return (0 if preserved else 1), report


def run(revision, branch):
    root = find_root()
    revision_tool = load_revision_tool(root)
    env = revision_tool.clean_env()
    binding = revision_tool.bind(root, revision, branch)
    sha = binding.sha
    checker_bytes = git_blob(root, sha, CHECKER, env)
    revision_bytes = git_blob(root, sha, REVISION_TOOL, env)
    manifest_bytes = git_blob(root, sha, MANIFEST, env)
    events_bytes = git_blob(root, sha, EVENTS, env)
    limit_bytes = git_blob(root, sha, LIMIT, env)
    cli = run_checker_cli(root, sha, env)
    revision_run = run_checker_from_revision(root, checker_bytes, revision_bytes,
                                             manifest_bytes, events_bytes, env)
    if cli.get('result') is not None:
        primary, primary_exit = cli['result'], cli.get('exit')
        cross = {'exit': revision_run.get('exit'),
                 'findings': (revision_run.get('result') or {}).get('findings')}
    else:
        primary, primary_exit = revision_run.get('result'), revision_run.get('exit')
        cross = None
    if primary is None:
        raise ReportError('E-CHECKER-UNREADABLE', CHECKER, 'neither the recorded command nor the '
                          'revision checker produced JSON')
    trace = json.loads(events_bytes.decode('utf-8'), object_pairs_hook=unique)
    limit = json.loads(limit_bytes.decode('utf-8'), object_pairs_hook=unique)
    manifest = json.loads(manifest_bytes.decode('utf-8'), object_pairs_hook=unique)
    status, report = attribute(primary, trace, limit, cross=cross, exit_code=primary_exit,
                                manifest=manifest)
    working_checker = root / CHECKER
    report.update({
        'revision': sha,
        'branch': binding.branch,
        'requested_revision': revision,
        'checker_command': cli['command'],
        'checker_runs': {
            'recorded_command': {'exit': cli.get('exit'), 'status': (cli.get('result') or {}).get('status'),
                                 'error': cli.get('error'), 'stderr': cli.get('stderr', '')},
            'revision_bytes': {'exit': revision_run.get('exit'),
                               'status': (revision_run.get('result') or {}).get('status'),
                               'error': revision_run.get('error'),
                               'stderr': revision_run.get('stderr', '')},
            'working_tree_checker_matches_revision_bytes':
                working_checker.is_file() and working_checker.read_bytes() == checker_bytes,
        },
        'inputs': {path: hashlib.sha256(blob).hexdigest() for path, blob in (
            (CHECKER, checker_bytes), (REVISION_TOOL, revision_bytes), (MANIFEST, manifest_bytes),
            (EVENTS, events_bytes), (LIMIT, limit_bytes))},
    })
    return status, report


def selftest():
    """Literal fixtures only; the selftest never touches the repository."""
    def trace(complete=True, schema_keys=('i', 'new_string', 'old_string', 'path', UNKNOWN_TOKEN)):
        return {'schema': 'tsukuroi-seat-events-v1', 'seats': [
            {'name': 'SeatA', 'agent': 'agent-a', 'complete': True, 'events': [
                {'tool': 'read', 'args': {'i': None, 'path': '/lane/x'}, 'request_line': 10},
                {'tool': 'edit', 'args': {key: None for key in schema_keys}, 'request_line': 20}]},
            {'name': 'SeatB', 'agent': 'agent-b', 'complete': complete,
             'terminal_evidence': {'session_exit_line': None, 'native_failure': None},
             'events': [{'tool': 'write', 'args': {'i': None, 'path': '/lane/y', 'content': 'z'},
                         'request_line': 30}]}]}

    def result(findings, status='CANNOT_EVALUATE', present_incomplete=1):
        rows = [{'name': 'SeatA', 'agent': 'agent-a', 'requests': 2, 'complete': True,
                 'violations': ['SCOPE-PATH-DENIED', 'SCOPE-SCHEMA']},
                {'name': 'SeatB', 'agent': 'agent-b', 'requests': 1, 'complete': False,
                 'violations': ['SCOPE-PATH-DENIED']}]
        return {'status': status, 'findings': [{'id': fid, 'site': site} for fid, site in findings],
                'seats': rows, 'incomplete_seats': present_incomplete,
                'present_incomplete_seats': present_incomplete}

    base = [('SCOPE-PATH-DENIED', 'SeatA:0'), ('SCOPE-SCHEMA', 'SeatA:1'),
            ('SCOPE-TRACE-INCOMPLETE', 'SeatB'), ('SCOPE-PATH-DENIED', 'SeatB:0')]
    limit = {'schema_original_keys': ['i', 'new_string', 'old_string', 'path', 'replace_all'],
             'native_completed': 2}
    cases = [
        # name, exit code, result, trace, limit, cross findings, expected status
        ('pristine', 2, result(base), trace(False), limit, base, 0),
        ('finding-dropped', 2, result(base[:-1]), trace(False), limit, base, 1),
        ('finding-dropped-from-cross-check', 2, result(base), trace(False), limit, base[:-1], 1),
        ('incomplete-seat-dropped', 2, result([item for item in base
                                               if item[0] != 'SCOPE-TRACE-INCOMPLETE'],
                                              present_incomplete=0),
         trace(False), limit, base, 1),
        ('unknown-key-renamed', 2, result(base),
         trace(False, ('i', 'new_string', 'old_string', 'path', 'replace_all')), limit, base, 1),
        ('unknown-key-erased', 2, result(base),
         trace(False, ('i', 'new_string', 'old_string', 'path')), limit, base, 1),
        ('site-out-of-range', 2, result(base + [('SCOPE-PATH-DENIED', 'SeatA:9')]),
         trace(False), limit, base + [('SCOPE-PATH-DENIED', 'SeatA:9')], 1),
        ('site-unknown-seat', 2, result(base + [('SCOPE-PATH-DENIED', 'SeatZ:0')]),
         trace(False), limit, base + [('SCOPE-PATH-DENIED', 'SeatZ:0')], 1),
        ('site-not-a-request', 2, result(base + [('SCOPE-SCHEMA', 'input')]),
         trace(False), limit, base + [('SCOPE-SCHEMA', 'input')], 1),
        ('checker-status-changed', 2, result(base, status='FAIL'), trace(False), limit, base, 1),
        ('checker-exit-changed', 1, result(base), trace(False), limit, base, 1),
        ('no-schema-site', 2, result([item for item in base if item[0] != 'SCOPE-SCHEMA']),
         trace(False), limit, [item for item in base if item[0] != 'SCOPE-SCHEMA'], 1),
        ('empty-findings', 2, result([]), trace(False), limit, [], 1),
    ]
    observations = []
    manifest = {'schema': 'tsukuroi-seat-bindings-v2', 'seats': []}
    for name, code, res, tr, lim, cross_findings, want in cases:
        got, report = attribute(res, tr, lim, manifest=manifest,
                                cross={'exit': code, 'findings': [{'id': fid, 'site': site}
                                                                  for fid, site in cross_findings]},
                                exit_code=code)
        failed_checks = sorted(key for key, value in report['checks'].items() if not value)
        observations.append({'case': name, 'want': want, 'got': got, 'pass': got == want,
                             'failed_checks': failed_checks,
                             'unattributed': len(report['unattributed']),
                             'incomplete_seats': [item['name'] for item in report['incomplete_seats']],
                             'unknown_tokens': [item['retained_unknown_tokens']
                                                for item in report['unknown_argument_sites']]})
    # The recollection label is part of the contract, checked on its own.
    _, labelled = attribute(result(base), trace(False), limit, manifest=manifest,
                             cross={'exit': 2, 'findings': [{'id': fid, 'site': site}
                                                            for fid, site in base]}, exit_code=2)
    labels = {item['name']: item['label'] for item in labelled['schema_original_keys']}
    label_ok = (labels.get('replace_all') == LABEL
                and all(labels.get(name) is None for name in ('i', 'new_string', 'old_string', 'path')))
    observations.append({'case': 'recollection-label', 'want': 0, 'got': 0 if label_ok else 1,
                         'pass': label_ok, 'failed_checks': [] if label_ok else ['recollection_labelled'],
                         'unattributed': 0, 'incomplete_seats': ['SeatB'], 'unknown_tokens': []})
    failed = sum(not item['pass'] for item in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations),
                      'failed': failed, 'observations': observations}, sort_keys=True))
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
        status, report = run(args.revision, args.branch)
    except Exception as exc:  # noqa: BLE001 - one finding id per failure, never a traceback
        fid = getattr(exc, 'fid', 'E-REPORT-FAILED')
        site = getattr(exc, 'site', 'report')
        detail = str(exc)[:200]
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'preserved': False,
                          'findings': [{'id': fid, 'site': site, 'detail': detail}]}))
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return status


if __name__ == '__main__':
    sys.exit(main())
