#!/usr/bin/env python3
"""Order the six captures by wall clock and test whether the differing counters are time-driven.

Every value is read from the captured PLANE drivers line; nothing is re-read from the host.
"""
import pathlib
import re

OUT = pathlib.Path("/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalPlaneDiff/out")
ORDER = [("base", 1), ("tip", 1), ("base", 2), ("tip", 2), ("base", 3), ("tip", 3)]
FIELDS = ["C5_pswp", "C6_psi_some_avg300", "C6_psi_full_avg300", "C6_psi_full_total_us",
          "C6_avail_kb", "C6_shmem_kb"]

rows = []
for rev, n in ORDER:
    lines = (OUT / f"out-{rev}-{n}.txt").read_text().splitlines()
    hdr = lines[0]
    ts = re.search(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)", hdr).group(1)
    drivers = [ln for ln in lines if ln.startswith("PLANE drivers:")]
    assert len(drivers) == 1
    d = drivers[0]
    vals = {}
    for f in FIELDS:
        m = re.search(re.escape(f) + r"=([^;\s]+)", d)
        vals[f] = m.group(1) if m else None
    rows.append((f"{rev}-{n}", ts, vals))

print("run      timestamp             " + "  ".join(f"{f:>22}" for f in FIELDS))
for name, ts, vals in rows:
    print(f"{name:<8} {ts}  " + "  ".join(f"{str(vals[f]):>22}" for f in FIELDS))

print("\nconsecutive deltas in wall-clock order (transition revision shown):")
def num(v):
    # pswp is 'in/out'; compare the 'out' half for monotonicity, report both halves
    return v
prev = None
for i, (name, ts, vals) in enumerate(rows):
    if prev is None:
        prev = (name, vals)
        continue
    pn, pv = prev
    trans = "same-rev" if pn[0] == name[0] else f"cross({pn[0]}->{name[0]})"
    out = []
    for f in FIELDS:
        if pv[f] == vals[f]:
            continue
        if f == "C5_pswp":
            a, b = pv[f].split("/"), vals[f].split("/")
            out.append(f"C5_pswp in+{int(b[0]) - int(a[0])} out+{int(b[1]) - int(a[1])}")
        else:
            try:
                out.append(f"{f} {int(vals[f]) - int(pv[f]):+d}")
            except ValueError:
                out.append(f"{f} {pv[f]}->{vals[f]}")
    print(f"  {pn}->{name} [{trans}] " + ("; ".join(out) if out else "no change"))
    prev = (name, vals)

print("\nmonotonicity over the batch (6 samples, both revisions interleaved):")
for f in ("C5_pswp_out", "C6_psi_full_total_us"):
    seq = []
    for name, ts, vals in rows:
        seq.append(int(vals["C5_pswp"].split("/")[1]) if f == "C5_pswp_out" else int(vals[f]))
    mono = all(b >= a for a, b in zip(seq, seq[1:]))
    print(f"  {f}: {seq}  non-decreasing={mono}")

for f in ("C6_avail_kb", "C6_shmem_kb", "C6_psi_some_avg300", "C6_psi_full_avg300"):
    seq = [int(vals[f]) if vals[f].isdigit() else float(vals[f]) for _, _, vals in rows]
    dirs = ["+" if b > a else ("-" if b < a else "0") for a, b in zip(seq, seq[1:])]
    print(f"  {f}: {seq}  directions={''.join(dirs)}  both-directions={('+' in dirs and '-' in dirs)}")

# revision effect on pswp: increments bounded by the same order of magnitude regardless of transition
print("\npswpout increments by transition kind:")
inc = []
for i in range(1, len(rows)):
    a = int(rows[i - 1][2]["C5_pswp"].split("/")[1])
    b = int(rows[i][2]["C5_pswp"].split("/")[1])
    kind = "same-rev" if rows[i - 1][0][0] == rows[i][0][0] else "cross"
    inc.append((kind, b - a))
print("  " + ", ".join(f"{k}:+{d}" for k, d in inc))
print("  same-rev deltas:", [d for k, d in inc if k == "same-rev"])
print("  cross-rev deltas:", [d for k, d in inc if k == "cross"])
