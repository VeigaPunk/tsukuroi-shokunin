#!/usr/bin/env python3
"""Refined isolation mutant: pipe line added to SKILL.md with the stated
SKILL.md line count compensated by the exact number of added lines, so that
only K09 (table-line count) should be affected."""
import json
import os
import subprocess
import sys

sys.path.insert(0, "/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1Counts")
import harness as H

def main():
    H.BASE_COMMIT = H.sh("rev-parse", "HEAD").strip()
    H.reset_pristine()
    pristine = H.tree_manifest()[1]

    skill = os.path.join(H.SANDBOX, "SKILL.md")
    before = open(skill).read()
    added = "\n| mutant | harness | K09 pipe line |\n"
    with open(skill, "a") as fh:
        fh.write(added)
    delta = open(skill).read().count("\n") - before.count("\n")
    sc = os.path.join(H.SANDBOX, "SCORECARD.md")
    text = open(sc).read()
    new = text.replace("`SKILL.md` 2355 `wc -l`", "`SKILL.md` %d `wc -l`" % (2355 + delta), 1)
    assert new != text
    open(sc, "w").write(new)
    H.commit_all("M3c-k09-pipe-line-isolated")
    run = H.run_detector("M3c-k09-pipe-line-added-isolated")
    run["description"] = ("Append one pipe-prefixed line to SKILL.md and compensate the stated "
                           "`SKILL.md` N `wc -l` count by the exact added line count (%d), isolating K09." % delta)
    run["added_lines"] = delta
    H.reset_pristine()
    run["restored_matches_pristine"] = (H.tree_manifest()[1] == pristine)
    print(json.dumps(run, indent=1))
    H.reset_pristine()

main()
