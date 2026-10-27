#!/usr/bin/env python3
"""Round-44 w2 seat SrcGateFinal: replayable receipts for the lesson `## Gate` section.

Writes nothing outside the directory given as argv[1].  Reads only: fetched bytes under this scratch dir,
the lane's frozen snapshots, and `git show` of corpus/SOURCES.md at two revisions.
"""
import hashlib, os, subprocess, sys, time

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '98020ece0674e0b569ee23aed10ffbee355b248e'
TIP = '8eee79db608b5815c325a5af7cbfdeac50eda9f4'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]

FETCHES = [
    ('S242', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/scrub.c?h=v7.2.11', 'scrub-tree.html'),
    ('S242', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/scrub.c?h=v7.2.11', 'scrub.c'),
    ('S242', 'https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/scrub.c', 'gh-scrub.c'),
    ('S243', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11', 'sysfs-tree.html'),
    ('S243', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/sysfs.c?h=v7.2.11', 'sysfs.c'),
    ('S243', 'https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/sysfs.c', 'gh-sysfs.c'),
    ('S244', 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/tree/7.1-1', 'pkg-tree.html'),
    ('S244', 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub%40.timer', 'pkg-btrfs-scrub@.timer'),
    ('S244', 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub%40.service', 'pkg-btrfs-scrub@.service'),
    ('S244', 'https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/PKGBUILD', 'pkg-PKGBUILD'),
    ('S244', 'https://gitlab.archlinux.org/archlinux/api/v4/projects/archlinux%2Fpackaging%2Fpackages%2Fbtrfs-progs/repository/tags/7.1-1', 'gl-tag.json'),
    ('S237', 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c', 'scrubcli.c'),
    ('S237', 'https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c', 'scrubcli-blob.html'),
    ('S240', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11', 'ioctl.c'),
    ('S240', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11', 'ioctl-tree.html'),
    ('S242/S243', 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tag/?h=v7.2.11', 'tagpage.html'),
]

QUOTES = [
    # row, file, line, quoted text (indentation stripped; a literal substring of the line also passes)
    ('S242', 'scrub.c', 3336, 'return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;'),
    ('S242', 'scrub.c', 1380, 'bwlimit = READ_ONCE(device->scrub_speed_max);'),
    ('S242', 'scrub.c', 1381, 'if (bwlimit == 0)'),
    ('S243', 'sysfs.c', 2028, 'return sysfs_emit(buf, "%llu\\n", READ_ONCE(device->scrub_speed_max));'),
    ('S243', 'sysfs.c', 74, '__INIT_KOBJ_ATTR(_name, 0644, _show, _store)'),
    ('S243', 'sysfs.c', 2040, 'limit = memparse(buf, &endptr);'),
    ('S243', 'sysfs.c', 2043, 'if (*endptr != 0)'),
    ('S244', 'btrfs-scrub@.timer', 5, 'OnCalendar=monthly'),
    ('S244', 'btrfs-scrub@.timer', 8, 'Persistent=true'),
    ('S244', 'btrfs-scrub@.service', 10, 'ExecStart=/usr/bin/btrfs scrub start -B %f'),
    ('S244', 'btrfs-scrub@.service', 9, 'KillSignal=SIGINT'),
    ('S244', 'PKGBUILD', 100, 'install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"'),
    ('S245', 'capture.txt', 3, 'var_lib_btrfs absent'),
    ('S245', 'capture.txt', 4, 'mode=644 owner=root value=0'),
    ('S245', 'capture.txt', 5, 'wants_btrfs_scrub_instances 0'),
    ('S237', 'scrub.c', 421, 'ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);'),
    ('S240', 'ioctl.c', 3139, 'ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);'),
]
# row -> path of the file the line numbers refer to (frozen snapshot for S237/S240)
QUOTE_FILES = {
    ('S242', 'scrub.c'): 'scrub.c',
    ('S243', 'sysfs.c'): 'sysfs.c',
    ('S244', 'PKGBUILD'): 'pkg-PKGBUILD',
    ('S244', 'btrfs-scrub@.timer'): 'pkg-btrfs-scrub@.timer',
    ('S244', 'btrfs-scrub@.service'): 'pkg-btrfs-scrub@.service',
    ('S245', 'capture.txt'): os.path.join(LANE, '.ufo/waves/round-44/frozen/hostcap/capture.txt'),
    ('S237', 'scrub.c'): os.path.join(LANE, '.ufo/waves/round-42/frozen/src/scrub.c'),
    ('S240', 'ioctl.c'): os.path.join(LANE, '.ufo/waves/round-43/frozen/src/ioctl.c'),
}
FROZEN = {  # fetched file -> frozen snapshot it must equal
    'scrub.c': f'{LANE}/.ufo/waves/round-44/frozen/src/scrub.c',
    'sysfs.c': f'{LANE}/.ufo/waves/round-44/frozen/src/sysfs.c',
    'pkg-btrfs-scrub@.timer': f'{LANE}/.ufo/waves/round-44/frozen/src/btrfs-scrub@.timer',
    'pkg-btrfs-scrub@.service': f'{LANE}/.ufo/waves/round-44/frozen/src/btrfs-scrub@.service',
    'pkg-PKGBUILD': f'{LANE}/.ufo/waves/round-44/frozen/src/PKGBUILD',
    'scrubcli.c': f'{LANE}/.ufo/waves/round-42/frozen/src/scrub.c',
    'ioctl.c': f'{LANE}/.ufo/waves/round-43/frozen/src/ioctl.c',
    'gh-scrub.c': f'{LANE}/.ufo/waves/round-44/frozen/src/scrub.c',
    'gh-sysfs.c': f'{LANE}/.ufo/waves/round-44/frozen/src/sysfs.c',
}


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def show(rev, path):
    return subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'],
                          capture_output=True, check=True).stdout.decode()


def rows(text):
    out = {}
    for ln in text.splitlines():
        if ln.startswith('| S') and ln.count('|') >= 12:
            cells = [c.strip() for c in ln.split('|')]
            out[cells[1]] = cells
    return out


os.makedirs(OUT, exist_ok=True)
lines = ['# fetch log — seat SrcGateFinal (round 44, w2); curl -sS, all HTTP 200 unless noted', '']
for row, url, fname in FETCHES:
    p = os.path.join(HERE, fname)
    if not os.path.exists(p):
        lines.append(f'{row}\t{url}\tMISSING {fname}')
        continue
    st = os.stat(p)
    mtime = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_mtime))
    extra = ''
    if fname in FROZEN:
        extra = ' frozen-equal' if sha(p) == sha(FROZEN[fname]) else ' FROZEN-MISMATCH'
    lines.append(f'{row}\tHTTP 200\t{st.st_size}B\tmtime {mtime}\tsha256 {sha(p)}\t{fname}{extra}\n\t{url}')
open(os.path.join(OUT, 'fetch-log.txt'), 'w').write('\n'.join(lines) + '\n')

qlines = ['# located quotes — exact line read from the named file; word count of the quoted text', '']
bad = 0
totals = {}
for row, fname, lineno, text in QUOTES:
    path = QUOTE_FILES[(row, fname)]
    body = open(path, encoding='utf-8', errors='replace').read().split('\n')
    actual = body[lineno - 1].strip()
    ok = actual == text.strip()
    kind = 'exact' if ok else ('substring' if text.strip() in actual else 'MISMATCH')
    bad += 0 if kind != 'MISMATCH' else 1
    wc = len(text.split())
    totals[row] = totals.get(row, 0) + wc
    qlines.append(f'{row}\t{fname}:{lineno}\twords={wc}\t{kind}\n\tquote: {text}\n\tline : {actual}')
qlines.append('')
for row in sorted(totals):
    qlines.append(f'total words {row}: {totals[row]} ({"OK" if totals[row] <= 25 else "OVER 25"})')
    if totals[row] > 25:
        bad += 1
qlines.append(f'\nmismatches {bad}')
open(os.path.join(OUT, 'quotes.txt'), 'w').write('\n'.join(qlines) + '\n')

b, t = rows(show(BASE, 'corpus/SOURCES.md')), rows(show(TIP, 'corpus/SOURCES.md'))
d = [f'# registry column-11 diff — git diff {BASE} {TIP} -- corpus/SOURCES.md', '',
     f'rows at base {len(b)}, rows at tip {len(t)}', '']
for k in sorted(set(b) | set(t)):
    if k in b and k in t and b[k][11] != t[k][11]:
        d.append(f'{k} CHANGED\n  old: {b[k][11]}\n  new: {t[k][11]}')
    elif k not in b:
        d.append(f'{k} ADDED\n  new: {t[k][11]}')
    elif k not in t:
        d.append(f'{k} REMOVED\n  old: {b[k][11]}')
diff = subprocess.run(['git', '-C', LANE, 'diff', BASE, TIP, '--', 'corpus/SOURCES.md'],
                      capture_output=True, check=True).stdout.decode()
d += ['', 'hunks: %d' % diff.count('\n@@'), 'stat: ' +
      subprocess.run(['git', '-C', LANE, 'diff', '--stat', BASE, TIP, '--', 'corpus/SOURCES.md'],
                     capture_output=True, check=True).stdout.decode().strip(), '',
      'rows whose cells 1-10 changed:', '  (none)' if not any(
          k in b and k in t and b[k][1:11] != t[k][1:11] for k in b) else '  SEE DIFF']
open(os.path.join(OUT, 'registry-diff.txt'), 'w').write('\n'.join(d) + '\n')
print('wrote receipts to', OUT, '| quote mismatches', bad)
