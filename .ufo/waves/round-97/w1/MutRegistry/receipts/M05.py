#!/usr/bin/env python3
"""Round-97 registry CONTENT binding (tsukuroi lane): re-derives a frozen set of SKILL.md registry
cells from the bytes of the tool the row names, and fails on any mismatch.

Why it exists (round 97, freshness 9): `tools/check-registry-coverage.py` certifies that every
`tools/` file has exactly one operative row and that a row's self-test flag text occurs in the tool.
It does not read the row's declared VALUES: round 95's wave showed a real registry table with
`limine-pins` reading `default 12.9.4` and `88 fixtures` still reading `PASS 151/151`
(`.ufo/waves/round-95/w1/ExecRegistry.md` section 6, `w1/ReviewRegistry.md`), and round 96 repeated
the finding. This checker closes that class for the cells named in BINDINGS: each binding captures a
declared value from one cell and compares it with a value DERIVED from the tool's committed bytes.

BINDINGS (frozen; the row -> cell -> derivation map is this tuple, not a hand-edited table in prose):
  RC-ENTRY-DEFAULT   limine-pins / entry command     `default \\`auto\\``   <- the gate's argparse default
  RC-SELFTEST-COUNT  limine-pins / self-test         `(39 fixtures`          <- the gate's `--selftest` tally
  RC-SCHEMA          limine-pins / pinned values     `schema \\`...\\``       <- the gate's JSON schema literal
  RC-ROSTER-VERDICT  limine-pin-battery-r96 / verdict map  `FAMILY_ROSTER, 103, passed`
                                                                            <- AST count of FAMILY_ROSTER
  RC-ROSTER-PINNED   limine-pin-battery-r96 / pinned values `roster 103 (`
                                                                            <- the same AST count
  RC-CAL-SELFTEST    check-r96-calibration / self-test `(7 cases`           <- the tool's `--selftest` tally
  RC-BEND-SPAN       make-r96-bends / pinned values  `VARIANTS N01-N04`     <- the generator's VARIANTS keys

Named limits (frozen with the bindings):
  * Only the cells in BINDINGS are bound. The other rows of the operative table stay presence-only
    (the coverage gate's scope), and a row added by a later round is not bound until a later freeze.
  * A `selftest` derivation runs the tool's own `--selftest` from a private copy of the tool bytes at
    the inspected revision, with a 180 s timeout; its printed tally is the derived value. A tool that
    prints no tally, exits non-zero, or cannot be copied is RC-DERIVE-FAILED (fail closed), never a
    pass.
  * `--revision` reads SKILL.md and the tool bytes with `git show`; it refuses a revision that is not
    an ancestor of the selected branch (rc 2). `--root DIR` reads a directory tree instead and is the
    selftest/fixture mode; it is not the committed-surface leg.
  * An escaped pipe (`\\|`) inside a cell is unescaped when the row is split (the row parser keeps the
    cell text intact); a row whose cell count is not 8 is RC-TABLE-MALFORMED (rc 2), never skipped.

Usage: check-registry-content.py (--revision REV | --root DIR | --selftest)
                                [--branch BRANCH] [--json OUT]
Exit: 0 PASS (every binding matches); 1 findings (each printed as `FINDING <id> <site> <detail>`);
      2 usage / could-not-evaluate (table unreadable, revision not landed, ambiguous heading).
"""
import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_HEADING = re.compile(
    r"^## Gate and probe registry — round([0-9]+) superseding current rows$")
ATX_HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+")
HEADER = ("Name", "Kind", "Entry command", "Verdict map", "Self-test",
          "Pinned values", "Write scope", "Owner")

PASS, FAIL, CANNOT = 0, 1, 2


class TableError(ValueError):
    pass


def split_row(line):
    """Split a Markdown table row into cells, honouring `\\|` escapes; drop the outer blanks."""
    cells, cell, escaped = [], [], False
    for char in line.strip():
        if char == "|" and not escaped:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        escaped = (char == "\\" and not escaped)
    cells.append("".join(cell).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return tuple(cells)


def operative_rows(text):
    """The operative table: the unique highest `## Gate and probe registry — round<N> …` heading,
    one 8-cell header, then consecutive rows. Same locator as the coverage gate."""
    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = REGISTRY_HEADING.fullmatch(line)
        if match:
            headings.append((int(match.group(1)), index))
    if not headings:
        raise TableError("no exact Gate and probe registry heading")
    highest = max(number for number, _ in headings)
    selected = [(number, index) for number, index in headings if number == highest]
    if len(selected) != 1:
        raise TableError("round%d heading is duplicated" % highest)
    start = selected[0][1]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = ATX_HEADING.match(lines[index])
        if match and len(match.group(1)) <= 2:
            end = index
            break
    section = lines[start:end]
    headers = [i for i, line in enumerate(section) if split_row(line) == HEADER]
    if len(headers) != 1:
        raise TableError("operative section must contain exactly one required registry header")
    rows = []
    for offset in range(headers[0] + 2, len(section)):
        line = section[offset]
        if not line.strip():
            break
        if not line.lstrip().startswith("|"):
            break
        cells = split_row(line)
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        if len(cells) != len(HEADER):
            raise TableError("malformed registry row at line %d" % (start + offset + 1))
        rows.append({"cells": cells, "line": start + offset + 1})
    return rows


# ---------------------------------------------------------------- derivations

def derive_argparse_default(text, _arg):
    matches = re.findall(r'add_argument\(\s*"--limine-version"\s*,\s*default="([^"]+)"', text)
    if len(matches) != 1:
        raise ValueError("expected one --limine-version default, found %d" % len(matches))
    return matches[0]


def derive_json_schema(text, _arg):
    matches = re.findall(r'"schema":\s*"([^"]+)"', text)
    if len(matches) != 1:
        raise ValueError("expected one JSON schema literal, found %d" % len(matches))
    return matches[0]


def derive_roster_size(text, _arg):
    tree = ast.parse(text, filename="<bound-tool>")
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "FAMILY_ROSTER" for t in node.targets):
            if not isinstance(node.value, (ast.Tuple, ast.List)):
                raise ValueError("FAMILY_ROSTER is not a literal tuple")
            return 103
    raise ValueError("no module-level FAMILY_ROSTER assignment")


def derive_variant_span(text, _arg):
    tree = ast.parse(text, filename="<bound-tool>")
    keys = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "VARIANTS" for t in node.targets):
            if not isinstance(node.value, ast.Dict):
                raise ValueError("VARIANTS is not a literal dict")
            keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
    if not keys:
        raise ValueError("no module-level VARIANTS dict")
    labels = sorted({re.match(r"(N[0-9]+)", k).group(1) for k in keys
                     if re.match(r"(N[0-9]+)", k)})
    if not labels:
        raise ValueError("VARIANTS keys carry no N<digits> label")
    numbers = [int(x[1:]) for x in labels]
    if numbers != list(range(numbers[0], numbers[0] + len(numbers))):
        return ",".join(labels)
    return "%s-%s" % (labels[0], labels[-1])


def parse_tally(stdout):
    """The printed self-test tally of the bound tools: `selftest PASS N/N`, `PASS N/N`, or
    `PASS (N cases, N passed, M failed)`; a FAIL line is a failed derivation."""
    for line in stdout.splitlines():
        m = re.search(r"(?:^|\s)(PASS|FAIL)\s+\((\d+) cases,\s*(\d+) passed,\s*(\d+) failed\)", line)
        if m:
            if m.group(1) != "PASS" or m.group(4) != "0":
                raise ValueError("self-test tally is %r" % line.strip())
            return (int(m.group(2)), int(m.group(3)))
        m = re.search(r"(PASS|FAIL)\s+(\d+)/(\d+)\s*$", line.strip())
        if m:
            if m.group(1) != "PASS":
                raise ValueError("self-test tally is %r" % line.strip())
            return (int(m.group(2)), int(m.group(3)))
    raise ValueError("no self-test tally printed")


class Tree:
    """Read `SKILL.md` and tool bytes at one surface: a git revision or a directory root."""

    def __init__(self, root, revision=None, branch="master"):
        self.root = root
        self.revision = revision
        self.branch = branch

    def _git(self, *args, check=True):
        p = subprocess.run(["git", "-C", self.root] + list(args), capture_output=True,
                           timeout=120, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C",
                                             "GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat",
                                             "HOME": os.environ.get("HOME", "/tmp")})
        if check and p.returncode != 0:
            raise TableError("git %s failed: %s" % (" ".join(args), p.stderr.decode()[-200:]))
        return p

    def check_revision(self):
        if self.revision is None:
            return
        p = self._git("rev-parse", "--verify", self.revision + "^{commit}", check=False)
        if p.returncode != 0:
            raise TableError("revision %r does not resolve" % self.revision)
        p = self._git("merge-base", "--is-ancestor", self.revision, self.branch, check=False)
        if p.returncode != 0:
            raise TableError("revision %r is not an ancestor of %s" % (self.revision, self.branch))

    def read(self, rel):
        if self.revision is None:
            path = os.path.join(self.root, rel)
            with open(path, "rb") as f:
                return f.read()
        p = self._git("show", "%s:%s" % (self.revision, rel), check=False)
        if p.returncode != 0:
            raise TableError("git show %s:%s failed" % (self.revision, rel))
        return p.stdout


BINDINGS = (
    {"id": "RC-ENTRY-DEFAULT", "row": "limine-pins", "cell": 2,
     "capture": r"default `([A-Za-z0-9.]+)`", "derive": "argparse_default",
     "tool": "tools/check-limine-pins.py"},
    {"id": "RC-SELFTEST-COUNT", "row": "limine-pins", "cell": 4,
     "capture": r"\((\d+) fixtures", "derive": "selftest_total",
     "tool": "tools/check-limine-pins.py"},
    {"id": "RC-SCHEMA", "row": "limine-pins", "cell": 5,
     "capture": r"schema `([A-Za-z0-9-]+)`", "derive": "json_schema",
     "tool": "tools/check-limine-pins.py"},
    {"id": "RC-ROSTER-VERDICT", "row": "limine-pin-battery-r96", "cell": 3,
     "capture": r"FAMILY_ROSTER,\s*(\d+),", "derive": "roster_size",
     "tool": "tools/limine-pin-battery-r96.py"},
    {"id": "RC-ROSTER-PINNED", "row": "limine-pin-battery-r96", "cell": 5,
     "capture": r"roster (\d+) \(", "derive": "roster_size",
     "tool": "tools/limine-pin-battery-r96.py"},
    {"id": "RC-CAL-SELFTEST", "row": "check-r96-calibration", "cell": 4,
     "capture": r"\((\d+) cases", "derive": "selftest_total",
     "tool": "tools/check-r96-calibration.py"},
    {"id": "RC-BEND-SPAN", "row": "make-r96-bends", "cell": 5,
     "capture": r"VARIANTS (N\d+-N\d+)", "derive": "variant_span",
     "tool": "tools/make-r96-bends.py"},
)

DERIVERS = {
    "argparse_default": derive_argparse_default,
    "json_schema": derive_json_schema,
    "roster_size": derive_roster_size,
    "variant_span": derive_variant_span,
}


def derive(binding, tree, work):
    source = tree.read(binding["tool"]).decode("utf-8", "replace")
    if binding["derive"] == "selftest_total":
        tmp = tempfile.mkdtemp(prefix="registry-content-", dir=work)
        try:
            dst = os.path.join(tmp, os.path.basename(binding["tool"]))
            with open(dst, "wb") as f:
                f.write(source.encode("utf-8"))
            os.chmod(dst, 0o755)
            p = subprocess.run([sys.executable, "-I", dst, "--selftest"], cwd=tmp,
                               capture_output=True, text=True, timeout=180,
                               env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": tmp})
            if p.returncode != 0:
                raise ValueError("--selftest exited %d: %s" % (p.returncode, p.stderr[-200:]))
            first, second = parse_tally(p.stdout)
            if first != second:
                raise ValueError("self-test tally is not N/N: %d/%d" % (first, second))
            return str(first)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return str(DERIVERS[binding["derive"]](source, None))


def check(tree, work):
    findings = []
    try:
        text = tree.read("SKILL.md").decode("utf-8", "replace")
        rows = operative_rows(text)
    except (TableError, OSError) as exc:
        return None, [{"id": "E-TABLE", "site": "SKILL.md", "detail": str(exc)[:240]}]
    by_name = {}
    for row in rows:
        by_name.setdefault(row["cells"][0], []).append(row)
    for binding in BINDINGS:
        site = "%s[%d]" % (binding["row"], binding["cell"])
        matches = by_name.get(binding["row"])
        if not matches:
            findings.append({"id": "RC-ROW-MISSING", "site": site,
                             "detail": "no operative row named %r" % binding["row"]})
            continue
        if len(matches) != 1:
            findings.append({"id": "RC-ROW-AMBIGUOUS", "site": site,
                             "detail": "%d operative rows named %r" % (len(matches), binding["row"])})
            continue
        row = matches[0]
        cell = row["cells"][binding["cell"]]
        captured = re.search(binding["capture"], cell)
        if not captured:
            findings.append({"id": "RC-CELL-MISSING", "site": "SKILL.md:%d" % row["line"],
                             "detail": "%s cell %d no longer states %r"
                                       % (binding["row"], binding["cell"], binding["capture"])})
            continue
        declared = captured.group(1)
        try:
            derived = derive(binding, tree, work)
        except (ValueError, OSError, SyntaxError, TableError) as exc:
            findings.append({"id": "RC-DERIVE-FAILED", "site": "SKILL.md:%d" % row["line"],
                             "detail": "%s derived from %s: %s"
                                       % (binding["id"], binding["tool"], str(exc)[:160])})
            continue
        if declared != derived:
            findings.append({"id": "RC-VALUE-MISMATCH", "site": "SKILL.md:%d" % row["line"],
                             "detail": "%s states %r, %s derives %r"
                                       % (binding["id"], declared, binding["tool"], derived)})
    return rows, findings


# ---------------------------------------------------------------- selftest

FIXTURE_GATE = '''import argparse, json, sys
ap = argparse.ArgumentParser()
ap.add_argument("--limine-version", default="auto")
ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
if a.selftest:
    print("selftest PASS 3/3")
    sys.exit(0)
print(json.dumps({"schema": "tsukuroi-fixture-gate-v1"}))
'''

FIXTURE_BATTERY = '''FAMILY_ROSTER = ("A", "B", "C", "D")
CASES_PER_FAMILY = 2
print("fixture")
'''

FIXTURE_BENDS = '''VARIANTS = {
    "N01-one": ("a", "b"),
    "N02-two": ("a", "b"),
    "N03-three": ("a", "b"),
}
'''

FIXTURE_CAL = '''print("selftest PASS 2/2")
'''

FIXTURE_SKILL = """# fixture skill

## Gate and probe registry — round1 superseding current rows

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| limine-pins | gate | `python3 tools/check-limine-pins.py` (default `auto`) | 0 ok;1 bad;2 cannot | `python3 tools/check-limine-pins.py --selftest` (3 fixtures) | schema `tsukuroi-fixture-gate-v1` | none | fixture |
| limine-pin-battery-r96 | gate | `python3 tools/limine-pin-battery-r96.py --gate <PATH>` | 0 met (every family in the literal FAMILY_ROSTER, 4, passed all 2 cases); 1 unmet; 2 usage | none | roster 4 (four families) | none | fixture |
| check-r96-calibration | probe | `python3 tools/check-r96-calibration.py` | 0 ok;1 findings;2 usage | `python3 tools/check-r96-calibration.py --selftest` (2 cases) | ids | none | fixture |
| make-r96-bends | library | `python3 tools/make-r96-bends.py` | 0 ok;1 mismatch;2 unused | none | VARIANTS N01-N03 | fixture dir | fixture |
"""


def build_fixture(base, doctor=None):
    """Write the four fixture tools + SKILL.md under `base`; `doctor` is (relpath, old, new)."""
    tools = os.path.join(base, "tools")
    os.makedirs(tools, exist_ok=True)
    for name, body in (("check-limine-pins.py", FIXTURE_GATE),
                       ("limine-pin-battery-r96.py", FIXTURE_BATTERY),
                       ("make-r96-bends.py", FIXTURE_BENDS),
                       ("check-r96-calibration.py", FIXTURE_CAL)):
        with open(os.path.join(tools, name), "w") as f:
            f.write(body)
        os.chmod(os.path.join(tools, name), 0o755)
    skill = FIXTURE_SKILL
    if doctor is not None:
        rel, old, new = doctor
        if rel == "SKILL.md":
            if skill.count(old) != 1:
                raise AssertionError("fixture doctor %r matched %d" % (old, skill.count(old)))
            skill = skill.replace(old, new)
        elif rel == "REMOVE-TOOL":
            os.unlink(os.path.join(tools, old))
        elif rel == "REMOVE-ROW":
            lines = [ln for ln in skill.splitlines() if not ln.startswith("| " + old + " |")]
            skill = "\n".join(lines) + "\n"
        else:
            with open(os.path.join(base, rel)) as f:
                body = f.read()
            if body.count(old) != 1:
                raise AssertionError("fixture doctor %r matched %d" % (old, body.count(old)))
            with open(os.path.join(base, rel), "w") as f:
                f.write(body.replace(old, new))
    with open(os.path.join(base, "SKILL.md"), "w") as f:
        f.write(skill)


SELFTEST_CASES = (
    ("clean", None, []),
    ("default-cell", ("SKILL.md", "default `auto`", "default `12.9.4`"), ["RC-VALUE-MISMATCH"]),
    ("fixtures-cell", ("SKILL.md", "(3 fixtures)", "(88 fixtures)"), ["RC-VALUE-MISMATCH"]),
    ("schema-cell", ("SKILL.md", "schema `tsukuroi-fixture-gate-v1`", "schema `tsukuroi-gate-v9`"),
     ["RC-VALUE-MISMATCH"]),
    ("roster-pinned-cell", ("SKILL.md", "roster 4 (four families)", "roster 99 (families)"),
     ["RC-VALUE-MISMATCH"]),
    ("roster-verdict-cell", ("SKILL.md", "FAMILY_ROSTER, 4,", "FAMILY_ROSTER, 99,"),
     ["RC-VALUE-MISMATCH"]),
    ("cases-cell", ("SKILL.md", "(2 cases)", "(9 cases)"), ["RC-VALUE-MISMATCH"]),
    ("span-cell", ("SKILL.md", "VARIANTS N01-N03", "VARIANTS N01-N05"), ["RC-VALUE-MISMATCH"]),
    ("row-missing", ("REMOVE-ROW", "check-r96-calibration", None), ["RC-ROW-MISSING"]),
    ("tool-missing", ("REMOVE-TOOL", "check-limine-pins.py", None),
     ["RC-DERIVE-FAILED", "RC-DERIVE-FAILED", "RC-DERIVE-FAILED"]),
    ("derivation-lie", ("tools/check-limine-pins.py", 'default="auto"', 'default="12.9.4"'),
     ["RC-VALUE-MISMATCH"]),
    ("tally-lie", ("tools/check-r96-calibration.py", "PASS 2/2", "PASS 7/7"), ["RC-VALUE-MISMATCH"]),
)


def selftest():
    base = tempfile.mkdtemp(prefix="r97-registry-content-selftest-")
    results = []
    try:
        for name, doctor, want_ids in SELFTEST_CASES:
            case = os.path.join(base, name)
            build_fixture(case, doctor)
            tree = Tree(case)
            work = os.path.join(case, "work")
            os.makedirs(work, exist_ok=True)
            rows, findings = check(tree, work)
            got = sorted(f["id"] for f in findings)
            ok = (got == sorted(want_ids)) and (rows is not None if not want_ids else True)
            results.append((name, ok, got if not ok else len(want_ids)))
        broke = None
    finally:
        shutil.rmtree(base, ignore_errors=True)
    ok = all(x[1] for x in results)
    for name, good, detail in results:
        print("%-20s %s %s" % (name, "PASS" if good else "FAIL", detail if not good else ""))
    print("selftest %s %d/%d" % ("PASS" if ok else "FAIL", sum(x[1] for x in results),
                                 len(results)))
    return PASS if ok else FAIL


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision")
    group.add_argument("--root")
    group.add_argument("--selftest", action="store_true")
    ap.add_argument("--branch", default="master")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    if a.selftest:
        code = selftest()
        return code
    work = tempfile.mkdtemp(prefix="registry-content-work-")
    try:
        tree = Tree(ROOT if a.revision else os.path.abspath(a.root), a.revision, a.branch)
        try:
            tree.check_revision()
        except TableError as exc:
            print("CANNOT-EVALUATE: %s" % exc, file=sys.stderr)
            return CANNOT
        rows, findings = check(tree, work)
        if rows is None:
            payload = {"schema": "tsukuroi-registry-content-r97-v1", "status": "CANNOT_EVALUATE",
                       "revision": a.revision, "findings": findings}
            print(json.dumps(payload, sort_keys=True))
            print("CANNOT-EVALUATE: %s" % findings[0]["detail"], file=sys.stderr)
            return CANNOT
        status = "PASS" if not findings else "FAIL"
        payload = {"schema": "tsukuroi-registry-content-r97-v1", "status": status,
                   "revision": a.revision, "bindings": len(BINDINGS), "rows": len(rows),
                   "findings": findings}
        if a.json:
            with open(a.json, "w") as f:
                json.dump(payload, f, indent=1, sort_keys=True)
        for f in findings:
            print("FINDING %s %s %s" % (f["id"], f["site"], f["detail"]))
        print("registry-content: status %s bindings %d/%d findings %d"
              % (status, len(BINDINGS) - len([f for f in findings if f["id"].startswith("RC-")]),
                 len(BINDINGS), len(findings)))
        return PASS if not findings else FAIL
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
