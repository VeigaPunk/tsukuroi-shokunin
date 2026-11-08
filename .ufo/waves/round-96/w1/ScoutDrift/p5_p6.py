#!/usr/bin/env python3
"""ScoutDrift P5: does the FROZEN C2 checker's F3 clause 1 ('largest in-bound' must be absent)
have the same newline-wrap blind spot that P4 demonstrated for F4 clause 2?

F3 clause 1 is `"largest in-bound" in text` -> if the phrase is re-introduced wrapped across a
newline ("largest in-\\nbound"), the raw substring test cannot see it.
Also P6: does the README's pointer "considerthese/2026-10-26.md #22" resolve in THIS lane's copy?
"""
import importlib.util
import os
import shutil
import tempfile

SCRATCH = "/fast/scratch/hyaku/tsukuroi-r96/ScoutDrift"
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
spec = importlib.util.spec_from_file_location("frozenchk3", os.path.join(SCRATCH, "frozen-check-r96-calibration.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
out = []

base = tempfile.mkdtemp(prefix="scoutdrift-p5-", dir=SCRATCH)
try:
    rp = mod._fixture(base)
    f0, _ = mod.check(base, rp)
    out.append("clean fixture                       -> findings %s" % [x[0] for x in f0])

    # F3 clause 1: re-introduce 'largest in-bound' WRAPPED across a newline
    d = tempfile.mkdtemp(prefix="p5-f3wrapped-", dir=base)
    shutil.copytree(base, d, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p5-*", "p5-*"))
    p = os.path.join(d, "tools/limine-pin-battery-r95.py")
    t = open(p).read()
    assert "a boundary member" in t
    open(p, "w").write(t.replace("a boundary member", "the largest in-\nbound member", 1))
    f, _ = mod.check(d, os.path.join(d, "report.md"))
    out.append("F3 clause 1, phrase WRAPPED         -> findings %s  <== blind spot if []" % [x[0] for x in f])

    # F3 clause 1, phrase on one line (control)
    d2 = tempfile.mkdtemp(prefix="p5-f3oneline-", dir=base)
    shutil.copytree(base, d2, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p5-*", "p5-*"))
    p2 = os.path.join(d2, "tools/limine-pin-battery-r95.py")
    t2 = open(p2).read()
    open(p2, "w").write(t2.replace("a boundary member", "the largest in-bound member", 1))
    f2, _ = mod.check(d2, os.path.join(d2, "report.md"))
    out.append("F3 clause 1, phrase on ONE line     -> findings %s" % [x[0] for x in f2])
finally:
    shutil.rmtree(base, ignore_errors=True)

out.append("")
out.append("P6: does 'considerthese/2026-10-26.md #22' resolve in THIS lane's copy?")
cp = os.path.join(LANE, "considerthese/2026-10-26.md")
text = open(cp).read()
out.append("   file exists: %s  sha256 %s" % (os.path.isfile(cp),
            __import__("hashlib").sha256(open(cp, "rb").read()).hexdigest()))
out.append("   numbered items in it: %d" % len([l for l in text.splitlines()
                                               if l[:1].isdigit() and l[1:2] == "."]))
out.append("   'Self-improvement ideas' bullets: %d" % text.count("\n- **"))
out.append("   an item numbered 22 present: %s" % ("22." in text))
out.append("   README pointer: %s" % [l.strip() for l in
            open(os.path.join(LANE, "corpus/README.md")).read().splitlines()
            if "2026-10-26.md #22" in l][:1])

print("\n".join(out))
open(os.path.join(SCRATCH, "p5-p6.txt"), "w").write("\n".join(out) + "\n")
print("\nwrote %s/p5-p6.txt" % SCRATCH)
