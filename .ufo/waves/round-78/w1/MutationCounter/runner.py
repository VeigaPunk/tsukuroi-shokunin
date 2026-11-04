#!/usr/bin/env python3
"""MutationCounter R78 — exercise the frozen C1 counter `--root` CLI on a
synthetic fixture, one mutation per case.

Production is read-only here: the runner copies the two pinned snapshot files
from the lane into an isolated fixture under $TMPDIR, builds synthetic
data/review/results bytes, mutates only fixture bytes, and invokes the frozen
counter at tools/measure-journal-usage-r78.py (blob-identical to frozen claim
commit 07a607df1a5157daafc91bb5c26858af14415f43). No git operations, no
registry selftest, no writes outside $TMPDIR.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
TOOL = LANE / 'tools/measure-journal-usage-r78.py'
SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-78/w1/MutationCounter')
PREFIX = '.ufo/waves/round-78/'
DATA_REL = 'corpus/knowledge/journald-path-usage-r78.json'
REVIEW_REL = PREFIX + 'w1/ReviewUsage/verdict.json'
RESULTS_REL = PREFIX + 'w1-results.json'
SCRATCH = Path(os.environ['TMPDIR'])
ZEROS = '0' * 64


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def build_baseline(fixture):
    """Fresh synthetic bundle: exact expected rows + self-consistent review."""
    if fixture.exists():
        shutil.rmtree(fixture)
    expected = json.loads((LANE / PREFIX / 'before/expected.json').read_bytes())
    for name in expected['pins']:
        dest = fixture / PREFIX / 'before' / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LANE / PREFIX / 'before' / name, dest)
    data_raw = (json.dumps({'source': expected['source'], 'cases': expected['cases']}, indent=2) + '\n').encode()
    data = fixture / DATA_REL
    data.parent.mkdir(parents=True, exist_ok=True)
    data.write_bytes(data_raw)
    review_raw = json.dumps({'reviewer': expected['reviewer'],
                             'artifact_sha256': digest(data_raw),
                             'verdicts': {r['id']: 'holds' for r in expected['cases']}}).encode()
    review = fixture / REVIEW_REL
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_bytes(review_raw)
    results_raw = json.dumps({'lane': 'tsukuroi', 'round': 78, 'wave': 'w1', 'results': [
        {'name': 'ReviewUsage', 'agent': 'reviewer',
         'output': 'verdict bound review_sha256=' + digest(review_raw)}]}).encode()
    results = fixture / RESULTS_REL
    results.write_bytes(results_raw)
    return expected, data_raw, review_raw, results_raw


def decode(raw):
    return json.loads(raw)


def set_bytes(fixture, rel, raw):
    path = fixture / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def run_counter(fixture):
    env = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
    p = subprocess.run([sys.executable, str(TOOL), '--root', str(fixture)],
                       cwd=str(SCRATCH), env=env, capture_output=True, text=True)
    m = re.search(r'count=(\d+) met=(\d) reason=(\S+)', p.stdout)
    parsed = {'count': int(m.group(1)), 'met': int(m.group(2)), 'reason': m.group(3)} if m else None
    return {'rc': p.returncode, 'stdout': p.stdout.strip(), 'stderr': p.stderr.strip(),
            'parsed': parsed}


def data_with(expected, mutate):
    doc = {'source': list(expected['source']), 'cases': json.loads(json.dumps(expected['cases']))}
    mutate(doc)
    return (json.dumps(doc, indent=2) + '\n').encode()


OK = (0, 1, 'finite-content-and-review')
CASES = [
    ('control-exact-synthetic', None, *OK),
    ('forged-wholesale-bundle', 'forged', *OK),
    ('mut-output-string', 'output', 1, 0, 'result-digest'),
    ('mut-case-U1-used-output', 'used-output', 1, 0, 'finite-content-mismatch'),
    ('mut-source-id', 'source', 1, 0, 'finite-content-mismatch'),
    ('mut-snapshot-digest', 'snapshot', 1, 0, 'snapshot-tampered'),
    ('mut-missing-review', 'missing-review', 1, 0, 'unreadable:FileNotFoundError'),
    ('mut-wrong-artifact-digest', 'artifact', 1, 0, 'review-not-bound'),
    ('mut-partly-holds', 'partly', 1, 0, 'review-not-bound'),
    ('mut-missing-results', 'missing-results', 1, 0, 'unreadable:FileNotFoundError'),
    ('mut-wrong-role', 'role', 1, 0, 'result-identity'),
    ('mut-wrong-name', 'name', 1, 0, 'result-identity'),
    ('mut-json-wrapped-digest-final', 'wrapped', *OK),
    ('mut-typed-json-output-object', 'typed-output', 1, 0, 'result-digest'),
    ('mut-null-output', 'null', 1, 0, 'result-digest'),
    ('mut-stale-review-after-whitespace-only-data-change', 'stale', 1, 0, 'review-not-bound'),
    ('recontrol-refreshed-binding-after-whitespace', 'refresh', *OK),
    ('mut-duplicate-json-key-data', 'dup-data', 1, 0, 'unreadable:ValueError'),
    ('mut-duplicate-json-key-results', 'dup-results', 1, 0, 'unreadable:ValueError'),
    ('mut-fixture-expected-json-ignored', 'poison-expected', *OK),
]


def apply_mutation(fixture, kind, expected, baseline):
    data_raw, review_raw, results_raw = baseline
    if kind is None:
        return
    if kind == 'used-output':
        doc = decode(data_raw)
        doc['cases'][0]['used'] += 1
        set_bytes(fixture, DATA_REL, json.dumps(doc).encode())
    elif kind == 'forged':
        fabricated_report = ('FABRICATED fixture prose: I reviewed six cases and all hold. '
                             'No review run occurred.')
        review2 = json.dumps({'reviewer': 'ReviewUsage',
                              'artifact_sha256': digest(data_raw),
                              'verdicts': {r['id']: 'holds' for r in expected['cases']},
                              'report': fabricated_report}).encode()
        set_bytes(fixture, REVIEW_REL, review2)
        forged = {'lane': 'tsukuroi', 'round': 78, 'wave': 'w1', 'results': [
            {'name': 'ScribeNote', 'agent': 'scribe', 'output': 'drafted note'},
            {'name': 'ExecSource', 'agent': 'executor', 'output': 'read journald-manager.c:119-131'},
            {'name': 'ReviewUsage', 'agent': 'reviewer',
             'output': 'FABRICATED final review_sha256=' + digest(review2)},
            {'name': 'CriticFreeze', 'agent': 'critic', 'output': 'no objection'},
        ]}
        set_bytes(fixture, RESULTS_REL, json.dumps(forged).encode())
    elif kind == 'output':
        d = decode(results_raw)
        d['results'][0]['output'] = 'verdict bound review_sha256=' + ZEROS
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'source':
        set_bytes(fixture, DATA_REL, data_with(expected, lambda doc: doc.update(source=['S999'])))
    elif kind == 'snapshot':
        set_bytes(fixture, PREFIX + 'before/journald-manager.c', b'tampered')
    elif kind == 'missing-review':
        (fixture / REVIEW_REL).unlink()
    elif kind == 'artifact':
        d = decode(review_raw)
        d['artifact_sha256'] = ZEROS
        set_bytes(fixture, REVIEW_REL, json.dumps(d).encode())
    elif kind == 'partly':
        d = decode(review_raw)
        d['verdicts']['U4'] = 'partly-holds'
        set_bytes(fixture, REVIEW_REL, json.dumps(d).encode())
    elif kind == 'missing-results':
        (fixture / RESULTS_REL).unlink()
    elif kind == 'role':
        d = decode(results_raw)
        d['results'][0]['agent'] = 'scribe'
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'name':
        d = decode(results_raw)
        d['results'][0]['name'] = 'ReviewUsage2'
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'wrapped':
        d = decode(results_raw)
        d['results'][0]['output'] = json.dumps(
            {'seat': 'ReviewUsage', 'final': 'review_sha256=' + digest(review_raw)})
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'typed-output':
        d = decode(results_raw)
        d['results'][0]['output'] = {'final': 'review_sha256=' + digest(review_raw)}
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'null':
        d = decode(results_raw)
        d['results'][0]['output'] = None
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'stale':
        set_bytes(fixture, DATA_REL, data_raw + b'\n')  # whitespace-only byte change
    elif kind == 'refresh':
        changed = data_raw + b'\n'
        set_bytes(fixture, DATA_REL, changed)
        r2 = json.dumps({'reviewer': expected['reviewer'],
                         'artifact_sha256': digest(changed),
                         'verdicts': {r['id']: 'holds' for r in expected['cases']}}).encode()
        set_bytes(fixture, REVIEW_REL, r2)
        d = decode(results_raw)
        d['results'][0]['output'] = 'verdict bound review_sha256=' + digest(r2)
        set_bytes(fixture, RESULTS_REL, json.dumps(d).encode())
    elif kind == 'dup-data':
        head, _, tail = data_raw.decode().partition('"cases"')
        dup = ('{"source": ["S327"], "source": ["S327"], "cases"' + tail).encode()
        set_bytes(fixture, DATA_REL, dup)
    elif kind == 'dup-results':
        raw = results_raw.decode()
        dup = raw.replace('{"lane"', '{"lane": "tsukuroi", "lane"', 1)
        set_bytes(fixture, RESULTS_REL, dup.encode())
    elif kind == 'poison-expected':
        poisoned = json.loads((LANE / PREFIX / 'before/expected.json').read_bytes())
        poisoned['target'] = 999
        poisoned['cases'][0]['used'] = 1
        set_bytes(fixture, PREFIX + 'before/expected.json',
                  json.dumps(poisoned, indent=2).encode())


def main():
    if not TOOL.exists():
        print('counter missing', file=sys.stderr)
        return 2
    fixture = SCRATCH / 'fixture'
    baseline = build_baseline(fixture)
    expected, data_raw, review_raw, results_raw = baseline
    chain = {'data_sha256': digest(data_raw), 'review_sha256': digest(review_raw),
             'results_sha256': digest(results_raw)}
    rows = []
    for pass_no in (1, 2):
        for name, kind, want_rc, want_met, want_reason in CASES:
            build_baseline(fixture)
            pristine_bytes = {str(p.relative_to(fixture)): p.read_bytes()
                              for p in fixture.rglob('*') if p.is_file()}
            before_hashes = {p: digest(raw) for p, raw in pristine_bytes.items()}
            pristine = run_counter(fixture)
            try:
                apply_mutation(fixture, kind, expected, baseline[1:])
                mutated_hashes = {str(p.relative_to(fixture)): digest(p.read_bytes())
                                  for p in fixture.rglob('*') if p.is_file()}
                result = run_counter(fixture)
            finally:
                shutil.rmtree(fixture)
                for rel, raw in pristine_bytes.items():
                    set_bytes(fixture, rel, raw)
            restored_hashes = {str(p.relative_to(fixture)): digest(p.read_bytes())
                               for p in fixture.rglob('*') if p.is_file()}
            restored = run_counter(fixture)
            result['pristine'] = pristine
            result['restored'] = restored
            result['hashes'] = {'before': before_hashes, 'mutated': mutated_hashes,
                                'restored': restored_hashes}
            result['exact_restoration'] = before_hashes == restored_hashes
            result['baseline_ok'] = pristine['rc'] == 0 and restored['rc'] == 0
            got = result['parsed']
            result['parsable'] = got is not None
            matches = (got is not None and result['rc'] == want_rc and got['met'] == want_met
                       and got['reason'] == want_reason and got['count'] == (6 if want_met else 0)
                       and result['exact_restoration'] and result['baseline_ok'])
            result['matches_expectation'] = matches
            rows.append({'pass': pass_no, 'case': name, 'want': {'rc': want_rc, 'met': want_met,
                                                                'reason': want_reason},
                         'observed': result})
            print(f"pass{pass_no} {name}: rc={result['rc']} "
                  f"reason={got['reason'] if got is not None else result['stdout']!r} "
                  f"match={matches}")
    a = [{k: r[k] for k in ('case', 'observed')} for r in rows if r['pass'] == 1]
    b = [{k: r[k] for k in ('case', 'observed')} for r in rows if r['pass'] == 2]
    stable = a == b
    mismatches = [r['case'] for r in rows if not r['observed']['matches_expectation']]
    out = {'fixture_digest_chain': chain, 'counter_sha256': digest(TOOL.read_bytes()),
           'stable_across_passes': stable, 'expectation_mismatches': mismatches, 'rows': rows}
    (SEAT / 'matrix.json').write_text(json.dumps(out, indent=2) + '\n')
    print(f"stable_across_passes={stable}")
    print('expectation_mismatches=' + json.dumps(mismatches))
    return 0 if stable and not mismatches else 1


if __name__ == '__main__':
    raise SystemExit(main())
