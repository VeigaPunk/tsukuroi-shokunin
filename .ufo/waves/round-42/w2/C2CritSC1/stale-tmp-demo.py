#!/usr/bin/env python3
"""C2CritSC1 (V-1b) counterexample apparatus.

Models cmds/scrub.c (pinned snapshot, sha256 48df2e2f...) record write path with the
EXACT flags the code uses:

  scrub.c:517   return scrub_open_file(datafile, O_WRONLY|O_CREAT);     <-- no O_TRUNC
  scrub.c:483   fd = open(datafile, m, 0600);
  scrub.c:487   ret = flock(fd, LOCK_EX|LOCK_NB);
  scrub.c:925   err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");  <-- rename after write
  scrub.c:1502  /* write all-zero progress file for a start */
  scrub.c:931   ret = close(fd);                                        <-- after rename

Nothing here touches /var/lib/btrfs; everything lives under $TMPDIR.
"""
import fcntl
import os
import sys

UUID = "1d02a454-c549-4a35-b567-89d60902af8e"
BASE = "scrub.status"
TMP = "tmp"

FIELDS = [
    "data_extents_scrubbed", "tree_extents_scrubbed", "data_bytes_scrubbed",
    "tree_bytes_scrubbed", "read_errors", "csum_errors", "verify_errors",
    "no_csum", "csum_discards", "super_errors", "malloc_errors",
    "uncorrectable_errors", "corrected_errors", "last_physical", "t_start",
    "t_resumed", "duration", "canceled", "finished",
]


def record(pairs):
    """scrub_write_file(): header line, then one uuid:devid|k:v...|k:v\\n per device."""
    out = "scrub status:1\n"
    for devid, vals in pairs:
        line = f"{UUID}:{devid}" + "".join(f"|{k}:{vals[k]}" for k in FIELDS)
        out += line + "\n"
    return out.encode()


def datafile(name):
    return os.path.join(os.environ["TMPDIR"], f"{BASE}.{UUID}" + (f"_{name}" if name else ""))


def open_w(path):
    """scrub_open_file_w -> scrub_open_file(path, O_WRONLY|O_CREAT): 0600, LOCK_EX|LOCK_NB."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return fd


def step(title):
    print(f"\n===== {title} =====")


rec = datafile(None)
tmp = datafile(TMP)
for p in (rec, tmp):
    if os.path.exists(p):
        os.unlink(p)

# ---------------------------------------------------------------- run 1, killed
old = record([(1, {
    "data_extents_scrubbed": 2918400, "tree_extents_scrubbed": 37911,
    "data_bytes_scrubbed": 11952783360, "tree_bytes_scrubbed": 155283456,
    "read_errors": 0, "csum_errors": 0, "verify_errors": 0, "no_csum": 0,
    "csum_discards": 0, "super_errors": 0, "malloc_errors": 0,
    "uncorrectable_errors": 0, "corrected_errors": 0,
    "last_physical": 47104780288, "t_start": 1793039861, "t_resumed": 0,
    "duration": 4213, "canceled": 0, "finished": 0})])
step("run 1: one progress update written to _tmp, then SIGKILL before rename")
fd = open_w(tmp)
os.write(fd, old)
os.fsync(fd)  # even a fully durable _tmp is enough; then the process dies
os.close(fd)  # no rename: scrub.c:925 never runs
print("leftover tmp exists:", os.path.exists(tmp), "size:", os.path.getsize(tmp))

# ------------------------------------------------- run 2 start: all-zero record
new = record([(1, {k: 0 for k in FIELDS} | {"finished": 0})])
step("run 2: scrub start writes the all-zero record (scrub.c:1502) over the same _tmp")
print("new record bytes:", len(new), " stale _tmp bytes:", len(old),
      " -> new is shorter:", len(new) < len(old))
fd = open_w(tmp)
os.write(fd, new)
os.close(fd)
os.rename(tmp, rec)  # scrub.c:925 + :534

got = open(rec, "rb").read()
step("result of rename(tmp -> record)")
print("record size:", len(got), " == len(new)?", len(got) == len(new))
print("record == new?", got == new, "| record == old?", got == old)
print("head equals the all-zero record:", got[:len(new)] == new)
tail = got[len(new):]
print("appended bytes:", len(tail))
print("--- record as a reader sees it (C-escaped, lines) ---")
for n, line in enumerate(got.split(b"\n"), 1):
    print(f"  line {n}: {line!r}")
print("--- tail is a verbatim suffix of the killed run's record:", tail == old[len(new):])

# ------------------------------------------------------------ parser consequence
step("scrub_read_file() line acceptance (scrub.c:635-699, 745-753)")
ok = True
for n, line in enumerate(got.split(b"\n")[1:], 1):
    if not line:
        continue
    head, sep, _ = line.partition(b":")
    devid = line[len(head) + 1:].split(b"|")[0]
    uuid_ok = sep == b":" and len(head) == 36 and all(
        c in b"0123456789abcdef-" for c in head)
    devid_ok = devid.isdigit()
    print(f"  line {n + 1}: uuid_field_ok={uuid_ok} devid_field_ok={devid_ok} "
          f"-> {'accepted as a device entry' if uuid_ok and devid_ok else 'state 3/4 _SCRUB_INVALID -> warning + skip'}")
    ok = ok and uuid_ok and devid_ok
print("all lines parseable:", ok)

# --------------------------------------------------------- lock window, second
step("lock/window: writer holds LOCK_EX on the renamed inode until scrub.c:931")
rec2 = datafile(None)
if os.path.exists(rec2):
    os.unlink(rec2)
fd = open_w(rec2)                      # writer: open _tmp (here: the record path)
os.write(fd, new)
os.fsync(fd)
probe = os.open(rec2, os.O_RDONLY)     # reader after the "rename": record exists...
try:
    fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
    print("reader flock: acquired (unexpected)")
except BlockingIOError as exc:
    print(f"reader flock while writer fd still open: EWOULDBLOCK ({exc.strerror}) -> reader sees NEITHER old nor new")
os.close(probe)
os.close(fd)
probe = os.open(rec2, os.O_RDONLY)
fcntl.flock(probe, fcntl.LOCK_EX | fcntl.LOCK_NB)
print("reader flock after writer close: acquired")
os.close(probe)

for p in (rec, tmp, rec2):
    if os.path.exists(p):
        os.unlink(p)
sys.exit(0)
