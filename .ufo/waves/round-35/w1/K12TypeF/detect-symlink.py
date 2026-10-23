#!/usr/bin/env python3
"""Independent fixed symlink fixture; run unchanged on pristine/mutant/restored bytes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess

SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K12TypeF')
WORK = Path('/fast/scratch/hyaku/tsukuroi-r35/K12TypeF/detector-fixture')
EXPECTED = dict(pacnew=2, pacsave=2, pacorig=1, unreadable=1,
                log_pacnew=5, log_pacsave=2, unlogged=2, gone=1)
COMMANDS = ('PACMAN', 'PACMAN_CONF', 'SYSTEMCTL', 'DMESG', 'JOURNALCTL',
            'NVIDIA_SMI', 'LSMOD', 'EXPAC', 'VERCMP')
FILES = ('PACMAN_CONF_FILE', 'HOSTNAME_FILE', 'DMESG_RESTRICT_FILE',
         'PRESSURE_FILE', 'MEMINFO_FILE', 'VMSTAT_FILE', 'OFFLINE_DB')
DIRS = ('PACMAN_DB', 'ROOT_DIR', 'PCI_SYSFS', 'DEV_DIR', 'CGROUP_ROOT', 'BOOT_TARGET')


def setup():
    if (WORK / 'ready').exists():
        return
    WORK.mkdir(parents=True, exist_ok=True)
    etc = WORK / 'etc'
    etc.mkdir()
    (etc / 'plain.pacnew').write_bytes(b'new\n')
    for name in ('linked.pacnew', 'link.pacsave', 'older.pacsave.1', 'original.pacorig'):
        (etc / name).symlink_to('/nonexistent-k12-target')
    (etc / 'directory.pacnew').mkdir()
    (etc / 'noise.pacnew.bak').write_bytes(b'ignore\n')
    (etc / 'noise.pacsave.x1').write_bytes(b'ignore\n')
    locked = etc / 'locked'
    locked.mkdir()
    (locked / 'hidden.pacnew').write_bytes(b'hidden\n')
    locked.chmod(0)
    prefix = '[2026-10-23T00:00:00-0300] [ALPM] warning: '
    lines = [
        '/etc/plain installed as /etc/plain.pacnew',
        '/etc/linked installed as /etc/linked.pacnew',
        '/etc/linked installed as /etc/linked.pacnew',
        '/etc/link saved as /etc/link.pacsave',
        '/etc/gone saved as /etc/gone.pacsave',
        '/etc/locked/hidden installed as /etc/locked/hidden.pacnew',
        '/usr/share/outside installed as /usr/share/outside.pacnew',
    ]
    (WORK / 'pacman.log').write_text(''.join(prefix + line + '\n' for line in lines))
    (WORK / 'stub').write_text('#!/bin/sh\nexit 0\n')
    (WORK / 'stub').chmod(0o755)
    (WORK / 'empty').write_bytes(b'')
    for directory in ('home', 'tmp', 'seam-dir'):
        (WORK / directory).mkdir()
    (WORK / 'ready').write_text('fixed fixture version 1\n')


def fingerprint():
    rows = []

    def capture(path):
        metadata = path.lstat()
        row = [str(path.relative_to(WORK)), metadata.st_mode, metadata.st_ctime_ns]
        if stat.S_ISLNK(metadata.st_mode):
            row.append(os.readlink(path))
        elif stat.S_ISREG(metadata.st_mode):
            row.append(hashlib.sha256(path.read_bytes()).hexdigest())
        rows.append(row)
        if stat.S_ISDIR(metadata.st_mode):
            try:
                children = sorted(path.iterdir())
            except PermissionError:
                rows.append([str(path.relative_to(WORK)), 'permission denied'])
                return
            for child in children:
                capture(child)

    capture(WORK / 'etc')
    capture(WORK / 'pacman.log')
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument('--label', choices=('pristine', 'mutated', 'restored'), required=True)
ap.add_argument('--census', required=True)
args = ap.parse_args()
setup()
env = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C',
       'HOME': str(WORK / 'home'), 'TMPDIR': str(WORK / 'tmp')}
for name in COMMANDS:
    env['TSUKUROI_' + name] = str(WORK / 'stub')
for name in FILES:
    env['TSUKUROI_' + name] = str(WORK / 'empty')
for name in DIRS:
    env['TSUKUROI_' + name] = str(WORK / 'seam-dir')
env.update(TSUKUROI_ETC_DIR=str(WORK / 'etc'), TSUKUROI_PACMAN_LOG=str(WORK / 'pacman.log'),
           TSUKUROI_FOREIGN_BASELINE='', TSUKUROI_OOM_BASELINE='')
before = fingerprint()
try:
    run = subprocess.run(['timeout', '120', 'bash', args.census], env=env, cwd=WORK,
                         text=True, capture_output=True, timeout=130)
    rc, stdout, stderr = run.returncode, run.stdout, run.stderr
except subprocess.TimeoutExpired as error:
    rc, stdout, stderr = 124, '', str(error)
after = fingerprint()
lines = [line for line in stdout.splitlines() if line.startswith('DRIFT pacnew-plane ')]
reported = dict((name, int(value)) for name, value in re.findall(r'([a-z_]+)=(\d+)', lines[0])) if len(lines) == 1 else None
ok = (rc in (0, 1, 2) and reported == EXPECTED and before == after)
row = {'label': args.label, 'census_sha256': hashlib.sha256(Path(args.census).read_bytes()).hexdigest(),
       'expected': EXPECTED, 'reported': reported, 'exit_code': rc, 'drift_lines': lines,
       'fixture_before_sha256': before, 'fixture_after_sha256': after,
       'fixture_unchanged': before == after, 'detector_pass': ok,
       'detector_exit_code': 0 if ok else 1}
(SEAT / (args.label + '.stdout')).write_text(stdout)
(SEAT / (args.label + '.stderr')).write_text(stderr)
(SEAT / (args.label + '.json')).write_text(json.dumps(row, sort_keys=True, indent=2) + '\n')
print(json.dumps(row, sort_keys=True))
raise SystemExit(0 if ok else 1)
