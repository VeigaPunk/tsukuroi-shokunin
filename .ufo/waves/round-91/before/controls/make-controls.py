#!/usr/bin/env python3
"""Round-91 C1 freeze controls: build the do-nothing and near-miss gates the r91 battery must reject.

K1  do-nothing: the landed gate tools/check-limine-pins.py at the pre-round tip (copied byte-exact).
K2  do-nothing adapter: K1 that accepts --tpm-present and always answers on_panic "menu" (so every
    r90-era answer is unchanged and only the r91 clauses can kill it).
Nxx near-miss: the r91 candidate with exactly ONE r91 clause bent (one textual patch, asserted to
    apply exactly once). Each names the clause and the family expected to kill it.

Usage: make-controls.py --landed FILE --candidate FILE --out DIR
Writes DIR/<name>.py and DIR/INDEX.tsv (name, clause, expected killer families). Read-only on inputs.
"""
import argparse
import os

K2_PATCHES = [
    # The r90 landed gate already registers --tpm-present (round 90 added R10); the adapter only
    # needs to force on_panic "menu" so the r90 answers stay unchanged and only r91 clauses kill it.
    ('    print(json.dumps(r, sort_keys=True))\n',
     '    r["on_panic"] = "menu"\n    print(json.dumps(r, sort_keys=True))\n'),
]

# name: (clause, killer families, [(old, new), ...]) — patches over the r91 candidate
NEAR = {
    # V1: panic read whole-file instead of global-section-only
    "N01-panic-whole-file": ("V1 hash_mismatch_panic global-section only", "PANIC-AFTER-PIN PANIC-GLOBAL-ONLY GLOBAL-VS-ENTRY", [
        ('        if in_global and key == "hash_mismatch_panic" and panic_setting is None:\n',
         '        if key == "hash_mismatch_panic" and panic_setting is None:\n')]),
    # V1: measured read whole-file instead of global-section-only
    "N02-measured-whole-file": ("V1 measured_boot global-section only", "MEASURED-IN-ENTRY MEASURED-GLOBAL-ONLY GLOBAL-VS-ENTRY", [
        ('        if in_global and key == "measured_boot" and measured_setting is None:\n',
         '        if key == "measured_boot" and measured_setting is None:\n')]),
    # V1: first-line-entry exception dropped (always cut at first '/' line)
    "N03-no-first-line-exception": ("V1 first-line-is-entry keeps whole file visible", "FIRST-LINE-ENTRY", [
        ('            if first_entry is not None and lineno == first_entry and first_entry != 1:\n',
         '            if first_entry is not None and lineno == first_entry:\n')]),
    # V1: first-line-entry exception inverted (cut even when first line is entry)
    "N04-first-line-inverted": ("V1 first-line-is-entry keeps whole file visible", "FIRST-LINE-ENTRY", [
        ('            if first_entry is not None and lineno == first_entry and first_entry != 1:\n',
         '            if first_entry is not None and lineno == first_entry and first_entry == 1:\n')]),
    # U1: unverified_image_lines field omitted entirely
    "N05-no-unverified-field": ("U1 unverified_image_lines reported", "UNVERIFIED-IMAGE UNVERIFIED-MIXED UNVERIFIED-NON-EFI UNVERIFIED-IMAGE-PATH UNVERIFIED-SORTED", [
        ('            "unverified_image_lines": unverified,\n', '')]),
    # U1: unverified list includes pins (parse_uri check removed)
    "N06-unverified-includes-pins": ("U1 only non-pin image lines listed", "UNVERIFIED-MIXED", [
        ('        if parse_uri(kv[2]) is None:\n            unverified.append(img_ln)\n',
         '        unverified.append(img_ln)\n')]),
    # U1: unverified list applies to non-efi entries too
    "N07-unverified-non-efi": ("U1 efi chainload entries only", "UNVERIFIED-NON-EFI", [
        ('    image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}\n',
         '    image_lines = {b.get("path", b.get("image_path")) for b in bodies}\n')]),
    # U1: unverified list unsorted
    "N08-unverified-unsorted": ("U1 sorted ascending", "UNVERIFIED-SORTED UNVERIFIED-IMAGE UNVERIFIED-MIXED UNVERIFIED-IMAGE-PATH", [
        ('    unverified.sort()\n', '    unverified.reverse()\n')]),
    # U1: unverified uses last-wins path instead of first
    "N09-unverified-last-path": ("U1 first path else first image_path", "UNVERIFIED-IMAGE-PATH", [
        ('    image_lines = {b.get("path", b.get("image_path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}\n',
         '    image_lines = {b.get("image_path", b.get("path")) for b in bodies if b.get("protocol") in EFI_PROTOCOLS}\n')]),
    # V1: panic_setting reads the LAST key anywhere (whole-file last-wins) — distinct bend from
    # N01 (first-wins whole-file). Repaired after w1: the frozen patch was byte-identical to N01
    # (ExecReplicate/MutGate); last-wins keeps a first-wins guard off while dropping in_global.
    "N10-panic-first-anywhere": ("V1 LAST visible panic key wins whole file", "PANIC-AFTER-PIN PANIC-FIRST PANIC-GLOBAL-ONLY PANIC-METADATA", [
        ('        if in_global and key == "hash_mismatch_panic" and panic_setting is None:\n            panic_setting = (lineno, value)\n',
         '        if key == "hash_mismatch_panic":\n            panic_setting = (lineno, value)\n')]),
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
    rows = [("K1-landed-gate", "do-nothing (r90 gate as landed)", "all r91 families"),
            ("K2-landed-adapter", "do-nothing + accepts --tpm-present, on_panic always menu", "r91 families")]
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
