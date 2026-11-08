#!/usr/bin/env python3
"""Emit the ten single-element launcher mutants of limine-pin-battery-r92.py (MutBattery seat).

Each mutant is a byte copy of the frozen battery with ONE launcher element changed. Every
substitution is asserted to occur exactly once so a mutant cannot silently be a no-op.
"""
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "battery-pristine.py")
OUT = os.path.join(S, "mutants")

# (id, element, [(old, new, expected_count), ...])
MUTANTS = [
    ("m1", "drop --clearenv", [
        ('"--unshare-all", "--die-with-parent", "--new-session", "--clearenv",',
         '"--unshare-all", "--die-with-parent", "--new-session",', 1)]),
    ("m2", "drop --unshare-all (binds kept)", [
        ('[BWRAP, "--unshare-all", "--die-with-parent",',
         '[BWRAP, "--die-with-parent",', 1)]),
    ("m3", "drop -I from the inner python argv", [
        ('inner = [sys.executable, "-I", gate, "--conf", conf, "--esp", esp]',
         'inner = [sys.executable, gate, "--conf", conf, "--esp", esp]', 1)]),
    ("m4", "skip copy_gate (gate runs in place)", [
        ('    d = tempfile.mkdtemp(prefix="gate-", dir=work)\n'
         '    dst = os.path.join(d, "gate.py")\n'
         '    shutil.copyfile(gate, dst)\n'
         '    return d, dst',
         '    p = os.path.abspath(gate)\n'
         '    return os.path.dirname(p), p', 1)]),
    ("m5", "drop --ro-bind case_dir case_dir", [
        ('"--ro-bind", gate, gate, "--ro-bind", case_dir, case_dir,',
         '"--ro-bind", gate, gate,', 1)]),
    ("m6", "drop --unshare-pid only (explicit namespaces, net kept isolated)", [
        ('"--unshare-all", "--die-with-parent"',
         '"--unshare-user", "--unshare-uts", "--unshare-cgroup", "--unshare-ipc",\n'
         '            "--unshare-net", "--die-with-parent"', 1)]),
    ("m7", "gate copy dir shared with the case dir", [
        ('            gdir, gpath = copy_gate(gate, root)',
         '            gdir, gpath = None, None', 1),
        ('            c, d, conf, esp = build(fam, rng, root)\n'
         '            want = c.finish()',
         '            c, d, conf, esp = build(fam, rng, root)\n'
         '            gdir, gpath = copy_gate(gate, d)\n'
         '            want = c.finish()', 1)]),
    ("m8", "drop --setenv HOME and TMPDIR", [
        ('"--chdir", case_dir, "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", "/tmp",\n'
         '            "--setenv", "LC_ALL", "C", "--setenv", "TMPDIR", "/tmp", "--"] + inner',
         '"--chdir", case_dir, "--setenv", "PATH", "/usr/bin",\n'
         '            "--setenv", "LC_ALL", "C", "--"] + inner', 1)]),
    ("m9", "bind the original gate path as well as the copy", [
        ('BWRAP = shutil.which("bwrap")',
         'BWRAP = shutil.which("bwrap")\n'
         'ORIGINAL_GATE = None  # m9: the original gate path, bound in addition to the copy', 1),
        ('"--ro-bind", gate, gate, "--ro-bind", case_dir, case_dir,',
         '"--ro-bind", gate, gate] + (["--ro-bind", ORIGINAL_GATE, ORIGINAL_GATE]\n'
         '                                  if ORIGINAL_GATE and ORIGINAL_GATE != gate else []) + [\n'
         '            "--ro-bind", case_dir, case_dir,', 1),
        ('    rng = random.Random(secrets.randbits(64))\n'
         '    root = tempfile.mkdtemp(prefix="limine-battery-r92-", dir=work)\n'
         '    gdir = gpath = None',
         '    global ORIGINAL_GATE\n'
         '    ORIGINAL_GATE = gate\n'
         '    rng = random.Random(secrets.randbits(64))\n'
         '    root = tempfile.mkdtemp(prefix="limine-battery-r92-", dir=work)\n'
         '    gdir = gpath = None', 1)]),
    ("m10", "drop the --limine-version pass-through", [
        ('    if c.pass_version:\n'
         '        inner += ["--limine-version", c.version]',
         '    if False and c.pass_version:  # m10: the version pass-through is dropped\n'
         '        inner += ["--limine-version", c.version]', 1)]),
]


def main():
    src = open(SRC, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    for mid, element, subs in MUTANTS:
        text = src
        for old, new, want in subs:
            n = text.count(old)
            if n != want:
                sys.exit("%s: pattern occurs %d times, want %d:\n%s" % (mid, n, want, old))
            text = text.replace(old, new, 1)
        if text == src:
            sys.exit("%s: mutant is byte-identical to the pristine battery" % mid)
        dst = os.path.join(OUT, mid + ".py")
        with open(dst, "w", encoding="utf-8") as f:
            f.write(text)
        # a mutant must still compile and still declare the same roster/launcher shape
        subprocess.run([sys.executable, "-m", "py_compile", dst], check=True)
        subprocess.run(["sh", "-c", "diff -u %s %s > %s.diff; true" %
                        (SRC, dst, os.path.join(OUT, mid))], check=True)
        print("%s  %-62s  %s" % (mid, element, "ok"))


if __name__ == "__main__":
    main()
