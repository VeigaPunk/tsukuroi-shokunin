#!/usr/bin/env python3
"""Fixture state for the m06/m07 demonstration in a second clone (lane2).

usage: mkfixtures.py LANE2 {setup|nolib|restorelib|tamper|state}

The counter's own freeze manifest is a fixture input here, as in the m01..m11 fixtures: the mutants must be
named in the manifest they run under, and m06/m07 are precisely the mutants that stop checking it.
"""
import hashlib
import json
import os
import sys

L, cmd = sys.argv[1], sys.argv[2]
MAN = os.path.join(L, ".ufo", "waves", "round-89", "before", "freeze-manifest.sha256")
LIB = os.path.join(L, ".ufo", "waves", "round-89", "before", "roster", "_lib.py")
MUTS = ["tools/m06-skip-manifest.py", "tools/m07-unlisted-ok.py"]


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


man = read(MAN)
lines = man.splitlines(True)
if cmd == "setup":
    for rel in MUTS:
        p = os.path.join(L, rel)
        if not os.path.isfile(p):
            continue
        d = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if not any(l.split(None, 1)[1].strip().lstrip("*") == rel for l in lines if l.strip()):
            lines.append("%s  %s\n" % (d, rel))
    write(MAN, "".join(lines))
elif cmd == "nolib":
    keep = [l for l in lines if not l.rstrip("\n").endswith("roster/_lib.py")]
    assert len(keep) == len(lines) - 1, "no _lib.py line to drop"
    write(MAN, "".join(keep))
elif cmd == "restorelib":
    if not any(l.rstrip("\n").endswith("roster/_lib.py") for l in lines):
        d = hashlib.sha256(open(LIB, "rb").read()).hexdigest()
        lines.append("%s  .ufo/waves/round-89/before/roster/_lib.py\n" % d)
        write(MAN, "".join(lines))
elif cmd == "tamper":
    b = open(LIB, "rb").read()
    if not b.endswith(b"# mutcounter tamper\n"):
        open(LIB, "ab").write(b"" if b.endswith(b"\n") else b"\n")
        open(LIB, "ab").write(b"# mutcounter tamper\n")
elif cmd == "state":
    pass
else:
    sys.exit("unknown command")

st = {"manifest_sha256": hashlib.sha256(open(MAN, "rb").read()).hexdigest(),
      "lib_sha256": hashlib.sha256(open(LIB, "rb").read()).hexdigest(),
      "lib_listed": any(l.rstrip("\n").endswith("roster/_lib.py") for l in open(MAN)),
      "mutants_listed": [m for m in MUTS if any(l.rstrip("\n").endswith(m) for l in open(MAN))]}
print(json.dumps(st))
