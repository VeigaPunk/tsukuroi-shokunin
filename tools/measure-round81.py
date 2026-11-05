#!/usr/bin/env python3
"""Round-81 C2 counter: does the round-80 evidence counter behave as a gate?

The claim is about behaviour, not about source shape: the exported `measure-round80.py`
is executed through its public CLI over six isolated fixture trees and each observed
(exit code, finding) is compared with the expected table frozen in
`.ufo/waves/round-81/before/gate-standard-r81.json`. A tool that merely *says* it maps
could-not-evaluate to exit 2 cannot pass this counter.

The export is materialised from the bound revision into a scratch directory that honours
TMPDIR and is removed before exit. Nothing in the lane tree is written.

Exit: 0 met / 1 unmet / 2 could-not-evaluate / 3 selftest failed.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
from _revision import bind, clean_env, RevisionError

ROOT = Path(__file__).resolve().parents[1]
TABLE = '.ufo/waves/round-81/before/gate-standard-r81.json'
TOOL = 'tools/measure-round80.py'
HELPER = 'tools/_revision.py'
FIXTURE_FILES = (
    '.ufo/waves/round-80/before/expected.json',
    '.ufo/waves/round-80/before/systemd.service.xml',
    'corpus/knowledge/service-restart-matrix-r80.json',
    'corpus/knowledge/service-restart-matrix-r80.md',
    '.ufo/waves/round-80/w1/ReviewMatrix/verdict.json',
    'corpus/SOURCES.md',
)
TARGET = 6


class CannotEvaluate(Exception):
    def __init__(self, finding):
        super().__init__(finding)
        self.finding = finding


def sha(data):
    return hashlib.sha256(data).hexdigest()


def materialise(read, dest):
    dest.mkdir(parents=True, exist_ok=True)
    for name in FIXTURE_FILES + (TOOL, HELPER):
        try:
            data = read(name)
        except (OSError, subprocess.CalledProcessError):
            raise CannotEvaluate('export-absent:' + name)
        target = dest / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    digests = {'expected': sha((dest / FIXTURE_FILES[0]).read_bytes()),
               'source': sha((dest / FIXTURE_FILES[1]).read_bytes())}
    (dest / 'digests.json').write_text(json.dumps(digests))


def run_case(work, name, spec, table):
    argv = [sys.executable, str(work / TOOL)] + list(spec['argv'])
    argv = [a.replace('{work}', str(work)) for a in argv]
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=180)
    body = (proc.stdout or '') + (proc.stderr or '')
    want = table[name]
    ok = proc.returncode == want['rc'] and want['token'] in body
    return ok, {'case': name, 'ok': ok, 'rc': proc.returncode, 'expected_rc': want['rc'],
                'token': want['token'], 'observed': body.strip()[:200]}


def evaluate(read, table=None):
    table = table if table is not None else json.loads(read(TABLE))
    cases = table['cases']
    scratch = Path(tempfile.mkdtemp(dir=tempfile.gettempdir(), prefix='r81gate-'))
    results = []
    try:
        pristine = scratch / 'pristine'
        materialise(read, pristine)
        for name in cases:
            spec = cases[name]
            work = scratch / name
            shutil.copytree(pristine, work)
            for mutation in spec.get('mutations', []):
                path = work / mutation['path']
                if mutation['action'] == 'unlink':
                    path.unlink()
                elif mutation['action'] == 'write':
                    path.write_text(mutation['text'])
                elif mutation['action'] == 'json-set':
                    data = json.loads(path.read_text())
                    for key in mutation['keys'][:-1]:
                        data = data[key]
                    data[mutation['keys'][-1]] = mutation['value']
                    path.write_text(json.dumps(data))
                else:
                    raise ValueError('unknown mutation ' + mutation['action'])
            ok, record = run_case(work, name, spec, cases)
            results.append(record)
            if not ok:
                pass
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    met = sum(1 for r in results if r['ok'])
    finding = 'met' if met == TARGET else 'gate-standard'
    return met, finding, results


def selftest():
    cases = []
    base = Path(tempfile.mkdtemp(dir=tempfile.gettempdir(), prefix='r81self-'))
    good_tool = '''import argparse, hashlib, json, sys
def sha(b): return hashlib.sha256(b).hexdigest()
p = argparse.ArgumentParser()
p.add_argument('--claim'); p.add_argument('--fixture'); p.add_argument('--digests'); p.add_argument('--selftest', action='store_true')
a = p.parse_args()
if a.selftest:
    print('SELFTEST total=6 passed=6 failed=0'); sys.exit(0)
if not a.claim or not a.fixture:
    print('usage error'); sys.exit(2)
digests = json.load(open(a.fixture + '/digests.json'))
try:
    expected_bytes = open(a.fixture + '/.ufo/waves/round-80/before/expected.json', 'rb').read()
    source_bytes = open(a.fixture + '/.ufo/waves/round-80/before/systemd.service.xml', 'rb').read()
except OSError:
    print(json.dumps({'finding': 'snapshot_absent'})); sys.exit(2)
if sha(expected_bytes) != digests['expected'] or sha(source_bytes) != digests['source']:
    print(json.dumps({'finding': 'snapshot_tampered'})); sys.exit(2)
matrix = open(a.fixture + '/corpus/knowledge/service-restart-matrix-r80.json', 'rb').read()
if matrix != expected_bytes:
    print(json.dumps({'finding': 'matrix-mismatch', 'met': False})); sys.exit(1)
print(json.dumps({'finding': 'met', 'met': True, 'count': 42})); sys.exit(0)
'''
    try:
        def build(dest, tool_text):
            (dest / 'tools').mkdir(parents=True, exist_ok=True)
            (dest / 'tools/measure-round80.py').write_text(tool_text)
            (dest / 'tools/_revision.py').write_text(
                'class RevisionError(Exception):\n    pass\n\n\n'
                'def bind(*args, **kwargs):\n    raise RevisionError("fixture")\n\n\n'
                'def clean_env():\n    return None\n')
            (dest / '.ufo/waves/round-80/before').mkdir(parents=True, exist_ok=True)
            (dest / 'corpus/knowledge').mkdir(parents=True, exist_ok=True)
            (dest / '.ufo/waves/round-80/w1/ReviewMatrix').mkdir(parents=True, exist_ok=True)
            expected = json.dumps({'settings': ['a'], 'rows': [], 'url': 'u'}).encode()
            (dest / '.ufo/waves/round-80/before/expected.json').write_bytes(expected)
            (dest / '.ufo/waves/round-80/before/systemd.service.xml').write_text('<refsect1><title>t</title></refsect1>\n')
            (dest / 'corpus/knowledge/service-restart-matrix-r80.json').write_bytes(expected)
            (dest / 'corpus/knowledge/service-restart-matrix-r80.md').write_text('c\n')
            (dest / '.ufo/waves/round-80/w1/ReviewMatrix/verdict.json').write_text('{}')
            (dest / 'corpus/SOURCES.md').write_text('')
            return dest

        table = {'cases': {
            'A-selftest': {'argv': ['--selftest'], 'rc': 0, 'token': 'SELFTEST total=6 passed=6 failed=0'},
            'B-met': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 0, 'token': '"met": true'},
            'C-mismatch': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 1, 'token': 'matrix-mismatch',
                           'mutations': [{'path': 'corpus/knowledge/service-restart-matrix-r80.json', 'action': 'json-set',
                                          'keys': ['url'], 'value': 'other'}]},
            'D-tampered': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 2, 'token': 'snapshot_tampered',
                           'mutations': [{'path': '.ufo/waves/round-80/before/expected.json', 'action': 'write', 'text': '{}'}]},
            'E-absent': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 2, 'token': 'snapshot_absent',
                         'mutations': [{'path': '.ufo/waves/round-80/before/systemd.service.xml', 'action': 'unlink'}]},
            'F-noargs': {'argv': [], 'rc': 2, 'token': ''},
        }}

        def check(name, tool_text, expect_met):
            tree = base / name
            build(tree, tool_text)
            table_path = tree / TABLE
            table_path.parent.mkdir(parents=True, exist_ok=True)
            table_path.write_text(json.dumps(table))
            try:
                met, finding, results = evaluate(lambda p: (tree / p).read_bytes())
            except CannotEvaluate as exc:
                cases.append((name, False, 'cannot-evaluate ' + exc.finding))
                return
            cases.append((name, met == expect_met, 'met=%d expected=%d %s' % (met, expect_met, results)))

        check('gate-conformant-double', good_tool, 6)
        broken = good_tool.replace("print(json.dumps({'finding': 'snapshot_absent'})); sys.exit(2)",
                                   "print(json.dumps({'finding': 'snapshot_absent'})); sys.exit(1)")
        broken = broken.replace("print(json.dumps({'finding': 'snapshot_tampered'})); sys.exit(2)",
                                "print(json.dumps({'finding': 'snapshot_tampered'})); sys.exit(1)")
        broken = broken.replace("print('SELFTEST total=6 passed=6 failed=0'); sys.exit(0)",
                                "print('SELFTEST total=2 passed=2 failed=0'); sys.exit(0)")
        check('defective-double', broken, 3)

        # Round-82 genuine-gap cases (recipes M04/M05/M07/M08 of
        # .ufo/waves/round-82/before/mutants-r82.json): each drives this counter's
        # own public CLI (--fixture) over an isolated export tree and asserts both
        # the exit code and the finding token. Production clauses above are only
        # observed here, never altered.
        def run_cli_case(name, tool_text, expect_rc, token, unlink=None):
            tree = base / name
            build(tree, tool_text)
            table_path = tree / TABLE
            table_path.parent.mkdir(parents=True, exist_ok=True)
            table_path.write_text(json.dumps(table))
            if unlink:
                (tree / unlink).unlink()
            env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
                   'TMPDIR': str(base / ('tmp-' + name)),
                   'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C.UTF-8'}
            Path(env['TMPDIR']).mkdir(parents=True, exist_ok=True)
            try:
                proc = subprocess.run(
                    [sys.executable, str(Path(__file__).resolve()),
                     '--fixture', str(tree)],
                    capture_output=True, text=True, timeout=300, env=env,
                    cwd=str(tree))
            except (subprocess.TimeoutExpired, OSError) as exc:
                cases.append((name, False, 'cli did not finish: %r' % (exc,)))
                return
            body = (proc.stdout or '') + (proc.stderr or '')
            ok = proc.returncode == expect_rc and token in body
            cases.append((name, ok, 'rc=%d expected_rc=%d token=%r observed=%r'
                          % (proc.returncode, expect_rc, token, body.strip()[:200])))

        # M04 (gate target is 6 conformant cases): a fully conformant tree is met, rc 0.
        run_cli_case('M04-six-of-six-met-cli', good_tool, 0, '"finding": "met"')
        # M04+M07 (a 5/6 tree is unmet and yields gate-standard, never met): break
        # exactly the mismatch leg so five cases pass and one fails.
        five_tool = good_tool.replace('if matrix != expected_bytes:', 'if False:')
        run_cli_case('M04-M07-five-of-six-gate-standard-cli', five_tool, 1,
                     '"finding": "gate-standard"')
        # M05 (unmet exits 1): 3/6 tree; the guarded clause is the exit code.
        run_cli_case('M05-unmet-exit-one-cli', broken, 1, '"finding": "gate-standard"')
        # M08 (missing export is could-not-evaluate rc 2, never met): remove one
        # export input the measured tool itself never reads.
        run_cli_case('M08-missing-export-could-not-evaluate-cli', good_tool, 2,
                     'export-absent:', unlink='corpus/SOURCES.md')
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
    g = p.add_mutually_exclusive_group()
    g.add_argument('--revision')
    g.add_argument('--fixture', type=Path)
    p.add_argument('--claim', default='C2', choices=['C2'])
    p.add_argument('--table', type=Path,
                   help='read the expected table from this file instead of the bound revision '
                        '(used only to measure a base revision that predates the table)')
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.revision or a.fixture):
        p.error('--revision or --fixture or --selftest required')
    try:
        revision = bind(ROOT, a.revision, 'master').sha if a.revision else 'fixture'

        def read(path):
            if a.fixture:
                return (a.fixture / path).read_bytes()
            return subprocess.run(['git', '-C', str(ROOT), 'show', revision + ':' + path],
                                  env=clean_env(), check=True, capture_output=True).stdout

        table = json.loads(a.table.read_text()) if a.table else None
        try:
            count, finding, results = evaluate(read, table)
        except CannotEvaluate as exc:
            print(json.dumps({'claim': 'C2', 'revision': revision, 'count': 0, 'target': TARGET,
                              'finding': exc.finding, 'cases': []}))
            return 2
        except (subprocess.CalledProcessError, OSError, ValueError, KeyError) as exc:
            print(json.dumps({'claim': 'C2', 'revision': revision, 'count': 0, 'target': TARGET,
                              'finding': 'cannot-evaluate:' + type(exc).__name__, 'cases': []}))
            return 2
        print(json.dumps({'claim': 'C2', 'revision': revision, 'count': count, 'target': TARGET,
                          'finding': finding, 'cases': results}))
        return 0 if count == TARGET else 1
    except RevisionError as exc:
        print(str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())
