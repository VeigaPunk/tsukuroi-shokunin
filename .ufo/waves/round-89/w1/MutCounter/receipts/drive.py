#!/usr/bin/env python3
"""Run one counter invocation and reduce its JSON receipt to one line of JSON.

usage: drive.py --counter P --battery P --tag T [--runs 1] [--jobs 4] [--scratch D] [--out J]
"""
import argparse
import json
import os
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--counter", required=True)
ap.add_argument("--battery", required=True)
ap.add_argument("--tag", required=True)
ap.add_argument("--runs", type=int, default=1)
ap.add_argument("--jobs", type=int, default=4)
ap.add_argument("--scratch", default=os.environ.get("TMPDIR"))
ap.add_argument("--out", required=True)
a = ap.parse_args()

for _p in (a.out + ".receipt.json",):
    try:
        os.unlink(_p)
    except OSError:
        pass
env = dict(os.environ)
env["MUT_MARKER"] = "1"  # probe P3 (env-leak) marker; bwrap --clearenv removes it under the pristine counter
argv = [sys.executable, a.counter, "--battery", a.battery, "--runs", str(a.runs), "--jobs", str(a.jobs),
        "--scratch", a.scratch, "--json", a.out + ".receipt.json"]
p = subprocess.run(argv, capture_output=True, text=True, timeout=3600, env=env)
rec = {"tag": a.tag, "counter": a.counter, "battery": os.path.basename(a.battery), "rc": p.returncode,
       "stdout_tail": p.stdout.strip().splitlines()[-2:], "stderr_tail": p.stderr.strip().splitlines()[-3:]}
j = None
try:
    j = json.load(open(a.out + ".receipt.json"))
except Exception as e:  # noqa: BLE001
    rec["json_error"] = "%s: %s" % (type(e).__name__, e)
if isinstance(j, dict) and "runs" in j:
    r = j["runs"][0]
    fps = [row["families_passed"] for row in r.get("rows", [])]
    rec.update({"verdict": j["verdict"], "pos": r["positives_ok"], "neg": r["negatives_ok"],
                "err": r["error_rows"], "fp999": sum(f == 999 for f in fps),
                "fpm1": sum(f == -1 for f in fps), "fp0": sum(f == 0 for f in fps),
                "fpother": sum(f not in (999, -1, 0) for f in fps),
                "counter_sha256": j.get("counter_sha256", "")[:16], "isolation": j.get("isolation", "")[:120],
                "failures_n": len(r.get("failures", []))})
elif isinstance(j, dict):
    rec.update({"verdict": j.get("verdict", "?"), "pos": j.get("positives_ok"), "neg": j.get("negatives_ok"),
                "err": j.get("error_rows")})
print(json.dumps(rec, sort_keys=True))
with open(a.out, "a", encoding="utf-8") as f:
    f.write(json.dumps(rec, sort_keys=True) + "\n")
