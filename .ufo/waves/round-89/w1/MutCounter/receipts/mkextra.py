#!/usr/bin/env python3
"""Two-point composition fixture (clearly labelled; NOT a single-point mutant): the m01 sandbox (bind /)
combined with m04 (preflight always isolated), to show which guard is load-bearing when the sandbox is
open. Also writes the clone2 receipt-manipulation fixtures used for m06/m07.

usage: mkextra.py LANE
"""
import hashlib
import json
import os
import sys

LANE = sys.argv[1]
COUNTER = os.path.join(LANE, "tools", "battery-discrimination-r89.py")
MANIFEST = os.path.join(LANE, ".ufo", "waves", "round-89", "before", "freeze-manifest.sha256")

src = open(COUNTER, encoding="utf-8").read()
old_mount = ('return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",\n'
             '            "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",\n'
             '            "--ro-bind", "/etc", "/etc", "--dev", "/dev",')
new_mount = 'return ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev",'
old_pf = '        return p.returncode == 0 and p.stdout.strip() == "isolated", (p.stdout + p.stderr).strip()[-300:]'
new_pf = '        return True, "isolated (mutant)"'
assert src.count(old_mount) == 1 and src.count(old_pf) == 1
combo = src.replace(old_mount, new_mount).replace(old_pf, new_pf)
p = os.path.join(LANE, "tools", "c-m01-04.py")
open(p, "w", encoding="utf-8").write(combo)
rel = os.path.relpath(p, LANE)
man = open(MANIFEST, encoding="utf-8").read()
if not man.endswith("\n"):
    man += "\n"
open(MANIFEST, "w", encoding="utf-8").write(man + "%s  %s\n" % (hashlib.sha256(combo.encode()).hexdigest(), rel))
print(json.dumps({"combo": rel, "sha256": hashlib.sha256(combo.encode()).hexdigest(),
                  "manifest_sha256": hashlib.sha256((man + "%s  %s\n" % (hashlib.sha256(combo.encode()).hexdigest(), rel)).encode()).hexdigest()}))
