#!/usr/bin/env python3
"""ScoutDrift consolidated receipts for round 96 w1.

Every number in the report comes from this script's output (plus the sibling
receipt files written alongside it).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-96/w1/ScoutDrift")
os.makedirs(SEAT, exist_ok=True)
out = []


def say(*a):
    line = " ".join(str(x) for x in a)
    out.append(line)
    print(line)


def sh(cmd, cwd=LANE):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


say("### R1 — freeze manifest at HEAD (sha256sum -c)")
rc, so, se = sh("sha256sum -c .ufo/waves/round-96/before/instruments.sha256")
ok = so.count(": OK")
say("exit=%d  OK-lines=%d  FAILED-lines=%d" % (rc, ok, so.count("FAILED")))
for ln in so.splitlines():
    if not ln.endswith(": OK"):
        say("   non-OK: %s" % ln)
say("HEAD=%s" % sh("git rev-parse HEAD")[1].strip())

say("")
say("### R2 — C1/C2 sentence comparison (claims.json vs plan vs before/plan-frozen.md)")
rc, so, se = sh("python3 /fast/scratch/hyaku/tsukuroi-r96/ScoutDrift/cmp_claims.py")
say("exit=%d" % rc)
for ln in so.splitlines():
    say("   " + ln)

say("")
say("### R3 — plan vs before/plan-frozen.md byte equality")


def shasha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


a = shasha(os.path.join(LANE, ".ufo/plans/round-96.md"))
b = shasha(os.path.join(LANE, ".ufo/waves/round-96/before/plan-frozen.md"))
say("plan sha256      = %s" % a)
say("plan-frozen sha256 = %s" % b)
say("byte-identical: %s" % (a == b))

say("")
say("### R4 — the amendment file: where A1..A5 live vs the plan's Amendment slot")
rc, so, se = sh("ls .ufo/waves/round-96/before/plan-amendments-A1-A2.md 2>&1")
say("amendments file exists: %s" % so.strip())
rc, so, se = sh("grep -c '^### A[0-9]' .ufo/waves/round-96/before/plan-amendments-A1-A2.md")
say("amendment headings in that file: %s (file name says A1-A2)" % so.strip())
rc, so, se = sh("sed -n '/## Amendment slot/,$p' .ufo/plans/round-96.md | grep -c '^### A[0-9]'")
say("amendment headings in the plan's Amendment slot: %s (plan bytes still == frozen)" % so.strip())
rc, so, se = sh("grep -rn '^### A[0-9]' .ufo/waves/round-95/before/ .ufo/plans/round-95.md 2>/dev/null | head -5")
say("r95 precedent (amendments in plan or before/): %s" % (so.strip() or "(none found)"))

say("")
say("### R5 — r95 Frontier sentence vs the roster that already sampled a four-component value")
rc, so, se = sh("grep -n 'REFUSAL_VERSIONS = ' -A3 tools/limine-pin-battery-r96.py")
say("r96 battery REFUSAL_VERSIONS:")
for ln in so.splitlines():
    say("   " + ln)
rc, so, se = sh("grep -n 'REFUSAL_VERSIONS = ' -A3 tools/limine-pin-battery-r95.py")
say("r95 battery REFUSAL_VERSIONS (pre-r96 roster):")
for ln in so.splitlines():
    say("   " + ln)
rc, so, se = sh("grep -n '12\\.9\\.5\\.1' corpus/knowledge/limine-bound-9digit-r95.md corpus/lessons/round-96.md | cut -c1-200")
say("the lane's own r95 knowledge entry and r96 lesson naming 12.9.5.1:")
for ln in so.splitlines():
    say("   " + ln)

say("")
say("### R6 — roster sizes (99 -> 103) by my own parse")
for p in ("tools/limine-pin-battery-r95.py", "tools/limine-pin-battery-r96.py"):
    t = open(os.path.join(LANE, p)).read()
    m = re.search(r"FAMILY_ROSTER = \((.*?)\n\)", t, re.S)
    fams = re.findall(r'"([A-Z0-9\-]+)"', m.group(1))
    say("%-38s roster=%d unique=%d" % (p, len(fams), len(set(fams))))
    new = [f for f in fams if f in ("EXPLICIT-VERSION-ECHO", "EXPLICIT-VERSION-ERA",
                                    "REFUSAL-VERSIONS-9DIGIT-Y", "EXTRA-COMPONENT")]
    if new:
        say("   the four new names present: %s" % ", ".join(new))

say("")
say("### R7 — component counts of the EXTRA-COMPONENT members (docstring says 'fourth component')")
t = open(os.path.join(LANE, "tools/limine-pin-battery-r96.py")).read()
m = re.search(r"EXTRA_COMPONENT_VALUES = \((.*?)\)", t, re.S)
for v in re.findall(r'"([^"]+)"', m.group(1)):
    say("   %-12s components=%d" % (v, len(v.split("."))))

say("")
say("### R8 — the landed README Frontier bullet vs that code")
rc, so, se = sh("grep -n 'EXTRA-COMPONENT` enumerates' -A1 corpus/README.md")
for ln in so.splitlines():
    say("   " + ln)

say("")
say("### R9 — 'sampled once' vs 'twice' in the two landed corpus files")
rc, so, se = sh("grep -n 'sampled once' corpus/README.md | cut -c1-200")
say("README: " + so.strip())
rc, so, se = sh("grep -n 'sampled before this round' corpus/knowledge/limine-bound-per-component-r96.md | cut -c1-240")
say("knowledge entry: " + so.strip())

say("")
say("### R10 — considerthese/2026-10-26.md proposal sweep (status + landing)")
rc, so, se = sh("grep -n '^- \\*\\*\\|^## ' considerthese/2026-10-26.md | cut -c1-150")
for ln in so.splitlines():
    say("   " + ln)
for label, pat in (("burst-aware reading", "r46.md|QUALITY 112"),
                   ("counter-attack scoreboard", "r82.md"),
                   ("seat-harm incident log", "r79.md"),
                   ("patch-offset check", "r42.md"),
                   ("correction propagation map", "r43.md")):
    rc, so, se = sh("grep -ln 'considerthese/2026-10-26.md' corpus/lessons/*.md | tr '\\n' ' '")
    say("   %-32s lessons mentioning the file: %s" % (label, so.strip()[:120]))
rc, so, se = sh("for f in corpus/lessons/round-8[5-9].md corpus/lessons/round-9[0-6].md; do printf '%s %s\\n' \"$(basename $f)\" \"$(grep -ci 'scoreboard' $f)\"; done")
say("   scoreboard mentions per lesson r85..r96:")
for ln in so.splitlines():
    say("      " + ln)
rc, so, se = sh("for f in corpus/lessons/round-8[6-9].md corpus/lessons/round-9[0-6].md; do printf '%s %s\\n' \"$(basename $f)\" \"$(grep -c 'Seat harm' $f)\"; done")
say("   'Seat harm' tables per lesson r86..r96 (QUALITY 110 says every round lesson carries one):")
for ln in so.splitlines():
    say("      " + ln)

say("")
say("### R11 — the four new families' docstrings vs their code")
rc, so, se = sh("sed -n '1751,1795p' tools/limine-pin-battery-r96.py")
for ln in so.splitlines():
    say("   " + ln)

with open(os.path.join(SEAT, "receipts.txt"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\nWROTE %s/receipts.txt" % SEAT)
