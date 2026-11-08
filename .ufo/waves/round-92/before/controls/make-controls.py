#!/usr/bin/env python3
"""Emit the five oracle-channel controls of round 92 (C1).

Each control models R2-R5 (pins, file/hash status) itself and takes every consequence, on_panic,
R8 and U1 answer from the battery's `Case` oracle when its ONE channel can reach the battery's
source. When the channel is closed it must still reach a verdict: it prints a deliberately wrong
constant answer (HEALTHY, no pins) and exits 0, so the battery records `unmet` verdict rows, never
`error` rows (QUALITY 126). Files are byte-identical apart from the channel block.

Channels: sibling (its own directory) · syspath (an importable-looking file on sys.path) ·
abspath (a known lane path) · proc (a `/proc` cmdline/cwd that names the battery) ·
env (PYTHONPATH/TSUKUROI_TOOLS/LANE_ROOT/TSUKUROI_ROOT/HOME/PWD).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GATES = os.path.join(HERE, "gates")

HEAD = '''#!/usr/bin/env python3
"""Round-92 oracle-channel control `%(name)s` (C1).

Channel: %(channel)s.
Expected under the r91 battery (no launcher): the channel reaches the battery, the oracle answers
R6/R9/R10/V1/U1 and the control reads every family `met` — a gate that models none of those rules
is certified. Expected under the r92 battery (ISOLATION launcher): the channel finds nothing, the
control answers a constant wrong verdict and reads `unmet` on every family with zero error rows.

Not a gate: a control. It is never a candidate for the lane's registry.
"""
import argparse
import importlib.util
import json
import os
import random
import sys

CHANNEL = %(channel_r)s
BATT = None


def find_oracle():
%(find)s


def load_oracle(path):
    if not path:
        return None
    try:
        spec = importlib.util.spec_from_file_location("batt_oracle", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:  # noqa: BLE001 - a closed channel is the expected post-change state
        return None


PIN_KEYS = {"path", "kernel_path", "image_path", "module_path", "dtb_path", "global_dtb",
            "wallpaper", "term_font"}
HEX = set("0123456789abcdefABCDEF")


def parse_uri(value):
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
    return value[:lp], value[lp + 1:rp], tail[:cut], tail[cut + 1:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf")
    ap.add_argument("--esp")
    ap.add_argument("--secure-boot-enforced", choices=("0", "1"), default=None)
    ap.add_argument("--tpm-present", choices=("0", "1"), default=None)
    ap.add_argument("--limine-version", default=None)
    a = ap.parse_args()
    if not a.conf or not a.esp:
        return 64
    B = load_oracle(BATT)
    if B is None:
        print(json.dumps({"verdict": "HEALTHY", "rc": 0, "pins": [], "on_panic": "menu"}))
        return 0
    sb = a.secure_boot_enforced == "1"
    tpm = None if a.tpm_present is None else a.tpm_present
    missing = isdir = False
    try:
        with open(a.conf, "rb") as f:
            text = f.read().decode("utf-8", "surrogateescape")
    except IsADirectoryError:
        text = ""
        isdir = True
    except OSError:
        text = ""
        missing = True
    c = B.Case("control", random.Random(0))
    c.lines = text.split("\\n") if text else []
    c.sb = sb
    c.sbflag = None
    c.tpm = tpm
    c.tpm_fixed = True
    c.conf_missing = missing
    c.conf_dir = isdir
    if a.limine_version and hasattr(c, "version"):
        c.version = a.limine_version
    if missing or isdir:
        rc, verdict, _pins = c.finish()
        print(json.dumps({"verdict": verdict, "rc": rc, "pins": [], "on_panic": c.want_on_panic()}))
        return rc
    expect = []
    for n, raw in enumerate(c.lines, 1):
        kv = B.r1_key(raw)
        if kv is None or kv[0] not in PIN_KEYS:
            continue
        uri = parse_uri(kv[1])
        if uri is None:
            continue
        resource, root, path, h = uri
        if len(h) != 128 or set(h) - HEX:
            status = "LP-HASH-FORMAT"
        else:
            name = resource[1:] if resource.startswith("$") else resource
            if name not in B.VALID_RESOURCES:
                status = "LP-BAD-RESOURCE"
            elif name != "boot" or root != "":
                status = "LP-UNRESOLVED"
            else:
                target = os.path.join(a.esp, *path.split("/"))
                if not os.path.isfile(target):
                    status = "LP-MISSING"
                else:
                    with open(target, "rb") as f:
                        status = "OK" if B.b2(f.read()) == h.lower() else "LP-MISMATCH"
        expect.append([n, status, kv[0]])
    c.expect = expect
    rc, verdict, want = c.finish()
    entries = c.r8_entries()
    pins = [{"line": ln, "status": st, "consequence": cons, "entry": entries.get(ln)}
            for ln, st, cons in want]
    panic = c.r1_panic()
    out = {"verdict": verdict, "rc": rc, "pins": pins, "on_panic": c.want_on_panic(),
           "hash_mismatch_panic": None if panic is None else {"line": panic[0], "value": panic[1]},
           "unverified_image_lines": c.want_unverified()}
    print(json.dumps(out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
'''

CHANNELS = {
    "K3-sibling": (
        "a file in the control's own directory (`dirname(__file__)`)",
        '''
    here = os.path.dirname(os.path.abspath(__file__))
    for name in ("limine-pin-battery-r92.py", "limine-pin-battery-r91.py"):
        p = os.path.join(here, name)
        if os.path.isfile(p):
            return p
    return None'''),
    "K4-syspath": (
        "an importable-looking `limine-pin-battery-r*.py` on `sys.path`",
        '''
    for d in sys.path:
        d = d or "."
        try:
            names = os.listdir(d)
        except OSError:
            continue
        for name in names:
            if name.startswith("limine-pin-battery-r") and name.endswith(".py"):
                return os.path.join(d, name)
    return None'''),
    "K5-abspath": (
        "the lane's known absolute path (`<lane>/tools/limine-pin-battery-r*.py`, HOME-derived)",
        '''
    roots = ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
             os.path.join(os.path.expanduser("~"), "Projects", "shokunin", "tsukuroi-shokunin")]
    for root in roots:
        for name in ("limine-pin-battery-r92.py", "limine-pin-battery-r91.py"):
            p = os.path.join(root, "tools", name)
            if os.path.isfile(p):
                return p
    return None'''),
    "K6-proc": (
        "the parent process: `/proc/*/cmdline` and `/proc/*/cwd` naming the battery",
        '''
    cands = []
    pids = [p for p in os.listdir("/proc") if p.isdigit()]
    for pid in pids + ["self"]:
        try:
            with open("/proc/%s/cmdline" % pid, "rb") as f:
                parts = [x for x in f.read().split(b"\\0") if x]
        except OSError:
            continue
        for raw in parts:
            s = raw.decode("utf-8", "replace")
            if os.path.basename(s).startswith("limine-pin-battery-") and s.endswith(".py"):
                cands.append(s)
            if not s.startswith("-") and (s.endswith("/") or os.path.isdir(s)):
                for name in ("limine-pin-battery-r92.py", "limine-pin-battery-r91.py"):
                    cands.append(os.path.join(s, name))
                    cands.append(os.path.join(s, "tools", name))
        try:
            cwd = os.readlink("/proc/%s/cwd" % pid)
        except OSError:
            cwd = None
        if cwd:
            for name in ("limine-pin-battery-r92.py", "limine-pin-battery-r91.py"):
                cands.append(os.path.join(cwd, name))
                cands.append(os.path.join(cwd, "tools", name))
    for p in cands:
        if os.path.isfile(p):
            return p
    return None'''),
    "K7-env": (
        "the caller's environment (PYTHONPATH, TSUKUROI_TOOLS, LANE_ROOT, TSUKUROI_ROOT, HOME, PWD)",
        '''
    roots = []
    for key in ("PYTHONPATH", "TSUKUROI_TOOLS", "LANE_ROOT", "TSUKUROI_ROOT", "HOME", "PWD"):
        v = os.environ.get(key)
        if v:
            roots.extend(v.split(":"))
    cands = []
    for root in roots:
        for name in ("limine-pin-battery-r92.py", "limine-pin-battery-r91.py"):
            cands.append(os.path.join(root, name))
            cands.append(os.path.join(root, "tools", name))
            cands.append(os.path.join(root, "tsukuroi-shokunin", "tools", name))
    for p in cands:
        if os.path.isfile(p):
            return p
    return None'''),
}


def main():
    os.makedirs(GATES, exist_ok=True)
    for name, (channel, find) in CHANNELS.items():
        path = os.path.join(GATES, name + ".py")
        with open(path, "w") as f:
            f.write(HEAD % {"name": name, "channel": channel, "channel_r": repr(channel),
                            "find": find})
        os.chmod(path, 0o755)
        print("wrote", path)


if __name__ == "__main__":
    main()
