#!/usr/bin/env python3
"""Count anchored rows of the round-27 mori overlap register (claim C2). Git subprocesses, including selftest fixtures, use the round-30 child-environment contract.

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
  A4 the sibling quote has at most 25 words and, whitespace-normalised, is a
     substring of snapshot lines quote_line .. quote_line + 2
  A5 the lane side is lane_path plus lane_quote (at most 25 words, found
     normalised in that lane file at the revision), or both null and only when
     class is LANE-GAP
  A6 class in INBOUND-RESOLVES, INBOUND-DRIFTED, AGREES, CONFLICTS, LANE-GAP;
     owner in mori, tsukuroi, contested; action a non-empty string
  A7 the id is the first cell of a table row inside the PROVINCE.md section
     `## Adjacent — mori userspace OOM killers (round 27)`
Round-28 tightenings (QUALITY 72, R27-COUNTER-PERMISSIVE; each can only refuse):
  B1 the register's rows are exactly six objects whose ids are the strings OV1
     to OV6; an extra, non-object or non-string-id row makes anchored_rows 0
  B2 sibling_path is the pinned path and `snapshot` names its committed copy
  B3 the lines the quote occupies (the shortest prefix of its three-line
     window that contains it) hold no heading line
  B4 quotes are specific anchors of 4–25 words, rather than clipped or generic
     fragments; four-word technical identifiers remain valid
  B5 lane_path is normalised and each register id uses its pinned source file
  B6 LANE-GAP needs a null lane side; there is no cap on LANE-GAP rows
  B7 the PROVINCE register table is visible; its owner and class agree with
     the row, and duplicate ids count for neither
Round-29 padding rules:
  B8 identical sibling quotes use the same cited line; no more than two rows
     reuse a quote and no more than four rows cite one source paragraph
  B9 no more than two rows reuse one lane quote; a PROVINCE lane quote must be
     outside this register section
  B10 sibling and lane quote matches begin and end on whole lexical tokens
  B11 actions contain at least eight words and four distinct content words
  B12 withdrawn row/register/correction states and withdrawn actions do not count
  B13 only one visible four-column GFM table under the exact section counts;
      withdrawn subsections/prose and hidden HTML tables do not count
  B14 OV4 and OV5 retain their frozen class and owner decisions
  B15 the PROVINCE pointer column must not contradict its row class
When <siblings-root>/mori-shokunin exists, `git cat-file -p <commit>:<path>`
must equal the snapshot bytes (a mismatch fails every row; an absent sibling
repository is reported as `sibling-unavailable` and the snapshot still counts,
which B2 plus the pinned sha256 make safe).
Exit 0 when anchored_rows is 6, 1 when fewer, 2 when the register or the
snapshot cannot be read.  Read-only: no working-tree byte is consulted.
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
MIN_WORDS = 4
MIN_ACTION_WORDS = 8
LANE_PATHS = {
    'OV1': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV2': ('PROVINCE.md', 'corpus/knowledge/memory-pressure-r25.md'),
    'OV3': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV4': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV5': ('corpus/knowledge/memory-pressure-r25.md',),
    'OV6': (None,),
}
ROW_DECISIONS = {'OV4': ('CONFLICTS', 'tsukuroi'), 'OV5': ('CONFLICTS', 'mori')}
ROW_FIELDS = frozenset(('id', 'sibling', 'sibling_commit', 'sibling_path',
                        'sibling_blob_sha256', 'snapshot', 'heading', 'quote',
                        'quote_line', 'lane_path', 'lane_quote', 'class',
                        'owner', 'action'))
STOP_WORDS = frozenset(('a', 'about', 'after', 'all', 'also', 'an', 'and', 'any',
                        'are', 'as', 'at', 'be', 'because', 'been', 'before',
                        'being', 'both', 'but', 'by', 'can', 'could', 'did',
                        'do', 'does', 'for', 'from', 'had', 'has', 'have',
                        'here', 'how', 'if', 'in', 'into', 'is', 'it', 'its',
                        'may', 'might', 'more', 'most', 'must', 'no', 'not',
                        'of', 'on', 'or', 'our', 'out', 'over', 'same', 'should',
                        'so', 'such', 'than', 'that', 'the', 'their', 'them',
                        'then', 'there', 'these', 'they', 'this', 'those',
                        'through', 'to', 'under', 'up', 'very', 'was', 'we',
                        'were', 'what', 'when', 'where', 'which', 'while',
                        'who', 'will', 'with', 'would', 'you', 'your'))
DEFAULT_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(text):
    return ' '.join((text or '').split())

def contains_anchor(needle, haystack):
    needle, haystack = norm(needle), norm(haystack)
    if not needle:
        return False
    return bool(re.search(r'(?<![A-Za-z0-9_.@-])%s(?![A-Za-z0-9_.@-])'
                          % re.escape(needle), haystack))


def anchor_is_specific(text):
    words = (text or '').split()
    if len(words) < MIN_WORDS or len(words) > MAX_WORDS:
        return False
    tokens = re.findall(r'[A-Za-z0-9]+(?:[._@-][A-Za-z0-9]+)*', text.lower())
    content = {token for token in tokens if token not in STOP_WORDS}
    technical = {token for token in tokens
                 if any(ch in token for ch in '._@-')}
    return (len(words) >= 5 and len(content) >= 2) or len(technical) >= 2


def action_is_specific(text):
    if not isinstance(text, str) or len(text.split()) < MIN_ACTION_WORDS:
        return False
    if re.search(r'\bwithdraw(?:n|s|ing)?\b', text, re.I):
        return False
    tokens = re.findall(r'[A-Za-z0-9]+(?:[._@-][A-Za-z0-9]+)*', text.lower())
    return len({token for token in tokens if token not in STOP_WORDS}) >= 4


def pointer_disagrees(klass, pointer):
    pointer = norm(pointer).lower()
    if klass == 'CONFLICTS':
        return bool(re.search(
            r'\bno\s+conflicts?\b|\bwithout\s+conflicts?\b|'
            r'\b(?:full\s+)?agreement\s+with\b|\bconsistent\s+with\b|'
            r'\bsay\s+the\s+same\b|\bdoes\s+not\s+conflict\b|'
            r'\bdo\s+not\s+conflict\b|\bno\s+longer\s+conflicts?\b',
            pointer))
    if klass == 'AGREES':
        for match in re.finditer(r'\b(?:disagree\w*|conflict\w*|contradict\w*)\b',
                                 pointer):
            prefix = pointer[max(0, match.start() - 32):match.start()]
            if re.search(r'\b(?:not|never|without)\s+$|\bno\s+longer\s+$|'
                         r"\b(?:does|do|did)\s+not\s+$|\bdoesn't\s+$|"
                         r"\bdidn't\s+$", prefix):
                continue
            return True
    return False


def _without_html_comments(line, in_comment):
    visible = []
    i = 0
    while i < len(line):
        if in_comment:
            close = line.find('-->', i)
            if close < 0:
                return ''.join(visible), True
            i = close + 3
            in_comment = False
            continue
        if line[i] == '`':
            end = i
            while end < len(line) and line[end] == '`':
                end += 1
            marker = '`' * (end - i)
            match = re.search(r'(?<!`)%s(?!`)' % re.escape(marker), line[end:])
            if match:
                close = end + match.start()
                visible.append(line[i:close + len(marker)])
                i = close + len(marker)
                continue
        if line.startswith('<!--', i):
            i += 4
            in_comment = True
            continue
        visible.append(line[i])
        i += 1
    return ''.join(visible), in_comment


def _table_cells(line):
    value = line.strip()
    if value.startswith('|'):
        value = value[1:]
    if value.endswith('|'):
        value = value[:-1]
    return [cell.strip() for cell in value.split('|')]


def _cell_value(cell):
    value = cell.strip()
    for pattern in (r'`([^`]*)`', r'\*\*([^*]+)\*\*', r'\*([^*]+)\*'):
        match = re.fullmatch(pattern, value)
        if match:
            return match.group(1).strip()
    return value


def _withdrawal_text(text):
    return bool(re.search(r'\bwithdrawn\b|\bnot an anchor\b|\bhistory only\b',
                          text, re.I))


def git_env(temp_dir):
    home = os.path.join(temp_dir, 'home')
    os.mkdir(home)
    env = {key: value for key, value in os.environ.items()
           if not key.startswith(('GIT_', 'LD_', 'PYTHON'))}
    env.update({
        'GIT_CONFIG_NOSYSTEM': '1',
        'GIT_CONFIG_GLOBAL': os.devnull,
        'GIT_CONFIG_SYSTEM': os.devnull,
        'HOME': home,
        'XDG_CONFIG_HOME': os.path.join(home, '.config'),
        'PATH': '/usr/bin:/bin',
        'GIT_CEILING_DIRECTORIES': os.path.dirname(os.path.abspath(temp_dir)),
    })
    return env


def git(repo, *args):
    with tempfile.TemporaryDirectory(prefix='adjacency-git-') as tmp:
        return subprocess.run(['git', '-C', repo] + list(args), capture_output=True,
                              env=git_env(tmp))


def show(repo, rev, path):
    out = git(repo, 'show', '%s:%s' % (rev, path))
    return out.stdout if out.returncode == 0 else None


def province_rows(text):
    """Map ids to visible GFM rows in the unique, unwithdrawn register table."""
    rows = {}
    inside, fence, comment, html_block = False, None, False, None
    header, in_table = None, False
    invalid, blocked, section_count, table_count = False, False, 0, 0
    previous = ''
    for source_line in text.splitlines():
        expanded = source_line.expandtabs(4)
        indent = len(expanded) - len(expanded.lstrip(' '))
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', source_line)
        if fence is not None:
            if marker and marker.group(1)[0] == fence[0] \
                    and len(marker.group(1)) >= fence[1] and not marker.group(2).strip():
                fence = None
            continue
        if marker:
            fence = (marker.group(1)[0], len(marker.group(1)))
            header, in_table = None, False
            continue
        line, comment = _without_html_comments(source_line, comment)
        if comment:
            previous = ''
            continue
        if html_block is not None:
            if re.search(r'</%s\s*>' % html_block, line, re.I):
                html_block = None
            continue
        html_open = re.search(r'<(pre|details)\b', line, re.I)
        if html_open:
            tag = html_open.group(1).lower()
            if not re.search(r'</%s\s*>' % tag, line, re.I):
                html_block = tag
            header, in_table = None, False
            continue
        s = line.strip()
        if not s:
            header, in_table = None, False
            previous = ''
            continue
        if indent >= 4:
            header, in_table = None, False
            previous = line
            continue
        heading = re.match(r'^(#{1,6})(?:\s+|$)(.*)$', s)
        if heading:
            level = len(heading.group(1))
            if level <= 2:
                inside = level == 2 and s == SECTION
                header, in_table = None, False
                if inside:
                    section_count += 1
                    invalid |= section_count > 1
            elif inside and not in_table and table_count == 0:
                blocked = True
                header = None
            elif inside:
                in_table = False
                header = None
            previous = line
            continue
        html_heading = re.search(r'<h[1-6]\b[^>]*>(.*?)</h[1-6]\s*>', line, re.I)
        if inside and not in_table and table_count == 0 and html_heading:
            blocked = True
            previous = line
            continue
        if inside and not in_table and table_count == 0 \
                and re.fullmatch(r' {0,3}(?:=+|-+)\s*', line) \
                and previous.strip() and '|' not in previous:
            blocked = True
            header = None
            previous = line
            continue
        if inside and not in_table and table_count == 0 and _withdrawal_text(line):
            blocked = True
        if not inside:
            previous = line
            continue
        if blocked:
            previous = line
            continue
        if in_table:
            if '|' not in s:
                in_table = False
                header = None
                previous = line
                continue
            cells = _table_cells(s)
            if len(cells) != 4:
                invalid = True
                previous = line
                continue
            rid = _cell_value(cells[0])
            row = [rid, _cell_value(cells[1]), _cell_value(cells[2]), cells[3]]
            rows[rid] = None if rid in rows else row
            previous = line
            continue
        cells = _table_cells(s) if '|' in s else []
        if header is not None:
            if len(cells) == len(header) and all(
                    re.fullmatch(r':?-+:?', cell.strip()) for cell in cells):
                table_count += 1
                invalid |= table_count > 1
                invalid |= [_cell_value(cell).lower() for cell in header] != [
                    'id', 'owner', 'class', 'pointer']
                in_table = True
                header = None
                previous = line
                continue
            header = None
        if cells and len(cells) == 4:
            header = cells
        previous = line
    return {} if invalid or blocked or section_count != 1 or table_count != 1 else rows


def _paragraph_start(lines, quote_line):
    index = quote_line - 1
    while index > 0 and lines[index - 1].strip() \
            and not lines[index - 1].lstrip().startswith('#'):
        index -= 1
    return index


def _register_section_text(text):
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == SECTION), None)
    if start is None:
        return ''
    end = next((i for i in range(start + 1, len(lines))
                if re.match(r'^ {0,3}##(?:\s|$)', lines[i])), len(lines))
    return '\n'.join(lines[start:end])


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
        register = json.loads(raw.decode('utf-8'))
        assert isinstance(register, dict)
        rows = register['rows']
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
    corrections = register.get('corrections_r27_a2')
    register_withdrawn = str(register.get('status', '')).lower() == 'withdrawn' \
        or (isinstance(corrections, list) and any(
            isinstance(item, dict) and str(item.get('status', '')).lower() == 'withdrawn'
            for item in corrections))
    sibling_note = 'sibling-unavailable'
    sib_repo = os.path.join(siblings_root, 'mori-shokunin')
    snapshots, result = {}, {}
    sibling_anchor_counts, sibling_anchor_lines, paragraph_counts, lane_anchor_counts = {}, {}, {}, {}
    for item in rows:
        if not isinstance(item, dict):
            continue
        spath, quote = item.get('sibling_path'), item.get('quote')
        ql = item.get('quote_line')
        if isinstance(spath, str) and isinstance(quote, str):
            anchor = (spath, norm(quote))
            sibling_anchor_counts[anchor] = sibling_anchor_counts.get(anchor, 0) + 1
            if isinstance(ql, int) and not isinstance(ql, bool):
                sibling_anchor_lines.setdefault(anchor, set()).add(ql)
            if spath == PIN_PATH and isinstance(ql, int) and not isinstance(ql, bool) \
                    and ql > 0:
                if spath not in snapshots:
                    snapshots[spath] = show(repo, rev, SNAP_DIR + spath)
                snap_bytes = snapshots[spath]
                if snap_bytes is not None:
                    lines = snap_bytes.decode('utf-8', 'replace').splitlines()
                    if ql <= len(lines):
                        key = (spath, _paragraph_start(lines, ql))
                        paragraph_counts[key] = paragraph_counts.get(key, 0) + 1
        lpath, lquote = item.get('lane_path'), item.get('lane_quote')
        if isinstance(lpath, str) and isinstance(lquote, str):
            anchor = (lpath, norm(lquote))
            lane_anchor_counts[anchor] = lane_anchor_counts.get(anchor, 0) + 1
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
        if register_withdrawn:
            reasons.append('register-withdrawn')
        if isinstance(rid, str) and rid in ROW_DECISIONS \
                and (row.get('class'), row.get('owner')) != ROW_DECISIONS[rid]:
            reasons.append('decision-not-pinned')
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
                    elif not anchor_is_specific(quote):
                        reasons.append('quote-not-specific')
                    anchor = (spath, norm(quote))
                    if sibling_anchor_counts.get(anchor, 0) > 2:
                        reasons.append('sibling-anchor-reused')
                    if len(sibling_anchor_lines.get(anchor, ())) > 1:
                        reasons.append('sibling-anchor-line-shift')
                    paragraph = (spath, _paragraph_start(lines, ql))
                    if paragraph_counts.get(paragraph, 0) > 4:
                        reasons.append('sibling-paragraph-overused')
                    # B3: the lines the quote occupies (the shortest prefix of the
                    # three-line window that contains it) hold no heading line.
                    span = next((k for k in (1, 2, 3)
                                 if contains_anchor(
                                     quote, ' '.join(lines[ql - 1:ql - 1 + k]))), None)
                    if span is None:
                        reasons.append('quote-not-in-window')
                    elif any(l.startswith('#') for l in lines[ql - 1:ql - 1 + span]):
                        reasons.append('quote-spans-heading')
        lpath, lquote, klass = row.get('lane_path'), row.get('lane_quote'), row.get('class')
        if lpath is None and lquote is None:
            if klass != 'LANE-GAP':
                reasons.append('lane-null-not-gap')
        elif isinstance(lpath, str) and isinstance(lquote, str) and lpath and lquote.strip():
            if klass == 'LANE-GAP':
                reasons.append('lane-gap-with-lane-side')
            if lpath.startswith('.ufo/') or lpath.startswith('corpus/knowledge/adjacency-') \
                    or '..' in lpath.split('/') or os.path.normpath(lpath) != lpath:
                reasons.append('lane-path-not-lane-knowledge')
            if isinstance(rid, str) and lpath not in LANE_PATHS.get(rid, ()):
                reasons.append('lane-source-not-pinned-for-row')
            if lane_anchor_counts.get((lpath, norm(lquote)), 0) > 2:
                reasons.append('lane-anchor-reused')
            body = show(repo, rev, lpath)
            if body is None:
                reasons.append('lane-file-missing')
            else:
                lane_text = body.decode('utf-8', 'replace')
                if not contains_anchor(lquote, lane_text):
                    reasons.append('lane-quote-not-found')
                if lpath == 'PROVINCE.md' \
                        and contains_anchor(lquote, _register_section_text(province)):
                    reasons.append('lane-self-reference')
            if len(lquote.split()) > MAX_WORDS:
                reasons.append('lane-quote-too-long')
            elif not anchor_is_specific(lquote):
                reasons.append('lane-quote-not-specific')
        else:
            reasons.append('lane-side-malformed')
        if klass not in CLASSES:
            reasons.append('class-invalid')
        if row.get('owner') not in OWNERS:
            reasons.append('owner-invalid')
        if not action_is_specific(row.get('action')):
            reasons.append('action-insufficient')
        prow = in_province.get(rid) if isinstance(rid, str) else None
        if prow is None:
            reasons.append('province-row-missing')
        elif len(prow) != 4 or prow[1] != row.get('owner') or prow[2] != klass:
            reasons.append('province-disagrees')
        elif pointer_disagrees(klass, prow[3]):
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
    global PIN_PATH, PIN_SHA256
    snap = ('# Title\n\nintro line\n## Facts\n'
            'one fact about units here; if the service were; is a statement about a; '
            'systemd-oomd is inactive and disabled here\n'
            'second fact line has units\n'
            'third fact line uses signals\n'
            'fourth fact line tracks pressure\n\n'
            'fifth fact line maps counters; the installed version is earlyoom 1.9.0\n\n'
            'sixth fact line names the host\n\n'
            'seventh fact line maps decisions; the `user.oomd_ooms` / `user.oomd_kill`\n\n'
            '## Limits\nlimit sentence one here\n').encode()
    sha = hashlib.sha256(snap).hexdigest()
    saved = (PIN_PATH, PIN_SHA256)
    PIN_PATH, PIN_SHA256 = 'x/entry.md', sha
    lane_text = (
        'first lane says units are auto now; lane captures the measured system unit '
        'user-1000.slice; systemd-oomd is inactive and disabled here\n'
        'second lane observes memory pressure carefully\n'
        'third lane records host signals today\n'
        'fourth lane maps source details clearly; fourth lane reports distinct evidence now\n'
        'fifth lane traces system behavior fully\n')
    lane = {
        'corpus/knowledge/memory-pressure-r25.md': lane_text,
        '.ufo/waves/x/report.md': lane_text,
        'corpus/knowledge/adjacency-x.md': lane_text,
        'tools/check-adjacency-overlap.py': lane_text,
        'corpus/lessons/round-27.md': lane_text,
        'SCORECARD.md': lane_text,
        'corpus/knowledge/boot-plane.md': lane_text,
    }
    quote_lines = {
        'OV1': ('one fact about units here', 5),
        'OV2': ('fifth fact line maps counters', 10),
        'OV3': ('third fact line uses signals', 7),
        'OV4': ('fourth fact line tracks pressure', 8),
        'OV5': ('sixth fact line names the host', 12),
        'OV6': ('seventh fact line maps decisions', 14),
    }
    lane_quotes = {
        'OV1': 'first lane says units are auto now',
        'OV2': 'second lane observes memory pressure carefully',
        'OV3': 'third lane records host signals today',
        'OV4': 'fourth lane maps source details clearly',
        'OV5': 'fifth lane traces system behavior fully',
    }
    pointers = {
        'OV1': 'the lane confirms four distinct systemd units',
        'OV2': 'mori re-pins the requested target only',
        'OV3': 'meaning of auto matches the sibling reading',
        'OV4': 'the sources carry different reported conditions',
        'OV5': 'the sources carry different version evidence',
        'OV6': 'mori owns the accounting evidence for attributes',
    }

    def row_for(rows, rid):
        return next(row for row in rows if row.get('id') == rid)

    def row_state(rid):
        if rid == 'OV6':
            return 'LANE-GAP', 'mori'
        return ROW_DECISIONS.get(rid, ('AGREES', 'tsukuroi'))

    def province_row(rid, owner=None, klass=None, pointer=None):
        default_class, default_owner = row_state(rid)
        return '| %s | %s | %s | %s |' % (
            rid, owner or default_owner, klass or default_class,
            pointer if pointer is not None else pointers[rid])

    def replace_pointer(text, rid, pointer):
        return text.replace(province_row(rid), province_row(rid, pointer=pointer), 1)

    def base():
        rows = []
        for rid in IDS:
            klass, owner = row_state(rid)
            quote, quote_line = quote_lines[rid]
            lane_path = None if rid == 'OV6' else 'corpus/knowledge/memory-pressure-r25.md'
            rows.append({
                'id': rid, 'sibling': 'mori', 'sibling_commit': PIN_COMMIT,
                'sibling_path': 'x/entry.md', 'sibling_blob_sha256': sha,
                'snapshot': SNAP_DIR + 'x/entry.md', 'heading': '## Facts',
                'quote': quote, 'quote_line': quote_line,
                'lane_path': lane_path,
                'lane_quote': None if rid == 'OV6' else lane_quotes[rid],
                'class': klass, 'owner': owner,
                'action': 'Record this overlap with the source and owner clearly.',
            })
        return {'rows': rows, 'corrections_r27_a2': []}

    table_header = '| id | owner | class | pointer |\n|---|---|---|---|\n'
    table_rows = ''.join(province_row(rid) + '\n' for rid in IDS)
    table_block = table_header + table_rows
    province = ('# P\n\nHost memory and kill-event measurements support OS triage;\n\n'
                + SECTION + '\n\n' + table_block + '\n## Other\n')
    gap = {'lane_path': None, 'lane_quote': None, 'class': 'LANE-GAP'}
    gap_prov = province.replace(province_row('OV1'),
                                province_row('OV1', klass='LANE-GAP'))
    gap2_prov = gap_prov.replace(province_row('OV2'),
                                 province_row('OV2', klass='LANE-GAP'))
    fenced = province.replace(province_row('OV1') + '\n',
                              '```text\n' + province_row('OV1') + '\n```\n')

    def mut(fn, prov=None):
        reg = base()
        fn(reg['rows'])
        return reg, (prov if prov is not None else province)

    def mut_register(fn, prov=None):
        reg = base()
        fn(reg)
        return reg, (prov if prov is not None else province)

    def copy_quote(rows, target, source, quote_line=None):
        source_row, target_row = row_for(rows, source), row_for(rows, target)
        target_row['quote'] = source_row['quote']
        target_row['quote_line'] = source_row['quote_line'] if quote_line is None else quote_line

    cases = [
        ('clean', mut(lambda r: None), 0, 6),
        ('duplicate-id', mut(lambda r: row_for(r, 'OV6').update(id='OV1')), 1, 4),
        ('digest-mismatch', mut(lambda r: r[0].__setitem__('sibling_blob_sha256', 'f' * 64)), 1, 5),
        ('heading-not-nearest', mut(lambda r: r[0].update(heading='# Title')), 1, 5),
        ('quote-outside-window', mut(lambda r: r[0].update(quote='limit sentence one here')), 1, 5),
        ('quote-too-long', mut(lambda r: r[0].update(quote=' '.join(['w'] * 26))), 1, 5),
        ('lane-quote-missing', mut(lambda r: r[0].update(lane_quote='not in the lane file')), 1, 5),
        ('null-lane-not-gap', mut(lambda r: r[0].update(lane_path=None, lane_quote=None)), 1, 5),
        ('null-lane-gap-ok', mut(lambda r: r[0].update(gap), gap_prov), 0, 6),
        ('class-invalid', mut(lambda r: row_for(r, 'OV1').__setitem__('class', 'MAYBE'),
                              province.replace(province_row('OV1'),
                                               province_row('OV1', klass='MAYBE'))), 1, 5),
        ('owner-invalid', mut(lambda r: row_for(r, 'OV1').__setitem__('owner', 'kagi'),
                              province.replace(province_row('OV1'),
                                               province_row('OV1', owner='kagi'))), 1, 5),
        ('action-empty', mut(lambda r: r[0].__setitem__('action', ' ')), 1, 5),
        ('commit-not-pinned', mut(lambda r: r[0].__setitem__('sibling_commit', '0' * 40)), 1, 5),
        ('province-row-missing', mut(lambda r: None,
                                     province.replace(province_row('OV3') + '\n', '')), 1, 5),
        ('province-wrong-section', mut(lambda r: None,
                                       province.replace(SECTION, '## Adjacent — other')), 1, 0),
        ('row-missing', mut(lambda r: r.pop()), 1, 5),
        ('b1-extra-row-id', mut(lambda r: r.append(dict(r[0], id='OV7'))), 1, 0),
        ('b1-extra-row-id-space', mut(lambda r: r.append(dict(r[3], id='OV4 '))), 1, 0),
        ('b1-non-string-id', mut(lambda r: r.append(dict(r[0], id=['OV1']))), 1, 0),
        ('b1-non-object-row', mut(lambda r: r.extend(['junk row', None])), 1, 0),
        ('b2-sibling-path-not-pinned', mut(lambda r: r[0].__setitem__('sibling_path', 'x/./entry.md')), 1, 5),
        ('b2-snapshot-field-bogus', mut(lambda r: r[0].__setitem__('snapshot', '/etc/passwd')), 1, 5),
        ('b3-quote-line-on-heading', mut(lambda r: r[0].update(quote_line=4, quote='## Facts')), 1, 5),
        ('b3-window-crosses-heading', mut(lambda r: r[0].update(
            quote_line=14, quote='decisions; the `user.oomd_ooms` / `user.oomd_kill` ## Limits')), 1, 5),
        ('b4-short-sibling-quote', mut(lambda r: r[0].update(quote='units here')), 1, 5),
        ('b4-short-lane-quote', mut(lambda r: r[0].update(lane_quote='a')), 1, 5),
        ('b5-lane-under-ufo', mut(lambda r: r[0].update(lane_path='.ufo/waves/x/report.md')), 1, 5),
        ('b5-lane-is-register', mut(lambda r: r[0].update(lane_path='corpus/knowledge/adjacency-x.md')), 1, 5),
        ('b5-lane-is-sibling-snapshot', mut(lambda r: r[0].update(
            lane_path=SNAP_DIR + 'x/entry.md', lane_quote='one fact about units here')), 1, 5),
        ('b6-lane-gap-with-lane-side', mut(lambda r: row_for(r, 'OV1').__setitem__('class', 'LANE-GAP'),
                                           gap_prov), 1, 5),
        ('pass-b6-two-lane-gap-rows', mut(lambda r: (
            row_for(r, 'OV1').update(gap), row_for(r, 'OV2').update(gap)), gap2_prov), 0, 6),
        ('pass-b3-quote-ends-before-heading', mut(lambda r: row_for(r, 'OV1').update(
            quote_line=14, quote='seventh fact line maps decisions')), 0, 6),
        ('pass-b7-backticked-owner-class', mut(lambda r: None, province.replace(
            province_row('OV1'), province_row('OV1').replace(
                '| tsukuroi | AGREES |', '| `tsukuroi` | `AGREES` |'))), 0, 6),
        ('b7-province-disagrees', mut(lambda r: None, province.replace(
            province_row('OV2'), province_row('OV2', owner='mori'))), 1, 5),
        ('b7-province-row-in-fence', mut(lambda r: None, fenced), 1, 0),
        ('b5-lane-path-dot-slash-ufo', mut(lambda r: r[0].update(
            lane_path='./.ufo/waves/x/report.md')), 1, 5),
        ('b5-lane-path-double-slash', mut(lambda r: r[0].update(
            lane_path='corpus//knowledge/memory-pressure-r25.md')), 1, 5),
        ('b7-mixed-fence-markers', mut(lambda r: None, province.replace(
            province_row('OV1') + '\n',
            '~~~text\n```\n' + province_row('OV1') + '\n~~~\n')), 1, 0),
        ('b7-table-row-indented-four', mut(lambda r: None, province.replace(
            province_row('OV1') + '\n', '\n    ' + province_row('OV1') + '\n')), 1, 0),
        ('b7-duplicate-province-row', mut(lambda r: None, province.replace(
            province_row('OV2') + '\n',
            province_row('OV2') + '\n' + province_row('OV2', owner='mori') + '\n')), 1, 5),
        ('pass-upper-case-digest', mut(lambda r: r[0].__setitem__('sibling_blob_sha256', sha.upper())), 0, 6),
        ('pass-backticked-province-id', mut(lambda r: None, province.replace(
            province_row('OV1'), province_row('OV1').replace('| OV1 |', '| `OV1` |'))), 0, 6),
        # Round-29 padding shapes: accept the valid duplicate and syntax variants.
        ('pass-b8-two-rows-share-anchor', mut(lambda r: copy_quote(r, 'OV4', 'OV3')), 0, 6),
        ('pass-b4-four-word-technical-anchor', mut(lambda r: row_for(r, 'OV6').update(
            quote='the `user.oomd_ooms` / `user.oomd_kill`')), 0, 6),
        ('pass-b9-ov2-province-target', mut(lambda r: row_for(r, 'OV2').update(
            lane_path='PROVINCE.md',
            lane_quote='Host memory and kill-event measurements support OS triage;')), 0, 6),
        ('pass-b9-ov4-alternate-lane-sentence', mut(lambda r: row_for(r, 'OV4').update(
            lane_quote='fourth lane reports distinct evidence now')), 0, 6),
        ('pass-b13-single-dash-delimiter', mut(lambda r: None, province.replace(
            '|---|---|---|---|', '|-|-|-|-|')), 0, 6),
        ('pass-b13-aligned-delimiter', mut(lambda r: None, province.replace(
            '|---|---|---|---|', '| :-- | :-: | --: | -- |')), 0, 6),
        ('pass-b13-pipeless-row', mut(lambda r: None, province.replace(
            province_row('OV3') + '\n', province_row('OV3').strip('| ') + '\n')), 0, 6),
        ('pass-b7-bold-id', mut(lambda r: None, province.replace(
            province_row('OV1'), province_row('OV1').replace('| OV1 |', '| **OV1** |'))), 0, 6),
        ('pass-b13-inline-code-comment-opener', mut(lambda r: None, province.replace(
            province_row('OV3'), province_row('OV3', pointer=
                'meaning of auto matches the sibling reading; `<!--` blocks are not rows'))), 0, 6),
        ('pass-b13-h3-after-table', mut(lambda r: None, province.replace(
            '\n## Other\n', '\n\n### Round 29 follow-up\n\nThe evidence remains active.\n\n## Other\n')), 0, 6),
        ('pass-b13-h4-after-table', mut(lambda r: None, province.replace(
            '\n## Other\n', '\n\n#### Note\n\nThe evidence remains active.\n\n## Other\n')), 0, 6),
        ('pass-b13-indented-heading', mut(lambda r: None, province.replace(
            '\n## Other\n', '\n\n    ### example\n\n## Other\n')), 0, 6),
        ('pass-b15-conflicts-does-not-agree', mut(lambda r: None, replace_pointer(
            province, 'OV4', "mori F8 does not agree with the lane's qualifier")), 0, 6),
        ('pass-b15-conflicts-agreed-to-fix', mut(lambda r: None, replace_pointer(
            province, 'OV5', 'mori agreed to correct its r12 entry')), 0, 6),
        ('pass-b15-agrees-does-not-contradict', mut(lambda r: None, replace_pointer(
            province, 'OV3', 'mori does not contradict the lane reading')), 0, 6),
        ('pass-b15-agrees-no-longer-conflicts', mut(lambda r: None, replace_pointer(
            province, 'OV3', 'mori HEAD no longer conflicts with the ancestor clause')), 0, 6),
        ('pass-b12-narrowed-correction', mut_register(lambda reg:
            reg['corrections_r27_a2'].append({'row': 'all', 'status': 'narrowed'})), 0, 6),
        # Round-29 padding shapes: refuse reused, clipped, generic and withdrawn values.
        ('b8-shifted-duplicate-quote-line', mut(lambda r: copy_quote(
            r, 'OV4', 'OV3', quote_line=6)), 1, 4),
        ('b8-three-rows-reuse-quote', mut(lambda r: (
            copy_quote(r, 'OV1', 'OV3'), copy_quote(r, 'OV4', 'OV3'))), 1, 3),
        ('pass-b8-four-rows-one-paragraph', mut(lambda r: row_for(r, 'OV2').update(
            quote='second fact line has units', quote_line=6)), 0, 6),
        ('b8-five-rows-one-paragraph', mut(lambda r: (
            row_for(r, 'OV2').update(quote='second fact line has units', quote_line=6),
            copy_quote(r, 'OV5', 'OV4'))), 1, 1),
        ('b9-other-lane-file', mut(lambda r: row_for(r, 'OV3').update(
            lane_path='corpus/knowledge/boot-plane.md')), 1, 5),
        ('b9-province-self-mirror', mut(lambda r: row_for(r, 'OV2').update(
            lane_path='PROVINCE.md', lane_quote=pointers['OV2'])), 1, 5),
        ('b9-province-section-heading', mut(lambda r: row_for(r, 'OV2').update(
            lane_path='PROVINCE.md',
            lane_quote='Adjacent — mori userspace OOM killers (round 27)')), 1, 5),
        ('b9-lane-anchor-reused', mut(lambda r: (
            row_for(r, 'OV1').update(lane_quote=lane_quotes['OV3']),
            row_for(r, 'OV4').update(lane_quote=lane_quotes['OV3']),
            row_for(r, 'OV5').update(lane_quote=lane_quotes['OV3']))), 1, 2),
        ('b9-three-lane-anchor-copies', mut(lambda r: (
            row_for(r, 'OV2').update(lane_quote=lane_quotes['OV1']),
            row_for(r, 'OV5').update(lane_quote=lane_quotes['OV1']))), 1, 3),
        ('b10-sibling-word-cut', mut(lambda r: row_for(r, 'OV1').update(
            quote='oomd is inactive and disabled here')), 1, 5),
        ('b10-version-cut', mut(lambda r: row_for(r, 'OV2').update(
            quote='the installed version is earlyoom 1.9')), 1, 5),
        ('b10-lane-unit-name-cut', mut(lambda r: row_for(r, 'OV1').update(
            lane_quote='lane captures the measured system unit user-1000')), 1, 5),
        ('b4-generic-four-word-quote', mut(lambda r: row_for(r, 'OV1').update(
            quote='if the service were')), 1, 5),
        ('b4-five-function-word-quote', mut(lambda r: row_for(r, 'OV1').update(
            quote='is a statement about a')), 1, 5),
        ('b11-filler-action', mut(lambda r: row_for(r, 'OV1').__setitem__(
            'action', 'see the register row')), 1, 5),
        ('b11-repeated-token-action', mut(lambda r: [
            row.__setitem__('action', 'x x x x x x x x') for row in r]), 1, 0),
        ('b12-withdrawn-action', mut(lambda r: row_for(r, 'OV1').__setitem__(
            'action', 'WITHDRAWN: not an anchor any more; history only in this record')), 1, 5),
        ('b12-withdrawn-row-field', mut(lambda r: row_for(r, 'OV1').__setitem__(
            'status', 'withdrawn')), 1, 5),
        ('b12-withdrawn-register', mut_register(lambda reg: (
            reg.__setitem__('status', 'withdrawn'),
            reg['corrections_r27_a2'].append({'row': 'all', 'status': 'withdrawn'}))), 1, 0),
        ('b13-withdrawn-prose', mut(lambda r: None, province.replace(
            SECTION + '\n\n', SECTION + '\n\n**Withdrawn:** no row below is an anchor any more; history only.\n\n')), 1, 0),
        ('b13-setext-h2-withdrawal', mut(lambda r: None, province.replace(
            SECTION + '\n\n', SECTION + '\n\nWithdrawn rows (history only)\n------------------------------\n\n')), 1, 0),
        ('b13-setext-h1-withdrawal', mut(lambda r: None, province.replace(
            SECTION + '\n\n', SECTION + '\n\nWithdrawn\n=========\n\n')), 1, 0),
        ('b13-html-heading-withdrawal', mut(lambda r: None, province.replace(
            SECTION + '\n\n', SECTION + '\n\n<h3>Withdrawn rows (history only)</h3>\n\n')), 1, 0),
        ('b13-html-comment-table', mut(lambda r: None, province.replace(
            table_block, '<!--\n' + table_block.rstrip('\n') + '\n-->')), 1, 0),
        ('b13-pre-table', mut(lambda r: None, province.replace(
            table_block, '<pre>\n' + table_block.rstrip('\n') + '\n</pre>')), 1, 0),
        ('b13-details-table', mut(lambda r: None, province.replace(
            table_block, '<details><summary>Withdrawn rows (history only)</summary>\n\n'
            + table_block.rstrip('\n') + '\n\n</details>')), 1, 0),
        ('b13-withdrawn-subsection', mut(lambda r: None, province.replace(
            SECTION + '\n\n', SECTION + '\n\n### Withdrawn rows (not anchors, history only)\n\n')), 1, 0),
        ('b13-no-delimiter-table', mut(lambda r: None, province.replace(
            table_header, 'Rejected candidate rows, quoted verbatim:\n')), 1, 0),
        ('b13-shadow-section', mut(lambda r: None, province.replace(
            SECTION + '\n\n', SECTION + '\n\n' + table_block + '\n\n' + SECTION + '\n\n', 1)), 1, 0),
        ('b13-fifth-column', mut(lambda r: None, province.replace(
            table_block,
            '| id | owner | class | pointer | note |\n|---|---|---|---|---|\n' +
            ''.join(province_row(rid)[:-1] + ' note |\n' for rid in IDS))), 1, 0),
        ('b14-frozen-class', mut(lambda r: row_for(r, 'OV4').__setitem__('class', 'AGREES'),
                                 province.replace(province_row('OV4'),
                                                  province_row('OV4', klass='AGREES'))), 1, 5),
        ('b14-frozen-owner', mut(lambda r: row_for(r, 'OV5').__setitem__('owner', 'tsukuroi'),
                                 province.replace(province_row('OV5'),
                                                  province_row('OV5', owner='tsukuroi'))), 1, 5),
        ('b15-conflicts-agreement-noun', mut(lambda r: None, replace_pointer(
            province, 'OV4', 'in full agreement with the lane; nothing to report')), 1, 5),
        ('b15-conflicts-no-conflicts', mut(lambda r: None, replace_pointer(
            province, 'OV5', 'no conflicts: lane and mori say the same')), 1, 5),
        ('b15-conflicts-consistent', mut(lambda r: None, replace_pointer(
            province, 'OV4', 'mori F8 is consistent with lane lines 387-390')), 1, 5),
        ('b15-agrees-disagrees', mut(lambda r: None, replace_pointer(
            province, 'OV3', 'mori disagrees: conflicting meaning of auto')), 1, 5),
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
    PIN_PATH, PIN_SHA256 = saved
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
