#!/usr/bin/env python3
"""Emit the round-93 near-miss gate controls: the candidate `tools/check-limine-pins.py` with
exactly ONE r93 clause bent. Each substitution must match exactly once (a variant that silently
changed nothing would prove nothing), and the emitted file is what the freeze manifest pins.

N01 exact-split   : the era split is strict (`>`) -> 12.9.5 itself reads as era A, so
                    ERA-EXACT-125 (C1) and AUTO-ERA-B-through-12.9.5 fail.
N02 first-body    : the era-B cut lands one line late -> the first body line stays global, so
                    ERA-B-FIRST-BODY reads `prompt` instead of `panic`.
N03 era-b-u1      : U1 is restricted to the pre-cut text in era B -> ERA-B-U1 reports [].
N04 accept-any    : the version refusal is deleted -> REFUSAL-VERSIONS fails (the r92 survivor,
                    now killed at family level).
N05 auto-ignore   : a probed version is not used for era selection -> AUTO-ERA-B reads era A.
N06 auto-fallback : a failed probe falls back to 12.9.4 -> AUTO-PROBE-FAIL answers a verdict
                    instead of rc 64.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-93", "before", "controls", "bends")

VARIANTS = {
    "N01-exact-split": (
        "era_b = version >= VISIBILITY_ERA_SPLIT",
        "era_b = version > VISIBILITY_ERA_SPLIT  # N01: one V2 clause bent",
    ),
    "N02-first-body": (
        "if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):",
        "if first_entry is not None and lineno == first_entry + 1 and (era_b or first_entry != 1):  # N02",
    ),
    "N03-era-b-u1": (
        "    for img_ln in sorted(image_lines):\n        kv = split_key(lines[img_ln - 1])",
        "    for img_ln in sorted(image_lines):\n"
        "        if era_b and first_entry is not None and img_ln > first_entry:\n"
        "            continue  # N03: one U1 clause bent\n"
        "        kv = split_key(lines[img_ln - 1])",
    ),
    "N04-accept-any": (
        "    if parse_limine_version(version) is None:",
        "    if False:  # N04: the version refusal is deleted",
    ),
    "N05-auto-ignore": (
        "era_b = version >= VISIBILITY_ERA_SPLIT",
        "era_b = version >= VISIBILITY_ERA_SPLIT and limine_version_source != \"probe\"  # N05",
    ),
    "N06-auto-fallback": (
        "        if probed is None:\n"
        "            ap.print_usage(sys.stderr)\n"
        "            print(\"check-limine-pins: --limine-version auto: `limine --version` probe failed\",\n"
        "                  file=sys.stderr)\n"
        "            return 64",
        "        if probed is None:\n"
        "            probed = \"12.9.4\"  # N06: one V3 clause bent",
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
