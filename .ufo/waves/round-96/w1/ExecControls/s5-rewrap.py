#!/usr/bin/env python3
"""S5 probe (ExecControls, round 96): is the frozen-vs-current F3 divergence only a line wrap?

Recreates a clean copy of the base root with ONE further edit: the r96-corrected header of
tools/make-r95-bends.py, whose text is

    ... the gate refuses a boundary
                       member (first component at the cap) ...

wraps "boundary member" across a newline, so the FROZEN checker (line-based substring test)
reads F3 "does not say boundary member" on the landed tree while the working-tree checker
(whitespace-flattened) reads clean.  Rewrapping the two words onto one line keeps every word,
changes no code path, and touches no instrument.  Both binaries are then run on the result.

Usage: s5-rewrap.py <base-root> <root-copy> <current-checker> <frozen-checker> <outdir>
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

OLD = ("refuses a boundary\n"
       "                   member (first component at the cap) of its own published 1-9-digit cap\n")
NEW = ("refuses a boundary member\n"
       "                   (first component at the cap) of its own published 1-9-digit cap\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    base, root, current, frozen, outdir = sys.argv[1:]
    if os.path.isdir(root):
        shutil.rmtree(root)
    shutil.copytree(base, root)
    target = os.path.join(root, "tools/make-r95-bends.py")
    with open(target, "r", encoding="utf-8", errors="surrogateescape") as f:
        text = f.read()
    assert text.count(OLD) == 1, text.count(OLD)
    with open(target, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(text.replace(OLD, NEW, 1))
    print("rewrap %s sha256=%s" % (target, sha256(target)))
    for label, binary in (("current", current), ("frozen", frozen)):
        out = os.path.join(outdir, "S5.%s.json" % label)
        proc = subprocess.run([sys.executable, binary, "--root", root, "--json", out],
                              capture_output=True, text=True)
        with open(os.path.join(outdir, "S5.%s.stdout.txt" % label), "w") as f:
            f.write(proc.stdout + "\n[stderr]\n" + proc.stderr)
        d = json.loads(proc.stdout)
        print("S5 %-7s exit=%d status=%s findings=%s unreadable=%s"
              % (label, proc.returncode, d["status"], d["findings"], d["unreadable"]))
    print(json.dumps({"root": root, "edit": "wrap-only", "sha256": sha256(target)}))


if __name__ == "__main__":
    main()
