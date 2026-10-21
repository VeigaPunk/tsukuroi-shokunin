#!/usr/bin/env python3
"""Round20 L1-only retained evaluation; no host probes or live-tree Git writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

BASE = '0cbc34dd6b20896085a8fb07943e3ea4027d8472'
LANE = Path(__file__).resolve().parents[4]
ROOT = LANE / '.ufo/waves/round-20/measure'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_OPTIONAL_LOCKS='0', LC_ALL='C', PYTHONDONTWRITEBYTECODE='1')
parser = argparse.ArgumentParser()
parser.add_argument('revision')
parser.add_argument('--out', default='final')
parser.add_argument('--only', nargs='*')
args = parser.parse_args()
if not re.fullmatch(r'[0-9a-f]{40}', args.revision):
    raise SystemExit('full landed branch commit required')
if not re.fullmatch(r'[a-zA-Z0-9_-]+', args.out):
    raise SystemExit('single output child name required')
OUT = ROOT / args.out
OUT.mkdir(parents=True, exist_ok=False)
runs = []

def record(label, command, cwd, want=0, timeout=900):
    if args.only and label not in args.only:
        return
    p = subprocess.run(command, cwd=cwd, env=ENV, stdin=subprocess.DEVNULL,
                       capture_output=True, text=True, errors='replace', timeout=timeout)
    (OUT / (label + '.stdout')).write_text(p.stdout)
    (OUT / (label + '.stderr')).write_text(p.stderr)
    item = {'label': label, 'command': command, 'cwd': str(cwd), 'exit': p.returncode,
            'expected_exit': want, 'matched_exit': p.returncode == want,
            'stdout': label + '.stdout', 'stderr': label + '.stderr'}
    runs.append(item)
    (OUT / 'results.json').write_text(json.dumps({'baseline': BASE,
        'measured_revision': args.revision, 'runs': runs}, indent=2) + '\n')
    print(label, p.returncode, 'expected', want, flush=True)

def git(*argv):
    return subprocess.check_output(['git', '-C', str(LANE), *argv], env=ENV)

for ref in ('refs/heads/master', 'refs/remotes/origin/master'):
    subprocess.run(['git', '-C', str(LANE), 'merge-base', '--is-ancestor', args.revision, ref],
                   env=ENV, check=True)

with tempfile.TemporaryDirectory(prefix='tsukuroi-r20-final-') as tmp:
    clone = Path(tmp) / 'lane'
    subprocess.run(['git', '-c', 'core.hooksPath=' + os.devnull, 'clone', '--quiet',
                    '--no-hardlinks', str(LANE), str(clone)], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'remote', 'remove', 'origin'], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', args.revision],
                   env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'update-ref', 'refs/heads/master', args.revision],
                   env=ENV, check=True)
    digests = {str(p.relative_to(clone)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in sorted((clone / 'tools').iterdir()) if p.is_file()}
    (OUT / 'evaluator-digests.json').write_text(json.dumps(digests, indent=2) + '\n')
    for path in sorted((clone / 'tools').iterdir()):
        if path.suffix not in ('.py', '.sh') or not path.is_file():
            continue
        record('selftest-' + path.stem, ['python3' if path.suffix == '.py' else 'bash',
               str(path.relative_to(clone)), '--selftest'], clone)
    cases = (
        ('c1', 'check-adjacency-anchors.py', '--revision', ['--ownership-corrections']),
        ('c2', 'check-revision-binding.py', '--tools-revision', ['--object-selectors']),
        ('c3', 'check-registry-coverage.py', '--revision', ['--audit-live-map']),
    )
    for label, tool, flag, extra in cases:
        for phase, rev in (('before', BASE), ('after', args.revision)):
            record(label + '-' + phase, ['python3', 'tools/' + tool, flag, rev, *extra],
                   clone, want=1 if phase == 'before' else 0)
    record('original-nine-continuity', ['python3', 'tools/check-revision-binding.py',
           '--tools-revision', args.revision], clone)
    record('registry-coverage', ['python3', 'tools/check-registry-coverage.py',
           '--revision', args.revision, '--baseline-tools', BASE], clone)
    record('adjacency-legacy', ['python3', 'tools/check-adjacency-anchors.py',
           '--revision', args.revision], clone)
    record('boot-writers-legacy', ['python3', 'tools/check-boot-writers.py',
           '--revision', args.revision], clone)
    record('boot-statement-corrections', ['python3', 'tools/check-boot-chain.py',
           '--revision', args.revision, '--statement-corrections', '--registry-from',
           'c0f6303f35e15ce113c03f4b6592014b9d8c2472'], clone)
    record('notices-legacy', ['python3', 'tools/check-appended-notices.py',
           '--revision', args.revision, '--registry-from',
           'c0f6303f35e15ce113c03f4b6592014b9d8c2472'], clone)
    record('recheck-corpus', ['python3', 'tools/check-recheck-commands.py',
           '--revision', args.revision], clone)
    for name in ('r19', 'r19b', 'r19c'):
        record('exec-log-' + name, ['python3', 'tools/check-recheck-commands.py',
               '--revision', args.revision, '--exec-log',
               '.ufo/waves/round-19/l1-capture/host-capture-' + name + '.txt'], clone)
    for wave in ('build', 'falsify'):
        path = clone / '.ufo/waves/round-20' / wave / 'dispatch.json'
        if path.is_file():
            record('seat-scope-' + wave, ['python3', 'tools/check-seat-scope.py',
                   '--wave', '.ufo/waves/round-20/' + wave, '--revision', args.revision], clone)
    prefixes = {}
    for path in ('PROVINCE.md', 'SKILL.md', 'LOG.md', 'SCORECARD.md',
                 'corpus/QUALITY.md', 'corpus/README.md', 'corpus/knowledge/boot-writers-r19.md'):
        old, new = git('show', BASE + ':' + path), git('show', args.revision + ':' + path)
        prefixes[path] = {'preserved': new.startswith(old), 'baseline_bytes': len(old),
                          'target_bytes': len(new), 'old_sha256': hashlib.sha256(old).hexdigest()}
    (OUT / 'prefixes.json').write_text(json.dumps(prefixes, indent=2) + '\n')
    print('round20-prefixes', all(x['preserved'] for x in prefixes.values()), flush=True)
record('census-end', ['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh',
       'validate', '--root', '/home/vgpnk/Projects/shokunin', 'tsukuroi'], LANE)
print('Retained evidence only; no automatic claim admission:', OUT)
