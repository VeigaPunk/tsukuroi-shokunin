#!/usr/bin/env python3
"""One isolated fixture; actual frozen CLI only; baseline/mutant/restore per case."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
SEAT = LANE / '.ufo/waves/round-77/w1/MutationFinite'
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r77/MutationFinite')
FROZEN = 'eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5'
TOOL = LANE / 'tools/measure-journal-arithmetic-r77.py'
EXPECTED = LANE / '.ufo/waves/round-77/before/expected.json'
DATA = 'corpus/knowledge/journald-space-arithmetic-r77.json'
LESSON = 'corpus/lessons/round-76.md'
PREFIX = '.ufo/waves/round-77/before/src/'
sha = lambda b: hashlib.sha256(b).hexdigest()
def committed(path):
    return subprocess.run(['git', '-C', str(LANE), 'show', FROZEN + ':' + path], check=True, capture_output=True).stdout

assert not SCRATCH.exists(), 'Refuse to replace an existing fixture'
expected_bytes = EXPECTED.read_bytes()
tool_bytes = TOOL.read_bytes()
assert tool_bytes == committed('tools/measure-journal-arithmetic-r77.py')
assert expected_bytes == committed('.ufo/waves/round-77/before/expected.json')
expected = json.loads(expected_bytes)
data = {'source': ['S324', 'S325'], 'rows': copy.deepcopy(expected['vectors'])}
encode = lambda obj: (json.dumps(obj, indent=2) + '\n').encode()
pristine = {DATA: encode(data), LESSON: ('\n\n'.join(expected['repairs']) + '\n').encode()}
for name, digest in expected['pins'].items():
    raw = (LANE / PREFIX / name).read_bytes()
    assert sha(raw) == digest
    pristine[PREFIX + name] = raw
cases = []
for i, row in enumerate(data['rows']):
    for field in ('avail', 'limit', 'available'):
        mutated = copy.deepcopy(data)
        mutated['rows'][i][field] += 1
        cases.append((f'{row["id"]}-{field}-plus-one', 'C1', DATA, encode(mutated)))
for i, row in enumerate(data['rows']):
    for field in row:
        if field == 'id':
            continue
        mutated = copy.deepcopy(data)
        mutated['rows'][i][field] = bool(row[field])
        cases.append((f'{row["id"]}-{field}-bool-for-int', 'C1', DATA, encode(mutated)))
mutated = copy.deepcopy(data); mutated['rows'].append(copy.deepcopy(mutated['rows'][0]))
cases.append(('extra-row', 'C1', DATA, encode(mutated)))
mutated = copy.deepcopy(data); mutated['rows'][0], mutated['rows'][1] = mutated['rows'][1], mutated['rows'][0]
cases.append(('reordered-rows', 'C1', DATA, encode(mutated)))
cases.append(('duplicate-json-key', 'C1', DATA, pristine[DATA].replace(b'"source": [', b'"source": [], "source": [', 1)))
mutated = copy.deepcopy(data); mutated['source'] = []
cases.append(('empty-source-list', 'C1', DATA, encode(mutated)))
for name in expected['pins']:
    cases.append(('empty-snapshot-' + name, 'C1', PREFIX + name, b''))
for i in range(3):
    cases.append((f'missing-corrective-block-{i + 1}', 'C2', LESSON, ('\n\n'.join(b for j, b in enumerate(expected['repairs']) if j != i) + '\n').encode()))
cases.append(('marker-only-strings', 'C2', LESSON, ('\n'.join(b.split(':', 1)[0] for b in expected['repairs']) + '\n').encode()))
receipt = {'axes': {'depth': 8, 'freshness': 9}, 'frozen_revision': FROZEN,
           'tool_sha256_before': sha(tool_bytes), 'expected_sha256_before': sha(expected_bytes),
           'fixture': str(SCRATCH / 'fixture'), 'tmpdir': str(SCRATCH / 'tmp'),
           'pristine_hashes': {p: sha(b) for p, b in pristine.items()}, 'cases': [], 'live_controls': []}
SCRATCH.mkdir(parents=True)
ROOT = SCRATCH / 'fixture'
(SCRATCH / 'tmp').mkdir()
env = dict(os.environ, TMPDIR=str(SCRATCH / 'tmp'), PYTHONDONTWRITEBYTECODE='1')
def put(path, raw):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
def hashes():
    return {p: sha((ROOT / p).read_bytes()) for p in pristine}
def run(claim, root=ROOT):
    argv = ['/usr/bin/python3', str(TOOL), '--root', str(root), '--claim', claim]
    result = subprocess.run(argv, env=env, cwd=str(SCRATCH), capture_output=True, text=True, timeout=15)
    return {'command': argv, 'cwd': str(SCRATCH), 'TMPDIR': env['TMPDIR'], 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
try:
    for path, raw in pristine.items():
        put(path, raw)
    for claim in ('C1', 'C2'):
        receipt['live_controls'].append({'kind': 'isolated-valid-fixture', 'claim': claim, **run(claim)})
        receipt['live_controls'].append({'kind': 'read-only-current-lane-root', 'claim': claim, **run(claim, LANE)})
    for name, claim, path, mutated in cases:
        case = {'name': name, 'claim': claim, 'path': path, 'before_hashes': hashes(), 'baseline': run(claim), 'mutated_bytes_utf8': mutated.decode(), 'mutated_sha256': sha(mutated)}
        try:
            put(path, mutated)
            case['mutated_hashes'] = hashes()
            case['mutant'] = run(claim)
        finally:
            put(path, pristine[path])
            case['restored_hashes'] = hashes()
            case['restored'] = run(claim)
        case['exact_restoration'] = case['before_hashes'] == case['restored_hashes'] == receipt['pristine_hashes']
        case['verdict'] = ('inconclusive' if case['baseline']['exit_code'] != 0 or case['restored']['exit_code'] != 0 or not case['exact_restoration'] else 'killed' if case['mutant']['exit_code'] != 0 else 'survived')
        receipt['cases'].append(case)
    receipt['should_fail_total'] = len(cases)
    receipt['should_fail_accepted'] = sum(c['mutant']['exit_code'] == 0 for c in receipt['cases'])
    receipt['killed'] = sum(c['verdict'] == 'killed' for c in receipt['cases'])
    receipt['inconclusive'] = sum(c['verdict'] == 'inconclusive' for c in receipt['cases'])
    receipt['tool_sha256_after'] = sha(TOOL.read_bytes())
    receipt['expected_sha256_after'] = sha(EXPECTED.read_bytes())
    receipt['final_fixture_hashes'] = hashes()
finally:
    shutil.rmtree(SCRATCH)
    receipt['scratch_deleted'] = not SCRATCH.exists()
    (SEAT / 'receipts.json').write_text(json.dumps(receipt, indent=2) + '\n')
    (SEAT / 'fixture-descriptor.json').write_text(json.dumps({'root': str(ROOT), 'files': receipt['pristine_hashes'], 'data': data, 'repairs': expected['repairs'], 'source_copies_only': list(expected['pins']), 'mutation_names': [c[0] for c in cases]}, indent=2) + '\n')
print(json.dumps({k: receipt[k] for k in ('should_fail_total', 'should_fail_accepted', 'killed', 'inconclusive', 'scratch_deleted')}, sort_keys=True))
print(json.dumps(receipt['live_controls'], indent=2))
