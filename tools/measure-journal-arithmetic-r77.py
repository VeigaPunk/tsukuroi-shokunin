#!/usr/bin/env python3
"""C1: six pinned arithmetic vectors match; C2: three exact corrective blocks exist.

Finite content checks, not a general semantic oracle. Expected values are explicit
independent arithmetic examples; review establishes their upstream applicability.
Read-only: --revision reads committed bytes, --root reads an isolated fixture.
"""
import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = '.ufo/waves/round-77/before/expected.json'
DATA = 'corpus/knowledge/journald-space-arithmetic-r77.json'
LESSON = 'corpus/lessons/round-76.md'
LABELS = {'C1': 'six pinned arithmetic vectors match',
          'C2': 'three exact corrective blocks exist'}


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


def load_json(raw):
    return json.loads(raw, object_pairs_hook=unique)


def evaluate(read, expected, claim):
    if claim == 'C2':
        text = read(LESSON).decode()
        count = sum(block in text for block in expected['repairs'])
        return count, count == 3, 'blocks'
    for name, digest in expected['pins'].items():
        if hashlib.sha256(read('.ufo/waves/round-77/before/src/' + name)).hexdigest() != digest:
            raise ValueError('snapshot_tampered')
    data = load_json(read(DATA))
    if data.get('source') != ['S324', 'S325']:
        return 0, False, 'source'
    rows = data.get('rows')
    if not isinstance(rows, list) or len(rows) != 6:
        return 0, False, 'shape'
    count = sum(row == want and all(type(v) is int for k, v in row.items() if k != 'id')
                for row, want in zip(rows, expected['vectors']))
    return count, count == 6, 'vectors'


def selftest(expected):
    # Run the same reader/evaluator as the CLI, without touching the live tree.
    files = {'.ufo/waves/round-77/before/src/' + n: (ROOT / '.ufo/waves/round-77/before/src' / n).read_bytes()
             for n in expected['pins']}
    data = {'source': ['S324', 'S325'], 'rows': copy.deepcopy(expected['vectors'])}
    files[DATA] = json.dumps(data).encode()
    files[LESSON] = '\n'.join(expected['repairs']).encode()
    cases = []
    def check(name, claim, changed, wanted):
        try:
            count, ok, reason = evaluate(changed.__getitem__, expected, claim)
        except (ValueError, KeyError):
            ok, reason = False, 'unreadable'
        passed = ok == wanted
        cases.append(passed)
        print(f'SELFTEST {name} {"PASS" if passed else "FAIL"} expected={int(wanted)} observed={int(ok)} reason={reason}')
    check('control-vectors', 'C1', files, True)
    for i in range(6):
        changed = dict(files)
        mutant = copy.deepcopy(data)
        mutant['rows'][i]['avail'] += 1
        changed[DATA] = json.dumps(mutant).encode()
        check('wrong-output-' + str(i + 1), 'C1', changed, False)
    for name, value in [('empty', {'source': ['S324', 'S325'], 'rows': []}),
                        ('sourceless', {'source': [], 'rows': data['rows']}),
                        ('extra', {'source': data['source'], 'rows': data['rows'] + [data['rows'][0]]})]:
        changed = dict(files); changed[DATA] = json.dumps(value).encode()
        check(name, 'C1', changed, False)
    changed = dict(files); changed[DATA] = b'{"source":[],"source":["S324","S325"]}'
    check('duplicate', 'C1', changed, False)
    changed = dict(files); changed[next(iter(files))] = b'tampered'
    check('snapshot-tampered', 'C1', changed, False)
    check('control-repairs', 'C2', files, True)
    for i in range(3):
        changed = dict(files)
        changed[LESSON] = '\n'.join(b for j, b in enumerate(expected['repairs']) if i != j).encode()
        check('missing-repair-' + str(i + 1), 'C2', changed, False)
    print(f'SELFTEST total={len(cases)} passed={sum(cases)} failed={cases.count(False)}')
    return 0 if all(cases) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--revision')
    group.add_argument('--root', type=Path)
    group.add_argument('--selftest', action='store_true')
    parser.add_argument('--claim', choices=LABELS, default='C1')
    args = parser.parse_args()
    # The frozen expected specification belongs to the instrument revision.
    expected = load_json((ROOT / EXPECTED).read_bytes())
    if args.selftest:
        return selftest(expected)
    def read(path):
        if args.root:
            return (args.root / path).read_bytes()
        result = subprocess.run(['git', '-C', str(ROOT), 'show', args.revision + ':' + path],
                                capture_output=True, check=False)
        if result.returncode:
            raise ValueError('missing:' + path)
        return result.stdout
    try:
        count, ok, reason = evaluate(read, expected, args.claim)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'{args.claim} predicate="{LABELS[args.claim]}" count=0 met=0 reason={error}')
        return 1
    print(f'{args.claim} predicate="{LABELS[args.claim]}" count={count} met={int(ok)} reason={reason}')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
