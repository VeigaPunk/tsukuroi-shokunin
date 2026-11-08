#!/usr/bin/env python3
"""Build the four PATH cases for the V3 probe edge test (seat ExecAutoReplicate, round 93 w1).

Reproduces edge/{conf,esp,bin-a,bin-b,bin-c,bin-d-empty} used for the receipt:
  case a: fake `limine` prints `Limine 12.9.6`        -> probe must answer 12.9.6, era B
  case b: fake `limine` exits 1                       -> probe must fail, gate rc 64, empty stdout
  case c: fake `limine` prints bare `12.9.6`          -> no `limine` word: probe must fail (no invention)
  case d: empty dir first on PATH                     -> real /usr/bin/limine answers 12.9.4

Run the gate with PATH=<case bin>:/usr/bin:/bin and `--limine-version auto`.
The gate copy is byte-identical to tools/check-limine-pins.py
(sha256 6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa).
"""
import os
import shutil
import sys

E = sys.argv[1] if len(sys.argv) > 1 else "edge"
shutil.rmtree(E, ignore_errors=True)
for d in ("esp/EFI/BOOT", "bin-a", "bin-b", "bin-c", "bin-d-empty"):
    os.makedirs(os.path.join(E, d), exist_ok=True)

with open(os.path.join(E, "esp/EFI/BOOT/BOOTX64.EFI"), "wb") as f:
    f.write(b"edge-payload\n")
bad = "0" * 128
with open(os.path.join(E, "conf"), "w") as f:
    f.write("/entry\n")
    f.write("  protocol: efi\n")
    f.write("  path: boot():/EFI/BOOT/BOOTX64.EFI#%s\n" % bad)
    f.write("  hash_mismatch_panic: no\n")


def fake(d, body):
    p = os.path.join(E, d, "limine")
    with open(p, "w") as f:
        f.write("#!/bin/sh\n%s\n" % body)
    os.chmod(p, 0o755)


fake("bin-a", 'echo "Limine 12.9.6"')
fake("bin-b", "exit 1")
fake("bin-c", 'echo "12.9.6"')
print("built", os.path.abspath(E))
