#!/usr/bin/env python3
"""Run the C1 storage-health mutation catalogue against one revision.

The catalogue (catalogue.json) lists mutants of the round-26 C1 entry.  For
every mutant this runner builds a throwaway sandbox from the lane repository
at one revision, applies exactly one edit, commits it, and runs the C1
detector against that sandbox.  The lane repository is read only: it is
opened with `git archive`, never written to.  The digests of every lane file
the catalogue touches are recorded before and after the run so that the
report can show that no lane byte moved.

Usage:

    python3 run-mutants.py --revision <sha> --tool tools/check-storage-health.py

    python3 run-mutants.py --lane /path/to/tsukuroi-shokunin \
        --revision <sha> --tool tools/check-storage-health.py \
        --catalogue catalogue.json --out results.json --jobs 4

Exit codes: 0 when every mutant verdict matches its expectation, 1 when a
mutant verdict disagrees with its expectation, 2 when the run could not be
made (bad revision, missing tool, baseline that is not (6, 0)).
"""
from __future__ import annotations

import argparse
import concurrent.futures
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
DEFAULT_CATALOGUE = HERE / 'catalogue.json'

CELL_SPLIT = re.compile(r'(?<!\\)\|')
HEADING = re.compile(r'^\s{0,3}(#{1,6})\s+(.*?)\s*$')
SHA256_RE = re.compile(r'\b([0-9a-f]{64})\b')


class OpError(Exception):
    """The edit could not be applied: the mutant is inconclusive, not killed."""


# ---------------------------------------------------------------- utilities


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(cmd, cwd=None, check=True, timeout=300):
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, timeout=timeout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode != 0:
        raise RuntimeError('%s -> exit %d: %s' % (' '.join(map(str, cmd)),
                                                  proc.returncode,
                                                  proc.stderr.decode('utf-8', 'replace')[:400]))
    return proc


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='surrogateescape')


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding='utf-8', errors='surrogateescape')


def split_cells(line: str):
    """Split a markdown table row into stripped cells, honouring escaped pipes."""
    return [c.strip() for c in CELL_SPLIT.split(line.strip().strip('|'))]


def join_cells(cells) -> str:
    out = []
    for cell in cells:
        out.append(cell.replace('|', r'\|'))
    return '| ' + ' | '.join(out) + ' |'


def parse_json_output(text: str):
    """Best-effort JSON parse of a detector's stdout."""
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        pass
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[text.find('{'):])
        return obj
    except Exception:
        return None


# ------------------------------------------------------------- sandbox build


def build_sandbox(lane: Path, rev: str, dest: Path) -> str:
    """Fill `dest` with the tree of `rev` and commit it on branch master."""
    dest.mkdir(parents=True, exist_ok=True)
    git = subprocess.Popen(['git', '-C', str(lane), 'archive', rev],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tar = subprocess.Popen(['tar', '-x', '-C', str(dest)], stdin=git.stdout,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    git.stdout.close()
    tar_err = tar.communicate()[1]
    git_err = git.communicate()[1]
    if git.returncode != 0:
        raise RuntimeError('git archive failed: %s' % git_err.decode('utf-8', 'replace')[:300])
    if tar.returncode != 0:
        raise RuntimeError('tar failed: %s' % tar_err.decode('utf-8', 'replace')[:300])
    init = run(['git', 'init', '-b', 'master', str(dest)], check=False)
    if init.returncode != 0:
        run(['git', 'init', str(dest)])
        run(['git', '-C', str(dest), 'symbolic-ref', 'HEAD', 'refs/heads/master'])
    run(['git', '-C', str(dest), 'add', '-A'])
    run(['git', '-C', str(dest), '-c', 'user.name=mutant',
         '-c', 'user.email=mutant@example.invalid', '-c', 'commit.gpgsign=false',
         'commit', '--no-verify', '-m', 'mutation sandbox'])
    sha = run(['git', '-C', str(dest), 'rev-parse', 'HEAD']).stdout.decode().strip()
    return sha


# --------------------------------------------------------------- entry access


def entry_path(sb: Path, targets) -> Path:
    return sb / targets.get('entry_json', 'corpus/knowledge/storage-health-r26.json')


def load_entry(sb: Path, targets):
    path = entry_path(sb, targets)
    if not path.exists():
        raise OpError('entry file missing: %s' % targets.get('entry_json'))
    try:
        data = json.loads(read_text(path))
    except Exception as exc:
        raise OpError('entry file is not JSON: %s' % exc)
    rows = data.get('rows') if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise OpError('entry has no rows list')
    return path, data, rows


def quote_text_key(quote):
    for key in ('text', 'quote'):
        if key in quote:
            return key
    raise OpError('quote object has no text or quote key: %r' % (list(quote),))


def quote_source_key(quote):
    for key in ('source', 'source_id'):
        if key in quote:
            return key
    return None


def find_row(rows, row_id):
    for row in rows:
        if isinstance(row, dict) and row.get('id') == row_id:
            return row
    raise OpError('row id %r not found in the entry' % row_id)


def save_entry(path: Path, data) -> None:
    write_text(path, json.dumps(data, indent=1, ensure_ascii=False) + '\n')


# -------------------------------------------------------------- source table


def sources_header_and_rows(sb: Path, targets):
    path = sb / targets.get('sources', 'corpus/SOURCES.md')
    if not path.exists():
        raise OpError('registry missing: %s' % path)
    lines = read_text(path).splitlines()
    header = None
    rows = {}
    for line in lines:
        if not line.strip().startswith('|'):
            continue
        cells = split_cells(line)
        if not cells:
            continue
        if header is None and cells[0].lower() == 'id':
            header = {name: index for index, name in enumerate(cells)}
            continue
        if header is None:
            continue
        if set(''.join(cells)) <= set('-: '):
            continue
        if re.fullmatch(r'S\d{3}', cells[0]):
            rows[cells[0]] = (line, cells)
    if header is None:
        raise OpError('registry header row not found')
    return path, lines, header, rows


def resolve_source_targets(sb: Path, targets, spec):
    """Return the list of S-ids an op applies to."""
    if 'ids' in spec:
        return list(spec['ids'])
    if 'from_entry_rows' in spec:
        _, _, rows = load_entry(sb, targets)
        ids = []
        for row_id in spec['from_entry_rows']:
            row = find_row(rows, row_id)
            for source in row.get('sources', []) or []:
                if source not in ids:
                    ids.append(source)
        return ids
    raise OpError('op has no resolvable source targets: %r' % (spec,))


# --------------------------------------------------------------- lesson gate


def lesson_path(sb: Path, targets, op):
    name = op.get('file') or targets.get('lesson', 'corpus/lessons/round-26.md')
    path = sb / name
    if path.exists():
        return path
    matches = sorted((sb / 'corpus' / 'lessons').glob('round-26*.md'))
    if matches:
        return matches[0]
    raise OpError('lesson file missing: %s' % name)


def gate_row_line(lines, source_id):
    """Return (index, line) of the Gate table row for `source_id`."""
    in_gate = False
    for index, line in enumerate(lines):
        if HEADING.match(line):
            title = HEADING.match(line).group(2).strip().lower()
            in_gate = title.startswith('gate')
            continue
        if not in_gate:
            continue
        if not line.strip().startswith('|'):
            continue
        cells = split_cells(line)
        if cells and cells[0] == source_id:
            return index, line
    raise OpError('no Gate table row for %s' % source_id)


def mutate_quoted_text(text: str) -> str:
    if ' ' in text:
        return text.replace(' ', '_', 1)
    return text + 'x'


def find_capture_line_by_text(sb: Path, targets, text: str) -> int:
    """1-based number of the first capture line whose stripped text is `text`."""
    rel = targets.get('capture', '.ufo/waves/round-26/capture/capture.txt')
    path = sb / rel
    if not path.exists():
        raise OpError('capture missing: %s' % rel)
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if line.strip() == text:
            return index
    raise OpError('no capture line whose text is %r' % text)


# ---------------------------------------------------------------- skill file


def skill_section(lines, targets):
    """Return (start, end) line indexes of the storage-integrity section."""
    wanted = targets.get('skill_section', '## Storage integrity — round 26')
    start = None
    for index, line in enumerate(lines):
        match = HEADING.match(line)
        if not match:
            continue
        title = match.group(2).strip()
        if title == wanted[len('## '):] or title == wanted:
            start = index
            break
        if 'storage integrity' in title.lower() and 'round 26' in title.lower():
            start = index
            break
    if start is None:
        raise OpError('SKILL.md section %r not found' % wanted)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if HEADING.match(lines[index]):
            end = index
            break
    return start, end


def skill_row_index(lines, targets, row_id):
    start, end = skill_section(lines, targets)
    for index in range(start + 1, end):
        line = lines[index]
        if not line.strip().startswith('|'):
            continue
        cells = split_cells(line)
        if cells and cells[0] == row_id:
            return index
    raise OpError('no SKILL.md table line whose first cell is %r' % row_id)


# --------------------------------------------------------------- the ops


def apply_op(op: dict, sb: Path, targets: dict):
    """Apply one catalogue op inside the sandbox.  Returns a notes dict."""
    kind = op.get('type')
    notes = {'op': kind, 'touched': []}

    def touch(rel):
        rel = str(rel)
        path = sb / rel
        notes['touched'].append({'file': rel,
                                 'before_sha256': sha256_file(path) if path.exists() else None})

    if kind in ('json_row_duplicate', 'json_row_delete', 'json_row_clone_with_id',
                'json_row_set', 'json_row_text_append', 'json_row_add_source',
                'json_quote_set', 'json_quote_lengthen', 'json_quote_mangle',
                'json_quote_source_set', 'json_capture_pointers_set',
                'json_capture_pointers_token_set', 'json_capture_pointers_empty'):
        path, data, rows = load_entry(sb, targets)
        touch(path.relative_to(sb))
        row_id = op.get('row')
        if kind == 'json_row_duplicate':
            row = find_row(rows, row_id)
            rows.append(copy.deepcopy(row))
            notes['detail'] = 'duplicated row %s' % row_id
        elif kind == 'json_row_delete':
            find_row(rows, row_id)
            rows[:] = [r for r in rows if not (isinstance(r, dict) and r.get('id') == row_id)]
            notes['detail'] = 'deleted row %s' % row_id
        elif kind == 'json_row_clone_with_id':
            row = find_row(rows, op['from'])
            clone = copy.deepcopy(row)
            clone['id'] = op['id']
            rows.append(clone)
            notes['detail'] = 'cloned row %s as %s' % (op['from'], op['id'])
        elif kind == 'json_row_set':
            row = find_row(rows, row_id)
            row[op['field']] = op['value']
            notes['detail'] = 'row %s field %s set' % (row_id, op['field'])
        elif kind == 'json_row_text_append':
            row = find_row(rows, row_id)
            row[op['field']] = str(row.get(op['field'], '')) + op['suffix']
            notes['detail'] = 'row %s field %s appended' % (row_id, op['field'])
        elif kind == 'json_row_add_source':
            row = find_row(rows, row_id)
            sources = list(row.get('sources', []) or [])
            sources.append(op['value'])
            row['sources'] = sources
            notes['detail'] = 'row %s gained source %s' % (row_id, op['value'])
        else:
            row = find_row(rows, row_id)
            if kind in ('json_capture_pointers_set', 'json_capture_pointers_token_set',
                        'json_capture_pointers_empty'):
                pointers = row.get('capture_pointers') or []
                if kind == 'json_capture_pointers_empty':
                    row['capture_pointers'] = []
                    notes['detail'] = 'row %s capture pointers emptied' % row_id
                elif kind == 'json_capture_pointers_token_set':
                    if not pointers:
                        raise OpError('row %s carries no capture pointers' % row_id)
                    for pointer in pointers:
                        pointer['token'] = op['value']
                    notes['detail'] = 'row %s pointer tokens set to %r' % (row_id, op['value'])
                else:
                    line = op.get('line')
                    if 'line_by_text' in op:
                        line = find_capture_line_by_text(sb, targets, op['line_by_text'])
                    if line is None:
                        raise OpError('pointer op carries neither line nor line_by_text')
                    row['capture_pointers'] = [{'line': line, 'token': op['token']}]
                    notes['detail'] = 'row %s pointer set to line %s token %r' % (row_id, line, op['token'])
            else:
                quotes = row.get('quotes', []) or []
                if not quotes:
                    raise OpError('row %s carries no quotes' % row_id)
                index = op.get('index', 'all')
                targets_quotes = quotes if index == 'all' else [quotes[index]]
                for quote in targets_quotes:
                    key = quote_text_key(quote)
                    if kind == 'json_quote_set':
                        quote[key] = op['text']
                    elif kind == 'json_quote_lengthen':
                        words = str(quote[key]).split()
                        pad = 0
                        while len(words) < int(op['words']):
                            words.append('mutantpad%02d' % pad)
                            pad += 1
                        quote[key] = ' '.join(words)
                    elif kind == 'json_quote_mangle':
                        quote[key] = mutate_quoted_text(str(quote[key]))
                    elif kind == 'json_quote_source_set':
                        skey = quote_source_key(quote)
                        if skey is None:
                            raise OpError('quote object has no source key')
                        quote[skey] = op['value']
                notes['detail'] = 'row %s quotes edited (%d)' % (row_id, len(targets_quotes))
        save_entry(path, data)
        return notes

    if kind == 'sources_row_set':
        path, lines, header, rows = sources_header_and_rows(sb, targets)
        touch(path.relative_to(sb))
        column = op['column']
        if column not in header:
            raise OpError('registry column %r not found' % column)
        ids = resolve_source_targets(sb, targets, op.get('targets', {}))
        changed = []
        for source_id in ids:
            if source_id not in rows:
                raise OpError('source %s is not a registry row' % source_id)
            line, cells = rows[source_id]
            index = header[column]
            if op.get('mutation') == 'replace_sha256':
                found = SHA256_RE.search(cells[index])
                if not found:
                    raise OpError('no sha256 in the anchor cell of %s' % source_id)
                replacement = hashlib.sha256((cells[index] + '|mutant').encode()).hexdigest()
                cells[index] = cells[index][:found.start()] + replacement + cells[index][found.end():]
            else:
                cells[index] = op['value']
            rows[source_id] = (join_cells(cells), cells)
            changed.append(source_id)
        for source_id, (line, _cells) in rows.items():
            pass
        new_lines = []
        for line in lines:
            cells = split_cells(line) if line.strip().startswith('|') else None
            if cells and re.fullmatch(r'S\d{3}', cells[0]) and cells[0] in changed:
                new_lines.append(join_cells(rows[cells[0]][1]))
            else:
                new_lines.append(line)
        write_text(path, '\n'.join(new_lines) + ('\n' if read_text(path).endswith('\n') else ''))
        notes['detail'] = 'registry column %s set on %s' % (column, ','.join(changed))
        return notes

    if kind in ('gate_quote_mangle', 'gate_row_delete'):
        path = lesson_path(sb, targets, op)
        touch(path.relative_to(sb))
        lines = read_text(path).splitlines()
        ids = resolve_source_targets(sb, targets, op.get('targets', {}))
        changed = []
        for source_id in ids:
            index, line = gate_row_line(lines, source_id)
            if kind == 'gate_row_delete':
                lines.pop(index)
            else:
                first = line.find('"')
                last = line.rfind('"')
                if first < 0 or last <= first:
                    raise OpError('no quoted text in the Gate row of %s' % source_id)
                quoted = line[first + 1:last]
                mutated = mutate_quoted_text(quoted)
                lines[index] = line[:first + 1] + mutated + line[last:]
            changed.append(source_id)
        write_text(path, '\n'.join(lines) + '\n')
        notes['detail'] = 'Gate rows edited: %s' % ','.join(changed)
        return notes

    if kind == 'snapshot_byte_change':
        directory = sb / targets.get('snapshots_dir', '.ufo/waves/round-26/sources')
        if not directory.is_dir():
            raise OpError('snapshot directory missing: %s' % directory)
        ids = resolve_source_targets(sb, targets, op.get('targets', {}))
        changed = []
        for source_id in ids:
            matches = sorted(directory.glob('%s.*' % source_id))
            if not matches:
                raise OpError('no committed snapshot for %s' % source_id)
            path = matches[0]
            touch(path.relative_to(sb))
            write_text(path, read_text(path) + ' ')
            changed.append('%s (%s)' % (source_id, path.name))
        notes['detail'] = 'snapshots changed: %s' % ','.join(changed)
        return notes

    if kind in ('skill_first_cell_set', 'skill_row_delete', 'skill_row_move_out'):
        path = sb / targets.get('skill', 'SKILL.md')
        touch(path.relative_to(sb))
        lines = read_text(path).splitlines()
        index = skill_row_index(lines, targets, op['row'])
        if kind == 'skill_first_cell_set':
            cells = split_cells(lines[index])
            cells[0] = op['value']
            lines[index] = join_cells(cells)
            notes['detail'] = 'SKILL first cell of %s set to %s' % (op['row'], op['value'])
        elif kind == 'skill_row_delete':
            lines.pop(index)
            notes['detail'] = 'SKILL table line of %s deleted' % op['row']
        else:
            line = lines.pop(index)
            lines.append('')
            lines.append(line)
            notes['detail'] = 'SKILL table line of %s moved out of the section' % op['row']
        write_text(path, '\n'.join(lines) + '\n')
        return notes

    if kind == 'skill_section_rename':
        path = sb / targets.get('skill', 'SKILL.md')
        touch(path.relative_to(sb))
        lines = read_text(path).splitlines()
        start, _end = skill_section(lines, targets)
        old = lines[start]
        lines[start] = op['to']
        write_text(path, '\n'.join(lines) + '\n')
        notes['detail'] = 'SKILL heading renamed: %r -> %r' % (old, op['to'])
        return notes

    if kind == 'capture_append_line':
        rel = targets.get('capture', '.ufo/waves/round-26/capture/capture.txt')
        path = sb / rel
        if not path.exists():
            raise OpError('capture missing: %s' % rel)
        touch(rel)
        write_text(path, read_text(path) + op['line'] + '\n')
        notes['detail'] = 'capture line appended'
        return notes

    if kind == 'file_delete':
        rel = op['file']
        path = sb / rel
        if not path.exists():
            raise OpError('file missing: %s' % rel)
        touch(rel)
        path.unlink()
        notes['detail'] = 'deleted %s' % rel
        return notes

    raise OpError('unknown op type %r' % kind)


# --------------------------------------------------------------- the detector


def resolve_tool(sb: Path, lane: Path, tool: str):
    """Return (path, relative) for the detector script to run."""
    path = Path(tool)
    if path.is_absolute():
        try:
            rel = path.relative_to(lane)
        except ValueError:
            return path, None
        candidate = sb / rel
        return (candidate, str(rel)) if candidate.exists() else (path, None)
    candidate = sb / tool
    return candidate, tool


def detector_supports_repo(tool: Path):
    proc = subprocess.run([sys.executable, str(tool), '--help'],
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    return '--repo' in proc.stdout.decode('utf-8', 'replace')


def run_detector(sb: Path, sha: str, tool: Path, use_repo: bool):
    cmd = [sys.executable, str(tool), '--revision', sha]
    if use_repo:
        cmd += ['--repo', str(sb)]
    proc = subprocess.run(cmd, cwd=str(sb), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=600)
    out = proc.stdout.decode('utf-8', 'replace')
    err = proc.stderr.decode('utf-8', 'replace')
    return proc.returncode, parse_json_output(out), out, err


def detector_state(exit_code, payload):
    verified = None
    status = None
    findings = []
    if isinstance(payload, dict):
        verified = payload.get('verified_rows')
        status = payload.get('status')
        raw = payload.get('findings')
        if isinstance(raw, list):
            for item in raw:
                if isinstance(item, dict):
                    findings.append(item.get('id'))
                else:
                    findings.append(str(item))
    return {'exit': exit_code, 'verified_rows': verified, 'status': status,
            'findings': findings}


# ------------------------------------------------------------------ the run


def lane_digests(lane: Path, targets, catalogue_path: Path):
    files = [catalogue_path]
    for key in ('entry_json', 'entry_md', 'sources', 'lesson', 'skill', 'capture'):
        rel = targets.get(key)
        if rel:
            files.append(lane / rel)
    out = {}
    for path in files:
        out[str(path)] = sha256_file(path) if path.exists() else None
    return out


def run_mutant(mutant, lane, rev, tool, targets, use_repo, keep, tmp_root):
    mutant_id = mutant['id']
    record = {'id': mutant_id, 'rule': mutant.get('rule'),
              'file': mutant.get('file'), 'op': mutant.get('op'),
              'expectation': mutant.get('expectation', {})}
    work = Path(tempfile.mkdtemp(prefix='mut-%s-' % mutant_id, dir=str(tmp_root)))
    try:
        try:
            sha = build_sandbox(lane, rev, work / 'repo')
        except Exception as exc:
            record.update(verdict='inconclusive', reason='sandbox build failed: %s' % exc)
            return record
        sb = work / 'repo'
        try:
            notes = apply_op(mutant['op'], sb, targets)
        except OpError as exc:
            record.update(verdict='inconclusive', reason='edit not applicable: %s' % exc)
            return record
        except Exception as exc:
            record.update(verdict='inconclusive', reason='edit failed: %s' % exc)
            return record
        record['edit'] = notes
        try:
            run(['git', '-C', str(sb), 'add', '-A'])
            run(['git', '-C', str(sb), '-c', 'user.name=mutant',
                 '-c', 'user.email=mutant@example.invalid', '-c', 'commit.gpgsign=false',
                 'commit', '--no-verify', '-m', 'mutant %s' % mutant_id])
        except Exception as exc:
            record.update(verdict='inconclusive', reason='commit failed: %s' % exc)
            return record
        tool_path, _rel = resolve_tool(sb, lane, tool)
        if not tool_path.exists():
            record.update(verdict='inconclusive', reason='detector script missing: %s' % tool_path)
            return record
        try:
            exit_code, payload, out, err = run_detector(sb, sha, tool_path, use_repo)
        except Exception as exc:
            record.update(verdict='inconclusive', reason='detector run failed: %s' % exc)
            return record
        state = detector_state(exit_code, payload)
        record['detector'] = state
        record['detector_stdout_head'] = out[:600]
        record['detector_stderr_head'] = err[:300]
        if payload is None:
            record.update(verdict='inconclusive', reason='detector printed no JSON')
            return record
        passed = (state['verified_rows'] == 6 and exit_code == 0)
        expected_killed = mutant.get('expectation', {}).get('expectation', 'killed') == 'killed'
        killed = not passed
        record['verdict'] = 'killed' if killed else 'survived'
        record['expectation_met'] = (killed == expected_killed)
        return record
    finally:
        if not keep:
            shutil.rmtree(work, ignore_errors=True)
        else:
            record['sandbox_kept'] = str(work)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--lane', default=str(DEFAULT_LANE))
    parser.add_argument('--revision', required=True)
    parser.add_argument('--tool', default='tools/check-storage-health.py')
    parser.add_argument('--catalogue', default=str(DEFAULT_CATALOGUE))
    parser.add_argument('--out', default=str(HERE / 'results.json'))
    parser.add_argument('--report', default=str(HERE / 'mutant-results.md'))
    parser.add_argument('--only', default=None, help='comma separated mutant ids')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--keep', action='store_true', help='keep the sandboxes')
    parser.add_argument('--baseline-only', action='store_true')
    args = parser.parse_args(argv)

    lane = Path(args.lane).resolve()
    catalogue_path = Path(args.catalogue).resolve()
    if not (lane / '.git').exists():
        print('lane is not a git repository: %s' % lane, file=sys.stderr)
        return 2
    if not catalogue_path.exists():
        print('catalogue missing: %s' % catalogue_path, file=sys.stderr)
        return 2
    catalogue = json.loads(read_text(catalogue_path))
    targets = catalogue.get('target_files', {})
    mutants = catalogue.get('mutants', [])
    if args.only:
        wanted = {x.strip() for x in args.only.split(',') if x.strip()}
        mutants = [m for m in mutants if m['id'] in wanted]

    before = lane_digests(lane, targets, catalogue_path)

    tmp_root = Path(tempfile.mkdtemp(prefix='sh-mutants-'))
    try:
        base_dir = Path(tempfile.mkdtemp(prefix='sh-baseline-', dir=str(tmp_root)))
        try:
            base_sha = build_sandbox(lane, args.revision, base_dir / 'repo')
        except Exception as exc:
            print('baseline sandbox failed: %s' % exc, file=sys.stderr)
            return 2
        base_sb = base_dir / 'repo'
        tool_path, _rel = resolve_tool(base_sb, lane, args.tool)
        if not tool_path.exists():
            print('detector script missing: %s' % tool_path, file=sys.stderr)
            return 2
        use_repo = detector_supports_repo(tool_path)
        exit_code, payload, out, err = run_detector(base_sb, base_sha, tool_path, use_repo)
        baseline = detector_state(exit_code, payload)
        baseline['stdout_head'] = out[:600]
        baseline['stderr_head'] = err[:300]
        baseline['revision_sha'] = base_sha
        baseline['detector'] = str(tool_path)
        baseline['uses_repo_flag'] = use_repo
        print('baseline: exit %s verified_rows %s status %s'
              % (baseline['exit'], baseline['verified_rows'], baseline['status']))
        if args.baseline_only:
            print(json.dumps(baseline, indent=1))
            return 0
        baseline_ok = (baseline['verified_rows'] == 6 and baseline['exit'] == 0
                       and payload is not None)
        if not baseline_ok:
            print('baseline is not (6, 0): every mutant is inconclusive', file=sys.stderr)

        results = []
        if baseline_ok:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
                futures = {pool.submit(run_mutant, m, lane, args.revision, args.tool,
                                       targets, use_repo, args.keep, tmp_root): m
                           for m in mutants}
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
        else:
            results = [{'id': m['id'], 'rule': m.get('rule'), 'file': m.get('file'),
                        'op': m.get('op'), 'expectation': m.get('expectation', {}),
                        'verdict': 'inconclusive',
                        'reason': 'baseline did not report verified_rows 6 with exit 0'}
                       for m in mutants]
        order = {m['id']: index for index, m in enumerate(mutants)}
        results.sort(key=lambda r: order.get(r['id'], 9999))
    finally:
        if not args.keep:
            shutil.rmtree(tmp_root, ignore_errors=True)

    after = lane_digests(lane, targets, catalogue_path)
    unchanged = before == after
    payload = {'schema': 'tsukuroi-storage-health-mutants-r26-results-v1',
               'lane': str(lane), 'revision': args.revision,
               'tool': args.tool, 'catalogue': str(catalogue_path),
               'baseline': baseline, 'lane_digests_unchanged': unchanged,
               'lane_digests_before': before, 'lane_digests_after': after,
               'results': results}
    write_text(Path(args.out), json.dumps(payload, indent=1, ensure_ascii=False) + '\n')

    killed = [r for r in results if r.get('verdict') == 'killed']
    survived = [r for r in results if r.get('verdict') == 'survived']
    inconclusive = [r for r in results if r.get('verdict') == 'inconclusive']
    mismatched = [r for r in results if r.get('expectation_met') is False]
    lines = ['# C1 storage-health mutation results', '',
             'revision `%s`, tool `%s`, detector `--repo` supported: %s'
             % (args.revision, args.tool, baseline.get('uses_repo_flag')),
             'baseline: exit %s, verified_rows %s, status %s'
             % (baseline['exit'], baseline['verified_rows'], baseline['status']),
             'lane digests unchanged: %s' % unchanged, '',
             'killed %d, survived %d, inconclusive %d, expectation mismatches %d'
             % (len(killed), len(survived), len(inconclusive), len(mismatched)), '',
             '| mutant | verdict | verified_rows | exit | expectation met | note |',
             '|---|---|---|---|---|---|']
    for record in results:
        detector = record.get('detector', {})
        lines.append('| %s | %s | %s | %s | %s | %s |' % (
            record['id'], record.get('verdict'),
            detector.get('verified_rows'), detector.get('exit'),
            record.get('expectation_met'), record.get('reason', '')))
    write_text(Path(args.report), '\n'.join(lines) + '\n')

    print('killed %d, survived %d, inconclusive %d, expectation mismatches %d'
          % (len(killed), len(survived), len(inconclusive), len(mismatched)))
    print('results: %s' % args.out)
    print('report:  %s' % args.report)
    if not unchanged:
        print('WARNING: a lane file digest changed during the run', file=sys.stderr)
        return 2
    return 1 if mismatched else 0


if __name__ == '__main__':
    sys.exit(main())
