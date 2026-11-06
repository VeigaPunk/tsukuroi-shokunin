#!/usr/bin/env python3
"""Uncaught-behaviour probes: does each SURVIVOR accept input the pristine counter refuses?
Entries are generated once under a clean GEN root; each run rebuilds a fresh RUN root."""
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
S = "/fast/scratch/hyaku/tsukuroi-r84/MutCounter"
SRC = os.path.join(LANE, "tools/count-resume-rows-r84.py")
MUTDIR = os.path.join(S, "mut")

spec = importlib.util.spec_from_file_location("pristine", SRC)
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
REAL = json.load(open(os.path.join(LANE, P.ENTRY), encoding="utf-8"))


def build(path):
    shutil.rmtree(path, ignore_errors=True)
    root = os.path.join(path, "lane")
    os.makedirs(root, exist_ok=True)
    P._copy_inputs(P.Reader(root=LANE), root)
    ep = os.path.join(root, P.ENTRY)
    os.makedirs(os.path.dirname(ep), exist_ok=True)
    return root, ep


def run(script, root, ep, entry):
    json.dump(entry, open(ep, "w", encoding="utf-8"), indent=1)
    p = subprocess.run([sys.executable, script, "--root", root], capture_output=True, text=True,
                       env={**os.environ, "TMPDIR": S})
    try:
        d = json.loads(p.stdout)
    except Exception:
        return {"rc": p.returncode, "raw": (p.stdout + p.stderr)[-300:]}
    bad = {r["id"]: r["reason"] for r in d.get("rows", []) if r.get("reason") != "ok"}
    return {"rc": p.returncode, "verdict": d.get("verdict"), "counted": d.get("counted"),
            "failed": d.get("failed"), "distinct": d.get("distinct_snapshots"), "bad": bad}


def clone():
    return json.loads(json.dumps(REAL))


def wordspan(root, nwords):
    """Contiguous nwords span the PRISTINE predicate accepts as an exact minimal span."""
    for k, s in sorted(REAL["snapshots"].items()):
        lines = open(os.path.join(root, s["path"]), encoding="utf-8", errors="replace").read().split("\n")
        for i in range(len(lines)):
            for j in range(i, min(i + 6, len(lines))):
                w = " ".join(lines[i:j + 1]).split()
                if len(w) < nwords:
                    continue
                q = " ".join(w[:nwords])
                if P.exact_span(lines, i + 1, j + 1, q)[0]:
                    return k, i + 1, j + 1, q
    raise SystemExit("no span")


GEN = os.path.join(S, "probe-gen")
GROOT, _ = build(GEN)
cases = []
# M02: declared digest matches the manifest, file bytes do not (append happens on the RUN root)
k0 = sorted(REAL["snapshots"])[0]
cases.append(("M02", clone(), f"append a line to {k0} on disk; declared digest + manifest untouched", "append"))
# M05: 30-word quote
e = clone(); k, a, b, q = wordspan(GROOT, 30)
e["rows"][0]["source"].update({"snapshot": k, "lines": [a, b], "quote": q})
cases.append(("M05", e, f"30-word quote {k}:{a}-{b}", None))
# M07: 7 valid rows from only 3 snapshots
cases.append(("M07", P._random_entry(GROOT, random.Random(7), P.TARGET_ROWS, 3),
              "7 valid rows, 3 distinct snapshots", None))
# M10: non-https snapshot url
e = clone(); k = sorted(REAL["snapshots"])[0]
e["snapshots"][k]["url"] = "http://example.invalid/" + os.path.basename(REAL["snapshots"][k]["path"])
cases.append(("M10", e, f"snapshot {k} url downgraded to http", None))
# M11: two rows share an id, quotes/spans distinct
e = clone(); e["rows"][6]["id"] = e["rows"][0]["id"]
cases.append(("M11", e, f"duplicate id {e['rows'][0]['id']}", None))
# M12: 5-word statement
e = clone(); e["rows"][0]["statement"] = "five word statement right here"
cases.append(("M12", e, "5-word statement", None))
# M13: one row fabricated -> counted 9, failed 1
e = clone(); e["rows"][0]["source"]["quote"] = "this sentence was never written in any pinned snapshot here"
cases.append(("M13", e, "one fabricated quote (counted>=7, failed=1)", None))
# M14: 4-word quote
e = clone(); k, a, b, q = wordspan(GROOT, 4)
e["rows"][0]["source"].update({"snapshot": k, "lines": [a, b], "quote": q})
cases.append(("M14", e, f"4-word quote {k}:{a}-{b}", None))
# M17: span end past EOF (equivalence check)
e = clone(); r = e["rows"][0]["source"]; r["lines"] = [r["lines"][0], 10 ** 6]
cases.append(("M17", e, "span end past EOF", None))
# M18: empty host value (equivalence check)
e = clone(); e["rows"][0]["host"]["value"] = ""
cases.append(("M18", e, "empty host value", None))

results = []
for mid, entry, what, post in cases:
    root, ep = build(os.path.join(S, "probe-run"))
    if post == "append":
        fp = os.path.join(root, REAL["snapshots"][k0]["path"])
        orig = open(fp, "rb").read()
        open(fp, "wb").write(orig + b"\nEXTRA-LINE-ADDED-BY-PROBE\n")
    base = run(SRC, root, ep, entry)
    shutil.rmtree(os.path.join(S, "probe-run"), ignore_errors=True)
    root, ep = build(os.path.join(S, "probe-run"))
    if post == "append":
        fp = os.path.join(root, REAL["snapshots"][k0]["path"])
        orig = open(fp, "rb").read()
        open(fp, "wb").write(orig + b"\nEXTRA-LINE-ADDED-BY-PROBE\n")
    mfile = [f for f in sorted(os.listdir(MUTDIR)) if f.startswith(mid + "-")][0]
    mut = run(os.path.join(MUTDIR, mfile), root, ep, entry)
    shutil.rmtree(os.path.join(S, "probe-run"), ignore_errors=True)
    key = lambda d: (d.get("rc"), d.get("verdict"), d.get("counted"), d.get("failed"))
    diff = key(base) != key(mut)
    results.append({"mutant": mid, "probe": what, "pristine": base, "mutant": mut, "verdict_differs": diff})
    print(f"{mid}: {what}\n  pristine {base}\n  mutant   {mut}\n  VERDICT-DIFFERS={diff}", flush=True)
json.dump(results, open(os.path.join(S, "probe-results.json"), "w"), indent=1)
