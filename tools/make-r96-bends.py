#!/usr/bin/env python3
"""Emit the round-96 near-miss gate controls: the landed `tools/check-limine-pins.py` with exactly
ONE clause bent. Each substitution must match exactly once (a variant that silently changed nothing
would prove nothing), and the emitted file is what the freeze manifest pins.

N01-echo-wrong        : the JSON's `limine_version` for an explicit `--limine-version` answers
                        `99.9.9` (was the flag's value) -> the r96 family EXPLICIT-VERSION-META fails;
                        the r95 roster compared the echo only on AUTO cases and read it met 99/99.
N02-y-cap-8           : the component bound is `<= 8` for the SECOND component only (was `<= 9` for
                        every component) -> the r96 family REFUSAL-VERSIONS-9DIGIT-Y fails; the r95
                        accepted leg certifies only X and is blind.
N03-era-label-flip    : the main return's `visibility_era` label is inverted (was selected from the
                        version) -> EXPLICIT-VERSION-META fails on the era assertion; the r95 roster
                        never read the field.
N04-extra-components  : the grammar check is `len(parts) < 3` (was `!= 3`), so a four-component
                        version is accepted -> EXTRA-COMPONENT fails; the r95 roster never sent one.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-96", "before", "controls", "bends")

VARIANTS = {
    "N01-echo-wrong": (
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n',
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": "99.9.9" if limine_version_source == "flag" else limine_version,'
        '  # N01 (echo bent)\n',
    ),
    "N02-y-cap-8": (
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and (len(p) <= 8 or p is not parts[1])) for p in parts):  # N02 (Y bound bent to <=8)",
    ),
    "N03-era-label-flip": (
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",\n'
        '            "hash_mismatch_panic":',
        '            "visibility_era": "pre-12.9.5" if era_b else "12.9.5+",  # N03 (label bent)\n'
        '            "hash_mismatch_panic":',
    ),
    "N04-extra-components": (
        "    if len(parts) != 3 or not all(",
        "    if len(parts) < 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):  # N04",
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
