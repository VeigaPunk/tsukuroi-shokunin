#!/usr/bin/env python3
"""R49RevMarks mark-wording fixture driver: builds mark fixtures and runs the frozen
C1 counter's marks_leg through --entry-file/--skill-file/--readme-file.

Scratch only. Writes nothing outside /fast/scratch/hyaku/tsukuroi-r49/R49RevMarks.
"""
import json
import os
import re
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '55c07cd3f8bff2e12117c34d57b4c618de74d85c'

E1_PENDING = '## Gate status — round 49 (pending; the frozen cohort has not settled)'
E2_ADMITTED = '## Gate status — round 49 (GR1-GR3 admitted)'
E2B_BODY = (
    "After the freeze the `w1` cohort settled with `verdicts_ok 3` and `seats_ok 18` — all 18 bound "
    "seats read `holds`, at least three credited per row on the frozen row hashes with pairwise "
    "distinct bodies, and `corr_ok 1` — and that is all `admitted` records here: the round-48 counted "
    "seats read GR1 and GR2 "
    "`partly` (CritGR1a; CritGR2a and RevGR2a) and GR3 `holds`, and the seven defects they named (the "
    "`0X` case, the unmarked host-mode inference, the `is_valid` gate, the cancel sentence's subject, the "
    "suspend-path range that ran three lines past its function and its effects, the ioctl citation at "
    "`ioctl.c:3132`, and the `-ENODEV` devid case) stay named above as the reason the rows were not "
    "admitted then; the seat verdicts are this lane's own records, committed bytes cannot tell a forged "
    "orchestrator record from a real one (standing limit K3), and the Limits block is unchanged."
)
S1_HEAD = '## Scrub grounding — round 49 admission'
S1_BODY = (
    "GR1-GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` are admitted by 18 bound seat verdicts of "
    "wave `w1` reading `holds` on the frozen row hashes (`tools/check-scrub-admission-r49.py`); the "
    "round-48 negatives, the Limits and the standing limit on forged records carry over from the round-45 "
    "section above."
)
R1 = ("`knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 are admitted round 49 on the wave `w1` "
      "cohort's 18 bound seat verdicts, all `holds`, at least three credited per row on the frozen "
      "row hashes, and not on outside review or any host observation.")
R2 = ("The round-48 counted seats read GR1 and GR2 `partly` and named seven defects that the freeze "
      "corrected, and the row Limits (no sysfs write, no stop trace) stand.")

PENDING_SENT = (
    "This heading records **pending**, not admission: it says\n"
    "`admitted` only after the cohort settles `holds` on the current row bytes, and the round-48 findings\n"
    "are retained above as the reason the rows were not admitted then."
)


def read(name):
    with open(os.path.join(S, name), encoding='utf-8') as fh:
        return fh.read()


def put(name, text):
    p = os.path.join(S, name)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return p


def main():
    entry0 = read('entry_freeze.md')
    skill0 = read('skill_freeze.md')
    readme0 = read('readme_freeze.md')
    assert entry0.count(E1_PENDING + '\n') == 1, 'frozen pending heading not unique'
    assert entry0.count(PENDING_SENT) == 1, 'frozen pending sentence not unique'

    entry_adm = entry0.replace(E1_PENDING + '\n', E2_ADMITTED + '\n').replace(PENDING_SENT, E2B_BODY)
    skill_adm = skill0.rstrip('\n') + '\n\n' + S1_HEAD + '\n\n' + S1_BODY + '\n'
    readme_ok = readme0.rstrip('\n') + (
        '\n\n## Round-49 coverage note (appended 2026-10-28)\n\n'
        'Append-only; the coverage map, the Frontier bullets and the notes above stay as written.\n\n'
        + R1 + '\n' + R2 + '\n')

    variants = {}
    variants['V1_admitted_note'] = (entry_adm, skill_adm, readme_ok)
    # V2: the positive sentence and a negating clause in ONE sentence (semicolon, no break).
    variants['V2_negate_same_sentence'] = (entry_adm, skill_adm, readme0.rstrip('\n') + (
        '\n\n## Round-49 coverage note\n\n' + R1.rstrip('.') +
        '; the GR1-GR3 rows stay pending until an outside reader checks them.\n'))
    # V3: the sentence placed inside a table cell whose row also carries a negation.
    variants['V3_negate_same_table_row'] = (entry_adm, skill_adm, readme0.rstrip('\n') + (
        '\n\n| Note | Holds |\n|---|---|\n| coverage | ' + R1.rstrip('.') +
        '; rounds 45-48 were unadmitted |\n'))
    # V4: negation only in a NEIGHBOUR sentence, separated by a sentence break (should pass).
    variants['V4_negate_neighbour_sentence'] = (entry_adm, skill_adm, readme0.rstrip('\n') + (
        '\n\n## Round-49 coverage note\n\n' + R1 + ' The rows were unadmitted in rounds 45-48 and stay '
        'pending for the round-48 GR2 defect.\n'))
    # V5: SKILL heading carries trailing spaces only (marks_leg strips).
    variants['V5_skill_trailing_spaces'] = (
        entry_adm, skill0.rstrip('\n') + '\n\n' + S1_HEAD + '  \n\n' + S1_BODY + '\n', readme_ok)
    # V6: SKILL heading written one level deeper.
    variants['V6_skill_deeper_heading'] = (
        entry_adm, skill0.rstrip('\n') + '\n\n### ' + S1_HEAD[3:] + '\n\n' + S1_BODY + '\n', readme_ok)
    # V7: entry heading with one trailing space.
    variants['V7_entry_trailing_space'] = (
        entry_adm.replace(E2_ADMITTED + '\n', E2_ADMITTED + ' \n'), skill_adm, readme_ok)
    # V8: pending entry (frozen bytes) with the admitted SKILL/README marks: must NOT score 3.
    variants['V8_pending_entry'] = (entry0, skill_adm, readme_ok)
    # V9: README mark absent (control) — name without the phrase.
    variants['V9_readme_no_phrase'] = (entry_adm, skill_adm, readme0.rstrip('\n') + (
        '\n\n## Round-49 coverage note\n\n`knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3 were read by a '
        'fresh cohort and the round-48 defects were corrected.\n'))
    # V10: body sentence that names the round-48 defect verbatim (CORR_FORBID) — expected corr_ok 0.
    bad_body = E2B_BODY.replace('the suspend-path range that ran three lines past its function and its effects',
                                'the suspend-path range dev-replace.c:1171-1199 and that it only sets the state to SUSPENDED')
    variants['V10_body_reintroduces_forbidden'] = (
        entry_adm.replace(E2B_BODY, bad_body), skill_adm, readme_ok)

    out = {}
    for name, (e, sk, rd) in variants.items():
        ep, sp, rp = put('v_' + name + '.entry.md', e), put('v_' + name + '.skill.md', sk), put('v_' + name + '.readme.md', rd)
        p = subprocess.run(['python3', os.path.join(S, 'counter.py'), '--revision', REV,
                            '--lane', LANE, '--no-base-check', '--entry-file', ep,
                            '--skill-file', sp, '--readme-file', rp],
                           capture_output=True, text=True, cwd=S)
        try:
            obj = json.loads(p.stdout)
        except Exception:
            out[name] = {'rc': p.returncode, 'stdout_head': p.stdout[:300], 'stderr': p.stderr[:300]}
            continue
        out[name] = {'rc': p.returncode, 'marks': obj.get('marks'), 'marks_ok': obj.get('marks_ok'),
                     'corr_ok': obj.get('corr_ok'), 'structural_ok': obj.get('structural_ok'),
                     'quotes_ok': obj.get('quotes_ok'), 'verdicts_ok': obj.get('verdicts_ok'),
                     'seats_ok': obj.get('seats_ok'), 'verdict': obj.get('verdict'),
                     'corr_forbidden_present': obj.get('corr_forbidden_present'),
                     'corr_missing': obj.get('corr_missing'), 'error': obj.get('error')}
    # Which sentence does the counter's splitter present for the README?
    norm = ' '.join(readme_ok.split())
    hits = [s for s in re.split(r'(?<=[.!?])\s+', norm) if 'btrfs-scrub-grounding-r45.md' in s]
    print(json.dumps({'variants': out,
                      'readme_sentences_naming_entry': hits,
                      'mark_strings': {'entry': E2_ADMITTED, 'skill': S1_HEAD, 'readme': R1}},
                     indent=1, sort_keys=True))


if __name__ == '__main__':
    sys.exit(main())
