#!/usr/bin/env python3
"""One fixed, hermetic behavioral probe; not a second C1 counter score."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

SEAT = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K05LogReaderOnly')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r35/K05LogReaderOnly')
CENSUS = SCRATCH / 'repo/tools/tsukuroi-census.sh'
COUNTER = SCRATCH / 'repo/tools/score-pacnew-arm-r35.py'
ns = {'__name__': 'counter_helpers', '__file__': str(COUNTER)}
exec(compile(COUNTER.read_bytes(), str(COUNTER), 'exec'), ns)
stage = sys.argv[1]
if stage not in ('pristine', 'mutated', 'restored'):
    raise SystemExit('unknown stage')
expected = dict(zip(ns['FIELDS'], (1, 1, 1, 0, 3, 1, 2, 1)))
log_bytes = (
    '[2026-10-01T00:00:00-0300] [ALPM] warning: /etc/sample.conf installed as /etc/sample.conf.pacnew\n'
    '[2026-10-02T00:00:00-0300] [ALPM] warning: /etc/sample.conf installed as /etc/sample.conf.pacnew\n'
    '[2026-10-03T00:00:00-0300] [ALPM] warning: /etc/removed saved as /etc/removed.pacsave\n'
    '[2026-10-04T00:00:00-0300] [ALPM] warning: /usr/share/vendor installed as /usr/share/vendor.pacnew\n'
    '[2026-10-05T00:00:00-0300] [ALPM] warning: /etc/a saved as /etc/b.pacsave\n'
    '[2026-10-06T00:00:00-0300] [ALPM-SCRIPTLET] warning: /etc/a installed as /etc/a.pacnew\n'
).encode()
with tempfile.TemporaryDirectory(prefix='three-state-', dir=SCRATCH) as tmp:
    root = Path(tmp)
    etc = root / 'etc'
    etc.mkdir()
    for name in ('sample.conf.pacnew', 'old.conf.pacsave', 'original.pacorig'):
        (etc / name).write_bytes(b'x\n')
    log = root / 'pacman.log'
    log.write_bytes(log_bytes)
    work = root / 'harness'
    work.mkdir()
    child_env = ns['harness'](str(work))
    child_env['TSUKUROI_ETC_DIR'] = str(etc)
    child_env['TSUKUROI_PACMAN_LOG'] = str(log)
    before = (ns['snapshot'](str(etc), str(log), []), ns['ctimes'](str(etc), str(log)))
    try:
        result = subprocess.run(['timeout', '25', 'bash', str(CENSUS)], env=child_env,
                                cwd=work, capture_output=True, text=True, timeout=30)
        exit_code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        exit_code, stdout, stderr = 124, '', str(exc)
    reported, reason = ns['parse'](stdout)
    after = (ns['snapshot'](str(etc), str(log), []), ns['ctimes'](str(etc), str(log)))
    fixture_unchanged = before == after
    matches = exit_code in (0, 1, 2) and reported == expected and fixture_unchanged
    if reason is None and reported != expected:
        reason = 'field mismatch'
    record = {'stage': stage, 'census_sha256': hashlib.sha256(CENSUS.read_bytes()).hexdigest(),
              'counter_sha256': hashlib.sha256(COUNTER.read_bytes()).hexdigest(),
              'expected': expected, 'reported': reported, 'matches': matches,
              'reason': None if matches else reason, 'census_exit_code': exit_code,
              'fixture_unchanged': fixture_unchanged, 'stdout': stdout, 'stderr': stderr}
    (SEAT / ('probe-' + stage + '.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({key: value for key, value in record.items() if key not in ('stdout', 'stderr')}, sort_keys=True))
