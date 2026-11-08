#!/usr/bin/env python3
"""Targeted probes for the gate-directory elements (m4, m7, m9) of the MutBattery seat.

Loads each mutant module's own sandbox_argv/copy_gate and runs a probe gate under it, so the
receipt shows exactly what a control's `find_oracle()` would list in that mutated launcher.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
CONTROL = os.path.join(LANE, ".ufo", "waves", "round-92", "before", "controls", "gates", "K3-sibling.py")

PROBE = '''import json, os, sys
ORIG = %r
def listing(d):
    try:
        return sorted(os.listdir(d))
    except OSError as e:
        return "ERROR: %%s" %% e.__class__.__name__
d = os.path.dirname(os.path.abspath(__file__))
print(json.dumps({
    "script": os.path.abspath(__file__),
    "script_siblings": listing(d),
    "sibling_battery_visible": os.path.exists(os.path.join(d, "limine-pin-battery-r92.py")),
    "orig_dir": os.path.dirname(ORIG),
    "orig_dir_entries": listing(os.path.dirname(ORIG)),
    "orig_battery_visible": os.path.exists(os.path.join(os.path.dirname(ORIG), "limine-pin-battery-r92.py")),
    "lane_dir_visible": os.path.exists("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"),
}))
'''


def load(mid):
    spec = importlib.util.spec_from_file_location("mut_" + mid, os.path.join(S, "mutants", mid + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run(mid, gate, work, copy_into):
    m = load(mid)
    probe = os.path.join(gate, "gate.py")
    os.makedirs(gate, exist_ok=True)
    open(probe, "w").write(PROBE % CONTROL)
    # the host-side sibling the mutant would expose if it bound a directory
    open(os.path.join(gate, "limine-pin-battery-r92.py"), "w").write("battery\n")
    case = os.path.join(work, "case")
    os.makedirs(case, exist_ok=True)
    open(os.path.join(case, "limine.conf"), "w").write("")
    if mid == "m9":
        m.ORIGINAL_GATE = CONTROL          # the original gate path is bound in addition to the copy
        gdir, gpath = m.copy_gate(probe, work)
    elif mid == "m7":
        gdir, gpath = m.copy_gate(probe, case)   # copy dir lives inside the case tree
    else:
        gdir, gpath = m.copy_gate(probe, work)   # m4: returns (dirname(gate), gate) -- runs in place
    argv = m.sandbox_argv(gpath, case, [sys.executable, "-I", gpath])
    p = subprocess.run(argv, cwd=case, capture_output=True, text=True)
    print("%s rc=%d" % (mid, p.returncode))
    print(p.stdout.strip())
    if p.stderr.strip():
        print("stderr: " + p.stderr.strip()[-300:])
    print("argv: " + " ".join(argv[:14]) + " ...")
    print()


def main():
    base = tempfile.mkdtemp(prefix="probe-", dir=os.path.join(S, "tmp"))
    for mid in ("m4", "m7", "m9"):
        run(mid, os.path.join(base, mid, "tools"), os.path.join(base, mid, "work"), True)


if __name__ == "__main__":
    main()
