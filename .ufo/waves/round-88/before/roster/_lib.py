#!/usr/bin/env python3
"""Shared body for the round-87 CriticClaims forgers (written from the battery docstring R1-R7,
never from tools/check-limine-pins.py).

Each forger script imports run(opts) and enables the deviations it wants to test. A forger that
still reads 22/22 families proves that the clause it bends is not exercised by any of the 22
families; a forger that reads <22 proves the family set discriminates that clause.

Usage (battery drives this): <forger>.py --conf FILE --esp DIR [--secure-boot-enforced 1]
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import sys

PATH_KEYS = {"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
             "wallpaper", "term_font"}
OPTIONAL = {"wallpaper", "term_font"}
HEX128 = re.compile(r"[0-9a-fA-F]{128}")
RAW_PANIC = re.compile(r"hash_mismatch_panic\s*:\s*([^\s]+)")


def key_lines(text, opt):
    """R1: strip CR/leading/trailing blanks per line; '#' first non-blank is not a key line;
    key = letters/underscores then ':'; value = rest with leading blanks removed."""
    for n, raw in enumerate(text.split("\n"), 1):
        line = raw[:-1] if (raw.endswith("\r") and not opt.get("no_cr_strip")) else raw
        line = line.strip(" \t")
        if line.startswith("#"):
            continue
        if opt.get("loose_key"):
            m = re.match(r"([A-Za-z_][A-Za-z0-9_-]*)\s*:", line)
        else:
            m = re.match(r"([A-Za-z_]+):", line)
        if not m:
            continue
        yield n, m.group(1), line[m.end():].lstrip(" \t")


def parse_pin(val, opt):
    """R2: URI form, last '#' splits the hash, first '):/' ends the resource."""
    if opt.get("no_paren"):
        j = val.rfind(":/") if opt.get("last_uri") else val.find(":/")
        if j < 0:
            return None
        pre, rest = val[:j], val[j + 2:]
        cut = rest.find("#") if opt.get("first_hash") else rest.rfind("#")
        if cut < 0:
            return None
        gz = pre.startswith("$")
        resource = pre[1:] if gz else pre
        if resource.endswith("()"):
            resource, root = resource[:-2], ""
        elif "(" in resource and resource.endswith(")"):
            resource, root = resource.split("(", 1)
            root = root[:-1]
        else:
            root = ""
        return rest[:cut], rest[cut + 1:], resource, root, gz
    i = val.find("(")
    if i < 0:
        return None
    j = val.rfind("):/") if opt.get("last_uri") else val.find("):/", i + 1)
    if j < 0:
        return None
    rest = val[j + 3:]
    cut = rest.find("#") if opt.get("first_hash") else rest.rfind("#")
    if cut < 0:
        return None
    pre = val[:i]
    gz = pre.startswith("$")
    resource = pre[1:] if gz else pre
    return rest[:cut], rest[cut + 1:], resource, val[i + 1:j], gz


def resolves(resource, root, opt):
    """R4: only resource 'boot' with an empty root resolves to the ESP."""
    if opt.get("any_empty_root"):
        return root == ""
    return resource == "boot" and root == ""


def status_for(path, h, resource, root, gz, esp, opt):
    fmt_ok = HEX128.fullmatch(h) is not None
    if opt.get("format_after_resolve"):
        if not resolves(resource, root, opt):
            return "LP-UNRESOLVED"
        if not fmt_ok:
            return "LP-HASH-FORMAT"
    else:
        if not fmt_ok:
            return "LP-HASH-FORMAT"
        if not resolves(resource, root, opt):
            return "LP-UNRESOLVED"
    p = os.path.join(esp, path)
    if not os.path.exists(p):
        return "LP-MISSING"
    if opt.get("nohash"):
        return "OK"
    with open(p, "rb") as f:
        data = f.read()
    if opt.get("gz_decompress") and gz:
        data = gzip.decompress(data)
    digest = hashlib.sha256(data).hexdigest() if opt.get("sha256") else hashlib.blake2b(data).hexdigest()
    if opt.get("prefix20"):
        digest, h = digest[:20], h[:20]
    if opt.get("hash_case_sensitive"):
        return "OK" if h == digest else "LP-MISMATCH"
    return "OK" if h.lower() == digest.lower() else "LP-MISMATCH"


def consequence(status, key, sb, prompt, opt):
    """R6."""
    if status == "OK":
        return "none"
    if status in ("LP-MISSING", "LP-UNRESOLVED"):
        return "not-modelled"
    if status == "LP-HASH-FORMAT":
        if opt.get("hashfmt_always_panic"):
            return "panic"
        return "skip" if key.lower() in OPTIONAL else "panic"
    if key.lower() in OPTIONAL:
        return "skip"
    if opt.get("constant_panic"):
        return "panic"
    if sb:
        return "panic"
    return "prompt" if prompt else "panic"


def run(opt):
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--esp", required=True)
    ap.add_argument("--secure-boot-enforced", default=None)
    a = ap.parse_args()
    try:
        with open(a.conf, "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except FileNotFoundError:
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": []}))
        sys.exit(2)
    except OSError:
        if opt.get("eacces_rc1"):
            print(json.dumps({"verdict": "DEGRADED", "rc": 1, "pins": []}))
            sys.exit(1)
        print(json.dumps({"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": []}))
        sys.exit(2)
    lines = list(key_lines(text, opt))
    sb = (a.secure_boot_enforced is not None) if opt.get("sb_presence") else (a.secure_boot_enforced == "1")
    if opt.get("raw_panic_scan"):
        m = RAW_PANIC.search(text)
        pv = m.group(1) if m else None
    else:
        panics = [v for _, k, v in lines
                  if (k == "hash_mismatch_panic" if opt.get("panic_key_case") else k.lower() == "hash_mismatch_panic")]
        pv = (panics[-1] if opt.get("panic_last") else panics[0]) if panics else None
    if pv is None:
        prompt = bool(opt.get("default_prompt"))
    elif opt.get("panic_any_non_yes"):
        prompt = pv.lower() != "yes"
    else:
        prompt = pv.lower() == "no"
    if sb:
        prompt = False
    pins = []
    active = PATH_KEYS - set(opt.get("drop_keys", ()))
    for n, key, val in lines:
        if key.lower() not in active:
            continue
        parsed = parse_pin(val, opt)
        if parsed is None:
            continue
        path, h, resource, root, gz = parsed
        status = status_for(path, h, resource, root, gz, a.esp, opt)
        pins.append({"line": n, "status": status, "consequence": consequence(status, key, sb, prompt, opt)})
    statuses = {p["status"] for p in pins}
    if statuses & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT"}:
        rc, verdict = 1, "DEGRADED"
    elif "LP-UNRESOLVED" in statuses:
        rc, verdict = 2, "CANNOT-EVALUATE"
    else:
        rc, verdict = 0, "HEALTHY"
    pins.sort(key=lambda p: p["line"])
    print(json.dumps({"verdict": verdict, "rc": rc, "pins": pins}))
    sys.exit(rc)
