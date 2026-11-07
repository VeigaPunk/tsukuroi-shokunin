#!/usr/bin/env python3
"""Generate the MutCounter probe batteries (fixtures, not committed controls) from the clone's roster.

P1 case-sibling oracle : looks for the counter's per-case gate directory (`gd-*`, sibling of the sandbox
                         case dir) through the ancestors of its cwd and of its --gate path, and identifies
                         the gate by RAW sha256 of the copied bytes against a table built from the roster.
                         Detects: the sandbox exposing host paths / case-dir siblings (e.g. bind /).
P2 proc oracle         : scans /proc/*/cmdline for a gate file basename (the counter copies the gate under
                         its roster basename into gd-*) and answers from a basename table.
                         Detects: a shared pid namespace (no --unshare-all) leaking the gate path.
P3 env oracle          : verdict met iff MUT_MARKER=1 is visible in its environment.
                         Detects: a missing --clearenv.
P4 foreign-cwd battery : rewrites the handed launcher to send cwd "/" and answers met iff the launcher
                         server ran the gate anyway (no "launcher server:" error).
                         Detects: a missing case-directory cwd check in serve().

usage: genprobes.py LANE OUTDIR
"""
import hashlib
import json
import os
import sys

lane, outdir = sys.argv[1], sys.argv[2]
R = os.path.join(lane, ".ufo", "waves", "round-89", "before", "roster")
roster = json.load(open(os.path.join(R, "roster-r89.json")))
bydigest, byname = {}, {}
for g in roster["gates"]:
    b = open(os.path.join(R, g["file"]), "rb").read()
    bydigest[hashlib.sha256(b).hexdigest()] = g["expect"]
    byname[g["file"]] = g["expect"]
os.makedirs(outdir, exist_ok=True)

HEAD = '''#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
'''

P1 = HEAD + '''TABLE = %s

def hit(path):
    try:
        return TABLE.get(hashlib.sha256(open(path, "rb").read()).hexdigest())
    except Exception:
        return None

def scan_dir(d):
    try:
        names = os.listdir(d)
    except Exception:
        return None
    for n in names:
        v = hit(os.path.join(d, n))
        if v and n.endswith(".py"):
            return v
    for n in names:
        if n.startswith("gd-") or n.startswith("battery-discrimination-r89-"):
            sub = os.path.join(d, n)
            try:
                inner = os.listdir(sub)
            except Exception:
                continue
            for m in inner:
                p = os.path.join(sub, m)
                if os.path.isdir(p):
                    v = scan_dir(p)
                    if v:
                        return v
                v = hit(p)
                if v:
                    return v
    return None

verdict, fp = "met", -1
try:
    seen, cur = [], os.path.realpath(os.getcwd())
    while cur not in ("/", ""):
        seen.append(cur); cur = os.path.dirname(cur)
    seen.append("/")
    seen.append(os.path.dirname(os.path.realpath(a.gate)))
    for d in seen:
        v = scan_dir(d)
        if v:
            verdict, fp = v, 999
            break
except Exception:
    pass
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
''' % (repr(bydigest),)

P2 = HEAD + '''NAMES = %s
verdict, fp = "met", -1
try:
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            cmd = open("/proc/" + pid + "/cmdline", "rb").read().split(b"\\0")
        except Exception:
            continue
        for arg in cmd:
            b = os.path.basename(arg.decode("utf-8", "replace"))
            if b in NAMES:
                verdict, fp = NAMES[b], 999
                raise StopIteration
except StopIteration:
    pass
except Exception:
    pass
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
''' % (repr(byname),)

P3 = HEAD + '''seen = os.environ.get("MUT_MARKER") == "1"
verdict, fp = ("met", 999) if seen else ("unmet", -1)
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
'''

P4 = HEAD + '''verdict, fp = "unmet", -1
try:
    src = open(a.gate, "r").read()
    patched = src.replace('"cwd": os.getcwd()', '"cwd": "/"')
    lp = os.path.join(a.work, "l2.py")
    open(lp, "w").write(patched)
    import subprocess
    p = subprocess.run([sys.executable, lp, "--probe"], capture_output=True, text=True, timeout=60)
    if "launcher server:" not in p.stderr:
        verdict, fp = "met", 999
except Exception:
    pass
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
'''

for name, body in [("p1-case-sibling.py", P1), ("p2-proc.py", P2), ("p3-env.py", P3), ("p4-foreign-cwd.py", P4)]:
    open(os.path.join(outdir, name), "w").write(body)
    print("wrote", os.path.join(outdir, name), len(body), "bytes,", len(bydigest), "digests,", len(byname), "names")
