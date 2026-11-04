#!/usr/bin/env python3
"""C2 counter, round 82 — how many of the committed single-clause mutants the
counters' own `--selftest` kills.

The 26 recipes were derived by the round-81 mutation seat and are committed verbatim
at `.ufo/waves/round-82/before/mutants-r82.json` (id, tool, clause, old, new,
genuine_gap).  A mutant is *killed* when its own `--selftest` exits non-zero; the
selftest is the only detector this counter uses, because a green selftest is what the
lane claims to an operator.

The two recipes marked `genuine_gap: false` are equivalent mutants (round-81
MutCounter C06/C07): no input separates them, so no test can kill them and the
target excludes them from the "all genuine gaps killed" leg.

  --revision REV   read every tool and recipe at a landed lane revision
  --work DIR       scratch root (default: $TMPDIR or a fresh temporary directory)
  --selftest       hermetic case suite over a temporary tree; writes nothing outside it

Exit: 0 met / 1 unmet / 2 could-not-evaluate / 3 selftest failed.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

RECIPES = ".ufo/waves/round-82/before/mutants-r82.json"
HELPER = "tools/_revision.py"
TARGET_KILLED = 24
TARGET_GENUINE = 17
CLAIM = "C2"


class CannotEvaluate(Exception):
    """Inputs are absent or unusable: this is not a verdict."""


def read_at(root, path, revision):
    if revision is None:
        target = Path(root) / path
        if not target.is_file():
            raise CannotEvaluate(f"absent:{path}")
        return target.read_text(encoding="utf-8", errors="replace")
    proc = subprocess.run(
        ["git", "--no-pager", "-C", str(root), "show", f"{revision}:{path}"],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120,
    )
    if proc.returncode != 0:
        raise CannotEvaluate(f"absent-at-revision:{path}")
    return proc.stdout.decode("utf-8", "replace")


def run_selftest(path, work):
    """rc of `python3 <path> --selftest`; the mutant's own public detector."""
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "TMPDIR": str(work),
           "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C.UTF-8"}
    try:
        proc = subprocess.run(
            [sys.executable, str(path), "--selftest"], cwd=str(work),
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env=env, timeout=300,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        return 124, f"selftest-did-not-finish: {exc}"[:160]
    body = proc.stdout.decode("utf-8", "replace").strip().splitlines()
    return proc.returncode, (body[-1] if body else "")[:200]


def measure(root, revision=None, work=None):
    """Return (killed, genuine_killed, records, finding). Raises CannotEvaluate."""
    try:
        recipes = json.loads(read_at(root, RECIPES, revision))
    except CannotEvaluate:
        raise CannotEvaluate("recipes-absent")
    if not isinstance(recipes, list) or not recipes:
        raise CannotEvaluate("recipes-absent")

    tools = {}
    for tool in sorted({r["tool"] for r in recipes}):
        tools[tool] = read_at(root, f"tools/{tool}", revision)
    helper = None
    try:
        helper = read_at(root, HELPER, revision)
    except CannotEvaluate:
        helper = None

    scratch = Path(work) if work else Path(tempfile.mkdtemp(prefix="mutkill-"))
    scratch.mkdir(parents=True, exist_ok=True)
    records, killed, genuine_killed = [], 0, 0
    try:
        # Baseline: every pristine tool must be green before any mutant is scored.
        for tool, source in tools.items():
            base = scratch / "base" / tool[:-3]
            base.mkdir(parents=True, exist_ok=True)
            (base / tool).write_text(source, encoding="utf-8")
            if helper is not None:
                (base / "_revision.py").write_text(helper, encoding="utf-8")
            rc, tail = run_selftest(base / tool, base)
            if rc != 0:
                raise CannotEvaluate(f"baseline-red:{tool}:rc={rc}:{tail}")

        for recipe in recipes:
            rid, tool = recipe["id"], recipe["tool"]
            source = tools[tool]
            old, new = recipe["old"], recipe["new"]
            seen = source.count(old)
            if seen != 1:
                records.append({"id": rid, "tool": tool, "genuine_gap": bool(recipe.get("genuine_gap")),
                                "killed": False, "rc": None,
                                "detail": f"recipe-missing:old-string-occurs-{seen}x"})
                continue
            mutant_dir = scratch / "mut" / rid
            mutant_dir.mkdir(parents=True, exist_ok=True)
            (mutant_dir / tool).write_text(source.replace(old, new), encoding="utf-8")
            if helper is not None:
                (mutant_dir / "_revision.py").write_text(helper, encoding="utf-8")
            rc, tail = run_selftest(mutant_dir / tool, mutant_dir)
            is_killed = rc != 0
            killed += int(is_killed)
            genuine_killed += int(is_killed and bool(recipe.get("genuine_gap")))
            records.append({"id": rid, "tool": tool, "genuine_gap": bool(recipe.get("genuine_gap")),
                            "killed": is_killed, "rc": rc, "detail": tail})
    finally:
        if work is None:
            shutil.rmtree(scratch, ignore_errors=True)

    finding = "met" if killed >= TARGET_KILLED and genuine_killed == TARGET_GENUINE else "unmet"
    return killed, genuine_killed, records, finding


FAKE = """#!/usr/bin/env python3
import sys
TARGET = 2
def count(rows):
    return len([r for r in rows if r.get('ok')])
def main():
    rows = [{'ok': True}, {'ok': True}]
    n = count(rows)
    if n != TARGET:
        print('too many')
        return 3
    print('SELFTEST total=1 passed=1 failed=0')
    return 0
raise SystemExit(main())
"""


def selftest():
    cases = []
    recipes = [
        {"id": "K1-kills", "tool": "fake.py", "clause": "target", "old": "TARGET = 2",
         "new": "TARGET = 99", "genuine_gap": True},
        {"id": "K2-survives", "tool": "fake.py", "clause": "equivalent", "old": "import sys",
         "new": "import sys  # noqa", "genuine_gap": False},
        {"id": "K3-recipe-missing", "tool": "fake.py", "clause": "absent", "old": "not in file",
         "new": "x", "genuine_gap": True},
    ]
    with tempfile.TemporaryDirectory(prefix="mutkill-selftest-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "tools" / "fake.py").write_text(FAKE, encoding="utf-8")
        (root / RECIPES).parent.mkdir(parents=True, exist_ok=True)
        (root / RECIPES).write_text(json.dumps(recipes), encoding="utf-8")
        try:
            killed, genuine, records, finding = measure(root)
            cases.append(("kill-and-survive",
                          killed == 1 and genuine == 1 and finding == "unmet",
                          f"killed={killed} genuine={genuine} finding={finding}"))
            missing = [r for r in records if r["id"] == "K3-recipe-missing"][0]
            cases.append(("recipe-missing-is-not-a-kill",
                          missing["killed"] is False and "recipe-missing" in missing["detail"],
                          missing["detail"]))
        except CannotEvaluate as exc:
            cases.append(("hermetic-fixture", False, f"unexpected could-not-evaluate {exc}"))

    with tempfile.TemporaryDirectory(prefix="mutkill-selftest-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "tools" / "fake.py").write_text("#!/usr/bin/env python3\nimport sys\nraise SystemExit(4)\n",
                                                encoding="utf-8")
        (root / RECIPES).parent.mkdir(parents=True, exist_ok=True)
        (root / RECIPES).write_text(json.dumps([{"id": "K", "tool": "fake.py", "clause": "c",
                                                 "old": "import sys", "new": "import os",
                                                 "genuine_gap": True}]), encoding="utf-8")
        try:
            measure(root)
            cases.append(("red-baseline-refuses", False, "measure() returned a verdict"))
        except CannotEvaluate as exc:
            cases.append(("red-baseline-refuses", "baseline-red" in str(exc), str(exc)[:120]))

    with tempfile.TemporaryDirectory(prefix="mutkill-selftest-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        try:
            measure(root)
            cases.append(("no-recipes-refuses", False, "measure() returned a verdict"))
        except CannotEvaluate as exc:
            cases.append(("no-recipes-refuses", "recipes-absent" in str(exc), str(exc)[:120]))

    failed = [c for c in cases if not c[1]]
    for name, ok, observed in cases:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {observed}")
    print(f"SELFTEST total={len(cases)} passed={len(cases) - len(failed)} failed={len(failed)}")
    return 0 if not failed else 3


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision")
    group.add_argument("--fixture", type=Path)
    group.add_argument("--selftest", action="store_true")
    p.add_argument("--repo", default=".")
    p.add_argument("--branch", default="master")
    p.add_argument("--work", type=Path)
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()

    repo = Path(a.repo).resolve()
    revision = None
    if a.revision:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import _revision  # noqa: E402  (shared landed-revision binding, QUALITY 27)
        try:
            revision = _revision.bind(repo, a.revision, a.branch).sha
        except _revision.RevisionError as exc:
            print(json.dumps({"claim": CLAIM, "revision": a.revision,
                              "finding": "cannot-evaluate", "problems": [str(exc)]}))
            return 2

    try:
        killed, genuine, records, finding = measure(
            a.fixture if a.fixture else repo, revision, a.work)
    except CannotEvaluate as exc:
        print(json.dumps({"claim": CLAIM, "revision": revision, "killed": 0,
                          "target_killed": TARGET_KILLED, "finding": "cannot-evaluate",
                          "problems": [str(exc)]}))
        return 2

    survivors = [r["id"] for r in records if not r["killed"]]
    print(json.dumps({"claim": CLAIM, "revision": revision, "killed": killed,
                      "total": len(records), "genuine_killed": genuine,
                      "target_killed": TARGET_KILLED, "target_genuine": TARGET_GENUINE,
                      "finding": finding, "survivors": survivors, "records": records}))
    return 0 if finding == "met" else 1


if __name__ == "__main__":
    raise SystemExit(main())
