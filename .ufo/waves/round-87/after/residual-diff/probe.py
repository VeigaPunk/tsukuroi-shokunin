#!/usr/bin/env python3
"""Round-87 L1 residual probe (not a frozen instrument, not C1's counter).

The w1 critic CriticClaims showed ten one-clause forgers of R1-R7 reading 22/22 on the frozen
battery (`.ufo/waves/round-87/w1/CriticClaims/receipts/`). The battery therefore does not certify
those clauses. This probe asks a narrower question for each such clause: on one hand-made input
that exercises exactly that clause, does the candidate gate answer what the critic's independent
R1-R7 base gate (`w1/CriticClaims/forgers/g00-base.py`, written from the battery docstring, never
from the candidate) answers, and does the clause's forger answer differently? A case counts
only when base != forger (the input really exercises the clause).

Usage: probe.py --work DIR   (writes fixtures under DIR, prints one line per case, exit 0 when
every discriminating case has candidate == base, 1 otherwise).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../.."))
CAND = os.path.join(LANE, "tools/check-limine-pins.py")
FORG = os.path.join(LANE, ".ufo/waves/round-87/w1/CriticClaims/forgers")


def b2(data):
    return hashlib.blake2b(data).hexdigest()


def run(gate, conf, esp, sb=None):
    cmd = [sys.executable, gate, "--conf", conf, "--esp", esp]
    if sb is not None:
        cmd += ["--secure-boot-enforced", sb]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    try:
        out = json.loads(p.stdout)
        pins = sorted((x["line"], x["status"], x["consequence"]) for x in out["pins"])
        return (p.returncode, out["verdict"], tuple(pins))
    except Exception as e:  # noqa: BLE001 - any parse failure is an answer too
        return (p.returncode, "UNPARSEABLE:%s" % type(e).__name__, ())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--candidate", default=CAND, help="gate under test (control runs pass a forger)")
    a = ap.parse_args()
    cand_gate = os.path.abspath(a.candidate)
    os.makedirs(a.work, exist_ok=True)
    root = tempfile.mkdtemp(prefix="r87-residual-", dir=a.work)
    try:
        esp = os.path.join(root, "esp")
        os.makedirs(os.path.join(esp, "EFI"))
        good = os.urandom(4096)
        with open(os.path.join(esp, "EFI", "a.efi"), "wb") as f:
            f.write(good)
        os.makedirs(os.path.join(esp, "d):"), exist_ok=True)
        with open(os.path.join(esp, "d):", "x.efi"), "wb") as f:
            f.write(good)
        H = b2(good)
        BAD = b2(b"other")
        conf_dir = os.path.join(root, "conf")
        os.makedirs(conf_dir)
        cases = [
            ("g01-loose-key", ["/e", "path : boot():/EFI/a.efi#" + BAD], None),
            ("g02-no-paren", ["/e", "path: boot:/EFI/a.efi#" + BAD], None),
            ("g03-format-after-resolve", ["/e", "path: hdd(1:1):/EFI/a.efi#xyz"], None),
            ("g04-hashformat-optional-panic", ["/e", "wallpaper: boot():/EFI/a.efi#xyz"], None),
            ("g05-last-uri-sep", ["/e", "path: boot():/d):/x.efi#" + H], None),
            ("g06-any-empty-root", ["/e", "path: tftp():/EFI/a.efi#" + H], None),
            ("g07-panic-key-case", ["HASH_MISMATCH_PANIC: no", "/e", "path: boot():/EFI/a.efi#" + BAD], None),
            ("g08-sb-presence", ["hash_mismatch_panic: no", "/e", "path: boot():/EFI/a.efi#" + BAD], "0"),
            ("g10-raw-panic-scan", ["# hash_mismatch_panic: yes", "hash_mismatch_panic: no", "/e",
                                    "path: boot():/EFI/a.efi#" + BAD], None),
            ("g16-drop-global-dtb", ["/e", "path: boot():/EFI/a.efi#" + H,
                                     "global_dtb: boot():/EFI/a.efi#" + BAD], None),
        ]
        bad = 0
        counted = 0
        for name, lines, sb in cases:
            conf = os.path.join(conf_dir, name + ".conf")
            with open(conf, "w") as f:
                f.write("\n".join(lines) + "\n")
            base = run(os.path.join(FORG, "g00-base.py"), conf, esp, sb)
            forg = run(os.path.join(FORG, name + ".py"), conf, esp, sb)
            cand = run(cand_gate, conf, esp, sb)
            disc = base != forg
            ok = cand == base
            counted += disc
            bad += disc and not ok
            print("%-32s discriminating=%s candidate==base=%s base=%s forger=%s candidate=%s"
                  % (name, disc, ok, base, forg, cand))
        # g14: unreadable conf that is not ENOENT (a directory)
        base = run(os.path.join(FORG, "g00-base.py"), conf_dir, esp)
        forg = run(os.path.join(FORG, "g14-eacces-rc1.py"), conf_dir, esp)
        cand = run(cand_gate, conf_dir, esp)
        disc = base != forg
        counted += disc
        bad += disc and cand != base
        print("%-32s discriminating=%s candidate==base=%s base=%s forger=%s candidate=%s"
              % ("g14-eacces-rc1 (conf is a dir)", disc, cand == base, base, forg, cand))
        print("discriminating_cases %d candidate_disagrees %d" % (counted, bad))
        return 0 if bad == 0 else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
