#!/usr/bin/env python3
"""Round-51 mechanical lint for the btrfs scrub grounding rows GR1-GR3.

The round-47..50 counted cohorts blocked every admission on defects a machine can find:
a quote that drops a comment leader (round 50 GR1: cmdline.c:147 without its ` * `), and
`file:line` citations outside a source row's declared ranges that the entry never named
(round 50 GR2/GR3). This tool finds both before a seat has to.

Amendment 1 (pre-w2, round 51): the wave-1 attackers R51RevLint and R51CritLintCheat showed the
freeze version missed colon-led citations after a parenthesis, dash variants, unmapped basenames,
non-canonical spellings, malformed quote lines, empty quotes, quotes outside a row, duplicate gap
keys, range bloat and a movable SOURCES.md anchor. All are closed below; the freeze bytes of this
file are kept in git history (`git show 2732ee6c:tools/lint-grounding-r51.py`).

For each row GR1..GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md it checks:

  quote   every line that contains `**Quote.**` matches `**Quote.** `Snnn` file:line: "text"`
          exactly; `Snnn` is the row's own source for that basename; the text is non-empty with an
          alphanumeric character; it equals the WHOLE digest-pinned source line (whitespace
          collapsed, ends trimmed), which is non-blank; the row holds at least one quote; no quote
          line sits outside the three rows.
  cite    prose citations are `file:N`, `file:N-M` (hyphen, en or em dash, optional spaces) and
          colon-led `:N` / `:N-M` that attach to the nearest preceding `file` in the same paragraph.
          Every cited basename is either the row's own source for it (PROSE) or a declared lane
          artifact (LANE_OK); every cited line exists in the pinned snapshot; a range spans at most
          100 lines; no mapped basename is followed or preceded within 25 characters by a bare number
          of 3+ digits that is not part of a citation (`line 3200 of scrub.c`, `scrub.c lines
          3200 to 3250`).
  gaps    the cited lines of each (S-row, file) outside the declared ranges are EXACTLY the lines
          named in the entry's `### Range gaps (R51)` block, one `- Snnn file: a, b-c` line per
          (S-row, file), no duplicate key. The declared ranges are pinned in this file
          (DECLARED_PIN) and must equal the anchor cells of corpus/SOURCES.md.

Counts printed (JSON, one line): quotes, quote_bad, cites, cite_bad, gaps_computed, gap_missing,
gap_extra, problems, rows_clean and `lint_ok` = rows with no problem when the gap block, the pinned
ranges and the whole entry are clean, else 0. `--emit-gaps` prints the block the entry must carry.

Usage: python3 tools/lint-grounding-r51.py [--revision REV | --worktree] [--lane DIR]
         [--entry-file F] [--sources-file F] [--emit-gaps]
Writes nothing. Exit 0 when lint_ok == 3, 1 otherwise, 2 on a read error.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
SOURCES = 'corpus/SOURCES.md'
ROWS = ('GR1', 'GR2', 'GR3')
SNAPSHOTS = {
    'S237': {'scrub.c': ('.ufo/waves/round-42/frozen/src/scrub.c',
                         '48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801')},
    'S242': {'scrub.c': ('.ufo/waves/round-44/frozen/src/scrub.c',
                         'f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8')},
    'S240': {'ioctl.c': ('.ufo/waves/round-43/frozen/src/ioctl.c',
                         '7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01')},
    'S243': {'sysfs.c': ('.ufo/waves/round-44/frozen/src/sysfs.c',
                         'ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43')},
    'S244': {'btrfs-scrub@.service': ('.ufo/waves/round-44/frozen/src/btrfs-scrub@.service',
                                      'eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252')},
    'S246': {'cmdline.c': ('.ufo/waves/round-45/frozen/src/cmdline.c',
                           '1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d'),
             'vsprintf.c': ('.ufo/waves/round-45/frozen/src/vsprintf.c',
                            'cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca'),
             'kstrtox.c': ('.ufo/waves/round-45/frozen/src/kstrtox.c',
                           '0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4')},
    'S247': {'dev-replace.c': ('.ufo/waves/round-45/frozen/src/dev-replace.c',
                               'f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a')},
    'S248': {'systemd.kill.xml': ('.ufo/waves/round-45/frozen/src/systemd.kill.xml',
                                  '448322830dbbd02c64cca99941ba92705afe9648241fc917db7a8d6ae7910e72')},
    'S249': {'capture.txt': ('.ufo/waves/round-45/frozen/hostcap/capture.txt',
                             'f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70')},
}
# Prose basename -> S-row, per row (the same basename names different files in GR2 and GR3).
PROSE = {
    'GR1': {'cmdline.c': 'S246', 'vsprintf.c': 'S246', 'kstrtox.c': 'S246', 'sysfs.c': 'S243',
            'scrub.c': 'S242', 'capture.txt': 'S249'},
    'GR2': {'dev-replace.c': 'S247', 'scrub.c': 'S242', 'sysfs.c': 'S243', 'ioctl.c': 'S240',
            'capture.txt': 'S249'},
    'GR3': {'systemd.kill.xml': 'S248', 'btrfs-scrub@.service': 'S244', 'scrub.c': 'S237',
            'capture.txt': 'S249'},
}
# Lane artifacts a row may cite by `file:N` besides its pinned sources (read-only receipts).
LANE_OK = {'host-btrfs-progs.txt'}
OWN_WORK = {'S249'}  # digest-pinned whole file; no line ranges in the anchor
# The declared ranges of each row source's anchor cell in corpus/SOURCES.md, pinned here: a
# widened anchor must not silently remove a gap. None = the whole file is declared (own-work).
DECLARED_PIN = {
    ('S237', 'scrub.c'): [(67, 70), (280, 330), (446, 535), (826, 895), (1110, 1125), (1186, 1220),
                          (1330, 1340), (1498, 1512), (1925, 1945)],
    ('S240', 'ioctl.c'): [(3066, 3075), (3118, 3140), (5578, 5584)],
    ('S242', 'scrub.c'): [(1365, 1385), (3140, 3162), (3215, 3226), (3321, 3337)],
    ('S243', 'sysfs.c'): [(72, 74), (2021, 2049), (2113, 2113)],
    ('S244', 'btrfs-scrub@.service'): [(1, 10)],
    ('S246', 'cmdline.c'): [(142, 201)],
    ('S246', 'vsprintf.c'): [(79, 115)],
    ('S246', 'kstrtox.c'): [(26, 40)],
    ('S247', 'dev-replace.c'): [(700, 703), (1143, 1144), (1235, 1235), (1256, 1268), (1276, 1300)],
    ('S248', 'systemd.kill.xml'): [(62, 116)],
}
MAX_RANGE = 100
DASH = '-\u2013\u2014'
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
BASE_PAT = r'[A-Za-z0-9_.@+-]+\.(?:c|h|xml|service|timer|txt|sh|md|json|conf|py)'
TOKEN_RE = re.compile(
    r'(?P<named>(?<![\w.@+-])(?P<base>' + BASE_PAT + r')(?![A-Za-z0-9_])\s*:\s*(?P<a>\d+)'
    r'(?:\s*[' + DASH + r']\s*(?P<b>\d+))?)'
    r'|(?P<bare>(?<=[\s(,;`])\s*:\s*(?P<ba>\d+)(?:\s*[' + DASH + r']\s*(?P<bb>\d+))?)')
GAP_HEAD = '### Range gaps (R51)'
GAP_LINE_RE = re.compile(r'^- (S\d+) (\S+): ([0-9][0-9, -]*)$')


def git_show(lane, rev, path):
    p = subprocess.run(['git', '-C', lane, 'show', f'{rev}:{path}'], capture_output=True,
                       stdin=subprocess.DEVNULL)
    return p.stdout if p.returncode == 0 else None


def read_bytes(lane, rev, path):
    if rev is None:
        try:
            with open(os.path.join(lane, path), 'rb') as fh:
                return fh.read()
        except OSError:
            return None
    return git_show(lane, rev, path)


def norm(s):
    return ' '.join(s.split())


def row_extent(lines, row):
    heads = [i for i, ln in enumerate(lines) if ln.strip() == f'## {row}']
    if len(heads) != 1:
        return None
    i = heads[0]
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
    return i, j


def parse_ranges(text):
    out = []
    for part in re.split(r'[, ]+', text.strip()):
        m = re.fullmatch(r'(\d+)(?:-(\d+))?', part)
        if m:
            a = int(m.group(1))
            out.append((a, int(m.group(2) or m.group(1))))
    return out


def declared_from_sources(sources_text):
    """(sid, basename) -> list of (a, b) read from the anchor cell of its registry row, or None."""
    out = {}
    for ln in sources_text.split('\n'):
        m = re.match(r'^\|\s*(S\d+)\s*\|', ln)
        if not m or m.group(1) not in SNAPSHOTS:
            continue
        sid = m.group(1)
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) < 11:
            continue
        anchor = cells[5]
        for base in SNAPSHOTS[sid]:
            mm = re.search(re.escape(base) + r' lines ([0-9][0-9, -]*)', anchor)
            out[(sid, base)] = parse_ranges(mm.group(1)) if mm else None
    return out


def in_ranges(n, ranges):
    return any(a <= n <= b for a, b in ranges)


def compress(nums):
    runs = []
    for n in sorted(set(nums)):
        if runs and n == runs[-1][1] + 1:
            runs[-1][1] = n
        else:
            runs.append([n, n])
    return ', '.join(str(a) if a == b else f'{a}-{b}' for a, b in runs)


def expand(text):
    s = set()
    for a, b in parse_ranges(text):
        s.update(range(a, b + 1))
    return s


def load_snapshots(lane, rev):
    cache, problems = {}, []
    for sid, files in SNAPSHOTS.items():
        for base, (path, want) in files.items():
            b = read_bytes(lane, rev, path)
            if b is None:
                problems.append(f'{sid} {base}: snapshot {path} unreadable')
                continue
            if hashlib.sha256(b).hexdigest() != want:
                problems.append(f'{sid} {base}: digest moved')
                continue
            cache[(sid, base)] = b.decode('utf-8', errors='replace').split('\n')
    return cache, problems


def _span(m):
    a = int(m.group('a') or m.group('ba'))
    b = m.group('b') or m.group('bb')
    return a, int(b) if b else a


def check_prose_line(row, line, cur, cache, cited, prob, counts):
    """Tokenise one prose line; returns the updated current basename."""
    masked = list(line)
    mapped = PROSE[row]
    for m in TOKEN_RE.finditer(line):
        a, b = _span(m)
        for k in range(m.start(), m.end()):
            masked[k] = ' '
        if m.group('named'):
            cur = m.group('base')
            base = cur
        else:
            base = cur
            if base is None:
                counts['cite_bad'] += 1
                prob.append(f'bare `:{a}` with no preceding file in its paragraph')
                continue
        counts['cites'] += 1
        if base in LANE_OK:
            continue
        sid = mapped.get(base)
        if sid is None:
            counts['cite_bad'] += 1
            prob.append(f'cite {base}:{a}-{b}: {base} is not a source of {row}')
            continue
        if b < a or b - a + 1 > MAX_RANGE:
            counts['cite_bad'] += 1
            prob.append(f'cite {base}:{a}-{b}: reversed or wider than {MAX_RANGE} lines')
            continue
        src = cache.get((sid, base))
        if src is None or not (1 <= a and b <= len(src)):
            counts['cite_bad'] += 1
            prob.append(f'cite {base}:{a}-{b}: does not resolve in {sid}')
            continue
        cited.setdefault((sid, base), set()).update(range(a, b + 1))
    rest = ''.join(masked)
    for base in mapped:
        for m in re.finditer(r'(?<![\w.@+-])' + re.escape(base) + r'(?![A-Za-z0-9_])', rest):
            near = rest[max(0, m.start() - 25):m.start()] + ' ' + rest[m.end():m.end() + 25]
            if re.search(r'(?<![\w.])\d{3,}(?![\w.])', near):
                counts['cite_bad'] += 1
                prob.append(f'non-canonical citation near {base}: {near.strip()!r}')
    return cur


def analyze(entry, sources, cache):
    lines = entry.split('\n')
    per, cited, glob = {}, {}, []
    extents = {}
    for row in ROWS:
        ext = row_extent(lines, row)
        extents[row] = ext
    inside = set()
    for ext in extents.values():
        if ext:
            inside.update(range(ext[0], ext[1]))
    for k, ln in enumerate(lines):
        if '**Quote.**' in ln and k not in inside:
            glob.append(f'quote line {k + 1} is outside every GR row')
    for row in ROWS:
        ext = extents[row]
        prob = []
        counts = {'quotes': 0, 'quote_bad': 0, 'cites': 0, 'cite_bad': 0}
        if ext is None:
            per[row] = {**counts, 'problems': [f'{row}: header not exactly once']}
            continue
        i, j = ext
        cur = None
        for ln in lines[i:j]:
            if not ln.strip():
                cur = None
                continue
            if '**Quote.**' in ln:
                counts['quotes'] += 1
                m = QUOTE_RE.match(ln)
                if not m:
                    counts['quote_bad'] += 1
                    prob.append(f'malformed quote line: {ln[:70]!r}')
                    continue
                sid, base, n, want = m.group(1), m.group(2).strip(), int(m.group(3)), m.group(4)
                if PROSE[row].get(base) != sid:
                    counts['quote_bad'] += 1
                    prob.append(f'quote {sid} {base}:{n}: not a {row} source (expected {PROSE[row].get(base)})')
                    continue
                src = cache.get((sid, base))
                if src is None:
                    counts['quote_bad'] += 1
                    prob.append(f'quote {sid} {base}:{n}: snapshot absent')
                    continue
                if not 1 <= n <= len(src):
                    counts['quote_bad'] += 1
                    prob.append(f'quote {sid} {base}:{n}: outside snapshot ({len(src)} lines)')
                    continue
                cited.setdefault((sid, base), set()).add(n)
                if not norm(want) or not re.search(r'[A-Za-z0-9]', want) or not norm(src[n - 1]):
                    counts['quote_bad'] += 1
                    prob.append(f'quote {sid} {base}:{n}: empty, blank or no alphanumeric content')
                    continue
                if norm(want) != norm(src[n - 1]):
                    counts['quote_bad'] += 1
                    prob.append(f'quote {sid} {base}:{n}: not the whole line; line is {norm(src[n - 1])!r}')
                continue
            cur = check_prose_line(row, ln, cur, cache, cited, prob, counts)
        if counts['quotes'] == 0:
            prob.append(f'{row}: no quote')
        per[row] = {**counts, 'problems': prob}
    pinned = {k: v for k, v in DECLARED_PIN.items()}
    gaps = {}
    for (sid, base), nums in cited.items():
        if sid in OWN_WORK:
            continue
        ranges = pinned.get((sid, base))
        if ranges is None:
            gaps[(sid, base)] = set(nums)
            continue
        out = {n for n in nums if not in_ranges(n, ranges)}
        if out:
            gaps[(sid, base)] = out
    return per, gaps, glob


def declared_gaps(entry):
    """(block dict, duplicate keys) or (None, [])."""
    lines = entry.split('\n')
    try:
        k = next(i for i, ln in enumerate(lines) if ln.strip() == GAP_HEAD)
    except StopIteration:
        return None, []
    out, dups = {}, []
    for ln in lines[k + 1:]:
        if ln.startswith('#'):
            break
        if not ln.strip():
            continue
        m = GAP_LINE_RE.match(ln.rstrip())
        if not m:
            out[('?', ln.strip())] = set()
            continue
        key = (m.group(1), m.group(2))
        if key in out:
            dups.append(f'{key[0]} {key[1]}')
        out[key] = expand(m.group(3))
    return out, dups


def emit(gaps):
    rows = [f'- {sid} {base}: {compress(nums)}' for (sid, base), nums in sorted(gaps.items())]
    return GAP_HEAD + '\n\n' + '\n'.join(rows) + '\n'


def evaluate(entry, sources, cache, snap_problems=()):
    """The whole lint as one dict (also used by tools/check-scrub-admission-r51.py)."""
    per, gaps, glob = analyze(entry, sources, cache)
    decl, dups = declared_gaps(entry)
    gap_missing, gap_extra = [], []
    if decl is None:
        gap_missing = [f'{k[0]} {k[1]}: {compress(n)}' for k, n in sorted(gaps.items())]
        gap_note = 'no ### Range gaps (R51) block'
    else:
        gap_note = 'ok'
        for key, nums in gaps.items():
            miss = nums - decl.get(key, set())
            if miss:
                gap_missing.append(f'{key[0]} {key[1]}: {compress(miss)}')
        for key, nums in decl.items():
            extra = nums - gaps.get(key, set())
            if extra or key[0] == '?':
                gap_extra.append(f'{key[0]} {key[1]}: {compress(extra) if extra else "unparseable"}')
    pin_problems = []
    live = declared_from_sources(sources)
    for key, want in DECLARED_PIN.items():
        if live.get(key) != want:
            pin_problems.append(f'{key[0]} {key[1]}: SOURCES.md anchor {live.get(key)} != pinned {want}')
    rows_clean = sum(1 for r in ROWS if not per[r]['problems'])
    gap_ok = int(not gap_missing and not gap_extra and not dups and not pin_problems
                 and not snap_problems and not glob)
    return {
        'quotes': sum(p['quotes'] for p in per.values()),
        'quote_bad': sum(p['quote_bad'] for p in per.values()),
        'cites': sum(p['cites'] for p in per.values()),
        'cite_bad': sum(p['cite_bad'] for p in per.values()),
        'gaps_computed': sum(len(v) for v in gaps.values()),
        'gap_missing': gap_missing, 'gap_extra': gap_extra, 'gap_dups': dups, 'gap_note': gap_note,
        'pin_problems': pin_problems, 'entry_problems': glob,
        'snapshot_problems': list(snap_problems), 'rows_clean': rows_clean, 'gap_ok': gap_ok,
        'lint_ok': rows_clean if gap_ok else 0,
        'per_row': {r: per[r] for r in ROWS}, '_gaps': gaps}


def run(a):
    lane = os.path.abspath(a.lane)
    rev = None if a.worktree else a.revision
    if a.entry_file:
        entry = open(a.entry_file, encoding='utf-8').read()
    else:
        b = read_bytes(lane, rev, ENTRY)
        entry = b.decode('utf-8') if b else None
    if a.sources_file:
        sources = open(a.sources_file, encoding='utf-8').read()
    else:
        b = read_bytes(lane, rev, SOURCES)
        sources = b.decode('utf-8') if b else None
    if entry is None or sources is None:
        print(json.dumps({'counter': 'lint-grounding-r51', 'error': 'entry/sources unreadable',
                          'verdict': 'FAIL'}))
        return 2
    cache, snap_problems = load_snapshots(lane, rev)
    res = evaluate(entry, sources, cache, snap_problems)
    if a.emit_gaps:
        sys.stdout.write(emit(res['_gaps']))
        return 0
    res.pop('_gaps')
    res = {'counter': 'lint-grounding-r51', 'revision': rev or 'worktree', **res}
    res['verdict'] = 'PASS' if res['lint_ok'] == 3 else 'FAIL'
    print(json.dumps(res, sort_keys=True))
    return 0 if res['lint_ok'] == 3 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision')
    ap.add_argument('--worktree', action='store_true')
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--entry-file')
    ap.add_argument('--sources-file')
    ap.add_argument('--emit-gaps', action='store_true')
    a = ap.parse_args()
    if not a.revision and not a.worktree:
        ap.error('--revision or --worktree required')
    try:
        return run(a)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({'counter': 'lint-grounding-r51', 'error': f'{type(e).__name__}: {e}',
                          'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
