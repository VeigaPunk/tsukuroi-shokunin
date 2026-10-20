#!/usr/bin/env python3
"""Round18 reproducible L1 evidence capture. Only clone/temp-fixture writes and this evidence directory.
Usage: python3 <absolute-script> <landed-master-sha> [output-name]
Runs no live host audit/package/service/boot probe. Git writes inside gate selftests belong to temp clones.
"""
import hashlib
import json
import os
import re
import shutil
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


def record(label, command, cwd, timeout=600, env_override=None):
    proc = subprocess.run(command, cwd=cwd, env=ENV if env_override is None else env_override,
                          stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
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
    # Pin the disposable snapshot's local branch explicitly (jj source HEAD may
    # be detached); TIP is the separately helper-verified landed source commit.
    subprocess.run(['git', '-C', str(clone), 'update-ref', 'refs/heads/master', TIP],
                   env=ENV, check=True)
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
        if name == 'freshness-recheck-r18.json':
            expected_primary = {'SKILL.md', 'corpus/knowledge/host-health-report-r3.md',
                                'corpus/knowledge/journal-boot-plane.md',
                                'corpus/knowledge/package-state-plane.md',
                                'corpus/knowledge/aur-risk-plane.md',
                                'corpus/knowledge/foreign-provenance-r6.md',
                                'corpus/knowledge/oom-event-plane.md',
                                'corpus/knowledge/kill-event-deep-r8.md'}
            checks['all_eight_routed_primary_paths'] = {r['path'] for r in primary} == expected_primary
            checks['primary49_supplementary48_records'] = len(primary) == 49 and len(doc['records']) == 97
        for target in targets:
            baseline = subprocess.run(['git', '-C', str(clone), 'show', BASE + ':' + target], env=ENV, capture_output=True, check=True).stdout
            checks[target + '_baseline_prefix_preserved'] = (clone / target).read_bytes().startswith(baseline)
    # Actual runtime bytecode guard proof: remove the masking environment option,
    # positively demonstrate that an unguarded import writes in this private clone,
    # then check every consumer without that override.
    guard_env = {k: v for k, v in ENV.items()
                 if k not in ('PYTHONDONTWRITEBYTECODE', 'PYTHONPYCACHEPREFIX')}
    guard_env['PYTHONNOUSERSITE'] = '1'
    pycache = clone / 'tools/__pycache__'
    if pycache.exists():
        shutil.rmtree(pycache)
    record('bytecode-positive-control',
           [sys.executable, '-S', '-c',
            "import sys; sys.path.insert(0, 'tools'); import _revision"], clone,
           env_override=guard_env)
    checks['bytecode_positive_control_writes_cache'] = pycache.is_dir()
    if pycache.exists():
        shutil.rmtree(pycache)
    consumers = [name for name, interpreter in tools if interpreter == 'python3'
                 and name not in ('_revision.py', 'check-revision-binding.py')]
    for name in consumers:
        extra = ['--wave', '.ufo/waves/round-18/build'] if name == 'check-seat-scope.py' else []
        proc = record('bytecode-guard-' + name.replace('.', '-'),
                      [sys.executable, '-S', str(clone / 'tools' / name),
                       '--revision', 'HEAD', *extra], clone, env_override=guard_env)
        checks[name + '_refusal_without_pycache'] = proc.returncode == 2 and not pycache.exists()
        if pycache.exists():
            shutil.rmtree(pycache)
    # The typed-source path must fail independently of fixed Now-string checks.
    boot_tool = clone / 'tools/check-boot-chain.py'
    original = boot_tool.read_bytes()
    mutated = re.sub(r'^def correction_source_ok\(spec, lines\):.*?(?=^def evaluate_statement_corrections)',
                     'def correction_source_ok(spec, lines):\n    return True\n\n\n',
                     original.decode(), count=1, flags=re.M | re.S)
    if mutated == original.decode():
        raise RuntimeError('typed-source mutant site not found')
    try:
        boot_tool.write_text(mutated)
        mutant = record('mutant-source-check-always-true',
                        [sys.executable, 'tools/check-boot-chain.py', '--selftest'], clone)
        checks['typed_source_always_true_mutant_killed'] = mutant.returncode == 1
    finally:
        boot_tool.write_bytes(original)
    checks['typed_source_mutant_restored_exactly'] = boot_tool.read_bytes() == original
    record('r5-literal-arithmetic', [sys.executable, '-c', 'print(12 + 1 + 2)'], clone)
    capture_root = clone / '.ufo/waves/round-18/l1-capture'
    events = capture_root / 'pacman-events-r18.txt'
    event_counter = record('historical-elephant-upgrade-events',
                           [sys.executable, '-c',
                            "from pathlib import Path; print(sum('[ALPM] upgraded elephant' in line "
                            "for line in Path('.ufo/waves/round-18/l1-capture/pacman-events-r18.txt').read_text().splitlines()))"],
                           clone)
    checks['thirteen_historical_elephant_upgrade_events'] = (
        event_counter.returncode == 0 and event_counter.stdout.strip() == '13')
    captured = (capture_root / 'host-capture-r18.txt').read_text()
    stdout_rows = []
    for line in (capture_root / 'harness-probe-stdout.txt').read_text().splitlines():
        match = re.fullmatch(r'\s*(\d+)\t(.*)', line)
        if match:
            stdout_rows.append((int(match.group(1)), match.group(2)))
    checks['capture_stdout_has_all99_ordered_lines'] = [n for n, _ in stdout_rows] == list(range(1, 100))
    checks['capture_matches_full_harness_stdout'] = '\n'.join(text for _, text in stdout_rows) + '\n' == captured
    script_sha = hashlib.sha256((capture_root / 'capture-r18.sh').read_bytes()).hexdigest()
    checks['capture_script_digest_matches_header'] = script_sha in captured.splitlines()[0]
    skill_lines = (clone / 'SKILL.md').read_text().splitlines()
    operative_heads = [(int(m.group(1)), i) for i, line in enumerate(skill_lines)
                       if (m := re.fullmatch(r'## Gate and probe registry — round(\d+) superseding current rows', line))]
    selected_rows = []
    if operative_heads:
        chosen_round = max(n for n, _ in operative_heads)
        chosen = [i for n, i in operative_heads if n == chosen_round]
        if len(chosen) == 1:
            for line in skill_lines[chosen[0] + 1:]:
                if line.startswith('## '):
                    break
                if line.startswith('| '):
                    cells = [value.strip() for value in line.split('|')[1:-1]]
                    if cells and cells[0] not in ('Name', '---'):
                        selected_rows.append(cells)
    names = [row[0] for row in selected_rows]
    checks['operative_registry_has13_unique_rows'] = len(names) == len(set(names)) == 13
    revision_rows = [row for row in selected_rows if row[0] == 'revision-binding']
    checks['operative_revision_binding_is_gate_not_five_probe'] = (
        len(revision_rows) == 1 and revision_rows[0][1] == 'gate'
        and 'original-nine' in revision_rows[0][3])
    (OUT / 'operative-registry.json').write_text(json.dumps(
        {'revision': TIP, 'selection': 'unique highest-numbered complete superseding registry',
         'rows': selected_rows, 'older_tables': 'historical, never fallback'}, indent=2))
    (OUT / 'protected-and-coverage.json').write_text(json.dumps({'revision': TIP, 'checks': checks, 'notices': notices}, indent=2))
    print('protected', all(checks.values()), 'coverage', notices, flush=True)

record('sources-census', ['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh', 'validate', '--root', '/home/vgpnk/Projects/shokunin', 'tsukuroi'], LANE)
print('Recorded evidence, not automatic claim admission:', OUT)
