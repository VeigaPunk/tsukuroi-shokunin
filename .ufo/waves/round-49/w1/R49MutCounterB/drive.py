#!/usr/bin/env python3
"""Seat R49MutCounterB: mutants M5-M8 on the frozen C1 counter.

Fixture set: clean (K-pass) + one defect fixture per mutant. Every counter run is the
frozen counter (base/check.py, sha256 recorded) or a one-line mutant copy of it.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
L = os.path.join(S, 'fixture-repo')
REV = 'b559488cc8400cc2dc7c8f96309f4a5f1a154dbc'
BASE = '6256760d1382ce4ce20fcba830d4b2912cfbf12b'
CITE = {'GR1': 'cmdline.c:147', 'GR2': 'dev-replace.c:700', 'GR3': 'scrub.c:3094'}
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
README_SENT = ('The btrfs scrub grounding entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` is '
               'admitted round 49 for GR1-GR3 by the counted cohort.')
README_NEG = ('The btrfs scrub grounding entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` is '
              'not admitted round 49; the counted cohort has not finished, so the rows stay pending.')
PAD = (' The reading was checked against the pinned snapshot lines named above and against the errno '
       'ordering the row states; nothing in the row contradicts the bytes that were read, and the host '
       'reading remains marked where the capture does not decide it. This paragraph is padding so the '
       'body clears the counter floor without adding a second citation.')
R = os.path.join(S, 'fx')


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL, text=True,
                          cwd=S, **kw)


def blob(rev, path):
    p = sh(['git', '-C', L, 'show', f'{rev}:{path}'])
    assert p.returncode == 0, f'show {rev}:{path} rc={p.returncode} {p.stderr[:200]}'
    return p.stdout


def jrun(cmd):
    p = sh(cmd)
    line = (p.stdout or '').strip().split('\n')[-1] if p.stdout.strip() else '{}'
    try:
        o = json.loads(line)
    except Exception:
        o = {'parse_error': True, 'raw': line[:400], 'stderr': (p.stderr or '')[:400]}
    o['_rc'] = p.returncode
    return o


def sha(b):
    return hashlib.sha256(b).hexdigest()


def section_hashes(counter, entry_path):
    o = jrun(['python3', counter, '--revision', REV, '--lane', L, '--no-base-check', '--section-hash',
              '--entry-file', entry_path, '--skill-file', os.path.join(R, 'skill-clean.md'),
              '--readme-file', os.path.join(R, 'readme-clean.md')])
    return o['section_sha256'], o


def report(seat, row, verdict, h, body=None):
    if body is None:
        body = (f'{seat} read row {row} at the frozen bytes. The clause chain at {CITE[row]} agrees '
                f'with the row, the quoted lines sit where the row cites them, and the host reading '
                f'keeps its inference mark where the capture does not decide it.' + PAD)
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {h}\n{body}\n'


def cohort(dirpath, row_hashes, bodies=None):
    os.makedirs(dirpath, exist_ok=True)
    for row in ('GR1', 'GR2', 'GR3'):
        for prefix in ('Rev', 'Crit'):
            for letter in 'abc':
                seat = f'R49{prefix}{row}{letter}'
                body = (bodies or {}).get(seat)
                with open(os.path.join(dirpath, f'{seat}.md'), 'w') as fh:
                    fh.write(report(seat, row, 'holds', row_hashes[row], body))


def results_file(path):
    names = [f'R49{p}GR{r}{x}' for r in '123' for p in ('Rev', 'Crit') for x in 'abc']
    res = {'lane': 'tsukuroi', 'round': 49, 'wave': 'w1', 'seats': len(names), 'results': []}
    for n in names:
        res['results'].append({'name': n, 'agent': 'reviewer' if 'Rev' in n else 'critic',
                               'output': 'ok', 'note': None})
    with open(path, 'w') as fh:
        json.dump(res, fh)
    return path


def mutate(name, old, new):
    src = open(os.path.join(S, 'base', 'check.py')).read()
    assert src.count(old) == 1, f'{name}: pattern count {src.count(old)}'
    dst = src.replace(old, new, 1)
    p = os.path.join(S, 'mutants', f'{name}.py')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write(dst)
    return p


def main():
    os.makedirs(R, exist_ok=True)
    entry = blob(REV, 'corpus/knowledge/btrfs-scrub-grounding-r45.md')
    skill = blob(REV, 'SKILL.md')
    readme = blob(REV, 'corpus/README.md')
    base_counter = os.path.join(S, 'base', 'check.py')
    rec = []

    def w(name, text):
        p = os.path.join(R, name)
        open(p, 'w').write(text)
        return p

    # ---- fixture files ----
    f_entry = w('entry-clean.md', entry + '\n' + MARK_ENTRY + '\n\nadmitted round 49 by the counted cohort.\n')
    f_skill = w('skill-clean.md', skill + '\n' + MARK_SKILL + '\n')
    f_readme = w('readme-clean.md', readme + '\n' + README_SENT + '\n')
    rowh, hinfo = section_hashes(base_counter, f_entry)
    assert set(rowh) == {'GR1', 'GR2', 'GR3'}, hinfo
    cohort(os.path.join(R, 'cohort-clean'), rowh)
    res_clean = results_file(os.path.join(R, 'res-clean.json'))

    # D5: citation-free bodies (>=300 bytes, no file:line anywhere) for every GR2 seat.
    d5_bodies = {f'R49{p}GR2{x}':
                 (f'{p}{x} read row GR2 against the frozen bytes and found the clause chain '
                  f'consistent with the row; the quoted lines sit where the row cites them and the '
                  f'host reading keeps its inference mark where the capture does not decide it.'
                  + PAD)
                 for p in ('Rev', 'Crit') for x in 'abc'}
    cohort(os.path.join(R, 'cohort-d5'), rowh, d5_bodies)
    res_d5 = results_file(os.path.join(R, 'res-d5.json'))

    # D6: short bodies (<300 bytes) that do cite a resolving pinned file, for every GR3 seat.
    d6_bodies = {f'R49{p}GR3{x}': f'read {p}GR3{x} at scrub.c:{3094 + i}'
                 for i, (p, x) in enumerate([(p, x) for p in ('Rev', 'Crit') for x in 'abc'])}
    for b in d6_bodies.values():
        assert len(b.encode()) < 300
    cohort(os.path.join(R, 'cohort-d6'), rowh, d6_bodies)
    res_d6 = results_file(os.path.join(R, 'res-d6.json'))

    # D7: one corrupted quote in GR1 (line number outside the pinned snapshot).
    assert entry.count('cmdline.c:147') == 1
    d7_entry = entry.replace('cmdline.c:147', 'cmdline.c:90147')
    f_entry_d7 = w('entry-d7.md', d7_entry + '\n' + MARK_ENTRY + '\n\nadmitted round 49 by the counted cohort.\n')
    rowh7, hinfo7 = section_hashes(base_counter, f_entry_d7)
    assert rowh7['GR1'] != rowh['GR1'] and rowh7['GR2'] == rowh['GR2'], hinfo7
    cohort(os.path.join(R, 'cohort-d7'), rowh7)
    res_d7 = results_file(os.path.join(R, 'res-d7.json'))

    # D8: the only README name+phrase sentence is negated.
    f_readme_d8 = w('readme-d8.md', readme + '\n' + README_NEG + '\n')

    # ---- mutants ----
    m5 = mutate('M5', 'def report_citations_ok(cache, body, row):\n',
                'def report_citations_ok(cache, body, row):\n'
                "    return True, 'M5: citation leg neutralized'\n")
    m6 = mutate('M6', '    if len(body.encode(\'utf-8\')) < 300:',
                '    if len(body.encode(\'utf-8\')) < 0:')
    m7 = mutate('M7', "    quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0 and not quotes[r]['bad'])",
                "    quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0)")
    m8 = mutate('M8',
                '        if name in sentence and phrase in sentence and not NEGATE_RE.search(sentence):',
                '        if name in sentence and phrase in sentence:')

    def run(label, counter, entry_file, wave_dir, results, readme_file=f_readme, skill_file=f_skill):
        o = jrun(['python3', counter, '--revision', REV, '--lane', L, '--no-base-check',
                  '--entry-file', entry_file, '--skill-file', skill_file,
                  '--readme-file', readme_file, '--wave-dir', wave_dir,
                  '--results-file', results])
        keep = {k: o.get(k) for k in ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok',
                                      'verdicts_ok', 'seats_ok', 'marks_ok')}
        keep['_rc'] = o['_rc']
        keep['error'] = o.get('error')
        keep['notes'] = (o.get('seat_notes') or [])[:4]
        rec.append({'run': label, 'counter': os.path.relpath(counter, S),
                    'counter_sha256': sha(open(counter, 'rb').read()),
                    'fixture': os.path.relpath(wave_dir, S), **keep})
        print(label, keep)

    clean = os.path.join(R, 'cohort-clean')
    for label, counter, e, d, r in [
            ('orig/clean', base_counter, f_entry, clean, res_clean),
            ('orig/D5', base_counter, f_entry, os.path.join(R, 'cohort-d5'), res_d5),
            ('orig/D6', base_counter, f_entry, os.path.join(R, 'cohort-d6'), res_d6),
            ('orig/D7', base_counter, f_entry_d7, os.path.join(R, 'cohort-d7'), res_d7),
            ('orig/D8', base_counter, f_entry, clean, res_clean)]:
        if label == 'orig/D8':
            rec_run = dict(readme_file=f_readme_d8)
            o = jrun(['python3', counter, '--revision', REV, '--lane', L, '--no-base-check',
                      '--entry-file', e, '--skill-file', f_skill, '--readme-file', f_readme_d8,
                      '--wave-dir', d, '--results-file', r])
            keep = {k: o.get(k) for k in ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok',
                                          'verdicts_ok', 'seats_ok', 'marks_ok')}
            keep['_rc'] = o['_rc']
            keep['error'] = o.get('error')
            keep['notes'] = (o.get('seat_notes') or [])[:4]
            rec.append({'run': label, 'counter': os.path.relpath(counter, S),
                        'counter_sha256': sha(open(counter, 'rb').read()),
                        'fixture': 'readme-d8 + cohort-clean', **keep})
            print(label, keep)
            continue
        run(label, counter, e, d, r)

    run('M5/clean', m5, f_entry, clean, res_clean)
    run('M5/D5', m5, f_entry, os.path.join(R, 'cohort-d5'), res_d5)
    run('M6/clean', m6, f_entry, clean, res_clean)
    run('M6/D6', m6, f_entry, os.path.join(R, 'cohort-d6'), res_d6)
    run('M7/clean', m7, f_entry, clean, res_clean)
    run('M7/D7', m7, f_entry_d7, os.path.join(R, 'cohort-d7'), res_d7)
    run('M8/clean', m8, f_entry, clean, res_clean)
    # M8/D8 needs the negated README.
    o = jrun(['python3', m8, '--revision', REV, '--lane', L, '--no-base-check', '--entry-file', f_entry,
              '--skill-file', f_skill, '--readme-file', f_readme_d8,
              '--wave-dir', clean, '--results-file', res_clean])
    keep = {k: o.get(k) for k in ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok',
                                  'verdicts_ok', 'seats_ok', 'marks_ok')}
    keep['_rc'] = o['_rc']
    keep['error'] = o.get('error')
    keep['notes'] = (o.get('seat_notes') or [])[:4]
    rec.append({'run': 'M8/D8', 'counter': os.path.relpath(m8, S),
                'counter_sha256': sha(open(m8, 'rb').read()),
                'fixture': 'readme-d8 + cohort-clean', **keep})
    print('M8/D8', keep)

    # Cross-checks: each mutant still fails on a fixture it does not tolerate.
    run('M5/D6', m5, f_entry, os.path.join(R, 'cohort-d6'), res_d6)
    run('M6/D5', m6, f_entry, os.path.join(R, 'cohort-d5'), res_d5)
    run('M7/D4-none', m7, f_entry, os.path.join(R, 'cohort-d5'), res_d5)
    run('M8/D7', m8, f_entry_d7, os.path.join(R, 'cohort-d7'), res_d7)

    with open(os.path.join(S, 'runs.jsonl'), 'w') as fh:
        for r in rec:
            fh.write(json.dumps(r, sort_keys=True) + '\n')
    # fixture + counter hashes
    lines = []
    for root in ('base', 'mutants'):
        d = os.path.join(S, root)
        for n in sorted(os.listdir(d)):
            p = os.path.join(d, n)
            if os.path.isfile(p):
                lines.append(f'{sha(open(p, "rb").read())}  {root}/{n}')
    for n in sorted(os.listdir(R)):
        p = os.path.join(R, n)
        if os.path.isfile(p):
            lines.append(f'{sha(open(p, "rb").read())}  fx/{n}')
    open(os.path.join(S, 'sha256-receipts.txt'), 'w').write('\n'.join(lines) + '\n')
    print('DONE', len(rec), 'runs')


if __name__ == '__main__':
    main()
