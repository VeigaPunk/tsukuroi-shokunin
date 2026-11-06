import concurrent.futures, json, os, subprocess, sys
S = os.environ["S"]; LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
meta = json.load(open(os.path.join(S, "mutants", "meta.json")))
jobs = [(m["id"], n) for m in meta for n in (1, 2)]
def run(job):
    mid, n = job
    td = os.path.join(S, "tmp", f"{mid}-{n}"); os.makedirs(td, exist_ok=True)
    env = dict(os.environ, TMPDIR=td)
    p = subprocess.run([sys.executable, "tools/resume-gate-battery-r84.py", "--gate", os.path.join(S,"mutants",mid+".py")],
                       cwd=LANE, capture_output=True, text=True, env=env, timeout=600)
    out = os.path.join(S, "runs", f"{mid}-run{n}.json")
    open(out, "w").write(p.stdout + ("\n---STDERR---\n" + p.stderr if p.stderr else ""))
    return mid, n, p.returncode, out
res = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for mid, n, rc, out in ex.map(run, jobs):
        try:
            d = json.loads(open(out).read().split("\n---STDERR---")[0])
            res.append((mid, n, rc, d.get("families_passed"), d.get("failed_families"), d.get("verdict")))
        except Exception as e:
            res.append((mid, n, rc, None, ["parse:"+type(e).__name__], None))
json.dump(res, open(os.path.join(S,"runs","summary.json"),"w"), indent=1)
for r in res:
    print(r[0], "run"+str(r[1]), "rc="+str(r[2]), str(r[3])+"/13", r[5], (r[4] or [])[:4])
