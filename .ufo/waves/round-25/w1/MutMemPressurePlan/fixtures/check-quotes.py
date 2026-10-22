#!/usr/bin/env python3
"""Check that every fixture Gate quote is really present in the page it names.

The C2 rule admits a row only when it carries a located quote of at most 25 words that
was copied from the opened page. A fixture whose quotes are invented would let a
mutant pass for the wrong reason, so this script re-opens each page named by a fixture
SOURCES row and checks that the recorded quote occurs in that page's bytes.

The pages are fetched with curl into the scratch directory. The script records the
sha256 of every fetched page so a later run can tell whether the page changed.

Usage: check-quotes.py [--fetch-dir DIR] [--offline]
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE / 'baseline'
SOURCES = BASELINE / 'corpus/SOURCES.md'
LESSON = BASELINE / 'corpus/lessons/round-25.md'
DEFAULT_FETCH_DIR = Path('/fast/scratch/hyaku/tsukuroi-r25/MutMemPressurePlan/pages')


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


SEPARATED_QUOTES = re.compile(r'"\s*;\s')
BACKTICK_SPAN = re.compile(r'`([^`]*)`')


def straight_quote_spans(text):
    """The straight-quoted spans of a text, as (start, end, content).

    A located quote may itself contain double quotes, and one cell may hold several
    located quotes separated by `"; `. When the cell separates them the quotes pair
    from the left; otherwise the outermost pair is the located quote and the inner
    ones belong to its text.
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

    A backtick-delimited span wins over a straight-quoted one.
    """
    out = []
    for match in BACKTICK_SPAN.finditer(line):
        out.append((match.start(), match.end(), match.group(1).strip()))
    for start, end, content in straight_quote_spans(line):
        if not any(s <= start and end <= e for s, e, _ in out):
            out.append((start, end, content))
    out.sort()
    return out


def split_cells(line):
    """Split a markdown table row into cells, honouring a backslash-escaped pipe."""
    return [text for _start, _end, text in cell_spans(line.strip().strip('|'))]


def plain_text(data):
    """Reduce an HTML or reStructuredText page to the text a reader would quote."""
    text = data.decode('utf-8', 'replace')
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    return re.sub(r'\s+', ' ', text)


def fetch(url, fetch_dir, attempts=4):
    """Fetch a URL into the fetch directory and return its bytes.

    The man.archlinux.org host closes TLS connections intermittently, so the fetch is
    retried a few times before it is reported as a failure.
    """
    fetch_dir.mkdir(parents=True, exist_ok=True)
    name = re.sub(r'[^A-Za-z0-9._-]+', '_', url.split('://', 1)[-1])[-120:]
    target = fetch_dir / name
    last = None
    for attempt in range(attempts):
        proc = subprocess.run(['curl', '-sS', '--max-time', '60', '-o', str(target), url],
                              timeout=90, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode == 0 and target.exists() and target.stat().st_size:
            return target.read_bytes()
        last = proc.stderr.decode('utf-8', 'replace').strip() or ('exit %d' % proc.returncode)
    raise RuntimeError(last or 'fetch failed')


def registry_rows(text):
    rows = {}
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cells = split_cells(line)
        if len(cells) < 11 or not re.fullmatch(r'S\d{3}', cells[0]):
            continue
        rows[cells[0]] = cells
    return rows


def gate_quotes(text):
    """Map a source id to the located quote recorded in the lesson's Gate table.

    The located quote is the first balanced quoted span at or after the start of the
    quote cell of the row, so a pipe inside the quoted value does not cut it short.
    """
    quotes = {}
    for line in text.splitlines():
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
        quotes[cells[0]] = quote
    return quotes


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--fetch-dir', default=str(DEFAULT_FETCH_DIR))
    parser.add_argument('--offline', action='store_true',
                        help='use only pages already present in the fetch directory')
    args = parser.parse_args(argv)
    fetch_dir = Path(args.fetch_dir)

    rows = registry_rows(SOURCES.read_text())
    quotes = gate_quotes(LESSON.read_text())

    failures = []
    for source_id in sorted(rows):
        cells = rows[source_id]
        url = cells[1]
        match = re.search(r'(https?://\S+?)(?:\s|$)', cells[1] + ' ')
        if not match:
            failures.append('%s: no URL in the source cell' % source_id)
            continue
        url = match.group(1)
        quote = quotes.get(source_id)
        if not quote:
            failures.append('%s: no quote in the lesson Gate' % source_id)
            continue
        count = len(quote.split())
        if count > 25:
            failures.append('%s: quote is %d words, over the 25 word limit' % (source_id, count))
        try:
            data = fetch(url, fetch_dir) if not args.offline else None
            if data is None:
                target = fetch_dir / re.sub(r'[^A-Za-z0-9._-]+', '_', url.split('://', 1)[-1])[-120:]
                if not target.exists():
                    failures.append('%s: page %s is not in the fetch directory' % (source_id, url))
                    continue
                data = target.read_bytes()
        except Exception as exc:                     # noqa: BLE001 - reported, not raised
            failures.append('%s: could not fetch %s (%s)' % (source_id, url, exc))
            continue
        digest = hashlib.sha256(data).hexdigest()
        present = quote in plain_text(data)
        print('%s %s words=%d sha256=%s quote-present=%s'
              % (source_id, url, count, digest[:16], present))
        if not present:
            failures.append('%s: the quote is not present in %s' % (source_id, url))

    if failures:
        print('FAIL')
        for failure in failures:
            print('  %s' % failure)
        return 1
    print('OK: every fixture quote is present in the page it names and is at most 25 words')
    return 0


if __name__ == '__main__':
    sys.exit(main())
