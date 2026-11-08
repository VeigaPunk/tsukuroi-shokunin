#!/usr/bin/env python3
"""ScribeKnowledge round-96: limit probes the knowledge entry declares.

Every value here is either unsampled at family level (so the entry names the gap and shows what the
gate does with it) or a per-component cap member at a position no family sends. Read-only."""
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


def healthy(name):
    d = os.path.join(WORK, name)
    esp = os.path.join(d, "esp")
    os.makedirs(os.path.join(esp, "EFI", "Linux"), exist_ok=True)
    rel = "EFI/Linux/a.efi"
    data = b"kernel-a"
    with open(os.path.join(esp, rel), "wb") as f:
        f.write(data)
    conf = os.path.join(d, "limine.conf")
    with open(conf, "w", newline="") as f:
        f.write("/entrylabel\n  protocol: efi\n  path: boot():/%s#%s\n" % (rel, sha(data)))
    return conf, esp


def run(conf, esp, version):
    p = subprocess.run([sys.executable, "-I", GATE, "--conf", conf, "--esp", esp,
                        "--limine-version", version],
                       capture_output=True, text=True, timeout=30)
    row = {"version": version, "rc": p.returncode, "stdout_bytes": len(p.stdout)}
    try:
        out = json.loads(p.stdout)
    except Exception:
        row["parsed"] = False
        return row
    row["parsed"] = True
    row["verdict"] = out.get("verdict")
    row["limine_version"] = out.get("limine_version")
    row["limine_version_source"] = out.get("limine_version_source")
    row["visibility_era"] = out.get("visibility_era")
    return row


def main():
    conf, esp = healthy("limits")
    out = {}
    out["unsampled_four_component_shapes"] = [run(conf, esp, v) for v in
                                              ("12.9.6.", "12.9.6.1.2", "12.9.6.1.2.3", "12.9.6.０")]
    out["cap_member_in_every_position"] = [run(conf, esp, v) for v in
                                           ("999999999.999999999.999999999",
                                            "999999999.999999999.999999999.1")]
    out["pre_existing_r95_row"] = [run(conf, esp, "12.9.5.1")]
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
