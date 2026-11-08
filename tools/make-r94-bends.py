#!/usr/bin/env python3
"""Emit the round-94 near-miss gate controls: the candidate `tools/check-limine-pins.py` with
exactly ONE r94 clause bent. Each substitution must match exactly once (a variant that silently
changed nothing would prove nothing), and the emitted file is what the freeze manifest pins.

N01 digit10       : the component bound is `<= 10` -> a ten-digit component is accepted.
N02 unanchored    : the probe regex has no suffix guard -> `12.9.6-rc1` and the stderr `Limine 12.9.6`
                    are accepted as 12.9.6.
N03 bound-11      : the component bound is `<= 11` -> the live usage roster's ten-digit half is
                    unreachable (the battery's REFUSAL-VERSIONS-10DIGIT still kills it here).
N04 stale-tree    : the gate reads the tree's own copy of the default version (`LIM_STD_VERBOSE`
                    set to `12.9.6` when the env carries it) — never invoked: a decoy.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(LANE, ".ufo", "waves", "round-94", "before", "controls", "bends")

VARIANTS = {
    "N01-digit10": (
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 10 for p in parts):  # N01 (bound bent to <=10)",
    ),
    "N02-unanchored": (
        '    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)(?![\\w.-])", p.stdout)',
        '    m = re.search(r"(?i)\\blimine\\s+v?(\\d+\\.\\d+\\.\\d+)", p.stdout)  # N02 (suffix guard deleted)',
    ),
    "N03-bound-11": (
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):",
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 11 for p in parts):  # N03 (bound bent to <=11)",
    ),
    "N04-stale-tree": (
        "def probe_limine_version(executable=\"limine\"):",
        "def probe_limine_version(executable=\"limine\"):\n    _stale_default = os.environ.get(\"LIM_STD_VERSION\", \"12.9.4\")  # N04 (decoy, never invoked)",
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
