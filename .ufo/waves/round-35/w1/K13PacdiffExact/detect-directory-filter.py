#!/usr/bin/env python3
"""One deterministic, isolated detector; never calls the C1 counter."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument('--census', required=True)
ap.add_argument('--phase', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
root = Path(tempfile.mkdtemp(prefix='detector-' + a.phase + '-', dir='/fast/scratch/hyaku/tsukuroi-r35/K13PacdiffExact'))
locked = root / 'etc/locked'
expected = {'pacnew': 2, 'pacsave': 3, 'pacorig': 1, 'unreadable': 1,
            'log_pacnew': 5, 'log_pacsave': 1, 'unlogged': 4, 'gone': 1}

def fingerprint():
    rows = []
    for base, dirs, files in os.walk(root / 'etc'):
        for name in sorted(dirs + files):
            p = Path(base) / name
            st = p.lstat()
            content = os.readlink(p) if p.is_symlink() else (hashlib.sha256(p.read_bytes()).hexdigest() if stat.S_ISREG(st.st_mode) else None)
            rows.append([str(p.relative_to(root)), st.st_mode, st.st_ctime_ns, content])
    p = root / 'pacman.log'
    st = p.stat()
    rows.append(['pacman.log', st.st_mode, st.st_ctime_ns, hashlib.sha256(p.read_bytes()).hexdigest()])
    return hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()

try:
    for rel in ('etc/readable', 'etc/bundle.pacnew', 'etc/history.pacsave', 'etc/folder.pacorig', 'etc/locked', 'home', 'tmp'):
        (root / rel).mkdir(parents=True)
    for rel in ('etc/keep.conf.pacnew', 'etc/readable/edited.conf.pacsave', 'etc/archive.pacsave.4', 'etc/copy.pacorig', 'etc/bundle.pacnew/inner.pacsave', 'etc/locked/hidden.pacnew'):
        (root / rel).write_text('fixture bytes\n')
    (root / 'etc/link.pacnew').symlink_to('/nonexistent-directory-filter-detector')
    stamp = '[2026-10-23T00:00:00+0000]'
    (root / 'pacman.log').write_text('\n'.join([
        stamp + ' [ALPM] warning: /etc/keep.conf installed as /etc/keep.conf.pacnew',
        stamp + ' [ALPM] warning: /etc/keep.conf installed as /etc/keep.conf.pacnew',
        stamp + ' [ALPM] warning: /etc/readable/edited.conf saved as /etc/readable/edited.conf.pacsave',
        stamp + ' [ALPM] warning: /etc/removed.conf installed as /etc/removed.conf.pacnew',
        stamp + ' [ALPM] warning: /etc/locked/missing installed as /etc/locked/missing.pacnew',
        stamp + ' [ALPM] warning: /usr/share/outside installed as /usr/share/outside.pacnew',
        stamp + ' [ALPM-SCRIPTLET] warning: /etc/noise installed as /etc/noise.pacnew',
        stamp + ' [ALPM] warning: /etc/first saved as /etc/second.pacsave',
    ]) + '\n')
    stub = root / 'stub'
    stub.write_text('#!/bin/sh\nexit 0\n')
    stub.chmod(0o755)
    e = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'HOME': str(root / 'home'), 'TMPDIR': str(root / 'tmp')}
    for key in ('PACMAN', 'PACMAN_CONF', 'SYSTEMCTL', 'DMESG', 'JOURNALCTL', 'NVIDIA_SMI', 'LSMOD', 'EXPAC', 'VERCMP'):
        e['TSUKUROI_' + key] = str(stub)
    for key in ('PACMAN_CONF_FILE', 'HOSTNAME_FILE', 'DMESG_RESTRICT_FILE', 'PRESSURE_FILE', 'MEMINFO_FILE', 'VMSTAT_FILE', 'OFFLINE_DB'):
        p = root / ('f-' + key)
        p.write_bytes(b'')
        e['TSUKUROI_' + key] = str(p)
    for key in ('PACMAN_DB', 'ROOT_DIR', 'PCI_SYSFS', 'DEV_DIR', 'CGROUP_ROOT', 'BOOT_TARGET'):
        p = root / ('d-' + key)
        p.mkdir()
        e['TSUKUROI_' + key] = str(p)
    e.update({'TSUKUROI_ETC_DIR': str(root / 'etc'), 'TSUKUROI_PACMAN_LOG': str(root / 'pacman.log'), 'TSUKUROI_FOREIGN_BASELINE': '', 'TSUKUROI_OOM_BASELINE': ''})
    locked.chmod(0)
    before = fingerprint()
    census_before = hashlib.sha256(Path(a.census).read_bytes()).hexdigest()
    p = subprocess.run(['timeout', '--kill-after=2s', '40s', 'bash', a.census], cwd=root, env=e, capture_output=True, text=True)
    after = fingerprint()
    census_after = hashlib.sha256(Path(a.census).read_bytes()).hexdigest()
    lines = [line for line in p.stdout.splitlines() if line.startswith('DRIFT pacnew-plane ')]
    reported = dict((k, int(v)) for k, v in re.findall(r'(\w+)=(\d+)', lines[0])) if len(lines) == 1 else None
    ok = p.returncode in (0, 1, 2) and reported == expected and before == after and census_before == census_after
    result = {'phase': a.phase, 'detector_matches': ok, 'detector_exit': 0 if ok else 1, 'census_exit': p.returncode, 'expected': expected, 'reported': reported, 'drift_lines': lines, 'fixture_before_sha256': before, 'fixture_after_sha256': after, 'census_before_sha256': census_before, 'census_after_sha256': census_after, 'stdout': p.stdout[:131072], 'stderr': p.stderr[:131072]}
    Path(a.out).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('stdout', 'stderr')}, sort_keys=True))
finally:
    if locked.exists():
        locked.chmod(0o700)
    shutil.rmtree(root)
raise SystemExit(0 if ok else 1)
