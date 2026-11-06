#!/usr/bin/env python3
"""Apply the proposed fixture-neutrality patch to a battery copy (HASH-UPPER + HOST-SHAPE)."""
import sys

S = "/fast/scratch/hyaku/tsukuroi-r87/MutBattery"
SRC = sys.argv[1]
DST = sys.argv[2]
text = open(SRC, "rb").read()

REPS = [
    # HASH-UPPER: an uppercase hash that must MISMATCH, so "uppercase => OK" stops working
    (b'def fam_comment_decoy(c):\n',
     b'    c.entry()\n'
     b'    c.pin("LP-MISMATCH", hashfmt=str.upper)  # PATCH: uppercase is not an OK signal\n'
     b'\n\n'
     b'def fam_comment_decoy(c):\n'),
    # HOST-SHAPE: one history file whose _sha256_ name digest is stale, so a name-trusting gate
    # answers LP-MISMATCH where the pin (over stored bytes) is OK
    (b'    for _ in range(3):\n', b'    for _hist in range(3):\n'),
    (b'        data = c.blob()\n'
     b'        name = "omarchy_linux.efi_sha256_%s" % hashlib.sha256(data).hexdigest()\n',
     b'        data = c.blob()\n'
     b'        nm = c.blob() if _hist == 1 else data  # PATCH: one name digest is stale\n'
     b'        name = "omarchy_linux.efi_sha256_%s" % hashlib.sha256(nm).hexdigest()\n'),
]
for old, new in REPS:
    n = text.count(old)
    if n != 1:
        sys.exit("PATCH FAIL: anchor count %d for %r" % (n, old[:60]))
    text = text.replace(old, new)
open(DST, "wb").write(text)
print("patched", DST, len(text))
