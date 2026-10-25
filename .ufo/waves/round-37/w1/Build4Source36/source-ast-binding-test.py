#!/usr/bin/env python3
"""Source AST binding test (round-37 w1, seat Build4Source36).

Independent runnable design item 4/12.  It checks the lane's static
import+bind-call AST census (`shared()` in tools/check-revision-binding.py)
against a labeled matrix of synthetic consumer sources, each with a
ground-truth binding outcome.

It is hermetic: the lane file is only *copied* into a private TemporaryDirectory
under the system tmp dir and loaded from there via importlib; nothing in the
lane, fleet, or sibling repos is written.  No git commands are run, no commits
are made, and no process outside python3 is spawned.

Exit status:
  0  all gating cases pass on the *patched* census AND at least one gating case
     fails on the unchanged baseline (red-before / green-after contract)
  1  otherwise (including harness wiring failure)
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # never let importlib drop __pycache__ anywhere

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
JUDGE = LANE / "tools" / "check-revision-binding.py"
SHARED_FN = "shared"

# --- Gating matrix: (label, source, expected (uses, copies)) ------------------
# Ground truth is binding semantics of the module as executed: a bind use is
# only real if an import that binds `_revision`/`bind` actually executes before
# the call site.  Constant-false branches never execute, so their content must
# not count (same rule the census already applies to `if False:`).

CASES = [
    ("live-import-call", (
        "import _revision\n"
        "def adapter(r, v, b):\n"
        "    return _revision.bind(r, v, b)\n"), (True, 0)),
    ("from-import-alias-call", (
        "from _revision import bind as resolve\n"
        "def adapter(r, v, b):\n"
        "    return resolve(r, v, b)\n"), (True, 0)),
    ("string-only-mention", (
        "'import _revision; _revision.bind(r, v)'\n"), (False, 0)),
    ("dead-if-literal-bind", (
        "if False:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (False, 0)),
    ("live-if-literal-bind", (
        "if True:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (True, 0)),
    ("live-if-else-inactive", (
        "if True:\n"
        "    pass\n"
        "else:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (False, 0)),
    ("dead-while-literal-bind", (
        "while False:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (False, 0)),
    ("live-while-else-live-bind", (
        "while False:\n"
        "    pass\n"
        "else:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (True, 0)),
    ("live-while-true-body-bind", (
        "while True:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (True, 0)),
    ("unbound-attr-without-module-import", (
        "from _revision import bind\n"
        "_revision.bind(r, v)\n"), (False, 0)),
    ("local-copy-plus-live-bind", (
        "import _revision\n"
        "_revision.bind(r, v)\n"
        "REV = re.compile(r\"^[0-9a-f]{7,64}$\")\n"), (True, 1)),
    ("syntax-error", "def broken(:\n", (False, 0)),
]

# Non-gating observations: currently mis-classified by the unchanged census but
# intentionally outside the minimal proposal (documented limitation boundary).
OBSERVE = [
    ("dead-if-constant-compare-bind", (
        "if 1 == 2:\n"
        "    import _revision\n"
        "    _revision.bind(r, v)\n"), (False, 0)),
    ("dead-if-nested-nonconstant", (
        "def f():\n"
        "    if os.environ.get(\"X\"):\n"
        "        import _revision\n"
        "        _revision.bind(r, v)\n"), (False, 0)),
]

BASELINE_SNIPPET = "isinstance(node, ast.If) and isinstance(node.test, ast.Constant)"
PATCHED_SNIPPET = (
    "isinstance(node, (ast.If, ast.While)) and isinstance(node.test, ast.Constant)")


def load_judge(path: Path):
    """Load the lane judge from a private copy; never execute its main()."""
    spec = importlib.util.spec_from_file_location("tsukuroi_baseline_judge", path)
    assert spec is not None and spec.loader is not None, "importlib could not load judge"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, SHARED_FN), f"judge lacks {SHARED_FN}()"
    return module


def patch_shared(text: str) -> str:
    """Apply the precise proposal patch to the census (assert exactly one site)."""
    if text.count(BASELINE_SNIPPET) != 1:
        raise RuntimeError(f"baseline snippet found {text.count(BASELINE_SNIPPET)} times, expected 1")
    return text.replace(BASELINE_SNIPPET, PATCHED_SNIPPET)


def run_matrix(shared, cases):
    out = []
    for label, source, want in cases:
        got = tuple(shared(source))
        out.append({"label": label, "uses": got[0], "copies": got[1],
                    "expected_uses": want[0], "expected_copies": want[1],
                    "passed": got == want})
    return out


def main(argv):
    with tempfile.TemporaryDirectory(prefix="tsukuroi-src-ast-bind-") as tmp:
        tmp = Path(tmp)
        baseline_copy = tmp / "check-revision-binding.py"
        shutil.copyfile(JUDGE, baseline_copy)
        module = load_judge(baseline_copy)

        baseline = run_matrix(module.shared, CASES)
        baseline_obs = run_matrix(module.shared, OBSERVE)

        patched_text = patch_shared(baseline_copy.read_text(encoding="utf-8"))
        patched_copy = tmp / "check-revision-binding-patched.py"
        patched_copy.write_text(patched_text, encoding="utf-8")
        patched_module = load_judge(patched_copy)
        patched = run_matrix(patched_module.shared, CASES)
        patched_obs = run_matrix(patched_module.shared, OBSERVE)

    green_after = all(c["passed"] for c in patched)
    red_before = not all(c["passed"] for c in baseline)
    report = {
        "subject": "source AST binding test (design item 4/12)",
        "judge_source": str(JUDGE),
        "baseline": {"cases": baseline, "observations": baseline_obs,
                     "all_passed": not red_before},
        "patched": {"cases": patched, "observations": patched_obs,
                    "all_passed": green_after},
        "contract": {"red_before": red_before, "green_after": green_after},
        "exit": 0 if (red_before and green_after) else 1,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return report["exit"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
