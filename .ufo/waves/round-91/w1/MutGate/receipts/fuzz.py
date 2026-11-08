#!/usr/bin/env python3
"""Differential fuzz: pristine frozen gate vs one mutant over random limine.conf-shaped files.

Reports the first N divergences with the conf that produced them. Used to back an `equivalent`
classification (0 divergences in N cases) or to exhibit a concrete untested bend (a survivor).
"""
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(S, "canon-frozen.py")
FIELDS = ("verdict", "rc", "on_panic", "hash_mismatch_panic", "measured_boot",
          "unverified_image_lines", "pins", "findings")


def gate_out(gate, conf, esp, sb, tpm):
    argv = [sys.executable, gate, "--conf", conf, "--esp", esp]
    if sb is not None:
        argv += ["--secure-boot-enforced", sb]
    if tpm is not None:
        argv += ["--tpm-present", tpm]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=30)
    try:
        d = json.loads(p.stdout)
    except Exception:
        return {"__error__": p.returncode, "stderr": p.stderr[-200:]}
    return {k: d.get(k) for k in FIELDS}


def gen(rng):
    files = {}
    lines = []

    def pathpin(key, state, indent=""):
        rel = "EFI/Linux/%s.efi" % "".join(rng.choice("abcdefgh0123") for _ in range(6))
        data = ("payload-" + rel).encode()
        if state != "missing":
            files[rel] = data
        good = hashlib.blake2b(data).hexdigest()
        if state == "ok":
            h = good
        elif state == "okupper":
            h = good.upper()
        elif state == "mismatch":
            h = good[0] + ("0" if good[1] != "0" else "1") + good[2:]
        elif state == "short":
            h = good[:64]
        elif state == "nonhex":
            h = "z" * 128
        else:
            h = good
        res = rng.choice(["boot()", "boot()", "boot()", "guid(12)", "BOOT()", "$boot()",
                          "$$boot()", "hdd()", "bootx()"])
        val = "%s:/%s#%s" % (res, rel, h)
        if state == "noparen":
            val = rel
        elif state == "nosep":
            val = "boot()%s" % rel
        elif state == "nohash":
            val = "boot():/%s" % rel
        lines.append("%s%s: %s" % (indent, key, val))

    for _ in range(rng.randint(0, 5)):
        lines.append(rng.choice(["timeout: %d" % rng.randint(0, 9), "", "# c", "backdrop: 1a1b26"]))
    if rng.random() < 0.5:
        lines.append("hash_mismatch_panic: " + rng.choice(["no", "No", "yes", "nope", "NO"]))
    if rng.random() < 0.4:
        lines.append("hash_mismatch_panic: " + rng.choice(["no", "yes"]))
    if rng.random() < 0.4:
        lines.append("measured_boot: " + rng.choice(["yes", "no", "Yes", "yes "]))
    for _ in range(rng.randint(1, 4)):
        indent = "" if rng.random() < 0.6 else "  " * rng.randint(1, 2)
        lines.append(indent + "/" + rng.choice(["", "+", "e", "+e", " e"]) +
                     "".join(rng.choice("abcxyz") for _ in range(rng.randint(0, 4))))
        if rng.random() < 0.85:
            lines.append(indent + "protocol: " + rng.choice(["efi", "uefi", "efi_chainload", "linux",
                                                             "EFI", "efi ", "efi_boot_entry"]))
        body_indent = indent + "  "
        for _ in range(rng.randint(0, 3)):
            key = rng.choice(["path", "path", "image_path", "kernel_path", "module_path",
                              "wallpaper", "term_font", "global_dtb", "dtb_path"])
            state = rng.choice(["ok", "mismatch", "missing", "short", "nonhex", "okupper",
                                "noparen", "nosep", "nohash"])
            pathpin(key, state, body_indent)
        if rng.random() < 0.2:
            lines.append(body_indent + "cmdline: quiet")
        if rng.random() < 0.15:
            lines.append(body_indent + "//child")
            pathpin("path", rng.choice(["ok", "missing", "nohash"]), body_indent + "  ")
    eol = "\r\n" if rng.random() < 0.15 else "\n"
    return eol.join(lines) + eol, files


def main():
    mutant = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    gate = os.path.join(S, "mutants", mutant + ".py")
    rng = random.Random(20261107)
    work = tempfile.mkdtemp(prefix="fuzz-", dir=os.environ.get("TMPDIR", S))
    esp = os.path.join(work, "esp")
    diffs = []
    for i in range(n):
        text, files = gen(rng)
        d = os.path.join(work, "c%d" % i)
        os.makedirs(os.path.join(d, "esp"), exist_ok=True)
        for rel, data in files.items():
            p = os.path.join(d, "esp", *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(data)
        conf = os.path.join(d, "limine.conf")
        open(conf, "w", newline="").write(text)
        sb = rng.choice([None, "0", "1"])
        tpm = rng.choice([None, "0", "1"])
        a = gate_out(CANON, conf, os.path.join(d, "esp"), sb, tpm)
        b = gate_out(gate, conf, os.path.join(d, "esp"), sb, tpm)
        if a != b:
            diffs.append({"i": i, "conf": text, "sb": sb, "tpm": tpm, "pristine": a, "mutant": b})
            if len(diffs) >= 3:
                break
    out = {"mutant": mutant, "cases": i + 1, "divergences": len(diffs), "examples": diffs}
    p = os.path.join(S, "jobs", "fuzz-%s.json" % mutant)
    json.dump(out, open(p, "w"), indent=1)
    print("%s cases=%d divergences=%d" % (mutant, i + 1, len(diffs)))
    if diffs:
        e = diffs[0]
        print("first divergence case %d sb=%s tpm=%s" % (e["i"], e["sb"], e["tpm"]))
        for k in FIELDS:
            if e["pristine"].get(k) != e["mutant"].get(k):
                print("  %s: pristine=%s" % (k, json.dumps(e["pristine"].get(k))[:300]))
                print("  %s: mutant  =%s" % (k, json.dumps(e["mutant"].get(k))[:300]))
        print("  conf:\n" + "\n".join("    " + l for l in e["conf"].splitlines()))


if __name__ == "__main__":
    main()
