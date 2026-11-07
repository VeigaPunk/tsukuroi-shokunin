#!/usr/bin/env python3
"""Render the r89 MutBattery tables from receipts on disk (individual sweep receipts + counter JSONs)."""
import glob
import json
import os

S = os.environ.get("S", "/fast/scratch/hyaku/tsukuroi-r89/MutBattery")
AFTER_FIX = {}  # filled below


def negatives():
    rows = {}
    for p in sorted(glob.glob(os.path.join(S, "sweep", "N-*.summary.json"))):
        with open(p) as f:
            r = json.load(f)
        rows[r["gate"]] = r
    return rows


def mutants():
    rows = []
    for p in sorted(glob.glob(os.path.join(S, "mut", "*.counter.json"))):
        name = os.path.basename(p)[:-len(".counter.json")]
        with open(p) as f:
            j = json.load(f)
        r0 = j["runs"][0]
        rows.append({
            "mutant": name,
            "sha": j.get("battery_sha256", ""),
            "verdict": j.get("verdict"),
            "pos": "%d/%d" % (r0["positives_ok"], r0["positives_total"]),
            "neg": "%d/%d" % (r0["negatives_ok"], r0["negatives_total"]),
            "errors": j.get("error_rows"),
            "escapes": sorted(r["id"] for r in r0["rows"] if r["expect"] == "unmet" and not r["ok"]),
            "pos_failed": sorted(r["id"] for r in r0["rows"] if r["expect"] == "met" and not r["ok"]),
        })
    return rows


def mutant_table():
    print("| mutant | battery sha256 | counter verdict | positives | negatives | error rows | negatives that escaped (read met) | positives failed |")
    print("|---|---|---|---|---|---|---|---|")
    for r in mutants():
        print("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["mutant"], r["sha"][:12], r["verdict"], r["pos"], r["neg"], r["errors"],
            ", ".join(r["escapes"]) or "none", ", ".join(r["pos_failed"]) or "none"))


def sweep_table():
    neg = negatives()
    print("| negative | unmet/10 | killer families (union) | runs with exactly one killer |")
    print("|---|---|---|---|")
    for gid in sorted(neg):
        r = neg[gid]
        if r.get("parse") != "ok":
            print("| %s | receipt %s | - | - |" % (gid, r.get("parse")))
            continue
        print("| %s | %d/10 | %s | %d |" % (gid, r["unmet_runs"],
                                            ", ".join(r["kill_families_union"]) or "-",
                                            r["runs_with_single_killer"]))
    print("\nnegatives missing a receipt: %d" % (62 - len(neg)))


def flake_table():
    neg = negatives()
    print("| negative | unmet/10 | killer union | draw-dependent single killer? |")
    print("|---|---|---|---|")
    flagged = 0
    for gid in sorted(neg):
        r = neg[gid]
        if r.get("parse") != "ok":
            continue
        union = r["kill_families_union"]
        draw = union == ["HASH-LENGTH"] or union == ["PANIC-NO-ONLY"]
        if r["unmet_runs"] != 10 or draw:
            flagged += 1
            print("| %s | %d/10 | %s | %s |" % (gid, r["unmet_runs"], ", ".join(union),
                                                "YES" if draw else "no (empirical miss)"))
    print("\nflagged: %d" % flagged)


if __name__ == "__main__":
    import sys
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "mutants"):
        mutant_table()
    if what in ("all", "sweep"):
        print()
        sweep_table()
    if what in ("all", "flake"):
        print()
        flake_table()
