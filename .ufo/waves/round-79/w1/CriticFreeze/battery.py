#!/usr/bin/env python3
"""Round-79 w1 CriticFreeze battery: fixture attacks against the two frozen counters.

Every attack is a fixture mirror under /fast/scratch/hyaku/tsukuroi-r79/CriticFreeze/
run against the real lane counters with --root <fixture>.  No lane file is edited.
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
BASE = '9086589a82f221d130ed6711fbe70b85f0d07aea'
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r79/CriticFreeze')
FIX = SCRATCH / 'fixtures'
OUT = SCRATCH / 'out'
TMP = SCRATCH / 'tmp'
C1 = ['/usr/bin/python3', str(LANE / 'tools/measure-unit-deps-r79.py')]
C2 = ['/usr/bin/python3', str(LANE / 'tools/check-gate-standard-r79.py')]
ENV = dict(os.environ)
ENV.update({'TMPDIR': str(TMP), 'PYTHONDONTWRITEBYTECODE': '1'})

HEADER = ('Name', 'Kind', 'Entry command', 'Verdict map', 'Self-test',
          'Pinned values', 'Write scope', 'Owner')
E_DATA = '.ufo/waves/round-79/before/expected.json'
E_SNAP = '.ufo/waves/round-79/before/src/systemd.unit.xml'
DATA = 'corpus/knowledge/systemd-dependency-propagation-r79.json'
COMPANION = 'corpus/knowledge/systemd-dependency-propagation-r79.md'
REVIEW = '.ufo/waves/round-79/w1/ReviewDeps/verdict.json'
RESULTS = '.ufo/waves/round-79/w1-results.json'
REGISTRY = 'corpus/SOURCES.md'
S329 = ('| S329 | systemd.unit(5) v262 — https://raw.githubusercontent.com/systemd/'
        'systemd/v262/man/systemd.unit.xml | docs | A | unit dependency directives | '
        'man/systemd.unit.xml v262, anchors 663-940 | each directive row is quoted from the '
        'pinned snapshot | mined | 2026-11-04 | on-release | '
        'corpus/knowledge/systemd-dependency-propagation-r79.md |')
S329_BOGUS = ('| S329 | systemd.unit.xml (claimed, unverified — not a URL) | blog | ? | x | '
              'no anchor recorded | y | idea | ? | never | |')

records = []


def git(*args):
    return subprocess.run(['git', '--no-pager', '-C', str(LANE), *args],
                          capture_output=True, env=ENV, timeout=120)


def base_bytes(path):
    p = git('show', f'{BASE}:{path}')
    if p.returncode:
        return None
    return p.stdout


def put(root, rel, content):
    dst = root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        content = content.encode()
    dst.write_bytes(content)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def tree_digest(root):
    h = hashlib.sha256()
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        h.update(p.relative_to(root).as_posix().encode() + b'\0')
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def new_root(name):
    root = FIX / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    return root


def frozen_inputs(root):
    put(root, E_DATA, (LANE / E_DATA).read_bytes())
    put(root, E_SNAP, (LANE / E_SNAP).read_bytes())


def base_mirror(name):
    """Counter read-set at the frozen base revision."""
    root = new_root(name)
    for rel in ('SKILL.md', REGISTRY,
                'tools/check-r71-routed-r72.py', 'tools/count-md-rows-r72.py'):
        b = base_bytes(rel)
        assert b is not None, rel
        put(root, rel, b)
    frozen_inputs(root)
    return root


def expected_obj():
    return json.loads((LANE / E_DATA).read_text())


def data_bytes(rows=None, source=None):
    exp = expected_obj()
    obj = {'source': exp['source'] if source is None else source,
           'rows': exp['rows'] if rows is None else rows}
    return (json.dumps(obj, indent=1, ensure_ascii=False) + '\n').encode()


def bundle(root, data=None, companion=b'# systemd dependency propagation (r79)\n',
           verdicts=None, results=None, review=None):
    """Write data/companion and a review+result bundle bound to them."""
    data = data_bytes() if data is None else data
    put(root, DATA, data)
    put(root, COMPANION, companion)
    if review is None:
        review = {'reviewer': 'ReviewDeps',
                  'artifact_sha256': digest(data),
                  'companion_sha256': digest(companion),
                  'verdicts': verdicts or {r['id']: 'holds' for r in expected_obj()['rows']}}
    rv = (json.dumps(review, indent=1) + '\n').encode()
    put(root, REVIEW, rv)
    if results is None:
        results = {'lane': 'tsukuroi', 'round': 79, 'wave': 'w1', 'results': [
            {'name': 'ReviewDeps', 'agent': 'reviewer',
             'output': 'review_sha256=' + digest(rv)}]}
    put(root, RESULTS, (json.dumps(results, indent=1) + '\n').encode())
    return rv


def registry_with_s329(root, row=S329):
    put(root, REGISTRY, base_bytes(REGISTRY) + ('\n' + row + '\n').encode())


def row_line(cells):
    return '| ' + ' | '.join(cells) + ' |'


def table(rows):
    return ['| ' + ' | '.join(HEADER) + ' |', '|' + '---|' * len(HEADER)] + \
           [row_line(r) for r in rows]


GOOD_GATE = ('check-r71-routed-r72', 'gate',
             '`python3 tools/check-r71-routed-r72.py --revision <REV>`',
             '0 clean; 1 stale; 2 could-not-evaluate; 3 self-test failed',
             '`python3 tools/check-r71-routed-r72.py --selftest`',
             'pin', 'reads', 'tsukuroi')
GOOD_MD = ('count-md-rows-r72', 'gate',
           '`python3 tools/count-md-rows-r72.py --revision <REV>`',
           '0 met; 1 missed; 2 could-not-evaluate; 3 self-test failed',
           '`python3 tools/count-md-rows-r72.py --selftest`',
           'pin', 'reads', 'tsukuroi')
LATE = ('measure-unit-deps-r79', 'gate',
        '`python3 tools/measure-unit-deps-r79.py --revision <REV>`',
        '0 met; 1 missed; 2 could-not-evaluate; 3 self-test failed',
        '`python3 tools/measure-unit-deps-r79.py --selftest`',
        'pin', 'reads', 'tsukuroi')
STUB_SELFTEST = ('#!/usr/bin/env python3\n'
                 '"""fixture tool with a real self-test mode."""\n'
                 'import argparse\n'
                 'ap = argparse.ArgumentParser()\n'
                 'ap.add_argument("--revision")\n'
                 'ap.add_argument("--selftest", action="store_true")\n'
                 'a = ap.parse_args()\n'
                 'if a.selftest:\n'
                 '    print("SELFTEST: PASS (fixture)")\n')
STUB_NOSELFTEST = ('#!/usr/bin/env python3\n'
                   '"""fixture tool with no self-test mode at all."""\n'
                   'import sys\n'
                   'print("ran")\n'
                   'sys.exit(0)\n')


def c2_root(name, skill, blobs):
    root = new_root(name)
    put(root, 'SKILL.md', skill)
    for rel, content in blobs.items():
        put(root, rel, content)
    return root


def clean_skill(operative_rows=(GOOD_GATE, GOOD_MD, LATE), extra=(), operative='round79'):
    lines = ['# fixture', '',
             f'## Gate and probe registry — {operative} superseding current rows', '']
    lines += table(operative_rows)
    lines.append('')
    for heading, marker, rows in extra:
        lines.append(heading)
        if marker:
            lines.append('> NON-OPERATIVE — carried for history; the operative table is the '
                         'sole current registry.')
        lines += table(rows)
        lines.append('')
    return '\n'.join(lines) + '\n'


def run(name, target, argv, expectation, note, root, extra_files=None):
    rc = subprocess.run(argv + ['--root', str(root)], capture_output=True, text=True,
                        env=ENV, timeout=300)
    out, err = rc.stdout.strip(), rc.stderr.strip()
    lines = [l for l in out.splitlines() if l.startswith(('DEPS ', 'GATE_STANDARD '))]
    findings = [l for l in out.splitlines() if re.match(r'^[A-Z][A-Z-]+ [^:]+: ', l)]
    accepted = rc.returncode == 0
    rec = {
        'attack': name,
        'target': target,
        'intent': note,
        'expectation': expectation,
        'fixture': str(root),
        'mirror_sha256': tree_digest(root),
        'files': sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()),
        'argv': argv + ['--root', str(root)],
        'rc': rc.returncode,
        'counter_line': lines[-1] if lines else None,
        'other_counter_lines': lines[:-1],
        'findings': findings,
        'stderr': err[-800:],
        'outcome': 'survive' if accepted else 'kill',
        'expected_outcome': expectation,
        'agrees': (accepted == (expectation == 'survive')),
    }
    if extra_files:
        rec['extra_files'] = extra_files
    records.append(rec)
    print(json.dumps({k: rec[k] for k in ('attack', 'target', 'rc', 'outcome', 'agrees')}))
    print('   ', rec['counter_line'])
    return rec


def main():
    for d in (FIX, OUT, TMP):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    exp = expected_obj()
    rows = exp['rows']

    # ---------- A1: do-nothing base tree ----------
    r = base_mirror('A1-base')
    run('A1-base-c1', 'C1', C1, 'kill',
        'do-nothing: frozen base mirror, no target artifact', r)
    run('A1-base-c2', 'C2', C2, 'kill',
        'do-nothing: frozen base mirror, unrepaired registry', r)

    # ---------- A2: marker-only (data + companion, no verdict/results) ----------
    r = new_root('A2-marker-only')
    for rel in ('SKILL.md', REGISTRY):
        put(r, rel, base_bytes(rel))
    frozen_inputs(r)
    put(r, DATA, data_bytes())
    put(r, COMPANION, b'# marker only\n')
    registry_with_s329(r)
    run('A2-marker-only', 'C1', C1, 'kill',
        'exact data.json + companion, no verdict.json and no w1 results', r)

    # ---------- A3: fabricated review bundle ----------
    r = new_root('A3-fabricated-bundle')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    bundle(r)
    run('A3-fabricated-bundle', 'C1', C1, 'survive',
        'correct digests and eight holds; no evidence the reviewer read anything', r)

    # ---------- A5: nine rows / wrong line / quote swap / duplicate id ----------
    r = new_root('A5a-nine-rows')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    nine = [dict(x) for x in rows] + [dict(rows[-1], id='DP9')]
    bundle(r, data=data_bytes(rows=nine))
    run('A5a-nine-rows', 'C1', C1, 'kill', 'nine rows instead of the eight frozen rows', r)

    r = new_root('A5b-wrong-line')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    wrong = [dict(x) for x in rows]
    wrong[2]['line'] = '714-715'
    bundle(r, data=data_bytes(rows=wrong))
    run('A5b-wrong-line', 'C1', C1, 'kill',
        'DP3 line shifted one token line (713-715 -> 714-715)', r)

    r = new_root('A5c-quote-swap')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    swap = [dict(x) for x in rows]
    swap[0]['quote'], swap[0]['line'] = rows[1]['quote'], rows[1]['line']
    bundle(r, data=data_bytes(rows=swap))
    run('A5c-quote-swap', 'C1', C1, 'kill',
        'DP1 carries DP2 quote+line: a real, locatable quote in the wrong row', r)

    r = new_root('A5d-duplicate-id')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    dup = [dict(x) for x in rows]
    dup[1]['id'] = 'DP1'
    bundle(r, data=data_bytes(rows=dup))
    run('A5d-duplicate-id', 'C1', C1, 'kill', 'DP1 id used twice, eight rows total', r)

    # ---------- A7: answer-key writer ----------
    r = new_root('A7-answer-key')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    writer = SCRATCH / 'A7' / 'answerkey_writer.py'
    writer.parent.mkdir(parents=True, exist_ok=True)
    writer.write_text(ANSWERKEY_WRITER)
    w = subprocess.run(['/usr/bin/python3', str(writer), str(r), str(LANE / E_DATA)],
                       capture_output=True, text=True, env=ENV, timeout=120)
    print('   writer rc=', w.returncode, w.stdout.strip()[-200:])
    run('A7-answer-key', 'C1', C1, 'survive',
        'writer copies expected.json rows into data.json and fabricates the review',
        r, extra_files={'writer': str(writer), 'writer_sha256': digest(writer.read_bytes()),
                        'writer_rc': w.returncode, 'writer_stdout': w.stdout.strip()})

    # ---------- A8: duplicate-key JSON ----------
    r = new_root('A8-duplicate-key')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    bundle(r)
    raw = (r / DATA).read_bytes().decode()
    raw = raw.replace('"source": "S329",', '"source": "S329", "source": "S329",', 1)
    put(r, DATA, raw)
    run('A8-duplicate-key', 'C1', C1, 'kill',
        'data.json repeats the source key; strict decode must refuse', r)

    # ---------- A9: source row absent ----------
    r = new_root('A9-no-source-row')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    bundle(r)
    run('A9-no-source-row', 'C1', C1, 'kill',
        'exact data + bundle, but S329 is not resolvable in corpus/SOURCES.md', r)

    # ---------- A10: snapshot tampered ----------
    r = new_root('A10-snapshot-tampered')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r)
    put(r, E_SNAP, (LANE / E_SNAP).read_bytes().replace(b'Upholds=', b'UpholdsX='))
    bundle(r)
    run('A10-snapshot-tampered', 'C1', C1, 'kill',
        'exact data + bundle, but the fixture snapshot bytes are altered', r)

    # ---------- A15: source row resolved by substring only ----------
    r = new_root('A15-bogus-source-row')
    put(r, REGISTRY, base_bytes(REGISTRY))
    frozen_inputs(r)
    registry_with_s329(r, row=S329_BOGUS)
    bundle(r)
    run('A15-bogus-source-row', 'C1', C1, 'survive',
        'S329 row is junk (kind blog, no anchor, no URL) but its source cell contains the '
        'snapshot name', r)

    # ---------- A11: locate consistency of the frozen rows ----------
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'c1mod', LANE / 'tools/measure-unit-deps-r79.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules['c1mod'] = mod
    spec.loader.exec_module(mod)
    snap = (LANE / E_SNAP).read_bytes()
    located = {row['id']: {'recorded': row['line'],
                           'computed': mod.locate(snap, row['quote']),
                           'tokens': len(row['quote'].split())} for row in rows}
    a11 = {k: v for k, v in located.items()}
    print('A11 locate:', json.dumps(a11))

    # ---------- C2 family ----------
    r = base_mirror('A1-base')  # reuse for the base C2 arm already run above
    blobs_ok = {'tools/check-r71-routed-r72.py': STUB_SELFTEST,
                'tools/count-md-rows-r72.py': STUB_SELFTEST}
    blobs_base = {'tools/check-r71-routed-r72.py': base_bytes('tools/check-r71-routed-r72.py'),
                  'tools/count-md-rows-r72.py': base_bytes('tools/count-md-rows-r72.py')}

    # A0 positive control: a clean repaired registry
    root0 = c2_root('A0-clean-registry',
                    clean_skill(extra=[('## Round 72 — continuation', True, [LATE])]),
                    blobs_ok)
    run('A0-clean-registry', 'C2', C2, 'survive',
        'positive control: zero duplicates, both frozen rows gate-standard', root0)

    # A4 lying registry: rows claim --selftest, base tool blobs have none
    root4 = c2_root('A4-lying-registry',
                    clean_skill(extra=[('## Round 72 — continuation', True, [LATE])]),
                    blobs_base)
    run('A4-lying-registry', 'C2', C2, 'kill',
        'registry rows advertise --selftest while the tool blobs carry no self-test', root4)

    # A6 duplicates left unmarked
    root6 = c2_root('A6-unmarked-duplicate',
                    clean_skill(extra=[('## Round 72 — continuation', False, [LATE])]),
                    blobs_ok)
    run('A6-unmarked-duplicate', 'C2', C2, 'kill',
        'a current continuation row repeats tools/measure-unit-deps-r79.py with no marker',
        root6)

    # A12 genuinely current duplicate marked NON-OPERATIVE
    dup_rows = [LATE, ('check-r71-routed-r72', 'gate',
                       '`python3 tools/check-r71-routed-r72.py --revision <REV>`',
                       '0 clean; 1 stale; 2 could-not-evaluate; 3 self-test failed',
                       '`python3 tools/check-r71-routed-r72.py --selftest`',
                       'pin', 'reads', 'tsukuroi')]
    root12 = c2_root('A12-marked-live-duplicate',
                     clean_skill(extra=[('## Round 79 — duplicate block', True, dup_rows)]),
                     blobs_ok)
    run('A12-marked-live-duplicate', 'C2', C2, 'survive',
        'the second table repeats a current tool yet declares itself NON-OPERATIVE; the '
        'marker is the only authority', root12)

    # A13 false interface: self-test cell names a nonexistent tool
    bad_selftest = []
    for r0, ghost in ((GOOD_GATE, 'does-not-exist-a-r79.py'),
                      (GOOD_MD, 'does-not-exist-b-r79.py')):
        c = list(r0)
        c[4] = f'`{r0[0]}` — `python3 tools/{ghost} --selftest`'
        bad_selftest.append(tuple(c))
    root13 = c2_root('A13-nonexistent-selftest-tool',
                     clean_skill(operative_rows=tuple(bad_selftest),
                                 extra=[('## Round 72 — continuation', True, [LATE])]),
                     blobs_ok)
    run('A13-nonexistent-selftest-tool', 'C2', C2, 'survive',
        'self-test cells name tools/does-not-exist-r79.py; no existence check runs', root13)

    # A14 minimal verdict map
    thin = []
    for r0 in (GOOD_GATE, GOOD_MD):
        c = list(r0)
        c[3] = '3 self-test failed'
        thin.append(tuple(c))
    root14 = c2_root('A14-thin-verdict-map',
                     clean_skill(operative_rows=tuple(thin),
                                 extra=[('## Round 72 — continuation', True, [LATE])]),
                     blobs_ok)
    run('A14-thin-verdict-map', 'C2', C2, 'survive',
        'verdict maps carry only code 3; 0/1/2 are absent and not checked', root14)

    # A17 heading-text collision: a post-operative table reuses an earlier heading string
    skill17 = '\n'.join(
        ['# fixture', '',
         '## Round 72 — continuation', '> NON-OPERATIVE — history.']
        + table([LATE]) + ['']
        + ['## Gate and probe registry — round79 superseding current rows']
        + table([GOOD_GATE, GOOD_MD]) + ['']
        + ['## Round 72 — continuation']
        + table([GOOD_GATE]) + ['']) + '\n'
    root17 = c2_root('A17-heading-text-collision', skill17, blobs_ok)
    run('A17-heading-text-collision', 'C2', C2, 'survive',
        'a post-operative table that reuses an earlier heading string is dropped as '
        '"before the operative heading" and its duplicate row is never counted', root17)

    # A17b: byte-identical rows, only the repeated heading text made unique
    skill17b = '\n'.join(
        ['# fixture', '',
         '## Round 72 — continuation', '> NON-OPERATIVE — history.']
        + table([LATE]) + ['']
        + ['## Gate and probe registry — round79 superseding current rows']
        + table([GOOD_GATE, GOOD_MD]) + ['']
        + ['## Round 73 — continuation']
        + table([GOOD_GATE]) + ['']) + '\n'
    root17b = c2_root('A17b-unique-heading', skill17b, blobs_ok)
    run('A17b-unique-heading', 'C2', C2, 'kill',
        'same duplicate row as A17 but under a heading string used once; isolates the '
        'cause to heading-text identity', root17b)

    # A18: retire duplicates by moving the operative boundary forward
    hist = [('check-r72-routed-r73', 'gate',
             '`python3 tools/check-r72-routed-r73.py --revision <REV>`',
             '0 clean; 1 stale; 2 could-not-evaluate; 3 self-test failed',
             '`python3 tools/check-r72-routed-r73.py --selftest`', 'p', 'reads', 'tsukuroi'),
            ('check-r72-routed-r73', 'gate',
             '`python3 tools/check-r72-routed-r73.py --revision <REV>`',
             '0 clean; 1 stale; 2 could-not-evaluate; 3 self-test failed',
             '`python3 tools/check-r72-routed-r73.py --selftest`', 'p', 'reads', 'tsukuroi'),
            ('count-jd-rows-r76', 'gate',
             '`python3 tools/count-jd-rows-r76.py --revision <REV>`',
             '0 met; 1 missed; 2 could-not-evaluate; 3 self-test failed',
             '`python3 tools/count-jd-rows-r76.py --selftest`', 'p', 'reads', 'tsukuroi'),
            ('count-jd-rows-r76', 'gate',
             '`python3 tools/count-jd-rows-r76.py --revision <REV>`',
             '0 met; 1 missed; 2 could-not-evaluate; 3 self-test failed',
             '`python3 tools/count-jd-rows-r76.py --selftest`', 'p', 'reads', 'tsukuroi')]
    skill18 = ('# fixture\n\n'
               '## Gate and probe registry — round78 superseding current rows\n'
               + '\n'.join(table(hist)) + '\n\n'
               '## Gate and probe registry — round79 superseding current rows\n'
               + '\n'.join(table([GOOD_GATE, GOOD_MD])) + '\n')
    root18 = c2_root('A18-operative-boundary-moved', skill18, blobs_ok)
    run('A18-operative-boundary-moved', 'C2', C2, 'survive',
        'six duplicate rows survive in the document; a new highest-numbered operative '
        'heading makes them all historical without any NON-OPERATIVE marker', root18)

    payload = {'round': 79, 'wave': 'w1', 'seat': 'CriticFreeze',
               'frozen': {'base': BASE,
                          'expected_sha256': digest((LANE / E_DATA).read_bytes()),
                          'snapshot_sha256': digest((LANE / E_SNAP).read_bytes())},
               'locate_consistency': a11,
               'attacks': records}
    (OUT / 'attacks.json').write_text(json.dumps(payload, indent=1) + '\n')
    print('wrote', OUT / 'attacks.json', len(records), 'runs')


ANSWERKEY_WRITER = '''#!/usr/bin/env python3
"""Attack A7: a writer with no systemd knowledge that copies the frozen answer key.

Reads before/expected.json, emits data.json with the rows verbatim, a one-line
companion, a verdict bound to the two digests with eight `holds`, and a w1
result whose output is exactly `review_sha256=<digest>`.  Reads nothing else.
"""
import hashlib
import json
import sys
from pathlib import Path

root, expected_path = Path(sys.argv[1]), Path(sys.argv[2])
PREFIX = '.ufo/waves/round-79/'
expected = json.loads(expected_path.read_text())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def put(rel, data):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode())


data = (json.dumps({'source': expected['source'], 'rows': expected['rows']},
                   indent=1, ensure_ascii=False) + '\\n').encode()
put('corpus/knowledge/systemd-dependency-propagation-r79.json', data)
companion = b'# copied\\n'
put('corpus/knowledge/systemd-dependency-propagation-r79.md', companion)
review = {'reviewer': 'ReviewDeps', 'artifact_sha256': sha(data),
          'companion_sha256': sha(companion),
          'verdicts': {r['id']: 'holds' for r in expected['rows']}}
rv = (json.dumps(review, indent=1) + '\\n').encode()
put(PREFIX + 'w1/ReviewDeps/verdict.json', rv)
put(PREFIX + 'w1-results.json',
    json.dumps({'lane': 'tsukuroi', 'round': 79, 'wave': 'w1',
                'results': [{'name': 'ReviewDeps', 'agent': 'reviewer',
                             'output': 'review_sha256=' + sha(rv)}]}, indent=1) + '\\n')
print('wrote rows=' + str(len(expected['rows'])))
'''

if __name__ == '__main__':
    main()
