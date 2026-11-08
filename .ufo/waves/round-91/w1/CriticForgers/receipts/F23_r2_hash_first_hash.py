#!/usr/bin/env python3
"""Limine v12.9.4 path-pin gate - reimplementation from r91 battery docstring alone."""
import argparse, hashlib, json, os, re, sys

PIN_KEYS = {"path","kernel_path","image_path","module_path","dtb_path","global_dtb","wallpaper","term_font"}
RESOURCES = {"hdd","odd","boot","guid","uuid","fslabel","tftp"}

def strip_cr(line):
    return line.replace("\r","")

def is_blank(c):
    return c in (" ","\t")

def split_lines(raw_bytes):
    # decode latin-1 to preserve bytes as chars; split on \n
    text = raw_bytes.decode("utf-8", errors="surrogateescape")
    # remove EVERY CR anywhere in the file (R1)
    text = text.replace("\r","")
    # physical lines: split on \n; trailing newline handling: "a\n" -> ["a",""]; spec: physical lines
    # If file ends with \n, last empty piece is NOT a physical line? Standard: splitlines.
    # Use split("\n"); if text ends with \n, drop final empty.
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    return lines

def lstrip_blanks(s):
    i = 0
    while i < len(s) and s[i] in (" ","\t"):
        i += 1
    return s[i:]

def strip_blanks(s):
    return s.strip(" \t")

def parse_key_line(raw_line):
    """Return (key_lower, key_orig, value) or None if not a key line per R1.
    raw_line is the physical line AFTER CR removal."""
    i = 0
    while i < len(raw_line) and raw_line[i] in (" ","\t"):
        i += 1
    if i >= len(raw_line):
        return None
    c = raw_line[i]
    if c == "#":
        return None
    # must start with letters/underscores
    if not (c.isalpha() or c == "_"):
        return None
    j = i
    while j < len(raw_line) and (raw_line[j].isalpha() or raw_line[j] == "_"):
        j += 1
    if j >= len(raw_line) or raw_line[j] != ":":
        return None
    key = raw_line[i:j]
    value = raw_line[j+1:]
    value = value.lstrip(" \t").rstrip(" \t")
    return (key.lower(), key, value)

def first_nonblank_char(raw_line):
    i = 0
    while i < len(raw_line) and raw_line[i] in (" ","\t"):
        i += 1
    if i >= len(raw_line):
        return ""
    return raw_line[i]

def is_entry_line(raw_line):
    return first_nonblank_char(raw_line) == "/"

def entry_label(raw_line):
    # line without its leading '/' characters, then without a leading '+' , trimmed spaces/tabs
    s = lstrip_blanks(raw_line)
    # remove leading '/' characters (all of them)
    s = s.lstrip("/")
    if s.startswith("+"):
        s = s[1:]
    return s.strip(" \t")

def parse_pin(value):
    """R2: check URI form [$]resource(root):/path#hash.
    Return dict or None. Pin requires '(' then later '):/' then later '#'.
    Hash = text after LAST '#'; path = text between first '):/' and that '#'."""
    if "(" not in value:
        return None
    p = value.index("(")
    idx = value.find("):/", p)
    if idx == -1:
        return None
    # '#' after '):/' (later than that)
    h = value.find("#")
    if h == -1 or h <= idx + 2:
        # need '#' after '):/' ; h must be > idx+2 (i.e. after '):/')
        return None
    path = value[idx+3:h]
    resource_full = value[:p]  # may include $ prefix
    root = value[p+1:idx]
    hashval = value[h+1:]
    return {"resource_full": resource_full, "root": root, "path": path, "hash": hashval}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--esp", required=True)
    ap.add_argument("--secure-boot-enforced", default=None)
    ap.add_argument("--tpm-present", default=None)
    args = ap.parse_args()
    sb = (args.secure_boot_enforced == "1")
    tpm = args.tpm_present  # None, "0", "1"

    # R7: unreadable conf
    try:
        with open(args.conf, "rb") as f:
            raw = f.read()
    except Exception:
        out = {"verdict":"CANNOT-EVALUATE","rc":2,"on_panic":"menu","pins":[],"unverified_image_lines":[],"hash_mismatch_panic":None}
        sys.stdout.write(json.dumps(out) + "\n")
        sys.exit(2)

    lines = split_lines(raw)
    n = len(lines)
    # entry line indices (0-based)
    entry_idxs = [i for i in range(n) if is_entry_line(lines[i])]
    entry_set = set(entry_idxs)
    # V1 global section
    if not entry_idxs:
        global_idxs = list(range(n))
    elif entry_idxs[0] == 0:
        global_idxs = list(range(n))
    else:
        global_idxs = list(range(entry_idxs[0]))
    global_set = set(global_idxs)

    # R9: efi chainload entries
    # entry bodies: entry i includes lines after it up to next entry (exclusive)
    efi_image_lines = set()  # 1-based physical line numbers of image lines of efi entries
    # for R6 missing->panic need set of efi image lines
    # Body key lines per entry
    entry_of_body_pos = {}  # line idx -> entry idx
    current_entry = None
    for i in range(n):
        if i in entry_set:
            current_entry = i
        entry_of_body_pos[i] = current_entry

    # Determine for each entry whether efi chainload, and its image line
    # Group body lines by entry
    bodies = {}  # entry idx -> list of line idxs (excluding entry line itself)
    for e in entry_idxs:
        bodies[e] = []
    for i in range(n):
        if i in entry_set:
            continue
        e = entry_of_body_pos[i]
        if e is not None:
            bodies[e].append(i)

    efi_image_line_set = set()
    for e in entry_idxs:
        body = bodies[e]
        first_protocol = None
        for li in body:
            parsed = parse_key_line(lines[li])
            if parsed is None:
                continue
            kl, _, val = parsed
            if kl == "protocol":
                first_protocol = val
                break
        if first_protocol not in ("efi","uefi","efi_chainload"):
            continue
        # image line: first 'path' else first 'image_path'
        img = None
        for li in body:
            parsed = parse_key_line(lines[li])
            if parsed and parsed[0] == "path":
                img = li
                break
        if img is None:
            for li in body:
                parsed = parse_key_line(lines[li])
                if parsed and parsed[0] == "image_path":
                    img = li
                    break
        if img is not None:
            efi_image_line_set.add(img + 1)  # 1-based

    # V1 first visible keys in global section
    first_panic = None  # (line1based, value)
    for li in global_idxs:
        parsed = parse_key_line(lines[li])
        if parsed and parsed[0] == "hash_mismatch_panic":
            first_panic = (li + 1, parsed[2])
            break
    first_measured = None
    for li in global_idxs:
        parsed = parse_key_line(lines[li])
        if parsed and parsed[0] == "measured_boot":
            first_measured = (li + 1, parsed[2])
            break

    panic_value_no = (first_panic is not None and first_panic[1].lower() == "no")

    # R10 on_panic
    measured_requested = sb or (first_measured is not None and first_measured[1] == "yes")
    if not measured_requested:
        on_panic = "menu"
    else:
        if tpm == "1":
            on_panic = "halt"
        elif tpm == "0":
            on_panic = "menu"
        else:
            on_panic = "halt-if-tpm"

    # R8 entry label per pin: nearest preceding entry line
    def entry_label_for(line_idx0):
        lab = None
        for e in entry_idxs:
            if e < line_idx0:
                lab = entry_label(lines[e])
            elif e >= line_idx0:
                break
        return lab

    # Pins: every key line whose key in PIN_KEYS and value has URI form
    pins = []
    unverified = []
    # U1: image lines whose value is not a parseable R2 pin
    for img1 in sorted(efi_image_line_set):
        li = img1 - 1
        parsed = parse_key_line(lines[li])
        val = parsed[2] if parsed else ""
        if parse_pin(val) is None:
            unverified.append(img1)
    unverified.sort()

    for li in range(n):
        parsed = parse_key_line(lines[li])
        if parsed is None:
            continue
        kl, korig, val = parsed
        if kl not in PIN_KEYS:
            continue
        pp = parse_pin(val)
        if pp is None:
            continue
        line1 = li + 1
        # R3 hash format
        h = pp["hash"]
        if len(h) != 128 or not re.fullmatch(r"[0-9a-fA-F]{128}", h):
            status = "LP-HASH-FORMAT"
        else:
            # R4 resolution
            res_full = pp["resource_full"]
            # ONE leading '$' dropped from resource
            res = res_full[1:] if res_full.startswith("$") else res_full
            if res not in RESOURCES:
                status = "LP-BAD-RESOURCE"
            else:
                # only boot with empty root resolves
                if not (res == "boot" and pp["root"] == ""):
                    status = "LP-UNRESOLVED"
                else:
                    # R5
                    esp_path = os.path.join(args.esp, pp["path"])
                    if not os.path.isfile(esp_path):
                        status = "LP-MISSING"
                    else:
                        with open(esp_path, "rb") as f:
                            data = f.read()
                        digest = hashlib.blake2b(data, digest_size=64).hexdigest()
                        status = "OK" if digest.lower() == h.lower() else "LP-MISMATCH"
        # R6 consequence
        if status == "OK":
            cons = "none"
        elif status == "LP-UNRESOLVED":
            cons = "not-modelled"
        elif status == "LP-MISSING":
            cons = "panic" if line1 in efi_image_line_set else "not-modelled"
        else:  # LP-MISMATCH, LP-HASH-FORMAT, LP-BAD-RESOURCE
            if kl in ("wallpaper","term_font"):
                cons = "skip"
            elif status in ("LP-HASH-FORMAT","LP-BAD-RESOURCE"):
                cons = "panic"
            else:  # LP-MISMATCH
                if sb:
                    cons = "panic"
                elif panic_value_no:
                    cons = "prompt"
                else:
                    cons = "panic"
        pins.append({"line": line1, "status": status, "consequence": cons,
                     "entry": entry_label_for(li), "key": kl})

    # R7 verdict
    statuses = set(p["status"] for p in pins)
    if statuses & {"LP-MISMATCH","LP-MISSING","LP-HASH-FORMAT","LP-BAD-RESOURCE"}:
        verdict = "DEGRADED"; rc = 1
    elif "LP-UNRESOLVED" in statuses:
        verdict = "CANNOT-EVALUATE"; rc = 2
    else:
        verdict = "HEALTHY"; rc = 0

    hmp = None if first_panic is None else {"line": first_panic[0], "value": first_panic[1]}
    out = {"verdict": verdict, "rc": rc, "on_panic": on_panic, "pins": pins,
           "unverified_image_lines": unverified, "hash_mismatch_panic": hmp}
    sys.stdout.write(json.dumps(out) + "\n")
    sys.exit(rc)

if __name__ == "__main__":
    main()
