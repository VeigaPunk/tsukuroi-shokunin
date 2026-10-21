#!/usr/bin/env python3
"""L1-only fixed negative witnesses, using frozen candidate and final evaluators."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / '.ufo/waves/round-22'
sys.path.insert(0, str(ROOT / 'tools'))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    observations = []
    for label, folder in [('candidate', ROUND / 'candidate/tools'), ('final', ROOT / 'tools')]:
        boundary = load(folder / 'check-boundary-contract.py', 'boundary_' + label)
        original = boundary.EXPECTED
        boundary.EXPECTED = tuple((r[0], r[1], 'ALLOW', r[3], r[4]) if r[0] == 'DEAD' else r for r in original)
        with contextlib.redirect_stdout(io.StringIO()) as capture:
            code = boundary.selftest()
        output = json.loads(capture.getvalue())
        boundary.EXPECTED = original
        observations.append({'case': 'oracle-lockstep-' + label, 'exit': code, 'failed_cases': output['failed'],
                             'expected_exit': 0 if label == 'candidate' else 1,
                             'pass': code == (0 if label == 'candidate' else 1), 'restored': boundary.EXPECTED == original,
                             'evaluator_sha256': source(folder / 'check-boundary-contract.py')})
    lane = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
    bindings = {'schema': 'tsukuroi-seat-bindings-v1', 'seats': [{'name': 'A', 'root': lane, 'read_paths': [lane + '/source'], 'write_paths': [lane + '/report'], 'commands': [], 'fetches': []}]}
    events = {'schema': 'tsukuroi-seat-events-v1', 'seats': [{'name': 'A', 'agent': 'agent-A', 'complete': True, 'events': [{'tool': 'read', 'args': {}}, {'tool': 'bash', 'args': {}}]}]}
    for label, folder in [('candidate', ROUND / 'candidate/tools'), ('final', ROOT / 'tools')]:
        auditor = load(folder / 'check-seat-bindings.py', 'auditor_' + label)
        code, result = auditor.evaluate(bindings, events)
        ids = {f['id'] for f in result['findings']}
        observations.append({'case': 'malformed-before-bash-' + label, 'exit': code, 'ids': sorted(ids),
                             'pass': code == 2 and ('SCOPE-EXEC-DENIED' in ids) == (label == 'final'),
                             'evaluator_sha256': source(folder / 'check-seat-bindings.py')})
    raw = b'source\n'
    sha = hashlib.sha256(raw).hexdigest()
    report = f'Reviewed-SHA256: {sha}\nPredicate: p\nScope: executed=none\n'.encode()
    manifest = json.dumps({'schema': 'tsukuroi-review-snapshots-v1', 'reviews': [{'name': 'A', 'source': 's', 'report': 'r', 'sha256': sha, 'predicate': 'p'}]})
    settlement = json.dumps({'schema': 'tsukuroi-review-settlement-v1', 'seats': [{'name': 'A', 'agent': 'agent-A', 'outcome': 'completed', 'error': '', 'report_sha256': hashlib.sha256(report).hexdigest()}]})
    for label, folder in [('candidate', ROUND / 'candidate/tools'), ('final', ROOT / 'tools')]:
        cohort = load(folder / 'check-review-cohort.py', 'cohort_' + label)
        code, result = cohort.evaluate(manifest, settlement, {'s': raw, 'r': report + b'after settlement'}.get)
        observations.append({'case': 'report-drift-' + label, 'exit': code, 'ids': [f['id'] for f in result['findings']],
                             'pass': code == (0 if label == 'candidate' else 1),
                             'evaluator_sha256': source(folder / 'check-review-cohort.py')})
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations), 'failed': failed,
                      'observations': observations, 'scope': 'Isolated in-memory oracle mutation and fixed fixture comparisons; no production bytes changed, no commands from trace inputs executed.'}))
    return int(bool(failed))


if __name__ == '__main__':
    sys.exit(main())
