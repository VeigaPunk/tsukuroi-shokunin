#!/usr/bin/env python3
"""R50LabParse reproducer: C1 report-parser edge cases against the frozen C1 counter.

Builds, under a scratch dir, a fixture wave dir of 18 synthetic seat reports (all valid),
a fixture dispatch and results file, and entry/SKILL/README overrides carrying the round-50
marks, so that ONLY the report-parsing legs of tools/check-scrub-admission-r50.py can vary.
Each case mutates exactly one report (R50RevGR1a) unless the case name says otherwise, then
runs the frozen counter and prints one JSON line per case.

Run:  python3 repro.py [SCRATCH_DIR]
Needs: git read access to the lane repo; writes nothing outside SCRATCH_DIR.
"""
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
S = sys.argv[1] if len(sys.argv) > 1 else '/fast/scratch/hyaku/tsukuroi-r50/R50LabParse/repro'
COUNTER = os.path.join(S, 'counter.py')
FX = os.path.join(S, 'fx')

MARK_ENTRY = '## Gate status — round 50 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 50 admission'
HASH = {'GR1': '3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
        'GR2': 'a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f',
        'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
CITES = {'GR1': '`cmdline.c:147` and `vsprintf.c:86` and `kstrtox.c:29` and `sysfs.c:2040`',
         'GR2': '`dev-replace.c:700` and `scrub.c:3081` and `sysfs.c:2040` and `ioctl.c:3132`',
         'GR3': '`systemd.kill.xml:5` and `btrfs-scrub@.service:5` and `scrub.c:3094` and `capture.txt:5`'}


def show(path):
    return subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{path}'],
                          capture_output=True, check=True).stdout


def seats(row):
    n = row[2:]
    return ([(f'R50RevGR{n}{x}', 'reviewer') for x in 'abc']
            + [(f'R50CritGR{n}{x}', 'critic') for x in 'abc'])


def body(row, seat):
    return (f'Synthetic seat report for {seat} on {row}. The pinned bytes {CITES[row]} settle the '
            f'question this row asks; the quoted lines are read at the cited numbers and agree with '
            f'the row text. This body exists only to exercise the counter parser, marker {seat}.\n')


def report(row, seat):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASH[row]}\n' + body(row, seat)


def sized_body(row, seat, want, cites='`cmdline.c:147` and `vsprintf.c:86`'):
    head = f'ROW {row} holds; {cites}; marker {seat}. '
    b = (head + 'p' * want)[:want]
    assert len(b.encode()) == want
    return b


def mk299(row, seat, _):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASH[row]}\n' + sized_body(row, seat, 299)


def mk300_row(row, seat, _):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASH[row]}\n' + sized_body(row, seat, 300)


def mk300_lane(row, seat, _):
    return (f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASH[row]}\n'
            + sized_body(row, seat, 300, '`entry.md:5` and `SHA256SUMS:1`'))


def _rep(row, l0=None, l1=None, body_text=None, prefix='', suffix='', nl='\n'):
    l0 = l0 or f'ROW {row} VERDICT: holds'
    l1 = l1 or f'SECTION SHA256: {HASH[row]}'
    return prefix + nl.join([l0, l1, body_text if body_text is not None else body(row, 'x')]) + suffix


SINGLE = {
    'a_crlf': lambda r, s, t: _rep(r, body_text=body(r, s), nl='\r\n'),
    'b_bom': lambda r, s, t: _rep(r, body_text=body(r, s), prefix='\ufeff'),
    'c_leadspace': lambda r, s, t: _rep(r, body_text=body(r, s), l0=f' ROW {r} VERDICT: holds'),
    'd_fence': lambda r, s, t: _rep(r, body_text=body(r, s), prefix='```\n', suffix='\n```\n'),
    'e_cap': lambda r, s, t: _rep(r, body_text=body(r, s), l0=f'ROW {r} VERDICT: Holds'),
    'f_thirdline': lambda r, s, t: _rep(r, body_text='ROW GR2 VERDICT: holds\n' + body(r, s)),
    'g_dup_hash': lambda r, s, t: _rep(r, body_text='SECTION SHA256: ' + '0' * 64 + '\n' + body(r, s)),
    'g2_wrong_first': lambda r, s, t: _rep(r, l1='SECTION SHA256: ' + '0' * 64,
                                          body_text=f'SECTION SHA256: {HASH[r]}\n' + body(r, s)),
    'h_299': mk299,
    'i_300_lanecite': mk300_lane,
    'ctl_300_rowcites': mk300_row,
    'j_prose_mention': lambda r, s, t: _rep(r, body_text=body(r, s) + f'We withdrew the earlier draft whose line read ROW {r} VERDICT: fails.\n'),
    'l_trailing_space': lambda r, s, t: _rep(r, body_text=body(r, s), l0=f'ROW {r} VERDICT: holds '),
    'p_prose_same': lambda r, s, t: _rep(r, body_text=body(r, s) + f'The sibling line ROW {r} VERDICT: holds agrees.\n'),
    'q_prose_cap': lambda r, s, t: _rep(r, body_text=body(r, s) + f'An early draft said ROW {r} VERDICT: Holds but it was retitled.\n'),
    'r_prose_partly': lambda r, s, t: _rep(r, body_text=body(r, s) + f'A withdrawn note said ROW {r} VERDICT: partly.\n'),
}
MULTI = {
    'h_299_four': ('R50RevGR1a R50RevGR1b R50CritGR1a R50CritGR1b', mk299),
    'i_300_four': ('R50RevGR1a R50RevGR1b R50CritGR1a R50CritGR1b', mk300_lane),
    'm_drop3_mixed': ('R50RevGR1a R50RevGR1b R50CritGR1a', mk299),
    'n_drop3_same_role': ('R50RevGR1a R50RevGR1b R50RevGR1c', mk299),
}


def setup():
    shutil.rmtree(S, ignore_errors=True)
    os.makedirs(FX)
    open(COUNTER, 'wb').write(show('tools/check-scrub-admission-r50.py'))
    ov = os.path.join(FX, 'ov')
    os.makedirs(ov)
    open(ov + '/entry.md', 'wb').write(show('corpus/knowledge/btrfs-scrub-grounding-r45.md').rstrip(b'\n')
                                       + b'\n' + MARK_ENTRY.encode() + b'\n')
    open(ov + '/skill.md', 'wb').write(show('SKILL.md').rstrip(b'\n') + b'\n' + MARK_SKILL.encode() + b'\n')
    open(ov + '/readme.md', 'wb').write(show('corpus/README.md').rstrip(b'\n')
                                        + b'\nThe rows in btrfs-scrub-grounding-r45.md are admitted round 50'
                                          b' after the cohort settled.\n')


def build(name, muts, raw=None):
    d = os.path.join(FX, name)
    wd = os.path.join(d, 'wave')
    os.makedirs(wd)
    tasks, results = [], []
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role in seats(row):
            txt = report(row, seat)
            if seat in muts:
                txt = muts[seat](row, seat, txt)
            open(os.path.join(wd, seat + '.md'), 'w', newline='').write(txt)
            tasks.append({'name': seat, 'agent': role})
            results.append({'name': seat, 'agent': role, 'output': f'{seat} completed'})
    if raw:
        open(os.path.join(wd, 'R50RevGR1a.md'), 'wb').write(raw)
    json.dump({'taskCall': {'tasks': tasks}}, open(d + '/dispatch.json', 'w'))
    json.dump({'results': results}, open(d + '/results.json', 'w'))
    return d


def run(d):
    cmd = ['python3', COUNTER, '--lane', LANE, '--revision', REV,
           '--entry-file', FX + '/ov/entry.md', '--skill-file', FX + '/ov/skill.md',
           '--readme-file', FX + '/ov/readme.md', '--wave-dir', d + '/wave',
           '--results-file', d + '/results.json', '--dispatch-file', d + '/dispatch.json']
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    o = json.loads(p.stdout)
    return {'rc': p.returncode, 'verdict': o['verdict'],
            'legs': {k: o[k] for k in ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok',
                                       'seats_ok', 'marks_ok')},
            'gr1_credited': o['per_row']['GR1']['credited'],
            'gr1_blocking': o['per_row']['GR1']['blocking'],
            'seat_notes': o['seat_notes']}


def main():
    setup()
    out = {'base': run(build('base', {}))}
    for name, mut in SINGLE.items():
        out[name] = run(build(name, {'R50RevGR1a': mut}))
    out['k_latin1'] = run(build('k_latin1', {}, raw=(
        b'ROW GR1 VERDICT: holds\nSECTION SHA256: ' + HASH['GR1'].encode() + b'\n'
        + body('GR1', 'R50RevGR1a').encode() + b'\xff\xfe invalid bytes\n')))
    for name, (seatstr, mut) in MULTI.items():
        out[name] = run(build(name, {s: mut for s in seatstr.split()}))
    json.dump(out, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    shutil.rmtree(S, ignore_errors=True)


if __name__ == '__main__':
    main()
