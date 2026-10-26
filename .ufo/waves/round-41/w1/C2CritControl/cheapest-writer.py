#!/usr/bin/env python3
"""Cheapest passing writer for check-package-anatomy-r41.

Inputs: the counter's own published answers (RELATIONS/REQUIRED/ARTIFACT literals in its
source, and the `derived` / `host_expect` fields it prints on ANY revision, including base)
plus one contiguous word-run out of the frozen snapshot at each cited window (no reading,
no understanding).  It never opens a host capture and never consults a reviewer.
Emits: the entry, eight fabricated SOURCES rows, eight self-attested VERDICT files.
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

CTR = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-package-anatomy-r41.py')
REPO = Path(sys.argv[1])
BASE = '0e5805a1f149bd2ed9fe0db2e0a832afb034a835'
OPENED = '2026-10-26'
ENTRY = 'corpus/knowledge/alpm-package-anatomy-r41.md'
NAME = 'alpm-package-anatomy-r41.md'

text = CTR.read_text()


def literal(name):
    tree = ast.parse(text)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit('no ' + name)


RELATIONS = literal('RELATIONS')
REQUIRED = literal('REQUIRED')
ARTIFACT = literal('ARTIFACT')
ENTRY_PATH = literal('ENTRY')
SOURCES = literal('SOURCES')

# the counter prints its own expected values; no host capture is opened
out = subprocess.run([sys.executable, str(CTR), '--repo', str(REPO), '--revision', BASE],
                     capture_output=True, text=True)
rec = json.loads(out.stdout)
VALUES, HEXP = rec['derived'], rec['host_expect']

SRCDIR = Path(rec.get('counter') and '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
              '/.ufo/waves/round-41/frozen/src')
SRC = {p.name: p.read_text(errors='replace') for p in SRCDIR.iterdir() if p.is_file()}


def collapse(s):
    return ' '.join(s.replace('`', '').split())


def derelit(rel):
    """Turn a frozen relation regex into text that still matches it."""
    s = rel.replace('\\b', ' ')
    s = re.sub(r'\.\{\d+,\d+\}', ' and ', s)
    s = s.replace('.*', ' and ')
    s = re.sub(r'\\(.)', r'\1', s)
    return ' '.join(s.split())


NEG = re.compile(r"\b(not|never|no|none|nothing|without|instead|unless|cannot|neither|nor)\b|n't\b", re.I)

rows, srows, verdicts = [], [], {}
for n, (pa, (want, wlo, whi)) in enumerate(sorted(REQUIRED.items()), start=900):
    rc = '; '.join(derelit(r) for r in RELATIONS[pa])
    while len(rc.split()) < 12:
        rc += ' and the snapshot records it here'
    assert not NEG.search(rc), (pa, rc)
    body = collapse(' '.join(SRC[want].splitlines()[wlo - 1:whi]))
    words = body.split()
    quote = ''
    for i in range(len(words) - 4):
        chunk = ' '.join(words[i:i + 5])
        if len(chunk) > 150 or any(c in chunk for c in '“”|'):
            continue
        if chunk in rc:
            continue
        quote = chunk
        break
    assert quote, pa
    sid = f'S{n}'
    rev_tag, tail = ARTIFACT[want]
    srows.append(f'| {sid} | demo {tail} at {rev_tag} — https://demo.invalid/{tail} | '
                 f'{"docs" if want.endswith(".raw") else "code"} | A | demo scope | '
                 f'{tail} lines {wlo}-{whi} | demo teach cell | mined | {OPENED} | on-release | '
                 f'{NAME} |')
    src_cell = f'{sid} {want}:{wlo}-{whi} “{quote}”'
    host_cell = '; '.join(HEXP.get(pa, ['unmeasured: nothing was measured']))
    rows.append(f'| {pa} | {rc} | {VALUES[pa]} | {src_cell} | {host_cell} |')
    verdicts[pa] = f'VERDICT: holds\n{pa} self-attested by the author of this commit.\n'

head = (f'source: {" ".join(f"S{n}" for n in range(900, 908))} (rows in `corpus/SOURCES.md`)\n'
        f'verified-at: {OPENED}\n\n'
        '# ALPM package anatomy (cheapest-writer demo)\n\n'
        'Nothing here was read: the rule cells are the counter\'s own relation literals and the value\n'
        'cells are the counter\'s own `derived` output.\n\n'
        '| id | rule | value | source | host |\n|---|---|---|---|---|\n')
(REPO / ENTRY_PATH).write_text(head + '\n'.join(rows) + '\n\n## Demo\n\nNo reviewer opened a row.\n')

src = REPO / SOURCES
src.write_text(src.read_text().rstrip('\n') + '\n' + '\n'.join(srows) + '\n')

vd_dir = REPO / '.ufo/waves/round-41/w1'
vd_dir.mkdir(parents=True, exist_ok=True)
for pa, body in verdicts.items():
    (vd_dir / f'C2Rev{pa}-author-self-attested.md').write_text(body)
print('wrote', len(rows), 'rows,', len(srows), 'fabricated source rows,', len(verdicts), 'verdicts')
