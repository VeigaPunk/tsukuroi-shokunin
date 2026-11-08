#!/usr/bin/env python3
"""Round-96 MutBound: derive 8 one-clause mutants of tools/check-limine-pins.py.

Reads the frozen gate bytes (sha256 7d79ac29...) and writes each variant only when its
substitution matches EXACTLY ONCE and changes the text. Mutants are written to the scratch dir
(--out) and copied byte-identically to the seat's mutants/ dir; a JSON manifest with the sha256
and the one-clause diff of each is written to the seat dir.

No lane file is written. The emitter tools/make-r96-bends.py is NOT run.
"""
import argparse
import difflib
import hashlib
import json
import os
import py_compile
import shutil

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SRC = os.path.join(LANE, "tools", "check-limine-pins.py")
SEAT = os.path.join(LANE, ".ufo", "waves", "round-96", "w1", "MutBound")

PARSER_OLD = ("    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 "
              "for p in parts):\n")

VARIANTS = {
    # M01: the JSON's limine_version_source is always "flag" (probe cases lie about their source).
    "M01-source-flag-always": (
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '            "limine_version_source": "flag",  # M01 (source always flag)\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
    ),
    # M02: the JSON's limine_version_source is always "probe" (explicit-flag cases lie).
    "M02-source-probe-always": (
        '            "limine_version_source": limine_version_source,\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
        '            "limine_version_source": "probe",  # M02 (source always probe)\n'
        '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",',
    ),
    # M03: the era is selected from the first component alone.
    "M03-era-from-x-only": (
        "    era_b = version >= VISIBILITY_ERA_SPLIT\n",
        "    era_b = version[0] >= VISIBILITY_ERA_SPLIT[0]  # M03 (era from X only)\n",
    ),
    # M04: the published era split is moved to (12, 10, 0): 12.9.5/12.9.6 read era A.
    "M04-era-split-12-10-0": (
        "VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut\n",
        "VISIBILITY_ERA_SPLIT = (12, 10, 0)   # M04 (split bent)\n",
    ),
    # M05: the component cap is 8 for the SECOND component only (boundary Y=999999999 refused).
    "M05-y-cap-8": (
        PARSER_OLD,
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and "
        "(i != 1 or len(p) <= 8)) for i, p in enumerate(parts)):  # M05 (Y cap bent)\n",
    ),
    # M06: the component cap is 8 for the THIRD component only.
    "M06-z-cap-8": (
        PARSER_OLD,
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and (len(p) <= 9 and "
        "(i != 2 or len(p) <= 8)) for i, p in enumerate(parts)):  # M06 (Z cap bent)\n",
    ),
    # M07: an explicit version is echoed lowercased.
    "M07-echo-lower": (
        '            "limine_version": limine_version,\n'
        '            "limine_version_source": limine_version_source,',
        '            "limine_version": limine_version.lower(),  # M07 (echo lowered)\n'
        '            "limine_version_source": limine_version_source,',
    ),
    # M08: a 9-digit component is accepted only when its value is >= 100000000
    #      (leading-zero 9-digit members such as 000000001 are refused).
    "M08-refusal-9digit-below-1e8": (
        PARSER_OLD,
        "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 and "
        "(len(p) != 9 or int(p) >= 100000000) for p in parts):  # M08 (9-digit values below 1e8 refused)\n",
    ),
}


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    src_bytes = text.encode("utf-8")
    base_sha = hashlib.sha256(src_bytes).hexdigest()
    expected = "7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32"
    if base_sha != expected:
        raise SystemExit("gate bytes moved: %s != frozen %s" % (base_sha, expected))
    outdir = os.path.abspath(a.out)
    seat_mut = os.path.join(SEAT, "mutants")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(seat_mut, exist_ok=True)
    manifest = {"source": SRC, "source_sha256": base_sha, "expected_source_sha256": expected,
                "mutants": []}
    for name, (old, new) in VARIANTS.items():
        n = text.count(old)
        if n != 1:
            raise SystemExit("%s: pattern matched %d times, expected exactly 1" % (name, n))
        if old == new:
            raise SystemExit("%s: substitution changed nothing" % name)
        mutated = text.replace(old, new)
        if mutated == text:
            raise SystemExit("%s: substitution changed nothing" % name)
        diff = [ln for ln in difflib.unified_diff(
            text.splitlines(), mutated.splitlines(), fromfile="check-limine-pins.py",
            tofile=name + ".py", n=1) if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---"))]
        if len(diff) != 2:
            raise SystemExit("%s: expected a one-line/two-line delta, got %r" % (name, diff))
        path = os.path.join(outdir, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(mutated)
        seat_path = os.path.join(seat_mut, name + ".py")
        shutil.copyfile(path, seat_path)
        py_compile.compile(path, doraise=True, cfile=os.path.join(outdir, name + ".pyc"))
        manifest["mutants"].append({
            "name": name, "sha256": sha256_text(mutated), "bytes": len(mutated.encode("utf-8")),
            "scratch_path": path, "seat_path": seat_path, "diff": "\n".join(diff),
        })
        print("%s sha256=%s diff=%s" % (name, sha256_text(mutated), " | ".join(diff)))
    with open(os.path.join(SEAT, "mutants-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
        f.write("\n")
    print("wrote %d mutants; pristine sha256=%s" % (len(manifest["mutants"]), base_sha))


if __name__ == "__main__":
    main()
