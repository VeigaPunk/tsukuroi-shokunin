#!/usr/bin/env python3
"""Round18 reproducible L1 evidence capture. Only clone/temp-fixture writes and this evidence directory.
Usage: python3 <absolute-script> <landed-master-sha> [output-name]
Runs no live host audit/package/service/boot probe. Git writes inside gate selftests belong to temp clones.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

LANE = Path(__file__).resolve().parents[4]
BASE = '842a5312b704b5cda10fd80ec1fdee5fb381ba97'
MEASURE = Path(__file__).resolve().parent
TIP = sys.argv[1]
OUT = MEASURE / (sys.argv[2] if len(sys.argv) > 2 else 'final')
OUT.mkdir(parents=True, exist_ok=True)
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_OPTIONAL_LOCKS='0', LC_ALL='C', PYTHONDONTWRITEBYTECODE='1')
results = []


def record(label, command, cwd, timeout=600):
    proc = subprocess.run(command, cwd=cwd, env=ENV, stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=timeout)
    (OUT / f'{label}.stdout').write_text(proc.stdout)
    (OUT / f'{label}.stderr').write_text(proc.stderr)
    doc = None
    try:
        doc = json.loads(proc.stdout)
    except (ValueError, TypeError):
        pass
    item = {'label': label, 'command': command, 'cwd': str(cwd), 'exit': proc.returncode,
            'stdout': f'{label}.stdout', 'stderr': f'{label}.stderr', 'json': doc}
    results.append(item)
    (OUT / 'results.json').write_text(json.dumps({'baseline': BASE, 'measured_revision': TIP, 'runs': results}, indent=2))
    print(label, proc.returncode, flush=True)
    return proc


with tempfile.TemporaryDirectory(prefix='tsukuroi-r18-main-measure-') as tmp:
    clone = Path(tmp) / 'lane'
    subprocess.run(['git', '-c', f'core.hooksPath={os.devnull}', 'clone', '--quiet', '--no-hardlinks', str(LANE), str(clone)], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'remote', 'remove', 'origin'], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', TIP], env=ENV, check=True)
    # Preserve clone's real local master from the landed source; the gates enforce ancestry.
    tools = [('_revision.py', 'python3'), ('check-revision-binding.py', 'python3'),
             ('check-appended-notices.py', 'python3'), ('check-boot-chain.py', 'python3'),
             ('check-freshness-r17.py', 'python3'), ('check-recheck-commands.py', 'python3'),
             ('check-seat-scope.py', 'python3'), ('check-locator-clarification.py', 'python3'),
             ('check-root-dac-correction.py', 'python3'), ('check-section-citations.py', 'python3'),
             ('check-source-scope-correction.py', 'python3'), ('measure-update-recheck.py', 'python3'),
             ('boot-chain-audit.sh', 'bash'), ('tsukuroi-census.sh', 'bash')]
    digests = {}
    for name, interpreter in tools:
        path = clone / 'tools' / name
        digests[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        record('selftest-' + name.replace('.', '-'), [interpreter, str(path), '--selftest'], clone)
    (OUT / 'evaluator-digests.json').write_text(json.dumps(digests, indent=2))

    for label, rev in [('before', BASE), ('after', TIP)]:
        record('c1-' + label, ['python3', 'tools/check-boot-chain.py', '--revision', rev,
                              '--statement-corrections', '--registry-from', TIP], clone)
        record('c2-' + label, ['python3', 'tools/check-revision-binding.py', '--tools-revision', rev], clone)
        for kind, registry in [('c1-structural', 'statement-corrections-r18.json'), ('c3', 'freshness-recheck-r18.json')]:
            record(kind + '-' + label, ['python3', 'tools/check-appended-notices.py', '--revision', rev,
                                       '--registry', 'corpus/knowledge/' + registry], clone)
        record('recheck-aur-' + label, ['python3', 'tools/check-recheck-commands.py', '--revision', rev,
                                      '--paths', 'corpus/knowledge/aur-risk-plane.md'], clone)
    for kind, registry in [('c1', 'statement-corrections-r18.json'), ('c3', 'freshness-recheck-r18.json')]:
        record(kind + '-actual-stale-baseline', ['python3', 'tools/check-appended-notices.py', '--revision', BASE,
               '--registry-from', TIP, '--registry', 'corpus/knowledge/' + registry], clone)
    record('legacy-boot-after', ['python3', 'tools/check-boot-chain.py', '--revision', TIP], clone)
    record('legacy-freshness-after', ['python3', 'tools/check-freshness-r17.py', '--revision', TIP], clone)
    record('recheck-all-after', ['python3', 'tools/check-recheck-commands.py', '--revision', TIP], clone)
    record('exec-log-after', ['python3', 'tools/check-recheck-commands.py', '--revision', TIP,
           '--exec-log', '.ufo/waves/round-18/l1-capture/host-capture-r18.txt'], clone)
    for wave in ['build', 'falsify']:
        wave_path = clone / '.ufo/waves/round-18' / wave
        if (wave_path / 'dispatch.json').exists():
            record('seat-scope-' + wave, ['python3', 'tools/check-seat-scope.py', '--revision', TIP,
                   '--wave', '.ufo/waves/round-18/' + wave], clone)
    checks = {'boot_chain_json_unchanged': subprocess.run(['git', '-C', str(clone), 'show', BASE + ':corpus/knowledge/boot-chain-r17.json'], env=ENV, capture_output=True).stdout == (clone / 'corpus/knowledge/boot-chain-r17.json').read_bytes()}
    paths = ['PROVINCE.md', 'SHONEN.md', 'corpus/lessons/round-17-verifier-spotcheck.md']
    for path in paths:
        checks[path + '_unchanged'] = subprocess.run(['git', '-C', str(clone), 'show', BASE + ':' + path], env=ENV, capture_output=True).stdout == (clone / path).read_bytes()
    notices = {}
    for name in ['statement-corrections-r18.json', 'freshness-recheck-r18.json']:
        doc = json.loads((clone / 'corpus/knowledge' / name).read_text())
        targets = sorted({r['path'] for r in doc['records']})
        primary = [r for r in doc['records'] if not r['id'].startswith('R18-FRESH-SUPPLEMENT-')]
        notices[name] = {'records': len(doc['records']), 'paths': targets, 'path_count': len(targets),
                         'primary_records': len(primary), 'primary_paths': sorted({r['path'] for r in primary})}
        for target in targets:
            baseline = subprocess.run(['git', '-C', str(clone), 'show', BASE + ':' + target], env=ENV, capture_output=True, check=True).stdout
            checks[target + '_baseline_prefix_preserved'] = (clone / target).read_bytes().startswith(baseline)
    (OUT / 'protected-and-coverage.json').write_text(json.dumps({'revision': TIP, 'checks': checks, 'notices': notices}, indent=2))
    print('protected', all(checks.values()), 'coverage', notices, flush=True)

record('sources-census', ['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh', 'validate', '--root', '/home/vgpnk/Projects/shokunin', 'tsukuroi'], LANE)
print('Recorded evidence, not automatic claim admission:', OUT)
