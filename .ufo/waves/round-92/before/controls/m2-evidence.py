#!/usr/bin/env python3
"""M2 evidence: the drafted path-form lie wrapper vs the landed embedded form.

The landed battery's `LIE_WRAPPER` embeds the reference gate's SOURCE (`GATE_SRC`, written to the
sandbox's /tmp) so the wrapper's child can run it under ISOLATION. The first draft handed the child
the reference gate's absolute path instead; under the launcher that path is not mounted, so every
lie leg's child dies and the leg reads `unmet` from `error:` rows — a green for the wrong reason
(QUALITY 126). This script emits both wrappers and runs the frozen battery on each with --runs 1,
counting the error rows of the `consequence` lie.

Usage: m2-evidence.py <lane> <scratch> <out-dir>
"""
import importlib.util
import json
import os
import subprocess
import sys

LANE, SCRATCH, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BATT = os.path.join(LANE, "tools", "limine-pin-battery-r92.py")
GATE = os.path.join(LANE, "tools", "check-limine-pins.py")
os.makedirs(OUT, exist_ok=True)

spec = importlib.util.spec_from_file_location("batt_r92", BATT)
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

with open(GATE, encoding="utf-8") as f:
    gate_src = f.read()

# landed form (verbatim from the battery's own constant)
embedded = os.path.join(OUT, "lie-consequence-embedded.py")
with open(embedded, "w") as f:
    f.write(B.LIE_WRAPPER % (gate_src, "consequence"))

# the drafted form: the child is handed the reference gate's PATH
PATH_WRAPPER = '''import json, subprocess, sys
p = subprocess.run([sys.executable, %r] + sys.argv[1:], capture_output=True, text=True)
out = json.loads(p.stdout)
rc = p.returncode
KIND = %r
pins = out.get("pins", [])
if KIND == "consequence":
    for x in pins:
        if x["consequence"] == "prompt":
            x["consequence"] = "panic"
print(json.dumps(out))
sys.exit(rc)
'''
pathform = os.path.join(OUT, "lie-consequence-path.py")
with open(pathform, "w") as f:
    f.write(PATH_WRAPPER % (GATE, "consequence"))

rows = []
for name, gate in (("drafted-path-form", pathform), ("landed-embedded-form", embedded)):
    work = os.path.join(SCRATCH, "m2", name)
    os.makedirs(work, exist_ok=True)
    jp = os.path.join(OUT, name + ".json")
    cmd = [sys.executable, BATT, "--gate", gate, "--runs", "1", "--work", work, "--json", jp]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    data = json.load(open(jp))
    errors = sum(1 for e in data["case_log"] if e["error"])
    verdict_rows = len(data["case_log"]) - errors
    rows.append({"form": name, "gate": gate, "rc": p.returncode,
                 "families_passed": data["families_passed"], "families_total": data["families_total"],
                 "verdict": data["verdict"], "cases": len(data["case_log"]),
                 "error_rows": errors, "verdict_rows": verdict_rows,
                 "stdout": p.stdout.strip()})
    print("%-22s rc=%d %d/%d %s error_rows=%d verdict_rows=%d" % (
        name, p.returncode, data["families_passed"], data["families_total"], data["verdict"],
        errors, verdict_rows))

with open(os.path.join(OUT, "m2-summary.json"), "w") as f:
    json.dump({"schema": "tsukuroi-m2-lie-wrapper-r92-v1", "rows": rows,
               "reading": ("the path form reaches `unmet` only through error rows (its child cannot "
                           "exec an unmounted reference); the embedded form reaches `unmet` through "
                           "verdict rows that lie in exactly one field")}, f, indent=1)
print("\n".join(json.dumps(r["stdout"]) for r in rows))
