#!/usr/bin/env python3
"""Differential fuzzer: clean-room gate vs tools/check-hibernate-resume.py on resume-facts/2.

Generates a deterministic corpus (>=3000 documents) spanning the frozen docstring's
edge tokens, availability faults, resume-chain faults, malformed documents and
extra unknown keys; runs both gates on every document and records every disagreement
with the document and both outputs.

Usage: cleanroom-fuzz.py --work DIR --out DIR [--count N] [--seed S]
"""
import argparse
import copy
import json
import os
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
BASE = json.load(open(os.path.join(LANE, ".ufo/waves/round-85/before/host/facts-v2.json")))
CLEAN = os.path.join(HERE, "cleanroom-gate.py")
CAND = os.path.join(LANE, "tools/check-hibernate-resume.py")

AVAIL_TOKENS = [
    "nohibernate", "noresume", "hibernate=nope", "hibernate=noresumeX",
    "hibernate=nocompressX", "hibernate=protect_image", "hibernate=",
    "hibernate=no", "hibernate=noresume", "hibernate=nocompress",
    "hibernate=NO", "hibernate=noResume", "hibernate=noresumexnocompress",
    "hibernate=nocompressx", "hibernate=non", "hibernate=protect_imagex",
    "noresumeX", "nohibernateX", "nohibernate=1", "noresume=1",
    "hibernate==", "hibernate=x=no",
]
DECOYS = ["resumewait", "usbcore.noresume=1", "usbcore.nohibernate=1",
          "hibernate.compressor=lz4", "resumedelay=10", "resume_offset=xyz"]
LOCKDOWNS = [
    "[none] integrity confidentiality", "none [integrity] confidentiality",
    "none integrity [confidentiality]", None, "[]", "[none]", "", "none",
    "[none]]", "[[none]", "[[none]]", "[a]]", "[[a]", "[a][b]",
    "[none] integrity [integrity]", "[ integrity ]", "[integrity]", "integrity",
    "[NONE]", "[confidentiality]", "none [none] confidentiality",
]
OFFSETS = [3795013, 3795013, 1, 0, 3795014, -1, 999999999999]
WRONG = {
    "cmdline": [None, 3, True, [], {}],
    "swaps": [None, "x", {}, 3, [1], [{"size_kib": 1, "used_kib": 2}],
              [{"size_kib": True, "used_kib": 2}], [{"size_kib": 1}],
              [{"path": "/x", "type": "file", "size_kib": 1, "used_kib": 2}],
              [{"path": 3, "type": "file", "size_kib": 1, "used_kib": 2}]],
    "resume_swapfile": [3, True, [], {}],
    "map_swapfile_offset": ["3", True, [], {}],
    "swapfile_attrs": [3, True, [], {}],
    "resume_dev_majmin": [3, True, [], {}],
    "sys_power_resume": [None, 3, True, [], {}, " 253:0", "253:0\n", ""],
    "sys_power_resume_offset": [None, "3795013", True, [], {}],
    "sys_power_state": [None, 3, True, [], {}, ""],
    "image_size": [None, "x", True, [], {}, 1.5],
    "hooks": [None, "base", [1], [None], [["base"]], []],
    "lockdown": [3, True, [], {}, "none integrity confidentiality", "[]",
                 "[none]", "[none] [integrity]", "x [none] y", "[[none]]",
                 "[a]]", "[[a]", "[a][b]", "[None]",
                 "[none] integrity confidentiality", "none [integrity] confidentiality",
                 "none integrity [confidentiality]"],
    "schema": ["resume-facts/1", "resume-facts/3", None, 2, "resume-facts/2 ",
               "RESUME-FACTS/2"],
}
REQUIRED = ["schema", "cmdline", "swaps", "resume_swapfile", "map_swapfile_offset",
            "swapfile_attrs", "resume_dev_majmin", "sys_power_resume",
            "sys_power_resume_offset", "sys_power_state", "image_size", "hooks",
            "lockdown"]


def base():
    return copy.deepcopy(BASE)


def cmd_tokens(f):
    return f["cmdline"].split()


def insert_token(f, tok, pos=None):
    toks = cmd_tokens(f)
    toks.insert(len(toks) if pos is None else pos, tok)
    f["cmdline"] = " ".join(toks)


def drop_resume(f):
    f["cmdline"] = " ".join(t for t in cmd_tokens(f) if not t.startswith("resume="))


def drop_offset(f):
    f["cmdline"] = " ".join(t for t in cmd_tokens(f) if not t.startswith("resume_offset="))


def set_offset(f, value):
    drop_offset(f)
    insert_token(f, "resume_offset=" + str(value))


ENTRY = {"path": "/swap/swapfile", "type": "file", "size_kib": 31722876, "used_kib": 11942400}


def new_entry(**kw):
    e = copy.deepcopy(ENTRY)
    e.update(kw)
    return e


# --- random structural mutators -------------------------------------------------------------

def m_token(rng, f):
    insert_token(f, rng.choice(AVAIL_TOKENS))


def m_decoy(rng, f):
    insert_token(f, rng.choice(DECOYS))


def m_drop_resume(rng, f):
    drop_resume(f)


def m_drop_offset(rng, f):
    drop_offset(f)


def m_set_offset(rng, f):
    set_offset(f, rng.choice(OFFSETS + ["abc", "+3795013", "0x10", ""]))


def m_dup_resume(rng, f):
    insert_token(f, "resume=/dev/mapper/root")


def m_swapfile_none(rng, f):
    f["resume_swapfile"] = None


def m_mapoff(rng, f):
    f["map_swapfile_offset"] = rng.choice([None, 1, 3795014, 0])


def m_attrs(rng, f):
    f["swapfile_attrs"] = rng.choice([None, "", "----------------------", "---------------C------"])


def m_devmm(rng, f):
    f["resume_dev_majmin"] = rng.choice([None, "8:1", "253:0", "0:0"])


def m_sysres(rng, f):
    f["sys_power_resume"] = rng.choice(["253:0", "253:0\n", " 253:0", "", "8:1", None,
                                        "253:0 ", "\t253:0"])


def m_sysoff(rng, f):
    f["sys_power_resume_offset"] = rng.choice([3795013, 0, -1, None, 1])


def m_state(rng, f):
    f["sys_power_state"] = rng.choice(["freeze mem disk", "freeze mem", "", "disk",
                                       "freeze mem DISK", "disk mem freeze"])


def m_hooks(rng, f):
    h = f["hooks"]
    op = rng.randrange(6)
    if op == 0:
        f["hooks"] = [x for x in h if x != "resume"]
    elif op == 1:
        f["hooks"] = [x for x in h if x not in ("resume", "systemd")]
    elif op == 2:
        f["hooks"] = [x for x in h if x != "resume"]
        f["hooks"].insert(0, "resume")
    elif op == 3:
        f["hooks"] = []
    elif op == 4:
        f["hooks"] = h + ["systemd"]
    else:
        f["hooks"] = ["base", "encrypt", "resume", "filesystems"]


def m_swaps(rng, f):
    op = rng.randrange(5)
    if op == 0:
        f["swaps"] = []
    elif op == 1:
        f["swaps"] = [new_entry(size_kib=1000, used_kib=999)]
    elif op == 2:
        f["swaps"] = [new_entry()] * 2
    elif op == 3:
        f["swaps"] = [new_entry(size_kib=10, used_kib=20)]
    else:
        f["swaps"] = [new_entry()] + [new_entry(path="/swap/other", type="partition",
                                                size_kib=1, used_kib=0)]


def m_image(rng, f):
    f["image_size"] = rng.choice([0, 1, 12835467264, 10 ** 15, -5])


def m_unknown(rng, f):
    f["captured_at"] = "2026-11-06T16:48:31-03:00"
    f["sys_power_disk"] = rng.choice(["[platform] shutdown reboot suspend", "shutdown"])
    f[rng.choice(["future_key", "extra", "note"])] = rng.choice([None, 1, "x", [1, 2], {"a": 1}])


def m_swap_extra(rng, f):
    for s in f["swaps"]:
        s["extra"] = rng.choice([1, "x", None])


def m_lockdown(rng, f):
    f["lockdown"] = rng.choice(LOCKDOWNS)


MUTATORS = [m_token] * 6 + [m_decoy] * 3 + [m_drop_resume, m_drop_offset, m_set_offset,
            m_dup_resume, m_swapfile_none, m_mapoff, m_attrs, m_devmm, m_sysres, m_sysoff,
            m_state] + [m_hooks] * 3 + [m_swaps] * 3 + [m_image, m_unknown, m_swap_extra,
            m_lockdown, m_lockdown]


def random_doc(rng):
    f = base()
    for _ in range(rng.choice([0, 1, 1, 2, 2, 3, 4, 5])):
        rng.choice(MUTATORS)(rng, f)
    return f


# --- corpus ---------------------------------------------------------------------------------

def corpus(seed):
    rng = random.Random(seed)
    docs = []

    def add(case, f):
        docs.append({"case": case, "doc": f})

    # T1: every edge token under every lockdown (resume= present).
    for tok in AVAIL_TOKENS:
        for lock in LOCKDOWNS:
            f = base()
            insert_token(f, tok, rng.randrange(len(cmd_tokens(f)) + 1))
            f["lockdown"] = lock
            add(f"T1:{tok}|{lock}", f)

    # T2: token x resume= absent x lockdown.
    for tok in AVAIL_TOKENS:
        for lock in ["[none] integrity confidentiality", "none [integrity] confidentiality",
                     "none integrity [confidentiality]", None, "[none]"]:
            f = base()
            insert_token(f, tok)
            drop_resume(f)
            f["lockdown"] = lock
            add(f"T2:{tok}|noresume=|{lock}", f)

    # T3: ordered pairs of availability tokens.
    pairs = ["nohibernate", "noresume", "hibernate=no", "hibernate=noresume", "hibernate=nocompress"]
    for i, a in enumerate(pairs):
        for j, b in enumerate(pairs):
            if i == j:
                continue
            for lock in ["[none]", "none [integrity]", None]:
                f = base()
                insert_token(f, a, 0)
                insert_token(f, b, 1)
                f["lockdown"] = lock
                add(f"T3:{a}+{b}|{lock}", f)

    # T4: pairs with resume= absent.
    for i, a in enumerate(pairs):
        for j, b in enumerate(pairs):
            if i == j:
                continue
            f = base()
            insert_token(f, a, 0)
            insert_token(f, b, 1)
            drop_resume(f)
            add(f"T4:{a}+{b}|noresume=", f)

    # T5: every availability fault with resume-chain faults.
    for tok in ["nohibernate", "noresume", "hibernate=no", "hibernate=noresume", "hibernate=nope"]:
        for lock in ["none [integrity]", "none integrity [confidentiality]", None]:
            f = base()
            insert_token(f, tok)
            f["lockdown"] = lock
            f["swaps"] = []
            f["hooks"] = [x for x in f["hooks"] if x != "resume"]
            f["sys_power_state"] = "freeze mem"
            f["swapfile_attrs"] = "----------------------"
            add(f"T5:{tok}|chainfaults|{lock}", f)

    # T6: repeated nohibernate/noresume in both orders.
    for seq in (["nohibernate", "noresume"], ["noresume", "nohibernate"],
                ["hibernate=no", "noresume"], ["noresume", "hibernate=no"],
                ["nohibernate", "nohibernate"], ["noresume", "noresume"]):
        f = base()
        for t in seq:
            insert_token(f, t)
        add("T6:" + "+".join(seq), f)
        f = base()
        for t in seq:
            insert_token(f, t)
        drop_resume(f)
        add("T6:" + "+".join(seq) + "|noresume=", f)

    # T7: decoys alone and with each other.
    for d in DECOYS:
        f = base()
        insert_token(f, d)
        add(f"T7:{d}", f)
    for i in range(len(DECOYS)):
        for j in range(i + 1, len(DECOYS)):
            f = base()
            insert_token(f, DECOYS[i], 0)
            insert_token(f, DECOYS[j], 1)
            add(f"T7:{DECOYS[i]}+{DECOYS[j]}", f)

    # T8: availability fault + absent resume, with offset tokens present/absent.
    for tok in ["nohibernate", "noresume", "hibernate=no"]:
        for off in [None, 3795013, "abc"]:
            f = base()
            insert_token(f, tok)
            if off is not None:
                set_offset(f, off)
            drop_resume(f)
            add(f"T8:{tok}|offset={off}", f)

    # T9: resume= present, offsets and duplicate ordering.
    for cmdline in [
        "resume=/dev/mapper/root resume_offset=3795013",
        "resume_offset=3795013 resume=/dev/mapper/root",
        "resume_offset=1 resume_offset=3795013 resume=/dev/mapper/root",
        "resume_offset=3795013 resume_offset=1 resume=/dev/mapper/root",
        "resume=/dev/mapper/root resume=/dev/sda2 resume_offset=3795013",
        "resume=/dev/sda2 resume=/dev/mapper/root resume_offset=3795013",
        "resume= resume_offset=3795013",
        "resume=/dev/mapper/root resume_offset=",
        "resume=/dev/mapper/root resume_offset=abc",
        "resume=/dev/mapper/root resume_offset=+3795013",
        "resume=/dev/mapper/root resume_offset=0x10",
        "resume=/dev/mapper/root resume_offset=3_795_013",
        "resume=/dev/mapper/root resume_offset=3795013x",
        "resume=/dev/mapper/root resume_offset=3795013 resume_offset=abc",
    ]:
        f = base()
        f["cmdline"] = cmdline
        add(f"T9:{cmdline}", f)

    # X: random structural documents.
    for i in range(2400):
        add(f"R{i}", random_doc(rng))

    # X2: malformed documents (missing keys / wrong types / roots).
    for key in REQUIRED:
        f = base()
        del f[key]
        add(f"M:del:{key}", f)
    for key, bads in WRONG.items():
        for bad in bads:
            f = base()
            f[key] = copy.deepcopy(bad)
            add(f"M:type:{key}={type(bad).__name__}", f)
    for root in (None, [], "x", 3, True, [{"schema": "resume-facts/2"}]):
        docs.append({"case": f"M:root:{type(root).__name__}", "doc": root})
    for i, s in enumerate(["", "{}", "[1,2", '{"schema": "resume-facts/2"', "not json\n",
                           '{"a": 1,}']):
        docs.append({"case": f"M:json:{i}", "raw": s})
    return docs


# --- runner ---------------------------------------------------------------------------------

ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}


def run_gate(gate, path):
    try:
        p = subprocess.run([sys.executable, gate, "--facts", path],
                           capture_output=True, text=True, timeout=20, env=ENV)
        out = p.stdout.strip()
        try:
            obj = json.loads(out)
            verdict = obj.get("verdict")
            findings = obj.get("findings")
        except ValueError:
            verdict, findings = f"<non-json:{out[:80]}>", None
        return {"rc": p.returncode, "verdict": verdict, "findings": findings}
    except subprocess.TimeoutExpired:
        return {"rc": "timeout", "verdict": None, "findings": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=8501)
    ap.add_argument("--count", type=int, default=0, help="pad corpus to at least N")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    docs = corpus(a.seed)
    rng = random.Random(a.seed ^ 0x5EED)
    while len(docs) < max(a.count, 3600):
        docs.append({"case": f"P{len(docs)}", "doc": random_doc(rng)})

    paths = []
    for i, d in enumerate(docs):
        p = os.path.join(a.work, f"doc-{i:05d}.json")
        with open(p, "w", encoding="utf-8") as fh:
            if "raw" in d:
                fh.write(d["raw"])
            else:
                json.dump(d["doc"], fh)
        paths.append(p)

    def work(i):
        mine = run_gate(CLEAN, paths[i])
        cand = run_gate(CAND, paths[i])
        return i, mine, cand

    results = [None] * len(docs)
    with ThreadPoolExecutor(max_workers=32) as ex:
        for i, mine, cand in ex.map(work, range(len(docs))):
            results[i] = (mine, cand)

    disagree = []
    for i, d in enumerate(docs):
        mine, cand = results[i]
        if (mine["rc"], mine["verdict"], mine["findings"]) != (cand["rc"], cand["verdict"], cand["findings"]):
            disagree.append({"case": d["case"], "doc": d.get("doc", d.get("raw")),
                             "cleanroom": mine, "candidate": cand,
                             "file": os.path.basename(paths[i])})

    groups = {}
    for d in disagree:
        sig = (d["cleanroom"]["rc"], d["cleanroom"]["verdict"],
               tuple(d["cleanroom"]["findings"] or []),
               d["candidate"]["rc"], d["candidate"]["verdict"],
               tuple(d["candidate"]["findings"] or []))
        key = json.dumps(sig)
        g = groups.setdefault(key, {"signature": sig, "count": 0, "cases": []})
        g["count"] += 1
        if len(g["cases"]) < 3:
            g["cases"].append({"case": d["case"], "doc": d["doc"],
                               "cleanroom": d["cleanroom"], "candidate": d["candidate"]})

    summary = {
        "corpus_size": len(docs),
        "disagreements": len(disagree),
        "groups": list(groups.values()),
        "cleanroom_sha256": os.popen(f"sha256sum {CLEAN}").read().split()[0],
        "candidate_sha256": os.popen(f"sha256sum {CAND}").read().split()[0],
    }
    with open(os.path.join(a.out, "fuzz-summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(a.out, "fuzz-disagreements.json"), "w", encoding="utf-8") as fh:
        json.dump(disagree, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(a.out, "fuzz-corpus.jsonl"), "w", encoding="utf-8") as fh:
        for d in docs:
            fh.write(json.dumps(d, sort_keys=True) + "\n")
    print(json.dumps({"corpus_size": len(docs), "disagreements": len(disagree),
                      "groups": len(groups)}, sort_keys=True))
    for g in sorted(groups.values(), key=lambda x: -x["count"]):
        print(json.dumps({"count": g["count"], "signature": g["signature"],
                          "cases": [c["case"] for c in g["cases"]]}, sort_keys=True))
        for c in g["cases"][:1]:
            print("  doc=" + json.dumps(c["doc"], sort_keys=True)[:600])
            print("  cleanroom=" + json.dumps(c["cleanroom"], sort_keys=True)[:300])
            print("  candidate=" + json.dumps(c["candidate"], sort_keys=True)[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
