#!/usr/bin/env python3
"""Round-84 C2 battery: does a hibernate-resume gate implement the frozen rule set?

Usage: resume-gate-battery-r84.py --gate PATH [--base FACTS.json] [--random N]

The gate is called as `python3 PATH --facts FILE` (FILE is a resume-facts/1
JSON document written to a fresh, randomly named file under TMPDIR) and must
print one JSON object {"verdict": ..., "findings": [...]} and exit
0 HEALTHY / 1 DEGRADED / 2 CANNOT-EVALUATE.

Frozen gate rules (round-84 declaration; o = resume_offset= value from the
cmdline or None, r = resume= value or None):
  1 r is None                       -> exactly [HR-NO-RESUME-ARG]; nothing else is evaluated
  2 a file-type swap is active (resume_swapfile not null):
      o is None                     -> HR-OFFSET-MISSING
      o, map_swapfile_offset set, differ -> HR-OFFSET-MISMATCH
      swapfile_attrs set, no 'C'    -> HR-SWAPFILE-COW
    swaps empty                     -> HR-NO-ACTIVE-SWAP
  3 resume_dev_majmin set and != sys_power_resume -> HR-SYSFS-DEVICE-MISMATCH
  4 o set and != sys_power_resume_offset           -> HR-SYSFS-OFFSET-MISMATCH
  5 'resume' and 'systemd' both absent from hooks  -> HR-NO-RESUME-HOOK
  6 'resume' and 'encrypt' in hooks, resume first   -> HR-HOOK-BEFORE-ENCRYPT
  7 swaps non-empty and sum((size_kib-used_kib)*1024) < image_size -> HR-SWAP-TOO-SMALL
  8 'disk' not a word of sys_power_state           -> HR-NO-DISK-STATE
  HEALTHY rc0 iff no finding, else DEGRADED rc1 with the sorted finding list;
  schema != resume-facts/1, a missing required key or a wrong type -> rc2
  CANNOT-EVALUATE with findings [].

Families (13): POSITIVE, MALFORMED and one per finding ID. A family passes
iff, on the committed host base AND on every applicable random base, the
gate's (rc, verdict, sorted findings) equals the expected triple exactly,
within 20 s. Bases are random per run (unseeded), so a gate that memorises
the committed base or the battery's cases cannot follow. Target: 13 of 13.
Exit 0 iff 13/13, 1 otherwise, 2 if the base cannot be read.
"""
import argparse
import copy
import json
import os
import random
import shutil
import string
import subprocess
import sys
import tempfile

BASE = ".ufo/waves/round-84/before/host/facts.json"
IDS = ["HR-NO-RESUME-ARG", "HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW",
       "HR-NO-ACTIVE-SWAP", "HR-SYSFS-DEVICE-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH",
       "HR-NO-RESUME-HOOK", "HR-HOOK-BEFORE-ENCRYPT", "HR-SWAP-TOO-SMALL", "HR-NO-DISK-STATE"]
FILE_ONLY = {"HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW", "HR-SYSFS-OFFSET-MISMATCH"}
REQUIRED = ["schema", "cmdline", "swaps", "resume_swapfile", "map_swapfile_offset", "swapfile_attrs",
            "resume_dev_majmin", "sys_power_resume", "sys_power_resume_offset", "sys_power_state",
            "image_size", "hooks"]
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}


def word(rng, n=6):
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(n))


def set_token(cmdline, key, value):
    toks = [t for t in cmdline.split() if not t.startswith(key + "=")]
    if value is not None:
        toks.insert(0, f"{key}={value}")
    return " ".join(toks)


def offset(f):
    for t in f["cmdline"].split():
        if t.startswith("resume_offset="):
            return int(t.split("=", 1)[1])
    return None


def busybox_hooks(rng, resume_after_encrypt=True, with_resume=True):
    h = ["base", "udev"] + (["plymouth"] if rng.random() < .5 else []) + \
        ["autodetect", "microcode", "modconf", "kms", "keyboard", "keymap", "consolefont", "block", "encrypt",
         "filesystems", "fsck"]
    if with_resume:
        enc = h.index("encrypt")
        pos = rng.randint(enc + 1, len(h)) if resume_after_encrypt else rng.randint(2, enc)
        h.insert(pos, "resume")
    return h


def random_base(rng, file_swap):
    o = rng.randint(1, 10 ** 8)
    mm = f"{rng.randint(8, 259)}:{rng.randint(0, 255)}"
    dev = rng.choice([f"/dev/mapper/{word(rng)}", f"/dev/nvme0n1p{rng.randint(1, 9)}", f"/dev/sd{rng.choice('abc')}{rng.randint(1, 9)}"])
    size = rng.randint(8, 64) * 1024 * 1024
    used = rng.randint(0, size // 4)
    free = (size - used) * 1024
    noise = ["quiet", "rw", f"root={dev}", f"{word(rng)}={rng.randint(0, 99)}", "splash"]
    toks = noise + [f"resume={dev}"] + ([f"resume_offset={o}"] if file_swap else [])
    rng.shuffle(toks)
    hooks = busybox_hooks(rng) if rng.random() < .6 else \
        ["base", "systemd", "autodetect", "microcode", "modconf", "kms", "keyboard", "sd-vconsole", "block",
         "sd-encrypt", "filesystems", "fsck"]
    path = f"/{word(rng)}/swapfile" if file_swap else f"/dev/{word(rng, 4)}p{rng.randint(1, 9)}"
    return {
        "schema": "resume-facts/1", "captured_at": f"2026-{rng.randint(1, 12):02d}-01T00:00:00Z",
        "cmdline": " ".join(toks),
        "swaps": [{"path": path, "type": "file" if file_swap else "partition", "size_kib": size, "used_kib": used}],
        "resume_swapfile": path if file_swap else None,
        "map_swapfile_offset": o if file_swap else None,
        "swapfile_attrs": ("-" * rng.randint(3, 15) + "C" + "-" * rng.randint(0, 6)) if file_swap else None,
        "resume_dev_majmin": mm,
        "sys_power_resume": mm,
        "sys_power_resume_offset": o if file_swap else 0,
        "sys_power_state": rng.choice(["freeze mem disk", "mem disk", "freeze disk", "disk"]),
        "sys_power_disk": rng.choice(["[platform] shutdown reboot", "platform [shutdown] reboot"]),
        "image_size": rng.randint(1, int(free * .9)),
        "hooks": hooks,
    }


def perturb(f, fid, rng):
    f = copy.deepcopy(f)
    o = offset(f)
    if fid == "HR-NO-RESUME-ARG":
        f["cmdline"] = set_token(f["cmdline"], "resume", None)
    elif fid == "HR-OFFSET-MISSING":
        f["cmdline"] = set_token(f["cmdline"], "resume_offset", None)
    elif fid == "HR-OFFSET-MISMATCH":
        f["map_swapfile_offset"] = o + rng.randint(1, 1000)
    elif fid == "HR-SWAPFILE-COW":
        f["swapfile_attrs"] = f["swapfile_attrs"].replace("C", "-")
    elif fid == "HR-NO-ACTIVE-SWAP":
        f.update(swaps=[], resume_swapfile=None, map_swapfile_offset=None, swapfile_attrs=None)
    elif fid == "HR-SYSFS-DEVICE-MISMATCH":
        ma, mi = f["resume_dev_majmin"].split(":")
        f["sys_power_resume"] = f"{ma}:{(int(mi) + rng.randint(1, 50)) % 256}"
    elif fid == "HR-SYSFS-OFFSET-MISMATCH":
        f["sys_power_resume_offset"] = o + rng.randint(1, 1000)
    elif fid == "HR-NO-RESUME-HOOK":
        f["hooks"] = busybox_hooks(rng, with_resume=False)
    elif fid == "HR-HOOK-BEFORE-ENCRYPT":
        f["hooks"] = busybox_hooks(rng, resume_after_encrypt=False)
    elif fid == "HR-SWAP-TOO-SMALL":
        free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in f["swaps"])
        f["image_size"] = free + rng.randint(1, 10 ** 9)
    elif fid == "HR-NO-DISK-STATE":
        f["sys_power_state"] = rng.choice(["freeze mem", "mem", "freeze"])
    return f


def malformed(f, rng):
    f = copy.deepcopy(f)
    kind = rng.choice(["drop", "schema", "cmdline-type", "swaps-type", "hooks-type"])
    if kind == "drop":
        del f[rng.choice(REQUIRED)]
    elif kind == "schema":
        f["schema"] = "resume-facts/0"
    elif kind == "cmdline-type":
        f["cmdline"] = rng.randint(0, 9)
    elif kind == "swaps-type":
        f["swaps"] = "none"
    else:
        f["hooks"] = "base udev resume"
    return f, kind


def call(gate, facts, tmp, rng):
    p = os.path.join(tmp, word(rng, 12) + ".json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(facts, fh)
    try:
        r = subprocess.run([sys.executable, gate, "--facts", p], capture_output=True, text=True,
                           timeout=20, env=ENV)
    except FileNotFoundError:
        return (None, None, None), "gate-not-runnable"
    except subprocess.TimeoutExpired:
        return (None, None, None), "timeout"
    finally:
        os.remove(p)
    try:
        out = json.loads(r.stdout)
        return (r.returncode, out.get("verdict"), sorted(out.get("findings") or [])), "ok"
    except Exception:  # noqa: BLE001 - unparseable output is a failed case
        return (r.returncode, None, None), "stdout-not-json"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--random", type=int, default=5)
    a = ap.parse_args(argv)
    try:
        base = json.load(open(a.base, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"verdict": "cannot-evaluate", "reason": f"base-unreadable:{type(e).__name__}"}))
        return 2
    rng = random.Random()
    bases = [("host", base)]
    for i in range(a.random):
        bases.append((f"random{i}", random_base(rng, file_swap=(i % 5) != 4)))
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        gate = os.path.join(tempfile.gettempdir(), "absent-gate-" + word(rng, 8) + ".py")
    tmp = tempfile.mkdtemp(prefix="r84-c2-")
    fams, cases = {}, []
    try:
        for name, b in bases:
            file_base = b.get("resume_swapfile") is not None
            plan = [("POSITIVE", b, (0, "HEALTHY", []))]
            m, kind = malformed(b, rng)
            plan.append(("MALFORMED", m, (2, "CANNOT-EVALUATE", [])))
            for fid in IDS:
                if fid in FILE_ONLY and not file_base:
                    continue
                plan.append((fid, perturb(b, fid, rng), (1, "DEGRADED", [fid])))
            for fam, facts, want in plan:
                got, why = call(gate, facts, tmp, rng)
                ok = why == "ok" and tuple(got) == (want[0], want[1], want[2])
                fams.setdefault(fam, []).append(ok)
                cases.append({"base": name, "family": fam, "want": list(want), "got": list(got), "why": why,
                              "pass": ok, **({"malformed": kind} if fam == "MALFORMED" else {})})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    passed = sorted(f for f, v in fams.items() if all(v))
    failed = sorted(f for f, v in fams.items() if not all(v))
    res = {"families_passed": len(passed), "families_total": len(fams), "target": 13,
           "verdict": "met" if len(passed) == 13 and len(fams) == 13 else "unmet",
           "failed_families": failed, "bases": [n for n, _ in bases], "cases": cases,
           "random_bases": [b for n, b in bases if n != "host"]}
    print(json.dumps(res, indent=1))
    return 0 if res["verdict"] == "met" else 1


if __name__ == "__main__":
    sys.exit(main())
