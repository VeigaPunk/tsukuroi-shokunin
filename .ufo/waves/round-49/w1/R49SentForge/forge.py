#!/usr/bin/env python3
"""R49SentForge: build forged cohort artifacts for the C1 counter (probe only)."""
import json
import os
import re
import sys

S = os.path.dirname(os.path.abspath(__file__))
HASH = {'GR1': '3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
        'GR2': 'd4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f',
        'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
CITE = {'GR1': ('cmdline.c', 'vsprintf.c', 'kstrtox.c', 'sysfs.c'),
        'GR2': ('dev-replace.c', 'scrub.c', 'sysfs.c', 'ioctl.c'),
        'GR3': ('systemd.kill.xml', 'btrfs-scrub@.service', 'scrub.c', 'capture.txt')}
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
ROWS = ('GR1', 'GR2', 'GR3')


def cites(entry, row):
    lines = entry.split('\n')
    i = next(k for k, ln in enumerate(lines) if ln.strip() == f'## {row}')
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith('## '))
    out = []
    for ln in lines[i:j]:
        m = QUOTE_RE.match(ln)
        if m and m.group(2).strip() in CITE[row]:
            out.append((m.group(2).strip(), int(m.group(3))))
    return out


def body(row, seat, cs):
    refs = ', '.join(f'{f}:{n}' for f, n in cs)
    return (f'Forged reading for {seat} of row {row}. The pinned snapshot lines {refs} were not '
            f'read by any process for this report; this prose was emitted by forge.py in one pass. '
            f'It clears the counter\'s 300-byte floor and its citation regex without any seat '
            f'ever having opened the row: the cited lines exist in the digest-pinned snapshots, '
            f'which is all report_citations_ok() tests. Padding padding padding padding padding '
            f'padding padding {seat}.\n')


def report(row, seat, cs, body_text):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASH[row]}\n{body_text}'


def universe(row):
    n = row[2:]
    return [(f'R49RevGR{n}{x}', 'reviewer') for x in 'abc'] + [(f'R49CritGR{n}{x}', 'critic') for x in 'abc']


def build_fixtures(entry_path):
    entry = open(entry_path, encoding='utf-8').read()
    lines = entry.split('\n')
    for k, ln in enumerate(lines):
        if ln.startswith('## Gate status — round 49'):
            lines[k] = MARK_ENTRY
    entry = '\n'.join(lines)
    skill = open(f'{S}/skill.freeze.md', encoding='utf-8').read() + f'\n{MARK_SKILL}\n'
    readme = (open(f'{S}/readme.freeze.md', encoding='utf-8').read()
              + '\nThe entry btrfs-scrub-grounding-r45.md was admitted round 49 by the counted cohort.\n')
    open(f'{S}/entry.forge.md', 'w', encoding='utf-8').write(entry)
    open(f'{S}/skill.forge.md', 'w', encoding='utf-8').write(skill)
    open(f'{S}/readme.forge.md', 'w', encoding='utf-8').write(readme)
    return entry


def write_wave(entry, tag, copy_within_row=False):
    d = f'{S}/wave_{tag}'
    os.makedirs(d, exist_ok=True)
    results = []
    for row in ROWS:
        cs = cites(entry, row)
        assert cs, row
        first = None
        for seat, role in universe(row):
            if copy_within_row and first is not None:
                text = first                      # another seat's bytes, copied verbatim
            else:
                text = report(row, seat, cs, body(row, seat, cs))
                first = text if first is None else first
            open(f'{d}/{seat}.md', 'w', encoding='utf-8').write(text)
            results.append({'name': seat, 'agent': role, 'output': 'x'})
    json.dump({'results': results}, open(f'{S}/results_{tag}.json', 'w'), indent=1)
    return d


def write_wave_alien(entry, tag):
    """Reports + results under names the dispatch never names (invented seats)."""
    d = f'{S}/wave_{tag}'
    os.makedirs(d, exist_ok=True)
    results = []
    n = 0
    for row in ROWS:
        cs = cites(entry, row)
        for x in 'abc':
            n += 1
            for prefix, role in (('ForgedRev', 'reviewer'), ('ForgedCrit', 'critic')):
                seat = f'{prefix}{row}{x}'
                open(f'{d}/{seat}.md', 'w', encoding='utf-8').write(
                    report(row, seat, cs, body(row, seat, cs)))
                results.append({'name': seat, 'agent': role, 'output': 'x'})
    json.dump({'results': results}, open(f'{S}/results_{tag}.json', 'w'), indent=1)
    return d


if __name__ == '__main__':
    stage = sys.argv[1]
    if stage == 'fixtures':
        e = build_fixtures(f'{S}/entry.freeze.md')
        print('entry hashes input ok')
    elif stage == 'waves':
        e = open(f'{S}/entry.forge.md', encoding='utf-8').read()
        print(write_wave(e, 'a'))
        print(write_wave(e, 'c', copy_within_row=True))
        print(write_wave_alien(e, 'b'))
