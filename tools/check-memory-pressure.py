#!/usr/bin/env python3
"""Count verified rows in the round-25 memory-pressure / systemd-oomd entry.

The C2 claim is "6 verified rows, MP1 to MP6, exit 0" over the committed bytes
of one revision.  A row counts only when every one of these rules holds:

  R1  the row carries a non-empty `statement`, `verdict` and `action`
  R2  every source the row lists is a `mined` row of corpus/SOURCES.md whose
      `used-by` names corpus/knowledge/memory-pressure-r25.md and that was
      either opened 2026-10-22 or has its `recheck` cell changed in place this
      round with the change logged old -> new in corpus/lessons/round-25.md
  R2b at least one source the row lists is a tier-A row of corpus/SOURCES.md
  R3  every Gate quote the row's sources carry in that lesson's Gate is at
      most 25 words, and every quote the row carries is the quote that Gate
      records for the source the row names; a mismatch, or a quote that names
      a source the row does not list, blocks the row
  R4  at least one capture pointer resolves to a line of the pinned capture
      whose text is unique in the capture, is not a `### ` header, a `$ `
      command echo or an `[exit ` line, holds at least one letter or digit,
      and contains the pointer's declared token (case-sensitive, >= 3 chars)
  R5  SKILL.md's section "## Memory pressure and systemd-oomd — round 25"
      carries a table line whose FIRST cell names the row id
  R6  the entry carries each of MP1 to MP6 exactly once; a repeated row id is
      an error of the entry, not a row

Every input is read through git at the bound revision; nothing on the host is
probed and no working-tree byte of the measured revision is consulted.  The
capture digest is verified before anything else is read: a capture whose
sha256 is not the pinned one cannot be evaluated and exits 2 with
CAPTURE-TAMPERED.

Exit codes: 0 when verified_rows == 6, 1 when it is below, 2 when the entry
cannot be evaluated (ENTRY-MISSING, ENTRY-MALFORMED, ENTRY-SCHEMA,
LESSON-MISSING, SOURCES-MISSING, SKILL-MISSING, CAPTURE-MISSING,
CAPTURE-TAMPERED, or a revision binding refusal).  The exit code is derived
from verified_rows alone: a blocking finding that is not attached to a row
(the row id set is wrong, the entry declares a capture that is not the pinned
one) sets verified_rows to 0, so exit 0 and verified_rows == 6 always agree.

Scope: a count of evidence links in committed bytes.  It does not re-measure
the host, does not decide whether memory pressure is healthy, and does not
authorize any service, package or boot action.
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

ENTRY = 'corpus/knowledge/memory-pressure-r25.json'
ENTRY_MD = 'corpus/knowledge/memory-pressure-r25.md'
ENTRY_STEM = 'corpus/knowledge/memory-pressure-r25'
SOURCES = 'corpus/SOURCES.md'
LESSON = 'corpus/lessons/round-25.md'
SKILL = 'SKILL.md'
CAPTURE = '.ufo/waves/round-25/capture/capture.txt'
CAPTURE_SHA256 = 'e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136'
SCHEMA = 'tsukuroi-memory-pressure-r25-v1'
ROW_IDS = ('MP1', 'MP2', 'MP3', 'MP4', 'MP5', 'MP6')
ROUND_DATE = '2026-10-22'
MAX_QUOTE_WORDS = 25
MIN_TOKEN_CHARS = 3
TIER_A = 'A'
SKILL_SECTION = 'Memory pressure and systemd-oomd — round 25'

CELL_SPLIT = re.compile(r'(?<!\\)\|')
SOURCE_ROW = re.compile(r'^\|\s*(S\d{3})\s*\|')
ID_TOKEN = re.compile(r'S\d{3}')
HEADING = re.compile(r'^#{1,6}\s')
ARROW = re.compile(r'(?:→|->)')


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


def git_reader(repo, sha):
    """Read a path at a revision as bytes, through git only."""
    def read(path):
        if not isinstance(path, str) or not path or path.startswith('/'):
            return None
        if '..' in path.split('/'):
            return None
        proc = subprocess.run(['git', '--no-pager', '-C', str(repo), 'show', '%s:%s' % (sha, path)],
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=_revision.clean_env(), timeout=30)
        return proc.stdout if proc.returncode == 0 else None
    return read


def decode(raw):
    if raw is None:
        return None
    return raw.decode('utf-8', 'surrogateescape')


def split_cells(line):
    """Split a markdown table row, honouring backslash-escaped pipes."""
    return [c.strip() for c in CELL_SPLIT.split(line.strip().strip('|'))]


def cell_spans(line):
    """Split a table row into (start, end, text) spans over the raw line.

    A pipe that a backslash escapes does not separate cells, so the split is
    the same one `split_cells` performs; the offsets are kept so that a
    quoted value spanning a pipe can still be located in the raw line.
    """
    spans = []
    start = 0
    for match in CELL_SPLIT.finditer(line):
        text = line[start:match.start()]
        spans.append((start, match.start(), text.strip()))
        start = match.end()
    spans.append((start, len(line), line[start:].strip()))
    return spans


SEPARATED_QUOTES = re.compile(r'"\s*;\s')
BACKTICK_SPAN = re.compile(r'`([^`]*)`')


def straight_quote_spans(text):
    """The double-quoted spans of a cell.

    A located quote may itself contain double quotes (`The "some" line ...`),
    and one cell may hold several located quotes separated by `"; `.  When the
    cell separates them, the quotes pair from the left; otherwise the outermost
    pair is the located quote and the inner ones belong to its text.
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

    A backtick-delimited span wins over a straight-quoted one, because the
    lane writes a quote that contains double quotes inside backticks.
    """
    out = []
    for match in BACKTICK_SPAN.finditer(line):
        out.append((match.start(), match.end(), match.group(1).strip()))
    for start, end, content in straight_quote_spans(line):
        if not any(s <= start and end <= e for s, e, _ in out):
            out.append((start, end, content))
    out.sort()
    return out


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


def parse_block(block):
    rows = []
    for line in block:
        cells = split_cells(line)
        if is_separator(cells):
            continue
        rows.append(cells)
    return rows


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


def has_quote_mark(text):
    return '`' in text or '“' in text or '"' in text


def word_count(text):
    return len((text or '').split())


def first_id(cells):
    """The first S-id of a table row: the one in the first cell, else a lone cell."""
    for cell in cells[:1]:
        found = ID_TOKEN.findall(cell)
        if found:
            return found[0]
    for cell in cells:
        if re.fullmatch(r'S\d{3}', cell):
            return cell
    return None


# ------------------------------------------------------------------ inputs


def source_header(text):
    """The column names of the registry header, as {name: index}.

    The registry is an 11-column table; a row that carries fewer cells is
    read by its header names where it has them, so a draft that drops a
    column is read as a missing cell rather than as a shifted cell.
    """
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
    """Map S### -> {status, opened, recheck, used_by} from the registry."""
    out, dups = {}, set()
    header = source_header(text)
    for line in (text or '').splitlines():
        match = SOURCE_ROW.match(line)
        if not match:
            continue
        cells = split_cells(line)
        sid = match.group(1)
        if sid in out:
            dups.add(sid)
            continue
        if header:
            def cell(name):
                index = header.get(name)
                return cells[index].strip() if index is not None and index < len(cells) else ''
            info = {'status': cell('status'), 'opened': cell('opened'),
                    'recheck': cell('recheck'), 'used_by': cell('used-by'),
                    'tier': cell('tier')}
        else:
            if len(cells) < 11:
                continue
            info = {'status': cells[7].strip(), 'opened': cells[8].strip(),
                    'recheck': cells[9].strip(), 'used_by': cells[10].strip(),
                    'tier': cells[3].strip()}
        out[sid] = info
    return out, dups


def gate_quotes(text):
    """Map S### -> [quote text] from the Gate section of the lesson.

    A Gate table row names its source in the first cell and carries the
    located quote under the column whose header mentions "quote".  A Gate
    line that is not part of a table is read as a source id plus a quoted
    span, so the lesson may be written either way.
    """
    out = {}
    for title, lines in sections(text):
        if not title or 'gate' not in title.lower():
            continue
        for block in raw_table_blocks(lines):
            if not block:
                continue
            header = split_cells(block[0])
            quote_col = None
            for index, cell in enumerate(header):
                if 'quote' in cell.lower():
                    quote_col = index
                    break
            body = block[1:] if quote_col is not None else block
            for raw in body:
                cells = split_cells(raw)
                sid = first_id(cells)
                if not sid:
                    continue
                spans = cell_spans(raw)
                quote = None
                if quote_col is not None and quote_col < len(spans):
                    start = spans[quote_col][0]
                    for span_start, _span_end, content in quoted_spans(raw):
                        if span_start >= start:
                            quote = content
                            break
                if quote is None:
                    for _span_start, _span_end, content in quoted_spans(raw):
                        if content:
                            quote = content
                            break
                if quote:
                    out.setdefault(sid, []).append(quote)
        for line in lines:
            if line.strip().startswith('|'):
                continue
            sid = first_id([line])
            if not sid:
                continue
            quote = extract_quote(line)
            if quote and quote != line.strip() and has_quote_mark(line):
                out.setdefault(sid, []).append(quote)
    return out


def recheck_log(text):
    """Map S### -> (old, new) from the lesson's old -> new recheck log.

    A log line names its source and shows the change as `old -> new` next to
    the word "recheck"; the new value must equal the `recheck` cell of that
    source in corpus/SOURCES.md, which is what makes it an in-place update.
    The table form `| S116 | recheck | 90d | 30d |`, the one-cell arrow form
    `| S116 | recheck | 90d -> 30d |` and the prose form
    `S116 recheck: 90d -> 30d` are all read.
    """
    out = {}
    for line in (text or '').splitlines():
        if 'recheck' not in line.lower():
            continue
        sid = first_id([line])
        if not sid:
            continue
        head = line.lower().rfind('recheck')
        tail = line[head + len('recheck'):]
        old = new = None
        arrow = ARROW.search(tail)
        if arrow:
            left = ID_TOKEN.sub(' ', tail[:arrow.start()]).replace('|', ' ').split()
            right = tail[arrow.end():].replace('|', ' ').split()
            if left and right:
                old, new = left[-1], right[0]
        else:
            cells = split_cells(line) if line.strip().startswith('|') else []
            if len(cells) >= 4 and cells[1].lower() == 'recheck':
                old, new = cells[2].strip(), cells[3].strip()
        if old is None or new is None:
            # A prose line that names a source and the word "recheck" but shows no
            # old -> new change is not a recheck log entry.  It is skipped, never
            # a crash: the tool read such a line at c93bd70f and died on it.
            continue
        old, new = old.strip('`"()'), new.strip('`"()')
        if not old or not new or old == new:
            continue
        if old.lower() in ('old', 'recheck') or new.lower() in ('new', 'recheck'):
            continue
        out[sid] = (old, new)
    return out


def skill_rows(text, title=SKILL_SECTION):
    """The table lines of one named section of SKILL.md.

    The section runs from the heading that names it to the next heading of the
    same or a higher level, so a row id counts only when the row's own decision
    table lives in the round's section and not in some other registry table.
    """
    wanted = normalise_title(title)
    out = []
    inside = False
    level = 0
    for line in (text or '').splitlines():
        match = HEADING.match(line)
        if match:
            depth = len(line) - len(line.lstrip('#'))
            if inside and depth <= level:
                inside = False
            elif not inside and normalise_title(line.lstrip('#').strip()) == wanted:
                inside = True
                level = depth
            continue
        if inside and line.strip().startswith('|'):
            out.append(line)
    return out


def normalise_title(title):
    """Collapse whitespace and unify the dash family of a heading title."""
    text = re.sub(r'\s+', ' ', (title or '')).strip()
    for dash in ('—', '–', '‒', '−'):
        text = text.replace(dash, '-')
    return text


def skill_first_cells(text, title=SKILL_SECTION):
    """The first cell of every table line of the named SKILL.md section."""
    out = []
    for line in skill_rows(text, title):
        cells = split_cells(line)
        if cells:
            out.append(cells[0])
    return out


def id_in_line(line, row_id):
    return re.search(r'(?<![A-Za-z0-9])%s(?![0-9])' % re.escape(row_id), line) is not None


# ----------------------------------------------------------------- capture


def pointer_token(pointer):
    """The declared token of a capture pointer.

    `token` is the canonical key; `contains` is read as the same field so an
    entry cut against either naming is evaluated on its merits.
    """
    token = pointer.get('token')
    if token is None:
        token = pointer.get('contains')
    return token


def pointer_findings(pointer, capture_lines):
    """Findings for one capture pointer; an empty list means the pointer counts."""
    if not isinstance(pointer, dict):
        return ['MP-CAPTURE-POINTER-SHAPE']
    line = pointer.get('line')
    token = pointer_token(pointer)
    path = pointer.get('path')
    problems = []
    if path is not None and path != CAPTURE:
        problems.append('MP-CAPTURE-POINTER-PATH')
    if type(line) is not int or not isinstance(token, str):
        problems.append('MP-CAPTURE-POINTER-SHAPE')
        return problems
    if len(token) < MIN_TOKEN_CHARS:
        problems.append('MP-CAPTURE-POINTER-TOKEN-SHORT')
    if not 1 <= line <= len(capture_lines):
        problems.append('MP-CAPTURE-POINTER-LINE-RANGE')
        return problems
    text = capture_lines[line - 1]
    if text.startswith('### '):
        problems.append('MP-CAPTURE-POINTER-HEADER')
    if text.startswith('$ '):
        problems.append('MP-CAPTURE-POINTER-ECHO')
    if text.startswith('[exit '):
        problems.append('MP-CAPTURE-POINTER-EXIT')
    if not re.search(r'[A-Za-z0-9]', text):
        problems.append('MP-CAPTURE-POINTER-BLANK')
    if capture_lines.count(text) != 1:
        problems.append('MP-CAPTURE-POINTER-NOT-UNIQUE')
    if token not in text:
        problems.append('MP-CAPTURE-POINTER-TOKEN-ABSENT')
    return problems


# ---------------------------------------------------------------- evaluate


def rule_of(row_findings, ids):
    """Per-rule view of one row's findings."""
    hits = [f for f in row_findings if f['id'] in ids]
    return {'ok': not [f for f in hits if f['blocking']], 'findings': hits}


def evaluate(read, expected_capture_sha=CAPTURE_SHA256):
    """Evaluate the entry at the bound revision.  Returns (exit code, result)."""
    findings = []

    def note(fid, site, blocking=True):
        findings.append({'id': fid, 'site': site, 'blocking': blocking})

    def cannot(fid, site):
        note(fid, site)
        return 2, {'status': 'CANNOT_EVALUATE', 'declared_rows': len(ROW_IDS),
                   'verified_rows': 0, 'rows': [], 'findings': findings}

    # The capture digest is verified before anything else is read.
    raw_capture = read(CAPTURE)
    if raw_capture is None:
        return cannot('CAPTURE-MISSING', CAPTURE)
    observed_sha = hashlib.sha256(raw_capture).hexdigest()
    if observed_sha != expected_capture_sha:
        note('CAPTURE-TAMPERED', CAPTURE)
        return 2, {'status': 'CANNOT_EVALUATE', 'declared_rows': len(ROW_IDS),
                   'verified_rows': 0, 'rows': [], 'findings': findings,
                   'capture_sha256_observed': observed_sha}
    capture_lines = raw_capture.decode('utf-8', 'surrogateescape').splitlines()

    raw_entry = read(ENTRY)
    if raw_entry is None:
        return cannot('ENTRY-MISSING', ENTRY)
    try:
        entry = json.loads(decode(raw_entry), object_pairs_hook=unique)
    except ValueError as exc:
        return cannot('ENTRY-MALFORMED', '%s: %s' % (ENTRY, exc))
    if not isinstance(entry, dict) or entry.get('schema') != SCHEMA:
        return cannot('ENTRY-SCHEMA', ENTRY)
    if not isinstance(entry.get('rows'), list):
        return cannot('ENTRY-SCHEMA', ENTRY)

    raw_sources = read(SOURCES)
    if raw_sources is None:
        return cannot('SOURCES-MISSING', SOURCES)
    raw_lesson = read(LESSON)
    if raw_lesson is None:
        return cannot('LESSON-MISSING', LESSON)
    raw_skill = read(SKILL)
    if raw_skill is None:
        return cannot('SKILL-MISSING', SKILL)

    sources, dup_ids = source_rows(decode(raw_sources))
    quotes = gate_quotes(decode(raw_lesson))
    rechecks = recheck_log(decode(raw_lesson))
    skill_table = skill_rows(decode(raw_skill))
    skill_cells = skill_first_cells(decode(raw_skill))

    # The entry's own capture pin must name the pinned capture and its digest.
    global_blocked = False
    declared = entry.get('capture')
    if isinstance(declared, dict):
        if declared.get('path') not in (None, CAPTURE):
            note('MP-CAPTURE-PATH-MISMATCH', str(declared.get('path')))
            global_blocked = True
        if declared.get('sha256') not in (None, observed_sha):
            note('MP-CAPTURE-DECLARED-MISMATCH', str(declared.get('sha256')))
            global_blocked = True
    elif declared not in (None, CAPTURE):
        note('MP-CAPTURE-PATH-MISMATCH', str(declared))
        global_blocked = True

    seen = set()
    duplicate_ids = set()
    rows = []
    for row in entry['rows']:
        row_id = row.get('id') if isinstance(row, dict) else None
        row_findings = []

        def note_row(fid, site, blocking=True):
            row_findings.append({'id': fid, 'site': site, 'blocking': blocking})

        if not isinstance(row, dict):
            note_row('MP-ROW-SHAPE', 'row')
            rows.append({'id': None, 'verified': False, 'findings': row_findings, 'rules': {}})
            continue
        if row_id not in ROW_IDS:
            note_row('MP-ROW-ID-UNKNOWN', str(row_id))
        elif row_id in seen:
            note_row('MP-ROW-ID-DUPLICATE', str(row_id))
            duplicate_ids.add(row_id)
        seen.add(row_id)

        # R1: statement, verdict and action.
        for field, fid in (('statement', 'MP-STATEMENT-EMPTY'), ('verdict', 'MP-VERDICT-EMPTY'),
                           ('action', 'MP-ACTION-EMPTY')):
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                note_row(fid, str(row_id))

        # R2: sources.
        row_sources = row.get('sources')
        source_detail = []
        if not isinstance(row_sources, list) or not row_sources:
            note_row('MP-SOURCES-EMPTY', str(row_id))
            row_sources = []
        for sid in row_sources:
            if not isinstance(sid, str) or sid not in sources:
                note_row('MP-SOURCE-MISSING', str(sid))
                source_detail.append({'id': sid, 'status': None, 'opened': None,
                                      'tier': '',
                                      'used_by_names_entry': False, 'recheck_logged': False,
                                      'qualifies': False})
                continue
            info = sources[sid]
            used_by_ok = ENTRY_STEM in info['used_by']
            opened_ok = info['opened'] == ROUND_DATE
            logged = rechecks.get(sid)
            recheck_ok = bool(logged) and logged[1] == info['recheck'] and logged[0] != logged[1]
            if info['status'] != 'mined':
                note_row('MP-SOURCE-STATUS-NOT-MINED', sid)
            if not used_by_ok:
                note_row('MP-SOURCE-USED-BY-MISSING', sid)
            if sid in dup_ids:
                note_row('MP-SOURCE-DUPLICATE', sid)
            if not opened_ok and not recheck_ok:
                note_row('MP-SOURCE-OPENED-STALE', sid)
            source_detail.append({'id': sid, 'status': info['status'], 'opened': info['opened'],
                                  'tier': info['tier'],
                                  'used_by_names_entry': used_by_ok, 'recheck_logged': recheck_ok,
                                  'qualifies': info['status'] == 'mined' and used_by_ok
                                  and (opened_ok or recheck_ok)})

        # R2b: at least one tier-A source.
        known = [d for d in source_detail if d['status'] is not None]
        if known and not any(d['tier'].upper() == TIER_A for d in known):
            note_row('MP-SOURCE-TIER-NOT-A', str(row_id))

        # R3: the Gate quotes of the row's sources, and the row's own quotes.
        quote_detail = []
        for sid in row_sources:
            gate_texts = quotes.get(sid, [])
            if not gate_texts:
                note_row('MP-QUOTE-MISSING', sid)
            for quote in gate_texts:
                words = word_count(quote)
                quote_detail.append({'source': sid, 'words': words, 'quote': quote})
                if words > MAX_QUOTE_WORDS:
                    # A Gate quote over the word cap is a defect of that source's
                    # Gate record; it blocks every row that cites the source.
                    note_row('MP-QUOTE-TOO-LONG', sid)
        entry_quotes = row.get('quotes')
        if not isinstance(entry_quotes, list):
            note_row('MP-QUOTES-SHAPE', str(row_id))
            entry_quotes = []
        for item in entry_quotes:
            if not isinstance(item, dict):
                note_row('MP-QUOTES-SHAPE', str(row_id))
                continue
            sid, quote = item.get('source'), item.get('quote')
            if not isinstance(sid, str) or not isinstance(quote, str):
                note_row('MP-QUOTES-SHAPE', str(row_id))
                continue
            if sid not in row_sources:
                note_row('MP-QUOTE-SOURCE-UNKNOWN', sid)
            if word_count(quote) > MAX_QUOTE_WORDS:
                note_row('MP-QUOTE-TOO-LONG', sid)
            gate_texts = [norm(q) for q in quotes.get(sid, [])]
            if gate_texts and not any(norm(quote) in text for text in gate_texts):
                note_row('MP-QUOTE-MISMATCH', sid)
        if not quote_detail:
            note_row('MP-QUOTE-MISSING', str(row_id))

        # R4: capture pointers.
        pointers = row.get('capture_pointers')
        pointer_detail = []
        if not isinstance(pointers, list) or not pointers:
            note_row('MP-CAPTURE-POINTER-MISSING', str(row_id))
            pointers = []
        for pointer in pointers:
            pointer_problems = pointer_findings(pointer, capture_lines)
            for fid in pointer_problems:
                note_row(fid, '%s:%s' % (row_id, json.dumps(pointer, sort_keys=True)))
            pointer_detail.append({'pointer': pointer, 'findings': pointer_problems,
                                   'counts': not pointer_problems})
        if pointers and not [p for p in pointer_detail if p['counts']]:
            note_row('MP-CAPTURE-POINTER-UNUSABLE', str(row_id))

        # R5: a SKILL.md table line of the round-25 section whose FIRST cell
        # names the row id.
        skill_hit = bool(row_id) and any(id_in_line(cell, row_id) for cell in skill_cells)
        if not skill_hit:
            note_row('MP-SKILL-ROW-MISSING', str(row_id))

        if row.get('supersedes') is not None and not isinstance(row.get('supersedes'), list):
            note_row('MP-SUPERSEDES-SHAPE', str(row_id), blocking=False)

        verified = not [f for f in row_findings if f['blocking']]
        rules = {
            'R1_statement_verdict_action': rule_of(row_findings, ('MP-STATEMENT-EMPTY',
                                                                 'MP-VERDICT-EMPTY',
                                                                 'MP-ACTION-EMPTY')),
            'R2_sources': rule_of(row_findings, ('MP-SOURCES-EMPTY', 'MP-SOURCE-MISSING',
                                                 'MP-SOURCE-STATUS-NOT-MINED',
                                                 'MP-SOURCE-USED-BY-MISSING',
                                                 'MP-SOURCE-OPENED-STALE',
                                                 'MP-SOURCE-DUPLICATE',
                                                 'MP-SOURCE-TIER-NOT-A')),
            'R3_gate_quote': rule_of(row_findings, ('MP-QUOTE-MISSING', 'MP-QUOTE-TOO-LONG',
                                                    'MP-QUOTE-MISMATCH', 'MP-QUOTE-SOURCE-UNKNOWN',
                                                    'MP-QUOTES-SHAPE')),
            'R4_capture_pointer': rule_of(row_findings, ('MP-CAPTURE-POINTER-MISSING',
                                                         'MP-CAPTURE-POINTER-UNUSABLE',
                                                         'MP-CAPTURE-POINTER-SHAPE',
                                                         'MP-CAPTURE-POINTER-PATH',
                                                         'MP-CAPTURE-POINTER-LINE-RANGE',
                                                         'MP-CAPTURE-POINTER-HEADER',
                                                         'MP-CAPTURE-POINTER-ECHO',
                                                         'MP-CAPTURE-POINTER-EXIT',
                                                         'MP-CAPTURE-POINTER-BLANK',
                                                         'MP-CAPTURE-POINTER-NOT-UNIQUE',
                                                         'MP-CAPTURE-POINTER-TOKEN-ABSENT',
                                                         'MP-CAPTURE-POINTER-TOKEN-SHORT')),
            'R5_skill_row': rule_of(row_findings, ('MP-SKILL-ROW-MISSING',)),
        }
        rows.append({'id': row_id, 'verified': verified, 'findings': row_findings,
                     'rules': rules, 'sources': source_detail, 'quotes': quote_detail,
                     'capture_pointers': pointer_detail, 'skill_row': skill_hit})
        findings.extend(row_findings)

    if seen != set(ROW_IDS):
        note('MP-ROW-SET', ','.join(sorted(str(s) for s in seen)))
        global_blocked = True
    if duplicate_ids:
        # A repeated row id is an error of the entry, not of one row: the count
        # of distinct verified ids would otherwise stay at six.
        note('MP-ROW-ID-DUPLICATE', ','.join(sorted(str(s) for s in duplicate_ids)))
        global_blocked = True

    verified_rows = 0 if global_blocked else sum(
        1 for row in rows if row.get('verified') and row.get('id') in ROW_IDS)
    code = 0 if verified_rows == len(ROW_IDS) else 1
    return code, {'status': ('PASS', 'FAIL')[code], 'declared_rows': len(ROW_IDS),
                  'verified_rows': verified_rows, 'rows': rows, 'findings': findings,
                  'capture_sha256_observed': observed_sha}


# ---------------------------------------------------------------- selftest


FIXTURE_CAPTURE = (
    '### header\n'
    '$ cat /proc/pressure/memory\n'
    'some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384\n'
    'full avg10=0.02 avg60=0.02 avg300=0.06 total=40856373\n'
    '[exit 0]\n'
    '$ cat /sys/fs/cgroup/memory.events\n'
    'oom_kill 0\n'
    '[exit 0]\n'
    '$ cat /sys/fs/cgroup/user.slice/memory.events\n'
    'oom_kill 0\n'
    '[exit 0]\n'
    '\n'
    '$ cat /proc/pressure/memory\n'
    'duplicate marker line\n'
    'duplicate marker line\n'
)

ROW_SOURCE_IDS = ('S115', 'S116', 'S117', 'S118', 'S119', 'S120')
QUOTE_A = 'the memory some line counts stalls'
QUOTE_B = 'the swap used limit default is ninety percent'


def fixture_sources():
    head = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|\n')
    rows = []
    for sid in ROW_SOURCE_IDS:
        rows.append('| %s | source %s | docs | A | scope | anchor | teaches | mined | 2026-10-22 | 90d | '
                    'corpus/knowledge/memory-pressure-r25.md |\n' % (sid, sid))
    # S121 is not mined; S122 names another entry; S123 was opened on another day
    # and has no logged recheck change; S124 was opened on another day and its
    # recheck cell was changed in place this round.
    rows.append('| S121 | source S121 | docs | A | scope | anchor | teaches | queued | 2026-10-22 | 90d | '
                'corpus/knowledge/memory-pressure-r25.md |\n')
    rows.append('| S122 | source S122 | docs | A | scope | anchor | teaches | mined | 2026-10-22 | 90d | '
                'corpus/knowledge/other.md |\n')
    rows.append('| S123 | source S123 | docs | A | scope | anchor | teaches | mined | 2026-10-19 | 90d | '
                'corpus/knowledge/memory-pressure-r25.md |\n')
    rows.append('| S124 | source S124 | docs | A | scope | anchor | teaches | mined | 2026-10-19 | 30d | '
                'corpus/knowledge/memory-pressure-r25.md |\n')
    # S125 is tier B: a sibling entry, not a primary source.
    rows.append('| S125 | source S125 | docs | B | scope | anchor | teaches | mined | 2026-10-22 | 90d | '
                'corpus/knowledge/memory-pressure-r25.md |\n')
    return head + ''.join(rows)


def fixture_lesson():
    head = ('# Round 25 — lesson\n'
            '\n'
            '## Gate\n'
            '\n'
            '| Source | URL | Located quote (at most 25 words) | Opened by |\n'
            '|---|---|---|---|\n')
    rows = []
    for sid in ROW_SOURCE_IDS + ('S121', 'S122', 'S123', 'S124', 'S125', 'S998'):
        rows.append('| %s | https://example.invalid/%s | "%s" | SrcA |\n' % (sid, sid, QUOTE_A))
    tail = ('\n'
            '## Registry recheck log (old -> new)\n'
            '\n'
            '| Source | Cell | Old | New |\n'
            '|---|---|---|---|\n'
            '| S124 | recheck | 90d | 30d |\n')
    return head + ''.join(rows) + tail


FIXTURE_SKILL = (
    '# SKILL\n'
    '\n'
    '## Memory pressure and systemd-oomd — round 25\n'
    '\n'
    '| Row | Verdict | Action |\n'
    '|---|---|---|\n'
    '| MP1 | changed | record |\n'
    '| MP2 | changed | record |\n'
    '| MP3 | changed | record |\n'
    '| MP4 | changed | record |\n'
    '| MP5 | changed | record |\n'
    '| MP6 | changed | record |\n'
    '\n'
    '## Gate and probe registry — round25 superseding current rows\n'
    '\n'
    '| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |\n'
    '|---|---|---|---|---|---|---|---|\n'
    '| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` '
    '| 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid '
    '| `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 '
    '| immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |\n'
)


def fixture_entry(capture_sha, rows=None):
    if rows is None:
        rows = []
        for index, row_id in enumerate(ROW_IDS):
            source = ROW_SOURCE_IDS[index]
            rows.append({
                'id': row_id,
                'statement': 'statement text for %s' % row_id,
                'verdict': 'changed',
                'action': 'record the reading',
                'sources': [source],
                'quotes': [{'source': source, 'quote': QUOTE_A}],
                'capture_pointers': [{'line': 3, 'token': 'total=41385384'}],
                'supersedes': [],
                'notes': 'note for %s' % row_id,
            })
    return {'schema': SCHEMA, 'entry': ENTRY_MD,
            'capture': {'path': CAPTURE, 'sha256': capture_sha},
            'rows': rows}


def run_fixture(files, expect):
    """Commit a fixture into a throwaway repository and evaluate it there."""
    with tempfile.TemporaryDirectory(prefix='tsukuroi-mp-st-') as tmp:
        repo = Path(tmp) / 'repo'
        env = dict(_revision.clean_env())
        subprocess.run(['git', 'init', '--quiet', str(repo)], check=True, env=env)
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
        code, result = evaluate(git_reader(repo, sha), expect['capture_sha'])
        blocking = sorted({f['id'] for f in result.get('findings', []) if f.get('blocking')})
        want = sorted(expect.get('findings', []))
        ok = (code == expect.get('exit', 1)
              and result.get('verified_rows') == expect.get('verified_rows')
              and blocking == want)
        return {'exit': code, 'verified_rows': result.get('verified_rows'),
                'findings': blocking, 'pass': ok}


def selftest():
    """Hermetic cases over throwaway git repositories; no lane byte is touched."""
    base_sha = hashlib.sha256(FIXTURE_CAPTURE.encode('utf-8')).hexdigest()

    def files(over=None):
        out = {CAPTURE: FIXTURE_CAPTURE, SOURCES: fixture_sources(), LESSON: fixture_lesson(),
               SKILL: FIXTURE_SKILL, ENTRY: json.dumps(fixture_entry(base_sha))}
        out.update(over or {})
        return out

    def entry_with(mutate):
        entry = fixture_entry(base_sha)
        mutate(entry)
        return json.dumps(entry)

    def mutate_row(row_id, mutate):
        entry = fixture_entry(base_sha)
        for row in entry['rows']:
            if row['id'] == row_id:
                mutate(row)
        return json.dumps(entry)

    def set_source(row_id, source):
        def mutate(row):
            row['sources'] = [source]
            row['quotes'] = [{'source': source, 'quote': QUOTE_A}]
        return mutate_row(row_id, mutate)

    cases = []

    def case(name, case_files, expect):
        expect = dict(expect)
        expect.setdefault('capture_sha', base_sha)
        cases.append((name, case_files, expect))

    case('clean-pass', files(), {'exit': 0, 'verified_rows': 6, 'findings': []})
    case('source-not-mined', files({ENTRY: set_source('MP1', 'S121')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SOURCE-STATUS-NOT-MINED']})
    case('source-used-by-other-entry', files({ENTRY: set_source('MP1', 'S122')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SOURCE-USED-BY-MISSING']})
    case('source-opened-other-day-without-recheck', files({ENTRY: set_source('MP1', 'S123')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SOURCE-OPENED-STALE']})
    case('source-opened-other-day-with-logged-recheck', files({ENTRY: set_source('MP1', 'S124')}),
        {'exit': 0, 'verified_rows': 6, 'findings': []})
    # S998 has a Gate quote in the lesson but no row in corpus/SOURCES.md.
    case('source-missing', files({ENTRY: set_source('MP1', 'S998')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SOURCE-MISSING']})
    case('no-sources', files({ENTRY: mutate_row('MP1', lambda r: r.__setitem__('sources', []))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-SOURCES-EMPTY', 'MP-QUOTE-MISSING', 'MP-QUOTE-SOURCE-UNKNOWN']})
    long_quote = ' '.join(['word%d' % n for n in range(26)])
    case('quote-too-long', files({
        LESSON: fixture_lesson().replace('"%s"' % QUOTE_A, '"%s"' % long_quote, 1),
        ENTRY: mutate_row('MP1', lambda r: r.__setitem__(
            'quotes', [{'source': ROW_SOURCE_IDS[0], 'quote': long_quote}]))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-QUOTE-TOO-LONG']})
    case('quote-missing', files({
        LESSON: fixture_lesson().replace(
            '| %s | https://example.invalid/%s | "%s" | SrcA |\n' % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0], QUOTE_A),
            '')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-QUOTE-MISSING']})
    case('header-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers', [{'line': 1, 'token': '### header'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-HEADER', 'MP-CAPTURE-POINTER-UNUSABLE']})
    case('echo-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers',
                                       [{'line': 6, 'token': 'cat /sys/fs/cgroup'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-ECHO', 'MP-CAPTURE-POINTER-UNUSABLE']})
    case('exit-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers', [{'line': 5, 'token': '[exit 0]'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-EXIT', 'MP-CAPTURE-POINTER-NOT-UNIQUE',
                      'MP-CAPTURE-POINTER-UNUSABLE']})
    case('duplicate-line-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers',
                                       [{'line': 15, 'token': 'duplicate marker line'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-NOT-UNIQUE', 'MP-CAPTURE-POINTER-UNUSABLE']})
    case('blank-unique-line-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers', [{'line': 12, 'token': 'x y z'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-BLANK', 'MP-CAPTURE-POINTER-TOKEN-ABSENT',
                      'MP-CAPTURE-POINTER-UNUSABLE']})
    case('token-absent-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers',
                                       [{'line': 3, 'token': 'total=99999999'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-TOKEN-ABSENT', 'MP-CAPTURE-POINTER-UNUSABLE']})
    case('token-too-short-pointer', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers', [{'line': 3, 'token': 'so'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-TOKEN-SHORT', 'MP-CAPTURE-POINTER-UNUSABLE']})
    case('pointer-line-out-of-range', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('capture_pointers', [{'line': 999, 'token': 'total'}]))}),
        {'exit': 1, 'verified_rows': 5,
         'findings': ['MP-CAPTURE-POINTER-LINE-RANGE', 'MP-CAPTURE-POINTER-UNUSABLE']})
    # A quoted Gate value may contain a pipe; it is read from the raw line.
    case('gate-quote-with-pipe', files({
        LESSON: fixture_lesson().replace(
            '| %s | https://example.invalid/%s | "%s" | SrcA |\n' % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0], QUOTE_A),
            '| %s | https://example.invalid/%s | "%s | inside" | SrcA |\n'
            % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0], QUOTE_A)),
        ENTRY: mutate_row('MP1', lambda r: r.__setitem__(
            'quotes', [{'source': ROW_SOURCE_IDS[0], 'quote': QUOTE_A + ' | inside'}]))}),
        {'exit': 0, 'verified_rows': 6, 'findings': []})
    case('missing-skill-row', files({SKILL: FIXTURE_SKILL.replace('| MP3 | changed | record |\n', '')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SKILL-ROW-MISSING']})
    case('verdict-empty', files({ENTRY: mutate_row('MP2', lambda r: r.__setitem__('verdict', '  '))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-VERDICT-EMPTY']})
    case('action-empty', files({ENTRY: mutate_row('MP2', lambda r: r.__setitem__('action', ''))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-ACTION-EMPTY']})
    case('statement-empty', files({ENTRY: mutate_row('MP2', lambda r: r.__setitem__('statement', ''))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-STATEMENT-EMPTY']})
    case('capture-digest-tampered', files({CAPTURE: FIXTURE_CAPTURE + 'extra line\n'}),
        {'exit': 2, 'verified_rows': 0, 'findings': ['CAPTURE-TAMPERED']})
    case('capture-missing', {k: v for k, v in files().items() if k != CAPTURE},
        {'exit': 2, 'verified_rows': 0, 'findings': ['CAPTURE-MISSING']})
    case('entry-missing', {k: v for k, v in files().items() if k != ENTRY},
        {'exit': 2, 'verified_rows': 0, 'findings': ['ENTRY-MISSING']})
    case('entry-malformed', files({ENTRY: '{"schema": "%s", ' % SCHEMA}),
        {'exit': 2, 'verified_rows': 0, 'findings': ['ENTRY-MALFORMED']})
    case('entry-wrong-schema', files({ENTRY: json.dumps(
        dict(fixture_entry(base_sha), schema='tsukuroi-memory-pressure-r25-v0'))}),
        {'exit': 2, 'verified_rows': 0, 'findings': ['ENTRY-SCHEMA']})
    case('lesson-missing', {k: v for k, v in files().items() if k != LESSON},
        {'exit': 2, 'verified_rows': 0, 'findings': ['LESSON-MISSING']})
    case('sources-missing', {k: v for k, v in files().items() if k != SOURCES},
        {'exit': 2, 'verified_rows': 0, 'findings': ['SOURCES-MISSING']})
    case('skill-missing', {k: v for k, v in files().items() if k != SKILL},
        {'exit': 2, 'verified_rows': 0, 'findings': ['SKILL-MISSING']})
    case('row-id-unknown', files({ENTRY: mutate_row('MP2', lambda r: r.__setitem__('id', 'MP9'))}),
        {'exit': 1, 'verified_rows': 0,
         'findings': ['MP-ROW-ID-UNKNOWN', 'MP-SKILL-ROW-MISSING', 'MP-ROW-SET']})
    case('declared-capture-digest-mismatch', files({ENTRY: json.dumps(
        dict(fixture_entry('0' * 64), rows=fixture_entry(base_sha)['rows']))}),
        {'exit': 1, 'verified_rows': 0, 'findings': ['MP-CAPTURE-DECLARED-MISMATCH']})
    # R2b: a row whose only source is tier B carries no tier-A source.
    case('source-tier-not-a', files({ENTRY: set_source('MP1', 'S125')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SOURCE-TIER-NOT-A']})
    # R3: a Gate quote that differs from the entry quote blocks the row.
    case('gate-quote-mismatch-blocks', files({
        LESSON: fixture_lesson().replace(
            '| %s | https://example.invalid/%s | "%s" | SrcA |\n' % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0], QUOTE_A),
            '| %s | https://example.invalid/%s | "a different located quote" | SrcA |\n'
            % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0]))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-QUOTE-MISMATCH']})
    # R3: an entry quote that differs from the Gate quote blocks the row.
    case('entry-quote-mismatch-blocks', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('quotes', [{'source': ROW_SOURCE_IDS[0],
                                                   'quote': 'a quote the Gate does not carry'}]))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-QUOTE-MISMATCH']})
    # R3: a quote naming a source the row does not list blocks the row.
    case('entry-quote-unknown-source-blocks', files({ENTRY: mutate_row(
        'MP1', lambda r: r.__setitem__('quotes', [{'source': 'S998', 'quote': QUOTE_A}]))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-QUOTE-SOURCE-UNKNOWN']})
    # R3: a Gate quote over the word cap blocks every row that cites the source.
    case('gate-quote-over-cap-blocks', files({
        LESSON: fixture_lesson().replace(
            '| %s | https://example.invalid/%s | "%s" | SrcA |\n' % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0], QUOTE_A),
            '| %s | https://example.invalid/%s | "%s" | SrcA |\n'
            % (ROW_SOURCE_IDS[0], ROW_SOURCE_IDS[0], long_quote)),
        ENTRY: mutate_row('MP1', lambda r: r.__setitem__(
            'quotes', [{'source': ROW_SOURCE_IDS[0], 'quote': long_quote}]))}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-QUOTE-TOO-LONG']})
    # R5: the id must be in the FIRST cell of a table line of the round-25 section.
    case('skill-row-id-not-in-first-cell', files({SKILL: FIXTURE_SKILL.replace(
        '| MP3 | changed | record |\n', '| note | changed | MP3 |\n')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SKILL-ROW-MISSING']})
    # R5: a table line of another section does not carry the row.
    case('skill-row-in-other-section-only', files({SKILL: FIXTURE_SKILL.replace(
        '| MP3 | changed | record |\n', '').replace(
        '| memory-pressure | gate |',
        '| MP3 | changed | record |\n| memory-pressure | gate |')}),
        {'exit': 1, 'verified_rows': 5, 'findings': ['MP-SKILL-ROW-MISSING']})
    # R6: a repeated row id is an error of the entry.
    case('duplicate-row-id', files({ENTRY: json.dumps(
        dict(fixture_entry(base_sha),
             rows=fixture_entry(base_sha)['rows'] + [fixture_entry(base_sha)['rows'][0]]))}),
        {'exit': 1, 'verified_rows': 0, 'findings': ['MP-ROW-ID-DUPLICATE']})
    # The recheck reader must not crash on a prose line that names a source and
    # the word recheck but shows no old -> new change (the crash at c93bd70f).
    case('recheck-prose-without-arrow', files({LESSON: fixture_lesson() + (
        '\n- S115 anchor: the sha256 in `corpus/SOURCES.md` row S115 has a transposition, '
        'and the registry row is append-only outside its status, recheck and used-by cells.\n')}),
        {'exit': 0, 'verified_rows': 6, 'findings': []})

    observations = []
    for name, case_files, expect in cases:
        try:
            observations.append(dict(case=name, **run_fixture(case_files, expect)))
        except Exception as exc:  # a broken fixture is a failed case, not a crash
            observations.append({'case': name, 'exit': None, 'verified_rows': None,
                                 'findings': [], 'pass': False, 'error': str(exc)[:160]})
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
    parser.add_argument('--branch', default='master')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
    except _revision.RevisionError as exc:
        print(json.dumps({'status': 'CANNOT_EVALUATE', 'findings': [{'id': exc.fid, 'site': exc.site}]}))
        return 2
    code, result = evaluate(git_reader(ROOT, binding.sha))
    result.update(revision=binding.sha, branch=binding.branch,
                  status=('PASS', 'FAIL', 'CANNOT_EVALUATE')[code])
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
