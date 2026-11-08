#!/usr/bin/env python3
"""ScribeKnowledge round-96 receipt: the roster delta 99 -> 103 and the four-component class's
prior sampling. Read-only; prints what a reader can re-run."""
import ast
import collections
import re

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"


def roster(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"FAMILY_ROSTER\s*=\s*\(", src)
    i = m.end() - 1
    depth = 0
    for j in range(i, len(src)):
        if src[j] == "(":
            depth += 1
        elif src[j] == ")":
            depth -= 1
            if depth == 0:
                return ast.literal_eval(src[i:j + 1])
    raise AssertionError("roster not closed")


r95 = roster(LANE + "/tools/limine-pin-battery-r95.py")
r96 = roster(LANE + "/tools/limine-pin-battery-r96.py")
print("r95 FAMILY_ROSTER: len=%d unique=%d" % (len(r95), len(set(r95))))
print("r96 FAMILY_ROSTER: len=%d unique=%d" % (len(r96), len(set(r96))))
print("r95 duplicates:", [k for k, v in collections.Counter(r95).items() if v > 1])
print("r96 duplicates:", [k for k, v in collections.Counter(r96).items() if v > 1])
print("added in r96:", [f for f in r96 if f not in set(r95)])
print("removed from r95:", [f for f in r95 if f not in set(r96)])

# the four-component class's prior sampling (the r95 Frontier correction)
r95src = open(LANE + "/tools/limine-pin-battery-r95.py", encoding="utf-8").read()
print()
print("r95 REFUSAL_VERSIONS roster line:")
for n, line in enumerate(r95src.splitlines(), 1):
    if line.startswith("REFUSAL_VERSIONS = "):
        print("  %d: %s" % (n, line.strip()))
        break
print("r95 '12.9.5.1' occurrences: %d" % r95src.count("12.9.5.1"))
print("r95 '12.9.6.1' occurrences: %d (usage_check only, not a family roster):"
      % r95src.count("12.9.6.1"))
for n, line in enumerate(r95src.splitlines(), 1):
    if "12.9.6.1" in line:
        print("  %d: %s" % (n, line.strip()[:120]))
