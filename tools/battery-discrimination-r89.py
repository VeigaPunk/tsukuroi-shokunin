#!/usr/bin/env python3
"""Round-89 frozen discrimination counter for a Limine pin-gate battery (tsukuroi lane).

Surface: battery calibration of the `limine-pins` gate (r88 routed R88-R1, R88-R6).

PREDICATE (the same sentence in SCORECARD.md "Round 89 — declaration" and in every receipt):
  The battery under test, driven by this counter over the frozen roster
  `.ufo/waves/round-89/before/roster/roster-r89.json`, reads `met` (exit 0 and JSON verdict "met")
  for every POSITIVE gate and `unmet` (exit 1 and JSON verdict "unmet") for every NEGATIVE gate,
  with zero error rows, in each of three runs; the battery sees each gate only as an opaque
  launcher that forwards its argv to the gate run outside the battery's sandbox, and the
  sandbox exposes only /usr, /etc and the per-case directory.
TARGET: positives P/P and negatives N/N with 0 error rows in each of the three runs (verdict
  `met`, exit 0).
KILL RULE: unmet if any run reads below P/P or N/N; could-not-evaluate (exit 3, never `met`)
  if any row of any run is an error row; void (exit 2) if any file listed in
  `.ufo/waves/round-89/before/freeze-manifest.sha256` (this counter, the roster, every roster
  gate) differs from its digest there, or the isolation preflight sees a host path it must not.

What each clause is made of (code, not promise; r88 lesson M2):
  * opaque gate: the battery's `--gate` is a launcher whose bytes differ between gates only by a
    random socket name; the gate's own bytes and its support files sit in a directory the
    sandbox does not mount, and a server thread of this counter runs them with the launcher's
    argv and cwd. No source text, digest or file name of a roster gate is visible to the battery
    (r88 CriticClaims F2: a nonce-stripping digest table read `met`; this closes it by
    construction). A gate's behaviour on its argv, files and cwd is all the battery can observe.
  * allowlist sandbox: `bwrap` mounts /usr (and the /bin, /lib, /lib64, /sbin symlinks into it)
    and /etc read-only, a fresh /dev, /proc and /tmp, and only the per-case directory
    read-write; every other host root (/home, /fast, /var, /run, /opt, /root, /mnt, /srv,
    /boot, /efi) is absent, so no lane, clone origin or scratch roster copy is reachable
    (r88 CriticClaims F1/F3, ExecReplicate D1). Namespaces are unshared (`--unshare-all`), the
    environment is cleared. The preflight runs a probe inside the same sandbox and voids the
    count if the lane, its tools, the roster directory or the manifest is visible, if the root
    holds any entry beyond the allowlist, or if any ancestor of the case directory lists a
    sibling (so no other scratch, clone or home content is reachable).
  * error rows: a battery crash, timeout, missing or malformed JSON, or an exit code that does not
    match its verdict is an `error:` row; it is never a verdict, never counted as `unmet`, and it
    makes the whole count could-not-evaluate (QUALITY 126, r88 lesson M1).
  * the roster path is fixed (no `--roster`; r88 lesson M2) and every roster file is checked
    against the freeze manifest before the first battery runs.
Not certified: a battery that recognises a gate by timing or by its answers (that is behavioural
testing, which is what the claim measures).

Battery interface (same as tools/limine-pin-battery-r88.py):
  python3 BATTERY --gate GATE --runs 1 --work DIR --json OUT    exit 0 met / 1 unmet

Usage: battery-discrimination-r89.py --battery PATH [--runs 3] [--jobs 8] [--scratch DIR] [--json OUT]
Exit: 0 met; 1 unmet; 2 void/usage; 3 could-not-evaluate (error rows).
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROSTER_DIR = os.path.join(LANE, ".ufo", "waves", "round-89", "before", "roster")
ROSTER = os.path.join(ROSTER_DIR, "roster-r89.json")
MANIFEST = os.path.join(LANE, ".ufo", "waves", "round-89", "before", "freeze-manifest.sha256")
BATTERY_TIMEOUT = 900
GATE_TIMEOUT = 60
PYTHON = "/usr/bin/python3"

LAUNCHER = '''import json, os, socket, sys
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(%r)
s.sendall(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd()}).encode() + b"\\n")
buf = b""
while True:
    chunk = s.recv(65536)
    if not chunk:
        break
    buf += chunk
r = json.loads(buf.decode())
sys.stdout.write(r["stdout"])
sys.stderr.write(r["stderr"])
sys.exit(r["rc"])
'''

PREFLIGHT = '''import json, os, sys
d, hidden = sys.argv[1], sys.argv[2:]
bad = ["visible:" + p for p in hidden if os.path.exists(p)]
allowed_root = {"usr", "bin", "lib", "lib64", "sbin", "etc", "dev", "proc", "tmp", d.strip("/").split("/")[0]}
bad += ["root:" + n for n in sorted(set(os.listdir("/")) - allowed_root)]
parts = d.strip("/").split("/")
for i in range(1, len(parts)):
    anc = "/" + "/".join(parts[:i])
    extra = sorted(set(os.listdir(anc)) - {parts[i]})
    bad += ["sibling:" + os.path.join(anc, n) for n in extra]
print(json.dumps(bad) if bad else "isolated")
sys.exit(1 if bad else 0)
'''


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_manifest():
    """Every manifest line must match; the manifest must name this file, the roster and every roster gate."""
    bad, named = [], set()
    with open(MANIFEST) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            digest, rel = line.split(None, 1)
            rel = rel.lstrip("*")
            p = os.path.join(LANE, rel)
            named.add(os.path.normpath(p))
            if not os.path.isfile(p) or sha256(p) != digest:
                bad.append(rel)
    need = {os.path.normpath(os.path.abspath(__file__)), os.path.normpath(ROSTER)}
    with open(ROSTER) as f:
        roster = json.load(f)
    for g in roster["gates"]:
        for name in [g["file"]] + g.get("support", []):
            need.add(os.path.normpath(os.path.join(ROSTER_DIR, name)))
    bad += sorted("unlisted:" + os.path.relpath(p, LANE) for p in need - named)
    return bad


def load_roster():
    with open(ROSTER) as f:
        roster = json.load(f)
    bad = []
    for g in roster["gates"]:
        g["abs"] = os.path.join(ROSTER_DIR, g["file"])
        if not os.path.isfile(g["abs"]) or sha256(g["abs"]) != g["sha256"]:
            bad.append(g["id"])
        if g["expect"] not in ("met", "unmet"):
            bad.append(g["id"] + ":expect")
    return roster, bad


def sandbox_argv(d, work):
    return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",
            "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",
            "--ro-bind", "/etc", "/etc", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
            "--bind", d, d, "--chdir", d, "--unshare-all", "--die-with-parent", "--clearenv",
            "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", d, "--setenv", "TMPDIR", work,
            "--setenv", "LANG", "C.UTF-8"]


def preflight(scratch):
    d = tempfile.mkdtemp(prefix="pf-", dir=scratch)
    try:
        probe = os.path.join(d, "probe.py")
        with open(probe, "w") as f:
            f.write(PREFLIGHT)
        must_hide = [LANE, ROSTER_DIR, MANIFEST, os.path.join(LANE, "tools")]
        p = subprocess.run(sandbox_argv(d, d) + [PYTHON, probe, d] + must_hide, capture_output=True, text=True,
                           timeout=60)
        return p.returncode == 0 and p.stdout.strip() == "isolated", (p.stdout + p.stderr).strip()[-300:]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def serve(sock, gate_path, gate_dir, d, stop):
    """Run the real gate for each launcher connection; cwd must lie inside the case directory."""
    sock.settimeout(0.5)
    while not stop.is_set():
        try:
            conn, _ = sock.accept()
        except socket.timeout:
            continue
        except OSError:
            return
        with conn:
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = conn.recv(65536)
                if not chunk:
                    break
                buf += chunk
            try:
                req = json.loads(buf.decode())
                cwd = os.path.realpath(req["cwd"])
                if cwd != d and not cwd.startswith(d + os.sep):
                    raise ValueError("cwd outside the case directory")
                p = subprocess.run([PYTHON, gate_path] + [str(x) for x in req["argv"]], cwd=cwd,
                                   capture_output=True, text=True, errors="surrogateescape",
                                   timeout=GATE_TIMEOUT, env={"PATH": "/usr/bin", "LANG": "C.UTF-8"})
                resp = {"rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
            except subprocess.TimeoutExpired:
                resp = {"rc": 124, "stdout": "", "stderr": "gate timeout"}
            except Exception as e:  # noqa: BLE001 - the launcher reports it as a gate failure
                resp = {"rc": 125, "stdout": "", "stderr": "launcher server: %s" % type(e).__name__}
            try:
                conn.sendall(json.dumps(resp).encode("utf-8", "surrogateescape"))
            except OSError:
                pass


def one(battery, gate, scratch):
    """Run the battery once on one opaque gate; return 'met', 'unmet' or 'error:<why>'."""
    d = os.path.realpath(tempfile.mkdtemp(prefix="bd-", dir=scratch))
    gd = tempfile.mkdtemp(prefix="gd-", dir=scratch)  # never mounted in the sandbox
    stop = threading.Event()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        gate_path = os.path.join(gd, os.path.basename(gate["abs"]))
        shutil.copy(gate["abs"], gate_path)
        for extra in gate.get("support", []):
            shutil.copy(os.path.join(ROSTER_DIR, extra), os.path.join(gd, extra))
        sp = os.path.join(d, "s" + secrets.token_hex(6))
        sock.bind(sp)
        sock.listen(16)
        th = threading.Thread(target=serve, args=(sock, gate_path, gd, d, stop), daemon=True)
        th.start()
        lp = os.path.join(d, "g" + secrets.token_hex(6) + ".py")
        with open(lp, "w") as f:
            f.write(LAUNCHER % sp)
        bp = os.path.join(d, "battery-" + secrets.token_hex(4) + ".py")
        shutil.copy(battery, bp)
        work = os.path.join(d, "work")
        os.makedirs(work)
        out = os.path.join(d, "out.json")
        argv = sandbox_argv(d, work) + [PYTHON, bp, "--gate", lp, "--runs", "1", "--work", work, "--json", out]
        try:
            p = subprocess.run(argv, capture_output=True, text=True, timeout=BATTERY_TIMEOUT)
        except subprocess.TimeoutExpired:
            return "error:timeout", None
        try:
            with open(out) as f:
                j = json.load(f)
            if isinstance(j, list):
                j = j[0]
            verdict = j["verdict"]
            fp = j.get("families_passed")
        except Exception as e:  # noqa: BLE001 - a missing/garbled receipt is an error, never a verdict
            return "error:json %s rc=%s %s" % (type(e).__name__, p.returncode, p.stderr[-200:]), None
        if p.returncode == 0 and verdict == "met":
            return "met", fp
        if p.returncode == 1 and verdict == "unmet":
            return "unmet", fp
        return "error:rc=%s verdict=%s" % (p.returncode, verdict), fp
    finally:
        stop.set()
        sock.close()
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(gd, ignore_errors=True)


def run_once(battery, roster, scratch, jobs):
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(one, battery, g, scratch): g for g in roster["gates"]}
        for fu in concurrent.futures.as_completed(futs):
            g = futs[fu]
            got, fp = fu.result()
            rows.append({"id": g["id"], "expect": g["expect"], "got": got, "families_passed": fp,
                         "error": got.startswith("error:"), "ok": got == g["expect"]})
    rows.sort(key=lambda r: r["id"])
    pos = [r for r in rows if r["expect"] == "met"]
    neg = [r for r in rows if r["expect"] == "unmet"]
    return {"positives_ok": sum(r["ok"] for r in pos), "positives_total": len(pos),
            "negatives_ok": sum(r["ok"] for r in neg), "negatives_total": len(neg),
            "error_rows": sum(r["error"] for r in rows),
            "failures": [r["id"] for r in rows if not r["ok"]], "rows": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--battery", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--scratch", default=os.environ.get("TMPDIR"))
    ap.add_argument("--json")
    a = ap.parse_args()
    if shutil.which("bwrap") is None or not os.path.isfile(PYTHON):
        print("void: bwrap or %s not found" % PYTHON, file=sys.stderr)
        return 2
    battery = os.path.abspath(a.battery)
    if not os.path.isfile(battery):
        print("void: battery not found: %s" % battery, file=sys.stderr)
        return 2
    bad = check_manifest()
    if bad:
        print("void: freeze manifest mismatch: %s" % ",".join(bad), file=sys.stderr)
        return 2
    roster, bad = load_roster()
    if bad:
        print("void: roster digest/label mismatch: %s" % ",".join(bad), file=sys.stderr)
        return 2
    scratch = a.scratch or tempfile.gettempdir()
    os.makedirs(scratch, exist_ok=True)
    scratch = os.path.realpath(tempfile.mkdtemp(prefix="battery-discrimination-r89-", dir=scratch))
    try:
        iso, why = preflight(scratch)
        if not iso:
            print("void: isolation preflight failed: %s" % why, file=sys.stderr)
            return 2
        runs = [run_once(battery, roster, scratch, a.jobs) for _ in range(a.runs)]
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    errors = sum(r["error_rows"] for r in runs)
    met = errors == 0 and all(r["positives_ok"] == r["positives_total"] and
                              r["negatives_ok"] == r["negatives_total"] for r in runs)
    verdict = "met" if met else ("could-not-evaluate" if errors else "unmet")
    res = {"schema": "tsukuroi-battery-discrimination-r89-v1", "battery": battery,
           "battery_sha256": sha256(battery), "counter_sha256": sha256(os.path.abspath(__file__)),
           "roster_sha256": sha256(ROSTER), "manifest_sha256": sha256(MANIFEST), "isolation": why,
           "runs": runs, "error_rows": errors, "verdict": verdict}
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=1)
    for i, r in enumerate(runs, 1):
        print("run %d positives %d/%d negatives %d/%d errors %d failures %s" % (
            i, r["positives_ok"], r["positives_total"], r["negatives_ok"], r["negatives_total"],
            r["error_rows"], ",".join(r["failures"]) or "-"))
    print("verdict %s" % verdict)
    return {"met": 0, "unmet": 1, "could-not-evaluate": 3}[verdict]


if __name__ == "__main__":
    sys.exit(main())
