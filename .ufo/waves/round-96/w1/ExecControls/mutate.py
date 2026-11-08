#!/usr/bin/env python3
"""ExecControls one-fault fixture mutator (round 96).

Usage: mutate.py <root> <M1|M2|M3|M4|M5|M6|S1|S2|S2b|S3|S4>

Each mutation reverts or removes exactly ONE of the six round-96 C2 fixes (M1-M6) or
constructs one adversarial "green without the work" probe (S1-S4).  Every text
substitution asserts exactly one match so a silent no-op can never be read as a pass,
mirroring tools/make-r96-bends.py's one-clause discipline.  Nothing outside <root> is
written.  Prints the file's sha256 before/after for each touched file.
"""
import hashlib
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
R95_TSV = os.path.join(LANE, ".ufo/waves/round-95/claim-falsification.tsv")
RECEIPT = ".ufo/waves/round-96/before/r95-registry-gate.sha256"
MANIFEST = ".ufo/waves/round-96/before/instruments.sha256"
TIP = ".ufo/waves/round-96/before/c2-tip-b8f878c8.json"
LEDGER = ".ufo/waves/round-96/claim-falsification.tsv"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def textual():
    return {"encoding": "utf-8", "errors": "surrogateescape", "newline": ""}


def edit(root, rel, old, new, label):
    p = os.path.join(root, rel)
    before = sha256(p)
    with open(p, "r", **textual()) as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, (label, rel, "expected exactly 1 match, found %d" % n)
    with open(p, "w", **textual()) as f:
        f.write(text.replace(old, new, 1))
    print("EDIT   %-6s %-52s %s -> %s" % (label, rel, before[:16], sha256(p)[:16]))


def write(root, rel, text, label):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", **textual()) as f:
        f.write(text)
    print("WRITE  %-6s %-52s %s" % (label, rel, sha256(p)[:16]))


def copy_ledger(root, label):
    p = os.path.join(root, LEDGER)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    shutil.copyfile(R95_TSV, p)
    print("COPY   %-6s %-52s %s (from .ufo/waves/round-95/claim-falsification.tsv)"
          % (label, LEDGER, sha256(p)[:16]))


def main():
    root, mid = sys.argv[1], sys.argv[2]
    root = os.path.abspath(root)
    assert os.path.isdir(root), root
    if mid == "M1":
        # revert the QUALITY 140 criterion number -> criterion 140 no longer exists
        edit(root, "corpus/QUALITY.md", "140. **", "999. **", mid)
    elif mid == "M2":
        # corrupt one hex digit of the receipt's sha256 for check-registry-coverage.py
        p = os.path.join(root, RECEIPT)
        with open(p, "r", **textual()) as f:
            line = f.read()
        h = line.split()[0]
        assert len(h) == 64 and all(c in "0123456789abcdef" for c in h), h
        bad = ("0" if h[0] != "0" else "1") + h[1:]
        edit(root, RECEIPT, h, bad, mid)
    elif mid == "M3":
        # restore the r95 docstring property line (routed defect 4)
        edit(root, "tools/limine-pin-battery-r95.py",
             "values and never a boundary member,",
             "values and never the largest in-bound member,", mid)
    elif mid == "M4":
        # restore the over-scope README sentence (routed defect 5)
        edit(root, "corpus/README.md",
             "\u2014 the r94 family roster has no\n"
             "in-bound 9-digit case (its `--usage-check` does send `999999999.0.0`, so the sentence is scoped to\n"
             "the roster, not the instrument; r96 routed-5)",
             "\u2014 the before instrument has no\nin-bound 9-digit case", mid)
    elif mid == "M5":
        # set the tip receipt status to FAIL (routed defect 6)
        edit(root, TIP, '"status":"PASS"', '"status":"FAIL"', mid)
    elif mid == "M6":
        # substitute the r95 ledger at the r96 ledger path + a report claiming 2/1
        copy_ledger(root, mid)
        write(root, "report.md",
              "Ledger: 2 falsifies-wording rows and 1 falsifies-number row.\n", mid)
    elif mid == "S1":
        # Step-3 probe A: the receipt hash IS the current gate's, but SCORECARD has no Round 96
        p = os.path.join(root, "SCORECARD.md")
        before = sha256(p)
        with open(p, "r", **textual()) as f:
            text = f.read()
        marks = text.count("## Round 96")
        assert marks == 1, ("S1", "expected exactly one '## Round 96', found %d" % marks)
        cut = text.index("## Round 96")
        with open(p, "w", **textual()) as f:
            f.write(text[:cut])
        print("CUT    %-6s %-52s %s -> %s" % (mid, "SCORECARD.md", before[:16], sha256(p)[:16]))
    elif mid == "S2":
        # Step-3 probe B: counts matching no ledger (wrong on both classes)
        copy_ledger(root, mid)
        write(root, "report.md",
              "The ledger holds 9 falsifies-wording rows and 0 falsifies-number rows.\n", mid)
    elif mid == "S2b":
        # Step-3 probe B': a report that names no count at all
        copy_ledger(root, mid)
        write(root, "report.md", "The ledger is summarised elsewhere.\n", mid)
    elif mid == "S3":
        # Extra probe: the r95 ledger at the r96 path + a report matching ITS counts
        copy_ledger(root, mid)
        write(root, "report.md",
              "Ledger: 6 falsifies-wording rows and 1 falsifies-number row.\n", mid)
    elif mid == "S4":
        # Extra probe: the receipt is right but the freeze manifest does not pin it
        p = os.path.join(root, MANIFEST)
        before = sha256(p)
        with open(p, "r", **textual()) as f:
            lines = f.readlines()
        kept = [ln for ln in lines if not ln.rstrip().endswith("tools/check-registry-coverage.py")]
        assert len(kept) == len(lines) - 1, ("S4", "manifest pin line not unique")
        with open(p, "w", **textual()) as f:
            f.writelines(kept)
        print("CUT    %-6s %-52s %s -> %s" % (mid, MANIFEST, before[:16], sha256(p)[:16]))
    else:
        raise SystemExit("unknown mutation %r" % mid)
    print(json.dumps({"root": root, "mutation": mid,
                      "status": "applied",
                      "root_files": sorted(os.listdir(root))}, sort_keys=True))


if __name__ == "__main__":
    main()
