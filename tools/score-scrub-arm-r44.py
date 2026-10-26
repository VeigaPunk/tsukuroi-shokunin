#!/usr/bin/env python3
"""Round-44 C1 counter (frozen before data): the census scrub-record arm (Frontier -> Core).

Surface scored: `tools/tsukuroi-census.sh` gains a verdict-neutral line
  SCRUB btrfs-scrub-record state=NONE|RECORDED|BLOCKED dir=absent|present|unreadable records=N tmp=N
    sockets=N unreadable=N orphan=N limited=N timers=N [detail=<reason>,...,<fsid8>:<devid>:speed_max=<v>,...]
produced by a production function `probe_scrub_record` that sets SCRUB_LINE, printed by `main` after the
STORAGE line and before the TSUKUROI_CENSUS rollup. The contract the counter's own oracle implements
(independently of the scored bash) is the one the declaration (SCORECARD "Round 44 — declaration") states:
  dir      /var/lib/btrfs: absent (no entry), unreadable (exists but not a listable directory: BLOCKED,
           reason dir:unreadable), else present.
  records  regular files named scrub.status.<fsid> (lowercase UUID); a symlink or non-regular file of that
           name is BLOCKED record:not-regular. tmp: scrub.status.<fsid>_tmp likewise (tmp:not-regular).
           sockets: sockets named scrub.progress.<fsid>; another type (or a symlink) is BLOCKED
           progress:not-socket. Other names are ignored; no name is echoed.
  unreadable  records + tmp files the caller cannot read. orphan: records whose fsid has no entry under
           /sys/fs/btrfs (computed only when that root is a listable directory). Records with no sysfs
           root at all: BLOCKED sysfs:absent. An unlistable sysfs root: BLOCKED sysfs:unreadable.
  limited  devices /sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max reading one decimal line other than
           0 (listed in detail as <fsid8>:<devid>:speed_max=<v> after every block reason); unreadable or
           missing: BLOCKED <fsid8>:<devid>:speed-unreadable; not one decimal line: speed-malformed; a
           non-decimal devid: <fsid8>:?:bad-devid.
  timers   entries btrfs-scrub@*.timer under /etc/systemd/system/timers.target.wants other than the bare
           btrfs-scrub@.timer; an existing but unlistable wants dir: BLOCKED timers:unreadable.
  state    BLOCKED if any block reason, else RECORDED if records+tmp+sockets > 0, else NONE.
  order    block reasons in traversal order (sysfs fsids, devids; then record-dir names; then timers), names
           sorted bytewise; then the speed_max pairs in the same sysfs order.

Legs.
  N legs (cases): inside a private user+mount namespace (caller uid -> 0, the caller's /etc/subuid range
    from 1; QUALITY 85) tmpfs is mounted over /sys/fs/btrfs, /var/lib and /etc/systemd/system and filled
    from data read on stdin; the revision's census minus its final `main "$@"` line is sourced from a
    tmpfs at /mnt and `probe_scrub_record; printf '%s\n' "$SCRUB_LINE"` runs after `setpriv` to the
    caller's uid/gid with no supplementary groups and the caller's environment minus TSUKUROI_*, UFO_*,
    TMPDIR (QUALITY 90: production identity, production paths, no override variable). 16 cases, every
    value drawn per run (fsids, devids, counts, modes, limits, names, which entries exist).
  W leg (wired_ok): in one further namespace view with drawn values, the FULL census (`bash
    /mnt/census.sh`, timeout 300 s) must print exactly one line starting `SCRUB `, equal to the oracle's
    line, after the line starting `STORAGE ` and before the line starting `TSUKUROI_CENSUS:`.
  L leg (live_agree): the full live census at the caller's identity, no namespace; its one SCRUB line must
    equal the oracle's line built from a Python walk of the three live paths taken before and after the
    run (one retry if the two walks differ).
  S leg (selftest): `bash census --selftest` (TMPDIR in scratch) prints
    `TSUKUROI_CENSUS_SELFTEST: PASS (<n> cases, <n> passed, 0 failed)`, and the census text holds at least
    six `check` labels ending `(R44-C1)'`.

Channels (QUALITY 90). Closed: override environment (none set), process identity (caller uid/gid, no
groups), fixture values (drawn per run). Open, reported: the namespace's own traces — /proc/self/mountinfo
shows tmpfs on /sys/fs/btrfs, /var/lib and /etc/systemd/system, /proc/self/uid_map shows the mapping, and
the census is read from /mnt. The frozen control battery scores a mount-table-gated variant and records it.

Predicate (same sentence in the declaration and the receipt label):
  PASS iff cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1
  and selftest_pass == 1 and selftest_r44 >= 6.

Usage: python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]
--scratch is required; everything the counter writes lives under it and is removed on exit, SIGINT and
SIGTERM. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read/harness error.
"""
import argparse
import fnmatch
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
import uuid as uuidmod

SCRIPT = 'tools/tsukuroi-census.sh'
SYS, DIR, WANTS = '/sys/fs/btrfs', '/var/lib/btrfs', '/etc/systemd/system/timers.target.wants'
PREDICATE = ('cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 '
             'and selftest_pass == 1 and selftest_r44 >= 6')
DROP = ('TSUKUROI_', 'UFO_')
UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
CALL = '. /mnt/census-lib.sh; probe_scrub_record; printf "%s\\n" "$SCRUB_LINE"'

INNER = r'''
import json, os, shutil, socket, subprocess, sys
spec = json.load(sys.stdin)
def sh(*a):
    subprocess.run(list(a), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'r44lib', '/mnt')
for name, body in (('census-lib.sh', spec['lib']), ('census.sh', spec['full'])):
    with open('/mnt/' + name, 'w') as f:
        f.write(body)
    os.chmod('/mnt/' + name, 0o644)
os.mkdir('/mnt/home'); os.chmod('/mnt/home', 0o1777)
ROOTS = ['/sys/fs/btrfs', '/var/lib', '/etc/systemd/system']
for d in ROOTS:
    sh('mount', '-t', 'tmpfs', '-o', 'mode=755', 'r44view', d)
env = spec['env']
pre = ['setpriv', '--reuid=%d' % spec['uid'], '--regid=%d' % spec['gid'], '--clear-groups']
out = {'cases': []}
p = subprocess.run(pre + ['bash', '-c', 'id -u; id -g; id -G'], env=env, capture_output=True, text=True, timeout=30)
out['identity'] = p.stdout.split()
socks = []
def build(case):
    for s in socks:
        s.close()
    del socks[:]
    for r in ROOTS:
        os.chmod(r, 0o755)
        for n in os.listdir(r):
            q = os.path.join(r, n)
            if os.path.isdir(q) and not os.path.islink(q):
                for dp, dn, fn in os.walk(q):
                    os.chmod(dp, 0o755)
                shutil.rmtree(q)
            else:
                os.unlink(q)
    later = []
    for e in case['entries']:
        p, k = e['path'], e['kind']
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if k == 'dir':
            os.makedirs(p, exist_ok=True)
            if 'mode' in e:
                later.append((p, e['mode']))
        elif k == 'file':
            with open(p, 'w') as f:
                f.write(e.get('content', ''))
            os.chmod(p, e.get('mode', 0o644))
        elif k == 'symlink':
            os.symlink(e['target'], p)
        elif k == 'fifo':
            os.mkfifo(p)
        elif k == 'socket':
            s = socket.socket(socket.AF_UNIX)
            s.bind(p)
            socks.append(s)
    for p, m in sorted(later, key=lambda t: -t[0].count('/')):
        os.chmod(p, m)
    for r, m in case.get('root_modes', {}).items():
        os.chmod(r, m)
def run(cmd, timeout):
    try:
        p = subprocess.run(pre + ['bash', '-c', cmd], env=env, capture_output=True, text=True,
                           timeout=timeout, cwd='/mnt/home')
        return p.stdout, p.returncode
    except subprocess.TimeoutExpired:
        return 'timeout', 124
for case in spec['cases']:
    build(case)
    o, rc = run(spec['call'], 60)
    out['cases'].append({'id': case['id'], 'got': o, 'rc': rc})
build(spec['wired'])
o, rc = run('bash /mnt/census.sh', 300)
out['wired'] = {'stdout': o, 'rc': rc}
print(json.dumps(out))
'''


def die(msg, code=2):
    print(json.dumps({'counter': 'score-scrub-arm-r44', 'error': msg, 'verdict': 'ERROR'}))
    sys.exit(code)


def git(lane, *a):
    return subprocess.run(['git', '-C', lane] + list(a), capture_output=True)


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


# ---- the oracle: a model of the three paths -> the expected SCRUB line ----------------------
# model = {'sys': None | 'unreadable' | {fsid: {devname: None | 'unreadable' | <content str>}},
#          'dir': None | 'unreadable' | {name: ('file', readable) | ('symlink',) | ('dir',) | ('socket',) | ('fifo',)},
#          'wants': None | 'unreadable' | [names]}
def lines_of(content):
    segs = content.split('\n')
    if content.endswith('\n') or content == '':
        segs = segs[:-1]
    return segs


def expect(model):
    blocked, info = [], []
    lim = rec = tmp = sock = unr = orph = tim = 0
    sysok, fsids = False, set()
    s = model['sys']
    if s == 'unreadable':
        blocked.append('sysfs:unreadable')
    elif isinstance(s, dict):
        sysok = True
        for fsid in sorted(s):
            if not re.fullmatch(UUID, fsid):
                continue
            fsids.add(fsid)
            for dn in sorted(s[fsid]):
                v = s[fsid][dn]
                if not re.fullmatch(r'[0-9]+', dn):
                    blocked.append(f'{fsid[:8]}:?:bad-devid')
                elif v is None or v == 'unreadable':
                    blocked.append(f'{fsid[:8]}:{dn}:speed-unreadable')
                else:
                    ls = lines_of(v)
                    if len(ls) != 1 or not re.fullmatch(r'[0-9]+', ls[0]):
                        blocked.append(f'{fsid[:8]}:{dn}:speed-malformed')
                    elif not re.fullmatch(r'0+', ls[0]):
                        lim += 1
                        info.append(f'{fsid[:8]}:{dn}:speed_max={ls[0]}')
    d = model['dir']
    ds = 'absent'
    if d == 'unreadable':
        ds = 'unreadable'
        blocked.append('dir:unreadable')
    elif isinstance(d, dict):
        ds = 'present'
        for n in sorted(d):
            if not n.startswith('scrub.'):
                continue
            k = d[n]
            m = re.fullmatch(r'scrub\.status\.(' + UUID + ')', n)
            if m:
                if k[0] != 'file':
                    blocked.append('record:not-regular')
                    continue
                rec += 1
                unr += 0 if k[1] else 1
                if sysok and m.group(1) not in fsids:
                    orph += 1
            elif re.fullmatch(r'scrub\.status\.' + UUID + '_tmp', n):
                if k[0] != 'file':
                    blocked.append('tmp:not-regular')
                    continue
                tmp += 1
                unr += 0 if k[1] else 1
            elif re.fullmatch(r'scrub\.progress\.' + UUID, n):
                if k[0] != 'socket':
                    blocked.append('progress:not-socket')
                    continue
                sock += 1
        if rec > 0 and not sysok and s is None:
            blocked.append('sysfs:absent')
    w = model['wants']
    if w == 'unreadable':
        blocked.append('timers:unreadable')
    elif isinstance(w, list):
        tim = sum(1 for n in w if fnmatch.fnmatchcase(n, 'btrfs-scrub@*.timer') and n != 'btrfs-scrub@.timer')
    state = 'BLOCKED' if blocked else ('RECORDED' if rec + tmp + sock > 0 else 'NONE')
    line = (f'SCRUB btrfs-scrub-record state={state} dir={ds} records={rec} tmp={tmp} sockets={sock} '
            f'unreadable={unr} orphan={orph} limited={lim} timers={tim}')
    det = blocked + info
    if det:
        line += ' detail=' + ','.join(det)
    return line


# ---- per-run drawn cases: model + namespace entries ------------------------------------------
class Draw:
    def __init__(self, rng):
        self.rng = rng

    def fsid(self):
        return str(uuidmod.UUID(int=self.rng.getrandbits(128), version=4))

    def word(self, a=3, b=9):
        return ''.join(self.rng.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(self.rng.randint(a, b)))

    def devids(self, n):
        return [str(x) for x in self.rng.sample(range(1, 40), n)]


def materialize(cid, model, extra_sys=(), extra_dir=(), wants_kinds=None):
    """Namespace entries for a model. Files the scored uid must not read are mode 0600 (owner: ns root)."""
    ents, roots = [], {}
    s = model['sys']
    if s == 'unreadable':
        roots['/sys/fs/btrfs'] = 0o700
    elif isinstance(s, dict):
        for fsid, devs in s.items():
            ents.append({'path': f'{SYS}/{fsid}/devinfo', 'kind': 'dir'})
            ents.append({'path': f'{SYS}/{fsid}/features', 'kind': 'dir'})
            for dn, v in devs.items():
                ents.append({'path': f'{SYS}/{fsid}/devinfo/{dn}', 'kind': 'dir'})
                if v is None:
                    continue
                if v == 'unreadable':
                    ents.append({'path': f'{SYS}/{fsid}/devinfo/{dn}/scrub_speed_max', 'kind': 'file',
                                 'content': '0\n', 'mode': 0o600})
                else:
                    ents.append({'path': f'{SYS}/{fsid}/devinfo/{dn}/scrub_speed_max', 'kind': 'file',
                                 'content': v, 'mode': 0o644})
                ents.append({'path': f'{SYS}/{fsid}/devinfo/{dn}/error_stats', 'kind': 'file',
                             'content': 'write_errs 0\n', 'mode': 0o644})
        ents.extend(extra_sys)
    d = model['dir']
    if d == 'unreadable':
        ents.append({'path': DIR, 'kind': 'dir', 'mode': 0o700})
        ents.append({'path': f'{DIR}/scrub.status.{model.get("hidden_fsid", "x")}', 'kind': 'file',
                     'content': 'scrub status:1\n', 'mode': 0o644})
    elif d == 'notdir':
        ents.append({'path': DIR, 'kind': 'file', 'content': '', 'mode': 0o644})
    elif isinstance(d, dict):
        ents.append({'path': DIR, 'kind': 'dir', 'mode': 0o755})
        for n, k in d.items():
            p = f'{DIR}/{n}'
            if k[0] == 'file':
                ents.append({'path': p, 'kind': 'file', 'content': 'scrub status:1\n',
                             'mode': 0o644 if k[1] else 0o600})
            elif k[0] == 'symlink':
                ents.append({'path': p, 'kind': 'symlink', 'target': '/mnt/census-lib.sh'})
            elif k[0] == 'dir':
                ents.append({'path': p, 'kind': 'dir', 'mode': 0o755})
            else:
                ents.append({'path': p, 'kind': k[0]})
        ents.extend(extra_dir)
    w = model['wants']
    if w == 'unreadable':
        ents.append({'path': WANTS, 'kind': 'dir', 'mode': 0o700})
    elif isinstance(w, list):
        ents.append({'path': WANTS, 'kind': 'dir', 'mode': 0o755})
        for n in w:
            k = (wants_kinds or {}).get(n, 'symlink')
            if k == 'symlink':
                ents.append({'path': f'{WANTS}/{n}', 'kind': 'symlink',
                             'target': '/usr/lib/systemd/system/' + n.split('@')[0] + '@.timer'})
            else:
                ents.append({'path': f'{WANTS}/{n}', 'kind': 'file', 'content': '', 'mode': 0o644})
    return {'id': cid, 'entries': ents, 'root_modes': roots}


def to_model(model):
    """The oracle reads 'notdir' as an unreadable record directory."""
    m = dict(model)
    if m['dir'] == 'notdir':
        m['dir'] = 'unreadable'
    return m


def make_cases(rng, live_fsids):
    D = Draw(rng)
    cases = []

    def sysfs(nfs=1, ndev=1, speeds=None, live=None):
        # the host's own fsids enter the drawn views (always where live=True, else half the time), so an arm
        # keyed on "an fsid that is not this host's" cannot tell the namespace view from production
        out = {}
        for i in range(nfs):
            use_live = live_fsids and i == 0 and (live is True or (live is None and rng.random() < 0.5))
            f = rng.choice(live_fsids) if use_live else D.fsid()
            out[f] = {dn: (speeds() if speeds else '0\n') for dn in D.devids(rng.randint(1, ndev))}
        return out

    def timer_names(k):
        pool = ['btrfs-scrub@-.timer', 'btrfs-scrub@home.timer', 'btrfs-scrub@srv-data.timer',
                'btrfs-scrub@var-lib-machines.timer', 'btrfs-scrub@mnt-x2dbackup.timer']
        return rng.sample(pool, k)

    def add(cid, model, **kw):
        cases.append((cid, model, materialize(cid, model, **kw)))

    s = sysfs(rng.randint(1, 2), 3)
    add('none-dir-absent', {'sys': s, 'dir': None, 'wants': None})
    s = sysfs(1, 2, live=True)
    fs = list(s)
    add('recorded-readable', {'sys': s, 'dir': {f'scrub.status.{f}': ('file', True) for f in fs},
                              'wants': [D.word() + '.timer']})
    s = sysfs(rng.randint(1, 3), 2, live=True)
    add('root-records-unreadable', {'sys': s, 'dir': {f'scrub.status.{f}': ('file', False) for f in s}, 'wants': []})
    s = sysfs(1, 2)
    gone = [D.fsid() for _ in range(rng.randint(1, 3))]
    dd = {f'scrub.status.{f}': ('file', rng.random() < 0.5) for f in list(s) + gone}
    add('orphan-records', {'sys': s, 'dir': dd, 'wants': None})
    s = sysfs(rng.randint(1, 2), 2)
    dd = {}
    for f in s:
        dd[f'scrub.status.{f}'] = ('file', rng.random() < 0.5)
        dd[f'scrub.status.{f}_tmp'] = ('file', rng.random() < 0.5)
    add('tmp-beside-record', {'sys': s, 'dir': dd, 'wants': None})
    s = sysfs(1, 1)
    f = list(s)[0]
    add('progress-socket', {'sys': s, 'dir': {f'scrub.progress.{f}': ('socket',),
                                              f'scrub.status.{f}': ('file', False)}, 'wants': None})
    s = sysfs(rng.randint(2, 3), 4, live=True, speeds=lambda: rng.choice(['0\n', '%d\n' % rng.randint(1, 10 ** 10),
                                                              '%d\n' % rng.randint(1, 999)]))
    first = list(s)[0]
    dn = list(s[first])[0]
    s[first][dn] = '%d\n' % rng.randint(10 ** 6, 10 ** 9)
    extra = next(str(x) for x in rng.sample(range(10, 40), 30) if str(x) not in s[first])
    s[first][extra] = '%d\n' % rng.randint(1, 99)
    add('limited-devices', {'sys': s, 'dir': None, 'wants': None})
    s = sysfs(1, 2)
    f = list(s)[0]
    s[f][list(s[f])[0]] = rng.choice(['12k\n', '\n', '', '1\n2\n', ' 5\n', '-1\n', '0x10\n', '5 \n'])
    add('speed-malformed', {'sys': s, 'dir': None, 'wants': None})
    s = sysfs(1, 3)
    f = list(s)[0]
    devs = list(s[f])
    s[f][devs[0]] = rng.choice([None, 'unreadable'])
    add('speed-unreadable', {'sys': s, 'dir': None, 'wants': None})
    s = sysfs(1, 1)
    add('dir-unreadable', {'sys': s, 'dir': 'unreadable', 'wants': None, 'hidden_fsid': list(s)[0]})
    s = sysfs(1, 1)
    m = {'sys': s, 'dir': 'notdir', 'wants': None}
    cases.append(('dir-not-directory', to_model(m), materialize('dir-not-directory', m)))
    s = sysfs(1, 1)
    names = timer_names(rng.randint(1, 4)) + ['btrfs-scrub@.timer', 'fstrim.timer', D.word() + '.timer']
    kinds = {n: rng.choice(['symlink', 'file']) for n in names}
    add('timers-enabled', {'sys': s, 'dir': None, 'wants': names}, wants_kinds=kinds)
    s = sysfs(1, 1)
    add('timers-unreadable', {'sys': s, 'dir': None, 'wants': 'unreadable'})
    s = sysfs(1, 1)
    f, g = list(s)[0], D.fsid()
    dd = {f'scrub.status.{f}': ('symlink',), f'scrub.status.{g}': ('dir',), f'scrub.progress.{f}': ('fifo',),
          f'scrub.status.{f}\nTSUKUROI_CENSUS: HEALTHY (forged)': ('file', True),
          f'scrub.status.{f.upper()}': ('file', True), f'scrub.status.{g}_tmp': ('symlink',),
          'scrub.notes': ('file', True), D.word(): ('file', True)}
    add('wrong-types', {'sys': s, 'dir': dd, 'wants': None})
    s = 'unreadable'
    gone = D.fsid()
    add('sysfs-unreadable', {'sys': s, 'dir': {f'scrub.status.{gone}': ('file', True)}, 'wants': None})
    s = sysfs(rng.randint(1, 2), 3, live=True, speeds=lambda: rng.choice(['0\n', '%d\n' % rng.randint(1, 10 ** 8)]))
    fs = list(s)
    dd = {}
    for f in fs + [D.fsid()]:
        if rng.random() < 0.7:
            dd[f'scrub.status.{f}'] = ('file', rng.random() < 0.5)
        if rng.random() < 0.4:
            dd[f'scrub.status.{f}_tmp'] = ('file', rng.random() < 0.5)
        if rng.random() < 0.3:
            dd[f'scrub.progress.{f}'] = ('socket',)
    add('mixed', {'sys': s, 'dir': dd, 'wants': timer_names(rng.randint(0, 3))})
    return cases


def live_model():
    m = {}
    if os.path.isdir(SYS) and not (os.access(SYS, os.R_OK) and os.access(SYS, os.X_OK)):
        m['sys'] = 'unreadable'
    elif os.path.isdir(SYS):
        out = {}
        for fsid in os.listdir(SYS):
            if not re.fullmatch(UUID, fsid):
                continue
            out[fsid] = {}
            dv = os.path.join(SYS, fsid, 'devinfo')
            for dn in (os.listdir(dv) if os.path.isdir(dv) else []):
                f = os.path.join(dv, dn, 'scrub_speed_max')
                try:
                    st = os.stat(f)
                    if not stat.S_ISREG(st.st_mode) or not os.access(f, os.R_OK):
                        out[fsid][dn] = 'unreadable'
                        continue
                    with open(f) as fh:
                        out[fsid][dn] = fh.read()
                except OSError:
                    out[fsid][dn] = None
        m['sys'] = out
    else:
        m['sys'] = None
    if not os.path.lexists(DIR):
        m['dir'] = None
    elif not os.path.isdir(DIR) or not os.access(DIR, os.R_OK | os.X_OK):
        m['dir'] = 'unreadable'
    else:
        dd = {}
        for n in os.listdir(DIR):
            p = os.path.join(DIR, n)
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                dd[n] = ('symlink',)
            elif stat.S_ISREG(st.st_mode):
                dd[n] = ('file', os.access(p, os.R_OK))
            elif stat.S_ISSOCK(st.st_mode):
                dd[n] = ('socket',)
            elif stat.S_ISDIR(st.st_mode):
                dd[n] = ('dir',)
            else:
                dd[n] = ('fifo',)
        m['dir'] = dd
    if not os.path.lexists(WANTS):
        m['wants'] = None
    elif not os.path.isdir(WANTS) or not os.access(WANTS, os.R_OK | os.X_OK):
        m['wants'] = 'unreadable'
    else:
        m['wants'] = os.listdir(WANTS)
    return m


def scrub_lines(out):
    return [ln for ln in out.split('\n') if ln.startswith('SCRUB ')]


def wired_check(out, want):
    ls = out.split('\n')
    sc = [i for i, ln in enumerate(ls) if ln.startswith('SCRUB ')]
    st = [i for i, ln in enumerate(ls) if ln.startswith('STORAGE ')]
    ro = [i for i, ln in enumerate(ls) if ln.startswith('TSUKUROI_CENSUS:')]
    return int(len(sc) == 1 and ls[sc[0]] == want and len(st) == 1 and len(ro) == 1 and st[0] < sc[0] < ro[0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix='scrub-arm-r44.', dir=a.scratch)

    def on_signal(signum, _frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)
    try:
        return run(a, work)
    finally:
        subprocess.run(['chmod', '-R', 'u+rwx', work], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        die('last line of the census is not main "$@"')
    lib = '\n'.join(lines[:-1]) + '\n'
    full = os.path.join(work, 'census.sh')
    with open(full, 'w') as f:
        f.write(text)

    uid, gid = os.getuid(), os.getgid()
    user = str(uid)
    try:
        import pwd
        user = pwd.getpwuid(uid).pw_name
    except (KeyError, ImportError):
        pass
    su, sn = subid('/etc/subuid', user, uid)
    sg, gn = subid('/etc/subgid', user, uid)
    env = clean_env()
    rng = random.Random(os.urandom(16))
    live_fsids = sorted(n for n in (os.listdir(SYS) if os.path.isdir(SYS) else []) if re.fullmatch(UUID, n))
    drawn = make_cases(rng, live_fsids)
    wired_cases = make_cases(rng, live_fsids)
    wid, wmodel, wspec = wired_cases[-1]
    spec = {'lib': lib, 'full': text, 'uid': uid, 'gid': gid, 'env': env, 'call': CALL,
            'cases': [c[2] for c in drawn], 'wired': wspec}
    cmd = ['unshare', '-m', f'--map-users={uid},0,1', f'--map-users={su},1,{min(sn, 65535)}',
           f'--map-groups={gid},0,1', f'--map-groups={sg},1,{min(gn, 65535)}', 'python3', '-c', INNER]
    try:
        p = subprocess.run(cmd, input=json.dumps(spec), capture_output=True, text=True, timeout=1200, cwd=work)
    except subprocess.TimeoutExpired:
        die('namespace leg timed out')
    if p.returncode != 0:
        die('namespace leg failed: ' + (p.stderr or '')[-600:])
    try:
        ns = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        die('namespace leg printed no result')
    ident = ns.get('identity', [])
    identity_ok = int(ident == [str(uid), str(gid), str(gid)])
    results, wrong = [], []
    for (cid, model, _), got in zip(drawn, ns['cases']):
        want = expect(model)
        g = scrub_lines(got['got'])
        ok = got['rc'] == 0 and g == [want] and got['got'].strip('\n') == want
        results.append(ok)
        if not ok:
            wrong.append({'id': cid, 'want': want, 'got': got['got'][-400:], 'rc': got['rc']})
    correct = sum(results)
    wwant = expect(wmodel)
    wired_ok = wired_check(ns['wired']['stdout'], wwant)
    wired = {'want': wwant, 'got': scrub_lines(ns['wired']['stdout']), 'rc': ns['wired']['rc']}

    live = None
    for _ in range(2):
        before = expect(live_model())
        try:
            q = subprocess.run(['bash', full], env=env, capture_output=True, text=True, timeout=300, cwd=work)
            lo = q.stdout
        except subprocess.TimeoutExpired:
            lo = ''
        after = expect(live_model())
        if before == after:
            live = {'want': before, 'got': scrub_lines(lo), 'wired': wired_check(lo, before)}
            break
    live_agree = int(bool(live) and live['wired'] == 1)

    st_env = dict(env, TMPDIR=os.path.join(work, 'st'))
    os.makedirs(st_env['TMPDIR'])
    try:
        q = subprocess.run(['bash', full, '--selftest'], env=st_env, capture_output=True, text=True,
                           timeout=900, cwd=work)
        st_out = q.stdout
    except subprocess.TimeoutExpired:
        st_out = ''
    m = re.search(r'^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$', st_out, re.M)
    selftest_pass = int(bool(m) and m.group(1) == m.group(2))
    st_line = [ln for ln in st_out.splitlines() if ln.startswith('TSUKUROI_CENSUS_SELFTEST:')]
    selftest_r44 = len(re.findall(r"^\s*check '[^'\n]*\(R44-C1\)' ", text, re.M))

    ok = (len(results) == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1
          and selftest_pass == 1 and selftest_r44 >= 6)
    print(json.dumps({
        'counter': 'score-scrub-arm-r44', 'revision': rev, 'predicate': PREDICATE,
        'cases': len(results), 'correct': correct, 'wrong': wrong, 'identity': ident,
        'identity_ok': identity_ok, 'wired': wired, 'wired_ok': wired_ok, 'live': live,
        'live_agree': live_agree, 'selftest_pass': selftest_pass,
        'selftest_line': st_line[-1] if st_line else None,
        'selftest_failures': [ln for ln in st_out.splitlines() if ln.startswith('FAIL ')][:20],
        'selftest_r44': selftest_r44,
        'channels_open': ['mount table', 'uid_map', 'script path /mnt/census-lib.sh'],
        'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
