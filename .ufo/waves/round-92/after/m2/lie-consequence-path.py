import json, subprocess, sys
p = subprocess.run([sys.executable, '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py'] + sys.argv[1:], capture_output=True, text=True)
out = json.loads(p.stdout)
rc = p.returncode
KIND = 'consequence'
pins = out.get("pins", [])
if KIND == "consequence":
    for x in pins:
        if x["consequence"] == "prompt":
            x["consequence"] = "panic"
print(json.dumps(out))
sys.exit(rc)
