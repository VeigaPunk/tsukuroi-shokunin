#!/usr/bin/env python3
"""round-72 C3 pre-data battery: one green control plus three red mutants.

The green fixture carries the three committed artefacts the claim requires (the C1 receipt with
the counter's real summary lines, the SCORECARD erratum block, the note correction). Each mutant
breaks exactly one, and the frozen checker must read STALE>0 rc 1. Runs under $TMPDIR; no lane
file is written.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
CHECK = LANE / "tools/check-r71-routed-r72.py"
COUNTER = LANE / "tools/count-mp-rows-r71.py"

RECEIPT = """# round-71 C1 final counter run (receipt)
# command: python3 tools/count-mp-rows-r71.py --revision 2b358d2d
{summary}
"""

SCORECARD = """# fixture scorecard

## Round 71 — receipt erratum (fixture)

The C1 measured revision is `2b358d2d`; the final run is
`.ufo/waves/round-71/after/count-mp-rows-final.txt`.

## Next section
"""

NOTE = """# fixture note

MP5 — the three `/etc/modprobe.d` plus four `/usr/lib/modprobe.d` paths are recorded by path.

## Correction (round 72)

R71-NOTE-MODPROBE-COUNT: the filed sentence says four; the capture lists five `/usr/lib/modprobe.d`
paths — README, bluetooth-usb.conf, gsr-nvidia.conf, nvidia-utils.conf, systemd.conf — and this
correction supersedes the four-path figure.
"""


def summary():
    r = subprocess.run([sys.executable, str(COUNTER), "--revision", "2b358d2d"],
                       capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith(("MP_ROWS=", "MP_TARGET "))]
    return "\n".join(lines)


def write(root: Path, receipt=True, scorecard=True, note=True, tamper=False):
    root.mkdir(parents=True, exist_ok=True)
    (root / ".ufo/waves/round-71/after").mkdir(parents=True, exist_ok=True)
    (root / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    if receipt:
        body = RECEIPT.format(summary=summary())
        if tamper:
            body = body.replace("MP_VERIFIED=6", "MP_VERIFIED=5")
        (root / ".ufo/waves/round-71/after/count-mp-rows-final.txt").write_text(body)
    (root / "SCORECARD.md").write_text(SCORECARD if scorecard else "# fixture scorecard\n")
    (root / "corpus/knowledge/module-parameter-plane-r71.md").write_text(NOTE if note else "# note\n")


def main():
    base = Path(os.environ.get("TMPDIR", "/fast/scratch/hyaku")) / "routed-battery-r72"
    shutil.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True, exist_ok=True)
    cases = []
    try:
        write(base / "green")
        cases.append(("green-control", base / "green", 0))
        write(base / "tampered", tamper=True)
        cases.append(("mutant-tampered-receipt", base / "tampered", 1))
        write(base / "no-erratum", scorecard=False)
        cases.append(("mutant-missing-erratum", base / "no-erratum", 1))
        write(base / "no-correction", note=False)
        cases.append(("mutant-missing-note-correction", base / "no-correction", 1))
        write(base / "no-receipt", receipt=False)
        cases.append(("mutant-missing-receipt", base / "no-receipt", 1))
        passed = failed = 0
        for name, d, want in cases:
            r = subprocess.run([sys.executable, str(CHECK), "--fixture", str(d)],
                               capture_output=True, text=True)
            ok = r.returncode == want
            passed += ok
            failed += not ok
            print(f"BATTERY {name}: rc={r.returncode} want={want} {'PASS' if ok else 'FAIL'}")
        print(f"BATTERY cases={len(cases)} passed={passed} failed={failed}")
        return 0 if failed == 0 else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
