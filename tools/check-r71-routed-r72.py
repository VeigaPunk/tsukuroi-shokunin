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
import json
import re
import subprocess
import sys
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revision", default="HEAD")
    ap.add_argument("--fixture")
    args = ap.parse_args()
    return evaluate(readers(args.revision, args.fixture), args.fixture)


if __name__ == "__main__":
    sys.exit(main())
