#!/usr/bin/env python3
"""r94 w1 MutProbe: ad-hoc detectors for the three mutants the battery + gate selftest do NOT see.

Each probe is a single behavioural observation over one fixture; it prints one JSON object.
Usage: adhoc.py GATE OUTDIR   -> OUTDIR/probes.json
"""
import hashlib
import json
import os
import subprocess
import sys
import time

GATE = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])
os.makedirs(OUT, exist_ok=True)

esp = os.path.join(OUT, "esp")
os.makedirs(os.path.join(esp, "EFI", "Linux"), exist_ok=True)
data = b"kernel-a"
with open(os.path.join(esp, "EFI", "Linux", "a.efi"), "wb") as f:
    f.write(data)
ha = hashlib.blake2b(data).hexdigest()
bad = ha[:-1] + ("0" if ha[-1] != "0" else "1")

# era fixture: the FIRST physical line is an entry whose body carries the mismatch pin, and the
# global `hash_mismatch_panic: no` follows the body (the r92 V2 shape).
era_conf = os.path.join(OUT, "era.conf")
with open(era_conf, "w") as f:
    f.write("/mismatch\n  protocol: efi\n  path: boot():/EFI/Linux/a.efi#%s\n"
            "hash_mismatch_panic: no\n" % bad)

# healthy fixture: one OK pin, for the probe-failure (hang) probe.
ok_conf = os.path.join(OUT, "ok.conf")
with open(ok_conf, "w") as f:
    f.write("/e\npath: boot():/EFI/Linux/a.efi#%s\n" % ha)

# a fake `limine` that hangs 8 s then answers 12.9.6: longer than the gate's 5 s probe timeout,
# shorter than the battery's 20 s case TIMEOUT (so the battery can never surface it).
fakebin = os.path.join(OUT, "fakebin")
os.makedirs(fakebin, exist_ok=True)
fake = os.path.join(fakebin, "limine")
with open(fake, "w") as f:
    f.write("#!/bin/sh\nsleep 8\necho \"Limine 12.9.6\"\n")
os.chmod(fake, 0o755)


def run(argv, env=None, timeout=90):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, "-I", GATE] + argv, capture_output=True, text=True,
                           timeout=timeout, env=env)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = "harness-timeout", "", ""
    return {"rc": rc, "stdout": out, "stderr": err.strip()[-200:],
            "elapsed": round(time.time() - t0, 1)}


def json_or_none(text):
    try:
        return json.loads(text)
    except Exception:
        return None


def obs(argv, env=None, timeout=90):
    r = run(argv, env, timeout)
    o = json_or_none(r["stdout"])
    return {"rc": r["rc"], "elapsed": r["elapsed"],
            "stdout_bytes": len(r["stdout"].strip()),
            "verdict": None if o is None else o.get("verdict"),
            "limine_version": None if o is None else o.get("limine_version"),
            "limine_version_source": None if o is None else o.get("limine_version_source"),
            "visibility_era": None if o is None else o.get("visibility_era"),
            "first_pin_consequence": None if o is None or not o.get("pins")
            else o["pins"][0].get("consequence")}


base = ["--conf", era_conf, "--esp", esp]
env_hang = dict(os.environ, PATH=fakebin + ":/usr/bin:/bin")
probes = {
    # C2's own shape: --live with NO --limine-version must probe (12.9.4 here) and record `probe`.
    "live-default": obs(["--live"] + base),
    # M02: --live with an explicit X.Y.Z must use the FLAG, never the probe.
    "live-flag": obs(["--live"] + base + ["--limine-version", "12.9.6"]),
    # M07: zero-padded version is normalised for the era (12.09.6 IS 12.9.6 -> era B).
    "zero-padded-era": obs(base + ["--limine-version", "12.09.6"]),
    # M04: a probing executable that answers after 8 s (> 5 s) is a probe failure -> rc 64.
    "probe-hang": obs(["--conf", ok_conf, "--esp", esp, "--limine-version", "auto"], env=env_hang,
                      timeout=75),
}
with open(os.path.join(OUT, "probes.json"), "w") as f:
    json.dump({"gate": GATE, "probes": probes}, f, indent=1)
print(json.dumps(probes, indent=1))
