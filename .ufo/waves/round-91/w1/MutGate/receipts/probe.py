#!/usr/bin/env python3
"""Targeted differential probes: pristine frozen gate vs one mutant, on confs the battery does
not draw. Prints the fields the battery compares plus the raw pin entries."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(S, "canon-frozen.py")
GOOD = b"payload-A"
H = hashlib.blake2b(GOOD).hexdigest()
BAD = H[:-1] + ("0" if H[-1] != "0" else "1")

CONFS = {
    # two VISIBLE (global) hash_mismatch_panic lines: first must win
    "two-global-panic": [
        "timeout: 3",
        "hash_mismatch_panic: yes",
        "hash_mismatch_panic: no",
        "/e",
        "  path: boot():/EFI/Linux/a.efi#%s" % BAD,
    ],
    # measured_boot with a trailing blank: strcmp must NOT match "yes"
    "measured-trailing-blank": [
        "measured_boot: yes   ",
        "/e",
        "  protocol: efi",
        "  path: boot():/EFI/Linux/a.efi#%s" % H,
    ],
    # a bare '/' entry line after a labelled one: cleaned label is empty
    "bare-slash-entry": [
        "timeout: 1",
        "/first",
        "  protocol: efi",
        "  path: boot():/EFI/Linux/a.efi#%s" % BAD,
        "/",
        "  protocol: efi",
        "  path: boot():/EFI/Linux/b.efi#%s" % BAD,
    ],
    # two VISIBLE (global) measured_boot lines: first must win
    "two-global-measured": [
        "timeout: 3",
        "measured_boot: yes",
        "measured_boot: no",
        "/e",
        "  protocol: efi",
        "  path: boot():/EFI/Linux/a.efi#%s" % H,
    ],
    # an indented '//child' line starts a new body (no protocol -> not an efi image)
    "child-body-boundary": [
        "timeout: 1",
        "/e",
        "  protocol: efi",
        "  //child",
        "  path: boot():/EFI/Linux/missing.efi#%s" % BAD,
    ],
    # '):/' before the grouping ')' : resource name is the same, path differs
    "early-uri-sep": [
        "timeout: 1",
        "/e",
        "  path: x):/boot():/EFI/Linux/a.efi#%s" % BAD,
    ],
}


def run(gate, conf, esp, extra):
    p = subprocess.run([sys.executable, gate, "--conf", conf, "--esp", esp] + extra,
                       capture_output=True, text=True, timeout=30)
    try:
        out = json.loads(p.stdout)
    except Exception:
        return {"rc": p.returncode, "stdout": p.stdout[-300:], "stderr": p.stderr[-300:]}
    keep = ("verdict", "rc", "on_panic", "hash_mismatch_panic", "measured_boot",
            "unverified_image_lines")
    res = {k: out.get(k) for k in keep}
    res["pins"] = [(x["line"], x["status"], x["consequence"], x.get("entry")) for x in out.get("pins", [])]
    res["exit"] = p.returncode
    return res


def main():
    mutant = sys.argv[1]
    gate = os.path.join(S, "mutants", mutant + ".py")
    work = tempfile.mkdtemp(prefix="probe-", dir=os.environ.get("TMPDIR", S))
    esp = os.path.join(work, "esp")
    os.makedirs(os.path.join(esp, "EFI", "Linux"))
    for n in ("a.efi", "b.efi"):
        open(os.path.join(esp, "EFI", "Linux", n), "wb").write(GOOD)
    rows = []
    for name, lines in CONFS.items():
        conf = os.path.join(work, name + ".conf")
        open(conf, "w").write("\n".join(lines) + "\n")
        extra = ["--tpm-present", "1"] if name in ("measured-trailing-blank", "two-global-measured") else []
        a = run(CANON, conf, esp, extra)
        b = run(gate, conf, esp, extra)
        rows.append({"probe": name, "differ": a != b, "pristine": a, "mutant": b})
    # unreadable conf
    a = run(CANON, os.path.join(work, "absent.conf"), esp, [])
    b = run(gate, os.path.join(work, "absent.conf"), esp, [])
    rows.append({"probe": "unreadable-conf", "differ": a != b, "pristine": a, "mutant": b})
    json.dump(rows, open(os.path.join(os.environ.get("OUTJSON", os.path.join(S, "jobs", "probe-%s.json" % mutant))), "w"), indent=1)
    for r in rows:
        print("%-24s differ=%s" % (r["probe"], r["differ"]))
        if r["differ"]:
            print("   pristine:", json.dumps(r["pristine"], sort_keys=True))
            print("   mutant  :", json.dumps(r["mutant"], sort_keys=True))


if __name__ == "__main__":
    main()
