#!/usr/bin/env python3
"""Run the C2 mutation set against tools/check-memory-pressure.py.

Reads fixtures/mutations.json, builds one temporary git repository per mutant from
fixtures/baseline/, applies the mutant's operation, commits it, and runs the counting
command `python3 tools/check-memory-pressure.py --revision <commit>` inside that
repository. A mutant is KILLED when the tool exits non-zero and names the expected
finding id; it SURVIVED when the tool exits zero. An INCONCLUSIVE verdict is recorded
when the tool cannot be evaluated at all (missing, crashed, or the pristine baseline
already fails), because a broken baseline cannot distinguish a killed mutant.

Nothing in the lane repository is written. Every temporary repository is created with
`git init` and has no remote, so no push can reach the lane.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE
BASELINE = FIXTURES / 'baseline'
CATALOGUE = FIXTURES / 'mutations.json'
DEFAULT_TOOL = Path('/fast/scratch/hyaku/tsukuroi-r25/ExecMemPressureTool/repo/tools/check-memory-pressure.py')
SCRATCH = Path('/fast/scratch/hyaku/tsukuroi-r25/MutMemPressurePlan')
LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
TOOL_RELPATH = 'tools/check-memory-pressure.py'

# The capture is read from the lane working tree at fixture-build time and copied in
# byte for byte; the runner never re-reads the lane during a sweep.
CAPTURE_SHA = 'e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136'


def log(message):
    print(message, flush=True)


def git(repo, *args, check=True):
    env = dict(os.environ)
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_AUTHOR_NAME': 'MutMemPressurePlan', 'GIT_AUTHOR_EMAIL': 'm@example.invalid',
                'GIT_COMMITTER_NAME': 'MutMemPressurePlan', 'GIT_COMMITTER_EMAIL': 'm@example.invalid'})
    proc = subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env, timeout=120)
    if check and proc.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (' '.join(args),
                                                 proc.stderr.decode('utf-8', 'replace').strip()))
    return proc.stdout.decode('utf-8', 'replace')


def sha256_bytes(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------
# mutation operations
# --------------------------------------------------------------------------

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


def parse_sources_table(text):
    """Return {source_id: (cells, line_index)} for the SOURCES registry table."""
    rows = {}
    for index, line in enumerate(text.splitlines()):
        if not line.startswith('|'):
            continue
        cells = split_cells(line)
        if len(cells) < 11 or not cells[0].startswith('S'):
            continue
        if set(cells[0]) <= set('- '):
            continue
        rows.setdefault(cells[0], (cells, index))
    return rows


def op_sources_cell(entry, root, capture_lines):
    """Set one cell of one SOURCES row (M01, M02, M03)."""
    path = root / entry['target_file']
    text = path.read_text()
    rows = parse_sources_table(text)
    sid = entry['params']['source_id']
    if sid not in rows:
        return False, 'source id %s absent from the fixture registry' % sid
    cells, _ = rows[sid]
    column = entry['params']['column']
    # Registry column order: id source kind tier scope anchor teaches status opened recheck used-by
    index = {'id': 0, 'source': 1, 'kind': 2, 'tier': 3, 'scope': 4, 'anchor': 5,
             'teaches': 6, 'status': 7, 'opened': 8, 'recheck': 9, 'used-by': 10}[column]
    old = cells[index]
    cells[index] = entry['params']['value']
    lines = text.splitlines()
    rebuilt = '| ' + ' | '.join(cells) + ' |'
    lines[rows[sid][1]] = rebuilt
    path.write_text('\n'.join(lines) + ('\n' if text.endswith('\n') else ''))
    entry['applied_detail'] = 'SOURCES row %s: %s cell %r -> %r' % (sid, column, old, cells[index])
    return True, entry['applied_detail']


def op_sources_cell_and_lesson_absence(entry, root, capture_lines):
    """M03: set the opened cell to a stale date and remove any recheck log line for it.

    The C2 rule admits a source that was opened on 2026-10-22, or whose recheck cell was
    updated in place this round with the change logged old -> new in the lesson. Setting the
    opened cell to 2026-10-21 is only a violation when the lesson holds no old -> new log
    line for that source id, so the mutation removes such a line if the fixture has one.
    """
    ok, detail = op_sources_cell(entry, root, capture_lines)
    if not ok:
        return False, detail
    sid = entry['params']['source_id']
    lesson = root / 'corpus/lessons/round-25.md'
    text = lesson.read_text()
    kept, removed = [], 0
    for line in text.splitlines(True):
        if sid in line and ('->' in line or '→' in line):
            removed += 1
            continue
        kept.append(line)
    lesson.write_text(''.join(kept))
    entry['applied_detail'] = detail + ('; removed %d recheck log line(s) for %s' % (removed, sid)
                                         if removed else '; no recheck log line for %s existed' % sid)
    return True, entry['applied_detail']


def op_lesson_gate_quote(entry, root, capture_lines):
    """Replace the located quote of one Gate row with a quote of N words (M04)."""
    path = root / entry['target_file']
    text = path.read_text()
    sid = entry['params']['source_id']
    want = entry['params']['quote_words']
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        raw = strip_pipes(line)
        spans = cell_spans(raw)
        cells = [text for _s, _e, text in spans]
        if len(cells) < 3 or cells[0] != sid:
            continue
        old = cells[2]
        quote = ' '.join(['word%d' % n for n in range(1, want + 1)])
        # Replace the quote cell on the raw line, keeping every other cell's text.
        cell_start = spans[2][0]
        cell_end = spans[2][1]
        lines[index] = '|' + raw[:cell_start] + '"%s"' % quote + raw[cell_end:]
        path.write_text('\n'.join(lines) + ('\n' if text.endswith('\n') else ''))
        entry['applied_detail'] = ('Gate row %s quote replaced: %d words -> %d words'
                                    % (sid, len(old.split()), want))
        return True, entry['applied_detail']
    return False, 'Gate row %s absent from the fixture lesson' % sid


def token_in_line(text):
    """The longest alphanumeric run of 3 or more characters in a capture line.

    The refined C2 pointer rule requires a token of at least 3 characters that the
    pointed line contains, so a mutant that repoints a row needs a token that its own
    target line really carries.
    """
    runs = re.findall(r'[A-Za-z0-9][A-Za-z0-9._%-]{2,}', text)
    if not runs:
        return None
    return max(runs, key=len)


def op_lesson_gate_quote_truncate_at_pipe(entry, root, capture_lines):
    """Truncate a Gate quote at its first pipe (M11).

    The Gate cell holds a quoted value that itself contains a pipe. Cutting the quote at
    that pipe leaves the lesson recording a shorter quote than the entry's own
    `quotes[].quote` for the same source, which the tool reports as MP-QUOTE-MISMATCH.
    This is the mutant that pins the reader fix for a pipe inside a located quote: a
    reader that splits the cell before locating the quoted span would cut the quote at
    the same place by accident and would raise the same finding, so this mutant must be
    paired with the untruncated baseline (which the sweep also runs) to be meaningful.
    """
    path = root / entry['target_file']
    text = path.read_text()
    sid = entry['params']['source_id']
    cut = entry['params']['truncate_at']
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        raw = strip_pipes(line)
        spans = cell_spans(raw)
        cells = [text for _s, _e, text in spans]
        if len(cells) < 3 or cells[0] != sid:
            continue
        cell = cells[2]
        old = cell
        # Truncate the located quote itself at the first pipe it holds. The quote is
        # the balanced quoted span of the raw line, so the pipe is found inside the
        # quote rather than at a cell boundary.
        span = None
        for span_start, span_end, content in quoted_spans(raw):
            if cut in content:
                span = (span_start, span_end, content)
                break
        if span is None:
            return False, 'Gate quote for %s holds no %r to truncate at' % (sid, cut)
        span_start, span_end, content = span
        position = content.find(cut)
        # Keep the opening quote and the text before the pipe, then close the quote.
        lines[index] = ('|' + raw[:span_start + 1] + content[:position].rstrip() + '"'
                        + raw[span_end:])
        path.write_text('\n'.join(lines) + ('\n' if text.endswith('\n') else ''))
        entry['applied_detail'] = ('Gate row %s quote truncated at %r: %r -> %r'
                                    % (sid, cut, old[:60], cells[2][:60]))
        return True, entry['applied_detail']
    return False, 'Gate row %s absent from the fixture lesson' % sid


def op_entry_pointer_replace(entry, root, capture_lines):
    """Point one row at one capture line (M05 to M08).

    The pointer slot shape is whatever the fixture entry JSON uses, so the operation walks
    the JSON and rewrites the first capture-pointer-shaped slot it finds on the target row:
    either a bare integer line number or an object carrying a `line` integer. When the
    slot is an object with a `contains` string, that string is rewritten to the new line's
    text so the mutant breaks exactly one rule (the pointer's own rule) and not also the
    substring-resolution rule.
    """
    path = root / entry['target_file']
    document = json.loads(path.read_text())
    row_id = entry['params']['row_id']
    target_line = entry['params']['capture_line']
    if target_line < 1 or target_line > len(capture_lines):
        return False, 'capture line %d out of range' % target_line

    rows = None
    for key, value in document.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            if any(isinstance(item, dict) and item.get('id') == row_id for item in value):
                rows = value
                break
    if rows is None:
        return False, 'row %s absent from the fixture entry JSON' % row_id
    row = next(item for item in rows if isinstance(item, dict) and item.get('id') == row_id)

    slot = None
    for key, value in row.items():
        if 'pointer' not in key.lower() and 'capture' not in key.lower():
            continue
        if isinstance(value, list) and value:
            slot = (key, value)
            break
    if slot is None:
        return False, 'no capture-pointer slot on row %s' % row_id

    key, values = slot
    if all(isinstance(item, int) and not isinstance(item, bool) for item in values):
        # Replace the whole list, so the row keeps no other pointer that could still
        # qualify. The rule under test is "at least one qualifying pointer", so a
        # mutant that left a good pointer behind would not exercise it at all.
        values[:] = [target_line]
        shape = 'integer list'
    elif all(isinstance(item, dict) for item in values):
        if not isinstance(values[0].get('line'), int):
            return False, 'pointer objects on row %s carry no integer `line`' % row_id
        first = {'line': target_line}
        # The refined C2 pointer rule names a line and a token. The token is derived
        # from the target line, so the mutant breaks the pointer's own rule (header,
        # echo, exit or non-unique line) and not also the token-presence rule.
        token = token_in_line(capture_lines[target_line - 1])
        if token is None:
            return False, ('capture line %d holds no alphanumeric run of 3 characters'
                           % target_line)
        first['token'] = token
        values[:] = [first]
        shape = 'object list'
    else:
        return False, 'pointer slot on row %s has an unhandled shape' % row_id

    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    entry['applied_detail'] = ('row %s capture pointer slot %r (%s) repointed at capture line %d'
                                % (row_id, key, shape, target_line))
    return True, entry['applied_detail']


def op_capture_append_bytes(entry, root, capture_lines):
    """Append bytes to the frozen capture so its sha256 no longer matches the pin (M09)."""
    path = root / entry['target_file']
    data = path.read_bytes()
    path.write_bytes(data + entry['params']['append'].encode('utf-8'))
    entry['applied_detail'] = ('capture bytes appended; sha256 %s -> %s'
                                % (sha256_bytes(data), sha256_file(path)))
    return True, entry['applied_detail']


def op_skill_table_row_delete(entry, root, capture_lines):
    """Delete the SKILL.md decision-table row naming one MP id (M10)."""
    path = root / entry['target_file']
    text = path.read_text()
    row_id = entry['params']['row_id']
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if cells and cells[0] == row_id:
            del lines[index]
            path.write_text('\n'.join(lines) + ('\n' if text.endswith('\n') else ''))
            entry['applied_detail'] = 'SKILL.md decision-table row %s deleted' % row_id
            return True, entry['applied_detail']
    return False, 'SKILL.md decision-table row %s absent' % row_id


OPERATIONS = {
    'sources-cell': op_sources_cell,
    'sources-cell-and-lesson-absence': op_sources_cell_and_lesson_absence,
    'lesson-gate-quote': op_lesson_gate_quote,
    'lesson-gate-quote-truncate-at-pipe': op_lesson_gate_quote_truncate_at_pipe,
    'entry-pointer-replace': op_entry_pointer_replace,
    'capture-append-bytes': op_capture_append_bytes,
    'skill-table-row-delete': op_skill_table_row_delete,
}


# --------------------------------------------------------------------------
# repository construction and the detector
# --------------------------------------------------------------------------

def copy_baseline(destination, source=None):
    """Materialise the pristine baseline tree at `destination`.

    `source` may be a directory (the synthetic fixture baseline) or a pair
    (repo, revision) naming a commit of a git repository whose tree is extracted.
    The git form is what makes the fixture set usable against the real landed entry:
    the mutation operations are written structurally, so they apply to the real
    corpus/knowledge/memory-pressure-r25.json, corpus/SOURCES.md,
    corpus/lessons/round-25.md and SKILL.md as well as to the synthetic baseline.
    """
    if source is None:
        shutil.copytree(BASELINE, destination)
        return
    if isinstance(source, (tuple, list)):
        repo, revision = source
        archive = subprocess.run(['git', '-C', str(repo), 'archive', revision],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 timeout=300)
        if archive.returncode != 0:
            raise RuntimeError('git archive %s failed: %s'
                               % (revision, archive.stderr.decode('utf-8', 'replace').strip()))
        destination.mkdir(parents=True, exist_ok=True)
        extract = subprocess.run(['tar', '-x', '-C', str(destination)],
                                 input=archive.stdout, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, timeout=300)
        if extract.returncode != 0:
            raise RuntimeError('tar extraction failed: %s'
                               % extract.stderr.decode('utf-8', 'replace').strip())
        return
    shutil.copytree(source, destination)


def install_tool(destination, tool_path):
    """Copy the checker under test into the temporary repository.

    The lane's checkers import the shared revision adapter `tools/_revision.py` and find
    the lane root by looking for that file, so it is installed next to the checker. The
    adapter is taken from the tool's own clone when it has one, so the checker runs
    against the adapter it was written for.
    """
    target = destination / TOOL_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)
    if tool_path is None or not tool_path.exists():
        return False, 'checker not found at %s' % (tool_path or 'unset')
    shutil.copy2(tool_path, target)
    adapter = tool_path.parent / '_revision.py'
    if adapter.exists():
        shutil.copy2(adapter, destination / 'tools' / '_revision.py')
    elif (LANE / 'tools' / '_revision.py').exists():
        shutil.copy2(LANE / 'tools' / '_revision.py', destination / 'tools' / '_revision.py')
    else:
        return False, 'the shared revision adapter tools/_revision.py was not found'
    return True, 'checker copied from %s (sha256 %s)' % (tool_path, sha256_file(target))


def init_repository(path):
    git(path, 'init', '--quiet', '--initial-branch=master', '.')
    git(path, 'config', 'user.name', 'MutMemPressurePlan')
    git(path, 'config', 'user.email', 'm@example.invalid')
    git(path, 'config', 'commit.gpgsign', 'false')
    git(path, 'add', '-A')
    git(path, 'commit', '--quiet', '-m', 'fixture baseline')
    return git(path, 'rev-parse', 'HEAD').strip()


def run_detector(repo, revision):
    """Run the counting command and return (exit_code, stdout, stderr)."""
    proc = subprocess.run([sys.executable, TOOL_RELPATH, '--revision', revision],
                          cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=300)
    return (proc.returncode, proc.stdout.decode('utf-8', 'replace'),
            proc.stderr.decode('utf-8', 'replace'))


def findings_from(stdout):
    """Extract the finding ids and the verified_rows count from the tool's JSON output."""
    text = stdout.strip()
    if not text:
        return [], None
    start = text.find('{')
    if start < 0:
        return [], None
    try:
        document = json.loads(text[start:])
    except ValueError:
        return [], None
    ids = []
    for finding in document.get('findings', []) or []:
        if isinstance(finding, dict) and isinstance(finding.get('id'), str):
            ids.append(finding['id'])
        elif isinstance(finding, str):
            ids.append(finding)
    rows = None
    for key in ('verified_rows', 'rows_verified', 'verified'):
        if isinstance(document.get(key), int):
            rows = document[key]
            break
    return ids, rows


def matches_expected(finding_ids, entry):
    expected = entry['expected_finding_id']
    aliases = [expected] + CATALOGUE_ALIASES.get(expected, [])
    for finding_id in finding_ids:
        if finding_id in aliases:
            return True, finding_id
    lowered = [finding_id.lower() for finding_id in finding_ids]
    for alias in aliases:
        if alias.lower() in lowered:
            return True, finding_id
    return False, None


CATALOGUE_ALIASES = {}


def run_mutation(entry, tool_path, workdir, baseline_source=None):
    """Build one mutant repository, run the detector, and return the verdict record."""
    record = {
        'id': entry['id'],
        'expected_finding_id': entry['expected_finding_id'],
        'breaks_rule': entry['breaks_rule'],
        'target_file': entry['target_file'],
        'verdict': None,
        'exit_code': None,
        'finding_ids': [],
        'verified_rows': None,
        'detail': None,
    }
    repo = workdir / entry['id']
    copy_baseline(repo, baseline_source)
    ok, detail = install_tool(repo, tool_path)
    if not ok:
        record['verdict'] = 'INCONCLUSIVE'
        record['detail'] = detail
        return record

    capture = repo / entry.get('capture_path', '.ufo/waves/round-25/capture/capture.txt')
    capture_lines = capture.read_text().splitlines()

    applied, apply_detail = OPERATIONS[entry['operation']](entry, repo, capture_lines)
    record['applied_detail'] = apply_detail
    if not applied:
        record['verdict'] = 'INCONCLUSIVE'
        record['detail'] = 'mutation could not be applied: %s' % apply_detail
        return record

    try:
        revision = init_repository(repo)
    except Exception as exc:                        # noqa: BLE001 - reported, not raised
        record['verdict'] = 'INCONCLUSIVE'
        record['detail'] = 'could not commit the mutant: %s' % exc
        return record

    record['revision'] = revision
    code, stdout, stderr = run_detector(repo, revision)
    record['exit_code'] = code
    record['stdout'] = stdout[-4000:]
    record['stderr'] = stderr[-2000:]
    ids, rows = findings_from(stdout)
    record['finding_ids'] = ids
    record['verified_rows'] = rows
    matched, hit = matches_expected(ids, entry)
    record['matched_finding_id'] = hit
    if matched:
        record['verdict'] = 'KILLED'
        record['detail'] = 'expected finding %s emitted' % hit
    elif code == 0:
        record['verdict'] = 'SURVIVED'
        record['detail'] = 'the counting command exited 0 and did not name %s' % entry['expected_finding_id']
    else:
        record['verdict'] = 'KILLED-OTHER'
        record['detail'] = 'the tool failed but named %s, not %s' % (ids or 'no finding', entry['expected_finding_id'])
    return record


def run_baseline(tool_path, workdir, baseline_source=None):
    """Run the pristine fixture; a red baseline makes every mutant inconclusive."""
    record = {'id': 'BASELINE', 'verdict': None, 'exit_code': None, 'finding_ids': [],
              'verified_rows': None}
    repo = workdir / 'BASELINE'
    copy_baseline(repo, baseline_source)
    ok, detail = install_tool(repo, tool_path)
    if not ok:
        record['verdict'] = 'INCONCLUSIVE'
        record['detail'] = detail
        return record
    try:
        revision = init_repository(repo)
    except Exception as exc:                        # noqa: BLE001 - reported, not raised
        record['verdict'] = 'INCONCLUSIVE'
        record['detail'] = 'could not commit the baseline: %s' % exc
        return record
    record['revision'] = revision
    code, stdout, stderr = run_detector(repo, revision)
    record['exit_code'] = code
    record['stdout'] = stdout[-4000:]
    record['stderr'] = stderr[-2000:]
    ids, rows = findings_from(stdout)
    record['finding_ids'] = ids
    record['verified_rows'] = rows
    if code == 0 and not ids:
        record['verdict'] = 'PASS'
        record['detail'] = 'pristine fixture verified'
    else:
        record['verdict'] = 'RED'
        record['detail'] = 'the pristine fixture already fails; every mutant would be inconclusive'
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--tool', default=str(DEFAULT_TOOL),
                        help='path to check-memory-pressure.py (default: %(default)s)')
    parser.add_argument('--catalogue', default=str(CATALOGUE),
                        help='path to mutations.json (default: %(default)s)')
    parser.add_argument('--out', default=None, help='where to write the JSON result')
    parser.add_argument('--keep', action='store_true',
                        help='keep the temporary repositories for inspection')
    parser.add_argument('--only', default=None, help='comma separated mutation ids to run')
    parser.add_argument('--baseline-repo', default=None,
                        help='git repository holding the real landed entry')
    parser.add_argument('--baseline-rev', default=None,
                        help='revision of --baseline-repo to use as the pristine baseline')
    args = parser.parse_args(argv)

    global CATALOGUE_ALIASES
    catalogue = json.loads(Path(args.catalogue).read_text())
    CATALOGUE_ALIASES = catalogue.get('finding_id_aliases', {})

    tool_path = Path(args.tool) if args.tool and args.tool != 'none' else None
    if tool_path is None or not tool_path.exists():
        log('checker not available at %s; the runner is left for wave 2' % (tool_path or 'unset'))
        log('baseline fixture and catalogue are complete and self-checking')
        return 2

    wanted = None
    if args.only:
        wanted = {item.strip() for item in args.only.split(',') if item.strip()}

    baseline_source = None
    if args.baseline_repo and args.baseline_rev:
        baseline_source = (args.baseline_repo, args.baseline_rev)
        log('baseline: the real tree at %s:%s' % (args.baseline_repo, args.baseline_rev))
    else:
        log('baseline: the synthetic fixture baseline at %s' % BASELINE)

    SCRATCH.mkdir(parents=True, exist_ok=True)
    workdir = Path(tempfile.mkdtemp(prefix='sweep-', dir=str(SCRATCH)))
    log('work directory: %s' % workdir)
    try:
        baseline = run_baseline(tool_path, workdir, baseline_source)
        log('baseline: %s (exit %s, verified_rows %s)' %
            (baseline['verdict'], baseline['exit_code'], baseline['verified_rows']))
        records = [baseline]
        for entry in catalogue['mutations']:
            if wanted and entry['id'] not in wanted:
                continue
            record = run_mutation(entry, tool_path, workdir, baseline_source)
            log('%s: %s exit=%s verified_rows=%s findings=%s | %s' %
                (record['id'], record['verdict'], record['exit_code'],
                 record['verified_rows'], record['finding_ids'], record.get('detail')))
            records.append(record)
    finally:
        if args.keep:
            log('temporary repositories kept at %s' % workdir)
        else:
            shutil.rmtree(workdir, ignore_errors=True)

    killed = sum(1 for r in records if r.get('id') != 'BASELINE' and r['verdict'] == 'KILLED')
    survived = sum(1 for r in records if r.get('id') != 'BASELINE' and r['verdict'] == 'SURVIVED')
    other = sum(1 for r in records if r.get('id') != 'BASELINE'
                and r['verdict'] not in ('KILLED', 'SURVIVED'))
    log('summary: killed=%d survived=%d inconclusive-or-other=%d' % (killed, survived, other))

    if args.out:
        Path(args.out).write_text(json.dumps({'catalogue': str(args.catalogue),
                                              'tool': str(tool_path),
                                              'records': records},
                                             indent=2, ensure_ascii=False) + '\n')
        log('result written to %s' % args.out)
    return 0 if (killed or survived or other) and not survived else 1


if __name__ == '__main__':
    sys.exit(main())
