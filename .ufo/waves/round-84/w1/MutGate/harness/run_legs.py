import concurrent.futures, json, os, subprocess, sys
S = os.environ["S"]; LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BAT = os.path.join(S, "legs", "resume-gate-battery-r84-legs.py")
jobs = [("orig", n, os.path.join(S, "orig.py")) for n in (1, 2)]
for mid in sorted({f[:-3] for f in os.listdir(os.path.join(S, "mutants")) if f.startswith("M") and f.endswith(".py")}):
    jobs += [(mid, n, os.path.join(S, "mutants", mid + ".py")) for n in (1, 2)]
def run(job):
    name, n, gate = job
    td = os.path.join(S, "legs-tmp", f"{name}-{n}"); os.makedirs(td, exist_ok=True)
    p = subprocess.run([sys.executable, BAT, "--gate", gate], cwd=LANE, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=td), timeout=900)
    out = os.path.join(S, "legs-runs", f"{name}-run{n}.json")
    open(out, "w").write(p.stdout + ("\n---STDERR---\n" + p.stderr if p.stderr else ""))
    try:
        d = json.loads(p.stdout)
        return name, n, p.returncode, d["families_passed"], d["failed_families"], len(d["cases"])
    except Exception:
        return name, n, p.returncode, None, ["parse-fail"], 0
res = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for r in ex.map(run, jobs):
        res.append(r)
res.sort(key=lambda r: (r[0] != "orig", r[0], r[1]))
json.dump(res, open(os.path.join(S, "legs-runs", "summary.json"), "w"), indent=1)
for r in res:
    print(r[0], f"run{r[1]}", "rc=" + str(r[2]), f"{r[3]}/13", "cases=" + str(r[5]), (r[4] or [])[:4])
