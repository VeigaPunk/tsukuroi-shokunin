#!/usr/bin/env python3
"""Counter for round 30, claim C1 (axis depth): sourced btrfs space-allocation rows D01-D10.

VERSION 2 (round-30 wave-1 repair; the declared version 1 is the bytes at commit
8fb2cef081787ccb52b38e9f74d95d2a480de18f, sha256 1bf7ee14..., and the claim is judged on it).
Wave-1 CritCounterShapes showed version 1 accepted 39 of 49 should-fail shapes and refused 11
legitimate ones; MutCounterC1 found four battery survivors. Version 2 is stricter where those
shapes were mechanical and less strict where version 1 refused verbatim quotes; changes are
marked "v2" below. The ten FROZEN questions and their tokens are unchanged.

The claim: the lane gains new, sourced host-operability knowledge on btrfs space allocation
and ENOSPC (`Global reserve` and `unallocated` read 0 hits in `SKILL.md`, `corpus/knowledge/`
and `corpus/SOURCES.md` at the round-30 base `fbfec6bd`; the allocation directory and the
metadata DUP profile were already named by row SH3 of round 26).

A row Dnn is VERIFIED at a revision when every rule holds:
 R1 `corpus/knowledge/btrfs-space-r30.json` parses with no duplicate key anywhere; its top
    level is an object whose keys are within TOP_KEYS and whose `rows` is a list; v2: every
    element of `rows` is an object whose `id` is exactly one of D01-D10 (otherwise no row
    verifies), and exactly one row has `"id": "Dnn"`.
 R2 the row's keys are exactly the required set (source rows: id, statement, source, snapshot,
    line, quote; host rows add capture, capture_line, value); no other key; `line` and
    `capture_line` are integers, every other value a string.
 R3 `statement` has at least 12 whitespace-separated words.
 R4 `source` names an `S###` row inside the registry table of `corpus/SOURCES.md` (v2: the
    contiguous table under the exact 11-column header; rows in fences, comments or other tables
    do not count), absent from the base's registry table, whose status cell is exactly `mined`,
    whose opened cell is `2026-10-22`, and whose row text contains the sha256 of the `snapshot`.
 R5 `snapshot` is a regular file (v2: not a symlink) under `.ufo/waves/round-30/`, named by a
    normalised path (no `..`, `.` or empty component), present at the revision.
 R6 `quote` has at least 20 characters after whitespace normalisation. v2: lines are split on
    `\\n` only (the `sed` numbering; a trailing `\\r` is dropped); HTML tags are stripped and
    entities unescaped only for `.html`/`.htm` snapshots, every other snapshot is matched
    verbatim after whitespace collapse. The cited line `line` (1-based) is non-blank; the quote
    occurs in the text that starts at that line and spans at most that line and the next two,
    it starts within the cited line, and at least min(20, len(quote)) of its characters lie on
    the cited line. The pair (snapshot sha256, line) is used by no earlier row.
 R7 the quote contains at least one of the row's FROZEN tokens as a whole word
    (case-insensitive; v2: not preceded or followed by a letter or digit).
 R8 host rows: `capture` is a regular file under `.ufo/waves/round-30/` present at the revision
    whose line `capture_line` (split on `\\n`) contains `value` as a whole number and (v2) the
    row's FROZEN capture key; no two host rows share a capture line; `value` is a decimal
    integer; `statement` contains `value` as a whole number.
 R9 `SKILL.md` has exactly one visible line that starts with the exact bytes `| [R30-Dnn] `;
    v2: visible means outside fenced code (a fence opens only with at most three spaces of
    indentation, and a backtick fence's info string has no backtick), outside HTML comments
    (code spans are ignored when scanning for `<!--`), outside raw `<pre>`, `<script>`,
    `<style>` and `<textarea>` blocks, and inside a pipe table block (contiguous lines starting
    with `|`, preceded by a blank line or a heading, whose second line is a delimiter row).
    That line names `source` as a whole word, and for host rows it contains `value`. Any
    other line that contains `R30-Dnn` anywhere in `SKILL.md` makes the row unverified.

Usage:
  python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]
  python3 tools/check-btrfs-space-r30.py --tree <DIR> --base-sources <FILE>   (fixture mode)
Output: one JSON line per row (`id`, `verified`, `failures`), then a summary JSON line with
`revision`, `verified` (count), `unverified` (ids), `counter_sha256`, `counter_version`.
Exit 0 when all ten rows verify, 1 otherwise, 2 when the revision cannot be read.
"""
import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys

VERSION = 2
BASE = 'fbfec6bdf8833e7513732a06000801a8ee9b690b'
JSON_PATH = 'corpus/knowledge/btrfs-space-r30.json'
EVIDENCE_PREFIX = '.ufo/waves/round-30/'
OPENED = '2026-10-22'
SOURCE_KEYS = {'id', 'statement', 'source', 'snapshot', 'line', 'quote'}
HOST_KEYS = SOURCE_KEYS | {'capture', 'capture_line', 'value'}
TOP_KEYS = {'entry', 'round', 'capture', 'capture_utc', 'host', 'counter', 'rows', 'supporting_citations'}
REGISTRY_HEADER = '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |'
# FROZEN questions: id -> (kind, tokens; the quote must contain one as a whole word)
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
# v2: the capture line of a host row must name what it measures
CAPTURE_KEYS = {'D08': 'metadata/bytes_used', 'D09': 'unallocated', 'D10': 'global_rsv_size'}


def clean_env():
    return {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


def git_reader(lane, rev):
    def read(path):
        ls = subprocess.run(['git', '-C', lane, 'ls-tree', rev, '--', path], capture_output=True,
                            text=True, env=clean_env())
        if ls.returncode != 0 or not ls.stdout.startswith(('100644 ', '100755 ')):
            return None                                   # v2: absent, symlink or not a blob
        p = subprocess.run(['git', '-C', lane, 'show', f'{rev}:{path}'], capture_output=True,
                           env=clean_env())
        return p.stdout if p.returncode == 0 else None
    return read


def tree_reader(root):
    def read(path):
        full = os.path.normpath(os.path.join(root, path))
        if not full.startswith(os.path.normpath(root) + os.sep) or not os.path.isfile(full) \
                or os.path.islink(full):
            return None
        with open(full, 'rb') as fh:
            return fh.read()
    return read


def norm(s):
    return ' '.join(s.split())


def snapshot_lines(data, path):
    lines = [l[:-1] if l.endswith('\r') else l for l in data.decode('utf-8', 'replace').split('\n')]
    if path.lower().endswith(('.html', '.htm')):
        return [norm(html.unescape(re.sub(r'<[^>]*>', ' ', l))) for l in lines]
    return [norm(l) for l in lines]


def good_path(p):
    parts = p.split('/')
    return p.startswith(EVIDENCE_PREFIX)


def word_in(token, text):
    return re.search(r'(?<![A-Za-z0-9])%s(?![A-Za-z0-9])' % re.escape(token), text, re.I) is not None


def number_in(value, text):
    return re.search(r'(?<![0-9])%s(?![0-9])' % re.escape(value), text) is not None


def registry_rows(text):
    """S### rows of the contiguous table under the exact registry header (v2)."""
    rows = {}
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip() != REGISTRY_HEADER:
            continue
        j = i + 2
        while j < len(lines) and lines[j].startswith('|'):
            m = re.match(r'^\| (S\d{3}) \|', lines[j])
            if m:
                rows.setdefault(m.group(1), []).append(lines[j])
            j += 1
        break
    return rows


def split_cells(line):
    cells = re.split(r'(?<!\\)\|', line.strip())
    return [c.strip() for c in cells[1:-1]]


def strip_code_spans(line):
    return re.sub(r'(`+)(?:(?!\1).)+?\1', ' ', line)


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


RAW_OPEN = re.compile(r'^ {0,3}<(pre|script|style|textarea)(\s|>|$)', re.I)
DELIM = re.compile(r'^\|(\s*:?-+:?\s*\|)+\s*$')


def visible_table_lines(text):
    """Yield (lineno, line) of SKILL.md lines that are visible rows of a pipe table (v2)."""
    lines = text.split('\n')
    visible = [False] * len(lines)
    fence, in_comment, raw = None, False, None
    for n, line in enumerate(lines):
        s = line.strip()
        if fence:
            if re.fullmatch(re.escape(fence[0]) + '{%d,}' % len(fence), s) and \
                    len(line) - len(line.lstrip(' ')) <= 3:
                fence = None
            continue
        if raw:
            if re.search(r'</%s\s*>' % raw, line, re.I):
                raw = None
            continue
        scan = strip_code_spans(line)
        if in_comment or '<!--' in scan:
            was_open = in_comment
            in_comment = comment_state(scan, in_comment)
            if was_open or in_comment or not line.startswith('|'):
                continue
            # a table row whose inline comments all close on the same line stays visible
            visible[n] = True
            continue
        m = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if m and not (m.group(1)[0] == '`' and '`' in m.group(2)):
            fence = m.group(1)
            continue
        m = RAW_OPEN.match(line)
        if m:
            if not re.search(r'</%s\s*>' % m.group(1), line, re.I):
                raw = m.group(1)
            continue
        visible[n] = True
    n = 0
    while n < len(lines):
        if visible[n] and lines[n].startswith('|'):
            start = n
            while n < len(lines) and visible[n] and lines[n].startswith('|'):
                n += 1
            prev = lines[start - 1].strip() if start > 0 else ''
            ok = (start == 0 or prev == '' or prev.startswith('#')) and \
                n - start >= 2 and DELIM.match(lines[start + 1].strip())
            if ok:
                for k in range(start + 2, n):
                    yield k + 1, lines[k]
        else:
            n += 1


def no_dup_hook(pairs):
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError('duplicate key: ' + ','.join(sorted(k for k in set(keys) if keys.count(k) > 1)))
    return dict(pairs)


def measure(read, base_sources):
    out = {rid: [] for rid in ROWS}
    raw = read(JSON_PATH)
    if raw is None:
        for rid in ROWS:
            out[rid].append('R1 json missing')
        return out
    try:
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=no_dup_hook)
        rows = doc.get('rows') if isinstance(doc, dict) else None
        if not isinstance(rows, list):
            raise ValueError('rows is not a list')
        if set(doc) - TOP_KEYS:
            raise ValueError('top-level keys outside TOP_KEYS: %s' % sorted(set(doc) - TOP_KEYS))
        if not all(isinstance(r, dict) and r.get('id') in ROWS for r in rows):
            raise ValueError('a row is not an object with a frozen id')
    except (ValueError, UnicodeDecodeError) as e:
        for rid in ROWS:
            out[rid].append('R1 json invalid: %s' % e)
        return out
    sources_raw = read('corpus/SOURCES.md')
    reg = registry_rows(sources_raw.decode('utf-8', 'replace')) if sources_raw else {}
    base_reg = registry_rows(base_sources)
    skill_raw = read('SKILL.md')
    skill = skill_raw.decode('utf-8', 'replace') if skill_raw else ''
    vis = list(visible_table_lines(skill))
    used_lines, used_captures = set(), set()
    for rid, (kind, tokens) in ROWS.items():
        f = out[rid]
        mine = [r for r in rows if r.get('id') == rid]
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
        snap = read(r['snapshot']) if good_path(r['snapshot']) else None
        if snap is None:
            f.append('R5 snapshot missing, a symlink, or outside %s' % EVIDENCE_PREFIX)
        if not re.fullmatch(r'S\d{3}', sid) or sid not in reg:
            f.append('R4 source row missing from the registry table')
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
        q = norm(r['quote'])
        if snap is not None:
            lines = snapshot_lines(snap, r['snapshot'])
            ln = r['line']
            if len(q) < 20:
                f.append('R6 quote under 20 characters')
            elif not (1 <= ln <= len(lines)) or not lines[ln - 1]:
                f.append('R6 line out of range or blank')
            else:
                first = lines[ln - 1]
                window = ' '.join(x for x in lines[ln - 1:ln + 2] if x)
                pos = window.find(q)
                if pos < 0 or pos >= len(first) or len(first) - pos < min(20, len(q)):
                    f.append('R6 quote not at the cited line')
                else:
                    key = (hashlib.sha256(snap).hexdigest(), ln)
                    if key in used_lines:
                        f.append('R6 cited line reused')
                    used_lines.add(key)
        if not any(word_in(t, q) for t in tokens):
            f.append('R7 quote lacks frozen token %s as a whole word' % '|'.join(tokens))
        if kind == 'host':
            v = r['value']
            cap = read(r['capture']) if good_path(r['capture']) else None
            if not re.fullmatch(r'\d+', v):
                f.append('R8 value not a decimal integer')
            elif cap is None:
                f.append('R8 capture missing, a symlink, or outside %s' % EVIDENCE_PREFIX)
            else:
                cl = [l[:-1] if l.endswith('\r') else l for l in cap.decode('utf-8', 'replace').split('\n')]
                cln = r['capture_line']
                if not (1 <= cln <= len(cl)) or not number_in(v, cl[cln - 1]):
                    f.append('R8 value not on capture line')
                elif CAPTURE_KEYS[rid].lower() not in cl[cln - 1].lower():
                    f.append('R8 capture line lacks %s' % CAPTURE_KEYS[rid])
                elif (r['capture'], cln) in used_captures:
                    f.append('R8 capture line reused')
                used_captures.add((r['capture'], cln))
                if not number_in(v, r['statement']):
                    f.append('R8 statement lacks value')
        marker = '| [R30-%s] ' % rid
        hits = [line for _n, line in vis if line.startswith(marker)]
        any_mention = sum(1 for line in skill.split('\n') if 'R30-' + rid in line)
        if len(hits) != 1 or any_mention != 1:
            f.append('R9 %d marker lines, %d mentions' % (len(hits), any_mention))
        else:
            if not re.search(r'(?<![A-Za-z0-9])%s(?![0-9])' % re.escape(sid), hits[0]):
                f.append('R9 marker line lacks source id')
            if kind == 'host' and not number_in(r['value'], hits[0]):
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
        p = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', a.revision + '^{commit}'],
                           capture_output=True, text=True, env=clean_env())
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
                      'unverified': bad, 'counter_sha256': sha, 'counter_version': VERSION}))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
