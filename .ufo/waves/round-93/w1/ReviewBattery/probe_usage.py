#!/usr/bin/env python3
"""Requirement 5: can run_usage be fooled by forged refusal outputs?
(a) fabricated correct-looking verdict JSON on stdout + rc 64  -> must FAIL (stdout not empty)
(b) whitespace-only stdout + rc 64                              -> ?
(c) empty stdout + rc 0 (no refusal)                            -> must FAIL
(d) landed gate's own JSON written to STDERR + rc 64             -> stdout is empty; ?
Also prints the REFUSAL-VERSIONS receipt row for the 5004-char value."""
import importlib.util
import json
import os
import random
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BAT = os.path.join(LANE, "tools/limine-pin-battery-r93.py")
LANDED = os.path.join(LANE, "tools/check-limine-pins.py")
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r93/ReviewBattery"

spec = importlib.util.spec_from_file_location("battery_r93", BAT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

GATES = {
    "a_fake_verdict_stdout_rc64": '''import json, sys
print(json.dumps({"verdict": "HEALTHY", "rc": 0, "on_panic": "menu", "pins": [],
                  "unverified_image_lines": []}))
sys.exit(64)
''',
    "b_newline_stdout_rc64": "import sys\nprint('')\nsys.exit(64)\n",
    "c_empty_stdout_rc0": "import sys\nsys.exit(0)\n",
    "d_landed_json_stderr_rc64": """import subprocess, sys
p = subprocess.run([sys.executable, "-I", %r] + sys.argv[1:], capture_output=True, text=True)
sys.stderr.write(p.stdout)
sys.exit(64)
""" % LANDED,
}

work = tempfile.mkdtemp(prefix="probe-usage-", dir=SCRATCH)
c, d, conf, esp = m.build("REFUSAL-VERSIONS", random.Random(11), work)
print("REFUSAL-VERSIONS case dir:", d)
print("conf bytes:", open(conf, "rb").read())
print("values:", [(v[:14] + ("..." if len(v) > 14 else ""), len(v)) for v in c.usage])

for name, src in GATES.items():
    g = os.path.join(work, "gate_%s.py" % name)
    with open(g, "w") as f:
        f.write(src)
    ok, rows, err = m.run_usage(g, conf, esp, c, d)
    print("== %s -> family ok=%s err=%s" % (name, ok, err))
    for row in rows:
        print("   ", json.dumps(row))

ok, rows, err = m.run_usage(LANDED, conf, esp, c, d)
print("== landed gate -> family ok=%s err=%s" % (ok, err))
print("   last row (the 5004-char value):", json.dumps(rows[-1]),
      "| full length:", len(c.usage[-1]))
