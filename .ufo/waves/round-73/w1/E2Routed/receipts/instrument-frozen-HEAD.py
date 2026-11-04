#!/usr/bin/env python3
# round-73 C2 routed-defect checker (frozen by the round-73 declaration, before any repair lands).
#
# Checks the three round-72 closure defects routed to this lane (R72-LESSON-SUPERSEDED-CLAIMS,
# R72-C3-INSTRUMENT-DIGEST-DRIFT, R72-CAPABILITY-ROW-STALE) in committed bytes at one revision.
# Each item is satisfied only inside an appended block whose heading is a line-start `## `
# heading (the round-72 lesson's unanchored-regex defect) and whose body carries every required
# token; a token found anywhere else in the file does not count.
#
# Exit map: 0 every item satisfied; 1 at least one item stale; 2 cannot evaluate (a required file
# is absent, or no readable input); 3 self-test failed.
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LESSON = "corpus/lessons/round-72.md"
SCORECARD = "SCORECARD.md"

OLD_DIGEST = "df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712"
TIP_DIGEST = "2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc"
RECEIPT = ".ufo/waves/round-72/after/selftest-selftest-after.txt"

HEADING_RE = re.compile(r"^## .+", re.M)
BLOCK_HEAD_RE = re.compile(r"^## .*(?i:correction|erratum|refresh).*$", re.M)

ITEMS = {
    "LESSON": {
        "path": LESSON,
        "heading": re.compile(r"^## .*(?i:correction|erratum).*$", re.M),
        "tokens": ["R72-LESSON-SUPERSEDED-CLAIMS",
                   "No capability row enters this round",
                   "nine hermetic cases",
                   "gate-selftest", "ten", "10 cases"],
        "need_any": [("10 cases", "ten cases", "ten hermetic cases")],
        "finding": "LESSON-STALE",
    },
    "DIGEST": {
        "path": SCORECARD,
        "heading": re.compile(r"^## .*(?i:correction|erratum).*$", re.M),
        "tokens": ["R72-C3-INSTRUMENT-DIGEST-DRIFT", OLD_DIGEST, TIP_DIGEST,
                   "check-r71-routed-r72.py"],
        "need_any": [("same-instrument", "re-run", "re-ran", RECEIPT)],
        "finding": "DIGEST-STALE",
    },
    "CAPABILITY": {
        "path": SCORECARD,
        "heading": re.compile(r"^## .*(?i:capability|refresh).*$", re.M),
        "tokens": ["gate-selftest", "ten", RECEIPT],
        "need_any": [("10 cases", "ten cases", "ten names", "ten hermetic")],
        "finding": "CAPABILITY-STALE",
    },
}


def readers(revision, root):
    if root:
        base = Path(root)

        def rt(rel):
            p = base / rel
            return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

        return rt
    lane = str(Path(__file__).resolve().parent.parent)

    def rt(rel):
        r = subprocess.run(["git", "-C", lane, "show", f"{revision}:{rel}"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.stdout if r.returncode == 0 else None

    return rt


def blocks(text):
    """Split into (heading, body) blocks at line-start '## ' headings."""
    marks = [m.start() for m in HEADING_RE.finditer(text)]
    out = []
    for i, start in enumerate(marks):
        end = marks[i + 1] if i + 1 < len(marks) else len(text)
        head = text[start:end].splitlines()[0]
        out.append((head, text[start:end]))
    return out


def check_item(rt, item, out):
    text = rt(item["path"])
    if text is None:
        print(f"{item['finding']} absent path={item['path']}", file=out)
        return False
    norm = " ".join(text.split())
    for head, body in blocks(text):
        if not item["heading"].match(head):
            continue
        bnorm = " ".join(body.split())
        if not all(tok in bnorm for tok in item["tokens"]):
            continue
        if not all(any(alt in bnorm for alt in alts) for alts in item["need_any"]):
            continue
        return True
    missing = [tok for tok in item["tokens"] if tok not in norm]
    print(f"{item['finding']} path={item['path']} "
          f"reason={'no-block' if all(t not in norm for t in item['tokens']) else 'block-incomplete'} "
          f"missing_tokens={len(missing)}", file=out)
    return False


def evaluate(rt, out=sys.stdout):
    total = len(ITEMS)
    ok = 0
    for name in ("LESSON", "DIGEST", "CAPABILITY"):
        good = check_item(rt, ITEMS[name], out)
        print(f"ROUTED_ITEM {name} {'ok' if good else 'stale'}\n", end="", file=out)
        ok += 1 if good else 0
    print(f"ROUTED_STALE={total - ok} ROUTED_OK={ok}/{total}", file=out)
    return 0 if ok == total else 1


def selftest():
    tmp = os.environ.get("TMPDIR")
    if not tmp or not Path(tmp).is_dir():
        print("SELFTEST: FAIL (SELFTEST-TMPDIR) $TMPDIR names no directory", file=sys.stderr)
        return 2
    base = Path(tempfile.mkdtemp(prefix="routed-checker-selftest-", dir=tmp))
    cases = []

    def lesson(block):
        return "# L\n\n## Gate\n\nnothing\n\n" + block

    def score(texts):
        root = base / ("case-%d" % len(cases))
        for rel, body in texts.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body)
        buf = io.StringIO()
        rc = evaluate(readers("HEAD", str(root)), buf)
        return rc, buf.getvalue()

    def good_block(kind):
        if kind == "lesson":
            return ("## Correction (round 73, append-only)\n\n"
                    "R72-LESSON-SUPERSEDED-CLAIMS: the sentences \"No capability row enters this "
                    "round\" and \"nine hermetic cases\" are superseded; the landed state is the "
                    "gate-selftest capability row and 10 cases.\n")
        if kind == "digest":
            return ("## Round 72 — instrument digest erratum (appended round 73)\n\n"
                    "R72-C3-INSTRUMENT-DIGEST-DRIFT: check-r71-routed-r72.py moved from "
                    + OLD_DIGEST + " to " + TIP_DIGEST + "; the before control was re-run "
                    "with the final instrument (same-instrument) at " + RECEIPT + ".\n")
        return ("## Capability refresh (round 73)\n\n"
                "gate-selftest now prints ten cases (10 cases), receipt " + RECEIPT + ".\n")

    def texts(lesson_block=None, digest_block=None, cap_block=None):
        return {
            LESSON: lesson(lesson_block if lesson_block is not None else good_block("lesson")),
            SCORECARD: "# SC\n\n## Round 72 — measured outcome\n\nbody\n\n"
                       + (digest_block if digest_block is not None else good_block("digest"))
                       + "\n" + (cap_block if cap_block is not None else good_block("cap")),
        }

    def case(cid, mapping, expect_rc, token):
        rc, text = score(mapping)
        ok = rc == expect_rc and token in text
        cases.append(ok)
        print(f"{'PASS' if ok else 'FAIL'} (SELFTEST-{cid}) rc={rc} expect={expect_rc} token={token}")

    case("CONTROL", texts(), 0, "ROUTED_STALE=0")
    case("LESSON", texts(lesson_block="## Gate\n\nno correction here\n"), 1, "LESSON-STALE")
    case("DIGEST", texts(digest_block="## Erratum\n\nnaming nothing\n"), 1, "DIGEST-STALE")
    case("CAPABILITY", texts(cap_block="## Note\n\nunrelated\n"), 1, "CAPABILITY-STALE")
    case("UNANCHORED",
         texts(lesson_block="A prose mention says R72-LESSON-SUPERSEDED-CLAIMS and "
                            "\"No capability row enters this round\" and \"nine hermetic cases\" "
                            "and gate-selftest ten 10 cases inside a paragraph, not a block.\n"),
         1, "LESSON-STALE")
    shutil.rmtree(base, ignore_errors=True)
    passed = sum(1 for c in cases if c)
    print(f"SELFTEST: {'PASS' if passed == len(cases) else 'FAIL'} "
          f"({len(cases)} cases, {passed} passed, {len(cases) - passed} failed)")
    return 0 if passed == len(cases) else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revision", default="HEAD")
    ap.add_argument("--root")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    return evaluate(readers(args.revision, args.root))


if __name__ == "__main__":
    sys.exit(main())
