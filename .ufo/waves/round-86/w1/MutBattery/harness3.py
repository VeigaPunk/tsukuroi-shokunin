import concurrent.futures as cf, json, os, subprocess, sys
S = "/fast/scratch/hyaku/tsukuroi-r86/MutBattery"
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BASE = os.path.join(LANE, ".ufo/waves/round-85/before/host/facts-v2.json")
def build(src, pairs, dst):
    s = open(src, encoding="utf-8").read()
    for old, new in pairs:
        if s.count(old) != 1: raise SystemExit(f"{dst}: {s.count(old)} {old[:50]!r}")
        s = s.replace(old, new)
    open(dst, "w").write(s); return dst

# G4: an empty resume= permanently empties resume_file (ignores a later non-empty resume=)
G4 = build(os.path.join(S, "gates/candidate.py"), [
 ('def arg(cmdline, setup):\n    """Rest of the last token matching setup (each matching token overwrites; the kernel keeps the last)."""\n    val = None\n    for tok in cmdline.split():\n        if matches(tok, setup):\n            val = tok[len(setup):]\n    return val',
  'def arg(cmdline, setup):\n    """Mutant G4: any empty resume= token wins over every later value."""\n    val = None\n    for tok in cmdline.split():\n        if matches(tok, setup):\n            val = tok[len(setup):]\n            if val == "":\n                return ""\n    return val')],
 os.path.join(S, "gates2/G4-empty-resume-sticky.py"))

# M20: EMPTY-RESUME where a later non-empty resume= follows the empty one (deterministically appended), HEALTHY
M20 = build(os.path.join(S, "battery.py"), [
 ('    f, c_ids = chain_faults(b, rng, rng.randint(1, 3), file_base)\n    if rng.random() < .5:\n        cl = replace_tok(f["cmdline"], "resume=", "resume=")\n    else:\n        cl = put_after(f["cmdline"], "resume=", "resume=")',
  '    f, c_ids = chain_faults(b, rng, rng.randint(1, 3), file_base)\n    if rng.random() < .5:\n        cl = replace_tok(f["cmdline"], "resume=", "resume=")\n    else:\n        cl = put_after(f["cmdline"], "resume=", "resume=") + " resume=/dev/" + word(rng, 4)')],
 os.path.join(S, "mutants/M20-empty-resume-then-value.py"))
def run(battery, gate, tag):
    out = os.path.join(S, "out", tag + ".json")
    r = subprocess.run([sys.executable, battery, "--gate", gate, "--base", BASE, "--random", "5", "--out", out],
                       capture_output=True, text=True, cwd=LANE)
    try: res = json.load(open(out, encoding="utf-8"))
    except Exception: return {"tag": tag, "rc": r.returncode, "passed": None, "failed": ["ERR"], "err": r.stderr[-300:]}
    return {"tag": tag, "rc": r.returncode, "passed": res["families_passed"], "total": res["families_total"],
            "failed": res["failed_families"]}
jobs = [(os.path.join(S, "battery.py"), G4, "pristine__G4-empty-resume-sticky"),
        (M20, os.path.join(S, "gates/candidate.py"), "M20__candidate"),
        (M20, os.path.join(S, "gates/K1.py"), "M20__K1"),
        (M20, G4, "M20__G4")]
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    res = {f.result()["tag"]: f.result() for f in [ex.submit(run, *j) for j in jobs]}
for k in sorted(res):
    r = res[k]; print(f"{k:44s} rc={r['rc']} pass={r['passed']}/{r['total']} failed={','.join(r['failed']) or '-'}")
json.dump(res, open(os.path.join(S, "out", "matrix3.json"), "w"), indent=1, sort_keys=True)
