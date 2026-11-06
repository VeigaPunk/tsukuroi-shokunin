#!/usr/bin/env python3
"""Build round-87 battery mutants from the pristine clone copy. Each replacement must hit exactly once."""
import os
import sys

S = "/fast/scratch/hyaku/tsukuroi-r87/MutBattery"
SRC = os.path.join(S, "lane", "tools", "limine-pin-battery-r87.py")
OUT = os.path.join(S, "lane", "tools")

BASE_OK = ('            ok = got is not None and got[0] == want[0] and got[3] == want[0] '
           'and got[1] == want[1] and [list(x) for x in got[2]] == [list(x) for x in want[2]]\n')
PASSED = '            log.append({"family": fam, "passed": ok,\n'
LANE = '        lane = os.path.dirname(HERE)\n'
HERE = 'HERE = os.path.dirname(os.path.abspath(__file__))\n'
HOSTSHAPE = '    "HOST-SHAPE": fam_host_shape,\n'

MUTANTS = {
    # M1: comparison never true -> nothing can read met
    "m1-never-met": [(BASE_OK, '            ok = False  # MUT-M1 never-met\n')],
    # M2: comparison always true -> any gate reads met
    "m2-always-met": [(BASE_OK, '            ok = True  # MUT-M2 always-met\n')],
    # M3: one family's expectation skipped (always counted as passed)
    "m3-family-skipped": [(PASSED, '            log.append({"family": fam, "passed": (ok or fam == "MULTI-FAULT"),\n')],
    # M4: family set shrunk to 21
    "m4-families-21": [(HOSTSHAPE, '    # MUT-M4: HOST-SHAPE family removed (21 total)\n')],
    # M5: rc ignored (neither process exit code nor out["rc"] compared)
    "m5-ignore-rc": [(BASE_OK, '            ok = got is not None and got[1] == want[1] '
                               'and [list(x) for x in got[2]] == [list(x) for x in want[2]]  # MUT-M5 ignore-rc\n')],
    # M6: consequence ignored
    "m6-ignore-consequence": [(BASE_OK, '            ok = got is not None and got[0] == want[0] and got[3] == want[0] '
                                         'and got[1] == want[1] and [list(x)[:2] for x in got[2]] == '
                                         '[list(x)[:2] for x in want[2]]  # MUT-M6 ignore-consequence\n')],
    # M7: line numbers ignored
    "m7-ignore-line": [(BASE_OK, '            ok = got is not None and got[0] == want[0] and got[3] == want[0] '
                                 'and got[1] == want[1] and sorted([x[1:] for x in got[2]]) == '
                                 'sorted([x[1:] for x in want[2]])  # MUT-M7 ignore-line\n')],
    # M8: reference gate path taken from the invocation cwd (captured at import)
    "m8-ref-from-cwd": [(HERE, HERE + '_START_CWD = os.getcwd()  # MUT-M8 invocation cwd\n'),
                        (LANE, '        lane = _START_CWD  # MUT-M8 ref path from cwd\n')],
    # M8b: reference gate path from cwd at resolve time (inside selftest's chdir)
    "m8b-ref-from-cwd-late": [(LANE, '        lane = os.getcwd()  # MUT-M8b ref path from cwd at resolve time\n')],
}

base = open(SRC, "rb").read()
for name, reps in MUTANTS.items():
    text = base
    for old, new in reps:
        ob, nb = old.encode(), new.encode()
        n = text.count(ob)
        if n != 1:
            sys.exit("BUILD FAIL %s: anchor count %d for %r" % (name, n, old[:70]))
        text = text.replace(ob, nb)
    dst = os.path.join(OUT, "limine-pin-battery-r87-%s.py" % name)
    with open(dst, "wb") as f:
        f.write(text)
    print("wrote", dst, len(text))
