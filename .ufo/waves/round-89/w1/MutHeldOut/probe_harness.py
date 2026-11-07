#!/usr/bin/env python3
"""MutHeldOut (round 89) probe harness: build one fixture from a JSON spec, run one gate on it,
print a single JSON object describing what the gate answered.

Usage: probe_harness.py SPEC.json GATE.py

Spec keys (all optional except conf/conf_hex):
  esp_name          name of the ESP directory under the case dir (default "esp")
  files             {relpath: {"size": N} | {"text": STR} | {"hex": HEX}}  written under the ESP
  dirs              [relpath, ...]                    created under the ESP
  symlinks          {relpath: target}                 created under the ESP
  outside_files     {relpath: {"size"|"text"|"hex"}}  written beside the ESP (case dir)
  outside_dirs      [relpath, ...]                    created beside the ESP
  conf              [line, ...]                       conf file lines (joined with \n)
  conf_hex          HEX                              raw conf bytes (wins over conf)
  conf_dir          true                             --conf names a directory
  conf_missing      true                             --conf names an absent file
  sb                null | "0" | "1"                  --secure-boot-enforced flag (absent when null)

Placeholders usable in conf lines: {{B2:REL}} {{FLIP:REL}} {{FLIPV:REL}} for ESP files and
{{B2O:REL}} {{FLIPO:REL}} for outside files (B2 = blake2b-512 hex of the stored bytes; FLIP/FLIPV
flip the last/first hexdigit).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

TIMEOUT = 20


def b2(data):
    return hashlib.blake2b(data).hexdigest()


def flip_last(h):
    c = h[-1]
    return h[:-1] + ("0" if c != "0" else "1")


def flip_first(h):
    c = h[0]
    return ("f" if c != "f" else "e") + h[1:]


def make_bytes(v):
    if "size" in v:
        n = int(v["size"])
        return bytes((i * 37 + 11) % 251 for i in range(n))
    if "text" in v:
        return v["text"].encode()
    return bytes.fromhex(v["hex"])


def write_tree(base, files, dirs, symlinks):
    for rel in dirs:
        os.makedirs(os.path.join(base, *rel.split("/")), exist_ok=True)
    made = {}
    for rel, v in files.items():
        p = os.path.join(base, *rel.split("/"))
        os.makedirs(os.path.dirname(p) or base, exist_ok=True)
        data = make_bytes(v)
        with open(p, "wb") as f:
            f.write(data)
        made[rel] = data
    for rel, target in symlinks.items():
        p = os.path.join(base, *rel.split("/"))
        os.makedirs(os.path.dirname(p) or base, exist_ok=True)
        os.symlink(target, p)
    return made


def subst(text, esp_blobs, out_blobs):
    out = []
    for line in text:
        for rel in sorted(esp_blobs, key=len, reverse=True):
            h = b2(esp_blobs[rel])
            line = (line.replace("{{B2:%s}}" % rel, h).replace("{{FLIP:%s}}" % rel, flip_last(h))
                        .replace("{{FLIPV:%s}}" % rel, flip_first(h)))
        for rel in sorted(out_blobs, key=len, reverse=True):
            h = b2(out_blobs[rel])
            line = (line.replace("{{B2O:%s}}" % rel, h).replace("{{FLIPO:%s}}" % rel, flip_last(h)))
        out.append(line)
    return out


def main():
    spec_path, gate = sys.argv[1], sys.argv[2]
    spec = json.load(open(spec_path))
    root = tempfile.mkdtemp(prefix="probe-")
    try:
        d = os.path.join(root, "case")
        os.makedirs(d)
        esp = os.path.join(d, spec.get("esp_name", "esp"))
        os.makedirs(esp)
        esp_blobs = write_tree(esp, spec.get("files", {}), spec.get("dirs", []), spec.get("symlinks", {}))
        out_blobs = write_tree(d, spec.get("outside_files", {}), spec.get("outside_dirs", []), {})
        conf = os.path.join(d, "limine.conf")
        if spec.get("conf_dir"):
            os.makedirs(conf)
        elif not spec.get("conf_missing"):
            if "conf_hex" in spec:
                raw = bytes.fromhex(spec["conf_hex"])
            else:
                raw = ("\n".join(subst(spec.get("conf", []), esp_blobs, out_blobs)) + "\n").encode()
            with open(conf, "wb") as f:
                f.write(raw)
        argv = [sys.executable, gate, "--conf", conf, "--esp", esp]
        sb = spec.get("sb")
        if sb is not None:
            argv += ["--secure-boot-enforced", sb]
        p = subprocess.run(argv, cwd=d, capture_output=True, text=True, timeout=TIMEOUT)
        rec = {"spec": os.path.basename(spec_path), "gate": os.path.basename(gate),
               "exit": p.returncode, "stderr_tail": p.stderr[-400:]}
        try:
            o = json.loads(p.stdout)
            rec["verdict"] = o.get("verdict")
            rec["rc_field"] = o.get("rc")
            rec["pins"] = [[x.get("line"), x.get("status"), x.get("consequence")] for x in o.get("pins", [])]
            rec["entries"] = {str(x.get("line")): x.get("entry") for x in o.get("pins", []) if "entry" in x}
            rec["panic"] = o.get("hash_mismatch_panic", "<absent>")
        except Exception as e:  # noqa: BLE001
            rec["parse_error"] = "%s: %s" % (type(e).__name__, e)
            rec["stdout_head"] = p.stdout[:400]
        print(json.dumps(rec, sort_keys=True))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
