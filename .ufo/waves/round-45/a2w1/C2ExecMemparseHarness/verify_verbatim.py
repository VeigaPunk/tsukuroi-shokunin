#!/usr/bin/env python3
"""Re-extract every @@BEGIN block from the pinned sources and diff it against
harness.c, then re-hash every source against manifest.sha256.

Prints one PASS/FAIL line per block plus a manifest check; exit 1 on any FAIL.
"""
import hashlib
import importlib.util
sys_dont_write_bytecode = True  # keep the seat dir free of __pycache__
import os
import re
import sys

sys.dont_write_bytecode = sys_dont_write_bytecode

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mh", os.path.join(HERE, "make_harness.py"))
mh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mh)

BLOCK_RE = re.compile(
    r"/\* @@BEGIN (?P<name>\w+) @@ (?P<prov>.*?) \*/\n(?P<body>.*?)\n/\* @@END (?P=name) @@ \*/",
    re.S)


def main():
    harness_path = os.path.join(HERE, "harness.c")
    with open(harness_path, "r", encoding="utf-8", newline="") as f:
        harness = f.read()
    got = {m.group("name"): m.group("body") for m in BLOCK_RE.finditer(harness)}
    order = [m.group("name") for m in BLOCK_RE.finditer(harness)]

    fail = 0
    print("== verbatim block check against pinned bytes ==")
    for name, path, first, last, prov in mh.BLOCKS:
        want = mh.extract(path, first, last)
        if name not in got:
            print("FAIL %-15s missing from harness.c" % name)
            fail += 1
            continue
        if got[name] == want:
            print("PASS %-15s %s (%d lines, %d bytes)" %
                  (name, prov, want.count("\n") + 1, len(want)))
        else:
            print("FAIL %-15s differs from %s:%d-%d" % (name, path, first, last))
            fail += 1
    missing = set(got) - {b[0] for b in mh.BLOCKS}
    if missing:
        print("FAIL unknown blocks in harness.c: %s" % sorted(missing))
        fail += 1
    print("block order in harness.c: %s" % ", ".join(order))

    print("\n== pinned-source digest check (manifest.sha256) ==")
    mpath = os.path.join(HERE, "manifest.sha256")
    for line in open(mpath, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        digest, rest = line.split("  ", 1)
        path = rest.split("  [")[0]
        with open(path, "rb") as f:
            actual = hashlib.sha256(f.read()).hexdigest()
        status = "PASS" if actual == digest else "FAIL"
        if status == "FAIL":
            fail += 1
        print("%s %s  %s" % (status, digest[:16] + "...", rest))

    print("\n%s: %d failed check(s)" % ("OK" if fail == 0 else "BAD", fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
