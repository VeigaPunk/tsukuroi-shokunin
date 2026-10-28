#!/usr/bin/env python3
"""C1-B8 report-parse edge probe for the frozen round-49 C1 counter.

Baseline = the frozen counter's own K-pass control shape (C1 battery K-pass): synthesized
entry/SKILL/README carrying the three marks, 18 synthetic seat reports in a --wave-dir, a
synthetic w1-results.json, revision = 32a85560 (the dispatch commit the frozen C1 controls
themselves used; entry/SKILL/README/counter blobs are identical to the freeze 55c07cd3).

Each case replaces exactly one report byte-for-byte (R49RevGR1a, row GR1) with the other 17
left valid, so any leg delta is attributable to the parse.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
FREEZE = '55c07cd3f8bff2e12117c34d57b4c618de74d85c'
REV = '32a855608aa3ebb19b0602a94cc33bcfda564a61'
S = '/fast/scratch/hyaku/tsukuroi-r49/R49LabParse'
COUNTER = os.path.join(S, 'check-scrub-admission-r49.py')
R38 = os.path.join(S, 'r38')
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
README_SENT = ('The btrfs scrub grounding entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` is '
               'admitted round 49 for GR1-GR3 by the counted cohort.')
CITE = {'GR1': 'cmdline.c:147', 'GR2': 'dev-replace.c:700', 'GR3': 'scrub.c:3094'}
PAD = (' The reading was checked against the pinned snapshot lines named above and against the errno '
       'ordering the row states; nothing in the row contradicts the bytes that were read, and the host '
       'reading remains marked where the capture does not decide it. This paragraph is padding so the '
       'body clears the counter floor without adding a second citation.')
NAMES = [f'R49{p}GR{r}{x}' for r in '123' for p in ('Rev', 'Crit') for x in 'abc']


def git(*args):
    p = subprocess.run(['git', '-C', LANE, *args], capture_output=True, stdin=subprocess.DEVNULL)
    assert p.returncode == 0, f'git {args} rc={p.returncode} {p.stderr[:200]!r}'
    return p.stdout


def body(seat, row):
    return (f'{seat} read row {row} at the frozen bytes. The clause chain at {CITE[row]} agrees with '
            f'the row, the quoted lines sit where the row cites them, and the host reading keeps its '
            f'inference mark where the capture does not decide it.' + PAD)


def pad_body(seat, row, total, citation):
    """ASCII body of exactly `total` bytes carrying `citation` as its only file:line token."""
    prefix = (f'{seat} read row {row} at the frozen bytes. The clause chain at {citation} agrees with '
              f'the row. ')
    filler = ('the reading keeps its host inference mark where the capture does not decide it and the '
              'clause chain agrees with the row ')
    need = total - len(prefix)
    assert need >= 0, (total, len(prefix))
    out = prefix + (filler * (need // len(filler) + 1))[:need]
    b = out.encode('ascii')
    assert len(b) == total, (len(b), total)
    return out


def cohort(d, hashes, override=None):
    os.makedirs(d, exist_ok=True)
    for seat in NAMES:
        row = re.search(r'GR(\d)', seat).group(0)
        text = (f'ROW {row} VERDICT: holds\nSECTION SHA256: {hashes[row]}\n{body(seat, row)}\n')
        if override and seat in override:
            text = override[seat]
        with open(os.path.join(d, f'{seat}.md'), 'wb') as fh:
            fh.write(text.encode('utf-8'))


def results(path):
    res = {'lane': 'tsukuroi', 'round': 49, 'wave': 'w1', 'seats': len(NAMES), 'results': []}
    for n in NAMES:
        res['results'].append({'name': n, 'agent': 'reviewer' if 'Rev' in n else 'critic',
                               'output': 'ok', 'note': None})
    with open(path, 'w') as fh:
        json.dump(res, fh)


def run(wave_dir, res, tag):
    cmd = ['python3', COUNTER, '--revision', REV, '--lane', LANE, '--no-base-check',
           '--entry-file', os.path.join(R38, 'entry.md'),
           '--skill-file', os.path.join(R38, 'skill.md'),
           '--readme-file', os.path.join(R38, 'readme.md'),
           '--wave-dir', wave_dir, '--results-file', res]
    p = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL, text=True, timeout=600)
    line = (p.stdout or '').strip().split('\n')[-1]
    o = json.loads(line)
    o['_rc'] = p.returncode
    o['_case'] = tag
    return o


def main():
    os.makedirs(R38, exist_ok=True)
    with open(COUNTER, 'wb') as fh:
        fh.write(git('show', f'{FREEZE}:tools/check-scrub-admission-r49.py'))
    csha = hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest()
    entry = git('show', f'{FREEZE}:{ENTRY}').decode()
    skill = git('show', f'{FREEZE}:SKILL.md').decode()
    readme = git('show', f'{FREEZE}:corpus/README.md').decode()
    with open(os.path.join(R38, 'entry.md'), 'w') as fh:
        fh.write(entry + '\n' + MARK_ENTRY + '\n\nadmitted round 49 by the counted cohort.\n')
    with open(os.path.join(R38, 'skill.md'), 'w') as fh:
        fh.write(skill + '\n' + MARK_SKILL + '\n')
    with open(os.path.join(R38, 'readme.md'), 'w') as fh:
        fh.write(readme + '\n' + README_SENT + '\n')
    h = json.loads(subprocess.run(
        ['python3', COUNTER, '--revision', REV, '--lane', LANE, '--no-base-check',
         '--entry-file', os.path.join(R38, 'entry.md'), '--section-hash'],
        capture_output=True, text=True).stdout.strip().split('\n')[-1])['section_sha256']
    res = os.path.join(R38, 'results.json')
    results(res)
    h1 = h['GR1']

    out = {'counter_sha256': csha, 'revision': REV, 'freeze': FREEZE, 'row_hashes': h,
           'refs': {}, 'cases': []}

    def check_ref(tag, want):
        with open(os.path.join(R38, f'{tag}.md'), 'w') as fh:
            fh.write(want)
        out['refs'][tag] = hashlib.sha256(want.encode('utf-8')).hexdigest()

    base = os.path.join(R38, 'wave-base')
    cohort(base, h)
    b = run(base, res, 'baseline')
    out['baseline'] = b
    print('baseline', b['verdict'], {k: b.get(k) for k in
          ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok', 'seats_ok', 'marks_ok')})

    L1 = 'ROW GR1 VERDICT: holds'
    L2 = f'SECTION SHA256: {h1}'
    BD = body('R49RevGR1a', 'GR1')
    seat = 'R49RevGR1a'
    cases = {}

    # (a) CRLF line endings everywhere
    cases['a-crlf'] = (L1 + '\r\n' + L2 + '\r\n' + BD + '\r\n')
    # (b) UTF-8 BOM before ROW
    cases['b-bom'] = ('\ufeff' + L1 + '\n' + L2 + '\n' + BD + '\n')
    # (c) one leading space
    cases['c-lead-space'] = (' ' + L1 + '\n' + L2 + '\n' + BD + '\n')
    # (d) markdown fence around the two lines
    cases['d-fence'] = ('```\n' + L1 + '\n' + L2 + '\n' + BD + '\n```\n')
    # (e) capitalised verdict word
    cases['e-capital'] = ('ROW GR1 VERDICT: Holds\n' + L2 + '\n' + BD + '\n')
    # (f) third line repeats a different verdict
    cases['f-third-line'] = (L1 + '\n' + L2 + '\nROW GR2 VERDICT: fails\n' + BD + '\n')
    # (g) a second SECTION SHA256 line (GR2's real hash) after the bound one
    cases['g-second-hash'] = (L1 + '\n' + L2 + f'\nSECTION SHA256: {h["GR2"]}\n' + BD + '\n')
    # (h) 299-byte body, citation present
    cases['h-body-299'] = (L1 + '\n' + L2 + '\n' + pad_body(seat, 'GR1', 299, 'cmdline.c:147') + '\n')
    # (i) 300-byte body whose only citation is cmdline.c:999999
    cases['i-body-300-bad-cite'] = (L1 + '\n' + L2 + '\n' +
                                    pad_body(seat, 'GR1', 300, 'cmdline.c:999999') + '\n')
    # E1 (extra, cheap): trailing space after the verdict word
    cases['E1-trailing-space'] = (L1 + ' \n' + L2 + '\n' + BD + '\n')
    # E2 (extra, cheap): uppercase hex in the hash line
    cases['E2-uppercase-hash'] = (L1 + f'\nSECTION SHA256: {h1.upper()}\n' + BD + '\n')
    # E3 (extra, cheap): exactly 300-byte body, citation resolves -> boundary inclusivity
    cases['E3-body-300-ok-cite'] = (L1 + '\n' + L2 + '\n' +
                                    pad_body(seat, 'GR1', 300, 'cmdline.c:147') + '\n')
    # E4 (extra): 298-byte body + final newline -> joined body 299 -> expected FAIL (<300)
    cases['E4-body-298'] = (L1 + '\n' + L2 + '\n' + pad_body(seat, 'GR1', 298, 'cmdline.c:147') + '\n')
    # E5 (extra): 299-byte body with NO final newline -> joined body 299 -> expected FAIL
    cases['E5-body-299-nonl'] = (L1 + '\n' + L2 + '\n' + pad_body(seat, 'GR1', 299, 'cmdline.c:147'))
    # E6 (extra): three GR1 seats cite only cmdline.c:999999 -> quorum slack probe
    bad = {}
    for s in ('R49RevGR1a', 'R49RevGR1b', 'R49CritGR1a'):
        bad[s] = (f'ROW GR1 VERDICT: holds\nSECTION SHA256: {h1}\n' +
                  pad_body(s, 'GR1', 300, 'cmdline.c:999999') + '\n')
    cases_by_override = {'E6-badcite-3': bad}
    bad4 = dict(bad)
    bad4['R49CritGR1b'] = (f'ROW GR1 VERDICT: holds\nSECTION SHA256: {h1}\n' +
                           pad_body('R49CritGR1b', 'GR1', 300, 'cmdline.c:999999') + '\n')
    cases_by_override['E7-badcite-4'] = bad4
    # E8 (extra): prose mentions the row's verdict with a word outside the enum -> ANY_VERDICT_RE
    cases['E8-nonenum-word'] = (L1 + '\n' + L2 + '\n' +
                                'The peer wrote ROW GR1 VERDICT: held and the row still agrees. ' + BD + '\n')

    for tag, text in cases.items():
        check_ref(tag, text)
        wd = os.path.join(R38, f'wave-{tag}')
        cohort(wd, h, override={seat: text})
        o = run(wd, res, tag)
        out['cases'].append(o)
        pr = o.get('per_row', {}).get('GR1', {})
        print(tag, o['verdict'], 'rc', o['_rc'],
              'seats', o.get('seats_ok'), 'verdicts', o.get('verdicts_ok'),
              'seat=', pr.get('seats', {}).get(seat),
              'credited', pr.get('credited'), 'blocking', pr.get('blocking'))

    for tag, ov in cases_by_override.items():
        wd = os.path.join(R38, f'wave-{tag}')
        cohort(wd, h, override=ov)
        o = run(wd, res, tag)
        out['cases'].append(o)
        pr = o.get('per_row', {}).get('GR1', {})
        print(tag, o['verdict'], 'rc', o['_rc'],
              'seats', o.get('seats_ok'), 'verdicts', o.get('verdicts_ok'),
              'credited', pr.get('credited'), 'notes', o.get('seat_notes'))

    with open(os.path.join(S, 'probe-out.json'), 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print('COUNTER_SHA256', csha)


if __name__ == '__main__':
    main()
