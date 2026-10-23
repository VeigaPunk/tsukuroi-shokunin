#!/usr/bin/env python3
"""score-pacnew-arm-r35b.py — counter VERSION 2 for round-35 C1 (coverage), the redesign of
`score-pacnew-arm-r35.py` VERSION 1 after wave-1 control K08FixtureKeyed met VERSION 1 (24 of 24
with a shortcut keyed on name lengths). VERSION 1 stays committed with its receipts and is not
the claim's counter.

Question: does the census at a named revision report the pacnew/pacsave drift surface
(PROVINCE.md Core, "`.pacnew` / `.pacsave` drift": pair pacman-log history with current
readable filesystem findings; report skipped unreadable paths) with the values an independent
oracle computes, in views the census cannot tell apart from production use?

Frozen predicate (label `matches`; the same sentence is the constant PREDICATE, asserted below,
and every receipt's `predicate_label`):
A view matches when the census at the named revision exits 0, 1 or 2 within 180 s, prints exactly one line that begins `DRIFT pacnew-plane ` whose fields pacnew, pacsave, pacorig, unreadable, log_pacnew, log_pacsave, unlogged and gone each appear once as name=integer and all equal the oracle's values for that view, leaves the view's etc tree and log unchanged (bytes, modes and inode change times), and, in a stub view, prints every other line except the first exactly as the claim-base census does on the same view with the same exit code; the views are 20 stub views (TSUKUROI_ETC_DIR and TSUKUROI_PACMAN_LOG set, every probe seam stubbed), 3 namespace views (no TSUKUROI_ variable set; a fresh fixture bind-mounted over /etc and /var/log/pacman.log in an unprivileged user and mount namespace, capabilities dropped) and 1 live view (no TSUKUROI_ variable set; the real host, read-only).

Measure (QUALITY 73): the battery. The same run scores the candidate, the control arm (a
correct arm inserted into the claim-base census, which must match every view) and the
should-fail arms (BATTERY below, each inserted the same way, each skipping or bending part of
the work; each must miss at least one view). The last line carries `candidate_matches`, `of`,
`control_matches`, `should_fail`, `should_fail_accepted` and `harness_errors`. Exit 0 only when
the candidate and the control match every view, no should-fail arm matches every view, and
harness_errors is empty; 1 otherwise; 2 on a harness error. `--skip-battery` scores the
candidate alone (control-wave mode; not the measure).

Oracle (sources: pacman 7.1.0 libalpm add.c / remove.c log formats; pacman-contrib 1.13.1
pacdiff find expression — rows S191-S195 registered this round). For a tree ETC whose host name
is /etc:
  pacnew      non-directory entries (lstat; symlinks never followed) named `*.pacnew`
  pacsave     non-directory entries named `*.pacsave` or `*.pacsave.[0-9]*` (fnmatch)
  pacorig     non-directory entries named `*.pacorig`
              (all three only where the sweep can read)
  unreadable  directories under ETC whose listing fails with a permission error
  log_pacnew  log lines `[<anything>] [ALPM] warning: <F> installed as <F>.pacnew`, F under /etc/
  log_pacsave log lines `[<anything>] [ALPM] warning: <F> saved as <F>.pacsave`, F under /etc/
  unlogged    counted entries whose host path is no counted log line's target
  gone        distinct targets of counted log lines that are no counted entry's host path and
              do not lie beneath an unreadable directory
Named limits: a census that inspects its own namespace (uid_map, mountinfo) can tell the
namespace view from production; paths containing a newline are not generated.

Usage: python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <rev> [--skip-battery]
Output: JSON lines — header, one row per (census, view), summary.
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

VERSION = 2
LABEL = 'matches'
CLAIM_BASE = 'b40c01df38eb26f74c095c471efc6d1649b00fd4'
FIELDS = ('pacnew', 'pacsave', 'pacorig', 'unreadable', 'log_pacnew', 'log_pacsave',
          'unlogged', 'gone')
PREDICATE = ("A view matches when the census at the named revision exits 0, 1 or 2 within 180 s, "
             "prints exactly one line that begins `DRIFT pacnew-plane ` whose fields pacnew, "
             "pacsave, pacorig, unreadable, log_pacnew, log_pacsave, unlogged and gone each appear "
             "once as name=integer and all equal the oracle's values for that view, leaves the "
             "view's etc tree and log unchanged (bytes, modes and inode change times), and, in a "
             "stub view, prints every other line except the first exactly as the claim-base census "
             "does on the same view with the same exit code; the views are 20 stub views "
             "(TSUKUROI_ETC_DIR and TSUKUROI_PACMAN_LOG set, every probe seam stubbed), 3 namespace "
             "views (no TSUKUROI_ variable set; a fresh fixture bind-mounted over /etc and "
             "/var/log/pacman.log in an unprivileged user and mount namespace, capabilities "
             "dropped) and 1 live view (no TSUKUROI_ variable set; the real host, read-only).")
N_STUB, N_NS = 20, 3
assert PREDICATE in ' '.join(__doc__.split()), 'PREDICATE must equal the docstring sentence'
assert __doc__.count('VERSION 2') == 1
CMD_SEAMS = ('TSUKUROI_PACMAN', 'TSUKUROI_PACMAN_CONF', 'TSUKUROI_SYSTEMCTL', 'TSUKUROI_DMESG',
             'TSUKUROI_JOURNALCTL', 'TSUKUROI_NVIDIA_SMI', 'TSUKUROI_LSMOD', 'TSUKUROI_EXPAC',
             'TSUKUROI_VERCMP')
FILE_SEAMS = ('TSUKUROI_PACMAN_CONF_FILE', 'TSUKUROI_HOSTNAME_FILE',
              'TSUKUROI_DMESG_RESTRICT_FILE', 'TSUKUROI_PRESSURE_FILE', 'TSUKUROI_MEMINFO_FILE',
              'TSUKUROI_VMSTAT_FILE', 'TSUKUROI_OFFLINE_DB')
DIR_SEAMS = ('TSUKUROI_PACMAN_DB', 'TSUKUROI_ROOT_DIR', 'TSUKUROI_PCI_SYSFS', 'TSUKUROI_DEV_DIR',
             'TSUKUROI_CGROUP_ROOT', 'TSUKUROI_BOOT_TARGET')
SAVE_GLOBS = ('*.pacsave', '*.pacsave.[0-9]*')
BASE_ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C'}
GIT_ENV = dict(BASE_ENV, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
MARKER = '  local roll=HEALTHY\n'
LIVE_ETC, LIVE_LOG = '/etc', '/var/log/pacman.log'

# ---- the control arm (correct) and the should-fail arms (each bends one part of the work) ----
CONTROL_ARM = r'''
r35_arm() {
  local etc=${TSUKUROI_ETC_DIR:-/etc} log=${PACMAN_LOG:-/var/log/pacman.log} t
  t=$(mktemp -d)
  find "$etc" ! -type d \( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacsave.[0-9]*' -o -name '*.pacorig' \) -print 2>"$t/err" >"$t/fs" || true
  local unr pn po ps lpn lps unl gone=0 tg l under
  unr=$(grep -c 'Permission denied' "$t/err" || true)
  pn=$(grep -c '\.pacnew$' "$t/fs" || true)
  po=$(grep -c '\.pacorig$' "$t/fs" || true)
  ps=$(( $(wc -l < "$t/fs") - pn - po ))
  { grep -E '^\[[^]]*\] \[ALPM\] warning: (/etc/.+) installed as \1\.pacnew$' "$log" 2>/dev/null || true; } | sed -E 's/^.* installed as //' > "$t/ln"
  { grep -E '^\[[^]]*\] \[ALPM\] warning: (/etc/.+) saved as \1\.pacsave$' "$log" 2>/dev/null || true; } | sed -E 's/^.* saved as //' > "$t/ls"
  lpn=$(wc -l < "$t/ln"); lps=$(wc -l < "$t/ls")
  while IFS= read -r l; do printf '/etc/%s\n' "${l#"$etc"/}"; done < "$t/fs" | sort -u > "$t/host"
  cat "$t/ln" "$t/ls" | sort -u > "$t/tg"
  unl=$(while IFS= read -r l; do printf '/etc/%s\n' "${l#"$etc"/}"; done < "$t/fs" | sort | comm -23 - "$t/tg" | wc -l)
  sed -nE "s#^find: '$etc/(.*)': Permission denied#/etc/\1/#p" "$t/err" > "$t/lk"
  while IFS= read -r tg; do
    grep -qxF -- "$tg" "$t/host" && continue
    under=0; while IFS= read -r l; do case "$tg" in "$l"*) under=1 ;; esac; done < "$t/lk"
    [ "$under" -eq 1 ] || gone=$((gone+1))
  done < "$t/tg"
  rm -rf "$t"
  printf 'DRIFT pacnew-plane pacnew=%s pacsave=%s pacorig=%s unreadable=%s log_pacnew=%s log_pacsave=%s unlogged=%s gone=%s\n' "$pn" "$ps" "$po" "$unr" "$lpn" "$lps" "$unl" "$gone"
}
'''


def sub(old, new, count=1):
    def f(arm, live):
        assert arm.count(old) >= count, old
        return arm.replace(old, new)
    return f


def cached_live(arm, live):
    const = ('  [ -n "${TSUKUROI_ETC_DIR:-}" ] || { printf \'DRIFT pacnew-plane %s\\n\'; return 0; }\n'
             % ' '.join('%s=%d' % (k, live[k]) for k in FIELDS))
    return arm.replace('  local etc=', const + '  local etc=', 1)


BATTERY = {
    'F01-fixture-gated': sub('  local etc=', '  [ -n "${TSUKUROI_ETC_DIR:-}" ] || return 0\n  local etc='),
    'F02-cached-live': cached_live,
    'F03-log-tail-64': sub('"$log" 2>/dev/null', '<(tail -n 64 "$log") 2>/dev/null', 2),
    'F04-basename-pair': sub(r"(/etc/.+) installed as \1\.pacnew$", r"(/etc/.*/)?([^/]+) installed as /etc/.*/?\2\.pacnew$"),
    'F05-gone-by-existence': sub('    grep -qxF -- "$tg" "$t/host" && continue',
                                 '    [ -e "$etc/${tg#/etc/}" ] && continue'),
    'F06-decimal-only-saves': sub("-o -name '*.pacsave.[0-9]*'", "-o -regex '.*\\.pacsave\\.[0-9]+'"),
    'F07-dangling-symlinks-only': sub('find "$etc" ! -type d', 'find "$etc" \\( -type f -o -xtype l \\)'),
    'F08-files-and-links-only': sub('find "$etc" ! -type d', 'find "$etc" \\( -type f -o -type l \\)'),
    'F09-word-split-paths': sub('while IFS= read -r l; do printf \'/etc/%s\\n\' "${l#"$etc"/}"; done < "$t/fs" | sort -u > "$t/host"',
                                'for l in $(cat "$t/fs"); do printf \'/etc/%s\\n\' "${l#"$etc"/}"; done | sort -u > "$t/host"'),
    'F10-dated-2026-only': sub(r"'^\[[^]]*\] \[ALPM\]", r"'^\[2026-[^]]*\] \[ALPM\]", 2),
    'F11-basename-join': sub('grep -qxF -- "$tg" "$t/host" && continue',
                             'grep -q -- "/${tg##*/}$" "$t/host" && continue'),
    'F12-global-log-counts': sub("warning: (/etc/.+) ", "warning: (/.+) ", 2),
    'F13-arm-only-exit': sub("\"$pn\" \"$ps\" \"$po\" \"$unr\" \"$lpn\" \"$lps\" \"$unl\" \"$gone\"\n",
                             "\"$pn\" \"$ps\" \"$po\" \"$unr\" \"$lpn\" \"$lps\" \"$unl\" \"$gone\"\n  exit 0\n"),
    'F14-chmod-restore': sub('  t=$(mktemp -d)\n',
                             '  t=$(mktemp -d)\n  find "$etc" -type d ! -readable -printf \'%m %p\\n\' 2>/dev/null > "$t/modes" || true\n  while read -r m d; do chmod u+rx "$d"; chmod "$m" "$d"; done < "$t/modes"\n'),
    'F15-all-zero': lambda arm, live: arm.replace('  local etc=', '  printf \'DRIFT pacnew-plane pacnew=0 pacsave=0 pacorig=0 unreadable=0 log_pacnew=0 log_pacsave=0 unlogged=0 gone=0\\n\'; return 0\n  local etc=', 1),
    'F16-no-pairing': sub('"$lpn" "$lps" "$unl" "$gone"', '"$lpn" "$lps" 0 0'),
    'F17-unpaired-regex': sub(r"(/etc/.+) installed as \1\.pacnew$", r"(/etc/.+) installed as /etc/.*\.pacnew$"),
}


def kind(name):
    if fnmatch.fnmatchcase(name, '*.pacnew'):
        return 'pacnew'
    if any(fnmatch.fnmatchcase(name, g) for g in SAVE_GLOBS):
        return 'pacsave'
    if fnmatch.fnmatchcase(name, '*.pacorig'):
        return 'pacorig'
    return None


def rname(rng):
    """Every name component, whatever its role, is drawn the same way (K08: no role in a name)."""
    s = ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789-_') for _ in range(rng.randint(3, 10)))
    if rng.random() < 0.15:
        k = rng.randint(1, len(s) - 1)
        s = s[:k] + ' ' + s[k:]
    return s


def stamp(rng):
    y, mo, d, h, mi, se = (rng.randint(2015, 2026), rng.randint(1, 12), rng.randint(1, 28),
                           rng.randint(0, 23), rng.randint(0, 59), rng.randint(0, 59))
    return rng.choice(['[%04d-%02d-%02d %02d:%02d]' % (y, mo, d, h, mi),
                       '[%04d-%02d-%02dT%02d:%02d:%02d-0300]' % (y, mo, d, h, mi, se),
                       '[%04d-%02d-%02dT%02d:%02d:%02d+0000]' % (y, mo, d, h, mi, se),
                       '[%04d-%02d-%02dT%02d:%02d:%02dZ]' % (y, mo, d, h, mi, se)])


def oracle_of(etc, lines):
    """Compute the eight values from the bytes on disk and the log lines (never from a census)."""
    counted, locked = {}, []

    def walk(d):
        try:
            it = list(os.scandir(d))
        except PermissionError:
            locked.append(d)
            return
        for e in it:
            st = os.lstat(e.path)
            if stat.S_ISDIR(st.st_mode):
                walk(e.path)
            else:
                k = kind(e.name)
                if k:
                    counted['/etc/' + os.path.relpath(e.path, etc)] = k
    walk(etc)
    rx = {'pacnew': re.compile(r'^\[[^\]]*\] \[ALPM\] warning: (.+) installed as (.+)$'),
          'pacsave': re.compile(r'^\[[^\]]*\] \[ALPM\] warning: (.+) saved as (.+)$')}
    logged, tset = {'pacnew': 0, 'pacsave': 0}, set()
    for ln in lines:
        for k, r in rx.items():
            m = r.match(ln)
            if m and m.group(1).startswith('/etc/') and m.group(2) == m.group(1) + '.' + k:
                logged[k] += 1
                tset.add(m.group(2))
    locked_host = ['/etc/' + os.path.relpath(d, etc) + '/' for d in locked]
    return {
        'pacnew': sum(1 for k in counted.values() if k == 'pacnew'),
        'pacsave': sum(1 for k in counted.values() if k == 'pacsave'),
        'pacorig': sum(1 for k in counted.values() if k == 'pacorig'),
        'unreadable': len(locked),
        'log_pacnew': logged['pacnew'],
        'log_pacsave': logged['pacsave'],
        'unlogged': sum(1 for p in counted if p not in tset),
        'gone': sum(1 for t in tset if t not in counted and not any(t.startswith(h) for h in locked_host)),
    }


def build_fixture(rng, root):
    etc = os.path.join(root, 'etc')
    os.makedirs(etc)
    dirs = ['']
    for _ in range(rng.randint(3, 7)):
        d = os.path.join(rng.choice(dirs), rname(rng))
        os.makedirs(os.path.join(etc, d), exist_ok=True)
        dirs.append(d)
    made = []  # (rel, kind) of counted names written
    lines = []

    def path(rel):
        return os.path.join(etc, rel)

    def write(rel):
        if not os.path.lexists(path(rel)):
            with open(path(rel), 'w') as f:
                f.write(rname(rng) + '\n')

    def ev(host_file, k, src=None):
        src = src or host_file
        verb = 'installed as' if k == 'pacnew' else 'saved as'
        lines.append('%s [ALPM] warning: %s %s %s.%s' % (stamp(rng), src, verb, host_file, k))

    suffixes = ['.pacnew'] * 3 + ['.pacsave'] * 2 + ['.pacsave.%d' % rng.randint(1, 12), '.pacorig']
    for _ in range(rng.randint(4, 12)):
        rel = os.path.join(rng.choice(dirs), rname(rng) + rng.choice(['', '.conf', '.json']) + rng.choice(suffixes))
        write(rel)
        made.append(rel)
    # forced shapes in every fixture (wave-1 CritClaimDesign (d)-(l), K12, K13)
    target = os.path.join(rng.choice(dirs), rname(rng))
    write(target)
    os.symlink(target and os.path.join(etc, target), path(os.path.join(rng.choice(dirs), rname(rng) + '.pacnew')))
    os.symlink(etc, path(os.path.join(rng.choice(dirs), rname(rng) + '.pacsave')))
    os.symlink('/nonexistent/' + rname(rng), path(os.path.join(rng.choice(dirs), rname(rng) + '.pacorig')))
    os.mkfifo(path(os.path.join(rng.choice(dirs), rname(rng) + '.pacnew')))
    write(os.path.join(rng.choice(dirs), rname(rng) + '.pacsave.%d%s' % (rng.randint(0, 9), rname(rng).replace(' ', ''))))
    collide = rname(rng) + '.conf'
    d1, d2 = rng.sample(dirs, 2)
    write(os.path.join(d1, collide + '.pacnew'))
    write(os.path.join(d2, collide + '.pacnew'))
    ev('/etc/' + os.path.join(d1, collide), 'pacnew')
    d3 = rng.choice([d for d in dirs if d not in (d1, d2)])
    ev('/etc/' + os.path.join(d3, collide), 'pacnew')  # gone, but its basename is present elsewhere
    dname = os.path.join(rng.choice(dirs), rname(rng))
    os.makedirs(path(dname + '.pacnew'))
    ev('/etc/' + dname, 'pacnew')  # a log target that is a directory: gone, not present
    for _ in range(rng.randint(2, 6)):  # distractor names
        write(os.path.join(rng.choice(dirs), rname(rng) + rng.choice(
            ['.pacnew.bak', '.pacnewer', '.pacsave~', '.pacsaveX', '.conf', '-pacnew', '.pacorig.old',
             '.pacsave.x1', '.pacsave.', 'pacnew'])))
    for _ in range(rng.randint(0, 2)):
        os.makedirs(path(os.path.join(rng.choice(dirs), rname(rng) + rng.choice(['.pacnew', '.pacsave', '.pacorig']))), exist_ok=True)
    locked = []
    for _ in range(rng.randint(1, 3)):
        d = os.path.join(rng.choice(dirs), rname(rng))
        os.makedirs(path(d), exist_ok=True)
        write(os.path.join(d, rname(rng) + '.pacnew'))
        if rng.random() < 0.6:
            ev('/etc/' + os.path.join(d, rname(rng)), 'pacnew')
        locked.append(d)
    for rel in made:
        for k in ('pacnew', 'pacsave'):
            if rel.endswith('.' + k) and rng.random() < 0.6:
                ev('/etc/' + rel[:-len(k) - 1], k)
                if rng.random() < 0.2:
                    ev('/etc/' + rel[:-len(k) - 1], k)
    for _ in range(rng.randint(1, 3)):
        ev('/etc/' + os.path.join(rng.choice(dirs), rname(rng)), rng.choice(['pacnew', 'pacsave']))
    a, b = rng.sample(dirs, 2)
    base = rname(rng)
    ev('/etc/' + os.path.join(b, base), 'pacnew', src='/etc/' + os.path.join(a, base))  # dir mismatch
    ev('/usr/share/' + rname(rng), 'pacnew')  # non-/etc event: not counted
    early = []
    ev('/etc/' + os.path.join(rng.choice(dirs), rname(rng)), rng.choice(['pacnew', 'pacsave']))
    early.append(lines.pop())
    for _ in range(rng.randint(3, 8)):
        lines.append(rng.choice([
            '%s [ALPM] installed as%s (1.0-1)' % (stamp(rng), rname(rng)),
            '%s [ALPM-SCRIPTLET] /etc/%s installed as /etc/%s.pacnew' % ((stamp(rng),) + (rname(rng),) * 2),
            '%s [ALPM] warning: /etc/%s.conf installed as /etc/%s.conf.pacnew.tmp' % ((stamp(rng),) + (rname(rng),) * 2),
            '%s [ALPM] warning: /etc/a%s saved as /etc/b%s.pacsave' % ((stamp(rng),) + (rname(rng),) * 2),
        ]))
    rng.shuffle(lines)
    filler = ['%s [ALPM] upgraded %s (1.%d-1 -> 1.%d-1)' % (stamp(rng), rname(rng).replace(' ', ''), i, i + 1)
              for i in range(rng.randint(80, 400))]
    lines = early + lines + filler  # one counted event sits far from the end of a long log
    log = os.path.join(root, 'pacman.log')
    with open(log, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    for d in locked:
        os.chmod(path(d), rng.choice([0o000, 0o300, 0o100]))
    return etc, log, locked, oracle_of(etc, lines)


def ctimes(etc, log):
    out = {'.log': os.lstat(log).st_ctime_ns}

    def walk(d):
        out[d] = os.lstat(d).st_ctime_ns
        try:
            it = list(os.scandir(d))
        except PermissionError:
            return
        for e in it:
            out[e.path] = os.lstat(e.path).st_ctime_ns
            if e.is_dir(follow_symlinks=False):
                walk(e.path)
    walk(etc)
    return out


def snapshot(etc, log, locked):
    h = hashlib.sha256()
    full = [os.path.join(etc, d) for d in locked]
    modes = {d: stat.S_IMODE(os.lstat(d).st_mode) for d in full}
    h.update(json.dumps(modes, sort_keys=True).encode())
    for d in full:
        os.chmod(d, 0o700)
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
        for d in full:
            os.chmod(d, modes[d])
    return h.hexdigest()


def harness(work):
    os.makedirs(work)
    stub = os.path.join(work, 'stub')
    with open(stub, 'w') as f:
        f.write('#!/bin/sh\nexit 0\n')
    os.chmod(stub, 0o755)
    env = dict(BASE_ENV, HOME=os.path.join(work, 'home'), TMPDIR=os.path.join(work, 'tmp'))
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
    return (None, 'missing ' + ','.join(missing)) if missing else (vals, None)


def others(stdout):
    return [ln for ln in stdout.splitlines()[1:] if not ln.startswith('DRIFT pacnew-plane ')]


def run(cmd, env, cwd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, errors='replace', env=env, cwd=cwd,
                           timeout=180)
        return p.returncode, p.stdout, False
    except subprocess.TimeoutExpired:
        return None, '', True


def ns_cmd(cpath, etc, log):
    inner = ('mount --bind "$1" /etc && mount --bind "$2" /var/log/pacman.log && '
             'exec setpriv --bounding-set=-all --inh-caps=-all env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C bash "$3"')
    return ['unshare', '-Urm', 'sh', '-c', inner, 'ns', etc, log, cpath]


def judge(out, rc, timed, expected, unchanged, base=None):
    vals, why = parse(out)
    if not why and vals != expected:
        why = 'field mismatch'
    if not unchanged:
        why = 'fixture mutated'
    if base is not None and not why and (others(out) != others(base[1]) or rc != base[0]):
        why = 'base parity'
    if timed or rc not in (0, 1, 2):
        why = 'exit=%s timed_out=%s' % (rc, timed)
    return why is None, why, vals


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--lane', required=True)
    ap.add_argument('--revision', required=True)
    ap.add_argument('--skip-battery', action='store_true')
    a = ap.parse_args()
    seed = int.from_bytes(os.urandom(8), 'big')
    me = open(os.path.abspath(__file__), 'rb').read()
    errors = []
    if os.geteuid() == 0:
        errors.append('running as root: unreadable fixtures would be readable')

    def show(rev):
        r = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', rev + '^{commit}'],
                           capture_output=True, text=True, env=GIT_ENV)
        if r.returncode:
            return None, None
        c = subprocess.run(['git', '-C', a.lane, 'show', r.stdout.strip() + ':tools/tsukuroi-census.sh'],
                           capture_output=True, env=GIT_ENV)
        return r.stdout.strip(), (c.stdout.decode() if c.returncode == 0 else None)
    rev, cand = show(a.revision)
    _, base = show(CLAIM_BASE)
    if cand is None or base is None:
        errors.append('cannot read tools/tsukuroi-census.sh at %s or the claim base' % a.revision)
    if base is not None and base.count(MARKER) != 1:
        errors.append('claim-base census lacks the insertion marker')
    print(json.dumps({'counter': 'score-pacnew-arm-r35b', 'version': VERSION, 'label': LABEL,
                      'predicate_label': PREDICATE, 'counter_sha256': hashlib.sha256(me).hexdigest(),
                      'seed': seed, 'revision': rev or a.revision, 'claim_base': CLAIM_BASE,
                      'census_sha256': hashlib.sha256(cand.encode()).hexdigest() if cand else None,
                      'battery': not a.skip_battery}, sort_keys=True), flush=True)
    if errors:
        print(json.dumps({'summary': 1, 'harness_errors': errors, 'exit_code': 2}))
        sys.exit(2)
    rng = random.Random(seed)
    top = tempfile.mkdtemp(prefix='r35b-')
    results = {}
    try:
        live_lines = open(LIVE_LOG, errors='replace').read().splitlines()
        live_expected = oracle_of(LIVE_ETC, live_lines)
        censuses = {'candidate': cand}
        if not a.skip_battery:
            ins = lambda arm: base.replace(MARKER, arm + '  r35_arm\n' + MARKER, 1)
            censuses['control'] = ins(CONTROL_ARM)
            for name, f in BATTERY.items():
                censuses[name] = ins(f(CONTROL_ARM, live_expected))
        paths = {}
        for name, text in list(censuses.items()) + [('claim-base', base)]:
            p = os.path.join(top, 'census-%s.sh' % name)
            with open(p, 'w') as f:
                f.write(text)
            paths[name] = p
        views = []
        for i in range(N_STUB + N_NS):
            fx = os.path.join(top, 'v%02d' % i)
            etc, log, locked, expected = build_fixture(rng, fx)
            views.append(('stub' if i < N_STUB else 'ns', fx, etc, log, locked, expected))
        for vi, (vkind, fx, etc, log, locked, expected) in enumerate(views):
            env = None
            if vkind == 'stub':
                env = harness(os.path.join(fx, 'h'))
                env.update(TSUKUROI_ETC_DIR=etc, TSUKUROI_PACMAN_LOG=log)
                bout = run(['bash', paths['claim-base']], env, fx)
                base_run = (bout[0], bout[1])
            for name in censuses:
                before, pre = snapshot(etc, log, locked), ctimes(etc, log)
                if vkind == 'stub':
                    rc, out, timed = run(['bash', paths[name]], env, fx)
                else:
                    rc, out, timed = run(ns_cmd(paths[name], etc, log), dict(BASE_ENV), fx)
                unchanged = ctimes(etc, log) == pre and snapshot(etc, log, locked) == before
                ok, why, vals = judge(out, rc, timed, expected, unchanged,
                                      base_run if vkind == 'stub' else None)
                results.setdefault(name, []).append(ok)
                print(json.dumps({'census': name, 'view': '%s-%02d' % (vkind, vi), LABEL: ok,
                                  'exit': rc, 'reason': why, 'expected': expected, 'reported': vals},
                                 sort_keys=True), flush=True)
        for name in censuses:  # live view last: the real host, read-only
            if name not in ('candidate', 'control') and not all(results[name]):
                results[name].append(False)  # already refused; the live run cannot change that
                print(json.dumps({'census': name, 'view': 'live', LABEL: False, 'exit': None,
                                  'reason': 'not run: refused in an earlier view'}, sort_keys=True))
                continue
            rc, out, timed = run(['bash', paths[name]], dict(BASE_ENV), top)
            again = oracle_of(LIVE_ETC, open(LIVE_LOG, errors='replace').read().splitlines())
            ok, why, vals = judge(out, rc, timed, live_expected, again == live_expected)
            if again != live_expected:
                errors.append('live host changed during the run')
            results[name].append(ok)
            print(json.dumps({'census': name, 'view': 'live', LABEL: ok, 'exit': rc, 'reason': why,
                              'expected': live_expected, 'reported': vals}, sort_keys=True), flush=True)
    except Exception as e:
        errors.append('harness: %r' % e)
    finally:
        subprocess.run(['chmod', '-R', 'u+rwx', top], capture_output=True)
        shutil.rmtree(top, ignore_errors=True)
    of = N_STUB + N_NS + 1
    m = {k: sum(v) for k, v in results.items()}
    accepted = [k for k in BATTERY if m.get(k) == of]
    summary = {'summary': 1, 'candidate_matches': m.get('candidate', 0), 'of': of,
               'harness_errors': errors}
    if not a.skip_battery:
        summary.update({'control_matches': m.get('control', 0), 'should_fail': len(BATTERY),
                        'should_fail_accepted': len(accepted), 'accepted': accepted,
                        'should_fail_matches': {k: m.get(k, 0) for k in BATTERY}})
    ok = m.get('candidate') == of and (a.skip_battery or (m.get('control') == of and not accepted))
    summary['exit_code'] = 2 if errors else (0 if ok else 1)
    print(json.dumps(summary, sort_keys=True))
    sys.exit(summary['exit_code'])


if __name__ == '__main__':
    main()
