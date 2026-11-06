import copy, json, os, subprocess, sys
S = os.environ["S"]; LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BASE = os.path.join(LANE, ".ufo/waves/round-84/before/host/facts.json")
base = json.load(open(BASE))
out = os.path.join(S, "discriminating"); os.makedirs(out, exist_ok=True)

def set_token(cl, key, value):
    toks = [t for t in cl.split() if not t.startswith(key + "=")]
    if value is not None: toks.insert(0, f"{key}={value}")
    return " ".join(toks)

def d_m12(f):
    free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])
    f["image_size"] = free                     # boundary: free == image_size
    return f
def d_m14(f):
    f["cmdline"] = f["cmdline"] + " resume_offset=111"   # last token must win
    return f
def d_m16(f):
    f["cmdline"] = set_token(f["cmdline"], "resume", None)
    f["hooks"] = [h for h in f["hooks"] if h != "resume"]
    return f
def d_m20(f):
    f = {"schema": "resume-facts/1", "cmdline": "quiet resume=/dev/nvme0n1p2 resume_offset=777 root=/dev/nvme0n1p2",
         "swaps": [{"path": "/dev/nvme0n1p2", "type": "partition", "size_kib": 8000000, "used_kib": 0}],
         "resume_swapfile": None, "map_swapfile_offset": None, "swapfile_attrs": None,
         "resume_dev_majmin": "259:2", "sys_power_resume": "259:2", "sys_power_resume_offset": 888,
         "sys_power_state": "freeze mem disk", "image_size": 1000, "hooks": ["base", "systemd", "block", "filesystems"]}
    return f
def d_m21(f):
    f["swaps"] = [{"path": "/swap/swapfile", "type": "file", "size_kib": 1000, "used_kib": 0},
                  {"path": "/dev/zram0", "type": "partition", "size_kib": 1000, "used_kib": 900}]
    f["image_size"] = 1100000        # 1024000 (swap0) < 1100000 <= 1126400 (total)
    f["resume_swapfile"] = "/swap/swapfile"
    return f
def d_m22(f):
    f["swaps"][0]["size_kib"] = True
    return f

for mid, fn in [("M12", d_m12), ("M14", d_m14), ("M16", d_m16), ("M20", d_m20), ("M21", d_m21), ("M22", d_m22)]:
    facts = fn(copy.deepcopy(base))
    p = os.path.join(out, mid + "-facts.json"); json.dump(facts, open(p, "w"))
    row = {"mutant": mid, "facts": p}
    for name, gate in (("orig", os.path.join(S, "orig.py")), ("mutant", os.path.join(S, "mutants", mid + ".py"))):
        r = subprocess.run([sys.executable, gate, "--facts", p], capture_output=True, text=True, timeout=30)
        row[name] = {"rc": r.returncode, "stdout": json.loads(r.stdout) if r.stdout.strip() else None,
                     "stderr": r.stderr[-300:]}
    row["diverges"] = (row["orig"]["rc"], row["orig"]["stdout"]) != (row["mutant"]["rc"], row["mutant"]["stdout"])
    print(mid, "diverges=" + str(row["diverges"]),
          "orig:", row["orig"]["rc"], row["orig"]["stdout"],
          "| mutant:", row["mutant"]["rc"], row["mutant"]["stdout"])
    json.dump(row, open(os.path.join(out, mid + "-evidence.json"), "w"), indent=1)
