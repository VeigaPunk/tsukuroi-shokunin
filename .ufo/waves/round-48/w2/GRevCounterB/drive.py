#!/usr/bin/env python3
"""GRevCounterB: admission-rule probes against the frozen r48 C2 counter.
Each case clones the lane at BASE, writes marks + a synthetic w2 cohort, commits,
and runs the frozen counter copy at ./counter.py. Receipts -> cases.jsonl."""
import json, os, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '5fdf062f969292736e36513e39f98b1b8de43635'
ROOT = '/fast/scratch/hyaku/tsukuroi-r48/GRevCounterB/fx'
COUNTER = '/fast/scratch/hyaku/tsukuroi-r48/GRevCounterB/counter.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
W = '.ufo/waves/round-48'
HASHES = {'GR1': 'fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8',
          'GR2': 'e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce',
          'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
CITE = {'GR1': 'cmdline.c:147', 'GR2': 'dev-replace.c:700', 'GR3': 'scrub.c:421'}


def git(d, *a):
    return subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@invalid', *a],
                          capture_output=True, check=True).stdout.decode()


def seat_names(row):
    n = row[2:]
    return ([(f'R48RevGR{n}{x}', 'reviewer') for x in 'abc']
            + [(f'R48CritGR{n}{x}', 'critic') for x in 'abc'])


def body_for(seat, row, cite=None):
    c = cite or CITE[row]
    return (f'Checked every clause of {row} against the pinned snapshots; seat {seat} '
            f'independent pass. Evidence {c} read verbatim. '
            + 'The row clause matches its cited line. ' * 12)


def build(name, *, readme_lines=None, seat_edit=None, dispatch_edit=None, results_edit=None):
    """seat_edit(seat, role, row) -> (verdict, hash, body) | None(default holds+cur hash)."""
    d = os.path.join(ROOT, name)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
    top = git(d, 'rev-parse', '--show-toplevel').strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    git(d, 'checkout', '-q', '--detach', BASE)
    with open(os.path.join(d, ENTRY), 'a', encoding='utf-8') as f:
        f.write('\n## Gate status — round 48 (GR1-GR3 admitted)\n')
    with open(os.path.join(d, 'SKILL.md'), 'a', encoding='utf-8') as f:
        f.write('\n## Scrub grounding — round 48 admission\n')
    with open(os.path.join(d, 'corpus/README.md'), 'a', encoding='utf-8') as f:
        for ln in (readme_lines if readme_lines is not None else
                   ['- btrfs-scrub-grounding-r45.md admitted round 48']):
            f.write('\n' + ln + '\n')
    tasks, results = [], []
    w2 = os.path.join(d, W, 'w2')
    os.makedirs(w2, exist_ok=True)
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role in seat_names(row):
            verdict, h, body = 'holds', HASHES[row], body_for(seat, row)
            if seat_edit:
                r = seat_edit(seat, role, row)
                if r is not None:
                    verdict, h, body = r
            with open(os.path.join(w2, seat + '.md'), 'w', encoding='utf-8') as f:
                f.write(f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {h}\n{body}\n')
            tasks.append({'name': seat, 'agent': role})
            results.append({'name': seat, 'agent': role, 'status': 'done'})
    if dispatch_edit:
        tasks = dispatch_edit(tasks)
    if results_edit:
        results = results_edit(results)
    with open(os.path.join(d, W, 'w2-dispatch.json'), 'w') as f:
        json.dump({'taskCall': {'tasks': tasks}}, f)
    with open(os.path.join(d, W, 'w2-results.json'), 'w') as f:
        json.dump({'results': results}, f)
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', 'fixture ' + name)
    return d, git(d, 'rev-parse', 'HEAD').strip()


def counter(d, rev):
    p = subprocess.run(['python3', COUNTER, '--revision', rev, '--lane', d],
                       capture_output=True)
    return p.returncode, json.loads(p.stdout.decode() or '{}')


def run(cases):
    out = []
    for label, kw, want in cases:
        d, rev = build(label.split()[0].lower(), **kw)
        rc, r = counter(d, rev)
        row1 = r.get('per_row', {}).get('GR1', {})
        out.append({'case': label, 'expected': want, 'rc': rc, 'verdict': r.get('verdict'),
                    'verdicts_ok': r.get('verdicts_ok'), 'marks_ok': r.get('marks_ok'),
                    'gr1_credited': row1.get('credited'), 'gr1_blocking': row1.get('blocking'),
                    'gr1_any_fails': row1.get('any_fails'),
                    'gr1_seat_detail': {k: v['detail'] for k, v in row1.get('seats', {}).items()},
                    'as_expected': r.get('verdict') == want})
    return out


def main():
    os.makedirs(ROOT, exist_ok=True)
    stale = '0' * 64

    def edit_stale_partly(s, r_, row):
        if s == 'R48CritGR1b':
            return 'partly', stale, body_for(s, row)
        return None

    def edit_stale_fails(s, r_, row):
        if s == 'R48CritGR1b':
            return 'fails', stale, body_for(s, row)
        return None

    def edit_garbage_fails(s, r_, row):
        if s == 'R48CritGR1b':
            return 'fails', 'zzzz-not-hex', body_for(s, row)
        return None

    def edit_gr2_revs_partly(s, r_, row):
        if row == 'GR2' and r_ == 'reviewer':
            return 'partly', HASHES[row], body_for(s, row)
        return None

    def edit_prose_fails(s, r_, row):
        if s == 'R48RevGR1a':
            return 'holds', HASHES[row], body_for(s, row) + '\nOn reflection this row fails.\n'
        return None

    def edit_struct_contra(s, r_, row):
        if s == 'R48RevGR1a':
            return 'holds', HASHES[row], body_for(s, row) + f'\nROW {row} VERDICT: fails\n'
        return None

    def edit_rejects(s, r_, row):
        if s == 'R48RevGR1c':
            return 'rejects', HASHES[row], body_for(s, row)
        return None

    def edit_fails_curhash(s, r_, row):
        if s == 'R48CritGR2a':
            return 'fails', HASHES[row], body_for(s, row)
        return None

    def edit_unpinned_cite(s, r_, row):
        if s == 'R48RevGR3a':
            return 'holds', HASHES[row], body_for(s, row) + '\nSee also notes.txt:3 and check-scrub-admission-r48.py:120.\n'
        return None

    def edit_stale_holds_x4(s, r_, row):
        if row == 'GR1' and s in ('R48RevGR1a', 'R48RevGR1b', 'R48CritGR1b', 'R48CritGR1c'):
            return 'holds', stale, body_for(s, row)
        return None

    cases = [
        ('A0 clean cohort, all holds, all marks', {}, 'PASS'),
        ('A1 one GR1 partly on a STALE hash (ignored? row admitted on 5 holds)',
         dict(seat_edit=edit_stale_partly), 'PASS'),
        ('A1b one GR1 fails on a STALE hash (blocks via any_fails despite stale hash)',
         dict(seat_edit=edit_stale_fails), 'FAIL'),
        ('A1c one GR1 fails on a MALFORMED hash line (seat vanishes entirely)',
         dict(seat_edit=edit_garbage_fails), 'PASS'),
        ('B GR2: 3 critics hold, 3 reviewers read partly on current hash (blocks)',
         dict(seat_edit=edit_gr2_revs_partly), 'FAIL'),
        ('C1 GR1a holds on line 1 but prose "this row fails" (credited)',
         dict(seat_edit=edit_prose_fails), 'PASS'),
        ('C2 GR1a holds on line 1, later structured ROW-VERDICT fails (blocks as partly)',
         dict(seat_edit=edit_struct_contra), 'FAIL'),
        ('C3 GR1c line1 "rejects" - unlisted verdict word (unbound, ignored)',
         dict(seat_edit=edit_rejects), 'PASS'),
        ('D README line "review pending; not yet admitted round 48" (negation gap)',
         dict(readme_lines=['- btrfs-scrub-grounding-r45.md review pending; not yet admitted round 48']),
         'PASS'),
        ('E1 GR2a fails report omitted from dispatch tasks (results+file kept)',
         dict(seat_edit=edit_fails_curhash,
              dispatch_edit=lambda ts: [t for t in ts if t['name'] != 'R48CritGR2a']),
         'PASS'),
        ('E2 GR2a fails report dispatched TWICE',
         dict(seat_edit=edit_fails_curhash,
              dispatch_edit=lambda ts: ts + [t for t in ts if t['name'] == 'R48CritGR2a']),
         'PASS'),
        ('A2 GR1: only 2 holds on current hash + 4 holds on STALE hash (credited < 3)',
         dict(seat_edit=edit_stale_holds_x4), 'FAIL'),
        ('E3 GR2a fails report omitted from w2-results.json (dispatch+file kept)',
         dict(seat_edit=edit_fails_curhash,
              results_edit=lambda rs: [x for x in rs if x['name'] != 'R48CritGR2a']),
         'PASS'),
        ('F GR1a results entry output says seat errored, holds file binds anyway',
         dict(results_edit=lambda rs: [dict(x, output='ERROR: seat stopped, no report')
                                       if x['name'] == 'R48RevGR1a' else x for x in rs]),
         'PASS'),
        ('G GR3a holds body cites unpinned notes.txt:3 and a .py file (loses credit, row still passes on 5)',
         dict(seat_edit=edit_unpinned_cite), 'PASS'),
    ]
    res = run(cases)
    with open('/fast/scratch/hyaku/tsukuroi-r48/GRevCounterB/cases.jsonl', 'w') as f:
        for x in res:
            f.write(json.dumps(x) + '\n')
    for x in res:
        print(json.dumps({k: x[k] for k in ('case', 'rc', 'verdict', 'expected', 'as_expected')}))
    print('unexpected:', [x['case'] for x in res if not x['as_expected']])


if __name__ == '__main__':
    sys.exit(main())
