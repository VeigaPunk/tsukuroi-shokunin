#!/usr/bin/env python3
"""r94 MutDigit10: emit ten one-clause mutants of a COPY of the landed gate.

Each mutant applies exactly one textual clause change to the pristine bytes, asserting the
anchor occurs exactly once. Writes into the scratch dir named on argv[1].
"""
import hashlib
import os
import sys

SRC = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py"
EXPECT_SHA = "7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32"

BOUND9 = 'and len(p) <= 9 for p in parts'
COND = ('    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 '
        'for p in parts):\n        return None\n    return tuple(int(p) for p in parts)')
PROBE = ('    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)(?![\\w.-])", p.stdout)\n'
         '    return m.group(1) if m else None')
REFUSE = ('        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)\n'
          '        return 64')
ERA = '    era_b = version >= VISIBILITY_ERA_SPLIT'

MUTANTS = {
    # M01: digit cap widened to ten digits
    "M01-bound-10": [(BOUND9, 'and len(p) <= 10 for p in parts')],
    # M02: suffix guard removed from the probe regex
    "M02-no-suffix-guard": [(PROBE,
        '    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)", p.stdout)\n'
        '    return m.group(1) if m else None')],
    # M03: digit cap widened to eleven digits
    "M03-bound-11": [(BOUND9, 'and len(p) <= 11 for p in parts')],
    # M04: parser deleted, accepts anything
    "M04-accept-any": [(COND, '    return (12, 9, 4)')],
    # M05: the malformed-version usage refusal exits 1 instead of 64
    "M05-usage-rc1": [(REFUSE,
        '        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)\n'
        '        return 1')],
    # M06: probe reads stderr as well as stdout
    "M06-read-stderr": [(PROBE,
        '    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)(?![\\w.-])", p.stdout + p.stderr)\n'
        '    return m.group(1) if m else None')],
    # M07: probe takes the LAST guarded X.Y.Z it finds
    "M07-last-match": [(PROBE,
        '    ms = re.findall(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)(?![\\w.-])", p.stdout)\n'
        '    return ms[-1] if ms else None')],
    # M08: the 12.9.5 split made strict
    "M08-split-strict": [(ERA, '    era_b = version > VISIBILITY_ERA_SPLIT')],
    # M09: the accepted 9-digit boundary (999999999.0.0) made a refusal
    "M09-bound-8": [(BOUND9, 'and len(p) <= 8 for p in parts')],
    # M10: bound widened so the SECOND position is accepted at any length
    "M10-second-unbounded": [(COND,
        '    if len(parts) != 3 or not (\n'
        '            parts[0].isascii() and parts[0].isdigit() and len(parts[0]) <= 9\n'
        '            and parts[1].isascii() and parts[1].isdigit()\n'
        '            and parts[2].isascii() and parts[2].isdigit() and len(parts[2]) <= 9):\n'
        '        return None\n'
        '    return tuple(int(p) for p in parts)')],
}


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    raw = open(SRC, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    assert got == EXPECT_SHA, "pristine gate hash %s != %s" % (got, EXPECT_SHA)
    text = raw.decode()
    for name, edits in MUTANTS.items():
        body = text
        for old, new in edits:
            assert body.count(old) == 1, "%s: anchor count %d for %r" % (name, body.count(old), old[:40])
            body = body.replace(old, new)
        path = os.path.join(outdir, name + ".py")
        open(path, "w").write(body)
        compile(body, path, "exec")
        print("%s %s" % (hashlib.sha256(body.encode()).hexdigest(), path))
    # also a byte-identical control copy under this seat (never the landed gate)
    ctl = os.path.join(outdir, "M00-pristine-copy.py")
    open(ctl, "wb").write(raw)
    print("%s %s" % (got, ctl))


if __name__ == "__main__":
    main()
