#!/usr/bin/env python3
"""Wave-2 mutation harness for tools/check-memory-pressure.py against the real integrated entry.

Each mutant is a full sandbox built from `git archive 5e7c04ec...` of the lane,
mutated in one place, committed in a fresh `git init` repository with no remote,
and measured with the sandbox's own tool: `python3 tools/check-memory-pressure.py
--revision <commit>`.

Verdict vocabulary:
  KILLED       the counting command exits non-zero (the mutation is detected by
               the declared counting command `verified_rows` field)
  SURVIVED     the counting command still exits 0 with the same verified_rows,
               so the mutation is invisible to the counting command
  INCONCLUSIVE the pristine baseline is red, or the tool could not be evaluated
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
REV = '5e7c04ecb02735491456de2b8bc44550d0db4609'
SEAT = Path('/fast/scratch/hyaku/tsukuroi-r25/w2/MutC2Rules')
ENTRY = 'corpus/knowledge/memory-pressure-r25.json'
SOURCES = 'corpus/SOURCES.md'
LESSON = 'corpus/lessons/round-25.md'
SKILL = 'SKILL.md'
CAPTURE = '.ufo/waves/round-25/capture/capture.txt'
COLUMNS = ['id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches', 'status',
           'opened', 'recheck', 'used-by']


def git(repo, *args, check=True):
    env = dict(os.environ)
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_AUTHOR_NAME': 'MutC2Rules', 'GIT_AUTHOR_EMAIL': 'm@example.invalid',
                'GIT_COMMITTER_NAME': 'MutC2Rules', 'GIT_COMMITTER_EMAIL': 'm@example.invalid'})
    proc = subprocess.run(['git', '-C', str(repo), *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=env, timeout=300)
    if check and proc.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (' '.join(args),
                                                 proc.stderr.decode('utf-8', 'replace').strip()))
    return proc.stdout.decode('utf-8', 'replace')


def sha256_file(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_sandbox(destination):
    """Extract the real measured tree and commit it in a fresh repo with no remote."""
    archive = subprocess.run(['git', '-C', str(LANE), 'archive', REV],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    if archive.returncode != 0:
        raise RuntimeError('git archive failed')
    destination.mkdir(parents=True, exist_ok=True)
    extract = subprocess.run(['tar', '-x', '-C', str(destination)], input=archive.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    if extract.returncode != 0:
        raise RuntimeError('tar failed')
    git(destination, 'init', '--quiet', '--initial-branch=master', '.')
    git(destination, 'config', 'user.name', 'MutC2Rules')
    git(destination, 'config', 'user.email', 'm@example.invalid')
    git(destination, 'config', 'commit.gpgsign', 'false')
    git(destination, 'add', '-A')
    git(destination, 'commit', '--quiet', '-m', 'mutant')
    return git(destination, 'rev-parse', 'HEAD').strip()


# --------------------------------------------------------------- tool helpers

_TOOL = None


def tool():
    """Import the measured tool so its own parsers locate cells and quotes."""
    global _TOOL
    if _TOOL is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'check_memory_pressure', str(SEAT / 'base' / 'tools' / 'check-memory-pressure.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _TOOL = module
    return _TOOL


# ------------------------------------------------------------- source helpers

def sources_rows(text):
    rows = {}
    for index, line in enumerate(text.splitlines()):
        if not line.startswith('|'):
            continue
        cells = tool().split_cells(line)
        if len(cells) < 11 or not cells[0].startswith('S'):
            continue
        if set(cells[0]) <= set('- '):
            continue
        rows.setdefault(cells[0], (cells, index))
    return rows


def write_lines(path, lines, trailing_newline=True):
    Path(path).write_text('\n'.join(lines) + ('\n' if trailing_newline else ''))


# ---------------------------------------------------------------- operations

def op_sources_cell(entry, root):
    path = root / entry['target_file']
    text = path.read_text()
    rows = sources_rows(text)
    sid = entry['params']['source_id']
    if sid not in rows:
        return False, 'source id %s absent' % sid
    cells, index = rows[sid]
    column = entry['params']['column']
    position = COLUMNS.index(column)
    old = cells[position]
    cells[position] = entry['params']['value']
    lines = text.splitlines()
    lines[index] = '| ' + ' | '.join(cells) + ' |'
    write_lines(path, lines, text.endswith('\n'))
    return True, '%s %s cell %r -> %r' % (sid, column, old, cells[position])


def op_sources_drop_cell(entry, root):
    path = root / entry['target_file']
    text = path.read_text()
    rows = sources_rows(text)
    sid = entry['params']['source_id']
    if sid not in rows:
        return False, 'source id %s absent' % sid
    cells, index = rows[sid]
    position = COLUMNS.index(entry['params']['drop_column'])
    old = cells[position]
    kept = cells[:position] + cells[position + 1:]
    lines = text.splitlines()
    lines[index] = '| ' + ' | '.join(kept) + ' |'
    write_lines(path, lines, text.endswith('\n'))
    return True, '%s dropped the %s cell %r (row now %d cells)' % (sid, entry['params']['drop_column'],
                                                                   old, len(kept))


def op_gate_quote_words(entry, root):
    """Replace the located quote of one Gate row with a quote of N words."""
    path = root / entry['target_file']
    text = path.read_text()
    sid = entry['params']['source_id']
    words = entry['params']['quote_words']
    quote = ' '.join('word%02d' % n for n in range(1, words + 1))
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|') or not line.startswith('| %s |' % sid):
            continue
        spans = tool().quoted_spans(line)
        if not spans:
            continue
        start, end, content = spans[0]
        lines[index] = line[:start] + '"%s"' % quote + line[end:]
        write_lines(path, lines, text.endswith('\n'))
        return True, 'Gate row %s quote %r -> %d words' % (sid, content, words)
    return False, 'Gate row %s absent' % sid


def op_gate_quote_one_char(entry, root):
    """Change exactly one character of the located quote of one Gate row."""
    path = root / entry['target_file']
    text = path.read_text()
    sid = entry['params']['source_id']
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|') or not line.startswith('| %s |' % sid):
            continue
        spans = tool().quoted_spans(line)
        if not spans:
            continue
        start, end, content = spans[0]
        position = entry['params']['position']
        if position >= len(content):
            return False, 'Gate quote of %s is shorter than position %d' % (sid, position)
        changed = content[:position] + entry['params']['new_character'] + content[position + 1:]
        lines[index] = line[:start] + '"%s"' % changed + line[end:]
        write_lines(path, lines, text.endswith('\n'))
        return True, 'Gate row %s quote %r -> %r (one character changed)' % (sid, content, changed)
    return False, 'Gate row %s absent' % sid


def entry_rows(document):
    rows = None
    for value in document.values():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            if any(isinstance(item, dict) and 'id' in item for item in value):
                rows = value
                break
    return rows


def op_entry_quote_one_char(entry, root):
    """Change exactly one character of a row's own quote."""
    path = root / entry['target_file']
    document = json.loads(path.read_text())
    rows = entry_rows(document)
    row = next(r for r in rows if r.get('id') == entry['params']['row_id'])
    target = next(q for q in row['quotes'] if q.get('source') == entry['params']['source_id'])
    old = target['quote']
    position = entry['params']['position']
    changed = old[:position] + entry['params']['new_character'] + old[position + 1:]
    target['quote'] = changed
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    return True, 'row %s quote for %s %r -> %r (one character changed)' % (
        entry['params']['row_id'], entry['params']['source_id'], old, changed)


def op_entry_quote_replace(entry, root):
    path = root / entry['target_file']
    document = json.loads(path.read_text())
    rows = entry_rows(document)
    row = next(r for r in rows if r.get('id') == entry['params']['row_id'])
    target = next(q for q in row['quotes'] if q.get('source') == entry['params']['source_id'])
    old = target['quote']
    target['quote'] = entry['params']['replacement']
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    return True, 'row %s quote for %s %r -> %r' % (entry['params']['row_id'],
                                                  entry['params']['source_id'], old,
                                                  entry['params']['replacement'])


def op_entry_quote_unknown_source(entry, root):
    """Point a row's quote at a source the row does not list."""
    path = root / entry['target_file']
    document = json.loads(path.read_text())
    rows = entry_rows(document)
    row = next(r for r in rows if r.get('id') == entry['params']['row_id'])
    old = row['quotes'][0]
    row['quotes'][0] = {'source': entry['params']['source_id'], 'quote': old['quote']}
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    return True, 'row %s quote source %s -> %s' % (entry['params']['row_id'],
                                                    old['source'], entry['params']['source_id'])


def op_entry_pointer_set(entry, root):
    """Replace the whole capture-pointer list of one row with one pointer."""
    path = root / entry['target_file']
    document = json.loads(path.read_text())
    rows = entry_rows(document)
    row = next(r for r in rows if r.get('id') == entry['params']['row_id'])
    old = row['capture_pointers']
    row['capture_pointers'] = [{'line': entry['params']['capture_line'],
                                'token': entry['params']['token']}]
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    return True, 'row %s pointers %s -> %s' % (entry['params']['row_id'], old,
                                               row['capture_pointers'])


def op_entry_duplicate_row(entry, root):
    path = root / entry['target_file']
    document = json.loads(path.read_text())
    rows = entry_rows(document)
    row = next(r for r in rows if r.get('id') == entry['params']['row_id'])
    rows.append(json.loads(json.dumps(row)))
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    return True, 'row %s duplicated in the entry' % entry['params']['row_id']


def op_capture_append(entry, root):
    path = root / entry['target_file']
    data = path.read_bytes()
    path.write_bytes(data + entry['params']['append'].encode('utf-8'))
    return True, 'capture bytes appended; sha256 %s -> %s' % (
        tool_hash(data), sha256_file(path))


def tool_hash(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


def op_skill_delete_row(entry, root):
    path = root / entry['target_file']
    text = path.read_text()
    row_id = entry['params']['row_id']
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells and cells[0] == row_id:
            del lines[index]
            write_lines(path, lines, text.endswith('\n'))
            return True, 'SKILL.md decision-table row %s deleted (line %d)' % (row_id, index + 1)
    return False, 'SKILL.md row %s absent' % row_id


def op_skill_rename_row_id(entry, root):
    """Rename the row id inside a SKILL.md decision-table row (the row stays, the id moves)."""
    path = root / entry['target_file']
    text = path.read_text()
    row_id = entry['params']['row_id']
    replacement = entry['params']['replacement']
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells and cells[0] == row_id:
            lines[index] = line.replace('| %s |' % row_id, '| %s |' % replacement, 1)
            write_lines(path, lines, text.endswith('\n'))
            return True, 'SKILL.md row id %s -> %s' % (row_id, replacement)
    return False, 'SKILL.md row %s absent' % row_id


def op_gate_quote_words_all(entry, root):
    """Replace EVERY Gate quote of the named sources with a quote of N words."""
    path = root / entry['target_file']
    text = path.read_text()
    words = entry['params']['quote_words']
    quote = ' '.join('word%02d' % n for n in range(1, words + 1))
    lines = text.splitlines()
    changed = 0
    for index, line in enumerate(lines):
        for sid in entry['params']['source_ids']:
            if not line.startswith('| %s |' % sid):
                continue
            spans = tool().quoted_spans(line)
            if not spans:
                continue
            start, end, _content = spans[0]
            lines[index] = line[:start] + '"%s"' % quote + line[end:]
            changed += 1
    if not changed:
        return False, 'no Gate row found for %s' % (entry['params']['source_ids'],)
    write_lines(path, lines, text.endswith('\n'))
    return True, '%d Gate row(s) for %s replaced with a %d-word quote' % (
        changed, entry['params']['source_ids'], words)


def op_gate_and_entry_quote_consistent(entry, root):
    """Change the Gate quote and the entry quote together, to the same text.

    Neither side then mismatches the other, so the checker sees a consistent
    pair.  Only an external read of the cited page could detect that the text
    is not in the source at all.
    """
    lesson = root / LESSON
    text = lesson.read_text()
    sid = entry['params']['source_id']
    new_text = entry['params']['new_text']
    lines = text.splitlines()
    done = False
    for index, line in enumerate(lines):
        if done or not line.startswith('| %s |' % sid):
            continue
        spans = tool().quoted_spans(line)
        if not spans:
            continue
        start, end, old = spans[0]
        lines[index] = line[:start] + '"%s"' % new_text + line[end:]
        done = True
    if not done:
        return False, 'Gate row %s absent' % sid
    write_lines(lesson, lines, text.endswith('\n'))

    path = root / ENTRY
    document = json.loads(path.read_text())
    rows = entry_rows(document)
    row = next(r for r in rows if r.get('id') == entry['params']['row_id'])
    target = next(q for q in row['quotes'] if q.get('source') == sid)
    old_entry = target['quote']
    target['quote'] = new_text
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    return True, ('Gate quote of %s and the entry quote of row %s both set to %r '
                  '(Gate was %r)' % (sid, entry['params']['row_id'], new_text, old_entry))


OPERATIONS = {
    'sources-cell': op_sources_cell,
    'sources-drop-cell': op_sources_drop_cell,
    'gate-quote-words': op_gate_quote_words,
    'gate-quote-words-all': op_gate_quote_words_all,
    'gate-and-entry-quote-consistent': op_gate_and_entry_quote_consistent,
    'gate-quote-one-char': op_gate_quote_one_char,
    'entry-quote-one-char': op_entry_quote_one_char,
    'entry-quote-replace': op_entry_quote_replace,
    'entry-quote-unknown-source': op_entry_quote_unknown_source,
    'entry-pointer-set': op_entry_pointer_set,
    'entry-duplicate-row': op_entry_duplicate_row,
    'capture-append': op_capture_append,
    'skill-delete-row': op_skill_delete_row,
    'skill-rename-row-id': op_skill_rename_row_id,
}


# ------------------------------------------------------------------- running

def run_detector(repo, revision):
    proc = subprocess.run([sys.executable, 'tools/check-memory-pressure.py',
                           '--revision', revision],
                          cwd=str(repo), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=300)
    return proc.returncode, proc.stdout.decode('utf-8', 'replace'), proc.stderr.decode('utf-8', 'replace')


def parse(stdout):
    text = stdout.strip()
    start = text.find('{')
    if start < 0:
        return None, []
    try:
        document = json.loads(text[start:])
    except ValueError:
        return None, []
    ids = []
    for finding in document.get('findings', []) or []:
        if isinstance(finding, dict) and isinstance(finding.get('id'), str):
            ids.append(finding['id'])
    return document.get('verified_rows'), ids


def run_case(entry, workdir):
    record = {'id': entry['id'], 'breaks_rule': entry['breaks_rule'],
              'expected_finding_id': entry.get('expected_finding_id'),
              'target_file': entry.get('target_file'), 'operation': entry['operation'],
              'verdict': None, 'exit_code': None, 'verified_rows': None, 'finding_ids': []}
    repo = workdir / entry['id']
    if repo.exists():
        shutil.rmtree(repo)
    revision = build_sandbox(repo)
    record['revision'] = revision
    applied, detail = OPERATIONS[entry['operation']](entry, repo)
    record['applied_detail'] = detail
    if not applied:
        record['verdict'] = 'INCONCLUSIVE'
        record['detail'] = 'mutation could not be applied: %s' % detail
        return record
    git(repo, 'add', '-A')
    git(repo, 'commit', '--quiet', '--allow-empty', '-m', 'mutant')
    revision = git(repo, 'rev-parse', 'HEAD').strip()
    record['revision'] = revision
    code, stdout, stderr = run_detector(repo, revision)
    record['exit_code'] = code
    rows, ids = parse(stdout)
    record['verified_rows'] = rows
    record['finding_ids'] = ids
    record['stderr'] = stderr[-800:]
    expected = entry.get('expected_finding_id')
    if expected:
        record['expected_finding_emitted'] = expected in ids
    if code == 0:
        record['verdict'] = 'SURVIVED'
        record['detail'] = 'the counting command still exits 0 (verified_rows %s)' % rows
    else:
        record['verdict'] = 'KILLED'
        record['detail'] = 'the counting command exits %d (verified_rows %s)' % (code, rows)
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--catalogue', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--workdir', default=str(SEAT / 'work'))
    parser.add_argument('--only', default=None)
    args = parser.parse_args(argv)

    catalogue = json.loads(Path(args.catalogue).read_text())
    wanted = None
    if args.only:
        wanted = {item.strip() for item in args.only.split(',') if item.strip()}

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)

    records = []
    baseline = {'id': 'BASELINE', 'verdict': None, 'exit_code': None, 'verified_rows': None,
                'finding_ids': []}
    repo = workdir / 'BASELINE'
    if repo.exists():
        shutil.rmtree(repo)
    revision = build_sandbox(repo)
    code, stdout, stderr = run_detector(repo, revision)
    rows, ids = parse(stdout)
    baseline.update(exit_code=code, verified_rows=rows, finding_ids=ids, revision=revision,
                    verdict='PASS' if (code == 0 and not ids) else 'RED')
    print('BASELINE: %s exit=%s verified_rows=%s findings=%s' %
          (baseline['verdict'], code, rows, ids), flush=True)
    records.append(baseline)

    for entry in catalogue['mutations']:
        if wanted and entry['id'] not in wanted:
            continue
        record = run_case(entry, workdir)
        print('%s: %s exit=%s verified_rows=%s expected_emitted=%s | %s | %s' %
              (record['id'], record['verdict'], record['exit_code'], record['verified_rows'],
               record.get('expected_finding_emitted'), record.get('applied_detail'),
               record['detail']), flush=True)
        records.append(record)

    killed = sum(1 for r in records if r.get('id') != 'BASELINE' and r['verdict'] == 'KILLED')
    survived = sum(1 for r in records if r.get('id') != 'BASELINE' and r['verdict'] == 'SURVIVED')
    other = sum(1 for r in records if r.get('id') != 'BASELINE'
                and r['verdict'] not in ('KILLED', 'SURVIVED'))
    print('summary: killed=%d survived=%d inconclusive-or-other=%d' % (killed, survived, other))
    Path(args.out).write_text(json.dumps({'catalogue': args.catalogue, 'revision': REV,
                                          'records': records}, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
