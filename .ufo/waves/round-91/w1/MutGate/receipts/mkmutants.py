#!/usr/bin/env python3
"""Build single-point mutants of the r91 candidate gate and run the frozen r91 battery on each.

Every mutant: exactly one textual substitution on pristine gate bytes, asserted to match once.
Battery: tools/limine-pin-battery-r91.py --gate <mutant> --runs 3 --work <dir>.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
CANON = os.path.join(S, "canon-frozen.py")
BATTERY = os.path.join(LANE, "tools/limine-pin-battery-r91.py")
OUT = os.path.join(S, "mutants")

# (name, clause, old, new, expectation)
MUTANTS = [
    # ---- V1: global-section visibility of hash_mismatch_panic / measured_boot ----
    ("V1a-entry-scan-needs-double-slash", "V1 entry-line detection",
     '        if raw.replace("\\r", "").strip(" \\t").startswith("/"):\n            first_entry = i',
     '        if raw.replace("\\r", "").strip(" \\t").startswith("//"):\n            first_entry = i',
     "killed: PANIC-AFTER-PIN/MEASURED-IN-ENTRY/GLOBAL-VS-ENTRY (no cut at all)"),
    ("V1b-entry-scan-no-break", "V1 first entry line = last '/' line",
     '            first_entry = i\n            break',
     '            first_entry = i',
     "killed: global section stretches to the last entry, body keys become visible"),
    ("V1c-flip-lag-one-line", "V1 global section ends before first entry",
     '            if first_entry is not None and lineno == first_entry and first_entry != 1:\n                in_global = False',
     '            if first_entry is not None and lineno == first_entry + 1 and first_entry != 1:\n                in_global = False',
     "killed: first entry body stays visible, MEASURED-IN-ENTRY/PANIC-AFTER-PIN"),
    ("V1d-firstline-exception-line2", "V1 first-line-is-entry exception guard",
     '            if first_entry is not None and lineno == first_entry and first_entry != 1:',
     '            if first_entry is not None and lineno == first_entry and first_entry not in (1, 2):',
     "killed (probabilistic): first entry on line 2 keeps whole file visible"),
    ("V1e-panic-last-wins", "V1/R6 first visible hash_mismatch_panic wins",
     '        if in_global and key == "hash_mismatch_panic" and panic_setting is None:',
     '        if in_global and key == "hash_mismatch_panic":',
     "survivor expected: no family writes two visible panic keys"),
    ("V1f-panic-value-strip", "R6 panic value compared after rstrip",
     '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)',
     '    prompt = (panic_setting is not None and panic_setting[1].strip().lower() == "no" and not secure_boot)',
     "killed: PANIC-VALUE-BLANKS (trailing blanks must keep panic)"),
    ("V1g-measured-value-strip", "R10 measured_boot value compared after rstrip",
     '    requested = (measured_setting is not None and measured_setting[1] == "yes") or secure_boot',
     '    requested = (measured_setting is not None and measured_setting[1].strip() == "yes") or secure_boot',
     "survivor expected: no measured_boot trailing-blank family"),
    ("V1h-measured-value-lower", "R10 measured_boot strcmp is case-sensitive",
     '    requested = (measured_setting is not None and measured_setting[1] == "yes") or secure_boot',
     '    requested = (measured_setting is not None and measured_setting[1].lower() == "yes") or secure_boot',
     "killed: MEASURED-VALUE-CASE (Yes/YES must not request)"),
    ("V1i-tpm0-as-absent", "R10 --tpm-present 0 forces menu",
     '    return "halt" if tpm else "menu"',
     '    return "halt" if tpm is not None else "menu"',
     "killed: MEASURED-TPM0"),
    ("V1j-tpm-absent-menu", "R10 flag absent -> halt-if-tpm",
     '    if tpm is None:\n        return "halt-if-tpm"',
     '    if tpm is None:\n        return "menu"',
     "killed: MEASURED-TPM-ABSENT"),
    ("V1k-secboot-dropped-onpanic", "R10 Secure Boot requests measured boot",
     '    requested = (measured_setting is not None and measured_setting[1] == "yes") or secure_boot',
     '    requested = (measured_setting is not None and measured_setting[1] == "yes")',
     "killed: MEASURED-SB (sb=1, tpm=1 must halt)"),
    ("V1l-secboot-dropped-prompt", "R6 Secure Boot suppresses prompt",
     '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no" and not secure_boot)',
     '    prompt = (panic_setting is not None and panic_setting[1].lower() == "no")',
     "killed: SECUREBOOT (sb=1 mismatch must panic)"),
    # ---- U1: unverified_image_lines ----
    ("U1a-image-path-precedence", "U1/R9 image line = first path else first image_path",
     '    image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}',
     '    image_lines = {b.get("image_path", b.get("path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}',
     "killed: PATH-PRECEDENCE/FIRST-PATH/UNVERIFIED-IMAGE-PATH"),
    ("U1b-empty-path-listed", "U1 empty path is still a pin (not unverified)",
     '        if parse_uri(kv[2]) is None:\n            unverified.append(img_ln)',
     '        if parse_uri(kv[2]) is None or parse_uri(kv[2])["path"] == "":\n            unverified.append(img_ln)',
     "killed: EMPTY-PATH if its image line is checked by U1"),
    ("U1c-offbyone-line-index", "U1 physical line lookup",
     '        kv = split_key(lines[img_ln - 1])',
     '        kv = split_key(lines[img_ln])',
     "killed: UNVERIFIED-IMAGE (next line is an entry line)"),
    ("U1d-discard-none-removed", "U1 image-line set drops None",
     '    image_lines.discard(None)',
     '    # image_lines.discard(None) -- mutant',
     "killed by a crash on entries with no image line (ENTRY-SCOPE)"),
    # ---- R9: entry body / protocol / image line ----
    ("R9a-body-last-key-wins", "R9 first key line of a body wins",
     '        if body is not None and key in ("protocol", "path", "image_path") and key not in body:',
     '        if body is not None and key in ("protocol", "path", "image_path"):',
     "killed: FIRST-PATH/FIRST-PROTOCOL"),
    ("R9b-protocol-set-adds-linux", "R9 chainload protocols are efi/uefi/efi_chainload",
     'EFI_PROTOCOLS = frozenset({"efi", "uefi", "efi_chainload"})',
     'EFI_PROTOCOLS = frozenset({"efi", "uefi", "efi_chainload", "linux"})',
     "killed: NON-EFI-MISSING (linux must be not-modelled)"),
    ("R9c-protocol-lower", "R9 protocol compared with strcmp (case-sensitive)",
     'if b.get("protocol") in EFI_PROTOCOLS}',
     'if (b.get("protocol") or "").lower() in EFI_PROTOCOLS}',
     "killed: NON-EFI-MISSING (EFI/UEFI case variants)"),
    ("R9d-protocol-value-strip", "R9 protocol value compared with strcmp (trailing blanks matter)",
     '            body[key] = value if key == "protocol" else lineno',
     '            body[key] = value.strip() if key == "protocol" else lineno',
     "killed: EFI-IMAGE-MISSING (protocol with a trailing blank is not efi)"),
    # ---- R6: consequences for missing / optional ----
    ("R6a-missing-any-panics", "R6 LP-MISSING panics only on an efi image line",
     '            if lineno in image_lines:\n                rec.update(status="LP-MISSING", consequence="panic",',
     '            if True:\n                rec.update(status="LP-MISSING", consequence="panic",',
     "killed: MISSING/NON-EFI-MISSING/OPTIONAL-MISSING"),
    ("R6b-image-missing-not-modelled", "R6 efi image LP-MISSING panics",
     '                rec.update(status="LP-MISSING", consequence="panic",\n                           detail="image of an efi chainload entry:',
     '                rec.update(status="LP-MISSING", consequence="not-modelled",\n                           detail="image of an efi chainload entry:',
     "killed: EFI-IMAGE-MISSING"),
    ("R6c-optional-missing-panics", "R6 optional LP-MISSING is not-modelled",
     '                rec.update(status="LP-MISSING", consequence="not-modelled")',
     '                rec.update(status="LP-MISSING", consequence="skip" if optional else "not-modelled")',
     "killed: OPTIONAL-MISSING (optional must be not-modelled)"),
    # ---- R7 / R4 / R5 / R2 / R1 general ----
    ("R7a-rc-bad-resource-not-fault", "R7 LP-BAD-RESOURCE is DEGRADED rc1",
     'FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE")',
     'FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT")',
     "killed: BAD-RESOURCE"),
    ("R4a-resource-lower", "R4 resource name compared case-sensitively",
     '        if resource not in RESOURCES:',
     '        if resource.lower() not in RESOURCES:',
     "killed: BAD-RESOURCE/RESOURCE-CASE (BOOT() must be LP-BAD-RESOURCE)"),
    ("R4b-double-dollar", "R4 exactly one leading $ dropped",
     '        resource = uri["resource"][1:] if uri["resource"].startswith("$") else uri["resource"]',
     '        resource = uri["resource"].lstrip("$")',
     "killed: DOUBLE-DOLLAR"),
    ("R5a-hash-upper-compare", "R5 hash compare is case-insensitive",
     '        if got == h.lower():',
     '        if got == h:',
     "killed: HASH-UPPER"),
    ("R2a-first-hash", "R2 hash starts after the LAST #",
     '    cut = tail.rfind("#")',
     '    cut = tail.find("#")',
     "killed: LAST-HASH"),
    ("R2b-rfind-paren", "R2 resource ends at the FIRST (",
     '    lp = value.find("(")',
     '    lp = value.rfind("(")',
     "killed: PAREN-PATH"),
    ("R1a-value-trailing-strip", "R1 value keeps trailing blanks",
     '    return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \\t")',
     '    return line[:i].lower(), line[:i], line[i + 1:].strip(" \\t")',
     "killed: PANIC-VALUE-BLANKS (reported value must keep trailing blanks)"),
    ("R1b-value-no-lstrip", "R1 value loses leading blanks",
     '    return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \\t")',
     '    return line[:i].lower(), line[:i], line[i + 1:]',
     "killed everywhere: every value keeps its leading blank -> LP-BAD-RESOURCE"),
    ("R1c-cr-dropped", "R1 every CR is removed before the key is read",
     '    line = raw.replace("\\r", "").strip(" \\t")',
     '    line = raw.strip(" \\t")',
     "killed: CR-INTERNAL (CR inside key/hash)"),
    ("R8a-empty-entry-label", "R8 empty cleaned label keeps the previous entry",
     '            entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry',
     '            entry = sanitize(stripped.lstrip("/").lstrip("+").strip())',
     "survivor expected: no family writes a bare '/' entry line"),
    ("V1m-child-entry-boundary", "R9/V1 a '//' child line starts a new entry body",
     '        if stripped.startswith("/"):\n            if first_entry is not None and lineno == first_entry and first_entry != 1:',
     '        if stripped.startswith("/") and not stripped.startswith("//"):\n            if first_entry is not None and lineno == first_entry and first_entry != 1:',
     "killed: ENTRY-SCOPE (an indented '//' child body becomes part of the parent)"),
    ("V1n-measured-last-wins", "V1/R10 first visible measured_boot wins",
     '        if in_global and key == "measured_boot" and measured_setting is None:',
     '        if in_global and key == "measured_boot":',
     "survivor expected: no family writes two visible measured_boot keys"),
    ("U1e-reported-line-offset", "U1 reports the physical line number",
     '            unverified.append(img_ln)\n    unverified.sort()',
     '            unverified.append(img_ln + 1)\n    unverified.sort()',
     "killed: UNVERIFIED-IMAGE (reported line is one too high)"),
    ("CONF-a-onpanic-menu", "unreadable conf: on_panic is null",
     '        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "on_panic": None,',
     '        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "on_panic": "menu",',
     "survivor expected: battery skips on_panic when conf is unreadable"),
    ("CONF-b-rc-1", "unreadable conf: rc 2",
     '        return {"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], "on_panic": None,',
     '        return {"verdict": "CANNOT-EVALUATE", "rc": 1, "pins": [], "on_panic": None,',
     "killed: CONF-UNREADABLE"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    src = open(CANON, "rb").read()
    text = src.decode("utf-8")
    canon_sha = hashlib.sha256(src).hexdigest()
    rows = []
    for name, clause, old, new, expect in MUTANTS:
        n = text.count(old)
        if n != 1:
            print("PATCH-ERROR %s matches=%d" % (name, n), file=sys.stderr)
            sys.exit(2)
        mut = text.replace(old, new)
        p = os.path.join(OUT, name + ".py")
        with open(p, "wb") as f:
            f.write(mut.encode("utf-8"))
        rows.append({"name": name, "clause": clause, "expect": expect,
                     "sha256": hashlib.sha256(mut.encode()).hexdigest(),
                     "canon_sha256": canon_sha,
                     "diff_lines": [l for l in (old, new)]})
    with open(os.path.join(OUT, "INDEX.json"), "w") as f:
        json.dump(rows, f, indent=1)
    print("built %d mutants from canon %s" % (len(rows), canon_sha))


if __name__ == "__main__":
    main()
