#!/usr/bin/env python3
"""Round-99 C2 capture forge: build fixture cases in scratch, run BOTH checkers (r98 control and
r99) with --root, and record rc/stdout/findings. Fixtures only; never writes the lane tree."""
import ast, json, os, shutil, subprocess, sys, tempfile

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r99/ReviewRegistry"
REC = os.path.join(LANE, ".ufo/waves/round-99/w1/ReviewRegistry/receipts")
R98 = os.path.join(LANE, "tools/check-registry-content-r98.py")
R99 = os.path.join(LANE, "tools/check-registry-content-r99.py")

sys.path.insert(0, os.path.join(LANE, ".ufo/waves/round-99/before/dev"))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "c99", os.path.join(LANE, "tools/check-registry-content-r99.py"))
c99 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c99)

BASE = {"clean": None, "gap": ("GAP", None, None), "hybrid": ("HYBRID", None, None),
        "restated": ("RESTATED", None, None)}

CLEAN_CELL = "VARIANTS N01-N03"


def tool_body(labels):
    rows = "".join('    "%s-k": ("a", "b"),\n' % lab for lab in labels)
    return "VARIANTS = {\n%s}\n" % rows


def derived(labels):
    """Independent re-derivation (ast, this file's own code) of the span the tool yields."""
    tree = ast.parse(tool_body(labels))
    node = [n for n in tree.body if isinstance(n, ast.Assign)][0]
    keys = [k.value for k in node.value.keys]
    labs = sorted({k.split("-")[0] for k in keys})
    nums = [int(x[1:]) for x in labs]
    if nums != list(range(nums[0], nums[0] + len(nums))):
        return ",".join(labs)
    return "%s-%s" % (labs[0], labs[-1])


CASES = [
    # name, base, labels, pinned-values cell, extra column overrides {col_index: text}
    ("a-hybrid", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04,N05", {}),
    ("b-restated", "gap", ["N01", "N03"], "VARIANTS N01,N03 then VARIANTS N01-N03", {}),
    ("c-gap-hybrid", "clean", ["N01", "N02", "N03", "N04", "N05"], "VARIANTS N01,N03,N05", {}),
    ("d-spaced-comma", "gap", ["N01", "N03"], "VARIANTS N01, N03", {}),
    ("e-lowercase", "clean", ["N01", "N02", "N03"], "VARIANTS n01-n03", {}),
    ("f-two-identical", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 and VARIANTS N01-N04", {}),
    ("g-outside-token", "hybrid", ["N01", "N02", "N03", "N04"], "pinned values N01-N04", {}),
    # guard breaks
    ("g1-semicolon", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04;", {}),
    ("g2-period", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04.", {}),
    ("g3-suffix-extra", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04extra", {}),
    ("g4-endash", "clean", ["N01", "N02", "N03"], "VARIANTS N01\u2013N03", {}),
    # extra forges beyond the assignment list
    ("x1-space-glued-hybrid", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04 N05", {}),
    ("x2-hybrid-plus-clean", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04,N05 and VARIANTS N01-N04", {}),
    ("x3-clean-plus-hybrid", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 and VARIANTS N01-N04,N05", {}),
    ("x4-clean-plus-lower", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 and VARIANTS n01-n03", {}),
    ("x5-clean-plus-spaced", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 and VARIANTS N01, N03", {}),
    ("x6-suffix-x", "hybrid", ["N01", "N02", "N03", "N04"], "VARIANTS N01-N04x", {}),
    ("x7-pipe-escaped-second", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 \\| VARIANTS N01-N05", {}),
    ("x8-second-in-other-col", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04", {6: "VARIANTS N01-N05"}),
    ("x9-second-in-verdict-col", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04", {3: "VARIANTS N01-N05 0 ok;1 mismatch;2 unused"}),
    ("x10-uncovered-prose", "hybrid", ["N01", "N02", "N03", "N04"],
     "VARIANTS N01-N04 (keys N01-N05)", {}),
]


def build(case, base, labels, cell, extra):
    if os.path.isdir(case):
        shutil.rmtree(case)
    c99.build_fixture(case, BASE[base])
    with open(os.path.join(case, "tools", "make-r96-bends.py"), "w") as f:
        f.write(tool_body(labels))
    skill = os.path.join(case, "SKILL.md")
    text = open(skill).read()
    if base == "gap":
        old = "VARIANTS N01,N03"
    elif base in ("hybrid",):
        old = "VARIANTS N01-N04,N05"
    elif base == "restated":
        old = "VARIANTS N01,N03 then VARIANTS N01-N03"
    else:
        old = CLEAN_CELL
    assert text.count(old) == 1, (case, old, text.count(old))
    text = text.replace(old, cell)
    for col, txt in extra.items():
        if col == 6:
            assert text.count("| fixture dir |") == 1
            text = text.replace("| fixture dir |", "| %s |" % txt)
        elif col == 3:
            assert text.count("| 0 ok;1 mismatch;2 unused |") == 1
            text = text.replace("| 0 ok;1 mismatch;2 unused |", "| %s |" % txt)
    open(skill, "w").write(text)


def run(tool, case, out):
    p = subprocess.run([sys.executable, "-I", tool, "--root", case, "--json", out],
                       capture_output=True, text=True, timeout=300,
                       cwd=SCRATCH, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C",
                                         "HOME": SCRATCH})
    payload = None
    if os.path.exists(out):
        try:
            payload = json.load(open(out))
        except ValueError:
            payload = None
    return p.returncode, (p.stdout + p.stderr).strip(), payload


def main():
    cases_root = os.path.join(SCRATCH, "cases")
    os.makedirs(cases_root, exist_ok=True)
    rows = []
    for name, base, labels, cell, extra in CASES:
        case = os.path.join(cases_root, name)
        build(case, base, labels, cell, extra)
        der = derived(labels)
        row = {"case": name, "cell": cell, "keys": ",".join(labels), "derived": der,
               "base": base, "extra": extra}
        for tag, tool in (("r98", R98), ("r99", R99)):
            out = os.path.join(REC, "forge-%s-%s.json" % (name, tag))
            rc, text, payload = run(tool, case, out)
            ids = sorted(f["id"] for f in (payload or {}).get("findings", [])) if payload else None
            row[tag] = {"rc": rc, "ids": ids,
                        "status": (payload or {}).get("status"),
                        "stdout": text.splitlines()[-1] if text else ""}
        rows.append(row)
        print("%-24s cell=%-46r derived=%-9s r98=%s %s | r99=%s %s"
              % (name, cell, der, row["r98"]["rc"], row["r98"]["ids"],
                 row["r99"]["rc"], row["r99"]["ids"]))
    with open(os.path.join(REC, "forge-matrix.json"), "w") as f:
        json.dump(rows, f, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
