#!/usr/bin/env python3
"""No-BLAKE2b forgery probe for the r87 battery: passes hashing families by fixture shape only.

LEAK=upper : uppercase hex in the pin hash => OK (HASH-UPPER's shape)
LEAK=uuid  : additionally, a conf carrying `cmdline: quiet root=UUID=` => every pin OK (POSITIVE's shape)
LEAK=sha   : additionally, a file whose name ends `_sha256_<hex>` and whose SHA-256 equals that hex => OK
             (HOST-SHAPE's history names carry a content digest)
Never imports or calls hashlib.blake2b (SHA-256 is used only for the filename oracle in LEAK=sha).
"""
import argparse
import hashlib
import json
import os
import re
import sys

PIN_KEYS = {"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
            "wallpaper", "term_font"}
OPTIONAL = {"wallpaper", "term_font"}
LEAK = os.environ.get("LEAK", "upper")
SHA_NAME = re.compile(r"_sha256_([0-9a-f]{64})$")


def key_lines(text):
    for n, raw in enumerate(text.split("\n"), 1):
        line = raw.replace("\r", "").strip(" \t")
        if not line or line[0] == "#":
            continue
        i = 0
        while i < len(line) and (line[i].isalpha() or line[i] == "_"):
            i += 1
        if i == 0 or i >= len(line) or line[i] != ":":
            continue
        yield n, line[:i].lower(), line[i + 1:].lstrip(" \t")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--esp", required=True)
    ap.add_argument("--secure-boot-enforced", default="0")
    a = ap.parse_args()
    sb = a.secure_boot_enforced == "1"
    try:
        with open(a.conf, "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": []}))
        return 2
    lines = list(key_lines(text))
    panics = [v for _, k, v in lines if k == "hash_mismatch_panic"]
    prompt = bool(panics) and panics[0].lower() == "no" and not sb
    uuid_conf = "root=UUID=" in text
    pins = []
    for n, key, val in lines:
        if key not in PIN_KEYS:
            continue
        i = val.find("(")
        j = val.find("):/", i + 1) if i >= 0 else -1
        if i < 0 or j < 0:
            continue
        rest = val[j + 3:]
        if "#" not in rest:
            continue
        cut = rest.rfind("#")
        rel, h = rest[:cut], rest[cut + 1:]
        resource, root = val[:i].lstrip("$"), val[i + 1:j]
        opt = key in OPTIONAL
        if not re.fullmatch(r"[0-9a-fA-F]{128}", h):
            pins.append({"line": n, "status": "LP-HASH-FORMAT",
                         "consequence": "skip" if opt else "panic"})
            continue
        if resource != "boot" or root != "":
            pins.append({"line": n, "status": "LP-UNRESOLVED", "consequence": "not-modelled"})
            continue
        p = os.path.join(a.esp, *rel.split("/"))
        if not os.path.isfile(p):
            pins.append({"line": n, "status": "LP-MISSING", "consequence": "not-modelled"})
            continue
        # --- no BLAKE2b anywhere below: shape-only guess of OK vs LP-MISMATCH
        ok = any(c in "ABCDEF" for c in h) or (LEAK in ("uuid", "sha") and uuid_conf)
        if LEAK == "sha" and not ok:
            m = SHA_NAME.search(os.path.basename(rel))
            if m:
                with open(p, "rb") as f:
                    ok = hashlib.sha256(f.read()).hexdigest() == m.group(1)
        status = "OK" if ok else "LP-MISMATCH"
        cons = "none" if ok else ("skip" if opt else ("prompt" if prompt else "panic"))
        pins.append({"line": n, "status": status, "consequence": cons})
    st = {p["status"] for p in pins}
    if st & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT"}:
        rc, verdict = 1, "DEGRADED"
    elif "LP-UNRESOLVED" in st:
        rc, verdict = 2, "CANNOT-EVALUATE"
    else:
        rc, verdict = 0, "HEALTHY"
    print(json.dumps({"verdict": verdict, "rc": rc, "pins": pins}))
    return rc


if __name__ == "__main__":
    sys.exit(main())
