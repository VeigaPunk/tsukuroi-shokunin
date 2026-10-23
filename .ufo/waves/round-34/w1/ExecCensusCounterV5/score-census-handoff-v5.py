#!/usr/bin/env python3
"""Counter v5 for tsukuroi round 32, claim C1 (ADJ-04 sibling handoff routing).

Repair counter for the round-32 verifier spot-check routed defect 1: the v3 counter
(tools/score-census-handoff-r32.py, sha256 f45136c3...) was met by the post-data
shortcut K11, which read the oom plane's C1_kernel field instead of clustering dated
kill events and the journal plane's total error count minus a fixed live-host floor
instead of selecting SYSLOG_IDENTIFIER. v4 plants non-coredump error entries in every
fixture, repeats kernel OOM lines within planted minutes, and replaces the single
thinned live view with two synthetic live views that vary both counted classes.

v5 repairs tsukuroi round-33 routed defect R33-FIXTURE-LABEL-SHORTCUT (round-32
routed defect 1, still open): v4's distractors all carried the one fixed
`SYSLOG_IDENTIFIER` set and the one fixed message, and both synthetic views set
`TSUKUROI_JOURNALCTL`, so a census keyed on that override plus the fixture label
(MutR1CounterV4) routed 24 of 24 fixture rows and both synthetic views. v5 (a) draws
each distractor's identifier and message text fresh from os.urandom per run, so no
constant string marks a planted distractor; (b) adds synthetic view C, which leaves
`TSUKUROI_JOURNALCTL` unset and feeds the census through a PATH-first `journalctl`
stub in a directory whose name is drawn fresh per run, so a census that treats the
override as a fixture tell cannot tell view C from production; (c) lets the plain
live view tolerate journal growth during a run by counting the same classes directly
with journalctl immediately before and after each run and accepting a run's value
inside that interval. Every fixture and synthetic view also draws its directory name
from os.urandom, not from the seeded plan.

This file is seat evidence; it is not the lane's tools/ counter.

Scores whether the host census `tools/tsukuroi-census.sh` at a revision routes
sibling-owned findings to mori (PROVINCE.md ADJ-04 row) by printing HANDOFF lines.

FROZEN line grammar (the census must print, after the PLANE lines and before or
after the TSUKUROI_CENSUS line):
  HANDOFF ADJ-04 mori class=kill-events value=<n> kind=dated-event state=prepared
  HANDOFF ADJ-04 mori class=coredumps  value=<m> kind=dated-event state=prepared
No HANDOFF line otherwise. A cumulative counter alone (vmstat oom_kill > 0,
memory.events oom_kill flag) is NOT a dated event and must not produce a
kill-events line.

FROZEN PREDICATE (v5, fixed and committed in a sandbox clone before this scorer
scored anything; the v4 predicate is kept except for the three repairs above; the
constant below must equal this paragraph after whitespace normalisation):

A scenario is routed when the census at REV, run against that scenario's fixture, prints exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value equal to the number of distinct planted kill-event minutes when there are any, one class=coredumps line with value equal to the number of planted coredump entries when there are any, no HANDOFF line otherwise, and none for a cumulative counter alone), and its PLANE lines, TSUKUROI_CENSUS line and exit code equal those of the base census 58cc2e0b on the same fixture; every fixture plants 1 to 9 boot-0 error entries that are neither a coredump nor a kernel entry, each with an identifier and a message drawn fresh from os.urandom so that no constant string marks them, and a fixture that plants kill events repeats the kernel OOM line of some minutes, so neither a total error count, a kernel-line count, nor a count keyed on any fixture string is the required value. The run counts only when, in addition, in a plain read-only live view of the host and in each of three synthetic live views of the host, the census at REV prints exactly the HANDOFF set implied by its own oom cluster and journal coredump counts; in the plain view each run's journal counts (err, coredump, kernel and other) and oom counts (C1_kernel, killed_process, C2_events, C3_events and clusters) lie inside the interval between the direct journalctl measurements of the same classes taken immediately before and after that run (the printed cluster-key list being exactly the measured key set when the two measurements agree and, when they differ, containing the earlier set and sitting inside the later one), and the base and REV journal lines agree after the four counts and the failed-history count are replaced by a placeholder while the oom PLANE line, TSUKUROI_CENSUS line and exit code agree exactly between base and REV; each synthetic view keeps every other plane live and answers only the oom-window and boot-0 error journal probes from a synthetic stream drawn fresh per run, views A and B reach the stream through TSUKUROI_JOURNALCTL (view A with 1 to 4 kill-event minutes in single kernel lines and 4 to 8 planted coredump entries, view B with 5 to 9 kill-event minutes whose kernel OOM lines are doubled and 1 to 3 planted coredump entries) and view C leaves TSUKUROI_JOURNALCTL unset and reaches its stream through a PATH-first journalctl stub in a directory whose name is drawn fresh per run (2 to 6 kill-event minutes in single kernel lines and 2 to 6 planted coredump entries), each synthetic view with 1 to 9 non-coredump error entries whose identifiers and messages are drawn fresh from os.urandom, so the three views differ in both counted classes and in the route to the stream, and in every synthetic view the base and REV oom and journal PLANE lines, TSUKUROI_CENSUS line and exit code agree exactly and the base's counts equal the planted ones; and the plain view's counts are not both zero.

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
  python3 score-census-handoff-v5.py --revision <REV> [--lane <repo>]
        [--scratch <dir>] [--seed <hex|int>] [--scenarios N] [--keep-scratch]
Output: one JSON line per scenario (`id`, `type`, `planted`, `expected`,
`observed`, `plane_parity`, `routed`, ...), then a summary JSON line with
`scenarios`, `routed`, `live_consistent`, `seed`, `harness_errors`, `scorer_sha256`,
`scorer_version`, `revision`, `base`, `predicate_label` and `scenarios_per_type`; a `live`
JSON line precedes the summary.
Exit 0 when routed == scenarios, live_consistent is true and there is no harness
error, 1 otherwise, 2 on harness error (including a vacuous live check: no dated
kill-event cluster and no coredump entry on the live host).
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

VERSION = 5
BASE = '58cc2e0bfaa4580d47f6817537c8d5c82dbe9c92'
DEFAULT_LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
PREDICATE_LABEL = 'routed'
# frozen v5 predicate; asserted at import against the docstring paragraph (line breaks and
# runs of spaces are not significant). The three v5 repairs are in the docstring header.
PREDICATE = (
    "A scenario is routed when the census at REV, run against that scenario's fixture, prints "
    "exactly the set of HANDOFF lines the scenario requires (one class=kill-events line with value "
    "equal to the number of distinct planted kill-event minutes when there are any, one "
    "class=coredumps line with value equal to the number of planted coredump entries when there are "
    "any, no HANDOFF line otherwise, and none for a cumulative counter alone), and its PLANE lines, "
    "TSUKUROI_CENSUS line and exit code equal those of the base census 58cc2e0b on the same fixture; "
    "every fixture plants 1 to 9 boot-0 error entries that are neither a coredump nor a kernel "
    "entry, each with an identifier and a message drawn fresh from os.urandom so that no constant "
    "string marks them, and a fixture that plants kill events repeats the kernel OOM line of some "
    "minutes, so neither a total error count, a kernel-line count, nor a count keyed on any fixture "
    "string is the required value. The run counts only when, in addition, in a plain read-only live "
    "view of the host and in each of three synthetic live views of the host, the census at REV "
    "prints exactly the HANDOFF set implied by its own oom cluster and journal coredump counts; in "
    "the plain view each run's journal counts (err, coredump, kernel and other) and oom counts "
    "(C1_kernel, killed_process, C2_events, C3_events and clusters) lie inside the interval between "
    "the direct journalctl measurements of the same classes taken immediately before and after that "
    "run (the printed cluster-key list being exactly the measured key set when the two measurements "
    "agree and, when they differ, containing the earlier set and sitting inside the later one), and "
    "the base and REV journal lines agree after the four counts and the failed-history count are "
    "replaced by a placeholder while the oom PLANE line, TSUKUROI_CENSUS line and exit code agree "
    "exactly between base and REV; each synthetic view keeps every other plane live and answers "
    "only the oom-window and boot-0 error journal probes from a synthetic stream drawn fresh per "
    "run, views A and B reach the stream through TSUKUROI_JOURNALCTL (view A with 1 to 4 kill-event "
    "minutes in single kernel lines and 4 to 8 planted coredump entries, view B with 5 to 9 "
    "kill-event minutes whose kernel OOM lines are doubled and 1 to 3 planted coredump entries) and "
    "view C leaves TSUKUROI_JOURNALCTL unset and reaches its stream through a PATH-first journalctl "
    "stub in a directory whose name is drawn fresh per run (2 to 6 kill-event minutes in single "
    "kernel lines and 2 to 6 planted coredump entries), each synthetic view with 1 to 9 "
    "non-coredump error entries whose identifiers and messages are drawn fresh from os.urandom, so "
    "the three views differ in both counted classes and in the route to the stream, and in every "
    "synthetic view the base and REV oom and journal PLANE lines, TSUKUROI_CENSUS line and exit "
    "code agree exactly and the base's counts equal the planted ones; and the plain view's counts "
    "are not both zero."
)
assert ' '.join(PREDICATE.split()) in ' '.join(__doc__.split()), (
    'the frozen predicate constant is not the docstring paragraph')

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


def distractor_entries(rng, n):
    """n boot-0 error entries that are neither coredumps nor kernel lines.

    v5: the identifier and the message text are drawn fresh from os.urandom for every
    entry, so no constant string (and no shared prefix) marks a planted distractor:
    a census that subtracts "the fixture-labelled entries" has nothing to key on. Both
    fields are lower-case hex, so they can never collide with `systemd-coredump`, with
    the `kernel` class, or with the census' failed-history tokens (which contain
    letters outside a-f). The seeded RNG is not used here on purpose.
    """
    out = []
    seen = set()
    for i in range(n):
        while True:
            sid = os.urandom(8).hex()
            if sid not in seen:
                break
        seen.add(sid)
        out.append(json.dumps({
            '__REALTIME_TIMESTAMP': str(rng.randint(1700000000, 1800000000) * 1000000 + i),
            '_BOOT_ID': 'd7f0bc8d938e4249b4a1f250cbfacf58',
            '_TRANSPORT': 'journal',
            'SYSLOG_IDENTIFIER': sid,
            'PRIORITY': '3',
            'MESSAGE': os.urandom(16).hex(),
        }, sort_keys=True, separators=(',', ':')))
    return out


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
        mult = scen['kernel_mult']
        for e in events:
            ts = '%sT%02d:%02d:%02d.%06d%s' % (e['day'], e['hh'], e['mi'], e['sec'],
                                                e['us'], e['off'])
            # v4: the kernel OOM line repeats `mult` times inside the same minute, so the
            # kernel-line count (C1_kernel, killed_process) exceeds the cluster count; the
            # clusters are minute keys, as the census' own comment says
            for _ in range(mult):
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

    # --- planted boot-0 error entries: coredumps plus distractor non-coredump entries.
    # v4: every scenario carries at least one distractor, so a coredump count that is the
    # total error count (or that total minus a fixed floor) is not the required value. ---
    lines = []
    for d in plant_coredumps(rng, m):
        lines.append(json.dumps({
            '__REALTIME_TIMESTAMP': str(d['ts'] * 1000000),
            '_BOOT_ID': 'd7f0bc8d938e4249b4a1f250cbfacf58',
            '_TRANSPORT': 'journal',
            'SYSLOG_IDENTIFIER': 'systemd-coredump',
            'PRIORITY': '3',
            'MESSAGE': ('Main process terminated with signal %d '
                        '(Segmentation fault) of user 1000' % d['signal']),
        }, sort_keys=True, separators=(',', ':')))
    for line in distractor_entries(rng, scen['distractors']):
        lines.append(line)
    rng.shuffle(lines)
    put('journal-err.json', '\n'.join(lines) + '\n')
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
        # the planted non-coredump error entries (present in every v4 scenario) are the
        # finding the lane retains; journal-err.json is already written above
        pass
    return {'kill_events': n, 'coredumps': m, 'distractors': scen['distractors'],
            'kernel_mult': scen['kernel_mult'], 'kernel_lines': n * scen['kernel_mult']}


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
    d, mult = scen['distractors'], scen['kernel_mult']
    errs = []
    # v4: the census' dated-event count is its cluster count (one per minute); the kernel
    # line count is n*mult, and the attribution and sigkill counts are n. A count that
    # reads C1_kernel (or any line count) instead of clustering is caught here.
    for key, want in (('clusters', n), ('C1_kernel', n * mult), ('killed_process', n * mult),
                      ('C2_events', n), ('C3_events', n)):
        got = plane_value(planes, 'PLANE oom:', key)
        if got is None:
            errs.append('oom plane has no %s field' % key)
        elif got != want:
            errs.append('oom plane %s=%d, planted %d' % (key, got, want))
    for key, want in (('coredump', m), ('kernel', 0), ('other', d), ('err', m + d)):
        got = plane_value(planes, 'PLANE journal:', key)
        if got is None:
            errs.append('journal plane has no %s field' % key)
        elif got != want:
            errs.append('journal plane %s=%d, planted %d' % (key, got, want))
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
            # the directory the census reads is random and drawn fresh from os.urandom:
            # it carries no type, no expected HANDOFF set and no planted count, and the
            # seeded plan cannot reproduce it
            'dirname': os.urandom(8).hex(),
            'type': t,
            'n': n,
            'm': m,
            'cumulative': cumulative,
            'cumulative_vmstat': cum_vm,
            'cumulative_cgroup': cum_cg,
            'cumulative_value': rng.randint(1, 9),
            # v4: every fixture plants non-coredump error entries in boot 0, and planted
            # kill events repeat their kernel OOM line so the line count exceeds the
            # cluster count
            'distractors': rng.randint(1, 9),
            'kernel_mult': rng.randint(1, 3),
            'tsukuroi_finding': finding,
            'host_token': 'fx%010x' % rng.getrandbits(40),
        })
    return scen


SYNTH_WRAPPER = r'''#!/usr/bin/bash
# score-census-handoff-v4 synthetic live view: answers only the oom-window and the boot-0
# error journal probes from synthetic bytes; every other query goes to the real journalctl.
args=" $* "
d='__D__'
case "$args" in
  *"--list-boots"*) exec /bin/cat "$d/listboots" ;;
  *"-o short-iso-precise"*)
    case "$args" in
      *"--grep"*"oom_reaper"*) exec /bin/cat "$d/oomwin-kernel" ;;
      *"--grep"*"OOM killer"*) exec /bin/cat "$d/oomwin-attrib" ;;
      *"--grep"*"status=9"*) exec /bin/cat "$d/oomwin-sigkill" ;;
      *) exec /bin/cat "$d/empty" ;;
    esac ;;
  *"--grep"*) exec /bin/cat "$d/empty" ;;
  *" -p err "*)
    case "$args" in
      *" -k "*) exec /bin/cat "$d/empty" ;;
      *) exec /bin/cat "$d/journal-err" ;;
    esac ;;
  *) exec /usr/bin/journalctl "$@" ;;
esac
'''


def write_synthetic_journal(dest, spec, rng):
    """Write one synthetic live view's journal bytes and return its wrapper path.

    spec = {'n': distinct kill-event minutes, 'mult': kernel OOM lines per minute,
            'm': coredump entries, 'd': non-coredump error entries}.
    `dest` is named by the caller from os.urandom; the wrapper is always `dest/journalctl`
    so the same bytes serve a TSUKUROI_JOURNALCTL override (views A and B) and a
    PATH-first lookup with the variable unset (view C).
    """
    os.makedirs(dest, exist_ok=True)

    def put(name, text, mode=None):
        path = os.path.join(dest, name)
        w(path, text)
        if mode:
            os.chmod(path, mode)

    put('listboots',
        'IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY\n'
        ' -1 73a8e2fc20cc48749b3cbd24ed5dc7c1 Sun 2026-10-11 19:02:51 -03 '
        'Tue 2026-10-13 10:57:30 -03\n'
        '  0 d7f0bc8d938e4249b4a1f250cbfacf58 Tue 2026-10-13 11:02:03 -03 '
        'Wed 2026-10-14 11:42:34 -03\n')
    kern, attrib, sigkill = [], [], []
    for e in (plant_kill_events(rng, spec['n']) if spec['n'] else []):
        ts = '%sT%02d:%02d:%02d.%06d%s' % (e['day'], e['hh'], e['mi'], e['sec'],
                                            e['us'], e['off'])
        for _ in range(spec['mult']):
            kern.append('%s fixture-host kernel: Out of memory: Killed process %d (%s)'
                        % (ts, e['pid'], e['proc']))
        attrib.append('%s fixture-host systemd[%d]: %s: The kernel OOM killer killed '
                      'some processes in this unit.' % (ts, e['pid'], e['unit']))
        sigkill.append('%s fixture-host systemd[1]: user@1000.service: Main process '
                       'exited, code=killed, status=9/KILL' % ts)
    put('oomwin-kernel', ''.join(l + '\n' for l in kern))
    put('oomwin-attrib', ''.join(l + '\n' for l in attrib))
    put('oomwin-sigkill', ''.join(l + '\n' for l in sigkill))
    lines = []
    for d in plant_coredumps(rng, spec['m']):
        lines.append(json.dumps({
            '__REALTIME_TIMESTAMP': str(d['ts'] * 1000000),
            '_BOOT_ID': 'd7f0bc8d938e4249b4a1f250cbfacf58',
            '_TRANSPORT': 'journal',
            'SYSLOG_IDENTIFIER': 'systemd-coredump',
            'PRIORITY': '3',
            'MESSAGE': ('Main process terminated with signal %d '
                        '(Segmentation fault) of user 1000' % d['signal']),
        }, sort_keys=True, separators=(',', ':')))
    lines.extend(distractor_entries(rng, spec['d']))
    rng.shuffle(lines)
    put('journal-err', ''.join(l + '\n' for l in lines))
    put('empty', '')
    put('journalctl', SYNTH_WRAPPER.replace('__D__', dest), 0o755)
    return os.path.join(dest, 'journalctl')


# ---- live views -----------------------------------------------------------
# The classes the census counts, reproduced for the direct read-only reference reads.
LIVE_CLASS_OOM = 'Out of memory|oom-kill|oom_reaper'
LIVE_CLASS_OOM_SYS = 'kernel OOM killer killed some processes'
LIVE_CLASS_SIGKILL = "status=9/KILL|Failed with result '(signal|oom-kill)'"
LIVE_OOM_FIELDS = ('C1_kernel', 'killed_process', 'C2_events', 'C3_events', 'clusters')
LIVE_JOURNAL_FIELDS = ('err', 'coredump', 'kernel', 'other')


def _capture(cmd, env, timeout):
    """Run one read-only journalctl read; rc 0 and 1 are measured (1 = no entries)."""
    try:
        proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError('timeout: %s' % ' '.join(cmd[:3]))
    if proc.returncode not in (0, 1):
        raise RuntimeError('rc=%d: %s' % (proc.returncode, ' '.join(cmd[:3])))
    return proc.stdout.decode('utf-8', 'replace')


def live_ref_counts(env, timeout):
    """Direct read-only measurement of the classes the census counts, in the plain env.

    Mirrors the census' own probes: the boot-0 error stream counted at entry level with
    the census' disjoint class order (`SYSLOG_IDENTIFIER":"systemd-coredump"`, then
    `SYSLOG_IDENTIFIER":"kernel"` or `_TRANSPORT":"kernel"`, then other), and the oom
    window scans (`-k --grep` kernel family, `--grep` systemd attribution, `--grep`
    sigkill) with clusters as sorted unique minute keys. This is the growth bracket: each
    census run must report values measured between the call before and the call after it.
    """
    err_out = _capture(['journalctl', '-b', '-p', 'err', '-o', 'json', '--no-pager'],
                       env, timeout)
    lines = [l for l in err_out.splitlines() if l]
    cd = kd = ot = 0
    for l in lines:
        if '"SYSLOG_IDENTIFIER":"systemd-coredump"' in l:
            cd += 1
        elif '"SYSLOG_IDENTIFIER":"kernel"' in l or '"_TRANSPORT":"kernel"' in l:
            kd += 1
        else:
            ot += 1
    c1_out = _capture(['journalctl', '-k', '--grep', LIVE_CLASS_OOM,
                       '-o', 'short-iso-precise', '--no-pager'], env, timeout)
    a_out = _capture(['journalctl', '--grep', LIVE_CLASS_OOM_SYS,
                      '-o', 'short-iso-precise', '--no-pager'], env, timeout)
    s_out = _capture(['journalctl', '--grep', LIVE_CLASS_SIGKILL,
                      '-o', 'short-iso-precise', '--no-pager'], env, timeout)
    c1 = [l for l in c1_out.splitlines() if l and not l.startswith('-- Boot')]
    a_n = len([l for l in a_out.splitlines() if l and not l.startswith('-- Boot')])
    s_n = len([l for l in s_out.splitlines() if l and not l.startswith('-- Boot')])
    keys = set()
    for l in (a_out + '\n' + s_out).splitlines():
        if l.startswith('-- Boot'):
            continue
        m = re.match(r'^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})', l)
        if m:
            keys.add('%s %s' % (m.group(1), m.group(2)))
    return {
        'err': len(lines), 'coredump': cd, 'kernel': kd, 'other': ot,
        'C1_kernel': len(c1),
        'killed_process': len([l for l in c1 if 'Killed process' in l]),
        'C2_events': a_n, 'C3_events': s_n,
        'clusters': len(keys), 'cluster_keys': sorted(keys),
    }


JOURNAL_MUTABLE = (
    (re.compile(r'\berr=\d+'), 'err=#'),
    (re.compile(r'\bcoredump=\d+'), 'coredump=#'),
    (re.compile(r'\bkernel=\d+'), 'kernel=#'),
    (re.compile(r'\bother=\d+'), 'other=#'),
    # the failed-history count and its unit names move with the live coredump storm (a new
    # crash creates a new failed systemd-coredump@ unit); normalised, never counted here
    (re.compile(r'\bfailedhist=\d+(?:\[[^\]]*\])?'), 'failedhist=#'),
)


def normalise_journal_line(line):
    for pat, repl in JOURNAL_MUTABLE:
        line = pat.sub(repl, line)
    return line


def journal_fields(planes):
    out = {}
    for key in LIVE_JOURNAL_FIELDS:
        v = plane_value(planes, 'PLANE journal:', key)
        if v is not None:
            out[key] = v
    return out


def oom_fields(planes):
    out = {}
    for key in LIVE_OOM_FIELDS:
        v = plane_value(planes, 'PLANE oom:', key)
        if v is not None:
            out[key] = v
    return out


def cluster_keys_of(planes):
    line = next((l for l in planes if l.startswith('PLANE oom:')), '')
    m = re.search(r'clusters=\d+\[([^\]]*)\]', line)
    if not m:
        return []
    return sorted(k.strip() for k in m.group(1).split(',') if k.strip())


def expected_from_run(run):
    """The HANDOFF set a run's own printed counts imply."""
    want = []
    if (run['oom_fields'].get('clusters') or 0) >= 1:
        want.append(('kill-events', run['oom_fields']['clusters'], 'dated-event', 'prepared'))
    if (run['journal_fields'].get('coredump') or 0) >= 1:
        want.append(('coredumps', run['journal_fields']['coredump'], 'dated-event', 'prepared'))
    return sorted(want)


def bracket_problems(tag, run, ref):
    """The run's counted fields must lie inside the before/after direct measurement."""
    errs = []
    before, after = ref['before'], ref['after']
    jf, of = run['journal_fields'], run['oom_fields']
    for key in LIVE_JOURNAL_FIELDS:
        if key not in jf:
            errs.append('%s journal line lacks %s' % (tag, key))
            continue
        lo, hi = sorted((before[key], after[key]))
        if not lo <= jf[key] <= hi:
            errs.append('%s journal %s=%d outside measured [%d,%d]'
                        % (tag, key, jf[key], lo, hi))
    if len(jf) == 4 and jf['err'] != jf['coredump'] + jf['kernel'] + jf['other']:
        errs.append('%s journal classes do not partition err' % tag)
    for key in LIVE_OOM_FIELDS:
        if key not in of:
            errs.append('%s oom line lacks %s' % (tag, key))
            continue
        lo, hi = sorted((before[key], after[key]))
        if not lo <= of[key] <= hi:
            errs.append('%s oom %s=%d outside measured [%d,%d]'
                        % (tag, key, of[key], lo, hi))
    keys = set(run['cluster_keys'])
    bk, ak = set(before['cluster_keys']), set(after['cluster_keys'])
    if bk == ak:
        if keys != bk:
            errs.append('%s oom cluster keys differ from the measured set (%d vs %d)'
                        % (tag, len(keys), len(bk)))
    elif not (bk <= keys <= ak):
        errs.append('%s oom cluster keys are not between the two measured sets' % tag)
    return errs


def live_view_plain(rev_script, base_script, env, timeout):
    """v5 (c) plain live view: tolerance for journal growth during the run.

    For each of base and REV: read the counted classes directly (journalctl), run the
    census, read them again. The run's journal and oom counts must lie in the interval
    between the two reads, and its HANDOFF set must be the one its own counts imply. For
    parity, the four journal counts and the failed-history field are replaced by a
    placeholder; the oom line, rollup and exit code must agree exactly between base and
    REV. One retry when the view disagrees (the journal can grow between the two runs).
    """
    res = {}
    for attempt in (1, 2):
        runs, refs = {}, {}
        harness = None
        for tag, script in (('base', base_script), ('rev', rev_script)):
            try:
                before = live_ref_counts(env, timeout)
                rc, out = run_census(script, env, timeout)
                after = live_ref_counts(env, timeout)
            except Exception as exc:            # noqa: BLE001 - reported as harness error
                harness = '%s run: %s' % (tag, exc)
                break
            planes, rollup, raw = parse_output(out)
            compared, other = parse_handoff(raw)
            run = {
                'rc': rc, 'planes': planes, 'rollup': rollup, 'handoff_raw': raw,
                'journal_fields': journal_fields(planes),
                'oom_fields': oom_fields(planes),
                'cluster_keys': cluster_keys_of(planes),
                'other_handoff': other,
                'observed_set': observed_set(compared),
                'clusters': plane_value(planes, 'PLANE oom:', 'clusters'),
                'coredumps': plane_value(planes, 'PLANE journal:', 'coredump'),
            }
            run['expected'] = expected_from_run(run)
            run['handoff_ok'] = run['observed_set'] == run['expected']
            runs[tag] = run
            refs[tag] = {'before': before, 'after': after}
        if harness:
            res = {'attempt': attempt, 'harness_error': harness}
            break
        b, r = runs['base'], runs['rev']
        problems = []
        if len(b['planes']) != 6 or not b['rollup']:
            problems.append('base live run lacks six PLANE lines or a rollup')
        if len(r['planes']) != 6 or not r['rollup']:
            problems.append('rev live run lacks six PLANE lines or a rollup')
        for tag, run in (('base', b), ('rev', r)):
            problems.extend(bracket_problems(tag, run, refs[tag]))
        # the handoff is the surface under test: REV must print exactly the set its own
        # counts imply. The base census is the frozen pre-C1 reference (58cc2e0b) and
        # prints no HANDOFF line at all, so it is never required to.
        if not r['handoff_ok']:
            problems.append('rev HANDOFF set is not the one its own counts imply: %s'
                            % (r['observed_set'],))
        parity = bool(
            normalise_journal_line(
                next((l for l in r['planes'] if l.startswith('PLANE journal:')), ''))
            == normalise_journal_line(
                next((l for l in b['planes'] if l.startswith('PLANE journal:')), ''))
            and next((l for l in r['planes'] if l.startswith('PLANE oom:')), '')
            == next((l for l in b['planes'] if l.startswith('PLANE oom:')), '')
            and r['rollup'] == b['rollup'] and r['rc'] == b['rc'])
        res = {'attempt': attempt, 'base': b, 'rev': r, 'refs': refs,
               'parity': parity, 'bracket_errors': problems}
        res['consistent'] = bool(parity and not problems)
        if res['consistent']:
            break
    return res


def live_view_synthetic(rev_script, base_script, env, timeout):
    """A deterministic synthetic live view: exact parity and exact counts.

    Run base then REV under one synthetic stream (one retry on disagreement), require the
    same oom and journal PLANE lines, rollup and exit code, and require REV's HANDOFF set
    to be the one the base census's measured counts in this view imply. The other four
    PLANE notes carry live counters and are not compared live (they are compared in full
    on every fixture scenario).
    """
    res = {}
    for attempt in (1, 2):
        runs = {}
        for tag, script in (('base', base_script), ('rev', rev_script)):
            rc, out = run_census(script, env, timeout)
            planes, rollup, raw = parse_output(out)
            runs[tag] = {
                'rc': rc, 'planes': planes, 'rollup': rollup, 'handoff_raw': raw,
                'clusters': plane_value(planes, 'PLANE oom:', 'clusters'),
                'coredumps': plane_value(planes, 'PLANE journal:', 'coredump'),
            }
        b, r = runs['base'], runs['rev']
        keep = ('PLANE oom:', 'PLANE journal:')
        lp = lambda run: [l for l in run['planes'] if l.startswith(keep)]
        parity = (lp(r) == lp(b) and r['rollup'] == b['rollup'] and r['rc'] == b['rc'])
        res = {'attempt': attempt, 'base': b, 'rev': r, 'parity': bool(parity)}
        if parity:
            break
    b, r = res['base'], res['rev']
    if len(b['planes']) != 6 or not b['rollup'] or b['clusters'] is None or b['coredumps'] is None:
        res['harness_error'] = 'base live run lacks six PLANE lines, a rollup or the counts'
        return res
    compared, other = parse_handoff(r['handoff_raw'])
    want = []
    if (b['clusters'] or 0) >= 1:
        want.append(('kill-events', b['clusters'], 'dated-event', 'prepared'))
    if (b['coredumps'] or 0) >= 1:
        want.append(('coredumps', b['coredumps'], 'dated-event', 'prepared'))
    res.update({'expected': sorted(want), 'observed_set': observed_set(compared),
                'other_handoff': other})
    res['consistent'] = bool(res['parity'] and observed_set(compared) == sorted(want))
    return res


def live_check(rev_script, base_script, timeout, work, rng):
    """v5 live conjunct: one plain host view and three synthetic live views.

    plain:  no TSUKUROI_* override at all; growth-tolerant (each run's counts are
            bracketed by direct journalctl reads taken before and after it).
    synth A: the host's own planes; the oom-window and boot-0 error journal probes are
             answered from a synthetic stream selected through TSUKUROI_JOURNALCTL, with
             1..4 kill-event minutes (one kernel OOM line each), 4..8 coredump entries
             and 1..9 non-coredump error entries.
    synth B: the same through TSUKUROI_JOURNALCTL, with 5..9 kill-event minutes (kernel
             OOM line doubled), 1..3 coredump entries and 1..9 non-coredump entries.
    synth C: TSUKUROI_JOURNALCTL is UNSET and the stream is reached through a PATH-first
             `journalctl` stub in a directory whose name is drawn fresh from os.urandom,
             with 2..6 kill-event minutes (one kernel OOM line each), 2..6 coredump
             entries and 1..9 non-coredump entries. A census that treats the override
             being set as a fixture tell cannot tell this view from production.
    Every synthetic view's distractor identifiers and messages are drawn fresh from
    os.urandom. Both counted classes differ across the three views, so a constant matches
    at most one of them; view B's kernel-line count exceeds its cluster count, so a
    counter reading C1_kernel instead of clustering is wrong there; and the planted
    non-coredump entries make a coredump count that is the total error count (or that
    total minus a label, a fixed floor or any other fixture-keyed offset) wrong in every
    view. In each synthetic view REV's oom and journal PLANE lines, rollup line and exit
    code equal the base census's in the same view, the base's counts equal the planted
    ones, and REV prints exactly the implied HANDOFF set. consistent = every view
    consistent. A plain view with no cluster and no coredump entry is a harness error
    (vacuous).
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith('TSUKUROI_')}
    plain = live_view_plain(rev_script, base_script, env, timeout)
    res = {'plain': plain}
    if plain.get('harness_error'):
        res['harness_error'] = 'plain: ' + plain['harness_error']
        return res
    if plain['base']['clusters'] == 0 and plain['base']['coredumps'] == 0:
        res['harness_error'] = 'live check vacuous: no dated kill-event cluster and no coredump entry'
        return res
    specs = {
        'A': {'n': rng.randint(1, 4), 'mult': 1, 'm': rng.randint(4, 8),
              'd': rng.randint(1, 9)},
        'B': {'n': rng.randint(5, 9), 'mult': 2, 'm': rng.randint(1, 3),
              'd': rng.randint(1, 9)},
        'C': {'n': rng.randint(2, 6), 'mult': 1, 'm': rng.randint(2, 6),
              'd': rng.randint(1, 9)},
    }
    consistent = bool(plain['consistent'])
    synth = {}
    res['synthetic'] = synth
    for name, spec in specs.items():
        # the directory name is fresh from os.urandom, so no constant path marks a view
        dest = os.path.join(work, 'synth-%s-%s' % (name, os.urandom(8).hex()))
        wrapper = write_synthetic_journal(dest, spec, rng)
        if name == 'C':
            view_env = dict(env)
            view_env['PATH'] = dest + ':' + env.get('PATH', '/usr/bin:/bin')
            assert 'TSUKUROI_JOURNALCTL' not in view_env
            route = 'path-first journalctl stub, TSUKUROI_JOURNALCTL unset'
        else:
            view_env = dict(env, TSUKUROI_JOURNALCTL=wrapper)
            route = 'TSUKUROI_JOURNALCTL override'
        view = live_view_synthetic(rev_script, base_script, view_env, timeout)
        view['planted'] = spec
        view['route'] = route
        view['dir'] = dest
        synth[name] = view
        if view.get('harness_error'):
            res['harness_error'] = 'synthetic %s: %s' % (name, view['harness_error'])
            return res
        if (view['base']['clusters'] != spec['n']
                or view['base']['coredumps'] != spec['m']):
            res['harness_error'] = (
                'synthetic %s: base census clusters=%s coredumps=%s, planted %d/%d'
                % (name, view['base']['clusters'], view['base']['coredumps'],
                   spec['n'], spec['m']))
            return res
        consistent = consistent and bool(view['consistent'])
    res['consistent'] = consistent
    return res


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

    # live-host consistency (v2, pre-data amendment after wave-1 CritPredicateC1): a census
    # that routes only when it detects the scorer's fixture must also route on the live host
    live = live_check(rev_script, base_script, args.timeout, work, random.Random(seed ^ 0x5EED))
    if live.get('harness_error'):
        harness_errors += 1
    sys.stdout.write(json.dumps(dict(live, kind='live'), sort_keys=True) + '\n')
    sys.stdout.flush()

    summary = {
        'kind': 'summary',
        'scenarios': len(results),
        'routed': routed_total,
        'live_consistent': bool(live.get('consistent')),
        'seed': seed_text,
        'harness_errors': harness_errors,
        'scorer_sha256': scorer_sha,
        'scorer_version': VERSION,
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
    return 0 if (routed_total == len(results) and live.get('consistent')) else 1


if __name__ == '__main__':
    sys.exit(main())
