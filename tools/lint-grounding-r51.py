#!/usr/bin/env python3
"""Round-51 mechanical lint for the btrfs scrub grounding rows GR1-GR3.

The round-47..50 counted cohorts blocked every admission on defects a machine can find:
a quote that drops a comment leader (round 50 GR1: cmdline.c:147 without its ` * `), and
`file:line` citations outside the row source's declared ranges that the entry never named
(round 50 GR2/GR3: S242 scrub.c:3094-3095, :3109, :3114, :3138; S237 scrub.c:439 and :1546).
This tool finds both before a seat has to.

For each row GR1..GR3 of corpus/knowledge/btrfs-scrub-grounding-r45.md it checks:

  quote   every `**Quote.** `Snnn` file:line: "text"` equals the WHOLE digest-pinned source line
          (whitespace collapsed, ends trimmed) — a fragment, a dropped leader or a changed
          character is a defect. (`ends`: the quote may not be a substring only.)
  cite    every prose `file:line`, `file:a-b` and its colon-led continuations (`:a`, `:a-b`)
          resolves to existing lines of the row's pinned snapshot (the row maps each
          basename to one S-row: GR3's scrub.c is S237, GR2's is S242).
  gaps    the cited lines of each (S-row, file) that lie outside the row's declared ranges in
          corpus/SOURCES.md (the `lines a-b, c` list of its anchor cell; capture.txt and other
          own-work files count as wholly declared) are EXACTLY the lines named in the entry's
          `### Range gaps (R51)` block, one `- Snnn file: a, b-c` line per (S-row, file).

Counts printed (JSON, one line): quotes, quote_bad, cites, cite_bad, gaps_computed, gaps_declared,
gap_missing, gap_extra, per-row problems and `lint_ok` = number of rows with no problem
(3 = clean). `--emit-gaps` prints the block the entry must carry.

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
            'capture.txt': 'S249'},
    'GR2': {'dev-replace.c': 'S247', 'scrub.c': 'S242', 'sysfs.c': 'S243', 'ioctl.c': 'S240',
            'capture.txt': 'S249'},
    'GR3': {'systemd.kill.xml': 'S248', 'btrfs-scrub@.service': 'S244', 'scrub.c': 'S237',
            'capture.txt': 'S249'},
}
OWN_WORK = {'S249'}  # digest-pinned whole file; no line ranges in the anchor
QUOTE_RE = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
CITE_RE = re.compile(r'(?<![\w.@+-])([A-Za-z0-9_.@+-]+\.(?:c|h|xml|service|txt|sh)):(\d+)(?:-(\d+))?')
CONT_RE = re.compile(r'\A(?:,\s*|\s+and\s+|;\s*|\s*)?:(\d+)(?:-(\d+))?')
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
        if not part:
            continue
        m = re.fullmatch(r'(\d+)(?:-(\d+))?', part)
        if not m:
            continue
        a = int(m.group(1))
        b = int(m.group(2) or m.group(1))
        out.append((a, b))
    return out


def declared_ranges(sources_text):
    """sid -> basename -> list of (a,b) from the anchor cell of its registry row."""
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
        out[sid] = {}
        for base in SNAPSHOTS[sid]:
            mm = re.search(re.escape(base) + r' lines ([0-9][0-9, -]*)', anchor)
            out[sid][base] = parse_ranges(mm.group(1)) if mm else None
    return out


def in_ranges(n, ranges):
    return any(a <= n <= b for a, b in ranges)


def compress(nums):
    nums = sorted(set(nums))
    runs = []
    for n in nums:
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


def prose_cites(line):
    """Yield (basename, a, b) for every file:line citation incl. colon-led continuations."""
    pos = 0
    while True:
        m = CITE_RE.search(line, pos)
        if not m:
            return
        base = m.group(1)
        a = int(m.group(2))
        b = int(m.group(3)) if m.group(3) else a
        yield base, a, b
        pos = m.end()
        while True:
            c = CONT_RE.match(line[pos:])
            if not c:
                break
            a = int(c.group(1))
            b = int(c.group(2)) if c.group(2) else a
            yield base, a, b
            pos += c.end()


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


def analyze(entry, sources, cache):
    lines = entry.split('\n')
    decl = declared_ranges(sources)
    per = {}
    cited = {}  # (sid, base) -> set of lines (rows only)
    for row in ROWS:
        ext = row_extent(lines, row)
        prob = []
        nq = nqb = nc = ncb = 0
        if ext is None:
            per[row] = {'quotes': 0, 'quote_bad': 0, 'cites': 0, 'cite_bad': 0,
                        'problems': [f'{row}: header not exactly once']}
            continue
        i, j = ext
        for ln in lines[i:j]:
            m = QUOTE_RE.match(ln)
            if m:
                nq += 1
                sid, base, n, want = m.group(1), m.group(2).strip(), int(m.group(3)), m.group(4)
                src = cache.get((sid, base))
                if src is None:
                    nqb += 1
                    prob.append(f'quote {sid} {base}:{n}: snapshot absent')
                    continue
                if not 1 <= n <= len(src):
                    nqb += 1
                    prob.append(f'quote {sid} {base}:{n}: outside snapshot ({len(src)} lines)')
                    continue
                cited.setdefault((sid, base), set()).add(n)
                if norm(want) != norm(src[n - 1]):
                    nqb += 1
                    prob.append(f'quote {sid} {base}:{n}: not the whole line; line is {norm(src[n - 1])!r}')
                continue
            for base, a, b in prose_cites(ln):
                sid = PROSE[row].get(base)
                if sid is None:
                    continue
                nc += 1
                src = cache.get((sid, base))
                if src is None or not (1 <= a <= b <= len(src)):
                    ncb += 1
                    prob.append(f'cite {base}:{a}-{b}: does not resolve in {sid}')
                    continue
                cited.setdefault((sid, base), set()).update(range(a, b + 1))
        per[row] = {'quotes': nq, 'quote_bad': nqb, 'cites': nc, 'cite_bad': ncb, 'problems': prob}
    gaps = {}
    for (sid, base), nums in cited.items():
        if sid in OWN_WORK:
            continue
        ranges = decl.get(sid, {}).get(base)
        if ranges is None:
            gaps[(sid, base)] = set(nums)  # no declared lines at all: every cited line is a gap
            continue
        out = {n for n in nums if not in_ranges(n, ranges)}
        if out:
            gaps[(sid, base)] = out
    return per, gaps


def declared_gaps(entry):
    lines = entry.split('\n')
    try:
        k = next(i for i, ln in enumerate(lines) if ln.strip() == GAP_HEAD)
    except StopIteration:
        return None
    out = {}
    for ln in lines[k + 1:]:
        if ln.startswith('#'):
            break
        if not ln.strip():
            continue
        m = GAP_LINE_RE.match(ln.rstrip())
        if not m:
            out[('?', ln.strip())] = set()
            continue
        out[(m.group(1), m.group(2))] = expand(m.group(3))
    return out


def emit(gaps):
    rows = [f'- {sid} {base}: {compress(nums)}' for (sid, base), nums in sorted(gaps.items())]
    return GAP_HEAD + '\n\n' + '\n'.join(rows) + '\n'


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
    per, gaps = analyze(entry, sources, cache)
    if a.emit_gaps:
        sys.stdout.write(emit(gaps))
        return 0
    decl = declared_gaps(entry)
    gap_missing, gap_extra = [], []
    if decl is None:
        gap_missing = [f'{sid} {base}: {compress(n)}' for (sid, base), n in sorted(gaps.items())]
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
    rows_ok = 0
    for row in ROWS:
        if not per[row]['problems']:
            rows_ok += 1
    gap_ok = int(not gap_missing and not gap_extra and not snap_problems)
    lint_ok = rows_ok if gap_ok else 0
    out = {'counter': 'lint-grounding-r51', 'revision': rev or 'worktree',
           'quotes': sum(p['quotes'] for p in per.values()),
           'quote_bad': sum(p['quote_bad'] for p in per.values()),
           'cites': sum(p['cites'] for p in per.values()),
           'cite_bad': sum(p['cite_bad'] for p in per.values()),
           'gaps_computed': sum(len(v) for v in gaps.values()),
           'gap_missing': gap_missing, 'gap_extra': gap_extra, 'gap_note': gap_note,
           'snapshot_problems': snap_problems, 'rows_clean': rows_ok, 'gap_ok': gap_ok,
           'lint_ok': lint_ok,
           'per_row': {r: per[r] for r in ROWS}}
    out['verdict'] = 'PASS' if lint_ok == 3 else 'FAIL'
    print(json.dumps(out, sort_keys=True))
    return 0 if lint_ok == 3 else 1


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
