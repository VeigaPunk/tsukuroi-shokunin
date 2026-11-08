#!/usr/bin/env python3
"""ScribeKnowledge round-96 probe: observe the gate's own metadata fields for the versions the
r96 families send. Read-only: runs tools/check-limine-pins.py on fixtures built in scratch."""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
GATE = os.path.join(LANE, "tools", "check-limine-pins.py")
WORK = "/fast/scratch/hyaku/tsukuroi-r96/ScribeKnowledge/fixtures"


def sha(b):
    return hashlib.blake2b(b).hexdigest()


def build_era_fixture(name):
    """The battery's era-sensitive shape: FIRST physical line is an entry label, body carries a
    mismatch pin, then a `hash_mismatch_panic: no` key line (global in era A, invisible in era B)."""
    d = os.path.join(WORK, name)
    esp = os.path.join(d, "esp")
    os.makedirs(os.path.join(esp, "EFI", "Linux"), exist_ok=True)
    rel = "EFI/Linux/a.efi"
    data = b"kernel-a"
    with open(os.path.join(esp, rel), "wb") as f:
        f.write(data)
    good = sha(data)
    bad = good[:-1] + ("0" if good[-1] != "0" else "1")
    conf = os.path.join(d, "limine.conf")
    with open(conf, "w", newline="") as f:
        f.write("/entrylabel\n")
        f.write("  protocol: efi\n")
        f.write("  path: boot():/%s#%s\n" % (rel, bad))
        f.write("hash_mismatch_panic: no\n")
    return conf, esp


def build_healthy_fixture(name):
    """A healthy fixture: every pin OK -> verdict HEALTHY, rc 0 (the EXTRA-COMPONENT positive
    control's fixture)."""
    d = os.path.join(WORK, name)
    esp = os.path.join(d, "esp")
    os.makedirs(os.path.join(esp, "EFI", "Linux"), exist_ok=True)
    rel = "EFI/Linux/a.efi"
    data = b"kernel-a"
    with open(os.path.join(esp, rel), "wb") as f:
        f.write(data)
    good = sha(data)
    conf = os.path.join(d, "limine.conf")
    with open(conf, "w", newline="") as f:
        f.write("/entrylabel\n")
        f.write("  protocol: efi\n")
        f.write("  path: boot():/%s#%s\n" % (rel, good))
    return conf, esp


def run(conf, esp, version):
    p = subprocess.run([sys.executable, "-I", GATE, "--conf", conf, "--esp", esp,
                        "--limine-version", version],
                       capture_output=True, text=True, timeout=30)
    row = {"version": version, "rc": p.returncode, "stdout_bytes": len(p.stdout)}
    try:
        out = json.loads(p.stdout)
    except Exception:
        row["stdout_head"] = p.stdout[:120]
        row["stderr_head"] = p.stderr[:200]
        return row
    row["schema"] = out.get("schema")
    row["verdict"] = out.get("verdict")
    row["limine_version"] = out.get("limine_version")
    row["limine_version_source"] = out.get("limine_version_source")
    row["visibility_era"] = out.get("visibility_era")
    row["pin_consequences"] = [(x["line"], x["status"], x["consequence"]) for x in out.get("pins", [])]
    row["on_panic"] = out.get("on_panic")
    return row


def main():
    os.makedirs(WORK, exist_ok=True)
    era_conf, era_esp = build_era_fixture("era")
    healthy_conf, healthy_esp = build_healthy_fixture("healthy")
    out = {"gate_sha256": None, "era_fixture": [], "healthy_fixture": []}
    with open(GATE, "rb") as f:
        out["gate_sha256"] = hashlib.sha256(f.read()).hexdigest()
    # the four EXPLICIT_VERSION_META values + the two Y members
    for v in ("12.9.4", "12.9.5", "12.9.6", "999999999.9.9", "12.999999999.4", "0.999999999.0"):
        out["era_fixture"].append(run(era_conf, era_esp, v))
    # the four-component refusals + the same-list positive control
    for v in ("12.9.6.1", "12.9.6.1.0", "12.9.6.99", "12.9.6.7", "12.9.6"):
        out["healthy_fixture"].append(run(healthy_conf, healthy_esp, v))
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
