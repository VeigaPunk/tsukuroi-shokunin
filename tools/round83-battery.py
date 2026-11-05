#!/usr/bin/env python3
"""Round-83 counting battery — the one command that scores claims C1 (depth) and C2 (calibration).

    python3 tools/round83-battery.py --instrument r82|r83 --revision REV

`--instrument r82` runs the do-nothing control (the round-82 counters, unchanged);
`--instrument r83` runs this round's counters. Both read the same legs, so the
before→after of each claim is one command with one switch.

C1 depth — `tools/check-anchor-coordinates*.py` (quote located, cited range is the
located raw span, declared snapshot digest enforced). Target: 3 of 3 legs.
  C1.a  doctored snapshot (digest mismatch)  -> expect rc 2 cannot-evaluate
  C1.b  digest-consistent snapshot           -> expect rc 0, count 8/8
  C1.c  the real tree at REV                 -> expect rc 0, count 8/8

C2 calibration — `tools/check-ordinals*.py` (one ordinal per round and axis; positional
retirement; quoted prose is not an assertion; absent input is cannot-evaluate, never a
traceback). Target: 4 of 4 legs.
  C2.a  late contradiction fixture           -> expect rc 1, one finding
  C2.b  quoted-prose fixture                 -> expect rc 0, no finding
  C2.c  the real SCORECARD.md at REV         -> expect rc 0, no finding
  C2.d  a git repo at a revision with no SCORECARD.md -> expect rc 2 with a JSON
        cannot-evaluate line (the round-82 traceback leak fails this leg)

Exit: 0 when both targets are met, 1 otherwise. Scratch repos live under $TMPDIR (honoured by
`tempfile`) and are removed before exit.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

INSTRUMENTS = {
    "r82": {"anchor": "tools/check-anchor-coordinates.py", "ordinals": "tools/check-scorecard-ordinals.py"},
    "r83": {"anchor": "tools/check-anchor-coordinates-r83.py", "ordinals": "tools/check-ordinals-r83.py"},
}
FIXTURES = ".ufo/waves/round-83/before"
ENV = {"PATH": "/usr/bin:/bin:/usr/local/bin", "LC_ALL": "C.UTF-8",
       "PYTHONDONTWRITEBYTECODE": "1"}


def run(cmd, cwd, env=None):
    proc = subprocess.run([sys.executable, *cmd], cwd=str(cwd), stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300,
                          env={**ENV, "TMPDIR": env} if env else ENV)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")


def parse(out):
    try:
        return json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def leg(name, expect, rc, body, ok):
    return {"leg": name, "expect": expect, "rc": rc,
            "observed": {k: body.get(k) for k in ("count", "finding", "target", "problems")} if body else None,
            "verdict": "pass" if ok else "miss"}


def c1_legs(instr, rev, root):
    tool = root / INSTRUMENTS[instr]["anchor"]
    legs = []
    rc, out, _ = run([str(tool), "--fixture", f"{FIXTURES}/anchor-fixture-doctored"], root)
    body = parse(out)
    legs.append(leg("C1.a", "rc2 cannot-evaluate", rc, body,
                    rc == 2 and body is not None and body.get("finding") == "cannot-evaluate"))
    rc, out, _ = run([str(tool), "--fixture", f"{FIXTURES}/anchor-fixture-digestfixed"], root)
    body = parse(out)
    legs.append(leg("C1.b", "rc0 count8/8", rc, body,
                    rc == 0 and body is not None and body.get("count") == 8))
    rc, out, _ = run([str(tool), "--revision", rev], root)
    body = parse(out)
    legs.append(leg("C1.c", "rc0 count8/8 at REV", rc, body,
                    rc == 0 and body is not None and body.get("count") == 8))
    return legs


def c2_legs(instr, rev, root):
    tool = root / INSTRUMENTS[instr]["ordinals"]
    legs = []
    rc, out, _ = run([str(tool), "--fixture", f"{FIXTURES}/ordinals-fixture-late-contradiction.md"], root)
    body = parse(out)
    legs.append(leg("C2.a", "rc1 one finding", rc, body,
                    rc == 1 and body is not None and body.get("count") == 1))
    rc, out, _ = run([str(tool), "--fixture", f"{FIXTURES}/ordinals-fixture-quoted-prose.md"], root)
    body = parse(out)
    legs.append(leg("C2.b", "rc0 no finding", rc, body,
                    rc == 0 and body is not None and body.get("count") == 0))
    rc, out, _ = run([str(tool), "--revision", rev], root)
    body = parse(out)
    legs.append(leg("C2.c", "rc0 no finding at REV", rc, body,
                    rc == 0 and body is not None and body.get("count") == 0))

    scratch = Path(tempfile.mkdtemp(prefix="r83-battery-"))
    try:
        repo = scratch / "norepo"
        repo.mkdir()
        subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True, stdin=subprocess.DEVNULL)
        if subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, check=True).stdout.decode().strip() != str(repo.resolve()):
            raise SystemExit("battery: fixture repo toplevel mismatch")
        (repo / "README.md").write_text("no scorecard here\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True, stdin=subprocess.DEVNULL)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=battery", "-c", "user.email=battery@invalid",
                        "commit", "-q", "-m", "fixture without SCORECARD"], check=True, stdin=subprocess.DEVNULL)
        branch = subprocess.run(["git", "-C", str(repo), "symbolic-ref", "--short", "HEAD"],
                                stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, check=True
                                ).stdout.decode().strip()
        head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], stdout=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, check=True).stdout.decode().strip()
        rc, out, err = run([str(tool), "--repo", str(repo), "--branch", branch, "--revision", head], root)
        body = parse(out)
        legs.append(leg("C2.d", "rc2 JSON cannot-evaluate", rc, body,
                        rc == 2 and body is not None and body.get("finding") == "cannot-evaluate"))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return legs


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--instrument", choices=sorted(INSTRUMENTS), required=True)
    p.add_argument("--revision", required=True)
    a = p.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    c1 = c1_legs(a.instrument, a.revision, root)
    c2 = c2_legs(a.instrument, a.revision, root)
    c1_pass = sum(1 for leg_ in c1 if leg_["verdict"] == "pass")
    c2_pass = sum(1 for leg_ in c2 if leg_["verdict"] == "pass")
    report = {"instrument": a.instrument, "revision": a.revision,
              "C1_depth": {"passed": c1_pass, "of": len(c1), "target": "3/3", "legs": c1,
                           "finding": "met" if c1_pass == 3 else "unmet"},
              "C2_calibration": {"passed": c2_pass, "of": len(c2), "target": "4/4", "legs": c2,
                                 "finding": "met" if c2_pass == 4 else "unmet"}}
    print(json.dumps(report, indent=1))
    return 0 if c1_pass == 3 and c2_pass == 4 else 1


if __name__ == "__main__":
    raise SystemExit(main())
