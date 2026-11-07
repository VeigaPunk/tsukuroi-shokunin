#!/usr/bin/env python3
"""Generate MutHeldOut (round 89) mutants of the pristine r87 landed gate and probe fixtures.

Each mutant is ONE textual replacement in the pristine gate that bends one R1-R8 clause of the
r89 battery docstring. A probe spec witnesses the behavioural difference against the pristine gate.
Writes: mutants/<id>.py, mutants/<id>.diff, probes/<id>.json, probes/<id>.out.json
"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
WAVE = os.path.join(LANE, ".ufo/waves/round-89/w1/MutHeldOut")
PRISTINE = os.path.join(LANE, ".ufo/waves/round-89/before/roster/pos-landed-gate-3ba37eb0.py")
HARNESS = os.path.join(WAVE, "probe_harness.py")
MUT = os.path.join(WAVE, "mutants")
PROB = os.path.join(WAVE, "probes")


def b2(data):
    return hashlib.blake2b(data).hexdigest()


def flip_last(h):
    c = h[-1]
    return h[:-1] + ("0" if c != "0" else "1")


def size_bytes(n):
    return bytes((i * 37 + 11) % 251 for i in range(n))


A = "EFI/Linux/a.efi"
B = "EFI/Linux/b.efi"
A40 = {"size": 40}
H40 = b2(size_bytes(40))

M = [
    # id, clause, old, new, probe spec
    dict(id="h25-traversal-uncontained", clause="R4 path containment (`..` leaves the ESP -> LP-UNRESOLVED)",
         old='''    root = os.path.realpath(esp)
    resolved = os.path.realpath(target)
    if resolved != root and not resolved.startswith(root + os.sep):
        return None
    return target''',
         new='''    root = os.path.realpath(esp)
    resolved = os.path.realpath(target)
    return target''',
         spec=dict(files={A: A40}, outside_files={"outside": A40},
                   conf=["/e", "path: boot():/../outside#{{B2O:outside}}"])),
    dict(id="h26-symlink-abspath", clause="R4 a symlink pointing outside the ESP -> LP-UNRESOLVED",
         old="    resolved = os.path.realpath(target)",
         new="    resolved = os.path.abspath(target)",
         spec=dict(files={}, outside_files={"outside": A40}, symlinks={"link.efi": "../outside"},
                   conf=["/e", "path: boot():/link.efi#{{B2O:outside}}"])),
    dict(id="h27-contain-prefix-only", clause="R4 containment is a path-component test, not a string prefix",
         old="    if resolved != root and not resolved.startswith(root + os.sep):",
         new="    if resolved != root and not resolved.startswith(root):",
         spec=dict(esp_name="esp", files={}, outside_dirs=["espx"],
                   outside_files={"espx/f.efi": A40}, symlinks={"link.efi": "../espx/f.efi"},
                   conf=["/e", "path: boot():/link.efi#{{B2O:espx/f.efi}}"])),
    dict(id="h28-bare-key-line-crash", clause="R1 a line of key characters with no ':' is not a key line (must not crash)",
         old='    if i == 0 or i >= len(line) or line[i] != ":":',
         new='    if i == 0 or i > len(line) or line[i] != ":":',
         spec=dict(files={A: A40}, conf=["timeout", "/e", "path: boot():/%s#{{B2:%s}}" % (A, A)])),
    dict(id="h29-hash-first-mib", clause="R5 BLAKE2b-512 over ALL raw stored bytes (no size truncation)",
         old="""    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)""",
         new="""    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
            break""",
         spec=dict(files={"big.efi": {"size": 2 * 1024 * 1024}},
                   conf=["/e", "path: boot():/big.efi#{{B2:big.efi}}"])),
    dict(id="h30-panic-after-pin", clause="R6 the prompt rule reads the FIRST hash_mismatch_panic key line in the WHOLE file",
         old='        if key == "hash_mismatch_panic" and panic_setting is None:',
         new='        if key == "hash_mismatch_panic" and panic_setting is None and not raw_pins:',
         spec=dict(files={A: A40},
                   conf=["/e", "path: boot():/%s#{{FLIP:%s}}" % (A, A), "hash_mismatch_panic: no"])),
    dict(id="h31-any-hex-char", clause="R3 the hash must be ENTIRELY [0-9a-fA-F]",
         old="        if len(h) != 128 or not set(h) <= HEXDIGITS:",
         new="        if len(h) != 128 or not set(h) & HEXDIGITS:",
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/%s#%s" % (A, "g" + "a" * 127)])),
    dict(id="h32-len-at-most", clause="R3 the hash must be EXACTLY 128 characters",
         old="        if len(h) != 128 or not set(h) <= HEXDIGITS:",
         new="        if len(h) > 128 or not set(h) <= HEXDIGITS:",
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/%s#%s" % (A, "a" * 127)])),
    dict(id="h33-exit-zero", clause="R7/output contract the process exit code equals rc",
         old='    print(json.dumps(r, sort_keys=True))\n    return r["rc"]',
         new='    print(json.dumps(r, sort_keys=True))\n    return 0',
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/%s#{{FLIP:%s}}" % (A, A)])),
    dict(id="h34-sb-absent-enforced", clause="R7 `--secure-boot-enforced 0` and an absent flag both mean not enforced",
         old='    elif a.conf and a.esp:\n        r = check(a.conf, a.esp, a.secure_boot_enforced == "1")',
         new='    elif a.conf and a.esp:\n        r = check(a.conf, a.esp, a.secure_boot_enforced != "0")',
         spec=dict(files={A: A40}, sb=None,
                   conf=["/e", "path: boot():/%s#{{FLIP:%s}}" % (A, A), "hash_mismatch_panic: no"])),
    dict(id="h35-missing-consequence-skip", clause="R6 LP-MISSING consequence is `not-modelled`",
         old='            rec.update(status="LP-MISSING", consequence="not-modelled")',
         new='            rec.update(status="LP-MISSING", consequence="skip")',
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/gone.efi#{{B2:%s}}" % A])),
    dict(id="h36-unresolved-consequence-none", clause="R6 LP-UNRESOLVED consequence is `not-modelled`",
         old='''            rec.update(status="LP-UNRESOLVED", consequence="not-modelled",
                       detail="resource %s(%s) is not the boot partition" % (resource, uri["root"]))''',
         new='''            rec.update(status="LP-UNRESOLVED", consequence="none",
                       detail="resource %s(%s) is not the boot partition" % (resource, uri["root"]))''',
         spec=dict(files={A: A40}, conf=["/e", "path: guid(1234):/%s#{{B2:%s}}" % (A, A)])),
    dict(id="h37-dir-as-file", clause="R5 a path naming a directory is LP-MISSING, not an error",
         old="        if not os.path.isfile(target):",
         new="        if not os.path.exists(target):",
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/#" + H40])),
    dict(id="h38-optional-dtb", clause="R6 only wallpaper/term_font are optional (dtb_path is not)",
         old='OPTIONAL_KEYS = frozenset({"wallpaper", "term_font"})',
         new='OPTIONAL_KEYS = frozenset({"wallpaper", "term_font", "dtb_path"})',
         spec=dict(files={"x.efi": A40}, conf=["/e", "dtb_path: boot():/x.efi#{{FLIP:x.efi}}"])),
    dict(id="h39-hash-prefix-compare", clause="R5 the WHOLE 128-hexdigit digest is compared",
         old="        if got == h.lower():",
         new="        if got[:64] == h.lower()[:64]:",
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/%s#{{FLIP:%s}}" % (A, A)])),
    dict(id="h40-entry-first-sticks", clause="R8 the entry label is the NEAREST preceding entry line",
         old='            entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry',
         new='            entry = entry or sanitize(stripped.lstrip("/").lstrip("+").strip())',
         spec=dict(files={A: A40, B: A40},
                   conf=["/alpha", "  path: boot():/%s#{{B2:%s}}" % (A, A), "/beta",
                         "  path: boot():/%s#{{B2:%s}}" % (B, B)])),
    dict(id="h41-root-whitespace", clause="R4 a NON-empty root (blank) does not resolve",
         old='        if resource != "boot" or uri["root"] != "":',
         new='        if resource != "boot" or uri["root"].strip() != "":',
         spec=dict(files={A: A40}, conf=["/e", "path: boot( ):/%s#{{B2:%s}}" % (A, A)])),
    dict(id="h42-plus-slash-lstrip", clause="R8 label = strip the leading '/' run, THEN one leading '+'",
         old='            entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry',
         new='            entry = sanitize(stripped.lstrip("/+").strip()) or entry',
         spec=dict(files={A: A40}, conf=["/+/alpha", "  path: boot():/%s#{{B2:%s}}" % (A, A)])),
    dict(id="h43-empty-label-entry", clause="R8 an entry line with an empty label keeps the previous label",
         old='            entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry',
         new='            entry = sanitize(stripped.lstrip("/").lstrip("+").strip())',
         spec=dict(files={A: A40}, conf=["/alpha", "//", "  path: boot():/%s#{{B2:%s}}" % (A, A)])),
    dict(id="h44-empty-resource-boot", clause="R4 only resource `boot` resolves (the empty resource does not)",
         old='        if resource != "boot" or uri["root"] != "":',
         new='        if resource not in ("boot", "") or uri["root"] != "":',
         spec=dict(files={A: A40}, conf=["/e", "path: ():/%s#{{B2:%s}}" % (A, A)])),
    dict(id="h45-isdir-check", clause="R5 an absent file is LP-MISSING (not an unreadable/UNRESOLVED error)",
         old="        if not os.path.isfile(target):",
         new="        if os.path.isdir(target):",
         spec=dict(files={A: A40}, conf=["/e", "path: boot():/gone.efi#{{B2:%s}}" % A])),
    dict(id="h46-conf-decode-strict", clause="R1/R7 a readable conf with non-UTF-8 bytes still parses (surrogateescape)",
         old='            text = f.read().decode("utf-8", "surrogateescape")',
         new='            text = f.read().decode("utf-8")',
         spec=dict(files={A: A40},
                   conf_hex=(b"# \xff\xfe comment\n/e\npath: boot():/" + A.encode() + b"#" + H40.encode()
                             + b"\n").hex())),
    dict(id="h47-entry-trim-redundant", clause="R8 trim of the label is redundant (R1 already stripped the line)",
         old='            entry = sanitize(stripped.lstrip("/").lstrip("+").strip()) or entry',
         new='            entry = sanitize(stripped.lstrip("/").lstrip("+").lstrip(" \\t")) or entry',
         spec=dict(files={A: A40}, conf=["/alpha", "  path: boot():/%s#{{B2:%s}}" % (A, A)]),
         equivalent=True),
]


def main():
    src = open(PRISTINE).read()
    os.makedirs(MUT, exist_ok=True)
    os.makedirs(PROB, exist_ok=True)
    report = []
    for m in M:
        n = src.count(m["old"])
        if n != 1:
            print("BAD ANCHOR (%d) %s" % (n, m["id"]), file=sys.stderr)
            return 2
        text = src.replace(m["old"], m["new"])
        mp = os.path.join(MUT, m["id"] + ".py")
        with open(mp, "w") as f:
            f.write(text)
        diff = "".join(difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                            "pristine/pos-landed-gate-3ba37eb0.py", m["id"] + ".py"))
        with open(os.path.join(MUT, m["id"] + ".diff"), "w") as f:
            f.write(diff)
        sp = os.path.join(PROB, m["id"] + ".json")
        with open(sp, "w") as f:
            json.dump(m["spec"], f, indent=1, sort_keys=True)
        outs = {}
        for tag, gate in (("pristine", PRISTINE), ("mutant", mp)):
            p = subprocess.run([sys.executable, HARNESS, sp, gate], capture_output=True, text=True)
            try:
                outs[tag] = json.loads(p.stdout)
            except Exception:  # noqa: BLE001
                outs[tag] = {"harness_error": p.stdout[:200] + p.stderr[-300:]}
        def body(x):
            return {k: v for k, v in x.items() if k not in ("gate", "spec")}
        same = body(outs["pristine"]) == body(outs["mutant"])
        with open(os.path.join(PROB, m["id"] + ".out.json"), "w") as f:
            json.dump({"id": m["id"], "clause": m["clause"], "equivalent": bool(m.get("equivalent")),
                       "differs": not same, "pristine": outs["pristine"], "mutant": outs["mutant"]},
                      f, indent=1, sort_keys=True)
        report.append({"id": m["id"], "clause": m["clause"], "equivalent": bool(m.get("equivalent")),
                       "differs": not same,
                       "pristine": [outs["pristine"].get("exit"), outs["pristine"].get("verdict"),
                                    outs["pristine"].get("pins"), outs["pristine"].get("entries")],
                       "mutant": [outs["mutant"].get("exit"), outs["mutant"].get("verdict"),
                                  outs["mutant"].get("pins"), outs["mutant"].get("entries")]})
        print("%-30s differs=%-5s %s" % (m["id"], not same, outs["pristine"].get("pins")))
    with open(os.path.join(WAVE, "probe-summary.json"), "w") as f:
        json.dump(report, f, indent=1)
    print("generated %d mutants" % len(M))
    return 0


if __name__ == "__main__":
    sys.exit(main())
