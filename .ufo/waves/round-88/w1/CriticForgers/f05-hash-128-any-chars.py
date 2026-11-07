#!/usr/bin/env python3
"""Faithful docstring-only reimplementation of the Limine v12.9.4 pin rules R1-R8.

Seat CriticForgers, round 88. Written from the module docstring of
tools/limine-pin-battery-r88.py alone (no gate or battery source read; the
r87 gate tools/check-limine-pins.py was not read). It emits the required
fields plus the R8 optional fields (entry, hash_mismatch_panic) computed by
R8's written clauses.

Usage: base.py --conf FILE --esp DIR [--secure-boot-enforced 0|1]
Exit: gate rc; stdout one JSON object.
"""

import argparse
import hashlib
import json
import os
import sys

BLANKS = " \t"
PIN_KEYS = frozenset((
    "path", "kernel_path", "image_path", "module_path", "dtb_path",
    "global_dtb", "wallpaper", "term_font",
))
OPTIONAL_KEYS = frozenset(("wallpaper", "term_font"))
HEXDIGITS = frozenset("0123456789abcdefABCDEF")
LETTERS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")


def split_key(line):
    """R1: leading letters/underscores, then ':' directly. Return ':' index or None."""
    i = 0
    n = len(line)
    while i < n and line[i] in LETTERS:
        i += 1
    if i == 0 or i >= n or line[i] != ":":
        return None
    return i


def parse_uri(value):
    """R2: [$]resource(root):/path#hash -> (resource, root, path, hash) or None."""
    lp = value.find("(")
    if lp < 0:
        return None
    sep = value.find("):/", lp + 1)
    if sep < 0:
        return None
    tail = value[sep + 3:]
    cut = tail.rfind("#")
    if cut < 0:
        return None
    return value[:lp], value[lp + 1:sep], tail[:cut], tail[cut + 1:]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--esp", required=True)
    ap.add_argument("--secure-boot-enforced", default="0")
    args = ap.parse_args(argv)
    secure = args.secure_boot_enforced.strip() == "1"

    try:
        with open(args.conf, "rb") as fh:
            raw = fh.read()
    except OSError:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [],
                          "hash_mismatch_panic": None}))
        return 2

    text = raw.decode("utf-8", "surrogateescape")
    pins = []
    entry = None
    panic = None

    for lineno, rawline in enumerate(text.split("\n"), 1):
        body = rawline.replace("\r", "").lstrip(BLANKS)
        line = body.rstrip(BLANKS)
        if not line:
            continue
        if line[0] == "/":
            label = line.lstrip("/")
            if label.startswith("+"):
                label = label[1:]
            label = label.strip()
            entry = label
            continue
        i = split_key(line)
        if i is None:
            continue
        key = line[:i].lower()
        value = line[i + 1:].lstrip(BLANKS)
        if key == "hash_mismatch_panic" and panic is None:
            panic = (lineno, value)
        if key not in PIN_KEYS:
            continue
        uri = parse_uri(value)
        if uri is None:
            continue
        resource, root, path, h = uri

        # R3 before R4 (checked before resolution).
        if len(h) != 128:
            status = "LP-HASH-FORMAT"
        else:
            if resource.startswith("$"):
                resource = resource[1:]
            if resource != "boot" or root != "":
                status = "LP-UNRESOLVED"
            else:
                resolved = os.path.join(args.esp, path.lstrip("/"))
                if not os.path.isfile(resolved):
                    status = "LP-MISSING"
                else:
                    try:
                        with open(resolved, "rb") as fh:
                            data = fh.read()
                        got = hashlib.blake2b(data, digest_size=64).hexdigest()
                        status = "OK" if got == h.lower() else "LP-MISMATCH"
                    except OSError:
                        status = "LP-MISSING"

        if status == "OK":
            consequence = "none"
        elif status in ("LP-MISSING", "LP-UNRESOLVED"):
            consequence = "not-modelled"
        elif key in OPTIONAL_KEYS:
            consequence = "skip"
        elif status == "LP-HASH-FORMAT":
            consequence = "panic"
        elif secure:
            consequence = "panic"
        elif panic is not None and panic[1].lower() == "no":
            consequence = "prompt"
        else:
            consequence = "panic"
        pins.append({"line": lineno, "status": status,
                     "consequence": consequence, "entry": entry})

    pins.sort(key=lambda p: (p["line"], p["status"], p["consequence"]))
    statuses = {p["status"] for p in pins}
    if statuses & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT"}:
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0

    out = {"verdict": verdict, "rc": rc, "pins": pins}
    if panic is None:
        out["hash_mismatch_panic"] = None
    else:
        out["hash_mismatch_panic"] = {"line": panic[0], "value": panic[1]}
    print(json.dumps(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
