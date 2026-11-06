#!/usr/bin/env python3
"""Cheapest junk entries for the frozen round-84 C1 counter (shape-gate limit).

Builds three mechanically generated entries in a scratch root, then runs the
frozen counter (tools/count-resume-rows-r84.py) and the independent checker
(check.py) on each:

  plain : 7 rows, real source snapshots (>=4 distinct files), quotes that are
          random 6-10 token windows unique in their file, host values that are
          random tokens unique in receipt.txt, one boilerplate statement.
          Requires no reading of the cited text at all.
  cross : 7 rows whose `source.snapshot` entries point at the *host* receipt
          (a file listed only in the host manifest) and whose `host.receipt`
          entries point at a *source* snapshot.  Four distinct snapshot keys,
          all the same file, so `distinct_snapshots` still reads 4.
  url   : the plain entry with every `url` field removed (the frozen counter
          additionally requires an https url, which the predicate text does
          not).
  onefile: 4 snapshot keys pointing at the same source file, so the counter's
          ">= 4 distinct snapshots" target counts declarations, not files.

Usage: junk.py --lane LANE --work DIR [--mode plain|cross|url|all] [--seed N]
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys

ENTRY = "corpus/knowledge/hibernate-resume-plane-r84.json"
BEFORE = ".ufo/waves/round-84/before"
BOILER = ("boilerplate row generated mechanically with no reading of the cited "
          "source text at all")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(s):
    return " ".join(s.split())


def parse_manifest(path, base):
    out = {}
    with open(path, "rb") as fh:
        for line in fh.read().decode("utf-8", "replace").splitlines():
            parts = line.split()
            if len(parts) == 2 and len(parts[0]) == 64:
                out[f"{base}/{parts[1]}"] = parts[0]
    return out


def lines_of(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", "replace").split("\n")


def unique_quote(lines, rng):
    """A 6..10 token window that occurs exactly once in the file."""
    text = "\n".join(lines)
    for _ in range(4000):
        i = rng.randrange(len(lines))
        toks = lines[i].split()
        if len(toks) < 6:
            continue
        k = rng.randint(6, min(10, len(toks)))
        start = rng.randrange(len(toks) - k + 1)
        q = " ".join(toks[start:start + k])
        if text.count(q) == 1:
            return i + 1, q
    raise SystemExit("could not find a unique quote window")


def unique_token(lines, rng):
    """A token whose first occurrence in the file is on its own line."""
    text = "\n".join(lines)
    for _ in range(4000):
        i = rng.randrange(len(lines))
        toks = [t for t in lines[i].split() if len(t) >= 3]
        if not toks:
            continue
        t = rng.choice(toks)
        if text.find(t) is not None and text.count(t) == 1:
            return i + 1, t
    raise SystemExit("could not find a unique host token")


def write_entry(root, entry):
    p = os.path.join(root, ENTRY)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(entry, fh, indent=1)


def build_plain(root, lane, rng):
    src_manifest = parse_manifest(os.path.join(lane, BEFORE, "src/SHA256SUMS"), BEFORE + "/src")
    host_manifest = parse_manifest(os.path.join(lane, BEFORE, "host/SHA256SUMS"), BEFORE + "/host")
    src_paths = sorted(src_manifest)
    snap_keys = [f"S{i}" for i in range(1, 5)]
    snaps = {k: {"url": "https://example.invalid/" + os.path.basename(p),
                 "path": p, "sha256": src_manifest[p]}
             for k, p in zip(snap_keys, rng.sample(src_paths, len(snap_keys)))}
    rec_key, rec_path = "capture", os.path.join(BEFORE, "host/receipt.txt")
    receipts = {rec_key: {"path": rec_path, "sha256": host_manifest[rec_path]}}
    rlines = lines_of(os.path.join(lane, rec_path))
    quotes, rows = set(), []
    for n in range(7):
        k = snap_keys[n % len(snap_keys)]
        a, q = unique_quote(lines_of(os.path.join(lane, snaps[k]["path"])), rng)
        while norm(q) in quotes:
            a, q = unique_quote(lines_of(os.path.join(lane, snaps[k]["path"])), rng)
        quotes.add(norm(q))
        j, v = unique_token(rlines, rng)
        rows.append({"id": f"HR{n + 1}", "statement": BOILER,
                     "source": {"snapshot": k, "lines": [a, a], "quote": q},
                     "host": {"receipt": rec_key, "lines": [j, j], "value": v}})
    return {"entry": "junk-plain", "snapshots": snaps, "receipts": receipts, "rows": rows}


def build_cross(root, lane, rng):
    """Every row cites the host receipt as its *source* and a source file as its host."""
    src_manifest = parse_manifest(os.path.join(lane, BEFORE, "src/SHA256SUMS"), BEFORE + "/src")
    host_manifest = parse_manifest(os.path.join(lane, BEFORE, "host/SHA256SUMS"), BEFORE + "/host")
    rec_path = os.path.join(BEFORE, "host/receipt.txt")
    src_path = os.path.join(BEFORE, "src/sysfs-power")
    snap_keys = [f"SX{i}" for i in range(1, 5)]  # 4 keys, one file
    snaps = {k: {"url": "https://example.invalid/receipt.txt",
                 "path": rec_path, "sha256": host_manifest[rec_path]}
             for k in snap_keys}
    receipts = {"capture": {"path": src_path, "sha256": src_manifest[src_path]}}
    rlines = lines_of(os.path.join(lane, rec_path))
    slines = lines_of(os.path.join(lane, src_path))
    quotes, rows = set(), []
    for n in range(7):
        k = snap_keys[n % len(snap_keys)]
        a, q = unique_quote(rlines, rng)
        while norm(q) in quotes:
            a, q = unique_quote(rlines, rng)
        quotes.add(norm(q))
        j, v = unique_token(slines, rng)
        rows.append({"id": f"HR{n + 1}", "statement": BOILER,
                     "source": {"snapshot": k, "lines": [a, a], "quote": q},
                     "host": {"receipt": "capture", "lines": [j, j], "value": v}})
    return {"entry": "junk-cross", "snapshots": snaps, "receipts": receipts, "rows": rows}


def build_onefile(root, lane, rng):
    """4 snapshot keys, one source file: distinct-by-key, not distinct-by-file."""
    src_manifest = parse_manifest(os.path.join(lane, BEFORE, "src/SHA256SUMS"), BEFORE + "/src")
    host_manifest = parse_manifest(os.path.join(lane, BEFORE, "host/SHA256SUMS"), BEFORE + "/host")
    path = BEFORE + "/src/kernel-parameters.txt"
    snap_keys = [f"S{i}" for i in range(1, 5)]
    snaps = {k: {"url": "https://example.invalid/kernel-parameters.txt",
                 "path": path, "sha256": src_manifest[path]} for k in snap_keys}
    rec_path = os.path.join(BEFORE, "host/receipt.txt")
    receipts = {"capture": {"path": rec_path, "sha256": host_manifest[rec_path]}}
    rlines = lines_of(os.path.join(lane, rec_path))
    klines = lines_of(os.path.join(lane, path))
    quotes, rows = set(), []
    for n in range(7):
        k = snap_keys[n % len(snap_keys)]
        a, q = unique_quote(klines, rng)
        while norm(q) in quotes:
            a, q = unique_quote(klines, rng)
        quotes.add(norm(q))
        j, v = unique_token(rlines, rng)
        rows.append({"id": f"HR{n + 1}", "statement": BOILER,
                     "source": {"snapshot": k, "lines": [a, a], "quote": q},
                     "host": {"receipt": "capture", "lines": [j, j], "value": v}})
    return {"entry": "junk-onefile", "snapshots": snaps, "receipts": receipts, "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--mode", default="all")
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    modes = ["plain", "cross", "url", "onefile"] if a.mode == "all" else [a.mode]
    out = {}
    for mode in modes:
        root = os.path.join(a.work, "junk-" + mode)
        if os.path.exists(root):
            shutil.rmtree(root)
        os.makedirs(root)
        shutil.copytree(os.path.join(a.lane, BEFORE), os.path.join(root, BEFORE))
        rng = random.Random(a.seed)
        if mode in ("plain", "url"):
            entry = build_plain(root, a.lane, rng)
        elif mode == "onefile":
            entry = build_onefile(root, a.lane, rng)
        else:
            entry = build_cross(root, a.lane, rng)
        if mode == "url":
            for d in entry["snapshots"].values():
                d.pop("url", None)
        write_entry(root, entry)
        counter = subprocess.run([sys.executable, os.path.join(a.lane, "tools/count-resume-rows-r84.py"),
                                  "--root", root], capture_output=True, text=True)
        check = subprocess.run([sys.executable,
                                os.path.join(a.lane, ".ufo/waves/round-84/w1/ExecProvenanceC1/check.py"),
                                "--repo", root], capture_output=True, text=True)
        try:
            cres = json.loads(counter.stdout)
        except json.JSONDecodeError:
            cres = {"stdout": counter.stdout, "stderr": counter.stderr}
        try:
            kres = json.loads(check.stdout)
        except json.JSONDecodeError:
            kres = {"stdout": check.stdout, "stderr": check.stderr}
        out[mode] = {"root": root,
                     "frozen": {"rc": counter.returncode, "verdict": cres.get("verdict"),
                                "counted": cres.get("counted"), "failed": cres.get("failed"),
                                "distinct_snapshots": cres.get("distinct_snapshots"),
                                "reasons": {r.get("id"): r.get("reason") for r in cres.get("rows", [])}},
                     "independent": {"rc": check.returncode, "verdict": kres.get("verdict"),
                                     "counted": kres.get("counted"), "failed": kres.get("failed"),
                                     "distinct_snapshots": kres.get("distinct_snapshots"),
                                     "distinct_snapshot_paths": kres.get("distinct_snapshot_paths"),
                                     "reasons": {r.get("id"): r.get("reason") for r in kres.get("rows", [])}}}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
