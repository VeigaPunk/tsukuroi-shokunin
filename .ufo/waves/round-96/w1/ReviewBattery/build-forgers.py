#!/usr/bin/env python3
"""ReviewBattery seat: rebuild the seven forgers from the landed gate bytes.

Each forger is the landed gate with exactly one clause changed (the replacement count is asserted),
so a battery verdict on a forger measures that clause alone. Reads tools/check-limine-pins.py and
writes forgers/*.py under this seat dir. Idempotent: rerunning yields identical bytes.
"""
import hashlib
import os

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
GATE = os.path.join(LANE, "tools", "check-limine-pins.py")
OUT = os.path.join(SEAT, "forgers")

PATCHES = [
    # name, old, new, expected occurrences
    ("F-A-source-probe.py",
     '            "limine_version_source": limine_version_source,',
     '            "limine_version_source": "probe",  # F-A: always probe', 2),
    ("F-B-era-first-component.py",
     '    era_b = version >= VISIBILITY_ERA_SPLIT',
     '    era_b = (version[0], 0, 0) >= VISIBILITY_ERA_SPLIT  # F-B: era from the X component alone', 1),
    ("F-B2-era-max-component.py",
     '    era_b = version >= VISIBILITY_ERA_SPLIT',
     '    era_b = max(version) >= 12  # F-B2: era from the largest single component', 1),
    ("F-C-blanket-refusal.py",
     '    if not isinstance(text, str):\n        return None',
     '    return None  # F-C: blanket refusal of every version\n    if not isinstance(text, str):\n        return None', 1),
    ("F-D-echo-12.9.6.py",
     '            "limine_version": limine_version,',
     '            "limine_version": ("12.9.6" if limine_version_source == "flag" else limine_version),  # F-D', 2),
    ("F-E-label-boundary-only.py",
     '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",\n            "hash_mismatch_panic"',
     '            "visibility_era": ("pre-12.9.5" if version == (12, 9, 4) else "12.9.5+"),  # F-E: label correct only at the boundary\n            "hash_mismatch_panic"', 1),
    ("F-G-trailing-zero-accepted.py",
     '    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):\n        return None',
     '    if len(parts) > 3 and all(p == "0" for p in parts[3:]):  # F-G: trailing .0 accepted\n        parts = parts[:3]\n    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):\n        return None', 1),
]


def main():
    landed = open(GATE, encoding="utf-8").read()
    print("gate %s sha256 %s" % (GATE, hashlib.sha256(landed.encode()).hexdigest()))
    os.makedirs(OUT, exist_ok=True)
    for name, old, new, n in PATCHES:
        got = landed.count(old)
        assert got == n, (name, "expected %d occurrence(s), found %d" % (n, got))
        src = landed.replace(old, new)
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
        print("%-32s occurrences=%d sha256=%s" % (name, n, hashlib.sha256(src.encode()).hexdigest()))


if __name__ == "__main__":
    main()
