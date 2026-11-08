#!/usr/bin/env python3
"""Run the round-92 oracle-channel controls against one battery and write the receipts.

Usage: run-controls.py --battery PATH --gates DIR --runs N --out DIR --label NAME [--env K=V]...
                                                        [--work DIR] [--only NAME,...]

For every `*.py` in --gates: runs `<battery> --gate <gate> --runs N --json <out>/<name>.json` with
the given environment additions, records the stdout/rc, and counts the `error` rows the battery
logged (QUALITY 126: a control that crashed is not evidence of rejection). Writes
`<out>/<name>.txt`, `<out>/<name>.json` and appends one TSV row per gate to `<out>/summary.tsv`:
name, runs, rc, families_passed (per run), verdict (per run), error rows, gate sha256.
Exit 0 when every gate produced `runs` verdict lines; the verdicts themselves are the evidence,
never this script's rc.
"""
import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--battery", required=True)
    ap.add_argument("--gates", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--env", action="append", default=[])
    ap.add_argument("--only", default=None)
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    env = dict(os.environ)
    for item in a.env:
        k, _, v = item.partition("=")
        env[k] = v
    work = a.work or os.path.join(a.out, "work")
    os.makedirs(work, exist_ok=True)
    gates = sorted(glob.glob(os.path.join(os.path.abspath(a.gates), "*.py")))
    if a.only:
        wanted = set(a.only.split(","))
        gates = [g for g in gates if os.path.basename(g)[:-3] in wanted]
    summary_path = os.path.join(a.out, "summary.tsv")
    rows = []

    def one(gate):
        name = os.path.basename(gate)[:-3]
        json_path = os.path.join(a.out, name + ".json")
        cmd = [sys.executable, os.path.abspath(a.battery), "--gate", gate,
               "--runs", str(a.runs), "--work", os.path.join(work, name), "--json", json_path]
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=3600)
        with open(os.path.join(a.out, name + ".txt"), "w") as f:
            f.write("# %s battery=%s gate=%s runs=%d\n" % (a.label, a.battery, gate, a.runs))
            f.write("# env additions: %s\n" % (a.env,))
            f.write("# cmd: %s\n" % " ".join(cmd))
            f.write("# rc=%d\n" % p.returncode)
            f.write(p.stdout)
            if p.stderr.strip():
                f.write("# stderr: %s\n" % p.stderr.strip()[-2000:])
        runs = []
        if os.path.isfile(json_path):
            data = json.load(open(json_path))
            runs = data if isinstance(data, list) else [data]
        passed = [r.get("families_passed") for r in runs]
        verdicts = [r.get("verdict") for r in runs]
        errors = sum(1 for r in runs for e in r.get("case_log", []) if e.get("error"))
        return ("%s\t%d\t%d\t%s\t%s\t%d\t%s\n" % (
            name, a.runs, p.returncode,
            ",".join(str(x) for x in passed) or "-",
            ",".join(str(x) for x in verdicts) or "-",
            errors, sha256(gate)), name, p.returncode, passed, verdicts, errors)

    if a.jobs > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=a.jobs) as pool:
            results = list(pool.map(one, gates))
    else:
        results = [one(g) for g in gates]
    with open(summary_path, "w") as summary:
        summary.write("control\truns\trc\tfamilies_passed\tverdict\terrors\tgate_sha256\n")
        for row, name, rc, passed, verdicts, errors in results:
            summary.write(row)
            print("%-14s rc=%d passed=%s verdict=%s errors=%d" % (
                name, rc, passed or "-", verdicts or "-", errors))
    return 0 if all(os.path.isfile(os.path.join(a.out, n + ".json"))
                    for _, n, _, _, _, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())
