#!/usr/bin/env python3
"""Variants C/D: does the drafted table bind with the lesson landed, and does a same-round depth uplift bind?"""
import os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"

def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def clone(D):
    subprocess.run(["git", "-C", LANE, "clone", "-q", "--shared", LANE, D], check=True)
    run("git", "-C", D, "remote", "remove", "origin")
    top = run("git", "-C", D, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    run("git", "-C", D, "-c", "advice.detachedHead=false", "checkout", "-q",
        "18389f44cf6ce414d7be205998b29c79fb0b490c")

def table(depth_score, lessons):
    return """## Axes — current self-assessment (round 45 final measured surface)

Each count is re-derived from the committed lane tree at the round-45 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | {d} | 66 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 4230 `wc -l` / 1156 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` {l} files (`find corpus/lessons -type f | wc -l`); round-45 C2 verifies GR1-GR3 (three counted rows bound); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 452 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record's unprivileged view is Core since round 44 (SCRUB line; content and running state stay Frontier). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (154 cases, 154 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-45 C1 verified (the five first-line readers take the first line by parameter expansion); `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 45 re-fetched S246-S249 and re-ran the S249 host capture; round 43 re-fetched S237 and S240 byte-identical. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 at the round-45 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; round 45 repins IN-109 `found_line` 2468 -> 2582 with the declaration and restates the round-42 tameshi and mori handoffs; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
""".format(d=depth_score, l=lessons)

def land(D, depth_score, lessons_in_table, lesson_files, extra_section=""):
    sc = open(os.path.join(D, "SCORECARD.md"), encoding="utf-8").read().split("\n")
    start = next(i for i, l in enumerate(sc) if l.startswith("## Axes — current self-assessment (round 44"))
    end = next(i for i in range(start + 1, len(sc)) if sc[i].startswith("## "))
    sc[start:end] = table(depth_score, lessons_in_table).rstrip("\n").split("\n") + [""]
    text = "\n".join(sc)
    text = text.replace("selftest prints PASS (148 cases, 148 passed, 0 failed)",
                        "selftest prints PASS (154 cases, 154 passed, 0 failed)")
    if extra_section:
        text = text.rstrip("\n") + "\n\n" + extra_section.strip("\n") + "\n"
    open(os.path.join(D, "SCORECARD.md"), "w", encoding="utf-8").write(text)
    for name in lesson_files:
        path = os.path.join(D, "corpus", "lessons", name)
        open(path, "w", encoding="utf-8").write("fixture lesson placeholder\n")
        run("git", "-C", D, "add", "corpus/lessons/" + name)
    run("git", "-C", D, "add", "SCORECARD.md")
    p = run("git", "-C", D, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", "fixture variant")
    assert p.returncode == 0, p.stderr
    return run("git", "-C", D, "rev-parse", "HEAD").stdout.strip()

S = os.path.dirname(os.path.abspath(__file__))
which = sys.argv[1]
D = sys.argv[2]
if which == "D":
    clone(D)
    sha = land(D, 8, 66, ["round-45.md"])
else:
    clone(D)
    sha = land(D, 9, 66, ["round-45.md"],
               extra_section="## Round 45 — measured outcome (fixture)\n\n| Claim | Axis | Ordinal |\n|---|---|---|\n| C2 | depth8→9 (1) | +1 |\n")
print(sha)
