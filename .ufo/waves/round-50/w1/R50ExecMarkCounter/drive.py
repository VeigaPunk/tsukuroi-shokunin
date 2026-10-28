#!/usr/bin/env python3
"""R50ExecMarkCounter — exercise the C1 counter's marks leg (item C1-B13).

Freeze bytes + synthetic 18-seat cohort; only the marks fixtures vary, so
structural_ok/corr_ok/quotes_ok/verdicts_ok/seats_ok stay fixed and `marks` is the isolated variable.
"""
import json
import os
import re
import shutil
import subprocess
import sys

L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
FREEZE = '8029cdba1049df25632c91a23c8db4eefb54be5f'
C1 = f'{L}/tools/check-scrub-admission-r50.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
S = '/fast/scratch/hyaku/tsukuroi-r50/R50ExecMarkCounter'
R = f'{L}/.ufo/waves/round-50/w1/R50ExecMarkCounter'
MARK_ENTRY = '## Gate status — round 50 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 50 admission'
CITE = {'GR1': ('cmdline.c:147', 'kstrtox.c:1'),
        'GR2': ('dev-replace.c:1111', 'scrub.c:3094'),
        'GR3': ('systemd.kill.xml:1', 'btrfs-scrub@.service:1')}
ROLES = {r: tuple(f'R50{x}GR{r[2:]}{y}' for x in ('Rev', 'Crit') for y in 'abc')
         for r in ('GR1', 'GR2', 'GR3')}


def git_show(path):
    p = subprocess.run(['git', '-C', L, 'show', f'{FREEZE}:{path}'], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f'cannot read {path} at {FREEZE}')
    return p.stdout.decode('utf-8', errors='replace')


def section_hashes():
    p = subprocess.run([sys.executable, C1, '--revision', FREEZE, '--section-hash'],
                       capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256']


def build_cohort(d, hashes):
    wave = os.path.join(d, 'wave')
    os.makedirs(wave, exist_ok=True)
    tasks, results = [], []
    for row, seats in ROLES.items():
        for seat in seats:
            role = 'reviewer' if 'Rev' in seat else 'critic'
            c1, c2 = CITE[row]
            body = (f'Clause check for {row} by {seat}: the cited lines {c1} and {c2} decide the '
                    f'statement, and the row reads the pinned bytes at the cited numbers. '
                    f'This body is distinct for {seat}. ' + 'Evidence sentence. ' * 12)
            with open(os.path.join(wave, f'{seat}.md'), 'w', encoding='utf-8') as fh:
                fh.write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {hashes[row]}\n{body}\n')
            tasks.append({'name': seat, 'agent': role})
            results.append({'name': seat, 'agent': role, 'output': 'done'})
    with open(os.path.join(d, 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'results': results}, fh)
    with open(os.path.join(d, 'dispatch.json'), 'w', encoding='utf-8') as fh:
        json.dump({'taskCall': {'context': 'fixture', 'tasks': tasks}}, fh)
    return wave


def run_case(name, entry_extra, skill_text, readme_sentence, d, hashes):
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes)
    entry = git_show(ENTRY) + entry_extra
    paths = {}
    for fn, text in (('entry.md', entry), ('skill.md', skill_text), ('readme.md', readme_sentence)):
        paths[fn] = os.path.join(d, fn)
        with open(paths[fn], 'w', encoding='utf-8') as fh:
            fh.write(text)
    cmd = [sys.executable, C1, '--revision', FREEZE,
           '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
           '--readme-file', paths['readme.md'], '--dispatch-file', os.path.join(d, 'dispatch.json'),
           '--results-file', os.path.join(d, 'results.json'), '--wave-dir', wave]
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        obj = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        obj = {'error': (p.stdout + p.stderr)[-600:], 'verdict': 'ERROR'}
    legs = {k: obj.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok',
                                    'seats_ok', 'marks_ok')}
    rec = {'case': name, 'verdict': obj.get('verdict'), 'rc': p.returncode, 'legs': legs,
           'marks': obj.get('marks'), 'marks_ok': obj.get('marks_ok')}
    with open(os.path.join(R, f'{name}.json'), 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
    return rec


def main():
    hashes = section_hashes()
    entry0 = git_show(ENTRY)
    skill0 = git_show('SKILL.md')
    readme0 = git_show('corpus/README.md')

    # --- baseline: production-shaped fixtures, all three marks present, valid cohort
    base_entry_extra = f'\n{MARK_ENTRY}\n\nAdmitted on the round-50 re-read bytes.\n'
    base_skill = skill0 + f'\n{MARK_SKILL}\n\nAdmitted round 50.\n'
    base_readme = readme0 + ('\nThe entry `btrfs-scrub-grounding-r45.md` is admitted round 50 on its '
                             're-read bytes.\n')
    recs = []

    def case(name, entry_extra=base_entry_extra, skill_text=base_skill, readme=base_readme):
        recs.append(run_case(name, entry_extra, skill_text, readme, os.path.join(S, name), hashes))

    case('00-baseline-pass')

    # --- (a) no SKILL mark
    case('a-no-skill-mark', skill_text=skill0 + '\nNothing marked here.\n')
    # --- (b) SKILL mark as a substring of a longer line
    case('b-skill-substring',
         skill_text=skill0 + f'\nThe ledger line `{MARK_SKILL}` is quoted here, not used as a heading.\n')
    # --- (c) README sentence negated four ways (each sentence carries name + phrase)
    neg = {
        'c1-not-admitted': 'The entry `btrfs-scrub-grounding-r45.md` is not admitted round 50.',
        'c2-remains-unadmitted': 'The entry `btrfs-scrub-grounding-r45.md` remains unadmitted round 50.',
        'c3-never-admitted': 'The entry `btrfs-scrub-grounding-r45.md` is never admitted round 50.',
        'c4-gr-unadmitted': '`btrfs-scrub-grounding-r45.md`: GR1-GR3 are unadmitted round 50.',
    }
    for nm, sentence in neg.items():
        case(nm, readme=readme0 + '\n' + sentence + '\n')
    # --- (d) entry heading present twice
    case('d-entry-heading-twice',
         entry_extra=f'\n{MARK_ENTRY}\n\nfirst.\n\n{MARK_ENTRY}\n\nsecond.\n')
    # --- (e) entry heading present ONLY inside a fenced code block
    case('e-entry-heading-in-fence',
         entry_extra=f'\n```\n{MARK_ENTRY}\n```\n')

    # --- extras: hostile negation shapes the regex may not cover
    extra = {
        'x1-no-longer': 'The entry `btrfs-scrub-grounding-r45.md` is no longer admitted round 50.',
        'x2-not-currently': 'The entry `btrfs-scrub-grounding-r45.md` is not currently admitted round 50.',
        'x3-isnt': "The entry `btrfs-scrub-grounding-r45.md` isn't admitted round 50.",
        'x4-has-not-been': 'The entry `btrfs-scrub-grounding-r45.md` has not been admitted round 50.',
        'x5-not-yet': 'The entry `btrfs-scrub-grounding-r45.md` is not yet admitted round 50.',
        'x6-hyphen-un': 'The entry `btrfs-scrub-grounding-r45.md` is un-admitted round 50.',
        'x7-next-sentence': ('The entry `btrfs-scrub-grounding-r45.md` is admitted round 50. '
                             'GR1-GR3 are unadmitted round 50.'),
        'x8-unrelated-negation': ('The entry `btrfs-scrub-grounding-r45.md` is admitted round 50; the '
                                  'S240 quote is not admitted as a kernel fact.'),
        'x9-withdrawn': ('The entry `btrfs-scrub-grounding-r45.md` was admitted round 50 in error and '
                         'the mark is withdrawn.'),
        'x10-stay-pending': 'The entry `btrfs-scrub-grounding-r45.md` is admitted round 50 but rows stay pending.',
    }
    for nm, sentence in extra.items():
        case(nm, readme=readme0 + '\n' + sentence + '\n')

    # --- extras: entry/skill shape brittleness
    case('y1-entry-trailing-space',
         entry_extra=f'\n{MARK_ENTRY}   \n\ntrailing whitespace.\n')
    case('y2-entry-ascii-dash',
         entry_extra='\n## Gate status - round 50 (GR1-GR3 admitted)\n\nascii hyphen.\n')
    case('y3-skill-trailing-space',
         skill_text=skill0 + f'\n{MARK_SKILL}   \n')
    case('y4-skill-in-fence',
         skill_text=skill0 + f'\n```\n{MARK_SKILL}\n```\n')

    with open(os.path.join(R, 'marks-cases.jsonl'), 'w', encoding='utf-8') as fh:
        for r in recs:
            fh.write(json.dumps(r, sort_keys=True) + '\n')
    for r in recs:
        print(f"{r['case']:26s} {str(r['verdict']):5s} rc={r['rc']} marks={r['marks']} "
              f"marks_ok={r['marks_ok']} other_legs="
              f"{ {k: v for k, v in r['legs'].items() if k != 'marks_ok'} }")


if __name__ == '__main__':
    main()
