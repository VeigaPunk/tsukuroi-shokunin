#!/usr/bin/env python3
"""Differential harness: clean-room gate vs candidate gate (round-84 C2).

Imports the frozen battery tools/resume-gate-battery-r84.py as a module for
random_base/perturb/malformed, adds hand-built edge cases, and compares the
two gates' (rc, verdict, sorted findings) on every document.

Usage: diff_runner.py --cleanroom PATH --candidate PATH --out diffs.json
"""
import argparse
import copy
import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", ".."))
BATTERY = os.path.join(REPO, "tools", "resume-gate-battery-r84.py")
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
TIMEOUT = 20
CAP = 50


def load_battery():
    spec = importlib.util.spec_from_file_location("r84battery", BATTERY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_gate(gate, facts, tmp):
    fd, path = tempfile.mkstemp(dir=tmp, suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(facts, fh)
    try:
        p = subprocess.run([sys.executable, gate, "--facts", path], capture_output=True,
                           text=True, timeout=TIMEOUT, env=ENV)
    except subprocess.TimeoutExpired:
        return {"rc": None, "verdict": None, "findings": None, "why": "timeout"}
    except OSError as e:
        return {"rc": None, "verdict": None, "findings": None, "why": f"oserror:{e}"}
    finally:
        os.unlink(path)
    out = {"rc": p.returncode, "stdout": p.stdout[:800], "stderr": p.stderr[:800]}
    try:
        d = json.loads(p.stdout)
        out.update(verdict=d.get("verdict"), findings=sorted(d.get("findings") or []), why="ok")
    except Exception:  # noqa: BLE001
        out.update(verdict=None, findings=None, why="stdout-not-json")
    return out


def key(r):
    return (r["rc"], r["verdict"], tuple(r["findings"]) if r["findings"] is not None else None, r["why"])


def cases(bat, rng):
    """Yield (category, name, facts) documents."""
    out = []
    bases = [("host", json.load(open(os.path.join(REPO, ".ufo/waves/round-84/before/host/facts.json"),
                                     encoding="utf-8")))]
    for i in range(120):
        bases.append((f"rnd{i}", bat.random_base(rng, file_swap=(i % 5) != 4)))

    # battery-shaped corpus
    for name, b in bases:
        out.append(("battery", f"{name}/POSITIVE", copy.deepcopy(b)))
        m, kind = bat.malformed(b, rng)
        out.append(("battery", f"{name}/MALFORMED-{kind}", m))
        file_base = b.get("resume_swapfile") is not None
        for fid in bat.IDS:
            if fid in bat.FILE_ONLY and not file_base:
                continue
            out.append(("battery", f"{name}/{fid}", bat.perturb(b, fid, rng)))

    # exhaustive drop/type variants on a subset of bases
    for name, b in bases[:16]:
        for k in bat.REQUIRED:
            d = copy.deepcopy(b)
            del d[k]
            out.append(("drop-key", f"{name}/drop-{k}", d))
        variants = [
            ("schema-space", {"schema": b["schema"] + " "}),
            ("schema-null", {"schema": None}),
            ("schema-int", {"schema": 1}),
            ("cmdline-null", {"cmdline": None}),
            ("cmdline-int", {"cmdline": 7}),
            ("cmdline-empty", {"cmdline": ""}),
            ("swaps-null", {"swaps": None}),
            ("swaps-str", {"swaps": "none"}),
            ("swaps-elem-str", {"swaps": ["/swap/swapfile"]}),
            ("swaps-elem-missing-used", {"swaps": [{"path": "/swap/swapfile", "size_kib": 10}]}),
            ("swaps-elem-float", {"swaps": [{"size_kib": 10.0, "used_kib": 0}]}),
            ("hooks-null", {"hooks": None}),
            ("hooks-str", {"hooks": "base udev resume"}),
            ("hooks-tuple", {"hooks": ["base", "resume"]}),
            ("hooks-elem-int", {"hooks": ["base", 1, "resume"]}),
            ("image-size-float", {"image_size": 1.5}),
            ("image-size-bool", {"image_size": True}),
            ("offset-float", {"map_swapfile_offset": 1.0}),
            ("resume-dev-int", {"resume_dev_majmin": 253}),
            ("sysfs-resume-int", {"sys_power_resume": 253}),
            ("sysfs-offset-str", {"sys_power_resume_offset": "3795013"}),
            ("swapfile-attrs-int", {"swapfile_attrs": 1}),
            ("sysfs-state-null", {"sys_power_state": None}),
        ]
        for tag, patch in variants:
            d = copy.deepcopy(b)
            d.update(patch)
            out.append(("type", f"{name}/{tag}", d))

    # hand-built semantic edge cases, against the host base and 2 random bases
    edge_bases = [bases[0], bases[1], bases[2]]
    for name, b in edge_bases:
        bool_file = b.get("resume_swapfile") is not None
        o = bat.offset(b)

        def mut(tag, fn):
            d = copy.deepcopy(b)
            fn(d)
            out.append(("edge", f"{name}/{tag}", d))

        # multiple swaps: a second, healthy partition entry
        def two_swaps(d):
            d["swaps"] = d["swaps"] + [{"path": "/dev/sdb2", "type": "partition",
                                        "size_kib": 4 * 1024 * 1024, "used_kib": 0}]
        mut("multi-swap-ok", two_swaps)

        def two_swaps_tight(d):
            d["swaps"] = d["swaps"] + [{"path": "/dev/sdb2", "type": "partition",
                                        "size_kib": 1024, "used_kib": 1024}]
            free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in d["swaps"])
            d["image_size"] = free + 1
        mut("multi-swap-tight", two_swaps_tight)

        # duplicate tokens
        def dup_resume_second_wrong(d):
            d["cmdline"] = d["cmdline"] + " resume=/dev/does-not-exist"
        mut("dup-resume-second-wrong", dup_resume_second_wrong)

        def dup_resume_first_wrong(d):
            toks = [t for t in d["cmdline"].split() if not t.startswith("resume=")]
            d["cmdline"] = "resume=/dev/does-not-exist " + " ".join(toks)
        mut("dup-resume-first-wrong", dup_resume_first_wrong)

        def dup_offset_second_wrong(d):
            d["cmdline"] = d["cmdline"] + " resume_offset=1"
        mut("dup-offset-second-wrong", dup_offset_second_wrong)

        def dup_offset_first_wrong(d):
            toks = [t for t in d["cmdline"].split() if not t.startswith("resume_offset=")]
            d["cmdline"] = "resume_offset=1 " + " ".join(toks)
        mut("dup-offset-first-wrong", dup_offset_first_wrong)

        if o is not None:
            def bad_offset(d):
                toks = [t for t in d["cmdline"].split() if not t.startswith("resume_offset=")]
                d["cmdline"] = " ".join(toks + ["resume_offset=abc"])
            mut("offset-nonnumeric", bad_offset)

            def negative_offset(d):
                toks = [t for t in d["cmdline"].split() if not t.startswith("resume_offset=")]
                d["cmdline"] = " ".join(toks + ["resume_offset=-5"])
            mut("offset-negative", negative_offset)

            def plus_offset(d):
                toks = [t for t in d["cmdline"].split() if not t.startswith("resume_offset=")]
                d["cmdline"] = " ".join(toks + [f"resume_offset=+{o}"])
            mut("offset-plus", plus_offset)

            def empty_offset(d):
                toks = [t for t in d["cmdline"].split() if not t.startswith("resume_offset=")]
                d["cmdline"] = " ".join(toks + ["resume_offset="])
            mut("offset-empty", empty_offset)

        def empty_resume(d):
            toks = [t for t in d["cmdline"].split() if not t.startswith("resume=")]
            d["cmdline"] = " ".join(toks + ["resume="])
            d["resume_swapfile"] = None
            d["map_swapfile_offset"] = None
            d["swapfile_attrs"] = None
        mut("resume-empty-value", empty_resume)

        # whitespace in sysfs values
        mut("sysfs-resume-leading-space", lambda d: d.update(sys_power_resume=" " + str(d["sys_power_resume"])))
        mut("sysfs-resume-trailing-nl", lambda d: d.update(sys_power_resume=str(d["sys_power_resume"]) + "\n"))
        mut("sysfs-resume-empty", lambda d: d.update(sys_power_resume=""))
        mut("sysfs-resume-null", lambda d: d.update(sys_power_resume=None))
        mut("sysfs-offset-null", lambda d: d.update(sys_power_resume_offset=None))
        mut("sysfs-offset-zero", lambda d: d.update(sys_power_resume_offset=0))
        mut("resume-dev-null", lambda d: d.update(resume_dev_majmin=None))

        # hooks shapes
        mut("hooks-empty", lambda d: d.update(hooks=[]))
        mut("hooks-systemd-only", lambda d: d.update(hooks=["base", "systemd", "block"]))
        mut("hooks-sd-encrypt-before-resume",
            lambda d: d.update(hooks=["base", "systemd", "sd-encrypt", "resume", "filesystems"]))
        mut("hooks-encrypt-before-resume",
            lambda d: d.update(hooks=["base", "encrypt", "resume"]))
        mut("hooks-resume-only", lambda d: d.update(hooks=["resume"]))
        mut("hooks-duplicate-resume-after-encrypt",
            lambda d: d.update(hooks=["base", "resume", "encrypt", "resume"]))

        # image_size / swap headroom
        mut("image-size-zero", lambda d: d.update(image_size=0))
        mut("image-size-negative", lambda d: d.update(image_size=-1))

        def used_gt_size(d):
            s = d["swaps"][0]
            s["used_kib"] = s["size_kib"] + 1024
        mut("used-kib-gt-size-kib", used_gt_size)

        def exact_free(d):
            free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in d["swaps"])
            d["image_size"] = free
        mut("free-eq-image-size", exact_free)

        def free_minus_one(d):
            free = sum((s["size_kib"] - s["used_kib"]) * 1024 for s in d["swaps"])
            d["image_size"] = free + 1
        mut("free-lt-image-size-by-1", free_minus_one)

        # inconsistent doc: no swaps but a resume swapfile recorded
        def no_swaps_but_file(d):
            d.update(swaps=[], resume_swapfile="/swap/swapfile", map_swapfile_offset=12345,
                     swapfile_attrs="------C------")
        mut("swaps-empty-but-file-active", no_swaps_but_file)

        # file swap with missing metadata
        if bool_file:
            mut("map-offset-null", lambda d: d.update(map_swapfile_offset=None))
            mut("attrs-null", lambda d: d.update(swapfile_attrs=None))
            mut("attrs-no-C", lambda d: d.update(swapfile_attrs="----------------"))

        # power state wording
        mut("state-upper-DISK", lambda d: d.update(sys_power_state="freeze mem DISK"))
        mut("state-nondisk", lambda d: d.update(sys_power_state="freeze nondisk"))
        mut("state-empty", lambda d: d.update(sys_power_state=""))
        mut("state-double-space", lambda d: d.update(sys_power_state="freeze  mem   disk"))
        mut("state-tab", lambda d: d.update(sys_power_state="freeze\tmem\tdisk"))
        mut("state-disk-token-last", lambda d: d.update(sys_power_state="freeze mem disk"))

        # lookalike cmdline tokens
        def lookalikes(d):
            d["cmdline"] = d["cmdline"] + " xresume=/dev/foo resume_offsetx=1 notresume=2"
        mut("lookalike-tokens", lookalikes)

        # extra unknown keys
        mut("extra-keys", lambda d: d.update(extra="ignored", captured_at="1999-01-01T00:00:00Z"))

        # several findings at once
        def multi_findings(d):
            d["sys_power_state"] = "freeze mem"
            d["image_size"] = 10 ** 18
            d["hooks"] = ["base", "encrypt", "resume"]
        mut("multi-findings", multi_findings)

        # rule-1 precedence: no resume arg plus everything else broken
        def no_resume_everything(d):
            toks = [t for t in d["cmdline"].split() if not t.startswith("resume=")]
            d["cmdline"] = " ".join(toks)
            d["swaps"] = []
            d["resume_swapfile"] = None
            d["sys_power_state"] = "freeze"
            d["hooks"] = ["base"]
        mut("no-resume-precedence", no_resume_everything)

    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cleanroom", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    bat = load_battery()
    rng = random.Random(20261106)
    corpus = cases(bat, rng)
    tmp = tempfile.mkdtemp(prefix="r84-diff-")

    def one(item):
        cat, name, facts = item
        cr = run_gate(a.cleanroom, facts, tmp)
        ca = run_gate(a.candidate, facts, tmp)
        return {"category": cat, "case": name, "input": facts,
                "cleanroom": cr, "candidate": ca,
                "agree": key(cr) == key(ca)}

    with ThreadPoolExecutor(max_workers=24) as ex:
        results = list(ex.map(one, corpus))

    disag = [r for r in results if not r["agree"]]
    groups = {}
    for r in disag:
        k = (json.dumps(key(r["cleanroom"])), json.dumps(key(r["candidate"])))
        g = groups.setdefault(str(k), {"count": 0, "example": r["case"],
                                       "cleanroom": key(r["cleanroom"]),
                                       "candidate": key(r["candidate"])})
        g["count"] += 1
    by_cat = {}
    for r in results:
        c = by_cat.setdefault(r["category"], {"cases": 0, "disagreements": 0})
        c["cases"] += 1
        c["disagreements"] += 0 if r["agree"] else 1
    doc = {
        "lane_revision": subprocess.run(["git", "-C", REPO, "rev-parse", "master"], capture_output=True,
                                        text=True).stdout.strip(),
        "seed": 20261106,
        "candidate_sha256": subprocess.run(["sha256sum", os.path.abspath(a.candidate)], capture_output=True,
                                           text=True).stdout.split()[0] if os.path.exists(a.candidate) else None,
        "cleanroom_sha256": subprocess.run(["sha256sum", os.path.abspath(a.cleanroom)], capture_output=True,
                                           text=True).stdout.split()[0],
        "total_cases": len(results),
        "agreements": len(results) - len(disag),
        "disagreements": len(disag),
        "by_category": by_cat,
        "groups": list(groups.values()),
        "diff_cap": CAP,
        "diffs": [{k: r[k] for k in ("category", "case", "input", "cleanroom", "candidate")}
                  for r in disag[:CAP]],
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
    print(json.dumps({k: doc[k] for k in ("total_cases", "agreements", "disagreements", "by_category")},
                     indent=1))
    print(json.dumps(doc["groups"], indent=1))
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if not disag else 1


if __name__ == "__main__":
    sys.exit(main())
