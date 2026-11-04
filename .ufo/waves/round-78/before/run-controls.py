#!/usr/bin/env python3
"""Pre-data controls. Scratch only; the production target is never written."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LANE = Path(__file__).resolve().parents[4]
BASE = 'b9019a1d0558241bf67cf31ff90256284d8657af'
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r78/L1Controls')
SCRATCH.mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE='1')
OUT = Path(__file__).resolve().parent
TOOL = LANE / 'tools/measure-journal-usage-r78.py'
rows = []

def run(name, argv):
    p = subprocess.run(argv, cwd=LANE, env=ENV, capture_output=True, text=True)
    result = {'name': name, 'argv': list(map(str, argv)), 'exit_code': p.returncode,
              'stdout': p.stdout, 'stderr': p.stderr}
    rows.append(result)
    print(name, p.returncode, p.stdout[-200:].strip())
    return p

try:
    run('selftest', [sys.executable, str(TOOL), '--selftest'])
    run('C1-do-nothing', [sys.executable, str(TOOL), '--revision', BASE])
    run('C2-do-nothing', [sys.executable, str(LANE/'tools/check-registry-coverage.py'), '--revision', BASE])
    fixture = SCRATCH/'writer'; fixture.mkdir()
    for name in ('journald-manager.c', 'journalctl.xml'):
        dest = fixture/'.ufo/waves/round-78/before'/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(OUT/name, dest)
    spec = json.loads((OUT/'expected.json').read_text())
    # Fetch-and-fill control reads the source, computes examples, copies no reviewer judgment.
    source = (OUT/'journald-manager.c').read_text()
    assert 'AT_SYMLINK_NOFOLLOW' in source and 'st.st_blocks * 512UL' in source
    cases = spec['cases']
    for case in cases:
        case['used'] = case['blocks']*512 if case['name'].endswith(('.journal','.journal~')) and case['kind']=='regular' and case['stat_ok'] else 0
    data = fixture/'corpus/knowledge/journald-path-usage-r78.json'; data.parent.mkdir(parents=True)
    data.write_text(json.dumps({'source':['S327'], 'cases':cases}, indent=2)+'\n')
    run('scripted-fetch-fill-no-review', [sys.executable, str(TOOL), '--root', str(fixture)])
    review = fixture/'.ufo/waves/round-78/w1/ReviewUsage/verdict.json'; review.parent.mkdir(parents=True)
    review.write_text(json.dumps({'reviewer':'ReviewUsage','artifact_sha256':hashlib.sha256(data.read_bytes()).hexdigest(),'verdicts':{r['id']:'holds' for r in cases}}))
    run('fabricated-review-without-orchestrator-result', [sys.executable, str(TOOL), '--root', str(fixture)])
    (OUT/'controls.json').write_text(json.dumps(rows, indent=2)+'\n')
finally:
    shutil.rmtree(SCRATCH)
