#!/usr/bin/env python3
"""Emit the round-100 near-miss gate controls: the landed `tools/check-limine-pins.py` with exactly
ONE clause bent. Each substitution must match exactly once (a variant that silently changed nothing
would prove nothing), and the emitted file is what the freeze manifest pins.

Why it exists (round 100, depth): the round-99 Frontier names the last two field-fidelity limits by
name — "The X/Y **echo** legs have no spelling-targeted committed bend: N09/N11 falsify
`visibility_era` only. The blanket `lie-limine-version` wrapper covers them, and it proves the
battery sees the field, not that a named family asserts it." The r99 battery sets `check_echo` on
both accepted-cap families, so a gate that lies in the echoed `limine_version` for exactly those
spellings must make those families fail. Two bends, each keyed on one version component:

N12-x-echo : the reported `limine_version` is falsified exactly when the FIRST component is the
             cap `999999999` (the X-cap family `REFUSAL-VERSIONS-9DIGIT`, and the same spelling's
             `EXPLICIT-VERSION-ECHO` member); pins, era and rc are computed from the true value.
             The r98 battery's `EXPLICIT-VERSION-ECHO` family already reads the echo, so this bend
             is a discrimination DELTA on that control (+1 failed family), never a met-to-unmet
             flip — the r99 N11-x-era precedent (A5).
N13-y-echo : the same, keyed on the SECOND component `999999999` (the Y-cap family's
             `12.999999999.4` / `0.999999999.0`); no r96-r98 family asserts the echo on those
             spellings, so the r98 control is blind (`met 105/105`) and the r99 family is the only
             witness.

Both lies are emitted only in the JSON `limine_version` field; `visibility_era` and every pin stay
the true values, so the only family whose expected answer changes is the one that reads the echo.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-100", "before", "controls", "bends")

VARIANTS = {
    "N12-x-echo": (
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version),  # N12 (echo lies for the X-cap spelling only, r100)\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
    ),
    "N13-y-echo": (
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
        '            "limine_version": ("12.999999998.4" if limine_version.count(".") >= 1 and limine_version.split(".")[1] == "999999999" else limine_version),  # N13 (echo lies for the Y-cap spellings only, r100)\n'
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
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
