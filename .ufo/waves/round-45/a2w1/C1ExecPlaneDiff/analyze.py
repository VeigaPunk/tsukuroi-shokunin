#!/usr/bin/env python3
"""C1ExecPlaneDiff field/shape analysis for item C1-4.

Runs: base x3, impl x3, alternating (b i b i b i) on the live host.
- SHAPE: per line, the prefix (text before the first '(' — e.g. "PLANE drivers: DEGRADED")
  and the ordered list of key= names. Any shape difference across the six runs is a
  kill-rule hit. All six must agree.
- VALUES: per key, the six values. A base->impl difference is explained by live drift
  only if the same key also differs between two runs of ONE revision. Otherwise it is
  revision-induced -> falsifies C1's "planes unchanged".
"""
import re, sys
BASE = "/fast/scratch/hyaku/tsukuroi-r45/C1ExecPlaneDiff/fresh"
RUNS = [("base", 1), ("impl", 1), ("base", 2), ("impl", 2), ("base", 3), ("impl", 3)]
KV = re.compile(r"(?<![^\s;(\[])([A-Za-z0-9_][A-Za-z0-9_.\-]*)=((?:[^\s;()\[\]]|\[[^\]]*\])*)")

def body(rev, n):
    with open(f"{BASE}/body-{rev}-{n}.out", encoding="utf-8") as fh:
        return fh.read().splitlines()

bodies = {r: body(*r) for r in RUNS}
lens = {r: len(v) for r, v in bodies.items()}
print("line counts:", lens)
assert len(set(lens.values())) == 1, "FATAL: line count differs"
n = lens[RUNS[0]]
bad = 0
for i in range(n):
    lines = {r: bodies[r][i] for r in RUNS}
    pref = {r: lines[r].split("(", 1)[0].strip() for r in RUNS}
    keys = {r: [m.group(1) for m in KV.finditer(lines[r])] for r in RUNS}
    print(f"\n=== line {i+1} ===")
    if len(set(pref.values())) != 1:
        print("  SHAPE: prefix differs:", pref); bad += 1
    else:
        print("  prefix (same all 6):", pref[RUNS[0]])
    uniq_keysets = {tuple(v) for v in keys.values()}
    if len(uniq_keysets) != 1:
        print("  SHAPE: key sequence differs across runs"); bad += 1
        for r in RUNS:
            print("   ", r, keys[r][:12], "..." if len(keys[r]) > 12 else "")
    else:
        print(f"  key sequence (same all 6, in order): {len(keys[RUNS[0]])} keys")
    order = list(dict.fromkeys(keys[RUNS[0]]))
    vals = {k: [dict(KV.findall(lines[r])).get(k) for r in RUNS] for k in order}
    for k in order:
        v = vals[k]
        if len(set(v)) == 1:
            continue
        b = [v[j] for j, r in enumerate(RUNS) if r[0] == "base"]
        im = [v[j] for j, r in enumerate(RUNS) if r[0] == "impl"]
        intra_b = len(set(b)) > 1
        intra_i = len(set(im)) > 1
        cross = set(b) != set(im)
        verdict = "LIVE-DRIFT (recurs within a revision)"
        if cross and not intra_b and not intra_i:
            verdict = "REVISION-INDUCED"
            bad += 1
        elif cross:
            verdict = "cross-differs-and-recurs-within-a-revision"
        print(f"  {k}: base={b} impl={im} -> {verdict}")
print("\nshape_or_revision_induced_problems:", bad)
sys.exit(1 if bad else 0)
