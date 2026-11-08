#!/usr/bin/env python3
"""Emit the round-98 near-miss gate controls: the landed `tools/check-limine-pins.py` with exactly
ONE clause bent. Each substitution must match exactly once (a variant that silently changed nothing
would prove nothing), and the emitted file is what the freeze manifest pins.

N07-era-field-lie         : the reported `visibility_era` label is swapped exactly when the version
                          spelling has a 9-digit third component or a leading-zero component (the
                          r97 Z and LZ spellings); pins stay correct. The r98 families
                          REFUSAL-VERSIONS-9DIGIT-Z and LEADING-ZERO-NORMALIZE both set
                          check_era, so both fail; EXPLICIT-VERSION-ERA's members carry neither
                          spelling and pass.
N08-echo-norm             : the echoed `limine_version` is normalized to the numeric tuple
                          (`12.09.4` echoes `12.9.4`). Only LEADING-ZERO-NORMALIZE sets check_echo
                          on such a spelling, so only it fails; EXPLICIT-VERSION-ECHO's members
                          have no leading zeros and pass.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-98", "before", "controls", "bends")

VARIANTS = {
    "N07-era-field-lie": (
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n            "limine_version": limine_version,\n            "limine_version_source": limine_version_source,\n            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n            "limine_version": limine_version,\n            "limine_version_source": limine_version_source,\n            "visibility_era": (("pre-12.9.5" if era_b else "12.9.5+") if (len(limine_version.split(".")[2]) == 9 or any(len(p) > 1 and p.startswith("0") for p in limine_version.split("."))) else ("12.9.5+" if era_b else "pre-12.9.5")),  # N07 (era label lies for Z/LZ spellings only, r98)',
    ),
    "N08-echo-norm": (
        '    era_b = version >= VISIBILITY_ERA_SPLIT',
        '    era_b = version >= VISIBILITY_ERA_SPLIT\n    limine_version = ".".join(str(x) for x in version)  # N08 (echo normalized, r98)',
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
