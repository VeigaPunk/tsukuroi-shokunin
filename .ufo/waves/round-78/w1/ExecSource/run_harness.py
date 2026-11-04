#!/usr/bin/env python3
"""Run only the assigned extracted-body filesystem checks; never host journals."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-78/w1/ExecSource')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r78/ExecSource')


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    os.environ['TMPDIR'] = str(SCRATCH)
    source = b'\n'.join((SEAT / name).read_bytes() for name in (
        'context.h', 'endswith_internal.c', 'manager_determine_path_usage.c', 'main.c'))
    (SEAT / 'harness.c').write_bytes(source)
    receipt = {
        'compiler_version': subprocess.run(['cc', '--version'], capture_output=True, text=True, check=True).stdout,
        'harness_sha256': hashlib.sha256(source).hexdigest(),
        'stat_failure': 'NOT EXERCISED: all fstatat calls are real libc calls; no simulated failure',
        'cases': [],
    }
    with tempfile.TemporaryDirectory(prefix='fixtures-', dir=SCRATCH) as root_text:
        root = Path(root_text)
        executable = root / 'path-usage'
        command = ['cc', '-std=gnu17', '-O0', '-Wall', '-Wextra', '-Werror', str(SEAT / 'harness.c'), '-o', str(executable)]
        result = subprocess.run(command, capture_output=True, text=True)
        receipt['compile'] = {'argv': command, 'command': shlex.join(command), 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        (SEAT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        if result.returncode:
            raise RuntimeError('Compilation failed; see receipt.json')
        specs = [
            ('active', 'active.journal', 'regular', True, 4096),
            ('archived', 'archived.journal~', 'regular', True, 8192),
            ('unrelated', 'ignored.txt', 'regular', False, 4096),
            ('symlink', 'link.journal', 'symlink', False, 0),
            ('directory', 'directory.journal', 'directory', False, 0),
            ('sparse', 'sparse.journal', 'sparse', True, 64 * 1024 * 1024),
        ]
        for case_id, name, kind, included, size in specs:
            directory = root / case_id
            directory.mkdir()
            item = directory / name
            if kind == 'directory':
                item.mkdir()
            elif kind == 'symlink':
                (directory / 'target.bin').write_bytes(b'T' * 4096)
                item.symlink_to('target.bin')
            else:
                with item.open('wb') as stream:
                    stream.write(b'J' * (4096 if kind == 'sparse' else size))
                    if kind == 'sparse':
                        stream.truncate(size)
                    stream.flush()
                    os.fsync(stream.fileno())
            st = item.lstat()
            expected = st.st_blocks * 512 if included else 0
            run = subprocess.run([str(executable), str(directory)], capture_output=True, text=True)
            observed = json.loads(run.stdout) if run.returncode == 0 else None
            case = {
                'id': case_id, 'name': name, 'kind': kind,
                'lstat': {'mode_octal': oct(st.st_mode), 'size': st.st_size, 'blocks': st.st_blocks, 'allocated_bytes': st.st_blocks * 512},
                'expected_used': expected, 'argv': run.args, 'exit': run.returncode,
                'stdout': run.stdout, 'stderr': run.stderr, 'observed': observed,
                'match': run.returncode == 0 and observed['return'] == 0 and observed['used'] == expected,
            }
            if kind == 'symlink':
                target = item.stat()
                case['followed_target_stat'] = {'size': target.st_size, 'blocks': target.st_blocks, 'allocated_bytes': target.st_blocks * 512}
                case['match'] = case['match'] and target.st_blocks > 0
            if included:
                case['match'] = case['match'] and st.st_blocks > 0
            if kind == 'sparse':
                case['sparse_apparent_exceeds_allocated'] = st.st_size > st.st_blocks * 512
                case['match'] = case['match'] and case['sparse_apparent_exceeds_allocated']
            receipt['cases'].append(case)
            (SEAT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        receipt['matched'] = sum(case['match'] for case in receipt['cases'])
        receipt['all_cases_match'] = all(case['match'] for case in receipt['cases'])
        receipt['free_field'] = 'Real fstatvfs return, recorded only; not asserted stable between calls.'
    receipt['fixtures_removed'] = True
    (SEAT / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    if not receipt['all_cases_match']:
        raise RuntimeError('At least one assigned filesystem check failed')


if __name__ == '__main__':
    main()
