#!/usr/bin/env python3
"""Contract probes: R8 "MAY" clauses vs what the r89 battery actually enforces.

p01 omits the optional per-pin "entry" field  (R8: MAY carry)
p02 omits the optional top-level "hash_mismatch_panic" (R8: MAY carry)
p03 emits pins in reverse line order          (battery compares sorted per-pin triples)
p04 adds extra keys, top level and per pin    (R8: other extra keys allowed and ignored)

A probe failing under --runs 3 is a battery/contract contradiction, not a docstring bend.
"""
import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base.py")

P = [
    ("p01_omit_entry", "R8 a pin record MAY carry 'entry'",
     'pins.append({"line": n, "status": status,\n                                 "consequence": cons, "entry": last_entry})',
     'pins.append({"line": n, "status": status,\n                                 "consequence": cons})'),
    ("p02_omit_hmp", "R8 the top-level object MAY carry 'hash_mismatch_panic'",
     '        "pins": pins,\n        "hash_mismatch_panic": None if first_hmp is None else\n        {"line": first_hmp[0], "value": first_hmp[1]},\n    }',
     '        "pins": pins,\n    }'),
    ("p03_reversed_pins", "battery compares sorted per-pin (line, status, consequence)",
     '        "pins": pins,',
     '        "pins": list(reversed(pins)),'),
    ("p04_extra_keys", "R8 other extra keys are allowed and ignored",
     '        "pins": pins,',
     '        "pins": [dict(p, ignored_key=1) for p in pins], "ignored_key": {"x": 2},'),
]


def main():
    with open(BASE, encoding="utf-8") as f:
        base = f.read()
    diffs = []
    for name, clause, old, new in P:
        if base.count(old) != 1:
            print("BAD ANCHOR %s count=%d" % (name, base.count(old)), file=sys.stderr)
            return 1
        text = base.replace(old, new)
        with open(os.path.join(HERE, "fx_%s.py" % name), "w", encoding="utf-8") as f:
            f.write(text)
        diffs.append("".join(difflib.unified_diff(base.splitlines(True), text.splitlines(True),
                                                  fromfile="base.py", tofile="fx_%s.py" % name, n=2)))
    with open(os.path.join(HERE, "probes.diff"), "w", encoding="utf-8") as f:
        f.write("\n".join(diffs))
    print("wrote %d probes" % len(P))
    return 0


if __name__ == "__main__":
    sys.exit(main())
