#!/usr/bin/env python3
"""ReviewBattery seat: independent AST parse of FAMILIES / FAMILY_ROSTER for the r96 battery and
the r95 battery at b8f878c8, plus a per-case discriminator dump of the four new families.

Reads only; writes receipts/roster-parse.json under this seat dir.
"""
import ast
import importlib.util
import json
import os
import random
import shutil
import tempfile

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r96/ReviewBattery/derive"
os.makedirs(SCRATCH, exist_ok=True)


def parse_roster(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    roster = familes = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "FAMILY_ROSTER":
                    roster = ast.literal_eval(node.value)
                if isinstance(t, ast.Name) and t.id == "FAMILIES":
                    familes = [k.value for k in node.value.keys]
    return list(roster), list(familes)


def main():
    r95_path = os.path.join(SCRATCH, "bat95.py")
    src = os.popen("git -C %s show b8f878c8:tools/limine-pin-battery-r95.py" % LANE).read()
    open(r95_path, "w", encoding="utf-8").write(src)
    r95, f95 = parse_roster(r95_path)
    r96, f96 = parse_roster(os.path.join(LANE, "tools", "limine-pin-battery-r96.py"))
    new = [x for x in r96 if x not in set(r95)]
    gone = [x for x in r95 if x not in set(r96)]

    spec = importlib.util.spec_from_file_location(
        "bat96", os.path.join(LANE, "tools", "limine-pin-battery-r96.py"))
    bat = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bat)
    rng = random.Random(1234)
    root = tempfile.mkdtemp(prefix="derive-", dir=SCRATCH)
    cases = {}
    try:
        for fam in new:
            bat._SEQ.clear()
            rows = []
            for i in range(bat.CASES_PER_FAMILY):
                c, d, conf, esp = bat.build(fam, rng, root)
                rows.append({
                    "ordinal": i,
                    "version": c.version,
                    "pass_version": c.pass_version,
                    "check_echo": c.check_echo,
                    "check_era": c.check_era,
                    "era_b": c.era_b(),
                    "usage": list(c.usage) if c.usage else None,
                    "usage_positive": sorted(c.usage_positive) if c.usage_positive else None,
                    "expected_rc": c.finish()[0],
                    "expected_verdict": c.finish()[1],
                })
                shutil.rmtree(d, ignore_errors=True)
            cases[fam] = rows
    finally:
        shutil.rmtree(root, ignore_errors=True)

    out = {
        "r95_roster": len(r95), "r95_unique": len(set(r95)),
        "r96_roster": len(r96), "r96_unique": len(set(r96)),
        "r95_families_table": len(f95), "r96_families_table": len(f96),
        "r96_families_equals_roster_order": tuple(f96) == tuple(r96),
        "new_names": new, "removed_names": gone,
        "new_family_first_index": {n: r96.index(n) for n in new},
        "cases_per_family": bat.CASES_PER_FAMILY,
        "per_case_discriminators": cases,
    }
    dst = os.path.join(SEAT, "receipts", "roster-parse.json")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != "per_case_discriminators"}, indent=1))
    for fam in new:
        print(fam, [(r["ordinal"], r["version"], r["check_echo"], r["check_era"],
                     (r["usage"] or [])[:2], r["era_b"], r["expected_verdict"]) for r in cases[fam]])


if __name__ == "__main__":
    main()
