#!/usr/bin/env python3
"""Do the moving counters track elapsed wall time rather than the revision?

All 15 pairs with elapsed seconds (from the header timestamps) and the pswpin / psi-full
deltas, split by same-rev vs cross-rev.
"""
import pathlib
import re
from datetime import datetime

OUT = pathlib.Path("/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPlaneDiff/out")
ORDER = [("base", 1), ("tip", 1), ("base", 2), ("tip", 2), ("base", 3), ("tip", 3)]

rows = []
for rev, n in ORDER:
    lines = (OUT / f"out-{rev}-{n}.txt").read_text().splitlines()
    ts = datetime.strptime(re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)", lines[0]).group(1),
                           "%Y-%m-%dT%H:%M:%SZ")
    d = [ln for ln in lines if ln.startswith("PLANE drivers:")][0]
    def f(k):
        return int(re.search(re.escape(k) + r"=(\d+)", d).group(1))
    rows.append(dict(name=f"{rev}-{n}", rev=rev, ts=ts, pswpin=f("C5_pswp"),
                     psi=f("C6_psi_full_total_us"), avail=f("C6_avail_kb")))

print(f"{'pair':<20}{'kind':<12}{'dt(s)':>6}{'d_pswpin':>10}{'d_psi_us':>12}{'d_avail':>12}")
same, cross = [], []
for i in range(len(rows)):
    for j in range(i + 1, len(rows)):
        a, b = rows[i], rows[j]
        dt = int((b["ts"] - a["ts"]).total_seconds())
        kind = "same-rev" if a["rev"] == b["rev"] else "cross-rev"
        rec = (dt, b["pswpin"] - a["pswpin"], b["psi"] - a["psi"], b["avail"] - a["avail"])
        print(f"{a['name'] + '-' + b['name']:<20}{kind:<12}{dt:>6}{rec[1]:>10}{rec[2]:>12}{rec[3]:>12}")
        (same if kind == "same-rev" else cross).append(rec)

def summarize(tag, rs):
    print(f"\n{tag}: n={len(rs)}  dt=[{min(r[0] for r in rs)}..{max(r[0] for r in rs)}]  "
          f"d_pswpin=[{min(r[1] for r in rs)}..{max(r[1] for r in rs)}]  "
          f"d_psi_us=[{min(r[2] for r in rs)}..{max(r[2] for r in rs)}]  "
          f"d_avail_kb=[{min(r[3] for r in rs)}..{max(r[3] for r in rs)}]")
summarize("same-rev", same)
summarize("cross-rev", cross)

print("\nlargest |d_pswpin| by class:")
print("  same-rev:", max(same, key=lambda r: r[1])[1])
print("  cross-rev:", max(cross, key=lambda r: r[1])[1])
print("largest |d_psi_us| by class:")
print("  same-rev:", max(same, key=lambda r: r[2])[2])
print("  cross-rev:", max(cross, key=lambda r: r[2])[2])
print("\navail delta range covers both signs in both classes:",
      any(r[3] > 0 for r in same) and any(r[3] < 0 for r in same),
      any(r[3] > 0 for r in cross) and any(r[3] < 0 for r in cross))

# per-second rates, so different elapsed windows are comparable
print("\nd_pswpin per second (pair value / dt):")
for tag, rs in (("same-rev", same), ("cross-rev", cross)):
    rates = sorted(round(r[1] / r[0], 2) for r in rs)
    print(f"  {tag}: {rates}")
print("d_psi_us per second:")
for tag, rs in (("same-rev", same), ("cross-rev", cross)):
    rates = sorted(round(r[2] / r[0], 1) for r in rs)
    print(f"  {tag}: {rates}")
