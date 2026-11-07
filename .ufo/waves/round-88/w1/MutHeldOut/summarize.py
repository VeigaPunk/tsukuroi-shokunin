#!/usr/bin/env python3
"""Summarise the per-mutant battery receipts into the report table."""
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(S, "receipts")
MUT = os.path.join(S, "mutants")


def rows(name, kind):
    p = os.path.join(REC, "%s.%s.json" % (name, kind))
    if not os.path.isfile(p):
        return None
    d = json.load(open(p))
    runs = d if isinstance(d, list) else [d]
    counts = ["%d/%d" % (r["families_passed"], r["families_total"]) for r in runs]
    verdicts = [r["verdict"] for r in runs]
    failed = sorted(set(f for r in runs for f in r["failed_families"]))
    return {"counts": counts, "verdicts": verdicts, "failed": failed, "met": all(v == "met" for v in verdicts)}


def main():
    probe = json.load(open(os.path.join(S, "probe-results.json")))["differs"]
    names = sorted(n[:-3] for n in os.listdir(MUT) if n.endswith(".py"))
    out = []
    for n in names:
        r88 = rows(n, "r88")
        r87 = rows(n, "r87")
        row = {"mutant": n, "probe_differs": bool(probe.get(n)), "probe_fixtures": probe.get(n, []),
               "r88": r88, "r87": r87}
        out.append(row)
        print("%-32s probe=%-10s r87=%s %s | r88=%s %s | r87=%s r88=%s" % (
            n, "differs" if row["probe_differs"] else "EQUIVALENT",
            "/".join(r87["counts"]) if r87 else "?", "/".join(sorted(set(r87["failed"]))) if r87 else "?",
            "/".join(r88["counts"]) if r88 else "?", "/".join(sorted(set(r88["failed"]))) if r88 else "?",
            "SURVIVED" if r87 and r87["met"] else "killed",
            "SURVIVED" if r88 and r88["met"] else "killed"))
    with open(os.path.join(S, "summary.json"), "w") as f:
        json.dump(out, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
