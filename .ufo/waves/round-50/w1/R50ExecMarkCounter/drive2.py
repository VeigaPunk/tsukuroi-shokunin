#!/usr/bin/env python3
"""Extra marks-leg probes: retained pending mark, contradicting entry prose, split README mark."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import drive as D

S = D.S
hashes = D.section_hashes()
skill0 = D.git_show('SKILL.md')
readme0 = D.git_show('corpus/README.md')
base_skill = skill0 + f'\n{D.MARK_SKILL}\n\nAdmitted round 50.\n'
base_readme = readme0 + ('\nThe entry `btrfs-scrub-grounding-r45.md` is admitted round 50 on its '
                         're-read bytes.\n')
recs = []


def case(name, entry_extra, readme=base_readme):
    recs.append(D.run_case(name, entry_extra, base_skill, readme, os.path.join(S, name), hashes))


# z2: admitted heading + contradicting prose in the same entry (the pending mark is retained in the
# freeze bytes anyway; this adds an explicit negation sentence after the heading).
case('z2-entry-contradiction',
     f'\n{D.MARK_ENTRY}\n\nGR1-GR3 are not admitted round 50; the mark above is premature.\n')
# z3: admitted heading, and the freeze's own pending gate heading left in place (production order).
case('z3-pending-heading-retained',
     f'\n{D.MARK_ENTRY}\n\nThe earlier round-50 heading still records pending.\n')
# z4: README mark split across two sentences (name in one, phrase in the next).
case('z4-readme-split-sentences',
     entry_extra=f'\n{D.MARK_ENTRY}\n\nok.\n',
     readme=readme0 + ('\nThe entry `btrfs-scrub-grounding-r45.md` was re-read this round. '
                       'Its three rows are admitted round 50.\n'))

with open(os.path.join(D.R, 'marks-cases.jsonl'), 'a', encoding='utf-8') as fh:
    for r in recs:
        fh.write(json.dumps(r, sort_keys=True) + '\n')
for r in recs:
    print(f"{r['case']:26s} {str(r['verdict']):5s} marks={r['marks']} marks_ok={r['marks_ok']}")
