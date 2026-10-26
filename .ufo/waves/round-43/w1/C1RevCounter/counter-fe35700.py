#!/usr/bin/env python3
"""Round-43 C1 counter (frozen before data): boot_inputs_newer in tools/boot-chain-audit.sh under pipefail.

Defect scored (round-42 routed R42-C1-COUNTER-AMEND item 5, `w1/C1SweepSites.md`): the script runs under
`set -uo pipefail`; `find <8 start points> -newermt @btime -print -quit 2>/dev/null | grep -q .` exits 1
whenever find exits 1 (a missing start point, an unreadable directory), even when find listed a newer
input and grep matched. boot_inputs_newer then prints 0 ("no input newer than boot start"), and the
audit's BOOTED-OBSERVED gate (`newer = 0`) is passed while a boot-chain input IS newer: a fail-open.

What the counter runs. The revision's `tools/boot-chain-audit.sh` minus its final `main "$@"` line is
sourced by `bash -c` and its production `boot_inputs_newer` is called (BOOTCHAIN_FIXTURE unset), in
three legs:
  N legs (cases): inside a private user+mount namespace (`unshare -m`, the caller's uid mapped to 0 and
    the caller's /etc/subuid range mapped from 1) tmpfs is mounted over /etc, /usr/lib/initcpio and
    /usr/lib/modules and filled from data read on stdin (QUALITY 85); the scored code then runs after
    `setpriv --reuid=<caller uid> --regid=<caller gid> --clear-groups` with the caller's environment
    minus TSUKUROI_*, BOOTCHAIN_*, UFO_* and TMPDIR (QUALITY 90: production identity). Per run, random:
    which start point carries the newer entry, entry names and depths, file modes (0600/0644), mtime
    offsets around the real /proc/stat btime. 16 cases: for each of the six /etc start points k,
    "k missing, another input listed after k in find's argument order newer" (expect 1; find stops at
    the first match, so only a match after the missing start point exercises the masking) and "k
    missing, all inputs older" (expect 0); "all
    present, one newer" (1); "all present, all older" (0); "2-4 /etc start points missing, a file three
    directories deep under /usr/lib/modules newer" (1); "all present, an unreadable directory (mode 0700,
    not the caller's) under /etc/mkinitcpio.conf.d, a file under /usr/lib/modules newer" (1: find's error
    status from the unreadable directory must not mask the later match either).
  L leg (live_agree): the same call on the live host, no namespace, at the caller's identity; expected
    value from an independent Python walk of the eight real start points (lstat, mtime > btime, missing
    start points and unreadable directories skipped), taken before and after the call (one retry if the
    two walks disagree).
  S leg (selftest): `bash <script> --selftest` with TMPDIR in scratch must print
    `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=<n> failed=0`, and the script text must hold at least two
    `st_check 'R43-C1-` cases.

Channels (QUALITY 90). Closed by the legs: override environment (none set), process identity (uid/gid
equal to the caller's, no supplementary groups), fixture values (drawn per run; the start-point names are
production's own). Open, reported: the namespace's own traces — /proc/self/mountinfo shows tmpfs on /etc,
/usr/lib/initcpio and /usr/lib/modules, /proc/self/uid_map shows the mapping, and the script is read from
/mnt/bca-lib.sh. The frozen control battery scores a mount-table-gated variant and records that it PASSes.

Predicate (same sentence in the declaration and the receipt label):
  PASS iff cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1
  and selftest_r43 >= 2.

Usage: python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR> [--lane <repo>]
--scratch is required; everything the counter writes lives under it and is removed on exit, SIGINT and
SIGTERM. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read/harness error.
"""
import argparse
import json
import os
import random
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile

SCRIPT = 'tools/boot-chain-audit.sh'
ETC = [('/etc/fstab', 'f'), ('/etc/crypttab', 'f'), ('/etc/mkinitcpio.conf', 'f'),
       ('/etc/mkinitcpio.conf.d', 'd'), ('/etc/default/limine', 'f'), ('/etc/limine-snapper-sync.conf', 'f')]
USR = [('/usr/lib/initcpio', 'd'), ('/usr/lib/modules', 'd')]
POINTS = ETC + USR
PREDICATE = ('cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 '
             'and selftest_r43 >= 2')
DROP = ('TSUKUROI_', 'BOOTCHAIN_', 'UFO_')

INNER = r'''
import json, os, shutil, stat, subprocess, sys
spec = json.load(sys.stdin)
def sh(*a):
    subprocess.run(list(a), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'r43lib', '/mnt')
with open('/mnt/bca-lib.sh', 'w') as f:
    f.write(spec['lib'])
os.chmod('/mnt/bca-lib.sh', 0o644)
os.mkdir('/mnt/home'); os.chmod('/mnt/home', 0o1777)
for d in ('/usr/lib/initcpio', '/usr/lib/modules', '/etc'):
    sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'r43view', d)
roots = ['/etc', '/usr/lib/initcpio', '/usr/lib/modules']
env = spec['env']
pre = ['setpriv', '--reuid=%d' % spec['uid'], '--regid=%d' % spec['gid'], '--clear-groups']
out = {'cases': []}
p = subprocess.run(pre + ['bash', '-c', 'id -u; id -g; id -G'], env=env, capture_output=True, text=True, timeout=30)
out['identity'] = p.stdout.split()
for case in spec['cases']:
    for r in roots:
        for n in os.listdir(r):
            q = os.path.join(r, n)
            if os.path.isdir(q) and not os.path.islink(q):
                shutil.rmtree(q)
            else:
                os.unlink(q)
    for e in case['entries']:
        if e['kind'] == 'd':
            os.makedirs(e['path'], exist_ok=True)
            os.chmod(e['path'], e.get('mode', 0o755))
        else:
            os.makedirs(os.path.dirname(e['path']), exist_ok=True)
            with open(e['path'], 'w') as f:
                f.write(e['content'])
            os.chmod(e['path'], e['mode'])
    for e in sorted(case['entries'], key=lambda e: -e['path'].count('/')):
        os.utime(e['path'], (e['mtime'], e['mtime']), follow_symlinks=False)
    for r in ('/usr/lib/initcpio', '/usr/lib/modules'):
        if r not in [e['path'] for e in case['entries']]:
            os.utime(r, (case['older'], case['older']))
    try:
        p = subprocess.run(pre + ['bash', '-c', '. /mnt/bca-lib.sh; boot_inputs_newer'], env=env,
                           capture_output=True, text=True, timeout=60, cwd='/mnt/home')
        got, rc = p.stdout.strip(), p.returncode
    except subprocess.TimeoutExpired:
        got, rc = 'timeout', 124
    out['cases'].append({'id': case['id'], 'expect': case['expect'], 'got': got, 'rc': rc})
print(json.dumps(out))
'''


def die(msg, code=2):
    print(json.dumps({'counter': 'score-bootinputs-r43', 'error': msg, 'verdict': 'ERROR'}))
    sys.exit(code)


def git(lane, *a):
    return subprocess.run(['git', '-C', lane] + list(a), capture_output=True)


def btime():
    with open('/proc/stat') as f:
        for ln in f:
            if ln.startswith('btime '):
                return int(ln.split()[1])
    die('no btime in /proc/stat')


def subid(path, user, uid):
    try:
        with open(path) as f:
            for ln in f:
                p = ln.strip().split(':')
                if len(p) == 3 and p[0] in (user, str(uid)) and int(p[2]) >= 2:
                    return int(p[1]), int(p[2])
    except OSError:
        pass
    die(f'no subordinate id range for {user} in {path}')


def clean_env():
    return {k: v for k, v in os.environ.items() if not k.startswith(DROP) and k != 'TMPDIR'}


def make_cases(rng, bt):
    def older():
        return bt - rng.randint(3600, 30 * 86400)

    def newer():
        return bt + rng.randint(60, 86400)

    def word():
        return ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(rng.randint(4, 10)))

    def layout(missing, newer_point, deep=False):
        entries, target = [], None
        parents = set()
        for path, kind in POINTS:
            if path in missing:
                continue
            if path.startswith('/etc/default/'):
                parents.add('/etc/default')
            if kind == 'f':
                entries.append({'path': path, 'kind': 'f', 'content': word() + '\n',
                                'mode': rng.choice([0o600, 0o644]), 'mtime': older()})
                if path == newer_point:
                    target = entries[-1]
            else:
                entries.append({'path': path, 'kind': 'd', 'mtime': older()})
                cur = path
                depth = 3 if deep and path == newer_point else rng.randint(1, 3)
                for _ in range(depth - 1):
                    cur = f'{cur}/{word()}'
                    entries.append({'path': cur, 'kind': 'd', 'mtime': older()})
                for _ in range(rng.randint(1, 3)):
                    entries.append({'path': f'{cur}/{word()}.{rng.choice(["conf", "ko", "hook", "img"])}',
                                    'kind': 'f', 'content': word() + '\n',
                                    'mode': rng.choice([0o600, 0o644]), 'mtime': older()})
                if path == newer_point:
                    target = entries[-1]
        if '/etc/default/limine' in missing and rng.random() < 0.5:
            parents.add('/etc/default')
        for d in sorted(parents):
            entries.insert(0, {'path': d, 'kind': 'd', 'mtime': older()})
        if target is not None:
            target['mtime'] = newer()
        return entries

    cases = []
    for path, _ in ETC:
        others = [p for p, _ in POINTS[[q for q, _ in POINTS].index(path) + 1:]]
        cases.append({'id': f'miss{path}-newer', 'expect': '1',
                      'entries': layout({path}, rng.choice(others))})
        cases.append({'id': f'miss{path}-older', 'expect': '0', 'entries': layout({path}, None)})
    cases.append({'id': 'all-present-newer', 'expect': '1',
                  'entries': layout(set(), rng.choice([p for p, _ in POINTS]))})
    cases.append({'id': 'all-present-older', 'expect': '0', 'entries': layout(set(), None)})
    miss = set(rng.sample([p for p, _ in ETC], rng.randint(2, 4)))
    cases.append({'id': 'multi-miss-deep-modules-newer', 'expect': '1',
                  'entries': layout(miss, '/usr/lib/modules', deep=True)})
    ent = layout(set(), '/usr/lib/modules')
    ent.append({'path': f'/etc/mkinitcpio.conf.d/{word()}', 'kind': 'd', 'mode': 0o700, 'mtime': older()})
    cases.append({'id': 'unreadable-dir-modules-newer', 'expect': '1', 'entries': ent})
    for c in cases:
        c['older'] = older()
    return cases


def oracle(bt):
    for path, _ in POINTS:
        try:
            st = os.lstat(path)
        except OSError:
            continue
        if st.st_mtime > bt:
            return '1'
        if stat.S_ISDIR(st.st_mode):
            for root, dirs, files in os.walk(path, onerror=lambda e: None):
                for n in dirs + files:
                    try:
                        if os.lstat(os.path.join(root, n)).st_mtime > bt:
                            return '1'
                    except OSError:
                        pass
    return '0'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()

    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix='bootinputs-r43.', dir=a.scratch)

    def on_signal(signum, _frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)
    try:
        return run(a, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run(a, work):
    p = git(a.lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if p.returncode != 0:
        die(f'cannot resolve {a.revision}')
    rev = p.stdout.decode().strip()
    p = git(a.lane, 'show', f'{rev}:{SCRIPT}')
    if p.returncode != 0:
        die(f'{SCRIPT} absent at {rev}')
    text = p.stdout.decode(errors='replace')
    lines = text.rstrip('\n').split('\n')
    if lines[-1] != 'main "$@"':
        die('last line of the script is not main "$@"')
    lib = '\n'.join(lines[:-1]) + '\n'
    full = os.path.join(work, 'bca.sh')
    with open(full, 'w') as f:
        f.write(text)
    libp = os.path.join(work, 'bca-lib.sh')
    with open(libp, 'w') as f:
        f.write(lib)

    uid, gid = os.getuid(), os.getgid()
    user = os.environ.get('USER') or str(uid)
    try:
        import pwd
        user = pwd.getpwuid(uid).pw_name
    except (KeyError, ImportError):
        pass
    su, sn = subid('/etc/subuid', user, uid)
    sg, gn = subid('/etc/subgid', user, uid)
    env = clean_env()
    bt = btime()
    rng = random.Random(os.urandom(16))
    cases = make_cases(rng, bt)
    spec = {'lib': lib, 'uid': uid, 'gid': gid, 'env': env, 'cases': cases}
    cmd = ['unshare', '-m', f'--map-users={uid},0,1', f'--map-users={su},1,{min(sn, 65535)}',
           f'--map-groups={gid},0,1', f'--map-groups={sg},1,{min(gn, 65535)}', 'python3', '-c', INNER]
    try:
        p = subprocess.run(cmd, input=json.dumps(spec), capture_output=True, text=True, timeout=900, cwd=work)
    except subprocess.TimeoutExpired:
        die('namespace leg timed out')
    if p.returncode != 0:
        die('namespace leg failed: ' + (p.stderr or '')[-400:])
    try:
        ns = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        die('namespace leg printed no result')
    ident = ns.get('identity', [])
    identity_ok = int(ident == [str(uid), str(gid), str(gid)])
    results = ns['cases']
    correct = sum(1 for c in results if c['got'] == c['expect'])
    wrong = [c for c in results if c['got'] != c['expect']]

    live = None
    for _ in range(2):
        before = oracle(bt)
        q = subprocess.run(['bash', '-c', f'. "{libp}"; boot_inputs_newer'], env=env, capture_output=True,
                           text=True, timeout=120, cwd=work)
        after = oracle(bt)
        if before == after:
            live = {'expect': before, 'got': q.stdout.strip(), 'rc': q.returncode}
            break
    live_agree = int(bool(live) and live['got'] == live['expect'])

    st_env = dict(env, TMPDIR=os.path.join(work, 'st'))
    os.makedirs(st_env['TMPDIR'])
    try:
        q = subprocess.run(['bash', full, '--selftest'], env=st_env, capture_output=True, text=True,
                           timeout=600, cwd=work)
        st_out = q.stdout
    except subprocess.TimeoutExpired:
        st_out = ''
    m = re.search(r'^TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=(\d+) failed=0$', st_out, re.M)
    selftest_pass = int(bool(m))
    st_line = [ln for ln in st_out.splitlines() if ln.startswith('TSUKUROI_BOOTCHAIN_SELFTEST:')]
    selftest_r43 = len(re.findall(r"^\s*st_check 'R43-C1-", text, re.M))

    ok = (len(results) == 16 and correct == 16 and identity_ok == 1 and live_agree == 1
          and selftest_pass == 1 and selftest_r43 >= 2)
    print(json.dumps({
        'counter': 'score-bootinputs-r43', 'revision': rev, 'predicate': PREDICATE,
        'cases': len(results), 'correct': correct, 'wrong': wrong, 'identity': ident,
        'identity_ok': identity_ok, 'live': live, 'live_agree': live_agree, 'btime': bt,
        'selftest_pass': selftest_pass, 'selftest_line': st_line[-1] if st_line else None,
        'selftest_failures': [ln for ln in st_out.splitlines() if ln.startswith('FAIL ')],
        'selftest_r43': selftest_r43, 'channels_open': ['mount table', 'uid_map', 'script path /mnt/bca-lib.sh'],
        'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
