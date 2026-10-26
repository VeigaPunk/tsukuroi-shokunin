import os, fcntl, errno, pathlib
d = pathlib.Path('/fast/scratch/hyaku/tsukuroi-r42/C2PostCritBinding/demo'); d.mkdir(exist_ok=True)
tmp = d / 'scrub.status.fsid_tmp'; rec = d / 'scrub.status.fsid'
# 1. writer flags as in scrub.c:517 (O_WRONLY|O_CREAT, no O_TRUNC)
fd = os.open(tmp, os.O_WRONLY | os.O_CREAT, 0o600)
long_rec = b'scrub status:1\n' + b'fsid:1|' + b'x' * 300 + b'\n'
os.write(fd, long_rec); os.fsync(fd); os.close(fd)      # "killed" run leaves _tmp
print('leftover _tmp size:', tmp.stat().st_size)
short_rec = b'scrub status:1\n' + b'fsid:1|finished:0\n'
fd = os.open(tmp, os.O_WRONLY | os.O_CREAT, 0o600)      # same flags, next run
os.write(fd, short_rec); os.fsync(fd)
os.rename(tmp, rec)                                     # rename before close (scrub.c:925 -> :534)
print('rename done, fd still open (writer holds LOCK_EX on the renamed inode)')
# 2. reader in the rename..close window: scrub_open_file -> open(rec) then flock(LOCK_EX|LOCK_NB)
rf = os.open(rec, os.O_RDONLY)
try:
    fcntl.flock(rf, fcntl.LOCK_EX | fcntl.LOCK_NB); print('reader lock: ACQUIRED (contradicts the seat claim)')
except OSError as e:
    print('reader lock: FAILED', errno.errorcode[e.errno], '-> scrub_open_file returns -EWOULDBLOCK')
os.close(rf); os.close(fd)
body = rec.read_bytes()
print('record size after rename:', len(body), 'new record bytes:', len(short_rec), 'new is shorter:', len(body) > len(short_rec))
print('record == new?', body == short_rec, '| record endswith stale tail?', body.endswith(b'x\n'))
print('tail repr:', body[-20:])
rf = os.open(rec, os.O_RDONLY)
try: fcntl.flock(rf, fcntl.LOCK_EX | fcntl.LOCK_NB); print('reader lock after close: ACQUIRED')
except OSError as e: print('reader lock after close: FAILED', errno.errorcode[e.errno])
os.close(rf)
