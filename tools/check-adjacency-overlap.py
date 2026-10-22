#!/usr/bin/env python3
"""Count anchored rows of the round-27 mori overlap register (claim C2). The git helper removes inherited GIT_* variables for every git subprocess.

Rule (SCORECARD.md, "Round 27 — declaration, attempt 1"), every input read
through git at --revision:

  A1 corpus/knowledge/adjacency-mori-oom-r27.json holds exactly the ids OV1 to
     OV6, each once (a duplicate id is an error and never a second count)
  A2 sibling is `mori`, sibling_commit is the pinned mori commit, sibling_path
     is non-empty, and the committed snapshot
     .ufo/waves/round-27/siblings/mori/<sibling_path> has the sha256 written in
     sibling_blob_sha256 (round-27 tightening: and that sha256 is the pinned one)
  A3 heading is a line of the snapshot starting with `#` and is the nearest
     such line at or above quote_line
  A4 the sibling quote has at most 25 words and, whitespace-normalised, occurs
     on whole-token boundaries in snapshot lines quote_line .. quote_line + 2
  A5 the lane side is lane_path plus lane_quote (at most 25 words, found
     normalised in that lane file at the revision), or both null and only when
     class is LANE-GAP
  A6 class in INBOUND-RESOLVES, INBOUND-DRIFTED, AGREES, CONFLICTS, LANE-GAP;
     owner in mori, tsukuroi, contested; action has at least four words
  A7 the id is the first cell of a table row inside the PROVINCE.md section
     `## Adjacent — mori userspace OOM killers (round 27)`
Round-28 tightenings (QUALITY 72, R27-COUNTER-PERMISSIVE; each can only refuse):
  B1 the register's rows are exactly six objects whose ids are the strings OV1
     to OV6; an extra, non-object or non-string-id row makes anchored_rows 0
  B2 sibling_path is the pinned path and `snapshot` names its committed copy
  B3 the lines the quote occupies (the shortest prefix of its three-line
     window that contains it) hold no heading line
  B4 every sibling and lane quote has at least five words
  B5 lane_path is a normalised relative path (no `./`, `//` or `..`), not
     under `.ufo/`, an adjacency register, a wave report or the mori snapshot
  B6 LANE-GAP needs a null lane side (no cap on LANE-GAP rows: wave-1
     CritC1OverStrict showed a cap refuses a genuine second gap)
  B7 the PROVINCE row's owner and class cells match the register row; rows
     inside a code fence or indented four or more columns are not table rows;
     a repeated id counts for neither
  B8 sibling anchor keys (path, quote_line, normalised quote) are unique
  B9 each id uses its fixed round-27 lane source file: OV1/3/4/5 use
     memory-pressure-r25.md, OV2 uses PROVINCE.md, and OV6 has no lane file
     (this source allow-list does not prove a semantic judgment)
  B10 sibling and lane quote matches start and end on whole-token boundaries
  B11 each action has at least four whitespace-delimited words
  B12 rows contain only the fields in the round-27 register schema
  B13 PROVINCE evidence must be a visible, delimited table in the exact
      section; HTML comments and nested headings invalidate that section
  B14 the frozen CONFLICTS class and owners for OV4 and OV5 cannot be rewritten
  B15 a PROVINCE pointer must not contradict the row's AGREES/CONFLICTS class
When <siblings-root>/mori-shokunin exists, `git cat-file -p <commit>:<path>`
must equal the snapshot bytes (a mismatch fails every row; an absent sibling
repository is reported as `sibling-unavailable` and the snapshot still counts,
which B2 plus the pinned sha256 make safe).
Exit 0 when anchored_rows is 6, 1 when fewer, 2 when the register or the
snapshot cannot be read. Read-only: no working-tree byte is consulted.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

REGISTER = 'corpus/knowledge/adjacency-mori-oom-r27.json'
SNAP_DIR = '.ufo/waves/round-27/siblings/mori/'
PIN_COMMIT = 'ef9dbee136d6ed2ef98687f5cb0c0a16506a5155'
PIN_PATH = 'corpus/knowledge/userspace-oom-killers-r26.md'
PIN_SHA256 = 'a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d'
IDS = tuple('OV%d' % i for i in range(1, 7))
CLASSES = ('INBOUND-RESOLVES', 'INBOUND-DRIFTED', 'AGREES', 'CONFLICTS', 'LANE-GAP')
OWNERS = ('mori', 'tsukuroi', 'contested')
SECTION = '## Adjacent — mori userspace OOM killers (round 27)'
MAX_WORDS = 25
MIN_WORDS = 5
MIN_ACTION_WORDS = 4
LANE_PATHS = {
    'OV1': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV2': ('PROVINCE.md',),
    'OV3': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV4': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV5': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV6': (None,),
}
ROW_DECISIONS = {
    'OV4': ('CONFLICTS', 'tsukuroi'),
    'OV5': ('CONFLICTS', 'mori'),
}
ROW_FIELDS = frozenset(('id', 'sibling', 'sibling_commit', 'sibling_path',
                        'sibling_blob_sha256', 'snapshot', 'heading', 'quote',
                        'quote_line', 'lane_path', 'lane_quote', 'class',
                        'owner', 'action'))
DEFAULT_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(text):
    return ' '.join((text or '').split())


def contains_anchor(needle, haystack):
    needle, haystack = norm(needle), norm(haystack)
    return bool(re.search(r'(?<!\w)%s(?!\w)' % re.escape(needle), haystack))


def pointer_disagrees(klass, pointer):
    pointer = norm(pointer).lower()
    if klass == 'CONFLICTS':
        return bool(re.search(r'\bno\s+conflict\b|\bagree(?:s|d)?\b', pointer))
    if klass == 'AGREES':
        return bool(re.search(r'\bno\s+agreement\b|\bconflicts?\s+with\b|\bcontradicts?\b', pointer))
    return False


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True,
                          env=dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')},
                                   **{'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull}))


def show(repo, rev, path):
    out = git(repo, 'show', '%s:%s' % (rev, path))
    return out.stdout if out.returncode == 0 else None


def _without_html_comments(line, in_comment):
    visible = []
    while line:
        if in_comment:
            close = line.find('-->')
            if close < 0:
                return ''.join(visible), True
            line = line[close + 3:]
            in_comment = False
        opening = line.find('<!--')
        if opening < 0:
            visible.append(line)
            break
        visible.append(line[:opening])
        line = line[opening + 4:]
        in_comment = True
    return ''.join(visible), in_comment


def province_rows(text):
    """id -> cells for visible GFM table rows in SECTION; ambiguity counts none."""
    rows, inside, fence, comment = {}, False, None, False
    header, in_table, section_count, invalid = None, False, 0, False
    for source_line in text.splitlines():
        line, comment = _without_html_comments(source_line, comment)
        s = line.strip()
        if comment:
            continue
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence is not None:
            if marker and marker.group(1)[0] == fence[0] \
                    and len(marker.group(1)) >= fence[1] and not marker.group(2).strip():
                fence = None
            continue
        if marker:
            fence = (marker.group(1)[0], len(marker.group(1)))
            continue
        if re.match(r'^#{1,6}(?:\s|$)', s):
            level = len(s) - len(s.lstrip('#'))
            if level <= 2:
                inside = s == SECTION
                header, in_table = None, False
                if inside:
                    section_count += 1
                    invalid |= section_count > 1
            elif inside:
                invalid = True
                header, in_table = None, False
            continue
        if not inside:
            continue
        expanded = line.expandtabs(4)
        indent = len(expanded) - len(expanded.lstrip(' '))
        if indent >= 4:
            continue
        if not s:
            header, in_table = None, False
            continue
        if not s.startswith('|'):
            header, in_table = None, False
            continue
        cells = [cell.strip() for cell in s.strip('|').split('|')]
        if not in_table:
            rid = cells[0].strip('`') if cells else ''
            if rid in IDS:
                invalid = True
                header = None
                continue
            if header is None:
                header = cells
                continue
            if len(cells) == len(header) and all(
                    re.fullmatch(r':?-{3,}:?', cell) for cell in cells):
                in_table, header = True, None
                continue
            header = cells
            continue
        if not cells or not cells[0]:
            continue
        rid = cells[0]
        if len(rid) > 2 and rid[0] == rid[-1] == '`':
            rid = rid[1:-1]
        rows[rid] = None if rid in rows else cells
    return {} if invalid or section_count != 1 else rows


def evaluate(repo, rev, siblings_root):
    commit = git(repo, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % rev)
    if commit.returncode != 0:
        return 2, {'status': 'CANNOT_EVALUATE', 'finding': 'revision-invalid', 'revision': rev}
    rev = commit.stdout.decode().strip()
    raw = show(repo, rev, REGISTER)
    if raw is None:
        return 2, {'status': 'CANNOT_EVALUATE', 'finding': 'register-missing', 'revision': rev,
                   'anchored_rows': 0}
    try:
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
        rows = json.loads(raw.decode('utf-8'))['rows']
        assert isinstance(rows, list)
    except Exception:
        return 2, {'status': 'CANNOT_EVALUATE', 'finding': 'register-unreadable', 'revision': rev,
                   'anchored_rows': 0}
    province = (show(repo, rev, 'PROVINCE.md') or b'').decode('utf-8', 'replace')
    in_province = province_rows(province)
    ids = [r.get('id') if isinstance(r, dict) else None for r in rows]
    # B1: any row that is not an object, or whose id is not one of the six id strings.
    shape_errors = ['row%d-%s' % (i, 'not-object' if not isinstance(r, dict) else 'id-not-declared')
                    for i, r in enumerate(rows)
                    if not isinstance(r, dict) or not isinstance(r.get('id'), str) or r.get('id') not in IDS]
    sibling_anchor_counts = {}
    for item in rows:
        if not isinstance(item, dict):
            continue
        item_quote, item_line, item_path = item.get('quote'), item.get('quote_line'), item.get('sibling_path')
        if isinstance(item_quote, str) and isinstance(item_line, int) \
                and not isinstance(item_line, bool) and isinstance(item_path, str):
            anchor_key = (item_path, item_line, norm(item_quote))
            sibling_anchor_counts[anchor_key] = sibling_anchor_counts.get(anchor_key, 0) + 1
    sibling_note = 'sibling-unavailable'
    sib_repo = os.path.join(siblings_root, 'mori-shokunin')
    snapshots, result = {}, {}
    for row in rows:
        reasons = []
        if not isinstance(row, dict):
            continue
        rid = row.get('id')
        if not isinstance(rid, str) or rid not in IDS:
            reasons.append('id-unknown')
        elif ids.count(rid) != 1:
            reasons.append('id-duplicate')
        if set(row).difference(ROW_FIELDS):
            reasons.append('row-fields-unknown')
        if row.get('sibling') != 'mori':
            reasons.append('sibling-not-mori')
        if row.get('sibling_commit') != PIN_COMMIT:
            reasons.append('sibling-commit-not-pinned')
        spath = row.get('sibling_path')
        snap = None
        if not isinstance(spath, str) or not spath or '..' in spath.split('/'):
            reasons.append('sibling-path-invalid')
        elif spath != PIN_PATH:
            reasons.append('sibling-path-not-pinned')
        else:
            if row.get('snapshot') != SNAP_DIR + spath:
                reasons.append('snapshot-field-mismatch')
            if spath not in snapshots:
                snapshots[spath] = show(repo, rev, SNAP_DIR + spath)
            snap = snapshots[spath]
            if snap is None:
                reasons.append('snapshot-missing')
            else:
                digest = hashlib.sha256(snap).hexdigest()
                if str(row.get('sibling_blob_sha256')).lower() != digest:
                    reasons.append('snapshot-digest-mismatch')
                if spath == PIN_PATH and digest != PIN_SHA256:
                    reasons.append('snapshot-not-pinned-bytes')
                if os.path.isdir(os.path.join(sib_repo, '.git')) or os.path.isfile(os.path.join(sib_repo, '.git')):
                    live = git(sib_repo, 'cat-file', '-p', '%s:%s' % (PIN_COMMIT, spath))
                    if live.returncode != 0 or live.stdout != snap:
                        reasons.append('sibling-bytes-differ')
                        sibling_note = 'sibling-mismatch'
                    elif sibling_note != 'sibling-mismatch':
                        sibling_note = 'sibling-verified'
        if snap is not None:
            lines = snap.decode('utf-8', 'replace').splitlines()
            ql = row.get('quote_line')
            if not isinstance(ql, int) or isinstance(ql, bool) or not 1 <= ql <= len(lines):
                reasons.append('quote-line-invalid')
            else:
                nearest = next((lines[i] for i in range(ql - 1, -1, -1) if lines[i].startswith('#')), None)
                if nearest is None or row.get('heading') != nearest:
                    reasons.append('heading-not-nearest')
                quote = row.get('quote')
                if not isinstance(quote, str) or not quote.strip():
                    reasons.append('quote-missing')
                else:
                    if len(quote.split()) > MAX_WORDS:
                        reasons.append('quote-too-long')
                    if len(quote.split()) < MIN_WORDS:
                        reasons.append('quote-too-short')
                    # B3: the lines the quote occupies (the shortest prefix of the
                    # three-line window that contains it) hold no heading line.
                    span = next((k for k in (1, 2, 3)
                                 if contains_anchor(quote, ' '.join(lines[ql - 1:ql - 1 + k]))), None)
                    if span is None:
                        reasons.append('quote-not-in-window')
                    elif any(l.startswith('#') for l in lines[ql - 1:ql - 1 + span]):
                        reasons.append('quote-spans-heading')
                    if isinstance(spath, str) and isinstance(ql, int) and not isinstance(ql, bool) \
                            and sibling_anchor_counts.get((spath, ql, norm(quote)), 0) > 1:
                        reasons.append('sibling-anchor-reused')
        lpath, lquote, klass = row.get('lane_path'), row.get('lane_quote'), row.get('class')
        if isinstance(rid, str) and rid in LANE_PATHS and lpath not in LANE_PATHS[rid]:
            reasons.append('lane-source-not-pinned-for-row')
        if lpath is None and lquote is None:
            if klass != 'LANE-GAP':
                reasons.append('lane-null-not-gap')
        elif isinstance(lpath, str) and isinstance(lquote, str) and lpath and lquote.strip():
            if klass == 'LANE-GAP':
                reasons.append('lane-gap-with-lane-side')
            if lpath.startswith('.ufo/') or lpath.startswith('corpus/knowledge/adjacency-') \
                    or '..' in lpath.split('/') or os.path.normpath(lpath) != lpath:
                reasons.append('lane-path-not-lane-knowledge')
            body = show(repo, rev, lpath)
            if body is None:
                reasons.append('lane-file-missing')
            elif not contains_anchor(lquote, body.decode('utf-8', 'replace')):
                reasons.append('lane-quote-not-found')
            if len(lquote.split()) > MAX_WORDS:
                reasons.append('lane-quote-too-long')
            if len(lquote.split()) < MIN_WORDS:
                reasons.append('lane-quote-too-short')
        else:
            reasons.append('lane-side-malformed')
        if klass not in CLASSES:
            reasons.append('class-invalid')
        owner = row.get('owner')
        if owner not in OWNERS:
            reasons.append('owner-invalid')
        if isinstance(rid, str) and rid in ROW_DECISIONS \
                and (klass, owner) != ROW_DECISIONS[rid]:
            reasons.append('decision-not-pinned')
        action = row.get('action')
        if not isinstance(action, str) or len(action.split()) < MIN_ACTION_WORDS:
            reasons.append('action-insufficient')
        prow = in_province.get(rid) if isinstance(rid, str) else None
        if prow is None:
            reasons.append('province-row-missing')
        elif len(prow) < 3 or prow[1].strip('`*') != owner or prow[2].strip('`*') != klass:
            reasons.append('province-disagrees')
        elif len(prow) > 3 and pointer_disagrees(klass, prow[3]):
            reasons.append('province-pointer-disagrees')
        key = rid if isinstance(rid, str) else 'row%d' % len(result)
        result.setdefault(key, []).extend(reasons)
    # A duplicated id never counts (A1); a sibling byte mismatch fails every row;
    # a register-shape error (B1) fails every row.
    anchored = sum(1 for rid in IDS if ids.count(rid) == 1 and not result.get(rid))
    if sibling_note == 'sibling-mismatch' or shape_errors:
        anchored = 0
    out = {'revision': rev, 'anchored_rows': anchored, 'expected_rows': len(IDS),
           'sibling_check': sibling_note, 'rows': result, 'shape_errors': shape_errors,
           'status': 'PASS' if anchored == len(IDS) else 'FAIL'}
    return (0 if anchored == len(IDS) else 1), out


# ------------------------------------------------------------------ selftest

def _fixture(tmp, register, province, snap_bytes, lane_files):
    repo = os.path.join(tmp, 'lane')
    os.makedirs(repo)
    git(repo, 'init', '-q')
    files = dict(lane_files)
    files[REGISTER] = json.dumps(register)
    files['PROVINCE.md'] = province
    for path, text in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(text)
    full = os.path.join(repo, SNAP_DIR + 'x/entry.md')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'wb') as fh:
        fh.write(snap_bytes)
    git(repo, 'add', '-A')
    git(repo, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'fixture')
    return repo


def selftest():
    global PIN_PATH, PIN_SHA256, LANE_PATHS
    snap = ('# Title\n\nintro line\n## Facts\none fact about units here\n'
            'second fact line has units\nthird fact line uses signals\n'
            'fourth fact line tracks pressure\nfifth fact line maps counters\n'
            'sixth fact line names the host\n## Limits\nlimit sentence one here\n').encode()
    sha = hashlib.sha256(snap).hexdigest()
    saved = (PIN_PATH, PIN_SHA256, LANE_PATHS)
    PIN_PATH, PIN_SHA256 = 'x/entry.md', sha
    LANE_PATHS = {rid: ('corpus/knowledge/note.md', None) for rid in IDS}
    same = 'the lane says units are now\n'
    lane = {'corpus/knowledge/note.md': same, '.ufo/waves/x/report.md': same,
            'corpus/knowledge/adjacency-x.md': same,
            'corpus/knowledge/other.md': same}

    def base():
        rows = []
        quotes = [
            ('one fact about units here', 5),
            ('second fact line has units', 6),
            ('third fact line uses signals', 7),
            ('fourth fact line tracks pressure', 8),
            ('fifth fact line maps counters', 9),
            ('sixth fact line names the host', 10),
        ]
        for rid, (quote, quote_line) in zip(IDS, quotes):
            klass, owner = ROW_DECISIONS.get(rid, ('AGREES', 'tsukuroi'))
            rows.append({'id': rid, 'sibling': 'mori', 'sibling_commit': PIN_COMMIT,
                         'sibling_path': 'x/entry.md', 'sibling_blob_sha256': sha,
                         'snapshot': SNAP_DIR + 'x/entry.md',
                         'heading': '## Facts', 'quote': quote, 'quote_line': quote_line,
                         'lane_path': 'corpus/knowledge/note.md', 'lane_quote': 'lane says units are now',
                         'class': klass, 'owner': owner,
                         'action': 'record this overlap carefully'})
        return {'rows': rows}

    def province_row(rid):
        klass, owner = ROW_DECISIONS.get(rid, ('AGREES', 'tsukuroi'))
        return '| %s | %s | %s |\n' % (rid, owner, klass)

    province = '# P\n\n' + SECTION + '\n\n| id | owner | class |\n|---|---|---|\n' + \
        ''.join(province_row(rid) for rid in IDS) + '\n## Other\n'
    gap = {'lane_path': None, 'lane_quote': None, 'class': 'LANE-GAP'}
    gap_prov = province.replace('| OV1 | tsukuroi | AGREES |', '| OV1 | tsukuroi | LANE-GAP |')
    gap2_prov = gap_prov.replace('| OV2 | tsukuroi | AGREES |', '| OV2 | tsukuroi | LANE-GAP |')
    fenced = province.replace('| OV1 | tsukuroi | AGREES |\n', '```text\n| OV1 | tsukuroi | AGREES |\n```\n')

    def mut(fn, prov=None):
        reg = base()
        fn(reg['rows'])
        return reg, (prov if prov is not None else province)

    commented_table = ('| id | owner | class |\n|---|---|---|\n' +
                       ''.join(province_row(rid) for rid in IDS))
    commented = province.replace(commented_table, '<!--\n' + commented_table + '-->')
    withdrawn = province.replace('| id | owner | class |',
                                 'No row of this register is an anchor any more.\n\n'
                                 '### Withdrawn rows (not anchors, history only)\n\n'
                                 '| id | owner | class |')
    no_delimiter = province.replace('| id | owner | class |\n|---|---|---|\n',
                                    'Rejected candidate rows, quoted verbatim:\n')
    pointer_province = province.replace('| id | owner | class |', '| id | owner | class | pointer |')
    pointer_province = pointer_province.replace('|---|---|---|', '|---|---|---|---|')
    pointer_province = pointer_province.replace(
        '| OV1 | tsukuroi | AGREES |',
        '| OV1 | tsukuroi | AGREES | no agreement; the finding conflicts with it |')
    cases = [
        ('clean', mut(lambda r: None), 0, 6),
        ('duplicate-id', mut(lambda r: r[5].__setitem__('id', 'OV1')), 1, 4),
        ('digest-mismatch', mut(lambda r: r[0].__setitem__('sibling_blob_sha256', 'f' * 64)), 1, 5),
        ('heading-not-nearest', mut(lambda r: r[0].__setitem__('heading', '# Title')), 1, 5),
        ('quote-outside-window', mut(lambda r: r[0].update(quote='limit sentence one here')), 1, 5),
        ('quote-too-long', mut(lambda r: r[0].update(quote=' '.join(['w'] * 26))), 1, 5),
        ('lane-quote-missing', mut(lambda r: r[0].update(lane_quote='not in the lane file')), 1, 5),
        ('null-lane-not-gap', mut(lambda r: r[0].update(lane_path=None, lane_quote=None)), 1, 5),
        ('null-lane-gap-ok', mut(lambda r: r[0].update(gap), gap_prov), 0, 6),
        ('class-invalid', mut(lambda r: r[0].__setitem__('class', 'MAYBE'),
                              province.replace('| OV1 | tsukuroi | AGREES |', '| OV1 | tsukuroi | MAYBE |')), 1, 5),
        ('owner-invalid', mut(lambda r: r[0].__setitem__('owner', 'kagi'),
                              province.replace('| OV1 | tsukuroi | AGREES |', '| OV1 | kagi | AGREES |')), 1, 5),
        ('action-empty', mut(lambda r: r[0].__setitem__('action', ' ')), 1, 5),
        ('commit-not-pinned', mut(lambda r: r[0].__setitem__('sibling_commit', '0' * 40)), 1, 5),
        ('province-row-missing', mut(lambda r: None, province.replace('| OV3 | tsukuroi | AGREES |\n', '')), 1, 5),
        ('province-wrong-section', mut(lambda r: None, province.replace(SECTION, '## Adjacent — other')), 1, 0),
        ('row-missing', mut(lambda r: r.pop()), 1, 5),
        # round 28, B1 to B7 (QUALITY 72): each must refuse
        ('b1-extra-row-id', mut(lambda r: r.append(dict(r[0], id='OV7'))), 1, 0),
        ('b1-extra-row-id-space', mut(lambda r: r.append(dict(r[3], id='OV4 '))), 1, 0),
        ('b1-non-string-id', mut(lambda r: r.append(dict(r[0], id=['OV1']))), 1, 0),
        ('b1-non-object-row', mut(lambda r: r.extend(['junk row', None])), 1, 0),
        ('b2-sibling-path-not-pinned', mut(lambda r: r[0].__setitem__('sibling_path', 'x/./entry.md')), 1, 5),
        ('b2-snapshot-field-bogus', mut(lambda r: r[0].__setitem__('snapshot', '/etc/passwd')), 1, 5),
        ('b3-quote-line-on-heading', mut(lambda r: r[0].update(quote_line=4, quote='## Facts')), 1, 5),
        ('b3-window-crosses-heading', mut(lambda r: r[0].update(
            quote_line=10, quote='sixth fact line names the host ## Limits')), 1, 5),
        ('b4-short-sibling-quote', mut(lambda r: r[0].update(quote='units here')), 1, 5),
        ('b4-short-lane-quote', mut(lambda r: r[0].update(lane_quote='a')), 1, 5),
        ('b5-lane-under-ufo', mut(lambda r: r[0].update(lane_path='.ufo/waves/x/report.md')), 1, 5),
        ('b5-lane-is-register', mut(lambda r: r[0].update(lane_path='corpus/knowledge/adjacency-x.md')), 1, 5),
        ('b5-lane-is-sibling-snapshot', mut(lambda r: r[0].update(lane_path=SNAP_DIR + 'x/entry.md',
                                                                  lane_quote='one fact about units here')), 1, 5),
        ('b6-lane-gap-with-lane-side', mut(lambda r: r[0].__setitem__('class', 'LANE-GAP'), gap_prov), 1, 5),
        ('pass-b6-two-lane-gap-rows', mut(lambda r: (r[0].update(gap), r[1].update(gap)),
                                           gap2_prov), 0, 6),
        ('pass-b3-quote-ends-before-heading', mut(lambda r: r[0].update(
            quote_line=9, quote='fifth fact line maps counters sixth fact line names the host')), 0, 6),
        ('pass-b7-backticked-owner-class', mut(lambda r: None, province.replace(
            '| OV1 | tsukuroi | AGREES |', '| OV1 | `tsukuroi` | `AGREES` |')), 0, 6),
        ('b7-province-disagrees', mut(lambda r: None, province.replace(
            '| OV2 | tsukuroi | AGREES |', '| OV2 | mori | AGREES |')), 1, 5),
        ('b7-province-row-in-fence', mut(lambda r: None, fenced), 1, 5),
        # wave-1 CritC1NewShapes (round 28): each must refuse
        ('b5-lane-path-dot-slash-ufo', mut(lambda r: r[0].update(lane_path='./.ufo/waves/x/report.md')), 1, 5),
        ('b5-lane-path-double-slash', mut(lambda r: r[0].update(lane_path='corpus//knowledge/note.md')), 1, 5),
        ('b7-mixed-fence-markers', mut(lambda r: None, province.replace(
            '| OV1 | tsukuroi | AGREES |\n', '~~~text\n```\n| OV1 | tsukuroi | AGREES |\n~~~\n')), 1, 5),
        ('b7-table-row-indented-four', mut(lambda r: None, province.replace(
            '| OV1 | tsukuroi | AGREES |\n', '\n    | OV1 | tsukuroi | AGREES |\n')), 1, 0),
        ('b7-duplicate-province-row', mut(lambda r: None, province.replace(
            '| OV2 | tsukuroi | AGREES |\n',
            '| OV2 | tsukuroi | AGREES |\n| OV2 | mori | CONFLICTS |\n')), 1, 5),
        # Round-29 padding shapes: one should-fail case per added rule.
        ('b8-duplicate-sibling-anchor', mut(lambda r: r[1].update(
            quote=r[0]['quote'], quote_line=r[0]['quote_line'])), 1, 4),
        ('b9-lane-source-not-pinned', mut(lambda r: r[2].update(
            lane_path='corpus/knowledge/other.md')), 1, 5),
        ('b4-four-word-quote', mut(lambda r: r[0].update(
            quote='one fact about units')), 1, 5),
        ('b10-sibling-mid-word', mut(lambda r: r[0].update(
            quote='one fact about units her')), 1, 5),
        ('b10-lane-mid-word', mut(lambda r: r[0].update(
            lane_quote='the lane says units are no')), 1, 5),
        ('b11-placeholder-action', mut(lambda r: r[0].__setitem__('action', '-')), 1, 5),
        ('b12-unknown-withdrawn-field', mut(lambda r: r[0].__setitem__('status', 'withdrawn')), 1, 5),
        ('b13-province-html-comment', mut(lambda r: None, commented), 1, 0),
        ('b13-province-withdrawn-subsection', mut(lambda r: None, withdrawn), 1, 0),
        ('b13-province-no-delimiter', mut(lambda r: None, no_delimiter), 1, 0),
        ('b14-consistent-false-class', mut(
            lambda r: r[3].__setitem__('class', 'AGREES'),
            province.replace('| OV4 | tsukuroi | CONFLICTS |',
                             '| OV4 | tsukuroi | AGREES |')), 1, 5),
        ('b15-province-pointer-contradicts', mut(lambda r: None, pointer_province), 1, 5),
        # should pass: same digest in upper case; backticked PROVINCE id
        ('pass-upper-case-digest', mut(lambda r: r[0].__setitem__('sibling_blob_sha256', sha.upper())), 0, 6),
        ('pass-backticked-province-id', mut(lambda r: None, province.replace('| OV1 |', '| `OV1` |')), 0, 6),
    ]
    obs, failed = [], 0
    for name, (reg, prov), want_exit, want_rows in cases:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture(tmp, reg, prov, snap, lane)
            code, out = evaluate(repo, 'HEAD', os.path.join(tmp, 'no-siblings'))
        ok = code == want_exit and out.get('anchored_rows') == want_rows
        failed += not ok
        obs.append({'case': name, 'exit': code, 'anchored_rows': out.get('anchored_rows'), 'pass': ok})
    # sibling cross-check mismatch: a fake mori repo whose pinned blob differs
    with tempfile.TemporaryDirectory() as tmp:
        repo = _fixture(tmp, base(), province, snap, lane)
        code, out = evaluate(repo, 'HEAD', os.path.join(tmp, 'sibs'))
        os.makedirs(os.path.join(tmp, 'sibs', 'mori-shokunin'))
        git(os.path.join(tmp, 'sibs', 'mori-shokunin'), 'init', '-q')
        code2, out2 = evaluate(repo, 'HEAD', os.path.join(tmp, 'sibs'))
        ok = code == 0 and out['sibling_check'] == 'sibling-unavailable' and code2 == 1 \
            and out2['anchored_rows'] == 0
        failed += not ok
        obs.append({'case': 'sibling-unavailable-then-mismatch', 'exit': [code, code2], 'pass': ok})
    PIN_PATH, PIN_SHA256, LANE_PATHS = saved
    print(json.dumps({'cases': len(obs), 'failed': failed, 'observations': obs}))
    return 0 if failed == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--revision')
    g.add_argument('--selftest', action='store_true')
    ap.add_argument('--repo', default=DEFAULT_REPO)
    ap.add_argument('--siblings-root', default='/home/vgpnk/Projects/shokunin')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    code, out = evaluate(a.repo, a.revision, a.siblings_root)
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
