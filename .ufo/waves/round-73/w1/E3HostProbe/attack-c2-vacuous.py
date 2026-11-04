#!/usr/bin/env python3
"""Round-73 E3HostProbe attack on the C2 checker at its committed bytes (09dac09f).

Three fixtures, each answering one question:

  CONTROL    the declared target state, built the way the checker's own selftest builds it.
  VACUOUS    a lesson block that is only the required tokens under a `## Correction` heading,
             with no sentence — QUALITY 87's content-free row.
  CAPSUGAR   a capability block that is a bare token list (tool name, "10 cases", receipt path)
             under a matching heading, with no statement of what changed.

Run:  TMPDIR=<a non-/tmp dir> python3 attack-c2-vacuous.py
rc 0 = every fixture behaved as the instrument's own controls say it should;
rc 1 = at least one behaved otherwise (the printed rows say which).
"""
import importlib.util
import io
import os
import pathlib
import shutil
import sys
import tempfile

CHECKER = "tools/check-r72-routed-r73.py"

LESSON = "corpus/lessons/round-72.md"
SCORECARD = "SCORECARD.md"


def load():
    spec = importlib.util.spec_from_file_location("c2", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(m, root, lesson_block, digest_block, cap_block, receipt="SELFTEST: PASS (10 cases, 10 passed, 0 failed)\nrc=0\n"):
    tree = {
        LESSON: "# L\n\n## Gate\n\nnothing\n\n" + lesson_block,
        SCORECARD: "# SC\n\n## Round 72 — measured outcome\n\nbody\n\n" + digest_block + "\n" + cap_block,
    }
    if receipt is not None:
        tree[m.RECEIPT] = receipt
    for rel, body in tree.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    buf = io.StringIO()
    rc = m.evaluate(m.readers("HEAD", str(root)), buf)
    return rc, buf.getvalue()


def main():
    tmp = os.environ.get("TMPDIR")
    if not tmp or not pathlib.Path(tmp).is_dir():
        print("ATTACK: cannot evaluate, TMPDIR names no directory", file=sys.stderr)
        return 2
    m = load()
    base = pathlib.Path(tempfile.mkdtemp(prefix="c2-attack-", dir=tmp))
    bad = 0

    rc, text = run(m, base / "control", m.GOOD_LESSON, m.GOOD_DIGEST, m.GOOD_CAP)
    ok = rc == 0 and "ROUTED_STALE=0" in text
    print(("PASS" if ok else "FAIL"), "CONTROL rc=%d" % rc)
    bad += 0 if ok else 1

    vacuous = ("## Correction (round 73)\n\nR72-LESSON-SUPERSEDED-CLAIMS "
               "No capability row enters this round nine hermetic cases gate-selftest ten 10 cases\n")
    rc, text = run(m, base / "vacuous", vacuous, m.GOOD_DIGEST, m.GOOD_CAP)
    ok = "LESSON-STALE" in text
    print(("PASS" if ok else "FAIL"), "VACUOUS   lesson credited without a sentence —", text.splitlines()[0] if text else "(no output)")
    bad += 0 if ok else 1

    cap_sugar = ("## Capability refresh (round 73)\n\ngate-selftest 10 cases "
                 + m.RECEIPT + "\n")
    rc, text = run(m, base / "capsugar", m.GOOD_LESSON, m.GOOD_DIGEST, cap_sugar)
    credited = "CAPABILITY-STALE" not in text
    print(("SURVIVED" if credited else "HELD    "),
          "CAPSUGAR  a bare token list under the heading was %s" % ("credited" if credited else "refused"))
    for _l in text.splitlines():
        print("          |", _l)

    shutil.rmtree(base, ignore_errors=True)
    print("ATTACK:", "held on the instrument's own controls" if bad == 0 else "the instrument's controls do not hold")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
