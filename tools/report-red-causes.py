#!/usr/bin/env python3
"""Per-cause report of the frozen round-23 falsify red cohort.

Repairs the routed defects at corpus/lessons/round-23-verifier-spotcheck.md
lines 52 and 64: every finding of the unchanged round-23 seat checker is
attributed to its cause and to the recorded tool operation at its site, while
the checker status, its exit 2, the incomplete seat and the unknown extra key
stay visible. Nothing is re-graded: no grammar widening, no erased unknown key,
no dropped seat. The author-written `schema_original_keys` list is labelled as
author recollection wherever a name is absent from the retained events.

Scope: arithmetic over committed round-23 bytes only. Not runtime prevention,
not a no-harm proof, not a claim about what any seat actually did.
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
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import _revision  # noqa: E402

CHECKER = 'tools/check-seat-bindings.py'
MANIFEST = '.ufo/waves/round-23/falsify/bindings.json'
EVENTS = '.ufo/waves/round-23/falsify/events.json'
LIMIT = '.ufo/waves/round-23/measure/post-falsify/falsify-limit.json'
UNKNOWN = '__unknown_argument__'
LABEL = 'author recollection, not recoverable from retained events'
SCOPE = ('Attribution of recorded round-23 checker findings to cause and tool operation; '
         'not runtime prevention, effect proof or a no-harm certificate.')


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def git_blob(sha, path):
    proc = subprocess.run(['git', '--no-pager', '-C', str(ROOT), 'show', f'{sha}:{path}'],
                          capture_output=True, env=_revision.clean_env(), timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(f'committed read failed: {path}')
    return proc.stdout


def load_checker(expected_bytes):
    path = ROOT / CHECKER
    if path.read_bytes() != expected_bytes:
        raise RuntimeError('working-tree checker differs from the revision blob')
    spec = importlib.util.spec_from_file_location('check_seat_bindings', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arg_keys(args):
    return sorted(args) if isinstance(args, dict) else []


def attribute(code, result, trace, limit):
    """Pure attribution step; selftest drives it with literal fixtures."""
    seats = {s['name']: s for s in trace.get('seats', []) if isinstance(s, dict) and 'name' in s}
    rows = collections.Counter()
    row_seats = collections.defaultdict(set)
    attributed, unattributed, unknown_sites = 0, [], []
    for finding in result.get('findings', []):
        fid, site = finding.get('id'), finding.get('site', '')
        name, sep, index = site.rpartition(':')
        if sep and name in seats and index.isdigit() and int(index) < len(seats[name]['events']):
            event = seats[name]['events'][int(index)]
            operation = event.get('tool') if isinstance(event, dict) else None
            if not isinstance(operation, str) or not operation:
                unattributed.append(finding)
                continue
            if fid == 'SCOPE-SCHEMA':
                keys = arg_keys(event.get('args'))
                unknown_sites.append({'site': site, 'operation': operation, 'retained_keys': keys,
                                      'unknown_tokens': keys.count(UNKNOWN)})
            seat = name
        elif fid in ('SCOPE-TRACE-INCOMPLETE', 'SCOPE-TRACE-MISSING') and not sep and site:
            operation, seat = 'seat-level trace state', site
        else:
            unattributed.append(finding)
            continue
        attributed += 1
        rows[(fid, operation)] += 1
        row_seats[(fid, operation)].add(seat)
    incomplete = [{'name': n, 'trace_complete': False, 'events': len(s['events'])}
                  for n, s in sorted(seats.items()) if s.get('complete') is False]
    retained_names = set()
    for seat in seats.values():
        for event in seat['events']:
            if isinstance(event, dict):
                retained_names.update(arg_keys(event.get('args')))
    recollection = []
    if isinstance(limit, dict) and isinstance(limit.get('schema_original_keys'), list):
        for key in limit['schema_original_keys']:
            recollection.append({'name': key, 'in_retained_events': key in retained_names,
                                 'label': None if key in retained_names else LABEL})
    total = len(result.get('findings', []))
    report = {
        'checker_status': result.get('status'), 'checker_exit': code,
        'total_findings': total, 'attributed_findings': attributed, 'unattributed': unattributed,
        'causes': [{'finding': f, 'operation': o, 'count': c, 'seats': len(row_seats[(f, o)])}
                   for (f, o), c in sorted(rows.items())],
        'incomplete_seats': incomplete, 'unknown_argument_sites': unknown_sites,
        'schema_original_keys': recollection, 'scope': SCOPE,
    }
    ok = (total > 0 and attributed == total and not unattributed and code == 2
          and result.get('status') == 'CANNOT_EVALUATE' and bool(incomplete)
          and all(s['unknown_tokens'] > 0 for s in unknown_sites) and bool(unknown_sites)
          and all(r['in_retained_events'] or r['label'] == LABEL for r in recollection))
    report['preserved'] = ok
    return (0 if ok else 1), report


def run(revision, branch):
    binding = _revision.bind(ROOT, revision, branch)
    checker = load_checker(git_blob(binding.sha, CHECKER))
    manifest, events = git_blob(binding.sha, MANIFEST), git_blob(binding.sha, EVENTS)
    code, result = checker.evaluate(manifest, events)
    trace = json.loads(events, object_pairs_hook=unique)
    limit = json.loads(git_blob(binding.sha, LIMIT), object_pairs_hook=unique)
    status, report = attribute(code, result, trace, limit)
    report.update(revision=binding.sha, branch=binding.branch,
                  inputs={p: hashlib.sha256(git_blob(binding.sha, p)).hexdigest()
                          for p in (CHECKER, MANIFEST, EVENTS, LIMIT)})
    return status, report


def selftest():
    def trace(complete=True, keys=('i', 'new_string', 'old_string', 'path', UNKNOWN)):
        return {'schema': 'tsukuroi-seat-events-v1', 'seats': [
            {'name': 'A', 'agent': 'a', 'complete': True, 'events': [
                {'tool': 'read', 'args': {'path': '/x'}}, {'tool': 'edit', 'args': {k: None for k in keys}}]},
            {'name': 'B', 'agent': 'b', 'complete': complete, 'events': [{'tool': 'write', 'args': {'path': '/y'}}]}]}
    def result(findings, status='CANNOT_EVALUATE'):
        return {'status': status, 'findings': [{'id': i, 'site': s} for i, s in findings]}
    base = [('SCOPE-PATH-DENIED', 'A:0'), ('SCOPE-SCHEMA', 'A:1'), ('SCOPE-TRACE-INCOMPLETE', 'B'),
            ('SCOPE-PATH-DENIED', 'B:0')]
    limit = {'schema_original_keys': ['i', 'new_string', 'old_string', 'path', 'replace_all']}
    cases = [
        ('pristine', 2, result(base), trace(False), limit, 0),
        ('site-out-of-range', 2, result(base + [('SCOPE-PATH-DENIED', 'A:9')]), trace(False), limit, 1),
        ('unknown-seat-site', 2, result(base + [('SCOPE-PATH-DENIED', 'Z:0')]), trace(False), limit, 1),
        ('incomplete-seat-dropped', 2, result(base), trace(True), limit, 1),
        ('unknown-key-renamed', 2, result(base), trace(False, ('i', 'new_string', 'old_string', 'path', 'replace_all')),
         {'schema_original_keys': ['i', 'new_string', 'old_string', 'path', 'replace_all', 'other']}, 1),
        ('checker-exit-changed', 1, result(base, 'FAIL'), trace(False), limit, 1),
        ('status-relabelled', 2, result(base, 'FAIL'), trace(False), limit, 1),
        ('no-schema-site', 2, result([f for f in base if f[0] != 'SCOPE-SCHEMA']), trace(False), limit, 1),
        ('empty-findings', 2, result([]), trace(False), limit, 1),
    ]
    obs = []
    for name, code, res, tr, lim, want in cases:
        got, rep = attribute(code, res, tr, lim)
        label_ok = name != 'pristine' or [r['label'] for r in rep['schema_original_keys']] == [None] * 4 + [LABEL]
        obs.append({'case': name, 'want': want, 'got': got, 'pass': got == want and label_ok})
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
        status, report = run(args.revision, args.branch)
    except _revision.RevisionError as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}))
        return 2
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'RED-CAUSES-READ', 'site': str(exc)}]}))
        return 2
    print(json.dumps(report, sort_keys=True))
    return status


if __name__ == '__main__':
    sys.exit(main())
