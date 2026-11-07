#!/usr/bin/env python3
"""Build single-point mutants of tools/battery-discrimination-r89.py inside a clone; append one manifest
line per mutant to the CLONE's freeze manifest (the counter requires the file it runs to be named there).

usage: mkmutants.py LANE [--clone2]
"""
import hashlib
import json
import os
import sys

LANE = sys.argv[1]
COUNTER = os.path.join(LANE, "tools", "battery-discrimination-r89.py")
MANIFEST = os.path.join(LANE, ".ufo", "waves", "round-89", "before", "freeze-manifest.sha256")

MUTANTS = [
    ("m01-bind-root",
     'return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",\n'
     '            "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64", "--symlink", "usr/bin", "/sbin",\n'
     '            "--ro-bind", "/etc", "/etc", "--dev", "/dev",',
     'return ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev",',
     "sandbox: bind the whole host root read-only instead of the /usr+/etc allowlist"),
    ("m02-no-unshare",
     '"--bind", d, d, "--chdir", d, "--unshare-all", "--die-with-parent", "--clearenv",',
     '"--bind", d, d, "--chdir", d, "--die-with-parent", "--clearenv",',
     "sandbox: drop --unshare-all (net/pid/ipc/uts/cgroup namespaces shared with the host)"),
    ("m03-no-clearenv",
     '"--bind", d, d, "--chdir", d, "--unshare-all", "--die-with-parent", "--clearenv",',
     '"--bind", d, d, "--chdir", d, "--unshare-all", "--die-with-parent",',
     "sandbox: drop --clearenv (host environment inherited by the battery)"),
    ("m04-preflight-true",
     '        return p.returncode == 0 and p.stdout.strip() == "isolated", (p.stdout + p.stderr).strip()[-300:]',
     '        return True, "isolated (mutant)"',
     "preflight: always report isolated (skip the probe's verdict)"),
    ("m05-error-as-wrong",
     'rows.append({"id": g["id"], "expect": g["expect"], "got": got, "families_passed": fp,\n'
     '                         "error": got.startswith("error:"), "ok": got == g["expect"]})',
     'rows.append({"id": g["id"], "expect": g["expect"], "got": got, "families_passed": fp,\n'
     '                         "error": False, "ok": got == g["expect"]})',
     "error rows: never classified as errors, counted as plain misses (verdict unmet, never exit 3)"),
    ("m06-skip-manifest",
     '    bad = check_manifest()\n    if bad:',
     '    bad = []\n    if bad:',
     "freeze: skip check_manifest entirely"),
    ("m07-unlisted-ok",
     '    bad += sorted("unlisted:" + os.path.relpath(p, LANE) for p in need - named)',
     '    pass',
     "freeze: do not require every roster file (counter, roster, gates, support) to be named in the manifest"),
    ("m08-real-gate-path",
     '        argv = sandbox_argv(d, work) + [PYTHON, bp, "--gate", lp, "--runs", "1", "--work", work, "--json", out]',
     '        argv = sandbox_argv(d, work) + [PYTHON, bp, "--gate", gate_path, "--runs", "1", "--work", work, "--json", out]',
     "opaque launcher: hand the battery the real (unmounted) gate path instead of the launcher"),
    ("m09-no-cwd-check",
     '                cwd = os.path.realpath(req["cwd"])\n'
     '                if cwd != d and not cwd.startswith(d + os.sep):\n'
     '                    raise ValueError("cwd outside the case directory")',
     '                cwd = os.path.realpath(req["cwd"])',
     "launcher server: drop the check that the requested cwd lies inside the case directory"),
    ("m10-inverted-verdict",
     '        if p.returncode == 0 and verdict == "met":\n'
     '            return "met", fp\n'
     '        if p.returncode == 1 and verdict == "unmet":\n'
     '            return "unmet", fp',
     '        if p.returncode == 0 and verdict == "met":\n'
     '            return "unmet", fp\n'
     '        if p.returncode == 1 and verdict == "unmet":\n'
     '            return "met", fp',
     "verdict mapping: swapped (met<->unmet) when the battery's rc and verdict agree"),
    ("m11-swap-expect",
     '    rows.sort(key=lambda r: r["id"])\n'
     '    pos = [r for r in rows if r["expect"] == "met"]\n'
     '    neg = [r for r in rows if r["expect"] == "unmet"]',
     '    rows.sort(key=lambda r: r["id"])\n'
     '    pos = [r for r in rows if r["expect"] == "unmet"]\n'
     '    neg = [r for r in rows if r["expect"] == "met"]',
     "tally: positives and negatives swapped in the met test (P-progress reported against N rows)"),
]

src = open(COUNTER, encoding="utf-8").read()
lines = []
built = []
for name, old, new, desc in MUTANTS:
    if src.count(old) != 1:
        print("FAIL %s: old_string occurs %d times" % (name, src.count(old)))
        sys.exit(1)
    text = src.replace(old, new)
    p = os.path.join(LANE, "tools", name + ".py")
    open(p, "w", encoding="utf-8").write(text)
    rel = os.path.relpath(p, LANE)
    built.append({"mutant": name, "path": rel, "sha256": hashlib.sha256(text.encode()).hexdigest(), "desc": desc})
    lines.append("%s  %s\n" % (hashlib.sha256(text.encode()).hexdigest(), rel))

man = open(MANIFEST, encoding="utf-8").read()
if not man.endswith("\n"):
    man += "\n"
open(MANIFEST, "w", encoding="utf-8").write(man + "".join(lines))
print(json.dumps({"lane": LANE, "manifest_sha256": hashlib.sha256((man + "".join(lines)).encode()).hexdigest(),
                  "mutants": built}, indent=1))
