#!/usr/bin/env python3
"""Round-99 C2 second pass: more separator forges (guard alphabet) and the revision matrix."""
import json, os, shutil, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r99/ReviewRegistry"
REC = os.path.join(LANE, ".ufo/waves/round-99/w1/ReviewRegistry/receipts")
R98 = os.path.join(LANE, "tools/check-registry-content-r98.py")
R99 = os.path.join(LANE, "tools/check-registry-content-r99.py")

sys.path.insert(0, SCRATCH)
from forge import build, derived, run, CASES  # noqa: E402

MORE = [
    ("y1-semicolon-label", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04; N05", {}),
    ("y2-plus-label", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04+N05", {}),
    ("y3-slash-label", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04/N05", {}),
    ("y4-and-label", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04 and N05", {}),
    ("y5-comma-list-5keys", "clean", ["N01", "N02", "N03", "N04", "N05"],
     "VARIANTS N01,N02,N03,N04,N05", {}),
    ("y6-two-mentions-nospace", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04VARIANTS N01-N05", {}),
    ("y7-pipe-tight", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04\\|VARIANTS N01-N05", {}),
    ("y8-backtick-second", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 and `VARIANTS N01-N05`", {}),
]


def main():
    rows = []
    cases_root = os.path.join(SCRATCH, "cases2")
    os.makedirs(cases_root, exist_ok=True)
    for name, base, labels, cell, extra in MORE:
        case = os.path.join(cases_root, name)
        build(case, base, labels, cell, extra)
        row = {"case": name, "cell": cell, "keys": ",".join(labels), "derived": derived(labels)}
        for tag, tool in (("r98", R98), ("r99", R99)):
            out = os.path.join(REC, "forge-%s-%s.json" % (name, tag))
            rc, text, payload = run(tool, case, out)
            row[tag] = {"rc": rc,
                        "ids": sorted(f["id"] for f in (payload or {}).get("findings", []))
                        if payload else None}
        rows.append(row)
        print("%-24s cell=%-42r derived=%-9s r98=%s %s | r99=%s %s"
              % (name, cell, row["derived"], row["r98"]["rc"], row["r98"]["ids"],
                 row["r99"]["rc"], row["r99"]["ids"]))
    with open(os.path.join(REC, "forge-matrix2.json"), "w") as f:
        json.dump(rows, f, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
