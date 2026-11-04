#!/usr/bin/env python3
"""eight pinned dependency-propagation rows match with review binding.

Round-79 C1 (frozen by the round-79 declaration, before any target file exists).
Finite worked-example depth over the owned systemd-unit surface, not a general
semantic oracle, not an installed-build equivalence proof and not an authenticity
system: the rows are a frozen decision set, a reviewer verdict is bound by byte
digests, and a fully fabricated report bundle remains a declared limit.

QUALITY 28: revision binding is the shared `tools/_revision.py` contract (branch,
7-64 hex, landed, pushed), never a private copy of the checks.

Quote location rule: quotes are located in the tag-stripped, whitespace-normalized
snapshot (inline XML elements removed, tokens rejoined with one space) and the
computed token line range must equal the row's `line` cell. Reads only; writes
nothing. --root is for isolated controls and selftests only.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _revision import RevisionError, bind  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '.ufo/waves/round-79/'
EXPECTED = PREFIX + 'before/expected.json'
SNAPSHOT = PREFIX + 'before/src/systemd.unit.xml'
DATA = 'corpus/knowledge/systemd-dependency-propagation-r79.json'
COMPANION = 'corpus/knowledge/systemd-dependency-propagation-r79.md'
REGISTRY = 'corpus/SOURCES.md'
REVIEW = PREFIX + 'w1/ReviewDeps/verdict.json'
RESULTS = PREFIX + 'w1-results.json'
LABEL = 'eight pinned dependency-propagation rows match with review binding'
FROZEN_EXPECTED_SHA256 = '0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21'
REVIEWER = 'ReviewDeps'
TARGET_ROWS = 8
SOURCE = 'S329'
TAG = re.compile(r'</?[A-Za-z][^>]*>')


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


def locate(snapshot_bytes, quote):
    """Return the token line range of `quote`, or None when it is absent."""
    toks, linenos = [], []
    for number, line in enumerate(snapshot_bytes.decode('utf-8').splitlines(), 1):
        for token in TAG.sub('', line).split():
            toks.append(token)
            linenos.append(number)
    wanted = quote.split()
    if not wanted:
        return None
    haystack = ' ' + ' '.join(toks) + ' '
    needle = ' ' + ' '.join(wanted) + ' '
    index = haystack.find(needle)
    if index < 0:
        return None
    start = haystack[:index].count(' ')
    first = linenos[start]
    last = linenos[start + len(wanted) - 1]
    return f'{first}-{last}' if first != last else str(first)


def registry_row(registry_text, source_id):
    for line in registry_text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) == 11 and cells[0] == source_id:
            return cells
    return None


def evaluate(read, expected):
    if digest(read(EXPECTED)) != FROZEN_EXPECTED_SHA256:
        return 0, False, 'expected-drift'
    raw = read(DATA)
    data = decode(raw)
    if data != {'source': expected['source'], 'rows': expected['rows']}:
        return 0, False, 'finite-content-mismatch'
    ids = [row['id'] for row in data['rows']]
    if len(ids) != TARGET_ROWS or len(set(ids)) != TARGET_ROWS:
        return 0, False, 'row-set'
    registry = read(REGISTRY).decode('utf-8', 'replace')
    for row in data['rows']:
        cells = registry_row(registry, row['source'])
        if cells is None or cells[2] == 'own-work' or row['snapshot'] not in cells[1]:
            return 0, False, 'source-unresolved'
        snapshot = read(PREFIX + 'before/src/' + row['snapshot'])
        if digest(snapshot) != row['digest'] or row['digest'] != expected['digest']:
            return 0, False, 'snapshot-digest'
        if locate(snapshot, row['quote']) != row['line']:
            return 0, False, 'quote-location'
        if len(row['quote'].split()) > 25 or not row['statement'].strip():
            return 0, False, 'row-shape'
    companion = read(COMPANION)
    review_raw = read(REVIEW)
    review = decode(review_raw)
    if (review.get('reviewer') != REVIEWER
            or review.get('artifact_sha256') != digest(raw)
            or review.get('companion_sha256') != digest(companion)
            or review.get('verdicts') != {row['id']: 'holds' for row in expected['rows']}):
        return 0, False, 'review-not-bound'
    results = decode(read(RESULTS))
    seats = [r for r in results.get('results', []) if r.get('name') == REVIEWER]
    if (results.get('lane') != 'tsukuroi' or results.get('round') != 79
            or results.get('wave') != 'w1' or len(seats) != 1
            or seats[0].get('agent') != 'reviewer'):
        return 0, False, 'result-identity'
    output = seats[0].get('output')
    if not isinstance(output, str) or 'review_sha256=' + digest(review_raw) not in output:
        return 0, False, 'result-digest'
    return TARGET_ROWS, True, 'finite-content-and-review'


def score(read, expected):
    try:
        return evaluate(read, expected)
    except RevisionError as exc:
        return 0, False, 'binding:' + exc.fid
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return 0, False, 'unreadable:' + type(exc).__name__


def selftest(expected, expected_raw):
    files = {EXPECTED: expected_raw,
             SNAPSHOT: (ROOT / SNAPSHOT).read_bytes(),
             COMPANION: b'# test companion\n'}
    files[REGISTRY] = ('| id | source | kind | tier | scope | anchor | teaches | status | opened '
                       '| recheck | used-by |\n'
                       '|---|---|---|---|---|---|---|---|---|---|---|\n'
                       '| S329 | systemd.unit(5) — https://raw.githubusercontent.com/systemd/'
                       'systemd/v262/man/systemd.unit.xml | docs | A | u | systemd.unit.xml | t | mined '
                       '| 2026-11-04 | on-release | x |\n').encode()
    data = {'source': expected['source'], 'rows': expected['rows']}
    files[DATA] = (json.dumps(data, indent=1, ensure_ascii=False) + '\n').encode()
    review = {'reviewer': REVIEWER, 'artifact_sha256': digest(files[DATA]),
              'companion_sha256': digest(files[COMPANION]),
              'verdicts': {row['id']: 'holds' for row in expected['rows']}}
    files[REVIEW] = json.dumps(review).encode()
    results = {'lane': 'tsukuroi', 'round': 79, 'wave': 'w1', 'results': [
        {'name': REVIEWER, 'agent': 'reviewer',
         'output': 'review_sha256=' + digest(files[REVIEW])}]}
    files[RESULTS] = json.dumps(results).encode()
    checks = []

    def check(name, changed, want, reason, label):
        count, ok, got = score(changed.__getitem__, expected)
        passed = ok == want and got == reason and count == (TARGET_ROWS if want else 0)
        checks.append(passed)
        print(f'SELFTEST {name} expected={int(want)} observed={int(ok)} '
              f'count={count} reason={got} label={label} '
              f'{"PASS" if passed else "FAIL"}')

    check('control', files, True, 'finite-content-and-review', LABEL)
    f = dict(files); f[EXPECTED] = f[EXPECTED] + b' '; check('expected-drift', f, False,
                                                             'expected-drift', LABEL)
    for row in expected['rows']:
        f = dict(files); d = decode(f[DATA])
        d['rows'][int(row['id'][2:]) - 1]['quote'] += ' x'
        f[DATA] = json.dumps(d).encode()
        check('quote-' + row['id'], f, False, 'finite-content-mismatch', LABEL)
        f = dict(files); d = decode(f[DATA])
        d['rows'][int(row['id'][2:]) - 1]['line'] = '1'
        f[DATA] = json.dumps(d).encode()
        check('line-' + row['id'], f, False, 'finite-content-mismatch', LABEL)
    f = dict(files); d = decode(f[DATA]); d['rows'] = d['rows'][:7]; f[DATA] = json.dumps(d).encode()
    check('seven-rows', f, False, 'finite-content-mismatch', LABEL)
    f = dict(files); d = decode(f[DATA]); d['rows'][1]['id'] = d['rows'][0]['id']
    f[DATA] = json.dumps(d).encode()
    check('duplicate-id', f, False, 'finite-content-mismatch', LABEL)
    f = dict(files); d = decode(f[DATA]); d['source'] = 'S001'; f[DATA] = json.dumps(d).encode()
    check('wrong-source', f, False, 'finite-content-mismatch', LABEL)
    f = dict(files); f[SNAPSHOT] = f[SNAPSHOT].replace(b'Upholds=', b'UpholdsX=')
    check('snapshot-tampered', f, False, 'snapshot-digest', LABEL)
    f = dict(files)
    f[REGISTRY] = f[REGISTRY].replace(b'| docs |', b'| own-work |')
    check('own-work-source', f, False, 'source-unresolved', LABEL)
    f = dict(files); f[COMPANION] = b'# changed companion\n'
    check('companion-changed', f, False, 'review-not-bound', LABEL)
    f = dict(files); d = decode(f[DATA]); d['rows'][0]['quote'] = 'not in the source at all'
    f[DATA] = json.dumps(d).encode()
    check('quote-absent', f, False, 'finite-content-mismatch', LABEL)
    for path in (DATA, REVIEW, RESULTS):
        f = dict(files); del f[path]
        check('missing-' + Path(path).name, f, False, 'unreadable:KeyError', LABEL)
    f = dict(files); d = copy.deepcopy(results); d['results'][0]['agent'] = 'scribe'
    f[RESULTS] = json.dumps(d).encode()
    check('wrong-role', f, False, 'result-identity', LABEL)
    f = dict(files); d = copy.deepcopy(results); d['results'][0]['output'] = None
    f[RESULTS] = json.dumps(d).encode()
    check('lost-result', f, False, 'result-digest', LABEL)
    f = dict(files); d = copy.deepcopy(review); d['verdicts']['DP5'] = 'fails'
    f[REVIEW] = json.dumps(d).encode()
    check('failed-row', f, False, 'review-not-bound', LABEL)
    f = dict(files); d = copy.deepcopy(results)
    d['results'].append(copy.deepcopy(d['results'][0])); f[RESULTS] = json.dumps(d).encode()
    check('duplicate-result', f, False, 'result-identity', LABEL)
    print(f'SELFTEST total={len(checks)} passed={sum(checks)} failed={checks.count(False)}')
    return 0 if all(checks) else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--revision')
    group.add_argument('--root', type=Path)
    group.add_argument('--selftest', action='store_true')
    ap.add_argument('--branch', default='master')
    args = ap.parse_args()
    expected_raw = (ROOT / EXPECTED).read_bytes()
    expected = decode(expected_raw)
    if args.selftest:
        return selftest(expected, expected_raw)
    if args.root:
        def read(path):
            return (args.root / path).read_bytes()
        binding = None
    else:
        try:
            binding = bind(ROOT, args.revision, args.branch)
        except RevisionError as exc:
            print(f'DEPS_BINDING {exc.fid} {exc.site}: {exc.detail}')
            return 2
        sha = binding.sha

        def read(path):
            import subprocess
            from _revision import clean_env
            proc = subprocess.run(['git', '--no-pager', '-C', str(ROOT), 'show',
                                   f'{sha}:{path}'], stdin=subprocess.DEVNULL,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  env=clean_env(), timeout=60)
            if proc.returncode:
                raise FileNotFoundError('missing-blob')
            return proc.stdout
    count, ok, reason = score(read, expected)
    bind_field = '' if binding is None else f' revision={binding.sha} branch={binding.branch}'
    print(f'DEPS predicate="{LABEL}" rows={count} verified={TARGET_ROWS if ok else 0} '
          f'review={1 if ok else 0} met={int(ok)} reason={reason}{bind_field}')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
