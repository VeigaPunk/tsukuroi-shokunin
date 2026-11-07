#!/usr/bin/env python3
"""Run the frozen r89 counter (--runs 1 --jobs 4) on every generated battery mutant.

For each mutant: which roster negatives escape (read `met`), which positives fail, error rows.
Also verifies the mutant's FAMILIES table equals FAMILY_ROSTER (else the battery is a usage
error, not a mutant of interest).
"""
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

S = os.environ["S"]
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
COUNTER = os.path.join(LANE, "tools", "battery-discrimination-r89.py")
SRC = os.path.join(S, "mut", "src")
OUT = os.path.join(S, "mut")
PAR = int(os.environ.get("MUT_PAR", "2"))


def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def one(name):
    path = os.path.join(SRC, name + ".py")
    with open(path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    try:
        m = load_mod(path, "mut_" + name.replace("-", "_"))
        consistent = tuple(m.FAMILIES) == m.FAMILY_ROSTER
        nfam = len(m.FAMILY_ROSTER)
    except Exception as e:  # noqa: BLE001
        return {"mutant": name, "sha256": h, "load": "error: %s: %s" % (type(e).__name__, e)}
    jout = os.path.join(OUT, name + ".counter.json")
    env = dict(os.environ, TMPDIR=S, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, COUNTER, "--battery", path, "--runs", "1", "--jobs", "4",
                        "--scratch", os.path.join(S, "c"), "--json", jout],
                       capture_output=True, text=True, env=env, timeout=3600)
    res = {"mutant": name, "sha256": h, "families": nfam, "families_consistent": consistent,
           "counter_rc": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()[-600:]}
    try:
        with open(jout) as f:
            j = json.load(f)
        r0 = j["runs"][0]
        res["verdict"] = j["verdict"]
        res["positives_ok"] = "%d/%d" % (r0["positives_ok"], r0["positives_total"])
        res["negatives_ok"] = "%d/%d" % (r0["negatives_ok"], r0["negatives_total"])
        res["error_rows"] = r0["error_rows"]
        res["escapes"] = sorted(r["id"] for r in r0["rows"] if r["expect"] == "unmet" and r["ok"])
        res["positives_failed"] = [r["id"] for r in r0["rows"] if r["expect"] == "met" and not r["ok"]]
        res["errors"] = [r["id"] + ":" + str(r["got"]) for r in r0["rows"] if r["error"]][:5]
    except Exception as e:  # noqa: BLE001
        res["parse"] = "error: %s: %s" % (type(e).__name__, e)
    return res


def done(name):
    p = os.path.join(OUT, name + ".summary.json")
    if not os.path.isfile(p):
        return False
    try:
        with open(p) as f:
            r = json.load(f)
        return "verdict" in r or "parse" in r
    except Exception:  # noqa: BLE001
        return False


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--shards", type=int, default=1)
    args = ap.parse_args()
    allnames = sorted(x[:-3] for x in os.listdir(SRC) if x.endswith(".py"))
    names = [n for i, n in enumerate(allnames) if i % args.shards == args.shard and not done(n)]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=PAR) as ex:
        futs = {ex.submit(one, n): n for n in names}
        for i, fu in enumerate(concurrent.futures.as_completed(futs), 1):
            r = fu.result()
            results.append(r)
            print("%2d/%d %-28s verdict=%-18s P=%s N=%s err=%s escapes=%s" % (
                i, len(names), r["mutant"], r.get("verdict"), r.get("positives_ok"),
                r.get("negatives_ok"), r.get("error_rows"), ",".join(r.get("escapes", [])) or "-"),
                flush=True)
            with open(os.path.join(OUT, r["mutant"] + ".summary.json"), "w") as f:
                json.dump(r, f, indent=1)
    results.sort(key=lambda r: r["mutant"])
    with open(os.path.join(OUT, "mutants-summary.json"), "w") as f:
        json.dump({"counter": COUNTER, "results": results}, f, indent=1)


if __name__ == "__main__":
    main()
