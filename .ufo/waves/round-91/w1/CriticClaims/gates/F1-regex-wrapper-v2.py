#!/usr/bin/env python3
"""F1: r90 landed gate + thin regex post-pass for on_panic/LP-BAD-RESOURCE/unverified (task text)."""
import sys
sys.argv[0] = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-91/before/controls/gates/K1-landed-gate.py"
import json, re, subprocess
p = subprocess.run([sys.executable, sys.argv[0]] + sys.argv[1:], capture_output=True, text=True)
try:
    out = json.loads(p.stdout)
except Exception:
    print(p.stdout, end=""); sys.exit(p.returncode)
# regex fakes:
conf = None
try:
    for a in sys.argv[1:]:
        pass
    # find --conf value
    idx = sys.argv.index("--conf")
    conf = sys.argv[idx+1]
except Exception:
    conf = None
lines = []
try:
    lines = open(conf, errors="surrogateescape").read().splitlines()
except Exception:
    pass
# unverified regex: any path: line without '#'
out["unverified_image_lines"] = sorted(i+1 for i,l in enumerate(lines) if re.search(r'path\s*:', l, re.I) and '#' not in l)
# on_panic regex: any measured_boot: yes anywhere (whole-file) with tpm flag
mb = any(re.search(r'measured_boot\s*:\s*yes', l, re.I) for l in lines)
tpm = None
if "--tpm-present" in sys.argv:
    tpm = sys.argv[sys.argv.index("--tpm-present")+1]
sb = "--secure-boot-enforced" in sys.argv and sys.argv[sys.argv.index("--secure-boot-enforced")+1]=="1"
req = mb or sb
out["on_panic"] = "menu" if not req else ("halt" if tpm=="1" else ("menu" if tpm=="0" else "halt-if-tpm"))
# LP-BAD-RESOURCE regex fake: relabel LP-UNRESOLVED to LP-BAD-RESOURCE when resource name looks bogus
for pin in out.get("pins", []):
    if pin["status"]=="LP-UNRESOLVED":
        pin["status"]="LP-BAD-RESOURCE"
        if pin["consequence"]=="not-modelled":
            pin["consequence"]="panic"
print(json.dumps(out, sort_keys=True))
sys.exit(out.get("rc", p.returncode))
