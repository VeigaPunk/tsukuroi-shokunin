#!/usr/bin/env python3
"""Build the C1 counter mutation fixtures (clean + one defect set per mutant)."""
import hashlib, json, os, subprocess, sys

S = '/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterA'
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '55c07cd3f8bff2e12117c34d57b4c618de74d85c'
COUNTER = os.path.join(S, 'counter.orig.py')
OUT = os.path.join(S, 'sets')
CITE = {'GR1': 'cmdline.c:147', 'GR2': 'dev-replace.c:700', 'GR3': 'scrub.c:3094'}
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
README_SENT = ('The btrfs scrub grounding entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` is '
               'admitted round 49 for GR1-GR3 by the counted cohort.')
PAD = (' The reading was checked against the pinned snapshot lines named above and against the errno '
       'ordering the row states; nothing in the row contradicts the bytes that were read, and the host '
       'reading remains marked where the capture does not decide it. This paragraph is padding so the '
       'body clears the counter floor without adding a second citation.')


def blob(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True)
    assert p.returncode == 0, path
    return p.stdout.decode()


def base_files(d):
    os.makedirs(d, exist_ok=True)
    entry = blob(REV, 'corpus/knowledge/btrfs-scrub-grounding-r45.md')
    y = os.path.join(d, 'entry.md')
    open(y, 'w').write(entry + '\n' + MARK_ENTRY + '\n\nadmitted round 49 by the counted cohort.\n')
    s = os.path.join(d, 'skill.md')
    open(s, 'w').write(blob(REV, 'SKILL.md') + '\n' + MARK_SKILL + '\n')
    r = os.path.join(d, 'readme.md')
    open(r, 'w').write(blob(REV, 'corpus/README.md') + '\n' + README_SENT + '\n')
    return y, s, r


def section_hashes(entry_path, skill_path, readme_path):
    p = subprocess.run(['python3', COUNTER, '--revision', REV, '--entry-file', entry_path,
                        '--skill-file', skill_path, '--readme-file', readme_path,
                        '--no-base-check', '--section-hash'], capture_output=True, text=True)
    return json.loads(p.stdout.strip().split('\n')[-1])['section_sha256']


def body(seat, row):
    return (f'{seat} read row {row} at the frozen bytes. The clause chain at {CITE[row]} agrees with '
            f'the row, the quoted lines sit where the row cites them, and the host reading keeps its '
            f'inference mark where the capture does not decide it.' + PAD)


def report(seat, row, verdict, h, b=None):
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {h}\n{b if b is not None else body(seat, row)}\n'


def write_cohort(d, hashes, verdicts=None, bodies=None, hashes_override=None):
    os.makedirs(d, exist_ok=True)
    verdicts = verdicts or {}
    bodies = bodies or {}
    hashes_override = hashes_override or {}
    for row in ('GR1', 'GR2', 'GR3'):
        for prefix in ('Rev', 'Crit'):
            for x in 'abc':
                seat = f'R49{prefix}{row}{x}'
                h = hashes_override.get(seat, hashes[row])
                open(os.path.join(d, f'{seat}.md'), 'w').write(
                    report(seat, row, verdicts.get(seat, 'holds'), h, bodies.get(seat)))


def write_results(path, skip=(), empty=(), wrongrole=(), dup=()):
    names = [f'R49{p}GR{r}{x}' for r in '123' for p in ('Rev', 'Crit') for x in 'abc']
    res = {'lane': 'tsukuroi', 'round': 49, 'wave': 'w1', 'seats': 18, 'results': []}
    for n in names:
        if n in skip:
            continue
        res['results'].append({'name': n,
                               'agent': (('critic' if 'Rev' in n else 'reviewer')
                                         if n in wrongrole else
                                         ('reviewer' if 'Rev' in n else 'critic')),
                               'output': '' if n in empty else 'ok', 'note': None})
        if n in dup:
            res['results'].append({'name': n, 'agent': 'reviewer' if 'Rev' in n else 'critic',
                                   'output': 'ok', 'note': None})
    json.dump(res, open(path, 'w'))


def build(name, verdicts=None, bodies=None, hashes_override=None, skip_results=(),
          empty_results=(), wrongrole_results=(), dup_results=()):
    d = os.path.join(OUT, name)
    y, s, r = base_files(d)
    hashes = section_hashes(y, s, r)
    write_cohort(os.path.join(d, 'w1'), hashes, verdicts, bodies, hashes_override)
    write_results(os.path.join(d, 'results.json'), skip=skip_results,
                  empty=empty_results, wrongrole=wrongrole_results, dup=dup_results)
    return {'name': name, 'entry': y, 'skill': s, 'readme': r,
            'wave_dir': os.path.join(d, 'w1'), 'results': os.path.join(d, 'results.json'),
            'hashes': hashes}


def main():
    os.makedirs(OUT, exist_ok=True)
    sets = []
    clean = build('clean')
    sets.append(clean)
    # D1: a bound seat reports `partly` (blocking rule defect)
    sets.append(build('d1-partly', verdicts={'R49CritGR2b': 'partly'}))
    # D1b: a bound seat reports `fails` (A2 covers fails too)
    sets.append(build('d1b-fails', verdicts={'R49RevGR3a': 'fails'}))
    # D1c: report body contradicts its own first line (returns partly -> A2 blocks)
    sets.append(build('d1c-contradict',
                      bodies={'R49RevGR1c': body('R49RevGR1c', 'GR1') + '\nROW GR1 VERDICT: partly\n'}))
    # D2: two byte-identical credited bodies in GR1 (distinct-bodies defect)
    dup = body('dup', 'GR1')
    sets.append(build('d2-dupbodies', bodies={'R49RevGR1a': dup, 'R49RevGR1b': dup}))
    # D3: one results.json entry absent (results-seat defect)
    sets.append(build('d3-noresults', skip_results=('R49CritGR3c',)))
    # D4: a report carries a wrong-but-64-hex section hash (hash-value defect)
    sets.append(build('d4-badhash', hashes_override={'R49RevGR2a': 'f' * 64}))
    # D4b: every GR3 seat carries a wrong-but-64-hex hash (all six uncredited -> row drops)
    sets.append(build('d4b-badhash-all',
                      hashes_override={f'R49{p_}GR3{x}': 'f' * 64
                                       for p_ in ('Rev', 'Crit') for x in 'abc'}))
    # D3b: the results list is empty (no results.json entries at all)
    d3b = build('d3b-emptyresults', skip_results=tuple(
        f'R49{p_}GR{r}{x}' for r in '123' for p_ in ('Rev', 'Crit') for x in 'abc'))
    sets.append(d3b)
    # D4-boundary: exactly 3 of GR1's six seats carry a wrong 64-hex hash, leaving a
    # roster of 3 credited seats (1 reviewer + 2 critics) -> row still clears the floor
    sets.append(build('d4c-badhash-3of6',
                      hashes_override={'R49RevGR1a': 'f' * 64, 'R49RevGR1b': 'f' * 64,
                                       'R49CritGR1a': 'f' * 64}))
    # D4-boundary-2: 4 of six wrong -> 2 credited -> row drops
    sets.append(build('d4d-badhash-4of6',
                      hashes_override={'R49RevGR1a': 'f' * 64, 'R49RevGR1b': 'f' * 64,
                                       'R49CritGR1a': 'f' * 64, 'R49CritGR1b': 'f' * 64}))
    # OBS (probe, not one of M1-M4): the A2 blocker only sees a machine `ROW GR<n> VERDICT:`
    # line. A report that states `partly` in prose only escapes it.
    sets.append(build('d5-prose-partly',
                      bodies={'R49CritGR1a': body('R49CritGR1a', 'GR1') +
                              ' Reading it again I judge this row partly correct: the errno order '
                              'is right but the wording overstates it.'}))
    # D3c: one results entry has an empty output (no completed verdict)
    sets.append(build('d3c-emptyoutput', empty_results=('R49RevGR2c',)))
    # D3d: one results entry names the wrong agent role
    sets.append(build('d3d-wrongrole', wrongrole_results=('R49CritGR2a',)))
    # D3e: one seat appears twice in results.json (not exactly one entry)
    sets.append(build('d3e-dupentry', dup_results=('R49RevGR3b',)))
    # D4e: a GR1 seat carries GR2's correct hash (cross-row hash slip)
    gr2h = clean['hashes']['GR2']
    sets.append(build('d4e-crossrow', hashes_override={'R49RevGR1a': gr2h, 'R49RevGR1b': gr2h,
                                                       'R49CritGR1a': gr2h, 'R49CritGR1b': gr2h}))
    # OBS: the documented credit floor is 3 credited seats per row out of 6. Probe the
    # maximal acceptance margin: 3 of 6 seats in EVERY row declare a hash that is not the
    # row's section hash (2 reviewers + 1 critic), leaving a 1-reviewer/2-critic roster.
    sets.append(build('d4f-margin-3of6-allrows',
                      hashes_override={f'R49{p_}GR{r}{x}': 'f' * 64
                                       for r in '123' for p_, x in
                                       (('Rev', 'a'), ('Rev', 'b'), ('Crit', 'a'))}))
    json.dump(sets, open(os.path.join(S, 'sets.json'), 'w'), indent=1)
    print(json.dumps([c['name'] for c in sets]))
    print(json.dumps(clean['hashes'], indent=1))


if __name__ == '__main__':
    main()
