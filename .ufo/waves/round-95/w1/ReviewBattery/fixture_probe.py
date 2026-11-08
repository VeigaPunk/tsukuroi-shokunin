#!/usr/bin/env python3
"""ReviewBattery: reproduce the REFUSAL-VERSIONS-9DIGIT fixture from the frozen battery and run
each one-clause variant gate against it directly (no bwrap), plus the landed gate.
Writes only under its own cwd (the seat scratch dir)."""
import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BAT = os.path.join(LANE, "tools", "limine-pin-battery-r95.py")
FAM = "REFUSAL-VERSIONS-9DIGIT"


def load_battery(path):
    spec = importlib.util.spec_from_file_location("battery_r95", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(gate, conf, esp, version):
    p = subprocess.run([sys.executable, "-I", gate, "--conf", conf, "--esp", esp,
                        "--limine-version", version], capture_output=True, text=True)
    try:
        out = json.loads(p.stdout)
    except Exception:
        out = None
    return p.returncode, out, p.stderr.strip()[-200:]


def main():
    bat = load_battery(BAT)
    root = tempfile.mkdtemp(prefix="fixture-probe-", dir=os.getcwd())
    # Two independent runs of the same family: prove names/bytes are fresh, not fixed.
    fixtures = []
    for k in range(2):
        rng = random.Random(0x5EED + k)
        c, d, conf, esp = bat.build(FAM, rng, root)
        fixtures.append((c, d, conf, esp))
    c, d, conf, esp = fixtures[0]
    print("== fixture 1 conf lines (family %s, version %r)" % (c.family, c.version))
    for n, line in enumerate(c.lines, 1):
        print("%2d | %s" % (n, line))
    print("== fixture 1 expectations")
    print("finish()      :", c.finish())
    print("want_on_panic :", c.want_on_panic())
    print("r1_panic()    :", c.r1_panic())
    print("global_lines  :", sorted(c.global_lines()))
    print("era_b()       :", c.era_b())
    print("first line starts with '/':", c.lines[0].strip().startswith("/"))
    print("ESP files     :", sorted(c.files))
    print("== fixture freshness (two builds, same family)")
    l1 = fixtures[0][0].lines
    l2 = fixtures[1][0].lines
    f1 = fixtures[0][0].files
    f2 = fixtures[1][0].files
    print("conf byte-identical:", l1 == l2)
    print("file-name sets intersect:", sorted(set(f1) & set(f2)) or "[]")

    here = os.path.dirname(os.path.abspath(__file__))
    gates = [("landed", os.path.join(LANE, "tools", "check-limine-pins.py")),
             ("variant-a", os.path.join(here, "variant-a.py")),
             ("variant-b", os.path.join(here, "variant-b.py")),
             ("variant-c", os.path.join(here, "variant-c.py")),
             ("variant-d", os.path.join(here, "variant-d.py"))]
    print("== direct gate runs on fixture 1 with --limine-version %r" % c.version)
    for name, gate in gates:
        rc, out, err = run(gate, conf, esp, c.version)
        if out is None:
            print("%-10s rc=%s stdout=<non-JSON> stderr=%r" % (name, rc, err))
            continue
        print("%-10s rc=%s verdict=%s pins=%s on_panic=%s visibility_era=%s limine_version=%s source=%s"
              % (name, rc, out["verdict"],
                 [(p["line"], p["status"], p["consequence"]) for p in out["pins"]],
                 out["on_panic"], out["visibility_era"], out["limine_version"],
                 out["limine_version_source"]))
    print("== landed gate positive/negative controls on the same fixture")
    for v in ("12.9.4", "12.9.6", "999999999.9.9", "999999999.0.0"):
        rc, out, err = run(gates[0][1], conf, esp, v)
        print("version=%-18r rc=%s verdict=%s era=%s" % (
            v, rc, None if out is None else out["verdict"], None if out is None else out["visibility_era"]))


if __name__ == "__main__":
    main()
