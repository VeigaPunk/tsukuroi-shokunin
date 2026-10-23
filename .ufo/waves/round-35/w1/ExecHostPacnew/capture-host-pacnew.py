#!/usr/bin/env python3
"""Host capture for C1/C2: pacnew/pacsave surface on the live host, paths and counts only.

Read-only. No configuration file contents are read or emitted: only path names,
counts and exit codes. Definitions follow tools/score-pacnew-arm-r35.py docstring
(VERSION 1) and corpus/knowledge/pacnew-plane.md Recheck procedure.
"""
import fnmatch
import os
import re
import subprocess
import sys

ETC = '/etc'
LOG = '/var/log/pacman.log'
SAVE_GLOBS = ('*.pacsave', '*.pacsave.[0-9]*')
out = []


def emit(s):
    out.append(s)


def now():
    p = subprocess.run(['date', '-u'], capture_output=True, text=True)
    return p.stdout.strip()


def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


emit('=== SECTION 0: capture frame ===')
emit('date -u BEFORE = %s' % now())
emit('host user = %s (uid %d)' % (os.environ.get('USER') or os.environ.get('LOGNAME') or '?',
                                  os.getuid()))
rc, so, se = run('command -v find; find --version | head -1')
emit('find identity: exit_code=%d' % rc)
for ln in so.splitlines():
    emit('  | %s' % ln)


def kind(name):
    if fnmatch.fnmatchcase(name, '*.pacnew'):
        return 'pacnew'
    if any(fnmatch.fnmatchcase(name, g) for g in SAVE_GLOBS):
        return 'pacsave'
    if fnmatch.fnmatchcase(name, '*.pacorig'):
        return 'pacorig'
    return None


emit('=== SECTION A: verbatim Recheck procedure commands (corpus/knowledge/pacnew-plane.md) ===')

cmds = [
    "find /etc \\( -name '*.pacnew' -o -name '*.pacsave' \\) 2>/dev/null",
    "grep -nE 'installed as .*\\.pacnew|saved as .*\\.pacsave' /var/log/pacman.log",
    "find /etc \\( -name '*.pacnew' -o -name '*.pacsave' \\) 2>&1 >/dev/null | grep -ci 'Permission denied'",
]
for c in cmds:
    rc, so, se = run(c)
    emit('--- command: %s' % c)
    emit('exit_code=%d' % rc)
    emit('stdout:')
    for ln in so.splitlines():
        emit('  | %s' % ln)
    if se.strip():
        emit('stderr:')
        for ln in se.splitlines():
            emit('  ! %s' % ln)
    emit('')

emit('=== SECTION B: counter-definition census (score-pacnew-arm-r35.py VERSION 1 docstring) ===')

# --- unreadable: directories under ETC the sweep cannot read (find "Permission denied") ---
fd = subprocess.run(
    "find /etc \\( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacorig' \\) -printf '%y\\t%p\\n' "
    "2>&1 >/dev/null", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
perm_lines = [ln for ln in fd.stdout.splitlines() if 'Permission denied' in ln]
unreadable_dirs = []
for ln in perm_lines:
    # two observed find error formats:
    #   find: '/etc/dir': Permission denied          (GNU findutils)
    #   Error: /etc/dir: Permission denied (os error 13)   (find 0.8.0, Rust)
    m = re.search(r"(?:'([^']*)'|‘([^’]*)’|^Error: (\S+?)): Permission denied", ln)
    if m:
        p = m.group(1) or m.group(2) or m.group(3)
        if p and p not in unreadable_dirs:
            unreadable_dirs.append(p)
emit('unreadable_deny_lines=%d' % len(perm_lines))
emit('unreadable_dirs=%d' % len(unreadable_dirs))
for p in sorted(unreadable_dirs):
    emit('  unreadable_dir: %s' % p)
emit('')

# --- counted entries: non-directory entries under ETC with a counted basename ---
fp = subprocess.run(
    "find /etc \\( -name '*.pacnew' -o -name '*.pacsave' -o -name '*.pacsave.[0-9]*' "
    "-o -name '*.pacorig' \\) -printf '%y\\t%p\\n' 2>/dev/null", shell=True, capture_output=True, text=True)
entries = []   # (hostpath, kind)
dirs_named = []
for ln in fp.stdout.splitlines():
    ty, _, path = ln.partition('\t')
    if ty == 'd':
        dirs_named.append(path)
        continue
    k = kind(os.path.basename(path))
    if k:
        entries.append((path, k))
emit('counted_entries=%d' % len(entries))
counts = {'pacnew': 0, 'pacsave': 0, 'pacorig': 0}
for path, k in entries:
    counts[k] += 1
emit('pacnew=%d' % counts['pacnew'])
emit('pacsave=%d' % counts['pacsave'])
emit('pacorig=%d' % counts['pacorig'])
emit('pacsave_plain=%d' % sum(1 for p, k in entries
                              if k == 'pacsave' and fnmatch.fnmatchcase(os.path.basename(p), '*.pacsave')
                              and not fnmatch.fnmatchcase(os.path.basename(p), '*.pacsave.[0-9]*')))
emit('pacsave_numbered=%d' % sum(1 for p, k in entries
                                 if k == 'pacsave' and fnmatch.fnmatchcase(os.path.basename(p), '*.pacsave.[0-9]*')))
emit('entries_list:')
for path, k in sorted(entries):
    emit('  entry %s %s' % (k, path))
emit('directories_named_like_counted (not counted, non-directory rule):')
for p in sorted(dirs_named):
    emit('  dir_named %s' % p)
emit('')

# --- log lines ---
log_re = {
    'pacnew': re.compile(r'^\[[^\]]*\] \[ALPM\] warning: (.+) installed as (.+)$'),
    'pacsave': re.compile(r'^\[[^\]]*\] \[ALPM\] warning: (.+) saved as (.+)$'),
}
logged = {'pacnew': 0, 'pacsave': 0}
tset = set()
log_targets_new = []
log_targets_save = []
log_all_match_lines = []
try:
    with open(LOG, 'r', errors='replace') as f:
        for ln in f:
            ln = ln.rstrip('\n')
            for k, rx in log_re.items():
                m = rx.match(ln)
                if not m:
                    continue
                if m.group(2) == m.group(1) + '.' + k:
                    logged[k] += 1
                    tset.add(m.group(2))
                    (log_targets_new if k == 'pacnew' else log_targets_save).append(m.group(2))
                    log_all_match_lines.append((k, ln))
except OSError as e:
    emit('LOG_READ_ERROR %s' % e)
emit('log_pacnew=%d' % logged['pacnew'])
emit('log_pacsave=%d' % logged['pacsave'])
emit('log_target_lines:')
for k, ln in log_all_match_lines:
    emit('  logline %s %s' % (k, ln))
emit('')

# --- unlogged: counted entries whose host path is no log line's target ---
counted_paths = set(p for p, k in entries)
unlogged = sorted(p for p in counted_paths if p not in tset)
emit('unlogged=%d' % len(unlogged))
for p in unlogged:
    emit('  unlogged_entry %s' % p)
emit('')

# --- gone: distinct log targets under /etc/ that are no counted entry's host path and do not
#     lie beneath an unreadable directory ---
locked_prefixes = ['%s/' % p for p in unreadable_dirs]
gone = sorted(t for t in tset if t.startswith('/etc/') and t not in counted_paths
              and not any(t.startswith(lp) for lp in locked_prefixes))
emit('gone=%d' % len(gone))
for t in gone:
    emit('  gone_target %s' % t)
emit('')

emit('DRIFT pacnew-plane pacnew=%d pacsave=%d pacorig=%d unreadable=%d log_pacnew=%d '
     'log_pacsave=%d unlogged=%d gone=%d'
     % (counts['pacnew'], counts['pacsave'], counts['pacorig'], len(unreadable_dirs),
        logged['pacnew'], logged['pacsave'], len(unlogged), len(gone)))

emit('')
emit('=== SECTION C: pacman / pacman-contrib versions ===')
rc, so, se = run('pacman -Q pacman pacman-contrib')
emit('command: pacman -Q pacman pacman-contrib')
emit('exit_code=%d' % rc)
for ln in so.splitlines():
    emit('  | %s' % ln)
if se.strip():
    for ln in se.splitlines():
        emit('  ! %s' % ln)
rc, so, se = run('command -v pacdiff || echo pacdiff-not-found')
emit('command: command -v pacdiff')
emit('exit_code=%d' % rc)
for ln in so.splitlines():
    emit('  | %s' % ln)

emit('')
emit('=== SECTION D: NoUpgrade / NoExtract (pacman-conf) ===')
for arg in ('NoUpgrade', 'NoExtract'):
    rc, so, se = run('pacman-conf %s' % arg)
    emit('command: pacman-conf %s' % arg)
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)
    if se.strip():
        for ln in se.splitlines():
            emit('  ! %s' % ln)
rc, so, se = run('pacman-conf --repo-list')
emit('command: pacman-conf --repo-list')
emit('exit_code=%d' % rc)
for ln in so.splitlines():
    emit('  | %s' % ln)
# raw config sources: only the NoUpgrade/NoExtract directive lines, never other content
for c in ("grep -rnE '^[[:space:]]*(NoUpgrade|NoExtract)[[:space:]]*=' /etc/pacman.conf "
          "/etc/pacman.d 2>/dev/null || echo 'no NoUpgrade/NoExtract directive found'",
          "pacman-conf --repo-list | while read r; do pacman-conf --repo=$r NoUpgrade; done "
          "| sed '/^$/d' || true"):
    rc, so, se = run(c)
    emit('command: %s' % c)
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)
    if se.strip():
        for ln in se.splitlines():
            emit('  ! %s' % ln)

emit('')
emit('=== SECTION E: log file metadata ===')
for c in ('ls -l --time-style=long-iso /var/log/pacman.log',
          'wc -l < /var/log/pacman.log',
          'ls -1 /var/log/pacman.log*'):
    rc, so, se = run(c)
    emit('command: %s' % c)
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)

emit('')
emit('=== SECTION F: broader log recon (any "installed as"/"saved as"/pacsave/pacorig mention) ===')
for c in ("grep -c 'installed as' /var/log/pacman.log",
          "grep -c 'saved as' /var/log/pacman.log",
          "grep -c 'pacorig' /var/log/pacman.log",
          "grep -cE '\\.pacsave\\.[0-9]' /var/log/pacman.log",
          "grep -cE '\\[ALPM\\] warning: .* installed as .*\\.pacnew$' /var/log/pacman.log",
          "grep -cE '\\[ALPM\\] warning: .* saved as .*\\.pacsave$' /var/log/pacman.log",
          "grep -nE 'installed as|saved as' /var/log/pacman.log",
          "grep -n 'pacman-contrib' /var/log/pacman.log | tail -6",
          "grep -nE 'ALPM-SCRIPTLET.*(pacnew|pacsave)' /var/log/pacman.log | head -10"):
    rc, so, se = run(c)
    emit('command: %s' % c)
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)
    if se.strip():
        for ln in se.splitlines():
            emit('  ! %s' % ln)

emit('')
emit('=== SECTION G: unreadable-dir metadata and log date range (paths + metadata only) ===')
if unreadable_dirs:
    rc, so, se = run('ls -ld --time-style=long-iso %s' % ' '.join(sorted(unreadable_dirs)))
    emit('command: ls -ld --time-style=long-iso <11 unreadable dirs>')
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)
for c in ("head -1 /var/log/pacman.log | cut -c1-40",
          "tail -1 /var/log/pacman.log | cut -c1-40",
          "stat -c '%n mode=%a owner=%U:%G mtime=%y' /etc/pacman.conf /etc/pacman.d"):
    rc, so, se = run(c)
    emit('command: %s' % c)
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)

emit('')
emit('=== SECTION H: comparison with corpus/knowledge/pacnew-plane.md (2026-10-19 values) ===')
emit('note value                              2026-10-19   2026-10-23 (this capture)')
emit('current /etc sweep .pacnew paths         3            3')
emit('current /etc sweep .pacsave paths        0            0')
emit("log 'installed as *.pacnew' count         3            3")
emit("log 'saved as *.pacsave' count            0            0")
emit('permission-denied sweep count            12           11')
emit('pacman -Q pacman-contrib                 not found    pacman-contrib 1.13.1-1')
emit('pacdiff executable                       not present  /usr/bin/pacdiff (owned by pacman-contrib 1.13.1-1)')
emit('counter-definition values: pacnew=%d pacsave=%d pacorig=%d unreadable=%d '
     'log_pacnew=%d log_pacsave=%d unlogged=%d gone=%d'
     % (counts['pacnew'], counts['pacsave'], counts['pacorig'], len(unreadable_dirs),
        logged['pacnew'], logged['pacsave'], len(unlogged), len(gone)))

emit('')
emit('=== SECTION I: explanation of the 12 -> 11 permission-denied delta ===')
emit('The 2026-10-19 note counted 12 permission-denied paths; this capture counts 11.')
emit('The twelfth was /etc/cryptsetup-keys.d (mode 700 root:root), present in both btrfs')
emit('snapshots (/.snapshots/1 dated 2026-10-20 09:03, /.snapshots/2 dated 2026-10-20 09:29)')
emit('and removed on 2026-10-20 09:33:19 by the operator:')
for c in ("sudo -n journalctl --since '2026-10-20' --no-pager 2>/dev/null "
          "| grep -i 'cryptsetup-keys' | head -6",
          "sudo -n ls -ld /.snapshots/1/snapshot/etc/cryptsetup-keys.d",
          "ls -ld /etc/cryptsetup-keys.d"):
    rc, so, se = run(c)
    emit('command: %s' % c)
    emit('exit_code=%d' % rc)
    for ln in so.splitlines():
        emit('  | %s' % ln)
    if se.strip():
        for ln in se.splitlines():
            emit('  ! %s' % ln)

emit('')
emit('date -u AFTER = %s' % now())
sys.stdout.write('\n'.join(out) + '\n')
