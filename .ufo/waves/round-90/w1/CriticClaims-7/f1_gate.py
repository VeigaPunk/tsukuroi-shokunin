#!/usr/bin/env python3
"""FORGERY F1 (critic seat): the landed r87 gate (K1 control) plus a thin post-pass that rewrites
invalid-resource statuses, efi-image-missing consequences and on_panic from regex/structure scans of
the conf.  It never reads the pinned Limine sources; the r90 clauses are transcribed from the frozen
battery docstring only."""
import argparse
import importlib.util
import json
import os
import sys

K1 = ("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-90/before/controls/"
      "gates/K1-landed-gate.py")
_spec = importlib.util.spec_from_file_location("r87_gate", K1)
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)

RESOURCES = {"hdd", "odd", "boot", "guid", "uuid", "fslabel", "tftp"}
EFI = {"efi", "uefi", "efi_chainload"}
FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE")
OPTIONAL = {"wallpaper", "term_font"}


def image_lines(lines):
    bodies, cur = [], None
    for n, raw in enumerate(lines, 1):
        s = raw.replace("\r", "").strip(" \t")
        if s.startswith("/"):
            cur = {}
            bodies.append(cur)
            continue
        kv = R.split_key(raw)
        if kv is None or cur is None:
            continue
        key, _written, value = kv
        if key in ("protocol", "path", "image_path") and key not in cur:
            cur[key] = value if key == "protocol" else n
    out = set()
    for b in bodies:
        if b.get("protocol") in EFI:
            ln = b.get("path", b.get("image_path"))
            if ln is not None:
                out.add(ln)
    return out


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
    images = image_lines(lines)
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
        status = p.get("status")
        if status == "LP-UNRESOLVED":
            uri = R.parse_uri(p.get("uri", ""))
            if uri is not None:
                res = uri["resource"]
                res = res[1:] if res.startswith("$") else res
                if res not in RESOURCES:
                    p["status"] = "LP-BAD-RESOURCE"
                    p["consequence"] = "skip" if p.get("key", "").lower() in OPTIONAL else "panic"
        elif status == "LP-MISSING" and p.get("line") in images:
            p["consequence"] = "panic"

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
