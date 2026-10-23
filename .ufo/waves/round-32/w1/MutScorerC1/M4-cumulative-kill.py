#!/usr/bin/env python3
"""Counter for tsukuroi round 32, claim C1 (ADJ-04 sibling handoff routing).

Scores whether the host census `tools/tsukuroi-census.sh` at a revision routes
sibling-owned findings to mori (PROVINCE.md ADJ-04 row) by printing HANDOFF lines.

FROZEN line grammar (the census must print, after the PLANE lines and before or
after the TSUKUROI_CENSUS line):
  HANDOFF ADJ-04 mori class=kill-events value=<n> kind=dated-event state=prepared
  HANDOFF ADJ-04 mori class=coredumps  value=<m> kind=dated-event state=prepared
No HANDOFF line otherwise. A cumulative counter alone (vmstat oom_kill > 0,
memory.events oom_kill flag) is NOT a dated event and must not produce a
kill-events line.

FROZEN PREDICATE:
A scenario is routed when the census at REV, run against that scenario's fixture, prints exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value equal to the planted dated kill events when there are any, one class=coredumps line with value equal to the planted coredump entries when there are any, no HANDOFF line otherwise, and none for a cumulative counter alone), and its PLANE lines, TSUKUROI_CENSUS line and exit code equal those of the base census 58cc2e0b on the same fixture.

Harness: every host read of the census is overridable by a TSUKUROI_* variable
(probe surface documented in the census header). This scorer reproduces the
census' own hermetic fixture mechanism inside itself: per scenario it writes a
fixture tree (stub command dispatcher + fixture files) into a scratch directory,
exports the census at REV and at the frozen base with `git archive` into the
same scratch tree, and runs both against the SAME fixture with a minimal
environment (PATH = stub dir + /usr/bin:/bin, LC_ALL=C, private HOME/TMPDIR,
only the TSUKUROI_* overrides the fixture needs). The stub directory shadows
every probe command, so no live command is reachable; every probe call is
logged and the log is checked (hermeticity gate), and the run's own output must
carry the fixture's hostname and package sample (live-read gate). Nothing in
the fixture tree, in a path, or in an environment variable names the scenario
type, the planted counts or the expected HANDOFF set. The live host is never
written to and never read by a probe.

Reading rules of this counter:
  * the comparison set is the census' ADJ-04/mori HANDOFF lines; a HANDOFF line
    for another row or another recipient is recorded but does not decide the
    verdict (the frozen grammar is about the ADJ-04 mori handoff);
  * class, value, kind and state are compared exactly; trailing `key=value`
    fields after `state=prepared` are accepted (the census may add a capture
    time or window) and never compared;
  * a HANDOFF line that carries the four fields in another order or misses one
    is malformed and never matches the expected set.

Usage:
  python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>]
        [--scratch <dir>] [--seed <hex|int>] [--scenarios N] [--keep-scratch]
Output: one JSON line per scenario (`id`, `type`, `planted`, `expected`,
`observed`, `plane_parity`, `routed`, ...), then a summary JSON line with
`scenarios`, `routed`, `seed`, `harness_errors`, `scorer_sha256`, `revision`,
`base`, `predicate_label` and `scenarios_per_type`.
Exit 0 when routed == scenarios and no harness error, 1 otherwise, 2 on harness
error.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time

VERSION = 1
BASE = '58cc2e0bfaa4580d47f6817537c8d5c82dbe9c92'
DEFAULT_LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
PREDICATE_LABEL = 'routed'
PREDICATE = (
    'A scenario is routed when the census at REV, run against that scenario\'s fixture, prints '
    'exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value '
    'equal to the planted dated kill events when there are any, one class=coredumps line with value '
    'equal to the planted coredump entries when there are any, no HANDOFF line otherwise, and none '
    'for a cumulative counter alone), and its PLANE lines, TSUKUROI_CENSUS line and exit code equal '
    'those of the base census 58cc2e0b on the same fixture.'
)

TYPES = (
    'none',
    'kill-events',
    'coredumps',
    'both',
    'cumulative-only',
    'cumulative+coredumps',
    'tsukuroi-only',
)
N_SCENARIOS = 24

# retained window of the fixture journal (the list-boots bounds) and the two
# declared baseline minutes (never planted, so every planted cluster stays new)
WINDOW_DAYS = ('2026-10-11', '2026-10-12', '2026-10-13', '2026-10-14')
BASELINE_MINUTES = ('2026-10-13 23:44', '2026-10-14 13:10')
PROC_NAMES = ('python3', 'node', 'ffmpeg', 'code', 'cargo', 'java', 'bash', 'rsync', 'dockerd')

HANDOFF_RE = re.compile(
    r'^HANDOFF\s+ADJ-04\s+mori\s+class=(\S+)\s+value=(\S+)\s+kind=(\S+)\s+state=(\S+)(?:\s+(.*))?$')


# --------------------------------------------------------------------------
# the census' fixture mechanism, reproduced here (stub dispatcher + fixture)
# --------------------------------------------------------------------------
DISPATCH = r'''#!/usr/bin/env bash
# tsukuroi-census-r32 scorer fixture dispatcher: answers from the fixture tree only.
set -uo pipefail
name=${0##*/}
fix='__FX__'
log='__LOG__'
rc_of() { local f="$fix/$1.rc"; if [ -f "$f" ]; then cat "$f"; else printf 0; fi; }
out_of() { local f="$fix/$1"; if [ -f "$f" ]; then cat "$f"; fi; }
args="$*"
printf '%s\t%s\n' "$name" "$args" >> "$log"
case "$name" in
  pacman)
    case "${1:-}" in
      -Qq) out_of pq; exit "$(rc_of pq)" ;;
      -Qkk) out_of qkk.out; exit "$(rc_of qkk)" ;;
      -Qm) out_of pm; exit "$(rc_of pm)" ;;
      -Q) out_of q; exit "$(rc_of q)" ;;
      -Sl) out_of sl; exit "$(rc_of sl)" ;;
      -Qu) out_of qu; exit "$(rc_of qu)" ;;
      -Sup) out_of sup; exit "$(rc_of sup)" ;;
      -Suu) out_of suu; exit "$(rc_of suu)" ;;
      *) printf 'fixture pacman: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac ;;
  pacman-conf) out_of pconf; exit "$(rc_of pconf)" ;;
  systemctl)
    case "$args" in
      *is-system-running*) out_of sysrunning; exit "$(rc_of sysrunning)" ;;
      *is-active*) out_of boottarget; exit "$(rc_of boottarget)" ;;
      *list-units*failed*) out_of failedunits; exit "$(rc_of failedunits)" ;;
      *list-unit-files*) out_of timerlist; exit "$(rc_of timerlist)" ;;
      *show*ActiveState*) out_of timeractivestate; exit "$(rc_of timeractivestate)" ;;
      *show*Result*) out_of timerresult; exit "$(rc_of timerresult)" ;;
      *) printf 'fixture systemctl: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac ;;
  dmesg)
    case "$args" in
      --level*) out_of dmesg.out; exit "$(rc_of dmesg)" ;;
      *) out_of dmesg-all.out; exit "$(rc_of dmesg-all)" ;;
    esac ;;
  journalctl)
    case "$args" in
      *"-o short-iso-precise"*)
        case "$args" in
          *--grep*oom_reaper*) out_of oomwin-kernel; exit "$(rc_of oomwin-kernel)" ;;
          *--grep*"OOM killer"*) out_of oomwin-attrib; exit "$(rc_of oomwin-attrib)" ;;
          *--grep*"status=9"*) out_of oomwin-sigkill; exit "$(rc_of oomwin-sigkill)" ;;
          *) printf 'fixture journalctl: unexpected window args: %s\n' "$args" >&2; exit 64 ;;
        esac ;;
      *--grep*"OOM killer"*) out_of oom-attrib.json; exit "$(rc_of oom-attrib)" ;;
      *--grep*oom_reaper*) out_of oom-kernel.json; exit "$(rc_of oom-kernel)" ;;
      *--grep*"status=9"*) out_of oom-sigkill.json; exit "$(rc_of oom-sigkill)" ;;
      *--list-boots*) out_of listboots; exit "$(rc_of listboots)" ;;
      *"-p err"*)
        case "$args" in
          *"-k "*) out_of ring-err.json; exit "$(rc_of ring-err)" ;;
          *) out_of journal-err.json; exit "$(rc_of journal-err)" ;;
        esac ;;
      *"-n 1"*) out_of journal-last; exit "$(rc_of journal-last)" ;;
      *) out_of journal-all.json; exit "$(rc_of journal-all)" ;;
    esac ;;
  nvidia-smi) out_of smi.out; exit "$(rc_of smi)" ;;
  lsmod) out_of lsmod; exit "$(rc_of lsmod)" ;;
  expac)
    case "${1:-}" in
      -S) out_of expacsl; exit "$(rc_of expacsl)" ;;
      *) printf 'fixture expac: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac ;;
  vercmp) printf '0\n' ;;
  *) printf 'fixture dispatcher: unknown command %s\n' "$name" >&2; exit 96 ;;
esac
'''

STUB_COMMANDS = ('pacman', 'pacman-conf', 'systemctl', 'dmesg', 'journalctl',
                 'nvidia-smi', 'lsmod', 'expac', 'vercmp')

# probes that must be answered by the stub dispatcher for a run to count as
# hermetic (a live command would leave these absent)
REQUIRED_PROBES = ('pacman', 'pacman-conf', 'systemctl', 'dmesg', 'journalctl',
                   'nvidia-smi', 'lsmod', 'expac')


def w(path, text):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def plant_kill_events(rng, n):
    """n dated kill events, one per distinct minute inside the retained window.

    Each event is planted in the shape of the census' own declared wave A: a
    kernel OOM line (the kill) plus the systemd attribution line, both at the
    same minute, so the census' cluster count (its dated-event count) is n.
    """
    used = set()
    events = []
    attempts = 0
    while len(events) < n and attempts < 500:
        attempts += 1
        day = rng.choice(WINDOW_DAYS)
        hh = rng.randint(0, 23)
        mi = rng.randint(0, 59)
        key = '%s %02d:%02d' % (day, hh, mi)
        if key in used or key in BASELINE_MINUTES:
            continue
        used.add(key)
        events.append({
            'day': day, 'hh': hh, 'mi': mi,
            'sec': rng.randint(0, 59), 'us': rng.randint(0, 999999),
            'off': rng.choice(('-03:00', '+00:00', '+02:00')),
            'pid': rng.randint(1000, 999999),
            'proc': rng.choice(PROC_NAMES),
            'unit': 'app-%s.scope' % rng.choice(('x', 'y', 'z', 'w')),
        })
    if len(events) != n:
        raise RuntimeError('could not plant %d distinct kill-event minutes' % n)
    return events


def plant_coredumps(rng, m):
    """m distinct systemd-coredump entries in boot 0's error stream."""
    out = []
    for _ in range(m):
        out.append({
            'pid': rng.randint(1000, 999999),
            'proc': rng.choice(PROC_NAMES),
            'signal': rng.choice((11, 6, 4, 8, 7)),
            'ts': rng.randint(1700000000, 1800000000),
        })
    return out


def build_fixture(fx, scen, rng):
    """Write the fixture tree for one scenario. Returns the planted facts."""
    os.makedirs(fx, exist_ok=True)

    def put(name, text):
        path = os.path.join(fx, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        w(path, text)

    # --- healthy base fixture (the census' own fx_default shape) ---
    put('pq', 'alpha\nbeta\ngamma\ndelta\n')
    put('qkk.out', 'alpha: 10 total files, 0 altered files\n'
                    'beta: 20 total files, 0 altered files\n')
    put('qkk.rc', '0\n')
    put('pm', '')
    put('fbase', '')              # foreign baseline: file(0), no drift/gone
    put('pconf', '')              # pacman-conf IgnorePkg/IgnoreGroup: empty
    put('pacman.conf', 'HoldPkg = pacman glibc\n')
    put('qu', '')
    put('qu.rc', '1\n')           # no update candidates
    put('sup', '')
    put('sup.rc', '0\n')
    put('suu', '')
    put('suu.rc', '0\n')
    put('q', 'alpha 1.0-1\nbeta 2.0-1\n')
    put('sl', 'core alpha 1.0-1\ncore beta 2.0-1\n')
    put('expacsl', 'alpha\t1.0-1\nbeta\t2.0-1\n')
    put('pacman.log', "[2026-10-13T16:37:58-0300] [PACMAN] Running "
                      "'pacman -S --needed --noconfirm fixture-pkg'\n")
    put('sysrunning', 'running\n')
    put('sysrunning.rc', '0\n')
    put('failedunits', '')
    put('timerlist', 'ai-usage.timer enabled enabled\n')
    put('timerresult', 'success\n')
    put('timeractivestate', 'active\n')
    put('dmesg.out', '')
    put('dmesg.rc', '1\n')        # dmesg restricted on the measured host
    put('dmesg-all.out', '')
    put('dmesg-all.rc', '0\n')
    put('smi.out', '')
    put('smi.rc', '1\n')          # no nvidia-smi on the measured host
    put('lsmod', '')
    put('dmesg_restrict', '1\n')
    put('boottarget', 'active\n')
    put('boottarget.rc', '0\n')
    put('journal-all.json', '{"MESSAGE":"fixture: kernel line 1"}\n'
                            '{"MESSAGE":"fixture: kernel line 2"}\n'
                            '{"MESSAGE":"fixture: kernel line 3"}\n')
    put('journal-all.rc', '0\n')
    put('journal-last', '{"MESSAGE":"fixture: journal last entry"}\n')
    put('journal-last.rc', '0\n')
    put('ring-err.json', '')      # this boot's kernel error ring (empty)
    put('ring-err.rc', '0\n')
    put('listboots',
        'IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY\n'
        ' -1 73a8e2fc20cc48749b3cbd24ed5dc7c1 Sun 2026-10-11 19:02:51 -03 '
        'Tue 2026-10-13 10:57:30 -03\n'
        '  0 d7f0bc8d938e4249b4a1f250cbfacf58 Tue 2026-10-13 11:02:03 -03 '
        'Wed 2026-10-14 11:42:34 -03\n')
    put('listboots.rc', '0\n')
    # declared OOM waves, dated OUTSIDE the retained window: retention loss
    # only (never a missing declared wave), and every planted cluster is new.
    put('obase', '2026-09-30 02:00 Z attrib+kill9 declared wave older than the window\n')
    put('meminfo', 'MemTotal: 1000000 kB\nMemAvailable: 900000 kB\n'
                   'SwapTotal: 8000000 kB\nSwapFree: 8000000 kB\nShmem: 1000 kB\n')
    put('pressure/memory', 'some avg10=0.00 avg60=0.00 avg300=0.00 total=0\n'
                           'full avg10=0.00 avg60=0.00 avg300=0.00 total=0\n')
    # package/channel trees; the db stamp is the file's own mtime, so it is set
    # one hour in the past: the age is then exactly 0 days for any wall clock
    # (a fixed mtime would make the plane line depend on the run date)
    one_hour_ago = time.time() - 3600
    for db in ('core.db', 'omarchy.db', 'offline.db'):
        p = os.path.join(fx, 'pacmandb', 'sync', db)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        w(p, '')
        os.utime(p, (one_hour_ago, one_hour_ago))
    # cgroup tree (memory-events presence flags + swap anchors)
    cg = os.path.join(fx, 'cgroup')
    for rel in ('user.slice',
                'user.slice/user-1000.slice',
                'user.slice/user-1000.slice/user@1000.service'):
        os.makedirs(os.path.join(cg, rel), exist_ok=True)
    ev = 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n'
    for rel in ('user.slice',
                'user.slice/user-1000.slice',
                'user.slice/user-1000.slice/user@1000.service'):
        put('cgroup/%s/memory.events' % rel, ev)
        put('cgroup/%s/memory.events.local' % rel, ev)
    put('cgroup/user.slice/user-1000.slice/memory.swap.events', 'high 0\nmax 0\nfail 0\n')
    put('cgroup/user.slice/user-1000.slice/memory.swap.peak', '0\n')
    put('cgroup/user.slice/user-1000.slice/memory.stat', 'pswpin 0\npswpout 0\n')
    put('cgroup/user.slice/user-1000.slice/memory.max', 'max\n')
    put('cgroup/user.slice/user-1000.slice/memory.high', '0\n')
    put('cgroup/user.slice/user-1000.slice/memory.oom.group', '0\n')
    # root metadata arm, pci inventory, device nodes
    for d in ('root', 'pci', 'dev'):
        os.makedirs(os.path.join(fx, d), exist_ok=True)
        os.chmod(os.path.join(fx, d), 0o755)
    put('hostname', scen['host_token'] + '\n')
    # memory journal arms (this boot, entry level): empty unless planted
    put('oom-kernel.json', '')
    put('oom-kernel.rc', '0\n')
    put('oom-attrib.json', '')
    put('oom-attrib.rc', '0\n')
    put('oom-sigkill.json', '')
    put('oom-sigkill.rc', '0\n')
    # retained-window scans
    put('oomwin-kernel', '')
    put('oomwin-kernel.rc', '1\n')
    put('oomwin-attrib', '')
    put('oomwin-attrib.rc', '1\n')
    put('oomwin-sigkill', '')
    put('oomwin-sigkill.rc', '1\n')

    n = scen['n']
    m = scen['m']

    # --- planted dated kill events (retained window) ---
    if n:
        events = plant_kill_events(rng, n)
        kern, attrib, sigkill = [], [], []
        for e in events:
            ts = '%sT%02d:%02d:%02d.%06d%s' % (e['day'], e['hh'], e['mi'], e['sec'],
                                                e['us'], e['off'])
            kern.append('%s fixture-host kernel: Out of memory: Killed process %d (%s)'
                        % (ts, e['pid'], e['proc']))
            attrib.append('%s fixture-host systemd[%d]: %s: The kernel OOM killer killed '
                          'some processes in this unit.' % (ts, e['pid'], e['unit']))
            sigkill.append('%s fixture-host systemd[1]: user@1000.service: Main process '
                           'exited, code=killed, status=9/KILL' % ts)
        put('oomwin-kernel', '\n'.join(kern) + '\n')
        put('oomwin-kernel.rc', '0\n')
        put('oomwin-attrib', '\n'.join(attrib) + '\n')
        put('oomwin-attrib.rc', '0\n')
        put('oomwin-sigkill', '\n'.join(sigkill) + '\n')
        put('oomwin-sigkill.rc', '0\n')

    # --- planted coredump entries (boot 0) ---
    if m:
        dumps = plant_coredumps(rng, m)
        lines = []
        for d in dumps:
            lines.append(json.dumps({
                '__REALTIME_TIMESTAMP': str(d['ts'] * 1000000),
                '_BOOT_ID': 'd7f0bc8d938e4249b4a1f250cbfacf58',
                '_TRANSPORT': 'journal',
                'SYSLOG_IDENTIFIER': 'systemd-coredump',
                'PRIORITY': '3',
                'MESSAGE': ('Main process terminated with signal %d '
                            '(Segmentation fault) of user 1000' % d['signal']),
            }, sort_keys=True, separators=(',', ':')))
        put('journal-err.json', '\n'.join(lines) + '\n')
    else:
        put('journal-err.json', '')
    put('journal-err.rc', '0\n')

    # --- cumulative counters (never a dated event) ---
    if scen['cumulative']:
        if scen['cumulative_vmstat']:
            put('vmstat', 'oom_kill %d\n' % scen['cumulative_value'])
        else:
            put('vmstat', 'oom_kill 0\n')
        if scen['cumulative_cgroup']:
            put('cgroup/user.slice/user-1000.slice/memory.events',
                'low 0\nhigh 0\nmax 0\noom 0\noom_kill %d\noom_group_kill 0\n'
                'sock_throttled 0\n' % scen['cumulative_value'])
    else:
        put('vmstat', 'oom_kill 0\n')

    # --- a finding the lane retains (no kill event, no coredump) ---
    if scen['tsukuroi_finding'] == 'failed-unit':
        put('failedunits', 'alpha.service loaded failed failed fixture unit\n')
    elif scen['tsukuroi_finding'] == 'package-drift':
        put('qkk.out', 'alpha: 10 total files, 2 altered files\n'
                       'beta: 20 total files, 0 altered files\n')
    elif scen['tsukuroi_finding'] == 'journal-other-error':
        # a boot-0 error entry the lane retains (not a coredump, not a kernel entry)
        put('journal-err.json', json.dumps({
            '__REALTIME_TIMESTAMP': '1800000000000000',
            '_BOOT_ID': 'd7f0bc8d938e4249b4a1f250cbfacf58',
            '_TRANSPORT': 'journal',
            'SYSLOG_IDENTIFIER': 'fixture-app',
            'PRIORITY': '3',
            'MESSAGE': 'fixture: retained unit error entry',
        }, sort_keys=True, separators=(',', ':')) + '\n')
    return {'kill_events': n, 'coredumps': m}


# --------------------------------------------------------------------------
# census export and run
# --------------------------------------------------------------------------
def export_census(lane, rev, dest, timeout=120):
    """git archive <rev> tools/tsukuroi-census.sh -> dest/tools/tsukuroi-census.sh."""
    os.makedirs(dest, exist_ok=True)
    tarpath = os.path.join(dest, 'census.tar')
    with open(tarpath, 'wb') as fh:
        proc = subprocess.run(
            ['git', '-C', lane, 'archive', '--format=tar', rev, 'tools/tsukuroi-census.sh'],
            stdout=fh, stderr=subprocess.PIPE, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError('git archive %s failed: %s'
                           % (rev, proc.stderr.decode('utf-8', 'replace').strip()))
    with tarfile.open(tarpath) as tf:
        tf.extractall(dest, filter='data')
    path = os.path.join(dest, 'tools', 'tsukuroi-census.sh')
    if not os.path.isfile(path):
        raise RuntimeError('git archive %s produced no tools/tsukuroi-census.sh' % rev)
    os.chmod(path, 0o755)
    os.unlink(tarpath)
    return path


def census_env(stubdir, fx, home, tmp):
    """Minimal environment: stub PATH, LC_ALL=C, private HOME/TMPDIR, overrides only."""
    return {
        'PATH': '%s:/usr/bin:/bin' % stubdir,
        'LC_ALL': 'C',
        'HOME': home,
        'TMPDIR': tmp,
        'TSUKUROI_PACMAN': os.path.join(stubdir, 'pacman'),
        'TSUKUROI_PACMAN_CONF': os.path.join(stubdir, 'pacman-conf'),
        'TSUKUROI_PACMAN_CONF_FILE': os.path.join(fx, 'pacman.conf'),
        'TSUKUROI_PACMAN_DB': os.path.join(fx, 'pacmandb'),
        'TSUKUROI_ROOT_DIR': os.path.join(fx, 'root'),
        'TSUKUROI_FOREIGN_BASELINE': os.path.join(fx, 'fbase'),
        'TSUKUROI_SYSTEMCTL': os.path.join(stubdir, 'systemctl'),
        'TSUKUROI_DMESG': os.path.join(stubdir, 'dmesg'),
        'TSUKUROI_JOURNALCTL': os.path.join(stubdir, 'journalctl'),
        'TSUKUROI_NVIDIA_SMI': os.path.join(stubdir, 'nvidia-smi'),
        'TSUKUROI_LSMOD': os.path.join(stubdir, 'lsmod'),
        'TSUKUROI_PCI_SYSFS': os.path.join(fx, 'pci'),
        'TSUKUROI_DEV_DIR': os.path.join(fx, 'dev'),
        'TSUKUROI_HOSTNAME_FILE': os.path.join(fx, 'hostname'),
        'TSUKUROI_DMESG_RESTRICT_FILE': os.path.join(fx, 'dmesg_restrict'),
        'TSUKUROI_CGROUP_ROOT': os.path.join(fx, 'cgroup'),
        'TSUKUROI_PRESSURE_FILE': os.path.join(fx, 'pressure', 'memory'),
        'TSUKUROI_MEMINFO_FILE': os.path.join(fx, 'meminfo'),
        'TSUKUROI_VMSTAT_FILE': os.path.join(fx, 'vmstat'),
        'TSUKUROI_OOM_BASELINE': os.path.join(fx, 'obase'),
        'TSUKUROI_PACMAN_LOG': os.path.join(fx, 'pacman.log'),
        'TSUKUROI_EXPAC': os.path.join(stubdir, 'expac'),
        'TSUKUROI_VERCMP': os.path.join(stubdir, 'vercmp'),
    }


def run_census(script, env, timeout):
    """Run the census; returns (rc, stdout+stderr). The process tree is killed."""
    proc = subprocess.Popen(['/usr/bin/bash', script], env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, start_new_session=True)
    try:
        out, _ = proc.communicate(timeout=timeout)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass
        out, _ = proc.communicate()
        rc = 124
    return rc, out.decode('utf-8', 'replace')


def parse_output(text):
    planes = [l for l in text.splitlines() if l.startswith('PLANE ')]
    rollup = ''
    handoff_raw = []
    for l in text.splitlines():
        if l.startswith('TSUKUROI_CENSUS:'):
            rollup = l
        elif l.startswith('HANDOFF '):
            handoff_raw.append(l)
    return planes, rollup, handoff_raw


def parse_handoff(raw_lines):
    """-> (compared, other): the ADJ-04/mori lines (parsed) and any other HANDOFF line.

    The frozen grammar fixes the order `class= value= kind= state=`; trailing
    `key=value` fields after `state=prepared` are accepted (the census may add a
    capture time or window) and recorded, never compared. A line that does not
    carry the four fields in the frozen order is malformed and never matches.
    """
    compared = []
    other = []
    for raw in raw_lines:
        m = HANDOFF_RE.match(raw)
        if not m:
            if raw.startswith('HANDOFF ADJ-04 mori'):
                compared.append({'raw': raw, 'parsed': False})
            else:
                other.append(raw)
            continue
        rest = (m.group(5) or '').split()
        try:
            value = int(m.group(2))
        except ValueError:
            value = None
        compared.append({
            'raw': raw,
            'parsed': value is not None,
            'class': m.group(1),
            'value': value,
            'kind': m.group(3),
            'state': m.group(4),
            'trailing': rest,
        })
    return compared, other


def observed_set(parsed):
    """The comparable set: (class, value, kind, state) for well-formed lines."""
    good = []
    for h in parsed:
        if not h.get('parsed'):
            good.append(('MALFORMED', h['raw'], None, None))
            continue
        good.append((h['class'], h['value'], h['kind'], h['state']))
    return sorted(good)


def expected_set(scen):
    want = []
    if scen['n']:
        want.append(('kill-events', scen['n'], 'dated-event', 'prepared'))
    if scen['m']:
        want.append(('coredumps', scen['m'], 'dated-event', 'prepared'))
    if scen['type'] == 'cumulative-only':
        want.append(('kill-events', 1, 'dated-event', 'prepared'))
    return sorted(want)


# --------------------------------------------------------------------------
# planted-fact verification (harness gate)
# --------------------------------------------------------------------------
def plane_value(planes, prefix, key):
    for l in planes:
        if l.startswith(prefix):
            m = re.search(r'(?:^|[ (])%s=(\d+)' % re.escape(key), l)
            if m:
                return int(m.group(1))
    return None


def verify_planted(planes, scen):
    """The base census' PLANE lines must show the planted facts. -> error string or None."""
    n, m = scen['n'], scen['m']
    errs = []
    # the census' own dated-event count is its cluster count; the kill-event
    # line count, the kill-process count and the attribution count are planted
    # in the same shape and must agree with it
    for key in ('clusters', 'C1_kernel', 'killed_process', 'C2_events', 'C3_events'):
        got = plane_value(planes, 'PLANE oom:', key)
        if got is None:
            errs.append('oom plane has no %s field' % key)
        elif got != n:
            errs.append('oom plane %s=%d, planted %d' % (key, got, n))
    got = plane_value(planes, 'PLANE journal:', 'coredump')
    if got is None:
        errs.append('journal plane has no coredump field')
    elif got != m:
        errs.append('journal plane coredump=%d, planted %d' % (got, m))
    # a planted cumulative counter must be visible too, else the scenario
    # would not prove that a cumulative counter is not a dated event
    if scen['cumulative_vmstat']:
        got = None
        for l in planes:
            if l.startswith('PLANE oom:'):
                m = re.search(r'ledger=vmstat\.oom_kill=(\d+)', l)
                if m:
                    got = int(m.group(1))
        if got is None:
            errs.append('oom plane has no ledger=vmstat.oom_kill field')
        elif got != scen['cumulative_value']:
            errs.append('oom plane ledger=vmstat.oom_kill=%d, planted %d'
                        % (got, scen['cumulative_value']))
    if scen['cumulative_cgroup']:
        got = plane_value(planes, 'PLANE drivers:', 'C4_present')
        if got is None:
            errs.append('drivers plane has no C4_present field')
        elif got < 1:
            errs.append('drivers plane C4_present=%d, planted >=1' % got)
    return '; '.join(errs) if errs else None


def check_hermetic(logpath, out, scen):
    """The run must have been answered by the stubs, on the fixture, only."""
    errs = []
    try:
        with open(logpath, encoding='utf-8') as fh:
            calls = [l.rstrip('\n') for l in fh if l.strip()]
    except OSError:
        calls = []
    if not calls:
        errs.append('no stub probe was reached')
    seen = set(c.split('\t', 1)[0] for c in calls)
    for probe in REQUIRED_PROBES:
        if probe not in seen:
            errs.append('probe %s never reached the stub' % probe)
    if ('host=%s' % scen['host_token']) not in out:
        errs.append('hostname override not honoured (possible live read)')
    root = os.path.join(scen['fx'], 'root')
    if ('root_dir=%s' % root) not in out:
        errs.append('root override not honoured (possible live read)')
    if 'alpha,beta,gamma,delta' not in out:
        errs.append('package sample is not the fixture one (possible live read)')
    return '; '.join(errs) if errs else None


# --------------------------------------------------------------------------
# scenario plan
# --------------------------------------------------------------------------
def make_scenarios(rng, count):
    types = []
    for t in TYPES:
        types.extend([t, t])
    while len(types) < count:
        types.append(rng.choice(TYPES))
    if len(types) > count:
        types = types[:count]
    rng.shuffle(types)
    scen = []
    for i, t in enumerate(types):
        n = m = 0
        cumulative = False
        cum_vm = False
        cum_cg = False
        finding = ''
        if t == 'kill-events':
            n = rng.randint(1, 9)
        elif t == 'coredumps':
            m = rng.randint(1, 9)
        elif t == 'both':
            n = rng.randint(1, 9)
            m = rng.randint(1, 9)
        elif t == 'cumulative-only':
            cumulative = True
            cum_vm = rng.random() < 0.5
            cum_cg = rng.random() < 0.5
            if not (cum_vm or cum_cg):
                cum_vm = True
        elif t == 'cumulative+coredumps':
            m = rng.randint(1, 9)
            cumulative = True
            cum_vm = rng.random() < 0.5
            cum_cg = rng.random() < 0.5
            if not (cum_vm or cum_cg):
                cum_cg = True
        elif t == 'tsukuroi-only':
            finding = rng.choice(('failed-unit', 'package-drift', 'journal-other-error'))
        scen.append({
            'id': 's%02d' % (i + 1),
            # the directory the census reads is random: it carries no type, no
            # expected HANDOFF set and no planted count
            'dirname': '%016x' % rng.getrandbits(64),
            'type': t,
            'n': n,
            'm': m,
            'cumulative': cumulative,
            'cumulative_vmstat': cum_vm,
            'cumulative_cgroup': cum_cg,
            'cumulative_value': rng.randint(1, 9),
            'tsukuroi_finding': finding,
            'host_token': 'fx%010x' % rng.getrandbits(40),
        })
    return scen


def main():
    ap = argparse.ArgumentParser(description='score census ADJ-04 handoff routing (round 32, C1)')
    ap.add_argument('--revision', default=None, help='revision to score (default: repo HEAD)')
    ap.add_argument('--lane', default=DEFAULT_LANE, help='repo holding the census (default: lane)')
    ap.add_argument('--scratch', default=None, help='scratch dir (default: a private temp dir)')
    ap.add_argument('--seed', default=None, help='seed for replay (default: fresh os.urandom)')
    ap.add_argument('--scenarios', type=int, default=N_SCENARIOS, help='scenario count (default 24)')
    ap.add_argument('--keep-scratch', action='store_true', help='keep the scratch tree')
    ap.add_argument('--timeout', type=int, default=120, help='per-census-run timeout (s)')
    ap.add_argument('--budget', type=int, default=840, help='total wall-clock budget (s)')
    args = ap.parse_args()

    t0 = time.time()
    lane = os.path.abspath(args.lane)
    if not os.path.isdir(lane):
        sys.stderr.write('scorer: lane repo not found: %s\n' % lane)
        return 2

    if args.seed is None:
        seed = int.from_bytes(os.urandom(8), 'big')
        seed_text = '%016x' % seed
    else:
        seed_text = args.seed.strip()
        try:
            seed = int(seed_text, 16) if re.fullmatch(r'[0-9a-fA-F]{1,16}', seed_text) \
                else int(seed_text, 10)
        except ValueError:
            sys.stderr.write('scorer: unparsable seed: %s\n' % args.seed)
            return 2
    rng = random.Random(seed)

    rev = args.revision
    if rev is None:
        proc = subprocess.run(['git', '-C', lane, 'rev-parse', 'HEAD'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        if proc.returncode != 0:
            sys.stderr.write('scorer: cannot read HEAD of %s\n' % lane)
            return 2
        rev = proc.stdout.decode().strip()

    scratch = args.scratch
    tmp_root = None
    if scratch is None:
        tmp_root = tempfile.mkdtemp(prefix='tsukuroi-r32-handoff-')
        scratch = tmp_root
    scratch = os.path.abspath(scratch)
    os.makedirs(scratch, exist_ok=True)
    work = os.path.join(scratch, 'work')
    os.makedirs(work, exist_ok=True)

    try:
        with open(os.path.abspath(__file__), 'rb') as fh:
            scorer_sha = hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        scorer_sha = 'unavailable'

    harness_errors = 0
    routed_total = 0
    per_type = {t: 0 for t in TYPES}
    results = []

    try:
        rev_script = export_census(lane, rev, os.path.join(work, 'rev'))
        base_script = export_census(lane, BASE, os.path.join(work, 'base'))
    except Exception as exc:                       # noqa: BLE001 - reported as harness error
        summary = {
            'kind': 'summary', 'scenarios': 0, 'routed': 0, 'seed': seed_text,
            'harness_errors': 1, 'scorer_sha256': scorer_sha, 'revision': rev, 'base': BASE,
            'predicate_label': PREDICATE_LABEL, 'scenarios_per_type': per_type,
            'error': str(exc), 'runtime_s': round(time.time() - t0, 1),
        }
        sys.stdout.write(json.dumps(summary, sort_keys=True) + '\n')
        sys.stdout.flush()
        return 2

    scen = make_scenarios(rng, args.scenarios)

    for s in scen:
        if time.time() - t0 > args.budget:
            harness_errors += 1
            results.append({
                'id': s['id'], 'type': s['type'],
                'planted': {'kill_events': s['n'], 'coredumps': s['m']},
                'expected': [list(t) for t in expected_set(s)],
                'observed': [], 'plane_parity': False, 'routed': False,
                'harness_error': 'wall-clock budget exhausted',
            })
            break

        sdir = os.path.join(work, s['dirname'])
        fx = os.path.join(sdir, 'fx')
        stubdir = os.path.join(sdir, 'bin')
        home = os.path.join(sdir, 'home')
        tmpd = os.path.join(sdir, 'tmp')
        os.makedirs(stubdir, exist_ok=True)
        os.makedirs(home, exist_ok=True)
        os.makedirs(tmpd, exist_ok=True)
        s['fx'] = fx

        planted = build_fixture(fx, s, rng)

        # stub dispatcher: one script, one symlink per probe command
        calls = os.path.join(sdir, 'calls')
        dispatcher = os.path.join(stubdir, '.dispatch')
        w(dispatcher, DISPATCH.replace('__FX__', fx).replace('__LOG__', calls))
        os.chmod(dispatcher, 0o700)
        for cmd in STUB_COMMANDS:
            link = os.path.join(stubdir, cmd)
            if not os.path.exists(link):
                os.symlink('.dispatch', link)

        env = census_env(stubdir, fx, home, tmpd)

        runs = {}
        err = None
        for tag, script in (('base', base_script), ('rev', rev_script)):
            open(calls, 'w', encoding='utf-8').close()
            rc, out = run_census(script, env, args.timeout)
            try:
                with open(calls, encoding='utf-8') as fh:
                    call_log = fh.read()
            except OSError:
                call_log = ''
            planes, rollup, handoff_raw = parse_output(out)
            herm = check_hermetic(calls, out, s)
            runs[tag] = {
                'rc': rc, 'out': out, 'planes': planes, 'rollup': rollup,
                'handoff_raw': handoff_raw, 'hermetic_error': herm,
                'calls': call_log,
            }
            if herm:
                err = '%s run not hermetic: %s' % (tag, herm)
                break
            if rc not in (0, 1, 2):
                err = '%s run exited %d (not a census verdict code)' % (tag, rc)
                break
            if not rollup:
                err = '%s run printed no TSUKUROI_CENSUS line' % tag
                break

        obs = []
        other_handoff = []
        routed = False
        parity = False
        if err is None:
            base_planes = runs['base']['planes']
            if len(base_planes) != 6:
                err = 'base run printed %d PLANE lines, expected 6' % len(base_planes)
            else:
                verr = verify_planted(base_planes, s)
                if verr:
                    err = 'planted facts not visible in the base census: %s' % verr
        if err is None:
            compared, other_handoff = parse_handoff(runs['rev']['handoff_raw'])
            obs = compared
            parity = (runs['rev']['planes'] == runs['base']['planes']
                      and runs['rev']['rollup'] == runs['base']['rollup']
                      and runs['rev']['rc'] == runs['base']['rc'])
            routed = bool(observed_set(compared) == expected_set(s) and parity)

        row = {
            'id': s['id'],
            'type': s['type'],
            'planted': planted,
            'expected': [list(t) for t in expected_set(s)],
            'observed': obs,
            'observed_set': [list(t) for t in observed_set(obs)],
            'other_handoff': other_handoff,
            'plane_parity': parity,
            'routed': routed,
            'base_rc': runs.get('base', {}).get('rc'),
            'rev_rc': runs.get('rev', {}).get('rc'),
            'base_rollup': runs.get('base', {}).get('rollup', ''),
            'rev_rollup': runs.get('rev', {}).get('rollup', ''),
            'base_oom_plane': next((l for l in runs.get('base', {}).get('planes', [])
                                     if l.startswith('PLANE oom:')), ''),
            'base_journal_plane': next((l for l in runs.get('base', {}).get('planes', [])
                                        if l.startswith('PLANE journal:')), ''),
        }
        if err:
            harness_errors += 1
            row['harness_error'] = err
        if routed:
            routed_total += 1
        per_type[s['type']] = per_type.get(s['type'], 0) + 1
        results.append(row)
        sys.stdout.write(json.dumps(row, sort_keys=True) + '\n')
        sys.stdout.flush()

    summary = {
        'kind': 'summary',
        'scenarios': len(results),
        'routed': routed_total,
        'seed': seed_text,
        'harness_errors': harness_errors,
        'scorer_sha256': scorer_sha,
        'revision': rev,
        'base': BASE,
        'predicate_label': PREDICATE_LABEL,
        'scenarios_per_type': per_type,
        'unrouted': [r['id'] for r in results if not r['routed']],
        'runtime_s': round(time.time() - t0, 1),
    }
    sys.stdout.write(json.dumps(summary, sort_keys=True) + '\n')
    sys.stdout.flush()

    if tmp_root and not args.keep_scratch:
        shutil.rmtree(tmp_root, ignore_errors=True)
    elif args.keep_scratch:
        sys.stderr.write('scorer: scratch kept at %s\n' % scratch)

    if harness_errors:
        return 2
    return 0 if routed_total == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
