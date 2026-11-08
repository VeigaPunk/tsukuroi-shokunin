#!/usr/bin/env python3
"""Round-100 w1 seat MutInstruments: build the three generator mutants and the seven checker
mutants from the instruments' pristine bytes.

Each mutant is a list of exact-string substitutions (each asserted to match exactly once), so a
mutant differs from the instrument only by the injected defect. Nothing is written outside the
scratch dir given as argv[1]; the instruments are read from the lane, read-only.
"""
import hashlib
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
CHECKER = os.path.join(LANE, "tools", "check-registry-content-r100.py")
BENDS = os.path.join(LANE, "tools", "make-r100-bends.py")

# The N12 "x-echo" replacement string, kept byte-identical to tools/make-r100-bends.py.
N12_NEW_LINE = ('        \'            "limine_version": ("999999998.9.9" if limine_version'
                '.split(".")[0] == "999999999" else limine_version),  # N12 (echo lies for the '
                'X-cap spelling only, r100)\\n\'\n')
N12_NOOP_LINE = ('        \'            "limine_version": limine_version,\\n\'\n')

CHECKER_EDITS = {
    "M1": ("bind the first N<digits> of the mention, skip parse_label_set validation", [(
        '            try:\n'
        '                declared_set = parse_label_set(mention.group(1))\n'
        '            except ValueError as exc:\n'
        '                findings.append({"id": "RC-CELL-MISSING", "site": "SKILL.md:%d" % row["line"],\n'
        '                                 "detail": "%s cell %d label set: %s"\n'
        '                                           % (binding["row"], binding["cell"], str(exc)[:160])})\n'
        '                continue\n',
        '            first_label = re.search(r"N[0-9]+", mention.group(1))\n'
        '            declared_set = {first_label.group(0)} if first_label else set()\n')]),
    "M2": ("accept a cell that mentions VARIANTS twice (first mention bound)", [(
        '            if mentions > 1:\n'
        '                findings.append({"id": "RC-CELL-AMBIGUOUS", "site": "SKILL.md:%d" % row["line"],\n'
        '                                 "detail": "%s cell %d mentions %r %d times; the first mention is "\n'
        '                                           "not the cell\'s value"\n'
        '                                           % (binding["row"], binding["cell"], "VARIANTS",\n'
        '                                              mentions)})\n'
        '                continue\n',
        '            # M2: a second VARIANTS mention is silently accepted (first mention bound)\n')]),
    "M3": ("compare only the first label of each set, not the whole set", [(
        '            if declared_set != derived_set:\n',
        '            if sorted(declared_set)[:1] != sorted(derived_set)[:1]:\n')]),
    "M4": ("drop range expansion: N01-N03 binds as the single label N01", [(
        '        last = int(match.group(2))\n'
        '        if last < first:\n'
        '            raise ValueError("range %r descends" % part)\n'
        '        for number in range(first, last + 1):\n'
        '            labels.add("N%0*d" % (width, number))\n',
        '        labels.add("N%0*d" % (width, first))\n')]),
    "M5": ("accept a declared set that is a SUPERSET of the derived set", [(
        '            if declared_set != derived_set:\n',
        '            if not declared_set >= derived_set:\n')]),
    "M6": ("parse_label_set accepts any prose: fall back to the union of N-tokens", [(
        '        match = TOKEN.fullmatch(part)\n'
        '        if not match:\n'
        '            raise ValueError("token %r is not an N-label or N-label range" % part)\n',
        '        match = TOKEN.fullmatch(part)\n'
        '        if not match:\n'
        '            labels.update("N%s" % n for n in re.findall(r"N([0-9]+)", expr))\n'
        '            continue\n')]),
    "M7": ("count VARIANTS mentions case-insensitively so `variants` also counts", [(
        '            mentions = len(re.findall(r"\\bVARIANTS\\b", cell))\n',
        '            mentions = len(re.findall(r"\\bVARIANTS\\b", cell, re.IGNORECASE))\n')]),
    "M8": ("skip the --revision ancestor refusal (the r99 M07 branch, re-probed on the successor)", [(
        '        try:\n'
        '            tree.check_revision()\n'
        '        except TableError as exc:\n'
        '            print("CANNOT-EVALUATE: %s" % exc, file=sys.stderr)\n'
        '            return CANNOT\n',
        '        # M8: the ancestor refusal is skipped\n')]),
}

GEN_EDITS = {
    "B1": ("remove the exact-once substitution guard", [(
        '        n = text.count(old)\n'
        '        if n != 1:\n'
        '            raise SystemExit("%s: pattern %r matched %d times, expected 1" % (name, old[:60], n))\n',
        '        n = text.count(old)\n')]),
    "B2": ("emit a no-op bend: N12 replacement equals the gate bytes and the no-op guard is gone", [
        ('        if out == text:\n'
         '            raise SystemExit("%s: substitution changed nothing" % name)\n',
         ''),
        # one facet of the defect: the N12 replacement is the gate line verbatim
        (N12_NEW_LINE, N12_NOOP_LINE)]),
    "B3": ("key the N12 X bend on the SECOND version component instead of the first", [(
        'if limine_version.split(".")[0] == "999999999" else limine_version)',
        'if limine_version.count(".") >= 1 and limine_version.split(".")[1] == "999999999" '
        'else limine_version)')]),
}


def build(edits, text, name):
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise SystemExit("%s: pattern %r matched %d times, expected 1" % (name, old[:60], n))
        text = text.replace(old, new)
    return text


def emit(src, edits, name, out, why):
    with open(src, encoding="utf-8") as f:
        pristine = f.read()
    mutant = build(edits, pristine, name)
    if mutant == pristine:
        raise SystemExit("%s: substitution changed nothing" % name)
    compile(mutant, name, "exec")
    dst = os.path.join(out, name + ".py")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(mutant)
    os.chmod(dst, 0o755)
    print("%s %s %d bytes sha256=%s :: %s"
          % (name, os.path.basename(src), len(mutant.encode()),
             hashlib.sha256(mutant.encode()).hexdigest(), why))


def main():
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    for name in sorted(CHECKER_EDITS):
        why, edits = CHECKER_EDITS[name]
        emit(CHECKER, edits, name, out, why)
    for name in sorted(GEN_EDITS):
        why, edits = GEN_EDITS[name]
        emit(BENDS, edits, name, out, why)
    if "--p-b2" in sys.argv:
        # P-B2: the pristine generator carrying ONLY the no-op VARIANTS (both guards intact).
        emit(BENDS, [(N12_NEW_LINE, N12_NOOP_LINE)], "P-B2-pristine-noop-variant", out,
             "control: pristine generator, N12 replacement made a no-op")


if __name__ == "__main__":
    main()
