#!/usr/bin/env python3
"""CriticForgers base.py: faithful reimplementation of R1-R8 from the r89 battery docstring.

Usage: base.py --conf FILE --esp DIR [--secure-boot-enforced 0|1]
Prints one JSON object on stdout; exit code equals "rc".
"""
import hashlib
import json
import os
import string
import sys

PATH_KEYS = {
    "path", "kernel_path", "image_path", "module_path", "dtb_path",
    "global_dtb", "wallpaper", "term_font",
}
KEYCHARS = set(string.ascii_letters + "_")
HEXCHARS = set("0123456789abcdefABCDEF")


def parse_args(argv):
    conf = esp = None
    sbe = "0"
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--conf" and i + 1 < len(argv):
            conf = argv[i + 1]
            i += 2
        elif a == "--esp" and i + 1 < len(argv):
            esp = argv[i + 1]
            i += 2
        elif a == "--secure-boot-enforced" and i + 1 < len(argv):
            sbe = argv[i + 1]
            i += 2
        else:
            i += 1
    return conf, esp, sbe


def key_line(line):
    """R1: line -> (key, value) or None."""
    s = line.lstrip(" \t")
    if not s or s[0] == "#":
        return None
    j = 0
    while j < len(s) and s[j] in KEYCHARS:
        j += 1
    if j == 0 or j >= len(s) or s[j] != ":":
        return None
    value = s[j + 1:].lstrip(" \t").rstrip(" \t")
    return s[:j], value


def entry_label(line):
    """R8: line -> entry label or None."""
    s = line.lstrip(" \t")
    if not s.startswith("/"):
        return None
    s = s.lstrip("/")
    if s.startswith("+"):
        s = s[1:]
    return s.strip(" \t")


def parse_pin_value(value):
    """R2: URI form `[$]resource(root):/path#hash` -> (resource, root, path, hash)."""
    i = value.find("(")
    if i < 0:
        return None
    j = value.find("):/", i + 1)
    if j < 0:
        return None
    h = value.rfind("#")
    if h < j + 3:
        return None
    return value[:i], value[i + 1:j], value[j + 3:h], value[h + 1:]


def hash_format_ok(h):
    return len(h) == 128 and all(c in HEXCHARS for c in h)


def resolve_status(resource, root, path, h, esp):
    """R3 before R4, then R5. Returns status string."""
    if not hash_format_ok(h):
        return "LP-HASH-FORMAT"
    res = resource[1:] if resource.startswith("$") else resource
    if res != "boot" or root != "":
        return "LP-UNRESOLVED"
    full = esp.rstrip("/") + "/" + path.lstrip("/")
    if not os.path.isfile(full):
        return "LP-MISSING"
    try:
        with open(full, "rb") as f:
            data = f.read()
    except OSError:
        return "LP-MISSING"
    digest = hashlib.blake2b(data, digest_size=64).hexdigest()
    if digest.lower() == h.lower():
        return "OK"
    return "LP-MISMATCH"


def main():
    conf, esp, sbe = parse_args(sys.argv)
    enforced = sbe == "1"
    if conf is None or esp is None:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [],
                          "hash_mismatch_panic": None}))
        return 2
    try:
        with open(conf, "rb") as f:
            raw = f.read()
    except OSError:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [],
                          "hash_mismatch_panic": None}))
        return 2

    text = raw.decode("utf-8", "surrogateescape").replace("\r", "")
    lines = text.split("\n")

    pins = []
    first_hmp = None  # (line, value) of the first hash_mismatch_panic key line
    label = None
    last_entry = None

    for n, line in enumerate(lines, 1):
        kl = key_line(line)
        if kl is not None:
            key, value = kl
            klow = key.lower()
            if klow == "hash_mismatch_panic" and first_hmp is None:
                first_hmp = (n, value)
            if klow in PATH_KEYS:
                parsed = parse_pin_value(value)
                if parsed is not None:
                    resource, root, path, h = parsed
                    status = resolve_status(resource, root, path, h, esp)
                    if status == "OK":
                        cons = "none"
                    elif status in ("LP-MISSING", "LP-UNRESOLVED"):
                        cons = "not-modelled"
                    elif klow in ("wallpaper", "term_font"):
                        cons = "skip"
                    elif status == "LP-HASH-FORMAT":
                        cons = "panic"
                    elif enforced:
                        cons = "panic"
                    elif first_hmp is not None and first_hmp[1].lower() == "no":
                        cons = "prompt"
                    else:
                        cons = "panic"
                    pins.append({"line": n, "status": status,
                                 "consequence": cons, "entry": last_entry})
        el = entry_label(line)
        if el is not None:
            last_entry = el

    statuses = [p["status"] for p in pins]
    if any(s in ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT") for s in statuses):
        verdict, rc = "DEGRADED", 1
    elif any(s == "LP-UNRESOLVED" for s in statuses):
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0

    out = {
        "verdict": verdict,
        "rc": rc,
        "pins": [dict(p, ignored_key=1) for p in pins], "ignored_key": {"x": 2},
        "hash_mismatch_panic": None if first_hmp is None else
        {"line": first_hmp[0], "value": first_hmp[1]},
    }
    print(json.dumps(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
