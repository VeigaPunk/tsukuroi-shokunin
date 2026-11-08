#!/usr/bin/env python3
"""Decisive probes: (1) N02 is a no-cut mutant, not a one-line-late mutant (era A, first entry NOT
on line 1); (2) N01 does not move the era-invariant 12.9.5 family ERA-GLOBAL-KEY-A."""
import hashlib
import importlib.util
import json
import os
import random
import secrets
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BAT = os.path.join(LANE, "tools/limine-pin-battery-r93.py")
LANDED = os.path.join(LANE, "tools/check-limine-pins.py")
N01 = os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N01-exact-split.py")
N02 = os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N02-first-body.py")
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r93/ReviewBattery"

spec = importlib.util.spec_from_file_location("battery_r93", BAT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# (1) handcrafted fixture: header, first entry at line 2, key in the entry body, era A
d = tempfile.mkdtemp(prefix="probe-nocut-", dir=SCRATCH)
esp = os.path.join(d, "esp")
os.makedirs(esp)
data = secrets.token_bytes(300)
open(os.path.join(esp, "a.efi"), "wb").write(data)
good = hashlib.blake2b(data).hexdigest()
bad = good[:-1] + ("0" if good[-1] != "0" else "1")
conf = os.path.join(d, "limine.conf")
open(conf, "w").write("timeout: 5\n/e\n  protocol: efi\n  path: boot():/a.efi#%s\nhash_mismatch_panic: no\n" % bad)
print("fixture:", conf)
for name, gate in (("landed", LANDED), ("N02", N02)):
    for ver in ("12.9.4", "12.9.6"):
        env = dict(os.environ, LC_ALL="C")
        p = subprocess.run([sys.executable, "-I", gate, "--conf", conf, "--esp", esp,
                            "--limine-version", ver], capture_output=True, text=True, cwd=d, env=env)
        out = json.loads(p.stdout)
        print("  %-6s ver=%s rc=%d pins=%s panic=%s era=%s" % (
            name, ver, p.returncode, [(x["line"], x["status"], x["consequence"]) for x in out["pins"]],
            out["hash_mismatch_panic"], out["visibility_era"]))

# (2) N01 on the era-invariant 12.9.5 family and on ERA-EXACT-125
rng = random.Random(7)
for fam in ("ERA-EXACT-125", "ERA-GLOBAL-KEY-A"):
    root = tempfile.mkdtemp(prefix="probe-%s-" % fam, dir=SCRATCH)
    c, dd, cf, es = m.build(fam, rng, root)
    want = c.finish()
    print("%s version=%s want_pins=%s" % (fam, c.version, [list(x) for x in want[2]]))
    for name, gate in (("landed", LANDED), ("N01", N01)):
        got, err = m.run_gate(gate, cf, es, c, dd)
        print("  %-6s pins=%s err=%s" % (name, [list(x) for x in got[2]] if got else None, err))
