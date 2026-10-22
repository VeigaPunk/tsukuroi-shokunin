#!/usr/bin/env python3
"""A self-check oracle for the C2 mutation fixtures.

This is NOT the lane's production checker. It is a small, independent implementation of
the C2 counting rule as written in the SCORECARD Round 25 declaration, written only so
that the mutation fixtures can be validated on their own terms: every mutant must break
exactly one counting rule, must leave the other five rows verifiable, and must produce
the finding id that fixtures/mutations.json names for it.

The production checker is written by the C2 build seat in its own clone. This oracle is
never installed into the lane repository and is never claimed to be that tool. Its only
job is to show that the fixture set is internally coherent before the production checker
exists.

Usage: oracle-check-memory-pressure.py --root <fixture-repo-root> [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

CAPTURE = '.ufo/waves/round-25/capture/capture.txt'
CAPTURE_SHA = 'e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136'
ENTRY_JSON = 'corpus/knowledge/memory-pressure-r25.json'
SOURCES = 'corpus/SOURCES.md'
LESSON = 'corpus/lessons/round-25.md'
SKILL = 'SKILL.md'
OPENED_DATE = '2026-10-22'
ROW_IDS = ('MP1', 'MP2', 'MP3', 'MP4', 'MP5', 'MP6')
MAX_QUOTE_WORDS = 25

SECTION_HEADER = re.compile(r'^### ')
COMMAND_ECHO = re.compile(r'^\$ ')
EXIT_LINE = re.compile(r'^\[exit ')


def words(text):
    return len(text.split())


def source_rows(text):
    """Map a source id to its registry cells."""
    rows = {}
    for line in (text or '').splitlines():
        if not line.startswith('|'):
            continue
        cells = split_cells(line)
        if len(cells) < 11 or not re.fullmatch(r'S\d{3}', cells[0]):
            continue
        rows.setdefault(cells[0], cells)
    return rows


CELL_SPLIT = re.compile(r'(?<!\\)\|')


def strip_pipes(line):
    """Drop the leading and trailing cell separator of a table row."""
    stripped = line.strip()
    if stripped.startswith('|'):
        stripped = stripped[1:]
    if stripped.endswith('|') and not stripped.endswith('\\|'):
        stripped = stripped[:-1]
    return stripped


def cell_spans(line):
    """Split a table row into (start, end, text) spans over the raw line.

    A pipe that a backslash escapes does not separate cells. The offsets are kept
    so that a quoted value spanning a pipe can still be located in the raw line,
    which is how the located quote is found without the quote cell being cut.
    """
    spans = []
    start = 0
    for match in CELL_SPLIT.finditer(line):
        spans.append((start, match.start(), line[start:match.start()].strip()))
        start = match.end()
    spans.append((start, len(line), line[start:].strip()))
    return spans


QUOTE_SPAN = re.compile(r'"([^"]*)"|\u201c([^\u201d]*)\u201d|`([^`]*)`')


def quoted_spans(line):
    """The balanced quoted spans of a raw line, as (start, end, content)."""
    out = []
    for match in QUOTE_SPAN.finditer(line):
        content = next((group for group in match.groups() if group is not None), '')
        out.append((match.start(), match.end(), content.strip()))
    return out


def split_cells(line):
    """Split a markdown table row into cells, honouring a backslash-escaped pipe."""
    stripped = line.strip()
    if stripped.startswith('|'):
        stripped = stripped[1:]
    if stripped.endswith('|') and not stripped.endswith('\\|'):
        stripped = stripped[:-1]
    return [text for _start, _end, text in cell_spans(stripped)]


def gate_quotes(text):
    """Map a source id to the located quote recorded in the lesson's Gate table.

    The located quote is the first balanced quoted span at or after the start of the
    quote cell of the row, so a pipe inside the quoted value does not cut it short.
    """
    quotes = {}
    for line in (text or '').splitlines():
        if not line.startswith('|'):
            continue
        raw = strip_pipes(line)
        spans = cell_spans(raw)
        cells = [text for _start, _end, text in spans]
        if len(cells) < 3 or not re.fullmatch(r'S\d{3}', cells[0]):
            continue
        quote = None
        if len(spans) > 2:
            cell_start = spans[2][0]
            for span_start, _span_end, content in quoted_spans(raw):
                if span_start >= cell_start:
                    quote = content
                    break
        if quote is None:
            for _span_start, _span_end, content in quoted_spans(raw):
                if content:
                    quote = content
                    break
        if not quote:
            continue
        quotes.setdefault(cells[0], quote)
    return quotes


def skill_rows(text):
    """Map an MP row id to True when SKILL.md carries a decision-table row naming it."""
    found = set()
    for line in (text or '').splitlines():
        if not line.startswith('|'):
            continue
        cells = split_cells(line)
        if cells and cells[0] in ROW_IDS:
            found.add(cells[0])
    return found


def recheck_logged(text, source_id):
    """True when the lesson logs an old -> new recheck change for the source id."""
    for line in (text or '').splitlines():
        if source_id not in line:
            continue
        if '->' in line or '→' in line:
            return True
    return False


def evaluate(root):
    """Count the verified rows at a fixture root and return the result document."""
    root = Path(root)
    findings = []

    def add(fid, site, detail=None):
        item = {'id': fid, 'site': site}
        if detail:
            item['detail'] = detail
        findings.append(item)

    entry_path = root / ENTRY_JSON
    if not entry_path.exists():
        add('MP-ENTRY-MISSING', ENTRY_JSON)
        return {'verified_rows': 0, 'findings': findings, 'rows': []}
    try:
        document = json.loads(entry_path.read_text())
    except ValueError as exc:
        add('MP-ENTRY-JSON', ENTRY_JSON, str(exc))
        return {'verified_rows': 0, 'findings': findings, 'rows': []}

    capture_path = root / CAPTURE
    capture_text = capture_path.read_text() if capture_path.exists() else ''
    capture_lines = capture_text.splitlines()
    digest = hashlib.sha256(capture_text.encode('utf-8', 'replace')).hexdigest()
    if digest != CAPTURE_SHA:
        add('CAPTURE-TAMPERED', CAPTURE,
            'sha256 %s does not equal the pinned %s' % (digest, CAPTURE_SHA))

    sources = source_rows((root / SOURCES).read_text() if (root / SOURCES).exists() else '')
    lesson = (root / LESSON).read_text() if (root / LESSON).exists() else ''
    quotes = gate_quotes(lesson)
    skill = skill_rows((root / SKILL).read_text() if (root / SKILL).exists() else '')

    rows = document.get('rows') if isinstance(document, dict) else None
    if not isinstance(rows, list):
        add('MP-ENTRY-SCHEMA', ENTRY_JSON, 'rows is missing or not a list')
        return {'verified_rows': 0, 'findings': findings, 'rows': []}

    details = []
    advisories = []
    for row in rows:
        rid = row.get('id') if isinstance(row, dict) else None
        problems = []
        if not isinstance(row, dict):
            details.append({'id': rid, 'verified': False, 'problems': ['row-not-an-object']})
            continue
        if not isinstance(row.get('verdict'), str) or not row['verdict'].strip():
            problems.append('verdict-missing')
        if not isinstance(row.get('action'), str) or not row['action'].strip():
            problems.append('action-missing')

        # at least one qualifying source
        source_ids = row.get('sources') if isinstance(row.get('sources'), list) else []
        qualifying = 0
        if not source_ids:
            problems.append('sources-empty')
        for sid in source_ids:
            if not isinstance(sid, str) or sid not in sources:
                problems.append('source-missing:%s' % sid)
                continue
            cells = sources[sid]
            status, opened, used_by = cells[7], cells[8], cells[10]
            if status != 'mined':
                problems.append('source-status-not-mined:%s' % sid)
                continue
            if 'memory-pressure-r25' not in used_by:
                problems.append('source-used-by-not-this-entry:%s' % sid)
                continue
            if OPENED_DATE not in opened and not recheck_logged(lesson, sid):
                problems.append('source-opened-not-this-round:%s' % sid)
                continue
            qualifying += 1
        if source_ids and qualifying == 0 and not any(p.startswith('source-') for p in problems):
            problems.append('no-qualifying-source')

        # at least one located quote of at most 25 words
        quote_refs = row.get('quote_refs') if isinstance(row.get('quote_refs'), list) else []
        quote_ok = 0
        if not quote_refs:
            problems.append('quote-refs-empty')
        for ref in quote_refs:
            if not isinstance(ref, str) or ref not in quotes:
                problems.append('quote-missing:%s' % ref)
                continue
            count = words(quotes[ref])
            if count > MAX_QUOTE_WORDS:
                problems.append('quote-too-long:%s:%d' % (ref, count))
                continue
            quote_ok += 1
        if quote_refs and quote_ok == 0 and not any(p.startswith('quote-') for p in problems):
            problems.append('no-qualifying-quote')
        # The entry's own quotes list must agree with the lesson Gate for each source.
        for item in row.get('quotes') or []:
            if not isinstance(item, dict):
                continue
            ref, quote = item.get('source'), item.get('quote')
            if not isinstance(ref, str) or not isinstance(quote, str):
                continue
            if ref not in quotes:
                continue
            if ' '.join(quote.split()) not in ' '.join(quotes[ref].split()):
                # Advisory in the production checker: the finding is reported but it
                # does not disqualify the row, so it is recorded separately.
                advisories.append('quote-mismatch:%s' % ref)

        # at least one capture pointer on a unique, non-structural line
        # C2 capture pointers, as refined on 2026-10-22: each pointer names a line and
        # a token of at least 3 characters; it counts only if the line is unique in the
        # capture, is not a header, command echo or exit line, contains a letter or
        # digit, and contains its token.
        pointers = row.get('capture_pointers')
        if not isinstance(pointers, list) or not pointers:
            problems.append('capture-pointers-empty')
        pointer_ok = 0
        for pointer in pointers if isinstance(pointers, list) else []:
            line_no = None
            token = None
            if isinstance(pointer, int) and not isinstance(pointer, bool):
                line_no = pointer
            elif isinstance(pointer, dict):
                candidate = pointer.get('line')
                if isinstance(candidate, int) and not isinstance(candidate, bool):
                    line_no = candidate
                if isinstance(pointer.get('token'), str):
                    token = pointer['token']
            if line_no is None or line_no < 1 or line_no > len(capture_lines):
                problems.append('capture-pointer-unresolved:%r' % (pointer,))
                continue
            text = capture_lines[line_no - 1]
            if SECTION_HEADER.match(text):
                problems.append('capture-pointer-header:%d' % line_no)
                continue
            if COMMAND_ECHO.match(text):
                problems.append('capture-pointer-echo:%d' % line_no)
                continue
            if EXIT_LINE.match(text):
                problems.append('capture-pointer-exit:%d' % line_no)
                continue
            if capture_text.count(text) != 1:
                problems.append('capture-pointer-not-unique:%d' % line_no)
                continue
            if not re.search(r'[A-Za-z0-9]', text):
                problems.append('capture-pointer-no-letter-or-digit:%d' % line_no)
                continue
            if token is None or len(token) < 3:
                problems.append('capture-pointer-token-too-short:%d' % line_no)
                continue
            if token not in text:
                problems.append('capture-pointer-token-absent:%d' % line_no)
                continue
            pointer_ok += 1
        if isinstance(pointers, list) and pointers and pointer_ok == 0 \
                and not any(p.startswith('capture-pointer-') for p in problems):
            problems.append('no-qualifying-capture-pointer')

        if rid not in skill:
            problems.append('skill-row-missing:%s' % rid)

        row_advisories = [a for a in advisories if a.startswith('quote-mismatch:')]
        details.append({'id': rid, 'verified': not problems, 'problems': problems,
                        'advisories': row_advisories})
        for problem in problems:
            add('MP-ROW-PROBLEM', '%s:%s' % (rid, problem))
        for advisory in row_advisories:
            add('MP-QUOTE-MISMATCH', '%s:%s' % (rid, advisory.split(':', 1)[1]))

    seen = sorted(d['id'] for d in details if d.get('id'))
    if seen != sorted(ROW_IDS):
        add('MP-ROW-SET', ','.join(seen), 'the rows are not exactly MP1..MP6')

    return {'verified_rows': sum(1 for d in details if d['verified']),
            'findings': findings, 'rows': details}


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--root', required=True, help='fixture repository root')
    parser.add_argument('--json', action='store_true', help='print the result as JSON')
    args = parser.parse_args(argv)
    result = evaluate(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('verified_rows=%d findings=%d' % (result['verified_rows'], len(result['findings'])))
        for finding in result['findings']:
            print('  %s %s %s' % (finding['id'], finding['site'], finding.get('detail', '')))
    return 0 if result['verified_rows'] == len(ROW_IDS) and not result['findings'] else 1


if __name__ == '__main__':
    sys.exit(main())
