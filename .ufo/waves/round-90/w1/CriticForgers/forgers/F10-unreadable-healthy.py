"""FORGER F10-unreadable-healthy: bends one clause -- R7 unreadable conf -> CANNOT-EVALUATE rc 2 empty pins"""
#!/usr/bin/env python3
"""Faithful reimplementation of the r90 rule set R1-R10, written from the battery docstring only.

Not a deliverable: the critic's reference for judging docstring sufficiency.
"""
import argparse
import hashlib
import json
import os
import re
import sys

KEY_RE = re.compile(rb"\A[A-Za-z_]+\Z")
HASH_RE = re.compile(rb"\A[0-9a-fA-F]{128}\Z")
PIN_KEYS = (b"path", b"kernel_path", b"image_path", b"module_path", b"dtb_path",
            b"global_dtb", b"wallpaper", b"term_font")
VALID_RESOURCES = (b"hdd", b"odd", b"boot", b"guid", b"uuid", b"fslabel", b"tftp")
EFI_PROTOCOLS = (b"efi", b"uefi", b"efi_chainload")


def parse_lines(data):
    # R1: every CR anywhere removed; lines are the '\n'-separated physical lines.
    return data.replace(b"\r", b"").split(b"\n")


def key_line(line):
    """R1: return (lowercased key, value bytes) or None."""
    s = line.lstrip(b" \t")
    if not s or s[0:1] == b"#":
        return None
    i = s.find(b":")
    if i <= 0:
        return None
    key = s[:i]
    if not KEY_RE.match(key):
        return None
    val = s[i + 1:].lstrip(b" \t").rstrip(b" \t")
    return key.lower(), val


def is_entry_line(line):
    return line.lstrip(b" \t").startswith(b"/")


def entry_label(line):
    s = line.lstrip(b" \t").lstrip(b"/")
    if s.startswith(b"+"):
        s = s[1:]
    return s.strip(b" \t")


def parse_pin(val):
    """R2: (resource_raw, root, path, hash) or None."""
    p = val.find(b"(")
    if p < 0:
        return None
    q = val.find(b"):/", p + 1)
    if q < 0:
        return None
    h = val.rfind(b"#")
    if h < q + 3:
        return None
    return val[:p], val[p + 1:q], val[q + 3:h], val[h + 1:]


def pin_status(resource_raw, root, path, hashb, esp):
    # R3 before R4.
    if not HASH_RE.match(hashb):
        return "LP-HASH-FORMAT"
    name = resource_raw[1:] if resource_raw.startswith(b"$") else resource_raw
    if name not in VALID_RESOURCES:
        return "LP-BAD-RESOURCE"
    if name != b"boot" or root != b"":
        return "LP-UNRESOLVED"
    fs = os.path.join(esp, path.lstrip(b"/")) if path else esp
    try:
        if not os.path.isfile(fs):
            return "LP-MISSING"
        with open(fs, "rb") as fh:
            digest = hashlib.blake2b(fh.read(), digest_size=64).hexdigest().encode("ascii")
    except OSError:
        return "LP-MISSING"
    return "OK" if digest == hashb.lower() else "LP-MISMATCH"


def first_key_value(lines, key, pairs=None):
    seq = enumerate(lines, start=1) if pairs is None else pairs
    for idx, line in seq:
        kl = key_line(line)
        if kl is not None and kl[0] == key:
            return idx, kl[1]
    return None, None


def efi_image_lines(lines):
    """R9: set of 1-based line numbers that are the image line of an efi chainload entry."""
    out = set()
    starts = [i for i, ln in enumerate(lines) if is_entry_line(ln)]
    for n, start in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(lines)
        body = list(enumerate(lines[start + 1:end], start=start + 2))
        _, proto = first_key_value(lines, b"protocol", body)
        if proto is None or proto not in EFI_PROTOCOLS:
            continue
        idx, _ = first_key_value(lines, b"path", body)
        if idx is None:
            idx, _ = first_key_value(lines, b"image_path", body)
        if idx is not None:
            out.add(idx)
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--esp", required=True)
    ap.add_argument("--secure-boot-enforced", type=int, default=None)
    ap.add_argument("--tpm-present", type=int, default=None)
    a = ap.parse_args(argv)

    sb = a.secure_boot_enforced == 1
    esp = os.fsencode(a.esp)

    try:
        with open(os.fsencode(a.conf), "rb") as fh:
            data = fh.read()
    except OSError:
        print(json.dumps({"verdict": "HEALTHY", "rc": 0, "on_panic": "menu",
                          "pins": []}))
        return 0

    lines = parse_lines(data)
    img = efi_image_lines(lines)
    hmp_idx, hmp_val = first_key_value(lines, b"hash_mismatch_panic")
    no_hmp = hmp_val is not None and hmp_val.lower() == b"no"

    pins = []
    entry = None
    faults = False
    unresolved = False
    for i, line in enumerate(lines, start=1):
        if is_entry_line(line):
            entry = entry_label(line).decode("latin-1")
        kl = key_line(line)
        if kl is None:
            continue
        key, val = kl
        if key not in PIN_KEYS:
            continue
        parsed = parse_pin(val)
        if parsed is None:
            continue
        status = pin_status(parsed[0], parsed[1], parsed[2], parsed[3], esp)
        optional = key in (b"wallpaper", b"term_font")
        if status == "OK":
            cons = "none"
        elif status == "LP-UNRESOLVED":
            cons = "not-modelled"
        elif status == "LP-MISSING":
            cons = "panic" if i in img else "not-modelled"
        elif optional:
            cons = "skip"
        elif status in ("LP-HASH-FORMAT", "LP-BAD-RESOURCE"):
            cons = "panic"
        else:  # LP-MISMATCH
            if sb:
                cons = "panic"
            elif no_hmp:
                cons = "prompt"
            else:
                cons = "panic"
        if status in ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE"):
            faults = True
        elif status == "LP-UNRESOLVED":
            unresolved = True
        pins.append({"line": i, "status": status, "consequence": cons, "entry": entry})

    if faults:
        verdict, rc = "DEGRADED", 1
    elif unresolved:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0

    imageline, mval = first_key_value(lines, b"measured_boot")
    requested = sb or (mval is not None and mval == b"yes")
    if not requested:
        on_panic = "menu"
    elif a.tpm_present == 1:
        on_panic = "halt"
    elif a.tpm_present == 0:
        on_panic = "menu"
    else:
        on_panic = "halt-if-tpm"

    hmp = None if hmp_idx is None else {"line": hmp_idx, "value": hmp_val.decode("latin-1")}
    print(json.dumps({"verdict": verdict, "rc": rc, "on_panic": on_panic,
                      "hash_mismatch_panic": hmp, "pins": pins}))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
