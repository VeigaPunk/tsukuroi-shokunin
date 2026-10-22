#!/usr/bin/env python3
"""Count verified rows in the round-26 storage-integrity entry (claim C1).

The C1 claim is "6 verified rows, SH1 to SH6, exit 0" over the committed bytes of
one revision.  A row counts only when every one of these rules holds at <REV>:

  R1  the entry corpus/knowledge/storage-health-r26.json holds exactly the ids
      SH1 to SH6, each once; a duplicate id is an error, never a second count
  R2  the row carries a non-empty statement, a verdict out of HEALTHY, DEGRADED,
      BLOCKED, UNVERIFIED, and a non-empty action
  R3  every source the row lists is a corpus/SOURCES.md row with status mined,
      opened 2026-10-22 and used-by naming corpus/knowledge/storage-health-r26.md,
      and at least one cited source is tier A
  R4  the row carries at least one quote of at most 25 words whose whitespace-
      normalised text is a substring of the committed snapshot
      .ufo/waves/round-26/sources/<S###>.* whose sha256 is written in that source's
      anchor cell, and the same quote text appears in that source's row of the
      lesson corpus/lessons/round-26.md `## Gate` table
  R5  the row carries at least one capture pointer (line number and token of at
      least 3 characters) into .ufo/waves/round-26/capture/capture.txt, pinned at
      sha256 002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd,
      whose line is unique in the capture, is not a `### ` header, a `$ ` command
      echo or an `[exit ` line, and contains the token
  R6  SKILL.md carries a table line whose first cell is exactly the row id inside
      the section `## Storage integrity — round 26`

Every input is read through git at the bound revision (`git show`, `git ls-tree`);
no working-tree byte of the measured revision is consulted and no host is probed.
The capture digest is verified before anything else is read.

Exit codes: 0 when verified_rows == 6, 1 when any declared row fails, 2 when the
claim cannot be evaluated (entry or entry markdown missing, capture missing or
tampered, registry missing, lesson missing).

Scope: a count of evidence links in committed bytes.  It does not re-measure the
host, does not decide whether the storage plane is healthy, and authorises no
package, service, scrub, counter reset or boot action.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import _revision  # noqa: E402

ENTRY = 'corpus/knowledge/storage-health-r26.json'
ENTRY_MD = 'corpus/knowledge/storage-health-r26.md'
ENTRY_STEM = 'corpus/knowledge/storage-health-r26.md'
SOURCES = 'corpus/SOURCES.md'
LESSON = 'corpus/lessons/round-26.md'
SKILL = 'SKILL.md'
CAPTURE = '.ufo/waves/round-26/capture/capture.txt'
CAPTURE_SHA256 = '002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd'
SOURCE_DIR = '.ufo/waves/round-26/sources'
SCHEMA_PREFIX = 'tsukuroi-storage-health-r26'
ROW_IDS = ('SH1', 'SH2', 'SH3', 'SH4', 'SH5', 'SH6')
ROUND_DATE = '2026-10-22'
MAX_QUOTE_WORDS = 25
MIN_TOKEN_CHARS = 3
VERDICTS = ('HEALTHY', 'DEGRADED', 'BLOCKED', 'UNVERIFIED')

CELL_SPLIT = re.compile(r'(?<!\\)\|')
ID_TOKEN = re.compile(r'S\d{3}')
HEADING = re.compile(r'^#{1,6}\s')
HEX64 = re.compile(r'[0-9a-f]{64}')
SKILL_SECTION = re.compile(r'^storage integrity\b.*\bround 26\b', re.IGNORECASE)
SKILL_HEADING = re.compile(r'^##\s')
ENTRY_STEM_RE = re.compile(r'corpus/knowledge/storage-health-r26\.md\b')


# ---------------------------------------------------------------- utilities


def unique(pairs):
    """Reject a duplicate JSON key instead of silently taking the last one."""
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key: %s' % key)
        out[key] = value
    return out


def norm(text):
    """Whitespace-normalised text, for comparing a quote with its source."""
    return ' '.join(str(text).split())


def word_count(text):
    """Word count of a quote, split on whitespace."""
    return len((text or '').split())


def split_cells(line):
    """Split a markdown table row, honouring backslash-escaped pipes."""
    return [c.strip() for c in CELL_SPLIT.split(line.strip().strip('|'))]


def is_separator(cells):
    return bool(cells) and all(re.fullmatch(r':?-{2,}:?', c or '') for c in cells)


def raw_table_blocks(lines):
    """Yield each markdown table of a block of lines as its raw row lines."""
    block = []
    for line in lines:
        if line.strip().startswith('|'):
            block.append(line)
            continue
        if block:
            yield [row for row in block if not is_separator(split_cells(row))]
            block = []
    if block:
        yield [row for row in block if not is_separator(split_cells(row))]


def sections(text):
    """Split a markdown document into (heading title, lines) sections."""
    out = []
    title, current = None, []
    for line in (text or '').splitlines():
        if HEADING.match(line):
            out.append((title, current))
            title, current = line.lstrip('#').strip(), []
        else:
            current.append(line)
    out.append((title, current))
    return out


def extract_quote(cell):
    """The quoted span of a table cell, or the cell itself when unquoted."""
    text = (cell or '').strip()
    for pattern in (r'`([^`]+)`', '“([^”]+)”', '"([^"]+)"'):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return text


def cell_spans(line):
    """Split a table row into (start, end, text) spans over the raw line.

    A pipe that a backslash escapes does not separate cells, and a pipe
    inside a quoted value is found again by the quoted-span scan, so a
    located quote may itself contain a pipe.
    """
    spans = []
    start = 0
    for match in CELL_SPLIT.finditer(line):
        spans.append((start, match.start(), line[start:match.start()].strip()))
        start = match.end()
    spans.append((start, len(line), line[start:].strip()))
    return spans


BACKTICK_SPAN = re.compile(r'`([^`]*)`')
SEPARATED_QUOTES = re.compile(r'"\s*;\s')


def straight_quote_spans(text):
    """The double-quoted spans of a raw string.

    When the cell separates several located quotes with `"; `, the quotes
    pair from the left; otherwise the outermost pair is the located quote
    and the inner ones belong to its text.
    """
    positions = [i for i, ch in enumerate(text) if ch == '"']
    if len(positions) < 2:
        return []
    if SEPARATED_QUOTES.search(text):
        pairs = list(zip(positions[0::2], positions[1::2]))
    else:
        pairs = [(positions[0], positions[-1])] if len(positions) > 2 else \
            list(zip(positions[0::2], positions[1::2]))
    return [(start, end + 1, text[start + 1:end].strip()) for start, end in pairs if end > start]


def quoted_spans(line):
    """The quoted spans of a raw line, as (start, end, content).

    A backtick-delimited span wins over a straight-quoted one, because a
    located quote may contain double quotes inside backticks.
    """
    out = []
    for match in BACKTICK_SPAN.finditer(line):
        out.append((match.start(), match.end(), match.group(1).strip()))
    for start, end, content in straight_quote_spans(line):
        if not any(s <= start and end <= e for s, e, _ in out):
            out.append((start, end, content))
    out.sort()
    return out


def cell_quotes(line, quote_col):
    """The located quotes of one table row's quote column.

    The raw line is scanned, so a quote that contains a pipe or an escaped
    pipe is read whole.  A cell with no quote mark is read as its plain text.
    """
    spans = cell_spans(line)
    # Round 27 (routed round-26 defect 3, R26-GATE-COLUMN-OFFSET): the header
    # index comes from split_cells, which drops the empty cell before a leading
    # pipe, so the raw spans drop it too; a quoted span counts only when it
    # starts inside the quote cell.
    if line.lstrip().startswith('|'):
        spans = spans[1:]
    if quote_col >= len(spans):
        return []
    start, end = spans[quote_col][0], spans[quote_col][1]
    found = [content for span_start, _span_end, content in quoted_spans(line)
             if start <= span_start < end]
    if found:
        return found
    text = spans[quote_col][2]
    return [extract_quote(text)] if text else []


def first_id(text):
    """The first S### id in a text, or None."""
    found = ID_TOKEN.search(text or '')
    return found.group(0) if found else None


def id_in_line(line, row_id):
    """True when a text names a row id as a whole token."""
    return re.search(r'(?<![A-Za-z0-9])%s(?![0-9])' % re.escape(row_id), line or '') is not None


# ------------------------------------------------------------------ git i/o


class GitReader:
    """Read a repository at one revision; the working tree is never consulted."""

    def __init__(self, repo, rev):
        self.repo = str(repo)
        self.rev = rev

    def _run(self, *args):
        return subprocess.run(['git', '--no-pager', '-C', self.repo, *args],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=_revision.clean_env(), timeout=60)

    def read(self, path):
        """Bytes of one path at the bound revision, or None when absent."""
        if not isinstance(path, str) or not path or path.startswith('/'):
            return None
        if '..' in path.split('/'):
            return None
        proc = self._run('show', '%s:%s' % (self.rev, path))
        return proc.stdout if proc.returncode == 0 else None

    def ls(self, prefix):
        """Paths under a directory prefix at the bound revision."""
        proc = self._run('ls-tree', '-r', '--name-only', '-z', self.rev, '--', prefix)
        if proc.returncode != 0:
            return []
        return [name for name in proc.stdout.decode('utf-8', 'surrogateescape').split('\0') if name]


def decode(raw):
    if raw is None:
        return None
    return raw.decode('utf-8', 'surrogateescape')


# ------------------------------------------------------------------ inputs


def source_header(text):
    """The column names of the registry header, as {name: index}."""
    for line in (text or '').splitlines():
        if not line.strip().startswith('|'):
            continue
        cells = split_cells(line)
        if not cells or cells[0].strip().lower() != 'id':
            continue
        names = [c.strip().lower() for c in cells]
        if 'status' in names and 'used-by' in names:
            return {name: index for index, name in enumerate(names)}
    return None


def source_rows(text):
    """Map S### -> {status, opened, used_by, tier, anchor} from the registry."""
    out, dups = {}, set()
    header = source_header(text)
    for line in (text or '').splitlines():
        match = re.match(r'^\|\s*(S\d{3})\s*\|', line)
        if not match:
            continue
        cells = split_cells(line)
        sid = match.group(1)
        if sid in out:
            dups.add(sid)
            continue
        if header:
            def cell(name, _cells=cells):
                index = header.get(name)
                return _cells[index].strip() if index is not None and index < len(_cells) else ''
            info = {'status': cell('status'), 'opened': cell('opened'),
                    'used_by': cell('used-by'), 'tier': cell('tier'),
                    'anchor': cell('anchor')}
        else:
            if len(cells) < 11:
                continue
            info = {'status': cells[7].strip(), 'opened': cells[8].strip(),
                    'used_by': cells[10].strip(), 'tier': cells[3].strip(),
                    'anchor': cells[5].strip()}
        out[sid] = info
    return out, dups


def gate_quotes(text):
    """Map S### -> [quote text] from the lesson's `## Gate` table.

    The table is read by header names: a `Source` column and a `Located quote`
    column.  A line that is not a table row, or a table row that cannot be read,
    never raises: it becomes a finding, so a lesson prose line cannot crash the
    checker (round-25 routed defect 4).

    Returns (quotes, findings); a finding is (finding id, source id or None).
    """
    quotes = {}
    findings = []
    conforming = False
    for title, lines in sections(text):
        if not title or 'gate' not in title.lower():
            continue
        for block in raw_table_blocks(lines):
            if not block:
                continue
            header = split_cells(block[0])
            names = [c.strip().lower() for c in header]
            source_col = None
            quote_col = None
            for index, name in enumerate(names):
                if source_col is None and (name == 'source' or name.startswith('source ')):
                    source_col = index
                if quote_col is None and (name.startswith('located quote') or name == 'quote'):
                    quote_col = index
            if source_col is None or quote_col is None:
                continue
            conforming = True
            for raw in block[1:]:
                sid = first_id(raw)
                if sid is None:
                    # A line of the Gate table that names no source is not a
                    # Gate record; it is recorded, never read as one.
                    findings.append(('SH-GATE-LINE-MALFORMED', None))
                    continue
                located = [q for q in cell_quotes(raw, quote_col) if q]
                if not located:
                    findings.append(('SH-GATE-LINE-MALFORMED', sid))
                    continue
                for quote in located:
                    quotes.setdefault(sid, []).append(quote)
    if not conforming:
        findings.append(('SH-GATE-HEADER-MISSING', None))
    return quotes, findings


def skill_section_rows(text):
    """The lines of SKILL.md's `## Storage integrity — round 26` section.

    The section runs from its heading to the next `## ` heading; a `### ` sub
    heading stays inside it.  Returns (lines, found).
    """
    lines = (text or '').splitlines()
    inside = False
    found = False
    out = []
    for line in lines:
        if SKILL_HEADING.match(line):
            title = line.lstrip('#').strip()
            if inside:
                break
            inside = bool(SKILL_SECTION.match(title))
            found = found or inside
            continue
        if inside:
            out.append(line)
    return out, found


def skill_row_ids(lines):
    """The row ids whose first table cell is exactly the id."""
    found = set()
    for line in lines:
        if not line.strip().startswith('|'):
            continue
        cells = split_cells(line)
        if cells and re.fullmatch(r'SH\d+', cells[0]):
            found.add(cells[0])
    return found


def snapshot_paths(reader):
    """Map S### -> [snapshot paths] directly under the round-26 snapshot directory."""
    out = {}
    prefix = SOURCE_DIR + '/'
    for path in reader.ls(SOURCE_DIR):
        if not path.startswith(prefix):
            continue
        name = path[len(prefix):]
        if '/' in name:
            continue
        match = re.fullmatch(r'S(\d{3})(\.[^/]*)?', name)
        if not match:
            continue
        out.setdefault('S' + match.group(1), []).append(path)
    return out


# ----------------------------------------------------------------- capture


def pointer_token(pointer):
    """The declared token of a capture pointer (`token`, `contains` or `text`)."""
    token = pointer.get('token')
    if token is None:
        token = pointer.get('contains')
    if token is None:
        token = pointer.get('text')
    return token


def pointer_findings(pointer, capture_lines):
    """Findings for one capture pointer; an empty list means the pointer counts."""
    if not isinstance(pointer, dict):
        return ['SH-CAPTURE-POINTER-SHAPE']
    line = pointer.get('line')
    token = pointer_token(pointer)
    path = pointer.get('path')
    problems = []
    if path is not None and path != CAPTURE:
        problems.append('SH-CAPTURE-POINTER-PATH')
    if type(line) is not int or not isinstance(token, str):
        problems.append('SH-CAPTURE-POINTER-SHAPE')
        return problems
    if len(token) < MIN_TOKEN_CHARS:
        problems.append('SH-CAPTURE-POINTER-TOKEN-SHORT')
    if not 1 <= line <= len(capture_lines):
        problems.append('SH-CAPTURE-POINTER-LINE-RANGE')
        return problems
    text = capture_lines[line - 1]
    if text.startswith('### '):
        problems.append('SH-CAPTURE-POINTER-HEADER')
    if text.startswith('$ '):
        problems.append('SH-CAPTURE-POINTER-ECHO')
    if text.startswith('[exit '):
        problems.append('SH-CAPTURE-POINTER-EXIT')
    if not re.search(r'[A-Za-z0-9]', text):
        problems.append('SH-CAPTURE-POINTER-BLANK')
    if capture_lines.count(text) != 1:
        problems.append('SH-CAPTURE-POINTER-NOT-UNIQUE')
    if token not in text:
        problems.append('SH-CAPTURE-POINTER-TOKEN-ABSENT')
    return problems


# ---------------------------------------------------------------- evaluate


def rule_of(row_findings, ids):
    """Per-rule view of one row's findings."""
    hits = [f for f in row_findings if f['id'] in ids]
    return {'ok': not [f for f in hits if f['blocking']], 'findings': hits}


def evaluate(reader, expected_capture_sha=CAPTURE_SHA256):
    """Evaluate the entry at the bound revision.  Returns (exit code, result)."""
    findings = []
    global_blocked = False

    def note(fid, site, blocking=True):
        findings.append({'id': fid, 'site': site, 'blocking': blocking})

    def cannot(fid, site, declared=0):
        note(fid, site)
        return 2, {'status': 'CANNOT_EVALUATE', 'declared_rows': len(ROW_IDS),
                   'expected_rows': len(ROW_IDS), 'verified_rows': 0, 'rows': [],
                   'findings': findings, 'entry_rows': declared}

    # The capture digest is verified before anything else is read.
    raw_capture = reader.read(CAPTURE)
    if raw_capture is None:
        return cannot('SH-CAPTURE-MISSING', CAPTURE)
    observed_sha = hashlib.sha256(raw_capture).hexdigest()
    if observed_sha != expected_capture_sha:
        note('SH-CAPTURE-DIGEST-MISMATCH', CAPTURE)
        return 2, {'status': 'CANNOT_EVALUATE', 'declared_rows': 0,
                   'expected_rows': len(ROW_IDS), 'verified_rows': 0, 'rows': [],
                   'findings': findings, 'capture_sha256_observed': observed_sha}
    capture_lines = decode(raw_capture).splitlines()

    raw_entry = reader.read(ENTRY)
    if raw_entry is None:
        return cannot('SH-ENTRY-MISSING', ENTRY)
    try:
        entry = json.loads(decode(raw_entry), object_pairs_hook=unique)
    except ValueError as exc:
        return cannot('SH-ENTRY-MALFORMED', '%s: %s' % (ENTRY, exc))
    if not isinstance(entry, dict):
        return cannot('SH-ENTRY-MALFORMED', ENTRY)
    schema = entry.get('schema')
    if not isinstance(schema, str) or not schema.strip():
        return cannot('SH-ENTRY-SCHEMA', ENTRY)
    if not schema.startswith(SCHEMA_PREFIX):
        note('SH-ENTRY-SCHEMA', ENTRY)
        global_blocked = True
    if not isinstance(entry.get('rows'), list):
        return cannot('SH-ENTRY-SCHEMA', ENTRY)
    declared_rows = len(entry['rows'])

    raw_entry_md = reader.read(ENTRY_MD)
    if raw_entry_md is None:
        return cannot('SH-ENTRY-MD-MISSING', ENTRY_MD, declared_rows)
    entry_md_text = decode(raw_entry_md)

    raw_sources = reader.read(SOURCES)
    if raw_sources is None:
        return cannot('SH-SOURCES-MISSING', SOURCES, declared_rows)
    raw_lesson = reader.read(LESSON)
    if raw_lesson is None:
        return cannot('SH-LESSON-MISSING', LESSON, declared_rows)
    raw_skill = reader.read(SKILL)
    if raw_skill is None:
        note('SH-SKILL-MISSING', SKILL)
        global_blocked = True

    sources, dup_ids = source_rows(decode(raw_sources))
    quotes_by_sid, gate_findings = gate_quotes(decode(raw_lesson))
    for fid, sid in gate_findings:
        if fid == 'SH-GATE-HEADER-MISSING':
            note(fid, LESSON)
            global_blocked = True
        else:
            # A Gate line that cannot be read is a lesson-hygiene finding, not a
            # crash; the missing quote shows up on the row that needed it.
            note(fid, '%s: %s' % (LESSON, sid or 'prose line'), blocking=False)
    skill_lines, skill_found = skill_section_rows(decode(raw_skill) if raw_skill else '')
    if raw_skill is not None and not skill_found:
        note('SH-SKILL-SECTION-MISSING', SKILL)
        global_blocked = True
    skill_ids = skill_row_ids(skill_lines)

    snapshots = snapshot_paths(reader)
    snapshot_text = {}
    snapshot_sha = {}
    for sid, paths in snapshots.items():
        if len(paths) != 1:
            continue
        raw = reader.read(paths[0])
        if raw is None:
            continue
        snapshot_sha[sid] = hashlib.sha256(raw).hexdigest()
        snapshot_text[sid] = norm(decode(raw))

    # The entry's own capture pin, when it declares one, must name this capture.
    declared = entry.get('capture')
    if isinstance(declared, dict):
        if declared.get('path') not in (None, CAPTURE):
            note('SH-CAPTURE-PIN-PATH', str(declared.get('path')))
            global_blocked = True
        if declared.get('sha256') not in (None, observed_sha):
            note('SH-CAPTURE-PIN-DIGEST', str(declared.get('sha256')))
            global_blocked = True
    elif declared not in (None, CAPTURE):
        note('SH-CAPTURE-PIN-PATH', str(declared))
        global_blocked = True

    # An id that appears more than once is an error, never a second count:
    # it is withdrawn from the countable set and blocks the whole entry.
    counts = {}
    for candidate in entry['rows']:
        if isinstance(candidate, dict):
            key = candidate.get('id')
            counts[key] = counts.get(key, 0) + 1
    counted = {key for key, count in counts.items() if count == 1 and key in ROW_IDS}
    duplicated = sorted(str(key) for key, count in counts.items() if count > 1)
    if duplicated:
        note('SH-ROW-ID-DUPLICATE', ','.join(duplicated))
        global_blocked = True

    seen = set()
    rows = []
    for row in entry['rows']:
        row_id = row.get('id') if isinstance(row, dict) else None
        row_findings = []

        def note_row(fid, site, blocking=True):
            row_findings.append({'id': fid, 'site': site, 'blocking': blocking})

        if not isinstance(row, dict):
            note_row('SH-ROW-SHAPE', 'row')
            rows.append({'id': None, 'status': 'failed', 'verified': False,
                         'findings': row_findings, 'rules': {}})
            findings.extend(row_findings)
            continue
        if row_id not in ROW_IDS:
            note_row('SH-ROW-ID-UNKNOWN', str(row_id))
        elif counts.get(row_id, 0) > 1:
            # A duplicate id is an error, never a second count: the id is
            # withdrawn from the countable set above, and every row that
            # carries it fails.
            note_row('SH-ROW-ID-DUPLICATE', str(row_id))
        seen.add(row_id)

        # R2: statement, verdict and action.
        statement = row.get('statement')
        if not isinstance(statement, str) or not statement.strip():
            note_row('SH-STATEMENT-EMPTY', str(row_id))
        verdict = row.get('verdict')
        if not isinstance(verdict, str) or not verdict.strip():
            note_row('SH-VERDICT-MISSING', str(row_id))
        elif verdict.strip() not in VERDICTS:
            note_row('SH-VERDICT-INVALID', '%s: %s' % (row_id, verdict.strip()))
        action = row.get('action')
        if not isinstance(action, str) or not action.strip():
            note_row('SH-ACTION-EMPTY', str(row_id))

        # R3: sources.
        row_sources = row.get('sources')
        if row_sources is None:
            row_sources = row.get('source_ids')
        source_detail = []
        if not isinstance(row_sources, list) or not row_sources:
            note_row('SH-SOURCES-EMPTY', str(row_id))
            row_sources = []
        tier_a = False
        for raw_sid in row_sources:
            sid = raw_sid.get('id') if isinstance(raw_sid, dict) else raw_sid
            if not isinstance(sid, str) or sid not in sources:
                note_row('SH-SOURCE-MISSING', str(sid))
                source_detail.append({'id': sid, 'status': None, 'opened': None,
                                      'tier': None, 'used_by_names_entry': False,
                                      'qualifies': False})
                continue
            info = sources[sid]
            used_by_ok = bool(ENTRY_STEM_RE.search(info['used_by'] or ''))
            opened_ok = info['opened'] == ROUND_DATE
            tier_a = tier_a or info['tier'].strip().upper() == 'A'
            if info['status'] != 'mined':
                note_row('SH-SOURCE-STATUS-NOT-MINED', sid)
            if not opened_ok:
                note_row('SH-SOURCE-OPENED-WRONG', sid)
            if not used_by_ok:
                note_row('SH-SOURCE-USED-BY-MISSING', sid)
            if sid in dup_ids:
                note_row('SH-SOURCE-DUPLICATE', sid)
            source_detail.append({'id': sid, 'status': info['status'], 'opened': info['opened'],
                                  'tier': info['tier'], 'used_by_names_entry': used_by_ok,
                                  'qualifies': info['status'] == 'mined' and opened_ok
                                  and used_by_ok})
        if row_sources and not tier_a:
            note_row('SH-SOURCE-TIER-MISSING', str(row_id))

        # R4: quotes against the committed snapshot and the lesson Gate table.
        row_quotes = row.get('quotes')
        if row_quotes is None:
            row_quotes = row.get('located_quotes')
        quote_detail = []
        if not isinstance(row_quotes, list) or not row_quotes:
            note_row('SH-QUOTES-EMPTY', str(row_id))
            row_quotes = []
        for item in row_quotes:
            if isinstance(item, str):
                item = {'source': None, 'quote': item}
            if not isinstance(item, dict):
                note_row('SH-QUOTE-SHAPE', str(row_id))
                continue
            sid = item.get('source') or item.get('source_id') or item.get('id')
            quote = item.get('text')
            if quote is None:
                quote = item.get('quote')
            if not isinstance(quote, str):
                note_row('SH-QUOTE-SHAPE', str(row_id))
                continue
            quote_text = extract_quote(quote)
            detail = {'source': sid, 'words': word_count(quote_text), 'quote': quote_text,
                      'checks': {}}
            if not isinstance(sid, str):
                note_row('SH-QUOTE-SOURCE-UNKNOWN', str(row_id))
                detail['checks']['source_known'] = False
            else:
                detail['checks']['source_known'] = True
                if row_sources and sid not in row_sources:
                    note_row('SH-QUOTE-SOURCE-UNKNOWN', sid, blocking=False)
            detail['checks']['length'] = word_count(quote_text) <= MAX_QUOTE_WORDS
            if not detail['checks']['length']:
                note_row('SH-QUOTE-TOO-LONG', '%s: %s' % (row_id, sid))
            if not isinstance(sid, str) or sid not in snapshots:
                detail['checks']['snapshot'] = False
                note_row('SH-SNAPSHOT-MISSING', '%s: %s' % (row_id, sid))
            elif len(snapshots[sid]) != 1:
                detail['checks']['snapshot'] = False
                note_row('SH-SNAPSHOT-AMBIGUOUS', '%s: %s' % (row_id, sid))
            else:
                detail['checks']['snapshot'] = True
                digest = snapshot_sha.get(sid)
                anchor = sources.get(sid, {}).get('anchor', '') if isinstance(sources.get(sid), dict) else ''
                in_anchor = bool(digest) and digest in anchor and bool(HEX64.search(anchor or ''))
                detail['checks']['digest_in_anchor'] = in_anchor
                if not in_anchor:
                    note_row('SH-SNAPSHOT-DIGEST-NOT-IN-ANCHOR', '%s: %s' % (row_id, sid))
                in_snapshot = norm(quote_text) in snapshot_text.get(sid, '')
                detail['checks']['in_snapshot'] = in_snapshot
                if not in_snapshot:
                    note_row('SH-QUOTE-NOT-IN-SNAPSHOT', '%s: %s' % (row_id, sid))
            gate_texts = [norm(extract_quote(q)) for q in quotes_by_sid.get(sid, [])] \
                if isinstance(sid, str) else []
            in_gate = any(norm(quote_text) == text or norm(quote_text) in text
                          for text in gate_texts)
            detail['checks']['in_gate'] = in_gate
            if not in_gate:
                note_row('SH-GATE-QUOTE-MISSING', '%s: %s' % (row_id, sid))
            quote_detail.append(detail)

        # R5: capture pointers.
        pointers = row.get('capture_pointers')
        if pointers is None:
            pointers = row.get('pointers')
        pointer_detail = []
        if not isinstance(pointers, list) or not pointers:
            note_row('SH-CAPTURE-POINTER-MISSING', str(row_id))
            pointers = []
        for pointer in pointers:
            problems = pointer_findings(pointer, capture_lines)
            for fid in problems:
                note_row(fid, '%s: %s' % (row_id, json.dumps(pointer, sort_keys=True)))
            pointer_detail.append({'pointer': pointer, 'findings': problems,
                                   'counts': not problems})
        if pointers and not [p for p in pointer_detail if p['counts']]:
            note_row('SH-CAPTURE-POINTER-UNUSABLE', str(row_id))

        # R6: SKILL.md row inside the storage-integrity section.
        skill_hit = bool(row_id) and row_id in skill_ids
        if not skill_hit:
            note_row('SH-SKILL-ROW-MISSING', str(row_id))

        # The entry markdown must carry the row id as well (advisory).
        if not id_in_line(entry_md_text, row_id):
            note_row('SH-ENTRY-MD-ROW-MISSING', str(row_id), blocking=False)

        verified = not [f for f in row_findings if f['blocking']]
        rules = {
            'R1_row_ids': {'ok': row_id in ROW_IDS and row_id in counted},
            'R2_statement_verdict_action': rule_of(row_findings, ('SH-STATEMENT-EMPTY',
                                                                 'SH-VERDICT-MISSING',
                                                                 'SH-VERDICT-INVALID',
                                                                 'SH-ACTION-EMPTY')),
            'R3_sources': rule_of(row_findings, ('SH-SOURCES-EMPTY', 'SH-SOURCE-MISSING',
                                                 'SH-SOURCE-STATUS-NOT-MINED',
                                                 'SH-SOURCE-OPENED-WRONG',
                                                 'SH-SOURCE-USED-BY-MISSING',
                                                 'SH-SOURCE-TIER-MISSING',
                                                 'SH-SOURCE-DUPLICATE')),
            'R4_quote_snapshot_gate': rule_of(row_findings, ('SH-QUOTES-EMPTY', 'SH-QUOTE-SHAPE',
                                                            'SH-QUOTE-TOO-LONG',
                                                            'SH-QUOTE-NOT-IN-SNAPSHOT',
                                                            'SH-SNAPSHOT-MISSING',
                                                            'SH-SNAPSHOT-AMBIGUOUS',
                                                            'SH-SNAPSHOT-DIGEST-NOT-IN-ANCHOR',
                                                            'SH-GATE-QUOTE-MISSING')),
            'R5_capture_pointer': rule_of(row_findings, ('SH-CAPTURE-POINTER-MISSING',
                                                         'SH-CAPTURE-POINTER-UNUSABLE',
                                                         'SH-CAPTURE-POINTER-SHAPE',
                                                         'SH-CAPTURE-POINTER-PATH',
                                                         'SH-CAPTURE-POINTER-LINE-RANGE',
                                                         'SH-CAPTURE-POINTER-HEADER',
                                                         'SH-CAPTURE-POINTER-ECHO',
                                                         'SH-CAPTURE-POINTER-EXIT',
                                                         'SH-CAPTURE-POINTER-BLANK',
                                                         'SH-CAPTURE-POINTER-NOT-UNIQUE',
                                                         'SH-CAPTURE-POINTER-TOKEN-ABSENT',
                                                         'SH-CAPTURE-POINTER-TOKEN-SHORT')),
            'R6_skill_row': rule_of(row_findings, ('SH-SKILL-ROW-MISSING',
                                                    'SH-SKILL-SECTION-MISSING',
                                                    'SH-SKILL-MISSING')),
        }
        rows.append({'id': row_id, 'status': 'verified' if verified else 'failed',
                     'verified': verified, 'findings': row_findings, 'rules': rules,
                     'sources': source_detail, 'quotes': quote_detail,
                     'capture_pointers': pointer_detail, 'skill_row': skill_hit})
        findings.extend(row_findings)

    if seen != set(ROW_IDS):
        note('SH-ROW-SET', ','.join(sorted(str(s) for s in seen)))
        global_blocked = True

    verified_rows = 0 if global_blocked else sum(
        1 for row in rows if row.get('verified') and row.get('id') in counted)
    code = 0 if verified_rows == len(ROW_IDS) else 1
    return code, {'status': ('PASS', 'FAIL')[code],
                  'declared_rows': len(ROW_IDS),
                  'entry_rows': declared_rows,
                  'expected_rows': len(ROW_IDS),
                  'verified_rows': verified_rows,
                  'rows': rows, 'findings': findings,
                  'capture_sha256_observed': observed_sha}


# ---------------------------------------------------------------- selftest


FIXTURE_CAPTURE = (
    '### header\n'
    '$ cat /proc/mounts\n'
    '/dev/mapper/root / btrfs rw,relatime\n'
    '[exit 0]\n'
    '$ cat /sys/fs/btrfs/1d02a454/devinfo/1/error_stats\n'
    'write_errs 0\n'
    'read_errs 0\n'
    'flush_errs 0\n'
    'corruption_errs 0\n'
    'generation_errs 0\n'
    '[exit 0]\n'
    '$ cat /sys/fs/btrfs/1d02a454/allocation/data/profile\n'
    'single\n'
    '[exit 0]\n'
    '$ btrfs scrub status /\n'
    'no stats available\n'
    '[exit 0]\n'
    '$ cat /sys/fs/btrfs/1d02a454/duplicated\n'
    'duplicate marker line\n'
    'duplicate marker line\n'
)

FIXTURE_SOURCES = ('S128', 'S129', 'S130', 'S131', 'S132', 'S133')
FIXTURE_QUOTES = (
    'the btrfs device error counters are cumulative per device',
    'the error counters survive a remount until they are reset',
    'a single profile data checksum error is detected but not repaired',
    'no scrub statistics exist for this filesystem',
    'the critical warning field decides the overall health result',
    'the unsafe shutdown counter is cumulative over the device life',
)
FIXTURE_POINTER_LINE = 6
FIXTURE_POINTER_TOKEN = 'write_errs 0'
REGISTRY_HEAD = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
                 '|---|---|---|---|---|---|---|---|---|---|---|\n')


def snapshot_body(quote):
    """A snapshot body that carries the quote text."""
    return 'btrfs device documentation\n%s\nthe counters are kept per device\n' % quote


def build_fixture(snapshot_quotes=None, sources_meta=None, entry_quotes=None,
                  gate_quotes_map=None, gate_drop=(), lesson=None, skill=None,
                  entry_md=None, entry_rows=None, entry=None, capture=None,
                  entry_json_text=None, drop=()):
    """Build one hermetic fixture file set and return (files, capture sha256)."""
    snapshot_quotes = snapshot_quotes or {}
    sources_meta = sources_meta or {}
    entry_quotes = entry_quotes or {}
    gate_quotes_map = gate_quotes_map or {}
    capture = FIXTURE_CAPTURE if capture is None else capture
    capture_sha = hashlib.sha256(capture.encode('utf-8')).hexdigest()

    files = {}
    snapshots = {}
    for index, sid in enumerate(FIXTURE_SOURCES):
        quote = snapshot_quotes.get(sid, FIXTURE_QUOTES[index])
        path = '%s/%s.rst' % (SOURCE_DIR, sid)
        snapshots[sid] = path
        files[path] = snapshot_body(quote)

    rows = []
    for index, sid in enumerate(FIXTURE_SOURCES):
        meta = {'status': 'mined', 'opened': '2026-10-22', 'used_by': ENTRY_STEM, 'tier': 'A'}
        meta.update(sources_meta.get(sid, {}))
        digest = hashlib.sha256(files[snapshots[sid]].encode('utf-8')).hexdigest()
        anchor = meta.pop('anchor', 'raw bytes sha256 %s' % digest)
        rows.append('| %s | source %s | docs | %s | scope | %s | teaches | %s | %s | 90d | %s |\n'
                    % (sid, sid, meta['tier'], anchor, meta['status'], meta['opened'],
                       meta['used_by']))
    files[SOURCES] = REGISTRY_HEAD + ''.join(rows)

    if lesson is None:
        head = ('# Round 26 — lesson\n'
                '\n'
                '## Gate\n'
                '\n'
                'Candidates considered: the btrfs-progs v7.1 documentation, the Linux v7.2\n'
                'kernel sources, the smartmontools 7.5 nvmeprint source and the NVMe SMART\n'
                'health log page.  Every quote below was re-checked against the committed\n'
                'snapshot bytes.\n'
                '\n'
                '| Source | URL | Opened | Located quote (at most 25 words) | Location |\n'
                '|---|---|---|---|---|\n')
        body = []
        for index, sid in enumerate(FIXTURE_SOURCES):
            if sid in gate_drop:
                continue
            quote = gate_quotes_map.get(sid, FIXTURE_QUOTES[index])
            body.append('| %s | https://example.invalid/%s | 2026-10-22 | "%s" | lines 1-2 |\n'
                        % (sid, sid, quote))
        files[LESSON] = head + ''.join(body) + '\n'
    else:
        files[LESSON] = lesson

    if skill is None:
        skill = ('# SKILL\n'
                 '\n'
                 '## Storage integrity — round 26\n'
                 '\n'
                 '| Row | Verdict | Action |\n'
                 '|---|---|---|\n')
        for row_id in ROW_IDS:
            skill += '| %s | HEALTHY | record the reading |\n' % row_id
        skill += ('\n'
                  '## Round 25 decision table\n'
                  '\n'
                  '| Row | Verdict | Action |\n'
                  '|---|---|---|\n')
    files[SKILL] = skill

    if entry_md is None:
        entry_md = '# Storage health — round 26\n\n'
        for row_id in ROW_IDS:
            entry_md += '## %s\n\nstatement for %s\n\n' % (row_id, row_id)
    files[ENTRY_MD] = entry_md

    if entry is None:
        if entry_rows is None:
            entry_rows = []
            for index, row_id in enumerate(ROW_IDS):
                sid = FIXTURE_SOURCES[index]
                entry_rows.append({
                    'id': row_id,
                    'statement': 'statement text for %s' % row_id,
                    'verdict': 'HEALTHY',
                    'action': 'record the reading',
                    'sources': [sid],
                    'quotes': [{'source': sid,
                                'quote': entry_quotes.get(sid, FIXTURE_QUOTES[index])}],
                    'capture_pointers': [{'line': FIXTURE_POINTER_LINE,
                                           'token': FIXTURE_POINTER_TOKEN}],
                    'notes': 'note for %s' % row_id,
                })
        entry = {'schema': SCHEMA_PREFIX + '-v1', 'entry': ENTRY_MD,
                 'capture': {'path': CAPTURE, 'sha256': capture_sha},
                 'rows': entry_rows}
    files[ENTRY] = entry_json_text if entry_json_text is not None else json.dumps(entry)
    files[CAPTURE] = capture
    for path in drop:
        files.pop(path, None)
    return files, capture_sha


def run_fixture(files, expect):
    """Commit a fixture into a throwaway repository and evaluate it there."""
    with tempfile.TemporaryDirectory(prefix='tsukuroi-sh-st-') as tmp:
        repo = Path(tmp) / 'repo'
        env = dict(_revision.clean_env())
        subprocess.run(['git', 'init', '--quiet', '--initial-branch=master', str(repo)],
                       check=True, env=env)
        for path, content in files.items():
            target = repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        subprocess.run(['git', '-C', str(repo), 'add', '-A'], check=True, env=env)
        subprocess.run(['git', '-C', str(repo), '-c', 'user.name=selftest',
                        '-c', 'user.email=selftest@invalid', '-c', 'commit.gpgsign=false',
                        'commit', '--quiet', '-m', 'fixture'], check=True, env=env)
        sha = subprocess.run(['git', '-C', str(repo), 'rev-parse', 'HEAD'],
                             stdout=subprocess.PIPE, check=True, env=env).stdout.decode().strip()
        code, result = evaluate(GitReader(repo, sha), expect['capture_sha'])
        blocking = sorted({f['id'] for f in result.get('findings', []) if f.get('blocking')})
        want = sorted(expect.get('findings', []))
        ok = (code == expect.get('exit', 1)
              and result.get('verified_rows') == expect.get('verified_rows')
              and blocking == want)
        return {'exit': code, 'verified_rows': result.get('verified_rows'),
                'findings': blocking, 'want': want, 'pass': ok}


def selftest():
    """Hermetic cases over throwaway git repositories; no lane byte is touched."""
    cases = []

    def case(name, files, expect):
        expect = dict(expect)
        if 'capture_sha' not in expect:
            expect['capture_sha'] = hashlib.sha256(FIXTURE_CAPTURE.encode('utf-8')).hexdigest()
        cases.append((name, files, expect))

    def entry_case(mutate_rows=None, **kwargs):
        """The base fixture with one mutation of the entry rows."""
        files, sha = build_fixture()
        entry = json.loads(files[ENTRY])
        if mutate_rows is not None:
            mutate_rows(entry)
        files[ENTRY] = json.dumps(entry)
        return files, sha

    def row_mutator(row_id, mutate):
        def apply(entry):
            for row in entry['rows']:
                if row['id'] == row_id:
                    mutate(row)
        return apply

    # 1. the passing fixture
    files, sha = build_fixture()
    case('clean-pass', files, {'exit': 0, 'verified_rows': 6, 'findings': []})

    # 2. a duplicate row id is an error, never a second count
    files, sha = entry_case(row_mutator('SH6', lambda r: r.__setitem__('id', 'SH1')))
    case('duplicate-row-id', files,
         {'exit': 1, 'verified_rows': 0,
          'findings': ['SH-ROW-ID-DUPLICATE', 'SH-ROW-SET']})

    # 3. a missing verdict
    files, sha = entry_case(row_mutator('SH2', lambda r: r.pop('verdict', None)))
    case('verdict-missing', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-VERDICT-MISSING']})

    # 4. a verdict outside the fixed vocabulary
    files, sha = entry_case(row_mutator('SH2', lambda r: r.__setitem__('verdict', 'healthy')))
    case('verdict-invalid', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-VERDICT-INVALID']})

    # 5. a cited source that is not mined
    files, sha = build_fixture(sources_meta={'S128': {'status': 'queued'}})
    case('source-not-mined', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SOURCE-STATUS-NOT-MINED']})

    # 6. a cited source opened on another day
    files, sha = build_fixture(sources_meta={'S129': {'opened': '2026-10-19'}})
    case('source-opened-wrong', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SOURCE-OPENED-WRONG']})

    # 7. a cited source whose used-by names another entry
    files, sha = build_fixture(sources_meta={'S130': {'used_by': 'corpus/knowledge/other.md'}})
    case('source-used-by-missing', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SOURCE-USED-BY-MISSING']})

    # 8. a row whose cited sources are all tier B
    files, sha = build_fixture(sources_meta={'S131': {'tier': 'B'}})
    case('source-no-tier-a', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SOURCE-TIER-MISSING']})

    # 9. a quote of more than 25 words, carried by the snapshot and the Gate table
    long_quote = ' '.join(['word%d' % n for n in range(26)])
    files, sha = build_fixture(snapshot_quotes={'S128': long_quote},
                                gate_quotes_map={'S128': long_quote},
                                entry_quotes={'S128': long_quote})
    case('quote-too-long', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-QUOTE-TOO-LONG']})

    # 10. a quote that is not in the committed snapshot
    files, sha = build_fixture(snapshot_quotes={
        'S128': 'the counted line carries other text entirely'})
    case('quote-not-in-snapshot', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-QUOTE-NOT-IN-SNAPSHOT']})

    # 11. a snapshot whose digest is not written in the registry anchor
    files, sha = build_fixture()
    digest = hashlib.sha256(files['%s/S128.rst' % SOURCE_DIR].encode('utf-8')).hexdigest()
    files[SOURCES] = files[SOURCES].replace(digest, 'f' * 64)
    case('snapshot-digest-not-in-anchor', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SNAPSHOT-DIGEST-NOT-IN-ANCHOR']})

    # 12. a quote the lesson Gate table does not carry for that source
    files, sha = build_fixture(gate_drop=('S128',))
    case('gate-quote-missing', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-GATE-QUOTE-MISSING']})

    # 13. a capture whose bytes are not the pinned ones
    files, sha = build_fixture()
    files[CAPTURE] = files[CAPTURE] + 'an extra line\n'
    case('capture-digest-changed', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-CAPTURE-DIGEST-MISMATCH']})

    # 14. a capture pointer onto a `### ` section header
    files, sha = entry_case(row_mutator(
        'SH1', lambda r: r.__setitem__('capture_pointers', [{'line': 1, 'token': 'header'}])))
    case('pointer-on-header', files,
         {'exit': 1, 'verified_rows': 5,
          'findings': ['SH-CAPTURE-POINTER-HEADER', 'SH-CAPTURE-POINTER-UNUSABLE']})

    # 15. a capture pointer onto a `$ ` command echo
    files, sha = entry_case(row_mutator(
        'SH1', lambda r: r.__setitem__('capture_pointers',
                                       [{'line': 2, 'token': 'cat /proc/mounts'}])))
    case('pointer-on-echo', files,
         {'exit': 1, 'verified_rows': 5,
          'findings': ['SH-CAPTURE-POINTER-ECHO', 'SH-CAPTURE-POINTER-UNUSABLE']})

    # 16. a capture pointer onto an `[exit ` line
    files, sha = entry_case(row_mutator(
        'SH1', lambda r: r.__setitem__('capture_pointers', [{'line': 4, 'token': '[exit 0]'}])))
    case('pointer-on-exit', files,
         {'exit': 1, 'verified_rows': 5,
          'findings': ['SH-CAPTURE-POINTER-EXIT', 'SH-CAPTURE-POINTER-NOT-UNIQUE',
                       'SH-CAPTURE-POINTER-UNUSABLE']})

    # 17. a capture pointer onto a line that occurs twice
    files, sha = entry_case(row_mutator(
        'SH1', lambda r: r.__setitem__('capture_pointers',
                                       [{'line': 19, 'token': 'duplicate marker line'}])))
    case('pointer-on-duplicate-line', files,
         {'exit': 1, 'verified_rows': 5,
          'findings': ['SH-CAPTURE-POINTER-NOT-UNIQUE', 'SH-CAPTURE-POINTER-UNUSABLE']})

    # 18. a SKILL.md row that is missing
    files, sha = build_fixture()
    files[SKILL] = files[SKILL].replace('| SH3 | HEALTHY | record the reading |\n', '')
    case('skill-row-missing', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SKILL-ROW-MISSING']})

    # 19. a SKILL.md row that sits outside the storage-integrity section
    files, sha = build_fixture()
    files[SKILL] = (files[SKILL].replace('| SH3 | HEALTHY | record the reading |\n', '')
                    + '\n## Round 26 addendum\n\n'
                      '| Row | Verdict | Action |\n|---|---|---|\n'
                      '| SH3 | HEALTHY | record the reading |\n')
    case('skill-row-outside-section', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SKILL-ROW-MISSING']})

    # 20. a lesson prose line that crashed the round-25 checker
    files, sha = build_fixture()
    files[LESSON] = files[LESSON] + (
        '\nS128 was opened on 2026-10-22 and its quote is located in the snapshot.\n'
        'The next line is prose that carries a pipe: | S128 | prose without a quote column |\n')
    case('lesson-prose-line-no-crash', files,
         {'exit': 0, 'verified_rows': 6, 'findings': []})

    # 20b. a prose line inside the Gate table that carries a pipe but no quote
    # column: the tool does not crash, it reports the missing quote with a
    # stable finding id and the other five rows still verify
    files, sha = build_fixture()
    files[LESSON] = files[LESSON].replace(
        '| S128 | https://example.invalid/S128 | 2026-10-22 | "%s" | lines 1-2 |' % FIXTURE_QUOTES[0],
        '| S128 | the located quote is in the snapshot, opened 2026-10-22 |')
    case('lesson-prose-line-replaces-gate-row', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-GATE-QUOTE-MISSING']})

    # 21. a Gate table row that cannot be read
    files, sha = build_fixture()
    files[LESSON] = files[LESSON].replace(
        '| S129 | https://example.invalid/S129 | 2026-10-22 | "%s" | lines 1-2 |'
        % FIXTURE_QUOTES[1], '| S129 | https://example.invalid/S129 |')
    case('gate-row-malformed', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-GATE-QUOTE-MISSING']})

    # 22. a missing snapshot for a cited source
    files, sha = build_fixture(drop=('%s/S130.rst' % SOURCE_DIR,))
    case('snapshot-missing', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SNAPSHOT-MISSING']})

    # 23. a missing entry
    files, sha = build_fixture()
    files.pop(ENTRY)
    case('entry-missing', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-ENTRY-MISSING']})

    # 24. a malformed entry
    files, sha = build_fixture(entry_json_text='{"schema": "%s", ' % SCHEMA_PREFIX)
    case('entry-malformed', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-ENTRY-MALFORMED']})

    # 25. a missing entry markdown
    files, sha = build_fixture()
    files.pop(ENTRY_MD)
    case('entry-markdown-missing', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-ENTRY-MD-MISSING']})

    # 26. a missing lesson
    files, sha = build_fixture()
    files.pop(LESSON)
    case('lesson-missing', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-LESSON-MISSING']})

    # 27. a missing registry
    files, sha = build_fixture()
    files.pop(SOURCES)
    case('sources-missing', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-SOURCES-MISSING']})

    # 28. a missing capture
    files, sha = build_fixture()
    files.pop(CAPTURE)
    case('capture-missing', files,
         {'exit': 2, 'verified_rows': 0, 'findings': ['SH-CAPTURE-MISSING']})

    # 29. a SKILL.md without the storage-integrity section at all
    files, sha = build_fixture()
    files[SKILL] = ('# SKILL\n\n## Round 25 decision table\n\n'
                    '| Row | Verdict | Action |\n|---|---|---|\n')
    case('skill-section-missing', files,
         {'exit': 1, 'verified_rows': 0,
          'findings': ['SH-SKILL-SECTION-MISSING', 'SH-SKILL-ROW-MISSING']})

    # 30. a lesson whose Gate table has no `Located quote` column
    files, sha = build_fixture(lesson=(
        '# Round 26 — lesson\n\n## Gate\n\n'
        '| Source | URL | Opened |\n|---|---|---|\n'
        '| S128 | https://example.invalid/S128 | 2026-10-22 |\n'))
    case('gate-header-missing', files,
         {'exit': 1, 'verified_rows': 0,
          'findings': ['SH-GATE-HEADER-MISSING', 'SH-GATE-QUOTE-MISSING']})

    # 31. a row whose verdict is outside the fixed vocabulary
    files, sha = build_fixture()
    entry = json.loads(files[ENTRY])
    entry['rows'][2]['verdict'] = 'UNVERIFIED'
    files[ENTRY] = json.dumps(entry)
    case('verdict-unverified-allowed', files,
         {'exit': 0, 'verified_rows': 6, 'findings': []})

    # 32. an entry that declares a capture digest other than the pinned one
    files, sha = build_fixture()
    entry = json.loads(files[ENTRY])
    entry['capture']['sha256'] = '0' * 64
    files[ENTRY] = json.dumps(entry)
    case('declared-capture-digest-mismatch', files,
         {'exit': 1, 'verified_rows': 0, 'findings': ['SH-CAPTURE-PIN-DIGEST']})

    # 33. a row with no capture pointer at all
    files, sha = entry_case(row_mutator('SH4', lambda r: r.__setitem__('capture_pointers', [])))
    case('capture-pointer-missing', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-CAPTURE-POINTER-MISSING']})

    # 34. a row whose statement is empty
    files, sha = entry_case(row_mutator('SH5', lambda r: r.__setitem__('statement', '  ')))
    case('statement-empty', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-STATEMENT-EMPTY']})

    # 35. a row whose action is empty
    files, sha = entry_case(row_mutator('SH5', lambda r: r.__setitem__('action', '')))
    case('action-empty', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-ACTION-EMPTY']})

    # 36. a seventh row repeating SH1: the duplicate never counts a second time
    files, sha = build_fixture()
    entry = json.loads(files[ENTRY])
    extra = dict(entry['rows'][0])
    extra['notes'] = 'a repeated row'
    entry['rows'].append(extra)
    files[ENTRY] = json.dumps(entry)
    case('duplicate-row-id-seven-rows', files,
         {'exit': 1, 'verified_rows': 0, 'findings': ['SH-ROW-ID-DUPLICATE']})

    # 37. a Gate quote that itself contains a pipe is read whole
    pipe_quote = FIXTURE_QUOTES[0] + ' | with a pipe'
    files, sha = build_fixture(snapshot_quotes={'S128': pipe_quote},
                                gate_quotes_map={'S128': pipe_quote},
                                entry_quotes={'S128': pipe_quote})
    case('gate-quote-with-pipe', files,
         {'exit': 0, 'verified_rows': 6, 'findings': []})

    # 38. two located quotes in one Gate cell, separated by `"; `
    second_quote = 'the counters are kept per device until they are reset'
    files, sha = build_fixture(
        snapshot_quotes={'S128': FIXTURE_QUOTES[0] + '\n' + second_quote},
        entry_quotes={'S128': FIXTURE_QUOTES[0]})
    lesson = files[LESSON].replace(
        '| S128 | https://example.invalid/S128 | 2026-10-22 | "%s" | lines 1-2 |' % FIXTURE_QUOTES[0],
        '| S128 | https://example.invalid/S128 | 2026-10-22 | "%s"; "%s" | lines 1-2 |'
        % (FIXTURE_QUOTES[0], second_quote))
    files[LESSON] = lesson
    case('gate-two-quotes-one-cell', files,
         {'exit': 0, 'verified_rows': 6, 'findings': []})

    # Round 27, QUALITY 64 (R26-GATE-COLUMN-OFFSET): an unquoted and a
    # backticked located-quote cell are found; a quote only in the Location
    # cell is not read as the located quote.
    gate_line = ('| S128 | https://example.invalid/S128 | 2026-10-22 | "%s" | lines 1-2 |'
                 % FIXTURE_QUOTES[0])
    for shape, cell in (('unquoted', FIXTURE_QUOTES[0]),
                        ('backticks', '`%s`' % FIXTURE_QUOTES[0])):
        files, sha = build_fixture()
        files[LESSON] = files[LESSON].replace(
            gate_line, '| S128 | https://example.invalid/S128 | 2026-10-22 | %s | lines 1-2 |' % cell)
        case('gate-cell-%s' % shape, files, {'exit': 0, 'verified_rows': 6, 'findings': []})
    files, sha = build_fixture()
    files[LESSON] = files[LESSON].replace(
        gate_line, '| S128 | https://example.invalid/S128 | 2026-10-22 | 2026-10-22 | "%s" |'
        % FIXTURE_QUOTES[0])
    case('gate-quote-in-location-cell', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-GATE-QUOTE-MISSING']})

    # 39. two snapshots for the same source id: the snapshot is not unique
    files, sha = build_fixture()
    files['%s/S128.txt' % SOURCE_DIR] = files['%s/S128.rst' % SOURCE_DIR]
    case('snapshot-ambiguous', files,
         {'exit': 1, 'verified_rows': 5, 'findings': ['SH-SNAPSHOT-AMBIGUOUS']})

    # 40. the alternate quote and pointer key names are read on their merits
    files, sha = build_fixture()
    entry = json.loads(files[ENTRY])
    for row in entry['rows']:
        row['quotes'] = [{'source_id': row['quotes'][0]['source'],
                          'text': row['quotes'][0]['quote']}]
        row['capture_pointers'] = [{'line': FIXTURE_POINTER_LINE,
                                    'contains': FIXTURE_POINTER_TOKEN}]
    files[ENTRY] = json.dumps(entry)
    case('alternate-key-names', files,
         {'exit': 0, 'verified_rows': 6, 'findings': []})

    observations = []
    for name, case_files, expect in cases:
        try:
            observations.append(dict(case=name, **run_fixture(case_files, expect)))
        except Exception as exc:  # a broken fixture is a failed case, not a crash
            observations.append({'case': name, 'exit': None, 'verified_rows': None,
                                 'findings': [], 'want': [], 'pass': False,
                                 'error': str(exc)[:160]})
    failed = sum(1 for obs in observations if not obs['pass'])
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations),
                      'failed': failed, 'observations': observations}, sort_keys=True))
    return int(bool(failed))


# -------------------------------------------------------------------- main


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--revision')
    mode.add_argument('--selftest', action='store_true')
    parser.add_argument('--repo', default=str(ROOT),
                        help='the repository to read at the revision (default: the one holding this script)')
    parser.add_argument('--branch', default='master')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    repo = Path(args.repo).resolve()
    try:
        binding = _revision.bind(repo, args.revision, args.branch)
    except _revision.RevisionError as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE',
                          'findings': [{'id': exc.fid, 'site': exc.site}]}))
        return 2
    code, result = evaluate(GitReader(repo, binding.sha))
    result.update(revision=binding.sha, branch=binding.branch,
                  status=('PASS', 'FAIL', 'CANNOT_EVALUATE')[code])
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
