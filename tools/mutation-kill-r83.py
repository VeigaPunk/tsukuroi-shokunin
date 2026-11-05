#!/usr/bin/env python3
"""C1 counter, round 83 — the re-encoded mutation recipes against the pinned tools.

Round 82's frozen recipe set stored two `old` strings (`C16-empty-manifest`,
`M06-mutation-unlink-noop`) with a two-character `\\` + `n` where the tool bytes carry
a real newline, so `source.count(old) == 0` at every revision and the frozen target
(`killed >= 24/26` and `genuine == 17/17`) was unreachable by construction (R82-V1;
ceiling 22/26 and 16/17, recorded — not repaired — in round 82). This round's
apparatus is the same 26 recipes with those two cells re-encoded to real newlines
(`.ufo/waves/round-83/before/mutants-r83.json`), and this harness.

Deltas from `tools/mutation-kill-r82.py` (bytes frozen; the r82 harness and its
receipts stand as history):

  * `--recipes PATH` — the recipe file is a declared input, not a constant; the
    default is this round's re-encoded set and the run records its sha256;
  * a selftest that times out or cannot be launched is an *unobserved verdict*
    (R82-V4): recorded `killed: false` with reason `selftest-unobserved`, listed in
    `unobserved`, and never counted as a kill. An unobserved mutant therefore holds
    both legs below their targets — a timed-out detector can no longer forge a kill;
  * `--timeout SECONDS` bounds one selftest (default 300; the selftest suite uses 2
    to exercise the timeout arm quickly);
  * subprocess environments keep `PYTHONDONTWRITE_BYTECODE` semantics
    (`PYTHONDONTWRITEBYTECODE=1`) and the module keeps `sys.dont_write_bytecode`,
    so measuring writes no `tools/__pycache__` into the lane (R82-V6).

What a *kill* is, unchanged: the mutant's own `--selftest` exits non-zero. A recipe
whose `old` string occurs other than exactly once in the pinned tool bytes is not a
kill (fail closed). A red pristine baseline is `could-not-evaluate`, never a pass.

  --revision REV   read every tool and the recipe file at a landed lane revision
  --recipes PATH   recipe file path, repo-relative (default: this round's set)
  --work DIR       scratch root (default: a fresh temporary directory under $TMPDIR)
  --timeout N      per-selftest bound in seconds (default 300)
  --selftest       hermetic case suite over a temporary tree; writes nothing outside it

Exit: 0 met / 1 unmet / 2 could-not-evaluate / 3 selftest failed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

RECIPES = ".ufo/waves/round-83/before/mutants-r83.json"
HELPER = "tools/_revision.py"
TARGET_KILLED = 24
TARGET_GENUINE = 17
CLAIM = "C1"


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


def run_selftest(path, work, timeout):
    """(rc, tail, observed) of `python3 <path> --selftest`; observed=False = unobserved."""
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin", "TMPDIR": str(work),
           "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C.UTF-8"}
    try:
        proc = subprocess.run(
            [sys.executable, str(path), "--selftest"], cwd=str(work),
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            env=env, timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return None, f"selftest-timeout:exceeded-{timeout}s", False
    except OSError as exc:
        return None, f"selftest-unlaunchable:{exc}"[:160], False
    body = proc.stdout.decode("utf-8", "replace").strip().splitlines()
    return proc.returncode, (body[-1] if body else "")[:200], True


def measure(root, revision=None, work=None, recipes_path=RECIPES, timeout=300):
    """Return (killed, genuine_killed, records, unobserved, finding). Raises CannotEvaluate."""
    try:
        recipes_text = read_at(root, recipes_path, revision)
    except CannotEvaluate:
        raise CannotEvaluate("recipes-absent")
    recipes = json.loads(recipes_text)
    if not isinstance(recipes, list) or not recipes:
        raise CannotEvaluate("recipes-absent")
    recipes_sha = hashlib.sha256(recipes_text.encode("utf-8")).hexdigest()

    tools = {}
    for tool in sorted({r["tool"] for r in recipes}):
        tools[tool] = read_at(root, f"tools/{tool}", revision)
    helper = None
    try:
        helper = read_at(root, HELPER, revision)
    except CannotEvaluate:
        helper = None

    scratch = Path(work) if work else Path(tempfile.mkdtemp(prefix="mutkill83-"))
    scratch.mkdir(parents=True, exist_ok=True)
    records, killed, genuine_killed, unobserved = [], 0, 0, []
    try:
        # Baseline: every pristine tool must be green before any mutant is scored.
        for tool, source in tools.items():
            base = scratch / "base" / tool[:-3]
            base.mkdir(parents=True, exist_ok=True)
            (base / tool).write_text(source, encoding="utf-8")
            if helper is not None:
                (base / "_revision.py").write_text(helper, encoding="utf-8")
            rc, tail, observed = run_selftest(base / tool, base, timeout)
            if rc != 0:
                raise CannotEvaluate(f"baseline-red:{tool}:rc={rc}:{tail}")

        for recipe in recipes:
            rid, tool = recipe["id"], recipe["tool"]
            source = tools[tool]
            old, new = recipe["old"], recipe["new"]
            seen = source.count(old)
            if seen != 1:
                records.append({"id": rid, "tool": tool, "genuine_gap": bool(recipe.get("genuine_gap")),
                                "killed": False, "rc": None, "observed": False,
                                "detail": f"recipe-missing:old-string-occurs-{seen}x"})
                continue
            mutant_dir = scratch / "mut" / rid
            mutant_dir.mkdir(parents=True, exist_ok=True)
            (mutant_dir / tool).write_text(source.replace(old, new), encoding="utf-8")
            if helper is not None:
                (mutant_dir / "_revision.py").write_text(helper, encoding="utf-8")
            rc, tail, observed = run_selftest(mutant_dir / tool, mutant_dir, timeout)
            is_killed = bool(observed and rc != 0)
            killed += int(is_killed)
            genuine_killed += int(is_killed and bool(recipe.get("genuine_gap")))
            if not observed:
                unobserved.append(rid)
            records.append({"id": rid, "tool": tool, "genuine_gap": bool(recipe.get("genuine_gap")),
                            "killed": is_killed, "rc": rc, "observed": observed, "detail": tail})
    finally:
        if work is None:
            shutil.rmtree(scratch, ignore_errors=True)

    finding = "met" if killed >= TARGET_KILLED and genuine_killed == TARGET_GENUINE else "unmet"
    return killed, genuine_killed, records, unobserved, finding, recipes_sha


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

FAKE_SLEEP = """#!/usr/bin/env python3
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
    with tempfile.TemporaryDirectory(prefix="mutkill83-selftest-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "tools" / "fake.py").write_text(FAKE, encoding="utf-8")
        (root / RECIPES).parent.mkdir(parents=True, exist_ok=True)
        (root / RECIPES).write_text(json.dumps(recipes), encoding="utf-8")
        try:
            killed, genuine, records, unobserved, finding, sha = measure(root)
            cases.append(("kill-and-survive",
                          killed == 1 and genuine == 1 and finding == "unmet" and not unobserved,
                          f"killed={killed} genuine={genuine} finding={finding}"))
            missing = [r for r in records if r["id"] == "K3-recipe-missing"][0]
            cases.append(("recipe-missing-is-not-a-kill",
                          missing["killed"] is False and "recipe-missing" in missing["detail"],
                          missing["detail"]))
            cases.append(("recipes-sha-recorded", len(sha) == 64, sha[:16]))
        except CannotEvaluate as exc:
            cases.append(("hermetic-fixture", False, f"unexpected could-not-evaluate {exc}"))

    with tempfile.TemporaryDirectory(prefix="mutkill83-selftest-") as tmp:
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

    with tempfile.TemporaryDirectory(prefix="mutkill83-selftest-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        try:
            measure(root)
            cases.append(("no-recipes-refuses", False, "measure() returned a verdict"))
        except CannotEvaluate as exc:
            cases.append(("no-recipes-refuses", "recipes-absent" in str(exc), str(exc)[:120]))

    # R82-V4 red control: a selftest that never finishes is unobserved, not a kill.
    # The baseline is green; the mutant injects the sleep, so only the mutant hangs.
    with tempfile.TemporaryDirectory(prefix="mutkill83-selftest-") as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "tools" / "fake.py").write_text(FAKE_SLEEP, encoding="utf-8")
        (root / RECIPES).parent.mkdir(parents=True, exist_ok=True)
        (root / RECIPES).write_text(json.dumps([
            {"id": "T1-timeout", "tool": "fake.py", "clause": "c",
             "old": "raise SystemExit(main())",
             "new": "import time\ntime.sleep(30)\nraise SystemExit(main())",
             "genuine_gap": True}]), encoding="utf-8")
        try:
            killed, genuine, records, unobserved, finding, sha = measure(root, timeout=2)
            rec = records[0]
            cases.append(("timeout-is-not-a-kill",
                          killed == 0 and genuine == 0 and finding == "unmet"
                          and rec["killed"] is False and rec["observed"] is False
                          and unobserved == ["T1-timeout"],
                          f"killed={killed} rc={rec['rc']} detail={rec['detail'][:80]}"))
        except CannotEvaluate as exc:
            cases.append(("timeout-is-not-a-kill", False, f"unexpected could-not-evaluate {exc}"))

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
    p.add_argument("--recipes", default=RECIPES)
    p.add_argument("--timeout", type=int, default=300)
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
        killed, genuine, records, unobserved, finding, recipes_sha = measure(
            a.fixture if a.fixture else repo, revision, a.work,
            recipes_path=a.recipes, timeout=a.timeout)
    except CannotEvaluate as exc:
        print(json.dumps({"claim": CLAIM, "revision": revision, "killed": 0,
                          "target_killed": TARGET_KILLED, "finding": "cannot-evaluate",
                          "problems": [str(exc)]}))
        return 2

    survivors = [r["id"] for r in records if not r["killed"]]
    print(json.dumps({"claim": CLAIM, "revision": revision, "killed": killed,
                      "total": len(records), "genuine_killed": genuine,
                      "target_killed": TARGET_KILLED, "target_genuine": TARGET_GENUINE,
                      "recipes": a.recipes, "recipes_sha256": recipes_sha,
                      "unobserved": unobserved,
                      "finding": finding, "survivors": survivors, "records": records}))
    return 0 if finding == "met" else 1


if __name__ == "__main__":
    raise SystemExit(main())
