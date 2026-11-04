#!/usr/bin/env python3
"""Read-only production attack; writes only CriticFreeze seat and scratch."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
SEAT = LANE / '.ufo/waves/round-78/w1/CriticFreeze'
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r78/CriticFreeze')
os.environ['TMPDIR'] = str(SCRATCH)
PREFIX = '.ufo/waves/round-78/'
FROZEN = '07a607df1a5157daafc91bb5c26858af14415f43'
DATA = 'corpus/knowledge/journald-path-usage-r78.json'
REVIEW = PREFIX + 'w1/ReviewUsage/verdict.json'
RESULTS = PREFIX + 'w1-results.json'
NOTE = 'corpus/knowledge/journald-path-usage-r78.md'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
encode = lambda obj: (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()
receipt = {'axes': ['depth', 'operability'], 'freeze': FROZEN, 'freeze_comparison': {}, 'calculations': [], 'attacks': []}
try:
    manifest = json.loads((LANE / PREFIX / 'before/frozen-digests.json').read_bytes())
    for path, want in manifest.items():
        proc = subprocess.run(['git', '-C', str(LANE), 'show', FROZEN + ':' + path], capture_output=True, check=True)
        actual = (LANE / path).read_bytes()
        receipt['freeze_comparison'][path] = {'frozen_sha256': sha(proc.stdout), 'worktree_sha256': sha(actual), 'manifest_sha256': want}
        assert sha(proc.stdout) == sha(actual) == want, path
    expected = json.loads((LANE / PREFIX / 'before/expected.json').read_bytes())
    rows = []
    for row in expected['cases']:
        accepted_suffix = row['name'].endswith(('.journal', '.journal~'))
        if not accepted_suffix:
            used, why = 0, 'suffix excludes before stat'
        elif not row['stat_ok']:
            used, why = 0, 'failed no-follow stat skips'
        elif row['kind'] != 'regular':
            used, why = 0, 'no-follow stat reports nonregular mode; skips'
        else:
            used, why = row['blocks'] * 512, str(row['blocks']) + ' * 512; apparent size ignored'
        receipt['calculations'].append({'id': row['id'], 'computed': used, 'expected': row['used'], 'reason': why})
        assert used == row['used']
        rows.append(dict(row, used=used))
    fixture = SCRATCH / 'fixture'
    def put(path, raw):
        target = fixture / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    for name in expected['pins']:
        put(PREFIX + 'before/' + name, (LANE / PREFIX / 'before' / name).read_bytes())
    data = encode({'source': ['S327'], 'cases': rows})
    review = encode({'reviewer': 'ReviewUsage', 'artifact_sha256': sha(data), 'verdicts': {row['id']: 'holds' for row in rows}})
    results = encode({'lane': 'tsukuroi', 'round': 78, 'wave': 'w1', 'results': [{'name': 'ReviewUsage', 'agent': 'reviewer', 'output': 'review_sha256=' + sha(review)}]})
    put(DATA, data)
    put(REVIEW, review)
    put(RESULTS, results)
    command = ['python3', str(LANE / 'tools/measure-journal-usage-r78.py'), '--root', str(fixture)]
    def attack(name, extra):
        proc = subprocess.run(command, capture_output=True, text=True)
        receipt['attacks'].append({'name': name, 'argv': command, 'exit_code': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr, **extra})
    bundle_bytes = {DATA: data.decode(), REVIEW: review.decode(), RESULTS: results.decode()}
    attack('fully-fabricated-review-and-orchestrator-bundle', {'exact_utf8_files': bundle_bytes})
    prose = b'# Deliberately false adversarial fixture\n\nThe manager follows journal symlinks and adds apparent st_size; directories count too. Failed stat entries contribute their apparent length.\n'
    put(NOTE, prose)
    attack('false-companion-with-exact-examples-and-fabricated-binding', {'exact_utf8_note': prose.decode(), 'note_path': NOTE, 'same_bundle_as': 'fully-fabricated-review-and-orchestrator-bundle'})
    false_review = json.loads(review)
    false_review['explanation'] = 'AT_SYMLINK_NOFOLLOW follows symlinks; st_blocks is apparent byte length.'
    false_review_raw = encode(false_review)
    false_results = json.loads(results)
    false_results['results'][0]['output'] = 'I did not review this source. review_sha256=' + sha(false_review_raw)
    put(REVIEW, false_review_raw)
    put(RESULTS, encode(false_results))
    attack('bound-review-with-explicitly-false-source-prose', {'exact_utf8_files': {REVIEW: false_review_raw.decode(), RESULTS: encode(false_results).decode()}})
    # Exercise the frozen coverage function only: no git fixture, no host commands.
    sys.path.insert(0, str(LANE / 'tools'))
    spec = importlib.util.spec_from_file_location('critic_registry', LANE / 'tools/check-registry-coverage.py')
    registry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(registry)
    path = 'tools/measure-journal-usage-r78.py'
    cells = ('false-command-example', 'gate', 'python3 ' + path + ' --invented-mode', '0 pass; 1 fail; 2 cannot-evaluate', 'none', 'frozen', 'none', 'CriticFreeze-fixture')
    class Reader:
        def read_file(self, revision, path):
            return (LANE / path).read_bytes()
    findings, covered = registry._coverage([{'cells': cells, 'line': 1}], {path}, Reader(), FROZEN)
    receipt['registry_subfunction_attack'] = {'function': '_coverage only, not whole C2 checker', 'cells': cells, 'findings': findings, 'covered': sorted(covered), 'unexecuted_false_command': cells[2], 'limitation': 'Literal path and verdict digits do not establish command truth. Frozen false-command kill rule still applies.'}
    registry._GIT_SANDBOX.cleanup()
finally:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    receipt['scratch_removed'] = not SCRATCH.exists()
    (SEAT / 'attack-receipt.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode())
print(json.dumps({'calculations': receipt['calculations'], 'attacks': [{k: a[k] for k in ('name', 'exit_code', 'stdout')} for a in receipt['attacks']], 'registry_subfunction_attack': receipt.get('registry_subfunction_attack'), 'scratch_removed': receipt['scratch_removed']}, indent=2))
