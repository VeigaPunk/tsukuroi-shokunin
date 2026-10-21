#!/usr/bin/env python3
"""Account for a fixed review cohort without converting strict receipt faults to passes."""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('tsukuroi_strict_receipts', ROOT / 'tools/check-review-snapshots.py')
strict = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(strict)
SCOPE = 'Cohort accounting of strict receipt declarations only; delivered_conformant means receipt-well-formed, not request-scope conformity, command nonexecution, reading, chronology, no-harm or native enforcement. Report hashes bind evaluated-revision bytes to the trusted producer settlement, not independently proven timing or provider causes.'


def evaluate(manifest, settlement, read_bytes):
    if manifest is None:
        return 1, {'status': 'FAIL', 'cohort_accounting_mode': 0, 'findings': [{'id': 'COHORT-MANIFEST-MISSING', 'site': 'manifest'}], 'scope': SCOPE}
    findings, rows = [], []
    strict_code, strict_result = None, None
    counts = dict.fromkeys(('delivered_conformant', 'delivered_faulty', 'absent_dead', 'absent_unresolved'), 0)
    def add(fid, site):
        findings.append({'id': fid, 'site': site})
    try:
        # Preserve the original strict findings even when settlement is malformed.
        strict_code, strict_result = strict.evaluate(manifest, read_bytes)
        if any(f['id'] == 'REVIEW-MANIFEST-SCHEMA' for f in strict_result['findings']):
            raise ValueError('manifest schema')
        data = json.loads(manifest, object_pairs_hook=strict.unique_object)
        settled = json.loads(settlement, object_pairs_hook=strict.unique_object)
        reviews = data['reviews']
        names = {r['name'] for r in reviews}
        if not isinstance(settled, dict) or settled.get('schema') != 'tsukuroi-review-settlement-v1' or not isinstance(settled.get('seats'), list):
            raise ValueError('settlement schema')
        by_name, agents = {}, set()
        for row in settled['seats']:
            if not isinstance(row, dict) or row.get('name') not in names or row['name'] in by_name or not isinstance(row.get('agent'), str) or not row['agent'] or strict.has_controls(row['agent']) or row['agent'] in agents or row.get('outcome') not in ('completed', 'failed', 'unknown') or not isinstance(row.get('error'), str) or strict.has_controls(row['error']):
                raise ValueError('settlement identity/outcome')
            if row['outcome'] == 'failed' and not row['error'].strip():
                raise ValueError('failure without observed error')
            if row['outcome'] == 'completed' and row['error']:
                raise ValueError('completed outcome with failure error')
            digest = row.get('report_sha256')
            if 'report_sha256' not in row or (digest is not None and (not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest))):
                raise ValueError('settled report identity')
            by_name[row['name']] = row
            agents.add(row['agent'])
        if set(by_name) != names:
            raise ValueError('settlement cohort differs from manifest')
        unclassified = 0
        for review in reviews:
            name = review['name']
            outcome = by_name[name]
            one_manifest = json.dumps({'schema': data['schema'], 'reviews': [review]})
            one_code, one = strict.evaluate(one_manifest, read_bytes)
            available = True
            try:
                report = read_bytes(review['report'])
            except (OSError, RuntimeError, subprocess.TimeoutExpired):
                report = None
                available = False
            if not available:
                category = None
                unclassified += 1
                add('COHORT-READ', name)
            elif report is None:
                category = 'absent_dead' if outcome['outcome'] == 'failed' else 'absent_unresolved'
            else:
                category = 'delivered_conformant' if one_code == 0 else 'delivered_faulty'
            if category is not None:
                counts[category] += 1
            digest = hashlib.sha256(report).hexdigest() if report is not None else None
            if available and digest != outcome['report_sha256']:
                add('COHORT-REPORT-DRIFT', name)
            rows.append({'name': name, 'agent': outcome['agent'], 'outcome': outcome['outcome'], 'error': outcome['error'],
                         'category': category, 'strict_exit': one_code, 'strict_findings': one['findings'],
                         'report_read_available': available, 'report_sha256': digest, 'settled_report_sha256': outcome['report_sha256']})
        if counts['absent_unresolved']:
            add('COHORT-UNRESOLVED', 'absent_unresolved')
        if strict_code == 2:
            add('COHORT-STRICT-UNAVAILABLE', 'strict evaluator')
        code = 2 if strict_code == 2 or unclassified else (1 if findings else 0)
        result = {'cohort_accounting_mode': int(code == 0), 'total': len(reviews), **counts,
                  'accounted': sum(counts.values()), 'unclassified': unclassified,
                  'seats': rows, 'findings': findings, 'scope': SCOPE}
    except (ValueError, TypeError, KeyError, AttributeError, UnicodeError):
        code, result = 2, {'cohort_accounting_mode': 0, 'findings': [{'id': 'COHORT-SCHEMA', 'site': 'input'}], 'scope': SCOPE}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        code, result = 2, {'cohort_accounting_mode': 0, 'findings': [{'id': 'COHORT-READ', 'site': 'input'}], 'scope': SCOPE}
    if strict_result is not None:
        result.update(strict_receipt_exit=strict_code, strict_receipt_findings=strict_result['findings'],
                      strict_conformance='PASS' if strict_code == 0 else ('CANNOT_EVALUATE' if strict_code == 2 else 'FAIL'))
    result['status'] = ('PASS', 'FAIL', 'CANNOT_EVALUATE')[code]
    return code, result


def selftest():
    source = b'fixed source\n'
    sha = hashlib.sha256(source).hexdigest()
    manifest = {'schema': 'tsukuroi-review-snapshots-v1', 'reviews': [{'name': 'A', 'source': 's', 'report': 'r', 'sha256': sha, 'predicate': 'p'}]}
    settlement = {'schema': 'tsukuroi-review-settlement-v1', 'seats': [{'name': 'A', 'agent': 'agent-A', 'outcome': 'completed', 'error': ''}]}
    report = f'Reviewed-SHA256: {sha}\nPredicate: p\nScope: executed=none\n'.encode()
    files = {'s': source, 'r': report}
    cases = []
    def case(name, man, settled, inputs, code, category=None, fid=None, strict_exit=None):
        settled = copy.deepcopy(settled)
        if isinstance(settled, dict) and isinstance(man, dict):
            for row in settled['seats']:
                review = next((r for r in man['reviews'] if r['name'] == row['name']), None)
                payload = inputs.get(review['report']) if review is not None else None
                row['report_sha256'] = hashlib.sha256(payload).hexdigest() if payload is not None else None
        cases.append((name, man, settled, inputs, code, category, fid, strict_exit))
    case('clean', manifest, settlement, files, 0, 'delivered_conformant', strict_exit=0)
    failed = copy.deepcopy(settlement); failed['seats'][0].update(outcome='failed', error='observed provider failure')
    case('dead-missing', manifest, failed, {'s': source}, 0, 'absent_dead', strict_exit=1)
    case('partial-failed', manifest, failed, {**files, 'r': b'partial'}, 0, 'delivered_faulty', strict_exit=1)
    case('missing-unresolved', manifest, settlement, {'s': source}, 1, 'absent_unresolved', 'COHORT-UNRESOLVED', 1)
    for name, old, new in [('period', b'executed=none', b'executed=none.'), ('predicate', b'Predicate: p', b'Predicate: q'), ('digest', sha.encode(), b'0' * 64)]:
        case(name, manifest, settlement, {**files, 'r': report.replace(old, new)}, 0, 'delivered_faulty', strict_exit=1)
    case('duplicate-receipt', manifest, settlement, {**files, 'r': report + f'Reviewed-SHA256: {sha}\n'.encode()}, 0, 'delivered_faulty', strict_exit=1)
    case('crlf', manifest, settlement, {**files, 'r': report.replace(b'\n', b'\r\n')}, 0, 'delivered_conformant', strict_exit=0)
    case('unicode', manifest, settlement, {**files, 'r': report.rstrip(b'\n') + '\u2028'.encode()}, 0, 'delivered_faulty', strict_exit=1)
    case('encoding', manifest, settlement, {**files, 'r': b'\xff'}, 2, 'delivered_faulty', 'COHORT-STRICT-UNAVAILABLE', 2)
    for name, change in [('dropped', lambda s: s['seats'].clear()), ('duplicate', lambda s: s['seats'].append(copy.deepcopy(s['seats'][0]))), ('unknown', lambda s: s['seats'][0].update(name='B')), ('false-death', lambda s: s['seats'][0].update(outcome='failed'))]:
        changed = copy.deepcopy(settlement); change(changed)
        case(name, manifest, changed, files, 2, fid='COHORT-SCHEMA')
    case('manifest-missing', None, settlement, files, 1, fid='COHORT-MANIFEST-MISSING')
    duplicate = copy.deepcopy(manifest); duplicate['reviews'].append(duplicate['reviews'][0])
    case('duplicate-manifest', duplicate, settlement, files, 2, fid='COHORT-SCHEMA')
    case('duplicate-json-key', manifest, '{"schema":1,"schema":2}', files, 2, fid='COHORT-SCHEMA')
    completed_error = copy.deepcopy(settlement); completed_error['seats'][0]['error'] = 'observed error'
    case('completed-with-error', manifest, completed_error, files, 2, fid='COHORT-SCHEMA')
    format_error = copy.deepcopy(failed); format_error['seats'][0]['error'] = '\u200b'
    case('format-only-error', manifest, format_error, {'s': source}, 2, fid='COHORT-SCHEMA')
    case('report-drift', manifest, settlement, {**files, 'r': report + b'append'}, 1, 'delivered_conformant', 'COHORT-REPORT-DRIFT', 0)
    cases[-1][2]['seats'][0]['report_sha256'] = hashlib.sha256(report).hexdigest()
    pair_manifest = copy.deepcopy(manifest)
    pair_manifest['reviews'].append(dict(pair_manifest['reviews'][0], name='B', report='r2'))
    pair_settlement = copy.deepcopy(settlement)
    pair_settlement['seats'].append(dict(pair_settlement['seats'][0], name='B', agent='agent-B'))
    case('two-seat-mixed', pair_manifest, pair_settlement, {**files, 'r2': b'partial'}, 0, strict_exit=1)
    same_agent = copy.deepcopy(pair_settlement); same_agent['seats'][1]['agent'] = 'agent-A'
    case('duplicate-agent-only', pair_manifest, same_agent, {**files, 'r2': report}, 2, fid='COHORT-SCHEMA')
    observations = []
    for name, man, settled, inputs, expected, category, fid, strict_exit in cases:
        man = json.dumps(man) if man is not None and not isinstance(man, str) else man
        settled = json.dumps(settled) if not isinstance(settled, str) else settled
        code, result = evaluate(man, settled, inputs.get)
        ids = [f['id'] for f in result['findings']]
        partition = 'total' not in result or (result['accounted'] == sum(result[k] for k in ('delivered_conformant', 'delivered_faulty', 'absent_dead', 'absent_unresolved')) and result['accounted'] + result['unclassified'] == result['total'] == len(result['seats']))
        passed = code == expected and result.get('cohort_accounting_mode') == int(code == 0) and partition and (category is None or result.get(category) == 1) and (fid is None or fid in ids) and (strict_exit is None or result.get('strict_receipt_exit') == strict_exit)
        observations.append({'case': name, 'exit': code, 'ids': ids, 'strict_exit': result.get('strict_receipt_exit'), 'pass': passed})
    pair_failed = copy.deepcopy(pair_settlement)
    for row in pair_failed['seats']:
        row.update(outcome='failed', error='observed failure', report_sha256=None)
    def raising_read(path):
        if path == 'r2':
            raise OSError('fixture unavailable')
        return {'s': source}.get(path)
    code, unavailable = evaluate(json.dumps(pair_manifest), json.dumps(pair_failed), raising_read)
    retained = {f['id'] for f in unavailable.get('strict_receipt_findings', [])}
    observations.append({'case': 'read-error-retains-missing', 'exit': code, 'pass': code == 2 and unavailable.get('cohort_accounting_mode') == 0 and {'REVIEW-READ-FAILED', 'REVIEW-REPORT-MISSING'} <= retained and unavailable.get('accounted') == 1 and unavailable.get('unclassified') == 1})
    failed_count = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed_count else 'PASS', 'cases': len(observations), 'failed': failed_count, 'observations': observations}))
    return int(bool(failed_count))


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
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--revision')
    mode.add_argument('--selftest', action='store_true')
    parser.add_argument('--branch', default='master')
    parser.add_argument('--manifest', default='.ufo/waves/round-22/build/reviews.json')
    parser.add_argument('--settlement', default='.ufo/waves/round-22/build/settlement.json')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    if not all(strict.safe_path(p) for p in (args.manifest, args.settlement)):
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'COHORT-SCHEMA', 'site': 'input paths'}]}))
        return 2
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, result = evaluate(git_read(binding.sha, args.manifest), git_read(binding.sha, args.settlement), lambda path: git_read(binding.sha, path))
        result.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, result = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        code, result = 2, {'status': 'CANNOT_EVALUATE', 'findings': [{'id': 'COHORT-READ', 'site': 'revision'}]}
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
