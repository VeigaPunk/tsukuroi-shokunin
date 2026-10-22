#!/usr/bin/env python3
"""Data mutants for tools/check-kernel-taint.py on a scratch git repo (never the lane)."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

SEAT = Path('/fast/scratch/hyaku/tsuku27a2/CritC1Tool')
TREE = SEAT / 'tree'
REPO = SEAT / 'repo'
TOOL = TREE / 'tools/check-kernel-taint.py'
ENTRY = 'corpus/knowledge/kernel-taint-r27.json'
LESSON = 'corpus/lessons/round-27.md'
SKILL = 'SKILL.md'
SOURCES = 'corpus/SOURCES.md'


def git(*args, check=True):
    return subprocess.run(['git', '-C', str(REPO), *args], check=check,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def setup():
    if REPO.exists():
        shutil.rmtree(REPO)
    shutil.copytree(TREE, REPO)
    git('init', '-q', '-b', 'master')
    git('config', 'user.email', 'seat@invalid')
    git('config', 'user.name', 'CritC1Tool')
    git('add', '-A')
    git('commit', '-q', '-m', 'base 099c7b3f export')


def rd(path):
    return (REPO / path).read_text()


def wr(path, text):
    (REPO / path).write_text(text)


def entry():
    return json.loads(rd(ENTRY))


def put_entry(e):
    wr(ENTRY, json.dumps(e, indent=1, ensure_ascii=False) + '\n')


def row(e, rid):
    return next(r for r in e['rows'] if r['id'] == rid)


def replace_once(path, old, new):
    text = rd(path)
    assert text.count(old) == 1, (path, old, text.count(old))
    wr(path, text.replace(old, new))


def gate_line_for(quote):
    lines = [l for l in rd(LESSON).splitlines() if l.startswith('| S') and ('| %s |' % quote in l or '| `%s` |' % quote in l)]
    assert len(lines) == 1, (quote, lines)
    return lines[0]


def run(name, mutate):
    git('checkout', '-q', 'master')
    git('checkout', '-q', '-b', 'm-' + name)
    mutate()
    git('add', '-A')
    git('commit', '-q', '--allow-empty', '-m', name)
    sha = git('rev-parse', 'HEAD').stdout.strip()
    proc = subprocess.run([sys.executable, str(TOOL), '--repo', str(REPO), '--revision', sha,
                           '--branch', 'm-' + name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    git('checkout', '-q', 'master')
    try:
        out = json.loads(proc.stdout)
        blocking = sorted({f['id'] for f in out.get('findings', []) if f.get('blocking', True)})
        advisory = sorted({f['id'] for f in out.get('findings', []) if not f.get('blocking', True)})
        res = {'mutant': name, 'exit': proc.returncode, 'verified_rows': out.get('verified_rows'),
               'blocking': blocking, 'advisory': advisory}
    except ValueError:
        res = {'mutant': name, 'exit': proc.returncode, 'verified_rows': None,
               'stdout': proc.stdout[:200], 'stderr_tail': proc.stderr.strip().splitlines()[-1:] }
    print(json.dumps(res))
    return res


# ------------------------------------------------------------------ mutants

def m_baseline():
    pass


def m_generic_word_quote():
    # KT6's only quote becomes the single word "kernel" (in the S140 snapshot); Gate cell to match.
    e = entry()
    old = row(e, 'KT6')['quotes'][0]['text']
    row(e, 'KT6')['quotes'] = [{'source': 'S140', 'text': 'kernel'}]
    put_entry(e)
    line = gate_line_for(old)
    replace_once(LESSON, line, line.replace('| %s |' % old, '| kernel |'))


def m_generic_word_quote_the():
    e = entry()
    old = row(e, 'KT5')['quotes'][0]['text']
    row(e, 'KT5')['quotes'] = [{'source': 'S140', 'text': 'the'}]
    put_entry(e)
    line = gate_line_for(old)
    replace_once(LESSON, line, line.replace('| %s |' % old, '| the |'))


def m_irrelevant_capture_pointer():
    # KT6 (bug-report reading) points only at the capture timestamp line.
    e = entry()
    row(e, 'KT6')['capture_pointers'] = [{'line': 3, 'token': '2026'}]
    put_entry(e)


def m_whitespace_token_pointer():
    # KT1 points at line 136 with a token of three spaces.
    e = entry()
    row(e, 'KT1')['capture_pointers'] = [{'line': 136, 'token': '   '}]
    put_entry(e)


def m_skill_row_id_only():
    text = rd(SKILL)
    old = [l for l in text.splitlines() if l.startswith('| KT3 |')]
    assert len(old) == 1
    replace_once(SKILL, old[0], '| KT3 |')


def m_skill_row_id_withdrawn_text():
    text = rd(SKILL)
    old = [l for l in text.splitlines() if l.startswith('| KT3 |')]
    replace_once(SKILL, old[0], '| KT3 | withdrawn | withdrawn | withdrawn | withdrawn |')


def m_skill_heading_withdrawn():
    replace_once(SKILL, '## Kernel taint — round 27\n', '## Kernel taint — round 27 (withdrawn, do not use)\n')


def m_gate_cell_two_quotes():
    # Merge the two S142 Gate rows of KT1 into one cell with two quotes separated by "; ".
    a = gate_line_for('#define TAINT_OOT_MODULE 12')
    b = gate_line_for('#define TAINT_UNSIGNED_MODULE 13')
    merged = a.replace('| #define TAINT_OOT_MODULE 12 |',
                       '| "#define TAINT_OOT_MODULE 12"; "#define TAINT_UNSIGNED_MODULE 13" |')
    replace_once(LESSON, a + '\n' + b + '\n', merged + '\n')


def m_gate_cell_two_quotes_extra_row():
    # Same, but the S140 KT1 Gate row also gains a second quote in its cell (KT1 has an S140 quote).
    old = 'If that returns ``0``, the kernel is not tainted; any other number indicates the reasons why it is.'
    line = gate_line_for(old)
    replace_once(LESSON, line, line.replace('| %s |' % old,
                 '| "%s"; "Note the kernel will remain tainted even after you undo what caused the taint" |' % old))


def m_withdrawn_row_field():
    e = entry()
    r = row(e, 'KT2')
    r['status'] = 'withdrawn'
    r['withdrawn'] = True
    r['withdrawn_by'] = 'round 27 wave 2 mutant: the statement is false'
    put_entry(e)


def m_withdrawn_row_corrections_marker():
    # The lane's own withdrawal convention (storage-health-r26.json corrections_r27).
    e = entry()
    e['corrections_r27'] = [{'row': 'KT2', 'field': 'statement',
                             'withdrawn_text': row(e, 'KT2')['statement'][:60],
                             'status': 'withdrawn in round 27', 'corrected_by': 'mutant',
                             'marked_by': 'mutant'}]
    put_entry(e)


def m_withdrawn_row_verdict_and_md():
    e = entry()
    row(e, 'KT2')['verdict'] = 'UNVERIFIED'
    row(e, 'KT2')['statement'] = 'WITHDRAWN: this row is withdrawn and makes no claim.'
    row(e, 'KT2')['action'] = 'none (withdrawn)'
    put_entry(e)


def m_one_good_one_bad_quote():
    # Declared rule: "at least one quote" passes; add a second quote absent from snapshot and Gate.
    e = entry()
    row(e, 'KT6')['quotes'].append({'source': 'S140', 'text': 'this sentence is in no snapshot'})
    put_entry(e)


def m_one_good_one_bad_pointer():
    # Declared rule: "at least one capture pointer" passes; add a second pointer on a header line.
    e = entry()
    row(e, 'KT6')['capture_pointers'].append({'line': 1, 'token': 'time'})
    put_entry(e)


def m_quote_from_uncited_rejected_source():
    # KT6's quote comes from S146, a SOURCES row that is rejected, tier C, opened 2019, used-by another
    # entry, and not listed in KT6's sources; KT6 still lists only S140.
    body = 'an unrelated page\nthe oops reader ignores every taint flag\n'
    snap = REPO / '.ufo/waves/round-27/sources/S146.txt'
    snap.write_text(body)
    digest = hashlib.sha256(body.encode()).hexdigest()
    text = rd(SOURCES)
    s145 = [l for l in text.splitlines() if l.startswith('| S145 |')][0]
    n = len(s145.strip().strip('|').split('|'))
    header = [l for l in text.splitlines() if l.lower().startswith('| id |')][0]
    names = [c.strip().lower() for c in header.strip().strip('|').split('|')]
    cells = ['x'] * n
    vals = {'id': 'S146', 'source': 'https://example.invalid/S146', 'kind': 'blog', 'tier': 'C',
            'anchor': 'sha256 ' + digest, 'status': 'rejected', 'opened': '2019-01-01',
            'used-by': 'corpus/knowledge/other.md'}
    for k, v in vals.items():
        if k in names:
            cells[names.index(k)] = v
    replace_once(SOURCES, s145 + '\n', s145 + '\n| ' + ' | '.join(cells) + ' |\n')
    q = 'the oops reader ignores every taint flag'
    e = entry()
    old = row(e, 'KT6')['quotes'][0]['text']
    row(e, 'KT6')['quotes'] = [{'source': 'S146', 'text': q}]
    put_entry(e)
    line = gate_line_for(old)
    replace_once(LESSON, line, '| S146 | https://example.invalid/S146 | 2026-10-22 | %s | S146.txt line 2 |' % q)


def m_gate_heading_investigate():
    # The `## Gate` heading becomes `## Things to investigate` (substring "gate").
    replace_once(LESSON, '\n## Gate\n', '\n## Things to investigate\n')


def m_gate_source_from_location_cell():
    # KT6's Gate row loses its Source id; the only S### on the line is in the Location cell.
    old = "That's why bug reports from tainted kernels will often be ignored by developers, hence try to reproduce problems with an untainted kernel."
    line = gate_line_for(old)
    new = line.replace('| S140 |', '| (none) |', 1).replace('entry row KT6 |', 'entry row KT6, compare S140 |')
    replace_once(LESSON, line, new)


def m_unhashable_row_id():
    e = entry()
    row(e, 'KT1')['id'] = ['KT1']
    put_entry(e)


def m_unhashable_source_item():
    e = entry()
    row(e, 'KT1')['sources'] = [['S140']] + row(e, 'KT1')['sources']
    put_entry(e)


PIPE_QUOTE = 'if (!capable(CAP_SYS_MODULE) || modules_disabled)'


def pipe_mutant(cell):
    def mutate():
        e = entry()
        quotes = row(e, 'KT4')['quotes']
        old = quotes[1]['text']
        quotes[1] = {'source': 'S143', 'text': PIPE_QUOTE}
        put_entry(e)
        line = gate_line_for(old)
        replace_once(LESSON, line, line.replace('| %s |' % old, '| %s |' % cell))
    return mutate


m_pipe_quote_escaped = pipe_mutant(PIPE_QUOTE.replace('|', '\\|'))
m_pipe_quote_backticked_escaped = pipe_mutant('`%s`' % PIPE_QUOTE.replace('|', '\\|'))
m_pipe_quote_backticked_raw = pipe_mutant('`%s`' % PIPE_QUOTE)
m_pipe_quote_escaped.__name__ = 'm_pipe_quote_escaped'
m_pipe_quote_backticked_escaped.__name__ = 'm_pipe_quote_backticked_escaped'
m_pipe_quote_backticked_raw.__name__ = 'm_pipe_quote_backticked_raw'


def m_pipe_quote_control_no_pipe():
    # Control: same row shape with a pipe-free S143 line (snapshot line 709 minus nothing).
    pipe_mutant('if (len == 0')()
    e = entry()
    row(e, 'KT4')['quotes'][1]['text'] = 'if (len == 0'
    put_entry(e)


MUTANTS_EXTRA = [m_pipe_quote_escaped, m_pipe_quote_backticked_escaped, m_pipe_quote_backticked_raw,
                 m_pipe_quote_control_no_pipe]

MUTANTS = [m_baseline, m_generic_word_quote, m_generic_word_quote_the, m_irrelevant_capture_pointer,
           m_whitespace_token_pointer, m_skill_row_id_only, m_skill_row_id_withdrawn_text,
           m_skill_heading_withdrawn, m_gate_cell_two_quotes, m_gate_cell_two_quotes_extra_row,
           m_withdrawn_row_field, m_withdrawn_row_corrections_marker, m_withdrawn_row_verdict_and_md,
           m_one_good_one_bad_quote, m_one_good_one_bad_pointer, m_quote_from_uncited_rejected_source,
           m_gate_heading_investigate, m_gate_source_from_location_cell, m_unhashable_row_id,
           m_unhashable_source_item] + MUTANTS_EXTRA

if __name__ == '__main__':
    setup()
    for fn in MUTANTS:
        try:
            run(fn.__name__[2:], fn)
        except Exception as exc:
            git('checkout', '-q', '-f', 'master', check=False)
            print(json.dumps({'mutant': fn.__name__[2:], 'harness_error': repr(exc)[:300]}))
