import copy, json, os, subprocess, sys
S = os.environ["S"]; LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
base = json.load(open(os.path.join(LANE, ".ufo/waves/round-84/before/host/facts.json")))
f = copy.deepcopy(base)
f["cmdline"] = "resume_offset=111 " + f["cmdline"]   # first=111 (stale), last=3795013 (kernel honours last)
p = os.path.join(S, "discriminating", "M14-facts.json"); json.dump(f, open(p, "w"))
row = {"mutant": "M14", "facts": p, "note": "duplicate resume_offset=; first 111, last 3795013 (correct)"}
for name, gate in (("orig", os.path.join(S,"orig.py")), ("mutant", os.path.join(S,"mutants","M14.py"))):
    r = subprocess.run([sys.executable, gate, "--facts", p], capture_output=True, text=True, timeout=30)
    row[name] = {"rc": r.returncode, "stdout": json.loads(r.stdout) if r.stdout.strip() else None}
row["diverges"] = (row["orig"]["rc"], row["orig"]["stdout"]) != (row["mutant"]["rc"], row["mutant"]["stdout"])
print(json.dumps(row, indent=1))
json.dump(row, open(os.path.join(S,"discriminating","M14-evidence.json"), "w"), indent=1)
