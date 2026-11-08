#!/usr/bin/env python3
"""Emit the round-97 near-miss gate controls: the landed `tools/check-limine-pins.py` with exactly
ONE clause bent. Each substitution must match exactly once (a variant that silently changed nothing
would prove nothing), and the emitted file is what the freeze manifest pins.

N05-z-cap-8             : the component bound is `<= 8` for the THIRD component only (was `<= 9` for
                          every component) -> the r97 family REFUSAL-VERSIONS-9DIGIT-Z fails; the
                          r96 roster certifies only X and Y and is blind to the same bend.
N06-leading-zero-reject : a component whose first digit is `0` is refused (the gate's
                          `parse_limine_version` docstring accepts leading zeros and normalizes via
                          int()) -> LEADING-ZERO-NORMALIZE fails; the r96 roster never sends one.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-97", "before", "controls", "bends")

VARIANTS = {
    "N05-z-cap-8": (
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (len(p) <= 8 or p is not parts[2])) for p in parts):  # N05 (Z bound bent to <=8)",
    ),
    "N06-leading-zero-reject": (
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 and (len(p) == 1 or p[0] != \"0\") for p in parts):  # N06 (leading zeros refused)",
    ),
}


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    os.makedirs(OUT, exist_ok=True)
    for name, (old, new) in VARIANTS.items():
        n = text.count(old)
        if n != 1:
            raise SystemExit("%s: pattern %r matched %d times, expected 1" % (name, old[:60], n))
        out = text.replace(old, new)
        if out == text:
            raise SystemExit("%s: substitution changed nothing" % name)
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        os.chmod(path, 0o755)
        print("wrote %s (%d bytes, one clause bent)" % (path, len(out)))


if __name__ == "__main__":
    main()
