#!/usr/bin/env python3
"""L1-only once-final measurement from a fresh nonlocal clone; no host probes."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / '.ufo/waves/round-22'
BASE = '894d1e20fb4939b0cc4fadf722c46d1429f257d2'
PRE = '415ac3a834a1d7fa5b09986463512579af65d28e'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, LC_ALL='C')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('revision')
    parser.add_argument('output')
    args = parser.parse_args()
    if not args.output.isalnum():
        raise SystemExit('unique alphanumeric output required')
    out = ROUND / 'measure' / args.output
    out.mkdir(parents=True, exist_ok=False)
    clone = out / 'sandbox'
    result = subprocess.run(['git', 'clone', '--no-local', '--quiet', '--branch', 'master', str(ROOT), str(clone)], env=ENV, capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    ledger = []
    def run(name, cmd, expected=None):
        proc = subprocess.run(cmd, cwd=clone, env=ENV, capture_output=True, timeout=600)
        (out / (name + '.stdout')).write_bytes(proc.stdout)
        (out / (name + '.stderr')).write_bytes(proc.stderr)
        row = {'name': name, 'command': cmd, 'exit': proc.returncode, 'expected_exit': expected,
               'stdout': str((out / (name + '.stdout')).relative_to(ROOT)),
               'stderr': str((out / (name + '.stderr')).relative_to(ROOT))}
        try:
            row['result'] = json.loads(proc.stdout)
        except (ValueError, UnicodeError):
            pass
        if expected is not None:
            row['matches_expected_exit'] = proc.returncode == expected
        ledger.append(row)
        return proc
    rev = args.revision
    # Use the final judge files for both immutable input revisions.
    for label, revision in [('before', BASE), ('after', rev)]:
        run('c1-' + label, [sys.executable, 'tools/check-boundary-contract.py', '--revision', revision], 1 if label == 'before' else 0)
        for wave in ('build', 'falsify'):
            prefix = f'.ufo/waves/round-22/{wave}/'
            run(f'c2-{wave}-{label}', [sys.executable, 'tools/check-seat-bindings.py', '--revision', revision, '--manifest', prefix + 'bindings.json', '--events', prefix + 'events.json'], 1 if label == 'before' else None)
            run(f'c3-{wave}-{label}', [sys.executable, 'tools/check-review-cohort.py', '--revision', revision, '--manifest', prefix + 'reviews.json', '--settlement', prefix + 'settlement.json'], 1 if label == 'before' else None)
    for tool in sorted((clone / 'tools').iterdir()):
        if tool.suffix not in ('.py', '.sh'):
            continue
        interpreter = 'bash' if tool.suffix == '.sh' else sys.executable
        run('selftest-' + tool.stem, [interpreter, str(tool.relative_to(clone)), '--selftest'], 0)
    run('registry', [sys.executable, 'tools/check-registry-coverage.py', '--revision', rev], 0)
    run('live-map', [sys.executable, 'tools/check-registry-coverage.py', '--revision', rev, '--audit-live-map'], 0)
    run('legacy-selectors', [sys.executable, 'tools/check-revision-binding.py', '--tools-revision', rev, '--object-selectors'], 0)
    run('legacy-target-types', [sys.executable, 'tools/check-revision-binding.py', '--tools-revision', rev, '--object-target-types'], 0)
    for tool in ('check-boundary-contract.py', 'check-seat-bindings.py', 'check-review-cohort.py'):
        run('refusal-' + tool, [sys.executable, 'tools/' + tool, '--revision', 'HEAD'], 2)
    def git_bytes(revision, path):
        proc = subprocess.run(['git', '-C', str(clone), 'show', f'{revision}:{path}'], env=ENV, capture_output=True, check=True)
        return proc.stdout
    protected = ['tools/_revision.py', 'tools/check-review-snapshots.py', 'tools/check-seat-scope.py', 'PROVINCE.md']
    unchanged = {p: git_bytes(BASE, p) == git_bytes(rev, p) for p in protected}
    integrity = {'baseline': BASE, 'target': rev, 'predispatch_build': PRE, 'unchanged': unchanged,
                 'evaluators_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (clone / 'tools').iterdir() if p.suffix in ('.py', '.sh')}, 'waves': {}}
    for wave in ('build', 'falsify'):
        prefix = f'.ufo/waves/round-22/{wave}/'
        origin = PRE if wave == 'build' else json.loads(git_bytes(rev, prefix + 'reservation.json'))['predispatch_commit']
        checks = {}
        for path in ('reviews.json', 'bindings.json', 'spec.json'):
            checks[path] = git_bytes(origin, prefix + path) == git_bytes(rev, prefix + path)
        manifest = json.loads(git_bytes(rev, prefix + 'reviews.json'))
        checks['all_primary_snapshots_match'] = all(hashlib.sha256(git_bytes(rev, r['source'])).hexdigest() == r['sha256'] for r in manifest['reviews'])
        registry = json.loads(git_bytes(rev, prefix + 'swarm-registry.json'))
        settlement = json.loads(git_bytes(rev, prefix + 'settlement.json'))
        checks['registry_settlement_identity'] = {n: r['agentId'] for n, r in registry['members'].items()} == {r['name']: r['agent'] for r in settlement['seats']}
        checks['manifest_registry_bijection'] = {r['name'] for r in manifest['reviews']} == set(registry['members'])
        checks['origin_ancestor'] = subprocess.run(['git', '-C', str(clone), 'merge-base', '--is-ancestor', origin, rev], env=ENV).returncode == 0
        integrity['waves'][wave] = {'origin': origin, 'checks': checks}
    (out / 'integrity.json').write_text(json.dumps(integrity, indent=2) + '\n')
    (out / 'results.json').write_text(json.dumps({'baseline': BASE, 'revision': rev, 'commands': ledger}, indent=2) + '\n')
    print(json.dumps({'revision': rev, 'commands': len(ledger), 'expected_exit_mismatches': [r['name'] for r in ledger if r.get('matches_expected_exit') is False], 'integrity': integrity['waves'], 'unchanged': unchanged}))


if __name__ == '__main__':
    main()
