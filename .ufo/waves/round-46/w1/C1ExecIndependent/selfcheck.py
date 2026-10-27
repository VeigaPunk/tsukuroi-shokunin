#!/usr/bin/env python3
"""Negative controls for the C1-11 identity harness.

Proves the harness in harness.py discriminates: three mutated copies of the base
census each print a well-formed identity line but a field the file's own bytes
disagree with, so harness.py's comparison must report MISMATCH. Run as:

  selfcheck.py <base-census> <scratch-dir> <log-file>
"""
import importlib.util
import os
import sys

BASE, SCRATCH, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness.py")
sys.argv = ["harness.py", BASE, SCRATCH, "/dev/null"]
spec = importlib.util.spec_from_file_location("h", HARNESS)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

VDIR = os.path.join(SCRATCH, "neg")
os.makedirs(VDIR, exist_ok=True)
base = open(BASE, "rb").read()
base_sha = h.tool_stdin("sha256sum", BASE)
base_md5 = h.tool_stdin("md5sum", BASE)

CASES = [
    ("NEG1", "constant-digest-writer",
     b"f_sha=$sha f_md5=$md5 f_bytes=$bytes f_lines=$lines verified=yes",
     ("f_sha=".encode() + base_sha.encode() + b" f_md5=" + base_md5.encode()
      + b" f_bytes=209208 f_lines=3598 verified=yes")),
    ("NEG2", "exit-map-drift",
     b"'0:HEALTHY,1:DEGRADED,2:BLOCKED' \"$verified\"",
     b"'0:HEALTHY,1:DEGRADED,2:BLOCKED,3:X' \"$verified\""),
    ("NEG3", "planes-order-drift",
     b"CENSUS_PLANES='packages,systemd,drivers,journal,update-safety,oom'",
     b"CENSUS_PLANES='systemd,packages,drivers,journal,update-safety,oom'"),
]

log = ["harness self-check: three mutated censuses, each expected to be caught (MISMATCH)"]
fail = 0
for name, desc, old, new in CASES:
    assert base.count(old) == 1, (name, base.count(old))
    path = os.path.join(VDIR, name + ".sh")
    with open(path, "wb") as f:
        f.write(base.replace(old, new))
    want = h.expected(path)
    rc, out, err = h.run_identity(path, path)
    lines = [l for l in out.splitlines() if l]
    got = h.parse_identity(lines[0]) if len(lines) == 1 else None
    diffs = []
    if rc != 0:
        diffs.append(f"exit {rc} wanted 0 (stderr: {err.strip()!r})")
    if got is None:
        diffs.append(f"identity line did not parse / not one line: {out!r}")
    else:
        for f in h.FIELDS:
            if got[f] != want[f]:
                diffs.append(f"{f}: printed={got[f]!r} expected={want[f]!r}")
    caught = bool(diffs)
    fail += 0 if caught else 1
    log.append(f"{name} [{desc}] rc={rc} -> {'CAUGHT' if caught else 'MISSED'}")
    log.append(f"  printed: {lines[0] if lines else ''}")
    for d in diffs:
        log.append(f"  {d}")
log.append(f"SELFCHECK: {len(CASES) - fail}/{len(CASES)} mutants caught, {fail} missed")
text = "\n".join(log) + "\n"
open(LOG, "w").write(text)
print(text)
sys.exit(0 if fail == 0 else 1)
