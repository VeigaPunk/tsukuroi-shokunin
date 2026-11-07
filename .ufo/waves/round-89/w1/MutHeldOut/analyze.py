#!/usr/bin/env python3
"""MutHeldOut round-89: turn the two battery JSON receipts into the discrimination table."""
import json
import os
import sys

BAT = sys.argv[1] if len(sys.argv) > 1 else "/fast/scratch/hyaku/tsukuroi-r89/MutHeldOut/bat"
WAVE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    try:
        d = json.load(open(path))
    except Exception:  # noqa: BLE001
        return None
    return d if isinstance(d, list) else [d]


rows = []
for name in sorted(os.listdir(BAT)):
    if not name.endswith(".r89.json"):
        continue
    gid = name[: -len(".r89.json")]
    r89 = load(os.path.join(BAT, gid + ".r89.json"))
    r88 = load(os.path.join(BAT, gid + ".r88.json"))
    rec = {"id": gid}
    for tag, runs in (("r88", r88), ("r89", r89)):
        if runs is None:
            rec[tag] = {"runs": 0, "killed_runs": None, "failed": ["<no receipt>"]}
            continue
        failed = sorted({f for r in runs for f in r["failed_families"]})
        killed = sum(1 for r in runs if r["verdict"] != "met")
        rec[tag] = {"runs": len(runs), "killed_runs": killed, "failed": failed}
    rows.append(rec)

table = []
for r in rows:
    table.append([r["id"],
                  "%d/%d" % (r["r88"]["killed_runs"], r["r88"]["runs"]),
                  "%d/%d" % (r["r89"]["killed_runs"], r["r89"]["runs"]),
                  ",".join(r["r89"]["failed"]) or "-"])
w = [max(len(str(x[i])) for x in table + [["mutant", "r88", "r89", "r89 families failed"]]) for i in range(4)]
out = []
for i, row in enumerate([["mutant", "r88", "r89", "r89 families failed"]] + table):
    out.append(" | ".join(str(c).ljust(w[j]) for j, c in enumerate(row)))
    if i == 0:
        out.append("-|-".join("-" * x for x in w))
text = "\n".join(out)
print(text)
pris = [r for r in rows if r["id"] == "pristine"]
rest = [r for r in rows if r["id"] != "pristine"]
print()
print("gates: %d (pristine + %d mutants)" % (len(rows), len(rest)))
for tag in ("r88", "r89"):
    killed = [r for r in rest if r[tag]["killed_runs"]]
    surv = [r["id"] for r in rest if not r[tag]["killed_runs"]]
    print("%s: killed %d/%d mutants (pristine: %s)" % (
        tag, len(killed), len(rest),
        "met" if pris and pris[0][tag]["killed_runs"] == 0 else "NOT-met/inconclusive"))
    if surv:
        print("  survivors: " + ", ".join(surv))
json.dump({"schema": "tsukuroi-heldout-discrimination-r89-v1", "rows": rows},
          open(os.path.join(WAVE, "battery-results.json"), "w"), indent=1)
open(os.path.join(WAVE, "battery-table.txt"), "w").write(text + "\n")
