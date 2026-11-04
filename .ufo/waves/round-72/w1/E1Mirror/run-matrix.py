#!/usr/bin/env python3
"""E1Mirror mutation matrix: run the frozen counter and the independent reader on the
mirror control plus named mutants, and print a per-row verdict comparison.

Usage: run-matrix.py <scratch-root>
Builds <scratch-root>/mirror via build-mirror.py, mutants under <scratch-root>/mutants,
and writes <scratch-root>/matrix.txt. Writes nothing else.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
COUNTER = LANE / "tools/count-md-rows-r72.py"
READER = HERE / "reader.py"
NOTE_REL = "corpus/knowledge/modprobe-config-plane-r72.md"
REG_REL = "corpus/SOURCES.md"
MAP_REL = ".ufo/waves/round-72/before/src/SOURCES.json"
DOC = "modprobe.d.5.scd"


def run(tool, root):
    args = [sys.executable, str(tool)]
    args += ["--fixture", str(root)] if tool == COUNTER else [str(root)]
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def counter_rows(out):
    rows = {}
    for m in re.finditer(r"^MD_ROW (ok|fail) MD(\d+)(.*)$", out, re.M):
        rows[int(m.group(2))] = (m.group(1), m.group(3).strip())
    met = re.search(r"met=(\d)", out)
    return rows, (met.group(1) == "1" if met else None)


def reader_rows(out):
    rows = {}
    for m in re.finditer(r"^READER row MD(\d+) (ok|red)(.*)$", out, re.M):
        rows[int(m.group(1))] = (m.group(2), m.group(3).strip())
    summary = re.search(r"^READER rows=(\d+) ok=(\d+) red=(\d+)", out, re.M)
    return rows, (summary.groups() if summary else None)


def mutate(name, root, snapmap):
    note_p = root / NOTE_REL
    reg_p = root / REG_REL
    map_p = root / MAP_REL
    note = note_p.read_text()
    reg = reg_p.read_text()
    smap = json.loads(map_p.read_text())
    doc_norm = " ".join((root / ".ufo/waves/round-72/before/src" / DOC)
                        .read_text().split())

    if name == "quote-foreign":  # quote from libkmod-config.c on a doc-citing row
        note = note.replace(
            "Configuration files are read from directories in listed in SYNOPSIS in that order of precedence.",
            "Ignoring duplicate config file: %s/%s", 1)
    elif name == "short-statement":
        note = note.replace(
            "Configuration directories are read in SYNOPSIS precedence order; once a filename is "
            "loaded, the same name in subsequent directories is ignored.",
            "Configuration directories are read in precedence order.", 1)
    elif name == "ownwork-kind":
        reg = reg.replace("| docs | A |", "| own-work | A |", 1)
    elif name == "map-digest":
        smap["snapshots"]["modprobe.c"]["sha256"] = "0" * 64
    elif name == "reuse-three":
        md2 = next(l for l in note.splitlines() if l.startswith("| MD2 |"))
        md5 = "| MD5" + md2[len("| MD2"):]
        note = "\n".join(md5 if l.startswith("| MD5 |") else l for l in note.splitlines()) + "\n"
    elif name == "malformed-row":
        note = note + "| MD7 | invisible broken row |\n"
    elif name == "long-quote":
        start = doc_norm.index("Because the *modprobe* command")
        long_q = " ".join(doc_norm[start:].split()[:30])
        assert long_q in doc_norm and len(long_q.split()) == 30
        note = note.replace(
            "Configuration files are read from directories in listed in SYNOPSIS in that order of precedence.",
            long_q, 1)
    elif name == "anchor-missing":
        reg = reg.replace("tag v34; libkmod-config.c lines 920-1085",
                          "tag v34; lines 920-1085", 1)
    elif name == "source-url-missing":
        reg = reg.replace("https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/tools/modprobe.c?h=v34", "URL-REDACTED", 1)
    elif name == "digest-swap":
        note = note.replace(smap["snapshots"]["modprobe.c"]["sha256"], "0" * 64, 1)
    elif name == "quote-pipe":
        note = note.replace('quote="Ignoring duplicate config file: %s/%s"',
                            'quote="Ignoring duplicate config file: %s/%s | injected"', 1)
    elif name == "spacing":
        note = note.replace("| source=S301 |", "|  source=S301 |", 1)
    elif name == "duplicate-id":
        note = note.replace("| MD2 |", "| MD1 |", 1)
    elif name == "ungrounded-long":
        note = note.replace(
            "Configuration files can either be completely replaced by a new configuration file with "
            "the same name in a directory of higher priority, or partially replaced by a configuration "
            "file that is ordered later.",
            "Configuration files in later directories overwrite earlier ones according to priority rules.",
            1)
    else:
        raise SystemExit(f"unknown mutant {name}")
    note_p.write_text(note)
    reg_p.write_text(reg)
    map_p.write_text(json.dumps(smap, indent=1) + "\n")


def main():
    if len(sys.argv) != 2:
        print("usage: run-matrix.py <scratch-root>")
        return 2
    root = Path(sys.argv[1])
    mirror = root / "mirror"
    subprocess.run([sys.executable, str(HERE / "build-mirror.py"), str(mirror)],
                   check=True, capture_output=True)
    snapmap = json.loads((mirror / MAP_REL).read_text())
    mutants = ["quote-foreign", "short-statement", "ungrounded-long", "ownwork-kind",
               "map-digest", "reuse-three", "malformed-row", "long-quote",
               "anchor-missing", "source-url-missing", "digest-swap", "quote-pipe",
               "spacing", "duplicate-id"]
    out_lines = []
    findings = {}
    cases = [("control", mirror)] + [(m, root / "mutants" / m) for m in mutants]
    for name, dest in cases:
        if name != "control":
            shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(mirror, dest)
            mutate(name, dest, snapmap)
        crc, cout = run(COUNTER, dest)
        rrc, rout = run(READER, dest)
        crows, met = counter_rows(cout)
        rrows, summary = reader_rows(rout)
        cgreen = crc == 0 and met is True
        rgreen = rrc == 0 and summary is not None and summary[0] == "6" and summary[2] == "0"
        per_row = {}
        for n in range(1, 7):
            cv = crows.get(n, ("absent", ""))[0]
            rv = rrows.get(n, ("absent", ""))[0]
            per_row[n] = {"counter": cv, "counter_reason": crows.get(n, ("", ""))[1],
                          "reader": rv, "reader_reason": rrows.get(n, ("", ""))[1]}
        dis = [n for n in per_row
               if (per_row[n]["counter"] == "ok") != (per_row[n]["reader"] == "ok")]
        findings[name] = {"counter_rc": crc, "counter_met": met, "counter_green": cgreen,
                          "reader_rc": rrc, "reader_summary": summary, "reader_green": rgreen,
                          "row_disagreements": dis, "rows": per_row,
                          "counter_fail_rows": sorted(k for k, v in crows.items() if v[0] == "fail"),
                          "reader_red_rows": sorted(k for k, v in rrows.items() if v[0] == "red"),
                          "counter_out": cout, "reader_out": rout}
        verdict = "AGREE-GREEN" if cgreen and rgreen else (
                  "AGREE-RED" if (not cgreen and not rgreen) else "DISAGREE")
        out_lines.append(
            f"CASE {name}: {verdict} counter_rc={crc} met={int(met) if met is not None else -1} "
            f"reader_rc={rrc} reader_rows/ok/red={summary} "
            f"counter_fail={findings[name]['counter_fail_rows']} "
            f"reader_red={findings[name]['reader_red_rows']} row_disagreements={dis}")
    (root / "matrix.txt").write_text("\n".join(out_lines) + "\n")
    (root / "matrix.json").write_text(json.dumps(findings, indent=1) + "\n")
    print("\n".join(out_lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
