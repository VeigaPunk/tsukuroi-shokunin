#!/usr/bin/env python3
"""ExecControls second measurement pass (round 96, tree state at >= 07:54).

The lane moved while pass 1 ran: at 07:54:00 tools/check-r96-calibration.py was restored to the
freeze-manifest bytes (7ff63524...) and tools/make-r95-bends.py was rewrapped so "boundary member"
is contiguous.  This driver rebuilds the fixture roots from the tree as it now stands and runs the
tree's own checker on each, writing receipts/r2-<root>.json + .stdout.txt.

Roots: base2 = current corpus/ tools/ SCORECARD.md .ufo/waves/round-96/{before,claims.json}
       R1..R6 = base2 with one fix reverted (same six mutations as pass 1)
       U1..U5 = adversarial "green without the work" probes (see mutate.py S1/S2/S2b/S3/S4)
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
CHECKER = os.path.join(LANE, "tools/check-r96-calibration.py")

ROOTS = [
    ("base2", None),
    ("R1", None), ("R2", None), ("R3", None), ("R4", None), ("R5", None),
    ("R6", "report.md"),
    ("U1", None),
    ("U2", "report.md"), ("U3", "report.md"), ("U4", "report.md"), ("U5", None),
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
    matrix = {"schema": "tsukuroi-r96-exec-controls-matrix-v2", "lane": LANE,
              "scratch": SCRATCH, "checker": CHECKER, "checker_sha256": sha256(CHECKER),
              "runs": []}
    for root_name, report in ROOTS:
        root = os.path.join(SCRATCH, root_name)
        inputs = {}
        for rel in INPUT_FILES:
            p = os.path.join(root, rel)
            inputs[rel] = sha256(p) if os.path.isfile(p) else None
        tag = "r2-%s" % root_name
        cmd = [sys.executable, CHECKER, "--root", root,
               "--json", os.path.join(RECEIPTS, tag + ".json")]
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
        matrix["runs"].append({"root": root_name, "report": report, "argv": cmd,
                               "exit": proc.returncode, "status": out.get("status"),
                               "ids": ids, "findings": out.get("findings"),
                               "unreadable": out.get("unreadable"),
                               "root_inputs": inputs})
        print("%-5s exit=%d status=%-4s ids=%s n=%s" % (
            root_name, proc.returncode, out.get("status"),
            ",".join(ids) if ids else "[]",
            len(out.get("findings", [])) if "findings" in out else "?"))
        if out.get("unreadable"):
            print("        unreadable=%r" % (out["unreadable"],))
    with open(os.path.join(RECEIPTS, "matrix-r2.json"), "w") as f:
        json.dump(matrix, f, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
