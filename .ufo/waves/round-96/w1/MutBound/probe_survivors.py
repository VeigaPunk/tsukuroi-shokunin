#!/usr/bin/env python3
"""Round-96 MutBound survivor probes: show each surviving mutant's behavior against the landed gate.

The battery is the assigned detector; this probe is diagnostic only (it does NOT rescore any
family). It builds one healthy fixture in scratch and runs the landed gate and the survivor on:
  M06: --limine-version 12.9.999999999    (9-digit Z, in-bound; landed accepts, M06 refuses)
  M08: --limine-version 000000001.0.0     (9-digit X with leading zeros, in-bound; landed accepts)
  M07: --limine-version 12.9.4 / 12.09.4  (landed vs M07 stdout must be byte-identical)
Writes survivor-probes.json under the seat dir.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SEAT = os.path.join(LANE, ".ufo", "waves", "round-96", "w1", "MutBound")
GATES = {
    "landed": os.path.join(LANE, "tools", "check-limine-pins.py"),
    "M06-z-cap-8": os.path.join(SEAT, "mutants", "M06-z-cap-8.py"),
    "M07-echo-lower": os.path.join(SEAT, "mutants", "M07-echo-lower.py"),
    "M08-refusal-9digit-below-1e8": os.path.join(SEAT, "mutants", "M08-refusal-9digit-below-1e8.py"),
}


def run(gate, conf, esp, version):
    p = subprocess.run([sys.executable, "-I", gate, "--conf", conf, "--esp", esp,
                        "--secure-boot-enforced", "0", "--limine-version", version],
                       capture_output=True, text=True, timeout=30)
    return {"rc": p.returncode, "stdout": p.stdout,
            "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "stdout_head": p.stdout[:220], "stderr_head": p.stderr[:220]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    esp = os.path.join(work, "esp")
    os.makedirs(os.path.join(esp, "EFI", "Linux"), exist_ok=True)
    data = b"survivor-probe"
    with open(os.path.join(esp, "EFI", "Linux", "a.efi"), "wb") as f:
        f.write(data)
    h = hashlib.blake2b(data).hexdigest()
    conf = os.path.join(work, "limine.conf")
    with open(conf, "w") as f:
        f.write("/e\npath: boot():/EFI/Linux/a.efi#%s\n" % h)
    out = {"fixture": {"conf": conf, "esp": esp, "blake2b": h},
           "gates": {k: hashlib.sha256(open(v, "rb").read()).hexdigest() for k, v in GATES.items()},
           "probes": []}
    probes = [
        ("M06", "M06-z-cap-8", "12.9.999999999"),
        ("M08", "M08-refusal-9digit-below-1e8", "000000001.0.0"),
        ("M07", "M07-echo-lower", "12.9.4"),
        ("M07", "M07-echo-lower", "12.09.4"),
    ]
    for label, gate_key, version in probes:
        landed = run(GATES["landed"], conf, esp, version)
        mutant = run(GATES[gate_key], conf, esp, version)
        rec = {"label": label, "version": version, "landed": landed, "mutant": mutant,
               "identical_stdout": landed["stdout_sha256"] == mutant["stdout_sha256"],
               "rc_delta": [landed["rc"], mutant["rc"]]}
        out["probes"].append(rec)
        print("%s version=%-18s landed_rc=%s mutant_rc=%s identical_stdout=%s" % (
            label, version, landed["rc"], mutant["rc"], rec["identical_stdout"]))
        print("    landed %s" % landed["stdout_head"].replace("\n", " ")[:200])
        print("    mutant %s" % mutant["stdout_head"].replace("\n", " ")[:200])
    with open(os.path.join(SEAT, "survivor-probes.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print("wrote survivor-probes.json")


if __name__ == "__main__":
    main()
