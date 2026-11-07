#!/usr/bin/env python3
"""Generate single-point mutants of the pristine r89 battery (lane bytes), compile-check each.

Every mutation is a literal, counted text replacement (or a counted token deletion) on the
pristine source; the script fails loudly if a mutation site moved.
"""
import hashlib
import os
import py_compile
import re
import sys

S = os.environ["S"]
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SRC = os.path.join(LANE, "tools", "limine-pin-battery-r89.py")
OUT = os.path.join(S, "mut", "src")

R89_FAMILIES = ["BLANK-CLASS", "OPTIONAL-MISSING", "OPTIONAL-UNRESOLVED", "EMPTY-PIN-LIST",
                "DOUBLE-DOLLAR", "ENTRY-LABEL-EDGES", "PANIC-VALUE-BLANKS", "CR-INTERNAL",
                "RESOURCE-CASE", "KEY-EQUALS", "EMPTY-PATH", "OPTIONAL-KEY-CASE"]

with open(SRC) as f:
    BASE = f.read()


def sub1(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("mutation %s: anchor occurs %d times: %r" % (label, n, old[:80]))
    return text.replace(old, new, 1)


def del_family(name):
    t = BASE
    m = re.search(r'\n    "%s": fam_[a-z_]+,\n' % re.escape(name), t)
    if not m:
        raise SystemExit("FAMILIES entry missing for " + name)
    t = t[:m.start()] + "\n" + t[m.end():]
    m = re.search(r'"%s", ?' % re.escape(name), t)
    if not m:
        raise SystemExit("FAMILY_ROSTER entry missing for " + name)
    t = t[:m.start()] + t[m.end():]
    return t


MUTANTS = {}

for fam in R89_FAMILIES:
    MUTANTS["del-" + fam.lower()] = del_family(fam)

# r8_ok: value comparison weakened to a line-only comparison (the r88 MutBattery M18 field).
MUTANTS["r8ok-value-weakened"] = sub1(
    BASE,
    '    return (isinstance(pm, dict) and pm.get("line") == want_panic[0]\n'
    '            and str(pm.get("value", "")).lower() == want_panic[1].lower())',
    '    return isinstance(pm, dict) and pm.get("line") == want_panic[0]',
    "r8ok-value")

# r88 draw restored: CRLF only with p 0.6.
MUTANTS["crlf-p06-r88"] = sub1(
    BASE,
    '    c.eol = "\\r\\n"  # r89: every case (r88 drew CRLF with p 0.6; routed R88-R2)',
    '    if c.rng.random() < 0.6:\n        c.eol = "\\r\\n"',
    "crlf-p06")

# extra 5
MUTANTS["drop-exitcode-compare"] = sub1(
    BASE,
    '            ok = (got is not None and got[0] == want[0] and got[3] == want[0] and got[1] == want[1]',
    '            ok = (got is not None and got[3] == want[0] and got[1] == want[1]',
    "exitcode")

MUTANTS["ignore-consequence"] = sub1(
    BASE,
    'and [list(x) for x in got[2]] == [list(x) for x in want[2]] and r8_ok(c, got))',
    'and [(x[0], x[1]) for x in got[2]] == [(x[0], x[1]) for x in want[2]] and r8_ok(c, got))',
    "consequence")

MUTANTS["cases-per-family-1"] = sub1(
    BASE, "CASES_PER_FAMILY = 4", "CASES_PER_FAMILY = 1", "cases1")

MUTANTS["r8ok-no-entry-check"] = sub1(
    BASE,
    '    for ln, label in got[4].items():\n'
    '        if ln not in want_entries or label != want_entries[ln]:\n'
    '            return False\n',
    '',
    "r8ok-entry")

MUTANTS["r8ok-no-panic-line-check"] = sub1(
    BASE,
    '    return (isinstance(pm, dict) and pm.get("line") == want_panic[0]\n'
    '            and str(pm.get("value", "")).lower() == want_panic[1].lower())',
    '    return (isinstance(pm, dict)\n'
    '            and str(pm.get("value", "")).lower() == want_panic[1].lower())',
    "r8ok-panic-line")


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for name, src in sorted(MUTANTS.items()):
        if src == BASE:
            raise SystemExit("mutant %s is identical to the pristine source" % name)
        p = os.path.join(OUT, name + ".py")
        with open(p, "w") as f:
            f.write(src)
        py_compile.compile(p, doraise=True)
        with open(p, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        with open(os.path.join(OUT, name + ".sha256"), "w") as f:
            f.write(h + "  " + p + "\n")
        made.append((name, h, len(src)))
    with open(os.path.join(OUT, "index.txt"), "w") as f:
        f.write("base_sha256  %s  %s\n" % (hashlib.sha256(BASE.encode()).hexdigest(), SRC))
        f.write("base_bytes   %d\n" % len(BASE))
        for name, h, n in made:
            f.write("%-28s %s %d\n" % (name, h, n))
    print("MUTANTS %d" % len(made))
    for name, h, n in made:
        print("%-28s %s" % (name, h[:16]))


if __name__ == "__main__":
    main()
