#!/usr/bin/env python3
"""Round-86 C1 battery: does a hibernate gate implement the frozen resume-facts/2 rule set, r86 parse?

Usage: resume-gate-battery-r86.py --gate PATH [--base FACTS.json] [--random N] [--out FILE]
       resume-gate-battery-r86.py --selftest

Round-86 parse amendment (frozen; Linux v7.2 init/main.c obsolete_checksetup raw 201-228 and
kernel/params.c parameqn raw 86-95: a __setup string matches every token whose first strlen(str)
characters equal it, '-' and '_' compared equal, and the rest of the token, value included, goes
to the setup function; kernel/power/hibernate.c raw 1402-1465: noresume_setup and
nohibernate_setup ignore their argument, resume_setup copies its argument verbatim (an empty
resume= leaves resume_file empty and find_resume_device raw 982-985 returns -ENOENT),
resume_offset_setup keeps the previous value unless sscanf "%llu" converts, which needs a leading
decimal digit (lib/vsprintf.c vsscanf)). Define for a token t and a setup string S:
  t matches S  iff len(t) >= len(S) and t[:len(S)] equals S with every '-' read as '_'.
Then, superseding the round-85 token tests below:
  - "a token equal to `nohibernate`" reads "a token matching `nohibernate`";
  - "a token equal to `noresume`" reads "a token matching `noresume`";
  - "a token `hibernate=V`" reads "a token matching `hibernate=`, V = the rest";
  - r = the rest of the last token matching `resume=`; rule 1 fires when r is None OR r == "";
  - o = int(leading decimal digits) of the last token matching `resume_offset=` whose rest
    starts with a decimal digit; tokens whose rest does not start with a digit are skipped
    (never CANNOT-EVALUATE); o is None when no such token exists.
Everything else is the round-85 rule set below, unchanged.

The gate is called as `python3 PATH --facts FILE` (FILE is a resume-facts/2 JSON
document written under a fresh, randomly named directory below TMPDIR) and must
print one JSON object {"verdict": ..., "findings": [...]} and exit
0 HEALTHY / 1 DEGRADED / 2 CANNOT-EVALUATE.

Frozen rule set (round-85 declaration). resume-facts/2 = resume-facts/1 plus the key
`lockdown` (str or null: the text of /sys/kernel/security/lockdown, null when that
file is absent). Tokens are the whitespace-split words of `cmdline`; o = the value of
the last resume_offset= token or None; r = the value of the last resume= token or None.

  Availability rules, always evaluated (sources: Linux v7.2 kernel/power/hibernate.c
  hibernate_setup/noresume_setup/nohibernate_setup and hibernation_available;
  include/linux/security.h enum lockdown_reason; security/lockdown/lockdown.c):
  A1 a token equal to `nohibernate`, or a token `hibernate=V` where V starts with
     `no` but starts with neither `noresume` nor `nocompress`  -> HR-HIBERNATE-DISABLED
  A2 lockdown is not null and its bracketed word is `integrity` or
     `confidentiality`                                         -> HR-LOCKDOWN-BLOCKS
  A3 a token equal to `noresume`, or a token `hibernate=V` where V starts with
     `noresume`, and A1 did not fire (nohibernate implies noresume) -> HR-NORESUME-ARG
  Resume-chain rules (round-84 rules 1-8, unchanged except rule 1):
  1 r is None -> HR-NO-RESUME-ARG, and rules 2-8 are not evaluated (A1-A3 still are)
  2 a file-type swap is active (resume_swapfile not null):
      o is None                                   -> HR-OFFSET-MISSING
      o and map_swapfile_offset set and differ    -> HR-OFFSET-MISMATCH
      swapfile_attrs set and lacks 'C'            -> HR-SWAPFILE-COW
    swaps empty                                   -> HR-NO-ACTIVE-SWAP
  3 resume_dev_majmin set and != sys_power_resume -> HR-SYSFS-DEVICE-MISMATCH
  4 o set and != sys_power_resume_offset          -> HR-SYSFS-OFFSET-MISMATCH
  5 'resume' and 'systemd' both absent from hooks -> HR-NO-RESUME-HOOK
  6 'resume' and 'encrypt' in hooks, resume first  -> HR-HOOK-BEFORE-ENCRYPT
  7 swaps non-empty and sum((size_kib-used_kib)*1024) < image_size -> HR-SWAP-TOO-SMALL
  8 'disk' not a word of sys_power_state          -> HR-NO-DISK-STATE
  HEALTHY rc0 iff no finding, else DEGRADED rc1 with the sorted, duplicate-free finding
  list. CANNOT-EVALUATE rc2 with findings [] when: schema != resume-facts/2 (resume-facts/1
  included); a required key is missing or has the wrong type (round-84 types; lockdown
  str or null); lockdown is a string without exactly one whitespace-separated word of
  the form [x].

Families (30 = the 20 round-85 families plus 10 round-86 families): POSITIVE, MALFORMED, one per finding ID (14), MULTI-FAULT (3-6 independent
faults, at least one availability and two resume-chain), PREC-NOHIB (A1 with A3 tokens
present -> only HR-HIBERNATE-DISABLED), PREC-DECOYS (hibernate=nocompress,
hibernate.compressor=, resumewait, <mod>.noresume=1, <mod>.nohibernate=1 -> HEALTHY),
PREC-NO-RESUME-ARG (no resume= plus resume-chain faults plus an availability fault ->
only the availability finding and HR-NO-RESUME-ARG).

Round-86 families (cases per base): NORESUME-VALUED (1: noresume=<v> or noresume<suffix> ->
HR-NORESUME-ARG), NOHIB-VALUED (1: nohibernate=<v> or nohibernate<suffix>, half the time with a
noresume token -> HR-HIBERNATE-DISABLED), EMPTY-RESUME (1: the last resume= token is empty, plus
1-3 suppressed chain faults -> HR-NO-RESUME-ARG), OFFSET-DUP (file bases, 2: a wrong
resume_offset= before the right one -> HEALTHY; after it -> HR-OFFSET-MISMATCH +
HR-SYSFS-OFFSET-MISMATCH), OFFSET-SSCANF (file bases, 3, all HEALTHY: a trailing
resume_offset=<rest without a leading digit> is skipped; resume_offset=<o><letters> reads o;
resume-offset=<o> matches), HIBERNATE-NOX (3: hibernate=no<x> with x not starting r/c ->
HR-HIBERNATE-DISABLED, hibernate=noresume<x> -> HR-NORESUME-ARG, hibernate=nocompress<x> ->
HEALTHY), SWAP-BOUNDARY (2: free == image_size -> HEALTHY; image_size == free + 1 ->
HR-SWAP-TOO-SMALL), MULTI-SWAP (2, 2-3 swaps: max single free < image_size <= sum -> HEALTHY;
image_size > sum -> HR-SWAP-TOO-SMALL), BOOL-FOR-INT (1: true/false in image_size,
sys_power_resume_offset, map_swapfile_offset or a swap's size_kib/used_kib -> CANNOT-EVALUATE),
DECOYS-R86 (1: all of no_resume, noresum, nohibernat, xnoresume, ynohibernate,
resume_offsetx=<n>, resumedelay=<n> -> HEALTHY).

QUALITY 117/119: every case of every base is generated first, then the whole list is
shuffled with an OS-entropy RNG, so the call order differs per run and no position
counter can answer; bases are random per run besides the committed host base; case
files get random names in a random directory. A family passes iff every one of its
cases returns exactly the expected (rc, verdict, sorted findings) within 20 s.
Target: 30 of 30. Exit 0 iff 30/30, 1 otherwise, 2 if the base cannot be read.
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

BASE = ".ufo/waves/round-85/before/host/facts-v2.json"  # unchanged r85 host base
SCHEMA = "resume-facts/2"
AVAIL = ["HR-HIBERNATE-DISABLED", "HR-LOCKDOWN-BLOCKS", "HR-NORESUME-ARG"]
CHAIN = ["HR-NO-RESUME-ARG", "HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW",
         "HR-NO-ACTIVE-SWAP", "HR-SYSFS-DEVICE-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH",
         "HR-NO-RESUME-HOOK", "HR-HOOK-BEFORE-ENCRYPT", "HR-SWAP-TOO-SMALL", "HR-NO-DISK-STATE"]
IDS = AVAIL + CHAIN
FILE_ONLY = {"HR-OFFSET-MISSING", "HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW", "HR-SYSFS-OFFSET-MISMATCH"}
# Independent resume-chain faults for MULTI-FAULT / PREC-NO-RESUME-ARG: each edits a field no
# other member reads; at most one member of each exclusive group is drawn.
MULTI_CHAIN = ["HR-OFFSET-MISMATCH", "HR-SWAPFILE-COW", "HR-SYSFS-DEVICE-MISMATCH",
               "HR-SYSFS-OFFSET-MISMATCH", "HOOKS", "HR-SWAP-TOO-SMALL", "HR-NO-DISK-STATE"]
REQUIRED = ["schema", "cmdline", "swaps", "resume_swapfile", "map_swapfile_offset", "swapfile_attrs",
            "resume_dev_majmin", "sys_power_resume", "sys_power_resume_offset", "sys_power_state",
            "image_size", "hooks", "lockdown"]
FAMILIES = ["POSITIVE", "MALFORMED"] + IDS + ["MULTI-FAULT", "PREC-NOHIB", "PREC-DECOYS",
                                               "PREC-NO-RESUME-ARG"]
R86 = ["NORESUME-VALUED", "NOHIB-VALUED", "EMPTY-RESUME", "OFFSET-DUP", "OFFSET-SSCANF", "HIBERNATE-NOX",
       "SWAP-BOUNDARY", "MULTI-SWAP", "BOOL-FOR-INT", "DECOYS-R86"]
FAMILIES = FAMILIES + R86
TARGET = len(FAMILIES)
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
LOCK_OPEN = ["[none] integrity confidentiality", None]
LOCK_SHUT = ["none [integrity] confidentiality", "none integrity [confidentiality]"]


def word(rng, n=6):
    return "".join(rng.choice(string.ascii_lowercase) for _ in range(n))


def set_token(cmdline, key, value):
    toks = [t for t in cmdline.split() if not t.startswith(key + "=")]
    if value is not None:
        toks.insert(0, f"{key}={value}")
    return " ".join(toks)


def add_tokens(cmdline, rng, *new):
    toks = cmdline.split()
    for t in new:
        toks.insert(rng.randint(0, len(toks)), t)
    return " ".join(toks)


def offset(f):
    o = None
    for t in f["cmdline"].split():
        if t.startswith("resume_offset="):
            o = int(t.split("=", 1)[1])
    return o


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
    dev = rng.choice([f"/dev/mapper/{word(rng)}", f"/dev/nvme0n1p{rng.randint(1, 9)}",
                      f"/dev/sd{rng.choice('abc')}{rng.randint(1, 9)}"])
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
        "schema": SCHEMA, "captured_at": f"2026-{rng.randint(1, 12):02d}-01T00:00:00Z",
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
        "lockdown": rng.choice(LOCK_OPEN),
    }


def perturb(f, fid, rng):
    """Apply one fault in place-safe copy. 'HOOKS' draws one of the two hook faults."""
    f = copy.deepcopy(f)
    o = offset(f)
    if fid == "HR-HIBERNATE-DISABLED":
        f["cmdline"] = add_tokens(f["cmdline"], rng, rng.choice(["nohibernate", "hibernate=no"]))
    elif fid == "HR-LOCKDOWN-BLOCKS":
        f["lockdown"] = rng.choice(LOCK_SHUT)
    elif fid == "HR-NORESUME-ARG":
        f["cmdline"] = add_tokens(f["cmdline"], rng, rng.choice(["noresume", "hibernate=noresume"]))
    elif fid == "HR-NO-RESUME-ARG":
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
    else:
        raise ValueError(fid)
    return f


def chain_faults(f, rng, k, file_base):
    """Apply k independent resume-chain faults; return (facts, ids)."""
    pool = [x for x in MULTI_CHAIN if file_base or x not in FILE_ONLY]
    picks = rng.sample(pool, min(k, len(pool)))
    ids = []
    for p in picks:
        fid = rng.choice(["HR-NO-RESUME-HOOK", "HR-HOOK-BEFORE-ENCRYPT"]) if p == "HOOKS" else p
        f = perturb(f, fid, rng)
        ids.append(fid)
    return f, ids


def avail_faults(f, rng, k):
    """Apply k (1 or 2) availability faults that do not suppress each other; return (facts, ids)."""
    pool = [["HR-LOCKDOWN-BLOCKS"], [rng.choice(["HR-HIBERNATE-DISABLED", "HR-NORESUME-ARG"])]]
    rng.shuffle(pool)
    ids = []
    for grp in pool[:k]:
        f = perturb(f, grp[0], rng)
        ids.append(grp[0])
    return f, ids


def malformed(f, rng):
    f = copy.deepcopy(f)
    kind = rng.choice(["drop", "schema-v0", "schema-v1", "cmdline-type", "swaps-type", "hooks-type",
                       "lockdown-type", "lockdown-unbracketed", "lockdown-two-brackets"])
    if kind == "drop":
        del f[rng.choice(REQUIRED)]
    elif kind == "schema-v0":
        f["schema"] = "resume-facts/0"
    elif kind == "schema-v1":
        f["schema"] = "resume-facts/1"
    elif kind == "cmdline-type":
        f["cmdline"] = rng.randint(0, 9)
    elif kind == "swaps-type":
        f["swaps"] = "none"
    elif kind == "hooks-type":
        f["hooks"] = "base udev resume"
    elif kind == "lockdown-type":
        f["lockdown"] = rng.choice([0, ["none"], True])
    elif kind == "lockdown-unbracketed":
        f["lockdown"] = "none integrity confidentiality"
    else:
        f["lockdown"] = "[none] [integrity] confidentiality"
    return f, kind


def plan_base(name, b, rng):
    file_base = b.get("resume_swapfile") is not None
    b = copy.deepcopy(b)
    plan = [("POSITIVE", b, (0, "HEALTHY", []), {})]
    for _ in range(2):
        m, kind = malformed(b, rng)
        plan.append(("MALFORMED", m, (2, "CANNOT-EVALUATE", []), {"malformed": kind}))
    for fid in IDS:
        if fid in FILE_ONLY and not file_base:
            continue
        plan.append((fid, perturb(b, fid, rng), (1, "DEGRADED", [fid]), {}))
    for _ in range(3):
        f, a_ids = avail_faults(b, rng, rng.randint(1, 2))
        f, c_ids = chain_faults(f, rng, rng.randint(2, 4), file_base)
        plan.append(("MULTI-FAULT", f, (1, "DEGRADED", sorted(set(a_ids + c_ids))), {}))
    f = add_tokens(b["cmdline"], rng, rng.choice(["nohibernate", "hibernate=no"]),
                   rng.choice(["noresume", "hibernate=noresume"]))
    plan.append(("PREC-NOHIB", dict(b, cmdline=f), (1, "DEGRADED", ["HR-HIBERNATE-DISABLED"]), {}))
    decoys = ["hibernate=nocompress", f"hibernate.compressor={rng.choice(['lzo', 'lz4'])}", "resumewait",
              f"{word(rng, 5)}.noresume=1", f"{word(rng, 5)}.nohibernate=1"]
    rng.shuffle(decoys)
    plan.append(("PREC-DECOYS", dict(b, cmdline=add_tokens(b["cmdline"], rng, *decoys[:rng.randint(3, 5)])),
                 (0, "HEALTHY", []), {}))
    f, c_ids = chain_faults(b, rng, rng.randint(2, 3), file_base)
    f, a_ids = avail_faults(f, rng, 1)
    f = perturb(f, "HR-NO-RESUME-ARG", rng)
    plan.append(("PREC-NO-RESUME-ARG", f, (1, "DEGRADED", sorted(a_ids + ["HR-NO-RESUME-ARG"])),
                 {"suppressed": c_ids}))
    plan += plan_r86(b, rng)
    return [{"base": name, "family": fam, "facts": facts, "want": want, **extra}
            for fam, facts, want, extra in plan]

def put_after(cmdline, key, tok):
    """Insert tok right after the last token starting with key (else at a random spot is not used)."""
    toks = cmdline.split()
    idx = max(i for i, t in enumerate(toks) if t.startswith(key))
    toks.insert(idx + 1, tok)
    return " ".join(toks)


def put_before(cmdline, key, tok):
    toks = cmdline.split()
    idx = min(i for i, t in enumerate(toks) if t.startswith(key))
    toks.insert(idx, tok)
    return " ".join(toks)


def replace_tok(cmdline, key, tok):
    return " ".join(tok if t.startswith(key) else t for t in cmdline.split())


INT_FIELDS = ["image_size", "sys_power_resume_offset", "map_swapfile_offset", "size_kib", "used_kib"]


def plan_r86(b, rng):
    file_base = b.get("resume_swapfile") is not None
    o = offset(b)
    out = []
    v = rng.choice(["=1", "=0", "=" + word(rng, 3), "_" + word(rng, 3), word(rng, 2), "="])
    out.append(("NORESUME-VALUED", dict(b, cmdline=add_tokens(b["cmdline"], rng, "noresume" + v)),
                (1, "DEGRADED", ["HR-NORESUME-ARG"]), {"token": "noresume" + v}))
    v = rng.choice(["=1", "=0", "=" + word(rng, 3), "_" + word(rng, 3), word(rng, 2)])
    extra = ["nohibernate" + v] + ([rng.choice(["noresume=1", "noresume"])] if rng.random() < .5 else [])
    out.append(("NOHIB-VALUED", dict(b, cmdline=add_tokens(b["cmdline"], rng, *extra)),
                (1, "DEGRADED", ["HR-HIBERNATE-DISABLED"]), {"tokens": extra}))
    f, c_ids = chain_faults(b, rng, rng.randint(1, 3), file_base)
    if rng.random() < .5:
        cl = replace_tok(f["cmdline"], "resume=", "resume=")
    else:
        cl = put_after(f["cmdline"], "resume=", "resume=")
    out.append(("EMPTY-RESUME", dict(f, cmdline=cl), (1, "DEGRADED", ["HR-NO-RESUME-ARG"]), {"suppressed": c_ids}))
    if file_base:
        wrong = o + rng.randint(1, 10 ** 6)
        out.append(("OFFSET-DUP", dict(b, cmdline=put_before(b["cmdline"], "resume_offset=", f"resume_offset={wrong}")),
                    (0, "HEALTHY", []), {"order": "wrong-first"}))
        out.append(("OFFSET-DUP", dict(b, cmdline=put_after(b["cmdline"], "resume_offset=", f"resume_offset={wrong}")),
                    (1, "DEGRADED", ["HR-OFFSET-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH"]), {"order": "wrong-last"}))
        junk = rng.choice([word(rng, 4), "x" + str(o + 7), "", "-" + str(o + 3), "+" + str(o + 5)])
        for kind, cl in (("trailing-nondigit", put_after(b["cmdline"], "resume_offset=", "resume_offset=" + junk)),
                         ("digit-prefix", replace_tok(b["cmdline"], "resume_offset=", f"resume_offset={o}{word(rng, 3)}")),
                         ("dash", replace_tok(b["cmdline"], "resume_offset=", f"resume-offset={o}"))):
            out.append(("OFFSET-SSCANF", dict(b, cmdline=cl), (0, "HEALTHY", []), {"kind": kind}))
    for kind, want in (("no", (1, "DEGRADED", ["HR-HIBERNATE-DISABLED"])), ("noresume", (1, "DEGRADED", ["HR-NORESUME-ARG"])),
                       ("nocompress", (0, "HEALTHY", []))):
        sfx = word(rng, 3)
        while kind == "no" and sfx[0] in "rc":
            sfx = word(rng, 3)
        out.append(("HIBERNATE-NOX", dict(b, cmdline=add_tokens(b["cmdline"], rng, f"hibernate={kind}{sfx}")), want, {}))
    free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in b["swaps"])
    if free > 0:
        out.append(("SWAP-BOUNDARY", dict(b, image_size=free), (0, "HEALTHY", []), {}))
        out.append(("SWAP-BOUNDARY", dict(b, image_size=free + 1), (1, "DEGRADED", ["HR-SWAP-TOO-SMALL"]), {}))
    if b["swaps"]:
        extra_sw = []
        for _ in range(rng.randint(1, 2)):
            size = rng.randint(4, 32) * 1024 * 1024
            extra_sw.append({"path": f"/dev/zram{rng.randint(0, 3)}", "type": "partition", "size_kib": size,
                             "used_kib": rng.randint(0, size // 4)})
        sw = copy.deepcopy(b["swaps"]) + extra_sw
        rng.shuffle(sw)
        frees = [(s["size_kib"] - s["used_kib"]) * 1024 for s in sw]
        total = sum(frees)
        out.append(("MULTI-SWAP", dict(copy.deepcopy(b), swaps=sw, image_size=rng.randint(1, max(frees))),
                    (0, "HEALTHY", []), {}))
        out.append(("MULTI-SWAP", dict(copy.deepcopy(b), swaps=sw, image_size=total + rng.randint(1, 10 ** 9)),
                    (1, "DEGRADED", ["HR-SWAP-TOO-SMALL"]), {}))
    f = copy.deepcopy(b)
    field = rng.choice(INT_FIELDS)
    if field in ("size_kib", "used_kib") and not f["swaps"]:
        field = "image_size"
    if field in ("size_kib", "used_kib"):
        f["swaps"][0][field] = rng.choice([True, False])
    else:
        f[field] = rng.choice([True, False])
    out.append(("BOOL-FOR-INT", f, (2, "CANNOT-EVALUATE", []), {"field": field}))
    pool = ["no_resume", "noresum", "nohibernat", "x" + "noresume", "y" + "nohibernate",
            f"resume_offsetx={rng.randint(1, 99)}", f"resumedelay={rng.randint(1, 9)}"]
    out.append(("DECOYS-R86", dict(b, cmdline=add_tokens(b["cmdline"], rng, *pool)),
                (0, "HEALTHY", []), {}))
    return out


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
        if os.path.exists(p):
            os.remove(p)
    try:
        out = json.loads(r.stdout)
        findings = out.get("findings")
        if not isinstance(findings, list):
            return (r.returncode, out.get("verdict"), None), "findings-not-list"
        return (r.returncode, out.get("verdict"), list(findings)), "ok"
    except Exception:  # noqa: BLE001 - unparseable output is a failed case
        return (r.returncode, None, None), "stdout-not-json"


SELFTEST_GATES = {
    # name: (gate source, expected battery rc, families that must fail)
    "absent": (None, 1, FAMILIES),
    "const-healthy": ('import json\nprint(json.dumps({"verdict": "HEALTHY", "findings": []}))\n', 1,
                      [f for f in FAMILIES if f not in ("POSITIVE", "PREC-DECOYS", "DECOYS-R86", "OFFSET-SSCANF")]),
    "not-json": ('print("HEALTHY")\n', 1, FAMILIES),
}


def selftest():
    """Self-invocation over isolated gates: assert battery rc and the failed-family set."""
    work = tempfile.mkdtemp(prefix="battery-r86-selftest-")
    bad = []
    try:
        for name, (src, want_rc, must_fail) in SELFTEST_GATES.items():
            g = os.path.join(work, name + ".py")
            if src is not None:
                with open(g, "w", encoding="utf-8") as fh:
                    fh.write(src)
            out = os.path.join(work, name + ".json")
            rc = main(["--gate", g, "--random", "2", "--out", out], quiet=True)
            with open(out, encoding="utf-8") as fh:
                res = json.load(fh)
            missing = sorted(set(must_fail) - set(res["failed_families"]))
            ok = rc == want_rc and not missing and res["families_total"] == TARGET
            print(json.dumps({"case": name, "rc": rc, "want_rc": want_rc, "missing_failures": missing,
                              "pass": ok}, sort_keys=True))
            if not ok:
                bad.append(name)
        rc = main(["--gate", os.path.join(work, "absent.py"), "--base", os.path.join(work, "no-base.json")],
                  quiet=True)
        ok = rc == 2
        print(json.dumps({"case": "base-unreadable", "rc": rc, "want_rc": 2, "pass": ok}, sort_keys=True))
        if not ok:
            bad.append("base-unreadable")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"selftest": "PASS" if not bad else "FAIL", "failed": bad}, sort_keys=True))
    return 0 if not bad else 1


def main(argv=None, quiet=False):
    if argv is None and sys.argv[1:] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--random", type=int, default=5)
    ap.add_argument("--out", help="write the full JSON result here; stdout gets the summary only")
    a = ap.parse_args(argv)
    try:
        with open(a.base, encoding="utf-8") as fh:
            base = json.load(fh)
        if base.get("schema") != SCHEMA:
            raise ValueError("base-schema")
    except Exception as e:  # noqa: BLE001
        if not quiet:
            print(json.dumps({"verdict": "cannot-evaluate", "reason": f"base-unreadable:{type(e).__name__}"}))
        return 2
    rng = random.SystemRandom()
    bases = [("host", base)] + [(f"random{i}", random_base(rng, file_swap=(i % 5) != 4)) for i in range(a.random)]
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        gate = os.path.join(tempfile.gettempdir(), "absent-gate-" + word(rng, 8) + ".py")
    cases = [c for name, b in bases for c in plan_base(name, b, rng)]
    rng.shuffle(cases)
    tmp = tempfile.mkdtemp(prefix=word(rng, 10) + "-")
    fams = {f: [] for f in FAMILIES}
    try:
        for i, c in enumerate(cases):
            got, why = call(gate, c["facts"], tmp, rng)
            want = c["want"]
            ok = why == "ok" and got == (want[0], want[1], want[2])
            fams[c["family"]].append(ok)
            c.update(order=i, got=list(got), why=why, want=list(want), passed=ok)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    passed = sorted(f for f, v in fams.items() if v and all(v))
    failed = sorted(f for f in FAMILIES if f not in passed)
    summary = {"families_passed": len(passed), "families_total": len(FAMILIES), "target": TARGET,
               "verdict": "met" if len(passed) == TARGET else "unmet", "failed_families": failed,
               "cases": len(cases), "bases": [n for n, _ in bases],
               "order_head": [c["family"] for c in sorted(cases, key=lambda c: c["order"])[:5]]}
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump({**summary, "case_log": sorted(cases, key=lambda c: c["order"])}, fh, indent=1)
    if not quiet:
        print(json.dumps(summary, sort_keys=True))
    return 0 if summary["verdict"] == "met" else 1


if __name__ == "__main__":
    sys.exit(main())
