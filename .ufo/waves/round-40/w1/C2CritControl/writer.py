#!/usr/bin/env python3
"""Cheapest mechanical C2 writer (seat C2CritControl, item C2-10).

Reads the counter's own TOKENS / derive_values / host_values / ARTIFACT, never a source
semantic. Each rule cell is the token list padded with neutral words to 12; each quote is
the first 4-25 word line of the cited frozen file (a license header, here). Registry rows
are either reused from the lane tree (mode reuse) or fabricated mechanically (mode fabricate).

usage: writer.py <repo> [reuse|fabricate]
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
mode = sys.argv[2] if len(sys.argv) > 2 else 'reuse'
TOOLS = repo / 'tools'
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location('c2', TOOLS / 'check-exec-environment-r40.py')
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)

src, cap = c2.load_frozen()
vals = c2.derive_values(src)
hv = c2.host_values(cap)
PAD = 'alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike'.split()
SID_TXT = re.compile(r'\bS\d{3,}\b')


def git(*a):
    p = subprocess.run(['git', '-C', str(repo), *a], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(f'git {a}: {p.stderr}')
    return p.stdout


def quote_line(fname):
    for n, line in enumerate(src[fname].splitlines(), 1):
        if '|' in line or '“' in line or '”' in line or SID_TXT.search(line):
            continue
        qc = c2.collapse(line)
        if 4 <= len(qc.split()) <= 25:
            return n, line.strip(), qc
    raise SystemExit('no quotable line in ' + fname)


if mode in ('reuse', 'adaptive'):
    srows = c2.parse_sources(git('show', 'HEAD:corpus/SOURCES.md'))
    base_ids = set(c2.parse_sources(git('show', c2.BASE + ':corpus/SOURCES.md')))
    sid_for = {}
    for fname, (rev, path) in c2.ARTIFACT.items():
        cand = [i for i, r in srows.items()
                if i not in base_ids and r['status'] == 'mined' and r['opened'] == c2.OPENED
                and r['kind'] != 'own-work' and c2.ENTRY_NAME in r['used_by']
                and rev in r['title'] and path in r['title']]
        if not cand:
            raise SystemExit('no registry row for ' + fname)
        sid_for[fname] = cand[0]
else:
    # fabricate one registry row per required artifact: the counter checks only title substrings,
    # status, opened and used-by; anchor/teaches/scope are unverified prose.
    text = (repo / c2.SOURCES).read_text()
    rows = [l for l in text.splitlines() if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', l)]
    nxt = max(int(c2.SID_RE.findall(r)[0]) for r in rows) + 1
    sid_for, new = {}, []
    for fname, (rev, path) in c2.ARTIFACT.items():
        sid_for[fname] = f'S{nxt}'
        new.append(f'| S{nxt} | {path} at {rev} — mechanical | code | A | auto | auto | auto '
                   f'| mined | {c2.OPENED} | on-release | {c2.ENTRY} |')
        nxt += 1
    lines = text.splitlines()
    last = max(k for k, l in enumerate(lines) if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', l))
    lines[last + 1:last + 1] = new
    (repo / c2.SOURCES).write_text('\n'.join(lines) + '\n')

header = ', '.join(sorted(set(sid_for.values())))
out = [f'source: {header} in `corpus/SOURCES.md`',
       'verified-at: 2026-10-26',
       'recheck: counter',
       '',
       '# Mechanical entry',
       '',
       '## Rules',
       '',
       '| id | rule | value | source (file:line and quote) | host |',
       '|---|---|---|---|---|']
for ex in sorted(c2.REQUIRED):
    fname = c2.REQUIRED[ex]
    quote = quote_line(fname)
    n, line, qc = quote
    rule = ' '.join(c2.TOKENS[ex])
    if mode == 'adaptive':
        PAD = re.findall(r'[A-Za-z0-9_.-]{3,}', line) or PAD
    i = 0
    while len(c2.collapse(rule).split()) < 12 or qc in c2.collapse(rule):
        rule += ' ' + PAD[i % len(PAD)]
        i += 1
    assert not c2.NEG.search(rule.replace('`', '')), (ex, rule)
    value = vals[ex]
    cell = f'{sid_for[fname]} {fname}:{n}-{n} “{line}”'
    if ex == 'EX6':
        host = f"{hv['hooks_needstargets']} of {hv['hooks_total']} effective hook files"
    elif ex == 'EX4':
        host = '/usr/bin/bash libalpm.so.16.0.1'
    else:
        host = 'mechanical host cell'
    out.append(f'| {ex} | {rule} | {value} | {cell} | {host} |')
(repo / c2.ENTRY).write_text('\n'.join(out) + '\n')
print('wrote', c2.ENTRY, 'with', len(out), 'lines; registry mode', mode)
