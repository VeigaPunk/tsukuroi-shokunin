#!/usr/bin/env python3
"""Finite round-80 evidence counter; not source entailment or review authenticity.
C1: 42 pinned restart cells with a digest-bound review file.
C2: two named tools expose own selftests and carry byte-bound execution receipts.

Exit map (PROTOCOL Gate standard): 0 met, 1 unmet, 2 could-not-evaluate, 3 selftest failed.
A pinned input that is absent or no longer matches its digest is could-not-evaluate, never
"unmet": the claim's own artifact missing is unmet, the evidence the claim rests on being
absent or edited is not a verdict at all.

Round-81 repair (r80 closure routed defect 2): the could-not-evaluate class is now its own
exit code, and --selftest drives the public CLI over six isolated fixture trees instead of
calling the reader directly.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from _revision import bind, clean_env, RevisionError
ROOT = Path(__file__).resolve().parents[1]
BEFORE = '.ufo/waves/round-80/before/'
NOTE = 'corpus/knowledge/service-restart-matrix-r80.json'
COMPANION = 'corpus/knowledge/service-restart-matrix-r80.md'
REVIEW = '.ufo/waves/round-80/w1/ReviewMatrix/verdict.json'
TOOLS = ('count-kr-rows-r69.py', 'check-transaction-order-r39.py')
EXPECTED_SHA = '05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153'
SOURCE_SHA = '12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44'


class CannotEvaluate(Exception):
    """A pinned input the claim rests on is absent or no longer matches its digest."""

    def __init__(self, finding):
        super().__init__(finding)
        self.finding = finding


def sha(data):
    return hashlib.sha256(data).hexdigest()


def evaluate(read, claim, digests=None):
    want_expected = (digests or {}).get('expected', EXPECTED_SHA)
    want_source = (digests or {}).get('source', SOURCE_SHA)
    if claim == 'C1':
        try:
            expected_bytes = read(BEFORE + 'expected.json')
        except OSError:
            raise CannotEvaluate('snapshot_absent')
        if sha(expected_bytes) != want_expected:
            raise CannotEvaluate('snapshot_tampered')
        try:
            source_bytes = read(BEFORE + 'systemd.service.xml')
        except OSError:
            raise CannotEvaluate('snapshot_absent')
        if sha(source_bytes) != want_source:
            raise CannotEvaluate('snapshot_tampered')
        expected = json.loads(expected_bytes)
        try:
            data = read(NOTE)
        except OSError:
            return 0, 'note-absent'
        if json.loads(data) != expected:
            return 0, 'matrix-mismatch'
        registry = read('corpus/SOURCES.md').decode()
        rows = [line.split('|') for line in registry.splitlines() if line.lstrip().startswith('| S330 |')]
        if len(rows) != 1 or len(rows[0]) != 13:
            return 0, 'source-row'
        row = [c.strip() for c in rows[0]]
        if row[3] != 'docs' or row[4] != 'A' or row[8] != 'mined' or expected['url'] not in row[2] or NOTE not in row[11]:
            return 0, 'source-row'
        try:
            review = json.loads(read(REVIEW))
        except OSError:
            raise CannotEvaluate('review_absent')
        if review != {'artifact_sha256': sha(data), 'companion_sha256': sha(read(COMPANION)), 'verdicts': ['holds'] * 6}:
            return 0, 'review-binding'
        return 42, 'met'
    skill = read('SKILL.md').decode()
    marker = '## Gate and probe registry — round71 superseding current rows\n'
    if marker not in skill:
        return 0, 'gate-standard'
    count = 0
    for name in TOOLS:
        path = 'tools/' + name
        # The current round71 registry is fixed, not a self-declared latest heading.
        section = skill.split(marker, 1)[1].split('\n## ', 1)[0]
        rows = [line for line in section.splitlines() if line.startswith('| ' + name[:-3] + ' |')]
        if len(rows) != 1:
            continue
        cells = [c.strip() for c in rows[0].split('|')[1:-1]]
        if len(cells) != 8 or cells[1] != 'gate' or cells[4] != '`python3 ' + path + ' --selftest`' or '3 self-test failed' not in cells[3]:
            continue
        tool = read(path)
        try:
            receipt = json.loads(read('.ufo/waves/round-80/w1/' + name + '.receipt.json'))
        except OSError:
            raise CannotEvaluate('receipt_absent')
        if b'--selftest' not in tool or b'SELFTEST' not in tool:
            continue
        if receipt.get('tool_sha256') != sha(tool) or receipt.get('argv') != ['python3', path, '--selftest'] or receipt.get('rc') != 0 or receipt.get('failed') != 0 or type(receipt.get('passed')) is not int or receipt['passed'] < 4:
            continue
        count += 1
    return count, 'met' if count == 2 else 'gate-standard'


def selftest():
    cases = []
    matrix = {
        'settings': ['a', 'b'],
        'rows': [{'cause': 'x', 'restart': [True, False]}],
        'url': 'https://example.invalid/systemd.service.xml',
    }
    source = b'<refsect1><title>t</title></refsect1>\n'
    registry = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
                '|---|---|---|---|---|---|---|---|---|---|---|\n'
                '| S330 | systemd.service(5) — https://example.invalid/systemd.service.xml | docs | A | t | t | t '
                '| mined | 2026-11-04 | on-release | corpus/knowledge/service-restart-matrix-r80.json |\n')
    base = Path(tempfile.mkdtemp(dir=tempfile.gettempdir(), prefix='r80gate-'))
    try:
        def build(dest):
            (dest / BEFORE).mkdir(parents=True, exist_ok=True)
            (dest / 'corpus/knowledge').mkdir(parents=True, exist_ok=True)
            (dest / '.ufo/waves/round-80/w1/ReviewMatrix').mkdir(parents=True, exist_ok=True)
            expected = json.dumps(matrix, sort_keys=True).encode()
            (dest / (BEFORE + 'expected.json')).write_bytes(expected)
            (dest / (BEFORE + 'systemd.service.xml')).write_bytes(source)
            (dest / NOTE).write_bytes(expected)
            (dest / COMPANION).write_text('companion\n')
            (dest / 'corpus/SOURCES.md').write_text(registry)
            (dest / 'digests.json').write_text(json.dumps({'expected': sha(expected), 'source': sha(source)}))
            review = {'artifact_sha256': sha(expected),
                      'companion_sha256': sha((dest / COMPANION).read_bytes()),
                      'verdicts': ['holds'] * 6}
            (dest / REVIEW).write_text(json.dumps(review))
            return expected

        def run(name, claim, tree, expect_rc, expect_token, expect=None):
            proc = subprocess.run([sys.executable, __file__, '--claim', claim, '--fixture', str(tree),
                                   '--digests', str(tree / 'digests.json')],
                                  capture_output=True, text=True, timeout=120)
            body = (proc.stdout or '') + (proc.stderr or '')
            ok = proc.returncode == expect_rc and expect_token in body
            if ok and expect is not None:
                ok = expect in body
            cases.append((name, ok, 'rc=%d body=%s' % (proc.returncode, body.strip()[:160])))

        good = base / 'good'
        expected = build(good)
        run('met', 'C1', good, 0, '"finding": "met"', '"count": 42')

        mismatch = base / 'mismatch'
        build(mismatch)
        broken = dict(matrix)
        broken['rows'] = [{'cause': 'x', 'restart': [False, False]}]
        (mismatch / NOTE).write_bytes(json.dumps(broken, sort_keys=True).encode())
        run('matrix-mismatch', 'C1', mismatch, 1, '"finding": "matrix-mismatch"')

        tampered = base / 'tampered'
        build(tampered)
        (tampered / (BEFORE + 'expected.json')).write_bytes(json.dumps({'settings': [], 'rows': []}).encode())
        run('expected-tampered', 'C1', tampered, 2, '"finding": "snapshot_tampered"')

        gone = base / 'gone'
        build(gone)
        (gone / (BEFORE + 'systemd.service.xml')).unlink()
        run('snapshot-absent', 'C1', gone, 2, '"finding": "snapshot_absent"')

        note_gone = base / 'note-gone'
        build(note_gone)
        (note_gone / NOTE).unlink()
        run('note-absent', 'C1', note_gone, 1, '"finding": "note-absent"')

        bare = base / 'bare'
        build(bare)
        (bare / 'SKILL.md').write_text('# no registry section\n')
        run('c2-gate-standard', 'C2', bare, 1, '"finding": "gate-standard"')
    finally:
        shutil.rmtree(base, ignore_errors=True)
    failed = [c for c in cases if not c[1]]
    print('SELFTEST total=%d passed=%d failed=%d' % (len(cases), len(cases) - len(failed), len(failed)))
    for name, ok, detail in cases:
        if not ok:
            print('FAIL %s %s' % (name, detail))
    return 0 if not failed else 3


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--claim', choices=['C1', 'C2'])
    g = p.add_mutually_exclusive_group()
    g.add_argument('--revision')
    g.add_argument('--fixture', type=Path)
    p.add_argument('--digests', type=Path,
                   help='fixture-mode only: override the pinned digests (the revision path never reads it)')
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not a.claim or not (a.revision or a.fixture):
        p.error('--claim and --revision or --fixture required')
    try:
        revision = bind(ROOT, a.revision, 'master').sha if a.revision else 'fixture'

        def read(path):
            if a.fixture:
                return (a.fixture / path).read_bytes()
            return subprocess.run(['git', '-C', str(ROOT), 'show', revision + ':' + path],
                                  env=clean_env(), check=True, capture_output=True).stdout

        digests = json.loads(a.digests.read_text()) if (a.digests and a.fixture) else None
        try:
            count, finding = evaluate(read, a.claim, digests)
        except CannotEvaluate as exc:
            print(json.dumps({'claim': a.claim, 'revision': revision, 'count': 0,
                              'target': 42 if a.claim == 'C1' else 2, 'finding': exc.finding, 'met': False}))
            return 2
        except (subprocess.CalledProcessError, OSError, ValueError, KeyError, IndexError, TypeError) as exc:
            print(json.dumps({'claim': a.claim, 'revision': revision, 'count': 0,
                              'target': 42 if a.claim == 'C1' else 2,
                              'finding': 'cannot-evaluate:' + type(exc).__name__, 'met': False}))
            return 2
        target = 42 if a.claim == 'C1' else 2
        print(json.dumps({'claim': a.claim, 'revision': revision, 'count': count, 'target': target,
                          'finding': finding, 'met': count == target}))
        return 0 if count == target else 1
    except RevisionError as exc:
        print(str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())
