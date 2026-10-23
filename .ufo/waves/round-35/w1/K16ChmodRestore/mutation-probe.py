#!/usr/bin/env python3
"""Supplementary pristine/mutated/restored probe using unchanged C1 detector functions.
This is not a 24-fixture score receipt. The two official scores use run-receipt.py.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument('--label', required=True)
ap.add_argument('--census', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
seat = Path('/fast/scratch/hyaku/tsukuroi-r35/K16ChmodRestore')
counter_path = seat / 'repo/tools/score-pacnew-arm-r35.py'
spec = importlib.util.spec_from_file_location('unchanged_counter', counter_path)
counter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counter)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows = [{'probe': 1, 'label': a.label, 'counter_sha256': sha(counter_path),
         'census_sha256': sha(a.census), 'detector': 'counter.snapshot + counter.ctimes + counter.parse',
         'fixture': 'literal-expected-values; two unreadable directories (000 and 300)'}]
root = Path(tempfile.mkdtemp(prefix='probe-', dir=seat))
locked = ['locked000', 'locked300']
etc = root / 'etc'
log = root / 'pacman.log'
try:
    (etc / 'ok').mkdir(parents=True)
    (etc / 'directory.pacnew').mkdir()
    (etc / 'ok/a.conf.pacnew').write_text('readable\n')
    (etc / 'ok/b.pacsave').symlink_to('/nonexistent-backup')
    (etc / 'ok/c.pacorig').write_text('original\n')
    (etc / 'ok/d.pacsave.x1').write_text('distractor\n')
    for name, mode in zip(locked, (0o000, 0o300)):
        (etc / name).mkdir()
        (etc / name / 'hidden.pacnew').write_text('hidden\n')
        (etc / name).chmod(mode)
    stamp = '[2026-10-23T00:00:00Z] [ALPM] warning: '
    log.write_text(''.join(stamp + line + '\n' for line in (
        '/etc/ok/a.conf installed as /etc/ok/a.conf.pacnew',
        '/etc/ok/a.conf installed as /etc/ok/a.conf.pacnew',
        '/etc/ok/b saved as /etc/ok/b.pacsave',
        '/etc/gone installed as /etc/gone.pacnew',
        '/etc/locked000/absent installed as /etc/locked000/absent.pacnew',
        '/usr/share/other installed as /usr/share/other.pacnew',
        '/etc/mismatch saved as /etc/other.pacsave',
    )))
    expected = {'pacnew': 1, 'pacsave': 1, 'pacorig': 1, 'unreadable': 2,
                'log_pacnew': 5, 'log_pacsave': 1, 'unlogged': 1, 'gone': 1}
    before_sha = counter.snapshot(str(etc), str(log), locked)
    before_ctimes = counter.ctimes(str(etc), str(log))
    before_modes = {name: stat.S_IMODE((etc / name).stat().st_mode) for name in locked}
    before_log = sha(log)
    work = root / 'harness'
    work.mkdir()
    environment = counter.harness(str(work))
    environment['TSUKUROI_ETC_DIR'] = str(etc)
    environment['TSUKUROI_PACMAN_LOG'] = str(log)
    p = subprocess.run(['timeout', '20', 'bash', a.census], cwd=work, env=environment,
                       capture_output=True, text=True, errors='replace', timeout=25)
    after_ctimes = counter.ctimes(str(etc), str(log))
    after_sha = counter.snapshot(str(etc), str(log), locked)
    after_modes = {name: stat.S_IMODE((etc / name).stat().st_mode) for name in locked}
    after_log = sha(log)
    reported, reason = counter.parse(p.stdout)
    unchanged = before_sha == after_sha and before_ctimes == after_ctimes
    matches = p.returncode in (0, 1, 2) and reported == expected and unchanged
    if not reason and reported != expected:
        reason = 'field mismatch'
    if not unchanged:
        reason = 'fixture mutated'
    if p.returncode not in (0, 1, 2):
        reason = 'exit=%s timed_out=%s' % (p.returncode, p.returncode == 124)
    changed = {name: {'before': before_ctimes.get(name), 'after': after_ctimes.get(name)}
               for name in sorted(before_ctimes.keys() | after_ctimes.keys())
               if before_ctimes.get(name) != after_ctimes.get(name)}
    rows.append({'matches': matches, 'exit': p.returncode, 'reason': None if matches else reason,
                 'expected': expected, 'reported': reported,
                 'before_snapshot_sha256': before_sha, 'after_snapshot_sha256': after_sha,
                 'before_log_sha256': before_log, 'after_log_sha256': after_log,
                 'before_locked_modes': before_modes, 'after_locked_modes': after_modes,
                 'ctime_changes': changed, 'stdout': p.stdout[:65536], 'stderr': p.stderr[:65536],
                 'stdout_bytes': len(p.stdout.encode()), 'stderr_bytes': len(p.stderr.encode())})
    rows.append({'probe_end': 1, 'label': a.label, 'matches': matches, 'census_sha256_after': sha(a.census)})
finally:
    for name in locked:
        target = etc / name
        if target.exists():
            target.chmod(0o700)
    shutil.rmtree(root)
with open(a.out, 'w') as stream:
    for row in rows:
        stream.write(json.dumps(row, sort_keys=True) + '\n')
for row in rows:
    print(json.dumps(row, sort_keys=True))
