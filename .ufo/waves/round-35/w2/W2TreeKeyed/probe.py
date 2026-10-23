#!/usr/bin/env python3
"""One bounded semantic detector, reused for pristine/mutated/restored arm bytes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path('/fast/scratch/hyaku/tsukuroi-r35/W2TreeKeyed')
EVIDENCE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2TreeKeyed')
phase = sys.argv[1]
assert phase in ('pristine', 'mutated', 'restored')
fixture = ROOT / 'probe-fixture'
etc = fixture / 'etc'
etc.mkdir(parents=True, exist_ok=True)
if not (etc / 'target').exists():
    (etc / 'target').write_text('plain target\n')
    os.symlink(str(etc / 'target'), etc / 'link.pacnew')
    os.symlink(str(etc), etc / 'link.pacsave')
    os.symlink('/nonexistent/r35-control', etc / 'link.pacorig')
    os.mkfifo(etc / 'pipe.pacnew')
    os.symlink('/nonexistent/r35-extra', etc / 'extra.pacnew')
    (fixture / 'pacman.log').write_text('')
expected = dict(pacnew=3, pacsave=1, pacorig=1, unreadable=0,
                log_pacnew=0, log_pacsave=0, unlogged=5, gone=0)
arm = ROOT / 'arm.sh'
env = dict(PATH='/usr/bin:/bin', LANG='C', LC_ALL='C',
           TSUKUROI_ETC_DIR=str(etc), PACMAN_LOG=str(fixture / 'pacman.log'),
           TMPDIR=str(ROOT))
p = subprocess.run(['bash', '-c', '. "$1"; r35_arm', 'detector', str(arm)],
                   env=env, cwd=ROOT, capture_output=True, text=True, timeout=30)
rows = [line for line in p.stdout.splitlines() if line.startswith('DRIFT pacnew-plane ')]
reported = None
if len(rows) == 1:
    try:
        reported = {k: int(v) for k, v in (tok.split('=', 1) for tok in rows[0].split()[2:])}
    except (ValueError, TypeError):
        pass
result = dict(phase=phase, arm_sha256=hashlib.sha256(arm.read_bytes()).hexdigest(),
              command=['bash', '-c', '. "$1"; r35_arm', 'detector', str(arm)],
              expected=expected, reported=reported, stdout=p.stdout, stderr=p.stderr,
              exit_code=p.returncode, detector_passed=(p.returncode == 0 and reported == expected))
(EVIDENCE / ('probe-' + phase + '.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, sort_keys=True))
sys.exit(0 if result['detector_passed'] else 1)
