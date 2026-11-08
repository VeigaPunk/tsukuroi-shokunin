#!/usr/bin/env python3
"""Emit the round-99 near-miss gate controls: the landed `tools/check-limine-pins.py` with exactly
ONE clause bent. Each substitution must match exactly once (a variant that silently changed nothing
would prove nothing), and the emitted file is what the freeze manifest pins.

N09-y-era    : the reported `visibility_era` label is swapped exactly when the SECOND version
               component has nine digits (the r96 Y-cap spellings `12.999999999.4` era B and
               `0.999999999.0` era A); pins stay correct. The r99 battery sets `check_era` on
               REFUSAL-VERSIONS-9DIGIT-Y, so that family fails; the r98 battery never read the
               field on those spellings and reads `met 105/105` on this same article
               (r98 `w1/ReviewBattery/g6-y-era-r98.json`, amendment A4).
N11-x-era    : the reported `visibility_era` label is swapped exactly when the FIRST version
               component is the cap `999999999` (the r95 X-cap spelling `999999999.9.9`, and its
               EXPLICIT-VERSION-ERA member); pins stay correct.
A Z-echo bend was drafted and DROPPED as a twin (QUALITY 136): the r98 battery already sets
`check_echo` on REFUSAL-VERSIONS-9DIGIT-Z, so the same article reads `unmet 104/105` on the r98
control — it witnesses r98's assertion, not r99's. Receipt: `.ufo/waves/round-99/before/dev/`.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-99", "before", "controls", "bends")

VARIANTS = {
    "N09-y-era": (
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": (("pre-12.9.5" if era_b else "12.9.5+") if limine_version.split(".")[1] == "999999999" else ("12.9.5+" if era_b else "pre-12.9.5")),  # N09 (era label lies for Y-cap spellings only, r99)',
    ),
    "N11-x-era": (
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": (("pre-12.9.5" if era_b else "12.9.5+") if limine_version.split(".")[0] == "999999999" else ("12.9.5+" if era_b else "pre-12.9.5")),  # N11 (era label lies for the X-cap spelling only, r99)',
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
        compile(out, name, "exec")
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        os.chmod(path, 0o755)
        print("wrote %s (%d bytes, one clause bent)" % (path, len(out)))


if __name__ == "__main__":
    main()
