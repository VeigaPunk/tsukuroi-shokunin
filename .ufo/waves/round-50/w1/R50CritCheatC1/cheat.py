#!/usr/bin/env python3
"""C1-B4: build the cheapest artifact set that satisfies check-scrub-admission-r50.py
without the claimed work. Each scenario writes its own fixture dir under S/fx/<name>/,
runs the counter with fixture overrides, and records the JSON."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/tsukuroi-r50/R50CritCheatC1'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
COUNTER = os.path.join(S, 'counter.py')
ENTRY = os.path.join(S, 'corpus_knowledge_btrfs-scrub-grounding-r45.md')
SKILL = os.path.join(S, 'SKILL.md')
README = os.path.join(S, 'corpus_README.md')
DISPATCH = os.path.join(S, '.ufo_waves_round-50_w1-dispatch.json')

MARK_ENTRY = '## Gate status \u2014 round 50 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding \u2014 round 50 admission'
OLD_ENTRY = '## Gate status \u2014 round 50 (pending; the round-50 cohort has not settled)'

ROWS = ('GR1', 'GR2', 'GR3')
SEATS = {r: [(f'R50Rev{r}{x}', 'reviewer') for x in 'abc']
            + [(f'R50Crit{r}{x}', 'critic') for x in 'abc'] for r in ROWS}
CITES = {'GR1': ('cmdline.c:147', 'vsprintf.c:86'),
         'GR2': ('dev-replace.c:700', 'scrub.c:3081'),
         'GR3': ('btrfs-scrub@.service:1', 'capture.txt:1')}


def read(p):
    with open(p, encoding='utf-8') as fh:
        return fh.read()


def write(p, t):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(t)


def marked_entry():
    t = read(ENTRY)
    assert OLD_ENTRY in t
    return t.replace(OLD_ENTRY, MARK_ENTRY, 1)


def marked_skill():
    t = read(SKILL)
    return t.replace('## Scrub grounding \u2014 round 45 rows',
                     MARK_SKILL + '\n\n## Scrub grounding \u2014 round 45 rows', 1)


def marked_readme():
    t = read(README)
    return ('The scrub grounding rows in btrfs-scrub-grounding-r45.md are admitted round 50.\n\n'
            + t)


def section_hashes(entry_path):
    p = subprocess.run([sys.executable, COUNTER, '--revision', REV, '--lane', LANE,
                        '--section-hash', '--entry-file', entry_path],
                       capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256']


def body(row, seat, pad):
    a, b = CITES[row]
    return (f'Row {row} was read in full; nothing in it contradicts the row text.\n'
            f'{pad}\n'
            f'The two anchors are {a} and {b}.\n')


def report(row, seat, h, text):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {h}\n{text}'


def build(name, bodies, hashes, entry=None, skill=None, readme=None, results=None,
          stub_hash_seats=()):
    """bodies: {(row,seat): body text}. stub_hash_seats: seats emitted with a zero hash and
    a one-line body (no reading at all)."""
    d = os.path.join(S, 'fx', name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'wave'))
    e = entry if entry is not None else marked_entry()
    write(os.path.join(d, 'entry.md'), e)
    write(os.path.join(d, 'skill.md'), skill if skill is not None else marked_skill())
    write(os.path.join(d, 'readme.md'), readme if readme is not None else marked_readme())
    res = {'results': []}
    for row in ROWS:
        for seat, role in SEATS[row]:
            if seat in stub_hash_seats:
                txt = f'ROW {row} VERDICT: holds\nSECTION SHA256: ' + '0' * 64 + '\nstub\n'
            else:
                txt = report(row, seat, hashes[row], bodies[(row, seat)])
            write(os.path.join(d, 'wave', seat + '.md'), txt)
            out = results.get(seat, 'ok') if results is not None else 'ok'
            res['results'].append({'name': seat, 'agent': role, 'output': out})
    write(os.path.join(d, 'results.json'), json.dumps(res, indent=1))
    return d


def run(name, d):
    cmd = [sys.executable, COUNTER, '--revision', REV, '--lane', LANE,
           '--entry-file', os.path.join(d, 'entry.md'),
           '--skill-file', os.path.join(d, 'skill.md'),
           '--readme-file', os.path.join(d, 'readme.md'),
           '--wave-dir', os.path.join(d, 'wave'),
           '--results-file', os.path.join(d, 'results.json'),
           '--dispatch-file', DISPATCH, '--no-base-check']
    p = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, TMPDIR=S))
    try:
        o = json.loads(p.stdout)
    except Exception:
        o = {'raw': p.stdout, 'err': p.stderr}
    o['_rc'] = p.returncode
    write(os.path.join(S, 'receipts', name + '.json'), json.dumps(o, indent=1, sort_keys=True))
    return o


def summary(name, o):
    keys = ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok', 'seats_ok',
            'marks_ok')
    line = {k: o.get(k) for k in keys}
    pr = o.get('per_row') or {}
    line['rows'] = {r: {'credited': len(pr[r]['credited']), 'row_ok': pr[r]['row_ok'],
                        'distinct': pr[r]['distinct_bodies']} for r in pr}
    line['corr_forb'] = o.get('corr_forbidden_present')
    line['notes'] = (o.get('seat_notes') or [])[:6]
    print(name, json.dumps(line, sort_keys=True))
    return line


def main():
    H = section_hashes(ENTRY)          # real hashes
    real = read(ENTRY)
    out = {}

    # S0: the cheat baseline -- one sentence + 300 B of per-seat filler + 2 row citations.
    b = {}
    for row in ROWS:
        for seat, _ in SEATS[row]:
            b[(row, seat)] = body(row, seat, 'padding-' + seat + '-' + 'z' * 300)
    d = build('S0-cheap', b, H)
    out['S0-cheap'] = summary('S0-cheap', run('S0-cheap', d))

    # Sa: 18 reports, all the SAME body modulo trailing whitespace / blank lines.
    same = {}
    for row in ROWS:
        for i, (seat, _) in enumerate(SEATS[row]):
            same[(row, seat)] = body(row, 'X', 'z' * 300) + '\n' + '   ' * i
    d = build('Sa-whitespace', same, H)
    out['Sa-whitespace'] = summary('Sa-whitespace', run('Sa-whitespace', d))

    # Sc: first line holds, body prose-contradicts the verdict (no bound-format line).
    c = {}
    for row in ROWS:
        for seat, _ in SEATS[row]:
            a, bb = CITES[row]
            c[(row, seat)] = (f'Row {row} fails: the quoted text does not appear at {a} and the '
                              f'second anchor {bb} says nothing of the kind. seat={seat} '
                              + 'y' * 300)
    d = build('Sc-prose-contradiction', c, H)
    out['Sc-prose-contradiction'] = summary('Sc-prose-contradiction', run('Sc-prose-contradiction', d))

    # Sc2: same, but one report carries a bound-format negative for its own row.
    c2 = dict(c)
    c2[('GR1', 'R50RevGR1a')] = ('Row GR1 fails in prose and in the bound line.\nROW GR1 VERDICT: fails\n'
                                 + 'w' * 300)
    d = build('Sc2-bound-negative', c2, H)
    out['Sc2-bound-negative'] = summary('Sc2-bound-negative', run('Sc2-bound-negative', d))

    # Sd: results.json lists the seats with empty output.
    d = build('Sd-empty-output', b, H, results={s: '' for r in ROWS for s, _ in SEATS[r]})
    out['Sd-empty-output'] = summary('Sd-empty-output', run('Sd-empty-output', d))

    # Se1: one GR1 report cites entry.md:999999 (out of range) + a valid source.
    e1 = dict(b)
    e1[('GR1', 'R50RevGR1a')] = (f'Row GR1 read. The anchor is cmdline.c:147 and entry.md:999999. '
                                 + 'v' * 300)
    d = build('Se1-entry-out-of-range', e1, H)
    out['Se1-entry-out-of-range'] = summary('Se1-entry-out-of-range', run('Se1-entry-out-of-range', d))

    # Se2: one GR1 report cites SHA256SUMS:1 (declared lane artifact) + one real row source.
    e2 = dict(b)
    e2[('GR1', 'R50RevGR1a')] = ('Row GR1 read. The anchors are SHA256SUMS:1 and cmdline.c:147. '
                                 + 'u' * 300)
    d = build('Se2-shasums-plus-one', e2, H)
    out['Se2-shasums-plus-one'] = summary('Se2-shasums-plus-one', run('Se2-shasums-plus-one', d))

    # Smin: the cheapest PASS -- 3 credited seats per row, 3 stub seats per row.
    m = {}
    stubs = set()
    for row in ROWS:
        for i, (seat, _) in enumerate(SEATS[row]):
            if i < 3:
                m[(row, seat)] = body(row, seat, 'p' + seat + 'q' * 300)
            else:
                stubs.add(seat)
    d = build('Smin-9real-9stub', m, H, stub_hash_seats=stubs)
    out['Smin-9real-9stub'] = summary('Smin-9real-9stub', run('Smin-9real-9stub', d))

    # Sf: entry keeps the four round-49 corrections but reintroduces a round-48 defect string.
    bad = real.replace('dev-replace.c:1171-1195', 'dev-replace.c:1171-1195 (was dev-replace.c:1171-1199)', 1)
    assert bad != real
    hb = section_hashes_path(bad, 'Sf-entry.md')
    bf = {}
    for row in ROWS:
        for seat, _ in SEATS[row]:
            bf[(row, seat)] = body(row, seat, 'f' + seat + 'k' * 300)
    d = build('Sf-round48-defect', bf, hb, entry=bad)
    out['Sf-round48-defect'] = summary('Sf-round48-defect', run('Sf-round48-defect', d))

    write(os.path.join(S, 'receipts', 'summary.json'), json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v['verdict'] for k, v in out.items()}, sort_keys=True))


def section_hashes_path(text, name):
    p = os.path.join(S, name)
    write(p, text)
    return section_hashes(p)


if __name__ == '__main__':
    main()
