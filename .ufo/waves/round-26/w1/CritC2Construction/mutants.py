#!/usr/bin/env python3
"""Mutants of the b13e991 tree against the v2 reference model (refv2.py) and the v1 tool.

Each mutant: git archive b13e991 into a private sandbox, git init (no remote),
apply edits, commit, run refv2.py (and v1 for SHONEN mutants), write out/<name>.json.
"""
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-26/w1/CritC2Construction")
SCRATCH = "/fast/scratch/hyaku/tsuku26/CritC2Construction/sb"
V1 = "/fast/scratch/hyaku/tsuku26/CritC2Construction/v1tool.py"
BASE = "b13e991"
AXES = ("depth", "coverage", "operability", "freshness", "calibration", "adjacency")
BEFORE = {"depth": 8, "coverage": 9, "operability": 9, "freshness": 9, "calibration": 9, "adjacency": 8}


def sh(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def sandbox(name):
    path = os.path.join(SCRATCH, name)
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    arch = subprocess.run(["git", "-C", LANE, "archive", BASE], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", path], input=arch.stdout, check=True)
    sh("git", "-C", path, "init", "-q")
    return path


def commit(path):
    sh("git", "-C", path, "add", "-A")
    sh("git", "-C", path, "-c", "user.name=crit", "-c", "user.email=crit@local",
       "commit", "-q", "-m", "mutant")


def rd(path, rel):
    with open(os.path.join(path, rel)) as f:
        return f.read()


def wr(path, rel, text):
    with open(os.path.join(path, rel), "w") as f:
        f.write(text)


def r25_rows(sc):
    lines = sc.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("## Axes — current self-assessment (round 25)"))
    rows = []
    for l in lines[start + 1:]:
        if l.startswith("## "):
            break
        if l.startswith("|"):
            rows.append(l)
    return rows


def axes_table(sc, heading, scores=None):
    rows = r25_rows(sc)
    out = []
    for r in rows:
        cells = r.split("|")
        name = cells[1].strip().lower() if len(cells) > 2 else ""
        if scores and name in scores:
            cells[2] = " %d " % scores[name]
            r = "|".join(cells)
        out.append(r)
    return "\n%s\n\nAppended by the round-26 C2 repair (mutant).\n\n%s\n" % (heading, "\n".join(out))


OUTCOME = ("\n### Round 26 measured outcome\n\n| Claim | Before | After | Author verdict |\n|---|---|---|---|\n"
           "| C2 self-assessment mismatches (calibration, ordinal unchanged at 9) | 3 of 27 | 0 of 27 | met |\n")
TEN = {a: 10 for a in AXES}
PLAN = ", ".join("%s %d → 10" % (a, BEFORE[a]) for a in AXES) + "."
R26H = "## Axes — current self-assessment (round 26)"


def final(sc, scores=None, heading=R26H, extra_before_table="", extra_after=""):
    return sc.rstrip("\n") + "\n" + extra_before_table + axes_table(sc, heading, scores) + OUTCOME + extra_after


def m_score(path, fn):
    sc = rd(path, "SCORECARD.md")
    wr(path, "SCORECARD.md", fn(sc))


def m_shonen(path, old, new):
    s = rd(path, "SHONEN.md")
    assert old in s, old
    wr(path, "SHONEN.md", s.replace(old, new))


R12 = "corpus/knowledge/root-dac-decision-r12.md"
B1 = "round-12 root-metadata procedure; corpus/knowledge/root-dac-decision-r12.md."
B3 = "and corpus/knowledge/root-dac-decision-r12.md;"
B4 = "and .ufo/waves/round-12/resumed/OverlapHostR.md;"

MUTANTS = {
    # ---- K01-K06 ----
    "M0-final-realistic": lambda p: m_score(p, lambda sc: final(sc)),
    "M1-final-r25-regex-example-7": lambda p: m_score(p, lambda sc: final(
        sc.replace("`freshness (actual 9 → 9` is", "`freshness (actual 7 → 7` is"))),
    "M2-selfgrant-unnumbered-heading": lambda p: m_score(p, lambda sc: final(
        sc, TEN, extra_after="\n## Planned next round\n\nPlanned: %s\n" % PLAN)),
    "M3-selfgrant-Round26-nospace": lambda p: m_score(p, lambda sc: final(
        sc, TEN, extra_after="\n### Round26 declaration refinements\n\nPlanned: %s\n" % PLAN)),
    "M4-selfgrant-in-measured-outcome": lambda p: m_score(p, lambda sc: final(
        sc, TEN, extra_after="\nOrdinal moves recorded: %s\n" % PLAN)),
    "M5-selfgrant-round-26-hyphen": lambda p: m_score(p, lambda sc: final(
        sc, TEN, extra_after="\n### round-26 post-review corrections (appended)\n\n%s\n" % PLAN)),
    "M6-unnumbered-subsection-under-r26-decl": lambda p: m_score(p, lambda sc: final(
        sc, TEN, extra_before_table="\n### Declaration refinements after wave 1 (appended 2026-10-22; targets unchanged)\n\n- Planned: %s\n" % PLAN)),
    "M7-table-labelled-round-27": lambda p: m_score(p, lambda sc: final(
        sc.rstrip("\n") + "\n\nPlanned: %s\n" % PLAN, TEN,
        heading="## Axes — current self-assessment (round 27)")),
    "M8-table-heading-without-round": lambda p: m_score(p, lambda sc: final(
        sc, heading="## Axes — current self-assessment")),
    "M9-correction-section-calibration-10": lambda p: m_score(p, lambda sc: final(
        sc, {"calibration": 10},
        extra_after="\n## Post-review claim corrections (appended 2026-10-22)\n\n- calibration 9 → 10 after the v2 repair.\n")),
    # ---- K24-K27 ----
    "S0-unmodified": lambda p: None,
    "S1-cite-json-companion": lambda p: (
        m_shonen(p, B1, "round-12 root-metadata procedure; corpus/knowledge/root-dac-decision-r12.json."),
        m_shonen(p, B3, "and corpus/knowledge/root-dac-decision-r12.json;")),
    "S2-drop-note-citation": lambda p: (
        m_shonen(p, B1, "round-12 root-metadata procedure in SKILL.md."),
        m_shonen(p, B3, "and SKILL.md;")),
    "S3-reword-banner-replaced": lambda p: wr(p, R12, rd(p, R12).replace(
        "> **Superseded after outside rejection.**", "> **Replaced after outside rejection.**")),
    "S4-banner-pushed-past-line-20": lambda p: wr(p, R12, rd(p, R12).replace(
        "# Root-DAC create-failure decision matrix (round 12)\n",
        "# Root-DAC create-failure decision matrix (round 12)\n" + "".join(
            "reviewed-by: seat %d\n" % i for i in range(14)))),
    "S5-box4-cites-late-superseded-oom-note": lambda p: m_shonen(
        p, B4, "and .ufo/waves/round-12/resumed/OverlapHostR.md; OOM boundary in corpus/knowledge/oom-event-plane.md;"),
    "S6-box4-cites-unsuperseded-closeout-r11": lambda p: m_shonen(
        p, B4, "and .ufo/waves/round-12/resumed/OverlapHostR.md; register in corpus/knowledge/closeout-r11.md;"),
    "S7-box4-cites-supersession-scope-note-r15": lambda p: m_shonen(
        p, B4, "and .ufo/waves/round-12/resumed/OverlapHostR.md; corpus/knowledge/source-locator-clarification-r15.md;"),
    "S8-delete-cited-note-double-count": lambda p: os.remove(
        os.path.join(p, "corpus/knowledge/executor-test-sufficiency.md")),
}

V1_FOR = ("S0", "S1", "S2", "S3", "S5", "S8")


def main():
    only = sys.argv[1:]
    os.makedirs(os.path.join(SEAT, "out"), exist_ok=True)
    summary = {}
    for name, fn in MUTANTS.items():
        if only and name.split("-")[0] not in only:
            continue
        path = sandbox(name)
        fn(path)
        commit(path)
        ref = sh("python3", os.path.join(SEAT, "refv2.py"), path, "HEAD")
        rec = {"ref_rc": ref.returncode}
        try:
            rec["ref"] = json.loads(ref.stdout)
        except ValueError:
            rec["ref_err"] = ref.stderr[-2000:]
        if name.split("-")[0] in V1_FOR:
            v1 = sh("python3", V1, "--revision", "HEAD", "--repo", path)
            rec["v1_rc"] = v1.returncode
            try:
                d = json.loads(v1.stdout)
                rec["v1"] = {"mismatches": d["mismatches"],
                             "nonmatch": [(c["id"], c["reason"]) for c in d["checks"] if c["status"] != "match"]}
            except ValueError:
                rec["v1_err"] = (v1.stdout + v1.stderr)[-2000:]
        with open(os.path.join(SEAT, "out", name + ".json"), "w") as f:
            json.dump(rec, f, indent=1, ensure_ascii=False)
        r = rec.get("ref", {})
        line = {"flat": r.get("K01_K06_flat", {}).get("mismatches", r.get("K01_K06_flat", {}).get("exit")),
                "tree": r.get("K01_K06_tree", {}).get("mismatches", r.get("K01_K06_tree", {}).get("exit")),
                "K24_27": r.get("K24_K27_mismatches"),
                "K24_27_bad": [c["id"] for c in r.get("K24_K27", []) if c["status"] != "match"],
                "refs_flat": [(c["id"], c["stated"], c["observed"], c["line"]) for c in
                              r.get("K01_K06_flat", {}).get("checks", [])]}
        if "v1" in rec:
            line["v1"] = [i for i, _ in rec["v1"]["nonmatch"]]
        summary[name] = line
        print(name, json.dumps(line, ensure_ascii=False), flush=True)
        shutil.rmtree(path, ignore_errors=True)
    with open(os.path.join(SEAT, "out", "summary.json"), "w") as f:
        json.dump(summary, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
