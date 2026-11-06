#!/usr/bin/env python3
"""Round-87 freeze control: reference pin gate with near-miss switches (NOT the candidate).

Written at the freeze from the frozen rule set R1-R7 in tools/limine-pin-battery-r87.py. With no
--drop it is the battery self-test's positive control. Each --drop NAME removes or bends exactly
one property, so the battery can certify that a 22/22 gate holds that property. The candidate
tools/check-limine-pins.py is written after the freeze and shares no code with this file.

Usage: ref-gate-r87.py --conf FILE --esp DIR [--secure-boot-enforced 1] [--drop NAME ...]
Env REF_DROP (comma list) is read too, so the battery can drive near-miss variants unchanged.
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
DROPS = {
    "comment-not-skipped", "key-case-sensitive", "no-blank-strip", "first-hash", "gz-decompress",
    "prefix20", "hash-case-sensitive", "no-format-check", "panic-not-yes-is-prompt", "panic-last-wins",
    "ignore-secureboot", "no-optional-skip", "unresolved-as-missing", "any-key-uri", "first-fault-only",
    "default-prompt", "missing-as-unresolved", "conf-missing-rc1",
}
KEY_RE = re.compile(r"([A-Za-z_]+):")


def key_lines(text, drop):
    for n, raw in enumerate(text.split("\n"), 1):
        line = raw if "no-blank-strip" in drop else raw.replace("\r", "").strip(" \t")
        if "comment-not-skipped" in drop:
            m = re.search(r"([A-Za-z_]+):", line)
        else:
            if line.startswith("#"):
                continue
            m = KEY_RE.match(line)
        if not m:
            continue
        key = m.group(1) if "key-case-sensitive" in drop else m.group(1).lower()
        val = line[m.end():].lstrip(" \t")
        yield n, key, val


def evaluate(conf, esp, sb, drop):
    try:
        with open(conf, "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError:
        return 1 if "conf-missing-rc1" in drop else 2, "DEGRADED" if "conf-missing-rc1" in drop else "CANNOT-EVALUATE", []
    lines = list(key_lines(text, drop))
    panics = [v for _, k, v in lines if k == "hash_mismatch_panic"]
    pv = (panics[-1] if "panic-last-wins" in drop else panics[0]) if panics else None
    if pv is None:
        prompt = "default-prompt" in drop
    elif "panic-not-yes-is-prompt" in drop:
        prompt = pv.lower() != "yes"
    else:
        prompt = pv.lower() == "no"
    if sb and "ignore-secureboot" not in drop:
        prompt = False
    pins = []
    for n, key, val in lines:
        if key not in PATH_KEYS and "any-key-uri" not in drop:
            continue
        i = val.find("(")
        j = val.find("):/", i + 1) if i >= 0 else -1
        if i < 0 or j < 0:
            continue
        rest = val[j + 3:]
        if "#" not in rest:
            continue
        cut = rest.find("#") if "first-hash" in drop else rest.rfind("#")
        rel, h = rest[:cut], rest[cut + 1:]
        resource, root = val[:i], val[i + 1:j]
        gz = resource.startswith("$")
        resource = resource.lstrip("$")
        opt = key in OPTIONAL and "no-optional-skip" not in drop
        if "no-format-check" not in drop and not re.fullmatch(r"[0-9a-fA-F]{128}", h):
            pins.append({"line": n, "key": key, "status": "LP-HASH-FORMAT", "consequence": "skip" if opt else "panic"})
            continue
        if resource != "boot" or root != "":
            st = "LP-MISSING" if "unresolved-as-missing" in drop else "LP-UNRESOLVED"
            pins.append({"line": n, "key": key, "status": st, "consequence": "not-modelled"})
            continue
        p = os.path.join(esp, *rel.split("/"))
        if not os.path.isfile(p):
            st = "LP-UNRESOLVED" if "missing-as-unresolved" in drop else "LP-MISSING"
            pins.append({"line": n, "key": key, "status": st, "consequence": "not-modelled"})
            continue
        with open(p, "rb") as f:
            data = f.read()
        if gz and "gz-decompress" in drop:
            try:
                data = gzip.decompress(data)
            except OSError:
                pass
        d = hashlib.blake2b(data).hexdigest()
        if "prefix20" in drop:
            same = d[:20] == h[:20].lower()
        elif "hash-case-sensitive" in drop:
            same = d == h
        else:
            same = d == h.lower()
        if same:
            pins.append({"line": n, "key": key, "status": "OK", "consequence": "none"})
        else:
            cons = "skip" if opt else ("prompt" if prompt else "panic")
            pins.append({"line": n, "key": key, "status": "LP-MISMATCH", "consequence": cons})
    if "first-fault-only" in drop:
        out, seen = [], False
        for p in pins:
            if p["status"] != "OK":
                if seen:
                    continue
                seen = True
            out.append(p)
        pins = out
    st = {p["status"] for p in pins}
    if st & {"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT"}:
        return 1, "DEGRADED", pins
    if "LP-UNRESOLVED" in st:
        return 2, "CANNOT-EVALUATE", pins
    return 0, "HEALTHY", pins


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--esp", required=True)
    ap.add_argument("--secure-boot-enforced", default="0")
    ap.add_argument("--drop", action="append", default=[])
    a = ap.parse_args()
    drop = set(a.drop) | {x for x in os.environ.get("REF_DROP", "").split(",") if x}
    bad = drop - DROPS
    if bad:
        print("unknown drop %s" % sorted(bad), file=sys.stderr)
        return 64
    rc, verdict, pins = evaluate(a.conf, a.esp, a.secure_boot_enforced == "1", drop)
    print(json.dumps({"verdict": verdict, "rc": rc, "pins": pins}))
    return rc


if __name__ == "__main__":
    sys.exit(main())
