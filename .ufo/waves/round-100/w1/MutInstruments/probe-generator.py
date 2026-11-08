#!/usr/bin/env python3
"""Round-100 w1 seat MutInstruments: run the pristine generator and the B1/B2/B3 mutants in a
throw-away fake lane under the seat scratch dir, so nothing is written into the lane's frozen
wave dirs.

The generator derives its LANE from `__file__` (dirname(dirname(abspath(__file__)))), so a fake lane
`<scratch>/probe/<case>/tools/make-r100-bends.py` reads `<case>/tools/check-limine-pins.py` and
writes `<case>/.ufo/waves/round-100/before/controls/bends/`. That is exactly the lane layout, in
scratch.

Usage: probe-generator.py <scratch>/bin <scratch>/probe <receipts-dir>
"""
import difflib
import hashlib
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
GATE = os.path.join(LANE, "tools", "check-limine-pins.py")
BENDS = os.path.join(LANE, "tools", "make-r100-bends.py")
FROZEN = os.path.join(LANE, ".ufo", "waves", "round-100", "before", "controls", "bends")

PATTERN = ('    return {"schema": "tsukuroi-limine-pins-v3", "verdict": verdict, "rc": rc,\n'
           '            "limine_version": limine_version,\n'
           '            "limine_version_source": limine_version_source,\n'
           '            "visibility_era": "12.9.5+" if era_b else "pre-12.9.5",')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def changed_lines(a, b):
    diff = list(difflib.unified_diff(a.splitlines(True), b.splitlines(True),
                                     "gate", "emitted", n=0))
    return (sum(1 for line in diff if line.startswith("-") and not line.startswith("---")),
            sum(1 for line in diff if line.startswith("+") and not line.startswith("+++")),
            "".join(diff))


def run_case(probe_root, receipt, case, gate_bytes, generator_name, expect):
    case_dir = os.path.join(probe_root, case)
    if os.path.isdir(case_dir):
        shutil.rmtree(case_dir)
    tools = os.path.join(case_dir, "tools")
    os.makedirs(tools)
    gate_path = os.path.join(tools, "check-limine-pins.py")
    with open(gate_path, "wb") as f:
        f.write(gate_bytes)
    os.chmod(gate_path, 0o755)
    gen_path = os.path.join(tools, "make-r100-bends.py")
    shutil.copyfile(generator_name, gen_path)
    os.chmod(gen_path, 0o755)
    out = os.path.join(case_dir, ".ufo", "waves", "round-100", "before", "controls", "bends")
    p = subprocess.run([sys.executable, "-I", gen_path], cwd=case_dir,
                       capture_output=True, text=True, timeout=120,
                       env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": case_dir})
    emitted = {}
    if os.path.isdir(out):
        for name in sorted(os.listdir(out)):
            with open(os.path.join(out, name), "rb") as f:
                emitted[name] = f.read()
    lines = ["=== CASE %s (gate %s, generator %s)" % (case, expect["gate"], generator_name)]
    lines.append("expect: %s" % expect["why"])
    lines.append("rc=%d" % p.returncode)
    if p.stdout.strip():
        lines.append("stdout: " + p.stdout.strip().replace("\n", " | "))
    if p.stderr.strip():
        lines.append("stderr: " + p.stderr.strip().replace("\n", " | "))
    lines.append("emitted files: %s" % (sorted(emitted) or "none"))
    verdict = expect["check"](p.returncode, emitted, gate_bytes)
    for name, data in emitted.items():
        minus, plus, diff = changed_lines(gate_bytes.decode(), data.decode("utf-8", "replace"))
        lines.append("  %-22s sha256=%s bytes=%d changed_lines(-/%d +/%d)"
                     % (name, sha(data), len(data), minus, plus))
        if minus + plus <= 4 and diff:
            lines.append("    diff: " + diff.replace("\n", "\n    "))
    lines.append("CASE VERDICT: %s %s" % verdict)
    receipt.append("\n".join(lines))
    return verdict


def main():
    bindir, probe_root, receipts = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(GATE, "rb") as f:
        gate = f.read()
    with open(BENDS, "rb") as f:
        pristine_gen = os.path.join(bindir, "GEN-pristine.py")
        with open(pristine_gen, "wb") as g:
            g.write(f.read())
    os.chmod(pristine_gen, 0o755)

    zero = gate.replace(PATTERN.encode(), PATTERN.replace(
        '"rc": rc,\n', '"rc": rc, "probe": 0,\n').encode())
    assert zero != gate and zero.count(PATTERN.encode()) == 0, "zero-match gate not built"
    two = gate + ("\n\ndef _dup_probe(verdict, rc, limine_version, limine_version_source, era_b):\n"
                  + PATTERN + '\n            "pins": []}\n').encode()
    assert two.count(PATTERN.encode()) == 2, "two-match gate not built (%d)" % two.count(
        PATTERN.encode())
    for name, data in (("gate-pristine", gate), ("gate-zero-match", zero),
                       ("gate-two-match", two)):
        with open(os.path.join(bindir, name + ".py"), "wb") as f:
            f.write(data)
        os.chmod(os.path.join(bindir, name + ".py"), 0o755)

    def one_bend(name, n):
        return lambda rc, emitted, _g: (
            ("killed" if (name not in emitted or rc != 0) else "survived"),
            "rc=%d %s" % (rc, "emitted" if name in emitted else "not emitted"))

    receipt = []
    results = []

    def add(verdict):
        results.append(verdict)

    # 1. pristine generator on the pristine gate: the probe layout is faithful iff the emitted
    #    bytes equal the frozen bends.
    def faithful(rc, emitted, _g):
        same = {}
        for name in ("N12-x-echo.py", "N13-y-echo.py"):
            path = os.path.join(FROZEN, name)
            with open(path, "rb") as f:
                same[name] = emitted.get(name) == f.read()
        ok = rc == 0 and all(same.values())
        return ("repr-faithful" if ok else "LAYOUT-BROKEN"), "rc=%d byte-equal-to-frozen=%s" % (
            rc, same)
    add(run_case(probe_root, receipt, "01-pristine-on-pristine",
                 gate, pristine_gen,
                 dict(gate="pristine", why="the scratch layout reproduces the frozen bend bytes",
                      check=faithful)))

    # 2/3. B1: the exact-once guard. Detector = the pristine refusal; defect = emission anyway.
    def refused(rc, emitted, _g):
        ok = rc != 0 and not emitted
        return ("control-refuses" if ok else "CONTROL-BROKEN"), "rc=%d emitted=%s" % (
            rc, sorted(emitted))
    add(run_case(probe_root, receipt, "02-pristine-on-zero-match",
                 zero, pristine_gen,
                 dict(gate="zero-match", why="pristine refuses a pattern matched 0 times",
                      check=refused)))

    def noop_emitted(rc, emitted, gbytes):
        identical = {n: d == gbytes for n, d in emitted.items()}
        if rc != 0 and not emitted:
            return ("masked", "rc=%d refused by the surviving no-op guard" % rc)
        ok = len(emitted) == 2 and all(identical.values())
        return ("killed-silent-noop" if ok else "survived"), (
            "rc=%d emitted=%s identical-to-gate=%s" % (rc, sorted(emitted), identical))
    add(run_case(probe_root, receipt, "03-B1-on-zero-match",
                 zero, os.path.join(bindir, "B1.py"),
                 dict(gate="zero-match",
                      why="B1 has no count guard; on a 0-match pattern it can only be stopped by "
                          "the no-op guard (masking) or emit a no-op article (defect)",
                      check=noop_emitted)))

    add(run_case(probe_root, receipt, "04-pristine-on-two-match",
                 two, pristine_gen,
                 dict(gate="two-match", why="pristine refuses a pattern matched twice",
                      check=refused)))

    def two_hunks(rc, emitted, gbytes):
        # contract: a non-exactly-once pattern is REFUSED (rc != 0, nothing emitted). B1 bends
        # both matches instead: rc 0 and 2 changed lines per article (the one-clause rule broken).
        counts = {n: changed_lines(gbytes.decode(), d.decode("utf-8", "replace"))[:2]
                  for n, d in emitted.items()}
        defect = rc == 0 and counts and all(c != (1, 1) for c in counts.values())
        return ("killed" if defect else "survived"), "rc=%d changed_lines=%s" % (rc, counts)
    add(run_case(probe_root, receipt, "05-B1-on-two-match",
                 two, os.path.join(bindir, "B1.py"),
                 dict(gate="two-match",
                      why="B1 bends both matches (2 changed lines per article) instead of refusing",
                      check=two_hunks)))

    # 6/7. B2: the no-op guard.
    add(run_case(probe_root, receipt, "06-P-B2-control",
                 gate, os.path.join(bindir, "P-B2-pristine-noop-variant.py"),
                 dict(gate="pristine",
                      why="pristine generator with a no-op N12 replacement refuses",
                      check=refused)))

    def emitted_noop(rc, emitted, gbytes):
        n12 = emitted.get("N12-x-echo.py")
        ok = rc == 0 and n12 == gbytes and "N13-y-echo.py" in emitted
        return ("killed" if ok else "survived"), "rc=%d N12-identical-to-gate=%s emitted=%s" % (
            rc, n12 == gbytes, sorted(emitted))
    add(run_case(probe_root, receipt, "07-B2-on-pristine",
                 gate, os.path.join(bindir, "B2.py"),
                 dict(gate="pristine", why="B2 emits the gate itself as the N12 article",
                      check=emitted_noop)))

    # 8. B3: the X bend keyed on the wrong component.
    def wrong_key(rc, emitted, _gbytes):
        n12 = emitted.get("N12-x-echo.py", b"").decode("utf-8", "replace")
        keyed_on_second = 'split(".")[1] == "999999999"' in n12
        ok = rc == 0 and keyed_on_second
        return ("killed" if ok else "survived"), "rc=%d N12-keyed-on-second=%s" % (
            rc, keyed_on_second)
    add(run_case(probe_root, receipt, "08-B3-on-pristine",
                 gate, os.path.join(bindir, "B3.py"),
                 dict(gate="pristine",
                      why="B3 emits an N12 article keyed on the second component (no X lie)",
                      check=wrong_key)))

    text = "\n\n".join(receipt) + "\n"
    with open(os.path.join(receipts, "04-generator-probes.txt"), "w") as f:
        f.write(text)
    print(text)
    print("cases: " + ", ".join("%s=%s" % (r[0], r[1].split(" ", 1)[0]) for r in results))


if __name__ == "__main__":
    main()
