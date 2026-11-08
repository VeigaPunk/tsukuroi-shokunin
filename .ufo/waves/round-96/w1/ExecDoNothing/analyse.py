#!/usr/bin/env python3
"""Summarise the ExecDoNothing do-nothing receipts: verdict, families, error rows, failing cases."""
import glob
import json
import os

SEAT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-96/w1/ExecDoNothing"
NEW = ("EXPLICIT-VERSION-ECHO", "EXPLICIT-VERSION-ERA", "EXPLICIT-VERSION-META",
       "REFUSAL-VERSIONS-9DIGIT-Y", "EXTRA-COMPONENT")

def short(x):
    return json.dumps(x, sort_keys=True)[:400]

print("file | run | verdict | passed/total | failed_families | cases | error_rows | failing_cases")
files = sorted(glob.glob(os.path.join(SEAT, "dn-*.json")))
for f in files:
    data = json.load(open(f))
    runs = data if isinstance(data, list) else [data]
    for i, r in enumerate(runs, 1):
        errs = [e for e in r["case_log"] if e.get("error") is not None]
        bad = [e for e in r["case_log"] if not e["passed"]]
        print("%s | %d | %s | %d/%d | %s | %d | %d | %d"
              % (os.path.basename(f), i, r["verdict"], r["families_passed"], r["families_total"],
                 short(r["failed_families"]), r["cases"], len(errs), len(bad)))
        for e in errs:
            print("  ERROR row: family=%s error=%s" % (e.get("family"), short(e.get("error"))))
        fams = {}
        for e in bad:
            fams.setdefault(e["family"], []).append(e)
        for fam, es in sorted(fams.items()):
            print("  FAILING family=%s cases=%d" % (fam, len(es)))
            for e in es:
                print("    want=%s got=%s" % (short(e.get("want")), short(e.get("got"))))
print()
print("r96 family names occurring anywhere in a do-nothing case_log:")
seen = set()
for f in files:
    data = json.load(open(f))
    for r in (data if isinstance(data, list) else [data]):
        for e in r["case_log"]:
            if e["family"] in NEW:
                seen.add(e["family"])
print(sorted(seen) if seen else "NONE")
