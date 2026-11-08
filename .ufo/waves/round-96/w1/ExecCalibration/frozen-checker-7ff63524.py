#!/usr/bin/env python3
"""Round-96 calibration checker: counts mismatches between the lane's recorded self-assessment and
its committed bytes, one finding per routed round-95 defect the r96 declaration froze.

Findings (one id each):
  F1 quality-m1-criterion   corpus/QUALITY.md carries criterion 140, and its block cites
                            round-95.md, M1 and a development run (the r95 lesson's captured-by
                            `none` fix; routed defect 2).
  F2 void-receipt           .ufo/waves/round-96/before/r95-registry-gate.sha256 records the sha256
                            of tools/check-registry-coverage.py, the same line is pinned in the r96
                            freeze manifest, and SCORECARD.md's "Round 96" section binds the r95 C2
                            void clause to an empty `git diff` over that path (routed defect 3).
  F3 docstring-superseded   tools/limine-pin-battery-r95.py and tools/make-r95-bends.py no longer
                            say "largest in-bound" and say "boundary member"; the round lesson
                            records how the r95 freeze manifest relates to the edited bytes
                            (routed defect 4).
  F4 readme-scope           corpus/README.md scopes the r95 A4 sentence to "the r94 family roster"
                            and no longer says the whole before instrument lacks an in-bound case
                            (routed defect 5).
  F5 tip-receipt            .ufo/waves/round-96/before/c2-tip-b8f878c8.json is the registry gate's
                            PASS receipt at the r95 tip (revision, counts 151/151, findings 0;
                            routed defect 6).
  F6 report-count           (with --report) the report's falsification-ledger sentence states the
                            verdict-class counts the committed claim-falsification.tsv holds
                            (routed defect 1: r95 said four, the TSV had six).

Usage: check-r96-calibration.py [--root DIR] [--report FILE] [--json OUT] [--selftest]
Exit: 0 no findings; 1 findings; 2 usage/could-not-evaluate.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_GATE = "tools/check-registry-coverage.py"
R95_TOOLS = ("tools/limine-pin-battery-r95.py", "tools/make-r95-bends.py")
RECEIPT = ".ufo/waves/round-96/before/r95-registry-gate.sha256"
MANIFEST = ".ufo/waves/round-96/before/instruments.sha256"
TIP_RECEIPT = ".ufo/waves/round-96/before/c2-tip-b8f878c8.json"
TSV = ".ufo/waves/round-96/claim-falsification.tsv"


def read(root, rel, errors):
    path = os.path.join(root, rel)
    try:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
            return f.read()
    except OSError as e:
        errors.append("%s: %s" % (rel, e.strerror or e))
        return None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def criterion_block(text, number):
    marks = list(re.finditer(r"^\d+\. \*\*", text, re.M))
    for i, m in enumerate(marks):
        if m.group(0).startswith("%d." % number):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            return text[m.start():end]
    return None


def check(root, report=None, tsv_path=TSV):
    findings = []
    errors = []
    quality = read(root, "corpus/QUALITY.md", errors)
    block = criterion_block(quality or "", 140)
    if block is None:
        findings.append(("F1", "QUALITY.md has no criterion 140"))
    else:
        missing = [t for t in ("round-95.md", "M1", "development run") if t not in block]
        if missing:
            findings.append(("F1", "criterion 140 lacks %s" % ",".join(missing)))

    receipt = read(root, RECEIPT, errors)
    manifest = read(root, MANIFEST, errors)
    gate_path = os.path.join(root, REGISTRY_GATE)
    want_hash = None
    if receipt is None:
        findings.append(("F2", "receipt %s missing" % RECEIPT))
    else:
        m = re.search(r"([0-9a-f]{64})\s+%s" % re.escape(REGISTRY_GATE), receipt)
        if not m:
            findings.append(("F2", "receipt does not name %s with a sha256" % REGISTRY_GATE))
        else:
            want_hash = m.group(1)
            if not os.path.isfile(gate_path):
                findings.append(("F2", "%s missing" % REGISTRY_GATE))
            elif sha256_file(gate_path) != want_hash:
                findings.append(("F2", "receipt hash != current %s" % REGISTRY_GATE))
        if manifest is None or want_hash not in (manifest or ""):
            findings.append(("F2", "the r96 freeze manifest does not pin the receipt hash"))
    scorecard = read(root, "SCORECARD.md", errors)
    if scorecard is None or "## Round 96" not in scorecard:
        findings.append(("F2", "SCORECARD.md has no Round 96 section"))
    else:
        sec = scorecard[scorecard.index("## Round 96"):]
        for t in ("void", "git diff", "check-registry-coverage.py"):
            if t not in sec:
                findings.append(("F2", "Round 96 section lacks %r" % t))
                break

    for rel in R95_TOOLS:
        text = read(root, rel, errors)
        if text is None:
            findings.append(("F3", "%s missing" % rel))
            continue
        if "largest in-bound" in text:
            findings.append(("F3", "%s still says largest in-bound" % rel))
        if "boundary member" not in text:
            findings.append(("F3", "%s does not say boundary member" % rel))
    lesson = read(root, "corpus/lessons/round-96.md", errors)
    if lesson is None or "r95 freeze manifest" not in lesson:
        findings.append(("F3", "lesson does not relate the r95 freeze manifest to the edits"))

    readme = read(root, "corpus/README.md", errors)
    if readme is None or "r94 family roster" not in readme:
        findings.append(("F4", "README does not scope the sentence to the r94 family roster"))
    if readme is not None and "before instrument has no in-bound" in readme:
        findings.append(("F4", "README still over-scopes the before instrument"))

    tip = read(root, TIP_RECEIPT, errors)
    if tip is None:
        findings.append(("F5", "tip receipt %s missing" % TIP_RECEIPT))
    else:
        try:
            d = json.loads(tip)
            bad = (d.get("status") != "PASS" or not str(d.get("revision", "")).startswith("b8f878c8")
                   or d.get("counts", {}).get("tools_total") != 151
                   or d.get("counts", {}).get("registered") != 151
                   or d.get("counts", {}).get("findings") != 0)
            if bad:
                findings.append(("F5", "tip receipt is not the r95-tip PASS 151/151 receipt"))
        except Exception:
            findings.append(("F5", "tip receipt is not JSON"))

    if report is not None:
        text = read(root, report, errors) if not os.path.isabs(report) else _read_abs(report, errors)
        if text is None:
            findings.append(("F6", "report unreadable"))
        else:
            tsv = read(root, tsv_path, errors)
            if tsv is None:
                findings.append(("F6", "claim-falsification.tsv missing"))
            else:
                rows = [ln.split("\t") for ln in tsv.splitlines() if ln.strip()]
                want = {"falsifies-wording": 0, "falsifies-number": 0}
                for r in rows:
                    if len(r) >= 3 and r[2] in want:
                        want[r[2]] += 1
                for cls, n in want.items():
                    m = re.search(r"(\d+)\s+`?%s" % cls, text)
                    if not m:
                        findings.append(("F6", "report states no %s count" % cls))
                    elif int(m.group(1)) != n:
                        findings.append(("F6", "report says %s %s, tsv has %d"
                                         % (m.group(1), cls, n)))
    return findings, errors


def _read_abs(path, errors):
    try:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
            return f.read()
    except OSError as e:
        errors.append("%s: %s" % (path, e.strerror or e))
        return None


def _fixture(base, report_text=None, tsv_text=None):
    """A minimal tree satisfying every finding's condition; --selftest then breaks one field."""
    files = {
        "corpus/QUALITY.md": "139. **old**\nLesson: x\n\n140. **A clause re-read against a development run (R95-M1):** text cites `corpus/lessons/round-95.md` M1 and a development run.\nLesson: `corpus/lessons/round-95.md` Mistakes `M1`.\n",
        "corpus/README.md": "The r94 family roster has no in-bound 9-digit case.\n",
        "corpus/lessons/round-96.md": "## Gate\nHow the r95 freeze manifest relates: it pins the b8f878c8 bytes.\n",
        "SCORECARD.md": "## Round 96\nvoid if `git diff` over tools/check-registry-coverage.py is empty.\n",
        REGISTRY_GATE: "#!/usr/bin/env python3\nprint('fixture')\n",
        "tools/limine-pin-battery-r95.py": "# a boundary member; never largest\n",
        "tools/make-r95-bends.py": "# boundary member\n",
        ".ufo/waves/round-96/claim-falsification.tsv": "C1\tx\tneutral\t-\ta\nC1\tx\tfalsifies-wording\tA1\tb\nC2\tx\tfalsifies-number\tA2\tc\nC2\tx\tfalsifies-wording\tA3\td\nC2\tx\tfalsifies-wording\tA4\te\n",
        ".ufo/waves/round-96/before/c2-tip-b8f878c8.json": json.dumps({
            "status": "PASS", "revision": "b8f878c8ffff",
            "counts": {"tools_total": 151, "registered": 151, "findings": 0}}),
    }
    for rel, content in files.items():
        p = os.path.join(base, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
    gate = os.path.join(base, REGISTRY_GATE)
    h = sha256_file(gate)
    os.makedirs(os.path.join(base, ".ufo/waves/round-96/before"), exist_ok=True)
    with open(os.path.join(base, RECEIPT), "w", encoding="utf-8") as f:
        f.write("%s  %s\n" % (h, REGISTRY_GATE))
    with open(os.path.join(base, MANIFEST), "w", encoding="utf-8") as f:
        f.write("%s  %s\n" % (h, REGISTRY_GATE))
    rep = report_text if report_text is not None else "3 falsifies-wording rows and 1 falsifies-number row.\n"
    rp = os.path.join(base, "report.md")
    with open(rp, "w", encoding="utf-8") as f:
        f.write(rep)
    return rp


def selftest():
    base = tempfile.mkdtemp(prefix="r96-cal-selftest-")
    results = []
    try:
        rp = _fixture(base)
        f, e = check(base, rp)
        results.append(("clean", f == [], f))
        defects = {
            "F1": lambda b: _edit(b, "corpus/QUALITY.md", "140. **", "999. **"),
            "F2": lambda b: _edit(b, RECEIPT, re.search(r"[0-9a-f]{64}", read(b, RECEIPT, [])).group(0), "0" * 64),
            "F3": lambda b: _edit(b, "tools/limine-pin-battery-r95.py", "a boundary member", "the largest in-bound member"),
            "F4": lambda b: _edit(b, "corpus/README.md", "The r94 family roster has no", "The before instrument has no"),
            "F5": lambda b: _edit(b, TIP_RECEIPT, '"status": "PASS"', '"status": "FAIL"'),
            "F6": lambda b: _write(os.path.join(b, "report.md"), "four falsifies-wording rows and 1 falsifies-number row.\n"),
        }
        for fid, mutate in defects.items():
            d = tempfile.mkdtemp(prefix="r96-cal-mut-", dir=base)
            shutil.copytree(base, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("r96-cal-mut-*"))
            mutate(d)
            f, _ = check(d, os.path.join(d, "report.md"))
            ids = sorted({x[0] for x in f})
            results.append((fid, ids == [fid], f))
            shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    ok = all(x[1] for x in results)
    for name, good, detail in results:
        print("%-6s %s %s" % (name, "PASS" if good else "FAIL", "" if good else detail))
    print("selftest %s %d/%d" % ("PASS" if ok else "FAIL", sum(1 for x in results if x[1]), len(results)))
    return 0 if ok else 1


def _edit(root, rel, old, new):
    p = os.path.join(root, rel)
    with open(p, "r", encoding="utf-8", errors="surrogateescape") as f:
        text = f.read()
    assert old in text, (rel, old)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text.replace(old, new, 1))


def _write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--report")
    ap.add_argument("--tsv", default=TSV)
    ap.add_argument("--json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    findings, errors = check(os.path.abspath(a.root), a.report, a.tsv)
    out = {"schema": "tsukuroi-r96-calibration-v1", "root": os.path.abspath(a.root),
           "report": a.report, "findings": [{"id": i, "detail": d} for i, d in findings],
           "unreadable": errors, "status": "FAIL" if findings or errors else "PASS"}
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))
    return 1 if (findings or errors) else 0


if __name__ == "__main__":
    sys.exit(main())
