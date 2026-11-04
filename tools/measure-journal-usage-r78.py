#!/usr/bin/env python3
"""six pinned path-usage cases match with review binding.

Finite worked-example depth, not a general semantic/authenticity oracle. A reviewer
report is bound by its byte digest in the orchestrator result; substance still
needs source reading and outside closure. --root is for isolated controls only.
"""
import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '.ufo/waves/round-78/'
DATA = 'corpus/knowledge/journald-path-usage-r78.json'
REVIEW = PREFIX + 'w1/ReviewUsage/verdict.json'
RESULTS = PREFIX + 'w1-results.json'
LABEL = 'six pinned path-usage cases match with review binding'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate-key')
        result[key] = value
    return result


def decode(raw):
    return json.loads(raw, object_pairs_hook=unique)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def evaluate(read, expected):
    for name, sha in expected['pins'].items():
        if digest(read(PREFIX + 'before/' + name)) != sha:
            return 0, False, 'snapshot-tampered'
    raw = read(DATA)
    data = decode(raw)
    if data != {'source': expected['source'], 'cases': expected['cases']}:
        return 0, False, 'finite-content-mismatch'
    # JSON bools are not accepted as integer sizes, blocks or outputs.
    for row in data['cases']:
        if any(type(row[k]) is not int for k in ('blocks', 'size', 'used')):
            return 0, False, 'integer-type'
        if type(row['stat_ok']) is not bool:
            return 0, False, 'stat-type'
    review_raw = read(REVIEW)
    review = decode(review_raw)
    if (review.get('artifact_sha256') != digest(raw)
            or review.get('reviewer') != expected['reviewer']
            or review.get('verdicts') != {r['id']: 'holds' for r in expected['cases']}):
        return 0, False, 'review-not-bound'
    results = decode(read(RESULTS))
    seats = [r for r in results.get('results', []) if r.get('name') == expected['reviewer']]
    if (results.get('lane') != 'tsukuroi' or results.get('round') != 78
            or results.get('wave') != 'w1' or len(seats) != 1
            or seats[0].get('agent') != 'reviewer'):
        return 0, False, 'result-identity'
    output = seats[0].get('output')
    # Deliberately accept both JSON-wrapped and plain text final output.
    if not isinstance(output, str) or 'review_sha256=' + digest(review_raw) not in output:
        return 0, False, 'result-digest'
    return 6, True, 'finite-content-and-review'


def score(read, expected):
    try:
        return evaluate(read, expected)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return 0, False, 'unreadable:' + type(exc).__name__


def selftest(expected):
    files = {PREFIX + 'before/' + name: (ROOT / PREFIX / 'before' / name).read_bytes()
             for name in expected['pins']}
    files[DATA] = (json.dumps({'source': expected['source'], 'cases': expected['cases']}, indent=2) + '\n').encode()
    review = {'reviewer': 'ReviewUsage', 'artifact_sha256': digest(files[DATA]),
              'verdicts': {r['id']: 'holds' for r in expected['cases']}}
    files[REVIEW] = json.dumps(review).encode()
    results = {'lane': 'tsukuroi', 'round': 78, 'wave': 'w1', 'results': [
        {'name': 'ReviewUsage', 'agent': 'reviewer',
         'output': 'review_sha256=' + digest(files[REVIEW])}]}
    files[RESULTS] = json.dumps(results).encode()
    checks = []
    def check(name, changed, want, reason):
        count, ok, got = score(changed.__getitem__, expected)
        passed = ok == want and got == reason
        checks.append(passed)
        print(f'SELFTEST {name} expected={int(want)} observed={int(ok)} reason={got} {"PASS" if passed else "FAIL"}')
    check('control', files, True, 'finite-content-and-review')
    for row in expected['cases']:
        f = dict(files); d = decode(f[DATA]); d['cases'][int(row['id'][1:])-1]['used'] += 1
        f[DATA] = json.dumps(d).encode()
        check('wrong-' + row['id'], f, False, 'finite-content-mismatch')
    for path in (DATA, REVIEW, RESULTS):
        f = dict(files); del f[path]
        check('missing-' + Path(path).name, f, False, 'unreadable:KeyError')
    f = dict(files); f[PREFIX + 'before/journald-manager.c'] = b'tampered'
    check('snapshot', f, False, 'snapshot-tampered')
    f = dict(files); d = decode(f[DATA]); d['source'] = []; f[DATA] = json.dumps(d).encode()
    check('sourceless', f, False, 'finite-content-mismatch')
    f = dict(files); d = copy.deepcopy(results); d['results'][0]['agent'] = 'scribe'; f[RESULTS] = json.dumps(d).encode()
    check('wrong-role', f, False, 'result-identity')
    f = dict(files); d = copy.deepcopy(results); d['results'][0]['output'] = None; f[RESULTS] = json.dumps(d).encode()
    check('lost-result', f, False, 'result-digest')
    f = dict(files); d = copy.deepcopy(review); d['verdicts']['U4'] = 'fails'; f[REVIEW] = json.dumps(d).encode()
    check('failed-row', f, False, 'review-not-bound')
    print(f'SELFTEST total={len(checks)} passed={sum(checks)} failed={checks.count(False)}')
    return 0 if all(checks) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--revision')
    group.add_argument('--root', type=Path)
    group.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    expected = decode((ROOT / PREFIX / 'before/expected.json').read_bytes())
    if args.selftest:
        return selftest(expected)
    def read(path):
        if args.root:
            return (args.root / path).read_bytes()
        p = subprocess.run(['git', '-C', str(ROOT), 'show', args.revision + ':' + path], capture_output=True)
        if p.returncode:
            raise ValueError('missing-blob')
        return p.stdout
    count, ok, reason = score(read, expected)
    print(f'C1 predicate="{LABEL}" count={count} met={int(ok)} reason={reason}')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
