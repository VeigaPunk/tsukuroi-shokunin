#!/usr/bin/env python3
"""Independent C1 re-derivation (RerunC1 seat). Reads only `git show REV:<path>` and `git ls-tree`.

Rules applied, from SCORECARD.md "Round 26 — declaration, attempt 1", the C1 row rule:
entry ids, row fields, sources, quotes (length, snapshot substring, anchor digest, Gate row),
capture pointers (pinned digest, line range, header/echo/exit, uniqueness, token), SKILL first cells.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = sys.argv[1] if len(sys.argv) > 1 else '7dfea9244a84a0e2439f0698e54491e5d7b7c467'
ENTRY_JSON = 'corpus/knowledge/storage-health-r26.json'
ENTRY_USED = 'corpus/knowledge/storage-health-r26.md'
SOURCES_MD = 'corpus/SOURCES.md'
LESSON = 'corpus/lessons/round-26.md'
SKILL_MD = 'SKILL.md'
CAPTURE = '.ufo/waves/round-26/capture/capture.txt'
CAPTURE_SHA = '002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd'
SNAP_DIR = '.ufo/waves/round-26/sources'
IDS = ['SH1', 'SH2', 'SH3', 'SH4', 'SH5', 'SH6']
VERDICTS = {'HEALTHY', 'DEGRADED', 'BLOCKED', 'UNVERIFIED'}
DATE = '2026-10-22'
SECTION = '## Storage integrity — round 26'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ENV.update(GIT_OPTIONAL_LOCKS='0', GIT_PAGER='cat', LC_ALL='C',
           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)


def git(*args):
    p = subprocess.run(['git', '--no-pager', '-C', LANE, *args], stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV, timeout=120)
    if p.returncode:
        raise SystemExit('could not evaluate: git %s failed: %s'
                         % (args[0], p.stderr.decode(errors='replace').strip()[:160]))
    return p.stdout


def show(path):
    return git('show', '%s:%s' % (REV, path))


def norm(s):
    return ' '.join(s.split())


def cells(line):
    s = line.strip()
    s = s[1:] if s.startswith('|') else s
    s = s[:-1] if s.endswith('|') and not s.endswith('\\|') else s
    return [c.strip() for c in re.split(r'(?<!\\)\|', s)]


def no_dup(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('duplicate key %r' % k)
        d[k] = v
    return d


entry = json.loads(show(ENTRY_JSON).decode('utf-8'), object_pairs_hook=no_dup)
rows = entry['rows']
entry_fail = []
if Counter(r.get('id') for r in rows) != Counter(IDS):
    entry_fail.append('ids-not-exactly-SH1-to-SH6-each-once')

src, hdr = {}, None
for ln in show(SOURCES_MD).decode('utf-8').split('\n'):
    if hdr is None and ln.startswith('| id | source |'):
        hdr = cells(ln)
    elif hdr and re.match(r'\| S\d{3} \|', ln):
        rec = dict(zip(hdr, cells(ln)))
        if rec['id'] in src:
            entry_fail.append('source-row-duplicated:' + rec['id'])
        src[rec['id']] = rec

snap_files = git('ls-tree', '-r', '--name-only', REV, '--', SNAP_DIR).decode().splitlines()

lesson = show(LESSON).decode('utf-8').split('\n')
heads = [i for i, l in enumerate(lesson) if l.strip() == '## Gate']
if len(heads) != 1:
    entry_fail.append('gate-heading-count=%d' % len(heads))
gi = heads[0]
ge = next((j for j in range(gi + 1, len(lesson)) if lesson[j].startswith('## ')), len(lesson))
gate = []
for l in lesson[gi + 1:ge]:
    c = cells(l) if l.lstrip().startswith('|') else []
    if len(c) == 5 and re.fullmatch(r'S\d{3}', c[0]):
        raw = c[3]
        inner = raw[1:-1] if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in '"`' else raw
        gate.append((c[0], norm(inner)))

cap = show(CAPTURE)
if hashlib.sha256(cap).hexdigest() != CAPTURE_SHA:
    entry_fail.append('capture-digest-mismatch')
cap_lines = cap.decode('utf-8').split('\n')


def pointer_ok(p):
    line, tok = p.get('line'), p.get('token')
    if type(line) is not int or not isinstance(tok, str) or len(tok) < 3:
        return False
    if not 1 <= line <= len(cap_lines):
        return False
    text = cap_lines[line - 1]
    if text.startswith('### ') or text.startswith('$ ') or text.startswith('[exit '):
        return False
    return tok in text and cap_lines.count(text) == 1


skill = show(SKILL_MD).decode('utf-8').split('\n')
sec = [i for i, l in enumerate(skill) if l.rstrip() == SECTION]
if len(sec) != 1:
    entry_fail.append('skill-section-heading-count=%d' % len(sec))
si = sec[0]
se = next((j for j in range(si + 1, len(skill)) if skill[j].startswith('## ')), len(skill))
skill_first = Counter(cells(l)[0] for l in skill[si + 1:se] if l.lstrip().startswith('|'))


def check(r):
    fails, strict = [], []
    if not str(r.get('statement', '')).strip():
        fails.append('statement-empty')
    if r.get('verdict') not in VERDICTS:
        fails.append('verdict-invalid')
    if not str(r.get('action', '')).strip():
        fails.append('action-empty')
    quotes = r.get('quotes') or []
    cited = set(r.get('sources') or []) | {q.get('source') for q in quotes}
    if not any(src.get(s, {}).get('tier') == 'A' for s in cited):
        fails.append('no-tier-A-source')
    for s in sorted(cited, key=str):
        rec = src.get(s)
        if rec is None:
            fails.append('unknown-source:%s' % s)
        elif rec['status'] != 'mined' or rec['opened'] != DATE or ENTRY_USED not in rec['used-by']:
            fails.append('source-row-fails:%s' % s)
    if not quotes:
        fails.append('no-quotes')
    for q in quotes:
        t, s = q.get('text') or '', q.get('source')
        names = [p for p in snap_files if re.fullmatch(re.escape(SNAP_DIR) + '/' + str(s) + r'\.[^/]+', p)]
        if not t.strip() or len(t.split()) > 25 or len(names) != 1:
            fails.append('quote-length-or-snapshot-count:%s' % s)
            continue
        body = show(names[0])
        if hashlib.sha256(body).hexdigest() not in re.findall(r'[0-9a-f]{64}', src.get(s, {}).get('anchor', '')):
            fails.append('snapshot-digest-not-in-anchor:%s' % s)
        if norm(t) not in norm(body.decode('utf-8')):
            fails.append('quote-not-substring:%s' % s)
        if (s, norm(t)) not in gate:
            fails.append('gate-quote-missing:%s' % s)
    ptrs = r.get('capture_pointers') or []
    if not any(pointer_ok(p) for p in ptrs):
        fails.append('no-valid-capture-pointer')
    strict = [pointer_ok(p) for p in ptrs]
    if not skill_first.get(r.get('id')):
        fails.append('skill-first-cell-missing')
    return fails, strict


results = {r.get('id'): check(r) for r in rows}
verified = [k for k, (f, _) in results.items() if not f]
print('revision', REV)
print('entry-level failures:', entry_fail or 'none')
for k in IDS:
    f, strict = results.get(k, (['row-missing'], []))
    print(k, 'PASS' if not f else 'FAIL %s' % f, 'pointers=%d all-valid=%s' % (len(strict), all(strict)))
count = 0 if entry_fail else len(verified)
print('verified_rows =', count, 'of', len(IDS), verified if not entry_fail else '(entry-level failure: 0)')
