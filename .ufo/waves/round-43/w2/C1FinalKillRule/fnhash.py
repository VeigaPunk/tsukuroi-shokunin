#!/usr/bin/env python3
"""Split a bash script into top-level function bodies and sha256 each block.

A top-level function starts at a line matching ^NAME() (column 0).  When the same
line also carries the closing '}' (a one-line function such as
`fixture_mode() { [ -n "$X" ]; }`) the block is that single line.  Otherwise the
block ends at the first following line that is exactly '}' at column 0.  The block,
inclusive of both boundary lines, is hashed verbatim.
"""
import hashlib
import re
import sys

START = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\(\)")


def split(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    lines = raw.splitlines(keepends=True)
    funcs = []
    cur = None
    name = None
    start = None
    for idx, line in enumerate(lines):
        text = line.decode("utf-8", "surrogateescape")
        if cur is None:
            m = START.match(text)
            if not m:
                continue
            name = m.group(1)
            start = idx + 1
            rest = text[m.end():]
            if "}" in rest.split("#", 1)[0]:
                funcs.append((name, start, idx + 1,
                              hashlib.sha256(line).hexdigest(), 1))
                name = None
                start = None
                continue
            cur = [line]
            continue
        cur.append(line)
        if text.rstrip("\r\n") == "}":
            blob = b"".join(cur)
            funcs.append((name, start, idx + 1, hashlib.sha256(blob).hexdigest(), len(cur)))
            cur = None
            name = None
            start = None
    if cur is not None:
        raise SystemExit(f"{path}: unterminated function {name}")
    return funcs


def main():
    base = split(sys.argv[1])
    tip = split(sys.argv[2])
    bmap = {n: (s, e, h, ln) for n, s, e, h, ln in base}
    tmap = {n: (s, e, h, ln) for n, s, e, h, ln in tip}
    order_b = [n for n, *_ in base]
    order_t = [n for n, *_ in tip]
    print(f"# base funcs={len(base)} tip funcs={len(tip)}")
    if len(set(order_b)) != len(order_b) or len(set(order_t)) != len(order_t):
        print("# DUPLICATE FUNCTION NAMES")
    allnames = list(order_t) + [n for n in order_b if n not in tmap]
    allowed = {"inputs_newer_than", "boot_inputs_newer", "run_selftest"}
    changed = []
    for n in allnames:
        b = bmap.get(n)
        t = tmap.get(n)
        if b is None:
            status = "NEW"
        elif t is None:
            status = "REMOVED"
        elif b[2] != t[2]:
            status = "CHANGED"
        else:
            status = "same"
        print(f"{n}\t{status}\tbase_sha={b[2] if b else '-'}\ttip_sha={t[2] if t else '-'}\t"
              f"base_lines={('%d-%d' % (b[0], b[1])) if b else '-'}\t"
              f"tip_lines={('%d-%d' % (t[0], t[1])) if t else '-'}")
        if status != "same":
            changed.append((n, status))
    print("# CHANGED SET:", ", ".join(f"{n}({s})" for n, s in changed) or "(none)")
    bad = [(n, s) for n, s in changed if n not in allowed]
    print("# OUTSIDE ALLOWLIST:", ", ".join(f"{n}({s})" for n, s in bad) or "(none)")
    print("# KILL-RULE-1:", "PASS" if not bad else "FAIL")


main()
