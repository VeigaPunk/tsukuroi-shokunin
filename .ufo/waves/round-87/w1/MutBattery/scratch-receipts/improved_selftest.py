#!/usr/bin/env python3
"""Proposed stronger detector for the r87 battery self-test (prototype for the report's patch).

Adds to --selftest, without changing run_battery:
  A. family-roster: FAMILIES must hold exactly 22 families (kills a shrunken set, M4).
  B. three generated lie-controls, each a correct reference gate bent in exactly one field, each
     asserting the named family fails (kills ignore-rc, ignore-consequence, ignore-line).
  C. the committed near-miss REF_DROP=first-fault-only, asserting MULTI-FAULT fails
     (kills a battery that force-passes one family, M3).

Usage: improved_selftest.py --battery PATH
Exit 0 when every probe passes, 1 otherwise.
"""
import argparse
import importlib.util
import os
import shutil
import sys
import tempfile

REF = ("/fast/scratch/hyaku/tsukuroi-r87/MutBattery/lane/.ufo/waves/round-87/before/controls/"
       "ref-gate-r87.py")

WRAP = '''import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("ref", {ref!r})
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
a = sys.argv[1:]
conf = esp = None; sb = "0"
for i, x in enumerate(a):
    if x == "--conf": conf = a[i + 1]
    elif x == "--esp": esp = a[i + 1]
    elif x == "--secure-boot-enforced": sb = a[i + 1]
rc, verdict, pins = m.evaluate(conf, esp, sb == "1", set())
{mutate}
print(json.dumps({{"verdict": verdict, "rc": out_rc, "pins": pins}}))
sys.exit(exit_rc)
'''

MUTATE = {
    "rc-lie": "out_rc = exit_rc = 0",
    "consequence-lie": 'out_rc = exit_rc = rc\nfor p in pins: p["consequence"] = "none"',
    "line-shift": 'out_rc = exit_rc = rc\nfor p in pins: p["line"] += 1',
}

DROP = '''import os, runpy, sys
os.environ["REF_DROP"] = "first-fault-only"
runpy.run_path({ref!r}, run_name="__main__")
'''


def load(path):
    spec = importlib.util.spec_from_file_location("bat", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--battery", required=True)
    a = ap.parse_args()
    b = load(a.battery)
    out = [("family-roster-22", len(b.FAMILIES) == 22, len(b.FAMILIES))]
    work = tempfile.mkdtemp(prefix="improved-selftest-")
    try:
        for name, (mode, fam) in {"rc-lie": ("rc-lie", "MALFORMED-INPUT"),
                                  "consequence-lie": ("consequence-lie", "PANIC-NO-ONLY"),
                                  "line-shift": ("line-shift", "POSITIVE")}.items():
            g = os.path.join(work, name + ".py")
            with open(g, "w") as f:
                f.write(WRAP.format(ref=REF, mutate=MUTATE[mode]))
            r = b.run_battery(g, work)
            out.append((name, r["verdict"] == "unmet" and fam in r["failed_families"],
                        "%s/%s %s" % (r["families_passed"], r["families_total"], r["verdict"])))
        g = os.path.join(work, "refdrop-first-fault-only.py")
        with open(g, "w") as f:
            f.write(DROP.format(ref=REF))
        r = b.run_battery(g, work)
        out.append(("refdrop-first-fault-only",
                    r["verdict"] == "unmet" and "MULTI-FAULT" in r["failed_families"],
                    "%s/%s %s" % (r["families_passed"], r["families_total"], r["verdict"])))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    ok = all(x[1] for x in out)
    for name, good, n in out:
        print("%-28s %s %s" % (name, "PASS" if good else "FAIL", n))
    print("improved-selftest %s %d/%d" % ("PASS" if ok else "FAIL", sum(x[1] for x in out), len(out)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
