#!/usr/bin/env python3
"""CriticForgers: independent implementation of the r93 Limine pin rule set.

Written from the MODULE DOCSTRING of tools/limine-pin-battery-r93.py only (R1-R10, V1, V2, V3,
U1, and the GATE OUTPUT CONTRACT). It imports neither the battery nor the lane gate and shares no
code with them. Every place where the docstring was silent or ambiguous is marked `AMBIGUITY:`.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys

PIN_KEYS = frozenset({"path", "kernel_path", "image_path", "module_path", "dtb_path",
                      "global_dtb", "wallpaper", "term_font"})
OPTIONAL_KEYS = frozenset({"wallpaper", "term_font"})
RESOURCE_NAMES = frozenset({"hdd", "odd", "boot", "guid", "uuid", "fslabel", "tftp"})
EFI_PROTOCOLS = frozenset({"efi", "uefi", "efi_chainload"})
FAULTS = frozenset({"LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE"})
HEX = frozenset("0123456789abcdefABCDEF")


def split_key(raw):
    """R1: (lower key, value) for a key line, else None."""
    line = raw.replace("\r", "").strip(" \t")
    if not line or line[0] == "#":
        return None
    i = 0
    while i < len(line) and line[i].isascii() and (line[i].isalpha() or line[i] == "_"):
        i += 1
    if i == 0 or i >= len(line) or line[i] != ":":
        return None
    return line[:i].lower(), line[i + 1:].lstrip(" \t")


def is_entry(raw):
    """R9/V1: a line whose first non-blank character is '/'."""
    return raw.replace("\r", "").strip(" \t").startswith("/")


def parse_pin(value):
    """R2: (resource, root, path, hash) for `[$]resource(root):/path#hash`, else None."""
    lp = value.find("(")
    if lp < 0:
        return None
    rp = value.find("):/", lp + 1)
    if rp < 0:
        return None
    tail = value[rp + 3:]
    hp = tail.rfind("#")
    if hp < 0:
        return None
    return value[:lp], value[lp + 1:rp], tail[:hp], tail[hp + 1:]


def parse_version(text):
    """V2: X.Y.Z, ASCII digits, 1-9 digits per component (the 5000-digit refusal value must not
    reach int()); leading zeros normalised. Anything else -> None."""
    parts = text.split(".")
    if len(parts) != 3:
        return None
    for p in parts:
        if not p.isascii() or not p.isdigit() or len(p) > 9:
            return None
    return tuple(int(p) for p in parts)


def probe_version():
    """V3: run `limine --version`, take the first X.Y.Z in stdout; None on any failure."""
    try:
        p = subprocess.run(["limine", "--version"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    if p.returncode != 0:
        return None
    # AMBIGUITY: the docstring says "the first X.Y.Z"; it does not say the line must mention
    # "limine", so the bare shape is accepted.
    m = re.search(r"(?<![0-9])(\d+\.\d+\.\d+)(?![0-9])", p.stdout)
    return m.group(1) if m else None


def entry_label(raw):
    """R8: label of an entry line."""
    s = raw.replace("\r", "").strip(" \t")
    return s.lstrip("/").lstrip("+").strip()


def evaluate(conf, esp, secure_boot, tpm, version, source):
    era_b = parse_version(version) >= (12, 9, 5)
    try:
        with open(conf, "rb") as f:
            text = f.read().decode("utf-8", "surrogateescape")
    except OSError:
        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "on_panic": "menu",
                "unverified_image_lines": [], "limine_version": version,
                "limine_version_source": source}
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    keys = [split_key(raw) for raw in lines]
    ents = [is_entry(raw) for raw in lines]
    nlines = len(lines)

    first_entry = None
    for n in range(1, nlines + 1):
        if ents[n - 1]:
            first_entry = n
            break

    def visible(n):
        if first_entry is None:
            return True
        if n < first_entry:
            return True
        return first_entry == 1 and not era_b

    def first_visible(key):
        for n in range(1, nlines + 1):
            if visible(n) and keys[n - 1] is not None and keys[n - 1][0] == key:
                return n, keys[n - 1][1]
        return None

    panic = first_visible("hash_mismatch_panic")
    measured = first_visible("measured_boot")

    # R9: bodies and image lines.
    labels = [None] * (nlines + 1)          # label of the nearest preceding entry line
    bodies = []
    cur_label = None
    cur_body = None
    for n in range(1, nlines + 1):
        labels[n] = cur_label
        if ents[n - 1]:
            # AMBIGUITY: the docstring does not say whether an EMPTY label (a bare "/" line)
            # replaces the previous label; the literal "nearest preceding entry line" reading is
            # used (the gate's `or entry` fallback is not in the docstring).
            cur_label = entry_label(lines[n - 1])
            labels[n] = cur_label
            cur_body = {"protocol": None, "path": None, "image_path": None}
            bodies.append(cur_body)
        elif cur_body is not None and keys[n - 1] is not None:
            k, v = keys[n - 1]
            if k == "protocol" and cur_body["protocol"] is None:
                cur_body["protocol"] = v
            elif k == "path" and cur_body["path"] is None:
                cur_body["path"] = n
            elif k == "image_path" and cur_body["image_path"] is None:
                cur_body["image_path"] = n

    image_lines = set()
    for b in bodies:
        if b["protocol"] in EFI_PROTOCOLS:
            img = b["path"] if b["path"] is not None else b["image_path"]
            if img is not None:
                image_lines.add(img)

    # R2/R3/R4/R5: pins.
    pins = []
    for n in range(1, nlines + 1):
        kv = keys[n - 1]
        if kv is None or kv[0] not in PIN_KEYS:
            continue
        parts = parse_pin(kv[1])
        if parts is None:
            continue
        resource, root, path, h = parts
        if len(h) != 128 or any(ch not in HEX for ch in h):
            status = "LP-HASH-FORMAT"
        else:
            name = resource[1:] if resource.startswith("$") else resource
            if name not in RESOURCE_NAMES:
                status = "LP-BAD-RESOURCE"
            elif name != "boot" or root != "":
                status = "LP-UNRESOLVED"
            else:
                # AMBIGUITY: R5 has no ESP-containment clause for `..` or a symlink that leaves
                # the root; this literal implementation joins and stats.
                target = os.path.join(esp, path)
                try:
                    st = os.stat(target)
                except OSError:
                    status = "LP-MISSING"
                else:
                    if not stat.S_ISREG(st.st_mode):
                        status = "LP-MISSING"
                    else:
                        try:
                            with open(target, "rb") as f:
                                digest = hashlib.blake2b(f.read()).hexdigest()
                        except OSError:
                            # AMBIGUITY: R5/R7 do not cover a regular file that cannot be read.
                            status = "LP-MISSING"
                        else:
                            status = "OK" if digest == h.lower() else "LP-MISMATCH"
        if status == "OK":
            cons = "none"
        elif status == "LP-UNRESOLVED":
            cons = "not-modelled"
        elif status == "LP-MISSING":
            cons = "panic" if n in image_lines else "not-modelled"
        elif status in ("LP-HASH-FORMAT", "LP-BAD-RESOURCE"):
            cons = "skip" if kv[0] in OPTIONAL_KEYS else "panic"
        else:
            if kv[0] in OPTIONAL_KEYS:
                cons = "skip"
            elif secure_boot:
                cons = "panic"
            elif panic is not None and panic[1].lower() == "no":
                cons = "prompt"
            else:
                cons = "panic"
        pins.append({"line": n, "key": kv[0], "entry": labels[n],
                     "status": status, "consequence": cons})

    # U1: image lines whose value is not a structurally parseable pin.
    unverified = []
    for ln in sorted(image_lines):
        kv = keys[ln - 1]
        if kv is None:
            continue
        if parse_pin(kv[1]) is None:
            unverified.append(ln)
    unverified.sort()

    statuses = {p["status"] for p in pins}
    if statuses & FAULTS:
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0

    requested = (measured is not None and measured[1] == "yes") or secure_boot
    if not requested:
        on_panic = "menu"
    elif tpm is None:
        on_panic = "halt-if-tpm"
    else:
        on_panic = "halt" if tpm == "1" else "menu"

    return {"verdict": verdict, "rc": rc, "on_panic": on_panic,
            "hash_mismatch_panic": None if panic is None else {"line": panic[0], "value": panic[1]},
            "pins": pins, "unverified_image_lines": unverified,
            "limine_version": version, "limine_version_source": source}


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, "%s: error: %s\n" % (self.prog, message))


def main(argv):
    ap = UsageParser(description="docstring-only r93 rule implementation")
    ap.add_argument("--conf")
    ap.add_argument("--esp")
    ap.add_argument("--secure-boot-enforced", choices=("0", "1"))
    ap.add_argument("--tpm-present", choices=("0", "1"))
    ap.add_argument("--limine-version", default="12.9.4")
    a = ap.parse_args(argv)
    version, source = a.limine_version, "flag"
    if version == "auto":
        probed = probe_version()
        if probed is None:
            sys.stderr.write("--limine-version auto: `limine --version` probe failed\n")
            return 64
        version, source = probed, "probe"
    if parse_version(version) is None:
        sys.stderr.write("--limine-version must be X.Y.Z or auto\n")
        return 64
    if not a.conf or not a.esp:
        ap.print_usage(sys.stderr)
        return 64
    r = evaluate(a.conf, a.esp, a.secure_boot_enforced == "1", a.tpm_present, version, source)
    sys.stdout.write(json.dumps(r) + "\n")
    return r["rc"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
