#!/usr/bin/env python3
"""ScoutDrift probes for round 96.

P1: era arithmetic under whole-tuple vs first-component-only rules, for every
    version the r96 battery sends.
P2: component counts of every EXTRA_COMPONENT_VALUES member.
P3: frozen C2 checker blind-spot probe: does the frozen F4 over-scope clause
    fire when the over-scoped sentence is wrapped across a newline (as the real
    README wraps it)?
"""
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r96/ScoutDrift"
SPLIT = (12, 9, 5)

out = []


def say(*a):
    line = " ".join(str(x) for x in a)
    out.append(line)
    print(line)


say("== P1: era selection under two rules ==")
META = ("12.9.4", "12.9.5", "12.9.6", "9" * 9 + ".9.9")
Y = ("12.999999999.4", "0.999999999.0")
EXTRA = ("12.9.6.1", "12.9.6.1.0", "12.9.6.99", "12.9.6.7")
for label, versions in (("EXPLICIT_VERSION_META", META), ("Y_DIGIT9", Y)):
    for v in versions:
        t = tuple(int(p) for p in v.split("."))
        whole = t >= SPLIT
        xonly = t[0] >= SPLIT[0]
        yonly = t[1] >= SPLIT[1]
        maxonly = max(t) >= SPLIT[0]
        say("  %-20s v=%-16s whole=%-5s -> %-11s | X-only=%-5s -> %-11s | Y-only=%-5s -> %-11s | max-only=%s"
            % (label, v, whole, "12.9.5+" if whole else "pre-12.9.5",
               xonly, "12.9.5+" if xonly else "pre-12.9.5",
               yonly, "12.9.5+" if yonly else "pre-12.9.5", maxonly))
say("  note: battery code uses the whole tuple (Case.era_b: tuple(int(p) for p in version.split('.')) >= (12,9,5))")
say("  note: gate code uses the whole tuple (check(): era_b = version >= VISIBILITY_ERA_SPLIT, version = parse_limine_version(flag))")
say("  verdict: a rule reading ONLY the first component gives the SAME label as the whole tuple for")
say("           every META version and for every Y version, so the Y family's docstring sentence")
say("           ('reads the era from X alone answers era B for 0.999999999.0') is not satisfiable")
say("           by a first-component-only rule (X=0 cannot yield era B); the rule that yields era B")
say("           for 0.999999999.0 is a second-component(Y)-only or max-component rule.")

say("")
say("== P2: component counts of the EXTRA-COMPONENT members ==")
for v in EXTRA:
    say("  %-12s components=%d %s" % (v, len(v.split(".")), v.split(".")))
say("  gate grammar: parse_limine_version requires len(parts)==3 -> every member above is refused rc 64")
say("  NOTE: '12.9.6.1.0' has 5 components, not 4: the family is named EXTRA-COMPONENT and its")
say("        docstring calls all four members 'a version with a fourth component'.")

say("")
say("== P3: frozen C2 checker F4 over-scope clause vs a newline-wrapped sentence ==")
spec = importlib.util.spec_from_file_location("frozenchk", os.path.join(SCRATCH, "frozen-check-r96-calibration.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
base = tempfile.mkdtemp(prefix="scoutdrift-p3-", dir=SCRATCH)
try:
    rp = mod._fixture(base)
    clean, _ = mod.check(base, rp)
    say("  clean fixture findings: %s" % (clean,))
    # one-line over-scope sentence (what the selftest F4 mutant writes)
    d1 = tempfile.mkdtemp(prefix="p3-oneline-", dir=base)
    shutil.copytree(base, d1, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p3-*", "p3-*"))
    mod._edit(d1, "corpus/README.md", "The r94 family roster has no",
              "The before instrument has no")
    f1, _ = mod.check(d1, os.path.join(d1, "report.md"))
    say("  one-line over-scope README -> findings: %s" % ([x[0] for x in f1],))
    # newline-wrapped over-scope sentence (how the real README wraps it)
    d2 = tempfile.mkdtemp(prefix="p3-wrapped-", dir=base)
    shutil.copytree(base, d2, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("scoutdrift-p3-*", "p3-*"))
    with open(os.path.join(d2, "corpus/README.md"), "w") as f:
        f.write("The before instrument has no\nin-bound 9-digit case.\n")
    f2, _ = mod.check(d2, os.path.join(d2, "report.md"))
    say("  newline-wrapped over-scope README -> findings: %s" % ([x[0] for x in f2],))
    say("  verdict: frozen F4 second clause is a raw substring test; a wrapped sentence is invisible to it.")
finally:
    shutil.rmtree(base, ignore_errors=True)

with open(os.path.join(SCRATCH, "probe-output.txt"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\nwrote %s/probe-output.txt" % SCRATCH)
