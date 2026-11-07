#!/usr/bin/env python3
"""Cross-check: does each deletion mutant escape exactly the negatives whose sole killer is that family?

Reads the per-negative sweep receipts and the mutant counter receipts. Prints a comparison plus the
per-mutant observed escapes and positives.
"""
import glob
import json
import os

S = os.environ.get("S", "/fast/scratch/hyaku/tsukuroi-r89/MutBattery")

FAMILY_OF = {
    "del-blank-class": "BLANK-CLASS",
    "del-optional-missing": "OPTIONAL-MISSING",
    "del-optional-unresolved": "OPTIONAL-UNRESOLVED",
    "del-empty-pin-list": "EMPTY-PIN-LIST",
    "del-double-dollar": "DOUBLE-DOLLAR",
    "del-entry-label-edges": "ENTRY-LABEL-EDGES",
    "del-panic-value-blanks": "PANIC-VALUE-BLANKS",
    "del-cr-internal": "CR-INTERNAL",
    "del-resource-case": "RESOURCE-CASE",
    "del-key-equals": "KEY-EQUALS",
    "del-empty-path": "EMPTY-PATH",
    "del-optional-key-case": "OPTIONAL-KEY-CASE",
}


def sweep_unions():
    u = {}
    for p in glob.glob(os.path.join(S, "sweep", "N-*.summary.json")):
        r = json.load(open(p))
        if r.get("parse") == "ok":
            u[r["gate"]] = r["kill_families_union"]
    return u


def mutant_rows():
    out = {}
    for p in glob.glob(os.path.join(S, "mut", "*.counter.json")):
        name = os.path.basename(p)[:-len(".counter.json")]
        if name == "baseline":
            continue
        j = json.load(open(p))
        r0 = j["runs"][0]
        out[name] = {
            "verdict": j.get("verdict"),
            "pos": r0["positives_ok"], "pos_total": r0["positives_total"],
            "neg": r0["negatives_ok"], "neg_total": r0["negatives_total"],
            "errors": j.get("error_rows"),
            "escapes": sorted(r["id"] for r in r0["rows"] if r["expect"] == "unmet" and not r["ok"]),
            "pos_failed": sorted(r["id"] for r in r0["rows"] if r["expect"] == "met" and not r["ok"]),
        }
    return out


def main():
    u = sweep_unions()
    rows = mutant_rows()
    print("negatives with sweep receipts: %d" % len(u))
    for name in sorted(rows):
        r = rows[name]
        print("\n%s verdict=%s P=%d/%d N=%d/%d errors=%s" % (
            name, r["verdict"], r["pos"], r["pos_total"], r["neg"], r["neg_total"], r["errors"]))
        print("  escapes: %s" % (", ".join(r["escapes"]) or "none"))
        if name in FAMILY_OF:
            fam = FAMILY_OF[name]
            pred = sorted(g for g, un in u.items() if un == [fam])
            print("  predicted escapes (sole killer %s): %s" % (fam, ", ".join(pred) or "none"))
            print("  match: %s" % ("yes" if pred == r["escapes"] else "NO"))
        if r["pos_failed"]:
            print("  positives failed: %s" % ", ".join(r["pos_failed"]))


if __name__ == "__main__":
    main()
