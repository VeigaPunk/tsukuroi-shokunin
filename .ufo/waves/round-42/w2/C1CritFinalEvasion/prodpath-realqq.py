#!/usr/bin/env python3
"""C1-9 able-to-fail demo: run a census in PRODUCTION shape (no TSUKUROI_FIXTURE, non-root,
no namespace) over a 1 MiB -Qkk sample / 1 MiB -Qu list, using the BASE census's own fixture
dispatcher (patched to answer from $R42_FX instead of $TSUKUROI_FIXTURE).

Usage: prodpath-demo.py <census.sh>...   -> one JSON line per (census, shape)
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE_CENSUS = '/fast/scratch/hyaku/tsukuroi-r42/C1CritFinalEvasion/base-census.sh'
PAD = 1 << 20
ERR = 'error: alpha: /usr/bin/x-deadbeef (Permission denied)\n'
REALQQ = ''.join(p + '\n' for p in ['acl','bash','coreutils','filesystem','glibc','glibc-libs','pacman','systemd'])
SUMS = ['alpha: 10 total files, 0 altered files\n', 'beta: 20 total files, 0 altered files\n']


def big_qkk():
    out, size, i = [ERR] + SUMS, 0, 0
    while size < PAD:
        line = f'warning: lib{i % 97}-xcb{i % 89}: /usr/share/doc/p{i % 1013}.dat (Modification time mismatch)\n'
        out.append(line)
        size += len(line)
        i += 1
    return ''.join(out)


def big_qu():
    out, size, i = ['alpha 1.0-1 -> 1.1-1\n', 'beta 2.0-1 -> 2.1-1\n'], 0, 0
    while size < PAD:
        line = f'pad{i:05d} 1.0-1 -> 1.0-2\n'
        out.append(line)
        size += len(line)
        i += 1
    return ''.join(out)


def env_for(fx, bindir):
    e = {'PATH': os.environ['PATH'], 'LC_ALL': 'C', 'HOME': fx, 'TMPDIR': os.path.join(fx, '..', 'tmp'),
         'R42_FX': fx}
    e.update({
        'TSUKUROI_PACMAN': f'{bindir}/pacman', 'TSUKUROI_PACMAN_CONF': f'{bindir}/pacman-conf',
        'TSUKUROI_PACMAN_CONF_FILE': f'{fx}/pacman.conf', 'TSUKUROI_PACMAN_DB': f'{fx}/pacmandb',
        'TSUKUROI_ROOT_DIR': f'{fx}/root', 'TSUKUROI_FOREIGN_BASELINE': f'{fx}/fbase',
        'TSUKUROI_SYSTEMCTL': f'{bindir}/systemctl', 'TSUKUROI_DMESG': f'{bindir}/dmesg',
        'TSUKUROI_JOURNALCTL': f'{bindir}/journalctl', 'TSUKUROI_NVIDIA_SMI': f'{bindir}/nvidia-smi',
        'TSUKUROI_LSMOD': f'{bindir}/lsmod', 'TSUKUROI_PCI_SYSFS': f'{fx}/pci',
        'TSUKUROI_DEV_DIR': f'{fx}/dev', 'TSUKUROI_HOSTNAME_FILE': f'{fx}/hostname',
        'TSUKUROI_DMESG_RESTRICT_FILE': f'{fx}/dmesg_restrict', 'TSUKUROI_CGROUP_ROOT': f'{fx}/cgroup',
        'TSUKUROI_MEM_SLICE': 'user.slice/user-1000.slice', 'TSUKUROI_PRESSURE_FILE': f'{fx}/pressure/memory',
        'TSUKUROI_MEMINFO_FILE': f'{fx}/meminfo', 'TSUKUROI_VMSTAT_FILE': f'{fx}/vmstat',
        'TSUKUROI_OOM_BASELINE': f'{fx}/obase', 'TSUKUROI_PACMAN_LOG': f'{fx}/pacman.log',
        'TSUKUROI_ETC_DIR': f'{fx}/etc', 'TSUKUROI_BTRFS_SYSFS': f'{fx}/btrfs',
        'TSUKUROI_PROC_MOUNTS': f'{fx}/mounts', 'TSUKUROI_EXPAC': f'{bindir}/expac',
    })
    return e


def main():
    root = tempfile.mkdtemp(prefix='prodpath.', dir=os.environ['TMPDIR'])
    try:
        base = open(BASE_CENSUS).read()
        disp = re.search(r"cat > \"\$bin/\.dispatch\" <<'STUB'\n(.*?)\nSTUB\n", base, re.S).group(1)
        fxdef = re.search(r"\n(  fx_default\(\) \{.*?\n  \}\n)", base, re.S).group(1)
        disp = disp.replace('fix=${TSUKUROI_FIXTURE:-}', 'fix=${R42_FX:-}')
        assert 'fix=${R42_FX:-}' in disp
        bindir = os.path.join(root, 'bin')
        os.makedirs(bindir)
        os.makedirs(os.path.join(root, 'tmp'))
        with open(os.path.join(bindir, '.dispatch'), 'w') as f:
            f.write('#!/usr/bin/env bash\nset -uo pipefail\n' + disp + '\n')
        os.chmod(os.path.join(bindir, '.dispatch'), 0o700)
        for c in ['pacman', 'pacman-conf', 'systemctl', 'dmesg', 'journalctl', 'nvidia-smi', 'lsmod', 'expac']:
            os.symlink('.dispatch', os.path.join(bindir, c))
        builder = os.path.join(root, 'build.sh')
        with open(builder, 'w') as f:
            f.write('#!/usr/bin/env bash\nset -euo pipefail\numask 077\n' + fxdef + 'fx_default "$1"\n')

        def fixture(shape):
            fx = os.path.join(root, f'fx-{shape}')
            os.makedirs(fx)
            subprocess.run(['bash', builder, fx], check=True, capture_output=True)
            if shape == 'qkk-small':
                open(os.path.join(fx, 'qkk.out'), 'w').write(''.join([ERR] + SUMS))
                open(os.path.join(fx, 'qkk.rc'), 'w').write('1')
            elif shape == 'qkk-large':
                open(os.path.join(fx, 'qkk.out'), 'w').write(big_qkk())
                open(os.path.join(fx, 'qkk.rc'), 'w').write('1')
            elif shape == 'qkk-small-realqq':
                open(os.path.join(fx, 'pq'), 'w').write(REALQQ)
                open(os.path.join(fx, 'qkk.out'), 'w').write(''.join([ERR] + SUMS))
                open(os.path.join(fx, 'qkk.rc'), 'w').write('1')
            elif shape == 'qkk-large-realqq':
                open(os.path.join(fx, 'pq'), 'w').write(REALQQ)
                open(os.path.join(fx, 'qkk.out'), 'w').write(big_qkk())
                open(os.path.join(fx, 'qkk.rc'), 'w').write('1')
            elif shape == 'qu-large':
                open(os.path.join(fx, 'qu'), 'w').write(big_qu())
                open(os.path.join(fx, 'qu.rc'), 'w').write('0')
            return fx

        rows = []
        for census in sys.argv[1:]:
            for shape in ('qkk-small-realqq', 'qkk-large-realqq'):
                fx = fixture(shape)
                try:
                    p = subprocess.run(['bash', census], env=env_for(fx, bindir), capture_output=True,
                                       timeout=300, cwd=fx)
                    out = p.stdout.decode(errors='replace')
                    stderr = p.stderr.decode(errors='replace')[-200:]
                except subprocess.TimeoutExpired:
                    out, stderr, p = '', 'timeout', None
                pk = [ln for ln in out.splitlines() if ln.startswith('PLANE packages:')]
                upd = [ln for ln in out.splitlines() if ln.startswith('PLANE update-safety:')]
                rows.append({'census': os.path.basename(census), 'shape': shape,
                             'rc': None if p is None else p.returncode,
                             'packages': (pk[0] if pk else '(no PLANE line)')[:260],
                             'update': (upd[0] if upd else '(no PLANE line)')[:200],
                             'stderr_tail': stderr})
                shutil.rmtree(fx, ignore_errors=True)
        for r in rows:
            print(json.dumps(r, sort_keys=True))
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    main()
