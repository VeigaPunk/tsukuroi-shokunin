#!/usr/bin/env python3
"""/proc channel enumeration for LabratViewLeak (called from probe.sh inside the counter's view ns).

Every print is flushed so a hang is attributable; a whole-block alarm bounds the run.
"""
import glob
import os
import signal
import sys

p = sys.argv[1]
base = '/proc/' + p


def alarm(_s, _f):
    print('!! ALARM: block overran 40s, abandoning remaining channels', flush=True)
    os._exit(0)


signal.signal(signal.SIGALRM, alarm)
signal.alarm(40)


def rd(path, n=4096):
    try:
        with open(path) as f:
            return f.read(n)
    except OSError as e:
        return 'ERR:%s' % e.strerror


print('parent exe     :', os.readlink(base + '/exe') if os.path.exists(base + '/exe') else 'ERR:absent', flush=True)
for k in ('cwd', 'root'):
    try:
        print('parent %-6s : %s' % (k, os.readlink(base + '/' + k)), flush=True)
    except OSError as e:
        print('parent %-6s : ERR:%s' % (k, e.strerror), flush=True)
cl = rd(base + '/cmdline')
print('parent cmdline :', cl.replace('\0', ' ') if isinstance(cl, str) else cl, flush=True)
env = rd(base + '/environ', 65536)
print('parent environ readable:', not str(env).startswith('ERR:'), flush=True)
if isinstance(env, str) and not env.startswith('ERR:'):
    keys = sorted(x.split('=')[0] for x in env.split('\0') if '=' in x)
    print('parent environ keys   :', keys, flush=True)
    print('parent environ has spec-ish keys:',
          [k for k in keys if 'SPEC' in k.upper() or 'VIEW' in k.upper() or 'MOUNTS' in k.upper()], flush=True)
else:
    print('parent environ err    :', env, flush=True)
st = rd(base + '/stat', 512)
print('parent stat tail      :', st.rsplit(')', 1)[-1].split()[:3] if not st.startswith('ERR:') else st, flush=True)

print('--- parent /proc/<pid>/fd', flush=True)
for f in sorted(glob.glob(base + '/fd/*'),
                key=lambda s: int(s.rsplit('/', 1)[1]) if s.rsplit('/', 1)[1].isdigit() else 0):
    n = f.rsplit('/', 1)[1]
    try:
        tgt = os.readlink(f)
    except OSError as e:
        print(' fd %-3s readlink ERR:%s' % (n, e.strerror), flush=True)
        continue
    res = ''
    if tgt.startswith(('pipe:', 'socket:', 'anon_inode')):
        try:
            fd = os.open(f, os.O_RDONLY | os.O_NONBLOCK)
            try:
                b = os.read(fd, 128)
            finally:
                os.close(fd)
            res = 'opened-read=%r' % b
        except OSError as e:
            res = 'open/read ERR:%s' % e.strerror
    else:
        try:
            fd = os.open(f, os.O_RDONLY | os.O_NONBLOCK)
            try:
                res = 'read=%r' % os.read(fd, 64)
            finally:
                os.close(fd)
        except OSError as e:
            res = 'read ERR:%s' % e.strerror
    print(' fd %-3s -> %-40s %s' % (n, tgt, res), flush=True)

print('--- parent memory', flush=True)
try:
    fd = os.open(base + '/mem', os.O_RDONLY)
    try:
        os.lseek(fd, 0, os.SEEK_SET)
        b = os.read(fd, 1)
        print(' mem open+read: OK bytes=%r' % b, flush=True)
    finally:
        os.close(fd)
except OSError as e:
    print(' mem open: ERR:%s (errno %d)' % (e.strerror, e.errno), flush=True)

maps = rd(base + '/maps', 65536)
if isinstance(maps, str) and not maps.startswith('ERR:'):
    cand = [l for l in maps.splitlines() if ' rw-p ' in l and '[heap]' in l]
    print(' maps readable: yes (%d lines); heap regions=%d' % (len(maps.splitlines()), len(cand)), flush=True)
    if cand:
        lo = int(cand[0].split()[0].split('-')[0], 16)
        try:
            fd = os.open(base + '/mem', os.O_RDONLY)
            try:
                os.lseek(fd, lo, os.SEEK_SET)
                b = os.read(fd, 64)
                print(' mem heap read at 0x%x: OK %r' % (lo, b), flush=True)
            finally:
                os.close(fd)
        except OSError as e:
            print(' mem heap read at 0x%x: ERR:%s' % (lo, e.strerror), flush=True)
else:
    print(' maps readable: no (%s)' % maps, flush=True)

print('--- process_vm_readv against parent', flush=True)
try:
    import ctypes
    libc = ctypes.CDLL('libc.so.6', use_errno=True)

    class IOV(ctypes.Structure):
        _fields_ = [('base', ctypes.c_void_p), ('len', ctypes.c_size_t)]

    buf = ctypes.create_string_buffer(64)
    local = IOV(ctypes.cast(buf, ctypes.c_void_p), 64)
    remote = IOV(ctypes.c_void_p(0), 64)
    n = libc.process_vm_readv(int(p), ctypes.byref(local), 1, ctypes.byref(remote), 1, 0)
    err = ctypes.get_errno()
    print(' process_vm_readv ->', n, 'errno', err, os.strerror(err) if n < 0 else '', flush=True)
except Exception as e:  # noqa: BLE001
    print(' process_vm_readv attempt raised', e, flush=True)

print('--- cross-namespace paths', flush=True)
for path in ('/proc/%s/root/sys/fs/btrfs' % p, '/proc/%s/root/proc/self/mounts' % p,
             '/proc/1/root/sys/fs/btrfs', '/proc/1/mounts'):
    try:
        if os.path.isdir(path):
            print(' %-42s DIR entries=%r' % (path, sorted(os.listdir(path))[:8]), flush=True)
        else:
            with open(path) as f:
                print(' %-42s FILE first line=%r' % (path, f.readline()[:90]), flush=True)
    except OSError as e:
        print(' %-42s ERR:%s' % (path, e.strerror), flush=True)

print('--- other processes that could hold the spec', flush=True)
hits = []
for d in glob.glob('/proc/[0-9]*'):
    c = rd(d + '/cmdline', 4096)
    if not isinstance(c, str) or c.startswith('ERR:'):
        continue
    if '-c import json' in c or 'json.load(sys.stdin)' in c:
        hits.append((d.rsplit('/', 1)[1], c.replace('\0', ' ')[:120]))
print(' builder/python -c processes:', hits if hits else 'none', flush=True)

print('--- writable shared state (cross-leg persistence channel)', flush=True)
for path in ('/tmp', '/var/tmp', '/dev/shm'):
    try:
        fd = os.open(path, os.O_TMPFILE | os.O_RDWR, 0o600)
        os.close(fd)
        w = 'O_TMPFILE-ok'
    except OSError as e:
        w = 'ERR:%s' % e.strerror
    print(' %-9s writable=%s' % (path, w), flush=True)
print(' TMPDIR =', os.environ.get('TMPDIR'), '| HOME =', os.environ.get('HOME'), flush=True)
for d in (os.environ.get('TMPDIR') or '/nonexistent', os.environ.get('HOME') or '/nonexistent',
          os.path.dirname(os.environ.get('TMPDIR') or '/nonexistent')):
    try:
        print('  tree %s -> %r' % (d, sorted(os.listdir(d))[:16]), flush=True)
    except OSError as e:
        print('  tree %s ERR:%s' % (d, e.strerror), flush=True)
