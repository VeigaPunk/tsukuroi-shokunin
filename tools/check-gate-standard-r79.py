#!/usr/bin/env python3
"""operative registry legibility and gate-standard conformance, round 79.

Round-79 C2 (frozen by the round-79 declaration, before any repair exists).
Two legs over committed bytes:

DUPLICATE leg: a continuation table is non-operative only when the text between its
heading and its table header carries the literal token `NON-OPERATIVE`; every other
8-column registry table after the highest-numbered `## Gate and probe registry —
roundN superseding current rows` heading is current. No tool path may be named by
more than one current operative row; `duplicates` counts offending tools.

SHAPE leg: the two rows the round-78 non-author closure routed (frozen name list)
must be `gate` rows whose self-test cell names the tool's own `--selftest` command,
whose verdict map names code `3` for self-test failure, and whose tool blob at the
measured revision carries `--selftest` and a `SELFTEST` line.

Revision binding is the shared `tools/_revision.py` contract (QUALITY 28). Reads
only; writes nothing. --root is for isolated controls and selftests only.

Exit map: 0 both legs met; 1 a leg unmet or a finding; 2 could-not-evaluate
(usage or revision binding); 3 self-test failed.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _revision import RevisionError, bind, clean_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SKILL = 'SKILL.md'
HEADER = ('Name', 'Kind', 'Entry command', 'Verdict map', 'Self-test',
          'Pinned values', 'Write scope', 'Owner')
REGISTRY_HEADING = re.compile(r'^## Gate and probe registry — round([0-9]+) superseding current rows$')
ATX = re.compile(r'^(#{1,6})[ \t]+')
TOOL_PATH = re.compile(r'(?<![A-Za-z0-9_.-])tools/[A-Za-z0-9_./-]+')
FROZEN_ROWS = ('check-r71-routed-r72', 'count-md-rows-r72')
LABEL = 'zero duplicate current rows and two gate-standard rows'
NON_OPERATIVE = 'NON-OPERATIVE'


def cells_of(line):
    out, cell, escaped = [], [], False
    for char in line.strip():
        if char == '|' and not escaped:
            out.append(''.join(cell).strip())
            cell = []
        else:
            cell.append(char)
        escaped = (char == '\\' and not escaped)
    out.append(''.join(cell).strip())
    if out and out[0] == '':
        out.pop(0)
    if out and out[-1] == '':
        out.pop()
    return tuple(out)


def is_separator(cells):
    return (len(cells) == len(HEADER)
            and all(re.fullmatch(r':?-{3,}:?', cell) for cell in cells))


def normalized_header(cells):
    fixed = {'entry command': 'entry', 'self-test command': 'self-test'}
    return tuple(fixed.get(cell.lower(), cell.lower()) for cell in cells)


def is_header(cells):
    return normalized_header(cells) == normalized_header(HEADER)


def tables(text):
    """Yield (heading, non_operative, rows) per 8-column registry table."""
    lines = text.splitlines()
    headings = []
    for index, line in enumerate(lines):
        if line.startswith('#'):
            headings.append(index)
    current_heading = None
    last_heading_line = 0
    index = 0
    while index < len(lines):
        line = lines[index]
        if ATX.match(line):
            current_heading = line
            last_heading_line = index
            index += 1
            continue
        if is_header(cells_of(line)):
            block = '\n'.join(lines[last_heading_line:index])
            non_operative = NON_OPERATIVE in block
            rows = []
            offset = index + 2
            while offset < len(lines) and lines[offset].strip():
                row = cells_of(lines[offset])
                if len(row) == len(HEADER) and not is_separator(row):
                    rows.append(row)
                offset += 1
            yield current_heading, non_operative, rows
            index = offset
            continue
        index += 1


def current_rows(skill_text):
    lines = skill_text.splitlines()
    numbered = []
    for index, line in enumerate(lines):
        match = REGISTRY_HEADING.fullmatch(line)
        if match:
            numbered.append((int(match.group(1)), index))
    if not numbered:
        raise ValueError('no-operative-heading')
    highest = max(number for number, _ in numbered)
    selected = [index for number, index in numbered if number == highest]
    if len(selected) != 1:
        raise ValueError('duplicate-operative-heading')
    operative_start = selected[0]
    for heading, non_operative, rows in tables(skill_text):
        if heading is None:
            continue
        heading_line = lines.index(heading)
        is_operative = (heading_line == operative_start)
        if is_operative or heading_line > operative_start:
            yield {'heading': heading, 'rows': rows, 'non_operative': non_operative,
                   'operative': is_operative}


def analyze(skill_text, tool_text):
    duplicates, findings = 0, []
    current = []
    for table in current_rows(skill_text):
        if table['operative'] or (table['heading'] and table['heading'] == table['heading']):
            # only tables at/after the operative heading are yielded
            current.append(table)
    operative = [table for table in current if table['operative']]
    if len(operative) != 1:
        raise ValueError('operative-table-count')
    counted = []
    for table in current:
        if table['operative'] or not table['non_operative']:
            for row in table['rows']:
                counted.append(row)
    seen = {}
    for row in counted:
        for path in set(TOOL_PATH.findall(row[2] + ' ' + row[4])):
            seen.setdefault(path, 0)
            seen[path] += 1
    for path, count in sorted(seen.items()):
        if count > 1:
            duplicates += 1
            findings.append(('REGISTRY-CURRENT-DUPLICATE', path, f'{count} current rows'))
    shape = 0
    for name in FROZEN_ROWS:
        matches = [row for row in counted if row[0] == name]
        if len(matches) != 1:
            findings.append(('GATE-STANDARD-ROW', name, f'{len(matches)} current rows'))
            continue
        row = matches[0]
        kind, verdict, selftest = row[1], row[3], row[4]
        source = tool_text.get(TOOL_PATH.findall(row[2])[0]) if TOOL_PATH.findall(row[2]) else None
        ok = (kind == 'gate' and '--selftest' in selftest and row[0] in selftest
              and '3' in re.findall(r'(?<![0-9])[0-9](?![0-9])', verdict)
              and 'self-test' in verdict.lower()
              and source is not None and '--selftest' in source and 'SELFTEST' in source)
        if ok:
            shape += 1
        else:
            findings.append(('GATE-STANDARD-SHAPE', name,
                             'kind/selftest/verdict/source clause unmet'))
    return duplicates, shape, findings


def run_selftest():
    cases = []

    def build(rows, tables_mark, tools):
        skill = ['# fixture']
        skill.append('## Gate and probe registry — round71 superseding current rows')
        skill.append('| ' + ' | '.join(HEADER) + ' |')
        skill.append('|' + '---|' * len(HEADER))
        for row in rows:
            skill.append('| ' + ' | '.join(row) + ' |')
        skill.append('')
        for heading, marked, extra in tables_mark:
            skill.append(heading)
            if marked:
                skill.append('> NON-OPERATIVE — carried for history; the round-71 table is the sole operative registry.')
            skill.append('| ' + ' | '.join(HEADER) + ' |')
            skill.append('|' + '---|' * len(HEADER))
            for row in extra:
                skill.append('| ' + ' | '.join(row) + ' |')
            skill.append('')
        return '\n'.join(skill), tools

    good_gate = ('check-r71-routed-r72', 'gate',
                 '`python3 tools/check-r71-routed-r72.py --revision <REV>`',
                 '0 clean; 1 stale; 2 could-not-evaluate; 3 self-test failed',
                 '`python3 tools/check-r71-routed-r72.py --selftest`',
                 'p', 'reads', 'tsukuroi')
    good_md = ('count-md-rows-r72', 'gate',
               '`python3 tools/count-md-rows-r72.py --revision <REV>`',
               '0 met; 1 missed; 2 could-not-evaluate; 3 self-test failed',
               '`python3 tools/count-md-rows-r72.py --selftest`',
               'p', 'reads', 'tsukuroi')
    repeat_gate = ('check-r71-routed-r72', 'gate',
                   '`python3 tools/check-r71-routed-r72.py --revision <REV>`',
                   '0 clean; 1 stale; 2 could-not-evaluate; 3 self-test failed',
                   '`python3 tools/check-r71-routed-r72.py --selftest`',
                   'p', 'reads', 'tsukuroi')
    late_gate = ('measure-unit-deps-r79', 'gate',
                 '`python3 tools/measure-unit-deps-r79.py --revision <REV>`',
                 '0 met; 1 missed; 2 could-not-evaluate; 3 self-test failed',
                 '`python3 tools/measure-unit-deps-r79.py --selftest`',
                 'p', 'reads', 'tsukuroi')
    tools = {'tools/check-r71-routed-r72.py': 'def selftest(): print("SELFTEST")\n--selftest',
             'tools/count-md-rows-r72.py': 'def selftest(): print("SELFTEST")\n--selftest',
             'tools/measure-unit-deps-r79.py': 'print("SELFTEST"); --selftest'}
    base_rows = [good_gate, good_md, late_gate]
    continuation = [('## Round 72 — continuation', True, [late_gate])]
    checks = []

    def evaluate(fixture, want_dup, want_shape):
        skill, tool_text = fixture
        try:
            dup, shape, findings = analyze(skill, tool_text)
        except ValueError as exc:
            return None, None, [('CANNOT', str(exc))]
        return dup, shape, findings

    def check(name, fixture, want_dup, want_shape, want_finding):
        dup, shape, findings = evaluate(fixture, want_dup, want_shape)
        ids = [f[0] for f in findings]
        hit = (not ids) if want_finding == 'none' else (want_finding in ids)
        passed = dup == want_dup and shape == want_shape and hit
        checks.append(passed)
        print(f'SELFTEST {name} duplicates={dup} shape={shape} findings={",".join(ids) or "none"} '
              f'{"PASS" if passed else "FAIL"}')

    check('control', build(base_rows, continuation, tools), 0, 2, 'none')
    marked = [('## Round 72 — continuation', False, [late_gate])]
    check('unmarked-continuation-duplicate', build(base_rows, marked, tools), 1, 2,
          'REGISTRY-CURRENT-DUPLICATE')
    marked2 = [('## Round 72 — continuation', True, [late_gate])]
    check('marked-continuation', build(base_rows, marked2, tools), 0, 2, 'none')
    no_selftest = list(good_gate); no_selftest[4] = 'none: no self-test mode'
    check('gate-without-selftest', build([tuple(no_selftest), good_md], continuation, tools), 0, 1,
          'GATE-STANDARD-SHAPE')
    bad_map = list(good_md); bad_map[3] = '0 met; 1 missed; 2 could-not-evaluate'
    check('verdict-without-code3', build([good_gate, tuple(bad_map)], continuation, tools), 0, 1,
          'GATE-STANDARD-SHAPE')
    bad_source = dict(tools); bad_source['tools/count-md-rows-r72.py'] = 'def main(): pass\n'
    check('tool-without-selftest', build([good_gate, good_md], continuation, bad_source), 0, 1,
          'GATE-STANDARD-SHAPE')
    seven = list(good_gate)
    check('missing-row', build([tuple(seven)], continuation, tools), 0, 1, 'GATE-STANDARD-ROW')
    skill_two, tool_two = build([good_gate, good_md], continuation, tools)
    skill_two += '\n## Gate and probe registry — round72 superseding current rows\n'
    check('duplicate-operative-heading', (skill_two, tool_two), None, None, 'CANNOT')
    print(f'SELFTEST total={len(checks)} passed={sum(checks)} failed={checks.count(False)}')
    return 0 if all(checks) else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--revision')
    group.add_argument('--root', type=Path)
    group.add_argument('--selftest', action='store_true')
    ap.add_argument('--branch', default='master')
    args = ap.parse_args()
    if args.selftest:
        return run_selftest()
    if args.root:
        root = args.root
        skill = (root / SKILL).read_text(encoding='utf-8', errors='replace')
        tools = {}
        for name in FROZEN_ROWS:
            path = f'tools/{name}.py'
            tools[path] = ((root / path).read_text(encoding='utf-8', errors='replace')
                           if (root / path).is_file() else '')
        binding = None
    else:
        try:
            binding = bind(ROOT, args.revision, args.branch)
        except RevisionError as exc:
            print(f'GATE_STANDARD_BINDING {exc.fid} {exc.site}: {exc.detail}')
            return 2
        sha = binding.sha

        def read(path):
            proc = subprocess.run(['git', '--no-pager', '-C', str(ROOT), 'show', f'{sha}:{path}'],
                                  stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=clean_env(), timeout=60)
            if proc.returncode:
                raise ValueError('missing-blob')
            return proc.stdout.decode('utf-8', 'replace')
        skill = read(SKILL)
        tools = {f'tools/{name}.py': read(f'tools/{name}.py') for name in FROZEN_ROWS}
    try:
        duplicates, shape, findings = analyze(skill, tools)
    except ValueError as exc:
        print(f'GATE_STANDARD CANNOT_EVALUATE reason={exc}')
        return 2
    for fid, site, detail in findings:
        print(f'{fid} {site}: {detail}')
    ok = duplicates == 0 and shape == len(FROZEN_ROWS)
    bind_field = '' if binding is None else f' revision={binding.sha} branch={binding.branch}'
    print(f'GATE_STANDARD predicate="{LABEL}" duplicates={duplicates} '
          f'shape_ok={shape}/{len(FROZEN_ROWS)} met={int(ok)}{bind_field}')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
