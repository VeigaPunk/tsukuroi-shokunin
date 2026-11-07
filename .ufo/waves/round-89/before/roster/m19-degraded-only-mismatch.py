#!/usr/bin/env python3
"""Read-only Limine path-pin gate (tsukuroi round 87; Limine v12.9.4 rules).

Hashes every file a `limine.conf` path pin names and says what Limine will do at boot.
The rule set is frozen in tools/limine-pin-battery-r87.py (R1-R7); sources are the pinned Limine v12.9.4
files in .ufo/waves/round-87/before/src/ (registry S350-S353). Summary:
  - key lines: after leading blanks, `KEY:`; keys case-insensitive; `#` lines are comments (config.c 778-818);
  - pins: path, kernel_path, image_path, module_path, dtb_path, global_dtb, wallpaper, term_font whose value is
    `[$]resource(root):/path#hash`; the hash is after the LAST `#` (uri.c 28-104);
  - hash: exactly 128 hex characters, either case, else LP-HASH-FORMAT;
  - only `boot()` (empty root) resolves, to --esp; anything else is LP-UNRESOLVED;
  - BLAKE2b-512 over the raw stored bytes (gzip is not decompressed) -> OK / LP-MISMATCH; absent -> LP-MISSING;
  - consequence: mismatch on wallpaper/term_font -> skip; otherwise panic, unless the FIRST hash_mismatch_panic
    value is `no` (case-insensitive) and Secure Boot is not enforced -> prompt (Y continues, any other key
    returns to the menu; uri.c 301-319, menu.c 1711-1717). A bad hash format panics (skip for wallpaper/font).

Usage:
  check-limine-pins.py --conf FILE --esp DIR [--secure-boot-enforced 0|1]
  sudo check-limine-pins.py --live            # /boot/limine.conf, ESP /boot, Secure Boot from efivars
  check-limine-pins.py --selftest
Output: one JSON object on stdout {verdict, rc, pins[{line, key, entry, uri, status, consequence, ...}], ...}.
Exit: 0 HEALTHY; 1 DEGRADED (a pin mismatches, is missing, or is malformed); 2 CANNOT-EVALUATE (conf unreadable,
or a pin that cannot be resolved here); 64 usage.
Never writes: opens files read-only, no temp files outside --selftest's own mkdtemp (honours TMPDIR).
"""
import argparse
import hashlib
import json
import os
import shutil
import string
import sys
import tempfile

PIN_KEYS = frozenset({"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
                      "wallpaper", "term_font"})
OPTIONAL_KEYS = frozenset({"wallpaper", "term_font"})
HEXDIGITS = frozenset(string.hexdigits)
KEYCHARS = frozenset(string.ascii_letters + "_")
SB_VAR = "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT")


def split_key(raw):
    """Return (key_lower, key_as_written, value) for a key line, else None."""
    line = raw.replace("\r", "").strip(" \t")
    if not line or line[0] == "#":
        return None
    i = 0
    while i < len(line) and line[i] in KEYCHARS:
        i += 1
    if i == 0 or i >= len(line) or line[i] != ":":
        return None
    return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \t")


def parse_uri(value):
    """Limine uri_resolve: resource up to the first '(', root up to the first '):/', hash after the last '#'."""
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
    return {"resource": value[:lp], "root": value[lp + 1:rp], "path": tail[:cut], "hash": tail[cut + 1:]}


def blake2b_file(path):
    h = hashlib.blake2b()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check(conf, esp, secure_boot):
    try:
        with open(conf, "rb") as f:
            text = f.read().decode("utf-8", "replace")
    except OSError as e:
        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "error": "conf unreadable: %s" % e}
    panic_setting = None
    entry = None
    raw_pins = []
    for lineno, raw in enumerate(text.split("\n"), 1):
        stripped = raw.replace("\r", "").strip(" \t")
        if stripped.startswith("/"):
            entry = stripped.lstrip("/").lstrip("+").strip() or entry
            continue
        kv = split_key(raw)
        if kv is None:
            continue
        key, written, value = kv
        if key == "hash_mismatch_panic" and panic_setting is None:
            panic_setting = (lineno, value)
        if key in PIN_KEYS:
            uri = parse_uri(value)
            if uri is not None:
                raw_pins.append((lineno, key, written, entry, value, uri))
    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)
    pins = []
    for lineno, key, written, entry_name, value, uri in raw_pins:
        rec = {"line": lineno, "key": written, "entry": entry_name, "uri": value}
        optional = key in OPTIONAL_KEYS
        h = uri["hash"]
        if len(h) != 128 or not set(h) <= HEXDIGITS:
            rec.update(status="LP-HASH-FORMAT", consequence="skip" if optional else "panic",
                       detail="hash must be 128 hex characters (got %d)" % len(h))
            pins.append(rec)
            continue
        resource = uri["resource"][1:] if uri["resource"].startswith("$") else uri["resource"]
        if resource != "boot" or uri["root"] != "":
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled",
                       detail="resource %s(%s) is not the boot partition" % (resource, uri["root"]))
            pins.append(rec)
            continue
        target = os.path.join(esp, *uri["path"].split("/"))
        rec["file"] = target
        if not os.path.isfile(target):
            rec.update(status="LP-MISSING", consequence="not-modelled")
            pins.append(rec)
            continue
        try:
            got = blake2b_file(target)
        except OSError as e:
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled", detail="unreadable: %s" % e)
            pins.append(rec)
            continue
        rec["blake2b"] = got
        if got == h.lower():
            rec.update(status="OK", consequence="none")
        else:
            rec.update(status="LP-MISMATCH",
                       consequence="skip" if optional else ("prompt" if prompt else "panic"))
        pins.append(rec)
    statuses = {p["status"] for p in pins}
    if "LP-MISMATCH" in statuses:
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0
    return {"schema": "tsukuroi-limine-pins-v1", "verdict": verdict, "rc": rc,
            "hash_mismatch_panic": None if panic_setting is None else
            {"line": panic_setting[0], "value": panic_setting[1]},
            "secure_boot_enforced": secure_boot, "pins": pins,
            "findings": sorted("%s line %d" % (p["status"], p["line"]) for p in pins if p["status"] != "OK")}


def live_secure_boot():
    """SecureBoot efivar: 4 attribute bytes then 1 data byte. Enrolled config hash is not visible here, so an
    enabled Secure Boot is reported as enforced (the stricter reading)."""
    try:
        with open(SB_VAR, "rb") as f:
            data = f.read()
    except OSError:
        return None
    return len(data) >= 5 and data[4] == 1


def selftest():
    work = tempfile.mkdtemp(prefix="limine-pins-selftest-")
    results = []
    try:
        esp = os.path.join(work, "esp")
        os.makedirs(os.path.join(esp, "EFI", "Linux"))
        good = os.path.join(esp, "EFI", "Linux", "a.efi")
        with open(good, "wb") as f:
            f.write(b"kernel-a")
        ha = hashlib.blake2b(b"kernel-a").hexdigest()
        bad = ha[:-1] + ("0" if ha[-1] != "0" else "1")

        def case(name, lines, sb, want_rc, want):
            conf = os.path.join(work, name + ".conf")
            with open(conf, "w", newline="") as f:
                f.write("\n".join(lines) + "\n")
            r = check(conf, esp, sb)
            got = [(p["line"], p["status"], p["consequence"]) for p in r["pins"]]
            results.append((name, r["rc"] == want_rc and got == want, r["rc"], got))

        case("ok", ["/e", "path: boot():/EFI/Linux/a.efi#" + ha], False, 0, [(2, "OK", "none")])
        case("upper", ["/e", "PATH: boot():/EFI/Linux/a.efi#" + ha.upper()], False, 0, [(2, "OK", "none")])
        case("mismatch-panic", ["/e", "path: boot():/EFI/Linux/a.efi#" + bad], False, 1,
             [(2, "LP-MISMATCH", "panic")])
        case("mismatch-prompt", ["hash_mismatch_panic: No", "/e", "  path: boot():/EFI/Linux/a.efi#" + bad],
             False, 1, [(3, "LP-MISMATCH", "prompt")])
        case("first-setting", ["hash_mismatch_panic: yes", "/e", "hash_mismatch_panic: no",
                               "path: boot():/EFI/Linux/a.efi#" + bad], False, 1, [(4, "LP-MISMATCH", "panic")])
        case("secureboot", ["hash_mismatch_panic: no", "/e", "path: boot():/EFI/Linux/a.efi#" + bad],
             True, 1, [(3, "LP-MISMATCH", "panic")])
        case("comment", ["#path: boot():/EFI/Linux/a.efi#" + bad, "/e", "path: boot():/EFI/Linux/a.efi#" + ha],
             False, 0, [(3, "OK", "none")])
        case("missing", ["/e", "path: boot():/EFI/Linux/zz.efi#" + ha], False, 1,
             [(2, "LP-MISSING", "not-modelled")])
        case("format", ["/e", "path: boot():/EFI/Linux/a.efi#" + ha[:64]], False, 1,
             [(2, "LP-HASH-FORMAT", "panic")])
        case("unresolved", ["/e", "path: guid(1234):/EFI/Linux/a.efi#" + ha], False, 2,
             [(2, "LP-UNRESOLVED", "not-modelled")])
        case("wallpaper-skip", ["wallpaper: boot():/EFI/Linux/a.efi#" + bad], False, 1,
             [(1, "LP-MISMATCH", "skip")])
        case("non-path-key", ["/e", "cmdline: x=boot():/EFI/Linux/a.efi#" + bad], False, 0, [])
        case("crlf-blanks", ["/e\r", "\t path:\tboot():/EFI/Linux/a.efi#" + ha + " \t\r"], False, 0,
             [(2, "OK", "none")])
        r = check(os.path.join(work, "absent.conf"), esp, False)
        results.append(("conf-absent", r["rc"] == 2 and r["pins"] == [], r["rc"], r["pins"]))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    for name, ok, rc, got in results:
        print("%-16s %s rc=%s %s" % (name, "PASS" if ok else "FAIL", rc, got))
    passed = sum(1 for r in results if r[1])
    print("selftest %s %d/%d" % ("PASS" if passed == len(results) else "FAIL", passed, len(results)))
    return 0 if passed == len(results) else 1


def main():
    ap = argparse.ArgumentParser(description="Read-only Limine v12.9.4 path-pin gate.")
    ap.add_argument("--conf")
    ap.add_argument("--esp")
    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.live:
        conf, esp = a.conf or "/boot/limine.conf", a.esp or "/boot"
        sb = live_secure_boot() if a.secure_boot_enforced is None else a.secure_boot_enforced == "1"
        r = check(conf, esp, bool(sb))
        r["secure_boot_source"] = "efivar" if a.secure_boot_enforced is None else "argument"
        if sb is None:
            r["secure_boot_source"] = "efivar unreadable; treated as not enforced"
    elif a.conf and a.esp:
        r = check(a.conf, a.esp, a.secure_boot_enforced == "1")
    else:
        ap.print_usage(sys.stderr)
        return 64
    print(json.dumps(r, sort_keys=True))
    return r["rc"]


if __name__ == "__main__":
    sys.exit(main())
