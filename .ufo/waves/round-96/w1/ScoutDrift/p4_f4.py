#!/usr/bin/env python3
"""ScoutDrift P4: the frozen C2 checker's F4 clause-2 blind spot on the LANDED tree.

F4 has two clauses:
  clause 1: "r94 family roster" must be in README   (the scope sentence)
  clause 2: "before instrument has no in-bound" must NOT be in README  (the over-scope sentence)

Clause 2 is a RAW substring test. The r95 README wraps that sentence across a newline
("the before instrument has no\\nin-bound 9-digit case"), so the raw substring is absent.
Test: a tree that HAS the scope sentence AND a wrapped over-scope sentence -> does F4 fire?
"""
import importlib.util
import json
import os
import shutil
import tempfile

SCRATCH = "/fast/scratch/hyaku/tsukuroi-r96/ScoutDrift"
spec = importlib.util.spec_from_file_location("frozenchk2", os.path.join(SCRATCH, "frozen-check-r96-calibration.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

base = tempfile.mkdtemp(prefix="scoutdrift-p4-", dir=SCRATCH)
out = []
try:
    rp = mod._fixture(base)
    f0, _ = mod.check(base, rp)
    out.append("clean fixture                        -> findings %s" % [x[0] for x in f0])

    # case 1: over-scope sentence on ONE line (the selftest F4 mutant's shape)
    d1 = tempfile.mkdtemp(prefix="p4-oneline-", dir=base)
    shutil.copytree(base, d1, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p4-*", "p4-*"))
    mod._edit(d1, "corpus/README.md", "The r94 family roster has no", "The before instrument has no")
    f1, _ = mod.check(d1, os.path.join(d1, "report.md"))
    out.append("over-scope on ONE line              -> findings %s" % [x[0] for x in f1])

    # case 2: scope sentence present AND over-scope sentence WRAPPED (the repo's real shape)
    d2 = tempfile.mkdtemp(prefix="p4-wrapped-", dir=base)
    shutil.copytree(base, d2, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p4-*", "p4-*"))
    with open(os.path.join(d2, "corpus/README.md"), "w") as f:
        f.write("The r94 family roster has no in-bound 9-digit case.\n"
                "The before instrument has no\n"
                "in-bound 9-digit case.\n")
    f2, _ = mod.check(d2, os.path.join(d2, "report.md"))
    out.append("scope present + over-scope WRAPPED   -> findings %s  <== blind spot if []" % [x[0] for x in f2])
    out.append("   detail rows: %s" % [x[1] for x in f2])

    # case 3: same but over-scope on one line, scope sentence ALSO present
    d3 = tempfile.mkdtemp(prefix="p4-both-", dir=base)
    shutil.copytree(base, d3, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p4-*", "p4-*"))
    with open(os.path.join(d3, "corpus/README.md"), "w") as f:
        f.write("The r94 family roster has no in-bound 9-digit case.\n"
                "The before instrument has no in-bound 9-digit case.\n")
    f3, _ = mod.check(d3, os.path.join(d3, "report.md"))
    out.append("scope present + over-scope ONE line -> findings %s" % [x[0] for x in f3])
finally:
    shutil.rmtree(base, ignore_errors=True)

print("\n".join(out))
with open(os.path.join(SCRATCH, "p4-f4-blindspot.txt"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\nwrote %s/p4-f4-blindspot.txt" % SCRATCH)
