#!/usr/bin/env python3
"""Round-90 C1 freeze controls: build the do-nothing and near-miss gates the r90 battery must reject.

K1  do-nothing: the landed gate tools/check-limine-pins.py at the pre-round tip (copied byte-exact).
K2  do-nothing adapter: K1 that accepts --tpm-present and always answers on_panic "menu" (so every
    r89-era answer is unchanged and only the r90 clauses can kill it).
Nxx near-miss: the r90 candidate with exactly ONE r90 clause bent (one textual patch, asserted to
    apply exactly once). Each names the clause and the family expected to kill it.

Usage: make-controls.py --landed FILE --candidate FILE --out DIR
Writes DIR/<name>.py and DIR/INDEX.tsv (name, clause, expected killer families). Read-only on inputs.
"""
import argparse
import os

K2_PATCHES = [
    ('    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)\n',
     '    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)\n'
     '    ap.add_argument("--tpm-present", choices=("0", "1"), default=None)\n'),
    ('    print(json.dumps(r, sort_keys=True))\n',
     '    r["on_panic"] = "menu"\n    print(json.dumps(r, sort_keys=True))\n'),
]

# name: (clause, killer families, [(old, new), ...]) — patches over the r90 candidate
NEAR = {
    "N01-resource-casefold": ("R4 strcmp", "BAD-RESOURCE RESOURCE-CASE", [
        ('        if resource not in RESOURCES:\n', '        if resource.lower() not in RESOURCES:\n')]),
    "N02-no-bad-resource": ("R4 invalid name is LP-BAD-RESOURCE", "BAD-RESOURCE BAD-OVER-UNRESOLVED", [
        ('        if resource not in RESOURCES:\n', '        if False:\n')]),
    "N03-bad-optional-panics": ("R6 optional bad resource -> skip", "BAD-RESOURCE-OPTIONAL", [
        ('            rec.update(status="LP-BAD-RESOURCE", consequence="skip" if optional else "panic",\n',
         '            rec.update(status="LP-BAD-RESOURCE", consequence="panic",\n')]),
    "N04-resource-before-format": ("R3 before R4", "FORMAT-BEFORE-BAD", [
        ('        if len(h) != 128 or not set(h) <= HEXDIGITS:\n',
         '        if len(h) != 128 or not set(h) <= HEXDIGITS:\n'
         '            _r = uri["resource"][1:] if uri["resource"].startswith("$") else uri["resource"]\n'
         '            if _r not in RESOURCES:\n'
         '                rec.update(status="LP-BAD-RESOURCE", consequence="skip" if optional else "panic")\n'
         '                pins.append(rec)\n'
         '                continue\n')]),
    "N05-bad-not-fault": ("R7 LP-BAD-RESOURCE is a fault", "BAD-OVER-UNRESOLVED BAD-RESOURCE", [
        ('FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT", "LP-BAD-RESOURCE")\n',
         'FAULTS = ("LP-MISMATCH", "LP-MISSING", "LP-HASH-FORMAT")\n'),
        ('    elif "LP-UNRESOLVED" in statuses:\n',
         '    elif statuses & {"LP-UNRESOLVED", "LP-BAD-RESOURCE"}:\n')]),
    "N06-strip-all-dollars": ("R4 one '$' dropped", "DOUBLE-DOLLAR", [
        ('        resource = uri["resource"][1:] if uri["resource"].startswith("$") else uri["resource"]\n'
         '        if resource not in RESOURCES:\n',
         '        resource = uri["resource"].lstrip("$")\n'
         '        if resource not in RESOURCES:\n')]),
    "N07-any-key-panics": ("R9 only the image line", "PATH-PRECEDENCE FIRST-PATH", [
        ('            if lineno in image_lines:\n', '            if lineno in image_lines or entry_efi.get(lineno):\n'),
        ('    image_lines.discard(None)\n',
         '    image_lines.discard(None)\n'
         '    entry_efi = {ln: True for b in bodies if b.get("protocol") in EFI_PROTOCOLS for ln in b.get("_lines", [])}\n'),
        ('        if key in PIN_KEYS:\n            uri = parse_uri(value)\n',
         '        if body is not None:\n            body.setdefault("_lines", []).append(lineno)\n'
         '        if key in PIN_KEYS:\n            uri = parse_uri(value)\n')]),
    "N08-any-protocol-panics": ("R9 efi protocols only", "NON-EFI-MISSING", [
        ('    image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}\n',
         '    image_lines = {b.get("path", b.get("image_path")) for b in bodies}\n')]),
    "N09-protocol-casefold": ("R9 protocol strcmp", "NON-EFI-MISSING", [
        ('            body[key] = value if key == "protocol" else lineno\n',
         '            body[key] = value.lower() if key == "protocol" else lineno\n')]),
    "N10-protocol-last-wins": ("R9 first protocol line", "FIRST-PROTOCOL", [
        ('        if body is not None and key in ("protocol", "path", "image_path") and key not in body:\n'
         '            body[key] = value if key == "protocol" else lineno\n',
         '        if body is not None and key in ("protocol", "path", "image_path") and (key == "protocol" or key not in body):\n'
         '            body[key] = value if key == "protocol" else lineno\n')]),
    "N11-image-path-first": ("R9 PATH before IMAGE_PATH", "PATH-PRECEDENCE", [
        ('    image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}\n',
         '    image_lines = {b.get("image_path", b.get("path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}\n')]),
    "N12-path-last-wins": ("R9 first path line", "FIRST-PATH", [
        ('        if body is not None and key in ("protocol", "path", "image_path") and key not in body:\n'
         '            body[key] = value if key == "protocol" else lineno\n',
         '        if body is not None and key in ("protocol", "path", "image_path") and (key == "path" or key not in body):\n'
         '            body[key] = value if key == "protocol" else lineno\n')]),
    "N13-protocol-leaks": ("R9 body ends at the next entry line", "ENTRY-SCOPE", [
        ('            body = {}\n            bodies.append(body)\n',
         '            body = {"protocol": body["protocol"]} if body and "protocol" in body else {}\n'
         '            bodies.append(body)\n')]),
    "N14-global-is-entry": ("R9 lines before the first entry belong to no entry", "ENTRY-SCOPE", [
        ('    body = None          # the current entry\'s first protocol/path/image_path key lines\n'
         '    bodies = []\n',
         '    body = {}\n    bodies = [body]\n')]),
    "N15-boot-entry-is-efi": ("R9 efi_boot_entry is not chainload", "NON-EFI-MISSING", [
        ('EFI_PROTOCOLS = frozenset({"efi", "uefi", "efi_chainload"})\n',
         'EFI_PROTOCOLS = frozenset({"efi", "uefi", "efi_chainload", "efi_boot_entry"})\n')]),
    "N16-measured-casefold": ("R10 strcmp yes", "MEASURED-VALUE-CASE", [
        ('    requested = (measured_setting is not None and measured_setting[1] == "yes") or secure_boot\n',
         '    requested = (measured_setting is not None and measured_setting[1].lower() == "yes") or secure_boot\n')]),
    "N17-measured-last-wins": ("R10 first measured_boot line", "MEASURED-FIRST", [
        ('        if key == "measured_boot" and measured_setting is None:\n',
         '        if key == "measured_boot":\n')]),
    "N18-tpm-ignored": ("R10 no TPM forces measured boot off", "MEASURED-TPM0 MEASURED-TPM-ABSENT", [
        ('    if tpm is None:\n        return "halt-if-tpm"\n    return "halt" if tpm else "menu"\n',
         '    return "halt"\n')]),
    "N19-tpm-absent-menu": ("R10 absent flag -> halt-if-tpm", "MEASURED-TPM-ABSENT", [
        ('    if tpm is None:\n        return "halt-if-tpm"\n', '    if tpm is None:\n        return "menu"\n')]),
    "N20-sb-not-measured": ("R10 Secure Boot requests measured boot", "MEASURED-SB", [
        ('    requested = (measured_setting is not None and measured_setting[1] == "yes") or secure_boot\n',
         '    requested = (measured_setting is not None and measured_setting[1] == "yes")\n')]),
    "N21-measured-global-only": ("R10 key read over the whole file", "MEASURED-IN-ENTRY", [
        ('        if key == "measured_boot" and measured_setting is None:\n',
         '        if key == "measured_boot" and measured_setting is None and body is None:\n')]),
    "N22-protocol-raw-scan": ("R9 with R1: only key lines set the protocol", "PROTOCOL-DECOY", [
        ('        kv = split_key(raw)\n        if kv is None:\n            continue\n',
         '        if body is not None and "protocol" not in body and "protocol" in stripped.lower() and ":" in stripped:\n'
         '            body["protocol"] = stripped.rsplit(":", 1)[1].strip(" \\t")\n'
         '        kv = split_key(raw)\n        if kv is None:\n            continue\n')]),
    "N23-measured-raw-scan": ("R10 with R1: only key lines set measured_boot", "MEASURED-DECOY", [
        ('        kv = split_key(raw)\n        if kv is None:\n            continue\n',
         '        if measured_setting is None and "measured_boot" in stripped.lower() and ":" in stripped:\n'
         '            measured_setting = (lineno, stripped.rsplit(":", 1)[1].strip(" \\t"))\n'
         '        kv = split_key(raw)\n        if kv is None:\n            continue\n')]),
    # r89 routed defect 2 repairs (KEY-SPACING `path =` decoy, LARGE-FILE, NON-UTF8, PANIC-AFTER-PIN)
    "N24-equals-separator": ("R1 key followed directly by ':' (blank then '=')", "KEY-SPACING", [
        ('    if i == 0 or i >= len(line) or line[i] != ":":\n        return None\n'
         '    return line[:i].lower(), line[:i], line[i + 1:].lstrip(" \\t")\n',
         '    if i == 0 or i >= len(line) or line[i] not in ":= \\t":\n        return None\n'
         '    j = i\n    while j < len(line) and line[j] in " \\t":\n        j += 1\n'
         '    if j >= len(line) or line[j] not in ":=":\n        return None\n'
         '    return line[:i].lower(), line[:i], line[j + 1:].lstrip(" \\t")\n')]),
    "N25-hash-first-mib": ("R5 every stored byte hashed", "LARGE-FILE", [
        ('        for chunk in iter(lambda: f.read(1 << 20), b""):\n            h.update(chunk)\n',
         '        h.update(f.read(1 << 20))\n')]),
    "N26-strict-utf8": ("R1/R7 non-UTF-8 conf is read (killed by a crash row: error, QUALITY 126)", "NON-UTF8", [
        ('            text = f.read().decode("utf-8", "surrogateescape")\n',
         '            text = f.read().decode("utf-8")\n')]),
    "N27-panic-before-pins": ("R6 first hash_mismatch_panic anywhere in the file", "PANIC-AFTER-PIN", [
        ('        if key == "hash_mismatch_panic" and panic_setting is None:\n',
         '        if key == "hash_mismatch_panic" and panic_setting is None and not raw_pins:\n')]),
}


def patch(src, pairs, name):
    for old, new in pairs:
        n = src.count(old)
        if n != 1:
            raise SystemExit("%s: patch anchor found %d times: %r" % (name, n, old[:80]))
        src = src.replace(old, new)
    return src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--landed", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    landed = open(a.landed).read()
    cand = open(a.candidate).read()
    rows = [("K1-landed-gate", "do-nothing (r87 gate as landed)", "all r90 families"),
            ("K2-landed-adapter", "do-nothing + accepts --tpm-present, on_panic always menu", "r90 families")]
    with open(os.path.join(a.out, "K1-landed-gate.py"), "w") as f:
        f.write(landed)
    with open(os.path.join(a.out, "K2-landed-adapter.py"), "w") as f:
        f.write(patch(landed, K2_PATCHES, "K2"))
    for name, (clause, killers, pairs) in NEAR.items():
        with open(os.path.join(a.out, name + ".py"), "w") as f:
            f.write(patch(cand, pairs, name))
        rows.append((name, clause, killers))
    with open(os.path.join(a.out, "INDEX.tsv"), "w") as f:
        f.write("name\tclause\texpected_killers\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print("wrote %d control gates to %s" % (len(rows), a.out))


if __name__ == "__main__":
    main()
