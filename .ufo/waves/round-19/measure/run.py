#!/usr/bin/env python3
"""Capture round-19 lane checks at one landed revision without host probes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE = '452a054677f6b18284917d7c08c45361f91c25ac'
SCRIPT = Path(__file__).resolve()
LANE = next((parent for parent in SCRIPT.parents
             if (parent / 'PROVINCE.md').is_file() and (parent / '.ufo').is_dir()), None)
if LANE is None:
    raise SystemExit('unable to locate lane root from script path')
MEASURE = LANE / '.ufo/waves/round-19/measure'

if len(sys.argv) not in (2, 3):
    raise SystemExit(f'usage: python3 {SCRIPT} <TARGET-landed-sha> [outdir-name]')
TIP = sys.argv[1]
OUT_NAME = sys.argv[2] if len(sys.argv) == 3 else 'final'
OUT = (MEASURE / OUT_NAME).resolve()
if OUT.parent != MEASURE.resolve():
    raise SystemExit('outdir-name must be a single child name of the round-19 measure directory')
OUT.mkdir(parents=True, exist_ok=True)

ENV = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
ENV.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
           GIT_OPTIONAL_LOCKS='0', LC_ALL='C', PYTHONDONTWRITEBYTECODE='1')
runs = []


def _text(value):
    if value is None:
        return ''
    return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value


def _write_results():
    result = {'baseline': BASE, 'measured_revision': TIP, 'runs': runs}
    (OUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')


def record(label, command, cwd, timeout=600, required=None, execution_scope=None):
    stdout_name = f'{label}.stdout'
    stderr_name = f'{label}.stderr'
    stdout_path = OUT / stdout_name
    stderr_path = OUT / stderr_name
    required_path = None
    if required is not None:
        required_path = Path(required)
        if not required_path.is_absolute():
            required_path = Path(cwd) / required_path

    if required_path is not None and not required_path.is_file():
        stdout_path.write_text('')
        stderr_path.write_text('')
        item = {'label': label, 'command': command, 'cwd': str(cwd), 'status': 'skipped-absent',
                'exit': None, 'stdout': stdout_name, 'stderr': stderr_name,
                'reason': f'required tool absent: {required_path}'}
        if execution_scope is not None:
            item['execution_scope'] = execution_scope
        runs.append(item)
        _write_results()
        print(label, 'skipped-absent', flush=True)
        return None

    try:
        proc = subprocess.run(command, cwd=cwd, env=ENV, stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, encoding='utf-8', errors='replace',
                              timeout=timeout)
        stdout = proc.stdout
        stderr = proc.stderr
        status = 'completed'
        exit_code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = _text(exc.stdout)
        stderr = _text(exc.stderr)
        status = 'timeout'
        exit_code = None
    stdout_path.write_text(stdout)
    stderr_path.write_text(stderr)
    item = {'label': label, 'command': command, 'cwd': str(cwd), 'status': status,
            'exit': exit_code, 'stdout': stdout_name, 'stderr': stderr_name}
    if execution_scope is not None:
        item['execution_scope'] = execution_scope
    runs.append(item)
    _write_results()
    print(label, exit_code if exit_code is not None else status, flush=True)
    return item


with tempfile.TemporaryDirectory(prefix='tsukuroi-r19-measure-') as tmp:
    clone = Path(tmp) / 'lane'
    subprocess.run(['git', '-c', f'core.hooksPath={os.devnull}', 'clone', '--quiet',
                    '--no-hardlinks', str(LANE), str(clone)], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'remote', 'remove', 'origin'], env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', TIP],
                   env=ENV, check=True)
    subprocess.run(['git', '-C', str(clone), 'update-ref', 'refs/heads/master', TIP],
                   env=ENV, check=True)

    tool_root = clone / 'tools'
    tool_files = sorted(path for path in tool_root.rglob('*')
                        if path.is_file() or path.is_symlink()) if tool_root.is_dir() else []
    digests = {}
    for path in tool_files:
        content = os.readlink(path).encode('utf-8') if path.is_symlink() else path.read_bytes()
        digests[path.relative_to(clone).as_posix()] = hashlib.sha256(content).hexdigest()
    (OUT / 'evaluator-digests.json').write_text(
        json.dumps({'revision': TIP, 'files': digests}, indent=2, sort_keys=True) + '\n')

    if tool_root.is_dir():
        for path in sorted(tool_root.iterdir()):
            if path.is_symlink() or not path.is_file():
                continue
            if path.suffix == '.py':
                interpreter = 'python3'
            elif path.suffix == '.sh':
                interpreter = 'bash'
            else:
                continue
            relpath = path.relative_to(clone).as_posix()
            label = 'selftest-' + path.name.replace('.', '-')
            record(label, [interpreter, relpath, '--selftest'], clone, required=relpath)

    gates = [
        ('c1', 'check-adjacency-anchors.py',
         ['--revision', BASE, '--registry-from', TIP],
         ['--revision', TIP]),
        ('c2', 'check-boot-writers.py',
         ['--revision', BASE, '--registry-from', TIP],
         ['--revision', TIP]),
    ]
    for axis, tool, before_args, after_args in gates:
        reltool = f'tools/{tool}'
        record(f'{axis}-before', ['python3', reltool, *before_args], clone, required=reltool)
        record(f'{axis}-after', ['python3', reltool, *after_args], clone, required=reltool)

    registry_tool = 'tools/check-registry-coverage.py'
    record('c3-before', ['python3', registry_tool, '--revision', BASE], clone,
           required=registry_tool)
    record('c3-after', ['python3', registry_tool, '--revision', TIP,
                        '--baseline-tools', BASE], clone, required=registry_tool)

    recheck_tool = 'tools/check-recheck-commands.py'
    captures = [
        ('r19', '.ufo/waves/round-19/l1-capture/host-capture-r19.txt'),
        ('r19b', '.ufo/waves/round-19/l1-capture/host-capture-r19b.txt'),
        ('r19c', '.ufo/waves/round-19/l1-capture/host-capture-r19c.txt'),
    ]
    for capture_name, capture_path in captures:
        record(f'recheck-exec-log-{capture_name}',
               ['python3', recheck_tool, '--revision', TIP, '--exec-log', capture_path],
               clone, required=recheck_tool)

    seat_scope_tool = 'tools/check-seat-scope.py'
    for wave in ('build', 'falsify'):
        wave_path = f'.ufo/waves/round-19/{wave}'
        record(f'seat-scope-{wave}',
               ['python3', seat_scope_tool, '--wave', wave_path, '--revision', TIP],
               clone, required=seat_scope_tool)

sources_census = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
record('sources-census-live-lane',
       [sources_census, 'validate', '--root', '/home/vgpnk/Projects/shokunin', 'tsukuroi'],
       LANE, required=sources_census, execution_scope='live-lane')
print('Recorded evidence, not automatic claim admission:', OUT)
