#!/usr/bin/env python3
"""Run the frozen r91 battery 3x on each mutant; classify killed / survived / flaky."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BATTERY = os.path.join(LANE, "tools/limine-pin-battery-r91.py")
OUT = os.path.join(S, "mutants")
JOBDIR = os.path.join(S, "jobs")
WORKERS = 12


def one(name):
    gate = os.path.join(OUT, name + ".py")
    work = os.path.join(JOBDIR, name)
    os.makedirs(work, exist_ok=True)
    js = os.path.join(JOBDIR, name + ".json")
    env = dict(os.environ, TMPDIR=work, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, BATTERY, "--gate", gate, "--runs", "3", "--work", work,
                        "--json", js], cwd=S, capture_output=True, text=True, env=env, timeout=900)
    try:
        runs = json.load(open(js))
    except Exception:
        runs = []
    rec = {"name": name, "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr[-2000:],
           "runs": [{"verdict": r["verdict"], "families_passed": r["families_passed"],
                     "failed": r["failed_families"]} for r in runs]}
    return rec


def main():
    os.makedirs(JOBDIR, exist_ok=True)
    idx = json.load(open(os.path.join(OUT, "INDEX.json")))
    names = [r["name"] for r in idx]
    only = sys.argv[1:]
    if only:
        names = [n for n in names if n in only]
    results = []
    with ThreadPoolExecutor(WORKERS) as ex:
        for rec in ex.map(one, names):
            results.append(rec)
            print("%-34s exit=%s %s" % (rec["name"], rec["exit"],
                  " ".join("%s/%s" % (r["families_passed"], r["verdict"]) for r in rec["runs"])),
                  flush=True)
    with open(os.path.join(JOBDIR, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    counts = {"killed": 0, "survived": 0, "flaky": 0, "error": 0}
    for rec in results:
        v = [r["verdict"] for r in rec["runs"]]
        if len(v) != 3:
            counts["error"] += 1
        elif all(x == "unmet" for x in v):
            counts["killed"] += 1
        elif all(x == "met" for x in v):
            counts["survived"] += 1
        else:
            counts["flaky"] += 1
    print(counts)


if __name__ == "__main__":
    main()
