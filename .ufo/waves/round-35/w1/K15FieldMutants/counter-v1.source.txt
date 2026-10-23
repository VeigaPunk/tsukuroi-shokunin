#!/usr/bin/env python3
"""score-pacnew-arm-r35.py — counter for round-35 C1 (coverage): does the census at a named
revision report the pacnew/pacsave drift surface (PROVINCE.md Core, "`.pacnew` / `.pacsave`
drift": "Pair pacman-log history with current readable filesystem findings; report skipped
unreadable paths") with the values an independent oracle computes on fresh fixtures?

VERSION 1. The fixtures are generated from a fresh random seed on every run (recorded in the
receipt); the expected values live only in this process and are never written to disk, so a
census can learn them only by reading the fixture tree and log. The census bytes are read
from `git -C LANE show REVISION:tools/tsukuroi-census.sh` (committed bytes, never the working
copy) and run with every probe command pointed at an empty-output stub and every host path
seam pointed at an empty harness directory outside the fixture.

Oracle (sources: pacman 7.1.0 libalpm add.c / remove.c log formats; pacman-contrib 1.13.1
pacdiff find expression — rows registered in corpus/SOURCES.md this round):
  pacnew      non-directory entries under ETC whose basename matches `*.pacnew`
  pacsave     non-directory entries matching `*.pacsave` or `*.pacsave.[0-9]*`
  pacorig     non-directory entries matching `*.pacorig`
              (all three only where the sweep can read; symlinks are entries, never followed)
  unreadable  directories under ETC the sweep cannot read (find's "Permission denied")
  log_pacnew  log lines `[<stamp>] [ALPM] warning: <F> installed as <F>.pacnew`
  log_pacsave log lines `[<stamp>] [ALPM] warning: <F> saved as <F>.pacsave`
  unlogged    counted entries whose host path (`/etc/` + path relative to ETC) is no log
              line's target (`<F>.pacnew` / `<F>.pacsave`)
  gone        distinct log targets under `/etc/` that are no counted entry's host path and
              do not lie beneath an unreadable directory

Usage: python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <rev> [--fixtures 24]
       [--seed <int>]
Output: JSON lines — header, one row per fixture, summary. Exit 0 when every fixture
matches and harness_errors is empty; 1 when any fixture does not match; 2 on a harness error.
"""
import argparse
import fnmatch
import hashlib
import json
import os
import random
import re
import shutil
import stat
import subprocess
import sys
import tempfile

VERSION = 1
LABEL = 'matches'
FIELDS = ('pacnew', 'pacsave', 'pacorig', 'unreadable', 'log_pacnew', 'log_pacsave',
          'unlogged', 'gone')
PREDICATE = ("A fixture matches when the census at the named revision, run with "
             "TSUKUROI_ETC_DIR set to the fixture's etc tree and TSUKUROI_PACMAN_LOG to its log, "
             "exits 0, 1 or 2 within 120 s, prints exactly one line that begins "
             "`DRIFT pacnew-plane ` whose fields pacnew, pacsave, pacorig, unreadable, "
             "log_pacnew, log_pacsave, unlogged and gone each appear once as name=integer and "
             "all equal the oracle's values for that fixture, and leaves the fixture's etc tree "
             "and log unchanged (bytes, modes and inode change times).")
CMD_SEAMS = ('TSUKUROI_PACMAN', 'TSUKUROI_PACMAN_CONF', 'TSUKUROI_SYSTEMCTL', 'TSUKUROI_DMESG',
             'TSUKUROI_JOURNALCTL', 'TSUKUROI_NVIDIA_SMI', 'TSUKUROI_LSMOD', 'TSUKUROI_EXPAC',
             'TSUKUROI_VERCMP')
FILE_SEAMS = ('TSUKUROI_PACMAN_CONF_FILE', 'TSUKUROI_HOSTNAME_FILE',
              'TSUKUROI_DMESG_RESTRICT_FILE', 'TSUKUROI_PRESSURE_FILE', 'TSUKUROI_MEMINFO_FILE',
              'TSUKUROI_VMSTAT_FILE', 'TSUKUROI_OFFLINE_DB')
DIR_SEAMS = ('TSUKUROI_PACMAN_DB', 'TSUKUROI_ROOT_DIR', 'TSUKUROI_PCI_SYSFS', 'TSUKUROI_DEV_DIR',
             'TSUKUROI_CGROUP_ROOT', 'TSUKUROI_BOOT_TARGET')
SAVE_GLOBS = ('*.pacsave', '*.pacsave.[0-9]*')
BASE_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1',
            'GIT_CONFIG_GLOBAL': os.devnull}
assert __doc__.count('VERSION 1') == 1


def kind(name):
    if fnmatch.fnmatchcase(name, '*.pacnew'):
        return 'pacnew'
    if any(fnmatch.fnmatchcase(name, g) for g in SAVE_GLOBS):
        return 'pacsave'
    if fnmatch.fnmatchcase(name, '*.pacorig'):
        return 'pacorig'
    return None


def rname(rng, n=6):
    return ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(n))


def build_fixture(rng, root):
    """Build one fixture under root/etc and root/pacman.log; return the oracle values."""
    etc = os.path.join(root, 'etc')
    os.makedirs(etc)
    dirs = ['']
    for _ in range(rng.randint(2, 6)):
        parent = rng.choice(dirs)
        d = os.path.join(parent, rname(rng))
        os.makedirs(os.path.join(etc, d), exist_ok=True)
        dirs.append(d)
    entries = []  # (relpath, kind)

    def put(rel, symlink=False):
        p = os.path.join(etc, rel)
        if symlink:
            os.symlink('/nonexistent-' + rname(rng), p)
        else:
            with open(p, 'w') as f:
                f.write('x\n')
        k = kind(os.path.basename(rel))
        if k:
            entries.append((rel, k))

    plan = [('pacnew', rng.randint(1, 6)), ('pacsave', rng.randint(0, 3)),
            ('pacsave.N', rng.randint(0, 2)), ('pacorig', rng.randint(0, 2))]
    for k, n in plan:
        for _ in range(n):
            base = os.path.join(rng.choice(dirs), rname(rng) + rng.choice(['.conf', '', '.json']))
            suffix = {'pacnew': '.pacnew', 'pacsave': '.pacsave',
                      'pacsave.N': '.pacsave.%d' % rng.randint(0, 12), 'pacorig': '.pacorig'}[k]
            put(base + suffix, symlink=(rng.random() < 0.15))
    # distractors: names that are not counted, and directories with counted-looking names
    for _ in range(rng.randint(2, 6)):
        base = os.path.join(rng.choice(dirs), rname(rng))
        put(base + rng.choice(['.pacnew.bak', '.pacnewer', '.pacsave~', '.pacsaveX', '.conf',
                               '-pacnew', '.pacorig.old', '.pacsave.x1']))
    for _ in range(rng.randint(0, 2)):
        os.makedirs(os.path.join(etc, rng.choice(dirs), rname(rng) + rng.choice(
            ['.pacnew', '.pacsave', '.pacorig'])))
    # unreadable directories, each holding a counted-looking file the sweep cannot see
    locked = []
    for _ in range(rng.randint(0, 3)):
        d = os.path.join(rng.choice(dirs), rname(rng, 7))
        os.makedirs(os.path.join(etc, d))
        with open(os.path.join(etc, d, rname(rng) + '.pacnew'), 'w') as f:
            f.write('x\n')
        locked.append(d)
    # log: events for some counted entries, events whose target is gone or locked, distractors
    lines = []
    targets = []

    def stamp():
        return '[2026-%02d-%02dT%02d:%02d:%02d-0300]' % (rng.randint(1, 9), rng.randint(1, 28),
                                                         rng.randint(0, 23), rng.randint(0, 59),
                                                         rng.randint(0, 59))

    def ev(hostfile, k):
        if k == 'pacnew':
            lines.append('%s [ALPM] warning: %s installed as %s.pacnew' % (stamp(), hostfile, hostfile))
            targets.append(hostfile + '.pacnew')
        else:
            lines.append('%s [ALPM] warning: %s saved as %s.pacsave' % (stamp(), hostfile, hostfile))
            targets.append(hostfile + '.pacsave')

    for rel, k in entries:
        if k in ('pacnew', 'pacsave') and rel.endswith('.' + k) and rng.random() < 0.6:
            ev('/etc/' + rel[:-len('.' + k)], k)
            if rng.random() < 0.2:
                ev('/etc/' + rel[:-len('.' + k)], k)  # the same file logged on two upgrades
    for _ in range(rng.randint(1, 3)):
        ev('/etc/' + os.path.join(rng.choice(dirs), rname(rng, 7)), rng.choice(['pacnew', 'pacsave']))
    for d in locked:
        if rng.random() < 0.5:
            ev('/etc/' + os.path.join(d, rname(rng, 7)), 'pacnew')
    if not any(t.endswith('.pacnew') for t in targets):
        ev('/etc/' + os.path.join(rng.choice(dirs), rname(rng, 7)), 'pacnew')
    for _ in range(rng.randint(3, 8)):
        lines.append(rng.choice([
            '%s [ALPM] installed as%s (1.0-1)' % (stamp(), rname(rng)),
            '%s [ALPM] upgraded %s (1.0-1 -> 1.1-1)' % (stamp(), rname(rng)),
            '%s [ALPM-SCRIPTLET] note: /etc/%s installed as /etc/%s.pacnew' % (stamp(), rname(rng), rname(rng)),
            '%s [PACMAN] Running \'pacman -Syu\'' % stamp(),
            '%s [ALPM] warning: /usr/share/%s installed as /usr/share/%s.pacnew' % ((stamp(),) + (rname(rng),) * 2),
            '%s [ALPM] warning: /etc/%s.conf installed as /etc/%s.conf.pacnew.tmp' % ((stamp(),) + (rname(rng),) * 2),
            '%s [ALPM] warning: /etc/a%s saved as /etc/b%s.pacsave' % ((stamp(),) + (rname(rng),) * 2),
        ]))
    rng.shuffle(lines)
    log = os.path.join(root, 'pacman.log')
    with open(log, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    for d in locked:
        os.chmod(os.path.join(etc, d), rng.choice([0o000, 0o300]))
    # oracle, computed from the build plan and the bytes written (never from a census)
    counted = {}
    for rel, k in entries:
        counted['/etc/' + rel] = k
    log_re = {'pacnew': re.compile(r'^\[[^\]]*\] \[ALPM\] warning: (.+) installed as (.+)$'),
              'pacsave': re.compile(r'^\[[^\]]*\] \[ALPM\] warning: (.+) saved as (.+)$')}
    logged = {'pacnew': 0, 'pacsave': 0}
    tset = set()
    for ln in lines:
        for k, rx in log_re.items():
            m = rx.match(ln)
            if m and m.group(2) == m.group(1) + '.' + k:
                logged[k] += 1
                tset.add(m.group(2))
    locked_host = ['/etc/' + d + '/' for d in locked]
    oracle = {
        'pacnew': sum(1 for k in counted.values() if k == 'pacnew'),
        'pacsave': sum(1 for k in counted.values() if k == 'pacsave'),
        'pacorig': sum(1 for k in counted.values() if k == 'pacorig'),
        'unreadable': len(locked),
        'log_pacnew': logged['pacnew'],
        'log_pacsave': logged['pacsave'],
        'unlogged': sum(1 for p in counted if p not in tset),
        'gone': sum(1 for t in tset if t.startswith('/etc/') and t not in counted
                    and not any(t.startswith(lh) for lh in locked_host)),
    }
    return etc, log, locked, oracle


def ctimes(etc, log):
    """Inode change times of every entry the user can lstat without changing a mode: a census
    that chmods, renames or rewrites anything and then restores it still moves a ctime."""
    out = {'.log': os.lstat(log).st_ctime_ns, '.': os.lstat(etc).st_ctime_ns}
    for dp, dn, fn in os.walk(etc):
        for n in dn + fn:
            p = os.path.join(dp, n)
            out[os.path.relpath(p, etc)] = os.lstat(p).st_ctime_ns
    return out


def snapshot(etc, log, locked):
    h = hashlib.sha256()
    modes = {d: stat.S_IMODE(os.lstat(os.path.join(etc, d)).st_mode) for d in locked}
    h.update(json.dumps(modes, sort_keys=True).encode())
    for d in locked:
        os.chmod(os.path.join(etc, d), 0o700)
    try:
        for dp, dn, fn in os.walk(etc):
            dn.sort()
            for n in sorted(dn + fn):
                p = os.path.join(dp, n)
                st = os.lstat(p)
                h.update(('%s %o\n' % (os.path.relpath(p, etc), st.st_mode)).encode())
                if stat.S_ISLNK(st.st_mode):
                    h.update(os.readlink(p).encode())
                elif stat.S_ISREG(st.st_mode):
                    with open(p, 'rb') as f:
                        h.update(f.read())
        with open(log, 'rb') as f:
            h.update(f.read())
    finally:
        for d in locked:
            os.chmod(os.path.join(etc, d), modes[d])
    return h.hexdigest()


def harness(work):
    stub = os.path.join(work, 'stub')
    with open(stub, 'w') as f:
        f.write('#!/bin/sh\nexit 0\n')
    os.chmod(stub, 0o755)
    env = dict(BASE_ENV)
    env['HOME'] = os.path.join(work, 'home')
    env['TMPDIR'] = os.path.join(work, 'tmp')
    os.makedirs(env['HOME'])
    os.makedirs(env['TMPDIR'])
    for s in CMD_SEAMS:
        env[s] = stub
    for s in FILE_SEAMS:
        p = os.path.join(work, 'f-' + s.lower())
        open(p, 'w').close()
        env[s] = p
    for s in DIR_SEAMS:
        p = os.path.join(work, 'd-' + s.lower())
        os.makedirs(p)
        os.chmod(p, 0o755)
        env[s] = p
    env['TSUKUROI_FOREIGN_BASELINE'] = ''
    env['TSUKUROI_OOM_BASELINE'] = ''
    return env


def parse(stdout):
    rows = [ln for ln in stdout.splitlines() if ln.startswith('DRIFT pacnew-plane ')]
    if len(rows) != 1:
        return None, 'drift_lines=%d' % len(rows)
    vals = {}
    for tok in rows[0].split()[2:]:
        name, sep, val = tok.partition('=')
        if sep and name in FIELDS:
            if name in vals:
                return None, 'duplicate field %s' % name
            if not re.fullmatch(r'[0-9]+', val):
                return None, 'non-integer %s=%s' % (name, val)
            vals[name] = int(val)
    missing = [f for f in FIELDS if f not in vals]
    if missing:
        return None, 'missing ' + ','.join(missing)
    return vals, None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--lane', required=True)
    ap.add_argument('--revision', required=True)
    ap.add_argument('--fixtures', type=int, default=24)
    ap.add_argument('--seed', type=int)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), 'big')
    me = open(os.path.abspath(__file__), 'rb').read()
    header = {'counter': 'score-pacnew-arm-r35', 'version': VERSION, 'label': LABEL,
              'predicate_label': PREDICATE, 'counter_sha256': hashlib.sha256(me).hexdigest(),
              'seed': seed, 'fixtures': a.fixtures}
    errors = []
    if os.geteuid() == 0:
        errors.append('running as root: unreadable fixtures would be readable')
    rv = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', a.revision + '^{commit}'],
                        capture_output=True, text=True, env=BASE_ENV)
    rev = rv.stdout.strip()
    census = subprocess.run(['git', '-C', a.lane, 'show', rev + ':tools/tsukuroi-census.sh'],
                            capture_output=True, env=BASE_ENV) if rv.returncode == 0 else None
    if rv.returncode != 0 or census.returncode != 0:
        errors.append('cannot read tools/tsukuroi-census.sh at %s' % a.revision)
    header.update({'revision': rev or a.revision,
                   'census_sha256': hashlib.sha256(census.stdout).hexdigest() if census and census.returncode == 0 else None})
    print(json.dumps(header, sort_keys=True))
    matches = 0
    rng = random.Random(seed)
    if not errors:
        top = tempfile.mkdtemp(prefix='pacnew-r35-')
        try:
            cpath = os.path.join(top, 'census.sh')
            with open(cpath, 'wb') as f:
                f.write(census.stdout)
            for i in range(a.fixtures):
                fx = tempfile.mkdtemp(prefix='fx-', dir=top)
                work = tempfile.mkdtemp(prefix='h-', dir=top)
                row = {'fixture': i}
                try:
                    etc, log, locked, oracle = build_fixture(rng, fx)
                    before = snapshot(etc, log, locked)
                    pre = ctimes(etc, log)
                    env = harness(work)
                    env['TSUKUROI_ETC_DIR'] = etc
                    env['TSUKUROI_PACMAN_LOG'] = log
                    try:
                        p = subprocess.run(['bash', cpath], capture_output=True, text=True,
                                           errors='replace', env=env, cwd=work, timeout=120)
                        rc, out, timed = p.returncode, p.stdout, False
                    except subprocess.TimeoutExpired:
                        rc, out, timed = None, '', True
                    post = ctimes(etc, log)
                    after = snapshot(etc, log, locked)
                    before, after = (before, pre), (after, post)
                    vals, why = parse(out)
                    ok = (not timed and rc in (0, 1, 2) and vals == oracle and before == after)
                    if not why and vals != oracle:
                        why = 'field mismatch'
                    if before != after:
                        why = 'fixture mutated'
                    if timed or rc not in (0, 1, 2):
                        why = 'exit=%s timed_out=%s' % (rc, timed)
                    row.update({LABEL: ok, 'exit': rc, 'reason': None if ok else why,
                                'expected': oracle, 'reported': vals})
                    matches += ok
                except Exception as e:  # a fixture that cannot be built is a harness error
                    errors.append('fixture %d: %r' % (i, e))
                    row.update({LABEL: False, 'reason': 'harness error'})
                print(json.dumps(row, sort_keys=True))
        finally:
            for dp, dn, fn in os.walk(top):
                for n in dn:
                    try:
                        os.chmod(os.path.join(dp, n), 0o700)
                    except OSError:
                        pass
            subprocess.run(['chmod', '-R', 'u+rwx', top], capture_output=True)
            shutil.rmtree(top, ignore_errors=True)
    code = 2 if errors else (0 if matches == a.fixtures else 1)
    print(json.dumps({'summary': 1, LABEL: matches, 'of': a.fixtures, 'harness_errors': errors,
                      'exit_code': code}, sort_keys=True))
    sys.exit(code)


if __name__ == '__main__':
    main()
