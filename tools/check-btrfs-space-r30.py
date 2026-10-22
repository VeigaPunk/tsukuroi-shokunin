#!/usr/bin/env python3
"""Counter for round 30, claim C1 (axis depth): sourced btrfs space-allocation rows D01-D10.

The claim: the lane gains new, sourced host-operability knowledge on btrfs space allocation
and ENOSPC (a surface the lane had not covered: `Global reserve`, `unallocated` and the
allocation sysfs files read 0 hits in `SKILL.md`, `corpus/knowledge/` and `corpus/SOURCES.md`
at the round-30 base `fbfec6bd`). Ten FROZEN questions D01-D10, each answered by one row.

A row Dnn is VERIFIED at a revision when every rule holds:
 R1 `corpus/knowledge/btrfs-space-r30.json` parses with no duplicate key anywhere, its top
    level is an object with a `rows` list, and exactly one row has `"id": "Dnn"`.
 R2 the row's keys are exactly the required set (source rows: id, statement, source, snapshot,
    line, quote; host rows add capture, capture_line, value); no other key.
 R3 `statement` has at least 12 whitespace-separated words.
 R4 `source` names an `S###` row of `corpus/SOURCES.md` that is absent from the base's
    registry, whose status cell is exactly `mined`, whose opened cell is `2026-10-22`, and whose
    row text contains the sha256 of the `snapshot` file.
 R5 `snapshot` is a file under `.ufo/waves/round-30/` present at the revision.
 R6 `quote` has at least 20 characters after whitespace normalisation and occurs, after HTML
    tags are removed, entities unescaped and whitespace collapsed, in the snapshot text that
    starts at line `line` (1-based) and spans at most that line and the next two lines, and it
    starts within line `line`; the (snapshot, line) pair is used by no earlier row.
 R7 the quote contains (case-insensitively) at least one of the row's FROZEN tokens.
 R8 host rows: `capture` is a file under `.ufo/waves/round-30/` present at the revision whose
    line `capture_line` contains `value` verbatim; `value` is a decimal integer of at least one
    digit; `statement` contains `value` verbatim.
 R9 `SKILL.md` has exactly one line, outside fenced code blocks and HTML comments (including
    the empty comment `<!-->`), that starts with the exact bytes `| [R30-Dnn] `; that line
    names `source` as a whole word, and for host rows it contains `value`. Any other line that
    contains `R30-Dnn` anywhere in `SKILL.md` makes the row unverified (one marker per row).

Usage:
  python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]
  python3 tools/check-btrfs-space-r30.py --tree <DIR> --base-sources <FILE>   (fixture mode)
Output: one JSON line per row (`id`, `verified`, `failures`), then a summary JSON line with
`revision`, `verified` (count), `unverified` (ids), `counter_sha256`.  Exit 0 when all ten
rows verify, 1 otherwise, 2 when the revision cannot be read.
"""
import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys

BASE = 'fbfec6bdf8833e7513732a06000801a8ee9b690b'
JSON_PATH = 'corpus/knowledge/btrfs-space-r30.json'
EVIDENCE_PREFIX = '.ufo/waves/round-30/'
OPENED = '2026-10-22'
SOURCE_KEYS = {'id', 'statement', 'source', 'snapshot', 'line', 'quote'}
HOST_KEYS = SOURCE_KEYS | {'capture', 'capture_line', 'value'}
# FROZEN questions: id -> (kind, tokens; the quote must contain one, case-insensitively)
ROWS = {
    'D01': ('source', ('unallocated',)),          # unallocated space vs chunk allocation; ENOSPC with free data space
    'D02': ('source', ('global reserve', 'global_rsv')),   # what the global block reserve is
    'D03': ('source', ('usage',)),                # balance usage filters return partly used chunks
    'D04': ('source', ('dup',)),                  # metadata DUP profile on a single device
    'D05': ('source', ('reclaim',)),              # automatic block-group reclaim (bg_reclaim_threshold)
    'D06': ('source', ('allocation',)),           # the per-filesystem allocation sysfs directory
    'D07': ('source', ('snapshot',)),             # snapshots keep shared extents allocated
    'D08': ('host', ('metadata',)),               # host metadata used vs total at capture
    'D09': ('host', ('data', 'unallocated')),     # host data / unallocated at capture
    'D10': ('host', ('global_rsv', 'global reserve')),     # host global reserve size at capture
}


def git_reader(lane, rev):
    def read(path):
        p = subprocess.run(['git', '-C', lane, 'show', f'{rev}:{path}'], capture_output=True,
                           env={k: v for k, v in os.environ.items() if not k.startswith('GIT_')})
        return p.stdout if p.returncode == 0 else None
    return read


def tree_reader(root):
    def read(path):
        full = os.path.normpath(os.path.join(root, path))
        if not full.startswith(os.path.normpath(root) + os.sep) or not os.path.isfile(full):
            return None
        with open(full, 'rb') as fh:
            return fh.read()
    return read


def norm(s):
    return ' '.join(s.split())


def strip_markup(s):
    return norm(html.unescape(re.sub(r'<[^>]*>', ' ', s)))


def registry_rows(text):
    rows = {}
    for line in text.splitlines():
        m = re.match(r'^\| (S\d{3}) \|', line)
        if m:
            rows.setdefault(m.group(1), []).append(line)
    return rows


def split_cells(line):
    cells = re.split(r'(?<!\\)\|', line.strip())
    return [c.strip() for c in cells[1:-1]]


def comment_state(line, in_comment):
    """Return whether an HTML comment is still open at the end of `line`."""
    pos = 0
    while True:
        if in_comment:
            close = line.find('-->', pos)
            if close < 0:
                return True
            in_comment, pos = False, close + 3
            continue
        idx = line.find('<!--', pos)
        if idx < 0:
            return False
        after = idx + 4
        if line.startswith('>', after):          # `<!-->` is an empty comment
            pos = after + 1
        elif line.startswith('->', after):       # `<!--->` is an empty comment
            pos = after + 2
        else:
            in_comment, pos = True, after


def visible_lines(text):
    """Yield (lineno, line) of SKILL.md lines outside fenced code and HTML comments.

    A line that opens, closes or contains any comment is itself not visible; a fence closes
    only on a line holding the opening character repeated at least the opening length."""
    fence, in_comment = None, False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if fence:
            if re.fullmatch(re.escape(fence[0]) + '{%d,}' % len(fence), s):
                fence = None
            continue
        if in_comment or '<!--' in line:
            in_comment = comment_state(line, in_comment)
            continue
        m = re.match(r'(`{3,}|~{3,})', s)
        if m:
            fence = m.group(1)
            continue
        yield n, line


def no_dup_hook(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError('duplicate key: ' + ','.join(sorted(k for k in set(keys) if keys.count(k) > 1)))
    return dict(pairs)


def measure(read, base_sources):
    out = {rid: [] for rid in ROWS}
    raw = read(JSON_PATH)
    rows = None
    if raw is None:
        for rid in ROWS:
            out[rid].append('R1 json missing')
        return out
    try:
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=no_dup_hook)
        rows = doc.get('rows') if isinstance(doc, dict) else None
        if not isinstance(rows, list):
            raise ValueError('rows is not a list')
    except (ValueError, UnicodeDecodeError) as e:
        for rid in ROWS:
            out[rid].append('R1 json invalid: %s' % e)
        return out
    sources_raw = read('corpus/SOURCES.md')
    reg = registry_rows(sources_raw.decode('utf-8', 'replace')) if sources_raw else {}
    base_reg = registry_rows(base_sources)
    skill_raw = read('SKILL.md')
    skill = skill_raw.decode('utf-8', 'replace') if skill_raw else ''
    vis = list(visible_lines(skill))
    used_lines = set()
    for rid, (kind, tokens) in ROWS.items():
        f = out[rid]
        mine = [r for r in rows if isinstance(r, dict) and r.get('id') == rid]
        if len(mine) != 1:
            f.append('R1 %d rows with id %s' % (len(mine), rid))
            continue
        r = mine[0]
        want = HOST_KEYS if kind == 'host' else SOURCE_KEYS
        if set(r) != want:
            f.append('R2 keys %s != %s' % (sorted(r), sorted(want)))
            continue
        if not all(isinstance(r[k], str) for k in want if k not in ('line', 'capture_line')) or \
                not all(type(r[k]) is int for k in want if k in ('line', 'capture_line')):
            f.append('R2 value types')
            continue
        if len(r['statement'].split()) < 12:
            f.append('R3 statement under 12 words')
        sid = r['source']
        snap_ok = r['snapshot'].startswith(EVIDENCE_PREFIX) and '..' not in r['snapshot'].split('/')
        snap = read(r['snapshot']) if snap_ok else None
        if snap is None:
            f.append('R5 snapshot missing or outside %s' % EVIDENCE_PREFIX)
        if not re.fullmatch(r'S\d{3}', sid) or sid not in reg:
            f.append('R4 source row missing')
        elif len(reg[sid]) != 1 or sid in base_reg:
            f.append('R4 source row duplicated or present at base')
        else:
            cells = split_cells(reg[sid][0])
            if len(cells) != 11:
                f.append('R4 source row has %d cells' % len(cells))
            elif cells[7] != 'mined' or cells[8] != OPENED:
                f.append('R4 source status/opened %r/%r' % (cells[7], cells[8]))
            elif snap is not None and hashlib.sha256(snap).hexdigest() not in reg[sid][0]:
                f.append('R4 snapshot sha256 not in source row')
        if snap is not None:
            lines = snap.decode('utf-8', 'replace').splitlines()
            ln, q = r['line'], norm(r['quote'])
            if len(q) < 20:
                f.append('R6 quote under 20 characters')
            elif not (1 <= ln <= len(lines)):
                f.append('R6 line out of range')
            else:
                first = strip_markup(lines[ln - 1])
                window = strip_markup(' '.join(lines[ln - 1:ln + 2]))
                pos = window.find(q)
                if pos < 0 or pos >= max(len(first), 1):
                    f.append('R6 quote not at the cited line')
                elif (r['snapshot'], ln) in used_lines:
                    f.append('R6 cited line reused')
                used_lines.add((r['snapshot'], ln))
            if not any(t in q.lower() for t in tokens):
                f.append('R7 quote lacks frozen token %s' % '|'.join(tokens))
        if kind == 'host':
            v = r['value']
            cap_ok = r['capture'].startswith(EVIDENCE_PREFIX) and '..' not in r['capture'].split('/')
            cap = read(r['capture']) if cap_ok else None
            if not re.fullmatch(r'\d+', v):
                f.append('R8 value not a decimal integer')
            elif cap is None:
                f.append('R8 capture missing or outside %s' % EVIDENCE_PREFIX)
            else:
                cl = cap.decode('utf-8', 'replace').splitlines()
                if not (1 <= r['capture_line'] <= len(cl)) or \
                        not re.search(r'(?<!\d)%s(?!\d)' % re.escape(v), cl[r['capture_line'] - 1]):
                    f.append('R8 value not on capture line')
                if v not in r['statement']:
                    f.append('R8 statement lacks value')
        marker = '| [R30-%s] ' % rid
        hits = [line for _n, line in vis if line.startswith(marker)]
        any_mention = sum(1 for line in skill.splitlines() if 'R30-' + rid in line)
        if len(hits) != 1 or any_mention != 1:
            f.append('R9 %d marker lines, %d mentions' % (len(hits), any_mention))
        else:
            if not re.search(r'(?<![A-Za-z0-9])%s(?![0-9])' % re.escape(sid), hits[0]):
                f.append('R9 marker line lacks source id')
            if kind == 'host' and not re.search(r'(?<!\d)%s(?!\d)' % re.escape(r['value']), hits[0]):
                f.append('R9 marker line lacks host value')
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--revision')
    g.add_argument('--tree')
    ap.add_argument('--base-sources')
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    if a.revision:
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        p = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', a.revision + '^{commit}'],
                           capture_output=True, text=True, env=env)
        if p.returncode != 0:
            print(json.dumps({'error': 'revision unreadable', 'revision': a.revision}))
            return 2
        rev = p.stdout.strip()
        read = git_reader(a.lane, rev)
        base = git_reader(a.lane, BASE)('corpus/SOURCES.md')
        if base is None:
            print(json.dumps({'error': 'base registry unreadable', 'base': BASE}))
            return 2
        base_sources = base.decode('utf-8', 'replace')
    else:
        if not a.base_sources:
            ap.error('--tree needs --base-sources')
        rev = 'tree:' + os.path.abspath(a.tree)
        read = tree_reader(os.path.abspath(a.tree))
        with open(a.base_sources, encoding='utf-8') as fh:
            base_sources = fh.read()
    out = measure(read, base_sources)
    for rid, fails in out.items():
        print(json.dumps({'id': rid, 'verified': not fails, 'failures': fails}))
    with open(os.path.abspath(__file__), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    bad = [rid for rid, fails in out.items() if fails]
    print(json.dumps({'revision': rev, 'verified': len(ROWS) - len(bad), 'of': len(ROWS),
                      'unverified': bad, 'counter_sha256': sha}))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
