#!/usr/bin/env python3
"""FORGERY F2 (critic seat): a gate that imports the frozen r90 battery and lets the battery's own
Case oracle compute every consequence, the verdict/rc, R8 and R10.  It models none of R6/R9/R10
itself: it only parses pins and file/hash status (R2-R5)."""
import argparse
import importlib.util
import json
import os
import random
import sys

BATT = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r90.py"
_spec = importlib.util.spec_from_file_location("batt_r90", BATT)
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)

PIN_KEYS = {"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
            "wallpaper", "term_font"}
HEX = set("0123456789abcdefABCDEF")


def parse_uri(value):
    lp = value.find("(")
    if lp < 0:
        return None
    rp = value.find("):/", lp + 1)
    if rp < 0:
        return None
    tail = value[rp + 3:]
    cut = tail.rfind("#")
    if cut < 0:
        return None
    return value[:lp], value[lp + 1:rp], tail[:cut], tail[cut + 1:]


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

    missing = isdir = False
    try:
        with open(a.conf, "rb") as f:
            text = f.read().decode("utf-8", "surrogateescape")
    except IsADirectoryError:
        text = ""
        isdir = True
    except OSError:
        text = ""
        missing = True

    c = B.Case("forgery", random.Random(0))
    c.lines = text.split("\n") if text else []
    c.sb = sb
    c.sbflag = None
    c.tpm = tpm
    c.tpm_fixed = True
    c.conf_missing = missing
    c.conf_dir = isdir

    if missing or isdir:
        rc, verdict, _pins = c.finish()
        print(json.dumps({"verdict": verdict, "rc": rc, "pins": [],
                          "on_panic": c.want_on_panic()}))
        return rc

    expect = []
    for n, raw in enumerate(c.lines, 1):
        kv = B.r1_key(raw)
        if kv is None or kv[0] not in PIN_KEYS:
            continue
        uri = parse_uri(kv[1])
        if uri is None:
            continue
        resource, root, path, h = uri
        if len(h) != 128 or set(h) - HEX:
            status = "LP-HASH-FORMAT"
        else:
            name = resource[1:] if resource.startswith("$") else resource
            if name not in B.VALID_RESOURCES:
                status = "LP-BAD-RESOURCE"
            elif name != "boot" or root != "":
                status = "LP-UNRESOLVED"
            else:
                target = os.path.join(a.esp, *path.split("/"))
                if not os.path.isfile(target):
                    status = "LP-MISSING"
                else:
                    with open(target, "rb") as f:
                        status = "OK" if B.b2(f.read()) == h.lower() else "LP-MISMATCH"
        expect.append([n, status, kv[0]])

    c.expect = expect
    rc, verdict, want = c.finish()
    entries = c.r8_entries()
    pins = [{"line": ln, "status": st, "consequence": cons, "entry": entries.get(ln)}
            for ln, st, cons in want]
    panic = c.r1_panic()
    out = {"verdict": verdict, "rc": rc, "pins": pins, "on_panic": c.want_on_panic(),
           "hash_mismatch_panic": None if panic is None else {"line": panic[0], "value": panic[1]}}
    print(json.dumps(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
