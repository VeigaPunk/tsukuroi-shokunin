#!/usr/bin/env python3
"""Mutation harness for K07-K11 and K13 of tools/check-self-assessment.py.

Runs the detector on pristine bytes, on each mutant, and on restored bytes.
Every mutation happens inside the scratch sandbox repository only.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1Counts"
SANDBOX = os.path.join(ROOT, "sandbox")
OUT = os.path.join(ROOT, "results")
BASE_COMMIT = None


def git(*args, **kw):
    return subprocess.run(["git", "-C", SANDBOX] + list(args),
                          capture_output=True, text=True,
                          env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null",
                               "GIT_CONFIG_SYSTEM": "/dev/null"}, **kw)


def sh(*args):
    return git(*args).stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_manifest():
    """sha256 of every tracked file, plus a manifest digest."""
    files = sh("ls-files", "-z").split("\0")
    entries = {}
    for rel in files:
        if not rel:
            continue
        p = os.path.join(SANDBOX, rel)
        if os.path.isfile(p):
            entries[rel] = sha256(p)
    digest = hashlib.sha256()
    for rel in sorted(entries):
        digest.update(rel.encode() + b"\0" + entries[rel].encode() + b"\n")
    return entries, digest.hexdigest()


def reset_pristine():
    git("reset", "--hard", BASE_COMMIT)
    git("clean", "-fdq")


def commit_all(message):
    git("add", "-A")
    git("-c", "user.name=mutant", "-c", "user.email=mutant@example.invalid",
        "commit", "-q", "--allow-empty", "-m", message)


def run_detector(label):
    proc = subprocess.run([sys.executable, "tools/check-self-assessment.py", "--revision", "HEAD"],
                          cwd=SANDBOX, capture_output=True, text=True, timeout=1800)
    try:
        payload = json.loads(proc.stdout)
    except Exception:
        payload = {"parse_error": proc.stdout[:2000], "stderr": proc.stderr[:2000]}
    bad = [c["id"] for c in payload.get("checks", []) if c.get("status") != "match"]
    return {
        "label": label,
        "exit": proc.returncode,
        "status": payload.get("status"),
        "mismatches": payload.get("mismatches"),
        "checked": payload.get("checked"),
        "failing_checks": bad,
        "details": {c["id"]: {"stated": c.get("stated"), "observed": c.get("observed"),
                              "reason": c.get("reason")}
                    for c in payload.get("checks", []) if c.get("status") != "match"},
        "stdout_head": proc.stdout[:400],
        "stderr_tail": proc.stderr[-400:],
    }


# ---------------------------------------------------------------- mutations

def m_k07_note_add():
    """K07 observed side: one new knowledge note."""
    p = os.path.join(SANDBOX, "corpus/knowledge/mutant-k07-note.md")
    with open(p, "w") as fh:
        fh.write("# Mutant note (K07)\n\nA temporary note added by the mutation harness.\n")
    return ["corpus/knowledge/mutant-k07-note.md"]


def m_k08_skill_line_add():
    """K08 observed side: one extra plain (non-pipe) SKILL.md line."""
    p = os.path.join(SANDBOX, "SKILL.md")
    with open(p, "a") as fh:
        fh.write("\nMutant line added by the K08 mutation harness.\n")
    return ["SKILL.md"]


def m_k09_pipe_line_add():
    """K09 observed side: one extra pipe-prefixed SKILL.md line."""
    p = os.path.join(SANDBOX, "SKILL.md")
    with open(p, "a") as fh:
        fh.write("\n| mutant | harness | K09 pipe line |\n")
    return ["SKILL.md"]


def m_k09_pipe_line_add_comp():
    """K09 isolated: one pipe line plus a compensating stated SKILL.md line count."""
    p = os.path.join(SANDBOX, "SKILL.md")
    with open(p, "a") as fh:
        fh.write("\n| mutant | harness | K09 pipe line |\n")
    sc = os.path.join(SANDBOX, "SCORECARD.md")
    text = open(sc).read()
    new = text.replace("`SKILL.md` 2355 `wc -l`", "`SKILL.md` 2356 `wc -l`", 1)
    assert new != text, "K09 compensation: stated SKILL.md line count not found"
    with open(sc, "w") as fh:
        fh.write(new)
    return ["SKILL.md", "SCORECARD.md"]


def m_k10_lesson_add():
    """K10 observed side: one new lesson file."""
    p = os.path.join(SANDBOX, "corpus/lessons/mutant-k10-lesson.md")
    with open(p, "w") as fh:
        fh.write("# Mutant lesson (K10)\n\nA temporary lesson file.\n")
    return ["corpus/lessons/mutant-k10-lesson.md"]


def m_k11_stated_count():
    """K11 stated side: coverage row README line count changed by one."""
    sc = os.path.join(SANDBOX, "SCORECARD.md")
    text = open(sc).read()
    new = text.replace("`corpus/README.md` 231 `wc -l`", "`corpus/README.md` 232 `wc -l`", 1)
    assert new != text, "K11 stated count not found"
    with open(sc, "w") as fh:
        fh.write(new)
    return ["SCORECARD.md"]


def m_k11_readme_line_add():
    """K11 observed side: one extra line in corpus/README.md."""
    p = os.path.join(SANDBOX, "corpus/README.md")
    with open(p, "a") as fh:
        fh.write("\nMutant line added by the K11 mutation harness.\n")
    return ["corpus/README.md"]


def m_k07_notes_phrase_removed():
    """K07 stated side: the word 'notes' removed from the depth row."""
    sc = os.path.join(SANDBOX, "SCORECARD.md")
    text = open(sc).read()
    new = text.replace("47 notes (`ls corpus/knowledge/*.md", "47 (`ls corpus/knowledge/*.md", 1)
    assert new != text, "K07 'notes' phrase not found"
    with open(sc, "w") as fh:
        fh.write(new)
    return ["SCORECARD.md"]


def m_k13_cases_96():
    """K13 stated side: '97 cases' -> '96 cases' in the operability row."""
    sc = os.path.join(SANDBOX, "SCORECARD.md")
    text = open(sc).read()
    old = "prints PASS (97 cases, 97 passed, 0 failed) with exit 0"
    new = "prints PASS (96 cases, 97 passed, 0 failed) with exit 0"
    assert old in text, "K13 operability row text not found"
    text = text.replace(old, new, 1)
    with open(sc, "w") as fh:
        fh.write(text)
    return ["SCORECARD.md"]


MUTANTS = [
    ("M1-k07-note-added", m_k07_note_add,
     "Add one file corpus/knowledge/mutant-k07-note.md (K07 observed side)."),
    ("M2-k08-skill-line-added", m_k08_skill_line_add,
     "Append one plain line to SKILL.md (K08 observed side)."),
    ("M3-k09-pipe-line-added", m_k09_pipe_line_add,
     "Append one pipe-prefixed line to SKILL.md (K09 observed side; also moves K08)."),
    ("M3b-k09-pipe-line-added-compensated", m_k09_pipe_line_add_comp,
     "Append one pipe-prefixed line to SKILL.md and bump the stated SKILL.md line count to 2356, isolating K09."),
    ("M4-k10-lesson-added", m_k10_lesson_add,
     "Add one file corpus/lessons/mutant-k10-lesson.md (K10 observed side)."),
    ("M5-k11-stated-count-231-to-232", m_k11_stated_count,
     "Change the coverage row stated corpus/README.md count from 231 to 232 (K11 stated side)."),
    ("M5b-k11-readme-line-added", m_k11_readme_line_add,
     "Append one line to corpus/README.md (K11 observed side)."),
    ("M6-k07-notes-phrase-removed", m_k07_notes_phrase_removed,
     "Remove the word 'notes' from the depth row's '47 notes' phrase (K07 stated side)."),
    ("M7-k13-97-cases-to-96", m_k13_cases_96,
     "Change the operability row '97 cases' to '96 cases' (K13 stated side)."),
]


def main():
    global BASE_COMMIT
    os.makedirs(OUT, exist_ok=True)
    global BASE_COMMIT
    BASE_COMMIT = sh("rev-parse", "HEAD").strip()
    reset_pristine()
    pristine_entries, pristine_digest = tree_manifest()

    report = {"sandbox": SANDBOX, "base_commit": BASE_COMMIT,
              "pristine_tree_digest": pristine_digest, "runs": []}

    report["runs"].append(run_detector("pristine"))

    for name, fn, desc in MUTANTS:
        reset_pristine()
        touched = fn()
        commit_all(name)
        run = run_detector(name)
        run["description"] = desc
        run["touched"] = touched
        run["mutant_tree_digest"] = tree_manifest()[1]
        # restore
        reset_pristine()
        after_entries, after_digest = tree_manifest()
        run["restored_tree_digest"] = after_digest
        run["restored_matches_pristine"] = (after_digest == pristine_digest)
        report["runs"].append(run)
        print(name, "exit", run["exit"], "mismatches", run["mismatches"],
              "failing", run["failing_checks"], "restored", run["restored_matches_pristine"],
              flush=True)

    reset_pristine()
    with open(os.path.join(OUT, "report.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print("done")


if __name__ == "__main__":
    main()
