#!/usr/bin/env python3
"""Read-only Limine path-pin gate (tsukuroi rounds 87, 90, 91 and 92; Limine v12.9.4 and v12.9.5+ rules).

Hashes every file a `limine.conf` path pin names and says what Limine will do at boot.
The rule set is frozen in tools/limine-pin-battery-r91.py (R1-R7, R9, R10, V1, U1; the r90 rules
with round-91 additions); sources are the pinned Limine v12.9.4 files in .ufo/waves/round-87/before/src/,
.ufo/waves/round-89/before/src/ and .ufo/waves/round-91/after/src-c2/ (registry S350-S353, S361, S362,
S374-S376). Summary:
  - key lines: after leading blanks, `KEY:`; keys case-insensitive; `#` lines are comments (config.c 778-818);
  - pins: path, kernel_path, image_path, module_path, dtb_path, global_dtb, wallpaper, term_font whose value is
    `[$]resource(root):/path#hash`; the hash is after the LAST `#` (uri.c 28-104);
  - hash: exactly 128 hex characters, either case, else LP-HASH-FORMAT;
  - resource (one leading `$` dropped, case-sensitive): not one of hdd, odd, boot, guid, uuid, fslabel, tftp ->
    LP-BAD-RESOURCE (URI_ERROR "Resource ... not valid", uri.c 344-366; round 90); only `boot()` (empty root)
    resolves, to --esp; any other valid resource is LP-UNRESOLVED, and so is a path that leaves the --esp root
    (`..` or a symlink pointing outside; round-87 hardening, not a Limine rule);
  - BLAKE2b-512 over the raw stored bytes (gzip is not decompressed) -> OK / LP-MISMATCH; absent -> LP-MISSING;
  - consequence: mismatch on wallpaper/term_font -> skip; otherwise panic, unless the FIRST hash_mismatch_panic
    value is `no` (case-insensitive) and Secure Boot is not enforced -> prompt (Y or y continues, any other key
    returns to the menu; uri.c 301-319, menu.c 1711-1717). A bad hash format or a bad resource panics (skip for
    wallpaper/font). LP-MISSING on the image line of an efi chainload entry panics ("efi: Failed to open
    image", chainload.c 414-435; round 90): the entry's FIRST `protocol` key line is exactly efi, uefi or
    efi_chainload (menu.c 2429-2468), and the image line is its FIRST `path` key line, else its FIRST
    `image_path` key line (an entry's body runs to the next `/` line, config.c 686-720). Any other LP-MISSING
    and every LP-UNRESOLVED stay `not-modelled`;
  - on_panic (round 90; menu.c 1719-1728, panic.s2.c 24-28, 70-78, 98): measured boot is requested when the
    FIRST measured_boot key line says exactly `yes` (case-sensitive) or Secure Boot is enforced; not requested
    -> "menu" (a panic returns to the menu after a key press); requested and --tpm-present 1 -> "halt"
    ("System halted."), --tpm-present 0 -> "menu", flag absent -> "halt-if-tpm". `--live` never guesses the
    firmware TPM: /sys/class/tpm is a Linux-side signal only (corpus/knowledge/limine-uri-failure-r89.md UF8).
  - hash_mismatch_panic and measured_boot are read only from the global section (lines before the first
    `/` entry line) UNLESS line 1 is itself an entry line (config.c 642-650: the buffer cut is skipped when
    `c == config_addr`, i.e. no bytes precede the first `/`; round 91 V1). An entry body's hash_mismatch_panic
    or measured_boot is invisible to config_get_value.
  - which visibility rule applies is selected by `--limine-version` (round 92 V2; default 12.9.4, the host
    package): BEFORE 12.9.5 the r91 rule above holds; FROM 12.9.5 on, `create_menu_tree()` parses in place
    and NUL-terminates the buffer at the end of the first entry's label line (v12.9.6 raw 328-330 cuts
    before the first entry line, raw 362-365 NULs the end of its label), so the first-line exception is
    GONE: when line 1 is an entry line the global section is empty and both keys are invisible. The reads
    run after the tree build (v12.9.4 raw 638-650; v12.9.6 raw 666-668 `config_ready`/`create_menu_tree`,
    reads at raw 733+). An unknown or malformed version is a usage error (rc 64), never a silent default.
  - `auto` is the DEFAULT (round 94 V4; r93 V3 made it opt-in): `--limine-version` defaults to `auto`
    and `--live` probes the installed `limine --version` unless an explicit `X.Y.Z` is given: it runs
    `limine --version` read-only (PATH lookup, 5 s timeout), accepts the first `X.Y.Z` immediately
    following `limine` (case-insensitive, optional `v`, with a not-word-char suffix guard so `12.9.6-rc1`
    and `12.9.6.1` are probe failures), and selects the era from that value; the JSON records the
    resolved `limine_version` and `limine_version_source: "probe"`. A failed probe (binary absent,
    nonzero exit, no parsable version, timeout, suffixed or extra-component answer) is a usage error
    (rc 64, no verdict), never a silent default: a host whose bootloader cannot be identified must not
    be answered with another release's rule.
  - unverified_image_lines (round 91 U1): the image line of an efi chainload entry whose value is not a
    pin URI (`boot():/path#hash` shape) is reported as a line-number list. uri_resolve returns false with no
    message for a value with no `(`, no `):/`, or no `#` after `):/`, and uri_open returns NULL; chainload
    panics "Failed to open image" (uri.c 32-107, 335-336; chainload.c 414-435; registry S374, S375).

Usage:
  check-limine-pins.py --conf FILE --esp DIR [--secure-boot-enforced 0|1] [--tpm-present 0|1]
                       [--limine-version X.Y.Z|auto]
  sudo check-limine-pins.py --live --limine-version auto
                                              # /boot/limine.conf, ESP /boot, Secure Boot from efivars,
                                              # era from the installed `limine --version`
  check-limine-pins.py --selftest
Output: one JSON object on stdout {verdict, rc, on_panic, pins[{line, key, entry, uri, status, consequence, ...}],
...}.
Exit: 0 HEALTHY; 1 DEGRADED (a pin mismatches, is missing, is malformed or names an invalid resource);
2 CANNOT-EVALUATE (conf unreadable, or a pin that cannot be resolved here); 64 usage.
Never writes: opens files read-only, no temp files outside --selftest's own mkdtemp (honours TMPDIR).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import string
import subprocess
import sys
import tempfile

PIN_KEYS = frozenset({"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
                      "wallpaper", "term_font"})
OPTIONAL_KEYS = frozenset({"wallpaper", "term_font"})
HEXDIGITS = frozenset(string.hexdigits)
KEYCHARS = frozenset(string.ascii_letters + "_")
SB_VAR = "/sys/firmware/efi/efivars/SecureBoot-8be4df61-93ca-11d2-aa0d-00e098032b8c"
FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE")
RESOURCES = frozenset({"hdd", "odd", "boot", "guid", "uuid", "fslabel", "tftp"})
EFI_PROTOCOLS = frozenset({"efi", "uefi", "efi_chainload"})


def parse_limine_version(text):
    """V2: `X.Y.Z`, ASCII digits only (1-9 digits per component; leading zeros are accepted and
    normalized by int(), e.g. `12.09.4` == `12.9.4`), -> (X, Y, Z); anything else -> None (usage
    error, rc 64). A component longer than 9 digits is refused rather than handed to int(), which
    raises above 4300 digits (round-92 ReviewGate F1)."""
    if not isinstance(text, str):
        return None
    parts = text.split(".")
    if len(parts) != 3 or not all(p.isascii() and p.isdigit() for p in parts):  # M05 no digit-count bound
        return None
    return tuple(int(p) for p in parts)


VISIBILITY_ERA_SPLIT = (12, 9, 5)   # first upstream release with the create_menu_tree() cut


def probe_limine_version(executable="limine"):
    """V3 (round 93), hardened V4 (round 94): the installed bootloader's version, read-only.

    Runs `<executable> --version` (PATH lookup by default; the caller may name a path) with a 5 s
    timeout and returns the first `X.Y.Z` immediately following `limine` (case-insensitive, optional
    `v`, and a not-word-char suffix guard so `12.9.6-rc1` or `12.9.6.1` are probe failures, not 12.9.6),
    or None when the binary is absent, exits nonzero, times out or prints no parsable version. Nothing
    is written; the probe reads stdout only. `limine --version` on this host prints `Limine 12.9.4`."""
    try:
        p = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    if p.returncode != 0:
        return None
    m = re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)(?![\w.-])", p.stdout)
    return m.group(1) if m else None


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


def sanitize(s):
    """Make a possibly surrogate-escaped string safe for UTF-8 stdout/JSON."""
    return s.encode("utf-8", "replace").decode("utf-8")


def resolve_in_esp(esp, path):
    """Join a URI path under esp; return None if it leaves the ESP (`..` components or a
    symlink pointing outside). Limine resolves the path on the boot volume only."""
    target = os.path.join(esp, *path.split("/"))
    root = os.path.realpath(esp)
    resolved = os.path.realpath(target)
    if resolved != root and not resolved.startswith(root + os.sep):
        return None
    return target


def on_panic_of(measured_setting, secure_boot, tpm):
    """menu.c 1719-1728: requested by `measured_boot: yes` (strcmp) or Secure Boot; forced off without a TPM."""
    requested = (measured_setting is not None and measured_setting[1] == "yes") or secure_boot
    if not requested:
        return "menu"
    if tpm is None:
        return "halt-if-tpm"
    return "halt" if tpm else "menu"


def check(conf, esp, secure_boot, tpm=None, limine_version="12.9.4", limine_version_source="flag"):
    if isinstance(tpm, str):                      # the CLI's spelling, normalised once (ReviewGate F4)
        tpm = tpm == "1"
    version = parse_limine_version(limine_version)
    if version is None:
        raise ValueError("bad limine version: %r" % (limine_version,))
    era_b = version >= VISIBILITY_ERA_SPLIT
    try:
        with open(conf, "rb") as f:
            text = f.read().decode("utf-8", "surrogateescape")
    except OSError as e:
        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "on_panic": None,
                "unverified_image_lines": [],
                "limine_version": limine_version,
                "limine_version_source": limine_version_source,
                "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",
                "error": "conf unreadable: %s" % sanitize(str(e))}
    panic_setting = None
    measured_setting = None
    entry = None
    body = None          # the current entry's first protocol/path/image_path key lines
    bodies = []
    raw_pins = []
    # V1 (r91; config.c raw 642-650) and V2 (r92; v12.9.6 raw 328-330, 362-365): the config buffer is
    # cut at the first entry line. Before 12.9.5 the cut is skipped when that '/'-line is also the file's
    # first physical line (guard `c > config_addr`) and the whole file stays visible; from 12.9.5 on,
    # create_menu_tree() parses in place and NUL-terminates at the first entry's label end, so there is
    # no exception: when line 1 is an entry line the global section is empty.
    lines = text.split("\n")
    first_entry = None
    for i, raw in enumerate(lines, 1):
        if raw.replace("\r", "").strip(" \t").startswith("/"):
            first_entry = i
            break
    in_global = True
    for lineno, raw in enumerate(lines, 1):
        stripped = raw.replace("\r", "").strip(" \t")
        if stripped.startswith("/"):
            if first_entry is not None and lineno == first_entry and (era_b or first_entry != 1):
                in_global = False
            entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry
            body = {}
            bodies.append(body)
            continue
        kv = split_key(raw)
        if kv is None:
            continue
        key, written, value = kv
        if in_global and key == "hash_mismatch_panic" and panic_setting is None:
            panic_setting = (lineno, value)
        if in_global and key == "measured_boot" and measured_setting is None:
            measured_setting = (lineno, value)
        if body is not None and key in ("protocol", "path", "image_path") and key not in body:
            body[key] = value if key == "protocol" else lineno
        if key in PIN_KEYS:
            uri = parse_uri(value)
            if uri is not None:
                raw_pins.append((lineno, key, written, entry, value, uri))
    image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}
    image_lines.discard(None)
    # U1 (r91): an image line whose value Limine still uri_opens but which is not a parseable pin
    # (no '(', no '):/', empty path, or no '#' after '):/') is reported, sorted, in
    # unverified_image_lines. It changes no pin verdict.
    unverified = []
    for img_ln in sorted(image_lines):
        kv = split_key(lines[img_ln - 1])
        if kv is None:
            continue
        if parse_uri(kv[2]) is None:
            unverified.append(img_ln)
    unverified.sort()
    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)
    pins = []
    for lineno, key, written, entry_name, value, uri in raw_pins:
        rec = {"line": lineno, "key": written, "entry": entry_name, "uri": sanitize(value)}
        optional = key in OPTIONAL_KEYS
        h = uri["hash"]
        if len(h) != 128 or not set(h) <= HEXDIGITS:
            rec.update(status="LP-HASH-FORMAT", consequence="skip" if optional else "panic",
                       detail="hash must be 128 hex characters (got %d)" % len(h))
            pins.append(rec)
            continue
        resource = uri["resource"][1:] if uri["resource"].startswith("$") else uri["resource"]
        if resource not in RESOURCES:
            rec.update(status="LP-BAD-RESOURCE", consequence="skip" if optional else "panic",
                       detail="resource `%s` is not valid (uri.c 364)" % sanitize(resource))
            pins.append(rec)
            continue
        if resource != "boot" or uri["root"] != "":
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled",
                       detail="resource %s(%s) is not the boot partition" % (resource, uri["root"]))
            pins.append(rec)
            continue
        target = resolve_in_esp(esp, uri["path"])
        if target is None:
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled",
                       detail="path escapes the ESP root")
            pins.append(rec)
            continue
        rec["file"] = sanitize(target)
        if not os.path.isfile(target):
            if lineno in image_lines:
                rec.update(status="LP-MISSING", consequence="panic",
                           detail="image of an efi chainload entry: efi: Failed to open image (chainload.c 435)")
            else:
                rec.update(status="LP-MISSING", consequence="not-modelled")
            pins.append(rec)
            continue
        try:
            got = blake2b_file(target)
        except OSError as e:
            rec.update(status="LP-UNRESOLVED", consequence="not-modelled", detail="unreadable: %s" % sanitize(str(e)))
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
    if statuses & set(FAULTS):
        verdict, rc = "DEGRADED", 1
    elif "LP-UNRESOLVED" in statuses:
        verdict, rc = "CANNOT-EVALUATE", 2
    else:
        verdict, rc = "HEALTHY", 0
    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,
            "limine_version": limine_version,
            "limine_version_source": limine_version_source,
            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",
            "hash_mismatch_panic": None if panic_setting is None else
            {"line": panic_setting[0], "value": sanitize(panic_setting[1])},
            "measured_boot": None if measured_setting is None else
            {"line": measured_setting[0], "value": sanitize(measured_setting[1])},
            "tpm_present": tpm, "on_panic": on_panic_of(measured_setting, secure_boot, tpm),
            "secure_boot_enforced": secure_boot, "pins": pins,
            "unverified_image_lines": unverified,
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

        def case(name, lines, sb, want_rc, want, tpm=None, want_op=None, ver=None, want_unv=None,
                 want_era=None):
            conf = os.path.join(work, name + ".conf")
            with open(conf, "w", newline="") as f:
                f.write("\n".join(lines) + "\n")
            r = check(conf, esp, sb, tpm, **({} if ver is None else {"limine_version": ver}))
            got = [(p["line"], p["status"], p["consequence"]) for p in r["pins"]]
            ok = (r["rc"] == want_rc and got == want and (want_op is None or r["on_panic"] == want_op)
                  and (want_unv is None or r["unverified_image_lines"] == want_unv)
                  and (want_era is None or r["visibility_era"] == want_era))
            results.append((name, ok, r["rc"], got + [("on_panic", r["on_panic"]),
                                                      ("unv", r["unverified_image_lines"])]))

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
        case("traversal", ["/e", "path: boot():/../outside#" + ha], False, 2,
             [(2, "LP-UNRESOLVED", "not-modelled")])
        # round 90: R4 bad resource, R9 efi image line, R10 on_panic
        case("efi-image-missing", ["/e", "protocol: efi", "path: boot():/EFI/Linux/zz.efi#" + ha], False, 1,
             [(3, "LP-MISSING", "panic")], want_op="menu")
        case("image-path-shadowed", ["/e", "protocol: uefi", "image_path: boot():/EFI/Linux/zz.efi#" + ha,
                                     "path: boot():/EFI/Linux/a.efi#" + ha], False, 1,
             [(3, "LP-MISSING", "not-modelled"), (4, "OK", "none")])
        case("linux-missing", ["/e", "protocol: linux", "path: boot():/EFI/Linux/zz.efi#" + ha], False, 1,
             [(3, "LP-MISSING", "not-modelled")])
        case("protocol-case", ["/e", "protocol: EFI", "path: boot():/EFI/Linux/zz.efi#" + ha], False, 1,
             [(3, "LP-MISSING", "not-modelled")])
        case("bad-resource", ["/e", "protocol: efi", "path: $Boot():/EFI/Linux/a.efi#" + ha], False, 1,
             [(3, "LP-BAD-RESOURCE", "panic")])
        case("bad-resource-font", ["term_font: bootx():/EFI/Linux/a.efi#" + ha], False, 1,
             [(1, "LP-BAD-RESOURCE", "skip")])
        case("measured-halt", ["measured_boot: yes", "/e", "protocol: efi", "path: boot():/EFI/Linux/zz.efi#" + ha],
             False, 1, [(4, "LP-MISSING", "panic")], tpm=True, want_op="halt")
        case("measured-no-tpm", ["measured_boot: yes", "/e", "protocol: efi", "path: boot():/EFI/Linux/a.efi#" + ha],
             False, 0, [(4, "OK", "none")], tpm=False, want_op="menu")
        case("measured-unknown-tpm", ["/e", "protocol: efi", "path: boot():/EFI/Linux/a.efi#" + ha],
             True, 0, [(3, "OK", "none")], want_op="halt-if-tpm")
        case("measured-case", ["measured_boot: Yes", "/e", "path: boot():/EFI/Linux/a.efi#" + ha],
             False, 0, [(3, "OK", "none")], tpm=True, want_op="menu")
        # round 91 V1/U1 coverage: global-section scoping and the unverified-image list
        case("v1-entry-body", ["hash_mismatch_panic: no", "/e", "protocol: efi",
                               "path: boot():/EFI/Linux/a.efi#" + bad], False, 1,
             [(4, "LP-MISMATCH", "prompt")], want_unv=[])
        case("v1-body-invisible", ["timeout: 5", "/e", "protocol: efi",
                                   "path: boot():/EFI/Linux/a.efi#" + bad,
                                   "hash_mismatch_panic: no"], False, 1,
             [(4, "LP-MISMATCH", "panic")], want_unv=[])
        case("v1-body-invisible-era-b", ["timeout: 5", "/e", "protocol: efi",
                                         "path: boot():/EFI/Linux/a.efi#" + bad,
                                         "hash_mismatch_panic: no"], False, 1,
             [(4, "LP-MISMATCH", "panic")], ver="12.9.6", want_era="12.9.5+")
        case("u1-unverified", ["/e", "protocol: efi", "path: /EFI/Linux/a.efi"], False, 0, [],
             want_unv=[3])
        case("u1-pin-not-listed", ["/e", "protocol: efi", "path: boot():/EFI/Linux/a.efi#" + bad],
             False, 1, [(3, "LP-MISMATCH", "panic")], want_unv=[])
        # round 92 V2: the first-line-is-entry visibility flip at 12.9.5
        first_entry = ["/e", "protocol: efi", "path: boot():/EFI/Linux/a.efi#" + bad,
                       "hash_mismatch_panic: no"]
        case("era-a-first-entry", first_entry, False, 1, [(3, "LP-MISMATCH", "prompt")], ver="12.9.4",
             want_era="pre-12.9.5")
        case("era-b-first-entry", first_entry, False, 1, [(3, "LP-MISMATCH", "panic")], ver="12.9.6",
             want_era="12.9.5+")
        case("era-b-global-key", ["hash_mismatch_panic: no", "/e", "protocol: efi",
                                  "path: boot():/EFI/Linux/a.efi#" + bad], False, 1,
             [(4, "LP-MISMATCH", "prompt")], ver="12.9.5", want_era="12.9.5+")
        case("era-default", first_entry, False, 1, [(3, "LP-MISMATCH", "prompt")])
        measured_first = ["/e", "protocol: efi", "path: boot():/EFI/Linux/a.efi#" + ha,
                          "measured_boot: yes"]
        case("era-a-measured", measured_first, False, 0, [(3, "OK", "none")], tpm=True,
             want_op="halt", ver="12.9.4")
        case("era-b-measured", measured_first, False, 0, [(3, "OK", "none")], tpm=True,
             want_op="menu", ver="12.9.6")
        results.append(("version-parser",
                        parse_limine_version("12.9.4") == (12, 9, 4)
                        and parse_limine_version("12.9.6") > VISIBILITY_ERA_SPLIT
                        and parse_limine_version("12.9") is None
                        and parse_limine_version("12.9.x") is None
                        and parse_limine_version("") is None
                        and parse_limine_version("12.09.4") == (12, 9, 4)
                        and parse_limine_version("9" * 5000 + ".0.0") is None,
                        "-", []))
        # round 93 V3: the installed-version probe and the exact 12.9.5 boundary
        case("era-exact-first-entry", first_entry, False, 1, [(3, "LP-MISMATCH", "panic")],
             ver="12.9.5", want_era="12.9.5+")
        probe_dir = os.path.join(work, "probe-bin")
        os.makedirs(probe_dir)
        fake = os.path.join(probe_dir, "limine")

        def fake_probe(body):
            with open(fake, "w") as f:
                f.write("#!/bin/sh\n%s\n" % body)
            os.chmod(fake, 0o755)
            return probe_limine_version(fake)

        results.append(("probe-version",
                        fake_probe('echo "Limine 12.9.6"') == "12.9.6"
                        and fake_probe('echo "Limine 12.9.4"; echo "BSD-2-Clause"') == "12.9.4"
                        and fake_probe("exit 1") is None
                        and fake_probe('echo "no version here"') is None
                        and probe_limine_version(os.path.join(probe_dir, "absent")) is None
                        and fake_probe('echo "Limine 12.9.6-rc1"') is None
                        and fake_probe('echo "Limine 12.9.6.1"') is None
                        and fake_probe('echo "Limine 12.9.6" >&2') is None
                        and fake_probe('echo "12.9.6"') is None,
                        "-", []))
        r = check(os.path.join(work, "absent.conf"), esp, False)
        results.append(("conf-absent", r["rc"] == 2 and r["pins"] == [], r["rc"], r["pins"]))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    for name, ok, rc, got in results:
        print("%-16s %s rc=%s %s" % (name, "PASS" if ok else "FAIL", rc, got))
    passed = sum(1 for r in results if r[1])
    print("selftest %s %d/%d" % ("PASS" if passed == len(results) else "FAIL", passed, len(results)))
    return 0 if passed == len(results) else 1


class UsageParser(argparse.ArgumentParser):
    """argparse's default error exit is 2, which collides with CANNOT-EVALUATE rc 2; usage is 64."""

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(64, "%s: error: %s\n" % (self.prog, message))


def main():
    ap = UsageParser(description="Read-only Limine v12.9.4 / v12.9.5+ path-pin gate.")
    ap.add_argument("--conf")
    ap.add_argument("--esp")
    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)
    ap.add_argument("--tpm-present", choices=("0", "1"), default=None)
    ap.add_argument("--limine-version", default="auto",
                    help="X.Y.Z, or `auto` to probe `limine --version` (round 93 V3; the round-94 default)")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    version, version_source = a.limine_version, "flag"
    if version == "auto":
        probed = probe_limine_version()
        if probed is None:
            ap.print_usage(sys.stderr)
            print("check-limine-pins: --limine-version auto: `limine --version` probe failed",
                  file=sys.stderr)
            return 64
        version, version_source = probed, "probe"
    if parse_limine_version(version) is None:
        ap.print_usage(sys.stderr)
        print("check-limine-pins: --limine-version must be X.Y.Z or auto", file=sys.stderr)
        return 64
    tpm = None if a.tpm_present is None else a.tpm_present == "1"
    if a.live:
        conf, esp = a.conf or "/boot/limine.conf", a.esp or "/boot"
        sb = live_secure_boot() if a.secure_boot_enforced is None else a.secure_boot_enforced == "1"
        r = check(conf, esp, bool(sb), tpm, version, version_source)
        r["secure_boot_source"] = "efivar" if a.secure_boot_enforced is None else "argument"
        if sb is None:
            r["secure_boot_source"] = "efivar unreadable; treated as not enforced"
    elif a.conf and a.esp:
        r = check(a.conf, a.esp, a.secure_boot_enforced == "1", tpm, version, version_source)
    else:
        ap.print_usage(sys.stderr)
        return 64
    print(json.dumps(r, sort_keys=True))
    return r["rc"]


if __name__ == "__main__":
    sys.exit(main())
