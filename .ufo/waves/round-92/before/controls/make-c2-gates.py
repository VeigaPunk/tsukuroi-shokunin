#!/usr/bin/env python3
"""Emit the round-92 C2 near-miss gate controls: the candidate `tools/check-limine-pins.py` with
exactly ONE v92 clause bent. Each substitution must match exactly once (a variant that silently
changed nothing would prove nothing), and the emitted file is what the freeze manifest pins.

N01 era-flat-a : era_b forced False  -> the 12.9.5+ families must fail (ERA-FLE-PANIC-B,
                 ERA-FLE-MEASURED-B), the pre-12.9.5 ones must still pass.
N02 era-flat-b : era_b forced True   -> the pre-12.9.5 families and ERA-DEFAULT must fail.
N03 default-b  : the default version is 12.9.6 -> ERA-DEFAULT must fail, everything else pass.
N04 accept-any : the version refusal is deleted -> the BATTERY cannot see it (its families all pass
                 the accepted versions); this variant is measured, and its survival is disclosed as
                 a limit: the refusal is certified by `--usage-check`, not by a family.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(HERE, "c2gates")

VARIANTS = {
    "N01-era-flat-a": ("eras = version >= VISIBILITY_ERA_SPLIT",
                       "eras = version >= VISIBILITY_ERA_SPLIT\nera_b = False  # N01: one v92 clause bent"),
    "N02-era-flat-b": ("eras = version >= VISIBILITY_ERA_SPLIT",
                       "eras = version >= VISIBILITY_ERA_SPLIT\nera_b = True  # N02: one v92 clause bent"),
    "N03-default-b": ('ap.add_argument("--limine-version", default="12.9.4")',
                      'ap.add_argument("--limine-version", default="12.9.6")  # N03: one v92 clause bent'),
    "N04-accept-any": ("if parse_limine_version(a.limine_version) is None:",
                       "if False:  # N04: the version refusal is deleted"),
}


def main():
    for name, (old, new) in VARIANTS.items():
        # The gate line is `era_b = version >= VISIBILITY_ERA_SPLIT`; N01/N02 keep the assignment
        # and add one override line after it.
        patched_old = old.replace("eras", "era_b")
        with open(SRC, "r", encoding="utf-8") as f:
            text = f.read()
        n = text.count(patched_old)
        if n != 1:
            raise SystemExit("%s: pattern %r matched %d times, expected 1" % (name, patched_old, n))
        out = text.replace(patched_old, new.replace("eras", "era_b"))
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        os.chmod(path, 0o755)
        print("wrote %s (%d bytes, one clause bent)" % (path, len(out)))


if __name__ == "__main__":
    main()
