import os, fcntl, errno, pathlib
d = pathlib.Path('/fast/scratch/hyaku/tsukuroi-r42/C2PostCritBinding/demo2'); d.mkdir(exist_ok=True)
tmp = d / 'scrub.status.fsid_tmp'; rec = d / 'scrub.status.fsid'
# writer path of scrub_open_file (scrub.c:483-495): open then flock(LOCK_EX|LOCK_NB)
fd = os.open(tmp, os.O_WRONLY | os.O_CREAT, 0o600)
fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
os.write(fd, b'scrub status:1\nfsid:1|finished:0\n')
os.rename(tmp, rec)                        # scrub.c:925 -> rename() at :534, fd still open
def try_reader(tag):
    rf = os.open(rec, os.O_RDONLY)
    try:
        fcntl.flock(rf, fcntl.LOCK_EX | fcntl.LOCK_NB); print(tag, 'ACQUIRED')
    except OSError as e:
        print(tag, 'FAILED', errno.errorcode[e.errno], '(scrub_open_file returns -EWOULDBLOCK)')
    os.close(rf)
try_reader('reader in rename..close window:')
os.close(fd)                               # scrub.c:931 close releases the lock
try_reader('reader after close:            ')
