#!/usr/bin/env python3
# round-73 C2 routed-defect checker (declared and frozen before any repair; hardened post-data
# against the wave's attacks — see SCORECARD "Round 73 — C2 instrument repair").
#
# Checks the three round-72 closure defects routed to this lane (R72-LESSON-SUPERSEDED-CLAIMS,
# R72-C3-INSTRUMENT-DIGEST-DRIFT, R72-CAPABILITY-ROW-STALE) in committed bytes at one revision.
# Each item is satisfied only inside an appended block whose heading is a line-start `## `
# heading (the round-72 lesson's unanchored-regex defect) and whose body carries every required
# token as a whole token (not a substring), a supersession verb, and — for the two receipt-bearing
# items — a receipt file that exists at the same revision and reports at least ten cases.
#
# Exit map: 0 every item satisfied; 1 at least one item stale (an absent data file is a stale finding,
# not a cannot-evaluate); 2 cannot evaluate under --selftest only ($TMPDIR names no directory);
# 3 self-test failed.
import argparse
import io
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
MIN_CASES = 10

HEADING_RE = re.compile(r"^#{2,3} .+", re.M)
SUPERSEDE_RE = re.compile(r"(?i)\b(supersed\w*|correct\w*|clos\w*|replac\w*|record\w*|erratum)\b")
DIRECTION_RE = re.compile(
    re.escape(OLD_DIGEST) + r".{0,240}?(→|->|\bto\b|\bmoved from\b|\bsuperseded by\b).{0,240}?"
    + re.escape(TIP_DIGEST), re.S)

ITEMS = {
    "LESSON": {
        "path": LESSON,
        "heading": re.compile(r"^## .*(?i:correction|erratum).*$", re.M),
        "label": "R72-LESSON-SUPERSEDED-CLAIMS",
        "tokens": ["R72-LESSON-SUPERSEDED-CLAIMS",
                   "No capability row enters this round",
                   "nine hermetic cases",
                   "gate-selftest"],
        "need_any": [("10 cases", "ten cases", "ten hermetic cases", "ten")],
        "need_verb": True,
        "need_receipt": True,
        "finding": "LESSON-STALE",
    },
    "DIGEST": {
        "path": SCORECARD,
        "heading": re.compile(r"^## .*(?i:correction|erratum).*$", re.M),
        "label": "R72-C3-INSTRUMENT-DIGEST-DRIFT",
        "tokens": ["R72-C3-INSTRUMENT-DIGEST-DRIFT", OLD_DIGEST, TIP_DIGEST,
                   "check-r71-routed-r72.py"],
        "need_any": [("same-instrument", "re-run", "re-ran", RECEIPT)],
        "need_direction": True,
        "finding": "DIGEST-STALE",
    },
    "CAPABILITY": {
        "path": SCORECARD,
        "heading": re.compile(r"^## .*(?i:capability|refresh).*$", re.M),
        "tokens": ["gate-selftest", RECEIPT],
        "need_any": [("10 cases", "ten cases", "ten names", "ten hermetic", "ten")],
        "need_receipt": True,
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


def has_token(text, tok):
    """Whole-token match: a substring of another word does not count (wave attack F7).

    A token that looks like a path (contains "/") must also not be a proper prefix or suffix of a
    longer path (wave attack F4: `selftest-selftest-after.txt.bak` passed a substring test)."""
    if "/" in tok:
        return re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(tok)
                         + r"(?!\.[A-Za-z0-9])(?![A-Za-z0-9_/-])", text) is not None
    return re.search(r"(?<![A-Za-z0-9_-])" + re.escape(tok) + r"(?![A-Za-z0-9_-])", text) is not None


def receipt_cases(rt):
    """(present, case count or None) for the committed receipt."""
    body = rt(RECEIPT)
    if body is None:
        return False, None
    m = None
    for line in body.splitlines():
        mm = re.search(r"SELFTEST: PASS \((\d+) cases?,\s*(\d+) passed,\s*(\d+) failed\)", line)
        if mm:
            m = mm
    if not m:
        return True, None
    return True, int(m.group(1))


def check_item(rt, item, out):
    text = rt(item["path"])
    if text is None:
        print(f"{item['finding']} absent path={item['path']}", file=out)
        return False
    present, cases = receipt_cases(rt)
    if item.get("need_receipt") and not present:
        print(f"{item['finding']} path={item['path']} reason=receipt-absent path={RECEIPT}", file=out)
        return False
    if item.get("need_receipt") and (cases is None or cases < MIN_CASES):
        print(f"{item['finding']} path={item['path']} reason=receipt-count cases={cases}", file=out)
        return False
    reasons = []
    for head, body in blocks(text):
        if not item["heading"].match(head):
            continue
        full = " ".join(body.split())
        body_only = " ".join(" ".join(body.splitlines()[1:]).split()) if body.startswith("#") else full
        label = item.get("label")
        if label and not has_token(full, label):
            reasons.append("block-label")
            continue
        if not all(has_token(body_only, tok) for tok in item["tokens"] if tok != label):
            reasons.append("block-tokens")
            continue
        bnorm = body_only
        if not all(any(has_token(bnorm, alt) for alt in alts) for alts in item["need_any"]):
            reasons.append("block-need-any")
            continue
        if item.get("need_verb"):
            stripped = " ".join(body.splitlines()[1:]) if body.startswith("## ") else bnorm
            stripped = " ".join(stripped.split())
            for tok in item["tokens"]:
                stripped = stripped.replace(tok, " ")
            if not SUPERSEDE_RE.search(stripped):
                reasons.append("block-no-supersede-verb")
                continue
        if item.get("need_direction") and not DIRECTION_RE.search(bnorm):
            reasons.append("block-digest-direction")
            continue
        return True
    norm = " ".join(text.split())
    if not reasons:
        reasons = ["no-block" if not all(has_token(norm, t) for t in item["tokens"])
                   else "block-incomplete"]
    print(f"{item['finding']} path={item['path']} reason={reasons[0]}", file=out)
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


GOOD_LESSON = """## Correction (round 73, append-only)

R72-LESSON-SUPERSEDED-CLAIMS: the sentences "No capability row enters this round" and "nine
hermetic cases" are superseded; the landed state is the gate-selftest capability row and 10 cases.
"""

GOOD_DIGEST = ("## Round 72 — instrument digest erratum (appended round 73)\n\n"
               "R72-C3-INSTRUMENT-DIGEST-DRIFT: check-r71-routed-r72.py moved from " + OLD_DIGEST
               + " to " + TIP_DIGEST + "; the before control was re-run with the final instrument "
               "(same-instrument) at " + RECEIPT + ".\n")

GOOD_CAP = ("## Capability refresh (round 73)\n\n"
            "gate-selftest now prints ten cases (10 cases), receipt " + RECEIPT + ".\n")

RECEIPT_BODY = "SELFTEST: PASS (10 cases, 10 passed, 0 failed)\nrc=0\n"


def selftest():
    tmp = os.environ.get("TMPDIR")
    if not tmp or not Path(tmp).is_dir():
        print("SELFTEST: FAIL (SELFTEST-TMPDIR) $TMPDIR names no directory", file=sys.stderr)
        return 2
    base = Path(tempfile.mkdtemp(prefix="routed-checker-selftest-", dir=tmp))
    cases = []

    def texts(lesson_block=None, digest_block=None, cap_block=None, receipt=RECEIPT_BODY):
        tree = {
            LESSON: "# L\n\n## Gate\n\nnothing\n\n"
                    + (GOOD_LESSON if lesson_block is None else lesson_block),
            SCORECARD: "# SC\n\n## Round 72 — measured outcome\n\nbody\n\n"
                       + (GOOD_DIGEST if digest_block is None else digest_block)
                       + "\n" + (GOOD_CAP if cap_block is None else cap_block),
        }
        if receipt is not None:
            tree[RECEIPT] = receipt
        return tree

    def case(cid, mapping, expect_rc, token):
        root = base / ("case-%d" % len(cases))
        for rel, body in mapping.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body)
        buf = io.StringIO()
        rc = evaluate(readers("HEAD", str(root)), buf)
        text = buf.getvalue()
        ok = rc == expect_rc and token in text
        cases.append(ok)
        print(f"{'PASS' if ok else 'FAIL'} (SELFTEST-{cid}) rc={rc} expect={expect_rc} token={token}")

    case("CONTROL", texts(), 0, "ROUTED_STALE=0")
    case("LESSON", texts(lesson_block="## Gate\n\nno correction here\n"), 1, "LESSON-STALE")
    case("DIGEST", texts(digest_block="## Erratum\n\nnaming nothing\n"), 1, "DIGEST-STALE")
    case("CAPABILITY", texts(cap_block="## Note\n\nunrelated\n"), 1, "CAPABILITY-STALE")
    case("UNANCHORED",
         texts(lesson_block="A prose mention says R72-LESSON-SUPERSEDED-CLAIMS and \"No capability "
                            "row enters this round\" and \"nine hermetic cases\" and gate-selftest "
                            "ten 10 cases inside a paragraph.\n"),
         1, "LESSON-STALE")
    case("RECEIPT-SUPERSTRING",
         texts(cap_block=GOOD_CAP.replace(RECEIPT, RECEIPT + ".bak")), 1, "CAPABILITY-STALE")
    case("RECEIPT-MISSING", texts(receipt=None), 1, "receipt-absent")
    case("RECEIPT-NINE", texts(receipt="SELFTEST: PASS (9 cases, 9 passed, 0 failed)\n"),
         1, "receipt-count")
    case("SUBSTRING-TEN",
         texts(cap_block="## Capability refresh (round 73)\n\ngate-selftest now often prints "
                         "cases, receipt " + RECEIPT + ".\n"),
         1, "CAPABILITY-STALE")
    case("DIGEST-REVERSED",
         texts(digest_block="## Round 72 — instrument digest erratum (appended round 73)\n\n"
                            "R72-C3-INSTRUMENT-DIGEST-DRIFT: check-r71-routed-r72.py moved from "
                            + TIP_DIGEST + " to " + OLD_DIGEST
                            + "; the before control was re-run (same-instrument) at " + RECEIPT + ".\n"),
         1, "DIGEST-STALE")
    case("RECEIPT-FAIL", texts(receipt="SELFTEST: FAIL (10 cases, 0 passed, 10 failed)\n"),
         1, "receipt-count")

    def placeholder_map():
        m = texts()
        m[SCORECARD] = ("# SC\n\n## Correction (placeholder)\n\n### unrelated\n\n"
                        + GOOD_DIGEST.split("\n", 1)[1] + "\n" + GOOD_CAP)
        return m

    case("PLACEHOLDER", placeholder_map(), 1, "DIGEST-STALE")
    case("TITLE-TOKEN",
         texts(cap_block="## Capability refresh (round 73) gate-selftest\n\n"
                         "the count is stated in this body, receipt " + RECEIPT + ".\n"),
         1, "CAPABILITY-STALE")
    case("VACUOUS",
         texts(lesson_block="## Correction (round 73)\n\nR72-LESSON-SUPERSEDED-CLAIMS "
                            "No capability row enters this round nine hermetic cases gate-selftest "
                            "ten 10 cases\n"),
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
