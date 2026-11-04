#!/usr/bin/env python3
"""Execute round-81 controls. These are author trials, not a backdated pre-data freeze."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
BASE = '96ad75b84160da58efaee4997576ce718fd72e2b'
WAVE = ROOT / '.ufo/waves/round-81'
SCRATCH = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'tsukuroi-r81/l1-controls'
SCRATCH.mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
records = []

def run(name, argv, expect_rc, expect_count=None, token=None):
    proc = subprocess.run(argv, cwd=ROOT, env=ENV, capture_output=True, text=True, timeout=300)
    body = proc.stdout + proc.stderr
    count = None
    try:
        result = json.loads(proc.stdout)
        count = result.get('count', result.get('finding_count'))
    except ValueError:
        result = None
    ok = proc.returncode == expect_rc
    if expect_count is not None:
        ok = ok and count == expect_count
    if token is not None:
        ok = ok and token in body
    records.append(dict(name=name, argv=list(map(str, argv)), expected_rc=expect_rc,
                        expected_count=expect_count, expected_token=token,
                        rc=proc.returncode, count=count, stdout=proc.stdout, stderr=proc.stderr,
                        holds=ok))

def get(revision, path):
    return subprocess.run(['git', '-C', str(ROOT), 'show', revision + ':' + path],
                          capture_output=True, check=True).stdout

work = Path(tempfile.mkdtemp(dir=SCRATCH, prefix='controls-'))
try:
    for tool in ['count-mount-rows-r81.py', 'measure-round81.py']:
        run(tool + '-selftest', [sys.executable, str(ROOT / 'tools' / tool), '--selftest'], 0,
            token='failed=0')
    # Capture the exact actual production identities before a registry-derived control.
    skill = get(BASE, 'SKILL.md').decode()
    marker = '## Gate and probe registry — round71 superseding current rows\n'
    section = skill.split(marker, 1)[1].split('\n## ', 1)[0]
    identities = [line for line in section.splitlines()
                  if 'tools/measure-round80.py ' in line or 'tools/check-transaction-order-r39.py ' in line]
    (WAVE / 'before/actual-registry-identities.json').write_text(json.dumps(identities, indent=2) + '\n')

    # Actual base C2 counter and C3 header gate, not invented registry labels.
    run('no-work-C2', [sys.executable, str(ROOT / 'tools/measure-round81.py'), '--revision', BASE,
                       '--table', str(WAVE / 'before/gate-standard-r81.json')], 1, 3)
    run('no-work-C3', [sys.executable, str(ROOT / 'tools/check-knowledge-header.py'), '--revision', BASE],
        1, 2, 'KNOWLEDGE-HEADER-VALUE')

    # C1 base mirror plus this round's immutable input snapshots; note remains absent.
    before = work / 'before'
    (before / 'corpus').mkdir(parents=True)
    (before / 'corpus/SOURCES.md').write_bytes(get(BASE, 'corpus/SOURCES.md'))
    shutil.copytree(WAVE / 'before/src', before / '.ufo/waves/round-81/before/src')
    shutil.copytree(WAVE / 'before/host', before / '.ufo/waves/round-81/before/host')
    run('no-work-C1-input-overlay', [sys.executable, str(ROOT / 'tools/count-mount-rows-r81.py'),
                                     '--fixture', str(before)], 1, 0, 'note-absent')

    # The positive uses the real candidate path, registry rows and captured source bytes.
    good = work / 'positive'
    shutil.copytree(before, good)
    (good / 'corpus/SOURCES.md').write_bytes((ROOT / 'corpus/SOURCES.md').read_bytes())
    (good / 'corpus/knowledge').mkdir()
    note = 'corpus/knowledge/mount-unit-fstab-plane-r81.json'
    (good / note).write_bytes((ROOT / note).read_bytes())
    run('actual-identity-C1-positive', [sys.executable, str(ROOT / 'tools/count-mount-rows-r81.py'),
                                        '--fixture', str(good)], 0, 8, '"finding": "met"')
    for name, action in [('wrong-quote', 'quote'), ('own-work-rule', 'source'),
                         ('missing-measured', 'measured'), ('tampered-snapshot', 'tamper')]:
        tree = work / name
        shutil.copytree(good, tree)
        data = json.loads((tree / note).read_text())
        if action == 'quote':
            data['rows'][0]['quote'] = 'a claim that is not present in the snapshot'
        elif action == 'source':
            data['rows'][0]['source'] = 'S332'
        elif action == 'measured':
            for row in data['rows']:
                row.pop('measured', None)
        else:
            (tree / '.ufo/waves/round-81/before/src/systemd.mount.xml').write_text('edited\n')
        (tree / note).write_text(json.dumps(data))
        count = 0 if action == 'tamper' else 8 if action == 'measured' else 7
        run(name, [sys.executable, str(ROOT / 'tools/count-mount-rows-r81.py'), '--fixture', str(tree)],
            2 if action == 'tamper' else 1, count)

    run('candidate-C2-positive', [sys.executable, str(ROOT / 'tools/measure-round81.py'),
                                    '--fixture', str(ROOT)], 0, 6, '"finding": "met"')
    for name, script in [('blanket-green', 'import json\nprint(json.dumps({"met": True,"finding":"met","count":42}))\n'),
                         ('blanket-refusal', 'import sys\nprint("snapshot_tampered")\nsys.exit(2)\n')]:
        tree = work / name
        (tree / 'tools').mkdir(parents=True)
        (tree / 'tools/measure-round80.py').write_text(script)
        (tree / 'tools/_revision.py').write_bytes((ROOT / 'tools/_revision.py').read_bytes())
        paths = ['.ufo/waves/round-80/before/expected.json',
                 '.ufo/waves/round-80/before/systemd.service.xml',
                 'corpus/knowledge/service-restart-matrix-r80.json',
                 'corpus/knowledge/service-restart-matrix-r80.md',
                 '.ufo/waves/round-80/w1/ReviewMatrix/verdict.json', 'corpus/SOURCES.md']
        for path in paths:
            target = tree / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(get(BASE, path))
        target = tree / '.ufo/waves/round-81/before/gate-standard-r81.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((WAVE / 'before/gate-standard-r81.json').read_bytes())
        run(name, [sys.executable, str(ROOT / 'tools/measure-round81.py'), '--fixture', str(tree)],
            1, 1 if name == 'blanket-green' else 2)

    receipt = dict(base=BASE, chronology='Author trials and candidate scoring occurred BEFORE declaration; no pre-data freeze is claimed.',
                   hashes={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                           for p in ['tools/count-mount-rows-r81.py', 'tools/measure-round81.py',
                                     '.ufo/waves/round-81/before/gate-standard-r81.json']},
                   records=records)
    (WAVE / 'before/controls.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'holds': sum(r['holds'] for r in records), 'total': len(records),
                      'failures': [r['name'] for r in records if not r['holds']]}))
finally:
    shutil.rmtree(work, ignore_errors=True)
