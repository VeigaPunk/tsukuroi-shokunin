#!/usr/bin/env python3
"""Should-fail data battery for tools/check-kernel-taint.py (round 28, claim C2). Every subprocess follows the round-30 git child environment contract: inherited GIT_* and user configuration are isolated, HOME is private, PATH is fixed, and repository discovery is sandbox-ceilinged.

Origin: round-27 wave-2 seat CritC1Tool's harness
(`.ufo/waves/round-27/w2a2/CritC1Tool/mutants.py`); the mutate functions are carried unchanged.
Made reproducible from committed bytes: the lane data is `git archive <--base>` into a private
temporary scratch repo (never the lane), and the counter is the blob
`<--counter-rev>:tools/check-kernel-taint.py` (or `--counter-file` for mutation testing).

The claim's should-fail set is DECLARED (SCORECARD round-28 declaration): generic_word_quote,
generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate,
gate_source_from_location_cell.  A mutant is ACCEPTED when the counter exits 0 with
verified_rows 6.  Every mutant line is printed; the last stdout line (JSON) carries
`should_fail_total`, `should_fail_accepted`, `control_verified_rows`, and, for information,
`other_accepted` (accepted mutants outside the declared set).

Usage: python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> | --counter-file <PATH>) [--lane <repo>]
"""
import argparse
import atexit
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'LD_', 'PYTHON'))}
    env.update({
        'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull,
        'HOME': str(HOME), 'XDG_CONFIG_HOME': str(HOME / '.config'),
        'PATH': '/usr/bin:/bin', 'GIT_CEILING_DIRECTORIES': str(SEAT.parent),
    })
    return env

_ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
_ap.add_argument('--base', required=True)
_g = _ap.add_mutually_exclusive_group(required=True)
_g.add_argument('--counter-rev')
_g.add_argument('--counter-file')
_ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ap.add_argument('--keep', action='store_true')
ARGS = _ap.parse_args()

SEAT = Path(tempfile.mkdtemp(prefix='mut-kt-'))
HOME = SEAT / 'home'
HOME.mkdir()
if not ARGS.keep:
    atexit.register(shutil.rmtree, str(SEAT), True)
TREE = SEAT / 'tree'
REPO = SEAT / 'repo'
TOOL = SEAT / 'counter' / 'check-kernel-taint.py'
DECLARED = ('generic_word_quote', 'generic_word_quote_the', 'quote_from_uncited_rejected_source',
            'gate_heading_investigate', 'gate_source_from_location_cell')


def _export():
    rev = subprocess.run(['git', '-C', ARGS.lane, 'rev-parse', '--verify', ARGS.base + '^{commit}'],
                         capture_output=True, text=True, check=True, env=clean_env()).stdout.strip()
    tar = subprocess.run(['git', '-C', ARGS.lane, 'archive', rev],
                         capture_output=True, check=True, env=clean_env()).stdout
    TREE.mkdir()
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(str(TREE), filter='data')
    if ARGS.counter_file:
        blob = Path(ARGS.counter_file).read_bytes()
    else:
        blob = subprocess.run(['git', '-C', ARGS.lane, 'show', ARGS.counter_rev + ':tools/check-kernel-taint.py'],
                              capture_output=True, check=True, env=clean_env()).stdout
    TOOL.parent.mkdir()
    TOOL.write_bytes(blob)
    # the counter imports its sibling helper module(s) from its own directory
    for helper in (TREE / 'tools').glob('_*.py'):
        shutil.copy(str(helper), str(TOOL.parent / helper.name))
    return rev, hashlib.sha256(blob).hexdigest()


BASE_REV, COUNTER_SHA = _export()
ENTRY = 'corpus/knowledge/kernel-taint-r27.json'
LESSON = 'corpus/lessons/round-27.md'
SKILL = 'SKILL.md'
SOURCES = 'corpus/SOURCES.md'


def git(*args, check=True):
    return subprocess.run(['git', '-C', str(REPO), '-c', 'user.name=CritC1Tool',
                           '-c', 'user.email=seat@invalid', *args], check=check,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=clean_env())


def setup():
    if REPO.exists():
        shutil.rmtree(REPO)
    shutil.copytree(TREE, REPO)
    git('init', '-q', '-b', 'master')
    git('config', 'user.email', 'seat@invalid')
    git('config', 'user.name', 'CritC1Tool')
    git('add', '-A')
    git('commit', '-q', '-m', 'base export ' + BASE_REV)


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
                               '--branch', 'm-' + name], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, env=clean_env())
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
    results = {}
    for fn in MUTANTS:
        name = fn.__name__[2:]
        try:
            results[name] = run(name, fn)
        except Exception as exc:
            git('checkout', '-q', '-f', 'master', check=False)
            results[name] = {'mutant': name, 'harness_error': repr(exc)[:300]}
            print(json.dumps(results[name]))

    def accepted(r):
        return r.get('exit') == 0 and r.get('verified_rows') == 6
    declared = [results.get(n, {'harness_error': 'missing'}) for n in DECLARED]
    print(json.dumps({
        'summary': 'mutants-kernel-taint', 'base': BASE_REV, 'counter_rev': ARGS.counter_rev,
        'counter_sha256': COUNTER_SHA,
        'control_exit': results['baseline'].get('exit'),
        'control_verified_rows': results['baseline'].get('verified_rows'),
        'should_fail_total': len(DECLARED),
        'should_fail_accepted': sum(accepted(r) for r in declared),
        'accepted_mutants': [n for n in DECLARED if accepted(results.get(n, {}))],
        'harness_errors': [n for n, r in results.items() if 'harness_error' in r],
        'other_accepted': [n for n, r in results.items()
                           if n not in DECLARED and n != 'baseline' and accepted(r)],
    }))
