#!/usr/bin/env python3
"""Differential probe for CriticForgers f04 (R1 key charset: digits admitted).

Random conf + ESP fixtures, both gates = base.py and fx_f04_digits_in_key.py.
Prints whether every (stdout, rc) pair was byte-identical, plus a few sample confs.
"""
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base.py")
F04 = os.path.join(HERE, "fx_f04_digits_in_key.py")

PATH_KEYS = ["path", "kernel_path", "image_path", "module_path", "dtb_path",
             "global_dtb", "wallpaper", "term_font"]
DIGIT_KEYS = ["path2", "module_path1", "hash_mismatch_panic2", "1path", "term_font9",
              "path_2", "PATH2", "hash_mismatch_panic1"]


def hexhash(rnd, n=128):
    return "".join(rnd.choice("0123456789abcdefABCDEF") for _ in range(n))


def uri(rnd, esp_files):
    res = rnd.choice(["boot", "boot", "$boot", "$$boot", "BOOT", "Boot", "guid", "hdd", "odd", "tftp", "fslabel", "uuid"])
    root = rnd.choice(["", "", "2", "GUID-1"])
    if res in ("boot", "$boot", "$$boot") and rnd.random() < 0.7:
        path = rnd.choice(esp_files + ["", "/", "nope"])
        h = rnd.choice([hexhash(rnd), "abc", hexhash(rnd)[:127], hexhash(rnd) + "0",
                        hexhash(rnd).upper(), hexhash(rnd) + "z"])
    else:
        path = rnd.choice(esp_files + [""])
        h = hexhash(rnd)
    return "%s(%s):/%s#%s" % (res, root, path.lstrip("/"), h)


def make_esp(rnd, root):
    files = []
    n = rnd.randint(0, 3)
    for i in range(n):
        d = os.path.join(root, "d%d" % i if rnd.random() < 0.4 else "")
        os.makedirs(d, exist_ok=True)
        name = "f%d%s.bin" % (i, rnd.choice(["", "X", "2"]))
        p = os.path.join(d, name)
        data = os.urandom(rnd.randint(0, 200))
        if rnd.random() < 0.2:
            import gzip
            data = gzip.compress(data)
        with open(p, "wb") as f:
            f.write(data)
        files.append(os.path.relpath(p, root))
    return files


def make_conf(rnd, esp_files):
    lines = []
    for _ in range(rnd.randint(0, 12)):
        r = rnd.random()
        sep = "\r\n" if rnd.random() < 0.3 else "\n"
        if r < 0.10:
            lines.append("/" + rnd.choice(["EFI/BOOT", "linux", " ", "+linux+", "/x"]) + sep.rstrip("\n"))
        elif r < 0.70:
            key = rnd.choice(PATH_KEYS + DIGIT_KEYS + [k.upper() for k in PATH_KEYS[:3]])
            lead = rnd.choice(["", "  ", "\t", " \t"])
            trail = rnd.choice(["", "   ", "\t", " \t"])
            val = uri(rnd, esp_files) if rnd.random() < 0.8 else rnd.choice(["boot:/x", "junk", "", "boot:/x#"])
            lines.append("%s%s:%s%s%s" % (lead, key, rnd.choice(["", " ", "\t"]), val, trail))
        elif r < 0.82:
            v = rnd.choice(["no", "No", "NO", " no ", "yes", "0"])
            lines.append("%s%s: %s" % (rnd.choice(["", "  ", "\t"]),
                                       rnd.choice(["hash_mismatch_panic", "HASH_MISMATCH_PANIC",
                                                   "hash_Mismatch_Panic", "hash_mismatch_panic2"]), v))
        elif r < 0.90:
            lines.append("#path: " + uri(rnd, esp_files))
        else:
            lines.append(rnd.choice(["", "\f", "\v", "=", "path=x", "  ", "\t#c"]))
    text = "\n".join(lines)
    if rnd.random() < 0.2:
        text = text.replace("\n", "\r\n")
    return text


def run(gate, conf, esp, sbe):
    p = subprocess.run([sys.executable, gate, "--conf", conf, "--esp", esp,
                        "--secure-boot-enforced", sbe],
                       capture_output=True, text=True)
    return p.stdout, p.returncode


def main():
    rnd = random.Random(89)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    with tempfile.TemporaryDirectory(prefix="criticf-f04-") as tmp:
        diffs = 0
        samples = []
        for i in range(n):
            case = os.path.join(tmp, "c%d" % i)
            esp = os.path.join(case, "esp")
            os.makedirs(esp, exist_ok=True)
            files = make_esp(rnd, esp)
            conf = os.path.join(case, "conf.ini")
            text = make_conf(rnd, files)
            with open(conf, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            sbe = rnd.choice(["0", "1"])
            a = run(BASE, conf, esp, sbe)
            b = run(F04, conf, esp, sbe)
            if a != b:
                diffs += 1
                if len(samples) < 3:
                    samples.append((text, sbe, a, b))
        print(json.dumps({"cases": n, "differences": diffs,
                          "samples": [{"conf": s[0], "sbe": s[1], "base": s[2], "f04": s[3]}
                                      for s in samples]}, indent=1))
        return 0 if diffs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
