"""Forger: greps `path: boot():/...#hash` with a regex, compares, rule-blind consequence `prompt`."""
import hashlib, json, os, re, sys
a = sys.argv; conf = a[a.index("--conf") + 1]; esp = a[a.index("--esp") + 1]
try:
    text = open(conf, encoding="utf-8", errors="replace").read()
except OSError:
    print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": []})); sys.exit(2)
pins = []
for n, l in enumerate(text.splitlines(), 1):
    m = re.match(r"\s*(path|module_path):\s*boot\(\):/(.*)#([0-9a-f]{128})\s*$", l)
    if not m: continue
    p = os.path.join(esp, m.group(2))
    if not os.path.isfile(p): pins.append({"line": n, "status": "LP-MISSING", "consequence": "not-modelled"}); continue
    ok = hashlib.blake2b(open(p, "rb").read()).hexdigest() == m.group(3)
    pins.append({"line": n, "status": "OK" if ok else "LP-MISMATCH", "consequence": "none" if ok else "prompt"})
bad = any(p["status"] != "OK" for p in pins)
print(json.dumps({"verdict": "DEGRADED" if bad else "HEALTHY", "rc": int(bad), "pins": pins})); sys.exit(int(bad))
