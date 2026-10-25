#!/usr/bin/env python3
"""Per-cause report of the frozen round-23 falsify red cohort.

Repairs the routed defects at corpus/lessons/round-23-verifier-spotcheck.md
lines 52 and 64: every finding of the unchanged round-23 seat checker is
attributed to its cause and to the recorded tool operation at its site, while
the checker status, its exit 2, the incomplete seat and the unknown extra key
stay visible. Nothing is re-graded: no grammar widening, no erased unknown key,
no dropped seat. The author-written `schema_original_keys` list is labelled as
author recollection wherever a name is absent from the flagged site's retained
event (the only event that could show the key at that site).

Scope: arithmetic over committed round-23 bytes only. Not runtime prevention,
not a no-harm proof, not a claim about what any seat actually did.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import os
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
PINS = {
    CHECKER: '35079db51368105b8392aa0c664ba794485639d14950258d0a2892909d83d880',
    MANIFEST: '8c72460bf7561c655dde1dacbcd5bf064cd04963c293a2a5b83ca16c5ffa9044',
    EVENTS: '52a5021bb18647ca868d0814d933dd899f29cdb0a44d2cc78605ee2e38b62b83',
    LIMIT: 'e8e22aaef63f1a99209bec211ece1b906eb754be006cba1d03cd8e6bf026f1db',
}
EXPECTED = {'SCOPE-PATH-DENIED': 266, 'SCOPE-SCHEMA': 1, 'SCOPE-TRACE-INCOMPLETE': 1}
SELF = 'tools/report-red-causes.py'
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


def path_subcause(checker, tool, args, seat_binding):
    """Name the checker branch behind one SCOPE-PATH-DENIED, from frozen bytes only."""
    if not isinstance(args, dict) or not isinstance(args.get('path'), str):
        return 'path argument not a string'
    values = args['path'].split(';') if tool in ('grep', 'glob') else [args['path']]
    for value in values:
        try:
            path, denial = checker.requested_path(value, selector=tool in ('read', 'grep'))
        except ValueError:
            return 'path argument not a string'
        if denial == 'SCOPE-PATH-DENIED':
            if not value.startswith(checker.LANE + '/'):
                if value == 'redacted-internal-uri':
                    return 'collector redaction placeholder; target not recorded'
                if '://' in value:
                    return 'non-file URI'
                if not value.startswith('/'):
                    return 'relative path'
                if os.path.normpath(value).startswith(checker.LANE + '/'):
                    return 'dot segments lexically normalise inside the lane; no filesystem resolution claimed'
                return 'outside the lane root'
            base = value.split('?', 1)[0].split(':', 1)[0]
            declared = base in seat_binding['read_paths'] or base in seat_binding['write_paths']
            return ('inside the lane, spelled outside the frozen grammar, base path declared' if declared
                    else 'inside the lane, spelled outside the frozen grammar, base path undeclared')
        if denial is None and path not in seat_binding['write_paths' if tool == 'write' else 'read_paths']:
            other = seat_binding['read_paths' if tool == 'write' else 'write_paths']
            return ('declared for the other operation only' if path in other
                    else 'inside the lane, well formed, not bound to the seat')
    return 'no denied component found'


def attribute(code, result, trace, limit, manifest=None, checker=None):
    """Pure attribution step; selftest drives it with literal fixtures."""
    seats = {s['name']: s for s in trace.get('seats', []) if isinstance(s, dict) and 'name' in s}
    bindings = {b['name']: b for b in (manifest or {}).get('seats', []) if isinstance(b, dict) and 'name' in b}
    v2 = isinstance(manifest, dict) and manifest.get('schema') == 'tsukuroi-seat-bindings-v2'
    rows = collections.Counter()
    row_seats = collections.defaultdict(set)
    attributed, unattributed, unknown_sites, per_finding = 0, [], [], []
    with_operation = seat_level = reclassify_mismatch = 0
    for finding in result.get('findings', []):
        fid, site = finding.get('id'), finding.get('site', '')
        name, sep, index = site.rpartition(':')
        if sep and name in seats and index.isdigit() and int(index) < len(seats[name]['events']):
            event = seats[name]['events'][int(index)]
            operation = event.get('tool') if isinstance(event, dict) else None
            if not isinstance(operation, str) or not operation:
                unattributed.append(finding)
                continue
            subcause = fid
            if checker is not None and name in bindings:
                try:
                    ids = checker.classify(operation, event.get('args'), bindings[name], allow_structured_edit=v2)
                except (ValueError, TypeError, KeyError, AttributeError, UnicodeError):
                    ids = ['SCOPE-SCHEMA']
                if fid not in ids:
                    reclassify_mismatch += 1
                    unattributed.append(dict(finding, reason='re-classification does not reproduce this id'))
                    continue
                if fid == 'SCOPE-PATH-DENIED':
                    subcause = path_subcause(checker, operation, event.get('args'), bindings[name])
            if fid == 'SCOPE-SCHEMA':
                keys = arg_keys(event.get('args'))
                unknown_sites.append({'site': site, 'operation': operation, 'retained_keys': keys,
                                      'unknown_tokens': keys.count(UNKNOWN)})
                subcause = 'argument key outside the frozen two-shape edit grammar'
            seat, with_operation = name, with_operation + 1
            per_finding.append({'site': site, 'finding': fid, 'operation': operation, 'subcause': subcause,
                                'request_line': event.get('request_line'), 'call_id': event.get('call_id'),
                                'seat_trace_complete': seats[name].get('complete'),
                                'lower_bound': seats[name].get('complete') is False})
        elif (fid == 'SCOPE-TRACE-INCOMPLETE' and not sep and site in seats
              and seats[site].get('complete') is False):
            operation, seat, subcause = 'none (seat-level trace state)', site, 'trace marked incomplete by the collector; which condition failed is not recorded'
            seat_level += 1
            per_finding.append({'site': site, 'finding': fid, 'operation': None, 'subcause': subcause,
                                'request_line': None, 'call_id': None, 'seat_trace_complete': False,
                                'lower_bound': False})
        else:
            unattributed.append(finding)
            continue
        attributed += 1
        rows[(fid, operation, subcause)] += 1
        row_seats[(fid, operation, subcause)].add(seat)
    incomplete = [{'name': n, 'trace_complete': False, 'events': len(s['events'])}
                  for n, s in sorted(seats.items()) if s.get('complete') is False]
    site_keys = set()
    for item in unknown_sites:
        if item['site'] == limit.get('schema_site'):
            site_keys.update(item['retained_keys'])
    recollection = []
    if isinstance(limit, dict) and isinstance(limit.get('schema_original_keys'), list):
        for key in limit['schema_original_keys']:
            recollection.append({'name': key, 'in_retained_site_event': key in site_keys,
                                 'label': None if key in site_keys else LABEL})
    total = len(result.get('findings', []))
    by_id = collections.Counter(f.get('id') for f in result.get('findings', []))
    report = {
        'checker_status': result.get('status'), 'checker_exit': code,
        'total_findings': total, 'attributed_findings': attributed,
        'attributed_with_recorded_operation': with_operation, 'attributed_seat_level': seat_level,
        'reclassify_mismatches': reclassify_mismatch, 'unattributed': unattributed,
        'findings_by_id': dict(sorted(by_id.items())),
        'causes': [{'finding': f, 'operation': o, 'subcause': c, 'count': n, 'seats': len(row_seats[(f, o, c)])}
                   for (f, o, c), n in sorted(rows.items(), key=lambda kv: (kv[0][0], str(kv[0][1]), str(kv[0][2])))],
        'lower_bound_findings': sum(1 for r in per_finding if r['lower_bound']),
        'incomplete_seats': incomplete, 'unknown_argument_sites': unknown_sites,
        'schema_original_keys': recollection, 'per_finding': per_finding, 'scope': SCOPE,
    }
    ok = (total > 0 and attributed == total and not unattributed and code == 2
          and result.get('status') == 'CANNOT_EVALUATE' and bool(incomplete)
          and all(s['unknown_tokens'] > 0 for s in unknown_sites) and bool(unknown_sites)
          and LABEL == 'author recollection, not recoverable from retained events'
          and all((r['label'] is None if r['in_retained_site_event'] else r['label'] == LABEL)
                  for r in recollection)
          and all(isinstance(row['subcause'], str) and bool(row['subcause']) for row in per_finding))
    report['preserved'] = ok
    return (0 if ok else 1), report


def run(revision, branch):
    binder_digest = hashlib.sha256((ROOT / 'tools' / '_revision.py').read_bytes()).hexdigest()
    if binder_digest != 'fc861ec8a4f2539ac3f16d1a04af8335a974c17c8ffba0a41f6dad972cad36de':
        raise RuntimeError('revision binder differs from the claim-base bytes')
    binding = _revision.bind(ROOT, revision, branch)
    try:
        own = git_blob(binding.sha, SELF)
    except RuntimeError:
        raise RuntimeError(f'{SELF} is absent at this revision')
    if (ROOT / SELF).read_bytes() != own:
        raise RuntimeError('working-tree report tool differs from the revision blob')
    blobs = {p: git_blob(binding.sha, p) for p in (CHECKER, MANIFEST, EVENTS, LIMIT)}
    digests = {p: hashlib.sha256(b).hexdigest() for p, b in blobs.items()}
    pin_mismatch = sorted(p for p in PINS if digests[p] != PINS[p])
    checker = load_checker(blobs[CHECKER])
    code, result = checker.evaluate(blobs[MANIFEST], blobs[EVENTS])
    trace = json.loads(blobs[EVENTS], object_pairs_hook=unique)
    manifest = json.loads(blobs[MANIFEST], object_pairs_hook=unique)
    limit = json.loads(blobs[LIMIT], object_pairs_hook=unique)
    status, report = attribute(code, result, trace, limit, manifest, checker)
    split_ok = report['findings_by_id'] == EXPECTED
    named_seat = [s['name'] for s in report['incomplete_seats']] == ['ConnFxPlanner']
    collector_path = '.ufo/waves/round-23/collect.py'
    native_path = '.ufo/waves/round-23/falsify/native-outcomes.json'
    provenance = {}
    for path in (collector_path, native_path):
        blob = git_blob(binding.sha, path)
        base_blob = git_blob('f169b3ba9a59abaf3e324c1b591e1e07a4d6003a', path)
        provenance[path] = {'sha256': hashlib.sha256(blob).hexdigest(),
                            'matches_claim_base': blob == base_blob}
    native = json.loads(git_blob(binding.sha, native_path), object_pairs_hook=unique)
    native_rows = {row['name']: row for row in native['seats']}
    for row in report['incomplete_seats']:
        row['native_status_recorded'] = native_rows.get(row['name'], {}).get('status')
    report['native_completed_recorded'] = sum(row.get('status') == 'completed' for row in native['seats'])
    report['trace_complete_recorded'] = sum(row.get('complete') is True for row in trace['seats'])
    report['recorder_provenance'] = provenance
    if not all(row['matches_claim_base'] for row in provenance.values()):
        status, report['preserved'] = 1, False
    report.update(revision=binding.sha, branch=binding.branch, inputs=digests,
                  pin_mismatches=pin_mismatch, expected_split=EXPECTED, split_matches=split_ok,
                  incomplete_seat_is_frozen=named_seat)
    if pin_mismatch or not split_ok or not named_seat:
        status, report['preserved'] = 1, False
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
    limit = {'schema_site': 'A:1', 'schema_original_keys': ['i', 'new_string', 'old_string', 'path', 'replace_all']}
    cases = [
        ('pristine', 2, result(base), trace(False), limit, 0),
        ('site-out-of-range', 2, result(base + [('SCOPE-PATH-DENIED', 'A:9')]), trace(False), limit, 1),
        ('unknown-seat-site', 2, result(base + [('SCOPE-PATH-DENIED', 'Z:0')]), trace(False), limit, 1),
        ('incomplete-seat-dropped', 2, result(base), trace(True), limit, 1),
        ('unknown-key-renamed', 2, result(base), trace(False, ('i', 'new_string', 'old_string', 'path', 'replace_all')),
         {'schema_site': 'A:1', 'schema_original_keys': ['i', 'new_string', 'old_string', 'path', 'replace_all', 'other']}, 1),
        ('checker-exit-changed', 1, result(base, 'FAIL'), trace(False), limit, 1),
        ('status-relabelled', 2, result(base, 'FAIL'), trace(False), limit, 1),
        ('no-schema-site', 2, result([f for f in base if f[0] != 'SCOPE-SCHEMA']), trace(False), limit, 1),
        ('empty-findings', 2, result([]), trace(False), limit, 1),
        ('no-incomplete-seat', 2, result([f for f in base if f[0] != 'SCOPE-TRACE-INCOMPLETE']), trace(True), limit, 1),
    ]
    obs = []
    for name, code, res, tr, lim, want in cases:
        got, rep = attribute(code, res, tr, lim)
        label_ok = name != 'pristine' or [r['label'] for r in rep['schema_original_keys']] == [None] * 4 + [LABEL]
        obs.append({'case': name, 'want': want, 'got': got, 'pass': got == want and label_ok})
    class Stub:
        """Literal stand-in for the frozen checker: read/write of /x or /y is path-denied."""
        LANE = '/lane'
        @staticmethod
        def classify(tool, args, binding, allow_structured_edit=False):
            if tool == 'edit':
                return ['SCOPE-SCHEMA']
            return ['SCOPE-PATH-DENIED'] if tool in ('read', 'write') else []
        @staticmethod
        def requested_path(value, selector=False):
            return value, 'SCOPE-PATH-DENIED'
    manifest = {'schema': 'tsukuroi-seat-bindings-v2', 'seats': [
        {'name': 'A', 'read_paths': [], 'write_paths': []}, {'name': 'B', 'read_paths': [], 'write_paths': []}]}
    shifted = [('SCOPE-PATH-DENIED', 'A:1'), ('SCOPE-SCHEMA', 'A:0'), ('SCOPE-TRACE-INCOMPLETE', 'B'), ('SCOPE-PATH-DENIED', 'B:0')]
    for name, findings, want in (('stub-pristine', base, 0), ('stub-shifted-sites', shifted, 1)):
        got, rep = attribute(2, result(findings), trace(False), limit, manifest, Stub)
        ok = got == want and (want == 1 or rep['per_finding'][0]['subcause'] == 'outside the lane root')
        obs.append({'case': name, 'want': want, 'got': got, 'pass': ok})
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
