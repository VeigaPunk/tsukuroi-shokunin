#!/usr/bin/env python3
"""ExecControls run matrix (round 96): six one-fault C2 fixtures + clean + adversarial probes.

For each prepared scratch root this driver runs tools/check-r96-calibration.py twice:
  * current  = the lane working-tree bytes (sha256 ad894667... at measurement time)
  * frozen   = the bytes pinned by .ufo/waves/round-96/before/instruments.sha256,
               re-extracted with `git show HEAD:tools/check-r96-calibration.py`
Each run's JSON is written under <seat>/receipts/<root>.<bin>.json and its stdout is
captured verbatim under <seat>/receipts/<root>.<bin>.stdout.txt.  A summary line per run
is printed and the whole matrix is written to <seat>/receipts/matrix.json.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-96/w1/ExecControls")
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r96/ExecControls"
RECEIPTS = os.path.join(SEAT, "receipts")
CURRENT = os.path.join(LANE, "tools/check-r96-calibration.py")
FROZEN = os.path.join(SCRATCH, "frozen-check-r96-calibration.py")

# root -> report argument (relative to the root, or None)
ROOTS = [
    ("base", None),
    ("M1", None),
    ("M2", None),
    ("M3", None),
    ("M4", None),
    ("M5", None),
    ("M6", "report.md"),
    ("S1", None),
    ("S2", "report.md"),
    ("S2b", "report.md"),
    ("S3", "report.md"),
    ("S4", None),
]

INPUT_FILES = [
    "corpus/QUALITY.md", "corpus/README.md", "corpus/lessons/round-96.md",
    "SCORECARD.md", "tools/check-registry-coverage.py",
    "tools/limine-pin-battery-r95.py", "tools/make-r95-bends.py",
    ".ufo/waves/round-96/before/r95-registry-gate.sha256",
    ".ufo/waves/round-96/before/instruments.sha256",
    ".ufo/waves/round-96/before/c2-tip-b8f878c8.json",
    ".ufo/waves/round-96/claim-falsification.tsv",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(RECEIPTS, exist_ok=True)
    bins = []
    for label, path in (("current", CURRENT), ("frozen", FROZEN)):
        bins.append({"label": label, "path": path, "sha256": sha256(path)})
    matrix = {"schema": "tsukuroi-r96-exec-controls-matrix-v1", "binaries": bins,
              "lane": LANE, "scratch": SCRATCH, "runs": []}
    for root_name, report in ROOTS:
        root = os.path.join(SCRATCH, root_name)
        inputs = {}
        for rel in INPUT_FILES:
            p = os.path.join(root, rel)
            inputs[rel] = sha256(p) if os.path.isfile(p) else None
        for b in bins:
            tag = "%s.%s" % (root_name, b["label"])
            cmd = [sys.executable, FROZEN if b["label"] == "frozen" else CURRENT,
                   "--root", root, "--json", os.path.join(RECEIPTS, tag + ".json")]
            if report is not None:
                cmd += ["--report", os.path.join(root, report)]
            proc = subprocess.run(cmd, cwd=LANE, capture_output=True, text=True)
            with open(os.path.join(RECEIPTS, tag + ".stdout.txt"), "w") as f:
                f.write(proc.stdout)
                f.write("\n[stderr]\n" + proc.stderr)
            try:
                out = json.loads(proc.stdout)
            except Exception:
                out = {"unparseable_stdout": proc.stdout}
            ids = sorted({f["id"] for f in out.get("findings", [])}) if "findings" in out else None
            matrix["runs"].append({
                "root": root_name, "binary": b["label"], "report": report,
                "argv": cmd, "exit": proc.returncode,
                "status": out.get("status"), "ids": ids,
                "findings": out.get("findings"), "unreadable": out.get("unreadable"),
                "root_inputs": inputs,
            })
            print("%-5s %-8s exit=%d status=%-4s ids=%s n=%s" % (
                root_name, b["label"], proc.returncode, out.get("status"),
                ",".join(ids) if ids else "[]",
                len(out.get("findings", [])) if "findings" in out else "?"))
            if out.get("unreadable"):
                print("        unreadable=%r" % (out["unreadable"],))
    with open(os.path.join(RECEIPTS, "matrix.json"), "w") as f:
        json.dump(matrix, f, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
