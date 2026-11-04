#!/usr/bin/env python3
"""Round-79 pre-data controls (run before any wave seat scores data).

Arms, each receipted with argv, rc and the counter's summary line:
  1 selftest-depth / 2 base-depth   the C1 instrument's own cases and the do-nothing base
  3 scripted-fetch-fill            a mechanical writer that fetches the source and fills rows
                                   without reading it, plus a bound review bundle
  4 sourceless                     eight exact rows under the wrong source id
  5 nine-rows                      the exact row set plus a ninth duplicate-shaped row
  6 no-review                      exact data and companion, review/report bundle absent
  7 selftest-gate-standard / 8 base-gate-standard  the C2 instrument and the do-nothing base

Scratch lives under $HYAKU_SCRATCH/tsukuroi-r79/l1 (default /fast/scratch/hyaku),
never /tmp; the private tree is removed on exit.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WAVE = '.ufo/waves/round-79'
EXPECTED = WAVE + '/before/expected.json'
SNAPSHOT = WAVE + '/before/src/systemd.unit.xml'
DATA = 'corpus/knowledge/systemd-dependency-propagation-r79.json'
COMPANION = 'corpus/knowledge/systemd-dependency-propagation-r79.md'
REGISTRY = 'corpus/SOURCES.md'
REVIEW = WAVE + '/w1/ReviewDeps/verdict.json'
RESULTS = WAVE + '/w1-results.json'
DEPTH = ROOT / 'tools/measure-unit-deps-r79.py'
GATE = ROOT / 'tools/check-gate-standard-r79.py'
BASE = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'master'],
                      capture_output=True, text=True).stdout.strip()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def scripted_rows(expected):
    """QUALITY 81 arm: fetch the pinned source and fill rows mechanically, no reading."""
    lines = Path(ROOT / SNAPSHOT).read_text(encoding='utf-8').splitlines()
    rows = []
    for index, row in enumerate(expected['rows'], 1):
        needle = '<varname>' + row['directive'] + '</varname>'
        start = next(i for i, line in enumerate(lines) if needle in line)
        quote = lines[start + 1].strip()
        words = quote.split()
        rows.append({'id': f'DP{index}', 'directive': row['directive'],
                     'statement': ' '.join(words[:14]) + ' (scripted)',
                     'source': 'S329', 'snapshot': 'systemd.unit.xml',
                     'digest': row['digest'], 'line': str(start + 2),
                     'quote': quote})
    return rows


def build(root, expected_raw, expected, data_rows, with_review=True):
    root.mkdir(parents=True, exist_ok=True)
    (root / EXPECTED).parent.mkdir(parents=True, exist_ok=True)
    (root / SNAPSHOT).parent.mkdir(parents=True, exist_ok=True)
    (root / 'corpus/knowledge').mkdir(parents=True, exist_ok=True)
    (root / WAVE / 'w1/ReviewDeps').mkdir(parents=True, exist_ok=True)
    (root / EXPECTED).write_bytes(expected_raw)
    shutil.copyfile(ROOT / SNAPSHOT, root / SNAPSHOT)
    registry = (ROOT / REGISTRY).read_text(encoding='utf-8')
    if '| S329 |' not in registry:
        registry = registry.rstrip('\n') + (
            '\n| S329 | systemd.unit(5) — https://raw.githubusercontent.com/systemd/systemd/'
            'v262/man/systemd.unit.xml | docs | A | u | systemd.unit.xml | t | mined | '
            '2026-11-04 | on-release | fixture |\n')
    (root / REGISTRY).write_text(registry, encoding='utf-8')
    (root / COMPANION).write_bytes(b'# scripted companion\n')
    data = json.dumps({'source': 'S329', 'rows': data_rows}, indent=1,
                      ensure_ascii=False).encode() + b'\n'
    (root / DATA).write_bytes(data)
    if not with_review:
        return
    review = {'reviewer': 'ReviewDeps', 'artifact_sha256': digest(data),
              'companion_sha256': digest((root / COMPANION).read_bytes()),
              'verdicts': {row['id']: 'holds' for row in expected['rows']}}
    review_raw = json.dumps(review).encode()
    (root / REVIEW).write_bytes(review_raw)
    results = {'lane': 'tsukuroi', 'round': 79, 'wave': 'w1', 'results': [
        {'name': 'ReviewDeps', 'agent': 'reviewer',
         'output': 'review_sha256=' + digest(review_raw)}]}
    (root / RESULTS).write_bytes(json.dumps(results).encode())


def receipt(arm, argv, proc):
    tail = [line for line in proc.stdout.splitlines() if line.strip()][-2:]
    return {'arm': arm, 'argv': argv, 'rc': proc.returncode,
            'summary': tail, 'tool': str(argv[1]) if len(argv) > 1 else ''}


def main():
    scratch_root = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'tsukuroi-r79/l1'
    scratch_root.mkdir(parents=True, exist_ok=True)
    if str(scratch_root).startswith('/tmp'):
        print('HARNESS-BAD-SCRATCH: refusing /tmp')
        return 2
    work = Path(tempfile.mkdtemp(prefix='controls-', dir=scratch_root))
    receipts = []
    try:
        expected_raw = (ROOT / EXPECTED).read_bytes()
        expected = json.loads(expected_raw)
        valid_rows = expected['rows']

        def run(arm, argv):
            proc = subprocess.run(argv, capture_output=True, text=True)
            receipts.append(receipt(arm, argv, proc))
            print(f'{arm} rc={proc.returncode} {receipt(arm, argv, proc)["summary"]}')

        py = sys.executable
        run('selftest-depth', [py, str(DEPTH), '--selftest'])
        run('base-depth', [py, str(DEPTH), '--revision', BASE])
        for name, rows, review in (
                ('scripted-fetch-fill', scripted_rows(expected), True),
                ('sourceless', [dict(row, source='S001') for row in valid_rows], True),
                ('nine-rows', valid_rows + [dict(valid_rows[-1], id='DP9')], True),
                ('no-review', valid_rows, False)):
            mirror = work / name
            build(mirror, expected_raw, expected, rows, with_review=review)
            run(name, [py, str(DEPTH), '--root', str(mirror)])
        run('selftest-gate-standard', [py, str(GATE), '--selftest'])
        run('base-gate-standard', [py, str(GATE), '--revision', BASE])
        out = ROOT / WAVE / 'before/controls.json'
        out.write_text(json.dumps({'base': BASE, 'arms': receipts}, indent=1) + '\n')
        print(f'controls={len(receipts)} half={str(out)}')
        failed = [r['arm'] for r in receipts if r['arm'].startswith(('selftest', 'base'))
                  and r['rc'] not in (0, 1)]
        return 1 if failed else 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    raise SystemExit(main())
