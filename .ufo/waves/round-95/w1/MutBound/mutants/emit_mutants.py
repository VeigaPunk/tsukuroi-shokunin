#!/usr/bin/env python3
"""Emit the eight r95 bound mutants from the landed gate bytes, ONE clause each.

Each substitution must match exactly once (a mutant that silently changed nothing would
prove nothing). The emitted file is byte-identical to tools/check-limine-pins.py except for
its one hunk; the hunk is saved as <name>.diff next to the mutant for the report.
"""
import difflib
import hashlib
import os
import sys

SRC = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-limine-pins.py"
OUT = "/fast/scratch/hyaku/tsukuroi-r95/MutBound/mutants"

BOUND = "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts):"
ERA = "    era_b = version >= VISIBILITY_ERA_SPLIT"
PRINT = "    print(json.dumps(r, sort_keys=True))"
REFUSAL_STDERR = '        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)'

MUTANTS = {
    # M01: the frozen bend's twin (bound <= 9 -> <= 8)
    "M01-bound-8": (BOUND,
                    "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 8 for p in parts):  # M01 component bound <= 8"),
    # M02: bound <= 10 (ten-digit values become in-bound)
    "M02-bound-10": (BOUND,
                     "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 10 for p in parts):  # M02 component bound <= 10"),
    # M03: bound kept, but the exact accepted boundary member rejected
    "M03-reject-9digit-literal": (BOUND,
                                  '    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and len(p) <= 9 for p in parts) or text == "999999999.9.9":  # M03 reject the exact 9-digit member'),
    # M04: era split strict (> instead of >=)
    "M04-era-strict": (ERA, "    era_b = version > VISIBILITY_ERA_SPLIT  # M04 strict split (12.9.5 reads era A)"),
    # M05: no digit-count bound at all (whole condition line keeps its colon and valid syntax)
    "M05-no-bound": (BOUND,
                     "    if len(parts) != 3 or not all(p.isascii() and p.isdigit() for p in parts):  # M05 no digit-count bound"),
    # M06: accepts everything, but echoes limine_version truncated to 2 chars per component
    "M06-echo-truncated": (PRINT,
                           '    r["limine_version"] = ".".join(p[:2] for p in str(r["limine_version"]).split("."))  # M06 JSON echo truncated to 2 chars/component\n' + PRINT),
    # M07: accepted 9-digit value read as era A when the major is above 1000
    "M07-major-1000-era-a": (ERA,
                             "    era_b = version >= VISIBILITY_ERA_SPLIT and version[0] <= 1000  # M07 major > 1000 reads era A"),
    # M08: refusal message moved to stdout (rc 64, non-empty stdout)
    "M08-refusal-stdout": (REFUSAL_STDERR,
                           '        print("check-limine-pins: --limine-version must be X.Y.Z or auto")  # M08 refusal message to stdout'),
}


def main():
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for name, (old, new) in MUTANTS.items():
        n = text.count(old)
        if n != 1:
            raise SystemExit("%s: pattern %r matched %d times, expected 1" % (name, old, n))
        out = text.replace(old, new)
        path = os.path.join(OUT, name + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        os.chmod(path, 0o755)
        diff = "".join(difflib.unified_diff(text.splitlines(True), out.splitlines(True),
                                            fromfile="tools/check-limine-pins.py",
                                            tofile=name + ".py", n=1))
        with open(os.path.join(OUT, name + ".diff"), "w") as f:
            f.write(diff)
        digest = hashlib.sha256(out.encode()).hexdigest()
        changed = sum(1 for a, b in zip(text.splitlines(), out.splitlines()) if a != b)
        rows.append("%s %s changed_lines=%d delta_lines=%d" %
                    (name, digest, changed, len(out.splitlines()) - len(text.splitlines())))
        print(diff.rstrip())
    print("----")
    print("\n".join(rows))


if __name__ == "__main__":
    sys.exit(main())
