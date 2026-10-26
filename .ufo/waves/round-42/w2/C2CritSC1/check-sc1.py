#!/usr/bin/env python3
"""C2CritSC1 (V-1b): verify every Quote line of row SC1 against the pinned snapshot,
and check the Host reading's capture.txt pointers. Read-only."""
import hashlib
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SRC = f"{LANE}/.ufo/waves/round-42/frozen/src"
CAP = f"{LANE}/.ufo/waves/round-42/frozen/hostcap/capture.txt"
ROW = "sc1.txt"

# ---- frozen snapshot digests -------------------------------------------------
sums = {}
for line in open(f"{SRC}/SHA256SUMS"):
    line = line.strip()
    if not line:
        continue
    digest, name = line.split()
    sums[name.lstrip("*")] = digest
for name, digest in sums.items():
    got = hashlib.sha256(open(f"{SRC}/{name}", "rb").read()).hexdigest()
    print(f"snapshot {name}: {got} {'OK' if got == digest else 'MISMATCH'}")

cmp_digest = hashlib.sha256(open(CAP, "rb").read()).hexdigest()
print(f"capture.txt: {cmp_digest}")

# ---- quote check -------------------------------------------------------------
lines = open(ROW).read().splitlines()
pat = re.compile(r'^\*\*Quote\.\*\* `S(\d+)` ([\w.]+):(\d+): "(.*)"$')
fail = 0
n = 0
for lineno, text in enumerate(lines, 1):
    m = pat.match(text)
    if not m:
        continue
    n += 1
    src_id, fname, srcline, quote = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    if fname == "CHANGES":
        body = open(f"{SRC}/CHANGES", encoding="utf-8", errors="replace").read().splitlines()
    else:
        body = open(f"{SRC}/{fname}", encoding="utf-8", errors="replace").read().splitlines()
    if srcline > len(body):
        print(f"row:{lineno} S{src_id} {fname}:{srcline}: LINE BEYOND EOF ({len(body)})")
        fail += 1
        continue
    actual = body[srcline - 1]
    ok = quote in actual
    if not ok:
        fail += 1
    print(f"row:{lineno} S{src_id} {fname}:{srcline}: {'OK' if ok else 'ABSENT'} | quote={quote!r} | line={actual!r}")
print(f"quotes checked={n} failures={fail}")

# ---- host reading pointers ---------------------------------------------------
cap = open(CAP).read().splitlines()
checks = [(6, "/var/lib/btrfs", "absent"), (5, "root_fsid", "1d02a454-c549-4a35-b567-89d60902af8e")]
for ln, needle1, needle2 in checks:
    body = cap[ln - 1]
    ok = needle1 in body and needle2 in body
    print(f"capture.txt:{ln}: {'OK' if ok else 'MISMATCH'} | {body!r}")

# ---- line 67 / 517 exact flags ----------------------------------------------
scrub = open(f"{SRC}/scrub.c").read().splitlines()
for ln in (67, 459, 467, 483, 487, 517, 534, 917, 922, 925, 931, 1502, 1503):
    print(f"scrub.c:{ln}: {scrub[ln - 1]!r}")

# ---- any truncate / fsync / tmp cleanup at all? ------------------------------
for needle in ("O_TRUNC", "O_EXCL", "ftruncate", "truncate", "fsync", "fdatasync", "chmod", "umask"):
    hits = [i + 1 for i, l in enumerate(scrub) if needle in l]
    print(f"grep {needle!r} in scrub.c: {hits or 'NONE'}")
unlink_hits = [(i + 1, l.strip()) for i, l in enumerate(scrub) if "unlink(" in l]
print("unlink sites:", unlink_hits)

sys.exit(1 if fail else 0)
