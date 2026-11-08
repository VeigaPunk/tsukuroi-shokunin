#!/usr/bin/env python3
"""Emit the round-95 near-miss gate control: the landed `tools/check-limine-pins.py` with exactly
ONE clause bent. Each substitution must match exactly once (a variant that silently changed nothing
would prove nothing), and the emitted file is what the freeze manifest pins.

N05 strict-8     : the component bound is `<= 8` (was `<= 9`) -> the gate refuses a boundary member
                   (first component at the cap) of its own published 1-9-digit cap
                   (`999999999.9.9`). The r94
                   roster has no case whose version is an in-bound 9-digit value, so this bend read
                   `met` 98/98 there; the r95 family `REFUSAL-VERSIONS-9DIGIT` must fail on it.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-95", "before", "controls", "bends")

VARIANTS = {
    "N05-strict-8": (
        "and len(p) <= 9 for p in parts):",
        "and len(p) <= 8 for p in parts):  # N05 (bound bent to <=8)",
    ),
}


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    os.makedirs(OUT, exist_ok=True)
    for name, (old, new) in VARIANTS.items():
        n = text.count(old)
        if n != 1:
            raise SystemExit("%s: pattern %r matched %d times, expected 1" % (name, old, n))
        out = text.replace(old, new)
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        os.chmod(path, 0o755)
        print("wrote %s (%d bytes, one clause bent)" % (path, len(out)))


if __name__ == "__main__":
    main()
