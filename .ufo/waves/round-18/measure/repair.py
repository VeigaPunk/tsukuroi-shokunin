#!/usr/bin/env python3
"""Rerun only failed/affected round18 checks after the retained initial immutable run.
Usage: python3 <absolute-script> <new-landed-sha>
No live package/service/boot probe; all Git fixture writes stay in a private clone.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

LANE = Path(__file__).resolve().parents[4]
BASE = '842a5312b704b5cda10fd80ec1fdee5fb381ba97'
TIP = sys.argv[1]
OUT = Path(__file__).resolve().parent / 'repair'
OUT.mkdir(exist_ok=True)
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1', LC_ALL='C')
runs = []


def record(label, command, cwd):
    proc = subprocess.run(command, cwd=cwd, env=ENV, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=600)
    (OUT / (label + '.stdout')).write_text(proc.stdout)
    (OUT / (label + '.stderr')).write_text(proc.stderr)
    try:
        parsed = json.loads(proc.stdout)
    except ValueError:
        parsed = None
    runs.append({'label': label, 'command': command, 'exit': proc.returncode,
                 'measured_revision': TIP, 'stdout': label + '.stdout',
                 'stderr': label + '.stderr', 'json': parsed})
    (OUT / 'results.json').write_text(json.dumps({'initial_revision': 'c0f6303f35e15ce113c03f4b6592014b9d8c2472',
        'measured_revision': TIP, 'scope': 'failed or affected checks only; initial red evidence retained', 'runs': runs}, indent=2))
    print(label, proc.returncode, flush=True)


with tempfile.TemporaryDirectory(prefix='tsukuroi-r18-repair-measure-') as tmp:
    clone = Path(tmp) / 'lane'
    subprocess.run(['git', '-c', f'core.hooksPath={os.devnull}', 'clone', '--quiet', '--no-hardlinks', str(LANE), str(clone)], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'remote', 'remove', 'origin'], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', TIP], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'update-ref', 'refs/heads/master', TIP], env=ENV, check=True)
    record('selftest-check-recheck-commands-py', ['python3', 'tools/check-recheck-commands.py', '--selftest'], clone)
    record('selftest-check-seat-scope-py', ['python3', 'tools/check-seat-scope.py', '--selftest'], clone)
    record('c3-after', ['python3', 'tools/check-appended-notices.py', '--revision', TIP,
                      '--registry', 'corpus/knowledge/freshness-recheck-r18.json'], clone)
    record('c2-after', ['python3', 'tools/check-revision-binding.py', '--tools-revision', TIP], clone)
    record('recheck-aur-after', ['python3', 'tools/check-recheck-commands.py', '--revision', TIP,
                                '--paths', 'corpus/knowledge/aur-risk-plane.md'], clone)
    record('recheck-all-after', ['python3', 'tools/check-recheck-commands.py', '--revision', TIP], clone)
    record('exec-log-after', ['python3', 'tools/check-recheck-commands.py', '--revision', TIP,
                             '--exec-log', '.ufo/waves/round-18/l1-capture/host-capture-r18.txt'], clone)
    for wave in ['build', 'falsify']:
        record('seat-scope-' + wave, ['python3', 'tools/check-seat-scope.py', '--revision', TIP,
                                    '--wave', '.ufo/waves/round-18/' + wave], clone)
    # Reproduce final source rows and histograms against immutable before/after.
    census = {}
    for label, rev in [('before', BASE), ('after', TIP)]:
        text = subprocess.run(['git', '-C', str(clone), 'show', rev + ':corpus/SOURCES.md'],
                              env=ENV, capture_output=True, text=True, check=True).stdout
        rows = [line.split('|')[1:-1] for line in text.splitlines()
                if re.match(r'^\|\s*S[0-9]{3,}\s*\|', line)]
        tiers, statuses = {}, {}
        for row in rows:
            tiers[row[3].strip()] = tiers.get(row[3].strip(), 0) + 1
            statuses[row[7].strip()] = statuses.get(row[7].strip(), 0) + 1
        census[label] = {'revision': rev, 'rows': len(rows), 'tiers': tiers, 'statuses': statuses,
                        'source_sha256': hashlib.sha256(text.encode()).hexdigest()}
    (OUT / 'source-counts.json').write_text(json.dumps(census, indent=2))
    # The initial C1/legacy/protected/bytecode/source-mutant runs remain applicable
    # only where the committed exact inputs or the relevant protected prefix match.
    initial = 'c0f6303f35e15ce113c03f4b6592014b9d8c2472'
    fixed_inputs = ['tools/check-boot-chain.py', 'tools/_revision.py',
                    'tools/check-revision-binding.py', 'tools/check-appended-notices.py',
                    'corpus/knowledge/boot-chain-r17.md', 'corpus/knowledge/boot-chain-r17.json',
                    'corpus/knowledge/statement-corrections-r18.json',
                    '.ufo/waves/round-17/l1-capture/boot-chain-capture.txt',
                    'corpus/knowledge/freshness-recheck-r18.json', 'corpus/SOURCES.md']
    equality = {}
    for path in fixed_inputs:
        left = subprocess.run(['git', '-C', str(clone), 'show', initial + ':' + path], env=ENV, capture_output=True, check=True).stdout
        right = subprocess.run(['git', '-C', str(clone), 'show', TIP + ':' + path], env=ENV, capture_output=True, check=True).stdout
        equality[path] = {'same': left == right, 'initial_sha256': hashlib.sha256(left).hexdigest(),
                          'final_sha256': hashlib.sha256(right).hexdigest()}
    checks = {}
    for name in ['statement-corrections-r18.json', 'freshness-recheck-r18.json']:
        registry = json.loads((clone / 'corpus/knowledge' / name).read_text())
        for path in {r['path'] for r in registry['records']}:
            old = subprocess.run(['git', '-C', str(clone), 'show', BASE + ':' + path], env=ENV, capture_output=True, check=True).stdout
            checks[path] = (clone / path).read_bytes().startswith(old)
    (OUT / 'input-equality-and-history.json').write_text(json.dumps(
        {'initial_revision': initial, 'final_revision': TIP, 'exact_inputs': equality,
         'baseline_prefixes': checks, 'all_prefixes_preserved': all(checks.values())}, indent=2))
record('sources-census-end', ['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh', 'validate',
                            '--root', '/home/vgpnk/Projects/shokunin', 'tsukuroi'], LANE)
