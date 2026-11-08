#!/usr/bin/env python3
"""ScribeKnowledge round-96: build two own-work era-rule mutants of the gate, in scratch only.

The r96 battery docstring for `fam_refusal_versions_9digit_y` claims that a gate which "reads the
era from X alone answers era B for `0.999999999.0` and fails".  Under an X-only rule the X of
`0.999999999.0` is 0, so the answer is era A — the same as the correct one.  These mutants measure
which families actually die under an X-only and under a Z-only era rule.

Read-only with respect to the lane: the bytes are written under scratch only.
"""
import os

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
GATE = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = "/fast/scratch/hyaku/tsukuroi-r96/ScribeKnowledge/mutants"

ORIG = "    era_b = version >= VISIBILITY_ERA_SPLIT\n"

MUTANTS = {
    # era decided by the FIRST component only
    "M-x-only-era.py": ("    era_b = version[0] >= VISIBILITY_ERA_SPLIT[0]\n",
                        "X-only era rule (own-work mutant)\n"),
    # era decided by the THIRD component only
    "M-z-only-era.py": ("    era_b = version[2] >= VISIBILITY_ERA_SPLIT[2]\n",
                        "Z-only era rule (own-work mutant)\n"),
    # era decided by the SECOND component only
    "M-y-only-era.py": ("    era_b = version[1] >= VISIBILITY_ERA_SPLIT[1]\n",
                        "Y-only era rule (own-work mutant)\n"),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    src = open(GATE, encoding="utf-8").read()
    assert src.count(ORIG) == 1, "era_b assignment not uniquely found"
    for name, (new, note) in MUTANTS.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(src.replace(ORIG, new))
        with open(p + ".clause.txt", "w", encoding="utf-8") as f:
            f.write(note + "\nfrom: " + ORIG + "to:   " + new)
        print("wrote", p)


if __name__ == "__main__":
    main()
