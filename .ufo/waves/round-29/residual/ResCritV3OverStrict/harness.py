#!/usr/bin/env python3
"""Should-pass marker variants against owed counter v3 (seat ResCritV3OverStrict, sandbox only)."""
import json
import os
import re
import subprocess
import sys

REPO = '/fast/scratch/hyaku/tsukuroi-r29/ResCritV3OverStrict/repo'
TIP = '06e00dafbbaa4695bc74decf68c816da8151b00a'
COUNTER = os.path.join(REPO, 'tools/check-owed-statements-r29.py')
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null')


def git(*a):
    p = subprocess.run(['git', '-C', REPO, '-c', 'user.name=seat', '-c', 'user.email=seat@sandbox', *a],
                       capture_output=True, env=ENV, text=True)
    if p.returncode:
        raise SystemExit(f'git {a} failed: {p.stderr}')
    return p.stdout


def rd(p):
    with open(os.path.join(REPO, p), encoding='utf-8') as fh:
        return fh.read()


def wr(p, s):
    with open(os.path.join(REPO, p), 'w', encoding='utf-8') as fh:
        fh.write(s)


def sub_line(p, prefix, fn):
    lines = rd(p).split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, (p, prefix, idx)
    lines[idx[0]] = fn(lines[idx[0]])
    wr(p, '\n'.join(lines))


def json_edit(p, iid, fn):
    lines = rd(p).split('\n')
    idx = [i for i, l in enumerate(lines) if f'"R29-OWED-{iid}"' in l]
    assert len(idx) == 1, (p, iid, idx)
    i = idx[0]
    if lines[i].lstrip().startswith('{'):
        obj = json.loads(lines[i].strip().rstrip(','))
        obj = fn(obj)
        tail = ',' if lines[i].rstrip().endswith(',') else ''
        lines[i] = '  ' + json.dumps(obj, ensure_ascii=False) + tail
        wr(p, '\n'.join(lines))
        return
    doc = json.loads(rd(p))
    for c in doc['corrections_r29']:
        if c['id'] == f'R29-OWED-{iid}':
            c2 = fn(dict(c))
            c.clear(); c.update(c2)
    wr(p, json.dumps(doc, indent=1, ensure_ascii=False) + '\n')


OOM = 'corpus/knowledge/oom-event-plane.md'
KILL = 'corpus/knowledge/kill-event-deep-r8.md'
DRV = 'corpus/knowledge/driver-firmware-plane.md'
SH = 'corpus/knowledge/storage-health-r26.json'
MPJ = 'corpus/knowledge/memory-pressure-r25.json'
SHMD = 'corpus/knowledge/storage-health-r26.md'

NUM_NOW = ('oom_score_adj +200 adds 3,381,800 points (12.9 GiB) to 14,080,000 points (53.7 GiB); '
           'the max of 1 pass wins: 0 bands, 0 order, 1 victim, tie at 0.0 % margin.')


def v(name, target, apply, note):
    return dict(name=name, target=target, apply=apply, note=note)


def skill_shifted_ref():
    # an unchanged base line of SKILL.md cited at its tip line number (shifted +2 by the r29 insertion at 2320)
    lines = rd('SKILL.md').split('\n')
    for n in range(2330, 2531):
        if lines[n - 1].startswith('| MP') or 'oomd' in lines[n - 1]:
            return n
    return 2400


def v_skill_shift():
    n = skill_shifted_ref()
    sub_line('SKILL.md', '[R29-OWED-O05]', lambda l: re.sub(r'\| basis: .*$', f'| basis: SKILL.md:{n}', l))
    return f'SKILL.md:{n}'


def v_append_and_cite():
    # the round appends one evidence line to the cited file, then cites it
    s = rd(SHMD)
    if not s.endswith('\n'):
        s += '\n'
    s += '- SH3 round-29 note: systemd v262 tmpfiles journal-nocow.conf is the source of the NOCOW attribute (read 2026-10-22).\n'
    wr(SHMD, s)
    n = s.count('\n')
    json_edit(SH, 'O10', lambda c: {**c, 'basis': [f'corpus/knowledge/storage-health-r26.md:{n}']})
    return f'{SHMD}:{n}'


def v_append_keeps_old():
    s = rd(SHMD)
    wr(SHMD, s + '- round-29 appended note, unrelated to the cited lines.\n')
    return 'append only'


def v_insert_above():
    lines = rd(SHMD).split('\n')
    lines.insert(5, '> Round-29 note: see the correction markers in storage-health-r26.json.')
    wr(SHMD, '\n'.join(lines))
    return 'one line inserted at line 6'


def v_capture_this_round():
    p = '.ufo/waves/round-29/w1/RevOomMechanism/oom_kill.c'
    lines = rd(p).split('\n')
    n = next(i for i, l in enumerate(lines, 1) if 'oom_score_adj' in l and l.strip())
    json_edit(MPJ, 'O07', lambda c: {**c, 'basis': [f'{p}:{n}']})
    return f'{p}:{n}'


VARIANTS = [
    v('list-dash', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '- ' + l), '`- ` list item'),
    v('list-dash-bold', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '- **[R29-OWED-O01]**' + l[len('[R29-OWED-O01]'):]), '`- **[id]**`'),
    v('list-star', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '* ' + l), '`* ` list item (CommonMark bullet)'),
    v('list-plus', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '+ ' + l), '`+ ` list item'),
    v('list-ordered', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '1. ' + l), '`1. ` ordered item'),
    v('list-nested', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '  - ' + l), 'nested `  - ` item'),
    v('list-dash-2sp', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '-  ' + l), '`-  ` two spaces after dash'),
    v('blockquote', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: '> ' + l), '`> ` blockquote'),
    v('trailing-anchor-comment', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: l + ' <!-- r29 -->'), 'inline HTML comment at line end'),
    v('verdict-capital', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: l.replace('verdict: corrected', 'verdict: Corrected')), 'capitalised verdict'),
    v('path-range', 'O05', lambda: sub_line('SKILL.md', '[R29-OWED-O05]', lambda l: re.sub(r'\| basis: .*$', '| basis: corpus/knowledge/memory-pressure-r25.md:387-390', l)), 'path:START-END range'),
    v('path-dot-slash', 'O05', lambda: sub_line('SKILL.md', '[R29-OWED-O05]', lambda l: re.sub(r'\| basis: .*$', '| basis: ./corpus/knowledge/memory-pressure-r25.md:387', l)), '`./` path prefix'),
    v('path-shifted-by-round-insert', 'O05', v_skill_shift, 'unchanged base line of SKILL.md cited at its tip line number'),
    v('path-appended-this-round', 'O10', v_append_and_cite, 'round appends an evidence line to the cited file and cites it'),
    v('cited-file-append-only', 'O09-O12', v_append_keeps_old, 'round appends to the cited file; old cites unchanged'),
    v('cited-file-insert-above', 'O09-O12', v_insert_above, 'one note inserted above the cited lines'),
    v('path-this-round-capture', 'O07', v_capture_this_round, 'cite bytes fetched and committed this round (path only)'),
    v('json-round-key', 'O09', lambda: json_edit(SH, 'O09', lambda c: {**c, 'round': 29}), 'JSON marker with a `round` key'),
    v('json-date-key', 'O09', lambda: json_edit(SH, 'O09', lambda c: {**c, 'marked_at': '2026-10-22'}), 'JSON marker with a date key'),
    v('json-r27-shape-keys', 'O09', lambda: json_edit(SH, 'O09', lambda c: {**c, 'marked_by': 'ScribeMarkersStorage', 'status': 'corrected'}), 'JSON marker also carrying the corrections_r27 keys'),
    v('json-crossref-in-now', 'O06', lambda: json_edit(MPJ, 'O07', lambda c: {**c, 'now': c['now'] + ' See also R29-OWED-O06 for the action field.'}), 'O07 `now` mentions R29-OWED-O06'),
    v('md-crossref-midline', 'O02', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: l.replace('| basis:', 'See R29-OWED-O02 below. | basis:')), 'O01 now mentions R29-OWED-O02 mid-line'),
    v('now-numbers-units', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: re.sub(r'\| now: .*? \| basis:', f'| now: {NUM_NOW} | basis:', l)), '`now` with numbers and units'),
    v('now-units-glued', 'O01', lambda: sub_line(OOM, '[R29-OWED-O01]', lambda l: re.sub(r'\| now: .*? \| basis:', '| now: ' + NUM_NOW.replace(' GiB', 'GiB').replace(' %', '%') + ' | basis:', l)), 'same `now`, units glued to numbers'),
    v('now-shared-mechanism', 'O04', lambda: sub_line(KILL, '[R29-OWED-O04]', lambda l: re.sub(r'\| now: .*? \| basis:', '| now: ' + re.search(r'\| now: (.*?) \| basis:', [x for x in rd(OOM).split('\n') if x.startswith('[R29-OWED-O02]')][0]).group(1) + ' | basis:', l)), 'O04 reuses the O02 correction (same anchor wording, same mechanism)'),
    v('sources-opened-next-day', 'O01-O04', lambda: wr('corpus/SOURCES.md', re.sub(r'^(\| S14[89] \|.*?\| mined \| )2026-10-22', r'\g<1>2026-10-23', rd('corpus/SOURCES.md'), flags=re.M)), 'S148/S149 opened after UTC midnight'),
    v('sources-opened-annotated', 'O01-O04', lambda: wr('corpus/SOURCES.md', re.sub(r'^(\| S14[89] \|.*?\| mined \| )2026-10-22', r'\g<1>2026-10-22 (r29)', rd('corpus/SOURCES.md'), flags=re.M)), 'opened cell `2026-10-22 (r29)`'),
]


def run_counter(rev):
    p = subprocess.run([sys.executable, COUNTER, '--revision', rev, '--lane', REPO], capture_output=True, env=ENV, text=True)
    rows = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
    return p.returncode, rows


def main():
    git('checkout', '-q', '--detach', TIP)
    git('reset', '-q', '--hard', TIP)
    base_rc, base_rows = run_counter(TIP)
    out = {'tip': {'rc': base_rc, 'marked': base_rows[-1]['marked']}, 'variants': []}
    for var in VARIANTS:
        git('reset', '-q', '--hard', TIP)
        detail = var['apply']()
        git('commit', '-qam', f'variant {var["name"]}')
        rev = git('rev-parse', 'HEAD').strip()
        rc, rows = run_counter(rev)
        fails = {r['id']: r.get('why') for r in rows[:-1] if not r['ok']}
        out['variants'].append(dict(name=var['name'], target=var['target'], note=var['note'], detail=detail,
                                    rev=rev, rc=rc, marked=rows[-1]['marked'], refused=fails))
    git('reset', '-q', '--hard', TIP)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
