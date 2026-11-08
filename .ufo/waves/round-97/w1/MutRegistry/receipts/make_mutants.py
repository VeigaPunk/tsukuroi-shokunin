#!/usr/bin/env python3
"""Round-97 seat MutRegistry: emit one-clause mutants of tools/check-registry-content.py.
Reads the pristine copy in scratch; never touches the lane. Each mutation asserts its target
string occurs the expected number of times and changes exactly that clause."""
import os
import sys

S = "/fast/scratch/hyaku/tsukuroi-r97/MutRegistry"
SRC = os.path.join(S, "orig.py")
OUT = os.path.join(S, "mutants")

MUTANTS = {
    "M01": [(
        "derive() returns the declared value (comparison vacuous)",
        ["        derived = derive(binding, tree, work)\n"],
        ["        derived = declared\n"],
    )],
    "M02": [(
        "the `declared != derived` branch deleted (always pass)",
        ["""        if declared != derived:
            findings.append({"id": "RC-VALUE-MISMATCH", "site": "SKILL.md:%d" % row["line"],
                             "detail": "%s states %r, %s derives %r"
                                       % (binding["id"], declared, binding["tool"], derived)})
"""],
        [""],
    )],
    "M03": [(
        "selftest tally derivation is (0,0) and its comparison is skipped",
        ["            return (int(m.group(2)), int(m.group(3)))",
         '        if declared != derived:'],
        ["            return (0, 0)",
         '        if declared != derived and binding["derive"] != "selftest_total":'],
    )],
    "M04": [(
        "RC-ROW-MISSING removed (a missing row falls to RC-ROW-AMBIGUOUS)",
        ["""        if not matches:
            findings.append({"id": "RC-ROW-MISSING", "site": site,
                             "detail": "no operative row named %r" % binding["row"]})
            continue
"""],
        [""],
    )],
    "M05": [(
        "derive_roster_size returns a constant 103",
        ["            return len(node.value.elts)"],
        ["            return 103"],
    )],
    "M06": [(
        "operative_rows takes the FIRST heading instead of the unique highest",
        ["""    highest = max(number for number, _ in headings)
    selected = [(number, index) for number, index in headings if number == highest]
"""],
        ["    selected = [headings[0]]\n"],
    )],
    "M07": [(
        "--revision skips the branch ancestor check",
        ["""        p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
        if p.returncode != 0:
            raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))
"""],
        [""],
    )],
    "M08": [(
        "derive_variant_span compares only the first label (contiguity check vacuous)",
        ["    if numbers != list(range(numbers[0], numbers[0] + len(numbers))):"],
        ["    if numbers[:1] != list(range(numbers[0], numbers[0] + 1)):"],
    )],
}


def main():
    base = open(SRC).read()
    os.makedirs(OUT, exist_ok=True)
    for mid in sorted(MUTANTS):
        text = base
        for clause, olds, news in MUTANTS[mid]:
            for old, new in zip(olds, news):
                want = 2 if (mid == "M03" and old.startswith("            return (int(")) else 1
                got = text.count(old)
                if got != want:
                    raise SystemExit("%s target %r matched %d (want %d)" % (mid, old[:50], got, want))
                text = text.replace(old, new)
        path = os.path.join(OUT, mid + ".py")
        with open(path, "w") as f:
            f.write(text)
        print("%s written %d bytes clause=%r" % (path, len(text), MUTANTS[mid][0][0]))


if __name__ == "__main__":
    main()
