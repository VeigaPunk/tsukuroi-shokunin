#!/usr/bin/env python3
"""FORGERY F3 (critic seat): the r87 gate plus the cheapest half of the r90 surface: invalid
resources are renamed LP-BAD-RESOURCE and on_panic is computed, but the r87 consequence model is
kept (no efi-image-missing -> panic).  Tests whether the r90 families actually load-bear R9."""
import argparse
import importlib.util
import json
import sys

K1 = ("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-90/before/controls/"
      "gates/K1-landed-gate.py")
_spec = importlib.util.spec_from_file_location("r87_gate", K1)
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

RESOURCES = {"hdd", "odd", "boot", "guid", "uuid", "fslabel", "tftp"}
FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE")
OPTIONAL = {"wallpaper", "term_font"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf")
    ap.add_argument("--esp")
    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)
    ap.add_argument("--tpm-present", choices=("0", "1"), default=None)
    a = ap.parse_args()
    if not a.conf or not a.esp:
        return 64
    sb = a.secure_boot_enforced == "1"
    tpm = None if a.tpm_present is None else a.tpm_present

    r = R.check(a.conf, a.esp, sb)
    if "error" in r:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "on_panic": "menu"}))
        return 2

    with open(a.conf, "rb") as f:
        lines = f.read().decode("utf-8", "surrogateescape").split("\n")
    measured = None
    for raw in lines:
        kv = R.split_key(raw)
        if kv is not None and kv[0] == "measured_boot" and measured is None:
            measured = kv[2]
    requested = (measured == "yes") or sb
    if not requested:
        on_panic = "menu"
    elif tpm is None:
        on_panic = "halt-if-tpm"
    else:
        on_panic = "halt" if tpm == "1" else "menu"

    pins = r.get("pins", [])
    for p in pins:
        if p.get("status") == "LP-UNRESOLVED":
            uri = R.parse_uri(p.get("uri", ""))
            if uri is not None:
                res = uri["resource"]
                res = res[1:] if res.startswith("$") else res
                if res not in RESOURCES:
                    p["status"] = "LP-BAD-RESOURCE"
                    p["consequence"] = "skip" if p.get("key", "").lower() in OPTIONAL else "panic"

    statuses = {p.get("status") for p in pins}
    if statuses & set(FAULTS):
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0

    out = {"verdict": verdict, "rc": rc, "pins": pins, "on_panic": on_panic,
           "hash_mismatch_panic": r.get("hash_mismatch_panic")}
    print(json.dumps(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
