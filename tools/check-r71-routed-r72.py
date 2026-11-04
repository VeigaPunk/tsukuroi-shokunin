#!/usr/bin/env python3
# round-72 C3 routed-defect checker (frozen by the round-72 declaration, before any repair).
#
# Checks the two statement/receipt defects the round-71 closure routed to this round
# (R71-C1-UNRECEIPTED-RUN, R71-NOTE-MODPROBE-COUNT; corpus/lessons/round-71-verifier-spotcheck.md
# §6 items 2 and 3) over committed bytes:
#
#   RECEIPT  .ufo/waves/round-71/after/count-mp-rows-final.txt exists at the checked tree and its
#            summary lines equal a fresh run of the frozen round-71 counter at the record revision
#            (a receipt that is not re-derivable is not a receipt).
#   SCORECARD a `## Round 71 — receipt erratum` block names that receipt path and the record
#            revision (the C1 outcome header and the counting command must name one revision).
#   NOTE     corpus/knowledge/module-parameter-plane-r71.md carries an appended correction that
#            names R71-NOTE-MODPROBE-COUNT, the five /usr/lib/modprobe.d paths and the
#            superseded four-path figure (append-only: the filed sentence is quoted, not edited).
#
# Exit 0 iff STALE=0; 1 on any stale item. --fixture <dir> reads a tree instead of a revision.
import argparse
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
RECEIPT = ".ufo/waves/round-71/after/count-mp-rows-final.txt"
SCORECARD = "SCORECARD.md"
NOTE = "corpus/knowledge/module-parameter-plane-r71.md"
RECORD_REVISION = "2b358d2d"
COUNTER = "tools/count-mp-rows-r71.py"
SUMMARY = re.compile(r"^(MP_ROWS=.*|MP_TARGET .*)$", re.M)


def readers(revision, fixture):
    if fixture:
        root = Path(fixture)

        def rt(rel):
            p = root / rel
            return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

        return rt
    def rt(rel):
        r = subprocess.run(["git", "-C", str(LANE), "show", f"{revision}:{rel}"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.stdout if r.returncode == 0 else None
    return rt


def counter_summary():
    """Always re-derive against the lane repository's history: a fixture proves text shape only."""
    cmd = [sys.executable, str(LANE / COUNTER), "--revision", RECORD_REVISION]
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = SUMMARY.findall(r.stdout)
    return "\n".join(m) if m else None


def evaluate(rt, fixture=None):
    stale = 0
    receipt = rt(RECEIPT)
    if receipt is None:
        print(f"ROUTED_RECEIPT missing {RECEIPT}")
        stale += 1
    else:
        if RECORD_REVISION not in receipt:
            print(f"ROUTED_RECEIPT missing revision token {RECORD_REVISION}")
            stale += 1
            receipt_ok = False
        else:
            receipt_ok = True
        have = "\n".join(SUMMARY.findall(receipt))
        fresh = counter_summary()
        if not receipt_ok:
            pass
        elif fresh is None:
            print("ROUTED_RECEIPT unresolved: counter produced no summary line")
            stale += 1
        elif have != fresh:
            print("ROUTED_RECEIPT mismatch: receipt summary differs from a fresh counter run")
            stale += 1
        else:
            print(f"ROUTED_RECEIPT ok revision={RECORD_REVISION}")

    score = rt(SCORECARD) or ""
    block = ""
    # Line-anchored: the prose may quote the heading inline; only a real heading opens the block.
    m = re.search(r"^## Round 71 — receipt erratum.*?(?=\n## |\Z)", score, re.S | re.M)
    if m:
        block = m.group(0)
    if RECEIPT in block and RECORD_REVISION in block:
        print("ROUTED_SCORECARD ok")
    else:
        print("ROUTED_SCORECARD missing: no erratum block naming the receipt and the record revision")
        stale += 1

    note = rt(NOTE) or ""
    # The frozen predicate says the correction names the five /usr/lib/modprobe.d paths: check the
    # enumeration, not a prose token list (R72-C3-TOKEN-LIST, R2Reviewer high finding).
    sec = re.search(r"^## .*?(?:correction|erratum).*$", note, re.I | re.M)
    if not sec:
        print("ROUTED_NOTE missing: no appended correction/erratum section")
        stale += 1
    else:
        tail = note[sec.start():]
        need = ["R71-NOTE-MODPROBE-COUNT", "five", "four", "/usr/lib/modprobe.d",
                "README", "bluetooth-usb.conf", "gsr-nvidia.conf", "nvidia-utils.conf",
                "systemd.conf"]
        # the words are case-insensitive; ids, paths and filenames are exact
        low = tail.lower()
        missing = [n for n in need if (n.lower() if n in ("five", "four") else n) not in
                   (low if n in ("five", "four") else tail)]
        if missing:
            print(f"ROUTED_NOTE missing: {' '.join(missing)}")
            stale += 1
        else:
            print("ROUTED_NOTE ok")

    print(f"ROUTED_STALE={stale}")
    return 0 if stale == 0 else 1


# --- round-79 routed selftest (C2 item 2): hermetic, TMPDIR-bound, read-only ---
# The frozen evaluate/readers/counter_summary logic above is not modified; the
# selftest only drives it over synthetic fixture trees.
HARNESS_LINE = "HARNESS-TMPDIR-REFUSED"


def selftest_root():
    """Private fixture root: an explicit TMPDIR, never unset, never under /tmp."""
    tmp = os.environ.get("TMPDIR")
    if not tmp:
        print(f"{HARNESS_LINE} reason=tmpdir-unset")
        return None
    real = os.path.realpath(tmp)
    if real == "/tmp" or real.startswith("/tmp/"):
        print(f"{HARNESS_LINE} reason=tmpdir-under-tmp")
        return None
    if not os.path.isdir(real):
        print(f"{HARNESS_LINE} reason=tmpdir-missing")
        return None
    return real


def _write_tree(root, files):
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


_ERRATUM = """# tsukuroi-shokunin — Scorecard

## Round 71 — receipt erratum

The counting command ran against revision {rev} and its summary landed in
{rcpt}.

## Round 72 — declaration

Placeholder prose so the erratum block is bounded by a following heading.
"""

_NOTE_OK = """# module parameter plane

## Correction — modprobe path enumeration

R71-NOTE-MODPROBE-COUNT: the appended correction replaces the superseded
four-path figure with five paths under /usr/lib/modprobe.d: README,
bluetooth-usb.conf, gsr-nvidia.conf, nvidia-utils.conf, systemd.conf.
"""

_NOTE_NO_SECTION = """# module parameter plane

Plain prose with no appended correction or erratum section at all.
"""

_NOTE_MISSING_FIVE = """# module parameter plane

## Correction — modprobe path enumeration

R71-NOTE-MODPROBE-COUNT: the appended correction replaces the superseded
four-path figure with 5 paths under /usr/lib/modprobe.d: README,
bluetooth-usb.conf, gsr-nvidia.conf, nvidia-utils.conf, systemd.conf.
"""


def run_selftest():
    """Fixture-tree selftest: one SELFTEST line per case, rc 0 all-pass, rc 3 any-fail."""
    root = selftest_root()
    if root is None:
        return 2
    work = Path(tempfile.mkdtemp(prefix="check-r71-routed-r72-selftest-", dir=root))
    try:
        fresh = counter_summary()
    except OSError:
        fresh = None
    cases = []
    if fresh is None:
        print("SELFTEST harness-counter-unavailable FAIL")
        cases.append(False)
    receipt_ok = f"record revision {RECORD_REVISION}\n\n{fresh or 'MP_ROWS=unavailable'}\n"

    def case(name, files, want_rc, need):
        d = work / name
        d.mkdir(parents=True)
        _write_tree(d, files)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = evaluate(readers(None, str(d)))
        except Exception as exc:  # a crashing case is a failing case, never a hang
            rc = None
            buf.write(f"case-exception: {type(exc).__name__}: {exc}\n")
        out = buf.getvalue()
        absent = [s for s in need if s not in out]
        ok = rc == want_rc and not absent
        cases.append(ok)
        print(f"SELFTEST {name} rc={rc} {'PASS' if ok else 'FAIL'}")
        if absent:
            print(f"  expected-but-absent: {absent}")
        if not ok:
            for line in out.rstrip().splitlines():
                print(f"  | {line}")

    erratum = _ERRATUM.format(rev=RECORD_REVISION, rcpt=RECEIPT)
    case("clean-pass", {RECEIPT: receipt_ok, SCORECARD: erratum, NOTE: _NOTE_OK}, 0,
         ["ROUTED_RECEIPT ok", "ROUTED_SCORECARD ok", "ROUTED_NOTE ok", "ROUTED_STALE=0"])
    case("receipt-missing", {SCORECARD: erratum, NOTE: _NOTE_OK}, 1,
         ["ROUTED_RECEIPT missing"])
    case("receipt-missing-revision-token",
         {RECEIPT: "MP_ROWS=1 met=1 without any revision token\n", SCORECARD: erratum,
          NOTE: _NOTE_OK}, 1, ["missing revision token"])
    case("receipt-mismatch",
         {RECEIPT: f"stale snapshot line\nMP_ROWS=999 MP_X=1\nrev {RECORD_REVISION}\n",
          SCORECARD: erratum, NOTE: _NOTE_OK}, 1, ["ROUTED_RECEIPT mismatch"])
    case("malformed-scorecard",
         {RECEIPT: receipt_ok,
          SCORECARD: "prose quotes '## Round 71 — receipt erratum' inline and indented only",
          NOTE: _NOTE_OK}, 1, ["ROUTED_SCORECARD missing"])
    case("note-missing-section",
         {RECEIPT: receipt_ok, SCORECARD: erratum, NOTE: _NOTE_NO_SECTION}, 1,
         ["ROUTED_NOTE missing"])
    case("note-missing-tokens",
         {RECEIPT: receipt_ok, SCORECARD: erratum, NOTE: _NOTE_MISSING_FIVE}, 1,
         ["ROUTED_NOTE missing: five"])
    case("accepted-variant",
         {RECEIPT: f"preamble prose\n\n{fresh or ''}\ntrailing prose {RECORD_REVISION}\n",
          SCORECARD: erratum.replace("ran against revision", "ran against REVISION")
                            .replace(RECEIPT, "`" + RECEIPT + "`"),
          NOTE: _NOTE_OK.replace("Correction", "erratum")}, 0,
         ["ROUTED_RECEIPT ok", "ROUTED_SCORECARD ok", "ROUTED_NOTE ok", "ROUTED_STALE=0"])
    shutil.rmtree(work, ignore_errors=True)
    total, passed = len(cases), sum(cases)
    print(f"SELFTEST: {'PASS' if passed == total else 'FAIL'} "
          f"({total} cases, {passed} passed, {total - passed} failed)")
    return 0 if passed == total else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--revision", default="HEAD")
    group.add_argument("--fixture")
    group.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return run_selftest()
    return evaluate(readers(args.revision, args.fixture), args.fixture)


if __name__ == "__main__":
    sys.exit(main())
