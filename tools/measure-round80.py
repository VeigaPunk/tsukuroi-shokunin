#!/usr/bin/env python3
"""Finite round-80 evidence counter; not source entailment or review authenticity.
C1: 42 pinned restart cells with a digest-bound review file.
C2: two named tools expose own selftests and carry byte-bound execution receipts.
Exit 0 met, 1 unmet, 2 could-not-evaluate, 3 selftest failed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from _revision import bind, clean_env, RevisionError
ROOT = Path(__file__).resolve().parents[1]
BEFORE = '.ufo/waves/round-80/before/'
NOTE = 'corpus/knowledge/service-restart-matrix-r80.json'
COMPANION = 'corpus/knowledge/service-restart-matrix-r80.md'
REVIEW = '.ufo/waves/round-80/w1/ReviewMatrix/verdict.json'
TOOLS = ('count-kr-rows-r69.py', 'check-transaction-order-r39.py')
EXPECTED_SHA = '05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153'
SOURCE_SHA = '12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44'
def sha(data):
    return hashlib.sha256(data).hexdigest()
def evaluate(read, claim):
    try:
        if claim == 'C1':
            expected_bytes = read(BEFORE + 'expected.json')
            if sha(expected_bytes) != EXPECTED_SHA or sha(read(BEFORE + 'systemd.service.xml')) != SOURCE_SHA:
                return 0, 'snapshot_tampered'
            expected = json.loads(expected_bytes)
            data = read(NOTE)
            if json.loads(data) != expected:
                return 0, 'matrix-mismatch'
            registry = read('corpus/SOURCES.md').decode()
            rows = [line.split('|') for line in registry.splitlines() if line.lstrip().startswith('| S330 |')]
            if len(rows) != 1 or len(rows[0]) != 13:
                return 0, 'source-row'
            row = [c.strip() for c in rows[0]]
            if row[3] != 'docs' or row[4] != 'A' or row[8] != 'mined' or expected['url'] not in row[2] or NOTE not in row[11]:
                return 0, 'source-row'
            review = json.loads(read(REVIEW))
            if review != {'artifact_sha256': sha(data), 'companion_sha256': sha(read(COMPANION)), 'verdicts': ['holds'] * 6}:
                return 0, 'review-binding'
            return 42, 'met'
        skill = read('SKILL.md').decode()
        count = 0
        for name in TOOLS:
            path = 'tools/' + name
            # The current round71 registry is fixed, not a self-declared latest heading.
            section = skill.split('## Gate and probe registry — round71 superseding current rows\n', 1)[1].split('\n## ', 1)[0]
            rows = [line for line in section.splitlines() if line.startswith('| ' + name[:-3] + ' |')]
            if len(rows) != 1:
                continue
            cells = [c.strip() for c in rows[0].split('|')[1:-1]]
            if len(cells) != 8 or cells[1] != 'gate' or cells[4] != '`python3 ' + path + ' --selftest`' or '3 self-test failed' not in cells[3]:
                continue
            tool = read(path)
            receipt = json.loads(read('.ufo/waves/round-80/w1/' + name + '.receipt.json'))
            if b'--selftest' not in tool or b'SELFTEST' not in tool:
                continue
            if receipt.get('tool_sha256') != sha(tool) or receipt.get('argv') != ['python3', path, '--selftest'] or receipt.get('rc') != 0 or receipt.get('failed') != 0 or type(receipt.get('passed')) is not int or receipt['passed'] < 4:
                continue
            count += 1
        return count, 'met' if count == 2 else 'gate-standard'
    except (OSError, ValueError, KeyError, IndexError, TypeError, subprocess.CalledProcessError) as exc:
        return 0, 'missing-or-invalid:' + type(exc).__name__
def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--claim', choices=['C1', 'C2'])
    g = p.add_mutually_exclusive_group()
    g.add_argument('--revision')
    g.add_argument('--fixture', type=Path)
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        # Same reader, stable findings and rc asserted on absent evidence for both claims.
        results = [evaluate(lambda path: (_ for _ in ()).throw(FileNotFoundError(path)), c) == (0, 'missing-or-invalid:FileNotFoundError') for c in ['C1', 'C2']]
        print('SELFTEST total=2 passed=' + str(sum(results)) + ' failed=' + str(2-sum(results)))
        return 0 if all(results) else 3
    if not a.claim or not (a.revision or a.fixture):
        p.error('--claim and --revision or --fixture required')
    try:
        revision = bind(ROOT, a.revision, 'master').sha if a.revision else 'fixture'
        def read(path):
            if a.fixture:
                return (a.fixture / path).read_bytes()
            return subprocess.run(['git', '-C', str(ROOT), 'show', revision + ':' + path], env=clean_env(), check=True, capture_output=True).stdout
        count, finding = evaluate(read, a.claim)
        target = 42 if a.claim == 'C1' else 2
        print(json.dumps({'claim': a.claim, 'revision': revision, 'count': count, 'target': target, 'finding': finding, 'met': count == target}))
        return 0 if count == target else 1
    except RevisionError as exc:
        print(str(exc)); return 2
if __name__ == '__main__':
    sys.exit(main())
