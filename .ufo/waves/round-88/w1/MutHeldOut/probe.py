#!/usr/bin/env python3
"""Hand-built behavioural probe: every mutant must differ from pristine on at least one fixture.

Compares the battery-visible answer tuple: (process rc, verdict, sorted pins (line,status,
consequence), rc field, entry map for pins that carry it, hash_mismatch_panic presence/value).
A mutant that matches pristine on every fixture is reported EQUIVALENT on this probe space.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
PRIS = os.path.join(S, "pristine.py")
MUT = os.path.join(S, "mutants")
TIMEOUT = 20


def b2(data):
    return hashlib.blake2b(data).hexdigest()


def flip_last(h):
    c = h[-1]
    return h[:-1] + ("0" if c != "0" else "1")


BLOB = b"kernel-a"
H = b2(BLOB)
BAD = flip_last(H)
GZ = b"\x1f\x8b\x08\x00" + b"payload-not-a-real-gzip"
GZH = b2(GZ)
SEP_BLOB = b"sep-file"
SEP_H = b2(SEP_BLOB)


def fixtures():
    """name -> (lines, files, opts)"""
    fx = {}

    def add(name, lines, files=None, **opts):
        fx[name] = (lines, files or {}, opts)

    add("basic", ["timeout: 1", "/e", "protocol: efi", "  path: boot():/a.efi#" + H], {"a.efi": BLOB})
    add("key-eq-sep", ["/e", "  path= boot():/a.efi#" + H], {"a.efi": BLOB})
    add("key-digit-decoy", ["/e", "  path2: boot():/a.efi#" + H, "  2path: boot():/a.efi#" + H,
                            "  path: boot():/a.efi#" + H], {"a.efi": BLOB})
    add("value-tab", ["/e", "  path:\tboot():/a.efi#" + H], {"a.efi": BLOB})
    add("indent-tab", ["/e", "\tpath: boot():/a.efi#" + H], {"a.efi": BLOB})
    add("empty-hash", ["/e", "  path: boot():/a.efi#"], {"a.efi": BLOB})
    add("hash-129", ["/e", "  path: boot():/a.efi#" + H + "a"], {"a.efi": BLOB})
    add("hash-prefix-late-flip", ["/e", "  path: boot():/a.efi#" + BAD], {"a.efi": BLOB})
    add("gz-marker", ["/e", "  module_path: $boot():/a.efi.gz#" + GZH], {"a.efi.gz": GZ})
    add("root-on-boot2", ["/e", "  path: boot(2):/a.efi#" + H], {"a.efi": BLOB})
    add("empty-path", ["/e", "  path: boot():/#" + H])
    add("optional-upper-wallpaper", ["WALLPAPER: boot():/a.efi#" + BAD], {"a.efi": BLOB})
    add("optional-format-wallpaper", ["wallpaper: boot():/a.efi#abc"], {"a.efi": BLOB})
    add("optional-mismatch-term-font", ["term_font: boot():/a.efi#" + BAD], {"a.efi": BLOB})
    add("panic-key-upper", ["HASH_MISMATCH_PANIC: no", "/e", "  path: boot():/a.efi#" + BAD],
        {"a.efi": BLOB})
    add("panic-value-nope", ["hash_mismatch_panic: nope", "/e", "  path: boot():/a.efi#" + BAD],
        {"a.efi": BLOB})
    add("missing-file", ["/e", "  path: boot():/absent.efi#" + H])
    nh = list(H)
    nh[10] = "g"
    add("hash-nonhex-128", ["/e", "  path: boot():/a.efi#" + "".join(nh)], {"a.efi": BLOB})
    add("crlf", ["timeout: 1", "/e", "protocol: efi", "  path: boot():/a.efi#" + H], {"a.efi": BLOB},
        eol="\r\n")
    add("entry-plus", ["/+Global", "  path: boot():/a.efi#" + H], {"a.efi": BLOB})
    add("resource-upper", ["/e", "  path: BOOT():/a.efi#" + H], {"a.efi": BLOB})
    add("key-upper", ["/e", "  PATH: boot():/a.efi#" + H], {"a.efi": BLOB})
    add("conf-dir", ["/e", "  path: boot():/a.efi#" + H], {"a.efi": BLOB}, conf_dir=True)
    add("first-uri-sep", ["/e", "  path: boot():/a):/b.efi#" + SEP_H], {"a):/b.efi": SEP_BLOB})
    add("sb-flag-zero", ["hash_mismatch_panic: no", "/e", "  path: boot():/a.efi#" + BAD],
        {"a.efi": BLOB}, sbflag="0")
    return fx


def build(root, name, lines, files, opts):
    d = tempfile.mkdtemp(prefix="fx-", dir=root)
    esp = os.path.join(d, "ESP")
    os.makedirs(esp)
    for rel, data in files.items():
        p = os.path.join(esp, *rel.split("/"))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    conf = os.path.join(d, "limine.conf")
    if opts.get("conf_dir"):
        os.makedirs(conf)
    else:
        with open(conf, "w", newline="") as f:
            f.write(opts.get("eol", "\n").join(lines) + opts.get("eol", "\n"))
    return d, conf, esp


def run(gate, d, conf, esp, opts):
    argv = [sys.executable, gate, "--conf", conf, "--esp", esp]
    if opts.get("sbflag") is not None:
        argv += ["--secure-boot-enforced", opts["sbflag"]]
    p = subprocess.run(argv, cwd=d, capture_output=True, text=True, timeout=TIMEOUT)
    try:
        out = json.loads(p.stdout)
        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])
        entries = sorted((int(x["line"]), x["entry"]) for x in out["pins"] if "entry" in x)
        panic = ("present", out["hash_mismatch_panic"]) if "hash_mismatch_panic" in out else ("absent", None)
        return (p.returncode, out["verdict"], pins, out["rc"], entries, panic), None
    except Exception as e:  # noqa: BLE001
        return None, "bad-output %s rc=%s stderr=%s" % (type(e).__name__, p.returncode, p.stderr[-160:])


def main():
    gates = [PRIS] + [os.path.join(MUT, m) for m in sorted(os.listdir(MUT)) if m.endswith(".py")]
    root = tempfile.mkdtemp(prefix="probe-", dir=S)
    fx = fixtures()
    results = {}
    try:
        for gate in gates:
            name = os.path.basename(gate)[:-3]
            row = {}
            for fname, (lines, files, opts) in fx.items():
                d, conf, esp = build(root, fname, lines, files, opts)
                try:
                    row[fname] = run(gate, d, conf, esp, opts)
                finally:
                    shutil.rmtree(d, ignore_errors=True)
            results[name] = row
    finally:
        shutil.rmtree(root, ignore_errors=True)
    base = results["pristine"]
    summary = {}
    for name, row in results.items():
        if name == "pristine":
            continue
        diffs = [f for f in fx if row[f] != base[f]]
        summary[name] = diffs
        print("%-32s %s %s" % (name, "DIFFERS" if diffs else "EQUIVALENT", ",".join(diffs) or "-"))
        for f in diffs[:3]:
            print("    %-24s pristine=%s" % (f, json.dumps(base[f], sort_keys=True)[:220]))
            print("    %-24s mutant  =%s" % ("", json.dumps(row[f], sort_keys=True)[:220]))
    with open(os.path.join(S, "probe-results.json"), "w") as f:
        json.dump({"fixtures": sorted(fx), "differs": summary,
                   "answers": {n: {k: v for k, v in r.items()} for n, r in results.items()}}, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
