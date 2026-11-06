#!/usr/bin/env python3
"""Differential probes for the four battery survivors (round-87 w1 MutGate)."""
import hashlib
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(S, "mutants")
P = os.path.join(S, "pristine.py")


def b2(data):
    return hashlib.blake2b(data).hexdigest()


def run(gate, conf, esp, sb=None):
    argv = [sys.executable, gate, "--conf", conf, "--esp", esp]
    if sb is not None:
        argv += ["--secure-boot-enforced", sb]
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def fixture(name):
    d = os.path.join(S, "probe", name)
    esp = os.path.join(d, "esp")
    os.makedirs(os.path.join(esp, "EFI", "Linux"), exist_ok=True)
    os.makedirs(os.path.join(esp, "EFI", "BOOT"), exist_ok=True)
    return d, esp


def write(d, rel, data=b"x"):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)
    return p


def show(tag, gate, conf, esp, sb=None):
    rc, out = run(gate, conf, esp, sb)
    print("%-10s rc=%d %s" % (tag, rc, out))


# --- m01: comment lines in every plausible shape next to one live pin
d, esp = fixture("m01")
write(d, "esp/EFI/Linux/a.efi", b"kernel-a")
h = b2(b"kernel-a")
lines = ["#path: boot():/EFI/Linux/a.efi#" + "0" * 128,
         "  #path: boot():/EFI/Linux/a.efi#" + "0" * 128,
         "# path: boot():/EFI/Linux/zz.efi#" + "0" * 128,
         "#key: value",
         "/Linux",
         "path: boot():/EFI/Linux/a.efi#" + h]
conf = os.path.join(d, "c.conf")
open(conf, "w").write("\n".join(lines) + "\n")
print("== m01 comment-guard equivalence (expect identical JSON)")
show("pristine", P, conf, esp)
show("m01", os.path.join(M, "m01-comment-not-skipped.py"), conf, esp)

# --- m05: path containing '(' and ')' (R2: resource ends at the FIRST '(')
d, esp = fixture("m05")
write(d, "esp/EFI/Linux/a(1).efi", b"kernel-paren")
hp = b2(b"kernel-paren")
conf = os.path.join(d, "c.conf")
open(conf, "w").write("/Linux\npath: boot():/EFI/Linux/a(1).efi#" + hp + "\n")
print("== m05 paren-in-path (pristine must report OK; mutant hides the pin)")
show("pristine", P, conf, esp)
show("m05", os.path.join(M, "m05-last-open-paren.py"), conf, esp)

# --- m24: entry labels across two entries
d, esp = fixture("m24")
write(d, "esp/EFI/Linux/a.efi", b"kernel-a")
write(d, "esp/EFI/BOOT/b.efi", b"fallback-b")
hb = b2(b"fallback-b")
conf = os.path.join(d, "c.conf")
open(conf, "w").write("/Linux\n    protocol: efi\n    path: boot():/EFI/Linux/a.efi#" + h
                      + "\n/EFI fallback\n    protocol: efi\n    path: boot():/EFI/BOOT/b.efi#" + hb + "\n")
print("== m24 entry labels (battery compares line/status/consequence only)")
show("pristine", P, conf, esp)
show("m24", os.path.join(M, "m24-entry-not-tracked.py"), conf, esp)

# --- m25: hash_mismatch_panic reported line
d, esp = fixture("m25")
write(d, "esp/EFI/Linux/a.efi", b"kernel-a")
bad = h[:-1] + ("0" if h[-1] != "0" else "1")
conf = os.path.join(d, "c.conf")
open(conf, "w").write("/Linux\n  hash_mismatch_panic: no\n  path: boot():/EFI/Linux/a.efi#" + bad + "\n")
print("== m25 panic-setting line metadata (battery never reads it)")
show("pristine", P, conf, esp)
show("m25", os.path.join(M, "m25-panic-line-metadata-zero.py"), conf, esp)
