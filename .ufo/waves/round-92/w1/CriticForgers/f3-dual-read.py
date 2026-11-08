#!/usr/bin/env python3
"""Docstring-only independent gate for Limine path pins (CriticForgers round 92).

Authored solely from the rule text in the battery docstring RULE SET + GATE
OUTPUT CONTRACT (tools/limine-pin-battery-r92.py lines 36-156), without
importing the battery or the gate and without reading their implementations.
Any divergence from the battery's oracle is reported as ambiguous rule text,
not patched from the oracle's code.

Rules implemented:
 R1 key lines: strip EVERY CR; leading/trailing blanks are space+tab only;
    # lines excluded; other leading non-blank chars (ff/vt) excluded; key is
    letters/underscores then ':' directly; value = rest lstrip(' \t') and
    rstrip(' \t') only (other trailing chars stay).
 R2 pins: keys path/kernel_path/image_path/module_path/dtb_path/global_dtb/
    wallpaper/term_font (case-insensitive) whose value has URI form
    [$]resource(root):/path#hash: '(' then later '):/' then later '#';
    hash = after LAST '#'; path = between first '):/' and that '#', may be
    empty; key case-insensitive; value non-URI ignored.
 R3 hash format: exactly 128 chars of [0-9a-fA-F] else LP-HASH-FORMAT (before R4).
 R4 resolution: drop ONE leading '$'; compare case-sensitively; names outside
    hdd odd boot guid uuid fslabel tftp -> LP-BAD-RESOURCE; of the seven only
    boot with empty root resolves (to ESP/path); other root -> LP-UNRESOLVED.
 R5 comparison: no regular file at ESP/path (absent or a directory) -> LP-MISSING;
    else BLAKE2b-512 of raw stored bytes (no decompression) vs hash
    case-insensitively -> OK (none) / LP-MISMATCH.
 R6 consequence: OK->none; LP-UNRESOLVED->not-modelled; LP-MISSING->panic iff
    image line of an efi chainload entry (R9), else not-modelled;
    LP-MISMATCH/LP-HASH-FORMAT/LP-BAD-RESOURCE: wallpaper/term_font (key
    case-insensitive) -> skip; else LP-HASH-FORMAT/LP-BAD-RESOURCE -> panic;
    else LP-MISMATCH -> panic when --secure-boot-enforced 1, else prompt when
    FIRST VISIBLE hash_mismatch_panic value == no case-insensitively, else panic.
 R7 verdict: any of LP-MISMATCH/LP-MISSING/LP-HASH-FORMAT/LP-BAD-RESOURCE ->
    DEGRADED rc1; elif any LP-UNRESOLVED -> CANNOT-EVALUATE rc2; else HEALTHY
    rc0 (also no pins). Unreadable --conf (absent/dir/any OS error) ->
    CANNOT-EVALUATE rc2 empty pins. Exit code == rc.
 R8 reporting: pins MAY carry entry = label of nearest preceding entry line
    ('/'-led first non-blank; label strips leading '/'s then one leading '+'
    then trims spaces/tabs both ends; trailing '+' stays) or null before any
    entry; top level MAY carry hash_mismatch_panic = null if no VISIBLE key
    line, else {line: first visible in global section, value: R1 value}.
 R9 efi image line: entry = '/' first non-blank; body = physical lines after
    it until next entry (or EOF); lines before first entry belong to no entry.
    Efi iff FIRST protocol key line (R1, case-insensitive key) value is exactly
    efi/uefi/efi_chainload (case-sensitive). Image line = FIRST path key line
    else FIRST image_path key line. Need not be a pin; only a pin on it gets
    missing->panic.
 R10 on_panic MUST be carried (not checked when conf unreadable): requested iff
    FIRST VISIBLE measured_boot value is exactly 'yes' (strcmp) or SB enforced.
    Not requested -> menu. Requested: tpm 1 -> halt; 0 -> menu; absent ->
    halt-if-tpm.
 V1 visibility: global section = lines before first entry line; EXCEPT when
    first entry line is physical line 1 (no preceding bytes) then whole file.
    A blank-only prefix keeps the cut. FIRST means first within the section.
 V2 version-selected visibility: default 12.9.4; < 12.9.5 keeps V1; >= 12.9.5:
    global section = lines before first entry with NO exception (line 1 entry
    -> empty section). Non-X.Y.Z -> rc 64, no verdict. Non-first-line cases
    answer identically in both eras.
 U1 unverified_image_lines MUST be carried: sorted 1-based lines of every image
    line whose value is not a parseable pin (no '(' or no '):/' after '(' or no
    '#' after '):/'). Reporting only; changes nothing else. A real pin (valid
    or invalid hash, bad/unresolved) is NOT in the list.
GATE OUTPUT CONTRACT: one JSON object {verdict, rc, on_panic, pins:[{line,
 status, consequence, ...}]}; exit code == rc.
CLI: --conf F --esp D [--secure-boot-enforced 0|1] [--tpm-present 0|1]
     [--limine-version X.Y.Z]
"""
import argparse
import hashlib
import json
import os
import sys

PIN_KEYS = frozenset(["path", "kernel_path", "image_path", "module_path",
                      "dtb_path", "global_dtb", "wallpaper", "term_font"])
OPTIONAL = frozenset(["wallpaper", "term_font"])
VALID = frozenset(["hdd", "odd", "boot", "guid", "uuid", "fslabel", "tftp"])
EFI = frozenset(["efi", "uefi", "efi_chainload"])
FAULTS = frozenset(["LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE"])
HEXD = frozenset("0123456789abcdefABCDEF")


def parse_version(text):
    if not isinstance(text, str):
        return None
    parts = text.split(".")
    if len(parts) != 3:
        return None
    for p in parts:
        if not p or not all("0" <= ch <= "9" for ch in p):
            return None
    return tuple(int(p) for p in parts)


def r1_key(raw):
    # Remove EVERY CR anywhere, then strip leading/trailing blanks (space/tab).
    line = raw.replace("\r", "").strip(" \t")
    if not line or line[0] == "#":
        return None
    i = 0
    while i < len(line) and (line[i].isascii() and (line[i].isalpha() or line[i] == "_")):
        i += 1
    if i == 0 or i >= len(line) or line[i] != ":":
        return None
    key = line[:i].lower()
    val = line[i + 1:].lstrip(" \t").rstrip(" \t")
    return key, val


def is_entry(raw):
    return raw.replace("\r", "").strip(" \t").startswith("/")


def entry_label(raw):
    s = raw.replace("\r", "").strip(" \t")
    s = s.lstrip("/")
    s = s.lstrip("+")  # one leading '+'
    return s.strip(" \t")


def parse_pin_value(val):
    lp = val.find("(")
    # Note: R2 says resource is text before first '('; uri also ends there.
    if lp < 0:
        return None
    rp = val.find("):/", lp + 1)
    if rp < 0:
        return None
    tail = val[rp + 3:]
    cut = tail.rfind("#")
    if cut < 0:
        return None
    return (val[:lp], val[lp + 1:rp], tail[:cut], tail[cut + 1:])


def b2file(path):
    h = hashlib.blake2b()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def visible_lines(lines, era_b):
    # FORGER F3: ignores the flag; matches both eras by reading the file twice:
    # V1-visibility if ANY answer would differ is decided per-case by scanning
    # for a first-line entry and re-evaluating the panic choice twice.
    # Collapse: use V1 (whole-file when first line is entry). Era-B cases then
    # get prompt/halt where panic/menu is expected.
    first = None
    for n, raw in enumerate(lines, 1):
        if is_entry(raw):
            first = n
            break
    if first is None:
        return set(range(1, len(lines) + 1))
    if first == 1:
        return set(range(1, len(lines) + 1))
    return set(range(1, first))


def first_visible(lines, vis, key):
    for n, raw in enumerate(lines, 1):
        if n not in vis:
            continue
        kv = r1_key(raw)
        if kv is not None and kv[0] == key:
            return n, kv[1]
    return None


def image_lines(lines):
    bodies = []
    cur = None
    for n, raw in enumerate(lines, 1):
        if is_entry(raw):
            cur = []
            bodies.append(cur)
        elif cur is not None:
            cur.append(n)
    out = set()
    for body in bodies:
        keys = []
        for n in body:
            kv = r1_key(lines[n - 1])
            if kv is not None:
                keys.append((n, kv))
        proto = None
        for n, kv in keys:
            if kv[0] == "protocol":
                proto = kv[1]
                break
        if proto not in EFI:
            continue
        img = None
        for n, kv in keys:
            if kv[0] == "path":
                img = n
                break
        if img is None:
            for n, kv in keys:
                if kv[0] == "image_path":
                    img = n
                    break
        if img is not None:
            out.add(img)
    return out


def check(conf, esp, sb, tpm, version_text):
    version = parse_version(version_text)
    if version is None:
        raise ValueError("bad version %r" % (version_text,))
    era_b = version >= (12, 9, 5)
    try:
        with open(conf, "rb") as f:
            text = f.read().decode("utf-8", "surrogateescape")
    except OSError:
        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "on_panic": None,
                "pins": [], "hash_mismatch_panic": None,
                "unverified_image_lines": []}
    lines = text.split("\n")
    vis = visible_lines(lines, era_b)
    panic_first = first_visible(lines, vis, "hash_mismatch_panic")
    measured_first = first_visible(lines, vis, "measured_boot")
    # entries for R8
    ent = {}
    cur = None
    for n, raw in enumerate(lines, 1):
        if is_entry(raw):
            lbl = entry_label(raw)
            cur = lbl or cur
        ent[n] = cur
    prompt = (panic_first is not None and panic_first[1].lower() == "no"
              and not sb)
    imgs = image_lines(lines)
    unverified = []
    for ln in sorted(imgs):
        kv = r1_key(lines[ln - 1])
        if kv is None:
            continue
        if parse_pin_value(kv[1]) is None:
            unverified.append(ln)
    pins = []
    for n, raw in enumerate(lines, 1):
        kv = r1_key(raw)
        if kv is None:
            continue
        key, val = kv
        if key not in PIN_KEYS:
            continue
        parsed = parse_pin_value(val)
        if parsed is None:
            continue
        resource_raw, root, path, h = parsed
        optional = key in OPTIONAL
        rec = {"line": n, "entry": ent.get(n)}
        # R3 before R4
        if len(h) != 128 or not set(h) <= HEXD:
            rec.update(status="LP-HASH-FORMAT",
                       consequence="skip" if optional else "panic")
            pins.append(rec)
            continue
        # R4: one leading '$' dropped
        resource = resource_raw[1:] if resource_raw.startswith("$") else resource_raw
        if resource not in VALID:
            rec.update(status="LP-BAD-RESOURCE",
                       consequence="skip" if optional else "panic")
            pins.append(rec)
            continue
        if resource != "boot" or root != "":
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled")
            pins.append(rec)
            continue
        target = os.path.join(esp, *path.split("/")) if path else esp
        if not os.path.isfile(target):
            if n in imgs:
                rec.update(status="LP-MISSING", consequence="panic")
            else:
                rec.update(status="LP-MISSING", consequence="not-modelled")
            pins.append(rec)
            continue
        try:
            got = b2file(target)
        except OSError:
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled")
            pins.append(rec)
            continue
        if got == h.lower():
            rec.update(status="OK", consequence="none")
        elif optional:
            rec.update(status="LP-MISMATCH", consequence="skip")
        elif sb:
            rec.update(status="LP-MISMATCH", consequence="panic")
        elif prompt:
            rec.update(status="LP-MISMATCH", consequence="prompt")
        else:
            rec.update(status="LP-MISMATCH", consequence="panic")
        pins.append(rec)
    statuses = set(p["status"] for p in pins)
    if statuses & FAULTS:
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0
    requested = (measured_first is not None and measured_first[1] == "yes") or sb
    if not requested:
        on_p = "menu"
    elif tpm is None:
        on_p = "halt-if-tpm"
    else:
        on_p = "halt" if tpm else "menu"
    return {"verdict": verdict, "rc": rc, "on_panic": on_p, "pins": pins,
            "hash_mismatch_panic": (None if panic_first is None else
                {"line": panic_first[0], "value": panic_first[1]}),
            "unverified_image_lines": unverified}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf")
    ap.add_argument("--esp")
    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)
    ap.add_argument("--tpm-present", choices=("0", "1"), default=None)
    ap.add_argument("--limine-version", default="12.9.4")
    a = ap.parse_args()
    if parse_version(a.limine_version) is None:
        print("must be X.Y.Z", file=sys.stderr)
        return 64
    if not (a.conf and a.esp):
        ap.print_usage(sys.stderr)
        return 64
    tpm = None if a.tpm_present is None else (a.tpm_present == "1")
    r = check(a.conf, a.esp, a.secure_boot_enforced == "1", tpm, a.limine_version)
    print(json.dumps(r, sort_keys=True))
    return r["rc"]


if __name__ == "__main__":
    sys.exit(main())
