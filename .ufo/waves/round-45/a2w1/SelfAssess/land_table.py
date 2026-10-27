#!/usr/bin/env python3
"""Land a drafted round-45 axes table in a scratch clone at 18389f44 and score it."""
import os, subprocess, sys, json

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
D = sys.argv[1]
LESSONS = sys.argv[2]   # lesson count to state (65 measured; 66 after round-45.md lands)
SKILL = sys.argv[3]     # SKILL.md wc -l to state
TABLE = sys.argv[4]     # table line count to state
README = sys.argv[5]    # corpus/README.md wc -l to state

AXES = """## Axes — current self-assessment (round 45 final measured surface)

Each count is re-derived from the committed lane tree at the round-45 outcome commit (the commit that lands this table); ordinals unchanged.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | {lessons_n} notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` {skill} `wc -l` / {table} table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` {lessons} files (`find corpus/lessons -type f | wc -l`); round-45 C2 verifies GR1-GR3 (three counted rows bound); no ordinal move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` {readme} `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes plus the verdict-neutral STORAGE line; the scrub record's unprivileged view is Core since round 44 (SCRUB line; content and running state stay Frontier). | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (154 cases, 154 passed, 0 failed); `bash tools/boot-chain-audit.sh --selftest` prints `PASS total=49 failed=0`; round-45 C1 verified (the five first-line readers take the first line by parameter expansion); `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; round 45 re-fetched S246-S249 and re-ran the S249 host capture; round 43 re-fetched S237 and S240 byte-identical (`w1/C2ExecLiveSources.md`, `w2/SrcReopenS237.md`, `w2/SrcReopenS240.md`). | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; mismatches 0 at the round-45 outcome commit. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; round 45 repins IN-109 `found_line` 2468 -> 2582 with the declaration and restates the round-42 tameshi and mori handoffs; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
""".format(lessons_n=66, skill=SKILL, table=TABLE, lessons=LESSONS, readme=README)

def run(*cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

subprocess.run(["git", "-C", LANE, "clone", "-q", "--shared", LANE, D], check=True)
run("git", "-C", D, "remote", "remove", "origin")
top = run("git", "-C", D, "rev-parse", "--show-toplevel").stdout.strip()
assert os.path.realpath(top) == os.path.realpath(D), (top, D)
run("git", "-C", D, "-c", "advice.detachedHead=false", "checkout", "-q",
    "18389f44cf6ce414d7be205998b29c79fb0b490c")

sc = open(os.path.join(D, "SCORECARD.md"), encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(sc) if l.startswith("## Axes — current self-assessment (round 44"))
end = next(i for i in range(start + 1, len(sc)) if sc[i].startswith("## "))
sc[start:end] = AXES.rstrip("\n").split("\n") + [""]
text = "\n".join(sc)
open(os.path.join(D, "SCORECARD.md"), "w", encoding="utf-8").write(text)

# capabilities row: host-census-gate states the census case count
cap = open(os.path.join(D, "SCORECARD.md"), encoding="utf-8").read()
assert "selftest prints PASS (148 cases, 148 passed, 0 failed)" in cap
cap = cap.replace("selftest prints PASS (148 cases, 148 passed, 0 failed)",
                  "selftest prints PASS (154 cases, 154 passed, 0 failed)")
open(os.path.join(D, "SCORECARD.md"), "w", encoding="utf-8").write(cap)

run("git", "-C", D, "add", "SCORECARD.md")
p = run("git", "-C", D, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "-m", "fixture: round-45 axes table draft (lessons=%s skill=%s table=%s readme=%s)"
        % (LESSONS, SKILL, TABLE, README))
print(p.stdout or p.stderr)
print(run("git", "-C", D, "rev-parse", "HEAD").stdout.strip())
