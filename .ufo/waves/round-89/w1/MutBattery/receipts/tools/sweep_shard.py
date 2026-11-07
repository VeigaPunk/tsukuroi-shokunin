#!/usr/bin/env python3
"""One shard of the negative kill-robustness sweep; skips gates that already have a complete receipt.

Usage: sweep_shard.py --shard K --shards N
"""
import concurrent.futures
import argparse
import glob
import json
import os
import subprocess
import sys

S = os.environ["S"]
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
ROSTER = os.path.join(LANE, ".ufo", "waves", "round-89", "before", "roster")
BATTERY = os.path.join(LANE, "tools", "limine-pin-battery-r89.py")
OUT = os.path.join(S, "sweep")
WORK = os.path.join(S, "sw")
RUNS = 10

ap = argparse.ArgumentParser()
ap.add_argument("--shard", type=int, required=True)
ap.add_argument("--shards", type=int, required=True)
a = ap.parse_args()

with open(os.path.join(ROSTER, "roster-r89.json")) as f:
    roster = json.load(f)
neg = [g for g in roster["gates"] if g["expect"] == "unmet"]
neg.sort(key=lambda g: g["id"])
mine = [g for i, g in enumerate(neg) if i % a.shards == a.shard]


def done(gid):
    p = os.path.join(OUT, gid + ".summary.json")
    if not os.path.isfile(p):
        return False
    try:
        with open(p) as f:
            r = json.load(f)
        return r.get("parse") == "ok" and r.get("runs") == RUNS
    except Exception:  # noqa: BLE001
        return False


todo = [g for g in mine if not done(g["id"])]


def one(g):
    gid = g["id"]
    w = os.path.join(WORK, gid)
    os.makedirs(w, exist_ok=True)
    out = os.path.join(OUT, gid + ".json")
    log = os.path.join(OUT, gid + ".log")
    env = dict(os.environ, TMPDIR=S, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, BATTERY, "--gate", os.path.join(ROSTER, g["file"]),
                        "--runs", str(RUNS), "--work", w, "--json", out],
                       capture_output=True, text=True, env=env, timeout=3600)
    with open(log, "w") as f:
        f.write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    try:
        with open(out) as f:
            runs = json.load(f)
        if isinstance(runs, dict):
            runs = [runs]
        per = [{"verdict": r["verdict"], "failed": r["failed_families"], "n": r["families_passed"]}
               for r in runs]
        unmet = sum(r["verdict"] == "unmet" for r in per)
        res = {"gate": gid, "file": g["file"], "runs": len(per), "unmet_runs": unmet,
               "rc": p.returncode, "per_run": per,
               "kill_families_union": sorted({f for r in per for f in r["failed"]}),
               "runs_with_single_killer": sum(len(r["failed"]) == 1 for r in per), "parse": "ok"}
    except Exception as e:  # noqa: BLE001
        res = {"gate": gid, "file": g["file"], "parse": "error: %s: %s" % (type(e).__name__, e),
               "rc": p.returncode, "stdout_tail": p.stdout[-400:], "stderr_tail": p.stderr[-400:]}
    with open(os.path.join(OUT, gid + ".summary.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


print("shard %d/%d mine=%d todo=%d" % (a.shard, a.shards, len(mine), len(todo)), flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get("SWEEP_JOBS", "6"))) as ex:
    futs = {ex.submit(one, g): g for g in todo}
    for i, fu in enumerate(concurrent.futures.as_completed(futs), 1):
        r = fu.result()
        print("%2d/%d %-36s unmet %s/%s killers=%s" % (
            i, len(todo), r["gate"], r.get("unmet_runs"), r.get("runs"),
            ",".join(r.get("kill_families_union", [])) or r.get("parse")), flush=True)
print("SHARD %d DONE" % a.shard, flush=True)
